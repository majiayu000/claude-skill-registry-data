---
name: oe-backend-prod-hardening
description: Production hardening review for the OpenEvent backend. Use when scanning for LLM smells, noisy prints, swallowed exceptions, dev-only defaults, fallback diagnostic leakage, and inconsistent error/logging patterns; produce a prioritized, PR-sized cleanup plan.
---

# oe-backend-prod-hardening

## Audit workflow (tight + actionable)

1. Scan for runtime smells:
   - `rg -n "print\\(" backend`
   - `rg -n "except Exception\\s*:\\s*(pass)?$" backend`
   - `rg -n "OE_FALLBACK_DIAGNOSTICS|FALLBACK" backend`
   - `rg -n "ENABLE_DANGEROUS_ENDPOINTS" backend`

2. Classify findings:
   - **User-visible** (must not leak diagnostics)
   - **Ops-visible** (structured logs, trace events)
   - **Dev-only** (move to scripts / gated)

3. Convert into a PR ladder:
   - One concern per PR: logging, error handling, config defaults, MCP bootstrap, etc.

## Canonical reference

- Add/maintain items in `docs/internal/BACKEND_REFACTORING_PLAN_DEC_2025_ADDENDUM.md`.

