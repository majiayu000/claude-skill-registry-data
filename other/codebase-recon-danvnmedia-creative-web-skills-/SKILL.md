---
name: codebase-recon
description: Use before non-trivial changes in an unfamiliar or mature repository to map real entry points, data flow, trust boundaries, similar working patterns, commands, tests, and deployment assumptions.
---
# Codebase Recon

1. Read project control-plane files first.
2. Locate the real entry point and trace the relevant user/request/data flow end to end.
3. Find at least one similar working implementation before inventing a new pattern.
4. Identify server/client boundaries, auth checks, persistence, external calls, and error handling.
5. Verify actual package scripts/commands; never invent a command because it is conventional.
6. Inspect nearby tests and runtime logs/errors.
7. Return a compact implementation map: key files, invariants, likely blast radius, unknowns, and verification route.
8. Stop exploring when enough evidence exists to make the bounded change safely.
