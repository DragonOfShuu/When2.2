import traceback
from datetime import datetime

error_log_location = "error_logs"

def log_it(e: Exception):
    now = datetime.now()

    with open(f'{error_log_location}/when_2.2_error_{now.strftime("%d-%m-%Y_%H-%M-%S")}.log', 'w') as f:
        f.write(f"Error: {e.args[0]}\n\n"+traceback.format_exc())
        