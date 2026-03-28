import os
import sys
import json
import time
from datetime import datetime, timedelta

HOSTS_PATH = "/etc/hosts" if os.name != 'nt' else r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
CONFIG_FILE = os.path.expanduser("~/.habithush_config.json")
HEADER_START = "# --- HABITHUSH START ---"
HEADER_END = "# --- HABITHUSH END ---"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"blocked_domains": [], "is_active": False, "expiry": None}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def update_hosts_file(domains, block=True):
    try:
        with open(HOSTS_PATH, 'r') as f:
            lines = f.readlines()

        new_lines = []
        in_block = False
        for line in lines:
            if HEADER_START in line:
                in_block = True
                continue
            if HEADER_END in line:
                in_block = False
                continue
            if not in_block:
                new_lines.append(line)

        if block:
            new_lines.append(f"\n{HEADER_START}\n")
            for domain in domains:
                new_lines.append(f"{REDIRECT_IP} {domain}\n")
            new_lines.append(f"{HEADER_END}\n")

        with open(HOSTS_PATH, 'w') as f:
            f.writelines(new_lines)
        return True
    except PermissionError:
        print("Error: Permission denied. Please run with sudo/administrator privileges.")
        return False

def block_sites(duration_minutes=None):
    config = load_config()
    if not config["blocked_domains"]:
        print("No domains configured. Add domains first.")
        return

    if update_hosts_file(config["blocked_domains"], block=True):
        config["is_active"] = True
        if duration_minutes:
            config["expiry"] = (datetime.now() + timedelta(minutes=duration_minutes)).isoformat()
        else:
            config["expiry"] = None
        save_config(config)
        print(f"Distractions blocked {'for ' + str(duration_minutes) + ' minutes' if duration_minutes else 'indefinitely'}.")

def allow_sites():
    config = load_config()
    if update_hosts_file([], block=False):
        config["is_active"] = False
        config["expiry"] = None
        save_config(config)
        print("Distractions allowed.")

def check_session():
    config = load_config()
    if config["is_active"] and config["expiry"]:
        if datetime.now() >= datetime.fromisoformat(config["expiry"]):
            allow_sites()
            print("Focus session expired. Sites unblocked.")

def add_domain(domain):
    config = load_config()
    if domain not in config["blocked_domains"]:
        config["blocked_domains"].append(domain)
        save_config(config)
        print(f"Added {domain} to blocklist.")
        if config["is_active"]:
            block_sites()

def remove_domain(domain):
    config = load_config()
    if domain in config["blocked_domains"]:
        config["blocked_domains"].remove(domain)
        save_config(config)
        print(f"Removed {domain} from blocklist.")
        if config["is_active"]:
            block_sites()