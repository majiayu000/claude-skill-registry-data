---
name: dingtalk-minutes-access-request
description: Use when the user wants to request access to restricted DingTalk AI 听记/minutes pages, recheck permission-pending AI 听记 links, or diagnose why a shanji.dingtalk.com transcript cannot be opened. Do not use this skill to read transcripts or summaries; use dws minutes for reading.
---

# DingTalk Minutes Access Request

Use this skill only for DingTalk AI 听记 permission work:

- request access for restricted `shanji.dingtalk.com` 听记 pages
- recheck links that were previously permission-blocked
- diagnose whether a page is blocked by login, permission, stale storage state, or page layout

Do not use this skill to extract, summarize, or save meeting transcript content. Reading 听记 detail, transcript, AI summary, speakers, todos, keywords, or mind graph must go through `dws minutes`.

## Boundary

- `dws minutes`: read/list/get/transcript/summary/todo/speaker/keyword/mind-graph operations.
- `dingtalk-minutes-access-request`: browser-based permission request and blocked-page diagnosis only.

If permission is granted after a recheck, stop and switch to `dws minutes` for the actual read.

## Missing Summary vs Empty Transcript

When a user reports that a minutes item may not have generated an AI summary, verify the two DWS surfaces separately before clicking the page:

```bash
dws minutes get summary --id <row_key> --format json
dws minutes get transcription --id <row_key> --format json
```

- If `get summary` returns non-empty `fullSummary` but `get transcription` returns no paragraphs, this is not a missing-summary case. Do not click `重新生成纪要`; that regenerates the AI summary and does not create transcript paragraphs. Treat the item as `zero_transcript`, do not save a transcript, and report the DWS transcript metadata.
- If the summary is empty and the page is accessible, open `https://shanji.dingtalk.com/app/transcribes/<row_key>`, switch to `AI纪要` / `AI Summary`, click the visible `重新生成纪要` / `Regenerate summary` or equivalent generate-summary primary action, wait for generation to finish, then re-read with `dws minutes get summary`.
- If transcript paragraphs are missing, look for a visible `转文字` / `Transcribe text` control on the page. Only click it when the page clearly shows no transcript and offers transcription generation. After clicking, wait and recheck with `dws minutes get transcription`; save only after paragraphs are non-zero and pagination completes.

Static bundle evidence from the Shanji minutes app includes `fullTextSummary.regenerateSummary` (`重新生成纪要`) and `detail.convertText` (`转文字`), so keep summary regeneration and transcript generation as separate page actions.

## What counts as a sent request

A request is sent only when the minute's page reads back `Applied, waiting for
processing` (`已发送` / `等待审批` / `Applied to` / `Reapply`). Before the click
the page offers `Send Application`; after a real one it does not.

The provider spells one refusal two ways, both with `server_key: "minutes"`:
`no permission` and `B_PERMISSION_NoPermission`. Match both — over one listing
of 253 minutes on 2026-09-18, 13 came back only in the second spelling.

`Request permission from` reading `Please select` means the page could not
resolve an owner to ask; the button stays disabled and no request can be sent
without choosing a person. That was 149 of 253 minutes in the same run, so
expect it to be the largest bucket, not an edge case.

Do not use `dws minutes +apply-permission` to request access. It answers
`{"requested": true, "result": {"success": true}, "policyId": 4}` for a request
its owner never receives: on 2026-09-18, 85 minutes were "requested" through it
and every one of their pages still offered `Send Application` afterwards, while
a single page click on an untouched minute flipped that same page to
`Applied to <owner> for Viewable only permission / Applied, waiting for
processing`. Treat its receipt as no evidence at all.

## Reading the admin backend

`shanji-admin.dingtalk.com/history` is the only listing that shows minutes you
cannot read; `dws minutes list` (any scope) returns only accessible ones.

- The backend masks **every** title, including your own minutes. Masking is not
  a permission signal. To tell whether a minute is readable, take its
  `row_key` and call `dws minutes get info`; a refusal comes back as a business
  error with `server_key: "minutes"` and `message: "no permission"`.
- The full title and the owner to ask are only on the minute's own page, not in
  the backend table.
- A row whose size column is `-` has been cleaned: approving it grants access to
  nothing. Exclude those before requesting.
- The pagination control updates its own page number before the table
  re-renders. Wait for the first `data-row-key` to change, not for the number,
  or you will re-read the previous page. A walk that was left on the last page
  reports `next` disabled: return to page 1 before enumerating.

## Prerequisites

- macOS with Google Chrome installed.
- Python 3.10+ and Playwright installed.
- A dedicated DingTalk browser profile/storage state may already exist from prior sync work.

## Session handling on Chrome 153 / Playwright 1.59

`connect_over_cdp` fails against Chrome 153 with `Browser context management is
not supported`, so `export_dingtalk_storage_state.py` cannot run as written.
The login is also a **session cookie**: closing the window ends it, and
`launch_persistent_context` over the same profile cannot open it while the
visible browser holds the lock.

Working sequence:

1. `launch_dingtalk_sync_browser.py` (visible), and the user signs in. Only the
   user does this step.
2. Read the session over raw CDP from the live browser: `Storage.getCookies` on
   the browser-level WebSocket endpoint (`/json/version`).
3. Launch a headless browser with `chromium.launch(channel="chrome",
   headless=True)`, `add_cookies` the result, and verify it lands on
   `/history` rather than `login.dingtalk.com`.

Everything after step 1 is headless. The carried session is still
session-scoped, so it expires on the provider's own schedule and the user signs
in again.

## Current Scripts

Check local prerequisites:

```bash
python3 scripts/doctor.py --pretty
```

Launch a dedicated visible browser when login refresh is needed:

```bash
python3 scripts/launch_dingtalk_sync_browser.py --pretty
```

Export storage state after login:

```bash
python3 scripts/export_dingtalk_storage_state.py --pretty
```

Check CDP connectivity:

```bash
python3 scripts/check_dingtalk_sync_browser.py --pretty
```

Recheck blocked permission pages and optionally send access requests:

```bash
python3 scripts/recheck_dingtalk_permission_pages.py \
  --storage-state ~/Documents/dingtalk-minutes-access-request/.storage_state.json \
  --url "https://shanji.dingtalk.com/app/transcribes/<row_key>" \
  --request-permissions \
  --pretty
```

Diagnose one blocked page:

```bash
python3 scripts/debug_permission_page.py \
  ~/Documents/dingtalk-minutes-access-request/.storage_state.json \
  <row_key>
```

## Default Local Layout

- config: `config.json`
- example config: `config.example.json`
- storage state: `~/Documents/dingtalk-minutes-access-request/.storage_state.json`
- dedicated Chrome profile: `~/Documents/dingtalk-minutes-access-request/.chrome-profile`

## Reporting Back

Always return:

- page URL or row key
- whether the page is accessible now
- whether an access request was sent
- permission-pending or failure reason
- next read path, normally `dws minutes ...`, when access is available
