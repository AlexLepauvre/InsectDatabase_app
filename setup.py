import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("InsectDatabaseApp.py", base=base, icon="insect_logo.ico")]

cx_Freeze.setup(
    name="Les Robetes",
    options={
        "build_exe": {
            "packages": ["tkinter", "pandas", "sqlite3"],
            "include_files": ["insect_logo.ico", "insect_bg.png"]
        }
    },
    version="0.01",
    description="Insects database application",
    executables=executables
)

