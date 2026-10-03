---
name: skill-build
description: Designs and builds a new Claude Code skill folder from a blank page in your own house style, surveying existing skills for overlap, interviewing, getting the design approved, then building and validating it with a preflight script. Use when the user wants to build, create, make, scaffold, or engineer a new skill. Not editing or auditing an existing skill (a hand-edit or skill-audit), publishing one, or general prompt writing.
when_to_use: Use when the user asks to build, create, make, scaffold, or engineer a new skill from scratch. It differs from skill-audit, which reads recent sessions and existing skills to recommend changes and never writes; skill-build writes a new skill folder and hands off to skill-audit once the skill is in use.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, Skill, WebSearch, WebFetch
argument-hint: [skill purpose, or leave blank to be interviewed]
---

# Skill Build

Design and build a complete new skill from a blank page, in your own house style. The skill lifecycle is **build (this skill), then audit ([`skill-audit`](../skill-audit/)), then publish (your publishing step, if you share skills)**; this skill owns the build stage and hands off to the next.

Adapted from `skill-engineer-master` by Antony Evans (edge-brain-lite, https://github.com/antonyevans/edge-brain-lite, CC BY 4.0). Modified: decoupled from the edge-brain research and persistence layer and the public skill marketplaces, re-targeted to a house style the builder records from your own existing skills, and the always-mandatory evals, Gotchas, learnings, and edge-cases requirements demoted to recommendations.

## What this builds

A skill folder under `~/.claude/skills/<name>/` that matches how your existing skills are built: frontmatter Claude Code actually reads (`name`, `description`, and usually `when_to_use`), numbered steps with their reasoning, reference files one level deep, scripts only for genuinely mechanical steps, and the conditional sections your skills use (a session log, an independent audit agent, a writing-voice prerequisite, a report-only contract). Read `references/house-style.md` for the house-style spec and `references/skill-design-framework.md` for the design principles.

## Phase 0: Survey the existing suite (do this first, always)

Before designing anything, check whether a skill for this already exists or whether an existing skill should be extended instead of adding a new one. Weight the merge instinct heavily; do not entrench a needless separation.

1. List `~/.claude/skills/`, and read your skill index if you keep one.
2. Grep the skill descriptions and the closest one or two SKILL.md files for the proposed capability.
3. If an existing skill already covers it or substantially overlaps, **stop and recommend extending that skill** rather than building a new one. Present the finding and ask before proceeding.
4. **If `references/house-style.md` has not been filled in yet**, fill it in now: read three to five of your existing skills and record their conventions under that file's section headings. Every later phase reads it.

WHY: a duplicated or near-duplicated skill drifts from its twin and creates routing ambiguity. The cheapest skill is the one not built. And a house style inferred once from real skills beats one guessed at on every build.

## Phase 1: Intake

Ask only the questions whose answers change the design. Skip any already answered.

1. **Task**: what workflow should this skill execute, in one sentence.
2. **Trigger**: what user input should activate it, and what should NOT (the negative cases).
3. **Tools and connectors**: what MCPs, APIs, or scripts it needs; any navigation notes.
4. **Human-in-the-loop points**: where a human must approve, choose, or verify before the skill continues.
5. **Output**: what a successful run produces (artifact type, format, destination).
6. **Failure baseline**: what Claude does wrong on this task today without a skill. If unknown, predict the failure modes now and verify them in Phase 4.
7. **Frontmatter choices**: does it pin `model`/`effort` (ask once; the default is to inherit the session model), and who may invoke it: both the user and the model (default), the model only (`user-invocable: false`, for a helper other skills call), or the user only (`disable-model-invocation: true`, for a skill that sends, publishes, or deletes; see the shorthand caveat in `references/house-style.md` section 3).

## Phase 2: Design (present, get approval before any writes)

Read `references/skill-design-framework.md` and `references/house-style.md`. Work through the design and present a full summary for approval. Build nothing until the design is approved: present, then wait.

Cover in the design summary:
- **Identity:** the name, the single-line description, and the `when_to_use` sentence. Invest most of the effort in the description; it is the routing signal that decides whether the skill fires. Draft it, and any internal agent prompts, with a prompt-writing step (a prompt-writing skill if you have one). The description names the artifact, uses outcome language for triggers, includes negative triggers, and stays on one line.
- **Output contract:** what it produces, what it does not, what it enables, and what consumes the output next.
- **Process steps:** each step with its reasoning principle, not just the procedure, so the skill generalizes past the cases you foresaw.
- **Script inventory:** classify every step as reason or execute. Ship a script for each execute step (an HTTP or API call, a repeatable file transform, a loop over more than about three items, an exact-format output, a credential touch, a schema or rubric check, or a state append). Start scripts from `scripts/archetypes/`. List the scripts in a table.
- **Conditional sections (from `references/house-style.md` section 3):** a session log section if the skill does project-folder work; an **independent audit agent** step if the skill produces rendered or quality-sensitive output (used in place of an evals folder); a writing-voice prerequisite if the skill produces prose in your voice (if you have no voice layer yet, create one first; see [`writing-voice-guide`](../writing-voice-guide/)); a report-only contract if the skill is advisory. If the skill creates, populates, or writes rules into a project folder, apply `references/house-style.md` section 9 as well.
- **Recommended, not mandatory:** offer a `## Gotchas` section (at least two real symptom, cause, and fix entries) and a small `evals/evals.json`. Both are good practice; recommend them, do not force them.

## Phase 3: Build

Generate the folder following `references/house-style.md`. Use the prompt-writing step for the description and any agent prompts. Keep SKILL.md a routing layer (steps and pointers); push dense rules, templates, and domain knowledge into `references/`, one level deep. Ship the scripts from the inventory, started from `scripts/archetypes/`. Copy `assets/skill-template.md` as the SKILL.md skeleton.

## Phase 4: Validate

Two steps:
1. Run the preflight script and fix every hard fail:
   ```
   python3 ~/.claude/skills/skill-build/scripts/preflight.py ~/.claude/skills/<name>
   ```
   It hard-fails on the invariants a skill needs to load and be read: SKILL.md present, `name` matches the directory, a single-line non-folded description at most 1536 characters (the point where the skill listing truncates silently), SKILL.md at most 500 lines, no nested reference chains, and no CHANGELOG.md in the skill root. It warns (does not fail) on a description over 500 characters, a missing negative trigger, a missing `when_to_use`, a `triggers:` or `category:` key Claude Code does not read, a body over 150 lines, a missing `## Gotchas`, and a README.md in the skill root. An optional name-prefix warning is off by default; `scripts/preflight.py` explains how to turn it on.
2. Run the semantic checklist the script cannot judge: read `references/preflight-checklist.md` and apply it.

## Phase 5: Register routing (approval gate)

A new skill is not done until it is discoverable. Most skills need nothing here, because the description is the routing signal and reaches every session on its own. Editing `~/.claude/CLAUDE.md` changes always-loaded global context, so any edit to it is a hard approval gate, not an automatic step.

1. If you keep a routing table in your CLAUDE.md, draft a row only where the description cannot carry the routing: a command word you type, a tie-break with a neighboring skill, or a default.
2. If you keep a skill index, add the new skill the way that index is maintained. If the index is generated from frontmatter, set the field it reads and regenerate it; never hand-edit a generated index, because the next regeneration wipes the row. `references/house-style.md` section 7 has the checklist.
3. Present every diff verbatim and wait for explicit approval. On approval, apply them.
4. Consider a headless variant only if the skill is meant to run unattended in batch.

## Phase 6: Test and hand off

Give the user a cold-start test plan: a fresh session with the skill installed runs it on two or three real tasks while the user watches for files read in the wrong order, missed references, or an overused section. Then offer the handoff: [`skill-audit`](../skill-audit/) to review it against recent friction once it has been used, and your publishing step if you share an anonymized version.

## Gotchas

- **Symptom:** the new skill never fires; the user has to name it by hand. **Cause:** a timid or vague description, the default undertriggering failure. **Fix:** rewrite the description to name the artifact in the outcome language a request would use. Widen it by naming what it covers, not by lengthening it, and add the negative triggers that keep the widening from stealing a neighboring skill's requests; in a large suite, a wrong fire costs what a missed fire costs.
- **Symptom:** the description renders on two lines and the skill behaves erratically. **Cause:** a multi-line or YAML-folded description; Claude reads only the first line. **Fix:** keep `description:` a single flat line, never `description: >`. The preflight script hard-fails this.
- **Symptom:** trigger phrases were written down but the skill still does not fire on them. **Cause:** they were put in a `triggers:` key, which Claude Code never reads. **Fix:** move every phrase that must route into `description`. The preflight script warns on a `triggers:` key.
- **Symptom:** the built skill works but does not look like the rest of your suite (no session log, no audit agent, no voice prerequisite). **Cause:** the generic template was followed instead of the house style. **Fix:** apply the conditional sections in `references/house-style.md` for the skill's type before shipping.
- **Symptom:** a near-duplicate of an existing skill ships and the two drift apart. **Cause:** Phase 0 was skipped. **Fix:** always survey the suite first; recommend extending the existing skill when one overlaps.

## Rules

- Never write skill files before the Phase 2 design is approved (the new skill's files; filling in `references/house-style.md` in Phase 0 is exempt).
- Never auto-edit `~/.claude/CLAUDE.md`; present the diff and wait (Phase 5). Never hand-edit a generated skill index; set the field it reads and regenerate.
- Never put domain knowledge, style guides, or long examples in SKILL.md; use reference files one level deep.
- Default to inheriting the session model; pin `model`/`effort` on the new skill only when the user asks.
- Ship a script for every execute step; argue the case in one sentence if a step that looks mechanical is genuinely reason-not-execute.
- Carry the CC BY 4.0 attribution into any skill adapted from third-party material, and wire your writing-voice prerequisite into any skill that produces prose in your voice.
- Deletion is a valid outcome: if a workflow is retired, remove its skill rather than leave it to misroute.
- **Never put a real client organization or a real private person into a skill, anywhere, including fixtures, test data, code comments, and a rule's stated provenance. Examples and fixtures are fictitious.** Public companies that are the subject of a teaching case, and published authors cited as sources, are not covered by this and stay; the rule is about paid engagements and people who are not public figures. **The way this gets broken is rarely by typing a client name on purpose.** It happens by building a fixture from a real delivered artifact, or by justifying a rule with the incident that produced it and naming the engagement. Both are natural, and both embed the client in the skill.
