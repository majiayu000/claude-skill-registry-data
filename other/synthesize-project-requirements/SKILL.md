---
name: synthesize-project-requirements
description: Create one evidence-backed project requirements and gotchas note from cumulative notes, current repository state, git history, and human-authored messages found with AI Session Search. Use when asked to "go through all the notes", "recover project requirements", "mine prior sessions", "collect requirements and gotchas", "make a project memory note", "prepare a project handoff", or preserve decisions and corrections for a handoff. Do not use for a one-off log summary or direct factual answer unless durable project memory or a handoff is requested. Default to the project's notes directory; publish to its documentation only when requested and add a guidance-file pointer only with permission.
license: Apache-2.0
metadata:
  version: 0.0.4
---

# Synthesize project requirements

<purpose>

Create a single current requirements note whose claims can be checked against repository or session evidence. Read [references/compatibility-and-validation.md](references/compatibility-and-validation.md) before claiming runtime support or release readiness.

The portable core assumes only a Markdown-capable skill host and relative package resources.
`agents/openai.yaml` is optional Codex/OpenAI display metadata. Record each target host's discovery,
invocation, reload, reference loading, and task-test status before claiming compatibility; unknown
is better than an unsupported claim.
The note may serve as a project handoff: make current status, open decisions, known gotchas,
verification commands, and the next safe action obvious to a new maintainer without requiring
access to private session transcripts.

</purpose>

<workflow>

## 1. Set scope and destination

Identify the project root, relevant time range, notes directories, current guidance files, and requested output. Default to the project's `notes/` directory and a collision-safe date-prefixed filename ending in `project-requirements-and-gotchas.md`. Never overwrite an existing note.

Use `assets/project-requirements-template.md` as the output skeleton. Remove empty optional sections rather than shipping placeholders.

## 2. Inventory project evidence

Read project guidance first. Enumerate markdown and text notes with a fast file listing, then classify each as current evidence, historical context, generated output, duplicate, or superseded. Follow direct links needed to interpret a requirement; do not recursively read unrelated archives.

Inspect current code, tests, configuration, and git history for claims that describe present behavior. A note proves what someone recorded, not that the implementation still matches it.

## 3. Search session history

Use AI Session Search instead of raw provider transcripts:

1. Search root user sessions by project path and short phrases for requirements, corrections, failures, defaults, "must", "should", "forgot", "gotcha", and named features.
2. Expand selected results with their session ID and message sequence.
3. Search later messages for corrections or reversals before accepting an earlier statement.
4. Treat subagent `role=user` messages as delegation prompts, not direct human quotes.
5. Treat mirrored or repeated provider records as correlated evidence.
6. Record the query, scope, and whether pagination was complete. A bounded search supports a bounded claim only.
7. If AI Session Search is unavailable, record the limitation, use only locally checkable evidence,
   and do not silently read raw provider transcripts or claim exhaustive history.

## 4. Code and reconcile the evidence

Assign each item one or more qualitative codes:

- requirement: desired behavior or artifact;
- constraint: boundary, prohibition, compatibility rule, or default;
- gotcha: repeated failure mode or non-obvious interaction;
- correction: later user message that changes prior direction;
- rationale: why a choice matters;
- verification: observable proof or command;
- unresolved: conflict, ambiguity, or missing evidence;
- superseded: historically useful but no longer current.

Normalize equivalent wording under one stable ID while preserving exact quotes in its evidence entries. Prefer the latest explicit correction, but retain the superseded statement and explain the transition. Never convert an agent's proposal into a user requirement without user acceptance or independent repository evidence.

## 5. Write one decision-ready note

For each requirement or gotcha, state:

1. the normalized claim and status (`current`, `proposed`, `superseded`, or `unresolved`);
2. scope, qualifiers, defaults, and affected components;
3. rationale or failure mode;
4. supporting evidence with file path and line, commit, command output, or `(provider session ID, message sequence, timestamp)`;
5. an exact user quote when user intent is material;
6. the smallest verification that would prove the current implementation complies.

For academic, scholarly, or publication work, apply applicable institution, venue, and licensing rules:
cite direct links, preserve attribution, distinguish quotation, paraphrase, and inference, disclose
material generated assistance when required, and never fabricate references or present generated text
as original research. Separate measured evidence, policy or requirement, and inference. Include an
evidence-method section with search scope and limitations, a conflict ledger, and unresolved
questions. Maintain a linked reference log with title, author or organization, URL, access date,
supported claim, and limitations.

## 6. Verify and publish conservatively

Cross-check every summary row against its evidence. Run a cold-reader pass for undefined project terms, missing antecedents, stale paths, and assumed access. Confirm the output contains no secrets or private transcript content unrelated to the project.

Treat `notes/` and guidance-file names as defaults, not required paths. If the result will leave the project boundary, remove unrelated local paths, provider identifiers, personal names, and transcript text; retain only the evidence needed to support the project claims.

Capture the starting file inventory and distinguish pre-existing changes from paths created or modified by this run. Never clean unrelated worktree changes to satisfy a completion check. If measured, report note size, evidence volume, references read, and relevant tool/runtime cost; otherwise mark those values unknown.

Keep the result in `notes/` by default. If the user asks to promote it, create or update the agreed docs file without deleting the evidence note. Only after explicit permission, add one brief line to the nearest applicable `AGENTS.md`, for example:

```markdown
Project requirements and gotchas: [docs/project-requirements.md](docs/project-requirements.md).
```

Do not add an `AGENTS.md` pointer to a provisional notes file unless the user explicitly requests that exact pointer.

</workflow>

<output_contract>

Report the note path, evidence sources searched, search bounds, requirements and gotcha counts, conflicts or unresolved questions, validation performed, and whether any docs or `AGENTS.md` file changed. Do not claim that session history or project notes were exhaustive unless every relevant page and file was actually read.

</output_contract>

<examples>

## Examples

- In scope: “Go through this project's notes and prior user sessions and write one requirements and gotchas note with evidence.” Produce a new collision-safe note and leave docs unchanged unless authorized.
- In scope: “Prepare a handoff for this project from its notes and prior sessions.” Produce the same evidence-backed note, with current status, unresolved items, verification commands, and next safe action made explicit.
- Out of scope: “Summarize this one log.” Do not synthesize durable project memory unless the user asks for it.
- Publication boundary: promote the note only with explicit permission, retain the evidence note, and remove unrelated private transcript details before sharing it.

</examples>
