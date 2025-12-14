#!/usr/bin/env python3
"""
Simple mirror test - minimal version to debug
"""

import sys
import time
from st3215 import ST3215

def main():
    print("=== Simple Mirror Test ===")

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

        if not source_servos:
            print(f"❌ No servos on {source_port}")
            return

        if not target_servos:
            print(f"❌ No servos on {target_port}")
            return

        # Simple 1-to-1 mapping
        mapping = list(zip(source_servos, target_servos))
        print(f"\nMapping: {mapping}")

        # Enable target servos
        print("\nEnabling target servos...")
        for _, target_id in mapping:
            result = target.StartServo(target_id)
            print(f"  Servo {target_id}: {result}")

        print("\n=== Starting Mirror ===")
        print("Press Ctrl+C to stop\n")

        iteration = 0
        while True:
            iteration += 1
            print(f"\nIteration {iteration}:")

            for source_id, target_id in mapping:
                # Read source position
                pos = source.ReadPosition(source_id)

                if pos is None:
                    print(f"  ❌ Failed to read servo {source_id}")
                    continue

                print(f"  Servo {source_id}: position = {pos}")

                # Write to target
                result = target.MoveTo(target_id, pos, speed=2400, acc=100, wait=False)

                if result:
                    print(f"  ✓ Servo {target_id} → {pos}")
                else:
                    print(f"  ❌ Failed to move servo {target_id}")

            time.sleep(0.1)  # 100ms delay

    except KeyboardInterrupt:
        print("\n\nStopped by user")

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
