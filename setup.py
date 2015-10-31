# -*- coding: utf-8 -*-
# setup.py

from distutils.core import setup
from esky.bdist_esky import Executable

setup(
    name='NLP',
    version='1.0',
    options={"bdist_esky": {
        "freezer_module": "cxfreeze",
        #"includes": ["twisted"],
        "excludes": ["tkinter", "tcl", "PyQt4.sqlite3", "PyQt4.QtOpenGL4", "PyQt4.QtSql"]
    }},
    scripts=[Executable('na_analysis.py')],
)
