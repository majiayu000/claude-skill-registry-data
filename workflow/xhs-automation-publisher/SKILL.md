---
name: xhs-automation-publisher
description: Run authorized Xiaohongshu browser workflows for login checks, creator preview fill, publish blockers, final posting, search, export, or approved engagement. Prefer native signed-in Chrome; keep Python/CDP for deterministic batch fallback.
---

# XHS Automation Publisher

This skill vendors `white0dew/XiaohongshuSkills` as a deterministic Xiaohongshu batch/export fallback. Interactive logged-in work should first load `$browser-automation-router` and use the Codex Chrome extension when available. The vendored Python + Chrome DevTools Protocol (CDP) commands remain useful for repeatable preview filling, creator data export, and explicit batch contracts.

## Use With The Local Role System

- Use `$xhs-publish-assistant` first when the user only needs copy-ready title/body/tags/image directory output.
- Use `$xhs-automation-publisher` when the user explicitly needs browser automation, login diagnosis, creator-center filling, auto-publish blocker debugging, content-data export, search/detail collection, or authorized final posting.
- Keep `内容主编` as coordinator for content strategy and publish authorization. `小红书` executes this skill only after scope and account boundary are clear.

## Hard Gates

- Default to preview/fill, not final posting. Prefer the native Chrome surface for an interactive reviewable fill; use `publish_pipeline.py --preview` or `cdp_publish.py fill` when a deterministic script fallback is required.
- `publish_pipeline.py` defaults to clicking publish when `--preview` is absent. Treat that as high risk.
- Do not run `click-publish`, `publish`, `post-comment-to-feed`, `respond-comment`, `note-upvote`, `note-unvote`, `note-bookmark`, `note-unbookmark`, `remove-account`, `re-login`, or `switch-account` without a fresh explicit user approval for that exact action.
- Do not store cookies, account tokens, login QR payloads, real account names, or Chrome profile paths in this repo.
- Do not use this skill for scraping or interaction at scale. Respect platform rules, rate limits, and account risk.
- Stop before final publish if the target account, media list, title, body, tags, or publish time is uncertain.

## Surface Selection

1. Use the Codex Chrome extension for an existing signed-in profile, visible creator-center review, one-off form filling, and user-observed troubleshooting.
2. Use the in-app Browser only when its separate login state is acceptable; it does not inherit the user's Chrome profile.
3. Use the vendored Python/CDP commands for batch export, a stable command contract, unattended repeatability, or an explicit fallback when native plugins are unavailable.
4. Do not launch or copy a local Chrome profile merely to bypass a missing native plugin. Do not commit profile paths or login state.

## Safe Default Flow

1. Confirm target account, desired mode, media files, and whether final posting is authorized.
2. For interactive work, verify the native Chrome surface and active account. For a script fallback, check/login only when requested:

```powershell
python scripts/cdp_publish.py check-login
python scripts/cdp_publish.py login
```

3. Fill creator-center form for human review:

```powershell
python scripts/publish_pipeline.py --preview --title-file title.txt --content-file content.txt --images image1.png
```

4. Only after explicit approval, run a publish command without `--preview` or run `click-publish`.
5. Return exact commands, status markers, account boundary, and any manual actions left.

## Useful Commands

```powershell
python scripts/chrome_launcher.py
python scripts/chrome_launcher.py --restart
python scripts/cdp_publish.py list-accounts
python scripts/cdp_publish.py search-feeds --keyword "选题关键词"
python scripts/cdp_publish.py content-data --csv-file "content_data.csv"
```

The scripts require Python 3.10+, Google Chrome, and dependencies from `requirements.txt`.

## Failure Handling

- Not logged in: switch to headed login and ask the user to scan QR code.
- Selector/page failure: inspect `scripts/cdp_publish.py` `SELECTORS`, upload waits, editor fill, and publish-button logic.
- Media path failure: use absolute paths; for WSL/remote CDP path mismatch, consider `--skip-file-check`.
- Comment/engagement uncertainty: do not guess target IDs or tokens; ask for the exact note/comment target.
