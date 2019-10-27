# PySimpleGUI Designer

## Install:
```bash
# Requirements: pyside2
# $ pip install PySide2
pip install PySimpleGUIDesigner
```

## Usage
Use GUI(by default):
```bash
PySimpleGUIDesigner
```

Use CLI:
```bash
PySimpleGUIDesigner -xml "~/folder1/test.ui" -ob "somegroupBox"
```

---

Want to know parameters? Get help by:
```bash
PySimpleGUIDesigner --help
```
Output:
```
Usage: main.py [OPTIONS]

Options:
  -v, --verbose                   Verbose mode
  -x, --run                       Just run gui example
  -xml, --xmlfile PATH            absolute or relative path to ui_file
  -ob, --objname TEXT             Object name of target container
  -nobadwidgets                   Forget about not-implemented(bad) widgets.
                                  Default - True
  -ic, --indent_char TEXT         Indent character. Default is " "
  -ia, --indent_char_size INTEGER
                                  Indent size
  -o, --outputfile PATH           Output file for PySimpleGUI code
  -pp_mouse                       Option - generate buttons events
  -pp_keys                        Option - generate all events
  --help                          Show this message and exit.
```

---


## I don't want `pip install`, how to use this repo's source code?

Download this repo, ***cd*** into it.

Run gui:
```bash
python3 main.py
```

#### If you see this error:
`ModuleNotFoundError: No module named '__main__.transpiler2'; '__main__' is not a package`
##### THEN just change in `main.py` line:
`from .transpiler2 import *`
##### to
`from transpiler2 import *`

----

Using as normal (easy):
```bash
python3 main.py --xmlfile="~/folder1/test.ui" --objname="somegroupBox"
# OR
python3 main.py -xml "~/folder1/test.ui" -ob "somegroupBox"
```

### Examples:

```bash
#=================== Basics:
### relative path
python3 main.py -xmlfile "untitled.ui" -objname="text1"
python3 main.py -xmlfile "examples_of_ui/untitled.ui" -objname="vv1"
### absolute path
python3 main.py -xmlfile "/tmp/examples_of_ui/untitled.ui" -objname="text1"

#=================== Indent:
# ia = indent amount, ic = indent char
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " "
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " " -ia 1 # the same effect, as command above

python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " " -ia 2


### add boilerplate to output file
python3 main.py -xmlfile "untitled.ui" -objname="text1" -pp_mouse -ic " " -ia 2
python3 main.py -xmlfile "untitled.ui" -objname="text1" -pp_keys
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " " -ia 2 -pp_keys

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
