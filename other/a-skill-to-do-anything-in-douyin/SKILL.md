---
name: do-anything-in-douyin
description: "Browser-based Douyin automation for any web-supported operation: persistent-login browser control, reusable CDP sessions, search and browsing, video/detail collection, comments, likes, favorites, notification/message interaction, batch operation plans, content drafting, cover/card generation, and Creator Center publishing. Use when Codex should operate Douyin through the web version with the user's default browser where possible, first-run login, later saved-session reuse, and scripted workflows instead of screenshot/computer-use control."
---

# DoAnythingInDouyin

Use the web automation backend first. The durable entry point is `scripts/douyin_web.mjs`, backed by SDK modules under `scripts/sdk/` for account/profile management, diagnostics, interaction actions, plan execution, run artifacts, and feed exploration. It launches a headed persistent browser profile, asks for login on first run, and reuses that profile for later commands.

Default to `run-plan` for real tasks. It keeps one browser tab/context open for the whole workflow, records per-step results, and avoids repeated browser open/close cycles.

## Browser Model

- Use `scripts/douyin_web.mjs --browser default` by default.
- `default` detects the macOS default browser and maps it to the closest Playwright backend.
- The script uses its own persistent profile under `state/web/profiles/`. It does not mutate the user's real browser profile.
- Use `accounts list|add|default|remove` and `--account NAME` for isolated multi-account profiles.
- Chromium-like browsers use reusable CDP sessions on Douyin-specific ports `9420-9426`, separate from other skills.
- A reusable CDP browser is bound to one account/profile at a time; close it before switching accounts on the same browser backend.
- CDP ports are accepted only after endpoint and private-profile ownership checks; an unrelated process on a reserved port is not silently attached.
- Browser-controlling commands use a local lock so even read-only navigation jobs do not fight over the same reusable CDP browser.
- First run: execute `scripts/douyin_web.mjs login --browser default`, let the user log in in the opened browser, then finish the command.
- Later runs: use the same `--browser` value and the saved profile should remain logged in unless Douyin expires the session.
- `browser-status` reports endpoint reachability plus `managed` or `unmanaged-or-recoverable` session state. `status` reports `loginState`, session-cookie evidence, web/creator cookie counts, and any detected web block. Douyin's normal site and Creator Center can expire independently, so check status before publishing or other direct actions.

## Operating Rules

- Prefer `scripts/douyin_web.mjs run-plan` for multi-step Douyin actions.
- Use a `diagnose` plan step when a web control is missing or a previous action behaved unexpectedly. It reports URL, visible controls, custom elements, internal scroll containers, and login/permission/rate-limit blocks.
- Use single commands only for diagnostics, quick login checks, or isolated operations.
- Treat `scripts/douyin_web.mjs` as the thin CLI and `scripts/sdk/` as the canonical SDK layer. Load `references/sdk-architecture.md` before adding or repairing backend functionality.
- Use `scripts/douyin_package.py` to create and inspect post packages.
- Use `scripts/douyin_image.py` to generate deterministic vertical cover/card images.
- Load `references/ui-workflows.md` before operating Douyin.
- Load `references/operation-plans.md` before building a multi-step browser plan, batch job, interaction task, or any operation not covered by a single command.
- Load `references/content-publishing.md` before drafting content, generating images, uploading media, or publishing posts.
- Do not add extra confirmation prompts when the user has already authorized direct execution.
- Treat Douyin web prompts, permissions, login, captcha, moderation, and rate limits as the authority. If the site blocks the operation, stop the current command and report the state.
- Treat a successful click, field fill, or Enter keypress as an attempt, not a completed social action. Report `confirmed`, `unconfirmed`, or `blocked` evidence; do not describe an `unconfirmed` interaction as completed.
- Treat browser permission pages such as `edge://permission-request-dialog/` or `chrome://permission-request-dialog/` as web blocks. Do not continue clicking Douyin controls until the prompt is resolved.
- Keep progress records for batch work in a local file when the task has more than one target.

## Script Quick Start

```bash
scripts/douyin_web.mjs detect-browser
scripts/douyin_web.mjs accounts list
scripts/douyin_web.mjs accounts add work --alias "Work account"
scripts/douyin_web.mjs login --browser default
scripts/douyin_web.mjs browser-status --browser default
scripts/douyin_web.mjs status --browser default
scripts/douyin_web.mjs search "上海周末爵士酒吧" --browser default --limit 20 --out /tmp/douyin-results.json
scripts/douyin_web.mjs open-url "https://www.douyin.com/" --browser default
scripts/douyin_web.mjs click-text "发布" --browser default
scripts/douyin_web.mjs fill "textarea" "hello" --browser default
scripts/douyin_web.mjs run-plan /tmp/douyin-plan.json --browser default --direct --out /tmp/douyin-plan-result.json --artifact-dir /tmp/douyin-artifacts
scripts/douyin_web.mjs message "好友名" "测试信息" --browser default --direct
scripts/douyin_image.py --title "Codex Skill 测试声明" --subtitle "自动化发布流程测试" --tag Codex测试 --out /tmp/douyin-post/cover.png
scripts/douyin_package.py create --topic "Codex Skill 测试声明" --out /tmp/douyin-post --title "Codex Skill 测试声明" --body "This is a Douyin automation test." --hashtag Codex测试 --image /tmp/douyin-post/cover.png --mode image
scripts/douyin_web.mjs publish /tmp/douyin-post/post.json --browser default --direct
scripts/douyin_web.mjs close-browser --browser default
```

## Workflow

1. Run `detect-browser` if the browser backend is unclear.
2. Run `login` once for the selected browser backend.
3. Run `status` before important work if login state may have expired.
4. For real work, create a JSON plan and execute it with `run-plan` so search, browsing, collecting, commenting, liking, notification/message interaction, and publishing happen in one session.
5. For batch operations, use one plan or one long-lived command. Prefer built-in run artifacts over ad hoc logs; every run-plan writes manifest, step records, failure snapshots, and a final result.
6. Finish with completed, unconfirmed, skipped, failed, and blocked counts plus relevant file paths. Launch-level failures also write a final result artifact before the command exits.

## Result Style

- For single actions: report action, target, browser backend, and final observed status.
- For publishing: report post package path, media paths, browser backend, selected upload mode, and `published`, `blocked`, or `unconfirmed` verification status. A direct publish exits nonzero unless Creator Center confirms publication.
- For batch operations: summarize confirmed, unconfirmed, skipped, failed, and blocked counts first, then point to the local progress log.
- For SDK maintenance: report changed modules, compatibility impact, and validation commands.
