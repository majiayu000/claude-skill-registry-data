---
name: architecture
description: Convert an approved AgentBoard spec into an architecture document and workspace cards — runs the level-aware pipeline (research → classification audit → L1/L2/L3 compose → design review), surfaces the bundle, audit, level, and design-review findings as transparency, then commits the architecture document and creates one card per Card Slice. Use ONLY when the user explicitly wants to run the architecture phase on an existing approved spec — e.g. "run architecture on docs/specs/X", "turn the spec into cards". Do NOT trigger on general architecture/design discussion, or when there is no approved spec yet (use foundation first).
---

# Architecture — Level-aware Boundary & Card Creation

You are the orchestrator of the architecture pipeline. Convert an approved spec into an architecture document and create one workspace card per Card Slice in that document. You do not pick the level, write the architecture document, or judge its design quality — you spawn the level-aware subagents (`architecture-research-agent`, `architecture-classification-auditor`, `architecture-compose-l1` / `-l2` / `-l3`, `architecture-design-reviewer`), verify their outputs, display results to the user, and act on the user's decisions.

## Inputs from the user

- The path to an approved spec at `docs/specs/<file>.md` (provided as an argument or the most recent file in `docs/specs/`).
- Optional `--pause` flag in the argument string to opt into the `/architecture` correction-loop pause for this run (e.g., `/architecture docs/specs/2026-05-23-my-spec.md --pause` or `/architecture --pause`). The token `pause` without leading dashes is also accepted. If neither form is present in the argument string, `/architecture` correction pause is off by default for this run; the user can re-issue `/architecture` with `--pause` to turn it on.

## Outputs you produce

- A committed architecture document at `docs/arch/<file>.md`.
- One workspace card per Card Slice in that document, each with a `depends_on` edge resolved against the slices' Depends on field.
- A scaffold card moved to `finished` that holds the four pipeline artifacts (`ARCH_FACTS_BUNDLE_V2`, `ARCH_BUNDLE_AUDIT_V2`, `architecture_document`, `ARCH_DESIGN_REVIEW_V1`) as its audit trail.

## Pipeline overview

```
/foundation produces docs/specs/<file>.md
   ↓
/architecture orchestrates:
  research wave   : architecture-research-agent          → ARCH_FACTS_BUNDLE_V2
  audit wave      : architecture-classification-auditor  → ARCH_BUNDLE_AUDIT_V2  (verified level)
  compose wave    : architecture-compose-l<N>            → architecture_document + docs/arch/<file>.md
  review wave     : architecture-design-reviewer         → ARCH_DESIGN_REVIEW_V1
  user approval   : you display the document and the review; the user approves, requests changes, or rejects
  commit + cards  : you commit the architecture document and create one workspace card per slice
   ↓
/orchestrate runs planning → review → implementation → audit on those cards
```

## Halt conditions (any of these stops the pipeline)

- A spawned subagent fails to submit its required artifact to the scaffold card (verified per round by the snapshot-and-diff in steps 6/7, 8/9, 11/12, and 14/15, not by a type-only lookup).
- The audit reports an invalid level (anything other than the integers `1`, `2`, or `3` in `verified_level`).
- A spawned compose agent halts because the audit reports `any_discrepancy: true` but carries no `corrected_bundle`, or `any_discrepancy: false` but the original bundle fetched via the audit's `audited_bundle_artifact_id` back-reference cannot be retrieved or parsed (compose's Step 2 audit-fetch-and-bundle-resolution fails). The orchestrator detects this by the absence of the compose agent's required artifact at step 12 and reads the failure card note compose wrote to the scaffold card.
- The architecture document is not present at the exact `architecture_document_path` derived in step 13 on disk after the compose wave.
- The user rejects the architecture document.

On any halt, write a card note to the scaffold card via `agentboard_update_workspace_card` naming the failing step and the specific condition, write an activity log entry via `agentboard_add_log_entry` naming the step and the condition, stop the pipeline, and report the halt to the user. Do not create any workspace cards from a halted pipeline.

## Instructions

Follow these 21 steps in order. Each step is mandatory; there are no skip conditions.

### 1. Load tools and skills

Call `ToolSearch` for `agentboard`, `codegraph`, `rag`, and `Context7` to make their tool schemas available. If only `agentboard_authenticate` and `agentboard_complete_authentication` are visible after the `ToolSearch`, run the OAuth bootstrap per `skills/agentboard/SKILL.md` §1.3 before proceeding.

### 2. Activate the expert-standards skill

Activate the `agentboard:expert-standards` skill via the `Skill` tool. This is your governing cognitive frame for the orchestration decisions you make in subsequent steps (halt-or-continue verdicts, applying user corrections, summarizing transparency to the user). Subagents activate the same skill independently as the first step of their own profiles; your activation does not satisfy theirs.

### 3. Locate the approved spec and detect the correction-pause flag

Parse the argument string into two pieces. First, scan the tokens for the literal flag `--pause` (case-sensitive) or the bare token `pause` (case-sensitive); if either is present, capture `architecture_correction_pause_flag = true` for step 4 and remove that token from the remaining argument string. Second, treat the remaining argument string as the spec path: if a spec path was passed, use that path; otherwise, list `docs/specs/` and pick the most recent file. Read the spec via `Read` in full to confirm it exists and is non-empty. Confirm with the user that this is the spec the architecture is being built for, and (if `architecture_correction_pause_flag == true`) confirm that they explicitly want the correction-loop pause on for this run.

### 4. Select or create a workspace board and correction-loop pause mode

Call `agentboard_list_apps`, then `agentboard_list_boards` for the chosen app. If no suitable board exists for this work, call `agentboard_create_app` and/or `agentboard_create_board` to make one. Call `agentboard_get_board` on the chosen board to read its `auto_transitions` settings (`review_blocking`, `audit_blocking`) and capture them. Set the `/architecture` correction-pause mode for this run from `architecture_correction_pause_flag` captured in step 3: `architecture_correction_pause = architecture_correction_pause_flag` (defaults to `false` because step 3 captures the flag only if `--pause` or `pause` was passed in the argument string). Report both the board's existing checkpoint behavior and the `/architecture` correction-pause mode to the user before continuing. The `/architecture` pause is distinct from the AgentBoard app's blocking-gate mechanism and does not modify board settings.

### 5. Create the scaffold card

Call `agentboard_create_workspace_card` with these fields:

- **Title:** `Architecture: <spec topic>` (derive the topic from the spec's filename or top-level heading).
- **Description:** `Architecture flow scaffold. Holds research bundle, audit, architecture document, and design review artifacts during the level-aware architecture pipeline. Will be moved to finished after cards are created from the architecture's slices.`
- **Status:** `backlog` (the scaffold stays in `backlog` for the whole pipeline; step 20 moves it to `finished`).

Capture the returned `scaffold_card_id` for use in every subsequent step that spawns a subagent or writes to the scaffold card.

### 6. Spawn the research agent

Before spawning the research agent, call `agentboard_list_workspace_artifacts` on `scaffold_card_id` and capture the set of existing artifact IDs as `pre_research_artifact_ids`. Step 7 diffs against this snapshot to bind the exact bundle this run produced, so a re-run from step 17 cannot rebind to a prior round's bundle.

Spawn `architecture-research-agent` (background). On the initial run, pass exactly these inputs in the prompt and no others: `spec_path`, `scaffold_card_id`, `agent_id`. On a re-run from step 17's `verified-bundle` route, ALSO pass `force_remeasure: true` so the agent's prior-bundle-reuse check is suppressed and a fresh V2 bundle is produced (short-spec CL-009). Wait for completion.

### 7. Verify the research bundle artifact

Call `agentboard_list_workspace_artifacts` on `scaffold_card_id`. Diff the returned artifact IDs against `pre_research_artifact_ids` from step 6; the artifact IDs not present in that snapshot are the ones this research run created. Among the newly created artifacts, select the one whose `artifact_type` is `ARCH_FACTS_BUNDLE_V2` (the sentinel-prefixed content is also acceptable when `artifact_type` is unset) and capture its exact artifact ID as `audited_bundle_artifact_id` for this round. Pass this captured ID to the auditor in step 8; never re-resolve the bundle by a type-only lookup, which would rebind to a prior round's bundle after a step-17 re-run. If no newly created bundle artifact exists, halt per the Halt conditions section.

### 8. Spawn the classification auditor

Before spawning the auditor, call `agentboard_list_workspace_artifacts` on `scaffold_card_id` and capture the set of existing artifact IDs as `pre_audit_artifact_ids`. Step 9 diffs against this snapshot to bind the exact audit this run produced, so a re-run from step 17 cannot rebind to a prior round's audit.

Spawn `architecture-classification-auditor` (background). Pass exactly these inputs in the prompt and no others: `spec_path`, `audited_bundle_artifact_id` (the per-round bundle ID captured in step 7), `scaffold_card_id`, `agent_id`. Wait for completion.

### 9. Verify the audit artifact and read the verified level

This step produces one seam object — `audit_artifact_id` — that the orchestrator threads forward unchanged to both compose (step 11) and the design reviewer (step 14), the same single value to both. The orchestrator does NOT resolve the verified bundle: that resolution moves to compose's Step 2 and to the design reviewer's Step 2(c), each of which fetches the audit via this same `audit_artifact_id`, branches on the audit's `any_discrepancy` flag, and either reads `corrected_bundle` directly (when `true`) or fetches the original bundle via the audit's `audited_bundle_artifact_id` back-reference and parses it (when `false`). This is the single-seam discipline: the audit is the only place the verified bundle lives; the orchestrator never serializes the bundle; no orphan-artifact failure mode is introduced; both downstream consumers (compose and reviewer) resolve the bundle identically by reading the same audit.

Call `agentboard_list_workspace_artifacts` on `scaffold_card_id`. Diff the returned artifact IDs against `pre_audit_artifact_ids` from step 8; the artifact IDs not present in that snapshot are the ones this audit run created. Among the newly created artifacts, select the one whose `artifact_type` is `ARCH_BUNDLE_AUDIT_V2` and capture its exact artifact ID as `audit_artifact_id` for this round; never re-resolve the audit by a type-only lookup, which would rebind to a prior round's audit after a step-17 re-run. Fetch its content via `agentboard_get_workspace_artifact` on `audit_artifact_id`. Read the `verified_level` field — an integer that is `1`, `2`, or `3`. Capture the audit's `field_verdicts`, `any_discrepancy` flag, and (when present) `corrected_bundle` for the transparency display in step 10.

If no newly created `ARCH_BUNDLE_AUDIT_V2` artifact exists, halt per the Halt conditions section. Before reporting the halt, call `agentboard_get_card` on `scaffold_card_id` to read the auditor's most recent card note for the diagnostic.

### 10. Display the bundle, audit, and verified level to the user — transparency, not approval

Render a brief markdown summary in the chat covering:

- The bundle's eight classification field values with their evidence counts and the seven design field summaries (file counts by role, edge count, library count, open question count).
- The rules that fired (e.g., `R-L3-EXT` because `external_system_count > 0`) with the reasoning trace from `rule_evaluation.reasoning`.
- The auditor's verdict per field (PASS or DISCREPANCY); if any DISCREPANCY, the corrected values and the recomputed level.
- The verified level rendered in human-readable form: `L1`, `L2`, or `L3`. Convert the integer `verified_level` (`1`, `2`, or `3`) to the `L#` form for chat display only; preserve the integer form for dispatch in step 11.

Do not ask the user to approve the level. Do not offer the user an option to change the level. Proceed to step 11 after rendering the summary.

### 11. Dispatch to the level-appropriate compose agent

Before spawning compose, call `agentboard_list_workspace_artifacts` on `scaffold_card_id` and capture the set of existing artifact IDs as `pre_compose_artifact_ids`. This snapshot is what step 12 diffs against to bind the exact artifact this compose run produced, so that a re-run from step 17 cannot rebind to a prior round's `architecture_document` artifact.

Read the integer `verified_level` captured in step 9. Dispatch on the numeric value:

- `verified_level == 1` → spawn `architecture-compose-l1` (background).
- `verified_level == 2` → spawn `architecture-compose-l2` (background).
- `verified_level == 3` → spawn `architecture-compose-l3` (background).
- Any other value (not in `{1, 2, 3}`) → halt per the Halt conditions section.

Pass exactly these inputs in the prompt to the dispatched compose agent and no others: `spec_path`, `verified_level` (as the integer `1`, `2`, or `3`), `scaffold_card_id`, `agent_id`, and `audit_artifact_id` (the same artifact ID also passed to the design reviewer at step 14). Compose's Step 2 fetches the audit via `agentboard_get_workspace_artifact` and resolves the verified bundle by the same `any_discrepancy`-branch logic the design reviewer uses at its Step 2(c). Never embed bundle JSON in the prompt — `audit_artifact_id` is the single seam between the orchestrator and compose for the verified bundle. Wait for completion.

### 12. Verify the architecture document artifact landed

Do not parse hook output yourself. The PreToolUse validation hook fires automatically when compose calls `agentboard_submit_workspace_artifact`; treat the artifact's presence or absence on the scaffold card as your verification surface.

Call `agentboard_list_workspace_artifacts` on `scaffold_card_id`. Diff the returned artifact IDs against `pre_compose_artifact_ids` from step 11; the artifact IDs not present in that snapshot are the ones this compose run created. Among the newly created artifacts, select the one whose `artifact_type` is `architecture_document` and capture its exact artifact ID as `architecture_document_artifact_id` for this round. Use this captured ID in step 14; never re-resolve the architecture document by a type-only lookup, which would rebind to a prior round's artifact after a step-17 re-run. If no newly created `architecture_document` artifact exists, halt per the Halt conditions section.

### 13. Verify the architecture document is on disk at its exact derived path

Derive the architecture document path deterministically from the spec path; do not infer it by closest-match scanning. The compose agents write the document to `docs/arch/architecture-<kebab-case-name>.md`, where `<kebab-case-name>` is the kebab-case form of the spec's name — the same naming convention `/foundation` uses for `docs/specs/`. Compute the expected path: take the spec filename from `spec_path` (the basename without its `.md` extension), strip a leading `architecture-` token only if the spec filename itself begins with one (it normally does not — spec filenames begin with a date or topic), and form `docs/arch/architecture-<spec-basename>.md` so the architecture filename mirrors the spec filename under the shared convention. Verify that this exact file exists on disk with a single `Glob` for that exact path (the pattern is the literal computed path, not the wildcard `docs/arch/*.md`). Capture the verified exact path as `architecture_document_path`. Thread this one exact value, unchanged, through step 14 (design reviewer input), step 16 (display and edits), step 17 (corrections), step 18 (git commit), and step 19 (card creation re-read). If the file at the exact derived path is not on disk after the compose wave, halt per the Halt conditions section — do not fall back to selecting a different `docs/arch/*.md` file by resemblance.

### 14. Spawn the design reviewer

Before spawning the design reviewer, call `agentboard_list_workspace_artifacts` on `scaffold_card_id` and capture the set of existing artifact IDs as `pre_review_artifact_ids`. Step 15 diffs against this snapshot to bind the exact review artifact this run produced, so a re-run from step 17 cannot rebind to a prior round's review artifact.

Spawn `architecture-design-reviewer` (background). Pass exactly these inputs in the prompt and no others: `spec_path`, `architecture_document_path` (the exact path from step 13), `architecture_document_artifact_id` (the per-round ID captured in step 12), `audit_artifact_id`, `scaffold_card_id`, `agent_id`. The value supplied for `audit_artifact_id` is the `ARCH_BUNDLE_AUDIT_V2` artifact's ID from step 9, never the original bundle's ID. The design reviewer fetches the audit and resolves the bundle from it by the same `any_discrepancy`-branch logic compose's Step 2 uses. Wait for completion.

### 15. Verify the design review artifact and read the findings

Call `agentboard_list_workspace_artifacts` on `scaffold_card_id`. Diff the returned artifact IDs against `pre_review_artifact_ids` from step 14; the artifact IDs not present in that snapshot are the ones this design-review run created. Among the newly created artifacts, select the one whose `artifact_type` is `ARCH_DESIGN_REVIEW_V1` and capture its exact artifact ID as the design review artifact for this round; never re-resolve the review by a type-only lookup, which would rebind to a prior round's review artifact after a step-17 re-run. Fetch its content via `agentboard_get_workspace_artifact` on that captured ID. Read the `findings` array; an empty array is a valid result and the pipeline continues. Read the `summary.blocker_count`, `summary.serious_count`, and `summary.minor_count`. If no newly created `ARCH_DESIGN_REVIEW_V1` artifact exists, halt per the Halt conditions section.

### 16. Display the architecture document and the design review to the user

Display in the chat:

- The architecture document content (rendered from `architecture_document_path`).
- The design review findings rendered by severity: `blocker` findings first, then `serious`, then `minor`. For each finding, show the `id`, `category`, `summary`, `document_citation` (the section, decision id or slice name, and quoted text), and `suggested_resolution`.
- The verified level in `L1` / `L2` / `L3` form.

Ask the user one of three responses: **approve** the document as written, **request changes** with specific rewording or substantive corrections, or **reject** the document outright. Ask one question at a time when iterating; do not bundle multiple questions into a single prompt.

If the user rejects the document, halt per the Halt conditions section.

### 17. Apply corrections if the user requests changes

If the user requests **substantive** corrections (rework of a Design decision, a different Components decomposition, an added or removed Card Slice, a new alternative considered, or a re-derivation triggered by a `blocker` or `serious` finding the user wants addressed), do not treat spec amendment as the default route. Run the correction loop as a real-time source-trace on the same `scaffold_card_id`.

Maintain `correction_round_count` for this architecture run. The initial compose/review pass is round `0`; each routed substantive correction increments the count by `1`. The correction loop has a finite retry cap of `3` on the same scaffold card.

For every substantive correction request, determine the actual origin from the evidence in hand:

- **`architecture-document` route** — the problem is in architecture reasoning, decomposition, traceability, slice boundaries, or design-review resolution while the verified bundle remains usable.
- **`verified-bundle` route** — the problem is in the research/audit facts or in a failure elsewhere that source-traces back to the verified bundle rather than the architecture document.
- **`spec` route** — the problem source-traces to the spec itself rather than to the architecture document or verified bundle.

Use the best-supported route from the document, review findings, user request, and pipeline state. Do not use a fixed mapping from problem type to route. Do not let the design reviewer own repeated-failure investigation or source-trace beyond the findings it already surfaced.

When `architecture_correction_pause == true`, pause before applying a routed substantive correction and ask the user whether to proceed with that correction round. When `architecture_correction_pause == false`, do not pause merely because a correction round is starting.

Construct a declared correction input for the affected stage as `correction_request_json`. This input must be explicit and auditable, not free-form prompt context. At minimum it contains:

- `round`: the incremented `correction_round_count`
- `origin`: one of `design-reviewer`, `owner-directed`, or `source-traced-upstream-failure`
- `routed_target`: one of `architecture-document`, `verified-bundle`, or `spec`
- `requested_change`: the substantive correction to apply
- `provenance`: the finding ID, user instruction, or failure trace that justified the correction

Then route by actual origin:

- **If route is `architecture-document`:**
  - Re-enter the already-verified compose stage in correction mode instead of editing `spec_path`.
  - Reuse the current `verified_level` and `audit_artifact_id` (compose's Step 2 re-fetches the audit and re-resolves the verified bundle from it on each compose invocation; no orchestrator-side bundle state to thread forward).
  - Dispatch the same compose profile selected in step 11 with these declared inputs: `spec_path`, `verified_level`, `scaffold_card_id`, `agent_id`, `audit_artifact_id`, `correction_request_json`, `prior_architecture_document_path` (the current `architecture_document_path`), and `prior_architecture_document_artifact_id` (the current `architecture_document_artifact_id`).
  - Then repeat steps 12 through 16 on the same scaffold card so the revised architecture document is re-verified and re-reviewed.
- **If route is `verified-bundle`:**
  - Do not send a compose correction request.
  - Re-run the pipeline from the research wave: repeat steps 6 through 16 on the same `scaffold_card_id` so research and audit produce a fresh verified bundle before compose runs again. When step 6 spawns research on this re-run, pass `force_remeasure: true` so the research agent suppresses its prior-bundle-reuse check and re-measures into a fresh V2 bundle (short-spec CL-009).
- **If route is `spec`:**
  - Do not edit `spec_path` inside `/architecture`.
  - Surface that the issue is spec-origin and hand it off to the external spec-modification path rather than using `/foundation` or an in-flow spec edit.
  - If owner input is required because the source-trace landed on the spec, report that explicitly to the user and stop the `/architecture` correction loop for this run.

If the same scaffold card reaches `correction_round_count == 3` without approval, do not keep retrying or dead-halt to the user by default. Hand the run off to the external investigator path and stop the local correction loop. The investigator handoff is automatic at the cap and is separate from the design reviewer. `/architecture` records the handoff by writing a scaffold-card note and activity log entry naming the round cap, the current routed evidence, and that an external investigator handoff is now required. Escalate to the user only when the external source-trace process determines that the issue is spec-origin.

If the user requests **minor** corrections (wording, a missed traceability row, a typo, a non-substantive rewording of a single sentence): apply the edits via `Edit` directly on the file at `architecture_document_path` (the exact path from step 13). Show the corrected document to the user and ask for approval again.

Iterate steps 16 and 17 until the user explicitly approves the document.

### 18. Commit the architecture document to git

Commit the file at `architecture_document_path` (the exact path captured in step 13, unchanged) to git on the current branch. Use `git add` on that exact path (not `git add .` or `git add -A`, which can pick up unrelated files), then `git commit` with a message naming the spec and the level (e.g., `Architecture for <spec topic> (L<n>)`). Do not commit the scaffold card's other artifacts — the bundle, audit, and design review are AgentBoard workspace artifacts, not git-tracked files.

### 19. Read the Card Slices section and create one workspace card per slice

Re-read the now-committed file at `architecture_document_path` (the exact path captured in step 13, unchanged). Locate the `## Card Slices` section. Each `### <Card title>` subsection within that section is a slice. Each slice contains these eight schema fields as bullets: Description, Allowed-touch list, Forbidden-touch list, Produces, Consumes, Verification scope, Depends on, Source decisions.

Create one workspace card per slice with a two-pass approach so `depends_on` edges resolve to real card IDs:

**Pass 1 — create the cards without `depends_on`.** For each slice, call `agentboard_create_workspace_card`:

- `board_id`: the board chosen in step 4.
- `title`: the slice's `### <Card title>` heading text.
- `description`: the full slice content — the eight schema fields copied verbatim into the card description. Downstream planning agents read this as the per-card `arch_slice`.
- `priority`: ask the user for a priority or default to `normal`.

Capture each returned card ID alongside its slice's title.

**Pass 2 — set `depends_on` edges.** For each card created in pass 1, read its slice's Depends on field. Resolve each cited slice title to the card ID captured in pass 1. Call `agentboard_update_workspace_card` with the resolved `depends_on` list. Slices whose Depends on field is `None` get no `depends_on` update.

### 20. Move the scaffold card to finished

Call `agentboard_update_workspace_card` on `scaffold_card_id` with `status: finished`. The scaffold card's four attached artifacts (bundle, audit, architecture document, design review) remain available on it as the audit trail of how the architecture was produced.

### 21. Summary to the user

Display this summary in the chat:

```
## Architecture Complete

**Spec:** the `spec_path` confirmed in step 3
**Architecture:** the exact `architecture_document_path` from step 13 (level: L<n>)
**App:** [name]
**Board:** [name] (ID)
**Cards created:** N
**Scaffold card:** [name] (finished — holds bundle, audit, architecture document, and design review artifacts)
**Design review:** N blocker / N serious / N minor finding(s); resolved or accepted by user before approval

| # | Card | Allowed-touch (count) | Depends on |
|---|------|-----------------------|------------|

**Next step:** Start a new session and run `/orchestrate` to begin the planning → review → implementation → audit pipeline on these cards.
```

Populate the table with one row per card created in step 19, ordered to match the order of the slices in the architecture document.

## Operating rules

- Do not write the architecture document yourself. Do not judge its design quality. Do not pick the level. Spawn agents, verify their outputs, display results to the user, and act on the user's decisions.
- Do not ask the user to approve the level. Do not offer level overrides.
- Do not create any workspace cards before step 19.
- Pass each subagent only the inputs that subagent's profile declares it consumes — no exceptions. Substantive corrections reach the affected stage only through declared correction-loop inputs and routed re-entry, never through undeclared prompt context and never through a silent `spec_path` edit.
- `audit_artifact_id` (the `ARCH_BUNDLE_AUDIT_V2` artifact's ID captured in step 9) is the single seam between the orchestrator and the downstream stages that consume the verified bundle: passed unchanged to compose at step 11 AND to the design reviewer at step 14 (the same value to both). The orchestrator never resolves the bundle and never embeds bundle JSON in any prompt — compose and the design reviewer each fetch the audit themselves and resolve the bundle by the audit's `any_discrepancy` branch.
- Bind every pipeline artifact (bundle, audit, architecture document, design review) by the exact ID captured via the snapshot-and-diff in steps 6/7, 8/9, 11/12, and 14/15 for that round. Never re-resolve any of them by a type-only lookup that could match a prior round's artifact after a step-17 re-run.
- Thread the single exact `architecture_document_path` from step 13 unchanged through review (step 14), display and edits (step 16), corrections (step 17), commit (step 18), and card creation (step 19). Never re-derive the document path by closest-match scanning.
- The `/architecture` correction pause is opt-in and off by default. It is separate from AgentBoard app blocking gates and must not mutate board settings.
- Ask one question at a time when iterating with the user on corrections.
