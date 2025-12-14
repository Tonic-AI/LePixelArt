**### Make a fork or copy of this repo and fill in your team submission details! ###**

# AMD_Robotics_Hackathon_2025_Le_Pixel_Art

## Team Information

**Team:** 26-30

- **video** : https://youtube.com/shorts/OrA4qn8cc9o?feature=share
- **models and data** : https://hf.co/lepixelart

### Important information

- we used a custom implementation of `opencv` to avoid camera timeouts during episode reccordings
- we produce 5 models and 6 datasets

### Code Examples 

```bash
!lerobot-train \
  --dataset.repo_id=LePixelArt/tower_raw \
  --policy.type=act \
  --batch_size=128 \
  --steps=3500 \
  --output_dir=outputs/train/tower_raw \
  --job_name=frontflip \
  --policy.device=cuda \
  --policy.push_to_hub=true \
  --policy.repo_id=LePixelArt/tower \
  --wandb.enable=false
```

### Example Results 

```bash
INFO 2025-12-14 13:16:06 ot_train.py:163 {'batch_size': 128,
 'checkpoint_path': None,
 'dataset': {'episodes': None,
             'image_transforms': {'enable': False,
                                  'max_num_transforms': 3,
                                  'random_order': False,
                                  'tfs': {'affine': {'kwargs': {'degrees': [-5.0,
                                                                            5.0],
                                                                'translate': [0.05,
                                                                              0.05]},
                                                     'type': 'RandomAffine',
                                                     'weight': 1.0},
                                          'brightness': {'kwargs': {'brightness': [0.8,
                                                                                   1.2]},
                                                         'type': 'ColorJitter',
                                                         'weight': 1.0},
                                          'contrast': {'kwargs': {'contrast': [0.8,
                                                                               1.2]},
                                                       'type': 'ColorJitter',
                                                       'weight': 1.0},
                                          'hue': {'kwargs': {'hue': [-0.05,
                                                                     0.05]},
                                                  'type': 'ColorJitter',
                                                  'weight': 1.0},
                                          'saturation': {'kwargs': {'saturation': [0.5,
                                                                                   1.5]},
                                                         'type': 'ColorJitter',
                                                         'weight': 1.0},
                                          'sharpness': {'kwargs': {'sharpness': [0.5,
                                                                                 1.5]},
                                                        'type': 'SharpnessJitter',
                                                        'weight': 1.0}}},
             'repo_id': 'LePixelArt/tower_raw',
             'revision': None,
             'root': None,
             'streaming': False,
             'use_imagenet_stats': True,
             'video_backend': 'torchcodec'},
 'env': None,
 'eval': {'batch_size': 50, 'n_episodes': 50, 'use_async_envs': False},
 'eval_freq': 20000,
 'job_name': 'frontflip',
 'log_freq': 200,
 'num_workers': 4,
 'optimizer': {'betas': [0.9, 0.999],
               'eps': 1e-08,
               'grad_clip_norm': 10.0,
               'lr': 1e-05,
               'type': 'adamw',
               'weight_decay': 0.0001},
 'output_dir': 'outputs/train/tower_raw',
 'policy': {'chunk_size': 100,
            'device': 'cuda',
            'dim_feedforward': 3200,
            'dim_model': 512,
            'dropout': 0.1,
            'feedforward_activation': 'relu',
            'input_features': {},
            'kl_weight': 10.0,
            'latent_dim': 32,
            'license': None,
            'n_action_steps': 100,
            'n_decoder_layers': 1,
            'n_encoder_layers': 4,
            'n_heads': 8,
            'n_obs_steps': 1,
            'n_vae_encoder_layers': 4,
            'normalization_mapping': {'ACTION': <NormalizationMode.MEAN_STD: 'MEAN_STD'>,
                                      'STATE': <NormalizationMode.MEAN_STD: 'MEAN_STD'>,
                                      'VISUAL': <NormalizationMode.MEAN_STD: 'MEAN_STD'>},
            'optimizer_lr': 1e-05,
            'optimizer_lr_backbone': 1e-05,
            'optimizer_weight_decay': 0.0001,
            'output_features': {},
            'pre_norm': False,
            'pretrained_backbone_weights': 'ResNet18_Weights.IMAGENET1K_V1',
            'pretrained_path': None,
            'private': None,
            'push_to_hub': True,
            'replace_final_stride_with_dilation': False,
            'repo_id': 'LePixelArt/tower',
            'tags': None,
            'temporal_ensemble_coeff': None,
            'type': 'act',
            'use_amp': False,
            'use_vae': True,
            'vision_backbone': 'resnet18'},
 'rename_map': {},
 'resume': False,
 'save_checkpoint': True,
 'save_freq': 20000,
 'scheduler': None,
 'seed': 1000,
 'steps': 3500,
 'use_policy_training_preset': True,
 'wandb': {'disable_artifact': False,
           'enable': False,
           'entity': None,
           'mode': None,
           'notes': None,
           'project': 'lerobot',
           'run_id': None}}
INFO 2025-12-14 13:16:06 ot_train.py:171 Logs will be saved locally.
INFO 2025-12-14 13:16:06 ot_train.py:183 Creating dataset
Fetching 4 files:   0%|                                   | 0/4 [00:00<?, ?it/s]
meta/episodes/chunk-000/file-000.parquet:   0%|      | 0.00/176k [00:00<?, ?B/s]

meta/tasks.parquet:   0%|                           | 0.00/2.37k [00:00<?, ?B/s]

meta/tasks.parquet: 100%|██████████████████| 2.37k/2.37k [00:00<00:00, 8.91kB/s]


stats.json: 13.0kB [00:00, 9.01MB/s]A

meta/episodes/chunk-000/file-000.parquet: 100%|█| 176k/176k [00:00<00:00, 386kB/
Fetching 4 files: 100%|███████████████████████████| 4/4 [00:00<00:00,  4.78it/s]
Fetching 9 files:   0%|                                   | 0/9 [00:00<?, ?it/s]
videos/observation.images.top/chunk-000/(…):   0%|   | 0.00/243M [00:00<?, ?B/s]

videos/observation.images.front/chunk-00(…):   0%|   | 0.00/143M [00:00<?, ?B/s]


data/chunk-000/file-000.parquet:   0%|               | 0.00/668k [00:00<?, ?B/s]



README.md: 3.77kB [00:00, 2.75MB/s]A




.gitattributes: 2.46kB [00:00, 6.61MB/s]A
Fetching 9 files:  11%|███                        | 1/9 [00:00<00:04,  1.78it/s]


data/chunk-000/file-000.parquet: 100%|███████| 668k/668k [00:00<00:00, 1.48MB/s]
Fetching 9 files:  33%|█████████                  | 3/9 [00:00<00:01,  3.73it/s]

videos/observation.images.front/chunk-00(…):   6%| | 8.80M/143M [00:00<00:11, 11
videos/observation.images.top/chunk-000/(…):  17%|▏| 41.4M/243M [00:01<00:06, 33
videos/observation.images.top/chunk-000/(…):  45%|▍| 108M/243M [00:01<00:02, 62.

videos/observation.images.front/chunk-00(…):  53%|▌| 75.9M/143M [00:01<00:01, 43

videos/observation.images.front/chunk-00(…): 100%|█| 143M/143M [00:02<00:00, 69.
Fetching 9 files:  89%|████████████████████████   | 8/9 [00:02<00:00,  3.31it/s]
videos/observation.images.top/chunk-000/(…):  72%|▋| 176M/243M [00:02<00:00, 98.
videos/observation.images.top/chunk-000/(…): 100%|█| 243M/243M [00:02<00:00, 103
Fetching 9 files: 100%|███████████████████████████| 9/9 [00:02<00:00,  3.26it/s]
INFO 2025-12-14 13:16:11 ot_train.py:202 Creating policy
INFO 2025-12-14 13:16:11 ot_train.py:247 Creating optimizer and scheduler
INFO 2025-12-14 13:16:11 ot_train.py:259 Output dir: outputs/train/tower_raw
INFO 2025-12-14 13:16:11 ot_train.py:262 cfg.steps=3500 (4K)
INFO 2025-12-14 13:16:11 ot_train.py:263 dataset.num_frames=24117 (24K)
INFO 2025-12-14 13:16:11 ot_train.py:264 dataset.num_episodes=64
INFO 2025-12-14 13:16:11 ot_train.py:267 Effective batch size: 128 x 1 = 128
INFO 2025-12-14 13:16:11 ot_train.py:268 num_learnable_params=51597190 (52M)
INFO 2025-12-14 13:16:11 ot_train.py:269 num_total_params=51597190 (52M)
INFO 2025-12-14 13:16:11 ot_train.py:324 Start offline training on a fixed dataset
INFO 2025-12-14 13:26:18 ot_train.py:351 step:200 smpl:26K ep:68 epch:1.06 loss:5.320 grdn:70.270 lr:1.0e-05 updt_s:2.958 data_s:0.073
INFO 2025-12-14 13:28:10 ot_train.py:351 step:400 smpl:51K ep:136 epch:2.12 loss:1.951 grdn:32.048 lr:1.0e-05 updt_s:0.498 data_s:0.062
INFO 2025-12-14 13:30:02 ot_train.py:351 step:600 smpl:77K ep:204 epch:3.18 loss:1.427 grdn:28.631 lr:1.0e-05 updt_s:0.498 data_s:0.063
INFO 2025-12-14 13:31:53 ot_train.py:351 step:800 smpl:102K ep:272 epch:4.25 loss:1.072 grdn:23.491 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:33:44 ot_train.py:351 step:1K smpl:128K ep:340 epch:5.31 loss:0.814 grdn:21.644 lr:1.0e-05 updt_s:0.497 data_s:0.056
INFO 2025-12-14 13:35:34 ot_train.py:351 step:1K smpl:154K ep:408 epch:6.37 loss:0.629 grdn:19.083 lr:1.0e-05 updt_s:0.497 data_s:0.056
INFO 2025-12-14 13:37:25 ot_train.py:351 step:1K smpl:179K ep:476 epch:7.43 loss:0.495 grdn:17.547 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:39:17 ot_train.py:351 step:2K smpl:205K ep:543 epch:8.49 loss:0.398 grdn:15.200 lr:1.0e-05 updt_s:0.497 data_s:0.062
INFO 2025-12-14 13:41:08 ot_train.py:351 step:2K smpl:230K ep:611 epch:9.55 loss:0.330 grdn:13.787 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:42:58 ot_train.py:351 step:2K smpl:256K ep:679 epch:10.61 loss:0.286 grdn:13.317 lr:1.0e-05 updt_s:0.497 data_s:0.056
INFO 2025-12-14 13:44:49 ot_train.py:351 step:2K smpl:282K ep:747 epch:11.68 loss:0.255 grdn:12.638 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:46:40 ot_train.py:351 step:2K smpl:307K ep:815 epch:12.74 loss:0.231 grdn:12.226 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:48:31 ot_train.py:351 step:3K smpl:333K ep:883 epch:13.80 loss:0.212 grdn:10.804 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:50:23 ot_train.py:351 step:3K smpl:358K ep:951 epch:14.86 loss:0.197 grdn:10.300 lr:1.0e-05 updt_s:0.497 data_s:0.062
INFO 2025-12-14 13:52:14 ot_train.py:351 step:3K smpl:384K ep:1K epch:15.92 loss:0.186 grdn:10.199 lr:1.0e-05 updt_s:0.497 data_s:0.061
INFO 2025-12-14 13:54:05 ot_train.py:351 step:3K smpl:410K ep:1K epch:16.98 loss:0.175 grdn:9.755 lr:1.0e-05 updt_s:0.496 data_s:0.058
INFO 2025-12-14 13:55:56 ot_train.py:351 step:3K smpl:435K ep:1K epch:18.05 loss:0.167 grdn:9.534 lr:1.0e-05 updt_s:0.497 data_s:0.057
INFO 2025-12-14 13:56:56 ot_train.py:361 Checkpoint policy after step 3500
INFO 2025-12-14 13:56:56 ot_train.py:430 End of training
```