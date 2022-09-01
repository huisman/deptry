from typing import Dict
import logging
import toml
from pathlib import Path


DEFAULTS = {
    'ignore_dependencies' : None,
    'ignore_directories' : ['.venv']
}

class Config:

    def __init__(self, cli_arguments: Dict):
        self.config = DEFAULTS
        self._override_config_with_pyproject_toml()
        self._override_config_with_cli_arguments(cli_arguments)

    def _override_config_with_pyproject_toml(self):
        pyproject_toml_config = self._read_configuration_from_pyproject_toml()
        if pyproject_toml_config:
            for argument in self.config.keys():
                if argument in pyproject_toml_config:
                    self.config[argument] = pyproject_toml_config[argument]
                    logging.debug(f'Argument {argument} set to {pyproject_toml_config[argument]} by pyproject.toml')

    def _override_config_with_cli_arguments(self, cli_arguments):
        for argument in cli_arguments.keys():
            if cli_arguments[argument] is not None:
                self.config[argument] = cli_arguments[argument]
                logging.debug(f'Argument {argument} set to {cli_arguments[argument]} by command line argument')

    def _read_configuration_from_pyproject_toml(self):
        try:
            pyproject_text = Path("./pyproject.toml").read_text()
            pyproject_data = toml.loads(pyproject_text)
            return  pyproject_data['tool']['deptry']
        except:
            logging.debug('No configuration for deptry was found in pyproject.toml.')
            return None