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
uv run lerobot-calibrate --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm
```

Replace `COM10` with your follower arm's port and give it a unique name.

**Leader:**
```powershell
uv run lerobot-calibrate --teleop.type=so101_leader --teleop.port=COM7 --teleop.id=my_awesome_leader_arm
```

Replace `COM7` with your leader arm's port and give it a unique name.

> **Note:** If you see a `Lock` error, you may need to unplug and replug the power to the arm.

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

## Troubleshooting: Motor Detection Errors

### IndexError: list index out of range

If you get `IndexError: list index out of range` during motor setup (especially during `broadcast_ping()`), this means the motor communication failed:

**What it means:**
- The code tried to communicate with the motor but got an empty or incomplete response
- This is a communication failure, not necessarily a hardware failure

**Quick fixes:**
1. **Check connections**: Ensure only ONE motor is connected, 3-pin cable is firm, power is on
2. **Retry**: Run the setup command again - it should resume from where it stopped
3. **Power cycle**: Unplug/replug power supply and USB cable, wait a few seconds
4. **Test with diagnostic**: `uv run python diagnose_motor.py COM7` (replace with your port)
5. **Try different motor**: Skip to the next motor to see if it's motor-specific

**If it persists:**
- The motor may have a non-standard baudrate
- Try running PowerShell as Administrator
- Check Device Manager for COM port issues
- The motor may need to be reset or replaced

### RuntimeError: Motor not found

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

## Step 5: Find Camera Index

Before recording datasets, you need to identify your camera's index:

```powershell
uv run lerobot-find-cameras opencv
```

This will list all available cameras with their indices. Note the index number (typically `0`, `1`, `2`, etc.) for your camera.

**Example output:**
```
Camera 0: USB Camera
Camera 1: Integrated Webcam
```

Use the index number in the camera configuration when teleoperating or recording.

## Step 6: Test Teleoperation (Optional but Recommended)

Test that both arms work together before recording:

**Basic teleoperation (without camera):**
```powershell
uv run lerobot-teleoperate `
    --robot.type=so101_follower `
    --robot.port=COM10 `
    --robot.id=my_awesome_follower_arm `
    --teleop.type=so101_leader `
    --teleop.port=COM7 `
    --teleop.id=my_awesome_leader_arm
```

**Teleoperation with camera:**
```powershell
uv run lerobot-teleoperate `
    --robot.type=so101_follower `
    --robot.port=COM10 `
    --robot.id=my_awesome_follower_arm `
    --robot.cameras="{top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" `
    --teleop.type=so101_leader `
    --teleop.port=COM7 `
    --teleop.id=my_awesome_leader_arm `
    --display_data=true
```

Replace `index_or_path: 0` with your camera's index from Step 5.

> **Note:** In PowerShell, use backticks (`) for line continuation, or put everything on one line.

## Step 7: Record Dataset

Once everything is working, you can record your dataset. The leader arm will control the follower arm to perform actions that get recorded.

### 7.1: Setup Hugging Face (if not already done)

If you haven't used Hugging Face Hub before, you'll need to login:

```powershell
# Set your Hugging Face token (get it from https://huggingface.co/settings/tokens)
$env:HUGGINGFACE_TOKEN="your_token_here"

# Login to Hugging Face
uv run huggingface-cli login --token $env:HUGGINGFACE_TOKEN --add-to-git-credential
```

Get your username:
```powershell
uv run huggingface-cli whoami
```

### 7.2: Record Dataset

**Example recording command:**
```powershell
uv run lerobot-record `
    --robot.type=so101_follower `
    --robot.port=COM10 `
    --robot.id=my_awesome_follower_arm `
    --robot.cameras="{top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" `
    --teleop.type=so101_leader `
    --teleop.port=COM7 `
    --teleop.id=my_awesome_leader_arm `
    --display_data=true `
    --dataset.repo_id=YOUR_HF_USERNAME/record-test `
    --dataset.num_episodes=60 `
    --dataset.episode_time_s=20 `
    --dataset.reset_time_s=10 `
    --dataset.single_task="pickup the cube and place it to the bin" `
    --dataset.root=$env:USERPROFILE\so101_dataset\
```

**Parameters explained:**
- `--dataset.num_episodes=60`: Number of teleoperation sessions to record
- `--dataset.episode_time_s=20`: Duration of each episode in seconds
- `--dataset.reset_time_s=10`: Time between episodes to reset the environment
- `--dataset.single_task`: Description of the task being performed
- `--dataset.root`: Where to save the dataset locally (Windows path format)
- `--dataset.repo_id`: Your Hugging Face username/repository name

**Important:**
- Replace `YOUR_HF_USERNAME` with your actual Hugging Face username
- Replace `index_or_path: 0` with your camera's index
- Adjust episode time and reset time based on your task complexity
- Use `Ctrl+C` to stop recording early
- Use `--resume=true` to continue recording if interrupted

The terminal will show logs when episodes start, reset, and when recording completes.

## Important Notes

- On Windows, use `COM6`, `COM7`, etc. (not `/dev/tty...`)
- Make sure only ONE motor is connected to the controller board at each step during motor setup
- Check your power supply and USB cables are properly connected
- If using Waveshare controller board, ensure jumpers are set on the `B` channel (USB)
- The motor must be powered to be detected by the script
- **Run PowerShell as Administrator** if you encounter permission errors
- Use backticks (`) for line continuation in PowerShell, or put commands on a single line

