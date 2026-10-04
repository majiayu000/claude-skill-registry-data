---
name: autocli_anthropic
description: >-
  Use when the user wants data fetched from a website, a site turned into a
  CLI, existing browser login state reused through Chrome, or a supported local
  CLI/desktop app accessed through AutoCLI. Prefer this before heavier browser
  automation when AutoCLI likely covers the target. Read this skill before using
  `autocli`.
targets: [hermes-default, hermes-gpt, claude-hermes]
---
# AutoCLI

Use this when a site or supported app already has an AutoCLI adapter, or when the user wants “turn this website into a command” behavior without a whole browser-driving session.

## What it does

AutoCLI is a fast Rust CLI that turns websites and some local tools/apps into command-line interfaces. It can:
- fetch structured data from supported sites
- reuse Chrome login state through its extension for browser-backed commands
- search for existing community adapters
- generate adapters for new sites via `autocli.ai`
- wrap a few local CLIs like `gh`, `docker`, `kubectl`, and Google Workspace helpers

Think of it as: “try a purpose-built website/app CLI first, then fall back to browser automation if needed.”

## URL-to-markdown extraction with curl.md

For one-off webpage-to-markdown extraction, use Hermes `curlmd_fetch` first when the goal is clean markdown context and no site-specific tool exists. It wraps `curl.md` with bounded timeouts, retry/backoff, authenticated token use from `CURLMD_API_KEY`/1Password when available, and a plain `curl` fallback for stalls, rate limits, weak/blocked pages, or CLI failures.

Current docs/observed behavior:
- Basic use inside Hermes: call `curlmd_fetch(url="https://example.com")`; terminal fallback is `npx -y curl.md@0.1.1 <url>`.
- Authenticated Mac Studio token is stored in 1Password item `CLI / curl.md API Token - Hermes Mac Studio`; expose it as `CURLMD_API_KEY` or pass `--token` for non-interactive terminal calls.
- Query-string targets need encoding as a path segment, e.g. PubMed search: `https://curl.md/pubmed.ncbi.nlm.nih.gov/%3Fterm=PLGA+drug+delivery`; otherwise the target query can be treated as curl.md API params and fetch the home page.
- Anonymous limits: standard fetches `100/hour`; `objective=` narrowing only `3/hour`. Authenticated limits: `1,000/hour` and `10/hour`. Paid usage skips these limits.
- Good fits from benchmark: docs, public forum pages like LPSG threads, normal GitHub repos, Apple docs, and PubMed encoded-query pages.
- Poor fits from benchmark: X profiles return empty shells (use `xurl` first), Reddit can return verification shells, YouTube can 429, and GitHub repo names containing dots such as `wevm/curl.md` can fail with upstream 404.
- Treat `x-tokens-count`, `x-tokens-saved`, `x-cache`, and rate-limit headers as useful benchmark telemetry, but judge extraction quality by content hits and blocked/error markers, not HTTP 200 alone.

See `references/curlmd-heavy-site-benchmark-2026-05-13.md` for the benchmark matrix, rate-limit receipts, query-string gotcha, and routing notes.

## Environment notes

- Expect the `autocli` binary to be available on `PATH`.
- Keep auth tokens in the machine's normal secure secret store or local AutoCLI auth flow.
- If a team already has a standard token-retrieval workflow, use that instead of inventing a new one.

Do not paste tokens into files, skills, or committed config.

## First checks

1. Confirm the binary exists:
   - `autocli --version`
2. If AI generation/search features need auth, run:
   - `autocli auth`
3. If browser-backed commands matter, make sure Chrome is open and the AutoCLI extension is installed.

## Default workflow

1. Check whether the target already has a command:
   - `autocli --help`
   - or `autocli search <url>`
2. If a matching adapter exists, use it directly.
3. If not, and the user wants extraction from a new site, try:
   - `autocli generate <url> --goal '<plain-English goal>' --ai`
4. If the task needs full arbitrary page interaction, rich login flows, or UI testing, switch to browser automation instead of forcing AutoCLI.

## Good fits

- “Get structured data from this website.”
- “Can you pull this page into JSON/CSV/markdown?”
- “Is there already an adapter for this site?”
- “Turn this site into a reusable CLI command.”
- “Use the site I’m already logged into in Chrome.”

## Poor fits

- Multi-step UI testing
- Complex forms or flows with lots of clicks
- Sites with no useful adapter path where browser automation is clearly simpler
- Tasks where raw browser screenshots/DOM interaction matter more than structured output

## Quick commands

```bash
autocli --version
autocli search https://example.com
autocli generate https://example.com --goal 'list the latest posts' --ai
autocli hackernews top --format json
autocli gh repo view cli/cli --format json
```

## Notes

- Public commands can work without browser auth.
- AI generation/auth features use `autocli.ai` and store local config in `~/.autocli/config.json`.
- If auth is needed again, prefer the machine's existing secure secret workflow instead of asking the user to retype a token that is already managed locally.
