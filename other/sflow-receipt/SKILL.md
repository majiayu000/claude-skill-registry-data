---
name: sflow-receipt
description: Replay compact evidence for a submitted phase.
argument-hint: "[WORK-ID]"

---
# Show a Singularity Flow evidence receipt

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Run `singularity-flow receipt show --work-id <WORK-ID> --json`, using the supplied Work ID or the attached Story. Report the exact phase and generation, source commit, changed-path count, requirement coverage, checks, approvals, governed context, publication state, review-packet hash, and receipt hash. Never turn unavailable evidence into zero or success. If the user asks for a review-ready form, run the same command with `--markdown` and display the complete bounded Markdown.
