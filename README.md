<div align="right">
  Language:
    🇺🇸
  <a title="Chinese" href="./README.zh-CN.md">🇨🇳</a>
</div>

<div align="center"><a title="" href="https://github.com/zjykzj/vocdev"><img align="center" src="./imgs/vocdev.png" alt=""></a></div>

> **⚠️ Repository Status: This repository is no longer actively maintained.**
>
> **🚀 Active development has moved to [DataFlow-CV](https://github.com/zjykzj/DataFlow-CV).**
>
> Please consider using the new repository for updated tools and support.

<p align="center">
  «vocdev» saved some documents, code, and tools for Pascal VOC
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square" alt=""></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg" alt=""></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg" alt=""></a>
</p>

* Convert VOC dataset to COCO format
  * [py/voc2coco.py](py/voc2coco.py)
* Convert VOC dataset to YOLOv5 format
  * [py/voc2yolov5.py](py/voc2yolov5.py)
* Convert VOCLike data to YOLOv5 format
  * [py/voclike2yolov5.py](py/voclike2yolov5.py)
* Convert YOLOv5 labels to Pascal VOC
  * [py/yolo2voclike.py](py/yolo2voclike.py)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Background](#background)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

[Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/) is a commonly used lightweight object identification and detection dataset. The purpose of creating this warehouse is to better use this dataset and save some commonly used implementations and documents here.

## Maintainers

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## Contributing

Anyone's participation is welcome! Open an [issue](https://github.com/zjykzj/vocdev/issues) or submit PRs.

Small note:

* Git submission specifications should be complied
  with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)
* If versioned, please conform to the [Semantic Versioning 2.0.0](https://semver.org) specification
* If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme)
  specification.

## License

[Apache License 2.0](LICENSE) © 2023 zjykzj