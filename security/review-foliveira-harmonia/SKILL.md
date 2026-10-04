---
name: review
description: Harmonia review stage - hierarchical review under the review lead with gates and receipts. Use ONLY when explicitly invoked as /harmonia:review.
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.
Read the `review` stage from `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` (already in context if the flow runner loaded it - do not re-read) - the panel roster and lens name list live there and are authoritative - do not hardcode them; each lens file under `${CLAUDE_PLUGIN_ROOT}/core/lenses/` carries its own trigger rules in frontmatter, which are authoritative for dispatch.

1. Workspace: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh resolve --repo .` (later stage: never mints; surface ambiguity or no-active-task and stop).
2. Gates before judgment:
   - `bash ${CLAUDE_PLUGIN_ROOT}/bin/check-criteria.sh --run --workspace <ws> --repo .` - executes every `- run:` criterion the scope declares, from the repo root, and prints the whole set it ran with each command verbatim. A failing criterion FAILS the review - this gate is hard; exit 3 means there was no scope declaration to run. Keep the order: the receipt audit passes only once a `criteria-run` receipt fresh for this tree is on disk.
   - `bash ${CLAUDE_PLUGIN_ROOT}/bin/verify-receipts.sh --workspace <ws> --repo .` - missing or stale receipts FAIL the review.
3. Dispatch the reviewer (review lead) by path with every artifact this stage declares `in`, plus the rest of the lead's charter `consumes:` list - both are authoritative and neither is restated here. The lead convenes the panel declared by this stage, dispatches lenses whose frontmatter triggers match the diff (security auto-fires on its fixed list), runs seats per `${CLAUDE_PLUGIN_ROOT}/core/patterns/panel.md` with model-diverse dispatch, and writes one attributed `verdict.md` to the workspace.
4. A test-immutability violation recorded in the workspace is treated like a missing receipt: the review fails.

Pass workspace paths, not prose recaps. Orchestrate only.
