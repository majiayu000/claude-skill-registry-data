---
name: submitting-llm-gateway-account-batches
description: Use when importing a local directory of Codex auth JSON files into StaticFlow's public LLM Gateway account-contribution review queue, especially when the single public submit endpoint is too slow because of per-request rate limiting.
---

# Submitting LLM Gateway Account Batches

Use this skill to queue many Codex auth JSON files through the public batch
submission API. This skill does not bypass review. It only creates `pending`
account-contribution requests for later admin validation and approval.

## When To Use

- The user has a directory of Codex account JSON files.
- The goal is to make them appear under the LLM Gateway admin review queue.
- The public single-submit endpoint is too slow because it is rate-limited per
  request.

## Public API

- Endpoint:
  `POST <api-base>/llm-gateway/account-contribution-requests/batch-submit`
- `api-base` examples:
  `http://127.0.0.1:19080/api`
  `https://ackingliu.top/api`
- Each batch request still goes through the public submission path and keeps the
  existing approval workflow.

## Preferred Workflow

1. Confirm the source directory and count `*.json` files.
2. Before any real submission, ask the user to confirm the reviewer-facing
   `contributor_message` and whether `requester_email` should be included.
3. Do not infer `requester_email` or `contributor_message` from JSON file
   contents.
4. Use the helper script with `--dry-run` first.
5. Submit the real batch.
6. Report `created_count`, `invalid_count`, and `conflict_count`.
7. Do not paste tokens or raw auth JSON into the chat.

## Helper Script

Run:

```bash
bash skills/submitting-llm-gateway-account-batches/scripts/submit-public-batch.sh --help
```

Typical dry run:

```bash
bash skills/submitting-llm-gateway-account-batches/scripts/submit-public-batch.sh \
  --dir "/mnt/c/Users/23946/Downloads/pickup-plus-json (5)" \
  --base-url "http://127.0.0.1:19080/api" \
  --message "batch submit from local Codex auth JSON files" \
  --dry-run
```

Typical real run:

```bash
bash skills/submitting-llm-gateway-account-batches/scripts/submit-public-batch.sh \
  --dir "/mnt/c/Users/23946/Downloads/pickup-plus-json (5)" \
  --base-url "http://127.0.0.1:19080/api" \
  --message "batch submit from local Codex auth JSON files"
```

Real run with explicit requester email:

```bash
bash skills/submitting-llm-gateway-account-batches/scripts/submit-public-batch.sh \
  --dir "/mnt/c/Users/23946/Downloads/pickup-plus-json (5)" \
  --base-url "http://127.0.0.1:19080/api" \
  --message "batch submit from local Codex auth JSON files" \
  --requester-email "user@example.com"
```

## Script Behavior

- Scans one directory level for `*.json`, sorted by filename.
- Derives a safe `account_name` from the filename stem and appends a short hash
  so names stay unique and within the backend limit.
- Sends each file as one batch item with `auth_json` equal to the file content.
- Uses top-level `contributor_message` for all items.
- Includes `requester_email` only when the operator passes
  `--requester-email`.
- Splits oversized directories into batches and waits between batch requests so
  public rate limiting stays respected.

## Notes

- Treat `contributor_message` and `requester_email` as user-confirmed input.
- If the user does not want an email attached, omit `--requester-email`.
- Prefer `--batch-size 200` or lower.
- Use `--prefix` when you want a stable namespace for derived account names.
- The backend returns per-item statuses:
  `pending`, `invalid`, `conflict`.
