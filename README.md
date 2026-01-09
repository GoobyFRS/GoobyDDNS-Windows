# GoobyDDNS_Windows

GoobyDDNS Client for Windows. It's like the NoIP DUC but for your own domain and with Akamai / Linode Name Servers. __I'll add multi-platform support at 10 Stars.__

**Current Version:** v0.9.3

**Release Date:** 2026-01-09

![DefaultView](https://github.com/user-attachments/assets/afa44bbe-99a1-45f1-96e5-ee5c0beffe2b)

**You'll need...**

- Linode API/PAT Key with Domain R/W Access
- Linode-CLI Domain Record ID
- Linode-CLI Subdomain Record ID

## Build Process

```shell
venv\Scripts\activate
pyinstaller --onefile --noconsole --add-data "template.ini;." --name GoobyDDNS_version app.py
```

Linux Users should consider [GoobyDDNS_Linux](https://github.com/GoobyFRS/GoobyDDNS)
