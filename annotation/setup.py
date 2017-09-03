from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["PyQt5.QtCore",
                                  "PyQt5.QtGui",
                                  "PyQt5.QtWidgets",
                                  "numpy",
                                  "pandas",
                                  "os",
                                  "csv",
                                  "sys"],
                                  excludes = [
                                  "Tkinter"])

import sys
import os
import PyQt5
base = 'Win32GUI' if sys.platform=='win32' else None
os.environ['TCL_LIBRARY'] = r'C:\Annaconda\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Annaconda\tcl\tk8.6'
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

executables = [
    Executable('myapp.py', base=base)
]

setup(name='AnnotationApp',
      version = '1.0',
      description = 'Tool helps to annotate Amazon reviews',
      options = dict(build_exe = buildOptions),
      executables = executables)
