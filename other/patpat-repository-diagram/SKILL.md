---
name: patpat-repository-diagram
description: Turn an explicitly requested idea, question, plan, or codebase into an interactive diagram. Create a self-contained HTML/SVG artifact from a user brief, repository evidence, or both, with five typed views and stable IDs for refinement. Use patpat-inspect for prose-only explanations and engineering skills for code changes.
metadata:
  patpat.ontology: '{"schema":"patpat-ontology/v1","mutation_level":"LOCAL_MUTATION","target_entity":"Artifact","requires_state":[],"produces_state":[],"verification_cmd":""}'
---

# Patpat Interactive Diagram

Before following this skill, apply the [skill state and mutation gate](../patpat-loop/references/operating-protocol.md#skill-state-and-mutation-gate).

Use this route only when the user explicitly asks for a diagram, map, visual explainer, or shareable view. Accept a brief, repository evidence, or both. Deliver a focused HTML artifact with editable typed JSON and SVG; preserve stable IDs when refining it. Patpat owns the schema, renderer, layout, viewer, and output contract. Do not install Archify or depend on its runtime. See [design references and attribution](references/spec-contract.md#selected-design-references) and [third-party notices](references/THIRD_PARTY_NOTICES.md). Before running a script, replace `<skill-root>` with the absolute directory containing this loaded `SKILL.md`.

## Scope and route

This skill creates diagrams; it does not edit application code, install dependencies, publish, or deliver externally. Use [patpat-inspect](../patpat-inspect/SKILL.md) for prose-only explanations and engineering skills for code changes.

Choose the smallest view that explains the subject:

| Type | Use for |
| --- | --- |
| `architecture` | Component ownership, calls, stores, and supported boundaries |
| `workflow` | Ordered work, gates, branches, retries, and outcomes |
| `sequence` | Calls and returns over time, including async messages |
| `dataflow` | Sources, transformations, stores, and consumers |
| `lifecycle` | States, transitions, retries, cancellation, and terminal outcomes |

If multiple views fit, choose one and state why in the summary. Ask only when that choice materially changes the story. Choose the destination from the request or repository convention; otherwise use `docs/diagrams/<slug>`. Never overwrite an existing artifact without an explicit replacement request.

For repository investigation, read [repository truth](../patpat-loop/principles/repository-truth.md), follow the [investigation playbook](../patpat-loop/playbooks/investigation.md), and use the [how-report contract](../patpat-inspect/references/how-report.md). Read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full for sensitive, security, cross-cutting, or material architecture questions. Do not load the router.

## Evidence and authoring

Separate user-brief claims from repository evidence. Brief claims are user-stated, not code-verified. For repository-backed diagrams, record the Git root, full HEAD, and dirty state; cite normalized relative paths and inclusive line ranges. `confirmed` means directly supported by the cited input, `inferred` means reasoned from it, and `unknown` needs a short reason. A line range proves only what those bytes show; never present static paths as observed runtime behavior. Never embed source snippets, credentials, tokens, or private remote URLs.

Author typed JSON outside the target repository. Set the title, summary, and labels in the user's language. Use the [schema and evidence contract](references/spec-contract.md#schema-evidence-and-layout-fields) and [typed graph rules](references/spec-contract.md#typed-graph-contract); use `render.py guide <type> --format text` for a concise type summary. Start with automatic graph layout. Inspect geometry diagnostics and the rendered view before adding explicit positions or route hints. Add hints only to fix a measured layout problem, never suppress a blocking warning, and group components only at evidenced boundaries. In workflows, keep the success or default path visually clear. Show a feedback edge only when the source supports recovery; keep unrecoverable failure, cancellation, and rejection as terminal outcomes. Evidence certainty describes claim support, not whether a step passed.

Add guided story views only when ordered exploration helps the reader. Story order does not prove causality or runtime impact. Keep titles and summaries clear, labels readable, route clearance generous, and controls compact. Use semantic shapes and line styles that convey meaning without color; omit detail and decoration that do not answer the request.

## Optional Python import map

Use the Python import analyzer only for an explicit dependency-map request. Send `--out-dir` to a location outside the repository. Run `python3 <skill-root>/scripts/import_graph.py --help` for its options. It parses imports without executing repository code or following symlinks; its edges are import dependencies, not calls or runtime behavior. Inspect the JSON report and sidecar before rendering. Report the selected roots/scope and any unresolved or ambiguous imports, skipped files, or limits; never present a partial inventory as complete. If the report says `no-resolved-repository-imports`, keep the report and stop; resource-limit failures produce no partial artifacts. Remove a temporary `.imports.json` with its source spec after review.

## Render and prove

Use the renderer shipped with this skill; do not substitute another renderer. Run `python3 <skill-root>/scripts/render.py guide --format text` and `python3 <skill-root>/scripts/render.py guide <type> --format text` when the supported schema or command details are unclear. The normal path is `validate` -> `finalize` -> `check`; pass `--repo-root` whenever evidence cites repository files. `finalize` checks the artifact and evidence, runs a local Chromium gate by default, and promotes only a passing output set through a recoverable transaction. Promotion replaces files one at a time, so readers may briefly see a mixed set. After interruption, automatic recovery proceeds only when ownership and required permissions can be proven; otherwise files remain untouched for manual review. Keep the renderer lock file while operations may run. Never request `--overwrite` without the user's replacement request.

Use schema 2 when the request needs interactive viewer behavior; use schema 1 when the user requests a static artifact. Schema 2 embeds Patpat's trusted offline viewer. For the relevant task, read the [finalization and browser contract](references/spec-contract.md#finalization-and-browser-checks), [viewer behavior](references/spec-contract.md#interactive-viewer), [preview contract](references/spec-contract.md#preview), or [comparison contract](references/spec-contract.md#architecture-comparison). `--public-source-links` is opt-in and sends direct, unauthenticated GitHub requests without configured proxy or Git credentials; links are emitted only for evidence matching the exact committed snapshot. Use `--no-browser` only when the browser gate cannot or should not run, and report that browser behavior remains unverified.

Open the final artifact when interaction is part of the request and a browser is available. Exercise the requested controls and inspect the screenshot separately. A render receipt proves the checked artifact loaded and its captured layout; it does not prove semantic accuracy, interaction behavior, or visual clarity. For browser captures, viewer features, preview, or architecture comparison, discover current flags with `python3 <skill-root>/scripts/render.py <command> --help`. Use `compare` only when the user asks to inspect structural change between prior architecture artifacts; it does not infer runtime impact, risk, compatibility, or merge safety. Use [patpat-impact](../patpat-impact/SKILL.md) for downstream risk. Remove temporary specs, screenshots, receipts, and preview servers unless the user requested them. Do not report checks you did not run.

## Report

Return links to the HTML and editable JSON; include SVG and receipt links when useful. For a chat-only visual, return editable source and state which render checks were unavailable. For repository or mixed evidence, name the exact revision and distinguish committed files from working-tree files. For brief-only output, say the claims came from the user's brief and were not code-verified. Report semantic review, structural checks, browser render checks, visual inspection, and unresolved unknowns separately.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
