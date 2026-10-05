---
name: shorts-upload
description: >-
  Cross-post Shorts from the YouTube channel configured in YOUTUBE_HANDLE to
  TARGET_PLATFORMS with the repository's code-first pipeline. Use for planning,
  uploading, retrying, verifying, or catching up Shorts. Browser/Computer tools
  are recovery tools for failed cells, inconclusive verification, and UI drift;
  they are not the default upload path. Do not use for video editing, analytics,
  YouTube-only publishing, or unrelated social tasks.
---

# Shorts upload

Run from the repository root. Use `.env` values and the declarative content
policy file. Never substitute maintainer or guessed account information.

## Non-negotiable rules

- **No duplicate uploads.** Re-upload only after fresh, direct verification on
  that platform shows the exact video is missing. A timeout, absent toast, or
  empty feed is not enough.
- **Exact post text.** Publish prepared `post_text`, or an uploader's documented
  length-limited form. Never add a YouTube ID, filename, URL, batch label, or
  debug note.
- **Oldest first.** Upload selected Shorts by `upload_date` and `timestamp`
  ascending so downstream feeds preserve source order.
- **Policy always applies.** Explicit `--video-id` bypasses candidate selection,
  not content policies. Respect allowed platforms, full-description rules, and
  UI disclosure requirements.
- **Failures are cell-local.** One platform's login, profile, UI, or verification
  problem must not stop healthy platforms. Fix selected IDs, exhaust runnable
  `video x platform` cells, then return to blockers.
- **Stop means cleanup.** On stop/cancel requests, immediately stop new work,
  terminate the pipeline and only its child Playwright/Chrome processes, verify
  that those PIDs are gone, then report completion.
- **Protect local state.** Never commit `.env`, cookies, Chrome profiles,
  downloads, SQLite files, screenshots, HTML captures, or other `data/` output.

## Interpret the request

- A number means the newest that many missing Shorts. Upload oldest first after
  selection.
- `all` means all missing items inside the configured lookback window.
- `skip ads` maps to `--skip-ads`; `include ads` maps to `--include-ads`.
- `dry run` maps to `--dry-run`.
- A named platform maps to `--platforms`.
- A specific YouTube ID maps to repeatable `--video-id`.
- Current explicit user instructions override batch size and ad inclusion only;
  they do not disable deduplication, verification, or content policies.

## Phase 1: inspect and freeze the plan

```bash
uv run shorts-dist doctor
uv run shorts-dist plan --json
```

If only some sessions are unavailable, preserve the selected video IDs and run
healthy platforms first. Login and 2FA require the user, but they do not block
unrelated platform lanes. If every enabled platform is blocked, report the exact
required action without attempting uploads.

For a no-publish request, run `uv run shorts-dist run --dry-run --json` and stop.

## Phase 2: run the code pipeline

```bash
uv run shorts-dist run --json
uv run shorts-dist run --platforms instagram,tiktok --video-id <ID> --json
```

Map requested count to `--upload-limit N`; map backlog to
`--selection-mode all`. Exit code `0` means no cell needs attention. Exit code
`3` means inspect `data/runs/<run_id>/report.json`; it does not mean the entire
batch failed.

Finish when each selected matrix cell is one of:

- `verified`, `published`, or `pending-verify`
- `already`
- `skipped-ad` or `skipped-policy`
- `blocked` with an exact user action

Do not leave runnable cells unattempted because an earlier lane failed.

## Phase 3: recover only failed cells

Use Browser/Computer only when the report contains `failed`, `blocked`, or
`agent-required`, or verification is `missing`/`inconclusive`.

1. Read that cell's `agent_brief`, screenshot, and full HTML.
2. Confirm the media and prepared text before clicking publish.
3. Do not use the same Chrome profile concurrently from code and agent tools.
4. Stop for login, 2FA, CAPTCHA, security review, copyright rejection, wrong
   account, missing permissions, or an unsupported paid-promotion decision.
5. Directly verify the resulting post using `references/verify-urls.md`.
6. Record a verified manual completion:

```bash
uv run shorts-dist mark-uploaded <platform> <ID> \
  --url '<POST_URL>' --source agent
```

### UI drift repair

When the same step repeatedly fails, repair the uploader rather than repeatedly
driving the UI:

1. Inspect artifacts for the actual dialog, labels, roles, and state attributes.
2. Add selectors to the candidate list in
   `src/shorts_distributor/uploaders/<platform>.py`; keep old candidates for
   coexisting UI versions.
3. Scope controls to the active dialog or panel. Prefer exact text and stable
   attributes over broad ancestor text.
4. After a click, verify the resulting state. Never close a page while upload or
   publish progress is visible.
5. Test one cell with `uv run shorts-dist upload <platform> <ID>`.
6. Add the reusable finding to `references/failure-modes.md`.

## Phase 4: verify and report

```bash
uv run shorts-dist verify --pending --json
```

Use post-specific evidence: unique text, title, thumbnail, direct post URL,
success dialog, or creator content-list row. Never record a platform root URL.
For an inconclusive result, cross-check before deciding to retry.

Report the final `platform x video` matrix, pending verification, skipped-policy
reasons, and exact blockers. A completed post without a direct URL may be kept as
`published`/pending, but must not be uploaded again solely to obtain a URL.

## References

- `references/architecture.md`: invariants, status model, state ownership, and
  profile lifecycle.
- `references/customization.md`: channel setup, policy rules, disclosures, and
  new uploader contracts.
- `references/failure-modes.md`: reusable UI and verification failures.
- `references/verify-urls.md`: platform-specific verification surfaces.
