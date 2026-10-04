---
name: external-api-onboarding
description: Configure external API keys, OAuth MCP connections, browser-assisted provider console setup, private .env storage, Codex MCP config, fallback audits, and smoke tests without exposing secrets. Use when Codex is asked to set up or repair external provider access for skills, MCP servers, browser-use, AnySearch, OpenRouter ICU, Figma, Notion, GitHub, Hugging Face, Kaggle, or similar services, especially when a skill might skip its authenticated main flow and fall back too early.
---

# External API Onboarding

## Overview

Use this skill to turn "I need this external API/MCP to work" into a safe setup loop: identify the provider, find the official setup path, guide browser or OAuth steps with the user in control, store credentials privately, and run a minimal smoke test.

This skill does not harvest, reveal, or bypass credentials. It keeps login, MFA, CAPTCHA, billing, and secret-copy actions human-approved.

For any setup that needs user authentication, the default UX must be assisted and visible: open the official provider console, token creation page, OAuth URL, or login page in a browser automatically when it is safe to do so. Do not leave the user with only a raw URL or a pasted command if the agent can open the official auth target directly. The user still completes login, MFA, CAPTCHA, billing consent, key reveal, and token copy.

For browser-session providers that need cookies or storage state, prefer a provider-specific visible-login helper over manual cookie paste: launch a fresh tool-controlled browser session, let the user complete login/CAPTCHA/MFA, then save only that session's required cookies/state to private user-level storage without printing values. The helper must work in non-interactive Codex terminals: do not require terminal `input()`, Enter presses, or pasted cookies; use browser-side confirmation, polling, OAuth callbacks, or provider status checks instead. Do not read existing Chrome/Edge/browser profiles unless the user explicitly asks and the target workflow requires it.

Audit fallback behavior before closing setup. If the target skill has a safe visible-login/OAuth/key helper but its instructions or scripts tend to stop at "credential missing", use anonymous mode, or report fallback results instead of driving the main authenticated flow, correct that skill or run the helper first. Fallback is a controlled exception, not the default path.

## Required Inputs

- Provider or target skill/MCP, inferred from context when possible.
- Desired access type: API key, OAuth MCP login, local stdio MCP, provider CLI login, or anonymous fallback.
- Storage target: private skill `.env`, project-local `.env`, user environment, or Codex `config.toml`. Default to private user-level storage, never a committed repo file.
- Smoke-test command or expected capability. Infer this for known providers; otherwise use official docs.

Ask one concise question only when the answer changes privacy, cost, provider scope, or where credentials are stored.

## Workflow

1. Classify the setup.
   - API key in `.env` or environment variable.
   - Streamable HTTP MCP with OAuth or bearer token.
   - Local stdio MCP that needs env vars.
   - Browser-assisted provider console setup.
   - Browser-session login that should save a fresh tool-controlled cookie/storage state.
   - Provider CLI login or no-auth fallback.
2. Load the relevant references.
   - Always follow `references/security-policy.md` before handling secrets or browser sessions.
   - Use `references/provider-patterns.md` for known providers.
   - For unknown or version-sensitive providers, search official docs or the provider console before acting.
3. Discover the official setup path.
   - Prefer provider docs, provider consoles, and official Codex/MCP docs.
   - Avoid third-party key brokers, copied tokens from tutorials, and unofficial mirrors.
   - If browser automation is useful, use it only to navigate and inspect non-secret UI. The user completes login, MFA, CAPTCHA, and secret reveal/copy steps.
4. Configure locally.
   - For API keys, prefer `scripts/set_env_secret.ps1` so the value is entered hidden and not printed.
   - For MCP servers, prefer `codex mcp add ...` or explicit `config.toml` edits.
   - For OAuth MCP, prefer `scripts/assist_oauth_login.ps1 -ServerName <server-name>` after the server is configured so the official authorization URL is opened automatically. If a provider-specific assisted login helper exists, use that helper.
   - For browser-session auth, prefer a visible helper that automatically saves the fresh session cookies/state after the user completes login; fall back to hidden local prompt only when no safe helper exists.
   - For PAT/API-key auth, open the official provider page automatically and guide the user to paste secrets only into a hidden local prompt or provider-controlled UI.
   - Do not read, print, paste into chat, commit, or summarize secret values.
5. Audit main-flow vs fallback behavior.
   - Inspect the target skill's `SKILL.md`, provider references, and relevant CLI flags for fallback-prone defaults.
   - If the skill would skip the main provider flow because a credential/cookie is missing while a safe helper exists, patch the skill or run the helper before using fallback.
   - Treat assisted-auth failure as a blocker for authenticated collection. Allow fallback only when the user explicitly asks for discovery-only/public cross-checking, or when the task itself is no-auth by design.
6. Smoke test.
   - Prefer dry-run, `whoami`, `list`, `doc`, or one cheap read-only request.
   - For paid APIs or write-capable providers, ask before making a real request.
   - Report only status: key present/missing, server configured, login required, request succeeded/failed, or blocker.
7. Close the loop.
   - Summarize provider, env var names, storage path, MCP server name, commands run, smoke-test result, and any restart needed.
   - Never include secret values, cookies, auth headers, or copied browser storage.

## Browser Assistance Rules

Allowed:

- Open the official provider docs or console.
- Automatically open official login, OAuth authorization, API-key creation, or token creation pages when user authentication is required.
- Launch a fresh visible automation browser, wait for the user to complete login/CAPTCHA/MFA, then save only the required session cookies/storage state into private user-level storage when the target workflow explicitly needs it.
- Help the user find account, developer, API key, OAuth app, or MCP setup pages.
- Click documented non-destructive controls after the user approves the goal.
- Read non-secret labels such as key name, scope names, redirect URL fields, and status messages.
- Wait while the user logs in, solves MFA/CAPTCHA, or copies a key into a local hidden prompt.

Not allowed:

- Bypass MFA, CAPTCHA, rate limits, paywalls, or account controls.
- Reveal, copy into chat, log, screenshot, or extract secret key values.
- Store cookies, browser storage, request headers, or session exports unless the target workflow explicitly requires it and the user performs the login in a visible, tool-controlled session.
- Read existing Chrome/Edge/browser profiles or copy browser storage from an unrelated profile unless the user explicitly asks and accepts the privacy risk.
- Create broad admin/billing/write scopes when a narrower read scope is enough.
- Delete, rotate, or regenerate credentials without explicit confirmation.

## Secret Writer

Use the bundled PowerShell helper for API-key style credentials:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\external-api-onboarding\scripts\set_env_secret.ps1 `
  -EnvFile "$env:USERPROFILE\.codex\skills\anysearch\.env" `
  -Name ANYSEARCH_API_KEY
```

Dry-run example for validation only:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\external-api-onboarding\scripts\set_env_secret.ps1 `
  -EnvFile .\tmp\example.env `
  -Name EXAMPLE_API_KEY `
  -Value DUMMY_VALUE `
  -AllowPlainValue `
  -DryRun
```

Avoid `-Value` for real secrets because command lines can be persisted in shell history or process listings.

## Assisted OAuth Login

Use the bundled helper for OAuth-style remote MCP authentication:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\external-api-onboarding\scripts\assist_oauth_login.ps1 `
  -ServerName huggingface
```

The helper runs `codex mcp login <server>`, watches for the official authorization URL, opens it in the default browser, and suppresses auth-looking output. The user completes login and consent in the browser. Use `-DryRun` to validate command shape without opening a browser.

## References

- `references/security-policy.md`: required guardrails for secrets, OAuth, browser sessions, storage, and reporting.
- `references/provider-patterns.md`: known provider routes, env var names, MCP command shapes, and smoke-test ideas.
- `scripts/assist_oauth_login.ps1`: generic visible OAuth helper for Codex remote MCP servers.
- Provider-specific visible-login helpers: preferred for cookie/storage-state providers; they should open a fresh browser, let the user authenticate, and save only status plus private state paths without printing secret values.
- Fallback audit: required for skills with optional anonymous/public modes; verify the helper-backed main flow is attempted before fallback.

## Done Criteria

- Credentials were stored only in the approved private target.
- User-auth steps were assisted with an automatic browser/provider-page open, or a blocker explains why automatic opening was not possible.
- Browser-session helpers were checked against non-interactive Codex execution and do not require terminal stdin to finish.
- Target skill defaults were checked for fallback drift; any "missing credential -> fallback" behavior was corrected or explicitly documented as user-approved.
- No secret value appears in chat, committed files, command output, or final summary.
- MCP or env configuration is documented by server name, env var name, and path only.
- A smoke test ran, or the blocker and next human action are clear.
