---
name: code-quality-review
description: Use when reviewing a diff, PR, or change set for correctness and quality before merge or handoff. For a deep security-only pass, use security-review instead.
---

# Code-Quality Review

Follow `AGENTS.md` first. Run the mechanical pass first (`make ci-local`, and `/code-review` if available); this skill is the judgment layer on top.

## Scan order (security-first)

Review in this order — don't rush past a step to get to style nits:

1. **Secrets** — hardcoded tokens/keys/URLs that belong in runtime `env`.
2. **Input validation** — untrusted args validated against Pydantic schemas/ranges before use.
3. **Trust boundary** — no caller-token passthrough to upstreams; fixed upstream host (no SSRF); Origin validation intact. (For the full boundary review, use `security-review`.)
4. **Dependencies** — new deps pinned in `uv.lock`, mainstream, no post-install hooks.
5. **Correctness** — logic, error handling, edge cases, response-envelope shape (`success` + flat `error_code`/`message`/`_meta`).
6. **Efficiency** — N+1 upstream calls, unbounded loops/inputs, missing size caps.
7. **Style / fleet rules** — modern typing (`X | None`), the per-file line budget (`scripts/check_file_size.py`), thin handlers, no PII in logs.

## Report each finding

Group by file. For each: **severity** (critical = bug/security · warning = fix before merge · suggestion = optional), the issue, and a concrete fix. Anchor to `file:line`.

## Common mistakes

- Reporting style nits while missing a token-passthrough or SSRF regression.
- Vague findings ("improve error handling") with no location or fix.
- Approving a diff that grows a module past the LOC budget with no split.
