---
name: bootstrap-game-project
description: "Use when starting a new game project or resuming an existing one to collect design specs and cascade downstream."
---

## 1. Overview

Orchestrator: collects Title/Genre/Core gameplay, delegates each spec via `task()`, runs alignment audit, proposes cascade.

## 2. Quick Reference

| Phase | Artifact(s) | Key Skill |
|-------|-------------|-----------|
| 0 | Resume check / config | — |
| 1 | game_genre.md | Ask title/genre/core gameplay |
| 2–7 | game_loop.md, screen_flow.md, raw_rules.md, system_roster.md, input_mapping.md, visual_style.md, localization_keys.md | Delegate via `task()` |
| 8 | Alignment audit | verify-spec-alignment |
| 9 | Project Charter | Present summary, get approval |
| 10 | Downstream specs | cascade-compile |
| 11 | Handoff | Propose /pipeline-orchestrator |

Rules: synchronous (`run_in_background=false`), one question per turn, delegate exclusively via `task(load_skills=["..."])`.

## 3. Execution Flow

| Phase | Artifact | Method |
|-------|----------|--------|
| 0 | Resume check | Read config, glob |
| 0b | `.game-dev-config.json` | Ask folder |
| 0c | `rendering_target.md` | `define-rendering-target` |
| 1 | `game_genre.md` | Ask one at a time |
| 2 | `game_loop.md` | `define-game-loop` |
| 2b | `screen_flow.md` | `define-screen-flow` |
| 3 | `raw_rules.md` | `define-game-rules` |
| 4 | `system_roster.md` | `define-game-systems` |
| 5 | `input_mapping.md` | `define-player-controls` |
| 6 | `visual_style.md` | `define-visual-style` |
| 7 | `localization_keys.md` | `define-localization-key` |
| 8 | Alignment audit | `verify-spec-alignment` |
| 9 | Project Charter | Present summary, get approval |
| 10 | Technical cascade | `cascade-compile` |
| 11 | Handoff | Propose `/pipeline-orchestrator` |

## 3. Phase 0 — Resume Check

Read `.game-dev-config.json` → `specs_dir`. If missing, skip to Phase 4. If config exists, glob `.md` files, present progress (e.g., "✅ game_genre.md, ❌ raw_rules.md"), ask to resume. **"yes"** → skip to first missing spec. **"no"** or missing → Phase 4.

Write `.game-dev-config.json` in current working directory:
```json
{ "target_folder": "{user_provided_path}", "specs_dir": "{user_provided_path}/docs" }
```

**Done:** `.game-dev-config.json` written AND target folder exists. If resuming, first missing spec identified.

## 4. Phase 1 — Ask Questions & Delegate Specs

Ask three questions sequentially via `question` tool:

```
Q1: "What's the game title?"
Q2: "What genre? (RPG / FPS / RTS / Platformer / Action / Adventure / Puzzle / Strategy / Simulation / Racing / Sports / Fighting / Horror / Roguelike / Visual Novel / Other)"
Q3: "What's the core gameplay? (1-2 sentences)"
```

After Q3, write `{TARGET_FOLDER}/docs/game_genre.md`.

Delegate each spec via:
```
task(category="unspecified-high", load_skills=["<skill>"], prompt="<context>. Generate {TARGET_FOLDER}/docs/<output_spec>.")
```

| Phase | Skill |
|-------|-------|
| Platform & Engine | `define-rendering-target` |
| Gameplay loop | `define-game-loop` |
| Screen flow | `define-screen-flow` |
| Game rules | `define-game-rules` |
| Game systems | `define-game-systems` |
| Player controls | `define-player-controls` |
| Visual style | `define-visual-style` |
| Localization | `define-localization-key` |

**Done:** All user specs generated via delegation AND each spec file exists in `{TARGET_FOLDER}/docs/`.

## 5. Phase 2 — Alignment Audit

```
task(category="unspecified-high", load_skills=["verify-spec-alignment"], prompt="Verify cross-spec consistency for all specs in {TARGET_FOLDER}/docs/. Report drift.")
```

**Done:** Audit result received — zero ERRORs; WARNINGs acceptable (proceed but flag).

## 6. Phase 3 — Project Charter

Present summary (Title/Genre/Core Gameplay, all user specs, audit result), ask approval. **yes** → Phase 7. **no** → ask which specs to revise.

**Done:** Summary presented AND user explicitly confirmed ("yes"). If "no", revision targets identified before proceeding.

## 7. Phase 4 — Technical Cascade

```
task(category="unspecified-high", load_skills=["cascade-compile"], prompt="Cascade-compile downstream core specs from user specs in {TARGET_FOLDER}/docs/.")
```

**Done:** All downstream core specs regenerated via `cascade-compile` AND results summarized (count of specs generated, any failures reported).

## 8. Rules

* **Phase 0**: Check progress first. **ASK ONCE**: STOP after each question. **SEQUENTIAL**: Advance one phase at a time.
* **SYNCHRONOUS**: Set `run_in_background=false`. After `task()`, response ENDS. Present results only.
* **MUST** use `task(load_skills=["..."], prompt="...")` — delegate to sub-skill logic exclusively.

## 9. Red Flags

Running resume check first · Asking one question at a time · Delegating to sub-skill logic exclusively via `task()` · Running alignment audit before charter · Always including `load_skills` in every delegation

## 10. Execution Command

`/bootstrap-game-project`
