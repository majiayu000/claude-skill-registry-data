---
name: fleet-standard-adoption
description: Use when bringing this repo into compliance with a GeneFoundry fleet standard (tool-naming, response-envelope, container-hardening, versioning, MCP transport, or logging) or closing its tracking issue.
---

# Fleet-Standard Adoption

Follow `AGENTS.md` first. The canonical standards live under `../genefoundry-router/docs/` (the sibling router repo for `*-link`; `docs/` in the router):

- `TOOL-NAMING-STANDARD-v1.md` — `verb_noun` snake_case, stable, collision-free names (lets the router drop any `transform`).
- `RESPONSE-ENVELOPE-STANDARD-v1.1.md` (current; supersedes v1) — `success`, the payload, flat execution-error fields (`error_code` / `message` / `retryable` / `recovery_action`), and `_meta` (`data_version`). v1.1 adds **untrusted-content fencing** and **error-message sanitation** (fixed/enum error fields — never reflect caller-supplied or upstream text into caller-visible fields or logs; see the FastMCP not-found reflection guard). The nested `error:{...}` shape is deferred — don't use it.
- `CONTAINER-HARDENING-STANDARD-v1.md` — non-root, read-only, cap-drop, digest-pin, Trivy + SBOM.
- `VERSIONING-STANDARD-v1.md` — single-source metadata version; no `serverInfo.version` framework leak.
- `MCP-TRANSPORT-STANDARD-v1.md` — single stateless `/mcp` (no 307 split), canonical `serverInfo` / health.
- Logging & CLI Standard v1 — structured logging + CLI conventions (canonical text tracked per-repo; no router doc).

## Workflow

1. Read the standard's **Definition of Done**; check this repo against it.
2. Apply the smallest change that meets the DoD; reuse the router's reference implementation rather than reinventing.
3. Add or update the **guard test** the standard specifies so the change can't regress.
4. Run `make ci-local`; note residual risk.
5. Close the standard's tracking issue with a one-line CHANGELOG note.

## Common mistakes

- Adding router-side workarounds instead of fixing the backend to the standard.
- Meeting the letter without the guard test — it regresses on the next change.
