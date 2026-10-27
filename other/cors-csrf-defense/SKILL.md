---
name: cors-csrf-defense
description: "Cross-Origin Resource Sharing (CORS) whitelisting, preflight caching, and anti-CSRF token verification."
---

# CORS & CSRF Defense Protocol

1. Never use Access-Control-Allow-Origin: * with credentials.
2. Whitelist explicit origin domains dynamically.
3. Require custom headers (e.g. X-Requested-With) on state-changing API mutations.
