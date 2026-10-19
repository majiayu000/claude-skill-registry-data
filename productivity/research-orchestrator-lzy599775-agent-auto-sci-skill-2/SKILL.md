---
name: research-orchestrator
description: Route substantive academic and scientific research goals through the current Agentic Research Workflow source of truth. Use for research planning, literature reviews, paper or method analysis, data-analysis planning, paper reproduction, manuscript evidence review, citation verification, figure planning, research idea evaluation, method design, and scientific workflow organization. Do not use for casual conversation, simple arithmetic, generic translation, or unrelated software questions unless repository research rules are materially needed.
---

# Research Orchestrator

Use this Skill as a thin cross-surface router. Retrieve current rules from GitHub, load only task-relevant context, select a specialist workflow or Skill, and report concise QC. Do not duplicate the repository manual here.

## Establish the workflow source

Use `Lzy599775/agent-auto-sci-skills` as the authoritative workflow repository.

- Use `main` for released work. Use an unmerged candidate only when the user explicitly selects that reviewed ref; report it as a candidate.
- Retrieve `docs/version.md`, `AGENTS.md`, `ARCHITECTURE.md`, and `docs/workflows/index.md` at the start of a substantive workflow.
- Report the workflow version and ref used.

Read [references/source-retrieval.md](references/source-retrieval.md) for GitHub retrieval, fallback, and version-drift behavior.

## Route the goal

Infer one primary route from the intended decision or deliverable:

- papers, literature, DOI, citations, Zotero, or synthesis -> literature;
- reproduce, replicate, reimplement, or benchmark -> paper reproduction;
- methodology / research design, causal identification, estimands, bias, sampling/measurement validity, inference assumptions, or model appropriateness -> methodology, using `agent-auto-sci-methodology`;
- cleaning data, fitting models, executing statistics/regression, or evaluating prediction performance -> data analysis;
- drafting, rewriting, or restructuring manuscript sections -> manuscript writing;
- whether a citation supports a statement -> citation-claim audit;
- plot, map, table, chart, or figure -> figure workflow;
- novelty, feasibility, research topic, or new idea -> research idea evaluation.

Do not require the user to name the workflow. Load the selected file under `docs/workflows/`, then only the standards and specialist Skills required to complete the task.

Select by the scientific decision or deliverable, not prompt keywords. Critiquing Methods
validity uses methodology; rewriting its prose uses manuscript writing. Reproducing a published
result uses paper reproduction; novelty/feasibility uses research idea evaluation, with
methodology as needed. Artifact identity checks alone use literature plus the artifact protocol.
A standalone resource preflight uses data analysis in `preflight_only` mode without starting
computation. The canonical router's `ROUTING_DECISION_CONTRACT_V1.json` records these choices.

There is no default discipline, dataset, or paper. Domain specialists are optional and loaded
only for the current task. Research questions, methods, data, results, figures, papers/Zotero
collections, and manuscript/exemplar state stay in the corresponding private project.
Resolve identity before private-state access; an unidentified task never inherits a prior
project. Ordinary method consultation and micro-edits do not read manuscript exemplar state
or initialize Master20/Core3.

## Automatic companion routes

- Online paper search automatically invokes `PAPER_ARTIFACT_AVAILABILITY_PROTOCOL_V1` for user-facing, qualified, shortlisted, evidence-table, exemplar, method-comparison, and synthesis papers. Raw monitor discovery does not trigger deep search; qualified candidates get Level 1, and reading/exemplar/reproduction records get Level 2. Network failure is not a negative finding.
- Substantive manuscript writing automatically invokes the isolated per-manuscript workflow under the unique `agent-auto-sci-scicomm` owner. Read that manuscript's authoritative private state and versions; never infer from memory or reuse another manuscript's corpus/artifact status. Micro-edits skip heavy initialization.

## Execute with evidence discipline

Apply these minimal fallback invariants on every surface:

- prioritize evidence integrity, reproducibility, and traceability;
- prefer original and authoritative sources;
- never invent citations, identifiers, source text, methods, values, results, or availability;
- separate source-reported fact, derived result, and inference;
- keep claim strength at or below evidence strength;
- preserve explicit unknown, unavailable, unverified, and conflicting states;
- treat Zotero as bibliographic/PDF source of truth when available;
- treat Research Vault records as derived knowledge, not original evidence;
- require explicit approval for destructive, publishing, submission, external-message, merge, force-push, private-data, or destructive Zotero actions.

Read [references/routing-and-qc.md](references/routing-and-qc.md) before finalizing the route or reporting completion.

## Use specialists

Prefer an installed specialist Skill when its scope matches. In particular, use `literature` for evidence-traceable literature search, extraction, synthesis, Zotero work, and citation-support audits. Specialist Skills implement procedures; this Skill owns orchestration and cross-surface source retrieval.

## Handle unavailable GitHub context

If the repository cannot be retrieved:

1. State `WORKFLOW_SOURCE_FALLBACK_USED`.
2. Identify the intended ref and files that could not be verified.
3. Apply only the minimal invariants in this Skill.
4. Avoid claiming the fallback is current or complete.
5. Continue low-risk work when valid; stop only at genuine access, legal, destructive, or material scientific-choice boundaries.

## Return

Report the selected route, workflow repository/ref/version, repository files loaded, specialist Skills used, evidence and uncertainty state, artifacts created, QC results, fallback status, and unresolved blockers.
