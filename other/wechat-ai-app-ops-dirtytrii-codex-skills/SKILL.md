---
name: wechat-ai-app-ops
description: Operate the WeChat Official Account AI-application workflow for articles, weekly digests, rich formatting, draft-box updates, and local handoff. Use for Agents, MCP, Skills, tool calling, workflows, and open-source AI updates; exclude Xiaohongshu and Xianyu.
---

# WeChat AI App Ops

Use this skill for the user's WeChat Official Account AI application content workflow, usually inside an `accounts` or content-operations repository. Stay inside the WeChat content lane unless the user explicitly asks for Xiaohongshu or Xianyu.

## Quick Workflow

1. Check repository state first:

```powershell
git status --short --branch
```

2. Read the current handoff, manifest, prediction, article, source list, and target article directory before editing or API calls.
3. Classify the article as `weekly` or `flexible`.
4. For weekly articles, review the previous weekly article in the same series before drafting.
5. If a separate raw drafting model/window is used, apply `content-model-handoff`: raw copy is not final copy; the WeChat role still owns source discipline, article structure, preview quality, draft-box state, and publish gates.
6. Improve the article as a WeChat article, not a cold changelog: use a strong hook, human judgment, varied section structures, visible reader stakes, and explanatory image anchors. Before generating preview or draft-box handoff, run a `humanizer-zh` pass to remove template phrasing, fake reader emotions, repetitive contrast structures, and AI-ish section labels without changing facts or attribution.
7. If the article feels visually dry, add useful illustrations or source screenshots before draft-box update. Save final media inside the WeChat article folder and configure the repository's inline-image manifest.
8. For formal public formatting, prefer `gzh-design` when installed: choose a theme by article type, generate a clean body HTML plus preview wrapper, and run `validate_gzh_html.py` until `ERROR=0`. Use `wechat-article-formatter` as the legacy fallback.
9. Write to the WeChat draft box only when authorized. Draft-box write is not publishing.
10. Before publish, read the latest manifest and run the publish gate. Never publish unless the user explicitly authorizes publishing in the current turn and the gate passes.

## References

- For weekly/flexible article continuity, read `references/weekly-series-workflow.md`.
- For draft-box API guardrails, `.env.wechat.local`, IP whitelist handling, and verification, read `references/draft-box-workflow.md`.
- For article tone, anti-AI texture, varied subhead structures, inline illustrations, and brand/avatar assets, read `references/formatting-and-visuals.md`.

## Conditional Related Skills

Load these only when the article task needs that capability. If a related skill is not installed in the current Codex environment, state that and continue with the closest safe fallback:

- `content-model-handoff`: use when a separate model/window produces raw article copy, title pools, or section drafts. Raw text is input to the WeChat role, not a publish-ready article.
- `gzh-design`: preferred for formal WeChat article layout when available. Use it to choose a theme, produce clean body HTML + preview wrapper, and validate with `validate_gzh_html.py` to `ERROR=0`.
- `wechat-tech-writer`: use for AI technology topic research, source gathering, and first-pass Chinese WeChat article drafting.
- `humanizer-zh`: use for Chinese article copy humanization, anti-AI texture, and final voice polish before WeChat preview or draft-box handoff.
- `story-deslop`: use only when a WeChat article contains narrative prose, story fragments, or dialogue that needs a natural storytelling pass; do not apply it to ordinary AI/tooling analysis copy.
- `wechat-article-formatter`: use as a legacy fallback when `gzh-design` is unavailable or the repository still relies on the older Markdown-to-WeChat HTML formatter.
- `guizang-social-card-skill`: use for WeChat covers, inline social-card-style illustrations, explanatory Swiss-style figures, and image-rich article assets.
- `imagegen`: use for new bitmap brand assets such as avatars or non-vector visual concepts; copy final project assets into the article directory.

## Local Commands

Prefer the repository's documented `node` command or system `node`. Use Codex bundled Node only when system `node` is unavailable or denied; discover the bundled path from the active Codex runtime/workspace dependencies instead of hard-coding a personal machine path.

On Windows PowerShell, read Chinese article files with explicit UTF-8 and avoid trusting garbled terminal output:

```powershell
Get-Content -Raw -Encoding UTF8 content\wechat\<date>\article.md
```

For repositories that have migrated to account-first content layout, prefer the repository's documented paths such as:

```text
content/accounts/<account>/platforms/wechat/<article-dir>/
content/accounts/<account>/platforms/wechat/automation/daily-runs/<date>.json
```

Older repositories may still use:

```text
content\wechat\<date>
```

Use the path documented by the target repo; do not create a parallel legacy directory just because an older command example says `content/wechat`.

If a Node one-liner needs to match Chinese text, prefer reading UTF-8 files directly or use Unicode escapes in the check script instead of piping raw Chinese through a shell that may recode it.

```powershell
node --check scripts\wechat\create-draft.cjs
```

For a repository that uses `scripts/wechat/create-draft.cjs`, the draft command usually looks like:

```powershell
node scripts\wechat\create-draft.cjs <article-directory>
```

Use `WECHAT_MP_DRY_RUN=1` with `WECHAT_MP_HTML_PREVIEW_PATH` to generate the local HTML preview without WeChat API calls.

When updating an existing draft, set these only for the current shell:

```powershell
$result = Get-Content -Raw -Encoding UTF8 content\wechat\<date>\wechat-draft-result.json | ConvertFrom-Json
$env:WECHAT_MP_UPDATE_DRAFT_MEDIA_ID = $result.draft_media_id
$env:WECHAT_MP_THUMB_MEDIA_ID = $result.thumb_media_id
```

## Formal GZH Layout And Draft Gate

When the article is moving toward a real WeChat draft:

1. **Format gate.** Prefer `gzh-design` if installed. Pick the theme by article type, generate the clean body HTML and preview wrapper, and run the validator until `ERROR=0`. Do not treat an unvalidated preview as publish-ready.
2. **Media gate.** Preserve source screenshots, factual images, charts, and inline illustrations. Redesign explanatory cards to match the selected theme, but keep factual screenshots as factual screenshots with reader-facing captions.
3. **Draft-box gate.** Updating the draft box is a write to the WeChat draft, not a publish. Reuse existing `draft_media_id` when updating the same article unless the user asks for a new draft.
4. **UI-prepare gate.** Before publish, verify or ask the user to verify original/comment/appreciation states. If the draft content changed after the last UI prepare, the old UI prepare report is stale.
5. **Manifest gate.** Publish automation must read the latest manifest/handoff file and stop on `no_manifest`, missing paths, stale UI prepare, low prediction score, too many revisions, window mismatch, or status not `ready_for_publish`.

Completion criterion: the final handoff can state the article path, prediction path, clean HTML/preview path, draft result, UI prepare state, manifest status, and whether the publish command was **not run** or was run with explicit current-turn approval.

## Non-Negotiables

- Never publish by default. Draft-box write is not publishing.
- Never run a final publish command from memory. Read the latest manifest / handoff file first and stop if it is missing or stale.
- A publish gate should stop unless all required conditions pass: manifest status is `ready_for_publish`; prediction score meets the repo threshold; revision-round limit is not exceeded; required article, prediction, preview, draft result, and UI-prepare report paths exist; original and comments are enabled or user-confirmed; publish window matches or the user explicitly overrides it.
- `appreciation=unknown` may be allowed when the repo policy says so, but `original` and `comments` should not be silently ignored.
- If the draft box was updated after the latest UI prepare / settings check, the old report is stale. Re-run UI prepare or ask for explicit manual confirmation before publishing.
- Never write AppID/AppSecret into repository files, article files, result JSON, or responses.
- Do not print secrets when checking `.env.wechat.local`; check presence only.
- Do not modify `content/xiaohongshu`, `content/xianyu`, or unrelated directories unless explicitly asked.
- If updating an existing WeChat draft, reuse the existing `draft_media_id` and `thumb_media_id` where possible instead of creating duplicate drafts.
- Do not leave generated WeChat assets only under `.codex/generated_images`; copy final assets into `content/wechat/...`.
- Body images must be uploaded through the WeChat article image path before API update; do not send draft content with local filesystem image paths.
- After API calls, report title, article path, cover path, source list path, draft `media_id`, and explicitly state whether it was only written to draft box and not published.
