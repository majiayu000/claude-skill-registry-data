---
name: attack-broken-link-hijacking
description: "Broken link hijacking — takeover via expired domains and broken external links"
category: "configuration"
version: "1.0"
author: "bountyreper-official"
tags:
  - broken-link
  - hijacking
  - takeover
tech_stack:
  - web
cwe_ids:
  - CWE-829
chains_with:
  - recon-hunter
  - attack-subdomain-takeover
prerequisites: []
---

# Broken Link Hijacking

## Objective

Hijack broken external links that point to expired or unregistered domains.

> **Attribution:** Methodology from [KathanP19/HowToHunt — BrokenLinkHijacking](https://github.com/KathanP19/HowToHunt/tree/master/BrokenLinkHijacking). Licensed GPL-3.0.

## Testing Methodology

```bash
# Extract external links
curl -s https://target.com | grep -o 'href="https://[^"]*"' | cut -d'"' -f2 | sort -u > links.txt

# Check each for 404 / unregistered
for url in $(cat links.txt); do
  domain=$(echo $url | cut -d'/' -f3)
  curl -s -o /dev/null -w "%{http_code} $domain\n" "https://$domain" | grep "000\|404"
  # Check if domain available for registration
  whois $domain | grep -i "no match\|available"
done

# Also check JS files for broken links
curl -s https://target.com/app.js | grep -o 'https://[^"]*'
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Broken link to unregistered domain you can claim | High (P2) |
| Broken link to expired service (S3, Heroku) | High (P2) |

## References

- [HowToHunt — BrokenLinkHijacking](https://github.com/KathanP19/HowToHunt/tree/master/BrokenLinkHijacking)
