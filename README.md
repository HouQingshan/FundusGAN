# FundusGAN: High-Fidelity Fundus Image Generation

FundusGAN is a hierarchical, feature-aware generative framework designed for producing high-quality synthetic fundus images. It enables both small-scale and large-scale data generation and facilitates training with minimal technical barriers. This repository provides instructions for virtual environment setup, data preprocessing, model training, and synthetic image generation.

---

## 📦 Environment Setup

To create and activate the Conda environment:

```bash
cd FundusGAN
conda env create -f fundusgan.yml
conda activate fundusgan
```

---

## 🧹 Dataset Preprocessing

The training data should be stored as an **uncompressed ZIP archive** containing uncompressed PNG files and a metadata file named `dataset.json`.

### Step 1: Generate `dataset.json` (if not provided)

Ensure labels are encoded as numeric values.

```bash
python gen_dataset_json.py /path/to/source_directory /path/to/source_directory/dataset.json
```

* `/path/to/source_directory`: Directory containing PNG images.
* `dataset.json`: Metadata file with numerical labels.

### Step 2: Create a ZIP dataset archive

```bash
python dataset_tool.py --source /path/to/source_directory --dest /path/to/xxx.zip --width 512 --height 512
```

* `--source`: Path to raw image dataset.
* `--dest`: Output path for the ZIP file.
* `--width`/`--height`: Target resolution (e.g., 512x512).

---

## 🧠 Train the Generator

Training starts from a pretrained StyleGAN2 model (e.g., `ffhq256`) for faster convergence.

```bash
python train.py --outdir=/path/to/train_output --data=/path/to/xxx.zip --gpus=1 --seed=0 --resume=ffhq256 --snap=10
```

* `--outdir`: Output directory for weights and logs.
* `--data`: Path to the ZIP dataset.
* `--gpus`: Number of GPUs (1 recommended for stability).
* `--seed`: Random seed for reproducibility.
* `--resume`: Pretrained model to resume from (`ffhq256`, `ffhq512`, etc.).
* `--snap`: Snapshot interval (e.g., every 10 ticks).

> Default training lasts for 25,000 iterations. You can manually terminate the training when desired.

---

## 🎨 Image Sampling from Trained Models

### Option 1: Sample by Random Seeds

Use this for low-volume generation:

```bash
python generate.py --outdir=/path/to/output --trunc=1 --seeds=85,265,297,849,789,6789 --network=/path/to/weight/network-snapshot-xxx.pkl
```

* `--trunc`: Higher values (closer to 1) generate more diverse images.
* `--seeds`: Comma-separated list of seeds.
* `--network`: Path to the trained model checkpoint.

### Option 2: Batch Generation

Support up to 1 million images with 7-digit filenames:

```bash
python generate_batch.py --outdir=/path/to/output --network=/path/to/weight/network-snapshot-xxx.pkl --trunc=1 --total-images=1000000 --num-folders=10 --batch-size=100
```

* `--total-images`: Total number of images to generate.
* `--num-folders`: Number of subfolders to divide images into.
* `--batch-size`: Images per generation batch (recommended: 100).

> For more than 1 million images, you may need to modify the naming conventions in the code.

---

## 📄 Citation

If you use FundusGAN or this pipeline in your work, please cite:

```bibtex
@article{hou2025fundusgan,
  title={Fundusgan: A hierarchical feature-aware generative framework for high-fidelity fundus image generation},
  author={Hou, Qingshan and Wang, Meng and Cao, Peng and Ke, Zou and Liu, Xiaoli and Fu, Huazhu and Zaiane, Osmar R},
  journal={arXiv preprint arXiv:2503.17831},
  year={2025}
}
```

To cite the companion platform that integrates FundusGAN into a no-code interface:

```bibtex
@article{wang2025clinician,
  title={A Clinician-Friendly Platform for Ophthalmic Image Analysis Without Technical Barriers},
  author={Wang, Meng and Lin, Tian and Hou, Qingshan and Lin, Aidi and Wang, Jingcheng and Peng, Qingsheng and Nguyen, Truong X and Fang, Danqi and Zou, Ke and Xu, Ting and others},
  journal={arXiv preprint arXiv:2504.15928},
  year={2025}
}
```
