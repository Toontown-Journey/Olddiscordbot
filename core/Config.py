#  Copyright (c) 2020. Toontown Journey. All rights reserved

import json
import os

config = None


def get_config():
    global config
    if config is None:
        config = Config()
    return config


def load_config_file():
    if not os.path.exists("config.json"):
        raise FileNotFoundError("config.json was not found, did you create it?")
    with open("config.json", encoding='utf=8') as cf:
        return json.load(cf)


def save_config_file(_config):
    if not os.path.exists("config.json"):
        raise FileNotFoundError("config.json was not found, did you move it while the bot was running?")
    with open("config.json", "w", encoding='utf=8') as cf:
        cf.write(json.dumps(_config, indent=3))
    del _config  # prevent accidental leakage


class InvalidConfigError(Exception):
    def __init__(self, message=None, *args):
        if message is not None:
            super().__init__(message, *args)
        else:
            super().__init__("Config file is invalid", *args)


class Config:

    def __init__(self):
        _config = load_config_file()
        self.token = _config["Bot Token"]
        self.prefix = _config["Bot Prefix"]
        self.cog_dir_name = _config["Cog Directory"]
        self.cog_dir = os.getcwd().replace('\\', '/') + self.cog_dir_name
        self.owners = _config["Bot Owner"]
        self.bot_description = _config["Bot Description"]
        self.disabled_cogs: [str] = _config["Disabled Cogs"]
        self.mysqlPassword = _config["MysqlPassword"] #store the password in config for better secrurity

    def disable_cog(self, cog):
        if cog not in self.disabled_cogs:
            self.disabled_cogs.append(cog)
            self.save_json()

    def enable_cog(self, cog):
        if cog in self.disabled_cogs:
            self.disabled_cogs.remove(cog)
            self.save_json()

    def save_json(self):
        _config = load_config_file()
        _config["Disabled Cogs"] = self.disabled_cogs
        save_config_file(_config)
        del config  # prevent accidental leakage
