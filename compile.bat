@echo off
echo Compiling main.py to executable...

rem Activate your virtual environment if you're using one
rem call path\to\your\venv\Scripts\activate.bat

rem Compile the script
pyinstaller --onefile --windowed --name FileProcessor main.py

echo Compilation complete.
echo The executable is located in the "dist" folder.

pause