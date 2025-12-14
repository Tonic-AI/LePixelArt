#!/usr/bin/env python3
"""
Position Replication Script
Reads positions from robots on ACM0 and replicates them on ACM1
"""

import sys
import time
from st3215 import ST3215

def main():
    print("=== ST3215 Position Replication ===")

    # Serial port configuration
    source_port = "/dev/ttyACM0"  # Read from this port
    target_port = "/dev/ttyACM1"  # Write to this port

    try:
        # Initialize connections to both serial ports
        print(f"\nConnecting to {source_port}...")
        source_servo = ST3215(source_port)
        print(f"✓ Connected to {source_port}")

        print(f"\nConnecting to {target_port}...")
        target_servo = ST3215(target_port)
        print(f"✓ Connected to {target_port}")

        # List servos on both ports
        print(f"\nScanning for servos on {source_port}...")
        source_servos = source_servo.ListServos()
        print(f"✓ Found servos on {source_port}: {source_servos}")

        print(f"\nScanning for servos on {target_port}...")
        target_servos = target_servo.ListServos()
        print(f"✓ Found servos on {target_port}: {target_servos}")

        if not source_servos:
            print(f"\n❌ No servos found on {source_port}!")
            sys.exit(1)

        if not target_servos:
            print(f"\n❌ No servos found on {target_port}!")
            sys.exit(1)

        # Find common servo IDs
        common_servos = sorted(set(source_servos) & set(target_servos))
        if not common_servos:
            print(f"\n⚠️  Warning: No matching servo IDs found between ports!")
            print(f"   Source servos: {source_servos}")
            print(f"   Target servos: {target_servos}")
            print(f"\n   Will attempt to map servos in order...")

            # Map servos by position in list
            servo_mapping = list(zip(source_servos, target_servos))
        else:
            print(f"\n✓ Common servo IDs: {common_servos}")
            servo_mapping = [(sid, sid) for sid in common_servos]

        # Enable torque on target servos
        print("\nEnabling torque on target servos...")
        for _, target_id in servo_mapping:
            result = target_servo.StartServo(target_id)
            if not result:
                print(f"❌ Failed to start servo {target_id} on {target_port}")
            else:
                print(f"✓ Servo {target_id} enabled on {target_port}")

        print("\n=== Starting Position Replication ===")
        print("Reading positions from source and replicating to target...")
        print("Press Ctrl+C to stop\n")

        # Continuous replication loop
        while True:
            for source_id, target_id in servo_mapping:
                # Read position from source
                position = source_servo.ReadPosition(source_id)

                if position is None:
                    print(f"⚠️  Failed to read position from servo {source_id} on {source_port}")
                    continue

                # Write position to target
                result = target_servo.MoveTo(target_id, position, speed=2400, acc=100, wait=False)

                if not result:
                    print(f"⚠️  Failed to move servo {target_id} on {target_port} to position {position}")
                else:
                    print(f"✓ Servo {source_id}→{target_id}: Position {position}", end='\r')

            time.sleep(0.05)  # 50ms delay between updates (20Hz update rate)

    except KeyboardInterrupt:
        print("\n\n⚠️  Replication stopped by user")
        print("Disabling torque on target servos...")
        try:
            for _, target_id in servo_mapping:
                target_servo.StopServo(target_id)
            print("✓ Target servos stopped safely")
        except:
            print("❌ Could not stop servos - please check manually")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Attempting to stop target servos...")
        try:
            for _, target_id in servo_mapping:
                target_servo.StopServo(target_id)
            print("✓ Target servos stopped safely")
        except:
            print("❌ Could not stop servos - please check manually")
        sys.exit(1)

if __name__ == "__main__":
    main()
