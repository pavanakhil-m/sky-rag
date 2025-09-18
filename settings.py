import yaml

file_path = "config.yml"


def load_configs(file_path: str) -> dict:
    with open(file_path, "r") as file:
        configs = yaml.safe_load(file)
    return configs


configs = load_configs(file_path)
