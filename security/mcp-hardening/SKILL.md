---
name: mcp-hardening
description: "Audit MCP authorization, transport, filesystem/network boundaries, tenant isolation, input limits and safe failure with evidence-backed checks."
---
# MCP security review

Record server/client/SDK versions, transport, deployment exposure and tool privileges. Consult the current official security guidance: https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices and the specification selected by the project. Different transports have different authorization requirements.

| Boundary | Evidence required |
|---|---|
| Authentication/authorization | Protected operations reject missing, expired, wrong-audience and insufficient-scope credentials. No token passthrough to unrelated upstreams. Explicitly justify any unauthenticated health/metrics route and ensure it discloses no sensitive data. |
| Origin/Host | HTTP Origin and Host policies tested separately; unexpected origins rejected under the selected transport specification. Local-only binding alone is not protection from DNS rebinding. |
| Outbound requests | Allowlist intended destinations; validate resolved addresses and redirects, block unintended local/link-local/metadata access, and prevent DNS validation-to-connect races. Test IPv4/IPv6, alternate representations and redirect chains. |
| Filesystem | Validate canonical path containment with path components, not string-prefix tests. `Path.resolve()` and `realpath()` both resolve symlinks; neither alone prevents a concurrent symlink swap. Use race-resistant directory-relative operations and no-follow controls for hostile writable trees. |
| Tenant isolation | Derive allowed scope from authenticated identity; every read, write, list and session operation enforces it. User-supplied namespaces cannot expand authority. |
| Input/resources | Validate schemas, bound payloads, response size, concurrency, sessions and deadlines. Parameterize queries and use argv subprocess calls. Propagate cancellation. |
| Rate limits | Bound expensive work per principal and globally; handle quota/timeout failures explicitly. |
| Transport | Protect credentials in transit; default to local binding, expose remotely only with approved TLS/auth/network controls. |
| Process/container | Least-privilege identity, minimal mounts/devices/capabilities, no privileged control sockets. Test actual deployment controls. |
| Configuration | Missing required permissions/secrets fail closed. Empty allowlists never imply wildcard authority. Configuration errors must be visible. |

For each item report PASS, FAIL, NOT_RUN or N/A with reason, exact evidence, impact and owner. Do not certify production readiness by counting nine passing boxes. Any unverified material boundary remains unresolved. Use disposable fixtures for traversal, SSRF and cross-tenant tests; obtain authorization before testing live systems.
