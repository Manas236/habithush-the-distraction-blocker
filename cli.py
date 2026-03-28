import argparse
import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

CONFIG_FILE = Path.home() / ".habithush.json"

def get_hosts_path():
    # Attempt to detect OS by checking for the existence of the Windows hosts file path
    win_path = r"C:\Windows\System32\drivers\etc\hosts"
    if os.path.exists(win_path):
        return win_path
    return "/etc/hosts"

HOSTS_PATH = get_hosts_path()
REDIRECT_IP = "127.0.0.1"
MARKER = "# HABITHUSH-START"
END_MARKER = "# HABITHUSH-END"

def is_windows():
    return HOSTS_PATH.lower().startswith('c:')

def load_config():
    if not CONFIG_FILE.exists():
        return {"blocked_domains": [], "is_active": False, "end_time": None}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def update_hosts(domains):
    if not is_windows():
        if os.geteuid() != 0:
            print("Error: Please run with sudo privileges.")
            sys.exit(1)

    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
    except PermissionError:
        print("Error: Permission denied. Please run as Administrator/root.")
        sys.exit(1)

    clean_lines = []
    in_block = False
    for line in lines:
        if MARKER in line:
            in_block = True
            continue
        if END_MARKER in line:
            in_block = False
            continue
        if not in_block:
            clean_lines.append(line)

    if domains:
        clean_lines.append(f"\n{MARKER}\n")
        for domain in domains:
            clean_lines.append(f"{REDIRECT_IP} {domain}\n")
        clean_lines.append(f"{END_MARKER}\n")

    try:
        with open(HOSTS_PATH, "w") as f:
            f.writelines(clean_lines)
    except PermissionError:
        print("Error: Could not write to hosts file. Please run with elevated privileges.")
        sys.exit(1)

def block(minutes):
    config = load_config()
    if not config["blocked_domains"]:
        print("No domains configured. Add them first.")
        return
    
    end_time = datetime.now() + timedelta(minutes=minutes) if minutes else None
    update_hosts(config["blocked_domains"])
    config["is_active"] = True
    config["end_time"] = end_time.isoformat() if end_time else None
    save_config(config)
    print(f"Distractions blocked {'until ' + config['end_time'] if minutes else 'indefinitely'}.")

def allow():
    update_hosts([])
    config = load_config()
    config["is_active"] = False
    config["end_time"] = None
    save_config(config)
    print("Distractions allowed.")

def add_domain(domain):
    config = load_config()
    if domain not in config["blocked_domains"]:
        config["blocked_domains"].append(domain)
        save_config(config)
        print(f"Added {domain} to block list.")

def main():
    parser = argparse.ArgumentParser(description="HabitHush: Distraction Blocker")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("allow")
    block_parser = subparsers.add_parser("block")
    block_parser.add_argument("--time", type=int, help="Minutes to block")
    
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("domain", type=str)

    args = parser.parse_args()

    if args.command == "block":
        block(args.time)
    elif args.command == "allow":
        allow()
    elif args.command == "add":
        add_domain(args.domain)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()