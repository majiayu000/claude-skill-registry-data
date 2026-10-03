---
name: translate-visual-novel
description: "Translate and localize complete visual novels, Galgames, and Ren'Py/KiriKiri-style narrative games for an explicit source and target locale. Use for projects that need engine and archive research, terminology and character voice, scene-level translation, independent review, lossless reinsertion, font work, repacking, playtesting, or recovery of an interrupted localization project. Do not use for an ordinary short translation or a runtime OCR overlay."
---

# Visual Novel Translation Pipeline

## Core model

Keep one coordinator responsible for the authoritative project state, research synthesis, source extraction, job boundaries, terminology decisions, merges, repacking, and delivery. Delegated agents may translate or review bounded jobs, but they do not own global state.

Persist the entire project in the workspace rather than relying on conversation memory. Treat the original game directory as read-only and perform work in separate staging, build, and release directories.

Use the current Codex session and its native agents for translation. Do not silently route the text through an unrelated external translation service.

## Start or resume

1. Confirm the exact game version, source locale, target locale, working directory, platform, and desired patch form.
2. For a new project run `scripts/init_project.py` with `--source-locale` and `--target-locale`. For an existing project read `run-state.json`, `planning/jobs.jsonl`, and the latest QA reports before doing new work.
3. Run `scripts/build_manifest.py` to create a SHA-256 inventory of the source files.
4. Read [workflow-and-state.md](references/workflow-and-state.md) and advance only from the last evidenced stage.
5. Record changes to facts, terminology, prompts, schemas, and source scripts; mark affected jobs instead of silently replacing decisions.

## Required pipeline

1. Register the exact release and inventory the source.
2. Research extraction, reinsertion, and repacking for that exact version.
3. Identify the engine and prove an untranslated round trip on a copy.
4. Extract text losslessly with stable IDs, hashes, speakers, routes, scenes, and control-token metadata.
5. Research engine facts, canon, relationships, knowledge state, and character voice without restricting source languages.
6. Research names, terminology, style, punctuation, and audience expectations specifically in the selected target locale.
7. Translate and review a representative calibration scene, then freeze the first Bible version.
8. Review the jobs suggested by `scripts/plan_jobs.py` and adjust boundaries according to scene dependencies.
9. Give each translation job a complete scene context and a frozen language-pair profile; use a separate agent for review when agents are available.
10. Adjudicate proposals centrally, materialize approved translations, and run automated QA.
11. Reinsert, repack, launch when authorized, play relevant routes, and build the patch.

## Read references when needed

- Project setup or recovery: [workflow-and-state.md](references/workflow-and-state.md).
- Online canon, engine, or target-locale research: [community-research.md](references/community-research.md).
- Extraction, reinsertion, or repacking: [extraction-and-repacking.md](references/extraction-and-repacking.md).
- Missing glyphs, fallback fonts, shaping, or runtime font selection: [font-runtime.md](references/font-runtime.md).
- Prompt preparation or translation: [translation-contract.md](references/translation-contract.md).
- Job planning and delegation: [subagent-orchestration.md](references/subagent-orchestration.md) and [shared-prefix-and-batching.md](references/shared-prefix-and-batching.md).
- Review, merge, playtest, or release: [qa-and-release.md](references/qa-and-release.md).

## Language-pair configuration

- Store BCP 47-style `source_locale` and `target_locale` values in `project.json`.
- Complete `bible/language-profile.md` before calibration. Define target punctuation, register, address forms, transliteration, names, casing, spacing, line breaking, and any source-language risks.
- Keep universal rules in the translation contract and project-specific language choices in the frozen language profile.
- Do not claim that a script or font engine supports a writing system until the actual game renders it correctly. Cmap coverage alone does not prove shaping, bidirectional layout, or line breaking.

## Delegated agents

- When agents are available, research engine evidence, canon and voice, and target-locale conventions as independent evidence lanes.
- For long coordinator histories, create a clean seed without the full parent conversation. Load the stable shared prefix in a fixed order, then dispatch related translation or review jobs from that seed.
- The shared prefix contains the contract, language profile, world rules, complete character and voice data, terminology, address policy, route knowledge, approved examples, and frozen decisions. Job-specific content comes afterward.
- Split oversized scenes by natural subscene. Every source ID has exactly one primary chunk; overlap is read-only context and must never be emitted twice.
- Give each agent exclusive output paths. Translation and review agents never edit final game scripts or the global Bible directly.
- Validate each returned batch immediately. If agents are unavailable, execute the same jobs sequentially without changing the output contract.

## Included helpers

- `init_project.py`: initialize a recoverable locale-aware project.
- `build_manifest.py`: hash the read-only source.
- `audit_project.py` and `set_stage.py`: validate and advance project stages.
- `plan_jobs.py`: propose scene-aware jobs for coordinator approval.
- `build_shared_prefix.py`: build a deterministic, content-addressed shared prefix.
- `record_cache_probe.py`: record best-effort cache observations when host usage data exists.
- `build_context_bundle.py`: generate compact job views, chunk plans, and coverage proofs.
- `set_job_status.py`: update job state atomically.
- `validate_translation.py`: validate IDs, hashes, protected tokens, locale-aware residual scripts, length ratios, and terminology.
- `apply_review_delta.py`: verify and materialize sparse independent-review deltas.
- `audit_font_coverage.py`: audit static Unicode coverage in the fonts intended for release.
- `merge_jobs.py`: merge approved jobs before global QA and reinsertion.
- `locate_garbro.ps1`: locate a user-provided GARbro installation when appropriate.

## Completion

Declare completion only when research is traceable, the untranslated round trip passed, every source unit has a stable ID, planned translations are approved, automated QA has no unresolved errors, repacking succeeds, target text renders with the intended fonts, the game launches, relevant routes and choices were exercised, and the patch contents and checksums are recorded. Report untested routes and remaining warnings.
