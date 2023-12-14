from when_two_point_two import main, log_it
from plyer import notification
from pathlib import Path
import os

try:
    os.chdir(Path(__file__).parent)
    main()
except Exception as e:
    log_it(e)

    notification.notify(  # type:ignore
        title="When 2.2: Error", message=f"An error occurred: {e.args[0]}"
    )
