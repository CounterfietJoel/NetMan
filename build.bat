@echo off
echo =======================================================
echo Building NetMan Standalone Executable (.exe)
echo =======================================================

python -m pip install pyinstaller
pyinstaller --onefile --noconsole --name "NetMan" --add-data "netman;netman" main.py

echo.
echo Build complete! Your standalone NetMan.exe is in the dist/ directory.
pause
