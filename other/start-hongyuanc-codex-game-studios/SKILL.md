---
name: start
description: Use when a first-time user needs project-state detection and guidance to the correct Codex Game Studios workflow.
---

## Codex-native operating rules

Ask one decision per turn and wait for the answer before asking another. A
`request_user_input` call contains 1-3 questions only when genuinely independent,
and each question contains 2-3 mutually exclusive options. Discovery is read-only
until a documented artifact changeset and target path are shown and approved.
Fresh projects route from `$start`; engine-dependent work with no configured
engine routes to `$setup-engine`.

# Guided Onboarding


This skill may update two persistent artifacts after showing their exact changes
and receiving explicit approval: `production/stage.txt` and
`.codex/studio.toml`. `.codex/studio.toml` is the sole persistent review-mode authority.
Never create a separate review-mode file.

This skill is the entry point for new users. It does NOT assume you have a game idea, an engine preference, or any prior experience. It asks first, then routes you to the right workflow.

---

## Plugin-native first run

Invoke this workflow as `$codex-game-studios:start` when the installed plugin is
the available entry point. A missing repository-root `.codex/studio.toml` is not
an error: continue read-only project detection, report that repository authority
is absent, and let the observed artifacts determine the onboarding path. Do not
infer a configured engine from another file.

Before presenting a persistent proposal, invoke the production
`tools.codex_studio.start_initialization` planning/validation interface with the
read-only project state and proposed event ledger. Do not present or perform a
write if it rejects the ledger. Its emitted normative contract controls every
first-run initialization rule below; the fingerprint and generated summary are
checked mechanically in both runtime and framework documentation.

For an installed plugin, execute the plugin-relative file
`./assets/studio/tools/codex_studio/start_initialization.py` from the plugin
root: `python3 -B ./assets/studio/tools/codex_studio/start_initialization.py
--preflight LEDGER.json --project-root PROJECT_ROOT`. `LEDGER.json` is one JSON
object with `authority_state` (`missing` or `initialized`) and ordered `events`.
An initialization event contains `authority_toml` and exact atomic `actions`; a
write repeats each approved action's `path`, `kind`, `material_change`, and
`sha256` in order. The command emits one JSON object with `status`, `mode`, and
`contract_sha256`; exit status 2 is a fail-closed validation error. After writes,
run the same path with `--audit` so the bundled validator reads actual path types
and file digests rather than trusting prospective write records.

<!-- start-initialization-contract:sha256=a6b2b182e7d40eb29ebf7ecbc61c45a66daff0902251782bd3da927c59b44145 -->
<!-- start-initialization-summary:start
- First run has exactly 1 Initialization changeset and at most 10 unique path mutations; each mutation is one filesystem path.
- The only first-run project-owned file targets are `.codex/studio.toml`, `production/stage.txt`; a parent directory is created only when observed missing, before a required create or merge child, never for delete or speculation.
- Each action and write has an exact closed schema, one normalized target, material change, and SHA-256 digest where content exists; actions use `create`, `modify`, `merge`, `delete`, `directory-create`, `managed-block-edit` and never `glob`, `recursive`, `tree-copy`, `bulk` or aliases.
- Forbidden roots and every descendant are `.agents/skills`, `.codex/agents`, `.codex/agent-packs`, `Codex Studio Testing Framework`, `docs/engine-reference`; all other paths are outside selected and approved project authority.
- No writes precede approval (0); writes match approved actions exactly in order, and a plan above the cap replans (True).
- The six-field default authority is `active_engine_pack = "none"`; `engine = "unconfigured"`; `engine_version = ""`; `language = ""`; `model_policy = "balanced"`; `review_mode = "phase-gated"`, and missing authority must create and write its exact bytes.
- Initialized repositories have 0 Initialization changesets and retain unique proposal-specific stage and review-mode approval/write groups; stage uses `create`, `modify`, `merge`, bound to its observed preimage, and must audit as a regular digest-matching file; review mode is a full-file `modify` from and to one of `full`, `phase-gated`, `solo`, preserving every other authority value.
- Installed execution uses `tools/codex_studio/start_initialization.py --preflight|--audit LEDGER --project-root PROJECT` and ledger schema version 1. Preflight and audit are link/reparse-safe; link-safe filesystem path types and SHA-256 digests (file mode is not part of this material contract).
start-initialization-summary:end -->
<!-- start-initialization-ledger-schema:sha256=51b3d3e87945534950f85ee25e18c06a25ec236e46db0de22d9bd42fdda07d0f -->
<!-- start-initialization-ledger-schema:start
{"action":{"directory_exact_keys":["expanded_paths","form","kind","material_change","path","required_by","sha256"],"expanded_paths":"[path]","file_exact_keys":["expanded_paths","form","kind","material_change","path","sha256"],"form":"atomic","kind":["create","modify","merge","delete","directory-create","managed-block-edit"],"material_change":"non-empty string","path":"normalized repository-relative approved target","required_by":"string (directory-create only)","sha256":"64 lowercase hex for file actions; null for delete and directory-create"},"authority":{"default_toml_exact_bytes":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","default_toml_sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc","missing_requirement":"exactly one .codex/studio.toml create action and reconciled write with these bytes and digest"},"control_events":{"approval":{"exact_keys":["type"]},"detect":{"exact_keys":["type"]},"review-mode-approval":{"exact_keys":["type"]},"select-next-step":{"exact_keys":["type","next_step"],"next_step":["brainstorm","setup-engine","project-stage-detect"]},"stage-approval":{"exact_keys":["type"]}},"events":{"initialization-changeset":{"authority_toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","exact_keys":["type","authority_toml","actions"]},"review-mode-proposal":{"authority_before_exact_keys":["engine","engine_version","language","review_mode","active_engine_pack","model_policy"],"exact_keys":["type","review_mode","authority_before","actions"],"review_mode":["full","phase-gated","solo"]},"stage-proposal":{"exact_keys":["type","actions"]}},"example_envelope":{"exact_keys":["initial_state","session","write_contents"],"initial_state":{"directories":{".codex":["missing","directory"],"production":["missing","directory"]},"exact_keys":["directories","files"],"files":"exact repository-relative UTF-8 pre-images"},"write_contents":"exact UTF-8 post-image for every non-directory, non-delete approved action"},"examples":{"first_run_brainstorm":{"initial_state":{"directories":{".codex":"missing","production":"missing"},"files":{}},"session":{"authority_state":"missing","events":[{"type":"detect"},{"next_step":"brainstorm","type":"select-next-step"},{"actions":[{"expanded_paths":[".codex"],"form":"atomic","kind":"directory-create","material_change":"create the authority parent","path":".codex","required_by":".codex/studio.toml","sha256":null},{"expanded_paths":[".codex/studio.toml"],"form":"atomic","kind":"create","material_change":"write the complete default authority","path":".codex/studio.toml","sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc"}],"authority_toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","type":"initialization-changeset"},{"type":"approval"},{"kind":"directory-create","material_change":"create the authority parent","path":".codex","sha256":null,"type":"write"},{"kind":"create","material_change":"write the complete default authority","path":".codex/studio.toml","sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc","type":"write"}]},"write_contents":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n"}},"first_run_project_stage_detect":{"initial_state":{"directories":{".codex":"missing","production":"missing"},"files":{}},"session":{"authority_state":"missing","events":[{"type":"detect"},{"next_step":"project-stage-detect","type":"select-next-step"},{"actions":[{"expanded_paths":[".codex"],"form":"atomic","kind":"directory-create","material_change":"create the authority parent","path":".codex","required_by":".codex/studio.toml","sha256":null},{"expanded_paths":[".codex/studio.toml"],"form":"atomic","kind":"create","material_change":"write the complete default authority","path":".codex/studio.toml","sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc"}],"authority_toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","type":"initialization-changeset"},{"type":"approval"},{"kind":"directory-create","material_change":"create the authority parent","path":".codex","sha256":null,"type":"write"},{"kind":"create","material_change":"write the complete default authority","path":".codex/studio.toml","sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc","type":"write"}]},"write_contents":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n"}},"first_run_setup_engine":{"initial_state":{"directories":{".codex":"missing","production":"missing"},"files":{}},"session":{"authority_state":"missing","events":[{"type":"detect"},{"next_step":"setup-engine","type":"select-next-step"},{"actions":[{"expanded_paths":[".codex"],"form":"atomic","kind":"directory-create","material_change":"create the authority parent","path":".codex","required_by":".codex/studio.toml","sha256":null},{"expanded_paths":[".codex/studio.toml"],"form":"atomic","kind":"create","material_change":"write the complete default authority","path":".codex/studio.toml","sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc"},{"expanded_paths":["production"],"form":"atomic","kind":"directory-create","material_change":"create the stage parent","path":"production","required_by":"production/stage.txt","sha256":null},{"expanded_paths":["production/stage.txt"],"form":"atomic","kind":"create","material_change":"write the selected initial stage","path":"production/stage.txt","sha256":"3c6356e0cc11bc22b99269b314ec6de24caf3e2fae6e9afac763023004f8ae7d"}],"authority_toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","type":"initialization-changeset"},{"type":"approval"},{"kind":"directory-create","material_change":"create the authority parent","path":".codex","sha256":null,"type":"write"},{"kind":"create","material_change":"write the complete default authority","path":".codex/studio.toml","sha256":"b36b0604a2a9ef02ffc036ad91e885c4db0beefcd4be0516f17695924b7d79fc","type":"write"},{"kind":"directory-create","material_change":"create the stage parent","path":"production","sha256":null,"type":"write"},{"kind":"create","material_change":"write the selected initial stage","path":"production/stage.txt","sha256":"3c6356e0cc11bc22b99269b314ec6de24caf3e2fae6e9afac763023004f8ae7d","type":"write"}]},"write_contents":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","production/stage.txt":"Concept\n"}},"initialized_review_mode":{"initial_state":{"directories":{".codex":"directory","production":"missing"},"files":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n"}},"session":{"authority_state":"initialized","events":[{"type":"detect"},{"actions":[{"expanded_paths":[".codex/studio.toml"],"form":"atomic","kind":"modify","material_change":"update only review_mode to full in the complete authority","path":".codex/studio.toml","sha256":"7acbd4b6ccda7ae0f07bf5a78f33ecaa2b24ad7cc398a881e3b6c0b7aebf83da"}],"authority_before":{"active_engine_pack":"none","engine":"unconfigured","engine_version":"","language":"","model_policy":"balanced","review_mode":"phase-gated"},"review_mode":"full","type":"review-mode-proposal"},{"type":"review-mode-approval"},{"kind":"modify","material_change":"update only review_mode to full in the complete authority","path":".codex/studio.toml","sha256":"7acbd4b6ccda7ae0f07bf5a78f33ecaa2b24ad7cc398a881e3b6c0b7aebf83da","type":"write"}]},"write_contents":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"full\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n"}},"initialized_stage":{"initial_state":{"directories":{".codex":"directory","production":"missing"},"files":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n"}},"session":{"authority_state":"initialized","events":[{"type":"detect"},{"actions":[{"expanded_paths":["production"],"form":"atomic","kind":"directory-create","material_change":"create the stage parent","path":"production","required_by":"production/stage.txt","sha256":null},{"expanded_paths":["production/stage.txt"],"form":"atomic","kind":"create","material_change":"write the selected initial stage","path":"production/stage.txt","sha256":"3c6356e0cc11bc22b99269b314ec6de24caf3e2fae6e9afac763023004f8ae7d"}],"type":"stage-proposal"},{"type":"stage-approval"},{"kind":"directory-create","material_change":"create the stage parent","path":"production","sha256":null,"type":"write"},{"kind":"create","material_change":"write the selected initial stage","path":"production/stage.txt","sha256":"3c6356e0cc11bc22b99269b314ec6de24caf3e2fae6e9afac763023004f8ae7d","type":"write"}]},"write_contents":{"production/stage.txt":"Concept\n"}},"initialized_stage_and_review_mode":{"initial_state":{"directories":{".codex":"directory","production":"missing"},"files":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"phase-gated\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n"}},"session":{"authority_state":"initialized","events":[{"type":"detect"},{"actions":[{"expanded_paths":["production"],"form":"atomic","kind":"directory-create","material_change":"create the stage parent","path":"production","required_by":"production/stage.txt","sha256":null},{"expanded_paths":["production/stage.txt"],"form":"atomic","kind":"create","material_change":"write the selected initial stage","path":"production/stage.txt","sha256":"3c6356e0cc11bc22b99269b314ec6de24caf3e2fae6e9afac763023004f8ae7d"}],"type":"stage-proposal"},{"type":"stage-approval"},{"kind":"directory-create","material_change":"create the stage parent","path":"production","sha256":null,"type":"write"},{"kind":"create","material_change":"write the selected initial stage","path":"production/stage.txt","sha256":"3c6356e0cc11bc22b99269b314ec6de24caf3e2fae6e9afac763023004f8ae7d","type":"write"},{"actions":[{"expanded_paths":[".codex/studio.toml"],"form":"atomic","kind":"modify","material_change":"update only review_mode to full in the complete authority","path":".codex/studio.toml","sha256":"7acbd4b6ccda7ae0f07bf5a78f33ecaa2b24ad7cc398a881e3b6c0b7aebf83da"}],"authority_before":{"active_engine_pack":"none","engine":"unconfigured","engine_version":"","language":"","model_policy":"balanced","review_mode":"phase-gated"},"review_mode":"full","type":"review-mode-proposal"},{"type":"review-mode-approval"},{"kind":"modify","material_change":"update only review_mode to full in the complete authority","path":".codex/studio.toml","sha256":"7acbd4b6ccda7ae0f07bf5a78f33ecaa2b24ad7cc398a881e3b6c0b7aebf83da","type":"write"}]},"write_contents":{".codex/studio.toml":"engine = \"unconfigured\"\nengine_version = \"\"\nlanguage = \"\"\nreview_mode = \"full\"\nactive_engine_pack = \"none\"\nmodel_policy = \"balanced\"\n","production/stage.txt":"Concept\n"}}},"initialized_groups":{"constraints":"each proposal type and mutation path appears at most once; only a stage proposal may include its observed-missing production parent immediately before the create or merge target","review-mode-proposal":{"action_kind":"modify","approval":"review-mode-approval","optional_parent":null,"post_image":"canonical complete six-field authority_before with only review_mode changed from one closed current value to a different closed target value; action/write SHA-256 matches exact post-image","target":".codex/studio.toml"},"stage-proposal":{"action_kind":["create","modify","merge"],"approval":"stage-approval","optional_parent":"production","post_image":"successful audit requires regular production/stage.txt whose SHA-256 matches the action and write","preimage":"create requires missing; modify or merge requires existing regular","target":"production/stage.txt"}},"ledger_schema_version":1,"ordering":{"first_run":{"exact_sequence":["detect","select-next-step","initialization-changeset","approval","one write per action in action order"],"initialization_changesets":1},"initialized":{"exact_prefix":["detect"],"initialization_changesets":0,"repeating_group":["unique proposal","matching separate approval","one write per action in action order"]}},"selection_stage_rule":"a production/stage.txt action exists if and only if select-next-step.next_step is setup-engine; it uses create for missing or modify/merge for existing regular and always leaves a digest-bound regular file; brainstorm and project-stage-detect omit it","top_level":{"authority_state":["missing","initialized"],"events":"array","exact_keys":["authority_state","events"]},"write":{"exact_keys":["kind","material_change","path","sha256","type"],"fields":"repeat approved action path/kind/material_change/sha256 in order","type":"write"},"write_reconciliation":{"cardinality":"exactly one write per approved action","exact_fields":["path","kind","material_change","sha256"],"order":"same order as actions","unapproved_writes":0}}
start-initialization-ledger-schema:end -->

On first run, this one Initialization changeset replaces the separate persistent
proposals in Phases 4-6. It may include `production/stage.txt` only when that
selected next step requires it; after approval, skip those separate persistent
proposals.

For a present, readable `.codex/studio.toml`, preserve the initialized-repository
protocol below, including its separate stage and review-mode approvals. An
unreadable or invalid TOML authority remains a repair case, including any
current `review_mode` outside `full`, `phase-gated`, or `solo`: show its exact
repair changeset and stop without writing until the user approves it.

---

## Legacy installation routing

Before plugin-native first-run handling, inspect repository-root
`.codex/codex-game-studios/installation.json` read-only. If it is canonical
schema 1 state for the supported legacy installation, offer exactly these four
choices:

- `verify legacy installation`
- `repair legacy installation`
- `migrate to plugin-native`
- `uninstall legacy installation`

Never migrate automatically. Verification, repair, migration, and uninstall
must use the authenticated legacy payload capsule. For every mutating choice,
present the complete digest-bound manager plan, including all actions,
preservations, conflicts, target observations, result observations, state
digest, approval-context commitment, and final plan digest, before asking for
approval. Apply only that exact approved plan. A schema 2 migration state uses
plugin-native validation; its repair is a validated no-op when healthy, and its
uninstall removes only the migration state while preserving every project path
and recorded remnant.

---

## Phase 1: Detect Project State

Before asking anything, silently gather context so you can tailor your guidance.
Do not emit a raw scan log; Phase 2 presents the relevant evidence as a concise
project-state summary before asking the user to confirm the starting point.

Check:
- **Engine configured?** Read `.codex/studio.toml`. If it is missing, continue
  read-only project detection under the plugin-native first-run protocol. If it
  is unreadable or invalid TOML, report that the canonical studio authority is
  unavailable, do not infer values from another file, offer restoration or an
  explicitly approved repair, then stop with `Verdict: **BLOCKED**`. If it contains
  `engine = "unconfigured"`, no engine pack is active. Use
  `.codex/docs/technical-preferences.md` only for the selected engine's detailed
  preferences after activation.
- **Game concept exists?** Check for `design/gdd/game-concept.md`.
- **Source code exists?** repository file search for source files in `src/` (`*.gd`, `*.cs`, `*.cpp`, `*.h`, `*.rs`, `*.py`, `*.js`, `*.ts`).
- **Prototypes exist?** Check for subdirectories in `prototypes/`.
- **Design docs exist?** Count real game-design Markdown artifacts in
  `design/gdd/`; exclude every nested `AGENTS.md` and instruction-only files such as `.gitkeep` from artifact counts.
- **Production artifacts?** Check for files in `production/sprints/` or `production/milestones/`.

Store these findings internally to validate the user's self-assessment and tailor recommendations.

When the engine is unconfigured and there are **No concept, source, prototype, design, or production artifacts**, classify the repository as fresh and route to `$brainstorm` after the onboarding decision below.

---

## Phase 2: Confirm the Detected Starting Point

This is the first thing the user sees. Summarize the classification and show the concrete evidence you found:
configured engine value, concept path or absence,
source-file count, prototype directories, design-document count, and production
artifact paths. Do not ask the user to choose a state contradicted by the
repository.

Use two sequential two-option decisions so every `request_user_input` call fits
the native schema.

First ask: "Which broad starting point best describes this project?"

- `New or exploratory` — no formalized game concept or implementation yet.
- `Defined or existing` — a clear concept or existing project artifacts are present.

Wait. If the user selects **New or exploratory**, ask one follow-up:

- `No idea yet (Path A)` — explore what to make.
- `Vague idea (Path B)` — develop a rough theme, feeling, or genre.

If the user selects **Defined or existing**, ask one follow-up instead:

- `Clear concept (Path C)` — formalize a known genre and core mechanic.
- `Existing work (Path D)` — organize or continue existing docs, prototypes, or code.

Wait for the second selection before routing. Never batch the two decisions.

---

## Phase 3: Confirm the Workflow Path

#### If A: No idea yet

The user needs creative exploration before anything else.

1. Acknowledge that starting from zero is completely fine
2. Briefly explain what `$brainstorm` does (guided ideation using professional frameworks — MDA, player psychology, verb-first design). Mention that it has two modes: `$brainstorm open` for fully open exploration, or `$brainstorm [hint]` if they have even a vague theme (e.g., "space", "cozy", "horror").
3. Recommend running `$brainstorm open` as the next step, but invite them to use a hint if something comes to mind
4. Show the recommended path:
   **Concept phase:**
   - `$brainstorm open` — discover your game concept
   - `$setup-engine` — configure the engine (brainstorm will recommend one)
   - `$prototype` — throwaway concept build: validate the core idea is fun before designing (1–3 days)
   - `$art-bible` — define visual identity (uses the Visual Identity Anchor brainstorm produces)
   - `$map-systems` — decompose the concept into systems
   - `$design-system` — author a GDD for each MVP system
   - `$review-all-gdds` — cross-system consistency check
   - `$gate-check` — validate readiness before architecture work
   **Architecture phase:**
   - `$create-architecture` — produce the master architecture blueprint and Required ADR list
   - `$architecture-decision (×N)` — record key technical decisions, following the Required ADR list
   - `$create-control-manifest` — compile decisions into an actionable rules sheet
   - `$architecture-review` — validate architecture coverage
   **Pre-Production phase:**
   - `$ux-design` — author UX specs for key screens (main menu, HUD, core interactions)
   - `$vertical-slice` — production-quality end-to-end build to validate the full game loop
   - `$playtest-report (×1+)` — document each vertical slice playtest session
   - `$create-epics` — map systems to epics
   - `$create-stories` — break epics into implementable stories
   - `$sprint-plan` — plan the first sprint
   **Production phase:** → pick up stories with `$dev-story`

#### If B: Vague idea

1. Ask them to share their vague idea — even a few words is enough
2. Validate the idea as a starting point (don't judge or redirect)
3. Recommend running `$brainstorm [their hint]` to develop it
4. Show the recommended path:
   **Concept phase:**
   - `$brainstorm [hint]` — develop the idea into a full concept
   - `$setup-engine` — configure the engine
   - `$prototype` — throwaway concept build: validate the core idea is fun before designing (1–3 days)
   - `$art-bible` — define visual identity (uses the Visual Identity Anchor brainstorm produces)
   - `$map-systems` — decompose the concept into systems
   - `$design-system` — author a GDD for each MVP system
   - `$review-all-gdds` — cross-system consistency check
   - `$gate-check` — validate readiness before architecture work
   **Architecture phase:**
   - `$create-architecture` — produce the master architecture blueprint and Required ADR list
   - `$architecture-decision (×N)` — record key technical decisions, following the Required ADR list
   - `$create-control-manifest` — compile decisions into an actionable rules sheet
   - `$architecture-review` — validate architecture coverage
   **Pre-Production phase:**
   - `$ux-design` — author UX specs for key screens (main menu, HUD, core interactions)
   - `$vertical-slice` — production-quality end-to-end build to validate the full game loop
   - `$playtest-report (×1+)` — document each vertical slice playtest session
   - `$create-epics` — map systems to epics
   - `$create-stories` — break epics into implementable stories
   - `$sprint-plan` — plan the first sprint
   **Production phase:** → pick up stories with `$dev-story`

#### If C: Clear concept

1. Ask them to describe their concept in one sentence — genre and core mechanic. Use plain text, not one-question prompt (it's an open response).
2. Acknowledge the concept, then ask one concise question and wait for the answer to offer two paths:
   - **Prompt**: "How would you like to proceed?"
   - **Options**:
     - `Formalize it first` — Run `$brainstorm [concept]` to structure it into a proper game concept document
     - `Jump straight in` — Go to `$setup-engine` now and write the GDD manually afterward
3. Show the recommended path:
   **Concept phase:**
   - `$brainstorm` or `$setup-engine` — (their pick from step 2)
   - `$prototype` — throwaway concept build: validate the core idea is fun before designing (1–3 days)
   - `$art-bible` — define visual identity (after brainstorm if run, or after concept doc exists)
   - `$design-review` — validate the concept doc
   - `$map-systems` — decompose the concept into individual systems
   - `$design-system` — author a GDD for each MVP system
   - `$review-all-gdds` — cross-system consistency check
   - `$gate-check` — validate readiness before architecture work
   **Architecture phase:**
   - `$create-architecture` — produce the master architecture blueprint and Required ADR list
   - `$architecture-decision (×N)` — record key technical decisions, following the Required ADR list
   - `$create-control-manifest` — compile decisions into an actionable rules sheet
   - `$architecture-review` — validate architecture coverage
   **Pre-Production phase:**
   - `$ux-design` — author UX specs for key screens (main menu, HUD, core interactions)
   - `$vertical-slice` — production-quality end-to-end build to validate the full game loop
   - `$playtest-report (×1+)` — document each vertical slice playtest session
   - `$create-epics` — map systems to epics
   - `$create-stories` — break epics into implementable stories
   - `$sprint-plan` — plan the first sprint
   **Production phase:** → pick up stories with `$dev-story`

#### If D: Existing work

1. Share what you found in Phase 1:
   - "I can see you have [X source files / Y design docs / Z prototypes]..."
   - "Your engine is [configured as X / not yet configured]..."

2. **Sub-case D1 — Early stage** (engine not configured or only a game concept exists):
   - Recommend `$setup-engine` first if engine not configured
   - Then `$project-stage-detect` for a gap inventory

   **Sub-case D2 — GDDs, ADRs, or stories already exist:**
   - Explain: "Having files isn't the same as the template's skills being able to use them. GDDs might be missing required sections. `$adopt` checks this specifically."
   - Recommend:
     1. `$project-stage-detect` — understand what phase and what's missing entirely
     2. `$adopt` — audit whether existing artifacts are in the right internal format

3. Show the recommended path for D2:
   - `$project-stage-detect` — phase detection + existence gaps
   - `$adopt` — format compliance audit + migration plan
   - `$setup-engine` — if engine not configured
   - `$design-system retrofit [path]` — fill missing GDD sections
   - `$architecture-decision retrofit [path]` — add missing ADR sections
   - `$architecture-review` — bootstrap the TR requirement registry
   - `$gate-check` — validate readiness for next phase

---

## Phase 4: Propose the Initial Stage Artifact

After confirming the starting path (and before asking about review mode), derive the initial stage value for `production/stage.txt`:

Stage mapping:
- **Path A, B, or C (starting from scratch)**: write `Concept`
- **Path D, existing project, engine not configured or only a game concept exists**: write `Concept`
- **Path D, existing project with GDDs but no architecture documents**: write `Systems Design`
- **Path D, existing project with full architecture (ADRs, architecture doc)**: write `Technical Setup`

Show the derived stage value and path, then ask one concise approval question.
Bind the proposed action kind to the observed target: use `create` only when
`production/stage.txt` is missing, and use `modify` or `merge` only when it is
an existing regular file. Never propose `delete` for the stage artifact. If
approved, create the `production/` directory only when needed and leave a
regular `production/stage.txt` whose SHA-256 matches the approved action. Run
the installed Start validator with `--audit` after the write. If declined,
leave the file unchanged and continue without claiming the stage was saved.

Say: "I've set `production/stage.txt` to `[stage]` — this anchors project-stage
detection and `$help` routing."

---

## Phase 5: Select Review Depth

Read the current `review_mode` from `.codex/studio.toml`, then show it with the
three available choices. Ask one concise question and wait for the answer:

- **Prompt**: "Review mode is currently `[current]`. Which review depth should the studio use across sessions?"
- **Options**:
  - `Full` — Director specialists review at each key workflow step. Best for teams, learning the workflow, or when you want thorough feedback on every decision.
  - `Phase-gated (recommended)` — Use lean optional-review depth while phase-transition and other mandatory director gates still run. Balanced for solo developers and small teams.
  - `Solo` — Skip optional director consultation for maximum speed; gates explicitly marked required still run.

Map the selection to the proposed persistent value:
- `Full` → `review_mode = "full"`
- `Phase-gated (recommended)` → `review_mode = "phase-gated"`
- `Solo` → `review_mode = "solo"`

Selecting a mode chooses a proposal; it does not write the configuration.

---

## Phase 6: Approve the Studio Configuration Changeset

Show the exact `.codex/studio.toml` diff and complete canonical post-image that
change only `review_mode`, then ask for explicit approval of that one-file
changeset. The `review-mode-proposal` records the closed target value and the
current exact six-field authority. Its sole action is a full-file `modify` whose
digest matches the canonical post-image; never propose delete, create, a parent
directory action, a partial line, or a managed-block edit. Preserve the engine,
version, language, active engine pack, and model policy values exactly and emit
all six fields in canonical order. If the selected value already matches,
report a no-op and do not rewrite the file. If approval is declined, leave
`.codex/studio.toml` unchanged and continue without claiming the selection was
saved.

Never create a separate review-mode file, even as a compatibility fallback.

---

## Phase 7: Confirm Before Proceeding

After presenting the recommended path, ask one concise question and wait for the answer to ask the user which step they'd like to take first. Never auto-run the next skill.

- **Prompt**: "Would you like to start with [recommended first step]?"
- **Options**:
  - `Yes, let's start with [recommended first step]`
  - `I'd like to do something else first`

---

## Phase 8: Hand Off

When the user confirms their next step, respond with a single short line: "Type `[skill command]` to begin." Nothing else. Do not re-explain the skill or add encouragement. The `$start` skill's job is done.

Verdict: **COMPLETE** — user oriented and handed off to next step.

---

## Edge Cases

- **User picks D but project is empty**: Gently redirect — "It looks like the project is a fresh template with no artifacts yet. Would Path A or B be a better fit?"
- **User picks A but project has code**: Mention what you found — "I noticed there's already code in `src/`. Did you mean to pick D (existing work)?"
- **User is returning (engine configured, concept exists)**: Skip onboarding entirely — "It looks like you're already set up! Your engine is [X] and you have a game concept at `design/gdd/game-concept.md`. Review mode: `[configured review mode]`. Want to pick up where you left off? Try `$sprint-plan` or just tell me what you'd like to work on."
- **User doesn't fit any option**: Let them describe their situation in their own words and adapt.

---

## Collaborative Protocol

1. **Ask first** — never assume the user's state or intent
2. **Present options** — give clear paths, not mandates
3. **User decides** — they pick the direction
4. **No auto-execution** — recommend the next skill, don't run it without asking
5. **Adapt** — if the user's situation doesn't fit a template, listen and adjust
