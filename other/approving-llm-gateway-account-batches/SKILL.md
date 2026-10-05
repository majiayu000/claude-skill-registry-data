---
name: approving-llm-gateway-account-batches
description: Use when pending LLM Gateway account-contribution requests need to be preflighted, validated, issued, patched, and usage-refreshed in bulk through the admin API, including deterministic proxy assignment and per-account concurrency settings.
---

# Approving LLM Gateway Account Batches

Use this skill after public account-contribution requests are already queued as
`pending`. It automates the admin side:

1. fetch pending requests,
2. preflight each request by attempting refresh and probing Codex models through
   the local `http://127.0.0.1:11116` proxy,
3. validate each request,
4. approve and issue each account,
5. patch the imported account with proxy, request settings, and
   `auto_refresh_enabled`,
6. attempt a best-effort usage refresh for the imported account.

This skill does not bypass the existing review flow. It only drives the
existing admin API in batch form.

## When To Use

- The public batch submit step already created `pending` requests.
- You want to process one batch end to end through admin APIs.
- Imported Codex accounts should receive standard settings after issue.
- Some imported Codex auth bundles may have usable access tokens but broken or
  intentionally short-lived refresh credentials.
- Imported Codex accounts should still be issuable when direct models access
  works even if OAuth refresh is broken.

## Admin API Assumptions

- Admin base examples:
  - `http://127.0.0.1:19182`
  - `http://127.0.0.1:19082`
- Required routes:
  - `GET /admin/llm-gateway/account-contribution-requests`
  - `POST /admin/llm-gateway/account-contribution-requests/{id}/validate`
  - `POST /admin/llm-gateway/account-contribution-requests/{id}/approve-and-issue`
  - `PATCH /admin/llm-gateway/accounts/{name}`
  - `POST /admin/llm-gateway/accounts/{name}/refresh-usage`
  - `GET /admin/llm-gateway/accounts`
  - `GET /admin/llm-gateway/proxy-configs`

## Preferred Workflow

1. Confirm the batch prefix and expected request count.
2. Run a dry run first.
3. Process only matching `pending` requests.
4. Preflight refresh and direct models access before validate.
5. Treat successful models access as the issue gate.
6. Skip validate and issue when the models probe fails.
7. If refresh preflight fails but models succeed, still issue the account and
   patch `auto_refresh_enabled = false`.
8. Patch imported accounts immediately after issue.
9. Attempt post-issue usage refresh through the dedicated usage endpoint.
10. If usage refresh fails, keep the issued account and record the failure, but
   do not roll back or mark the whole batch item as failed.
11. Verify all matching requests moved out of `pending`.

## Proxy Assignment Rule

- Only consider `active` proxy configs.
- Count current usage from `active` Codex accounts with `proxy_config_id`.
- Choose the proxy with the lowest current count.
- Break ties by proxy name for deterministic output.
- Update the in-memory count after each assignment so one batch is balanced.

## Standard Patch Settings

- `auto_refresh_enabled = refresh_preflight_ok`
- `request_max_concurrency = 3`
- `request_min_start_interval_ms = random[100, 1000]`
- `proxy_mode = fixed`
- `proxy_config_id = selected least-used proxy`
- post-issue usage refresh is best-effort and does not block a models-usable
  account from being considered successfully issued

## Helper Script

Run:

```bash
python3 skills/approving-llm-gateway-account-batches/scripts/approve_account_contribution_batch.py --help
```

Dry run:

```bash
python3 skills/approving-llm-gateway-account-batches/scripts/approve_account_contribution_batch.py \
  --admin-base-url "http://127.0.0.1:19182" \
  --account-prefix "pickup7_" \
  --expected-count 20 \
  --admin-note "batch validate and issue"
```

Real run:

```bash
python3 skills/approving-llm-gateway-account-batches/scripts/approve_account_contribution_batch.py \
  --admin-base-url "http://127.0.0.1:19182" \
  --account-prefix "pickup7_" \
  --expected-count 20 \
  --admin-note "batch validate and issue" \
  --apply
```

Real run with explicit refresh tuning:

```bash
python3 skills/approving-llm-gateway-account-batches/scripts/approve_account_contribution_batch.py \
  --admin-base-url "http://127.0.0.1:19182" \
  --account-prefix "pickup7_" \
  --expected-count 20 \
  --admin-note "batch validate and issue" \
  --codex-proxy-url "http://127.0.0.1:11116" \
  --refresh-max-attempts 6 \
  --refresh-retry-delay-seconds 2 \
  --apply
```

## Notes

- Prefer local pb-mapper admin access on `127.0.0.1:19182` when available.
- Default Codex preflight proxy is `http://127.0.0.1:11116`.
- The script prints per-account progress with immediate flush, so long-running
  preflight/validate/issue/usage-refresh steps stay observable.
- The script does not write raw request tokens into the result JSON. It records
  only preflight conclusions such as models success, refresh success, and the
  chosen `auto_refresh_enabled` value.
- The script stops neither validation, issue, nor usage refresh routing logic
  inside the backend; it only sequences admin calls.
- The script records one JSON result file under `/tmp/`.
