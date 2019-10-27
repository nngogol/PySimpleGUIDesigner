from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from transpiler2 import *
import sys
import os
import PySimpleGUI as sg


class MyWin(QtWidgets.QMainWindow):
	def __init__(self, object_name):
		super().__init__(None)

		# get path to files
		cd = os.path.dirname(os.path.abspath(__file__))
		tmp_untitled = os.path.join(cd, 'tmp_untitled.ui')
		result_psg_ui = os.path.join(cd, 'result_psg.layout')
		
		try:

			# READ xml-UI into python-qt object
			xml_ui_file = QFile(tmp_untitled)
			xml_ui_file.open(QFile.ReadOnly)
			ui = QUiLoader().load(xml_ui_file)


			# convert to psg
			no_bad_widgets = sys.argv[2] == '1'
			psg_ui = optimize_psg_code(to_psg_element(
				getattr(ui, object_name), pass_bad_widgets=no_bad_widgets))

			# output psg code to file
			with open(result_psg_ui, 'w', encoding='utf-8') as ff:
				ff.write(psg_ui)

		except Exception as e:

			message = 'Error:   \n' + str(e)
			if '''PySide2.QtWidgets.QMainWindow' object has no attribute''' in str(e):
				message = 'Error:   \nElement with "object name"="' + object_name + '" not found'
			
			# output psg code to file
			with open(result_psg_ui, 'w', encoding='utf-8') as ff:
				ff.write(message)

			return message


if __name__ == "__main__":
	qapp = QtWidgets.QApplication(sys.argv)
	myqapp = MyWin(sys.argv[1])
	myqapp.close()
