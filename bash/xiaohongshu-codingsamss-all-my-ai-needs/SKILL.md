---
name: xiaohongshu
description: "Read Xiaohongshu (小红书) through OpenCLI using the user's Chrome logged-in session. Actions: search notes, read note details, read comments, browse feed, read user notes. Keywords: xiaohongshu, xhs, 小红书, 红书, 笔记, 评论, feed."
---

# Xiaohongshu Skill (Read-Only)

Use OpenCLI as the single supported Xiaohongshu implementation. The previous HTTP/API and Chrome Cookie DB extraction path was removed because Xiaohongshu frequently requires browser-side login verification and risk-control handling.

## When To Use

Triggered by:
- "小红书搜 [query]", "search xiaohongshu [query]"
- "读小红书笔记", "read xhs note [url]"
- "小红书评论", "xhs comments"
- "小红书 feed", "小红书首页"
- "小红书用户主页", "xhs user"

## Prerequisites

1. Node.js and npm are installed.
2. OpenCLI is installed: `npm install -g @jackwener/opencli`
3. The OpenCLI Chrome extension is installed manually from the Chrome Web Store.
4. Chrome is open and logged into Xiaohongshu.

Check status without starting or changing the daemon:

```bash
opencli daemon status
```

Do not run `opencli doctor` for routine checks; it can start the daemon.

## Commands

Search notes:

```bash
opencli xiaohongshu search "<query>" -f yaml
```

Read a note:

```bash
opencli xiaohongshu note "<note_url>" -f yaml
```

Read comments:

```bash
opencli xiaohongshu comments "<note_id>" -f yaml
```

Browse feed:

```bash
opencli xiaohongshu feed -f yaml
```

Read a user's public notes:

```bash
opencli xiaohongshu user "<user_id>" -f yaml
```

Download media from a note:

```bash
opencli xiaohongshu download "<full_note_url_with_xsec_token>" --output "./xiaohongshu-downloads" -f yaml
```

## Recommended Workflows

### Preflight

1. Check that the daemon and Chrome extension are available:

```bash
opencli daemon status
```

2. Check Xiaohongshu login state before reading search results, profiles, or notes:

```bash
opencli xiaohongshu whoami -f yaml --window background --site-session persistent --trace retain-on-failure
```

If `whoami` succeeds but another command returns `AUTH_REQUIRED`, treat the target page as blocked by a login wall and ask the user to refresh Xiaohongshu login in Chrome. Do not switch to cookie extraction or unofficial APIs.

If OpenCLI returns `BROWSER_CONNECT` or cannot bind `127.0.0.1:19825`, the daemon may be blocked by the current sandbox. Start or check the daemon from an unrestricted host shell when available, then rerun the same OpenCLI command. Do not use `opencli doctor` for routine checks.

### Profile Share Links

Do not pass a profile `xhslink.com/m/...` URL directly to `opencli xiaohongshu user` and assume the short-link tail is the user id. In practice, OpenCLI may incorrectly navigate to:

```text
https://www.xiaohongshu.com/user/profile/<short-link-tail>
```

If the trace shows a `404` for that URL, the `EMPTY_RESULT` error is probably a bad profile id, not proof that the user has no public notes.

For profile share links, first resolve the canonical profile URL:

- Prefer a real URL like `https://www.xiaohongshu.com/user/profile/<user_id>?xsec_token=...`.
- If only a short link is available, ask the user to open it while logged in, then read the final URL from the current Chrome tab or recent Chrome history.
- Use Chrome only for URL resolution or visible-page confirmation. Keep Xiaohongshu data extraction in OpenCLI.

After resolving the canonical profile URL, probe the profile:

```bash
opencli xiaohongshu user "<canonical_profile_url>" --limit 5 -f yaml --window background --site-session persistent --trace retain-on-failure
```

If `search "<creator_name>"` returns `[]`, do not conclude the creator is missing. Try the canonical profile URL or the user's browser history/open tab instead.

### Batch Profile Media Download

For bulk image download from a profile, use a staged flow:

1. Probe the profile with `--limit 5`.
2. Download 1-3 notes first to verify media extraction and local file layout.
3. Save a manifest before full download:

```bash
opencli xiaohongshu user "<canonical_profile_url>" --limit 250 -f json --window background --site-session persistent --trace retain-on-failure > notes-manifest.json
```

4. Download from manifest URLs, not note ids alone. The manifest URLs usually include the required `xsec_token`.
5. Write a status log per note, continue past single-note failures, and add a short delay between notes to reduce risk-control friction.
6. Preserve the raw download directory. If the user wants clean names, copy into a separate `named/` directory instead of destructively renaming raw files.

Suggested clean naming:

```text
named/
  001_<article-title>/
    <article-title>_1.jpg
    <article-title>_2.jpg
```

When generating filenames, sanitize filesystem-illegal characters such as `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, and control characters. Keep a rename manifest that maps source files to named files.

### Interpreting Download Results

- `No media found` on a profile share link usually means the input is a profile, not a note. Resolve the profile, list note URLs, then download each note URL.
- `EMPTY_RESULT` from `user` with a profile short link usually means the short-link tail was treated as a bad user id. Inspect the trace before reporting "no public notes".
- A successful `download` command writes files locally and is still read-only with respect to Xiaohongshu. It must not post, like, follow, comment, delete, or publish anything.

## Notes

- Use full note URLs from search or feed results when possible; Xiaohongshu often requires `xsec_token`.
- If OpenCLI returns `AUTH_REQUIRED`, ask the user to refresh Xiaohongshu login in Chrome.
- Do not use HTTP/API scraping, Chrome Cookie DB extraction, `xiaohongshu-mcp`, or `xhs-cli` as hidden fallbacks.
- Do not post, comment, like, favorite, follow, or bypass captcha/risk controls.
- Never run write commands such as `publish`, `delete-note`, `follow`, or `unfollow` unless the user explicitly asks for that exact action and the normal browser safety confirmation rules are satisfied.
- For batch tasks, report the canonical profile URL or user id used, manifest count, success/failure count, output directories, and whether any temporary daemon/browser session was left running.
