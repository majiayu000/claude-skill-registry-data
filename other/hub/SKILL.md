---
name: hub
description: "Open the AOS Hub on 127.0.0.1:7900 (services, plan kits, store) or stop/status it. Generated from plugin-commands.json; invoke as $bdb-aos:hub."
---

Run `aos hub` to start the AOS Hub and report the URL (`http://127.0.0.1:7900`). On demand: if the hub already answers, it only opens the browser. `aos hub stop` stops it, `aos hub restart` stops and starts it again, `aos hub status [--json]` reports state. Never store secrets or tokens. Arguments: whatever the user wrote after the skill name
