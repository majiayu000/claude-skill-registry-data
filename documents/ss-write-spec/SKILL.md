---
name: ss-write-spec
description: Generates or updates OpenSpec delta specs under openspec/changes/<change-id>/ from a proposal, PRD, or plain-language requirement, bootstrapping the openspec/ skeleton first if the project doesn't have one yet. Use this to align capability specs with reviewers before writing a full execution plan, or to adjust deltas without regenerating the plan.
---

# Write OpenSpec Delta

Generate OpenSpec-compatible delta specs under `openspec/changes/<change-id>/`. This is a
plumbing skill: day-to-day development normally goes through the `ss-plan` skill,
whose Phase 0 runs this same logic automatically.

## When To Use

- You need to align capability specs with reviewers before writing a full execution plan.
- You need to adjust delta specs without regenerating the plan.
- The `ss-coding` or `ss-create-pr` skill reported missing or invalid delta
  specs.

## Inputs

| Input | Handling |
|-------|----------|
| A URL to a hosted doc (wiki, Confluence, Google Docs, etc.) | Fetch it with your document-reading tool, or an available doc-integration skill, and convert it to markdown |
| A local markdown file | Read the file directly |
| Plain text | Treat it as the requirement source |

If none of these is available, ask the user for the proposal, PRD, or requirement text
before continuing.

**Language of the deltas:** write requirement and scenario prose in the same language as
the input document (or the project's existing docs, if that's a clearer signal); default
to English when neither gives a signal. `SHALL`/`MUST` keywords, code identifiers, and
file paths always stay in English.

## Step 0: Ensure the OpenSpec Skeleton Exists

Check whether `openspec/specs/` and `openspec/changes/` already exist. If this repository
has no OpenSpec structure yet, create it first by following
`../ss-references/openspec-skeleton.md`, then continue with Step 1 below.

## Process

### Step 1: Read Context

Read:

- `openspec/config.yaml`, if present
- all existing `openspec/specs/*/spec.md`
- active deltas under `openspec/changes/*/specs/*/spec.md`, excluding `archive/`
- relevant OpenAPI definitions, if API paths are mentioned
- project guidance files (e.g., `AGENTS.md` / `CLAUDE.md`), if present

### Step 2: Derive Change ID

Use an explicit `--change-id` if provided. Otherwise derive a kebab-case id from, in order:

1. the current branch name, stripped of its type prefix, or
2. the proposal title, or
3. the first meaningful requirement sentence.

The id must contain only lowercase letters, digits, and hyphens.

### Step 3: Decide Capability Ownership

For each requirement:

- Prefer an existing capability under `openspec/specs/`.
- Create a new capability only when no existing capability owns the behavior.
- Capability names are kebab-case business noun phrases.
- If ownership is ambiguous, stop and ask the user to confirm. Do not guess.

### Step 4: Generate Delta Files

Write one file per capability:

```plaintext
openspec/changes/<change-id>/
├── proposal.md
└── specs/
    └── <capability>/
        └── spec.md
```

Allowed section headings are exactly:

- `## ADDED Requirements`
- `## MODIFIED Requirements`
- `## REMOVED Requirements`
- `## RENAMED Requirements`

Requirement format:

```markdown
### Requirement: <name>
The system SHALL ...

#### Scenario: <name>
- **WHEN** ...
- **THEN** ...
- **AND** ...
```

Rules:

- Every Requirement MUST have at least one Scenario.
- Scenario headings MUST be `#### Scenario:`.
- `MODIFIED` MUST copy the original Requirement in full, then edit it — don't write a
  partial diff.
- `REMOVED` MUST include a **Reason** and a **Migration** note.
- `RENAMED` uses `FROM: <old> → TO: <new>`.
- Do not write implementation details. Specs describe observable behavior only.

### Step 5: Self-Review

Verify:

- every source requirement is represented
- existing capabilities were reused where appropriate
- no placeholder text remains
- every `MODIFIED` entry is complete
- every `REMOVED` entry has a Migration note
- OpenAPI paths mentioned in specs match available OpenAPI definitions, when present

## Output

Report:

- the `change-id`
- files written
- capabilities touched
- ADDED / MODIFIED / REMOVED / RENAMED counts
- any user decisions still pending

Suggest the next step: run the `ss-plan` skill with the same input to generate the
execution plan.
