from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import re
import textwrap
#####################################################################
#           _       _           _                    __ _           #
#          | |     | |         | |                  / _(_)          #
#      __ _| | ___ | |__   __ _| |   ___ ___  _ __ | |_ _  __ _     #
#     / _` | |/ _ \| '_ \ / _` | |  / __/ _ \| '_ \|  _| |/ _` |    #
#    | (_| | | (_) | |_) | (_| | | | (_| (_) | | | | | | | (_| |    #
#     \__, |_|\___/|_.__/ \__,_|_|  \___\___/|_| |_|_| |_|\__, |    #
#      __/ |                                               __/ |    #
#     |___/                                               |___/     #
#####################################################################

INSERT_ID_FOR_ALL_ELEMENT = True
INLINE_TAB_IN_TABWIDGET_DEFENITION = True # not True

# =================================
# =================================
# =================================

IMPLEMENTED_CONTAINERS = [QGridLayout, QVBoxLayout,
                          QHBoxLayout, QGroupBox, QFrame, QWidget]
IMPLEMENTED_CONTROL_ELEMENTS = [
    QLabel, QSpinBox, QCheckBox, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit]
ALL_IMPLEMENTED_ELEMENTS = IMPLEMENTED_CONTROL_ELEMENTS + IMPLEMENTED_CONTAINERS
# isCrate       = lambda item: type(item) in IMPLEMENTED_CONTAINERS
def is_implemented_widget(item): return type(item) in ALL_IMPLEMENTED_ELEMENTS


def brak(x):
    return f'[{x}]'


def get_widget_type(a_widget):
    return str(type(a_widget)).replace("<class 'PySide2.QtWidgets.", '').strip(".>'")


def str_widget(a_widget):
    idd = a_widget.objectName()
    return f'id={idd}; type=' + get_widget_type(a_widget)


def empty_widget(GUItype='tk'):
    # dummy elemets for EMPTY SPOTS in QGridLayout
    if GUItype == 'tk':
        return 'sg.T('')'
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

    elif type(node) in [QHBoxLayout, QVBoxLayout]:
        # import pdb; pdb.set_trace();

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
        raise Exception(f'HOWTO find childrens in "{type(node)}"')


#                       _
#                      | |
#  _ __ ___   ___  __ _| |_
# | '_ ` _ \ / _ \/ _` | __|
# | | | | | |  __/ (_| | |_
# |_| |_| |_|\___|\__,_|\__|


#   ____  __  __                  ____
#  / __ \|  \/  |                |  _ \
# | |  | | \  / | ___ _ __  _   _| |_) | __ _ _ __
# | |  | | |\/| |/ _ \ '_ \| | | |  _ < / _` | '__|
# | |__| | |  | |  __/ | | | |_| | |_) | (_| | |
#  \___\_\_|  |_|\___|_| |_|\__,_|____/ \__,_|_|

class Pepe(object):
    """
    class for parsing QMenuBar
    """

    def __init__(self, title, ob='', nodes=[]):
        self.title = title
        self.ob = ob
        self.nodes = nodes

    def nest_2(self, lvl=0):
        # mehh...
        tabs = '\t'*lvl
        if self.nodes:
            nodes = ',\n'.join([i.nest(lvl+1) for i in self.nodes])
            nodes = f', nodes=\n{nodes})\n'
        else:
            nodes = ')'
        return f'{tabs}Node("{self.title}"{nodes}'

    def nest_1(self, lvl=0):
        # working
        tabs = '\t'*lvl if not one_line else ''
        return_line__join = ',\n'
        if self.nodes:
            nodes = ',\n'.join([i.nest(lvl+1, one_line) for i in self.nodes])
            return f'{tabs}"{self.title}", [\n{nodes}\n{tabs}]'
        else:
            return f'{tabs}"{self.title}"'

    def nest(self, lvl=0, one_line=False):
        # added keyword paramas
        if one_line:
            tabs = ''
            return_line__join = ', '
            return_line_1 = ''
            return_line_2 = ' '
        else:
            tabs = '\t'*lvl
            return_line__join = ',\n'
            return_line_1 = '\n'
            return_line_2 = '\n'

        if self.nodes:
            nodes = [i.nest(lvl+1, one_line) for i in self.nodes]
            nodes = return_line__join.join(nodes)
            return f'{tabs}"{self.title}", [{return_line_1}{nodes}{return_line_2}{tabs}]'
        else:
            return f'{tabs}"{self.title}"'

    def __repr__(self):
        return f'Node("{self.title}", nodes={repr(self.nodes)})'

    def __str__(self):
        childrens = ''
        ob = f':{self.ob}' if self.ob else ''
        if self.nodes:
            childrens = ', [' + ', '.join([str(i) for i in self.nodes]) + ']'
        return f"['{self.title}{ob}'{childrens}]"


def _parseQMenu_obj(qmenu, lvl=0):
    try:
        actions = qmenu.actions()
        pepes = []
        for a in actions:
            pepe = Pepe('')
            # вывести текст
            if not a.isSeparator():
                pepe.title = a.iconText()

                # вывести вложенные менюшки
                menus = []
                try:
                    menus = _parseQMenu_obj(a.menu(), lvl+1)
                except Exception as e:
                    pass
                pepe.nodes = menus
            else:
                pepe.title = '---'
            pepes.append(pepe)

        return pepes
    except Exception as e:  # листок
        pass
        return Pepe(qmenu.title())
# ▲


def make_psg_menu(qmenubar: QMenuBar, menubar_oneline=False):
    menu_items = _parseQMenu_obj(qmenubar)
    res = ',\n'.join([brak(i.nest(menubar_oneline)) for i in menu_items])
    return brak(res)
# ▲


def _tab_da_shit(make_tabs, psg_rows, is_top, my_tab='\t'):
    # ▲     Add tabulation. I use '\t', not 4 spaces '    '
    final = my_tab + f',\n{my_tab}'.join(psg_rows)
    # tabs
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


def _compile_VBbox(parent_node: QVBoxLayout, is_top=False, make_tabs=-1, GUItype='tk', pass_bad_widgets=False):

    hbox_items = get_chidrens(parent_node)

    psg_rows = []
    for index, hbox_item in enumerate(hbox_items):
        # import pdb; pdb.set_trace();

        if not is_implemented_widget(hbox_item):
            print(f'>>> (!) Skipping element (not implemented) "{str_widget(hbox_item)}"')
            continue

        # =================
        # nested containers
        # =================
        if type(hbox_item) is QGridLayout:

            el = brak(to_psg_element(hbox_item, GUItype=GUItype,
                                      pass_bad_widgets=pass_bad_widgets))
            psg_rows.append(el)

        elif type(hbox_item) in [QHBoxLayout, QVBoxLayout]:

            elements = get_chidrens(hbox_item)
            psg_elemets = [to_psg_element(
                qt_widget, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets) for qt_widget in elements]
            el = brak(', '.join(psg_elemets))
            psg_rows.append(el)

        # =================
        # nested containers
        # =================
        else:

            message = f'''
            >>> ERROR in parsing vertical/horizontal BOX ITEM:
            hbox_item        : {str_widget(hbox_item)}
            parent_container : {str_widget(parent_node)}
            '''
            raise Exception(message)

    return _tab_da_shit(make_tabs, psg_rows, is_top)
# ▲
#                       parent_node: QGridLayout


def _compile_GridLayout(parent_node, make_column_not_frame=False, is_top=False, make_tabs=-1, GUItype='tk', pass_bad_widgets=False):

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

        el = brak(', '.join([i[1] for i in psg_elemets]))
        psg_rows.append(el)

    return _tab_da_shit(make_tabs, psg_rows, is_top)


def _escape_(text):
    return text.replace('\n', '\\n').replace('\\', '\\\\')


def to_psg_element(normal_item, size='', GUItype='tk', pass_bad_widgets=False, pure=False, menubar_oneline=False, make_column_not_frame=False):
    global INSERT_ID_FOR_ALL_ELEMENT

    # import pdb; pdb.set_trace();

    idd = normal_item.objectName()
    res = type(normal_item)

    if size != '' and type(size) in [tuple, list] and len(size) == 2:
        size = 'size=({0}, {1}), '.format(*size)
    elif size == '':
        pass
    else:
        raise Exception(f'IIn element "{normal_item}", BAD size: "{size}"')

    if 'QSpacerItem' in str(type(normal_item)):
        return empty_widget()

    #                  _        _
    #                 | |      (_)
    #   ___ ___  _ __ | |_ __ _ _ _ __   ___ _ __ ___
    #  / __/ _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
    # | (_| (_) | | | | || (_| | | | | |  __/ |  \__ \
    #  \___\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/

    if type(normal_item) in [QVBoxLayout, QHBoxLayout, QGridLayout]:
        if type(normal_item) == QGridLayout:
            ui = _compile_GridLayout(normal_item, is_top=False, make_tabs=2,
                                     GUItype=GUItype, pass_bad_widgets=pass_bad_widgets, make_column_not_frame=make_column_not_frame)
        else:
            ui = _compile_VBbox(normal_item, is_top=False, make_tabs=2,
                                GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)

        if make_column_not_frame:
            return f"sg.Column([\n{ui}\n])"
        return ui if pure else f"sg.Frame('', {size}layout = [\n{ui}\n])"
        # return ui if pure else f"sg.Frame('', {size}key='{idd}', layout = [\n{ui}\n])"

    elif type(normal_item) is QTabWidget:

        # core
        pages = normal_item.children()[0].children()
        tabs = [i for i in pages if type(i) == QWidget]

        if not INLINE_TAB_IN_TABWIDGET_DEFENITION:
            tabs = [[index,
                     normal_item.tabText(index),
                     to_psg_element(widget_in_tab, pure=True).strip()
                     ] for index, widget_in_tab in enumerate(tabs)]

            # 1
            variables_and_ui = '\n\n'.join([f'tab{i}_layout = [\n\t\t{ui}\n]' for i, title, ui in tabs])

            # 2
            sg_tab = ', '.join([f"sg.Tab('{title}', tab{i}_layout)" for i, title, ui in tabs])
            sg_TabGroup = f"sg.TabGroup([[{sg_tab}]], {size}key='{idd}')"

            return variables_and_ui + '\n\n' + sg_TabGroup
        else:
            tabs = [[index,
                     normal_item.tabText(index),
                     to_psg_element(widget_in_tab, pure=True).strip()
                     ] for index, widget_in_tab in enumerate(tabs)]
            # 2
            sg_tab = [f"sg.Tab('{title}', [\n\t\t{ui}\n])" for i, title, ui in tabs]
            sg_TabGroup = "sg.TabGroup(key='{idd}', layout=[[{layout}]], {size})".format(
                idd=idd, size=size, layout=',\n'.join(sg_tab))

            return sg_TabGroup

    elif type(normal_item) in [QFrame, QGroupBox]:

        children = normal_item.children()[0]

        if type(children) is QGridLayout:
            ui = _compile_GridLayout(children,   make_tabs=2, GUItype=GUItype,
                                     pass_bad_widgets=pass_bad_widgets, make_column_not_frame=True)
        elif type(children) in [QVBoxLayout, QHBoxLayout]:
            ui = _compile_VBbox(children,        make_tabs=2,
                                GUItype=GUItype, pass_bad_widgets=pass_bad_widgets)
        else:
            raise Exception(textwrap.dedent(f'''
                "{idd}" has a FLOAT LAYOUT
                -(solution)-> select HBOX/HBOX/GRID-layout'''))

        title = ''
        if type(normal_item) is QGroupBox:
            title = normal_item.title()

        if INSERT_ID_FOR_ALL_ELEMENT:
            return f"sg.Frame('{title}', {size}key='{idd}', layout = [\n{ui}\n])"
        else:
            return f"sg.Frame('{title}', {size}layout=[\n{ui}\n])"

    elif type(normal_item) is QWidget:
        # return to_psg_element(normal_item.children()[0], pure=pure)
        return to_psg_element(normal_item.children()[0], size=size, GUItype=GUItype, pass_bad_widgets=pass_bad_widgets, pure=pure)

    # menu
    elif type(normal_item) is QMenuBar:
        qmenubar_layout = make_psg_menu(normal_item, menubar_oneline)
        return f"qmenubar_layout = {qmenubar_layout}\n\nsg.Menu(qmenubar_layout, key='{idd}')"

    #                  _             _            _     _            _
    #                 | |           | |          (_)   | |          | |
    #   ___ ___  _ __ | |_ _ __ ___ | | __      ___  __| | __ _  ___| |_ ___
    #  / __/ _ \| '_ \| __| '__/ _ \| | \ \ /\ / / |/ _` |/ _` |/ _ \ __/ __|
    # | (_| (_) | | | | |_| | | (_) | |  \ V  V /| | (_| | (_| |  __/ |_\__ \
    #  \___\___/|_| |_|\__|_|  \___/|_|   \_/\_/ |_|\__,_|\__, |\___|\__|___/
    #                                                      __/ |
    #                                                     |___/

    # label
    elif type(normal_item) is QLabel:
        text = _escape_(normal_item.text())
        if INSERT_ID_FOR_ALL_ELEMENT:
            return f"sg.T('{text}', {size}key='{idd}')"
        else:
            return f"sg.T('{text}', {size})".replace('  ', ' ').replace('  ', ' ').replace(', )', ')')

    elif type(normal_item) is QGraphicsView:
        img_file = normal_item.toolTip()
        return f"sg.Image(r'{img_file}', {size}key='{idd}')"

    # items
    elif type(normal_item) is QComboBox:
        w = normal_item
        curr = w.currentText()
        values = str([w.itemText(i) for i in range(w.count())])
        return f"sg.Combo({values}, default_value=\"{curr}\", {size}key='{idd}')"
        # return f"sg.Spin({values}, initial_value=\"{curr}\", {size}key='{idd}')"

    elif type(normal_item) is QListWidget:
        w = normal_item

        curr = w.currentItem()
        curr = f'default_value={curr.text()}, ' if curr else ''

        values = str([w.item(i).text() for i in range(w.count())])
        size = "size=(30, 10), "
        return f"sg.Listbox({values}, {size}key='{idd}')"

    # int
    elif type(normal_item) is QSpinBox:
        w = normal_item
        mina, maxa, curr = w.minimum(), w.maximum(), w.value()
        return f"sg.Spin(list(range({mina}, {maxa})), initial_value={curr}, {size}key='{idd}')"

    elif type(normal_item) is QDoubleSpinBox:
        w = normal_item

        min_, max_, curr, step = float(w.minimum()), float(
            w.maximum()), w.value(), float(w.singleStep())
        amount = ((max_*1000000-min_*1000000)/1000000)/step
        # return f"sg.Spin(list(np.linspace({min_}, {max_}, {amount})), initial_value={curr}, {size}key='{idd}')"

        values = f"[i/10000000 for i in range(int({min_} * 10000000), int({max_} * 10000000), int({step} * 10000000))]"
        return f"sg.Spin({values}, initial_value={curr}, {size}key='{idd}')"

    elif type(normal_item) is QSlider:
        mina, maxa, curr = normal_item.minimum(), normal_item.maximum(), normal_item.value()
        orientation = 'h' if normal_item.orientation() == Qt.Horizontal else 'v'
        range_ = f'range=({mina}, {maxa}),'
        curr = f'default_value={curr},'
        orientation = f"orientation='{orientation}',"
        return f"sg.Slider({range_} {orientation} {curr} {size}key='{idd}')"

    # bool
    elif type(normal_item) is QCheckBox:
        isChecked = str(normal_item.isChecked())
        text = _escape_(normal_item.text())
        return f"sg.CB('{text}', default={isChecked}, {size}key='{idd}')"

    # text
    elif type(normal_item) is QLineEdit:
        text = _escape_(normal_item.text())
        return f"sg.I('{text}', {size}key='{idd}')"

    elif type(normal_item) is QTextEdit:
        text = _escape_(normal_item.text())
        return f"sg.Multiline('{text}', {size}key='{idd}')"

    elif type(normal_item) is QPlainTextEdit:
        text = _escape_(normal_item.toPlainText())
        return f"sg.Multiline('{text}', {size}key='{idd}')"

    # button
    elif type(normal_item) is QPushButton:
        text = _escape_(normal_item.text())
        return f"sg.B('{text}', {size}key='{idd}')"

    elif type(normal_item) is QRadioButton:
        text, group_id = _escape_(
            normal_item.text()), _escape_(normal_item.toolTip())
        if not group_id:
            raise Exception(f"Set radio_group for '{idd}' as a toolTip text")
        return f"sg.Radio('{text}', '{group_id}', key='{idd}')"

    else:
        if pass_bad_widgets:
            return empty_widget(GUItype='tk')
        else:
            raise Exception(f"Not implemented for element '{type(normal_item)}'?")



def optimize_psg_code(code):
    # 1 optimization
    new_code = code.replace(", key=''", '')

    # 2 optimization
    key_patters = ['checkBox_', 'graphicsView_', 'gridLayout_',
                   'horizontalSlider_', 'horizontalLayout_', 'label_', 'layoutWidget_',
                   'lineEdit_', 'listWidget_', 'plainTextEdit_', 'pushButton_',
                   'radioButton_', 'spinBox_', 'textEdit_', 'verticalLayout_']
    for i in key_patters:
        new_code = re.sub(rf""", key=\'{i}\d*\'""", '',
                          new_code, flags=re.MULTILINE)

    # 3 avoid empty sg.T widgets
    new_code = new_code.replace('sg.T()', "sg.T('')")
    return new_code


'''

def parseQMenu_str(qmenu, lvl=0):
    # QMenu
    #   actions
    #   submenus
    str_format = ''
    try:
        actions     = qmenu.actions()
        for a in actions:
            # вывести текст
            if a.isSeparator():
                str_format += '\t'*lvl + '-'*10 + '\n'
            else:
                str_format += '\t'*lvl + a.iconText() + '\n'

            # вывести вложенные менюшки
            try:
                menus = a.menu()
                
                # str_format += '\t'*lvl + '{'
                str_format += parseQMenu_str(menus, lvl+1)
                # str_format += '\t'*lvl + '}'
            except Exception as e:
                pass
        return str_format
    except Exception as e: # листок
        # str_format += 'листок\n'
        str_format += ''
    return str_format

'''

'''
    ??? GET WIDTHEDST ELEMENTS in GRID ???

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
'''
