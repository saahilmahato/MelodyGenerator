import yaml
from data_handlers.load_instrument_data import extract_notes

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


if __name__ == "__main__":
    extract_notes(config)