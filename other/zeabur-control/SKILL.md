---
name: zeabur-control
description: Manage KobePlay and HillStreet Zeabur projects through the authenticated Zeabur MCP connection.
---

# Zeabur Control

Use the configured `zeabur` MCP connection for project, service, deployment, domain, port, environment, and log operations.

1. Inspect before mutation and match resources by verified IDs.
2. Never print or write secret values into reports, source, issues, or logs.
3. Never delete projects, services, domains, deployments, or volumes without explicit authorization.
4. Record rollback state before production-domain, secret, or persistent-volume changes.
5. Prefer immutable Docker digests and verify runtime logs, ports, TLS, and health after changes.
6. Report `PRODUCTION_VERIFIED` only after functional endpoint checks pass.

Canonical Open-Connect gateway:

- MCP: `https://open-connect.site/mcp`
- API: `https://open-connect.site/api/v1`
- OAuth issuer: `https://open-connect.site`

Open-System managed execution target (Hermes Agent fork):

- Dashboard: `open-system.space` on port `9119`
- API: `api.open-system.space` on port `8642`

Do not advertise an Open-System hostname as the Open-Connect MCP gateway. Open-Connect owns connectors, resources, skills, toolkits, MCP registration, prompts, and agent-control metadata; Open-System executes authorized work delegated by that control plane.

Never store `ZEABUR_TOKEN` or `MCP_BRIDGE_TOKEN` in this skill.
