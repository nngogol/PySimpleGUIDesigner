from boilerplate_psg import boilerplate_
from platform import system as gimme_system
from re import compile as make_regex, finditer, MULTILINE
from shutil import copy as copyfile
import click
import json
import os
import re
import sys
import subprocess
import PySimpleGUI as sg
from transpiler import *
cd = os.path.dirname(os.path.abspath(__file__))


def build_boilerplate(layout='[[]]', mouse_clicks=False, keys=False):
	# create a str with PSG code

	def do_callbacks(keys):
		return '\n'.join([f"\tif event == '{i}':\n\t\tpass" for i in keys])

	def do_mice_events(ui, boilerplate):
		# find regex pattern from all buttons
		regex_pattern = make_regex(
			r'(RButton|ReadButton|B)\([\'\"][\w\ \_\d]*[\'\"],?\s?((key)\s*=\s*[\'\"]([\w\ \_\d]+?)[\'\"])')
		# find all keys in you ui
		keys = [i.group(4) for i in finditer(regex_pattern, ui)]
		return boilerplate.replace('# ~TARGET', do_callbacks(keys))

	def do_keys_events(ui, boilerplate):
		# find regex pattern from all elements
		regex_pattern = make_regex(r'(key)\s*=\s*[\'\"]([\w\d]+?)[\'\"]')
		# find all keys in you ui
		keys = [i.group(2) for i in finditer(regex_pattern, ui)]
		return boilerplate.replace('# ~TARGET', do_callbacks(keys))

	if not mouse_clicks and not keys:
		text = boilerplate_
	elif mouse_clicks:
		text = do_mice_events(layout, boilerplate_)
	elif keys:
		text = do_keys_events(layout, boilerplate_)

	return text.replace('[[]]', layout)


def just_compile(values):
	#
	# compile "XML_file + object_name" to "PSG ui"
	#
	OBJ_NAME, inputXMLui, NO_BAD_WIDGETS = values['objname'], values['xmlfile'], values['no_bad_widgets']
	# make absolute path, if just filename given
	if '/' not in inputXMLui and '\\' not in inputXMLui:
		inputXMLui = os.path.join(cd, inputXMLui)

	# validation
	inputXMLui = inputXMLui if inputXMLui[:2] != '~/' else os.path.join(
		os.environ['HOME'], inputXMLui[2:])

	python = 'python'
	if gimme_system() == 'Linux':
		python += '3'

	# idea is simple:
	# 1 copy input ui file to .
	# 2 run "psg_ui_maker.py" -> it will compile inputXMLui, and give output in RESULTPSG file
	# 3 rm   input ui file from .
	# 4 read output of rm   input ui file from .

	# 1
	ui_file = os.path.join(cd, 'tmp_untitled.ui')
	copyfile(inputXMLui, ui_file)
	# 2
	psg_ui_maker__py = os.path.join(cd, 'psg_ui_maker.py')
	NO_BAD_WIDGETS = '1' if NO_BAD_WIDGETS else '0'
	command = '{0} "{1}" {2} {3}'.format(
		python, psg_ui_maker__py, OBJ_NAME, NO_BAD_WIDGETS)
	subprocess.run(command, shell=True, stdout=subprocess.DEVNULL,
				   stderr=subprocess.DEVNULL)
	# 3
	os.remove(ui_file)
	# 4
	RESULTPSG = os.path.join(cd, 'result_psg.ui')
	if not os.path.exists(RESULTPSG):
		return f'error, no obj_name="{OBJ_NAME}"" found'

	with open(RESULTPSG, 'r', encoding='utf-8') as ff:
		content = ff.read()
	os.remove(RESULTPSG)

	return content


def run_gui():
	def clear_empty_top_widget(ui):
		'''
		clear ui to easyily for coping functionality (ctrl+c)
		'''

		'''
		# case1
		sg.Frame('', key='gridLayout', layout = [
					[sg.RButton('PushButton', key='pushButton'), sg.RButton('PushButton', key='pushButton_2')]
		])
		'''
		first_line = ui.split('\n')[0]
		regex_matched = make_regex(
			r"^sg.Frame\('',\s?key='.*',\slayout\s=\s\[").match(first_line)
		if regex_matched and ui[-2:] == '])':
			new_ui = '[\n' + '\n'.join(ui.split('\n')[1:]).strip()
			return new_ui[:-1]
		return ui

	def update_clear_btn(my_window, my_values, real_value=''):
		objname = my_values['objname'] if real_value == '' else real_value
		all_object_names_in_combo = my_window.Element('objs').Values

		if my_values['xmlfile'] and objname and objname in all_object_names_in_combo:
			my_window.Element('compile_btn').Update(disabled=False)
			my_window.Element('compilepp_btn').Update(disabled=False)
		else:
			my_window.Element('compile_btn').Update(disabled=True)
			my_window.Element('compilepp_btn').Update(disabled=True)
	#              _
	#             (_)
	#   __ _ _   _ _
	#  / _` | | | | |
	# | (_| | |_| | |
	#  \__, |\__,_|_|
	#   __/ |
	#  |___/

	ralign = {'size': (16, 3), "justification": 'r'}
	input_frame = [[sg.T('\nxml file', **ralign),                   sg.In(key='xmlfile', change_submits=True),  sg.FileBrowse(target='xmlfile'),    sg.T('possible\nobject names', justification='r'), sg.InputCombo(values=[''], key='objs', size=(40, 1), change_submits=True)],
				   [sg.T('\nTarget object name', **ralign),         sg.In(key='objname', change_submits=True),  sg.B('compile', key='compile_btn', disabled=True), sg.B('compile++', key='compilepp_btn', disabled=True),
					sg.Radio('all keys', 1, True, key='r2_keys'),   sg.Radio('mouse clicks', 1, key='r2_mouse_clicks')]]
	layout = [
		[sg.Frame('Input data', input_frame)],
		[sg.B('Clear'),
		 sg.CB('forget about bad widgets', True, key='no_bad_widgets'),
		 sg.CB('empty top widget', True, key='empty_top_widget')],
		[sg.Multiline(key='psg_ui_output', size=(120, 14))]
	]
	window = sg.Window('Transpiler', layout,
					   auto_size_buttons=False,
					   default_button_element_size=(10, 1))

	while True:             # Event Loop
		event, values = window.Read()

		if event in (None, 'Exit'):
			break
		elif event == 'xmlfile':
			myxml_file = values['xmlfile']
			if os.path.exists(myxml_file):

				# get xml
				with open(myxml_file, 'r', encoding='utf-8') as ff:
					xml_code = ff.read()

				# filter object names
				widgets_regexpattern = make_regex(
					r"^[ \s]{1,}<(widget)\s?.*?\s?name=\"(.+)\"\/?>", MULTILINE)
				layouts_regexpattern = make_regex(
					r"^[ \s]{1,}<(layout)\s?.*?\s?name=\"(.+)\"\/?>", MULTILINE)
				widgets = [i.group(2) for i in finditer(
					widgets_regexpattern, xml_code)]
				layouts = [i.group(2) for i in finditer(
					layouts_regexpattern, xml_code)]

				combo_items = ['# LAYOUTS widgets #', *layouts, '# WIDGETS widgets #', *widgets]

				# set it
				window.Element('objs').Update(values=combo_items)
				update_clear_btn(window, values)

				el = combo_items[1]
				if ' ' not in el:
					window.Element('objname').Update(el)
					update_clear_btn(window, values, real_value=el)

		elif event == 'objs':
			# add only REAL object names -> those, who not contain ' '
			if ' ' not in values['objs']:
				window.Element('objname').Update(values['objs'])
			update_clear_btn(window, values, real_value=values['objs'])
		elif event == 'objname':
			update_clear_btn(window, values)
		elif event == 'Clear':
			window.Element('psg_ui_output').Update('')
		elif event == 'compile_btn':
			ui = just_compile(values)

			if values['empty_top_widget']:
				ui = clear_empty_top_widget(ui)

			window.Element('psg_ui_output').Update(ui)
		elif event == 'compilepp_btn':
			ui = just_compile(values)

			# case for 'speed up'
			# psg_ui_output = values['psg_ui_output']
			# ui = ... psg_ui_output ...

			ui = just_compile(values)

			if values['empty_top_widget']:
				ui = clear_empty_top_widget(ui)

			psg_ui = build_boilerplate(layout=ui,
									   mouse_clicks=values['r2_mouse_clicks'],
									   keys=values['r2_keys'])
			window.Element('psg_ui_output').Update(psg_ui)

		elif event == 'Try in PySimpleGUI':
			pass
		#   try:
		#       ui = values['psg_ui_output'].strip()

		#       if ui[:18] == "sg.Frame('', key='" and ui[-2:] == "])":
		#           ui = ui[ui.index('['):-1]
		#       elif ui[0] == "[" and ui[-1] == "]":
		#           pass

		#       window2 = sg.Window('test', myui)
		#       window2.Read()
		#       window2.Close()

		#   except Exception as e:
		#       mbox(str(e))

	window.Close()


@click.command()
@click.option('-x', '--run', default=True, is_flag=True, help='just run gui example')
@click.option('-xmlfile', type=click.Path(exists=True), help='abs path to ui file')
@click.option('-objname', type=str, help='object name of target container')
@click.option('-nobadwidgets', default=True, is_flag=True, help='forget about bad widgets. Default - True')
@click.option('-o', '--outputfile', type=click.Path(), help='file to output compiled PySimpleGUI ui')
@click.option('-pp_mouse', default=False, is_flag=True, help='compile++ option - do the mouse clicks events')
@click.option('-pp_keys',  default=False, is_flag=True, help='compile++ option - do the keys events')
def cli(run, xmlfile, objname, nobadwidgets, outputfile, pp_mouse, pp_keys):

	if run and not (xmlfile and objname):
		run_gui()
	elif xmlfile and objname:

		try:
			psg_ui = just_compile({'objname': objname,
								   'xmlfile': xmlfile, 'no_bad_widgets': nobadwidgets})
			# compile++
			if pp_mouse:
				psg_ui = build_boilerplate(layout=psg_ui, mouse_clicks=True)
			elif pp_keys:
				psg_ui = build_boilerplate(layout=psg_ui, keys=True)

			# output
			if outputfile:
				with open(outputfile, 'w', encoding='utf-8') as ff:
					ff.write(psg_ui)
			else:
				click.echo(psg_ui)
			# click.echo(click.style("\n~~~done", bg='black', fg='green'))
		except Exception as e:
			click.echo(click.style(str(e), bg='black', fg='red'))


if __name__ == '__main__':
	cli()
