---
name: attack-web-source-review
description: "Web source code review — manual JS, HTML, and API source analysis for hidden endpoints and secrets"
category: "information-gathering"
version: "1.0"
author: "bountyreper-official"
tags:
  - source-review
  - js
  - secrets
tech_stack:
  - web
cwe_ids:
  - CWE-200
chains_with:
  - recon-hunter
  - wstg-info-02
prerequisites: []
---

# Web Source Review

## Objective

Manual review of client-side source for hidden endpoints, secrets, and logic flaws.

> **Attribution:** Methodology from [KathanP19/HowToHunt — Web_Source_Review](https://github.com/KathanP19/HowToHunt/tree/master/Web_Source_Review). Licensed GPL-3.0.

## Testing Methodology

```bash
# Extract JS files
curl -s https://target.com | grep -o 'src="[^"]*\.js[^"]*"' | cut -d'"' -f2 > js.txt
cat js.txt | while read js; do curl -s "https://target.com$js" | grep -E "api|key|secret|token|admin" | head; done

# Search for hidden endpoints
grep -r "api/" js_files/
grep -r "fetch\|axios\|XMLHttpRequest" js_files/

# Check HTML comments
curl -s https://target.com | grep -i "comment\|todo\|fixme"

# Use LinkFinder
python3 LinkFinder.py -i https://target.com -o cli
```

## References

- [HowToHunt — Web Source Review](https://github.com/KathanP19/HowToHunt/tree/master/Web_Source_Review)
