---
name: db-redis-rce
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Exploit unauthenticated Redis instances for remote code execution via CONFIG SET dir/dbfilename to write cron jobs, SSH authorized_keys, or webshells.
subdomain: database-security
tags:
  - redis
  - rce
  - config-set
  - cron
  - ssh-keys
  - exploit
nist_csf:
  - DE.CM-04
mitre:
  - T1190
  - T1505
cwe:
  - CWE-78
  - CWE-306
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
