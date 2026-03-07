# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此代码仓库中工作提供指导。

## 仓库概述

vocdev 是一个用于 Pascal VOC 数据集的工具集，提供多种格式转换和可视化功能。Pascal VOC 是一个常用的轻量级目标识别和检测数据集，本仓库保存了常用的实现和文档。

## 主要功能

1. **格式转换**：
   - VOC → COCO：`py/voc2coco.py`
   - VOC → YOLOv5：`py/voc2yolov5.py`
   - VOCLike → YOLOv5：`py/voclike2yolov5.py`
   - YOLOv5 → VOCLike：`py/yolo2voclike.py`

2. **工具脚本**：
   - `py/find_classes.py`：遍历标注文件，提取类别列表
   - `py/show_voclike_label.py`：可视化 VOCLike 格式的标注
   - `py/show_yololike_label.py`：可视化 YOLOLike 格式的标注

3. **辅助文件**：
   - `voc.names`：Pascal VOC 的 20 个默认类别列表

## 项目结构

```
.
├── py/                    # 所有 Python 脚本
│   ├── voc2coco.py       # VOC 转 COCO
│   ├── voc2yolov5.py     # VOC 转 YOLOv5
│   ├── voclike2yolov5.py # VOCLike 转 YOLOv5
│   ├── yolo2voclike.py   # YOLOv5 转 VOCLike
│   ├── find_classes.py   # 提取类别列表
│   ├── show_voclike_label.py # 可视化 VOCLike 标注
│   ├── show_yololike_label.py # 可视化 YOLOLike 标注
│   ├── dataset.py        # 数据集相关（简单示例）
│   └── __init__.py
├── assets/               # 资源文件
├── imgs/                # 图片资源
├── voc.names            # 类别名称文件
├── README.md            # 英文说明
├── README.zh-CN.md      # 中文说明
└── LICENSE              # Apache 2.0 许可证
```

## 使用方法

### 环境依赖
所有脚本基于 Python 3，依赖以下库：
- `torchvision`（用于加载 VOC 数据集，依赖 PyTorch）
- `numpy`
- `PIL`（Pillow）
- `tqdm`
- `opencv-python`（用于可视化脚本）
- `argparse`（Python 标准库）

可通过以下命令安装依赖：
```bash
pip install torchvision numpy Pillow tqdm opencv-python
```

### 常用命令

#### 1. VOC 转 COCO
```bash
python py/voc2coco.py -v ../datasets/voc -c ../datasets/voc2coco -l train-2007 val-2007 test-2007 train-2012 val-2012
```
- `-v`：VOC 数据集根路径
- `-c`：COCO 格式输出路径
- `-l`：要处理的数据集列表（支持 train-2007, val-2007, test-2007, trainval-2007, train-2012, val-2012, trainval-2007）

#### 2. VOC 转 YOLOv5
```bash
python py/voc2yolov5.py -s ../datasets/voc -d ../datasets/voc2yolov5-train -l trainval-2007 trainval-2012
python py/voc2yolov5.py -s ../datasets/voc -d ../datasets/voc2yolov5-val -l test-2007
```
- `-s`：源数据集路径
- `-d`：目标输出路径
- `-l`：数据集列表

#### 3. VOCLike 转 YOLOv5
```bash
python py/voclike2yolov5.py ../datasets/voclike/JPEGImages ../datasets/voclike/Annotations voc.names ../datasets/voclike2yolov5
```
- 第一个参数：图像目录路径（JPEGImages）
- 第二个参数：标注目录路径（Annotations）
- 第三个参数：类别文件路径（如 voc.names）
- 第四个参数：YOLOv5 格式输出路径

#### 4. YOLOv5 转 VOCLike
```bash
python py/yolo2voclike.py ../datasets/yolov5 voc.names ../datasets/yolov52voclike
```
- 第一个参数：YOLOv5 数据根路径（包含 images/ 和 labels/ 目录）
- 第二个参数：类别文件路径（如 voc.names）
- 第三个参数：VOCLike 格式输出路径

#### 5. 提取类别列表
```bash
python py/find_classes.py ../../myai/mask/datasets/MaskDatasets/datasets/
```
- 第一个参数：VOCLike 数据根路径（包含 XML 标注文件）
- `--dst`：输出目录（默认为 ./output）

#### 6. 可视化标注
```bash
# 可视化 VOCLike 标注（单个文件）
python py/show_voclike_label.py assets/voclike/000006.jpg assets/voclike/000006.xml
# 可视化整个目录
python py/show_voclike_label.py assets/voclike/ assets/voclike/
# 保存标注图像到输出目录
python py/show_voclike_label.py assets/voclike/ assets/voclike/ --dst ./output/

# 可视化 YOLOLike 标注（单个文件）
python py/show_yololike_label.py assets/yololike/000000082986.jpg assets/yololike/000000082986.txt
# 可视化整个目录
python py/show_yololike_label.py assets/yololike/ assets/yololike/
# 保存标注图像到输出目录
python py/show_yololike_label.py assets/yololike/ assets/yololike/ --dst ./output/
```

### 注意事项
- 转换脚本默认使用 `voc.names` 作为类别文件，可通过 `--classes` 参数指定自定义文件
- VOC 数据集转换时，如果本地不存在数据集，`torchvision` 会自动下载（需要网络连接）
- 输出目录会自动创建，如果已存在会进行覆盖检查（使用 `assert` 防止意外覆盖）

## 开发规范

### 代码风格
- Python 文件使用 UTF-8 编码，带有 `# -*- coding: utf-8 -*-` 头
- 文档字符串包含作者、日期和描述
- 使用类型注解（`typing` 模块）
- 导入顺序：标准库 → 第三方库 → 本地模块

### Git 提交
- 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
- 示例：`feat(py/voc2coco.py): add support for VOC2012`
- 使用语义化版本控制（Semantic Versioning 2.0.0）

### 扩展开发
- 添加新脚本时，请参考现有脚本的结构
- 提供完整的命令行参数和帮助信息
- 在 README 中更新功能说明

## 架构说明

### 数据格式
1. **Pascal VOC**：标准 VOC 格式，使用 `torchvision.datasets.VOCDetection` 加载
2. **COCO**：遵循 COCO 的 JSON 格式，输出 `instances_{dataset}{year}.json`
3. **YOLOv5**：每个图像对应一个 `.txt` 文件，每行格式：`cls_id x_center y_center width height`（归一化坐标）
4. **VOCLike**：类似 VOC 但不完全相同，包含 `JPEGImages/` 和 `Annotations/` 目录

### 转换逻辑
- 所有转换脚本都使用类似的结构：`parse_args()` → `main()` → `process()`
- 忽略 `difficult=1` 的标注对象
- 坐标转换时进行归一化处理（YOLO 格式）
- 支持批量处理多个数据集（通过 `-l` 参数指定列表）

### 模块关系
- `dataset.py` 仅作为示例，实际使用 `torchvision` 的 `VOCDetection`
- `find_classes.py` 可独立使用，不依赖其他模块
- 可视化脚本依赖 OpenCV（`cv2`），如果未安装会自动跳过图像显示

## 故障排除

### 常见问题
1. **依赖缺失**：确保安装了 `torchvision`，它可能依赖 PyTorch
2. **数据集路径错误**：使用绝对路径或正确的相对路径
3. **类别不匹配**：确保自定义类别文件与标注中的类别名称一致
4. **内存不足**：处理大型数据集时可能需要分批处理

### 调试建议
- 使用小规模数据集测试
- 检查中间输出目录结构
- 查看脚本打印的详细参数信息

---

*本文件最后更新于 2026-03-06，基于仓库当前状态编写。*