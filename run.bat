@REM cd %~dp0
echo "I ran" > "invisible.txt"
"%~dp0.venv\Scripts\pythonw.exe" "%~dp0When2.2.py" > run_info.log
