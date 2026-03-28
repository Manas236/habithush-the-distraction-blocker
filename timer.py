import time
import threading
import json
import os
from datetime import datetime, timedelta

class TimerManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self._ensure_config()

    def _ensure_config(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump({"blocked": False, "expiry": None}, f)

    def get_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self, data):
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=4)

    def start_timer(self, minutes, callback):
        """
        Starts a timer in a background thread.
        callback: Function to execute once the timer expires.
        """
        expiry_time = datetime.now() + timedelta(minutes=minutes)
        config = self.get_config()
        config["blocked"] = True
        config["expiry"] = expiry_time.isoformat()
        self.save_config(config)

        def run():
            time.sleep(minutes * 60)
            callback()
            self.stop_timer()

        timer_thread = threading.Thread(target=run, daemon=True)
        timer_thread.start()
        return expiry_time

    def stop_timer(self):
        config = self.get_config()
        config["blocked"] = False
        config["expiry"] = None
        self.save_config(config)

    def is_active(self):
        config = self.get_config()
        if not config.get("blocked") or not config.get("expiry"):
            return False
        
        expiry = datetime.fromisoformat(config["expiry"])
        if datetime.now() >= expiry:
            self.stop_timer()
            return False
        return True

    def get_remaining_seconds(self):
        config = self.get_config()
        if not config.get("expiry"):
            return 0
        expiry = datetime.fromisoformat(config["expiry"])
        remaining = (expiry - datetime.now()).total_seconds()
        return max(0, int(remaining))