---
name: research-grounded-storyboard-pipeline
description: Internal production pipeline behind the storyboard entry point. Turns a confirmed production config into shots, keyframes, five prompt routes, generated frames, and a combined XLSX. Do not trigger this directly on a user request — the `storyboard` skill routes here after scope is confirmed. Read it when following that route, when resuming an existing `storyboard_runs/` directory, or when a caller names this pipeline explicitly.
---

# Research-Grounded Storyboard Pipeline

## Core Contract

One isolated run per request. Confirm scope, then produce: locked shots → keyframes → prompts → generated frames → workbook. Every image traces back to its keyframe, shot, prompt, world assets, evidence bindings, generator, and absolute path.

Configuration, estimates, gates, and QA stay inside the run. User-facing delivery starts with approved images and downloadable files.

## Capabilities

Load each companion skill before its first use. Skip cleanly if one is absent.

| Need | Load | If unavailable |
|---|---|---|
| keyframes, world assets | `imagegen` | run `image_generation_scope: prompts_only` |
| source research beyond local files | `web-access` | mark gaps `待核实`, stay with local material |
| the combined XLSX | `spreadsheets` (`@oai/artifact-tool`) | export CSV + Markdown, note the gap |

## Resume

An interrupted run resumes from `run.json.status`, never from scratch. Read `run.json`, `planning/production_config.json`, and the latest `qa/*.json`, then re-enter at the matching step:

| `status` | Re-enter at |
|---|---|
| `production_config` | §0 |
| `evidence_profile` | §2 |
| `bible_ready` | §4 |
| `pre_generation_ready` | §6 |
| `generating` | §6, skipping keyframes already approved in `manifests/assets.json` |
| `audit` | §7 |

Never recreate a run directory that already holds approved assets.

## 0. Confirm Production Scope

Read [production-configuration.md](references/production-configuration.md) and [quality-floor.md](references/quality-floor.md).

Determine total duration and the duration of each scene. Run `scripts/estimate_storyboard_scope.py` for `compact`, `standard`, and `detailed` when the user wants to compare.

Treat explicit user values as confirmed; infer stable values from the source and project. Present **one** compact approval line covering only the still-open fields plus the expected image count. Record everything in `planning/production_config.json` and `planning/scope_estimate.json`.

Default `image_generation_scope` to `approval_sample`. Move to `all_selected` only when the user accepts the full image count.

## 0.5 Check The Script Fits

Before any shot exists, extract the narration into segments and run:

```bash
python3 scripts/validate_script_capacity.py --script <segments.json> --run <run-dir>
```

This is arithmetic, not editing: it reports speaking rate and names the segments that hold more words than their seconds allow. A script that needs 86 seconds at a comfortable pace but has 75 does not improve by being cut into shots — every shot inherits the overload, and it only becomes visible when someone records the voice-over.

When the report says the script does not fit, say so plainly and give the two real options — cut text, or extend the running time — then stop and wait. Do not silently re-time shots to absorb it.

## 1. Start An Isolated Run

```bash
python3 scripts/init_run.py \
  --project <project-dir> --slug <short-name> \
  --duration-seconds <duration> --scene-durations <s1,s2,s3> \
  --production-depth <compact|standard|detailed> \
  --evidence-mode <strict_evidence|hybrid_evidence|fiction_consistency> \
  --bible-section characters,locations \
  --style-token "9:16竖屏,骨白/墨黑/土褐/信号红,暖侧光,中央竖轴" \
  --image-generation-scope approval_sample --approval-sample-count 5 \
  --prompt-route all --generation-confirmed --confirmed
```

`--style-token` is one short line naming the project's fixed palette, light, aspect ratio, and framing axis. Every image prompt appends it verbatim, once. Declaring it here means the style is written down in one place instead of being re-improvised in every prompt — which is what turns a whole route into one repeated sentence.

`--scene-durations` takes the real per-scene seconds. Groups, transitions, and handoffs are all planned scene by scene, so an 8s opening beside a 142s middle produces different counts than an even split — `--scene-count` alone falls back to an equal split and marks the estimate `scene_layout_exact: false`.

`--bible-section` declares the visual-bible sections this project actually needs, beyond the always-required `style` and `continuity`. Choose from `world, characters, costumes, props, locations, architecture, vehicles, creatures, materials, typography, graphics`. Declare only what the project contains — an explainer with no people declares no `characters`.

Record reference roots in `run.json`. Load previous runs only when the user selects them. Read [run-layout-and-manifests.md](references/run-layout-and-manifests.md) before writing any manifest — it holds the exact key names, and prose in this file is a summary of it, not a substitute.

## 2. Resolve Evidence And World Design

Read `../research-grounded-world-design/SKILL.md` and its [evidence modes](../research-grounded-world-design/references/evidence-modes.md).

- `strict_evidence` — reality-anchored subjects (historical, scientific, documentary, geographic, museum).
- `hybrid_evidence` — real anchors plus invented characters, events, or aesthetics.
- `fiction_consistency` — fully invented; external factual scope is zero.

Use an approved `world_design_runs/` package when one exists; create one when recurring entities still need stable IDs. Record its absolute path in `run.json.world_design_run`.

For `fiction_consistency`, register internal rules in `research/world_consistency_brief.md`.

For real entities, inventory local files first, then read [reference-first-evidence.md](references/reference-first-evidence.md) and produce:

- `research/source_register.csv` — source ID, absolute path or URL, type, reliability, usable visual facts.
- `research/truth_brief.md` — what is known and what is not.
- `research/reference_frames/` — one reference image per file.
- `research/visual_fact_cards.csv` — one row per reference-bound subject, columns per the SKILL contract, binding subject → sources → reference images → shots.

Write prompts from observable facts only: silhouette, proportions, construction, material, surface, placement, handling. Pass the reference image to the generator directly when it accepts images.

Gate R:

```bash
python3 scripts/validate_evidence_binding.py --run <run-dir>
```

A `待核实` subject keeps its shots out of generation until resolved.

## 3. Build The Visual Bible

Fill each declared `bible/<section>.md` with positive visual specifications and continuity keys. Generate setting images one subject per file.

Gate B: every recurring element has a stable world asset ID, a written specification, continuity keys, and at least one approved reference or generated image. Set `run.json.status` to `bible_ready`.

## 4. Lock Shots, Keyframes, Prompts, And Packets

Read [granularity-contract.md](references/granularity-contract.md), [shot-language.md](references/shot-language.md), [prompt-types-and-delivery.md](references/prompt-types-and-delivery.md), and [jimeng-dual-mode-prompting.md](references/jimeng-dual-mode-prompting.md).

Write, using the exact schemas in [run-layout-and-manifests.md](references/run-layout-and-manifests.md):

- `shots/shots.json` — unique IDs, continuous timecodes, one beat and one primary action each. Camera is recorded as three enumerated fields (`shot_size`, `camera_angle`, `camera_movement`) plus a per-shot `camera_note` that is never reused. On-screen text goes in `text_elements` with a `text_layer` of `generation` or `post`; anything that moves, counts, or appears during a segment is `post`, because current video generators render moving text unreliably.
- `shots/keyframes.json` — every shot gets an anchor; neighbours stay within the confirmed interval; first frame at 0 and last at exact duration.
- `shots/motion_prompts.json` — one per shot.
- `shots/transitions.json` — one per adjacent keyframe pair **within a scene**. Transitions never cross a scene boundary.
- `shots/shot_groups.json` — consecutive groups ≤ 15s with ordered `@素材` references, timed beats, and entry/exit contracts. Handoffs join neighbouring groups **within a scene**.
- `prompts/prompt_manifest.json` — one canonical entry per prompt.

Then build the production packets — they are derived from the locked shot list and must exist before validation:

```bash
python3 scripts/make_agent_packets.py --run <run-dir>
```

Set `run.json.status` to `pre_generation_ready`, then run Gate S:

```bash
python3 scripts/validate_pre_generation.py --run <run-dir>
python3 scripts/validate_video_prompt_plans.py --run <run-dir>
python3 scripts/validate_prompt_package.py --run <run-dir>
```

`validate_pre_generation.py` reports the distribution of the three camera fields. It never fails on distribution — a montage may legitimately repeat — but when one value covers more than 60% of shots, surface it and ask whether that is the intent.

`validate_prompt_package.py` fails when more than 60% of one route's prompts end with the same thirty characters, or when this skill's own acceptance wording appears inside a prompt. Both mean the same thing: the writing stopped and the template took over. Fix by moving shared style into `style_token` and rewriting the unique part, not by shuffling words.

## 5. Plan Versions

Create a version only when the visual thesis, factual basis, or shot plan changes materially. Record it in `versions/version_manifest.json`; move rejected versions to `garbage_pile/`. Keep prompt and asset IDs stable within a version.

## 6. Generate And Register Frames

Keep the main agent responsible for research synthesis, schema ownership, continuity, integration, and export. Process packets sequentially unless the user authorizes parallel work — then read [multi-agent-orchestration.md](references/multi-agent-orchestration.md).

For each selected keyframe:

1. Read its record, parent shot, bible entries, world asset IDs, and evidence bindings.
2. Build the prompt from the shot record and bible entries only — **do not read previously written prompts**. Write what differs from the previous keyframe, then append `style_token` verbatim once. Sound never enters an image prompt.
3. Load every bound reference image and generate one complete image.
4. Save to `frames/<scene>/<keyframe-id>__v001.png` and append its asset record immediately.
5. Inspect it before advancing.
6. Compare real entities against their fact cards, invented ones against their design cards. Record every comparison in `qa/reference_fidelity.csv`.

Generate declared handoff anchors as complete images with `slot: handoff`, bound to both adjacent groups. Replacements increment the version; earlier versions move to `garbage_pile/asset_versions/`.

## 7. Integrate And Audit

```bash
python3 scripts/validate_shot_manifest.py --run <run-dir>
python3 scripts/validate_evidence_binding.py --run <run-dir> --require-fidelity
python3 scripts/audit_images.py --run <run-dir>
python3 scripts/build_asset_index.py --run <run-dir> --title <title>
```

Review every duplicate candidate visually — `near_duplicate_pairs` blocks the gate, `review_candidates` is advisory. Regenerate one member of each confirmed pair with a distinct camera position, scale, action, or temporal state. Repeat until zero missing shots, zero exact duplicates, and zero confirmed near-duplicates.

## 8. Export

Load the `spreadsheets` skill and follow the workbook contract in [prompt-types-and-delivery.md](references/prompt-types-and-delivery.md). Sheets in order: `关键帧图文`, `逐镜分镜`, `图生视频提示词`, `智能多帧`, `全能参考`, `世界资产`, `制作配置`, `QA`. Open on `关键帧图文`; mark the last two as internal control sheets.

Embed approved thumbnails. **Write each original absolute path as visible cell text**, not only as a hyperlink target — the delivery check reads both, but visible text is what survives a copy-paste into another tool.

Deliverable hygiene, all of which has gone wrong in practice:

- ASCII-safe filenames — no full-width punctuation such as `：` in any exported name.
- Keep the `__v001` version suffix on full-resolution frames so they match the asset index.
- Exactly one asset index. Pass `--title` so the file is `<title>_asset_index.csv` and no second copy appears.
- No internal inspection or scratch files in `deliverables/`.
- The config sheet records `evidence_mode`, `style_token`, scene durations, and the planned-versus-actual shot count with no contradiction between them.

Export to `deliverables/`: `<title>_storyboard_prompts.xlsx`, `<title>_fullres_frames/`, `<title>_asset_index.csv`, `<title>_prompts.md`, `<title>_prompt_manifest.json`. Store QA at `qa/<title>_qa_report.md`.

```bash
python3 scripts/validate_combined_workbook.py --run <run-dir> --workbook <xlsx-path>
```

## Completion Report

Lead with the completed image count and delivery path. Then shot count, keyframe count, five prompt-route counts, workbook path, one quality status line. Keep estimates, gate records, and audit counts in the run; surface them on request.
