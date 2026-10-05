---
name: manage-adr
description: "Create, update, and validate Architecture Decision Records (ADRs) following MADR 4.0 format. Use when the user mentions ADR, architecture decision, decision record, or asks to document a technical decision. Also use when creating new files in docs/decisions/. Handles numbering, frontmatter, section structure, and README index updates. Do NOT use for general documentation or non-architectural decisions."
metadata:
  author: Serghei Iakovlev
  version: "1.1"
  category: documentation
---

# Managing Architecture Decision Records

This project stores ADRs in `docs/decisions/` following [MADR 4.0](https://adr.github.io/madr/) with project-specific conventions documented below.

## File Conventions

- Path: `docs/decisions/NNNN-kebab-case-title.md`
- Numbering: zero-padded four digits, sequential. See "Get Sequence Number" below.
- Index: `docs/decisions/README.md` contains a table of all ADRs. Update it after every create, rename, or status change.

## Running scripts bundled with this skill

Script paths in this document (e.g. `scripts/`) are resolved relative to **this** SKILL.md file, not to your current working directory. If a relative command fails to resolve, prefix it with the path your platform loaded this SKILL.md from.

**Fallback.** If `python3` cannot be located, analyze the script's purpose and logic and execute its intent with available tools, but warn the user that python is not available and the logic was executed with a fallback approach that may not be perfect.

## Running scripts bundled with this skill

Script paths in this document (e.g. `scripts/`) are resolved relative to **this** SKILL.md file, not to your current working directory. If a relative command fails to resolve, prefix it with the path your platform loaded this SKILL.md from.

## ADR Template

Use [assets/adr-template.md](assets/adr-template.md) as the starting point. The template contains the exact frontmatter and section structure. Copy it, fill in the content, remove sections marked optional if unused.

Key rules:

- Frontmatter fields `status` and `date` are required. `decision-makers` is required for accepted decisions.
- `status` values: `proposed`, `accepted`, `deprecated`, `superseded by NNNN`
- `date` format: `YYYY-MM-DD` (date of last status change)
- The H1 title is a short imperative phrase: "Use X for Y", not "Decision about X"
- "Decision Outcome" must begin with `Chosen option: **X**, because Y`
- "Considered Options" is a bullet list. Detailed analysis goes under "### Considered Options in Detail" inside "Decision Outcome"
- Decision Drivers use numbered bold-label items: `1. **Label.** Description`

## Writing for durability

An accepted ADR is immutable: a permanent record of a decision at a point in time, not edited afterward. Everything in it must stay true and legible for years without depending on anything that changes. Apply these rules to Context, Drivers, Consequences, and rationale:

- **No references to mutable documents.** Do not cite architecture-doc section numbers (`Section 5.3.5`, `§8.4`), file line numbers, or any pointer into a doc that will be renumbered, rewritten, or deleted. The ADR cannot be edited to follow the move, so the reference rots into a lie. The reader also cannot resolve a bare `Section 5.3.5` with no document named. State the fact directly in the ADR's own voice instead.
- **No tracker IDs, and no ticket-driven framing.** Do not cite issue or ticket IDs (`#240`, Jira keys), and never frame the ADR's reason for existing as "Issue #N requests X." An ADR records an architect's decision in response to a force in the system, not a response to a ticket. Open Context with the problem and its stakes.
- **Ground claims in stable identifiers.** Config field names (`agent.max_sessions`), table names (`run_history`), environment variables, tool names, and event field names change rarely and are meaningful without a lookup. Prefer them over document coordinates.
- **Prefer self-containment over cross-references.** Relating one ADR to another by filename is acceptable when it carries real lineage, but default to stating an inherited constraint as a fact (for example, "{Product_name} ships as a single statically-linked binary") rather than linking out.
- **Use tense discipline for before-and-after state.** Write enduring facts in the present tense. Write the specific deficiencies the decision removes in the past tense ("no table held a per-issue total"; "`session_metadata` kept only the latest session"). A present-tense claim about the pre-decision state ("`run_history` has no token columns") becomes false the day the decision ships, in a document you cannot edit.

## Get Sequence Number

Two strategies depending on context:

**Pre-assigned number** (passed by caller or human): Use it directly. Do not call the script - this prevents duplicate numbers when multiple ADRs are created in parallel.

**No number assigned** (standalone use) `python3 scripts/next_adr_number.py` to get the next available number:

```bash
# Output: 0004
```

For batch allocation (multiple ADRs in one session) `python3 scripts/next_adr_number.py --count 3` to reserve a block of numbers:

```bash
# Output:
# 0004
# 0005
# 0006
```

Allocate all numbers upfront before creating any files. This avoids the script returning the same number twice when files haven't been written yet.

By default the script resolves `docs/decisions/` relative to its own location. If your ADRs live elsewhere - or the default path does not match the layout this skill was loaded from - pass `--decision-dir <path>` to override:

```bash
python3 scripts/next_adr_number.py --decision-dir docs/decisions
python3 scripts/next_adr_number.py --decision-dir docs/decisions --count 3
```

## Operations

### Create ADR

1. Get the next ADR number (see "Get Sequence Number" above).
2. Copy `assets/adr-template.md` to `docs/decisions/NNNN-kebab-case-title.md`.
3. Fill in frontmatter: `status: proposed`, `date: <today>`, `decision-makers: <name>`.
4. Write Context, Decision Drivers, Considered Options, and Decision Outcome. Follow "Writing for durability": self-contained, no references to mutable sources, framed from the architectural force rather than from a ticket.
5. Remove unused optional sections (Consequences, Confirmation).
6. Update `docs/decisions/README.md` - add a row to the table.

### Update ADR Status

1. Edit the `status` field in frontmatter.
2. Update `date` to today.
3. If superseded, set `status: superseded by NNNN` and link to the replacement ADR.
4. Update the Status column in `docs/decisions/README.md`.

### Validate ADRs

Check every file in `docs/decisions/` (excluding README.md):

- [ ] Filename matches `NNNN-kebab-case-title.md`
- [ ] YAML frontmatter has `status`, `date` fields
- [ ] `date` is valid `YYYY-MM-DD`
- [ ] `status` is one of: `proposed`, `accepted`, `deprecated`, `superseded by NNNN`
- [ ] `decision-makers` is present and non-empty when `status` is `accepted`
- [ ] H1 title exists and is an imperative phrase
- [ ] Sections present: "Context and Problem Statement", "Considered Options", "Decision Outcome"
- [ ] "Decision Outcome" contains `Chosen option: **` pattern
- [ ] "Considered Options" is a bullet list
- [ ] No references to mutable sources: no architecture-doc section numbers (`Section N.N`, `§N`), no file line numbers, no tracker issue/ticket IDs, and the rationale is not framed around a ticket
- [ ] `docs/decisions/README.md` table has a row for this ADR with correct title and status

Report all violations. Do not auto-fix without confirmation.

### Update README Index

Regenerate the table in `docs/decisions/README.md` by scanning all ADR files:

```markdown
| ADR                              | Title         | Status |
| -------------------------------- | ------------- | ------ |
| [NNNN](NNNN-kebab-case-title.md) | H1 title text | Status |
```

- Sort by ADR number ascending.
- Title column uses the H1 text from the ADR file.
- Status column uses the `status` frontmatter value, capitalized.
- Preserve the introductory paragraph and heading above the table.
