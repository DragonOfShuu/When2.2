from dataclasses import dataclass, asdict
import json as j


@dataclass
class ConfigObj:
    speaker_has: list[str]
    speaker_not_have: list[str]
    last_public_update: str | None
    last_beta_update: str | None
    retrieve_new_data: bool = True


class Config:
    _config: None | ConfigObj = None

    @classmethod
    @property
    def config(cls) -> ConfigObj:
        if cls._config is not None:
            return cls._config
        return cls.load()

    @classmethod
    def load(cls):
        with open("config.json") as c:
            config_dict = j.loads(c.read())

        cls._config = ConfigObj(**config_dict)
        return cls._config

    @classmethod
    def save(cls):
        with open("config.json", "w") as c:
            c.write(j.dumps(asdict(cls.config), indent=4))
        return cls._config
