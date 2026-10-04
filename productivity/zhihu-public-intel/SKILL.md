---
name: zhihu-public-intel
description: Route Zhihu research through safe zhihu-mcp authentication, public fallback discovery, normalization, and synthesis. Use when Codex needs Zhihu-related search or capture for public topics, people, questions, answers, articles, comments, user profiles, or JSONL/CSV/Markdown reports. For keyword/topic/person search, automatically run the local zhihu-mcp auth loop first; use AnySearch only if login is declined, two assisted login attempts fail, the MCP runtime remains unavailable, or public-index cross-checking is requested.
---

# Zhihu Public Intel

## Overview

Use this skill for Zhihu research and evidence collection. The default keyword/topic/person workflow is `check zhihu-mcp runtime -> verify MCP login status -> run visible-browser login helper if needed -> verify again -> use zhihu-mcp tools -> normalize outputs`. Do not silently fall back to generic web search or AnySearch before running the zhihu-mcp authentication path unless the user explicitly declines login.

Zhihu often presents login walls for search, article details, comments, and user activity. When that happens, do not stop at "blocked":

1. Record the blocker precisely (`signin`, 401/403, CAPTCHA, empty tool result, or hidden comments).
2. Guide the user through the local authenticated flow in `references/zhihu-mcp-setup.md` and `scripts/assist_zhihu_login.ps1`.
3. Use AnySearch only if the user declines login, two assisted login attempts fail, the MCP runtime remains unavailable, or a public-index cross-check is useful.
4. Never ask the user to paste cookies or request headers in chat.

## Mandatory Auth Loop

For keyword/topic/person search, exact-name lookup, comments, user activity, or any task that needs Zhihu search:

1. Run `check-runtime`.
2. Check login with MCP `check_login_status` or `cookie_status` before search.
3. If `logged_in=false`, `login_verified=false`, cookies are missing/stale, or a plausible exact-name search returns an auth-looking empty result, immediately run the visible login helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\zhihu-public-intel\scripts\assist_zhihu_login.ps1
```

4. Tell the user to complete login/MFA/CAPTCHA in the opened browser, then verify again with `check_login_status` or `cookie_status`.
5. Only after verified login, run `search_content`/detail/comment/profile MCP tools.

Do not merely say "login expired" and switch to AnySearch. Existing `cookies.json` is not proof of login; if MCP verification fails, treat it as stale and refresh it through the helper. The helper may replace an existing `cookies.json` only after successful visible login, and it never prints cookie values.

AnySearch is allowed only when:

- the user explicitly declines login or asks for public-index cross-checking;
- the visible helper cannot run in the current environment;
- two assisted login attempts fail or the MCP runtime remains unavailable.

When AnySearch is used, label output as discovery/snippet evidence, not full Zhihu capture.

## Decision Tree

1. Identify the target:
   - keyword/topic search;
   - question URL or question ID;
   - answer URL or answer ID;
   - zhuanlan article URL or article ID;
   - comments for an answer/article;
   - user public profile or public recent activity;
   - bulk public crawl.
2. Plan the backend before crawling. For keyword/topic/person targets, the plan must recommend `zhihu-mcp-auth`:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py plan `
  --target "大模型 Agent" `
  --needs search,question,answers,comments,report `
  --scale medium
```

3. Execute only the needed lane:
   - `zhihu-mcp-auth`: default lane. Check runtime, guide visible-browser login if needed, verify login, then use MCP tools.
   - `public-browser-lite`: detail lane for already discovered public question/answer/article/profile URLs.
   - `AnySearch discovery`: fallback when user declines login, two assisted login attempts fail, MCP remains unavailable, or public-index cross-checking is requested. Use snippets only as discovery evidence.
   - `zhihu-k-search`: optional convenience CLI when already installed.
   - `zhihu-mcp`: authenticated MCP workflow for search, discovered URLs/IDs, full details, comments, or user activity after `check-runtime` and login-status checks.
   - `MediaCrawler`: optional larger public bulk crawl.
   - `ZhihuApis`: optional logged-in comment-completeness lane; cookies stay local.
4. Normalize results before synthesis:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py normalize `
  --input output\zhihu\raw_search.json `
  --source public-browser-lite `
  --output-dir output\zhihu\normalized
```

5. Produce reports from normalized artifacts, not from untracked browser state.

## Backend Routing

Read `references/source-routing.md` before selecting a backend.

Hard rule for keyword/topic/person tasks:

- Do not run generic web search, direct Zhihu URL probing, or AnySearch before the mandatory auth loop above.
- Run `check-runtime`; if login is missing/stale or MCP says `logged_in=false`/`login_verified=false`, run `assist_zhihu_login.ps1` immediately so the user can log in in a visible browser.
- Existing `cookies.json` can be stale; refresh it through the helper instead of treating the file as success.
- Verify with `check_login_status` or `cookie_status`, then use `zhihu_mcp.search_content`.
- Use AnySearch only after the user declines login, two assisted login attempts fail, MCP remains unavailable, or a public-index cross-check is explicitly requested.

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py check-runtime
powershell -ExecutionPolicy Bypass -File .\skills\zhihu-public-intel\scripts\assist_zhihu_login.ps1
```

- Use `public-browser-lite` for already discovered public pages and lightweight reports. Save public raw HTML/JSON-like captures under `raw/`, then normalize.
- Use `zhihu-k-search` only as an optional convenience CLI when it is already installed or the user approves setup.
- Use `zhihu-mcp` as the default after login verification. For repeatable setup, read `references/zhihu-mcp-setup.md` and prefer `scripts/setup_zhihu_mcp.ps1`.
- Use AnySearch fallback only after auth is declined/blocked:

```powershell
python C:\Users\Administrator\.codex\skills\anysearch\scripts\anysearch_cli.py batch_search `
  --query "site:zhihu.com 王皓波" `
  --query "site:zhuanlan.zhihu.com 王皓波" `
  --query '"王皓波" 知乎'
```

- Use `MediaCrawler` only when scale matters and the user accepts external crawler setup.
- Use `ZhihuApis` only when comment completeness is the key requirement and the user approves authorized local cookies.

## Common Commands

Print backend plan:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py plan `
  --target "https://www.zhihu.com/question/19550225" `
  --needs question,answers,comments,report
```

Plan a keyword/person authenticated run:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py plan `
  --target "王皓波" `
  --needs search,articles,comments,report
```

Extract IDs and classify a URL:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py inspect-url `
  "https://www.zhihu.com/question/19550225/answer/1992353258262504861"
```

Print the normalized artifact contract:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py schema
```

Generate a run scaffold:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py scaffold `
  --output-dir output\zhihu\agent_discussion `
  --target "大模型 Agent" `
  --needs search,answers,comments,report
```

Check private `zhihu-mcp` runtime without reading cookie values:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py check-runtime
```

Print the safe login-wall recovery guide:

```powershell
python skills\zhihu-public-intel\scripts\zhihu_public_intel.py auth-guide `
  --target "王皓波" `
  --needs search,articles,comments
```

Install/update the optional MCP runtime, then open a visible browser for user-controlled login:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\zhihu-public-intel\scripts\setup_zhihu_mcp.ps1
powershell -ExecutionPolicy Bypass -File .\skills\zhihu-public-intel\scripts\assist_zhihu_login.ps1
```

The login helper stores Playwright-format Zhihu cookies only under the private user-level runtime:
`%USERPROFILE%\.codex\skills\zhihu-public-intel\runtime\zhihu-mcp\cookies.json`.
It does not print cookie values.

## Output Contract

Keep raw captures and normalized data separate:

- `raw/`: untouched backend outputs, screenshots, or API captures.
- `items.jsonl`: normalized question, answer, article, search result, and user rows.
- `comments.jsonl`: normalized comments and nested replies.
- `sources.csv`: review table with URL, title, type, author, counts, and backend provenance.
- `manifest.json`: backend plan, commands run, timestamps, limits, and blockers.
- `summary.md`: human-facing synthesis with links back to normalized source IDs.

Read `references/output-schema.md` before merging multiple backend outputs.

## Guardrails

- Do not focus on personal favorites, private collections, or browsing history unless the user explicitly asks.
- Do not run generic web search or AnySearch before offering zhihu-mcp auth for keyword/topic/person tasks.
- Default work must remain useful without MCP, paid scraping, external API keys, or committed login state.
- Keep `cookies.json`, `auth.json`, browser storage state, `.env`, request headers, and token-like values out of git and final answers.
- Use logged-in browser state only when the user has authorized access and the target content is available to that account.
- Do not bypass CAPTCHAs automatically or describe blocks as missing data.
- If login is needed, make the user perform login/MFA/CAPTCHA in a visible browser; Codex may run the helper but must not extract or print secrets.
- Rate-limit crawls and prefer small smoke tests before bulk collection.
- Do not republish copyrighted Zhihu content in bulk. Summarize and cite URLs; keep full captures local.
- Respect robots, platform terms, author rights, and legal constraints.

## Resources

- `scripts/zhihu_public_intel.py`: planner, URL inspector, scaffold generator, schema printer, and JSON normalizer.
- `scripts/setup_zhihu_mcp.ps1`: optional repeatable setup for the `zhihu_mcp` Codex MCP server in a private global skill runtime.
- `scripts/assist_zhihu_login.ps1`: optional visible-browser login helper that writes local Playwright-format Zhihu cookies without printing them.
- `references/source-routing.md`: backend selection and setup notes.
- `references/zhihu-mcp-setup.md`: details for the optional MCP backend, cookie boundaries, and smoke tests.
- `references/output-schema.md`: normalized JSONL fields and merge policy.
