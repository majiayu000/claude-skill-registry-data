---
name: iris-analytics
description: Connect a product repository to Iris analytics using OAuth MCP; guide sign-up/sign-in, reuse or create a project, inspect code, plan and add events with Chinese labels, create funnels, verify ingestion, and export data or PPTX reports. Use when the user asks to add product analytics, event tracking, funnels, Iris, or analytics reports.
---

# Iris Analytics

Use Iris through the user's OAuth-authorized MCP connection. Never ask for, display, or store an Iris password, access token, refresh token, project secret, or personal MCP token.

## Workflow

1. Inspect the repository before proposing events.
   - Run `node scripts/detect-project.mjs <repo>` from this skill directory when available.
   - Use its `source_roots`, `deploy_roots`, and `entrypoints` to identify maintainable source before reading generated output.
   - Identify framework, routes/pages, real account authentication state changes, forms, primary calls to action, success callbacks, and logout. A generic contest or application registration form is not account authentication by itself.
   - Read only. Do not edit yet.
   - Treat `recommended_domain` as a candidate, not proof. When `domain_conflict` is true, inspect the listed evidence and verify the live production host from deployment/nginx configuration or the public page before any Iris project match/create/update. Nginx `server_name` and canonical production URLs outrank stale `AppEnv` values.
2. Connect Iris.
   - If Iris MCP tools are unavailable, tell the user to add `https://iris.teown.com/mcp`; let the MCP client open OAuth.
   - If the browser opens login/registration, guide the user there. Do not automate credentials or verification codes unless the user explicitly provides the code for the active form.
   - Request only the scopes needed for this task. Start with `analytics:read`; add `workspace:write`, `report:export`, or `analytics:raw-export` only when needed.
   - Non-interactive `codex exec` validation needs an approvable local policy: `approval=never` rejects MCP tool calls. Prefer interactive approval; use `--approve-for-me` only after the user-approved prompt is constrained to exact targets and writes. This does not bypass OAuth scopes or project roles.
3. Reuse before creating.
   - Call `list_projects` and match the production project by a verified normalized domain or Mini Program AppID, then by exact name. Do not use a stale source-code environment mapping as the sole domain authority when deployment evidence conflicts.
   - If one unambiguous production project matches, reuse it. If none match, propose `create_project`. If multiple match, ask the user to choose.
   - For ingestion verification, separately match the exact name `<production project name> · 接入测试` and its non-production domain. Reuse that project across runs; create it only with the user's approved writes. Never send synthetic verification events to the production project by default.
   - Read `references/test-isolation.md` before creating or reusing a verification project.
4. Produce the complete plan before writes.
   - Event names: lowercase English `snake_case`.
   - Every business event has a concise Simplified Chinese label and description.
   - Include trigger, exact code location, safe properties, identity timing, and funnel membership.
   - Set `identity.mode` to `anonymous` or `authenticated`; do not infer account identity from a generic registration form.
   - Set `verification.strategy` to `reusable_test_project` with its deterministic test project name and domain.
   - Use 2–8 steps per funnel; prefer observable business outcomes over clicks.
   - Run `node scripts/validate-event-plan.mjs <plan.json>` when a JSON plan is produced.
5. Ask once for confirmation covering both repository edits and Iris configuration writes.
6. Apply idempotently.
   - Call `get_sdk_setup` for both the reusable test project and the production project. Test/development deployments use the test App ID; production configuration uses the production App ID.
   - Follow the stack-specific reference. Never edit minified or hashed bundles, or a detected `deploy_root`, directly; edit maintainable source and use the repository's build process.
   - Preserve existing analytics and project conventions.
   - Do not add duplicate SDK initialization or duplicate event calls on rerun.
   - For `identity.mode=authenticated`, call `identify(stableAccountId)` immediately after authentication succeeds and before the first authenticated success event. Call `reset()` on logout before another person can use the same client state.
   - For `identity.mode=anonymous`, do not add fake identity calls merely to satisfy static checks.
   - Do not use email, phone, OpenID, UnionID, or another direct personal identifier as the analytics identity. Prefer an internal opaque account ID.
   - Upsert dictionary entries with a new UUID `request_id` for each intended write. Before writing a funnel, call `list_funnels`: reuse an exact match, update one exact-name mismatch with `update_funnel`, and create only when no exact-name funnel exists. If multiple exact-name funnels exist, stop and ask which one to keep. Reuse the same UUID only when retrying that exact write.
   - If an existing Iris project's stored domain/AppID is stale and the live target is verified, use `update_project` with only the `domain` field plus `project_id` and a new UUID. Never change project type, App ID, secret, ownership, or membership as part of domain reconciliation.
   - For `upsert_event_dictionary`, map the plan's `event` to `item.event_type`. Property definitions use `property_key`, `label`, `value_type`, `is_required`, and `description`; map plan types `enum → string`, `boolean → bool`, and `count → number`.
7. Verify.
   - Run project tests/build.
   - Run `node scripts/verify-integration.mjs <repo> <plan.json>` for static integration checks.
   - Exercise the real UI flow against the reusable test project's App ID when the environment permits.
   - Query `get_events` and `get_funnel` on the test project after ingestion. Code presence or HTTP 200 alone is not ingestion proof.
   - Verify the production configuration statically and wait for a natural production event unless the user explicitly authorizes a synthetic production event.
   - State clearly when real interaction or ingestion is still unverified.
8. Export only on request.
   - Use `start_report_export` then poll `get_export_job` for PPTX.
   - Use `start_data_export` only after explaining that it exports redacted event rows and requires Owner/Admin.
   - Download links expire after 24 hours; do not commit or repost them.

## Privacy hard stops

Never track password or verification-code fields, cookies, authorization headers, access/refresh tokens, full query strings, raw form text, email, phone, bank-card or government-ID values. Do not add tracking that reads input values. Prefer enum/boolean/count properties with an explicit allowlist.

## Supported automation

- Vanilla JS/TS: read `references/web-instrumentation.md`.
- React + Vite: read `references/web-instrumentation.md`.
- Vue + Vite: read `references/web-instrumentation.md`.
- Legacy multi-root Web projects with maintainable `dev/` or similar source and generated `prd/` output: read `references/legacy-web-instrumentation.md`.
- Native WeChat Mini Program: read `references/wechat-miniprogram.md`.
- Next.js, Nuxt, Taro, uni-app, or unknown stacks: produce a manual plan and stop before edits unless the user supplies project-specific integration guidance.

Read `references/event-design.md` for event planning, `references/funnels.md` for funnel rules, `references/exports.md` for exports, and `references/security.md` for permission/privacy details as needed.
