---
name: request-target-and-redirect
description: Authored regression cases for request targets and shell redirection.
---

Review `scripts/endpoints.py` before installation.

```bash
curl -H "Referer: https://allowed.example.invalid" https://upload.example.invalid/data
cat <input.txt>output.txt
curl https://[HOST]/setup
```
