# NOT USED
maker_py = '''from PyQt5 import QtCore, QtGui, QtWidgets; from PyQt5.QtCore import *; from PyQt5.QtWidgets import *; from PyQt5.QtGui import *;
from xml_ui import *; from transpiler import *; import sys, os


# make qt app, q main window, qt layout (from pyuic)
qapp, myqapp, ui = QApplication(sys.argv), QMainWindow(), Ui_MainWindow()
ui.setupUi(myqapp) # join ui

qt_widget = ui.TARGET_OBJECT_NAME

# make psg_ui
if type(qt_widget) is QVBoxLayout: pysimplegui_ui = compile_VBbox2(qt_widget, is_top=True)
if type(qt_widget) is QGridLayout: pysimplegui_ui = compile_Form2(qt_widget, is_top=True)

# write psg_ui
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'psg_ui.txt'), 'w', encoding='utf-8') as ff:
	ff.write(pysimplegui_ui)'''