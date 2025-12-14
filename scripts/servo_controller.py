#!/usr/bin/env python3
"""
ST3215 Servo Controller with Recording and Playback
- Mirror mode: Replicate positions from ACM0 to ACM1
- Record mode: Record position sequences
- Playback mode: Replay sequences with interpolation
"""

import sys
import time
import json
import os
import threading
import select
from st3215 import ST3215

class ServoController:
    def __init__(self, source_port="/dev/ttyACM0", target_port="/dev/ttyACM1"):
        self.source_port = source_port
        self.target_port = target_port
        self.source_servo = None
        self.target_servo = None
        self.servo_mapping = []
        self.sequences_dir = "sequences"

        # Soft limits
        self.soft_limits = {}
        self.load_soft_limits()

        # Create sequences directory if it doesn't exist
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

    def connect(self):
        """Connect to both serial ports"""
        print(f"\nConnecting to {self.source_port}...")
        self.source_servo = ST3215(self.source_port)
        print(f"✓ Connected to {self.source_port}")

        print(f"\nConnecting to {self.target_port}...")
        self.target_servo = ST3215(self.target_port)
        print(f"✓ Connected to {self.target_port}")

    def scan_servos(self):
        """Scan and map servos on both ports"""
        print(f"\nScanning for servos on {self.source_port}...")
        source_servos = self.source_servo.ListServos()
        print(f"✓ Found servos on {self.source_port}: {source_servos}")

        print(f"\nScanning for servos on {self.target_port}...")
        target_servos = self.target_servo.ListServos()
        print(f"✓ Found servos on {self.target_port}: {target_servos}")

        if not source_servos:
            raise ValueError(f"No servos found on {self.source_port}!")

        if not target_servos:
            raise ValueError(f"No servos found on {self.target_port}!")

        # Find common servo IDs
        common_servos = sorted(set(source_servos) & set(target_servos))
        if common_servos:
            print(f"\n✓ Common servo IDs: {common_servos}")
            self.servo_mapping = [(sid, sid) for sid in common_servos]
        else:
            print(f"\n⚠️  No matching servo IDs. Mapping by order...")
            self.servo_mapping = list(zip(source_servos, target_servos))

        print(f"Servo mapping: {self.servo_mapping}")
        return self.servo_mapping

    def enable_target_servos(self):
        """Enable torque on target servos"""
        print("\nEnabling torque on target servos...")
        for _, target_id in self.servo_mapping:
            result = self.target_servo.StartServo(target_id)
            if not result:
                print(f"❌ Failed to start servo {target_id}")
            else:
                print(f"✓ Servo {target_id} enabled")

    def disable_target_servos(self):
        """Disable torque on target servos"""
        print("\nDisabling torque on target servos...")
        for _, target_id in self.servo_mapping:
            self.target_servo.StopServo(target_id)
        print("✓ Target servos stopped")

    def read_positions(self):
        """Read current positions from source servos"""
        positions = {}
        for source_id, _ in self.servo_mapping:
            position = self.source_servo.ReadPosition(source_id)
            if position is not None:
                positions[source_id] = position
        return positions

    def mirror_mode(self):
        """Continuous position mirroring"""
        print("\n=== Mirror Mode ===")
        print("Replicating positions from source to target...")
        print("Press Ctrl+C to stop\n")

        last_positions = {}
        error_counts = {target_id: 0 for _, target_id in self.servo_mapping}

        try:
            while True:
                status_parts = []

                for source_id, target_id in self.servo_mapping:
                    position = self.source_servo.ReadPosition(source_id)

                    if position is None:
                        status_parts.append(f"S{source_id}:ERR")
                        continue

                    # Only send if position changed significantly (reduces bus traffic)
                    if source_id in last_positions:
                        if abs(position - last_positions[source_id]) < 5:
                            status_parts.append(f"S{source_id}:{position}")
                            continue

                    last_positions[source_id] = position

                    # Apply soft limits for target servo
                    constrained_position = self.apply_soft_limits(target_id, position)

                    # Send to target with higher speed for responsiveness
                    result = self.target_servo.MoveTo(target_id, constrained_position, speed=3400, acc=200, wait=False)

                    if result:
                        if constrained_position != position:
                            status_parts.append(f"S{source_id}:{position}→{constrained_position}✓")
                        else:
                            status_parts.append(f"S{source_id}:{position}✓")
                    else:
                        error_counts[target_id] += 1
                        status_parts.append(f"S{source_id}:{position}✗")

                # Print status on one line
                status_line = " | ".join(status_parts)
                print(f"\r{status_line}                              ", end='', flush=True)

                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\n\n=== Statistics ===")
            print("Error counts per servo:")
            for servo_id, count in error_counts.items():
                if count > 0:
                    print(f"  Servo {servo_id}: {count} errors")
            print("\n⚠️  Mirror mode stopped")

    def record_mode(self):
        """Record position sequences with live mirroring"""
        print("\n=== Record Mode with Live Mirroring ===")
        print("- Servos will mirror from ACM0 to ACM1")
        print("- Press ENTER to capture current positions")
        print("- Type 'done' and press ENTER to finish\n")

        # Enable target servos
        self.enable_target_servos()

        sequence = []
        frame_number = 0
        should_stop = False
        should_capture = False
        last_positions = {}

        def input_handler():
            nonlocal should_stop, should_capture
            while not should_stop:
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline().strip().lower()
                    if line == 'done':
                        should_stop = True
                    else:
                        should_capture = True
                time.sleep(0.05)

        # Start input thread
        input_thread = threading.Thread(target=input_handler, daemon=True)
        input_thread.start()

        try:
            print("Ready! Press ENTER to capture frames...")

            while not should_stop:
                status_parts = []
                current_positions = {}

                # Read and mirror positions
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

                # Check if we should capture
                if should_capture:
                    sequence.append(current_positions.copy())
                    frame_number += 1
                    print(f"\n✓ Frame {frame_number} captured: {current_positions}")
                    print("Press ENTER for next frame, or type 'done' to finish...")
                    should_capture = False

                # Print status
                status_line = " | ".join(status_parts)
                if not should_capture:
                    print(f"\r{status_line}                              ", end='', flush=True)

                time.sleep(0.05)

            # Disable target servos
            self.disable_target_servos()

            if not sequence:
                print("\n⚠️  No frames recorded. Aborting save.")
                return

            # Save sequence
            print(f"\n✓ Recorded {frame_number} frames")
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
                "frames": sequence,
                "frame_count": len(sequence)
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"✓ Sequence saved to {filepath}")

        except KeyboardInterrupt:
            print("\n\n⚠️  Recording interrupted")
            self.disable_target_servos()

    def interpolate_positions(self, pos1, pos2, steps):
        """Linear interpolation between two position dictionaries"""
        interpolated = []
        for i in range(steps + 1):
            t = i / steps
            frame = {}
            for servo_id in pos1.keys():
                if servo_id in pos2:
                    # Linear interpolation
                    frame[servo_id] = int(pos1[servo_id] + t * (pos2[servo_id] - pos1[servo_id]))
            interpolated.append(frame)
        return interpolated

    def playback_mode(self):
        """Playback recorded sequences with interpolation"""
        print("\n=== Playback Mode ===")

        # List available sequences
        sequences = [f for f in os.listdir(self.sequences_dir) if f.endswith('.json')]

        if not sequences:
            print("❌ No sequences found in 'sequences' directory")
            return

        print("Available sequences:")
        for idx, seq in enumerate(sequences):
            print(f"  {idx + 1}. {seq}")

        try:
            choice = int(input("\nSelect sequence number: ")) - 1
            if choice < 0 or choice >= len(sequences):
                print("❌ Invalid selection")
                return
        except ValueError:
            print("❌ Invalid input")
            return

        filepath = os.path.join(self.sequences_dir, sequences[choice])

        # Load sequence
        with open(filepath, 'r') as f:
            data = json.load(f)

        frames = data['frames']
        print(f"\n✓ Loaded sequence: {sequences[choice]}")
        print(f"  Frames: {len(frames)}")
        print(f"  Duration: {len(frames) * 2} seconds (2s per frame)")

        # Convert string keys back to integers
        frames = [{int(k): v for k, v in frame.items()} for frame in frames]

        input("\nPress ENTER to start playback...")

        print("\n=== Playing Sequence ===")

        try:
            # Enable target servos
            self.enable_target_servos()
            time.sleep(0.5)

            # Play each frame with interpolation
            for idx in range(len(frames)):
                current_frame = frames[idx]

                if idx < len(frames) - 1:
                    next_frame = frames[idx + 1]

                    # Interpolate over 2 seconds (2000ms / 50ms = 40 steps)
                    interpolated = self.interpolate_positions(current_frame, next_frame, 40)

                    print(f"\nFrame {idx} → {idx + 1}")

                    for interp_frame in interpolated:
                        for servo_id, position in interp_frame.items():
                            # Find corresponding target servo
                            target_id = None
                            for src, tgt in self.servo_mapping:
                                if src == servo_id:
                                    target_id = tgt
                                    break

                            if target_id is not None:
                                # Apply soft limits
                                constrained_position = self.apply_soft_limits(target_id, position)
                                self.target_servo.MoveTo(target_id, constrained_position, speed=3400, acc=200, wait=False)

                        time.sleep(0.05)  # 50ms between interpolated steps
                else:
                    # Last frame - just hold position
                    print(f"\nFrame {idx} (final)")
                    for servo_id, position in current_frame.items():
                        target_id = None
                        for src, tgt in self.servo_mapping:
                            if src == servo_id:
                                target_id = tgt
                                break

                        if target_id is not None:
                            # Apply soft limits
                            constrained_position = self.apply_soft_limits(target_id, position)
                            self.target_servo.MoveTo(target_id, constrained_position, speed=2400, acc=100, wait=False)

                    time.sleep(2)  # Hold final position for 2 seconds

            print("\n✓ Playback complete!")

        except KeyboardInterrupt:
            print("\n\n⚠️  Playback interrupted")
        finally:
            self.disable_target_servos()


def main():
    print("=== ST3215 Servo Controller ===")

    controller = ServoController()

    try:
        # Connect and scan
        controller.connect()
        controller.scan_servos()

        while True:
            print("\n" + "="*50)
            print("Select mode:")
            print("  1. Mirror Mode (replicate ACM0 to ACM1)")
            print("  2. Record Mode (capture position sequences)")
            print("  3. Playback Mode (replay sequences)")
            print("  4. Exit")
            print("="*50)

            choice = input("Enter choice (1-4): ").strip()

            if choice == '1':
                controller.enable_target_servos()
                controller.mirror_mode()
                controller.disable_target_servos()

            elif choice == '2':
                controller.record_mode()

            elif choice == '3':
                controller.playback_mode()

            elif choice == '4':
                print("\n👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if controller.target_servo:
            try:
                controller.disable_target_servos()
            except:
                pass
        print("\n✓ Cleanup complete")

if __name__ == "__main__":
    main()
