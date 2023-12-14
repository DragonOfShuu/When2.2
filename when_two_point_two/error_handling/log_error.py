from tkinter import messagebox
from datetime import datetime
from pathlib import Path
import traceback

error_log_location = Path("error_logs")


def log_it(e: Exception):
    now = datetime.now()

    if not error_log_location.exists():
        error_log_location.mkdir()

    log_name = f'when_2.2_error_{now.strftime("%d-%m-%Y_%H-%M-%S")}.log'
    full_log_loc = (error_log_location / log_name).absolute()
    with open(full_log_loc, "w") as f:
        f.write(f"Error: {e.args[0]}\n\n" + traceback.format_exc())
    messagebox.showerror("Error Made", f"An error was created at {full_log_loc}")
