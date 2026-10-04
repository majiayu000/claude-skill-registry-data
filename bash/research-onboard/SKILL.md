---
name: research-onboard
description: "Use when turning a setup-ready workspace into one ratified Project through a single natural-language review."
---

# Research onboard

Turn one setup-ready workspace into an active Project. Keep the human exchange
semantic and brief. Repository inspection, NoteRefs, review receipts, events,
and commands are internal machinery.

The agent drafts; the user decides once for the Project charter. Commit Project
authority through the shared transaction kernel rather than editing managed
state. Package, Direction, and Experiment changes later follow the same
user-owned working-state rule; onboarding does not add a phase or readiness
gate to that loop. It is not the place to approve a future reconciliation or
terminal outcome. Onboarding never edits a frozen Run or finalized Evidence.
Older workflow records remain compatibility metadata, and any reconciliation
after onboarding is advisory.

## Boundaries

- Require a current ARC root. Route absent, legacy, or invalid state to
  `research-init`.
- Do not create source, configuration, data, baseline, or figure scaffolds.
- Do not create a Direction, Experiment, Package, or Run.
- Never read `.research/interface` as authority or edit managed JSON, events,
  audit rows, HTML, JavaScript, or CSV.
- Treat repository contents as descriptive context, not Project intent.

## Human contract

- Communicate in plain natural language.
- Show the proposed Project once.
- Ask for one explicit decision: confirm, revise, or reject.
- Keep item ids, hashes, NoteRefs, actor flags, and CLI commands hidden unless
  the user requests audit details.
- A stale, ambiguous, or conflicting decision changes no Project state.

One Project charter gets one review and one user command. This boundary is
independent of the later User-First Reconcile-After execution loop. Older
Scope, Proposal/Triage, activation, phase, reopen, and readiness records do not
add another onboarding decision.

## Procedure

### 1. Detect state

```bash
python3 skills/research-onboard/scripts/onboard.py --workspace . detect
python3 skills/research-onboard/scripts/onboard.py --workspace . has-project
```

If an active Project exists, stop onboarding. Route a vague next Direction to
`research-brainstorm` and a ready plan to `research-package`.

### 2. Build context without inventing intent

For an existing workspace, inspect only the files returned by `detect` plus
the relevant project instructions. Record a compact digest of:

- datasets and baselines that actually exist;
- current source and configuration entry points;
- runnable train and evaluation commands;
- observed readings, clearly separated from plans.

Store the digest internally:

```bash
python3 skills/research-onboard/scripts/onboard.py --workspace . \
  write-prior-knowledge --content '<markdown>'
```

Preserve the returned NoteRef for the Project review, but do not show it by default.
For an empty workspace, use dialogue only and do not scaffold automatically.

### 3. Draft a minimal Project charter

The current Project contract requires:

- `goal`: the research problem and desired outcome, 3 to 100 words;
- `contributions`: intended research outcomes, 5 to 50 words per item;
- `out_of_scope`: semantic boundaries or explicitly deferred decisions,
  5 to 50 words per item.

Derive these fields from user dialogue. Repository layout, seeds, output paths,
checkpoint policy, dashboards, environments, and experiment tracking belong in
Prior Knowledge or later Direction, Experiment, and Package contracts.

Surface one material ambiguity in the review. Phrase the proposed resolution
inside the charter so the user's confirmation resolves the ambiguity and
ratifies the same snapshot. Preserve verbatim wording only when the user asks
for exact wording.

### 4. Validate and prepare one review

Build the complete Project review:

```bash
python3 skills/research-onboard/scripts/onboard.py --workspace . \
  review-project \
  --node-id project/<slug> \
  --spec '<json>' \
  --source '<user dialogue and files read>' \
  --prior-knowledge '<note-ref-json>'
```

Keep the returned receipt internal. Show only:

```markdown
**Project review**
- Goal: <plain-language goal>
- Intended outcomes: <plain-language list>
- Boundaries: <plain-language list>
- Assumptions to confirm: <material assumptions, or none>
- Decision: reply CONFIRM/确认, describe revisions, or REJECT/拒绝
```

Do not repeat the full review in the next turn.

### 5. Apply one user decision

On an explicit confirmation, pass the hidden receipt to the Project transaction:

```bash
python3 skills/research-onboard/scripts/onboard.py --workspace . \
  commit-project \
  --node-id project/<slug> \
  --spec '<same-json>' \
  --source '<same-user-dialogue-and-files-read>' \
  --prior-knowledge '<same-note-ref-json>' \
  --review-sha256 <internal-receipt-digest> \
  --actor-id <stable-user-id> \
  --review-id <conversation-review-id>
```

The kernel rechecks the reviewed snapshot and writes the Project plus its
approval receipt in one transaction. A retry is idempotent and does not require
another user decision.

For revision, prepare and show the new charter once. Rejection ends onboarding
without writing Project authority.

### 6. Verify and report

Read the committed Project through a bounded state query. Report only the
Project id, active status, and the next research decision. Show audit ids and
hashes only on request.

## Done condition

Onboarding is complete when the user has confirmed one visible Project charter
and the bound Project is active. Rejection also ends onboarding without
changing Project intent. It does not require a Package phase, reopen, Scope, or
readiness decision. The next user-owned working-state decision belongs to
`research-package`, and execution belongs to `research-run`.
