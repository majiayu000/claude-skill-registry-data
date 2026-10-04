---
name: sci-research-manager
description: Coordinate long-running research state, evidence, project literature interfaces, experiment lifecycles, direction decisions, claim reconciliation, submission audits, and provenance-safe maintenance. Use when a task changes or audits project state, evidence strength, experiment protocol, research direction, or cross-artifact consistency. Do not use it as an extra wrapper around ordinary paper reading, known-paper intake, manuscript prose, or unchanged task execution. This is the primary research-state owner and accepts bounded typed handbacks from specialists.
---

# SCI Research Lifecycle Manager

Be the single owner of research state and evidence transitions. Specialists may return bounded content; they do not become parallel workflow owners.

An owner is a responsibility of the current primary agent, not an additional agent or mandatory skill call. Direct specialist requests may finish with the user without opening this coordinator. Enter lifecycle coordination only for an actual project decision, state transition, evidence promotion, or cross-domain integration; never bounce a finished handback between owners. If a specialist is unavailable, use an available equivalent capability within the same evidence and permission boundaries, or report the specific missing capability. Do not install dependencies or weaken verification implicitly.

## Respect authority and existing authorization

- Follow the user request and applicable `AGENTS.md`, `CLAUDE.md`, repository rules, schemas, and templates. This skill never weakens a stricter local rule.
- Distinguish inspection from mutation. Preserve unrelated changes, original artifacts, timestamps, Git boundaries, and historical IDs; never reset, auto-commit, reformat, delete, publish, migrate, or start costly work as a side effect.
- Reuse authorization that still covers the same action, target, cost class, and recipient. Ask again only when one of those materially changes or the action is otherwise outside scope.
- External disclosure of AI, models, agents, providers, plugins, automation, or other work tools remains `not_authorized` unless the user separately approves the exact wording, location, recipient/platform, and version. This includes adding, retaining, changing, removing, uploading, or publishing disclosure text. Verify external requirements read-only and keep internal provenance out of external artifacts by default.

## Choose the lightest operating intensity

These labels guide behavior; do not add them to project schemas. Persist only the project's approved lifecycle vocabulary.

| Intensity | What is enough | What does not start automatically |
|---|---|---|
| Discussion | Existing project context plus the exact source or artifact needed to answer one question | Durable records, paper intake, remote work, downloads, probes, goals, or a full audit |
| Targeted check | A bounded novelty/evidence query, decisive primary-source sections, and one compact comparison | Field-wide review, automatic registration of every hit, or an experiment |
| Minimal probe | One falsifiable uncertainty, frozen small protocol, raw output, and a predeclared decision gate | Parameter sweeps, follow-on runs, or formal-claim promotion |
| Formal experiment | Full protocol, provenance, monitoring, verification, experiment-card/index closure, and claim calibration | Unplanned expansion after an ambiguous result |
| Submission audit | Frozen package inventory and complete cross-artifact, policy, and disclosure checks | Repairs, upload, publication, or final submission without their own authorization |

Classify actual project work with the established stage:

`idea_exploration / minimal_probe / formal_experiment / result_analysis / paper_writing / submission_prepare / maintenance`

A maintenance request is scoped to the named assets; it is not permission for a whole-workspace audit.

## Ground once, then follow deltas

Read root-to-target rules, root and project `README`/`HANDOFF`, then the smallest relevant index, note, card, or raw artifact. Stop when the task is grounded. Before writes, inspect the relevant Git/worktree state and protected originals.

Maintain an in-task context receipt: paths or source IDs already read, their relevant version/hash/mtime when identity matters, the question each answered, and unresolved items. Reuse it across steps and pass only the needed entries to a worker. Do not manually reload unchanged Skill files, manifests, tool inventories, generic instructions, or project entrypoints merely to regain confidence. On resumption, inspect the state delta and live handle first. This economy never permits skipping a decisive primary source or raw artifact.

Ask tools for the narrowest useful output: identifiers, status, selected fields, exact sections, error tails, or paths. Keep full logs, catalogs, tables, and paper text on disk and reopen a specific portion when needed. Truncation must remain visible; it cannot turn missing evidence into success.

## Put literature before avoidable investment

Pure concept naming, explanation, or brainstorming stays in Discussion unless answering it requires a source. Once the request asks whether a method is novel, feasible, worth pursuing, worth testing, changes a signal's role, or justifies costly expansion, read [literature-decision-check.md](references/literature-decision-check.md). Do the nearest-prior screen before downloads, dataset preparation, or analysis whose only purpose is to justify that proposal, unless an asset fact is needed to formulate the comparison. Reuse a still-applicable comparison. Ordinary reading, known-paper intake, bug fixes, and unchanged approved protocols do not repeat this gate.

A close precedent changes the question; it does not by itself invalidate the whole direction. Report substantive overlap, information/protocol differences, the remaining testable delta, and what evidence would distinguish it. A failed proxy or one negative run constrains only the tested formulation.

## Execute, delegate, and wait economically

- Prefer a deterministic command or existing script for inventory, hashing, conversion, extraction, transfer verification, and other mechanical work.
- Delegate only when allowed by the user and applicable rules, and when the task is independent and the expected saved work exceeds handoff plus review. Give exact inputs, allowed actions, exclusions, coverage boundary, completion condition, and a compact return schema. Do not delegate merely to wait, reread the same context, or obtain a second broad opinion. The primary owner checks decisive evidence and never accepts a conclusion broader than the worker's checked scope.
- Bundle a mechanical download/verify/execute/receipt chain when it has one owner and one safe completion condition. Do not split one live handle between the primary owner and a worker.
- Prefer event completion when available, but do not assume notifications or a particular model exist. Otherwise poll the same task identity at intervals justified by its ETA or observed progress, lengthen the interval when unchanged, and do useful independent work between checks. A timeout is an observation, not a restart signal.
- Record remote truth before detaching: scheduler/job ID or remote PID, command identity, output path, and success/failure marker. A local SSH, PTY, uploader, or polling handle ending does not prove the remote process ended. Before restarting or changing transport, query that identity. If no identity was recorded, perform a bounded remote lookup limited to the expected user, command signature, and output path; treat an unresolved match as potentially active rather than restarting. After cancellation, verify the remote process/job and relevant open output handles are gone. Preserve partial files and mark them incomplete.
- Do not wait forever. Stop an active wait when another check has no decision value until a named event or reasonable ETA; return the handle, last verified progress, next eligible check, and restart prohibition. If the user explicitly asks for continuous monitoring, use the available monitoring mechanism with the same single-owner rule.

## Protect scientific quality

Use this evidence order: raw artifact + exact script/config/commit + frozen protocol; verified card or reproducibility record; canonical registry/claim map/HANDOFF; session summaries and old indexes; filename inference or memory. A weaker source never overwrites a stronger one. Use recency only within the same evidence level and lineage; a newer summary cannot replace verified raw evidence.

When results conflict, reopen the decisive raw artifact and its protocol even if this costs more context. State both claims, locate the mismatch in data, metric, selection rule, code identity, or information access, and mark unresolved evidence explicitly. Token economy is not a reason to average incompatible numbers, hide failure, relax statistics, or promote a test-selected result.

For a direction decision:

1. State the scientific question and separate observation from inferred cause.
2. Compare the closest literature and existing artifacts before choosing the cheapest check that distinguishes live explanations.
3. Freeze information access, data/split, metric, baseline, selection rule, controls, success gate, and stop gate before a run.
4. Afterward state what is supported, unsupported, weakened, or still ambiguous. Preserve valid negative evidence at its tested scope.
5. End with one existing decision value: `continue`, `redirect`, `reference_only`, `stop`, or `needs_literature`; do not turn a resource stop into mechanism impossibility.

Use claim strength `main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported`. Keep lifecycle stage, experiment status, evidence status, claim strength, and direction decision separate. A completed run is not automatically verified, canonical, successful, or paper-facing. Freeze seeds, exact config/command, run/result path, and code commit as part of the protocol. Close locally as `raw -> card -> project EXPERIMENTS/index`; preserve existing `EXPERIMENT_INDEX.csv/.md` as the sole editable authority when already established, rather than creating a second source; update a shared registry only for canonical promotion/replacement or a changed evidence warning, and update `HANDOFF` only when stage, central question, blocker, active execution, canonical route, ownership, or next action changes.

## Load detailed workflows only when the task enters them

- Project Source-ID views, reading depth, LiteratureClaim notes, or project literature audit: [project-literature-interface.md](references/project-literature-interface.md).
- Experiment design, execution tracking, analysis, promotion, supersession, or audit: [experiment-library-lifecycle.md](references/experiment-library-lifecycle.md).
- A task truly crossing literature, experiments, and manuscript claims: [research-library-workflow.md](references/research-library-workflow.md).
- Manuscript lifecycle coordination: [manuscript-stage-workflows.md](references/manuscript-stage-workflows.md), then `academic-manuscript-writing`.
- Final package/readiness review: [final-submission-audit.md](references/final-submission-audit.md).
- Creating or materially restructuring lifecycle documents: [artifact-contracts.md](references/artifact-contracts.md).
- Specialist selection only when unclear: [specialist-routing.md](references/specialist-routing.md).
- Maintenance closeout only for checks relevant to changed assets: [audit-checklists.md](references/audit-checklists.md).
- If a project lacks status vocabulary: [research-state-model.md](references/research-state-model.md); otherwise do not load it.

Global search, PDF identity, metadata, version/alias, deduplication, and BibTeX/RIS belong to `sci-literature-manager`. Paper mechanisms and decisive sections belong to `sci-paper-reader`. Prose, statistics, figures, and document production go only to the smallest matching specialist. A typed handback proposes no new claim, protocol, or state transition unless the lifecycle owner verifies it.

## Use portable maintenance tools only when needed

Use `scripts/provenance_guard.py` for approved path-sensitive moves and `scripts/audit_workspace.py` for bounded read-only structural checks. Deletion and migration remain separate authorizations; preserve originals and a rollback mapping.

Use `scripts/audit_research_libraries.py` for a read-only first pass over literature inventory/catalog drift, declared PDF counts, required library entry points, project namespace links, and result-registry links. Pass explicit root-layout options for nonstandard projects, `--allow-value FIELD=VALUE` for documented stricter vocabularies, and `--map-value FIELD=ALIAS:CANONICAL` when a custom value must participate in canonical completion, verification, or claim-safety gates. Unmapped custom experiment states are treated conservatively and cannot weaken evidence gates. Its output detects structural drift only; it does not verify scientific interpretation, citation relevance, or numerical reproducibility.

Use `scripts/scan_external_disclosures.py` to inventory possible workflow-tool disclosures in an external package. Exit `0` means no candidates were found in fully scanned supported content, `1` means candidates require author review, and `2` means the scan was incomplete or the input invalid. A clean scan never grants disclosure approval or replaces rendered-file and portal review.

Keep audit reports internal until reviewed for release. The disclosure scanner omits absolute input roots by default, but its filenames, hashes, and matched context may still contain sensitive manuscript metadata. Other legacy audit/provenance reports may include supplied filesystem roots.

## Write and close only on events

One fact has one durable owner. When durable records are required, reuse at most one working note and one run record per question; do not create parallel plan, status, audit, and handoff documents for the same unchanged fact. Discussion and interim waiting stay in conversation or an authorized scratch area. Required indexes receive only semantic state changes.

Validate what changed, then broaden only for a concrete risk. Recheck relevant links, symlinks, Git state, protected timestamps, evidence registration, and unresolved conflicts. Report the outcome, evidence checked, files changed, checks run, unchecked scope, limitations, and safest next action. Do not claim measured token or quota savings without comparable telemetry, and never equate an aggregate token counter with billing.
