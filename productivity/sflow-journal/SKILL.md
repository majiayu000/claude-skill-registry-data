---
name: sflow-journal
description: Review and manage the private machine-local My Work journal.
disable-model-invocation: true
argument-hint: "[today|refresh|settings|pause|resume|delete|export|doctor]"

---
# Local work journal

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

The journal is advisory return memory. It is never governance evidence, approval authority, a productivity score, or a remote source of truth.

1. With no requested action, run `singularity-flow journal today --json`. Explain that the result is stored locally and never pushed.
2. Use `singularity-flow journal refresh --json` only after the user asks to refresh local facts. It reads local Git state without fetching, pushing, or contacting a remote.
3. Use `singularity-flow journal settings --json` to inspect capture. Change mode, retention, or time zone only after showing the exact proposed settings and receiving explicit confirmation.
4. `singularity-flow journal pause` and `singularity-flow journal resume` change only future local capture. They do not alter governed work or delete history.
5. For day deletion, require the date twice: `singularity-flow journal delete --date YYYY-MM-DD --confirm YYYY-MM-DD --json`. For all history, require the exact phrase `DELETE LOCAL JOURNAL`.
6. Export only a reviewed summary, never raw events. The CLI refuses export inside a registered workspace so it cannot be staged accidentally.
7. Preserve refusals and diagnostics verbatim. Never describe locally observed remote-tracking refs as a live remote check.

Do not infer work duration, effort, attendance, or individual performance from journal records.
