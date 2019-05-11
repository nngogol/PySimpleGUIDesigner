from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from untitled import *
from transpiler import *
from qu import *
import sys, os, re, shutil, random

def gen_name(target_folder, range_=(500, 10000), prefix='tmp', suffix=''):
	'''
	make a random name, base on given target_folder
	range_ in random number from given range, appended to filename

	returns random_int_appended_to_filename, random_filename
	'''
	rand_num = random.randint(*range_)
	
	name = os.path.join(target_folder, f'{prefix}{rand_num}{suffix}')

	if not os.path.exists(name):
		return rand_num, name
	else:
		attemps = 0
		while not os.path.exists(name):
			attemps+=1
			rand_num = random.randint(*range_)
			name = os.path.join(target_folder, f'{prefix}{rand_num}{suffix}')

			if attemps > 10000:
				raise Exception("Can't generate valid name")
		return rand_num, name

def build_boilerplate(layout='[[]]', mouse_clicks=False, keys=False):

	def do_mice_events(ui, boilerplate):
		regex_pattern = re.compile(r'(RButton|ReadButton)\([\'\"][\w\ \_\d]*[\'\"],?\s?((key)\s*=\s*[\'\"]([\w\ \_\d]+?)[\'\"])')
		keys = [i.group(4) for i in re.finditer(regex_pattern, ui)]
		callbacks = '\n'.join([f"\tif event == '{i}':\n\t\tpass" for i in keys])
		return boilerplate.replace('mice', callbacks)

	def do_keys_events(ui, boilerplate):
		regex_pattern = re.compile(r'(key)\s*=\s*[\'\"]([\w\d]+?)[\'\"]')
		keys = [i.group(2) for i in re.finditer(regex_pattern, ui)]
		callbacks = '\n'.join([f"\tif event == '{i}':\n\t\tpass" for i in keys])
		return boilerplate.replace('keys', callbacks)

	def rread_file(fname):
		with open(f'resources/boilerplate_{fname}.py', 'r', encoding='utf-8') as ff:
			return ff.read()

	
	if not mouse_clicks and not keys:
		text = rread_file('basic').replace('[[]]', layout)
	elif mouse_clicks:
		text = do_mice_events(layout, rread_file('clicks')).replace('[[]]', layout)
	elif keys:
		text = do_keys_events(layout, rread_file('keys')).replace('[[]]', layout)
		
	return text


class MyWin(QtWidgets.QMainWindow):
	ENABLE_SAVE_INPUTFIELDS_VALUES = True
	EXPAND_PSG_OUTPUT = False

	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.setWindowTitle('Transpiler')
		# ====

		def expand_psg_output_clicked():
			self.EXPAND_PSG_OUTPUT = not self.EXPAND_PSG_OUTPUT
			if self.EXPAND_PSG_OUTPUT:
				self.ui.main_input_data.setMaximumHeight(16777214)
				self.ui.examples_tabs.setMaximumHeight(20)
			else:
				self.ui.main_input_data.setMinimumHeight(220)
				self.ui.examples_tabs.setMaximumHeight(16777214)

		def browse_input_file_clicked():
			mypath = QFileDialog.getOpenFileName(self, 'Select file', '', 'Any files (*.*)')[0]
			if mypath != '' and os.path.exists(mypath):
				setv(self.ui.input__file, mypath)

		def compile_clicked():
			# dynamic compile

			input__file = getv(self.ui.input__file)
			target_object_name = getv(self.ui.target_object_name)
			pass_bad_widgets = getv(self.ui.pass_bad_widgets)

			GUItype = 'tk'
			if getv(self.ui.guitype_web): 	GUItype = 'web'
			if getv(self.ui.guitype_qt): 	GUItype = 'qt'
			if getv(self.ui.guitype_wx): 	GUItype = 'wx'

			# make mini "qt app"


			xml_ui_file = QFile(input__file)
			xml_ui_file.open(QFile.ReadOnly)
			ui = QUiLoader().load(xml_ui_file)

			# from PySide2.uic import loadUiType
			# form, base = loadUiType(input__file)
			# w, ui = base(), form()
			# ui.setupUi(w)

			try:
				# make psg_ui
				target_widget = getattr(ui, target_object_name)
				# compile
				psg_ui = to_psg_element(target_widget, # is_top=True,
						GUItype=GUItype, 
						pass_bad_widgets=pass_bad_widgets)
				# output psg gui
				setv(self.ui.psg_ui_output, psg_ui)

			except Exception as e:
				self.mbox(str(e))
				return

		def compile_full_clicked():
			compile_clicked()

			setv(self.ui.psg_ui_output, build_boilerplate(layout=getv(self.ui.psg_ui_output),
				 mouse_clicks=getv(self.ui.mouse_clicks_), keys=getv(self.ui.keys_)))

		def try_run_clicked():

			if getv(self.ui.guitype_tk): 
				import PySimpleGUI as sg
			if getv(self.ui.guitype_web): 
				import PySimpleGUIWeb as sg
			if getv(self.ui.guitype_qt): 
				import PySimpleGUIQt as sg
			if getv(self.ui.guitype_wx): 
				import PySimpleGUIWx as sg

			try:
				layout = eval(getv(self.ui.psg_ui_output))

				window = sg.Window('App').Layout(layout)
				window.Read()
				window.Close()
			except Exception as e:
				self.mbox(str(e))
				return

		QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(lambda : expand_psg_output_clicked())
		QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
		self.ui.clear_psg_output.clicked.connect(lambda : self.ui.psg_ui_output.clear())
		self.ui.compile_.clicked.connect(compile_clicked)
		self.ui.compile_pp.clicked.connect(compile_full_clicked)
		self.ui.expand_psg_output.clicked.connect(expand_psg_output_clicked)
		self.ui.file__browse.clicked.connect(browse_input_file_clicked)
		self.ui.try_run_.clicked.connect(try_run_clicked)
		if self.ENABLE_SAVE_INPUTFIELDS_VALUES:
			self.settings = QSettings('PSG_designer', 'Gicompany', self)
			self.loadS()
		# QTimer.singleShot(0, lambda : self.close())

	def mbox(self, body, title='Error'):
		dialog = QMessageBox(QMessageBox.Information, title, body)
		dialog.exec_()

	def closeEvent(self, e):
		if self.ENABLE_SAVE_INPUTFIELDS_VALUES:
			self.saveS()
		e.accept()
		
	def loadS(self):
		if self.settings.contains('input__file'): setv(self.ui.input__file, self.settings.value('input__file'))
		if self.settings.contains('target_object_name'): setv(self.ui.target_object_name, self.settings.value('target_object_name'))
		if self.settings.contains('psg_ui_output'): setv(self.ui.psg_ui_output, self.settings.value('psg_ui_output'))

	def saveS(self):
		self.settings.setValue('input__file',  getv(self.ui.input__file))
		self.settings.setValue('target_object_name',  getv(self.ui.target_object_name))
		self.settings.setValue('psg_ui_output',  getv(self.ui.psg_ui_output))

if __name__ == "__main__":
	# normal
	qapp = QtWidgets.QApplication(sys.argv); myqapp = MyWin(); myqapp.show(); sys.exit(qapp.exec_())

	# quick
	# qapp = QtWidgets.QApplication(sys.argv); myqapp = MyWin(); myqapp.close()



# # NOT USED
# def compile1_clicked():
# 	try:
# 		# # # 	
# 		# # # 	1 take xml_ui.xml from user
# 		# # # 	2 mkdir tmpXXX
# 		# # # 	3.1 cp xml_ui.xml     ./tmpXXX/xml_ui.xml
# 		# # # 	3.2 cp .transpiler.py ./tmpXXX/transpiler.py
# 		# # # 	4 pyuic -> produce .py version of xml
# 		# # # 	5 touch ./tmpXXX/main.py  OR cp maker.py ./tmpXXX/maker.py
# 		# # # 		load xml_ui.py into qt app
# 		# # # 		compile to psg
# 		# # # 		output result into res.txt
# 		# # # 	6 run main.py
# 		# # # 	7 read res.py
# 		# # # 	8 output res.py result into GUI
# 		# # # 	

# 		# 1
# 		target_object_name = getv(self.ui.target_object_name)
# 		xmlfile = getv(self.ui.input__file)

# 		# 2
# 		Xindex, tmp_folder = gen_name(os.path.join(os.path.dirname(os.path.abspath(__file__))), prefix = f'tmp_')
# 		os.mkdir(tmp_folder)

# 		# 3
# 		tmp__xml_ui_xml, tmp__xml_ui_py = os.path.join(tmp_folder, 'xml_ui.ui'), os.path.join(tmp_folder, 'xml_ui.py')
# 		shutil.copy(xmlfile, tmp__xml_ui_xml)
# 		shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'transpiler.py'), os.path.join(tmp_folder, 'transpiler.py'))
# 		# 4
# 		os.system('py -m PySide2.uic.pyuic -x "{0}" -o "{1}"'.format(tmp__xml_ui_xml, tmp__xml_ui_py))

# 		# 5
# 		tmp__main_py = os.path.join(tmp_folder, 'main.py')

# 		with open(tmp__main_py, 'w', encoding='utf-8') as ff2:
# 			ff2.write(maker_py.replace('TARGET_OBJECT_NAME', target_object_name))
# 		# 6
# 		os.system(f'py "{tmp__main_py}"')

# 		# 7
# 		with open(os.path.join(tmp_folder, 'psg_ui.txt'), 'r', encoding='utf-8') as ff:
# 			psg_ui = ff.read()

# 		# 8
# 		setv(self.ui.psg_ui_output, psg_ui)



# 	except Exception as e:
# 		print(str(e))
