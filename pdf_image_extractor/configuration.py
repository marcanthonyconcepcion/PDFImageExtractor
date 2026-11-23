from pathlib import Path
from typing import Any, Dict, Union

import yaml


class ConfigurationError(ValueError):
    pass


class YAMLConfigurationLoader:
    def load(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError("Configuration file not found: {}".format(path))

        try:
            with path.open("r", encoding="utf-8") as configuration_file:
                configuration = yaml.safe_load(configuration_file)
        except yaml.YAMLError as error:
            raise ConfigurationError("Invalid YAML configuration: {}".format(error)) from error

        if not isinstance(configuration, dict):
            raise ConfigurationError("Configuration file must contain a YAML mapping")

        return configuration


def load_yaml_configuration(file_path: Union[str, Path]) -> Dict[str, Any]:
    return YAMLConfigurationLoader().load(file_path)

