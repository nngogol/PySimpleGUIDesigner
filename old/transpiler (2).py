from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

IMPLEMENTED_CONTAINERS = [QGridLayout,
						  QVBoxLayout, QHBoxLayout, QGroupBox, QFrame]
IMPLEMENTED_CONTROL_ELEMENTS = [
	QLabel, QSpinBox, QCheckBox, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit]


def isCrate(item):
	return type(item) in IMPLEMENTED_CONTAINERS


def isNormalWidget(item):
	return type(item) in IMPLEMENTED_CONTROL_ELEMENTS


def empty_widget(GUItype='tk'):
	# dummy elemets for EMPTY SPOTS in QGridLayout
	if GUItype == 'tk':
		return 'sg.T("")'
	if GUItype == 'qt':
		return 'sg.HSep()'
	if GUItype == 'web':
		raise Exception("Not IMPLEMENTED")
	if GUItype == 'wx':
		raise Exception("Not IMPLEMENTED")


def get_chidrens(node):
	elements = []

	if type(node) in [QGroupBox, QFrame]:
		items = node.children()
		item_1st = items[0]
		if type(item_1st) in [QGridLayout, QHBoxLayout, QVBoxLayout]:
			return get_chidrens(item_1st)
		else:
			raise Exception(f'HOWTO find childrens in "{node.objectName()}" -> {node}')

	elif type(node) is QHBoxLayout or type(node) is QVBoxLayout:

		for i in range(node.count()):
			el = node.itemAt(i)
			obj = el.widget() if type(el) is QWidgetItem else el
			elements.append(obj)
		return elements

	elif type(node) is QGridLayout:

		for i in range(node.rowCount()):
			row = []
			for j in range(node.columnCount()):
				item = node.itemAtPosition(i, j)
				item = item.widget() if type(item) is QWidgetItem else item
				row.append(item)
			elements.append(row)
		return elements

	else:
		raise Exception(f'HOWTO find childrens in {type(node)}')


#                       _
#                      | |
#  _ __ ___   ___  __ _| |_
# | '_ ` _ \ / _ \/ _` | __|
# | | | | | |  __/ (_| | |_
# |_| |_| |_|\___|\__,_|\__|



def to_psg_element(normal_item, size='', GUItype='tk', pass_bad_widgets=False):

	if size != '' and type(size) in [tuple, list] and len(size) == 2:
		size = 'size=({0}, {1}), '.format(*size)
	elif size == '':
		pass
	else:
		raise Exception(f'BAD size: {size}')

	idd = normal_item.objectName()

	if type(normal_item) in [QVBoxLayout, QHBoxLayout]:
		ui = compile_VBbox(normal_item, is_top=False, make_tabs=2,
						   GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		return f"sg.Frame('', {size}key='{idd}', layout = [\n{ui}\n])"

	elif type(normal_item) is QFrame:
		children = normal_item.children()[0]
		if type(children) is QGridLayout:
			ui = compile_GridLayout(
				children,   make_tabs=2, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		if type(children) in [QVBoxLayout, QHBoxLayout]:
			ui = compile_VBbox(children,        make_tabs=2,
							   GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		return f"sg.Frame('', {size}key='{idd}', layout = [\n{ui}\n])"

	elif type(normal_item) is QGroupBox:
		children = normal_item.children()[0]
		if type(children) is QGridLayout:
			ui = compile_GridLayout(
				children,   make_tabs=2, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		if type(children) in [QVBoxLayout, QHBoxLayout]:
			ui = compile_VBbox(children,        make_tabs=2,
							   GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		return f"sg.Frame('', {size}key='{idd}', layout = [\n{ui}\n])"
		title = normal_item.title()
		return f"sg.Frame('{title}', {size}key='{idd}', layout = [\n{ui}\n])"

	elif type(normal_item) is QGridLayout:
		ui = compile_GridLayout(normal_item, is_top=False, make_tabs=2,
								GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
		return f"sg.Frame('', {size}key='{idd}', layout = [\n{ui}\n])"

	elif type(normal_item) is QLabel:
		text = normal_item.text()
		return f"sg.I('{text}', {size}key='{idd}')"

	elif type(normal_item) is QSpinBox:
		mina, maxa, curr = int(normal_item.minimum()), int(
			normal_item.maximum()), normal_item.value()
		return f"sg.Spin(list(range({mina}, {maxa})), initial_value={curr}, {size}key='{idd}')"

	elif type(normal_item) is QSlider:
		mina, maxa, curr = normal_item.minimum(), normal_item.maximum(), normal_item.value()
		orientation = 'h' if normal_item.orientation() == Qt.Horizontal else 'v'
		range_ = f'range=({mina}, {maxa}),'
		curr = f'default_value={curr},'
		orientation = f"orientation='{orientation}',"
		return f"sg.Slider({range_} {orientation} {curr} {size}key='{idd}')"

	elif type(normal_item) is QCheckBox:
		isChecked = str(normal_item.isChecked())
		text = normal_item.text()
		return f"sg.Checkbox('{text}', default={isChecked}, {size}key='{idd}')"

	elif type(normal_item) is QPushButton:
		text = normal_item.text()
		return f"sg.RButton('{text}', {size}key='{idd}')"

	elif type(normal_item) is QLineEdit:
		text = normal_item.text()
		return f"sg.I('{text}', {size}key='{idd}')"

	elif type(normal_item) is QTextEdit:
		text = normal_item.text()
		return f"sg.Multiline('{text}', {size}key='{idd}')"

	elif type(normal_item) is QPlainTextEdit:
		text = normal_item.toPlainText()
		return f"sg.Multiline('{text}', {size}key='{idd}')"

	elif type(normal_item) is QRadioButton:
		text, group_id = normal_item.text(), normal_item.toolTip()
		if not group_id:
			raise Exception(f"Set radio_group for {idd} as a toolTip text")
		return f"sg.Radio('{text}', '{group_id}', key='{idd}')"

	else:
		if pass_bad_widgets:
			return empty_widget(GUItype='tk')
		else:
			raise Exception(f"HOWTO compile {type(normal_item)}?")


# ▲
def compile_VBbox(parent_node: QVBoxLayout, is_top=False, make_tabs=-1, GUItype='tk', pass_bad_widgets=False):

	hbox_items = get_chidrens(parent_node)

	psg_rows = []
	for index, hbox_item in enumerate(hbox_items):

		res = type(hbox_item)

		if isNormalWidget(hbox_item) or type(hbox_item) is QGridLayout:

			el = '[' + to_psg_element(hbox_item, GUItype=GUItype,
									  pass_bad_widgets=pass_bad_widgets) + ']'
			psg_rows.append(el)

		elif type(hbox_item) is QHBoxLayout:

			elements = get_chidrens(hbox_item)
			psg_elemets = [to_psg_element(
				qt_widget, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets) for qt_widget in elements]
			el = '[' + ', '.join(psg_elemets) + ']'
			psg_rows.append(el)

		else:
			raise Exception(f'What is {type(hbox_item)}?')

	# ▲ 	Iterate thought grid
	my_tab = '\t'
	final = my_tab + f',\n{my_tab}'.join(psg_rows)

	space = ''
	if make_tabs != -1 and make_tabs > 0:
		space = my_tab * make_tabs
		final = '\n'.join([f'{space}{i}' for i in final.split('\n')])

	if is_top:
		# tabs
		if make_tabs != -1 and make_tabs > 0:
			return f'[\n{final}{space}\n]'
		else:
			return f'[\n{final}\n]'
	else:
		if make_tabs != -1 and make_tabs > 0:
			return final
		else:
			return space + final


# ▲
def compile_GridLayout(parent_node: QGridLayout, is_top=False, make_tabs=-1, GUItype='tk', pass_bad_widgets=False):

	def _get_widthedst_elements(myQGridLayout):

		# iterate thought grid
		cols = []
		for i in range(myQGridLayout.columnCount()):
			items = []
			for j in range(myQGridLayout.rowCount()):

				# get widget
				el = myQGridLayout.itemAtPosition(j, i)
				el = el.widget() if type(el) is QWidgetItem else el

				if el is not None:
					items.append([el, j])

			cols.append(items)
		# get list of widthest cols (list of integers)
		return [max([item.geometry().width()
					 for item in row_data[0]])
				for i, row_data in enumerate(cols)]

	# widthedst_elements = _get_widthedst_elements(parent_node)
	psg_elemets, psg_rows = [], []
	# ▲     Iterate thought grid
	for i in range(parent_node.rowCount()):
		psg_elemets = []
		for j in range(parent_node.columnCount()):
			# get widget
			res = parent_node.itemAtPosition(i, j)
			res = res.widget() if type(res) is QWidgetItem else res

			# this if means, that:
			# if current element is thesame as previuos element,
			# than current element has grid_span > 1,
			# and we don't need to parse,
			# because we already did it in previous step (loop step)
			if j > 0 and res == psg_elemets[-1][0]:
				continue

			if res is not None:
				# how can I use here this: size=(widthedst_elements[j],1)
				psg_elemets.append((res, to_psg_element(
					res, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)))
			else:
				# add dummy "empty lable"
				psg_elemets.append((res, empty_widget(GUItype=GUItype)))

		el = '[' + ', '.join([i[1] for i in psg_elemets]) + ']'
		psg_rows.append(el)

	# ▲     Add tabulation. I use tab, not 4 spaces
	my_tab = '\t'
	final = my_tab + f',\n{my_tab}'.join(psg_rows)
	# tabs
	space = ''
	if make_tabs != -1 and make_tabs > 0:
		space = my_tab * make_tabs
		final = '\n'.join([f'{space}{i}' for i in final.split('\n')])

	if is_top:
		if make_tabs != -1 and make_tabs > 0:
			return f'[\n{final}{space}\n]'
		else:
			return f'[\n{final}\n]'
	else:
		if make_tabs != -1 and make_tabs > 0:
			return final
		else:
			return space + final
