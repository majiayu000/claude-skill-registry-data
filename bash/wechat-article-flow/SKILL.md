---
name: wechat-article-flow
description: Guide a WeChat article workflow through article selection, style selection, local preview, and explicitly confirmed draft upload using the installer's own local adapter. Use when a user wants to preview a Markdown article for WeChat, choose an article style in chat, configure a WeChat draft adapter, or upload an already approved article to their own WeChat official-account draft box.
---

# WeChat Article Flow

Run an account owner's local article adapter in small, confirmed conversation steps. This skill is intentionally adapter-neutral: it does not bundle credentials, an uploader, a specific API client, a browser profile, or a publishing account.

## Configuration gate

Before previewing or uploading, read `references/account-profile.template.md`. The user must explicitly provide the path to their private account profile and confirm that they trust its adapter executable; do not search for or execute a profile merely because it exists in the current workspace.

- If no trusted adapter executable is configured, explain the required profile fields and stop. Do not invent a command or ask the user to paste credentials into chat.
- Keep AppID, Secret, Cookie, token, and access-token output in protected local environment configuration, never in the profile, prompt, skill folder, terminal output, or Git.
- A compatible adapter must expose three noninteractive operations: `list`, `preview`, and `upload-draft`. It may be a shell script, Python CLI, or another local tool.
- Treat the profile as executable configuration. Before the first operation, show the resolved executable and exact argument list, obtain one explicit trust confirmation, invoke it with an argv array, and never use shell strings, `sh -c`, `eval`, interpolation, or command substitution. Pass article, style, and cover values as separate arguments.

## State machine

### 1. Choose an article

Run `<trusted-adapter> list` or accept an explicit Markdown path. Show the returned choices and require the user to select one. Do not infer the newest file as approval.

### 2. Choose presentation

Ask for a registered style/theme after the article is selected. Use the user's default only when they explicitly accept it. A cover override requires a separately supplied local path or approved URL.

### 3. Generate a local preview

Run `<trusted-adapter> preview --article <path> --style <style> [--cover <path>]` with argv-safe values. It must not open a browser, upload assets, create a remote draft, or publish.

Report the local preview path and ask whether the user wants to open it, revise the article, or upload this exact approved selection. Opening a browser is a separate decision.

### 4. Upload only after an explicit confirmation

Before upload, verify that the adapter's credential configuration exists without printing its contents. State the selected article, cover, and style, then require an explicit upload confirmation.

Run only `<trusted-adapter> upload-draft --article <path> --style <style> [--cover <path>]`. Report a redacted result: draft identifier or success/failure category is acceptable; tokens, secrets, cookies, request headers, and full secret paths are not.

Uploading a draft is not publishing. Stop after the draft unless the user separately asks for another externally authorized step.

## Guardrails

- Preserve article text, cover metadata, image rights decisions, and adapter configuration; this flow does not rewrite content.
- Treat preview, browser opening, draft upload, scheduling, and final publication as separate decisions.
- Never bypass a low-resolution-cover warning or an adapter safety check without an explicit user acceptance of that specific risk.
- On partial, timeout, or unknown upload results, do not retry automatically. Inspect the adapter's own idempotency/status mechanism first.
- Use a local Python runtime with required image packages only when the user's adapter declares it; do not assume Codex Desktop tooling exists.
