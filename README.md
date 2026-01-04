# GoobyDDNS-Windows

GoobyDDNS Client for Windows. It's like the NoIP DUC but for your own domain and with Akamai / Linode Name Servers. __I'll add multi-platform support at 10 Stars__

## You'll Need

- Linode API/PAT Key with Domain R/W Access
- Linode-CLI Domain Record ID
- Linode-CLI Subdomain Record ID

### Build Process

```shell
venv\Scripts\activate
pyinstaller --onefile --noconsole --add-data "template.ini;." --add-data "goobyddns.ico;." app.py
```
