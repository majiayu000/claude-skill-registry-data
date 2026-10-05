---
name: gpt2api-rs-admin
description: Use when operating the full gpt2api-rs image gateway, including local service lifecycle, admin control-plane work, public image-generation APIs, and the StaticFlow /admin/gpt2api-rs integration page.
---

# gpt2api-rs Operator

Use this skill when the user wants to operate the standalone `gpt2api-rs`
service in `deps/gpt2api_rs`, validate its OpenAI-compatible image APIs, or
drive it through StaticFlow's `/admin/gpt2api-rs` page.

## Scope

This skill covers the full surface:

- Service bootstrap and local runtime checks
- Admin control plane
  - `/admin/status`
  - `/admin/accounts`
  - `/admin/accounts/import`
  - `/admin/accounts/refresh`
  - `/admin/accounts/update`
  - `/admin/keys`
  - `/admin/usage`
- Public API compatibility
  - `/auth/login`
  - `/version`
  - `/v1/models`
  - `/v1/images/generations`
  - `/v1/images/edits`
  - `/v1/chat/completions`
  - `/v1/responses`
- StaticFlow integration
  - config file `conf/gpt2api-rs.json`
  - backend admin proxy `/admin/gpt2api-rs/*`
  - frontend page `/admin/gpt2api-rs`

This skill is not for CPA-pool style remote account import. It is focused on
the local service, its direct REST surface, and the StaticFlow admin wrapper.

## Prerequisites

- A running `gpt2api-rs` process or the ability to start one
- A storage directory, for example `/tmp/gpt2api`
- An admin token for the service
- A local HTTP proxy if upstream ChatGPT Web calls must go through one
  - For this project, the common requirement is `127.0.0.1:11118`
- Imported ChatGPT credentials if you want to test real image generation

## Service Lifecycle

Start the service:

```bash
cd /home/ts_user/rust_pro/static_flow/deps/gpt2api_rs
cargo run -- serve \
  --listen 127.0.0.1:8787 \
  --storage-dir /tmp/gpt2api \
  --admin-token "$ADMIN_TOKEN"
```

Production/local-public runs should use the release binary, not `cargo run`.
When the StaticFlow backend is live on this host, build with `--jobs 1` and
start from `target/release/gpt2api-rs`.

Email notifications reuse StaticFlow's account config file:

```text
backend/.local/email_accounts.json
```

or an explicit path from `GPT2API_EMAIL_ACCOUNTS_FILE` / `EMAIL_ACCOUNTS_FILE`.
The file format is the same as `backend/email_accounts.example.json`; gpt2api-rs
uses `public_mailbox` for SMTP credentials and display name. Also set
`GPT2API_PUBLIC_BASE_URL` or `SITE_BASE_URL` so completion emails link to
`/gpt2api/share/<token>`. `GPT2API_SMTP_*` environment variables still override
the file values when necessary.

Health check:

```bash
curl http://127.0.0.1:8787/healthz
```

Version check:

```bash
curl http://127.0.0.1:8787/version
```

## Admin Operations

Read the admin status snapshot:

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://127.0.0.1:8787/admin/status
```

List accounts:

```bash
cd /home/ts_user/rust_pro/static_flow/deps/gpt2api_rs
cargo run -- admin \
  --base-url http://127.0.0.1:8787 \
  --admin-token "$ADMIN_TOKEN" \
  accounts list \
  --json
```

List keys:

```bash
cd /home/ts_user/rust_pro/static_flow/deps/gpt2api_rs
cargo run -- admin \
  --base-url http://127.0.0.1:8787 \
  --admin-token "$ADMIN_TOKEN" \
  keys list \
  --json
```

List recent usage:

```bash
cd /home/ts_user/rust_pro/static_flow/deps/gpt2api_rs
cargo run -- admin \
  --base-url http://127.0.0.1:8787 \
  --admin-token "$ADMIN_TOKEN" \
  usage list \
  --limit 50 \
  --json
```

Import accounts by access token or session JSON:

```bash
curl -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/admin/accounts/import \
  -d '{
    "access_tokens": ["<access-token>"],
    "session_jsons": []
  }'
```

Refresh all accounts:

```bash
curl -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/admin/accounts/refresh \
  -d '{"access_tokens":[]}'
```

Update one account:

```bash
curl -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/admin/accounts/update \
  -d '{
    "access_token": "<access-token>",
    "plan_type": "pro",
    "status": "active",
    "quota_remaining": 10,
    "request_max_concurrency": 1,
    "request_min_start_interval_ms": 0
  }'
```

Delete one account:

```bash
curl -X DELETE \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/admin/accounts \
  -d '{"access_tokens":["<access-token>"]}'
```

## Public API Operations

Login probe:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  http://127.0.0.1:8787/auth/login
```

List models:

```bash
curl -H "Authorization: Bearer $API_KEY" \
  http://127.0.0.1:8787/v1/models
```

Generate images:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/v1/images/generations \
  -d '{
    "model": "gpt-image-1",
    "prompt": "Draw a cinematic anime heroine with rain-soaked neon reflections.",
    "n": 1
  }'
```

Edit images:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -F "model=gpt-image-1" \
  -F "prompt=Keep the same style, change the outfit and lighting" \
  -F "n=1" \
  -F "image=@/path/to/input.png" \
  http://127.0.0.1:8787/v1/images/edits
```

Chat-completions style image request:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/v1/chat/completions \
  -d '{
    "model": "gpt-image-1",
    "modalities": ["image"],
    "messages": [
      {
        "role": "user",
        "content": [
          { "type": "text", "text": "Generate a painterly anime portrait." }
        ]
      }
    ]
  }'
```

Responses-style image request:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8787/v1/responses \
  -d '{
    "model": "gpt-5",
    "input": "Generate a moody anime city poster.",
    "tools": [{ "type": "image_generation" }]
  }'
```

## StaticFlow Integration

StaticFlow now owns a local config file:

```text
conf/gpt2api-rs.json
```

Shape:

```json
{
  "base_url": "",
  "admin_token": "",
  "api_key": "",
  "timeout_seconds": 60
}
```

StaticFlow backend reads and proxies this config through:

- `GET /admin/gpt2api-rs/config`
- `POST /admin/gpt2api-rs/config`
- `GET /admin/gpt2api-rs/status`
- `GET /admin/gpt2api-rs/version`
- `GET /admin/gpt2api-rs/models`
- `POST /admin/gpt2api-rs/auth/login`
- `GET /admin/gpt2api-rs/accounts`
- `POST /admin/gpt2api-rs/accounts/import`
- `DELETE /admin/gpt2api-rs/accounts`
- `POST /admin/gpt2api-rs/accounts/refresh`
- `POST /admin/gpt2api-rs/accounts/update`
- `GET /admin/gpt2api-rs/keys`
- `GET /admin/gpt2api-rs/usage`
- `POST /admin/gpt2api-rs/images/generations`
- `POST /admin/gpt2api-rs/images/edits`
- `POST /admin/gpt2api-rs/chat/completions`
- `POST /admin/gpt2api-rs/responses`

Frontend entry:

```text
/admin/gpt2api-rs
```

This page is protected by the same StaticFlow admin gate as other admin pages:

- localhost access, or
- `x-admin-token` if the backend is configured with `ADMIN_TOKEN`

The browser never talks to `gpt2api-rs` directly. It always goes through
StaticFlow's backend admin proxy.

## Local Verification Workflow

1. Start `gpt2api-rs`
2. Start a local StaticFlow backend on a non-production port
3. Point `conf/gpt2api-rs.json` or `GPT2API_RS_CONFIG` at the test instance
4. Build or serve the frontend locally
5. Open `/admin/gpt2api-rs`
6. Verify:
   - config save/load
   - status/version/models/login
   - account import / refresh / delete / update
   - key list / usage list
   - image generation
   - image edit
   - chat completions image request
   - responses image request

## Proxy Notes

If the upstream ChatGPT Web flow must go through a local HTTP proxy, export it
before starting `gpt2api-rs`, for example:

```bash
export http_proxy=http://127.0.0.1:11118
export https_proxy=http://127.0.0.1:11118
```

## Troubleshooting

- `401 authorization is invalid`
  - Check whether you used the admin token or the public API key on the
    correct endpoint family
- `status` works but generation fails
  - The service may be up while imported accounts are empty, invalid, or
    limited
- image edit returns `image file is required`
  - The request did not send multipart correctly, or the StaticFlow admin page
    did not finish loading the file into base64 first
- StaticFlow admin page loads but every action fails
  - Check `conf/gpt2api-rs.json`
  - Check StaticFlow backend admin access rules
  - Check that StaticFlow can reach the configured `base_url`
