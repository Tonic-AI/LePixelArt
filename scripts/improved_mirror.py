#!/usr/bin/env python3
"""
Improved mirror with better error handling and visual feedback
"""

import sys
import time
from st3215 import ST3215

def main():
    print("=== Improved Mirror Mode ===")

    source_port = "/dev/ttyACM0"
    target_port = "/dev/ttyACM1"

    try:
        # Connect
        print(f"Connecting to {source_port}...")
        source = ST3215(source_port)
        print(f"✓ Connected to {source_port}")

        print(f"Connecting to {target_port}...")
        target = ST3215(target_port)
        print(f"✓ Connected to {target_port}")

        # Scan servos
        print(f"\nScanning {source_port}...")
        source_servos = source.ListServos()
        print(f"Source servos: {source_servos}")

        print(f"\nScanning {target_port}...")
        target_servos = target.ListServos()
        print(f"Target servos: {target_servos}")

        if not source_servos or not target_servos:
            print("❌ No servos found")
            return

        # Simple 1-to-1 mapping
        mapping = list(zip(source_servos, target_servos))
        print(f"\nMapping: {mapping}")

        # Enable target servos
        print("\nEnabling target servos...")
        for _, target_id in mapping:
            result = target.StartServo(target_id)
            if result:
                print(f"  ✓ Servo {target_id} enabled")
            else:
                print(f"  ❌ Servo {target_id} failed to enable")

        print("\n=== Starting Mirror ===")
        print("Move servos on ACM0, they will be mirrored on ACM1")
        print("Press Ctrl+C to stop\n")

        # Statistics
        error_counts = {target_id: 0 for _, target_id in mapping}
        last_positions = {}

        iteration = 0
        while True:
            iteration += 1

            # Build status line
            status_parts = []

            for source_id, target_id in mapping:
                # Read source position
                pos = source.ReadPosition(source_id)

                if pos is None:
                    status_parts.append(f"S{source_id}:ERR")
                    continue

                # Only send if position changed significantly (reduces bus traffic)
                if source_id in last_positions:
                    if abs(pos - last_positions[source_id]) < 5:
                        status_parts.append(f"S{source_id}:{pos}")
                        continue

                last_positions[source_id] = pos

                # Write to target with retry
                result = target.MoveTo(target_id, pos, speed=3400, acc=200, wait=False)

                if result:
                    status_parts.append(f"S{source_id}:{pos}✓")
                else:
                    error_counts[target_id] += 1
                    status_parts.append(f"S{source_id}:{pos}✗")

            # Print status on one line
            status_line = " | ".join(status_parts)
            print(f"\r{status_line}                    ", end='', flush=True)

            time.sleep(0.05)  # 50ms = 20Hz update rate

    except KeyboardInterrupt:
        print("\n\n=== Statistics ===")
        print("Error counts per servo:")
        for servo_id, count in error_counts.items():
            if count > 0:
                print(f"  Servo {servo_id}: {count} errors")
        print("\n✓ Stopped by user")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\nDisabling target servos...")
        try:
            for _, target_id in mapping:
                target.StopServo(target_id)
            print("✓ Done")
        except:
            pass

if __name__ == "__main__":
    main()
