boilerplate_ = '''import PySimpleGUI as sg

layout = [[]]
window = sg.Window('App', layout)

while True:
	event, values = window.read()
	if event in (None, 'Exit'): break

	if event == '':
		pass

# ~TARGET

window.close()
'''