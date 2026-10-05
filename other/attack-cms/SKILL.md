---
name: attack-cms
description: "CMS hunting — WordPress, Drupal, AEM, Moodle enumeration, plugin exploits, and misconfiguration leading to RCE"
category: "configuration"
version: "1.0"
author: "bountyreper-official"
tags:
  - cms
  - wordpress
  - drupal
  - aem
  - moodle
  - rce
tech_stack:
  - wordpress
  - drupal
  - aem
  - moodle
  - php
cwe_ids:
  - CWE-94
  - CWE-20
chains_with:
  - wstg-conf-01
  - wstg-injection
prerequisites: []
---

# CMS Hunting Methodology

## Objective

Identify CMS-specific exposures in WordPress, Drupal, AEM, and Moodle that lead to information disclosure, authentication bypass, or RCE via plugins and misconfigurations.

> **Attribution:** Methods from [KathanP19/HowToHunt — CMS](https://github.com/KathanP19/HowToHunt/tree/master/CMS) (WordPress, Drupal, Moodle, AEM). Licensed GPL-3.0.

## Testing Methodology

### WordPress

```bash
# Enumeration
wpscan --url https://target.com --enumerate p,ut,vt,cb,dbe
curl https://target.com/wp-json/wp/v2/users # user enumeration
curl https://target.com/readme.html | grep WordPress
curl https://target.com/wp-config.php.bak

# Plugin exploits
# Check for vulnerable plugins: wp-content/plugins/<plugin>/readme.txt
# Test upload bypass via plugin file upload
```

Check:
- `xmlrpc.php` enabled → brute force / pingback SSRF
- `wp-json` exposed → user enumeration
- Backup files: `wp-config.php~`, `.bak`

### Drupal

```bash
# Version
curl -s https://target.com/CHANGELOG.txt | head
curl -s https://target.com/core/CHANGELOG.txt | head

# Drupalgeddon check
curl https://target.com/?q=user/password
```

### AEM

```bash
# AEM specific paths
curl https://target.com/libs/granite/core/content/login.html
curl https://target.com/etc.json
curl https://target.com/crx/packmgr/list.jsp
curl https://target.com/system/console/bundles
# Check for Sling post servlet RCE
```

### Moodle

```bash
curl https://target.com/admin/tool/task/scheduledtasks.php
curl https://target.com/mod/assign/view.php
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| RCE via plugin/CMS core | Critical (P1) |
| Admin access via default creds / misconfig | High (P2) |
| User enumeration / info disclosure | Medium (P3) |
| Version disclosure with known CVE | Medium (P3) |

## References

- [HowToHunt — CMS](https://github.com/KathanP19/HowToHunt/tree/master/CMS)
