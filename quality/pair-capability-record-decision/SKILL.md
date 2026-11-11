---
name: pair-capability-record-decision
description: "Records an architectural or non-architectural decision. Architectural decisions produce an ADR; non-architectural decisions produce an ADL entry. Both always update the relevant adoption files. Invocable independently or composed by /pair-process-implement and /pair-process-review."
version: 0.4.1
author: Foomakers
---

# /pair-capability-record-decision — Decision Recorder

Record a technical decision as either an ADR (architectural) or ADL (non-architectural). Always update the corresponding adoption files to keep them as the single source of truth for "what we use now."

## Arguments

| Argument   | Required | Description                                                                      |
| ---------- | -------- | -------------------------------------------------------------------------------- |
| `$type`    | Yes      | Decision type: `architectural` or `non-architectural`                            |
| `$topic`   | Yes      | Short kebab-case topic name (e.g., `streaming-downloads`, `date-library-choice`) |
| `$summary` | No       | One-line summary of the decision (will be asked interactively if omitted)        |

## Core Rule: ADR and ADL Are Mutually Exclusive

- **Architectural decision** → ADR file + adoption update. Never ADL.
- **Non-architectural decision** → ADL file + adoption update. Never ADR.
- **Adoption update is always required** regardless of decision type.
- Adoption files = "what we use now." ADR/ADL = "why we decided."

## Algorithm

### Step 1: Classify Decision Type

1. **Check**: Is `$type` provided? If yes, use it.
2. **Act**: If not provided, ask the developer:

   > Is this decision **architectural** (affects system structure, patterns, service boundaries, quality attributes) or **non-architectural** (library choice, convention adoption, tooling preference)?

3. **Verify**: Decision type is set to `architectural` or `non-architectural`.

### Step 2: Detect Existing Decision

1. **Check**: Search for existing decision files matching `$topic`:
   - If `architectural`: scan [adoption/tech/adr/](../../../.pair/adoption/tech/adr) for files containing `$topic` in filename.
   - If `non-architectural`: scan [adoption/decision-log/](../../../.pair/adoption/decision-log) for files containing `$topic` in filename.
2. **Skip**: If no existing file found, proceed to Step 3 (create new).
3. **Act**: If existing file found, ask the developer:

   > Found existing decision: `[filename]`. Do you want to **update** this decision or **create a new one**?

   - **Update**: Read existing file, present current content, proceed to Step 4 with update mode.
   - **Create new**: Proceed to Step 3 with create mode (for cases where the topic evolved into a distinct decision).
4. **Verify**: Mode is set to `create` or `update`.

### Step 3: Write Decision File

**File naming**: `YYYY-MM-DD-<topic>.md` (today's date, one file per decision).

#### If `architectural` → ADR:

1. **Check**: Does [adoption/tech/adr/](../../../.pair/adoption/tech/adr) directory exist?
2. **Act**: If not, create it.
3. **Act**: Create (or update) the ADR file at [adoption/tech/adr/](../../../.pair/adoption/tech/adr)`YYYY-MM-DD-<topic>.md` following the standalone [ADR template](../../../.pair/knowledge/guidelines/collaboration/templates/adr-template.md). Fill in all sections: Status, Date, Context, Options Considered, Decision, Consequences, and Adoption Impact.
4. **Verify**: ADR file exists with complete content following the template structure.

#### If `non-architectural` → ADL:

1. **Check**: Does [adoption/decision-log/](../../../.pair/adoption/decision-log) directory exist?
2. **Act**: If not, create it.
3. **Act**: Create (or update) the ADL file at [adoption/decision-log/](../../../.pair/adoption/decision-log)`YYYY-MM-DD-<topic>.md` following the standalone [ADL template](../../../.pair/knowledge/guidelines/collaboration/templates/adl-template.md). Fill in all sections: Date, Status, Category, Context, Decision, Alternatives Considered, Consequences, and Adoption Impact.
4. **Verify**: ADL file exists with complete content following the template structure.

### Step 4: Update Adoption Files

This step is **always required** — adoption is the single source of truth.

1. **Check**: Identify which adoption files are affected by this decision:
   - [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — if the decision involves libraries, frameworks, or tools
   - [architecture.md](../../../.pair/adoption/tech/architecture.md) — if the decision involves architectural patterns, boundaries, or infrastructure
   - [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — if the decision involves process, workflow, or tooling conventions
   - Other adoption files as relevant
2. **Act**: For each affected adoption file:
   - Read current content.
   - Add or update the relevant entry to reflect the decision.
   - Preserve existing content — only add/modify the affected section.
3. **Verify**: Each updated adoption file reflects the current state of facts.

### Step 5: Consistency Check

1. **Check**: Re-read the decision file (ADR or ADL) and all updated adoption files.
2. **Act**: Verify that every claim in the decision file is reflected in adoption, and vice versa.
3. **Verify**: If inconsistency found, report to developer and propose correction.

## Output Format

```text
DECISION RECORDED:
├── Type:     [Architectural (ADR) | Non-architectural (ADL)]
├── File:     [path to decision file]
├── Mode:     [Created | Updated]
├── Adoption: [list of updated adoption files]
└── Status:   [Consistent | Inconsistency detected — details]
```

## Composition Interface

When composed by `/pair-process-implement` or `/pair-process-review`:

- **Input**: The composing skill detects a decision need and invokes `/pair-capability-record-decision` with `$type` and `$topic`.
- **Output**: Returns the path to the decision file and list of updated adoption files.
- The composing skill includes the decision file in the next commit.

When invoked **independently**:

- Interactive: asks for type, topic, and summary if not provided as arguments.
- Writes files and reports results. Developer commits the changes.

## Edge Cases

- **Same topic + same date**: If a file `YYYY-MM-DD-<topic>.md` already exists and the developer chose "create new," append an incremented suffix: `YYYY-MM-DD-<topic>-2.md`.
- **Adoption file doesn't exist**: Create it with the decision content as the initial entry. Warn the developer that a new adoption file was created.
- **Decision supersedes another**: Set the old decision's status to "Superseded by [new file]" and the new decision references the old one.

## Graceful Degradation

- If [ADR template](../../../.pair/knowledge/guidelines/collaboration/templates/adr-template.md) is not found, use the minimal ADR structure: Status, Date, Context, Decision, Consequences, Adoption Impact.
- If [ADL template](../../../.pair/knowledge/guidelines/collaboration/templates/adl-template.md) is not found, use the minimal ADL structure: Date, Status, Context, Decision, Consequences, Adoption Impact.
- If adoption directories don't exist, create them and warn: "Created adoption directory — this appears to be a new project."

## Notes

- ADR and ADL are mutually exclusive. Never write both for the same decision.
- Adoption files are always updated. A decision without adoption update is incomplete.
- Date-based naming (`YYYY-MM-DD-<topic>.md`) ensures sortability and avoids numbering conflicts.
- This skill modifies files: decision files and adoption files. All changes should be committed together.
