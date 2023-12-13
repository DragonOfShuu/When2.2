if exist .venv\ (
  echo "Skipped env creation"
) else (
  python -m venv .venv
)

@REM call .\.venv\Scripts\activate
.\.venv\Scripts\pip.exe install -r requirements.txt
schtasks /create /tn whengd /tr "'%~dp0run.bat'" /sc MINUTE /mo 1
