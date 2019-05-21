
#  _       _   __
# | |     | | /_ |
# | |_   _| |  | |
# | \ \ / / |  | |
# | |\ V /| |  | |
# |_| \_/ |_|  |_|

# # ▲
# def compile_VBbox(parent_node: QVBoxLayout):

# 	# hbox_rows = parent_node.children()
# 	# more secure
# 	hbox_rows = get_chidrens(parent_node)

# 	if any([(index, i) for index, i in enumerate(hbox_rows) if type(i) is not QHBoxLayout]):
# 		raise Exception('Ты сверстал в row\'ы неправильно.\nКакой-то елемент не обернут в вертикальный layout')

# 	psg_rows = []
# 	for index, hbox_row in enumerate(hbox_rows):
# 		elements = get_chidrens(hbox_row)
# 		psg_elemets = [ to_psg_element(qt_widget) for qt_widget in elements]
# 		el = '[' +  ', '.join(psg_elemets) + ']'
# 		psg_rows.append((index, hbox_row, el))

# 	final = '[' + ',\n'.join([i[2] for i in psg_rows]) + ']'
# 	return final

# # ▲
# def compile_Form(parent_node: QGridLayout):

# 	# if any([(index, i) for index, i in enumerate(hbox_rows) if type(i) is not QHBoxLayout]):
# 	# 	raise Exception('Ты сверстал в row\'ы неправильно.\nКакой-то елемент не обернут в вертикальный layout')

# 	psg_elemets = []
# 	psg_rows = []
# 	for i in range(parent_node.rowCount()):
# 		psg_elemets = []
# 		for j in range(parent_node.columnCount()):
# 			res = parent_node.itemAtPosition(i, j)
# 			res = res.widget() if type(res) is QWidgetItem else res
# 			if res:
# 				psg_elemets.append(to_psg_element(res))
# 			else:
# 				psg_elemets.append(empty_input_text())
# 		el = '[' +  ', '.join(psg_elemets) + ']'
# 		psg_rows.append(el)
	
# 	final = '[' + ',\n'.join(psg_rows) + ']'
# 	return final




# def to_psg_element2_original(normal_item, size=''):

# 	idd = ob(normal_item)

# 	if type(normal_item) is QFrame or type(normal_item) is QVBoxLayout:
# 		ui = compile_VBbox(normal_item, is_top=False, make_tabs=2)
# 		return f"sg.Frame('', key='{idd}', layout = [\n{ui}\n])"

# 	if type(normal_item) is QGridLayout:
# 		ui = compile_GridLayout(normal_item, is_top=False, make_tabs=2)
# 		return f"sg.Frame('', key='{idd}', layout = [\n{ui}\n])"

# 	if type(normal_item) is QLabel:
# 		text = normal_item.text()
# 		return f"sg.I('{text}', key='{idd}')"

# 	if type(normal_item) is QSpinBox:
# 		mina, maxa, curr = int(normal_item.minimum()), int(normal_item.maximum()), normal_item.value()
# 		return f"sg.Spin(list(range({mina}, {maxa})), initial_value={curr}, key='{idd}')"

# 	if type(normal_item) is QSlider:
# 		mina, maxa, curr = int(normal_item.minimum()), int(normal_item.maximum()), normal_item.value()
# 		orientation = 'h' if normal_item.orientation() == Qt.Horizontal else 'v'
# 		return f"sg.Slider(range=({mina}, {maxa}), orientation='{orientation}', default_value={curr}, key='{idd}')"

# 	if type(normal_item) is QCheckBox:
# 		isChecked = str(normal_item.isChecked())
# 		text = normal_item.text()
# 		return f"sg.Checkbox('{text}', default={isChecked}, key='{idd}')"

# 	if type(normal_item) is QPushButton:
# 		text = normal_item.text()
# 		return f"sg.RButton('{text}', key='{idd}')"

# 	if type(normal_item) is QLineEdit:
# 		text = normal_item.text()
# 		return f"sg.I('{text}', key='{idd}')"

# 	if type(normal_item) is QTextEdit:
# 		text = normal_item.text()
# 		return f"sg.Multiline('{text}', key='{idd}')"

# 	if type(normal_item) is QPlainTextEdit:
# 		text = normal_item.toPlainText()
# 		return f"sg.Multiline('{text}', key='{idd}')"
