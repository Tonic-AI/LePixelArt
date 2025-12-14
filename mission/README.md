# LePixelArt - Automated Pixel Art Production with Rubik's Cubes

## Mission Overview

Our mission is to **automate the production of pixel art using Rubik's cubes** with SO101 robotic arms. This project leverages the LeRobot framework to train multiple specialized models that work together to create pixel art formations from Rubik's cubes. The system allows anyone to produce pixel art using Rubik's cubes with robotic automation.

## Real-World Application

This project demonstrates a practical application of robotics for artistic creation, combining:
- **Precision manipulation** of Rubik's cubes
- **Multi-model coordination** for complex tasks
- **Automated assembly** of pixel art formations
- **Accessibility** - enabling anyone to create pixel art without manual cube manipulation

## System Architecture

Our solution consists of **six specialized models**, each trained to perform a specific action:

1. **Face Turn Model** - Rotates a specific face of the Rubik's cube
2. **Flip Model** - Flips the entire Rubik's cube to access different faces
3. **Top Face Turn Model** - Rotates the top face of the Rubik's cube
4. **Cube Dispenser Model** - Retrieves Rubik's cubes from our custom cardboard dispenser
5. **All-Actions Model** - A comprehensive model containing every action in a single model
6. **Formation Placement Model** - Places Rubik's cubes in the correct formation to create pixel art

Together, these models coordinate to produce Rubik's cubes in the right formation, enabling automated pixel art creation.

## Technical Implementation

### Framework
- **LeRobot Framework** - Used for dataset collection, model training, and inference
- **SO101 Robotic Arms** - Multi-arm robotic system for cube manipulation

### Dataset Collection
- Teleoperation-based dataset collection
- Multiple specialized datasets for each model
- Aggregated dataset combining all actions

### Training
- Individual models trained for specific actions
- Comprehensive model trained with all actions
- Transfer learning and fine-tuning approaches

## Hugging Face Resources

### Organization
🔗 **LePixelArt Organization**: [https://huggingface.co/LePixelArt](https://huggingface.co/LePixelArt)

### Models

1. **faceturn** - [https://huggingface.co/LePixelArt/faceturn](https://huggingface.co/LePixelArt/faceturn)
   - Rotates a specific face of the Rubik's cube

2. **wholecubeturnleft** - [https://huggingface.co/LePixelArt/wholecubeturnleft](https://huggingface.co/LePixelArt/wholecubeturnleft)
   - Rotates the entire cube to the left

3. **frontflip** - [https://huggingface.co/LePixelArt/frontflip](https://huggingface.co/LePixelArt/frontflip)
   - Flips the Rubik's cube forward

### Datasets

1. **all_datasets_aggregated** - [https://huggingface.co/datasets/LePixelArt/all_datasets_aggregated](https://huggingface.co/datasets/LePixelArt/all_datasets_aggregated)
   - Comprehensive dataset with 127k samples combining all actions

2. **therealfrontflip_raw** - [https://huggingface.co/datasets/LePixelArt/therealfrontflip_raw](https://huggingface.co/datasets/LePixelArt/therealfrontflip_raw)
   - Raw dataset for front flip action (27.7k samples)

3. **faceturn** - [https://huggingface.co/datasets/LePixelArt/faceturn](https://huggingface.co/datasets/LePixelArt/faceturn)
   - Dataset for face turn action (17.7k samples)

4. **tileplane** - [https://huggingface.co/datasets/LePixelArt/tileplane](https://huggingface.co/datasets/LePixelArt/tileplane)
   - Dataset for tile placement (30.4k samples)

5. **tower_raw** - [https://huggingface.co/datasets/LePixelArt/tower_raw](https://huggingface.co/datasets/LePixelArt/tower_raw)
   - Raw dataset for tower/formation building (24.4k samples)

6. **wholecubeturnleft** - [https://huggingface.co/datasets/LePixelArt/wholecubeturnleft](https://huggingface.co/datasets/LePixelArt/wholecubeturnleft)
   - Dataset for whole cube rotation (27.1k samples)

7. **EASYTEST** - [https://huggingface.co/datasets/LePixelArt/EASYTEST](https://huggingface.co/datasets/LePixelArt/EASYTEST)
   - Test dataset (667 samples)

## Project Logs

📋 **Training Logs**: [logs/training_logs.md](logs/training_logs.md) *(placeholder)*

📋 **Inference Logs**: [logs/inference_logs.md](logs/inference_logs.md) *(placeholder)*

📋 **System Logs**: [logs/system_logs.md](logs/system_logs.md) *(placeholder)*

## Demonstration Video

🎥 **YouTube Demonstration**: [https://youtube.com/watch?v=PLACEHOLDER](https://youtube.com/watch?v=PLACEHOLDER) *(placeholder)*

## Innovation & Creativity

### Novel Approach
- **Multi-model coordination** - Specialized models working together for complex manipulation
- **Custom hardware integration** - Cardboard dispenser for automated cube retrieval
- **Pixel art automation** - First-of-its-kind automated pixel art creation using Rubik's cubes
- **Modular design** - Each model can be used independently or in combination

### Technical Innovation
- Transfer learning across related manipulation tasks
- Efficient dataset collection through teleoperation
- Real-time coordination of multiple robotic arms
- Generalizable approach applicable to other manipulation tasks

## Ease of Use

### Generalizability
- Models can be adapted for different cube manipulation tasks
- Framework supports easy extension to new actions
- Modular architecture allows for task-specific fine-tuning

### User Interface
- Simple command interface for pixel art generation
- Automated pipeline from design to physical realization
- No manual cube manipulation required

## Repository

🔗 **GitHub Repository**: [https://github.com/Tonic-AI/LePixelArt](https://github.com/Tonic-AI/LePixelArt)

## Team

This project was developed as part of the **AMD Robotics Hackathon 2025**.

---

*For more information about the LeRobot framework, visit: [https://github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)*
