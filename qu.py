from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import datetime
import random

def getv(widget):
	type_w = type(widget)

	# qt models
	if type_w is QListView:
		index = widget.currentIndex().row()
		if index != -1:
			return widget.model()[index]
	if type_w is QTableView:
		index = self.widget.currentIndex().row()
		if index != -1:
			return widget.model()[index]
	# BOOL
	if type_w is QCheckBox:
		return widget.checkState() == 2
	if type_w is QRadioButton:
		return widget.isChecked()

	# NUM
	if type_w is QSlider:
		return widget.value()
	if type_w is QSpinBox:
		return widget.value()
	if type_w is QDoubleSpinBox:
		return widget.value()

	# TEXT
	if type_w is QLabel:
		return widget.text()
	if type_w is QPushButton:
		return widget.text()
	if type_w is QComboBox:
		return widget.currentText()
	if type_w is QLineEdit:
		return widget.text()
	if type_w is QPlainTextEdit:
		return widget.toPlainText()

	# DATE
	if type_w is QTimeEdit:
		return widget.time().toPyTime()
	if type_w is QDateEdit:
		return widget.date().toPyDate()
	if type_w is QDateTimeEdit:
		return widget.dateTime().toPyDateTime()


def setv(widget, val):
	type_w = type(widget)

	if val == None:
		return

	def bool_to_check(val):
		return 2 if val else 0

	# BOOL
	if isinstance(val, bool):
		if type_w is QCheckBox:
			widget.setCheckState(bool_to_check(val))
		elif type_w is QRadioButton:
			widget.setChecked(val)

	# NUMBER
	elif isinstance(val, int) or isinstance(val, float):

		if type_w is QLabel:
			widget.setText(str(val))
		elif type_w is QSlider:
			widget.setValue(val)
		elif type_w is QSpinBox:
			widget.setValue(val)
		elif type_w is QDoubleSpinBox:
			widget.setValue(val)

	# TEXT
	elif isinstance(val, str):

		if type_w is QLabel:
			widget.setText(val)
		elif type_w is QLineEdit:
			widget.setText(val)
		elif type_w is QPushButton:
			widget.setText(val)
		elif type_w is QPlainTextEdit:
			widget.setPlainText(val)

	# date
	elif type_w is QDateTimeEdit:
		widget.setDateTime(QDateTime(val))
	elif type_w is QDateEdit:
		if type(val) is datetime.date:
			widget.setTime(QTime(val.year, val.month, val.day))
		if type(val) is datetime.datetime:
			val = val.date()
			widget.setTime(QTime(val.year, val.month, val.day))
	elif type_w is QTimeEdit:

		if type(val) is datetime.time:
			widget.setTime(QTime(val.hour, val.minute, val.second))
		if type(val) is datetime.datetime:
			val = val.time()
			widget.setTime(QTime(val.hour, val.minute, val.second))
	else:
		raise Exception(f'{val} - value is wrong for {type_w}!')
