# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

`vocdev` is a toolset for Pascal VOC dataset, providing format conversion and visualization utilities. Pascal VOC is a commonly used lightweight object detection dataset. This repository contains commonly used implementations and documentation.

> **Note:** This repository is no longer actively maintained. Active development has moved to [DataFlow-CV](https://github.com/zjykzj/DataFlow-CV).

## Main Functionality

1. **Format Conversion**:
   - VOC → COCO: `py/voc2coco.py`
   - VOC → YOLOv5: `py/voc2yolov5.py`
   - VOCLike → YOLOv5: `py/voclike2yolov5.py`
   - YOLOv5 → VOCLike: `py/yolo2voclike.py`

2. **Utility Scripts**:
   - `py/find_classes.py`: Traverse annotation files and extract class list
   - `py/show_voclike_label.py`: Visualize VOCLike format annotations
   - `py/show_yololike_label.py`: Visualize YOLOLike format annotations

3. **Supporting Files**:
   - `voc.names`: Default 20-class list for Pascal VOC (see below for contents)

## Project Structure

```
.
├── py/                    # All Python scripts
│   ├── voc2coco.py       # VOC to COCO
│   ├── voc2yolov5.py     # VOC to YOLOv5
│   ├── voclike2yolov5.py # VOCLike to YOLOv5
│   ├── yolo2voclike.py   # YOLOv5 to VOCLike
│   ├── find_classes.py   # Extract class list
│   ├── show_voclike_label.py # Visualize VOCLike annotations
│   ├── show_yololike_label.py # Visualize YOLOLike annotations
│   ├── dataset.py        # Dataset example (minimal)
│   └── __init__.py
├── assets/               # Sample data for testing
├── imgs/                # Image resources
├── voc.names            # Class names file (see below)
├── README.md            # English documentation
├── README.zh-CN.md      # Chinese documentation
└── LICENSE              # Apache 2.0 license
```

**voc.names contents** (20 Pascal VOC classes):
```
aeroplane
bicycle
bird
boat
bottle
bus
car
cat
chair
cow
diningtable
dog
horse
motorbike
person
pottedplant
sheep
sofa
train
tvmonitor
```

## Usage

### Environment Dependencies
All scripts require Python 3 and the following libraries:
- `torchvision` (depends on PyTorch, used for loading VOC datasets)
- `numpy`
- `PIL` (Pillow)
- `tqdm`
- `opencv-python` (for visualization scripts only)
- `argparse` (standard library)

Install with:
```bash
pip install torchvision numpy Pillow tqdm opencv-python
```

### Common Commands

#### 1. VOC to COCO
```bash
python py/voc2coco.py -v ../datasets/voc -c ../datasets/voc2coco -l train-2007 val-2007 test-2007 train-2012 val-2012
```
- `-v`: VOC dataset root path
- `-c`: COCO format output path
- `-l`: List of datasets to process (supports train-2007, val-2007, test-2007, trainval-2007, train-2012, val-2012, trainval-2007)

#### 2. VOC to YOLOv5
```bash
python py/voc2yolov5.py -s ../datasets/voc -d ../datasets/voc2yolov5-train -l trainval-2007 trainval-2012
python py/voc2yolov5.py -s ../datasets/voc -d ../datasets/voc2yolov5-val -l test-2007
```
- `-s`: Source dataset path
- `-d`: Destination output path
- `-l`: Dataset list

#### 3. VOCLike to YOLOv5
```bash
python py/voclike2yolov5.py ../datasets/voclike/JPEGImages ../datasets/voclike/Annotations voc.names ../datasets/voclike2yolov5
```
- First argument: Image directory path (JPEGImages)
- Second argument: Annotation directory path (Annotations)
- Third argument: Class file path (e.g., voc.names)
- Fourth argument: YOLOv5 format output path

#### 4. YOLOv5 to VOCLike
```bash
python py/yolo2voclike.py ../datasets/yolov5 voc.names ../datasets/yolov52voclike
```
- First argument: YOLOv5 data root path (contains images/ and labels/ directories)
- Second argument: Class file path (e.g., voc.names)
- Third argument: VOCLike format output path

#### 5. Extract Class List
```bash
python py/find_classes.py ../../myai/mask/datasets/MaskDatasets/datasets/
```
- First argument: VOCLike data root path (contains XML annotation files)
- `--dst`: Output directory (default ./output)

#### 6. Visualize Annotations
```bash
# Visualize single VOCLike annotation
python py/show_voclike_label.py assets/voclike/000006.jpg assets/voclike/000006.xml
# Visualize entire directory
python py/show_voclike_label.py assets/voclike/ assets/voclike/
# Save annotated images to output directory
python py/show_voclike_label.py assets/voclike/ assets/voclike/ --dst ./output/

# Visualize single YOLOLike annotation
python py/show_yololike_label.py assets/yololike/000000082986.jpg assets/yololike/000000082986.txt
# Visualize entire directory
python py/show_yololike_label.py assets/yololike/ assets/yololike/
# Save annotated images to output directory
python py/show_yololike_label.py assets/yololike/ assets/yololike/ --dst ./output/
```

### Notes
- Conversion scripts default to using `voc.names` as the class file; use `--classes` parameter to specify a custom file
- When converting VOC datasets, if the dataset doesn't exist locally, `torchvision` will automatically download it (requires internet)
- Output directories are created automatically; existing directories trigger an `assert` check to prevent accidental overwrites

## Development Guidelines

### Code Style
- Python files use UTF-8 encoding with `# -*- coding: utf-8 -*-` header
- Docstrings include author, date, and description
- Use type annotations (`typing` module)
- Import order: standard library → third‑party libraries → local modules

### Git Commits
- Follow [Conventional Commits](https://www.conventionalcommits.org/) specification
- Example: `feat(py/voc2coco.py): add support for VOC2012`
- Use semantic versioning (Semantic Versioning 2.0.0)

### Adding New Scripts
- Follow the existing pattern: `parse_args()` → `main()` → `process()` functions
- Provide complete command‑line argument parsing with `argparse` and help messages
- Include a usage example in the script’s docstring
- Update this CLAUDE.md and the README files with the new functionality

### Testing and Quality Assurance
- This repository currently has no automated tests, linting, or build system
- When modifying or adding scripts, manually verify the conversion on a small sample dataset
- Ensure backward compatibility is maintained (if required) by checking existing command‑line arguments

## Architecture

### Data Formats
1. **Pascal VOC**: Standard VOC format, loaded via `torchvision.datasets.VOCDetection`
2. **COCO**: Follows COCO JSON format; outputs `instances_{dataset}{year}.json`
3. **YOLOv5**: Each image has a corresponding `.txt` file with lines: `cls_id x_center y_center width height` (normalized coordinates)
4. **VOCLike**: Similar to VOC but not identical; contains `JPEGImages/` and `Annotations/` directories

### Conversion Logic
- All conversion scripts share a similar structure: `parse_args()` → `main()` → `process()`
- Objects with `difficult=1` are ignored
- Coordinate conversion includes normalization (for YOLO format)
- Supports batch processing of multiple datasets (via `-l` parameter)

### Module Relationships
- `dataset.py` is only an example; actual VOC loading uses `torchvision`’s `VOCDetection`
- `find_classes.py` is standalone and does not depend on other modules
- Visualization scripts depend on OpenCV (`cv2`); if not installed, image display is skipped

## Troubleshooting

### Common Issues
1. **Missing dependencies**: Ensure `torchvision` (and PyTorch) are installed
2. **Incorrect dataset paths**: Use absolute paths or correct relative paths
3. **Class mismatch**: Ensure custom class files match the annotation class names exactly
4. **Out of memory**: Process large datasets in batches

### Debugging Suggestions
- Test with a small subset of data first
- Check intermediate output directory structure
- Examine the detailed parameter information printed by the scripts

---

*This file was generated based on repository state as of 2026‑03‑14. Previous Chinese version is available in git history.*