#! /bin/bash

# qt untitled.ui
PySimpleGUIDesigner -xmlfile="./untitled.ui" -objname="v1" > psg.py

# generate png

cat psg.py
# python3 make_img.py