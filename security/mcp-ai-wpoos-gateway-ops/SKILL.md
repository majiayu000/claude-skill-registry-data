---
name: mcp-ai-wpoos-gateway-ops
description: Operational guide for the NV oOS MCP Gateway (addons/mcp-gateway → mirror nvoos-mcp-gateway → Cloudways Velocity at mcp.nvoos.pro, issue #6902). Covers the live site-slug map, public-key management (GATEWAY_PUBLIC_KEYS syntax, rotation, the PUBLIC_SITE_SLUGS privacy filter), the upstream-401 token re-mint loop, deploy verification (version marker, 0.2.0 fingerprints, stale-deploy recovery), registry publishing via mcp-publisher (100-char description cap, device-flow expiry, verification URLs), the directory-submission pack + demo-key rule, asset shipping, and the test gotchas. Use when operating the gateway, debugging gateway auth/upstream errors, deploying to Velocity, or continuing the MCP directory submissions.
---

# mcp-ai-wpoos — Gateway ops

## What / where

- Canonical source: `addons/mcp-gateway/` (Node, express, zero-added-deps, env-configured, fail-closed).
- One-way mirror: `nvdigitalsolutions/nvoos-mcp-gateway` (`main`) via `.github/workflows/sync-mcp-gateway.yml` — snapshot commit per sync, no `--force`, version-guarded (older `package.json` versions are skipped). Never commit to the mirror directly.
- Deploy target: Cloudways Velocity at **`https://mcp.nvoos.pro`**. Auto-deploy fires on the mirror push; env vars are dashboard-only (no Cloudways API/MCP surface for Velocity).
- Tracking issue: **#6902**. Deploy guide: `docs/operations/deployment/mcp-gateway-velocity-setup.md`. Submission pack: `docs/operations/deployment/mcp-gateway-directory-submission.md`.

## Live map (verified 2026-11-01)

| Slug | Site | Visibility |
|---|---|---|
| `demo` | `https://nvoos.pro` | Public — demo key, listings |
| `sascha` | `https://nirmanawellness.nvdigital.solutions` | Private client — own key |
| `ideabits` | `https://ideabits.nvdigital.solutions` | Private client — own key |
| `console` | `https://console.nvoos.cloud` | (not bound at time of writing) |

- `PUBLIC_SITE_SLUGS=demo` — public `/health` reports only `demo`; `/health/full` (keyed) reports every site.
- Demo key (published in directory listings, **never in the repo**): bound to `demo` only, allowlisted `get_environment_status` + `deep_research`.
- Client sites carry their **own** public keys (one key may bind both ideabits+sascha when the same client owns them).

## Public keys — GATEWAY_PUBLIC_KEYS

- Syntax: `key=slug-a,slug-b;key2=slug-c` (or a JSON object `{"key":["slug-a"]}`).
  `;` = entry separator, `=` = key→sites, `,` = multiple sites. A trailing `;`
  is harmless. Whitespace is trimmed.
- Keys are 32-byte `base64url` (`node -e "console.log(require('crypto').randomBytes(32).toString('base64url'))"`)
  — the alphabet can never contain `;`, `,`, or `=`, so no quoting is needed.
  Minimum length 16 (`MIN_KEY_LENGTH`).
- **One variable, one line**: the Velocity dashboard must have a single
  `GATEWAY_PUBLIC_KEYS` row holding the whole map — duplicate rows do not
  merge.
- **Fail-closed**: a key bound to an unconfigured slug (no
  `NVOOS_SITE_<SLUG>_URL`/`_TOKEN`) is a boot error and takes the whole
  gateway down — add the site vars in the same env edit as the key.
- Rotation: new key in `GATEWAY_PUBLIC_KEYS`, old one in
  `GATEWAY_PUBLIC_KEYS_PREVIOUS` (accepted with a one-time warning), remove
  once consumers switched.
- `PUBLIC_SITE_SLUGS` (added 2026-11-01, PR #7347): comma-separated slugs
  visible on the public `/health`; unset/`*` = all (legacy). Hidden sites
  stay invisible publicly and their degradation does not flip the public
  `status`; `/health/full` always reports everything. Unknown slugs are
  **boot warnings, never fatal** (a typo hides sites — the safe direction).

## Upstream 401 playbook (the recurring failure)

Symptom: `tools/list` → `_meta.gateway.errors.<slug>: "upstream error (401)"`
(the gateway degrades gracefully — other sites keep flowing).

1. Identify the host: `GET /health/full` with any key → `sites.<slug>.url`.
2. Probe the site directly:
   `curl -s -X POST https://<host>/wp-json/mcp-ai/v1/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}'`
   — the plugin's structured `{"code":"wp_mcp_ai_mcp_auth_required",...}`
   401 means the **operator token is stale/rotated** (not a bot-wall; a
   Cloudways Anti-Bot/Imunify wall would return HTML/403).
3. Fix on the target site: Settings → External Operators → re-mint the
   demo/client operator's token (**full `op_xxxx.SECRET`**, both halves, no
   trailing whitespace) and set its Allowed tools (least privilege —
   e.g. `get_environment_status` for public demo keys).
4. Update `NVOOS_SITE_<SLUG>_TOKEN` in the Velocity env (env edits restart
   the app — `/health` `uptime` resets).
5. Verify: `tools/list` shows no `_meta.gateway.errors` + one safe
   `tools/call` (e.g. `<slug>.get_environment_status`).

## Deploy verification ladder

- **Version marker**: `/health.version` must equal `addons/mcp-gateway/package.json`'s
  `version`. The `VERSION` constant in `src/index.js` is a hardcoded string
  that must track it (PR #7345 added the comment + a health test that
  enforces the contract — a version bump that misses the constant now fails
  the suite). Historical: the 0.2.0 bump forgot it and `/health` lied 0.1.1.
- **0.2.0 fingerprints** (independent of the marker): `traceparent` response
  header + RFC 9558 `RateLimit-*` headers (the policy layer).
- **Restart clock**: `uptime` tells when the app last restarted — compare
  against the mirror-sync time to judge whether a deploy landed.
- **Stale deploy** (mirror advanced, `/health` version behind, uptime older
  than the sync): Velocity auto-deploy missed it → Deployment Manager shows
  a commit not in the mirror history → disconnect/reconnect the GitHub repo
  and redeploy (§7 of the setup guide). Also the CI-skip-marker incident:
  a squash body absorbing `[ci skip]` runs zero workflows — recover with a
  follow-up PR touching `addons/mcp-gateway/**` or
  `gh workflow run sync-mcp-gateway.yml --ref alpha-working`.
- **Env edit pitfall**: paste-append, never replace the whole env set — the
  replace dropped three site-var groups in one session (2026-11-01).

## Registry publishing (mcp-publisher)

- Binary: `C:/Users/rasta/.mcp-publisher/mcp-publisher.exe` (device-flow
  session stored on the machine; **the JWT expires — re-run
  `mcp-publisher login github` before publish**; the flow prints a GitHub
  device code and polls).
- `validate` hits the live registry schema (no auth). **`description` must
  be ≤ 100 chars** (422 otherwise; the bridge entry used 95).
- `publish` from the `addons/mcp-gateway/` dir (resolves `server.json` from
  the CWD). Entry: `io.github.nvdigitalsolutions/nvoos-mcp-gateway`
  (remote-only; no packages/ownership marker needed for remotes).
- Verify: `GET https://registry.modelcontextprotocol.io/v0.1/servers?search=<name>`
  → `count:1`, `_meta.io.modelcontextprotocol.registry/official.status: active`.
  Detail URL: `/v0.1/servers/<encodeURIComponent(name)>/versions/<version>`.
- Propagation: mcp.directory, PulseMCP, and Glama **auto-import from the
  official registry** — no manual submission; check +24h/+7d. Only
  **mcpservers.org** needs a manual form (https://mcpservers.org/submit).
- Demo-key rule: the key value is published **in each directory listing**
  but must never be committed to the repo or issues.

## Assets & tests

- `addons/mcp-gateway/assets/` is served at `/assets` (static middleware).
  Logo for listings: `https://mcp.nvoos.pro/assets/nvoos-logo.png`
  (512×512, converted from the brand favicon via PowerShell System.Drawing;
  ship the source JPG alongside).
- The local `.git/info/exclude` ignores `*.png`/`*.jpg` (per-worktree guard)
  — `git check-ignore -v <path>` before adding, then `git add -f` for
  deliberate assets.
- Tests: `npm test` hangs on Windows after the quota suites (pre-existing;
  run targeted files instead — `node --test src/routes/health.test.js
  src/utils/config.test.js src/middleware/auth.test.js`). `node --test <dir>`
  does not recurse — pass explicit files or the package script.

## Cross-references

- `mcp-ai-wpoos-schedule-anything-ops` — the Velocity deploy/mirror-sync
  mechanics shared with the other Velocity apps.
- `mcp-ai-wpoos-git-ops` — sibling-PR conflict resolution, shared-worktree
  rules, `.git/info/exclude` force-add.
- Docs: `docs/operations/deployment/mcp-gateway-velocity-setup.md`,
  `docs/operations/deployment/mcp-gateway-directory-submission.md`,
  `docs/project/proposals/061-mcp-registry-publishing-implementation-plan.md`.
