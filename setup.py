import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico','themes/','images/','json/','modules/','logins.py',]

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "AutotaskAssistant",
    version = "1.0",
    description = "Automated support for repair technicians",
    author = "Vank Programming and Design",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
