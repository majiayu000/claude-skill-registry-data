---
name: web-video
description: Record and auto-edit short, focused screen videos of a web app with Playwright, ffmpeg and an event log. Mode feature-demo makes a polished client walkthrough (cursor, click zoom, numbered captions, optional voiceover, intro/outro). Mode bug-report makes a QA repro clip under 60 s with a steps panel, frozen bug moment, red box, EXPECTED vs ACTUAL, console/network errors, plus redacted trace, HAR and a bug-report.md. Use for "record a demo", "walkthrough video", "video hướng dẫn", "quay bug", "repro video", "attach video to issue", "trim/speed up this screen recording".
allowed-tools: [Bash, Read, Write, Edit]
---

# web-video

Scripted take with an **event log** → EDL → one ffmpeg graph → self-verify → export.
Scripts do the fragile parts (timing, filters, redaction); you plan, look at frames and talk to the user.

```bash
WV=~/.claude/skills/web-video                         # scripts: $WV/scripts, examples: $WV/assets/examples
PY=$(command -v python3 || command -v python)         # Windows (Git Bash): python
```
Works on macOS, Windows and Linux. The same pipeline is on PATH as `web-video <command>` after `install.py` (`web-video help`; `web-video make sb.yaml --slug x` runs every step). Prefer the individual scripts below when you need to look between steps.

## When to Use

| Situation | Mode |
|---|---|
| Show a client how a delivered feature works | `feature-demo` |
| QA/dev needs a short repro of a bug for developers | `bug-report` |
| User already has a recording and wants it shorter | `edl.py --edit-only` (no event log) |

Not for: tutorials over 3 min, native desktop apps (record them with the OS recorder, then edit-only), marketing films (use a Remotion/HyperFrames skill).

## Hard rules

1. **Ask, confirm, execute.** Show the storyboard in plain language and wait for a yes before the real take.
2. **Nothing leaves the machine without a yes.** No uploads, posts, issue comments or accounts. Cloud TTS (`tts.py --allow-cloud`) sends text out: ask first. Default narration is local (Piper / `say`) or captions only.
3. **Test data only.** Test accounts, `storage_state` or a browser profile (only when the user asks for their own sign-in); seed and clean fixtures; never film production customer data. Run `redact.py` before sharing trace/HAR/console; attach only `*.redacted.*`.
4. **One clock.** Times come from `events.json` plus the single `video_offset` that `calibrate.py` writes. Never add an offset anywhere else. If it is wrong, fix it with `calibrate.py RUN --set`.
5. **Never overwrite a run.** `record.py --slug` creates `video-out/<slug>/v<N>/`; re-edits write new files in that run only.
6. **A click counts only if it happened.** `record.py` refuses hidden, off-screen or covered targets; you confirm the effect in the contact sheet.
7. **Frames are the source of truth.** Never call a video done from logs alone: run `verify.py`, open `verify/contact.png`, state what you could not check (audio).
8. **Draft, then final.** Show the 480p draft and the verify report; render the final only after approval. At most 3 fix passes without new input from the user.

## Step 0. Preflight (first use, or when something breaks)

```bash
which ffmpeg ffprobe && ffmpeg -hide_banner -filters | grep -wcE "drawtext|zoompan|subtitles"   # expect 3
$PY -c "import playwright, yaml, PIL; print('python deps ok')"
$PY $WV/scripts/install_tts.py --check || $PY $WV/scripts/install_tts.py   # Vietnamese voice, ~200 MB in ~/.cache/web-video
$PY $WV/scripts/selftest.py        # full pipeline on the bundled fixture app, both modes (~1 min)
```
Missing something: print the install command and ask; never install silently. Python deps: `$PY -m pip install -r $WV/requirements.txt && $PY -m playwright install chromium`. ffmpeg: `brew install ffmpeg-full` + its bin first on PATH (macOS; plain `ffmpeg` 8+ lacks drawtext), `winget install Gyan.FFmpeg` (Windows), `apt install ffmpeg` (Linux).
If `video-out/<slug>/project.md` exists, read it and summarise the last run in one line before asking anything.

## Step 1. Inputs and storyboard

Ask for everything missing in **one** message: URL and start route; login (test account, storage state, or the user's browser profile for SSO sites); the flow and what the viewer must see; may the take create/delete data; output folder; language of captions. For bug-report also: expected, actual, environment/build, reporter's version.

Write `storyboard.yaml` (schema and caption rules: `references/storyboard.md`; examples: `assets/examples/feature-demo.yaml`, `assets/examples/bug-report.yaml`):
```yaml
mode: feature-demo                 # or bug-report
url: http://localhost:3000
lang: vi
title: "Tạo hoá đơn mới"
steps:
  - {caption: "Đăng nhập", hidden: true, do: ["goto /login", "fill #email | qa@example.com", "fill #password | ***", "click button[type=submit]", "wait_url **/"]}
  - {caption: "Bấm New invoice", do: "click [data-testid=new-invoice]"}
```
**Look (feature-demo): the video must look like the project it shows.** Before writing the storyboard, read that project's design and turn it into a theme; never ship the neutral base silently:
```bash
$PY $WV/scripts/theme.py init --repo <project root> --out theme.yaml   # tokens, CSS vars, Tailwind, DESIGN.md, fonts, brand
$PY $WV/scripts/theme.py check theme.yaml && $PY $WV/scripts/theme.py preview theme.yaml --out /tmp/look --title "..."
```
Read the `# Sources:` and notes in the draft, compare with the project's DESIGN.md / UI skill / logo, fix by hand, Read `/tmp/look/frame-preview.png` and `intro.png`, then set `theme: theme.yaml`. Only when the project has no design signals use `theme: clean`, and say so to the user. Details: `references/themes.md`.

Quote any action that contains `#` (YAML comment). feature-demo: 30-90 s, max 8 visible steps, captions about benefits (≤ 12 words). bug-report: ≤ 60 s, mark the failing step `bug: true` (optional `bug_target:` selector for the red box).

## Step 2. Discover → Rehearse → Record

```bash
$PY $WV/scripts/record.py storyboard.yaml --discover    # visible elements + selectors before each step
$PY $WV/scripts/record.py storyboard.yaml --rehearse    # every step, fail loudly; repeat until all "ok"
$PY $WV/scripts/record.py storyboard.yaml --slug invoice-demo   # the take; prints "run dir: ..."
RUN=video-out/invoice-demo/v1      # copy the printed run dir; never pick "the latest" folder
```
**Sites behind SSO (Google, Okta):** Playwright cannot sign in for the user. Use a persistent profile; the user signs in, you never type a password:
```bash
$PY $WV/scripts/browser_profile.py chrome-profiles                     # Chrome profiles: dir | name | account
$PY $WV/scripts/browser_profile.py import demo --from-chrome "Profile 1"   # copy that profile's sessions (macOS)
$PY $WV/scripts/browser_profile.py login demo https://app.example.com  # or: user signs in a real window, closes it
$PY $WV/scripts/browser_profile.py check demo https://app.example.com  # headless check before the take
$PY $WV/scripts/record.py storyboard.yaml --rehearse --profile demo    # or `profile: demo` in the storyboard
```
Ask which Chrome profile first. A profile holds live sessions: `browser_profile.py delete demo` after the video, and redact HAR/trace (cookies) before sharing. Details: `references/record.md`.

Use selectors from the discover dump, never guesses. For bug-report, rehearse must print `bug step reached` (and the errors you expect); if not, the bug did not reproduce: stop and report (status vocabulary in `references/bug-report.md`).
The take writes `raw.webm events.json console.json net.har trace.zip meta.json` and calibrates the offset with a sync flash. Exit 2 = a step failed (artifacts kept), 3 = no video. Details, limits (25 fps VP8, native dropdowns invisible): `references/record.md`.

## Step 3. Narration (feature-demo, optional)

```bash
$PY $WV/scripts/tts.py "$RUN"                    # lang vi: Piper Ngọc Lan (local, MIT); else macOS say
$PY $WV/scripts/tts.py "$RUN" --voice quanghuy   # ngoclan | minhanh | thuha | yennhi (nữ), quanghuy (nam)
```
Text = step `say:` or caption; numbers/%/$/đ are spelled out in Vietnamese. English UI words sound accented: prefer the Vietnamese label ("bấm Lưu") or write it phonetically in `say:` ("bấm nút xếp"). Prints words/s per clip; aim for ≤ 4. `edl.py` holds each step until its clip ends. Voices and tuning: `references/overlays.md`.

## Step 4. Auto-edit, draft render

```bash
$PY $WV/scripts/edl.py "$RUN" --render draft     # edl.json, filter.txt, captions.srt, draft.mp4 (480p)
```
Keeps ±1 s around every action at 1x, speeds idle 6x (bug-report 8x, never longer than 0.6 s), cuts hidden steps, holds captions long enough to read, zooms ≤ 1.5x on clicks (feature-demo), freezes the bug moment 2 s (bug-report). Rules and manual ffmpeg recipes: `references/edl-ffmpeg.md`; overlay look: `references/overlays.md`.

## Step 5. Self-verify (before showing anything)

```bash
$PY $WV/scripts/verify.py "$RUN"                 # ffprobe checks, checkpoint frames, verify/contact.png, report.md
```
Then **Read `verify/contact.png`** and tick the manual checklist in `verify/report.md` (caption not covering the click, click effect visible, bug visible at the red box, text readable, no secrets on screen). Fix (storyboard, `calibrate.py --set`, `--zoom`, `--no-zoom`) and re-run Steps 2-5, max 3 passes. For a client-facing video you may ask a fresh subagent to criticise the contact sheet against the storyboard. Details: `references/verify.md`.

Show the user: draft path, duration, the verify table, what you could not check. Wait for approval.

## Step 6. Final render, export, package

```bash
$PY $WV/scripts/edl.py "$RUN" --render final && $PY $WV/scripts/verify.py "$RUN" --video edited.mp4
$PY $WV/scripts/export.py "$RUN/edited.mp4" "$RUN/final.mp4" --max-mb 9   # add --gif "$RUN/final.gif" only if asked
$PY $WV/scripts/redact.py "$RUN"                 # bug-report (and any time trace/HAR is shared)
$PY $WV/scripts/report.py "$RUN"                 # summary.txt or bug-report.md; appends ../project.md
```
Set the bug-report **status** yourself (`confirmed` / `partially confirmed` / `not reproduced` / `blocked`); the script only suggests one. Add to `project.md` what the user asked to change and which selectors failed. Size targets per platform and `gh --attach` (needs gh ≥ 2.99, explicit yes): `references/export.md`.

## Scripts

| Script | Does |
|---|---|
| `scripts/browser_profile.py` | persistent signed-in profiles: import from Chrome, interactive login, check, delete |
| `scripts/record.py` | storyboard → discover / rehearse / take with cursor, ripple, event log, HAR, trace |
| `scripts/calibrate.py` | sync-flash offset (auto after a take); `--set` / `--show` |
| `scripts/tts.py`, `scripts/install_tts.py` | per-step narration (Piper Vietnamese via `scripts/piper_worker.py`, or `say`; cloud only with `--allow-cloud`); one-time voice install |
| `scripts/edl.py` | events → EDL → `filter.txt` → draft/final render; `--edit-only` for existing recordings |
| `scripts/theme.py`, `scripts/theme_init.py` | project theme from the repo's design (`init`), `check`, `preview`, `fonts`, `list`; framed recording, caption band, themed cards |
| `scripts/overlay.py` | caption, card, bug panel, red box, timestamp, SRT builders (imported by edl.py) |
| `scripts/verify.py` | probe checks, frames, contact sheet, report |
| `scripts/export.py` | size-targeted H.264 encode, optional GIF |
| `scripts/redact.py` | mask secrets in HAR, trace, console (headers, cookies, typed secrets) |
| `scripts/report.py` | summary.txt / bug-report.md + project.md log |
| `scripts/web_video.py` | terminal entry point, on PATH as `web-video` after `install.py` |
| `scripts/selftest.py`, `scripts/lint_skill.py` | end-to-end test on `assets/fixture/`; skill lint (run after editing the skill) |

## References

`references/storyboard.md` (schema, actions, caption rules) · `references/record.md` (take, event log, limits) · `references/edl-ffmpeg.md` (EDL rules, ffmpeg recipes, edit-only) · `references/overlays.md` (captions, zoom, cards, bug panel, narration) · `references/verify.md` (checks, review loop) · `references/bug-report.md` (status, template, repro discipline) · `references/export.md` (platform limits, GIF, attach) · `references/failures.md` (symptom → fix) · `references/hifi-capture.md` (crisper capture for client demos) · `references/themes.md` (designed background, project guideline → theme)

## Quick failure map

- SSO site shows the sign-in page: the profile is signed out; `browser_profile.py login NAME URL`, then `check`.
- Step fails in rehearse: use the printed element list; selector matches 2+ elements → make it specific.
- Zoom/caption a few frames off: `calibrate.py RUN --show`, then `--set`; re-run edl.py.
- Click recorded but nothing happens on screen: element covered or wrong target; check `click*+0.3` frame.
- Captions show boxes instead of letters: font lacks glyphs; set `WEB_VIDEO_FONT=/path/font.ttf`.
- `final.mp4` over the limit: `export.py … --max-mb 9 --height 540`, or cut steps.
More in `references/failures.md`.
