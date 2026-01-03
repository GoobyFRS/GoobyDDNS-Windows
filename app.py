#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import threading
import time
import requests
import json
import configparser
import shutil
import sys
from pathlib import Path
from datetime import datetime

APP_VERSION = str("0.9.0")
APP_NAME = "GoobyDDNS"
CHECK_INTERVAL = 300  # seconds
CONFIG_NAME = "running_config.ini"
TEMPLATE_NAME = "template.ini"

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

BASE_PATH = get_base_path()
CONFIG_PATH = BASE_PATH / CONFIG_NAME
TEMPLATE_PATH = BASE_PATH / TEMPLATE_NAME

if not CONFIG_PATH.exists():
    shutil.copy(TEMPLATE_PATH, CONFIG_PATH)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

LINODE_API_KEY = config.get("linode", "LINODE_API_KEY", fallback=None)
LINODE_API_VERSION = config.get("linode", "LINODE_API_VERSION", fallback="v4")
DOMAIN_RECORD_ID = config.get("linode", "DOMAIN_RECORD_ID", fallback=None)
SUBDOMAIN_RECORD_ID = config.get("linode", "SUBDOMAIN_RECORD_ID", fallback=None)
FQDN = config.get("dns", "FQDN", fallback="unknown")

# ---------------- NETWORK FUNCTIONS ---------------- #

def get_my_wan_ipv4():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json().get("ip")
    except Exception:
        return None

def update_dns_record(my_public_ip):
    ipv_type = "AAAA" if ":" in my_public_ip else "A"

    url = f"https://api.linode.com/{LINODE_API_VERSION}/domains/{DOMAIN_RECORD_ID}/records/{SUBDOMAIN_RECORD_ID}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {LINODE_API_KEY}"
    }

    payload = {
        "target": my_public_ip,
        "name": FQDN,
        "type": ipv_type,
        "ttl": 300
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload), timeout=10)
    return response.status_code == 200

# ---------------- GUI APP ---------------- #

class DDNSApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"GoobyDDNS {APP_VERSION}")
        self.root.resizable(False, False)

        self.last_ip = None

        self.build_ui()
        self.update_clock()
        self.start_ddns_thread()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid()

        # Status indicator
        self.status_canvas = tk.Canvas(frame, width=20, height=20, highlightthickness=0)
        self.status_dot = self.status_canvas.create_oval(2, 2, 18, 18, fill="gray")
        self.status_canvas.grid(row=0, column=0, rowspan=2, padx=5)

        ttk.Label(frame, text="FQDN:").grid(row=0, column=1, sticky="w")
        self.fqdn_label = ttk.Label(frame, text=FQDN)
        self.fqdn_label.grid(row=0, column=2, sticky="w")

        ttk.Label(frame, text="Last IP:").grid(row=1, column=1, sticky="w")
        self.ip_label = ttk.Label(frame, text="—")
        self.ip_label.grid(row=1, column=2, sticky="w")

        ttk.Label(frame, text="Last Check:").grid(row=2, column=1, sticky="w")
        self.last_check_label = ttk.Label(frame, text="—")
        self.last_check_label.grid(row=2, column=2, sticky="w")

        ttk.Label(frame, text="Local Time:").grid(row=3, column=1, sticky="w")
        self.clock_label = ttk.Label(frame, text="—")
        self.clock_label.grid(row=3, column=2, sticky="w")

    # ---------------- UI HELPERS ---------------- #
    def set_status(self, color):
        self.status_canvas.itemconfig(self.status_dot, fill=color)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(10_000, self.update_clock)

    # ---------------- DDNS LOOP ---------------- #
    def start_ddns_thread(self):
        thread = threading.Thread(target=self.ddns_loop, daemon=True)
        thread.start()

    def ddns_loop(self):
        while True:
            self.run_ddns_check()
            time.sleep(CHECK_INTERVAL)

    def run_ddns_check(self):
        ip = get_my_wan_ipv4()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not ip:
            self.root.after(0, lambda: self.set_status("red"))
            return

        def update_ui():
            self.ip_label.config(text=ip)
            self.last_check_label.config(text=timestamp)

        self.root.after(0, update_ui)
        if ip == self.last_ip:
            self.root.after(0, lambda: self.set_status("yellow"))
            return

        success = update_dns_record(ip)
        if success:
            self.last_ip = ip
            self.root.after(0, lambda: self.set_status("green"))
        else:
            self.root.after(0, lambda: self.set_status("red"))

def main():
    root = tk.Tk()
    DDNSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
