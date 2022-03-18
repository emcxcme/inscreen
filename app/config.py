import yaml


def _extract_id_from(token: str) -> int:
    id = int(token.split(":")[0])
    return id


config_file = "./config.yaml"
mode = "r"
with open(config_file, mode) as stream:
    CONFIG = yaml.safe_load(stream)
CONFIG["INSCREEN_ID"] = _extract_id_from(CONFIG["INSCREEN_TOKEN"])
CONFIG["INSCREEN_HELPER_IDS"] = list(
    map(_extract_id_from, CONFIG["INSCREEN_HELPER_TOKENS"])
)
