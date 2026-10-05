---
name: demo-recording
description: Explore a real site/feature with agent-browser, record per-scene screen clips + artifacts, then generate a CapCut-ready script grounded in the captured files. Includes retake workflow.
---

User input (must consider):

$ARGUMENTS

# Objective

Produce a "demo pack" that a human can assemble in CapCut with minimal thinking:

- per-scene clips (canonical filenames)
- per-scene end-frame screenshots for review
- scene plan (replayable)
- manifest (durations, checks, retake history)
- CapCut script in the style of `video-production` skill, but ONLY referencing real captured assets

# Hard rules

- Ground truth only: never invent UI labels/states; derive steps from real exploration (`snapshot`, `get text`, etc.).
- Prefer robust locators: `find role|text|label|placeholder|testid …` over `@eN` refs (refs unstable across reloads).
- Recording is per-scene.
- Retakes supported:
  - auto-retake when configured checks fail
  - manual later: user message like `retake scenes: 3,5` or `retake scenes: invite-member`
- Minimal cleanup/idempotency in MVP: optional best-effort delete steps per scene; otherwise warn about state drift.

# Required tool base

Use `agent-browser` commands from `skills/agent-browser/references/commands.md`:

- Navigation: `open`, `back`, `reload`
- Analysis: `snapshot -i`, `get url`, `wait --url/--text/--load`
- Capture: `record start <file.webm>`, `record stop`, `screenshot <file.png>`, `screenshot --annotate` (writes to temp; move to stills/)
- State: `state save/load`, `--session-name`

Rule: for reliability across retakes, run EVERY agent-browser command with `--session-name <session_name>`.

- When drafting `scene-plan.yml`, bake `--session-name <session_name>` into each step command string (see template).

# Output pack structure (create on run)

Create a new run dir (or reuse existing on retake):

```
<runDir>/
  scene-plan.yml
  manifest.json
  review.md
  clips/
    01-<slug>.webm
    02-<slug>.webm
    _tmp/
    _replaced/
  stills/
    01-end.png
    01-annotated.png   (optional; create via `agent-browser screenshot --annotate` then move temp file)
  script/
    capcut-script.md
    shotlist.csv
  repro/
    auth.json          (optional)
    fixtures.json      (optional)
    run-log.md
```

Naming rule: `NN-<slug>` where `NN` is 2-digit scene index.

# Modes (conversation-level)

Implement 3 modes; choose based on user intent:

## Mode A: PLAN (explore → draft scene plan)

Goal: produce `scene-plan.yml` draft grounded in observed UI.

Process:

1. Ask up to 6 clarifying questions total, 1 per message, only if missing:
   - site URL + env (staging/prod)
   - auth method (none / email+pass / SSO+2FA manual)
   - target aspect (default 16:9) + fps (default 30)
   - audience + key message + CTA
   - list of features/journey steps (or "explore and propose")
2. Start a dedicated browser session:
   - Prefer: `agent-browser --session-name <project>-demo open <url>`
3. Explore each candidate scene:
   - `agent-browser snapshot -i` (capture real labels)
   - capture notes: what user sees, what changes, what should be checked
   - optional: `agent-browser screenshot --annotate` (returns temp path) then move it to `stills/NN-annotated.png` for callouts
4. Draft `scene-plan.yml` (prefer semantic `find …` commands; avoid `@eN`):
   - scenes with: setup steps, record steps, checks (URL/text)
   - keep record steps user-facing only
5. Output config summary + ask: "Record now?".

## Mode B: RECORD (record all scenes)

Goal: create clips + stills + manifest + CapCut script.

Loop scenes in order:

- Run `setup_steps` (not recorded)
- Record:
  - `agent-browser record start clips/_tmp/NN-slug.webm`
  - run `record_steps` (include human pacing waits)
  - `agent-browser record stop`
- Post-capture:
  - `agent-browser screenshot stills/NN-end.png`
  - Evaluate checks (if present):
    - URL: `agent-browser get url` then glob match
    - Snapshot text: `agent-browser snapshot -c` then substring(s) match
- Auto-retake (only if checks present and failing):
  - retry up to `max_attempts` (default 2)
  - on each attempt overwrite the temp webm
- Promote to canonical clip:
  - if `clips/NN-slug.webm` exists, move it to `clips/_replaced/NN-slug_<timestamp>.webm`
  - move temp to `clips/NN-slug.webm`
- Update `manifest.json` per attempt, per scene.

After all scenes:

- Write `review.md` (scene table: status, clip path, still path, check failures)
- Generate `script/shotlist.csv` (one row per scene)
- Generate `script/capcut-script.md` using `video-production` formatting conventions.
  - Must reference only existing files in `<runDir>/clips` and `<runDir>/stills`.

## Mode C: RETAKE (subset)

Triggered by user message:

- `retake scenes: 3,5`
- `retake scenes: create-project, invite-member`

Behavior:

- Load existing `<runDir>/scene-plan.yml` + `manifest.json`
- Only re-run selected scenes using Mode B loop
- Always:
  - back up old canonical to `clips/_replaced/…`
  - regenerate `review.md`, `shotlist.csv`, `capcut-script.md`

# Checks (MVP)

Scene `checks` supports:

- `url_glob`: e.g. `"**/dashboard"`
- `snapshot_contains`: list of substrings expected in `snapshot -c` output

If checks absent: mark scene `NO_CHECKS` in review.

# Minimal Scene Plan schema (YAML)

See template: `templates/scene-plan.template.yml`.

# CapCut script output rules

Use the `video-production` skill conventions:

- absolute timestamps (M:SS.s) across whole video
- track conventions (V1 base, V2+ overlays; A1 music, A2 SFX, A3 VO)
- per scene: Elements Table + actionable CapCut steps

But: keep CapCut UI paths non-hallucinated.

- If unsure: `Path (may vary): …` + `Search keyword: "…"`

# Common pitfalls

- Using `@eN` refs in saved plans → breaks on retake. Prefer `find …` semantic commands.
- Not waiting for page transitions → add `wait --url`, `wait --text`, or `wait --load networkidle`.
- State drift after retake → warn; optionally add scene-level `delete_steps`.

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
