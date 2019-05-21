from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from transpiler import *
import sys
import os

class MyWin(QtWidgets.QMainWindow):
	def __init__(self, object_name):
		super().__init__(None)

		cd = os.path.dirname(os.path.abspath(__file__))
		xml_ui_file = QFile(os.path.join(cd, 'tmp_untitled.ui'))
		xml_ui_file.open(QFile.ReadOnly)

		ui = QUiLoader().load(xml_ui_file)

		no_bad_widgets = sys.argv[2] == '1'
		psg_ui = to_psg_element(getattr(ui, object_name), pass_bad_widgets=no_bad_widgets) # compile | is_top=True, # GUItype=None,

		result_psg_ui = os.path.join(cd, 'result_psg.ui')
		with open(result_psg_ui, 'w', encoding='utf-8') as ff:
			ff.write(psg_ui)


if __name__ == "__main__":
	qapp = QtWidgets.QApplication(sys.argv)
	myqapp = MyWin(sys.argv[1])
	myqapp.close()


