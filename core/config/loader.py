import yaml
from pathlib import Path
import os

SCHEMA_PATH = Path(__file__).parent / "schema.yaml"

class ConfigLoader:
    _config = None

    @classmethod
    def load(cls):
        if cls._config is None:
            if not SCHEMA_PATH.exists():
                raise FileNotFoundError(f"Configuration schema not found at {SCHEMA_PATH}")
            with open(SCHEMA_PATH, "r") as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, section: str, key: str = None, default=None):
        config = cls.load()
        if section not in config:
            return default
        if key:
            return config[section].get(key, default)
        return config[section]
