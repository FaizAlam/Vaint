# Vaint - Virtual Air Painter

![Vaint](https://socialify.git.ci/FaizAlam/Vaint/image?description=1&descriptionEditable=Virtual%20Air%20Painter&font=Inter&forks=1&language=1&name=1&owner=1&pattern=Plus&stargazers=1&theme=Light)

This is an application that enables one to **vitually paint in the air** using their fingers. It is developed in python **on openCV and Mediapipe**.
So go ahead and recreate your imaginations in the air !


[![Made with Python](https://img.shields.io/badge/Made%20with%20-Python-red?style=for-the-badge&logo=python)](http://www.python.org/)
[![GitHub followers](https://img.shields.io/github/followers/FaizAlam?label=Follow&style=social)](https://github.com/FaizAlam?tab=followers) [![GitHub stars](https://img.shields.io/github/stars/FaizAlam/Vaint?color=red&style=flat-square)](https://github.com/FaizAlam/Vaint/stargazers)
### Cloning
Use the link below to close this repository to your machine.
```bash
$ https://github.com/FaizAlam/Vaint.git
```
## Directory Contents
```bash
$ cd Vaint/
$ tree
.
├── Header
    ├── 1.png
    ├── 2.png
    ├── 3.png
    └── 4.png    
├── __pycache__
├── templates
    └── index.html
├── README.md
├── app.py
├── cam.py
├── VirtualPainter.py
├── HandTrackingModule.py
└── requirements.txt


```

### Pre-requisites
These are the required dependencies needed to setup the environment
```
$ pip3 install -r requirements.txt
```
### Instructions
> 1. To run on local machine **without a Flask server**.
```bash
$ python3 run VirtualPainter.py
```
> 2. To run as a local host on a **Flask server**.
>- Run the Flask app
```bash
$ python3 run app.py
```
>- On your phone's browser enter your machine's ip and port 5000. Say ip is 192.168.1.1.
```
192.168.1.1:5000
```

### Usage:
- Use your index finger to draw.
- To change color/ use eraser, use index and middle fingers to select it by hovering on it.
- Enjoy painting !








