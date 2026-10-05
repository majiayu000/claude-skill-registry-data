---
name: codex-reset-credits
description: Query Codex banked reset credits from the local Codex Desktop login state and report available reset count plus expiration times. Use when the user asks to check Codex reset credits, reset opportunities, reset chances, reset count, rate-limit reset credits, or expiration times; also use when the user provides a codex-reset-credits-skill or codex-reset-credits runbook link and asks Codex to query the result directly.
---

# Codex Reset Credits

## Overview

Query Codex banked reset credits through the bundled read-only script. Return a concise, sanitized answer with available count and expiration times.

## Workflow

1. Run the bundled script:

   ```sh
   python3 "$SKILL_DIR/scripts/query_reset_credits.py" --json
   ```

   If `$SKILL_DIR` is not available, locate this Skill folder by the directory containing this `SKILL.md`, then run `scripts/query_reset_credits.py` inside it.

2. Parse the sanitized JSON result.

3. Answer in the user's language using this format:

   ```markdown
   查到了。你当前有 `<available_count>` 个可用 Codex 重置机会。

   最早到期：`<earliest expires_at.time_local>`

   | # | 状态 | 类型 | 到期时间 | UTC |
   | --- | --- | --- | --- | --- |
   | 1 | `available` | `codex_rate_limits` | 2026-07-16 15:51:44 CST | 2026-07-16 07:51:44 UTC |
   ```

   Keep the answer concise. Do not wrap the table in a code block. Mention that output is sanitized only when useful or when sharing with someone else.

## Safety Rules

- Do not ask the user to paste access tokens.
- Do not print access tokens, full `auth.json`, full account ids, full credit ids, or raw backend responses.
- Do not write real backend responses to the workspace.
- Do not redeem reset credits or call mutation/control endpoints.
- Treat HTTP 401/403 as an auth/login problem, not proof that no reset credits exist.

## Failure Handling

If the script returns `ok: false`, report the error and next step:

- `missing_auth`: open Codex Desktop and log in.
- `invalid_auth_shape`: Codex auth storage changed or is unreadable by the script.
- `missing_access_token`: refresh or relogin Codex Desktop.
- `http_error` with 401/403: relogin Codex Desktop.
- `http_error` with 429: wait for `retry_after` when present.
- `invalid_json`: backend response shape changed; inspect endpoint behavior without exposing secrets.

## Link Runbook

When the user provides a link to `USE_WITH_CODEX.md`, follow that runbook. It exists for users who have not installed this Skill yet.

## Maintenance Reference

Read `references/api.md` only when debugging the endpoint, auth headers, or response-field mapping.
