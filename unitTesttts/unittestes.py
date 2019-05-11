import unittest

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys

from unittest_ui import *
from transpiler import *


class QtTemplateWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent); self.ui = Ui_MainWindow(); self.ui.setupUi(self)

class TestEnv(unittest.TestCase):

	def setUp(self):

		# # make mini "qt app"
		# self.form, self.base = loadUiType('untitled.ui')
		# self.w, self.ui = self.base(), self.form()
		# self.ui.setupUi(self.w)
		# self.qt = self.ui.ui

		# ============
		# ============
		# ============

		# self.qt_app = QtWidgets.QApplication(sys.argv);
		# self.qt_ = MyWin()
		# myqapp.close()

		# ============
		# ============
		# ============

		self.qt_app = QtWidgets.QApplication(sys.argv)
		self.qt_ = QtTemplateWindow()
		self.qt = self.qt_.ui

	def gen_psg_ui_gridlayout(self, qt_wdiget:QGridLayout):
		# returns a string, containng a PySimpleGUI UI (in python language)
		if type(qt_wdiget) is not QGridLayout:
			raise Exception(f'Give me a QGridLayout, not {type(qt_wdiget)}')
		return compile_GridLayout(qt_wdiget, is_top=True)

	def gen_psg_ui_vbox(self, qt_wdiget:QVBoxLayout):
		# returns a string, containng a PySimpleGUI UI (in python language)
		if type(qt_wdiget) is not QVBoxLayout:
			raise Exception(f'Give me a QVBoxLayout, not {type(qt_wdiget)}')
		return compile_VBbox(qt_wdiget, is_top=True)

	#        _
	#       | |
	# __   _| |__   _____  __
	# \ \ / / '_ \ / _ \ \/ /
	#  \ V /| |_) | (_) >  <
	#   \_/ |_.__/ \___/_/\_\

	def test_vboxlayout_v1(self):
		true_ui = '''[
	[sg.I('Age', key='label_21'), sg.Spin((0, 99), initial_value=0, key='spinBox_5')],
	[sg.Frame('', key='frame_7', layout = [
			[sg.I('Age', key='label_23'), sg.Spin((0, 99), initial_value=0, key='spinBox_7')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_18'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_19')]
])],
	[sg.Checkbox('sex: male', default=False, key='checkBox_10'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_11')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_vbox(self.qt.v1))


	def test_vboxlayout_v2(self):

		true_ui = '''[
	[sg.I('Age', key='label_24'), sg.Spin((0, 99), initial_value=0, key='spinBox_8')],
	[sg.Frame('', key='frame_8', layout = [
			[sg.Frame('', key='gridLayout_6', layout = [
					[sg.I('first name 5', key='label_30'), sg.I('56', key='lineEdit_18')],
					[sg.Checkbox('sex: male', default=False, key='checkBox_26'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_27')],
					[sg.I(""), sg.RButton('submit', key='pushButton_9')]
		])]
])],
	[sg.Checkbox('sex: male', default=False, key='checkBox_24'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_25')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_vbox(self.qt.v2))

	#             _     _
	#            (_)   | |
	#   __ _ _ __ _  __| |
	#  / _` | '__| |/ _` |
	# | (_| | |  | | (_| |
	#  \__, |_|  |_|\__,_|
	#   __/ |
	#  |___/

	def test_gridlayout_g1(self):
		true_ui = '''[
	[sg.I('first name 5', key='label_31'), sg.I('56', key='lineEdit_17')],
	[sg.I(""), sg.Frame('', key='gridLayout_8', layout = [
			[sg.I('first name 5', key='label_33'), sg.I('56', key='lineEdit_19')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_29'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_28')],
			[sg.I(""), sg.RButton('submit', key='pushButton_10')]
])],
	[sg.Checkbox('sex: male', default=False, key='checkBox_22'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_23')],
	[sg.I(""), sg.RButton('submit', key='pushButton_7')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_gridlayout(self.qt.g1))


	def test_gridlayout_g2(self):
		true_ui = '''[
	[sg.I('first name 5', key='label_34'), sg.I('56', key='lineEdit_20')],
	[sg.Frame('', key='gridLayout_10', layout = [
			[sg.I('first name 5', key='label_35'), sg.I('56', key='lineEdit_21')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_33'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_32')],
			[sg.I(""), sg.RButton('submit', key='pushButton_12')]
]), sg.I("")],
	[sg.Checkbox('sex: male', default=False, key='checkBox_30'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_31')],
	[sg.I(""), sg.RButton('submit', key='pushButton_11')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_gridlayout(self.qt.g2))


	def test_gridlayout_g3(self):
		true_ui = '''[
	[sg.I('first name 5', key='label_28'), sg.I('56', key='lineEdit_14')],
	[sg.Frame('', key='gridLayout_4', layout = [
			[sg.I('first name 5', key='label_32'), sg.I('56', key='lineEdit_16')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_16'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_17')],
			[sg.I(""), sg.RButton('submit', key='pushButton_6')]
])],
	[sg.Checkbox('sex: male', default=False, key='checkBox_14'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_15')],
	[sg.I(""), sg.RButton('submit', key='pushButton_5')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_gridlayout(self.qt.g3))


	def test_gridlayout_g4(self):
		true_ui = '''[
	[sg.I('first name 5', key='label_29'), sg.I('56', key='lineEdit_15')],
	[sg.I(""), sg.Frame('', key='verticalLayout_3', layout = [
			[sg.I('Age', key='label_22'), sg.Spin((0, 99), initial_value=0, key='spinBox_6')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_12'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_13')]
])],
	[sg.Checkbox('sex: male', default=False, key='checkBox_20'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_21')],
	[sg.I(""), sg.RButton('submit', key='pushButton_8')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_gridlayout(self.qt.g4))


	def test_gridlayout_g5(self):
		true_ui = '''[
	[sg.I('first name 5', key='label_36'), sg.I('56', key='lineEdit_22')],
	[sg.Frame('', key='verticalLayout_7', layout = [
			[sg.I('Age', key='label_25'), sg.Spin((0, 99), initial_value=0, key='spinBox_9')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_36'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_37')]
]), sg.I("")],
	[sg.Checkbox('sex: male', default=False, key='checkBox_35'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_34')],
	[sg.I(""), sg.RButton('submit', key='pushButton_13')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_gridlayout(self.qt.g5))


	def test_gridlayout_g6(self):
		true_ui = '''[
	[sg.I('first name 5', key='label_37'), sg.I('56', key='lineEdit_23')],
	[sg.Frame('', key='verticalLayout_8', layout = [
			[sg.I('Age', key='label_26'), sg.Spin((0, 99), initial_value=0, key='spinBox_10')],
			[sg.Checkbox('sex: male', default=False, key='checkBox_40'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_41')]
])],
	[sg.Checkbox('sex: male', default=False, key='checkBox_39'), sg.Checkbox('Is Enterprenuer', default=False, key='checkBox_38')],
	[sg.I(""), sg.RButton('submit', key='pushButton_14')]
]'''
		self.assertEqual(true_ui, self.gen_psg_ui_gridlayout(self.qt.g6))


	# def test_vbox(self):
	# 	pass
	# def test_groupbox(self):
	# 	pass
	# def test_frame(self):
	# 	pass

if __name__ == '__main__':
	unittest.main()