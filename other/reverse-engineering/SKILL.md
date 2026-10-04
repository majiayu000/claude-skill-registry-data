---
name: reverse-engineering
description: Use when asked to bootstrap a project's docs/ set or reverse-engineer an existing codebase into that set.
---

# mak:reverse-engineering — Project Analysis into the Doc Set

Bootstraps the project's `docs/` from the bundled template set at
`${CLAUDE_PLUGIN_ROOT}/skills/reverse-engineering/assets/project_docs/`,
then fills it by analyzing the codebase — recording the facts observed in the code.

The set's own rules live inside it:

- `project_docs/00.INDEX.md` — structure, per-topic SSOT, frontmatter conventions, content rules, domain / process registries (the rulebook)
- `project_docs/CLAUDE.md` — the analysis procedure (how to execute the rulebook)

This skill orchestrates: copy → analyze/fill → template cleanup. The two files above are the SSOT for everything else — follow them, don't restate them.

The set is one fixed composition — core documents `00`–`06` plus the unnumbered `domains/` (one file per feature domain) and `processes/` (one file per traced scenario) folders, each with a `_template.md` copy source. Templates are in English. Fill content in the user's language (or the project's documented language policy), keeping the structure.

## Procedure

### 1. Confirm target and state

- Confirm the project root (default: current working directory).
- Check for existing guide documents — `docs/` content, plus obvious guide files elsewhere (e.g. a root-level ARCHITECTURE/CONTRIBUTING guide). If any exist, list them and **confirm with the user whether to merge** (merge / copy only missing files / abort). **Never overwrite an existing document without reading it first.**
- **On merge, this skill's doc-set format is the baseline** — migrate the existing documents' content into the set's structure (per-topic SSOT, numbering, frontmatter per `00.INDEX.md`), not the other way around. For projects with a mature `docs/`, recommend "copy only missing files" as the lower-impact default. **Before executing a merge, present the plan first**: which files will be created/changed and which originals become superseded — proceed after confirmation. Facts already written in the existing guides are treated as source material for step 3 (verify against code before carrying over; unverifiable claims become `_(TODO)_`). After migration, list the superseded originals and let the user decide whether to archive or delete them — do not delete on your own.

### 2. Copy the set

- Copy the whole set from `${CLAUDE_PLUGIN_ROOT}/skills/reverse-engineering/assets/project_docs/` into `<project>/docs/`.
- Copy `domains/` and `processes/` **recursively** (each holds its `_template.md` — copying only top-level `*.md` loses them).
- If the project has no `README.md`, offer `${CLAUDE_PLUGIN_ROOT}/skills/reverse-engineering/assets/README.template.md` as an optional starting skeleton (separate decision; skip silently if the user doesn't want it).

### 3. Analyze and fill

Follow `docs/CLAUDE.md` §2 (single flow and fill order — SSOT there, not restated here; scenarios go to `processes/<name>.md`, feature domains to `domains/<name>.md`, each via its `_template.md`).

**Delegation** — if the `mak:analyzer` agent is in the available agent list, delegate the analysis/filling to it in batches, following `docs/CLAUDE.md` §2's order. Pass each batch: the project root, the assigned document list, a pointer to `docs/00.INDEX.md` + `docs/CLAUDE.md` as the rulebook, and the output language. Keep interactive decisions (merge confirmations, ambiguous conventions needing user input) in the main thread, and apply the cross-document syncs (`00.INDEX.md` registries, `related_to` symmetry) that analyzer reports back. If analyzer is unavailable, fill directly.

Batches may be delegated in parallel, but only after the fill order and cross-document dependencies are respected, only among batches that have no dependency on each other, and only when their assigned document sets do not overlap — two batches writing the same document collide. A workable split: **A** `processes/` + `02` + `05` first (the trace grounds the structure documents) → **B** `01` §1–§4 + `03` and **C** `04` + `06` in parallel → **D** `domains/` + `01` §5–§6 after A, B, and C (domains are discovered while tracing; `01`'s Change Checklist and Troubleshooting link into `03`/`04`/`06`).

Hard rules while filling (SSOT: `docs/CLAUDE.md` §1):

- Record observed **facts (is)**, not aspirations; unverified cells get `_(TODO — <what's needed>)_`, never guesses.
- Respect per-topic SSOT — one home per topic, links elsewhere.
- Keep frontmatter `type` / `related_to` symmetric per the INDEX rules.
- No time-stamped status anywhere in the set.

### 4. Template cleanup + verification

Run the cleanup and the completion checklist exactly as defined in `docs/CLAUDE.md` §2 step 4 and §4 (remove `> Template:` blocks except in `CLAUDE.md`/`_template.md`, remove the INDEX intro and example registry rows, prune the stack table, no unreplaced `<...>`, grep check zero hits).

### 5. Report

Summarize: files created, docs filled vs left `_(TODO)_`, improvement observations noted while tracing (listed here only — never written into the set), and suggested next steps (e.g. fill remaining TODOs; if the user wants a roadmap, `mak:roadmap-planning` creates it as a separate document outside the set).

## Cautions

- This skill writes **documents only** — no source-code changes.
- Large analysis can be staged: agree with the user on which docs to fill this session and record the rest as `_(TODO)_`.
- Do not run git commit/push unless the user explicitly says "commit"/"push".
