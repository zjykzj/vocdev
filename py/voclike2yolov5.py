# -*- coding: utf-8 -*-

"""
@Time    : 2023/11/18 20:08
@File    : voclike2yolov5.py
@Author  : zj
@Description:

Usage: Convert YOLOv5 labels to Pascal VOC:
    $ python3 py/voclike2yolov5.py assets/voclike assets/voclike ./voc.names ./output/yolo_data/

For /path/to/classes, the file content is as follows:

    person
    ...

For /path/to/yolov5_data/, the file structure is as follows:

    yolov5_data/
        images/
            aaaa.jpg
            bbbb.jpg
        labels/
            aaaa.txt
            bbbb.txt

"""
from typing import Dict, List, Any

import os
import shutil
import argparse
import collections

import numpy as np
from tqdm import tqdm
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_args():
    parser = argparse.ArgumentParser(description="VOCLike2YOLOv5")
    parser.add_argument('image', metavar='IMAGE', type=str,
                        help='Image root.')
    parser.add_argument('label', metavar='LABEL', type=str,
                        help='Label path.')
    parser.add_argument("classes", metavar='CLASSES', type=str,
                        help="Classes path.")

    parser.add_argument('dst', metavar='DST', type=str,
                        help='YOLOv5 data root path.')
    args = parser.parse_args()
    print("args:", args)
    return args


def voc2yolov5_label(target: Dict, cls_list: List):
    img_w = int(target['annotation']['size']['width'])
    img_h = int(target['annotation']['size']['height'])

    label_list = list()
    for obj in target['annotation']['object']:
        difficult = int(obj['difficult'])
        if difficult != 0:
            continue
        cls_name = obj['name']
        assert cls_name in cls_list, cls_name
        xmin = float(obj['bndbox']['xmin'])
        ymin = float(obj['bndbox']['ymin'])
        xmax = float(obj['bndbox']['xmax'])
        ymax = float(obj['bndbox']['ymax'])

        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2
        box_w = xmax - xmin
        box_h = ymax - ymin
        # [x1, y1, x2, y2] -> [cls_id, x_center/img_w, y_center/img_h, box_w/img_w, box_h/img_h]
        label_list.append(
            [cls_list.index(cls_name), x_center / img_w, y_center / img_h, box_w / img_w, box_h / img_h])

    return label_list


def parse_voc_xml(node: ET.Element) -> Dict[str, Any]:
    voc_dict: Dict[str, Any] = {}
    children = list(node)
    if children:
        def_dic: Dict[str, Any] = collections.defaultdict(list)
        for dc in map(parse_voc_xml, children):
            for ind, v in dc.items():
                def_dic[ind].append(v)
        if node.tag == "annotation":
            def_dic["object"] = [def_dic["object"]]
        voc_dict = {node.tag: {ind: v[0] if len(v) == 1 else v for ind, v in def_dic.items()}}
    if node.text:
        text = node.text.strip()
        if not children:
            voc_dict[node.tag] = text
    return voc_dict


def load_voc_data(image_dir: str, label_dir: str):
    assert os.path.isdir(image_dir) and os.path.isdir(label_dir), "Image and label directories must exist"

    image_list = list()
    xml_list = list()
    print(f"Retrieval {label_dir}")
    for xml_path in Path(label_dir).rglob(pattern="*.xml"):
        image_path = str(xml_path).replace(label_dir, image_dir).replace(".xml", ".jpg")
        assert os.path.isfile(image_path), image_path

        image_list.append(image_path)
        xml_list.append(xml_path)

    return image_list, xml_list


def main(args):
    save_root = args.dst
    dst_image_root = os.path.join(save_root, "images")
    if not os.path.exists(dst_image_root):
        os.makedirs(dst_image_root)
    dst_label_root = os.path.join(save_root, "labels")
    if not os.path.exists(dst_label_root):
        os.makedirs(dst_label_root)

    class_path = args.classes
    dst_class_path = os.path.join(save_root, os.path.basename(class_path))
    shutil.copyfile(class_path, dst_class_path)
    classes = np.loadtxt(class_path, dtype=str, delimiter=' ').tolist()
    if isinstance(classes, str):
        classes = [classes]

    image_list, xml_list = load_voc_data(args.image, args.label)
    for image_path, xml_path in tqdm(zip(image_list, xml_list), total=len(image_list)):
        # Image
        image_name = os.path.basename(image_path)
        dst_image_path = os.path.join(dst_image_root, image_name)
        shutil.copyfile(image_path, dst_image_path)

        # Label
        target = parse_voc_xml(ET.parse(xml_path).getroot())
        label_list = voc2yolov5_label(target, classes)

        label_name = os.path.basename(xml_path).replace(".xml", ".txt")
        dst_label_path = os.path.join(dst_label_root, label_name)
        np.savetxt(dst_label_path, label_list, fmt="%f", delimiter=' ')

    print(f"Save to {save_root}")


if __name__ == '__main__':
    args = parse_args()
    main(args)
