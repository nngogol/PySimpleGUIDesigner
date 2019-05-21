# PySimeplGUI Designer

**Install**:
```bash
pip install PySimpleGUIDesigner
```

## Usage
Run GUI:
```bash
psg_des
```

Use options:
```bash
psg_des --xmlfile="~/folder1/test.ui" --objname="somegroupBox"
```

Help:
```bash
psg_des --help
```
Output:
```
Usage: main.py [OPTIONS]

Options:
  -x, --run              just run gui example
  -xmlfile PATH          abs path to ui file
  -objname TEXT          object name of target container
  -nobadwidgets          forget about bad widgets. Default - True
  -o, --outputfile PATH  file to output compiled PySimpleGUI ui
  -pp_mouse              compile++ option - do the mouse clicks events
  -pp_keys               compile++ option - do the keys events
  --help                 Show this message and exit.


```
---
## Usage (source code)

Run gui:
```bash
python3 main.py
```

Compile by using options:
```bash
python3 main.py --xmlfile="~/folder1/test.ui" --objname="somegroupBox"
```
