from pathlib import Path
import traceback
from datetime import datetime

error_log_location = Path("error_logs")

def log_it(e: Exception):
    now = datetime.now()

    if not error_log_location.exists():
        error_log_location.mkdir()

    with open(error_log_location/ f'when_2.2_error_{now.strftime("%d-%m-%Y_%H-%M-%S")}.log', 'w') as f:
        f.write(f"Error: {e.args[0]}\n\n"+traceback.format_exc())
        