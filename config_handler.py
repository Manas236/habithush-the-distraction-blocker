import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_FILENAME = "config.json"
APP_DIR = Path.home() / ".habithush"

def get_config_path() -> Path:
    """Returns the path to the configuration file, ensuring the directory exists."""
    if not APP_DIR.exists():
        APP_DIR.mkdir(parents=True, exist_ok=True)
    return APP_DIR / CONFIG_FILENAME

def load_config() -> Dict[str, Any]:
    """Loads the configuration from the JSON file or returns default if not found."""
    config_path = get_config_path()
    if not config_path.exists():
        return {
            "blocked_domains": [],
            "is_blocking": False,
            "timer_end": None
        }
    
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"blocked_domains": [], "is_blocking": False, "timer_end": None}

def save_config(config: Dict[str, Any]) -> None:
    """Persists the configuration dictionary to the JSON file."""
    config_path = get_config_path()
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving configuration: {e}")

def update_config(key: str, value: Any) -> None:
    """Updates a specific key in the configuration."""
    config = load_config()
    config[key] = value
    save_config(config)