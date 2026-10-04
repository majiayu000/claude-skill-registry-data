---
name: watch-and-learn
description: Watch a how-to / tutorial / demo video and turn the procedure it teaches into one or more working Claude Code skills. Use when the user wants to "turn this video into a skill", "watch this tutorial and make a skill", "learn how to do X from this video", "build a skill from this screencast/demo/talk", or capture a repeatable workflow shown in a video. Sends an agent to watch the video (local file or URL) with a local, free, no-API toolchain, breaks the procedure down, authors the skill(s), and verifies they actually work.
license: MIT
compatibility: Runs python3 scripts locally. First run installs av, Pillow, faster-whisper, and yt-dlp into ~/.video-watch-tools (one-time, via scripts/install-tools.sh) and downloads a ~150MB Whisper transcription model. Needs internet on the first run and for URL inputs; no API keys or accounts.
---

# watch-and-learn

Turn a video that *demonstrates a procedure* into a reusable Claude Code skill (or a small set of them), then prove the skill works. The video is the teacher; the output is a skill someone can invoke later without watching anything.

Watching is local and free: `scripts/watch.py` extracts keyframes (PNG) + a labelled contact sheet and transcribes the audio (PyAV + faster-whisper, no API keys, no torch). See `references/watching.md` for how the engine works and its options.

> **Placeholders:** `<this-skill>` = this skill's own directory (where this SKILL.md lives). `<file-or-URL>` = the video you're processing.

## Prerequisites (one-time per machine, usually already done)

`watch.py` **self-locates its toolchain venv and re-execs into it** — no activation, and a plain `python3` invocation is fine (it finds the venv via `$VIDEO_WATCH_TOOLS`, a `tools/venv` up the directory tree, or `~/.video-watch-tools/venv`, which is where the bundled installer puts it). You normally do **nothing** here.

Only if `watch.py` reports the toolchain is missing (a fresh machine) do you install it once:

```sh
bash <this-skill>/scripts/install-tools.sh   # creates the venv at ~/.video-watch-tools (av, Pillow, faster-whisper, yt-dlp)
```

First transcription downloads the Whisper `base` model (~150 MB), cached thereafter.

## Workflow

### 1. Qualify — is this worth a skill?
Before spending on a full watch, decide whether the video actually teaches a **reusable, transferable procedure** worth capturing. Do it cheaply: run `watch.py --transcript-only` (for a talk/narrated video) or just read the title + description, and judge against `references/qualifying.md`. **Proceed** if it's a real how-to you'd invoke later; **STOP and say why** (suggesting notes or a reference doc instead) if it's opinion, a one-off, too trivial, or already covered by an existing skill. **Escape hatch:** an obviously strong tutorial doesn't need belabouring — note it in one line and move on.

### 2. Watch — send an agent
Run the watch step **in a subagent** (the Agent tool), not the main thread: a video digest is 15–25 images plus a transcript, and you don't want that flooding the main context. (No subagent capability in your harness? Run it inline, then summarize into the procedure spec below and drop the raw frames from context before continuing — same result, you just manage the context yourself.) Tell the subagent to:

```sh
python3 <this-skill>/scripts/watch.py "<file-or-URL>" --max-frames 20 --out <a-scratch-dir>
```

Pass `--out` to a scratch/temp dir so nothing lands in a working repo (the default is already a temp dir, but be explicit). Then have the subagent **Read the contact sheet first** (one-image overview), **then** the individual `frames/` it needs, alongside `transcript.txt`, and return a compact **procedure spec** (next step) — not the raw frames. For a long/dense video, raise `--max-frames`; for a slow screencast, `--mode interval --every 5`. **Capture modes:** a talk or podcast is cheaper with `--transcript-only`; a silent screencast with `--frames-only`. Full options + when to use each: `references/watching.md`.

### 3. Break it down — a procedure spec
From the digest, extract the teachable procedure into the structure in `references/procedure-spec-template.md`: the **goal/capability**, **prerequisites**, the **ordered steps**, the **exact commands / tools / UI actions / keystrokes** shown, **decision points**, **gotchas**, and **inputs → outputs**. Cite frame timestamps for anything visual. If the video shows *what* but not *why*, infer carefully and mark inferred bits.

### 4. Decide skill boundaries
One video ≠ always one skill. Apply the rubric in `references/skill-authoring.md`: a skill is **one coherent, reusable capability** with a **narrow trigger**. Split when the video teaches clearly separable capabilities; keep it one skill when the steps only make sense together. Name each skill in kebab-case by the *capability*, not the video. **Escape hatch:** if the video teaches a single small procedure, skip the boundary analysis — it's one skill; don't over-ceremony it.

### 5. Author the skill(s)
Write each `SKILL.md` (plus `scripts/` and `references/` where they earn their place) following `references/skill-authoring.md`. Keep `SKILL.md` lean and action-oriented; push depth into references. The `description` frontmatter must carry real trigger phrases so the skill actually fires. Where the video demonstrates deterministic commands, encode them as a script rather than prose.

### 6. Verify it works — do not skip
A skill that was never exercised is a draft. Verification is **two distinct layers** — do both.

**6a — Structural check (automated):**
```sh
python3 <this-skill>/scripts/validate_skill.py <path-to-new-skill>
```
Checks frontmatter validity, structure, and that any bundled scripts parse / respond to `--help`. Passing this is necessary but **not** sufficient — it does not prove the skill is followable.

**6b — Rehearsal (the actual proof):** spawn a *fresh* subagent given **only** the new `SKILL.md` + a realistic test task (not the digest, not your procedure spec), and confirm it follows the procedure to a correct result. (No subagent capability? Start a clean, separate session with only the new skill loaded and run the test task there — the point is a fresh context that has *only* the skill to go on.) If it stumbles, the skill is underspecified — revise and re-rehearse. See `references/validation-checklist.md`.

## Guardrails
- Public / owner-shared videos only; you're extracting a *procedure*, not re-hosting the footage.
- Don't bake secrets or one-off paths from the video into the skill — parameterise them.
- If transcription is unavailable (no audio, or `--frames-only`), rely on frames + on-screen text and say so in the procedure spec.

## Files
- `scripts/watch.py` — the watch engine (frames + transcript + `digest.json`).
- `scripts/install-tools.sh` — one-time toolchain installer (creates the venv at `~/.video-watch-tools`).
- `scripts/validate_skill.py` — structural validator for an authored skill.
- `references/qualifying.md` — the worth-it gate: PASS/FAIL signals + worked examples.
- `references/watching.md` — engine options (incl. capture modes) + how to read a digest.
- `references/procedure-spec-template.md` — the breakdown structure.
- `references/skill-authoring.md` — how to write a good SKILL.md + the boundary rubric.
- `references/validation-checklist.md` — the verify step in full.
