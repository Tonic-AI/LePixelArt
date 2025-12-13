# SO-101 Motor Setup Guide (Windows)

## Step 1: Identify Ports for Each Arm

Run the port finder for each arm separately:

```powershell
uv run lerobot-find-port
```

**For Follower Arm:**
- Connect only the follower arm's USB cable
- Run the command and note the port (e.g., `COM6`)
- Disconnect when prompted to confirm

**For Leader Arm:**
- Connect only the leader arm's USB cable  
- Run the command again and note the port (e.g., `COM7`)
- Disconnect when prompted to confirm

## Step 2: Setup Follower Motors

Use the Windows COM port format (not `/dev/tty...`):

```powershell
uv run lerobot-setup-motors --robot.type=so101_follower --robot.port=COM6
```

Replace `COM6` with the actual port you identified for the follower arm.

**Process:**
1. Connect only the gripper motor (id=6) to the controller board
2. Press Enter when prompted
3. You'll see: `'gripper' motor id set to 6`
4. Disconnect and connect only the wrist_roll motor (id=5)
5. Press Enter
6. Repeat for each motor in sequence:
   - wrist_flex (id=4)
   - elbow_flex (id=3)
   - shoulder_lift (id=2)
   - shoulder_pan (id=1)

**Note:** The `lerobot-setup-motors` command automatically handles motors that already have IDs configured. It will scan for the motor at different baudrates and IDs, find it, and then change it to the correct ID and baudrate for your robot configuration.

## Step 3: Setup Leader Motors

```powershell
uv run lerobot-setup-motors --teleop.type=so101_leader --teleop.port=COM7
```

Replace `COM7` with the actual port you identified for the leader arm.

Follow the same process as the follower arm.

## Step 4: Calibrate Arms

**Follower:**
```powershell
uv run lerobot-calibrate --robot.type=so101_follower --robot.port=COM6
```

**Leader:**
```powershell
uv run lerobot-calibrate --teleop.type=so101_leader --teleop.port=COM7
```

## Resetting/Re-registering Motors

If your motors are already registered with different IDs or baudrates and you want to reset them:

### The Setup Process Automatically Handles This

The `lerobot-setup-motors` command is designed to handle motors that already have IDs configured. It will:

1. **Scan for motors** at multiple baudrates (typically 115200, 1000000, etc.)
2. **Detect the motor** regardless of its current ID
3. **Change the ID** to the correct value for your robot configuration
4. **Set the baudrate** to match your setup

### If Motor Still Not Found

If the motor is not being detected even though it's powered and connected:

1. **Try different baudrates manually**: The script tries common baudrates, but if your motor was configured with a non-standard baudrate, it might not be found.

2. **Check motor communication**: 
   - Ensure the motor is an STS3215 model
   - Verify the 3-pin cable is properly connected (not loose)
   - Check that the motor responds to power (LED indicators if available)

3. **Reset motor to factory defaults** (if supported by your motor):
   - Some motors have a factory reset procedure
   - Check your motor's documentation for reset instructions
   - This typically involves a specific sequence or button press

4. **Try the setup process anyway**: Even if you get a "motor not found" error initially, the setup script may still be able to communicate with the motor if:
   - The motor is powered
   - The connection is stable
   - You try running the command again after ensuring proper connections

### Re-registering Process

To re-register all motors:

1. **Start fresh**: Disconnect all motors from the controller board
2. **Run setup command**: Use the same `lerobot-setup-motors` command
3. **Connect one motor at a time**: Follow the prompts to connect each motor individually
4. **The script will handle ID changes**: It will find each motor and change its ID to the correct value

**Example for Follower:**
```powershell
uv run lerobot-setup-motors --robot.type=so101_follower --robot.port=COM6
```

**Example for Leader:**
```powershell
uv run lerobot-setup-motors --teleop.type=so101_leader --teleop.port=COM7
```

## Troubleshooting: "Motor not found" Error

If you get `RuntimeError: Motor 'gripper' (model 'sts3215') was not found`, check the following:

### 1. Power Supply
- ✅ **Ensure the power supply is connected and powered on**
- ✅ The motor needs power to be detected
- ✅ Check that the power LED on the controller board is on

### 2. Physical Connections
- ✅ **3-pin cable**: Make sure the 3-pin cable is firmly connected:
  - One end to the motor's 3-pin connector
  - Other end to the controller board's motor port
- ✅ **Only ONE motor connected**: Disconnect all other motors from the controller board
- ✅ **USB cable**: Ensure USB cable is still connected to your computer

### 3. Motor State
- ✅ If repurposing motors from another robot, they may have a different ID or baudrate
- ✅ Try a different motor to see if the issue is motor-specific
- ✅ Ensure the motor is an STS3215 model (as expected by the script)

### 4. Controller Board
- ✅ **Waveshare board**: Ensure jumpers are set on the `B` channel (USB)
- ✅ Check that the controller board is properly powered
- ✅ Try disconnecting and reconnecting the USB cable

### 5. Connection Sequence
When the script says "Connect the controller board to the 'gripper' motor only":
1. **Disconnect** any other motors from the controller board
2. **Connect** only the gripper motor's 3-pin cable to the controller board
3. **Verify** the power supply is on
4. **Press Enter** in the terminal

### 6. Windows-Specific Issues
- ✅ Try running PowerShell as Administrator
- ✅ Check Device Manager to ensure COM port is recognized
- ✅ Try unplugging and replugging the USB cable
- ✅ **Use the diagnostic script** (see below) to test serial communication

### 7. Diagnostic Script

If the motor still isn't found, use the diagnostic script to identify the issue:

```powershell
uv run python diagnose_motor.py COM8
```

Replace `COM8` with your actual COM port. This script will:
- Test if the serial port can be opened
- Try all baudrates that lerobot uses for STS3215 motors
- Report if any motors are detected
- Provide specific troubleshooting steps based on the results

**What the diagnostic script tests:**
- Serial port access (permissions, port availability)
- Motor detection at baudrates: 1,000,000, 500,000, 250,000, 128,000, 115,200, 57,600, 38,400, 19,200
- Broadcast ping functionality (how lerobot finds motors)

**Common findings:**
- If serial port fails: Permission issue or port in use
- If no motors found at any baudrate: Power, connection, or hardware issue
- If motors found at wrong baudrate: Motor needs reconfiguration

## Windows-Specific Serial Port Issues

If you're experiencing persistent "Motor not found" errors on Windows, it could be related to:

### 1. Serial Port Permissions
Windows may restrict access to COM ports. Try:
- **Run PowerShell as Administrator** before running commands
- Check if another program is using the COM port (close other serial terminal programs)

### 2. USB Driver Issues
- Open **Device Manager** (Win+X → Device Manager)
- Look under "Ports (COM & LPT)" for your device
- If you see a yellow warning icon, update the driver
- Try uninstalling and reinstalling the USB-to-serial driver

### 3. COM Port Access
Some Windows systems require explicit permission. You can test with:
```powershell
# Check if port is accessible
[System.IO.Ports.SerialPort]::getportnames()
```

### 4. Serial Port Timeout Issues
Windows serial communication can have different timing than Linux/Mac. The diagnostic script helps identify if this is the issue.

### 5. UV/Python Environment
While unlikely, if you're using `uv`, ensure the virtual environment has all dependencies:
```powershell
uv pip install pyserial
```

## Important Notes

- On Windows, use `COM6`, `COM7`, etc. (not `/dev/tty...`)
- Make sure only ONE motor is connected to the controller board at each step
- Check your power supply and USB cables are properly connected
- If using Waveshare controller board, ensure jumpers are set on the `B` channel (USB)
- The motor must be powered to be detected by the script
- **Run PowerShell as Administrator** if you encounter permission errors

