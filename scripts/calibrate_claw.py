#!/usr/bin/env python3
"""
Calibrate claw (motor 6) boundaries
Records min and max positions for soft limits
"""

import sys
import json
import os
from st3215 import ST3215

def main():
    print("=== Claw Calibration (Motor 6) ===\n")

    source_port = "/dev/ttyACM0"
    claw_id = 6
    config_file = "claw_limits.json"

    try:
        # Connect
        print(f"Connecting to {source_port}...")
        servo = ST3215(source_port)
        print(f"✓ Connected to {source_port}\n")

        # Check if servo 6 exists
        print(f"Checking for servo {claw_id}...")
        if not servo.PingServo(claw_id):
            print(f"❌ Servo {claw_id} not found on {source_port}")
            print("   Available servos:", servo.ListServos())
            return

        print(f"✓ Servo {claw_id} found\n")

        # Calibrate minimum position
        print("=" * 60)
        print("STEP 1: Calibrate MINIMUM position")
        print("=" * 60)
        print(f"Manually move servo {claw_id} to its MINIMUM safe position")
        print("(fully open or minimum extent of travel)")
        input("Press ENTER when ready...")

        min_position = servo.ReadPosition(claw_id)
        if min_position is None:
            print(f"❌ Failed to read position from servo {claw_id}")
            return

        print(f"✓ Minimum position recorded: {min_position}\n")

        # Calibrate maximum position
        print("=" * 60)
        print("STEP 2: Calibrate MAXIMUM position")
        print("=" * 60)
        print(f"Manually move servo {claw_id} to its MAXIMUM safe position")
        print("(fully closed or maximum extent of travel)")
        input("Press ENTER when ready...")

        max_position = servo.ReadPosition(claw_id)
        if max_position is None:
            print(f"❌ Failed to read position from servo {claw_id}")
            return

        print(f"✓ Maximum position recorded: {max_position}\n")

        # Validate
        if min_position == max_position:
            print("❌ Min and max positions are the same!")
            return

        # Ensure min < max
        if min_position > max_position:
            print("⚠️  Swapping min and max (min was greater than max)")
            min_position, max_position = max_position, min_position

        # Summary
        print("=" * 60)
        print("CALIBRATION SUMMARY")
        print("=" * 60)
        print(f"Servo ID:        {claw_id}")
        print(f"Minimum position: {min_position}")
        print(f"Maximum position: {max_position}")
        print(f"Range:           {max_position - min_position} steps")
        print("=" * 60)

        # Confirm save
        confirm = input("\nSave these limits? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Calibration cancelled")
            return

        # Save to file
        calibration_data = {
            "servo_id": claw_id,
            "min_position": min_position,
            "max_position": max_position,
            "range": max_position - min_position
        }

        with open(config_file, 'w') as f:
            json.dump(calibration_data, f, indent=2)

        print(f"\n✓ Calibration saved to {config_file}")
        print("\nThese limits will be applied during teleoperation to prevent")
        print(f"servo {claw_id} from exceeding safe boundaries.\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Calibration cancelled")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
