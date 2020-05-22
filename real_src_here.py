#!/usr/bin/python3
# copy paste from all_in_one_imports
# from all_in_one_imports import *
from re import compile as make_regex, finditer, MULTILINE
import re, json, random, click, json, os, re, sys, subprocess
from platform import system as gimme_system
from shutil import copy as copyfile
import PySimpleGUI as sg
from hashlib import sha256

cd = os.path.dirname(os.path.abspath(__file__))

def file_hash(file_path):
    def readfile_bin(filename):
        with open(filename, 'rb') as ff:
            return ff.read()
    
    m = sha256()
    m.update(readfile_bin(file_path))
    return m.digest()

main_boilerplate = '''import PySimpleGUI as sg

layout = [[]]
window = sg.Window('App', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break

    if event == '':
        pass

# ~TARGET

window.close()
'''

def make_tab_indent(psg_code, indent_size=1, indent_char=' '):
    space_char = indent_char*indent_size
    result = []
    start_spaces_regex = re.compile(r'(^\s*)(.*?)$', flags=re.M | re.DOTALL)
    for curr_line in psg_code.split('\n'):
        stripped_line = curr_line.strip('\t')

        # if len(stripped_line) != len(curr_line):
        if curr_line.startswith('\t'):
            space_regex = list(re.finditer(start_spaces_regex, curr_line))[0]
            space_len = len(space_regex.group(1))
            result.append((space_char * space_len) + stripped_line)
        else:
            result.append(curr_line)

    return '\n'.join(result)

def build_boilerplate(layout='[[]]', btns_event=False, all_events=False):
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

    if not btns_event and not all_events:
        text = main_boilerplate
    elif btns_event:
        text = do_mice_events(layout, main_boilerplate)
    elif all_events:
        text = do_keys_events(layout, main_boilerplate)

    boilerplate_layout = text.replace('[[]]', layout)
    if 'layout = sg.Frame' in boilerplate_layout:
        replaces_pairs = [
            ('layout = sg.Frame', 'layout = [\n [sg.Frame'),
            ('''\nwindow = sg.Windo''', ''']]\nwindow = sg.Windo'''),
        ]
        for old_text, good_text in replaces_pairs:
            boilerplate_layout = boilerplate_layout.replace(old_text, good_text)

    return boilerplate_layout

def just_compile(values):

    #
    # compile "XML_file + object_name" to "PSG ui"
    #
    OBJ_NAME, inputXMLui, NO_BAD_WIDGETS = values['objname'], values['xmlfile'], values['no_bad_widgets']
    indent_size = int(values['indent_size'])
    indent_char = values['indent_char']
    


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
    # rm given file
    os.remove(ui_file)
    # 4
    # return psg code
    RESULTPSG = os.path.join(cd, 'result_psg.layout')
    if not os.path.exists(RESULTPSG):
        raise Exception(f'error, no obj_name="{OBJ_NAME}" found')
    content = readfile(RESULTPSG)
    os.remove(RESULTPSG)
    return make_tab_indent(content, indent_size=indent_size, indent_char=indent_char)

def writefile(fpath, content):
    with open(fpath, 'w', encoding='utf-8') as ff:
        ff.write(content)

def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as ff:
        return ff.read()

curr_lang = 'en'
langs = {
    'en': {
        # 'key' : 'text'

        # main
        ## labels:
        '_lbl_xml file' : 'xml file'
        ,'_lbl_target object name' : 'target object name'
        ,'_lbl_all object names' : 'all object names'
        ,'_lbl_options:' : 'options:'
        ## buttons:
        ,'convert_btn' : 'convert'
        ,'convert_all_events' : 'convert++\nall events'
        ,'convert_btns_events' : 'convert++\nbtns events'
        ,'no_bad_widgets' : 'try convert unknows widgets'

        # settings
        ,'-memento-file-cb-' : 'Remember path to previous file'
        ,'_lbl_indent_size' : 'Indent size'
        ,'_lbl_indent_char' : 'Indent char'

        ,'_title_Auto updater' : 'Auto updater'
        ,'enable_autocompiler' : 'Enable'
        ,'_lbl_interval(ms)' : 'interval(ms)'
        ,'_lbl_output folder:   ' : 'output folder:   '
        ,'copy_xmlfile_btn' : 'copy folder\nfrom input-file'
        ,'browse_input_file_key' : 'Browse folder...'
        ,'_lbl_output file name:' : 'output file name:'

        ,'clear_btn' : 'Clear output'
        ,'Try' : 'Execute output (used after convert++)'
        ,'message_board': 'Output data'

    },
    'ru': {
        # 'key' : 'text'
        '_lbl_xml file' : 'xml файл'
        ,'_lbl_target object name' : 'Имя виджет\n(т.е. object name)'
        ,'_lbl_all object names' : 'список всех имен'
        ,'_lbl_options:' : 'Опции:'
        ## buttons:
        ,'convert_btn' : 'запуск'
        ,'convert_all_events' : 'запуск++\nвсе события'
        ,'convert_btns_events' : 'запуск++\nтолько события кнопок'
        ,'no_bad_widgets' : 'попробовать конвертировать незнакомые виджеты'

        # settings
        ,'-memento-file-cb-' : 'Запомнить путь к предыдущему .ui файл'
        ,'_lbl_indent_size' : 'Размер табуляции'
        ,'_lbl_indent_char' : 'Символ табуляции'

        ,'_title_Auto updater' : 'Авто обновлятор'
        ,'enable_autocompiler' : 'Вкл'
        ,'_lbl_interval(ms)' : 'Интервал(мсек)'
        ,'_lbl_output folder:   ' : 'Папке, где будет выходной файл:   '
        ,'copy_xmlfile_btn' : 'вставить папку \nиз буффера обмена'
        ,'browse_input_file_key' : 'Выбрать папку...'
        ,'_lbl_output file name:' : 'Имя выходного файла:'

        ,'clear_btn' : 'Очистить'
        ,'Try' : 'Запустить код (только после ++ версии)'
        ,'message_board': 'Результат'
    }
}

def run_gui():
    settings_path = os.path.join(cd, 'setting.json')



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
        all_object_names_in_combo = my_window['objs'].Values

        if my_values['xmlfile'] and objname and objname in all_object_names_in_combo:
            my_window['convert_btn'].update(disabled=False)
            my_window['convert_all_events'].update(disabled=False)
            my_window['convert_btns_events'].update(disabled=False)
        else:
            my_window['convert_btn'].update(disabled=True)
            my_window['convert_all_events'].update(disabled=True)
            my_window['convert_btns_events'].update(disabled=True)

    def update_app_settings():
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(_settings, f, ensure_ascii=False, indent=2)

    def send_board_message(text='*** Done ***'):

        curr_title = window['message_board'].metadata
        new_title = '{} | {} '.format(curr_title, text)
        window['message_board'].TKFrame.config(text=new_title)

        # counter end -> execute this:
        def clear_frame():
            new_board_message = window['message_board'].metadata
            window['message_board'].TKFrame.config(text=new_board_message)
        return {'count': 1, 'finished' : clear_frame}

    def parse_n_load_possible_widgets(myxml_file='', values={}):
        '''
        возвращает найденые object_names все виджетов
        '''

        if os.path.exists(myxml_file) and os.path.isfile(myxml_file):
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
            widgets.sort()
            layouts.sort()

            # #####################
            # обработка id виджетов
            # #####################
            for i in widgets:
                if '"' in i: i = i[:i.index('"')]

            for i in layouts:
                if '"' in i: i = i[:i.index('"')]

            # ######
            # insert
            # ######
            combo_items = ['# pick LAYOUTS widgets #', *layouts, '# pick WIDGETS widgets #', *widgets]
            window['objs'].update(values=combo_items)
            update_clear_btn(window, values)

            el = combo_items[1]
            if ' ' not in el:
                window['objname'].update(el)
                update_clear_btn(window, values, real_value=el)

            return combo_items
        else:
            window['objs'](values=[])
            window['objname']('')
        
        return []

        
    def change_language():
        global curr_lang
        if curr_lang == 'en':
            curr_lang = 'ru'
        else:
            curr_lang = 'en'

        # self.ParentNotebook.tab(self.ContainerElemementNumber-1, text=self.Title)
        for psg_key, element_text in langs[curr_lang].items():
            # get elem + his type
            elem = window[psg_key]; elem_type = type(elem)

            # update text of widget
            try:
                if elem_type in [sg.Frame, sg.Text]:
                    elem.update(value=element_text)
                elif elem_type in [sg.Button, sg.Checkbox]:
                    elem.update(text=element_text)
                else:
                    raise Exception("eerororor")
            except Exception as e:
                print(type(elem), psg_key, elem, elem_type)
                raise e

        # special update
        if curr_lang == 'en':
            window['message_board'].metadata = 'Output code'
            window['_tab_transpiler'](title='Transpiler')
            window['_tab_settings'](title='Settings')
        elif curr_lang == 'ru':
            window['message_board'].metadata = 'Результат'
            window['_tab_transpiler'](title='Основное')
            window['_tab_settings'](title='Настройка')

        # window['change_lang_btn']()
        # window['_tab_settings']()
        # _tab_transpiler

    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                _settings = json.load(f)
        except Exception as e:
            _settings = {
                '-memento-file-cb-': False,
                'xmlfile': ''
            }
            update_app_settings()
    else:
        _settings = {
            '-memento-file-cb-': False,
            'xmlfile': ''
        }
        update_app_settings()

    ###############
    ###   GUI   ###
    ###############
    ralign = {'size': (16, 2), "justification": 'r'}
    
    main_layout = [
        [sg.T('xml file', **ralign, key='_lbl_xml file'),
            sg.I(key='xmlfile', size=(35, 2), change_submits=True),
            sg.FileBrowse(target='xmlfile')],

        [sg.T('target object name', **ralign, key='_lbl_target object name'),
         sg.I(key='objname', size=(35, 2), change_submits=True)],

        [sg.T('all object names', **ralign, key='_lbl_all object names'),
            sg.Drop(values=[''], key='objs',
            size=(34, 1), change_submits=True)
        ],
        [
            sg.T('', **ralign), sg.B('convert', key='convert_btn', disabled=True),
            sg.B('convert++\nall events', size=(-1, 2), key='convert_all_events', disabled=True),
            sg.B('convert++\nbtns events', size=(-1, 2), key='convert_btns_events', disabled=True)
        ],
        [
            sg.T('options:', **ralign, key='_lbl_options:'),
            sg.CB('try convert unknows widgets', True,
                    key='no_bad_widgets')
        ],
    ]

    settings_layout = [
        [sg.CB('Remember path to previous file', False, change_submits=True, key='-memento-file-cb-')],
        [sg.T('Indent size', key='_lbl_indent_size'), sg.I('1', size=(5, 1), key='indent_size')],
        [sg.T('Indent char', key='_lbl_indent_char'), sg.I(' ', size=(5, 1), key='indent_char')],

        ############
        # autoupdate
        ############
        [sg.Frame('Auto updater', layout=[
            [sg.CB('Enable', False, key='enable_autocompiler',
                    change_submits=True, pad=(0,0), size=(20, 1)),
              sg.T('interval(ms)', size=(15, 1), key='_lbl_interval(ms)'),
              sg.Spin(list(range(500, 1000)), initial_value=500, key='autocompile_interval_ms',
                    size=(10, 1), change_submits=True, pad=(0,0))],

            [sg.T('===========================')],

            [ sg.T('output folder:   ', pad=(0,0), size=(15, 2), key='_lbl_output folder:   '),
                sg.I('', key='autotarget_file'),
                sg.B('copy folder\nfrom input-file', key='copy_xmlfile_btn',
                    size=(10,3), pad=(0,0), button_color=('black', 'blue')),
                sg.FolderBrowse('Browse folder...',
                      target='autotarget_file', pad=(0,0), key='browse_input_file_key')
            ],
            [ sg.T('output file name:', pad=(0,0), size=(20, 1), key='_lbl_output file name:'),
                sg.I('untitled_psg.py', key='PSG_OUTPUT_FNAME'),
            ],
        ], key='_title_Auto updater')],
    ]

    layout = [
        [
            sg.Col([
                [sg.TabGroup([[
                     sg.Tab('transpiler', main_layout, key='_tab_transpiler')
                    ,sg.Tab('settings', settings_layout, key='_tab_settings')
                ]], key='-tab_group-')]
                ,[sg.T('\n'*4)]
                ,[sg.B('Change language/Поменять язык', size=(40, 2), key='change_lang_btn')]
            ]),
            sg.Frame('Output data', layout=[
                [sg.B('Clear output', key='clear_btn'), 
                 sg.B('Execute output (used after convert++)',
                        size=(35, 1), disabled=True, key='Try')],
                [sg.ML(key='psg_ui_output', size=(70, 20))]
            ], key='message_board')],
    ]

    window = sg.Window('PySimpleGUIDesigner by nngogol', layout, auto_size_buttons=False, default_button_element_size=(10, 1), finalize=True, location=(100, 100))

    # coz current_version of PSG is 4.4
    window['message_board'].metadata = 'Output data'

    # #####
    # setup
    # #####
    if _settings['-memento-file-cb-']:
        window['-memento-file-cb-'].update(True)
        window['xmlfile'].update(_settings['xmlfile'])
        update_app_settings()
    psg_vals = window(timeout=0)[1]
    parse_n_load_possible_widgets(psg_vals['xmlfile'].strip(), psg_vals)

    # #########
    # variables
    # #########
    timers = []

    # ############
    # variables: for auto-compile
    # ############
    is_autocompiler_working = False
    autocompile_interval_ms = psg_vals['autocompile_interval_ms']
    p_input_xml_hash = None
    curr_file_hash = file_hash(psg_vals['xmlfile']) if os.path.exists(psg_vals['xmlfile']) else b''
    current_obj_names = []



    status = True
    window['autocompile_interval_ms'](disabled=status); window['autotarget_file'](disabled=status); window['copy_xmlfile_btn'](disabled=status); window['browse_input_file_key'](disabled=status); window['PSG_OUTPUT_FNAME'](disabled=status)

    while True:
        if is_autocompiler_working:
            event, values = window(timeout=autocompile_interval_ms)
        else:
            event, values = window(timeout=500)


        if event in (None, 'Exit'):
            break

        # сдежка за таймерами и их работами
        for a_timer in timers:
            if a_timer['count'] > 0:
                a_timer['count'] -= 1
            elif a_timer['count'] == 0:
                a_timer['finished']()
                timers.remove(a_timer)

        ################################
        #     _             _          #
        #    | |           (_)         #
        #    | | ___   __ _ _  ___     #
        #    | |/ _ \ / _` | |/ __|    #
        #    | | (_) | (_| | | (__     #
        #    |_|\___/ \__, |_|\___|    #
        #              __/ |           #
        #             |___/            #
        ################################

        # ############
        # auto compile
        # ############
        is_autocompiler_working = values['enable_autocompiler']
        if is_autocompiler_working:

            autotarget_file_dir = os.path.dirname(values['autotarget_file'])

            if values['objname'] not in current_obj_names:
                window['psg_ui_output']('(autocompiler) Error :\nBad target object name.')
            elif not os.path.exists(autotarget_file_dir):
                window['psg_ui_output']('(autocompiler) Error :\nBad output folder.')
            elif not os.path.exists(values['xmlfile']):
                window['psg_ui_output']('(autocompiler) Error :\nBad input xml file.')
            else:
                file_hash_val = file_hash(values['xmlfile'])
                if not curr_file_hash:
                    # first time
                    output_file = os.path.join(autotarget_file_dir, values['PSG_OUTPUT_FNAME'])
                    psg_ui_code = just_compile(values)
                    writefile(output_file, psg_ui_code)
                    window['psg_ui_output']('compiled!')
                else:
                    # as usual
                    if curr_file_hash != file_hash_val or event == 'objname':
                        # long
                        output_file = os.path.join(autotarget_file_dir, values['PSG_OUTPUT_FNAME'])
                        psg_ui_code = just_compile(values)

                        writefile(output_file, psg_ui_code)
                        window['psg_ui_output']('compiled!')

                curr_file_hash = file_hash_val

        # ###########
        # sg.I events
        # ###########
        # update ms update interval sg.Spin
        if event == 'autocompile_interval_ms':
            autocompile_interval_ms = values['autocompile_interval_ms']

        if event == 'enable_autocompiler':
            status = not values['enable_autocompiler']
            window['autocompile_interval_ms'](disabled=status); window['autotarget_file'](disabled=status); window['copy_xmlfile_btn'](disabled=status); window['browse_input_file_key'](disabled=status); window['PSG_OUTPUT_FNAME'](disabled=status)

        if event == 'xmlfile':
            
            # remember this file
            if _settings['-memento-file-cb-']:
                _settings['xmlfile'] = values['xmlfile'].strip()
                update_app_settings()
            obj_names = parse_n_load_possible_widgets(values['xmlfile'].strip(), values)
            current_obj_names = obj_names

        elif event == 'objs':
            # add only REAL object names -> those, who not contain ' '
            if ' ' not in values['objs']:
                window['objname'].update(values['objs'])
            update_clear_btn(window, values, real_value=values['objs'])

        elif event == 'objname':
            update_clear_btn(window, values)


        # ########
        # checkbox
        # ########
        if event == '-memento-file-cb-':
            _settings['-memento-file-cb-'] = values['-memento-file-cb-']
            _settings['xmlfile'] = '' if values['-memento-file-cb-'] else values['xmlfile']
            update_app_settings()
        
        # #######
        # buttons
        # #######
        elif event == 'clear_btn':
            window['psg_ui_output'].update('')

        elif event == 'copy_xmlfile_btn':
            window['autotarget_file'](os.path.dirname(values['xmlfile']) + '/')
        
        elif event == 'convert_btn':
            ui = just_compile(values)
            window['psg_ui_output'].update(ui)

            if ui.startswith('Error:'):
                # fail
                timers.append(send_board_message(text='***!!!*** Fail ***!!!***'))
            else:
                # success
                timers.append(send_board_message(text='*** Done ***'))

        elif event == 'convert_all_events':
            ui = just_compile(values)
            psg_ui = build_boilerplate(layout=ui, btns_event=False, all_events=True)

            if ui.startswith('Error:'):
                # fail
                window['psg_ui_output'].update(ui)
                timers.append(send_board_message(text='***!!!*** Fail ***!!!***'))
            else:
                # success
                window['psg_ui_output'].update(psg_ui)
                timers.append(send_board_message(text='*** Done ***'))
            

        elif event == 'convert_btns_events':
            ui = just_compile(values)
            psg_ui = build_boilerplate(layout=ui, btns_event=True, all_events=False)

            if ui.startswith('Error:'):
                # fail
                window['psg_ui_output'].update(ui)
                timers.append(send_board_message(text='***!!!*** Fail ***!!!***'))
            else:
                # success
                window['psg_ui_output'].update(psg_ui)
                timers.append(send_board_message(text='*** Done ***'))
                

        elif event == 'Try':
            try:
                psg_ui = values['psg_ui_output'].strip()
                psg_ui_lines = psg_ui.split('\n')

                '''
                case 1:
                    import PySimpleGUI as sg
                    ...
                case 2:
                    sg.Frame('', layout = [
                        [...],
                        [...],
                        [...],
                    ])
                case 3:
                    [
                        [...],
                        [...],
                        [...],
                    ]
                '''
                if psg_ui.startswith('import PySimpleGUI as sg'):
                    exec(psg_ui)
                if psg_ui_lines[0].startswith("""sg.Frame('""") and psg_ui_lines[0].endswith("""', layout = ["""):
                    window2 = sg.Window('test', eval(psg_ui))
                    window2.read()
                    window2.close()
                if psg_ui_lines[0].startswith("""[""") and psg_ui_lines[-1].endswith("""]"""):
                    possible_ui = eval(psg_ui)
                    possible_ui
                    if type(possible_ui) is list and type(possible_ui[0]) is not list:
                        raise Exception(f"bad ui given. It's not a list of LISTS.")
                    window2 = sg.Window('test', possible_ui)
                    window2.read()
                    window2.close()

            except Exception as e:
                sg.popup(str(e))
        elif event == 'change_lang_btn':
            change_language()
    window.close()


@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True, help='Verbose mode')
@click.option('-xml', '--xmlfile', type=click.Path(exists=True), help='absolute or relative path to ui_file')
@click.option('-ob', '--objname', type=str, help='Object name of target container')
@click.option('-nobadwidgets', default=True, is_flag=True, help='Forget about not-implemented(bad) widgets. Default - True')
@click.option('-ic', '--indent_char', type=str, default=' ', help='Indent character. Default is " "')
@click.option('-ia', '--indent_char_amount', type=int, default=1, help='Indent amount')
@click.option('-o', '--outputfile', type=click.Path(), help='Output file for PySimpleGUI code')
@click.option('-pp_mouse', default=False, is_flag=True, help='Option - generate buttons events')
@click.option('-pp_keys',  default=False, is_flag=True, help='Option - generate all events')
def cli(xmlfile, objname, nobadwidgets, outputfile, pp_mouse, pp_keys, indent_char, indent_char_amount, verbose):

    if not (xmlfile and objname):
        run_gui()
    elif xmlfile and objname:

        try:
            # PRE-process
            ##=#=#=#=#=#=#
            # RELATIVE path: add PWD to current file path
            if not (xmlfile.startswith('/') or xmlfile[1] == ':'):
                xmlfile = os.path.join(cd, xmlfile)
                if verbose:
                    print(f'input = "{xmlfile}"')

            psg_ui = just_compile({'objname': objname,
                                   'xmlfile': xmlfile, 'no_bad_widgets': nobadwidgets,
                                    'indent_size' : indent_char_amount,
                                    'indent_char' : indent_char})

            # compile++
            if pp_mouse:
                psg_ui = build_boilerplate(layout=psg_ui, btns_event=True)
            elif pp_keys:
                psg_ui = build_boilerplate(layout=psg_ui, all_events=True)

            # POST-PROCESS
            ##=#=#=#=#=#=#

            if outputfile:  # write PSG_UI to file
                with open(outputfile, 'w', encoding='utf-8') as ff:
                    ff.write(psg_ui)
            else:  # output to console
                click.echo(psg_ui)

            if verbose:
                click.echo(click.style("\n~~~done", bg='black', fg='green'))

        except Exception as e:
            click.echo(click.style(str(e), bg='black', fg='red'))
