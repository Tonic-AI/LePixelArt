#!/usr/bin/env python3
"""
Record mode with live teleoperation (non-blocking)
Mirror positions while recording frames on ENTER press
"""

import sys
import time
import json
import os
import threading
import select
from st3215 import ST3215

class TeleopRecorder:
    def __init__(self, source_port="/dev/ttyACM0", target_port="/dev/ttyACM1"):
        self.source_port = source_port
        self.target_port = target_port
        self.source_servo = None
        self.target_servo = None
        self.servo_mapping = []
        self.sequences_dir = "sequences"

        # Recording state
        self.recording = False
        self.frames = []
        self.should_capture = False
        self.should_stop = False

        # Soft limits
        self.soft_limits = {}
        self.load_soft_limits()

        # Create sequences directory
        if not os.path.exists(self.sequences_dir):
            os.makedirs(self.sequences_dir)

    def load_soft_limits(self):
        """Load soft limits from calibration file"""
        config_file = "claw_limits.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    servo_id = data['servo_id']
                    self.soft_limits[servo_id] = {
                        'min': data['min_position'],
                        'max': data['max_position']
                    }
                    print(f"✓ Loaded soft limits for servo {servo_id}: [{data['min_position']}, {data['max_position']}]")
            except Exception as e:
                print(f"⚠️  Failed to load soft limits: {e}")
        else:
            print(f"ℹ️  No soft limits file found ({config_file})")

    def apply_soft_limits(self, servo_id, position):
        """Apply soft limits to a position"""
        if servo_id in self.soft_limits:
            limits = self.soft_limits[servo_id]
            original_pos = position
            position = max(limits['min'], min(limits['max'], position))
            if position != original_pos:
                print(f"\n⚠️  Servo {servo_id}: Position {original_pos} clamped to {position}")
            return position
        return position

    def connect_and_scan(self):
        """Connect to both ports and scan servos"""
        print(f"Connecting to {self.source_port}...")
        self.source_servo = ST3215(self.source_port)
        print(f"✓ Connected to {self.source_port}")

        print(f"Connecting to {self.target_port}...")
        self.target_servo = ST3215(self.target_port)
        print(f"✓ Connected to {self.target_port}")

        print(f"\nScanning servos on {self.source_port}...")
        source_servos = self.source_servo.ListServos()
        print(f"✓ Found servos: {source_servos}")

        print(f"\nScanning servos on {self.target_port}...")
        target_servos = self.target_servo.ListServos()
        print(f"✓ Found servos: {target_servos}")

        if not source_servos or not target_servos:
            raise ValueError("No servos found on one or both ports")

        # Map servos
        common_servos = sorted(set(source_servos) & set(target_servos))
        if common_servos:
            self.servo_mapping = [(sid, sid) for sid in common_servos]
        else:
            self.servo_mapping = list(zip(source_servos, target_servos))

        print(f"\nServo mapping: {self.servo_mapping}")

        # Enable target servos
        print("\nEnabling target servos...")
        for _, target_id in self.servo_mapping:
            self.target_servo.StartServo(target_id)
        print("✓ All target servos enabled")

    def input_thread(self):
        """Non-blocking input thread"""
        print("\n=== Recording Mode with Live Teleoperation ===")
        print("- Move servos on ACM0, they will mirror on ACM1")
        print("- Press ENTER to capture current frame")
        print("- Type 'done' and press ENTER to finish\n")

        while not self.should_stop:
            # Use select to check if input is available (non-blocking on Linux)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline().strip().lower()

                if line == 'done':
                    self.should_stop = True
                    print("\n✓ Stopping recording...")
                    break
                else:
                    # Empty line (ENTER pressed)
                    self.should_capture = True

            time.sleep(0.05)

    def mirror_and_record(self):
        """Main loop: mirror positions and capture frames on demand"""
        last_positions = {}
        frame_count = 0

        while not self.should_stop:
            status_parts = []

            # Read all positions
            current_positions = {}

            for source_id, target_id in self.servo_mapping:
                position = self.source_servo.ReadPosition(source_id)

                if position is None:
                    status_parts.append(f"S{source_id}:ERR")
                    continue

                current_positions[source_id] = position

                # Only send if position changed significantly
                if source_id in last_positions:
                    if abs(position - last_positions[source_id]) < 5:
                        status_parts.append(f"S{source_id}:{position}")
                        continue

                last_positions[source_id] = position

                # Apply soft limits for target servo
                constrained_position = self.apply_soft_limits(target_id, position)

                # Mirror to target
                result = self.target_servo.MoveTo(target_id, constrained_position, speed=3400, acc=200, wait=False)

                if result:
                    if constrained_position != position:
                        status_parts.append(f"S{source_id}:{position}→{constrained_position}✓")
                    else:
                        status_parts.append(f"S{source_id}:{position}✓")
                else:
                    status_parts.append(f"S{source_id}:{position}✗")

            # Check if we should capture a frame
            if self.should_capture:
                self.frames.append(current_positions.copy())
                frame_count += 1
                print(f"\n✓ Frame {frame_count} captured: {current_positions}")
                print("Press ENTER for next frame, or type 'done' to finish...")
                self.should_capture = False

            # Print status
            status_line = " | ".join(status_parts)
            if not self.should_capture:  # Don't overwrite capture message
                print(f"\r{status_line}                              ", end='', flush=True)

            time.sleep(0.05)

    def save_sequence(self):
        """Save recorded sequence to file"""
        if not self.frames:
            print("\n⚠️  No frames recorded")
            return

        print(f"\n✓ Recorded {len(self.frames)} frames")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = input(f"Enter filename (default: sequence_{timestamp}.json): ").strip()

        if not filename:
            filename = f"sequence_{timestamp}.json"
        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.sequences_dir, filename)

        data = {
            "timestamp": timestamp,
            "servo_mapping": self.servo_mapping,
            "frames": self.frames,
            "frame_count": len(self.frames)
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Sequence saved to {filepath}")

    def cleanup(self):
        """Disable target servos"""
        print("\nDisabling target servos...")
        for _, target_id in self.servo_mapping:
            self.target_servo.StopServo(target_id)
        print("✓ Done")

    def run(self):
        """Main execution"""
        try:
            self.connect_and_scan()

            # Start input thread
            input_thread = threading.Thread(target=self.input_thread, daemon=True)
            input_thread.start()

            # Run mirror and record loop
            self.mirror_and_record()

            # Save sequence
            self.save_sequence()

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            self.should_stop = True

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

        finally:
            self.cleanup()


def main():
    print("=== Teleop Recording ===")
    recorder = TeleopRecorder()
    recorder.run()

if __name__ == "__main__":
    main()
