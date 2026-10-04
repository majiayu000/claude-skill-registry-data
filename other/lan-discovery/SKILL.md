---
name: lan-discovery
description: Implement DNS-SD/mDNS and beacon discovery for MCOS gateway advertisement.
disable-model-invocation: true
---

# LAN Discovery Skill

Procedure:

1. Read current beacon/discovery code.
2. Add/normalize DNS-SD registration for `_mcos._tcp`, `_mcos-mcp._tcp`, and `_mcos-onboarding._tcp`.
3. Include TXT metadata from `.claude/rules/30-mcp-gateway-discovery.md`.
4. Add `/.well-known/mcos.json`.
5. Add `/api/discovery` returning the same core data in JSON.
6. Add optional UDP JSON beacon fallback.
7. Keep discovery LAN-trust and no app-layer authentication.
8. Add tests that serialize expected advertisement metadata.

Output must include sample DNS-SD TXT fields and sample discovery JSON.
