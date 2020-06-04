# PySimpleGUI Designer

In this video I explain how to use QtDesigner + my software video (by me): https://www.youtube.com/watch?v=dN7gXwnNoBA
![designer](https://github.com/nngogol/PySimpleGUIDesigner/blob/master/gif.gif)



## Install:
```bash
            THIS PACKAGE         Requirements 
pip install PySimpleGUIDesigner  PySide2 click
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

Want to know parameters? Get help by:
```bash
PySimpleGUIDesigner --help
# 
# Output:
# 
Usage: main.py [OPTIONS]

Options:
  -v, --verbose                   Verbose mode
  -xml, --xmlfile PATH            absolute or relative path to ui_file
  -ob, --objname TEXT             Object name of target container
  -nobadwidgets                   Forget about not-implemented(bad) widgets.
                                  Default - True

  -ic, --indent_char TEXT         Indent character. Default is " "
  -ia, --indent_char_amount INTEGER
                                  Indent amount
  -o, --outputfile PATH           Output file for PySimpleGUI code
  -pp_mouse                       Option - generate buttons events
  -pp_keys                        Option - generate all events
  --help                          Show this message and exit.

```



## I want to use source code directly (from this repo code)

Ok(I don't know you need this), but here are the steps.

Let's imagine you say **"I don't want `pip install`, I want to donwload this repo and run code. How can I do this?"**

Solution 1:
```bash
# removing (if installed) PySimpleGUIDesigner:
pip uninstall -y PySimpleGUIDesigner

mkdir psgdesigner
cd psgdesigner
git clone https://github.com/nngogol/PySimpleGUIDesigner
python3 -m PySimpleGUIDesigner
# NOTE for Windows users: replace "python3"   with   "python" OR "py"

# ALSO, output "help" by:
# $ python3 -m PySimpleGUIDesigner --help
```

Solution 2:
```bash
mkdir psgdesigner
cd psgdesigner
git clone https://github.com/nngogol/PySimpleGUIDesigner
cd PySimpleGUIDesigner
python3 -m main_for_devel.py
# for Windows users: replace "python3"   with   "python" OR "py"
```
----

# Examples (fun part)

##### Using as normal (easy):
```bash
python3 main.py --xmlfile="~/folder1/test.ui" --objname="somegroupBox"
# a bit shorter command:
python3 main.py -xml "~/folder1/test.ui" -ob "somegroupBox"
```

#### hot-reloader trick For Unix-like OS

I like to use `watch` command.
This command will *compile* every **3 second** and **output to the screen**:
```bash
watch -n 3 PySimpleGUIDesigner -xml "~/folder1/test.ui" -ob somegroupBox
```

also, there is an `entr` command (install by `apt install entr`), which works even better. It makes you command, when file is changed:

This command will *compile* file `~/folder1/test.ui`, when you change it(like you hit `ctrl+s` to save layout in .ui file):
```bash
echo "~/folder1/test.ui" | entr -p -s 'PySimpleGUIDesigner -xml "~/folder1/test.ui" -ob somegroupBox'
```

If you are on Windows OS without bash, then PySimpleGUIDesigner has build-it hot-reloader! So, use it, if you need.

##### Redirect output
Use bash redirect (or `-o` option):
```bash
PySimpleGUIDesigner -xml untitled.ui -ob v1 > untitled.py
PySimpleGUIDesigner -xml untitled.ui -ob v1 -o untitled.py
```

## More Examples:

```bash
#=================== Basics:
### using relative path:
python3 main.py -xmlfile "untitled.ui" -objname="text1"
python3 main.py -xmlfile "examples_of_ui/untitled.ui" -objname="vv1"

### using absolute path:
python3 main.py -xmlfile "/tmp/examples_of_ui/untitled.ui" -objname="text1"

#=================== Indent:
# ia = indent amount, ic = indent char
# indent 1:
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " "
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " " -ia 1 # the same effect, as command above
# indent 2:
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " " -ia 2

### add boilerplate to output file
python3 main.py -xmlfile "untitled.ui" -objname="text1" -pp_mouse -ic " " -ia 2
python3 main.py -xmlfile "untitled.ui" -objname="text1" -pp_keys
python3 main.py -xmlfile "untitled.ui" -objname="text1" -ic " " -ia 2 -pp_keys
```

## Gogol, HELP me! I don't know what I'm doing!

Keep calm. I will try to help you.

Really do *super easy* thing - "Open Issue" in this repository: https://github.com/nngogol/PySimpleGUIDesigner/issues

## Todo

- [done] xml -> py
- [interesting] psg code -> xml
- add some `picking templates` for user
- add some `boilerplate`'s in output generated code
- unit tests, `pytest`?
