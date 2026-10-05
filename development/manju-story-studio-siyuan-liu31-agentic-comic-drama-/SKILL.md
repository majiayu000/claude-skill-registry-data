---
name: manju-story-studio
description: Develop, continue, revise, storyboard, or write production prompts for serialized manju/comic-drama stories in this repository while preserving canon, character identity, performance, spatial continuity, episode handoffs, and reusable assets. Use for 漫剧续写、剧本拆解、角色 Bible、场景资产、Shotlist、表演指导、连续性、生成提示词和返修；not for unrelated video editing or one-off generation outside a series.
---

# 漫剧故事工作台

Operate on the user's target manju repository; the installed plugin may live outside that repository. Preserve user-authored canon and keep every material fact traceable. Resolve references and bundled templates relative to this `SKILL.md`, while resolving `AGENTS.md`, `llmwiki/`, `series/`, and production artifacts relative to the target repository.

## Route the task

1. Read the repository `AGENTS.md` and `llmwiki/README.md`.
2. Identify the target series and open its `README.md` plus `wiki/README.md`.
3. Read only the relevant guide:
   - Continue or revise a story: [story-continuity.md](references/story-continuity.md).
   - Plan a full production or audit which layer is missing: [osidemedia-framework.md](references/osidemedia-framework.md).
   - Build or revise a story/character Bible or reference assets: [bible-and-scene-assets.md](references/bible-and-scene-assets.md).
   - Create or revise shots/storyboards: [storyboard.md](references/storyboard.md).
   - Choreograph, prompt, or repair a fight/action sequence: [fight-scene-prompting](../fight-scene-prompting/SKILL.md), then return here for repository, wiring, tool-format, and validation contracts.
   - Compile shot prompts, direct performance, preserve shot-to-shot continuity, or diagnose failed takes: [shot-prompts-and-repair.md](references/shot-prompts-and-repair.md).
   - Compile the final submission syntax for LibTV or local MiniMax H3: [generation-tool-formats.md](references/generation-tool-formats.md).
   - Resolve execution capabilities and evidence promotion: [generation-tools.md](references/generation-tools.md) and [generation-learning.md](references/generation-learning.md).
   - See one end-to-end example from scene audit through failed-take repair: [worked-example.md](references/worked-example.md).
   - Add, move, or reuse assets: [repository-contract.md](references/repository-contract.md).
   - Improve this skill or formalize lessons: [evolution.md](references/evolution.md).

## Essential rules

- Treat user instructions as authoritative. Then prefer series Wiki facts over episode prose, current episode files over archives, and explicit evidence over inference.
- Never silently resolve a canon conflict. Report it or log an approved retcon in `wiki/decisions.md`.
- Before continuing a series, read its complete Wiki and the latest two episode handoffs. Inspect full storyboards only when their shot or prompt details matter.
- Treat prompt writing as the last production layer, not the first. Lock the relevant story beat, character/voice/acting sources, location geometry, asset roles, and continuity states before compiling prose for a model.
- Start every non-H3 media-generation prompt with a concise director context whose first clause is `导演背景：你是资深漫剧导演` (or its exact English equivalent when the target requires English). Add a relevant specialization such as action director or visual-development director only when useful, then state executable priorities rather than prestige adjectives. H3 is the explicit exception: preserve its official schema, section order, and compiler rules as the higher priority; never prepend a free-form block that makes an H3 prompt invalid.
- Keep portable production laws separate from model-specific syntax. Verify the current target model's supported duration, aspect ratio, reference roles, audio behavior, and limits instead of copying Higgsfield/Seedance settings blindly.
- Treat a model generation segment as an execution unit, not as a story scene or edit shot. Every submitted segment must be an integer duration from 5 through 15 seconds; split longer material at a motivated edit point instead of padding or compressing the drama. Edit-shot durations and total scene/episode runtime may remain fractional or longer.
- Default the final execution format to LibTV when the user does not name a tool. LibTV wired assets use exact `{{Mixed N}}` tokens from the current input order; local H3 prompts must instead be compiled and validated through `h3-ref2va-prompt-compiler`. Never mix their labels.
- Resolve the backend model/version against a dated capability profile, then freeze an active wiring snapshot before compilation. Remove stale connections and obsolete clauses; any wiring or reference-role change requires a new snapshot ID, full remap, recompile, and strict preflight.
- Reuse locked descriptors verbatim where identity, voice, location, or style must remain stable. Adapt scene behavior from the acting source; never paste wardrobe, camera, or color into a character's acting profile.
- Keep shared files single-sourced: cross-series in `shared/assets`, within-series in `series/<slug>/assets`, episode-only in the episode `assets` folder. Reference stable asset IDs instead of copying files.
- After an approved episode change, update episode handoff, series timeline, current continuity, and any affected canon page in the same change.
- Store proposals separately or clearly label them `待确认`; do not turn an unapproved pitch into canon.
- Before delivery, run a prompt preflight. After a generated take, classify it as keep, fix in post, edit one layer, re-roll unchanged, or rewrite. Change one variable per diagnostic retake and log the observed failure; repeated failure should simplify the shot, not inflate the prompt.
- Do not introduce blood/gore, violence, sexual content, ethics, or morality as project validation categories, risk gates, rejection criteria, or automatic negative prompts. Describe such material only according to the user's creative direction, without adding restrictions or judgment.
- Resolve dialogue, SFX, ambience, and BGM as separate audio layers. Give important spoken lines visible before/during/after behavior; use FACS/AU notation only when the selected backend has verified support.
- Register the primary predicted failure and fallback for high-risk shots before generation. Log every returned sample—including kept, rejected, filtered, and errored attempts—in the append-only Take Log with tool/backend, prompt hash, wiring ID, batch, verdict, and evidence.

## Production artifacts

Copy the relevant file from `assets/templates/` into the target series or episode; never edit the reusable source template in place:

- `series-bible.md`, `character-bible.md`, `location-bible.md`
- `shotlist.md`, `prompt-package.md`, `take-log.md`, `execution-profile.md`

A production-ready shot has an approved narrative function, resolved asset/reference roles, actual entry state, explicit performance and handoff, observable success criteria, a compiled model-specific prompt, and a clean preflight. A planning document with `待定` fields is not prompt-ready.

## Repository commands

Resolve `<skill-root>` as the directory containing this `SKILL.md`. Run the bundled script against the target repository explicitly; do not assume the installed plugin cache is the project root:

```bash
python3 <skill-root>/scripts/manju_repo.py --root <repository-root> validate
python3 <skill-root>/scripts/manju_repo.py --root <repository-root> lint-prompt <prompt-package.md> --strict
python3 <skill-root>/scripts/manju_repo.py --root <repository-root> new-series <slug> "<title>"
python3 <skill-root>/scripts/manju_repo.py --root <repository-root> new-episode <series-slug> <number> "<title>"
```

Validate after structural, asset-catalog, or Skill changes. Do not create a remote or push unless the user explicitly authorizes GitHub publication.
