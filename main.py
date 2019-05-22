from .boilerplate_psg import boilerplate_
from platform import system as gimme_system
from re import compile as regex, finditer
from shutil import copy as copyfile
import click
import json
import os
import PySimpleGUI as sg
import re
import subprocess
import sys
from .transpiler import *
cd = os.path.dirname(os.path.abspath(__file__))

def build_boilerplate(layout='[[]]', mouse_clicks=False, keys=False):
	# create a str with PSG code

	def do_callbacks(keys):
		return '\n'.join([f"\tif event == '{i}':\n\t\tpass" for i in keys])

	def do_mice_events(ui, boilerplate):
		# find regex pattern from all buttons
		regex_pattern = regex(
			r'(RButton|ReadButton|B)\([\'\"][\w\ \_\d]*[\'\"],?\s?((key)\s*=\s*[\'\"]([\w\ \_\d]+?)[\'\"])')
		# find all keys in you ui
		keys = [i.group(4) for i in finditer(regex_pattern, ui)]
		return boilerplate.replace('# ~TARGET', do_callbacks(keys))

	def do_keys_events(ui, boilerplate):
		# find regex pattern from all elements
		regex_pattern = regex(r'(key)\s*=\s*[\'\"]([\w\d]+?)[\'\"]')
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
	subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
	#              _
	#             (_)
	#   __ _ _   _ _
	#  / _` | | | | |
	# | (_| | |_| | |
	#  \__, |\__,_|_|
	#   __/ |
	#  |___/

	ralign = {'size': (5, 2), "justification": 'r'}
	input_frame = [[sg.T('xml\nfile', **ralign), 			sg.In(key='xmlfile', change_submits=True), sg.FileBrowse(target='xmlfile'), sg.InputCombo(values=[''], key='objs', size=(40,1), change_submits=True)],
				   # [)],
				   [sg.T('Target\nobject name', **ralign), 	sg.In(key='objname'),	  sg.B('compile'), sg.B('compile++'),
					sg.Radio('all keys', 1, True, key='r2_keys'), sg.Radio('mouse clicks', 1, key='r2_mouse_clicks')]]
	layout = [
		[sg.Frame('Input data', input_frame)],
		[sg.B('Clear'), sg.CB(
			'forget about bad widgets', True, key='no_bad_widgets')],
		[sg.Multiline(key='psg_ui_output', size=(120, 14))]
	]
	window = sg.Window('Transpiler', layout,
					   auto_size_buttons=False,
					   default_button_element_size=(10, 1))

	while True:             # Event Loop
		event, values = window.Read()
		# click.echo(event, values)

		if event == 'xmlfile':
			myxml_file = values['xmlfile']
			if os.path.exists(myxml_file):

				# get xml
				with open(myxml_file, 'r', encoding='utf-8') as ff: xml_code = ff.read()
				# filter object names
				listvalues = [i.group(1) for i in re.finditer(re.compile(r"^[ \s]{1,}<widget\s.*?\bname=\"(.+)\"\/?>", re.MULTILINE), xml_code)]
				# set it
				if listvalues:
					window.Element('objs').Update(values=
								[i
								for i in listvalues
								if  'label' != i[:6] and
									'pushButton' != i[:10]])

		if event in (None, 'Exit'):
			break
		if event == 'objs':
			window.Element('objname').Update(values['objs'])
		if event == 'Clear':
			window.Element('psg_ui_output').Update('')
		if event == 'compile':
			psg_ui = just_compile(values)
			window.Element('psg_ui_output').Update(psg_ui)
		if event == 'compile++':
			psg_ui = build_boilerplate(layout=just_compile(values),
									   mouse_clicks=values['r2_mouse_clicks'],
									   keys=values['r2_keys'])
			window.Element('psg_ui_output').Update(psg_ui)

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

	if run and not (xmlfile and objname): run_gui()
	elif xmlfile and objname:

		try:
			psg_ui = just_compile({'objname': objname,
				'xmlfile': xmlfile, 'no_bad_widgets': nobadwidgets })
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
