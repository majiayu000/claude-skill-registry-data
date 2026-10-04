---
name: scoville-handoff
description: Create one compact, factual continuation prompt for an explicitly requested transfer to another agent or session, including Scoville Handoff or "handoff to a new session". Do not activate for ordinary summaries, shortening, low context, wrapping up, or ending a session.
compatibility: "Any Agent Skills host that can read explicitly named or already established task sources. Optional read-only version-control inspection (git). No scripts, no network, no subagents. Developed for Codex and Claude Code; other hosts untested."
---

# Scoville Handoff

Give the receiver accurately labeled context to continue safely from one
copy-ready snapshot. An explicit transfer applies even when work is empty,
completed or not started. Without a transfer request, perform the requested
task without a handoff. If future reuse is requested but transfer intent is
unclear, ask one question before reading sources or producing a handoff.
When asked to explain or assess a hypothetical handoff, answer that question.
Produce the continuation artifact only for a requested transfer of an actual
task.

## Read within the transfer scope

Any already required and authorized pre-transfer update belongs to its active
owner, such as Plan for Step status, and must finish before Handoff starts.
The transfer request grants no additional editing authority.

Use task facts already established in the conversation. Additional reads are
limited to sources explicitly named or already established as task sources in
the conversation, optional read-only version-control inspection, and the
[continuation template](assets/continuation-prompt.md). Do not search for more
sources. Throughout this workflow, do not advance the task: no edits, builds,
tests, probes, dummy or other task commands, unrelated reads, stat or list
operations, or external effects.
Missing facts do not authorize additional actions.

For each source, retain its exact path and whether the read was complete,
partial or failed. Finish a truncated read through its missing range or cursor.
Retry a failed range once only if the error is plausibly transient. Stop on no
progress or repeated failure; explicit user read limits take precedence.
Complete permitted recovery before rendering rather than assigning that read
to the receiver. After recovery stops or a read limit prevents it, preserve the
usable facts and record recovery, gaps and unread ranges beside that source.
A partial source is not wholly unavailable.
Conflicting source revisions and material unread ranges remain explicit
blockers for receiver verification.

## Preserve continuation facts

Keep the handoff as short as possible and only as long as necessary. Necessary
facts let the receiver continue correctly without hidden context. Select the
relevant continuation facts below; omit repetition and history that no longer
affects the remaining work.

Capture the goal, deliverable, acceptance, scope and authority, canonical
owners, user-owned changes, accepted decisions, active work and running handles,
observed evidence and its limits, blockers, hazards and next safe action.
Preserve exact IDs, paths, commits, URLs, commands, errors, quoted decisions,
assumptions, unknowns and time-sensitive details where needed for continuation.
Transfer known material facts, not just pointers or instructions to reread them.
The handoff request itself is not a task decision. Keep preferences and proposals
distinct from requirements and accepted decisions.

Use `unknown` for missing information and `none known` when no instances are
known, such as no known blockers. Neither proves absence. Set `Status:
not_started` only when the conversation or an explicitly named or already
established task source establishes it; otherwise a missing status stays
`unknown`.

For file-based work, use the task working directory established by the
conversation or an explicitly named or already established canonical project
source. A task repository already verified during the work is sufficient; the
user need not name it again. If no task location is established, include
`Working directory: unknown`. Runtime CWD alone does not establish the task
location. Include temporary workspace or host state only when established as
task state.

Replace every secret value with `[redacted]` before composing any response,
including warnings, quotations and redaction instructions. Keep a variable name
when needed, never its secret value.

For a tight output limit, remove repetition and unrelated history first, then
shorten explanations. Preserve authority, ownership, hazards, evidence limits
and the safe first step. An explicit lossless request preserves every in-scope
non-secret fact. If the required content still cannot fit, return only a concise
size-conflict explanation and request a larger limit.

## Compose and check the prompt

Fill the continuation template, keeping its four H2 sections, the meaning of
every Receiver Instruction and three Resume Steps. Use the user's requested
output language, otherwise the conversation language. Translate headings,
labels and Receiver Instructions consistently; preserve technical identifiers,
literal markers such as `unknown`, and exact quotations except secret values.
Use one outer Markdown fence with at least four backticks and more backticks
than any run inside the prompt; match its opening and closing length, including
when saving the artifact to a file.
Include every Objective field. Under State, always preserve Status and the
required continuation facts, including relevant unknowns. Other template labels
are optional; omit empty or inapplicable categories. Name each source once beside
its facts and identify conversation facts as such. Repeat a fact only when a
hazard or first step needs it.

Step 1 resolves the first blocker, otherwise recovers in-flight work, otherwise
states the next safe action. Make the remaining steps concrete and end with an
observable completion criterion. Active or incompletely accepted work names its
decisive next check. For completed work with current evidence, the three steps
cover only checking current state, reconciling contradictions and confirming
no material mismatch. Do not invent more work or repeat a current check to fill
a step.

Compare the full prompt with the captured facts and sources. Check required
facts, exact identifiers, source attribution, Objective fields, Receiver
Instructions and the first safe step. For a lossless request, check every
in-scope non-secret fact. Correct omissions or contradictions before returning
exactly the fenced artifact, with no surrounding text. Leave no placeholders,
secrets, invented facts or tool details used only to prepare the snapshot.

Handoff owns the snapshot.

This Skill works independently. Other Scoville Skills are optional. Use an
available, active sibling only for its applicable concern; do not install,
simulate or require an absent sibling. Honor explicit user exclusions.

Family owners, in suite order:

- `scoville-code`: engineering scope, implementation, risk, and validation.
- `scoville-plan`: durable Plans, Work Items, Decisions, and lifecycle state.
- `scoville-ui`: framework UI implementation and acceptance, including supported WordPress admin surfaces.
- `scoville-handoff`: active-work transfer.
- `scoville-project-context-cleanup`: requested project-rule and index wording, information quality and structure.

Preserve active sibling state in the snapshot.
