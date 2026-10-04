---
name: ss-trace-spec
description: Traces when an OpenSpec Requirement or Scenario was added, modified, removed, or renamed by searching current specs, archived deltas, and git history. Use this to answer "when and why did this behavior change" questions about a capability.
---

# Trace OpenSpec History

Reconstruct the history of a Requirement or Scenario by searching current specs and
archived deltas.

## Inputs

Required: the requirement or scenario text (or a close paraphrase) to trace.

## Process

1. Search current specs for the query text, e.g., using your repository search tool over
   `openspec/specs`.
2. Search archived deltas for the same query over `openspec/changes/archive`.
3. For each archive hit, read the surrounding context:
   - the archive directory name
   - which delta section it appeared in (ADDED / MODIFIED / REMOVED / RENAMED)
   - the Requirement heading
   - the proposal heading or summary, if present
4. If the project is under git, also pull the source-of-truth file history, e.g.
   `git log --oneline -- openspec/specs`.

## Output

Return a chronological summary covering:

- where the behavior currently lives
- which archived changes touched it, in order
- whether each touch added, modified, removed, or renamed it
- file paths worth reading next

Do not edit any files.
