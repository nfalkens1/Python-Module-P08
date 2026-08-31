import os
import sys
from dotenv import load_dotenv, dotenv_values


CONFIG_DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "",
}

REQUIRED_CONFIG_DATA: tuple[str, ...] = (
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
)

VALID_MODES: tuple[str, ...] = (
    "development",
    "production",
)

SECRET_KEYS: tuple[str, ...] = (
    "API_KEY",
    "DATABASE_URL",
)


def load_config() -> tuple[dict[str, str], bool, list[str]]:
    """
    Loads all config values, inserts defaults where nothing is set.
    Returns a tuple with:
     -dict containing config data
     -bool that checks of env can be loaded
     -list of all overridden configs
    """
    env_keys = set(os.environ)
    env_check = load_dotenv()
    file_keys = set(dotenv_values())
    config: dict[str, str] = {}
    for name, default in CONFIG_DEFAULTS.items():
        config[name] = os.getenv(name, default)
    overridden = sorted(file_keys & env_keys)

    return config, env_check, overridden


def interpret_config(config: dict[str, str]) -> dict[str, str]:
    """
    Takes config data and returns formatted output.
    Hides secretive config info.
    """
    mode_value = config["MATRIX_MODE"]
    url = config["DATABASE_URL"].lower().strip()
    if not url:
        url_value = "Not configured"
    elif "localhost" in url or "127.0.0.1" in url:
        url_value = "Connected to local instance"
    else:
        url_value = "Connected to remote instance"
    api = config["API_KEY"].strip()
    if not api:
        api_value = "Not authenticated"
    else:
        api_value = "Authenticated"
    log_lvl_value = config["LOG_LEVEL"].strip()
    zion = config["ZION_ENDPOINT"].strip()
    if not zion:
        zion_value = "Offline"
    else:
        zion_value = "Online"
    return {
        "Mode": mode_value,
        "Database": url_value,
        "API Access": api_value,
        "Log Level": log_lvl_value,
        "Zion Network": zion_value,
    }


def validate_config(config: dict[str, str]) -> list[str]:
    """
    Analyzes validity of configs and returns warnings.
    """
    error_msgs: list[str] = []
    for k in REQUIRED_CONFIG_DATA:
        if not config[k].strip():
            error_msgs.append(f"{k}: Is not set")
    if config["MATRIX_MODE"] not in VALID_MODES:
        error_msgs.append(f"MATRIX_MODE: must be {VALID_MODES[0]}"
                          f" or {VALID_MODES[1]}")
    if not config["LOG_LEVEL"].strip():
        error_msgs.append("LOG_LEVEL: Missing config!")
    return error_msgs


if __name__ == "__main__":
    header = "\nORACLE STATUS: Reading the Matrix...\n"
    security_header = "\nEnvironment security check:"
    footer = "\n=== The Oracle sees all configurations ===\n"
    loaded_msg = "Configuration loaded:"
    config_raw = load_config()
    config_data = config_raw[0]
    env_found = config_raw[1]
    prod_check = config_raw[2]
    is_prod_mode = config_data["MATRIX_MODE"] == "production"
    config_show = interpret_config(config_data)
    print(header)
    print(loaded_msg)
    for k, v in config_show.items():
        print(f" {k}: {v}")
    problems = validate_config(config_data)
    ok_msgs = [
        " [OK] No hardcoded secrets detected",
        " [OK] .env file properly configured",
        f" [OK] Production overrides active: {', '.join(prod_check)}",
        " [OK] Production overrides available but none active",
    ]
    ko_msgs = [
        " [KO] hardcoded secrets detected",
        " [KO] no .env file found",
    ]
    if problems:
        if is_prod_mode:
            print("\nCRITICAL ERRORS:")
            for problem in problems:
                print(f" {problem}")
            print("\nThe program will exit in a failed state!")
            sys.exit(1)
        else:
            print("\nWarnings:")
            for problem in problems:
                print(f" {problem}")
    print(security_header)
    hardcoded = [k for k in SECRET_KEYS if CONFIG_DEFAULTS[k].strip()]
    if hardcoded:
        print(ko_msgs[0])
    else:
        print(ok_msgs[0])
    if env_found:
        print(ok_msgs[1])
    else:
        print(ko_msgs[1])
    if prod_check:
        print(ok_msgs[2])
    else:
        print(ok_msgs[3])
    print(footer)
    sys.exit(0)
