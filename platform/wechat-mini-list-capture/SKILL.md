---
name: wechat-mini-list-capture
description: Cooperative visible-UI workflow for collecting simple WeChat mini-program list/detail pages with Codex-generated screenshot annotations and optional Android ADB no-mouse execution. Use when the user wants Codex to mark app/list/item boxes, apply annotations to config, run captures without taking over the Windows mouse, guide tab switching, or export review files without private API replay.
---

# WeChat Mini List Capture

Use this skill as a human-Codex operating loop, not as a blind crawler. Prefer Android ADB mode when the user does not want Windows mouse takeover. The user keeps the mini program visible in the chosen environment and performs login/tab switching when needed; Codex directly annotates screenshots, applies those annotations to config, runs small samples, and exports review artifacts.

## Boundaries

- Use only user-visible, already-open UI state.
- Do not read, copy, or store cookies, tokens, headers, localStorage, private APIs, or credentials.
- Keep raw screenshots, OCR text, checkpoints, and logs under the ignored runtime directory.
- Put only status and sanitized review/export summaries in `D:\todo`.
- Treat OCR and AI outputs as candidates until human-reviewed.

## Local Harness

Default local code path:

```powershell
D:\agent-workflow-lab\harnesses\wechat-mini-list-capture
```

Default private runtime:

```powershell
D:\agent-workflow-lab\runtime\wechat-mini-list-capture
```

Before running commands, read the harness `README.md` for current command usage and screenshot-review criteria. If a referenced `references/harness-workflow.md` exists in a future version, read that as the more specific runbook.

## OfferShow List B Fast Profile

For the OfferShow `list_b` high-salary sample/comment workflow, do not rely on hand-edited `runtime\wechat-mini-list-capture\config.local.json` values. Before any full or resumed `list_b` run, apply the saved profile from the harness repo:

```powershell
cd D:\agent-workflow-lab\harnesses\wechat-mini-list-capture
.\scripts\apply-list-b-fast-profile.ps1
```

This profile is the durable source for the faster desktop strategy: PageDown-style list/comment movement, a 5s detail-page load wait, salary-table-first detail capture, no routine blank/content-area clicks inside detail pages, OCR-recognized reply-expander clicks, re-screenshot/re-OCR after each reply expansion before clicking another expander, dynamic mini-program back (`app-back`), and a strict guard requiring the full app OCR to show `顶尖人才计划` plus salary-card structure before scanning a `list_b` round or opening any next detail. If scrolling appears slow again, first reapply this profile and inspect `scroll-events.jsonl` / per-item `comment_events` before changing ad hoc runtime config.

## Driver Choice

- Prefer `android_adb` when the user wants no mouse takeover. It controls a real Android device or emulator through ADB screenshots, taps, swipes, and back key events.
- Use `desktop` only when the user accepts Windows mouse/focus takeover or Android is unavailable.
- If `doctor-android.ps1` reports `adb is not installed or not on PATH`, stop and ask the user to install Android SDK Platform Tools or provide `-AdbPath`.

## Operating Loop

1. Run the relevant doctor command. Prefer `doctor-android.ps1 -Screenshot` for no-mouse mode.
2. Inspect the raw current screenshot, usually `runtime\wechat-mini-list-capture\calibration-<list-id>-screen.png`.
3. Create a Codex annotation JSON with `app_region`, `list_region`, and full-card `items[]` boxes.
4. Apply the annotation with `apply-annotation.ps1`; this renders a review image and writes `config.local.json`.
5. Inspect the rendered review image. If boxes are good, run a small sample first, usually `-MaxItems 3`.
6. If boxes are bad, revise the annotation JSON and reapply it. Do not ask the user to manually mark row slots.
7. After sample capture, export a review CSV and ask the user to confirm field quality before full capture.
8. Write back durable status in `D:\todo` when the workflow meaningfully progresses.

## Codex Annotation Format

Generate JSON like this under the private runtime:

```json
{
  "list_id": "list_a",
  "source_image": "D:\\agent-workflow-lab\\runtime\\wechat-mini-list-capture\\calibration-list_a-screen.png",
  "annotator": "codex",
  "app_region": [765, 96, 1392, 1274],
  "list_region": [765, 690, 1392, 1274],
  "items": [
    {
      "id": "list_a_visible_1",
      "label": "visible card title",
      "box": [790, 690, 1368, 962],
      "confidence": 0.86,
      "note": "full visible card; excludes announcement"
    }
  ]
}
```

Apply it:

```powershell
.\scripts\apply-annotation.ps1 -Annotation D:\agent-workflow-lab\runtime\wechat-mini-list-capture\codex-annotation-list_a.json
```

The harness stores Codex item boxes as `candidate_mode=row_slots`, but the user does not manually mark them. The harness still OCRs each slot during runtime and uses OCR text for deduplication.

## Annotation Rules

- Make `app_region` cover the mini-program window only.
- Make `list_region` start below tabs and announcement boxes unless the announcement is an intended item.
- Make each `items[].box` cover one whole clickable card.
- Exclude announcement text, close buttons, floating share/add buttons, terminal text, and VS Code UI.
- Prefer 1-3 visible full cards over many uncertain partial boxes.
- If a card is partly covered by a floating button, either avoid the covered edge or mark confidence lower.

## User Coordination

Ask the user only for actions Codex cannot do reliably:

- open the mini program;
- keep the mini-program window visible and stable;
- switch from list A to list B;
- confirm a rendered Codex annotation review image, sample review CSV, or ambiguous screenshot;
- resolve login, QR, CAPTCHA, or platform prompts.

Do not ask the user to manually mark every row unless Codex annotation repeatedly fails and the user explicitly accepts manual fallback.
