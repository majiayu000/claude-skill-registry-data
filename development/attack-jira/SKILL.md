---
name: attack-jira
description: "JIRA hunting — unauthenticated dashboards, filters, and misconfigurations leading to sensitive data exposure"
category: "configuration"
version: "1.0"
author: "bountyreper-official"
tags:
  - jira
  - information-disclosure
tech_stack:
  - jira
cwe_ids:
  - CWE-200
  - CWE-306
chains_with:
  - wstg-conf-01
prerequisites: []
---

# JIRA Hunting

## Objective

Find exposed JIRA instances with unauthenticated access to boards, filters, and issue data.

> **Attribution:** Methodology from [KathanP19/HowToHunt — JIRA](https://github.com/KathanP19/HowToHunt/tree/master/JIRA). Licensed GPL-3.0.

## Testing Methodology

```bash
# Detect JIRA
curl -s https://target.com | grep -i "atlassian\|jira"
curl -s https://target.atlassian.net -o /dev/null -w "%{http_code}\n"

# Common paths
for p in /secure/Dashboard.jspa /rest/api/2/dashboard /rest/api/2/filter /secure/ConfigurePortalPages!default.jspa; do
  curl -s https://target.atlassian.net$p | head -20
done

# Check for public filters/projects
curl -s "https://target.atlassian.net/rest/api/2/search?jql=project%20is%20not%20EMPTY" | jq '.issues[0]'

# Unauthenticated board access
curl -s https://target.atlassian.net/rest/agile/1.0/board | jq
```

## References

- [HowToHunt — JIRA](https://github.com/KathanP19/HowToHunt/tree/master/JIRA)
