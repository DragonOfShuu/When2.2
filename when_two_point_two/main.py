from pathlib import Path
from .config_parse import Config

from dataclasses import dataclass
from plyer import notification
from datetime import datetime
from requests import Session
from tzlocal import get_localzone_name
import json as j
import pytz


gd = 322170


@dataclass
class GDObj:
    public_time: int
    beta_time: int


def get_gd():
    raw_data: dict
    if Config.config.retrieve_new_data:
        with Session() as s:
            raw_data = s.get(f"https://api.steamcmd.net/v1/info/{gd}").json()
        with open("test_data.json", "w") as f:
            f.write(j.dumps(raw_data, indent=4))
    else:
        with open("test_data.json", "r") as f:
            raw_data = j.loads(f.read())

    branches = raw_data["data"][str(gd)]["depots"]["branches"]

    return GDObj(
        public_time=int(branches["public"]["timeupdated"]),
        beta_time=int(branches["beta"]["timeupdated"]),
    )


def compare_public(public_update_time: datetime):
    last_update = Config.config.last_public_update

    if last_update is not None and public_update_time > datetime.fromisoformat(
        last_update
    ):
        notification.notify(  # type:ignore
            title="2.2 IS OUT NOW",
            message="I don't think I need to say much more",
        )
        from .audio import play_ringtone

        play_ringtone()

        with open(Path.home() / "Desktop" / "2-2_OUT.txt", "w") as f:
            f.write("2.2 is out now, congrats!")

    Config.config.last_public_update = public_update_time.isoformat()
    Config.save()
    return


def compare_beta(beta_update_time: datetime):
    last_update = Config.config.last_beta_update

    if last_update is not None and beta_update_time > datetime.fromisoformat(
        last_update
    ):
        notification.notify(  # type:ignore
            title="Beta Updated",
            message="The beta branch updated again...",
        )

    Config.config.last_beta_update = beta_update_time.isoformat()
    Config.save()
    return


def main():
    gd_obj = get_gd()
    public_update_time = datetime.fromtimestamp(gd_obj.public_time, pytz.utc)
    beta_update_time = datetime.fromtimestamp(gd_obj.beta_time, pytz.utc)

    print(
        f"Last update: {public_update_time.astimezone(pytz.timezone(get_localzone_name())).strftime('%B %d, %Y, %H:%M:%S')}"
    )
    print(
        f"Last beta update: {beta_update_time.astimezone(pytz.timezone(get_localzone_name())).strftime('%B %d, %Y, %H:%M:%S')}"
    )
    print(
        f"The current time: {datetime.now().astimezone(pytz.timezone(get_localzone_name())).strftime('%B %d, %Y, %H:%M:%S')}"
    )

    compare_public(public_update_time)
    compare_beta(beta_update_time)
    Config.config.last_retrieval = datetime.now().isoformat()
    Config.save()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        notification.notify(  # type:ignore
            title="TwoPointTwoWhen Error", message=e.args[0], timeout=10
        )
