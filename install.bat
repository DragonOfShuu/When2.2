if exist "%~dp0.venv\" (
  echo "Skipped env creation"
) else (
  python -m venv %~dp0.venv
)

@REM call .\.venv\Scripts\activate
"%~dp0.venv\Scripts\pip.exe" install -r "%~dp0requirements.txt"

schtasks /create /tn whengd /tr "'%~dp0.venv\Scripts\pythonw.exe' '%~dp0When2.2.py'" /sc MINUTE /mo 15
