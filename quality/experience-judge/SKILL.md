---
name: experience-judge
description: Score the visual quality of the public surfaces the experience-audit organ captured — layout, typography, coherence, trust — and record verdicts. Use when asked to judge, review, or grade how the public sites/pages LOOK (not just whether they load), or to run the visual half of the experience audit. The mechanical half (reachable/fast/light/no-errors) is scripts/experience-audit.py; this skill is its human/model-in-the-loop visual complement.
---

# experience-judge

experience-audit.py measures the MECHANICAL rungs of a visitor's experience (reachable, fast, light,
no broken images, no console errors, has a title). It cannot judge whether the page *looks good*.
This skill is that missing rung: read the latest capture, score each surface on **layout,
typography, coherence, trust** (each 0-5), and append the verdict to the judgment register so the
effector can file bounded visual-fix tasks.

A judgment is pinned to the exact pixels it judged: cite the screenshot's `sha256`. A re-sweep that
changes the capture invalidates the old verdict — so judge against the CURRENT artifact only.

## Steps

1. **Read the latest sweep artifact.** `logs/experience-audit.json` (schema `limen.experience_audit.v1`).
   If it is missing or stale, run `python3 scripts/experience-audit.py --sweep` first (needs
   playwright + chromium for screenshots; the http tier captures no shots, so a real visual judgment
   requires the playwright tier). Each surface entry carries its `url`, `screenshot_sha256`,
   `captured_at`, and the mechanical rungs already scored.

2. **View each surface's shot.** `logs/experience/shots/<id>.png` (latest capture, overwritten each
   sweep). Confirm the file's sha256 matches the artifact's `screenshot_sha256` before judging — if
   they differ, re-sweep (the shot is newer/older than the recorded judgment target).

3. **Score each surface 0-5** on:
   - **layout** — spacing, alignment, hierarchy, responsive fit
   - **typography** — legibility, scale, consistent families/weights
   - **coherence** — visual consistency with the rest of the estate; does it feel like one brand
   - **trust** — does it read as credible/professional to a first-time visitor (the demand-funnel test)
   Set `verdict: pass` when the surface is clearly acceptable to show a buyer; `verdict: fail` when a
   visible defect would repel the visitor. Record concrete, **PII-clean, public-safe** `defects` and
   one `suggested_fix`.

4. **Append rows to the register.** For each judged surface, append a row under its id in
   `institutio/observatory/experience-judgments.yaml` (newest last), with `judged_at`, `captured_at`
   (copied from the artifact), `screenshot_sha256`, `model` (your model id or a human handle),
   `verdict`, `scores`, `defects`, `suggested_fix`. Keep the existing schema exactly — run
   `python3 scripts/experience-audit.py --doctor` and confirm it exits 0 (it validates verdicts and
   0-5 scores).

5. **Open a PR.** Branch `feat/experience-judgments-<mmdd>` off `origin/main` in a worktree, stage
   ONLY `institutio/observatory/experience-judgments.yaml`, commit (body ends with the
   `Co-Authored-By: Claude Fable 5` line), push, and open a PR whose body cites each judged
   surface's screenshot sha256 (the pixels the verdict is pinned to) and summarizes the scores. Do
   not commit anything under `logs/` (gitignored artifacts). The effector
   (`generate-experience-backlog.py`) reads the merged verdicts and files bounded
   `EXP-<surface>-visual` tasks for any `verdict: fail`.
