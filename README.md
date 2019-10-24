# PySimpleGUI Designer

## Install:
```bash
# Requirements: pyside2
# pip install PySide2
pip install PySimpleGUIDesigner
```

## Usage
Run GUI:
```bash
PySimpleGUIDesigner
```

Use options(cli-verison):
```bash
PySimpleGUIDesigner --xmlfile="~/folder1/test.ui" --objname="somegroupBox"
```

---

Help:
```bash
PySimpleGUIDesigner --help
```
Output:
```
Usage: main.py [OPTIONS]

Options:
  -v, --verbose                  Verbose mode
  -x, --run                      just run gui example
  -xmlfile PATH                  abs or rel path to ui_file
  -tc, --tabchar TEXT            tab character. Default is "\t"
  -ta, --tabchar_amount INTEGER  indent tab amount
  -objname TEXT                  object name of target container
  -nobadwidgets                  forget about bad widgets. Default - True
  -o, --outputfile PATH          file to output compiled PySimpleGUI ui
  -pp_mouse                      compile++ option - do the mouse clicks events
  -pp_keys                       compile++ option - do the keys events
  --help                         Show this message and exit.

```

---


## Usage (source code)

Download this repo, ***cd*** into directory.

Run gui:
```bash
python3 main.py
```

Compile by using options:
```bash
python3 main.py --xmlfile="~/folder1/test.ui" --objname="somegroupBox"
```

Examples:

```bash
# # #        give different path for xmlfile
### Abs path
python3 main.py -xmlfile "/tmp/examples_of_ui/untitled.ui" -objname="text1"
### Relative path
python3 main.py -xmlfile "examples_of_ui/untitled.ui" -objname="vv1"
python3 main.py -xmlfile "untitled.ui" -objname="text1"

### tab character
### tc = tab character, ta = tab amount
python3 main.py -xmlfile "untitled.ui" -objname="text1" -tc " "
python3 main.py -xmlfile "untitled.ui" -objname="text1" -tc " " -ta 1 # the same effect, as command above
python3 main.py -xmlfile "untitled.ui" -objname="text1" -tc " " -ta 2

### add boilerplate to output file
python3 main.py -xmlfile "untitled.ui" -objname="text1" -pp_mouse -tc " " -ta 2
python3 main.py -xmlfile "untitled.ui" -objname="text1" -pp_keys
python3 main.py -xmlfile "untitled.ui" -objname="text1" -tc " " -ta 2 -pp_keys

```

---

## Todo

Possible:
- improve `psg_ui_maker.py` - somewhere in `__init__` method, maybe;
- add some `picking templates` for user
- add some `boilerplate`'s in output generated code
- maybe some unit tests, idk. `pytest`?


## FAQ

How do I use PySimpleGUIDesigner WITH Qt Designer?
Watch this video (by me):

https://www.youtube.com/watch?v=dN7gXwnNoBA
