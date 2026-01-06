# GoobyDDNS_Windows

GoobyDDNS Client for Windows. It's like the NoIP DUC but for your own domain and with Akamai / Linode Name Servers. __I'll add multi-platform support at 10 Stars.__

![img](URL)

**You'll need...**

- Linode API/PAT Key with Domain R/W Access
- Linode-CLI Domain Record ID
- Linode-CLI Subdomain Record ID

## Build Process

```shell
venv\Scripts\activate
pyinstaller --onefile --noconsole --add-data "template.ini;." --name GoobyDDNS app.py
```

Linux Users should consider [GoobyDDNS_Linux]()
