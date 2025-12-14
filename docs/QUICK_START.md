# Quick Start Guide - Your Setup

Based on your configuration:
- **Leader Arm**: COM7
- **Follower Arm**: COM10
- **Camera**: Connected (find index with `lerobot-find-cameras`)

## Next Steps (In Order)

### 1. Setup Motors (if not already done)

**Follower Motors:**
```powershell
uv run lerobot-setup-motors --robot.type=so101_follower --robot.port=COM10
```

**Leader Motors:**
```powershell
uv run lerobot-setup-motors --teleop.type=so101_leader --teleop.port=COM7
```

### 2. Calibrate Both Arms

**Follower:**
```powershell
uv run lerobot-calibrate --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm
```

**Leader:**
```powershell
uv run lerobot-calibrate --teleop.type=so101_leader --teleop.port=COM7 --teleop.id=my_awesome_leader_arm
```

### 3. Find Your Camera Index

```powershell
uv run lerobot-find-cameras opencv
```

Note the camera index (e.g., `0`, `1`, `2`) - you'll use this in the next steps.

### 4. Test Teleoperation (Recommended)

```powershell
uv run lerobot-teleoperate --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM7 --teleop.id=my_awesome_leader_arm --display_data=true
```

Replace `index_or_path: 0` with your actual camera index from step 3.

### 5. Setup Hugging Face (First Time Only)

```powershell
# Get your token from https://huggingface.co/settings/tokens
$env:HUGGINGFACE_TOKEN="your_token_here"
uv run huggingface-cli login --token $env:HUGGINGFACE_TOKEN --add-to-git-credential

# Get your username
uv run huggingface-cli whoami
```

### 6. Record Dataset

```powershell
uv run lerobot-record --robot.type=so101_follower --robot.port=COM10 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM7 --teleop.id=my_awesome_leader_arm --display_data=true --dataset.repo_id=YOUR_HF_USERNAME/record-test --dataset.num_episodes=60 --dataset.episode_time_s=20 --dataset.reset_time_s=10 --dataset.single_task="pickup the cube and place it to the bin" --dataset.root=$env:USERPROFILE\so101_dataset\
```

**Before running, replace:**
- `YOUR_HF_USERNAME` with your Hugging Face username
- `index_or_path: 0` with your camera index
- Adjust episode parameters as needed

## Troubleshooting

- If you get permission errors, run PowerShell as Administrator
- If motors aren't found, ensure power is on and only ONE motor is connected during setup
- If camera isn't detected, try different indices (0, 1, 2, etc.)
- See `docs/windows_uv_setup.md` for detailed troubleshooting


