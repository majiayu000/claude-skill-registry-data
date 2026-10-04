---
name: implement
description: Harmonia implement stage - red-green build, tests leading, under the criteria gate. Use ONLY when explicitly invoked as /harmonia:implement.
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.
Read the `implement` stage from `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` (already in context if the flow runner loaded it - do not re-read) - agents, artifacts, gates, and the red-green `loop` definition (including `max_rounds`) are authoritative; do not hardcode them.

1. Workspace: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh resolve --repo .` (later stage: never mints; on ambiguity or no-active-task, surface the script's message and stop).
2. Criteria gate: `bash ${CLAUDE_PLUGIN_ROOT}/bin/check-criteria.sh --workspace <ws> --repo .` - refuse to start while it fails (Goal-Driven Execution). It writes its receipt.
3. Red-green loop, at most `max_rounds` rounds:
   - Dispatch the test-engineer: red-first for behavior; cover-first at gaps it finds by reading the diff against the tests (a green-on-arrival test at a gap completes the round - skip the implementer turn).
   - `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh record-test-hashes --repo .` after every test-engineer turn.
   - Dispatch the implementer to go green; it may not edit tests.
   - `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh verify-test-hashes --repo .` before accepting the round - a violation fails the round and is recorded for the review lead.
   - Exit when the test-engineer reports no behavior left to pin and no changed code left unexercised; on the cap, exit incomplete and record the disagreement in the workspace.
4. Producer duties on completion: write `boundary.md` and `diff-summary.md` to the workspace.

Pass workspace paths, not prose recaps. Orchestrate only.
