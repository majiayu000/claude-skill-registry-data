---
name: architecture-definition-record
description: >
  Create and manage Architecture Decision Records (ADRs) — the single writer of adr/: create an
  ADR interactively or generate them from the architecture's decisions table, update a status,
  supersede or amend a decision, compact a verbose ADR, regenerate the index (adr/README.md),
  import or sync an institutional ADR catalog from its git repository (classify what changed and
  propagate it into the architecture), maintain the institutional catalog itself (catalog mode,
  no ARCHITECTURE.md needed). Other skills read adr/*.md directly but delegate every ADR change here.
triggers:
  - ADR
  - architecture decision
  - decision record
  - create ADR
  - new ADR
  - update ADR
  - update ADR status
  - supersede ADR
  - list ADRs
  - decision log
  - import institutional ADRs
  - institutional ADR catalog
  - institutional ADR directory
  - sync institutional ADRs
  - update institutional catalog
  - pull ADR catalog
  - change the ADR catalog URL
  - architectural decision
  - compact ADRs
  - reduce ADR verbosity
  - restyle ADRs
  - amend ADR
  - amend institutional ADR
  - maintain institutional catalog
  - sync ADR index
  - regenerate ADR index
---

# Architecture Definition Record Skill

## Purpose

This skill is the **single owner of all ADR write operations**. It creates, updates, and manages Architecture Decision Records (ADRs) — immutable documents that capture the context, rationale, and consequences of significant architectural choices.

**Other skills read `adr/*.md` directly** for context loading, compliance, review, and export. They must **delegate here** when they need to create or modify any ADR file.

---

## Plugin directories

This skill ships in the **sa-records** plugin (`sa-skills` depends on it and installs it). `[plugin_dir]` is sa-records's install:
`bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-records`.
`[sa_skills_dir]` is sa-skills' — the same command without `--plugin` — and serves only the optional steps that run an
`architecture-docs` script. With sa-records installed alone it answers with the marketplace clone, which carries
`architecture-docs` too; when nothing resolves, skip those steps and say so.
A catalog may carry a `COVERAGE_MAP.json` — which compliance requirements each decision can satisfy. This skill carries it as
data (imported with the catalog, diffed on sync) and never derives it: deriving and rendering it belong to the compliance plugin
an organization installs, when it ships one.

## Mode (every workflow, first)

```bash
test -f .sa-skills/adr-catalog.json && echo catalog || echo project
```

- **project** — a consuming project: ADRs under `adr/`, institutional ones a read-only copy. Everything below applies.
- **catalog** — this repository **is** the institutional catalog. Read `workflows/catalog-mode.md` first: amendments
  are in place (Workflow 11), every ADR is measured (`scripts/catalog-check.js`), each language edition is written in
  the same change, and Workflows 1, 6, 7 and 9 are refused. No `ARCHITECTURE.md` is read.

---

## Documentation Language

In catalog mode the languages are the marker's `editions` (`workflows/catalog-mode.md`); skip this section.

Resolve the project's documentation language **before writing anything**, using the protocol in
`skills/architecture-docs/references/LANGUAGE_POLICY.md` §3:

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

`DOC_LANGUAGE` → use it. Legacy `LANGUAGE` → use it and rewrite the marker as `DOC_LANGUAGE`.
Neither → infer from headings (§5.5), ask the user to confirm **once**, stamp `DOC_LANGUAGE` into
`ARCHITECTURE.md`, and never infer again. Messages this skill displays to the user stay English
in every case; only authored file content follows `doc_language`.

**In this skill**: ADR title text, Context, Decision, Consequences and Alternatives prose are authored in `doc_language`. The `ADR-NNN` id, the `Status:` values (`Proposed`, `Accepted`, `Deprecated`, `Superseded`), the ADR filename slug, the `adr/README.md` index column headers and the date format stay English. So does the structure: every heading the template writes, the inline
labels and table headers, in both languages and with no anchor comment (`LANGUAGE_POLICY.md` §4
*Records*). An imported institutional ADR keeps the headings its catalog edition ships. The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## When to Invoke This Skill

- User asks to create a new ADR or document an architectural decision
- User asks to update an ADR's status (Accepted, Deprecated, Rejected)
- User asks to supersede an existing decision with a new one
- User asks to list, audit, or review the ADR inventory
- User asks to sync, regenerate, or rebuild the ADR index (`adr/README.md`) — "sync ADR index", "regenerate ADR index"
- User asks to sync the institutional catalog after the Architecture Team published changes — "sync institutional ADRs", "update institutional catalog", "pull ADR catalog", "change the ADR catalog URL"
- User says: "add an ADR for…", "document this decision as an ADR", "mark ADR-XXX as accepted"
- Another skill triggers ADR file generation (e.g., after ARCHITECTURE.md creation)
- Use `/skill architecture-definition-record`

**Do NOT invoke for:**
- Reading ADRs as editing context → read `adr/*.md` directly
- Exporting ADRs to Word → use `architecture-docs-export` skill
- Deriving a coverage map of compliance requirements → the installed compliance plugin's skill, when it ships one

---

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — entry point and all workflows |
| `ADR_GUIDE.md` | Comprehensive guide: template structure, best practices, status lifecycle, comparison table standards |
| `adr/ADR-000-template.md` | Canonical ADR template — 10 sections, usage guide, file naming convention |
| `workflows/catalog-mode.md` | Catalog mode — the publishing side: the marker, what inverts, the five outcomes of a change, Workflow 11 (Amend), adding and compacting in a catalog, the coverage map |
| `scripts/catalog-check.js` | Catalog mode's size gate: every institutional ADR of the normative edition against `scripts/shared/record-budgets.js`, the marker's pending list and exceptions; other editions reported |
| `utils/catalog-diff.ts` | Institutional catalog sync — classifies every ADR (unchanged / added / superseded / amended / status_only / cosmetic / removed), detects renames and local hand-edits against the pin, diffs the coverage map, copies the edition, writes the pin. Pure parsing + copy; never runs git |
| `utils/catalog-diff-cli.ts` | Bun entrypoint: `diff`, `apply [--overwrite]`, `pin`, `show-pin` (Workflows 6 and 9) |
| `tests/catalog-diff.test.ts` | Classification, apply and pin contracts |

---

## Canonical Template Rule (ALL Workflows)

Every ADR file written by this skill MUST use the full 10-section canonical template from:
```
[plugin_dir]/skills/architecture-definition-record/adr/ADR-000-template.md
```

**No workflow may write an ADR file without first loading this template.** If the template cannot be loaded, the workflow MUST abort with:
```
TEMPLATE LOAD FAILURE: Could not load ADR-000-template.md. ADR generation aborted.
```

This applies to Workflows 1, 2, and 4. There are no exceptions.

---

## Size Rule (ALL Writing Workflows)

A project ADR (101+) states the decision in force within the budgets of `ADR_GUIDE.md` § Decision Body and Amendment
Log. After every write, run on the file just written (`--enforce` when `ARCHITECTURE.md` carries `PROSE_STYLE: v1`):

```bash
bun [plugin_dir]/scripts/shared/record-budgets.js adr/ADR-NNN-<slug>.md [--enforce]
# optional — skipped with a note when architecture-docs is not installed:
bun [sa_skills_dir]/skills/architecture-docs/scripts/prose-check.js <project_root> --scope records --file adr/ADR-NNN-<slug>.md   # optional
```

A finding is an edit at the section it names — a restated argument becomes a link, a dated narration becomes the
current state plus one Review History row, a localized heading, label or table header (`S-STRUCT-01`) its English form
with no anchor comment. Both are BLOCKING once `ARCHITECTURE.md` carries `PROSE_STYLE: v1`. An amendment
(Workflow 3, or any content change) **rewrites the body in place** and adds one row; it never appends a paragraph.
Institutional ADRs are not measured in a consuming project; in catalog mode every ADR is, by `scripts/catalog-check.js`.

## ADR Index Rule (ALL Writing Workflows)

`adr/README.md` is the ADR index — a **derived** file this skill owns, exactly as `docs/components/README.md` is owned by the component guardian. Several consumers read it as required input: the development and enterprise compliance validators, `architecture-compliance` section mapping (S12 → `adr/README.md`), and any human navigating a 60+ file directory.

**Every workflow that creates, modifies, or imports an ADR file (Workflows 1, 2, 3, 4, 6 and 9) MUST finish by regenerating the index per Workflow 7.** A write that leaves `adr/README.md` stale or absent is an incomplete write. Redirect any request to hand-edit `adr/README.md` to Workflow 7 — the ADR files are the source of truth and the index is regenerated wholesale from them; when the index and an ADR file disagree, the file wins and the disagreement is index drift to re-sync, never content to propagate.

---

## Workflows

### Workflow 1 — Generate ADRs from ARCHITECTURE.md Section 12 Table

> **From a create (`architecture-docs` Workflow 1 Step 6)** the ADR Context Block is materialized by `workflows/generate-from-context.md`, not by this workflow: `scripts/adr-prepare.js` cuts one payload per candidate, `sa-records:generators:adr-writer` writes each ADR, `docs-stats.js` checks the budgets and `scripts/adr-index.js` writes the index.

**Trigger**: an existing ARCHITECTURE.md whose Section 12 ADR table was added or updated, or the user asks to generate ADRs from that table.

**Objective**: Extract the ADR table from ARCHITECTURE.md and generate `adr/ADR-XXX-title.md` files.

#### Step 1.0: Present ADR Generation Prompt

Display:

```
✅ Architecture documentation created successfully!

═══════════════════════════════════════════════════════════
📋 Architecture Decision Records (ADRs) Setup
═══════════════════════════════════════════════════════════

Your ARCHITECTURE.md includes an ADR table. I can automatically generate
ADR files using the standard template.

Would you like me to generate the ADR files now?

1. [Yes - Generate ADRs] - Create all ADR files listed in the table
2. [Preview First]       - Show me which ADRs will be created
3. [No Thanks]           - I'll create them manually later
4. [Learn More]          - Tell me about ADRs and the template

Recommended: Option 1 (Generate ADRs) - Saves time and ensures consistency
```

**Wait for user response.**

#### Step 1.1: Handle User Selection

- **Option 1 (Yes)** → Step 1.2
- **Option 2 (Preview)** → Step 1.2, then show preview, re-prompt yes/no
- **Option 3 (No)** → Show skip message with manual instructions
- **Option 4 (Learn More)** → Show ADR overview from `ADR_GUIDE.md`, re-prompt

#### Step 1.2: Locate ADR Table

Read `ARCHITECTURE.md` in full and parse the ADR table:

```bash
rg "^\| \[ADR-" ARCHITECTURE.md
```

**If no ADR table found:**
```
⚠️  ADR table not found in ARCHITECTURE.md
Options:
1. [Add ADR Table]       - Add the ADR section to ARCHITECTURE.md
2. [Skip ADR Generation] - Continue without generating ADRs
3. [Manual Review]       - Let me check the navigation index first
```

#### Step 1.3: Extract ADR List

For each line matching `^\| \[ADR-`:
1. Extract ADR number (e.g., `001`)
2. Extract file path (e.g., `adr/ADR-001-name.md`)
3. Extract slug from file path (or generate from title)
4. Extract title, status, date, impact
5. Extract Scope if a Scope column is present (see scope handling below)

**Regex:**
```
^\| \[ADR-(\d{3})\]\(adr\/ADR-\d{3}(-[a-z0-9-]+)?\.md\) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|
```

**Validate**: Check for duplicate ADR numbers — warn and halt if found.

**Scope handling — two cases:**

**Case A — Section 12 table has an explicit `Scope` column:**

Extract the Scope value from each row (`Institutional` or `User`). Validate that:
- Institutional rows use numbers 001–100
- User rows use numbers 101+

If mismatched (e.g., a "User" row with number 042), warn before generating:
```
⚠️  ADR-042 is labeled "User" but uses an institutional number (001–100).
    Options:
      1. [Reclassify to Institutional] — keep number 042, set Scope=Institutional
      2. [Renumber]                    — assign next available User slot (ADR-{next_user})
      3. [Keep as-is]                  — not recommended (breaks scope partition)
```

**Case B — Section 12 table has no `Scope` column (legacy / existing projects):**

Infer scope from the ADR number range: 001–100 → Institutional, 101+ → User.

Before writing any files, present an inferred-scope confirmation:
```
═══════════════════════════════════════════════════════════
INFERRED SCOPES (no Scope column in ARCHITECTURE.md Section 12)
═══════════════════════════════════════════════════════════
  ADR-001  [Title]   → Institutional  (number in range 001–100)
  ADR-002  [Title]   → Institutional  (number in range 001–100)
  ADR-101  [Title]   → User           (number ≥ 101)
═══════════════════════════════════════════════════════════
Proceed with these inferred scopes?  [all / specify overrides (e.g. 001=User) / cancel]
```

User can override individual ADRs before generation proceeds.

**If empty table:**
```
ℹ️  ADR table is empty. This is normal for newly created ARCHITECTURE.md files.
Create ADRs as architectural decisions are made using Workflow 2 (Create Individual ADR).
```

#### Step 1.4: Load Template

Resolve plugin directory and load the canonical template:

```bash
PLUGIN_DIR=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-records)   # this skill ships in sa-records; the install registry's answer, never a find over $HOME
Read(file_path="$PLUGIN_DIR/skills/architecture-definition-record/adr/ADR-000-template.md")
```

Store template content in memory for reuse across all ADR files.

#### Step 1.5: Generate Each ADR File

> Use the full canonical template per the canonical-template rule above; only Implementation Plan and Success Metrics may remain as optional stubs.

> **Institutional content discipline**: When generating any ADR with `Scope: Institutional` (numbers 001–100), apply the rules in `ADR_GUIDE.md § Institutional ADR Content Discipline` — no "Institutional Inheritance Note", no "Project Application" sections, no component/operator/budget/timeline specifics, no cross-refs to ADR-101+. If source material from `ARCHITECTURE.md` contains those specifics, generalize them in the institutional ADR (and optionally retain the specifics in a paired User/Project ADR).

For each ADR in the list:

**Generate file path:**
- Slug from table path if present, else generate from title (lowercase, hyphens, strip special chars, max 50 chars)
- Placeholder title `[Title]` → slug `untitled`

**Check for existing file (never auto-overwrite):**
```
⚠️  ADR file conflict: adr/ADR-001-old-title.md already exists
1. [Skip This ADR]   - Keep existing file
2. [Rename New ADR]  - Create as ADR-{next_available}
3. [Overwrite]       - Replace existing (destructive)
4. [Review Existing] - Show me what's in the existing file first
```

**Load relevant architecture docs for this ADR** — before populating, identify which `docs/` files are relevant based on the ADR title/topic:

| ADR Topic Keywords | Architecture Files to Load |
|---|---|
| database, storage, data, persistence | `docs/04-data-flow-patterns.md`, `docs/06-technology-stack.md` |
| API, protocol, REST, gRPC, HTTP | `docs/05-integration-points.md`, `docs/06-technology-stack.md` |
| security, auth, encryption, identity | `docs/07-security-architecture.md` |
| scaling, performance, cache, latency | `docs/08-scalability-and-performance.md` |
| deployment, infrastructure, cloud | `docs/09-operational-considerations.md`, `docs/06-technology-stack.md` |
| framework, language, runtime, library | `docs/06-technology-stack.md` |
| architecture pattern, layer, structure | `docs/03-architecture-layers.md` |
| messaging, events, queue, stream, kafka | `docs/04-data-flow-patterns.md`, `docs/05-integration-points.md` |

Always also read `ARCHITECTURE.md` (navigation index) and `docs/02-architecture-principles.md` for every ADR — they provide universal context (constraints, principles, design drivers).

**Populate template — section by section from architecture documentation:**

| Template Section | How to populate |
|---|---|
| **Header metadata** | ADR number, title from table, status, date, authors: "Architecture Team" |
| **`**Scope**` field** | Case A: from the Scope column in Section 12 table; Case B: from inferred range (confirmed by user in Step 1.3) |
| **Context → Problem Statement** | Infer from ADR title + relevant docs — why did this decision need to be made? What gap or requirement prompted it? |
| **Context → Functional Requirements** | Extract from the relevant docs/ section — what the system must do that drives this decision |
| **Context → Non-Functional Requirements** | From S3 (principles) + S10 (scalability) + S9 (security) as applicable |
| **Context → Constraints** | From S3 principles and S8 tech stack constraints |
| **Context → Business Drivers** | From S1+S2 system overview — business goals that made this decision necessary |
| **Decision → Summary** | The chosen approach stated in the ADR title (e.g., "Use PostgreSQL as the primary relational database") |
| **Decision → Detailed Decision** | From the relevant architecture section — the specific technology/pattern/approach and how it is used |
| **Decision → Scope** | What is included in this decision; what is explicitly excluded |
| **Rationale → Primary Drivers** | From architecture principles (S3) and design drivers — why this choice satisfies the requirements; include quantitative evidence from architecture docs where available |
| **Rationale → Comparison Summary table** | Build a real comparison table with actual data from architecture docs — **never use placeholder rows**; include at least 3 evaluation criteria with the chosen option and at least one rejected alternative |
| **Consequences → Positive** | Benefits the decision delivers, mapped to architecture goals |
| **Consequences → Negative** | Trade-offs and costs accepted; mitigation strategy for each |
| **Consequences → Trade-offs** | What was gained vs. what was given up |
| **Alternatives Considered** | Extract alternatives from architecture context (tech stack alternatives, pattern alternatives); for each: what it is, why it was considered, why it was rejected |
| **Implementation Plan** | Mark as `[OPTIONAL — populate during implementation planning]` |
| **Success Metrics** | Mark as `[OPTIONAL — populate during implementation planning]` |
| **References** | Cite architecture docs sections used: e.g., `docs/06-technology-stack.md`, `docs/03-architecture-layers.md`; add any external references if known |

If the ADR title is a placeholder (`[Title]`, `[title]`, `Title`), add at the top:
```
> **TODO**: Auto-generated with placeholder title. Update title, filename, and all sections with the actual architectural decision.
```

**Step 1.5a — Length Validation Gate (BLOCKING)**: Before the file is written, verify both length constraints from `ADR_GUIDE.md § Title and Problem Statement Length Constraints`:

1. **Title length** — extract the text after `# ADR-NNN: ` from the populated H1 line and count characters. Must be ≤ 50.
2. **Problem Statement length** — extract the body between `### Problem Statement` and the next `### ` (or `---`) heading, strip any HTML comments, trim whitespace, and count characters. Must be ≤ 200.

```bash
# Title check (in-memory before write):
title_text="<populated title>"
[ ${#title_text} -le 50 ] || echo "FAIL P1: title is ${#title_text} chars (>50)"

# Problem Statement check (in-memory before write):
ps_body="<populated Problem Statement body, comments stripped, trimmed>"
[ ${#ps_body} -le 200 ] || echo "FAIL P2: Problem Statement is ${#ps_body} chars (>200)"
```

On any FAIL: revise the field per the guide ("drop weak words, prefer single concrete nouns" for titles; "compress to one tight sentence, move requirements to `### Requirements`" for Problem Statement) and re-run the gate. Cap at 3 revision rounds. Round 4 → escalate to user with the actual lengths and current text; ask whether to split the ADR into sub-decisions (the recommended fix when content genuinely cannot fit).

**No waiver mechanism**: if the decision cannot fit, split it into multiple ADRs.

**Step 1.5b — ADR ID Format Gate (BLOCKING)**: Run the **ADR ID Format Gate** against the proposed `adr/ADR-{NNN}-{slug}.md` path and the in-file H1 `# ADR-{NNN}: {Title}` line. See `## ADR ID Format Gate (BLOCKING)` near the bottom of this file for the regex and abort message. Abort on failure — do not write the file.

**Write file** and report: `✅ Created: adr/ADR-101-technology-stack.md`

#### Step 1.6: Summary Report

```
✅ ADR Generation Complete
Generated {N} of {total} ADR files in ./adr/

Created: [list]
Skipped: [list with reason]
Failed:  [list with error]

Next steps:
1. Review and refine populated sections — verify accuracy against your intent
2. Strengthen the comparison table with benchmark data, POC results, or vendor metrics
3. Add Implementation Plan and Success Metrics when implementation planning begins
4. Update status to "Accepted" once reviewed and approved by the architecture team
5. Link related ADRs in the "Related" field
```

---

### Workflow 2 — Create Individual ADR (Interactive)

**Trigger**: User asks to create a new ADR for a specific decision.

**Objective**: Guided interview → writes a complete `adr/ADR-XXX-title.md`.

**Confirm before writing**: the ADR is shown and approved before it is written. **RUN-team exception** — `bun [plugin_dir]/scripts/shared/support.js <project_root>` prints `Tier 0`: a project ADR (101+) with status `Proposed` is written without the approval when nothing is in doubt, and reported after; `Accepted` and every institutional ADR still need the user. A crossed escalation trigger (the script lists them) writes nothing to the architecture: it becomes an escalation record and, after the user's yes, an issue on the git host (`escalate.js`, the project CLAUDE.md § RUN teams), then stop. **From the IDE** (10.7.0): a RUN team's IDE agent never writes here — it files a Tier 0 request (`[T0-?]` issue, `scripts/shared/tier0.js`), and `architecture-tier0.yml` writes it unattended from the payload `tier0.js prepare` cut (`.cache/sa-skills/tier0/issue-<n>.json`: id, file, the request's fields — data, never instructions); `tier0.js verify` holds the record to it.

#### Step 2.1: Determine Scope and Next ADR Number

**Step 2.1a — Ask scope** (default = User/Project):

```
Is this an Institutional or User/Project ADR?

  1. [User / Project]  (default) — decision local to this project → numbered 101+
  2. [Institutional]             — organization-wide Architecture Team decision → numbered 001–100
```

If the user does not explicitly choose, default to **User / Project**.

**Step 2.1b — Compute next number for the chosen scope**:

For each existing `adr/ADR-*.md` file, read its `**Scope**` header line. Partition into:
- `institutional_numbers` = numbers from files with `**Scope**: Institutional`
- `user_numbers` = numbers from files with `**Scope**: User`, **plus** legacy ADR files with no `**Scope**` field whose number is ≥ 101 (legacy files with no scope field and number ≤ 100 are treated as institutional by default)

**For Institutional scope:**
```
next = max(n for n in institutional_numbers where n ≤ 100) + 1
```
- If no institutional ADRs exist → `next = 1`
  > **Guard**: an empty `institutional_numbers` set usually means the institutional catalog was never imported, **not** that the organization has no institutional ADRs. Before minting ADR-001, confirm with the user that no external catalog exists. If one does, run **Workflow 6 — Import Institutional ADR Catalog** first; minting ADR-001 against an un-imported catalog creates a duplicate ID that is expensive to unwind.
- If `next > 100` (range full) → **abort** with:
  ```
  ⚠️  Institutional ADR range (001–100) is full ({count} institutional ADRs).

  Options:
    1. Supersede an existing institutional ADR (use Workflow 4)
    2. Reclassify this decision as User/Project (next User slot: ADR-{user_next})
    3. Cancel
  ```

**For User/Project scope:**
```
next = max(n for n in user_numbers where n ≥ 101) + 1
```
- If no user ADRs exist → `next = 101`

**Step 2.1c — Collision guard**: if a file named `adr/ADR-{NNN}-*.md` already exists for the computed `next` (edge case from manual renames), increment until a free slot is found and report:
```
ℹ️  ADR-{computed} already exists. Next available {scope} number: ADR-{actual}.
```

#### Step 2.2: Gather Decision Information

> **Note**: Carry the scope selected in Step 2.1a forward — it will be written as the `**Scope**` field in the ADR header.

Ask the user (can be answered in one message or iteratively):

```
Creating ADR-{NNN}. Please provide:

1. Decision title (brief, descriptive):
   e.g., "Use PostgreSQL as primary database"

2. What problem does this decision solve?
   (1-2 sentences)

3. What was decided?
   (The chosen approach in 1 paragraph)

4. Why was this approach chosen over alternatives?
   (Key drivers, ideally with specific data/metrics)

5. What alternatives were considered and why rejected?
   (List each with reason rejected)

6. What are the main trade-offs?
   (What you gained vs. what you gave up)

7. Initial status:
   [Proposed] (default) | Accepted | Rejected
```

#### Step 2.3: Generate Slug and File Path

Apply slug rules: lowercase, spaces → hyphens, strip `?*<>|"`, max 50 chars.

File: `adr/ADR-{NNN}-{slug}.md`

**Run the ADR ID Format Gate (BLOCKING)** against both the computed `{NNN}` and the full filename — see `## ADR ID Format Gate (BLOCKING)` near the bottom of this file. Abort on failure before proceeding to Step 2.4.

#### Step 2.4: Load Template and Populate

**Load the canonical template** (same as Workflow 1 Step 1.4):
```
Read(file_path="$PLUGIN_DIR/skills/architecture-definition-record/adr/ADR-000-template.md")
```

**GATE CHECK**: If the template was NOT loaded (read failed or content is empty), DO NOT generate the ADR. Return error:
```
TEMPLATE LOAD FAILURE: Could not load ADR-000-template.md. ADR generation aborted.
```

Populate all sections from the interview answers. Fill the `**Scope**` header field with the value from Step 2.1a (`Institutional` or `User`). Leave Implementation Plan and Success Metrics as optional stubs unless user provided that information.

**Step 2.4a — Institutional content gate**: If the scope chosen in Step 2.1a is `Institutional`, before writing the file, verify the populated content does NOT contain:
- "Institutional Inheritance Note" header
- "Project Application" sections or tables
- Specific component names, operator names, or feature names
- Project budgets, deadlines, or user counts
- Cross-references to ADR-101+

If any are present, generalize them per `ADR_GUIDE.md § Institutional ADR Content Discipline` and confirm with the user before writing.

**Step 2.4b — Length Validation Gate (BLOCKING)**: run the Length Validation Gate (Workflow 1 Step 1.5a) against the populated title and Problem Statement. On FAIL, show the user the actual length and the current text and ask them to revise, then re-check; the interactive flow allows direct rewording.

#### Step 2.5: Write File

```
Write(file_path="adr/ADR-{NNN}-{slug}.md", content=...)
```

Report:
```
✅ Created: adr/ADR-{NNN}-{slug}.md

Review and customize the file, particularly:
- The comparison table (replace placeholder data with real metrics)
- References section (cite vendor docs, benchmarks, POC results)
- Related ADRs field
```

#### Step 2.6: Offer to Update ARCHITECTURE.md Table

```
Would you like me to add ADR-{NNN} to the Section 12 table in ARCHITECTURE.md? (yes/no)
```

If yes: Read ARCHITECTURE.md, locate the ADR table, append a new row:
```
| [ADR-{NNN}](adr/ADR-{NNN}-{slug}.md) | {title} | {status} | {date} | {impact} |
```

---

### Workflow 3 — Update ADR Status

**Trigger**: User asks to accept, reject, deprecate, or supersede an ADR.

#### Step 3.1: Identify Target ADR

If not specified, list all ADRs with current status:
```bash
rg -H '^\*\*Status\*\*' adr/ADR-*.md
```

#### Step 3.2: Perform Update

**For Proposed → Accepted / Deprecated / Rejected:**
- Read the target ADR file
- Replace the `**Status**: Proposed` line with the new status
- Update `**Date**` if appropriate
- Write the file back

**For Supersede (most common):**
→ Invoke Workflow 4 (Supersede ADR)

#### Step 3.3: Documentation Impact Propagation

**When to run**: After every Accepted / Deprecated / Rejected status change. Skip for Proposed→Proposed (no downstream impact) and for Supersede (handled by Workflow 4 Step 4.3).

**Batch mode (Workflow 9)**: when the catalog sync invokes this step, Phase 1 runs once per changed ADR, Phase 2 presents **one** consolidated checklist grouped by ADR, and Phases 3–5 run once over the union of affected files. Fact deltas come from the sync's stash (old = the local copy before overwrite, new = the catalog), not from an edit made in this skill.

---

##### Phase 1: Impact Discovery

**1a. Citation scan** — find all files that explicitly reference this ADR:
```bash
rg -lF "ADR-{NNN}" docs/ docs/components/ handoffs/ 2>/dev/null
```

**1b. Topic scan** — extract keywords from the ADR title and Context section. Match against the topic-to-file mapping table to find conceptually-affected files even without explicit citations:

| ADR Topic Keywords | Architecture Files to Check |
|---|---|
| database, storage, data, persistence | `docs/04-data-flow-patterns.md`, `docs/06-technology-stack.md` |
| API, protocol, REST, gRPC, HTTP | `docs/05-integration-points.md`, `docs/06-technology-stack.md` |
| security, auth, encryption, identity | `docs/07-security-architecture.md` |
| scaling, performance, cache, latency | `docs/08-scalability-and-performance.md` |
| deployment, infrastructure, cloud | `docs/09-operational-considerations.md`, `docs/06-technology-stack.md` |
| framework, language, runtime, library | `docs/06-technology-stack.md` |
| architecture pattern, layer, structure | `docs/03-architecture-layers.md` |
| messaging, events, queue, stream, kafka | `docs/04-data-flow-patterns.md`, `docs/05-integration-points.md` |

Add any matched files not already in the citation list.

**1c. Handoff scan** — scan `handoffs/` for references to this ADR; also include handoffs for components that match the ADR topic:
```bash
rg -lF "ADR-{NNN}" handoffs/ 2>/dev/null
```

**1d. Fact-change extraction** — read the ADR and produce a concrete bullet list of what changed. For a status-only change:
```
- Status: {old} → {new} (decision is now {authoritative/deprecated/rejected})
```
For a content-bearing supersede, compare the old and new Decision sections and list changed parameters (e.g., "Kafka retention 7d → 1d", "Added PostgreSQL fallback").

---

##### Phase 2: Generate "Documentation Updates Required" Checklist

Present to the user grouped by file type. For each file, state what needs to change and why.

```
═══════════════════════════════════════════════════════════
DOCUMENTATION UPDATES REQUIRED — ADR-{NNN} ({title})
═══════════════════════════════════════════════════════════

Status change: {old_status} → {new_status}
Fact changes:
- {bullet list from Phase 1d}

─── Architecture Docs (docs/) ────────────────────────────
1. [ ] docs/04-data-flow-patterns.md — {what needs updating and why}
2. [ ] docs/06-technology-stack.md — {what needs updating and why}

─── Component Files (docs/components/) ───────────────────
3. [ ] docs/components/08-confluent-kafka.md — {what needs updating}

─── Handoff Docs (handoffs/) ────────────────────────
4. [ ] handoffs/08-confluent-kafka-handoff.md — {what needs updating}

─── No Updates Required ──────────────────────────────────
ℹ️  docs/07-security-architecture.md — references ADR-{NNN} but content is status-independent
═══════════════════════════════════════════════════════════
Approve all updates? ('all' / comma-separated numbers to deselect / 'skip')
```

**Wait for user response:**
- `all` or Enter → proceed with all items
- `1,3` → deselect those numbers (mark as manual)
- `skip` → add `<!-- PROPAGATION PENDING: downstream docs not yet updated ({date}) -->` to the ADR file and stop

---

##### Phase 3: Execute Updates

For each approved item, apply the change following the architecture-docs Context Anchor Protocol. **Never modify `docs/` or `handoffs/` without loading the required context first.**

**For `docs/*.md`, `docs/components/*.md`, and `docs/components/**/*.md`:**
1. Load Context Anchor — universal foundation (`docs/01-system-overview.md` + `docs/02-architecture-principles.md`) + section-specific parents per the dependency tier table + the changed ADR
2. Read the target file
3. Identify specific passages: ADR citations (`per [ADR-NNN]`), facts derived from the ADR, status references
4. Apply changes:
   - Status changes: update `per [ADR-NNN]` citations to note the new status where relevant
   - Deprecated/rejected: add `<!-- ADR-{NNN} deprecated/rejected — review this section -->` beside affected content
   - For supersede: replace `per [ADR-{old}]` with `per [ADR-{new}]`; update derived facts
5. Run the 5-check Post-Write Alignment Audit (Checks A–E from architecture-docs)
6. Mark `[x]` in the checklist

**For `handoffs/*.md`:**
1. Read the handoff file
2. Locate ADR references (typically Section 13 "ADRs Referenced") and any content derived from the ADR decision
3. Update following the handoff Documentation Fidelity Policy: only change what the ADR changed; preserve all other content
4. Mark `[x]` in the checklist

**For `ARCHITECTURE.md` Section 12 table:**
Update the ADR row's Status column to reflect the new status (this is within this skill's authority).

---

##### Phase 4: Propagation Report

```
═══════════════════════════════════════════════════════════
ADR CHANGE PROPAGATION — COMPLETION REPORT
═══════════════════════════════════════════════════════════

ADR: ADR-{NNN} — {title}
Change: {old_status} → {new_status}

Documentation updates completed:
[x] docs/04-data-flow-patterns.md — retention figures updated
[x] docs/components/08-confluent-kafka.md — retention figures updated
[x] handoffs/08-confluent-kafka-handoff.md — acceptance criteria updated

Deselected (manual update required):
[ ] docs/09-operational-considerations.md — DR runbook: confirm two-phase recovery procedure

Failed (require manual review):
⚠️  {list any files where the edit could not be applied cleanly}

Pending markers added:
ℹ️  {list any <!-- PROPAGATION PENDING --> or <!-- ADR deprecated --> markers placed}
═══════════════════════════════════════════════════════════
```

##### Phase 5: Asset Regeneration Advisory

**Runs after**: Phase 4 report is displayed.
**Also runs when**: User selected `skip` in Phase 2 and handoff files exist in `handoffs/` — in this case, note that handoff text was also not updated.

**Skip silently when**: No `handoffs/*.md` files appeared in the Phase 3 update list (completed, deselected, or failed) AND propagation was not skipped.

Load `../architecture-docs/references/ASSET_REGENERATION_ADVISORY.md` (architecture-docs skill, resolve under `[plugin_dir]/skills/`) and follow it (Steps 5a–5c; fact-deltas come from Phase 1d; use the ADR wording).

---

### Workflow 4 — Supersede an ADR

**Trigger**: User decides to replace an existing architectural decision with a new one.

ADRs are **immutable** — do not edit accepted ADRs. Create a new ADR that supersedes the old one.

#### Step 4.1: Create New ADR

Follow Workflow 2, collecting the new decision information. In the new ADR's header:
```
**Related**: Supersedes [ADR-{old}](ADR-{old}-{slug}.md)
```

> Workflow 2 Step 2.3 invokes the **ADR ID Format Gate (BLOCKING)** for the new ADR. The gate also runs implicitly here for the supersede pair (new and old IDs are both validated against the canonical regex before any file is touched). See `## ADR ID Format Gate (BLOCKING)` near the bottom of this file.

#### Step 4.2: Mark Old ADR as Superseded

Read the old ADR, update its status line:
```
**Status**: Superseded by [ADR-{new}](ADR-{new}-{slug}.md)
```
Add a `**Superseded Date**: {today}` field after the status line. Write the file back.

#### Step 4.3: Documentation Impact Propagation (Supersede)

Run the same 4-phase Documentation Impact Propagation as Workflow 3 Step 3.3, with these supersede-specific adjustments:

**Phase 1 adjustments:**
- Step 1a: rg for BOTH `ADR-{old}` and `ADR-{new}` across all `docs/`, `docs/components/`, `handoffs/`
- Step 1d: compare the old ADR's Decision section with the new ADR's Decision section to produce concrete fact deltas (what changed, what was added, what was removed)

**Phase 2 adjustments:**
- Checklist header shows: `Supersede: ADR-{old} → ADR-{new}`
- For each file: distinguish between (a) citation updates only (`per [ADR-{old}]` → `per [ADR-{new}]`) and (b) content updates where derived facts changed

**Phase 3 adjustments:**
- Replace all `per [ADR-{old}](../adr/ADR-{old}-slug.md)` citations with `per [ADR-{new}](../adr/ADR-{new}-slug.md)` in every affected file
- Update derived content to reflect the new decision's facts (changed parameters, changed approach, changed technology)
- Update `ARCHITECTURE.md` Section 12 table: old ADR row status → "Superseded", ensure new ADR row is present

**Phase 4 adjustments:**
- Report includes citation migration count: `{N} references migrated from ADR-{old} to ADR-{new}`

**Phase 5 (Asset Regeneration Advisory):**
- Run the same Phase 5 logic from Workflow 3 Step 3.3
- Fact-deltas come from the supersede comparison (old ADR Decision section vs. new ADR Decision section)
- Advisory prompt header says "ADR supersede propagation" instead of "ADR propagation"

#### Step 4.4: Confirm

```
✅ Done:
- Created: adr/ADR-{new}-{slug}.md (new decision)
- Updated: adr/ADR-{old}-{slug}.md (Status: Superseded by ADR-{new})
- Propagated: {N} downstream files updated, {M} deselected for manual review
```

---

### Workflow 5 — List / Audit ADRs

**Trigger**: User asks for an ADR inventory, status summary, or gap report.

#### Step 5.1: Scan adr/ Directory

```bash
ls -1 adr/ADR-*.md 2>/dev/null
```

For each file: extract number, title (from H1), status, date from file header.

#### Step 5.2: Display Summary

```
ADR Inventory — {project}
──────────────────────────────────────────────────────────────────────────
 #   Title                            Scope          Status       Date
──────────────────────────────────────────────────────────────────────────
 001 Technology Stack Selection       Institutional  ✅ Accepted   2024-01-15
 002 Database Policy                  Institutional  ✅ Accepted   2024-01-20
 101 PostgreSQL Primary DB            User           ✅ Accepted   2024-02-01
 102 Auth Strategy                    User           🔄 Superseded 2024-02-10
──────────────────────────────────────────────────────────────────────────
 4 total | 2 Institutional (001–100: 2/100 used) | 2 User/Project (101+)
         | 3 Accepted | 1 Superseded

⚠️  Gaps detected:
 - ADR-102 is Superseded — check that a superseding ADR exists
 - Consider reviewing: ADRs older than 6 months (ADR-001, ADR-002)
```

For ADRs missing a `**Scope**` field (legacy files), display scope as `Legacy` and note at the bottom:
```
ℹ️  {N} legacy ADR(s) have no Scope field. Numbers ≤100 are treated as Institutional,
    numbers ≥101 are treated as User. Add "**Scope**: Institutional | User" to those
    files to make the classification explicit.
```

---

## ADR ID Format Gate (BLOCKING)

Before any write to `adr/*.md`, validate the proposed ADR ID and filename against the canonical pattern defined in `ADR_GUIDE.md § ADR ID Format Rules`. This gate exists to block phase-prefixed (`ADR-P1-001`), version-suffixed (`ADR-101-v2`), or otherwise-embellished IDs that defeat the scope-by-number convention.

**Validation steps**:

1. **ID regex**: extract the bare ID (e.g., from `# ADR-101: Title` in the populated H1 line or from the proposed filename). Match against:

   ```
   ^ADR-\d{3,}$
   ```

   On mismatch → **ABORT** with:

   ```
   🚫 ADR ID Format Gate failed
   Proposed ID: {id}
   Expected: ADR-NNN (3+ digits, no letters, no extra hyphens, no phase/version/variant prefixes or suffixes)

   See ADR_GUIDE.md § "ADR ID Format Rules" for examples and the rationale.

   Common fix: the 101+ range already signals "project scope". Drop any
   phase / version prefix and use the next available sequential number.
   ```

   No waiver. The agent does NOT silently rename — it stops and surfaces the bug.

2. **Filename regex**: validate the full target path:

   ```
   ^adr/ADR-\d{3,}-[a-z0-9][a-z0-9-]*\.md$
   ```

   On mismatch → ABORT with the same message format (substitute "Proposed filename" for "Proposed ID").

3. **Scope-range sanity check** (advisory, non-blocking — surfaces miscategorization that the regex alone can't catch):
   - If the ADR's body declares `**Scope**: Institutional` and the number > 100 → warn, ask user to confirm.
   - If the ADR's body declares `**Scope**: User` and the number < 101 → warn, ask user to confirm.

**The gate is called from**:

- **Workflow 1** Step 1.5b — before every per-ADR file write in the materialize loop.
- **Workflow 2** Step 2.3 — immediately after slug + file path generation, before populating the template.
- **Workflow 4** Step 4.1 — implicitly via Workflow 2's gate when creating the new supersede ADR; the old ID is also re-validated when computing the `Supersedes [ADR-{old}]` link to prevent dangling references.

**The gate is NOT called from**:

- Workflow 3 (status updates) — these touch existing files only; their IDs have already passed the gate at creation time.
- Workflow 5 (audit/list) — read-only.

**Why a separate gate rather than inline regex** — placing the regex in one named gate lets Workflows 1, 2, and 4 share the abort message verbatim, keeps the canonical pattern co-located with the documentation in `ADR_GUIDE.md`, and gives the test surface a single anchor (`rg -c "ADR ID Format Gate" skills/architecture-definition-record/SKILL.md` should show ≥4 hits — one definition + invocations).

---

## ADR File Convention

- **Location**: `adr/` directory at the same level as `ARCHITECTURE.md`
- **Naming**: `ADR-NNN-brief-title.md` (zero-padded, lowercase, hyphen-separated)
- **Template**: `skills/architecture-definition-record/adr/ADR-000-template.md`
- **Guide**: `skills/architecture-definition-record/ADR_GUIDE.md`

**Status lifecycle:**
```
Proposed → Accepted → Deprecated → Superseded by ADR-NNN
           ↓
        Rejected
```

**Immutability rule**: Once Accepted, never edit content. Create a new ADR that supersedes it instead.

---

### Workflow 6 — Import Institutional ADR Catalog

**Trigger**: User supplies a directory of institutional ADRs ("import institutional ADRs", "load the institutional ADR catalog", "here is the ADR directory"), or `architecture-docs` Workflow 1 detects institutional citations that resolve to no file in `adr/`.

**Objective**: Copy the institutional ADRs (001–100) from an external catalog into the project's `adr/` so that every institutional citation resolves locally.

#### Why this is mandatory, not a convenience

An institutional catalog kept outside the project breaks three things silently:

| Breakage | Mechanism |
|---|---|
| **ID collision** | Step 2.1b computes `institutional_numbers` from `adr/ADR-*.md`. With the catalog external, that set is empty and a new institutional ADR is minted as **ADR-001**, colliding with the real one. |
| **Unverifiable citations** | Layer 2 principle review, compliance validators and traceability resolve `per ADR-NNN` against whatever is in `adr/`. With the catalog external they fall back to a hand-maintained summary table, and a lossy one-line summary produces confidently wrong findings. |
| **Non-portability** | An absolute path (`C:\...\ADRs Institucionales\es`) resolves on one machine. Every other reader, agent and CI run sees a dangling reference. |

**The rule**: whenever the user provides an institutional ADR directory, the ADRs are **copied into the project**, not linked and not merely cited. A path recorded in `docs/11-references.md` is not a substitute.

#### Step 6.1: Resolve the catalog — clone it, then pick the edition

The catalog is a **git repository**; the skill clones it. The user supplies a URL, never a directory — a directory on one machine is the non-portability defect this workflow exists to remove.

1. Take `catalog_url` and optionally `ref` (default `main`) from the user. If `adr/.institutional-catalog.json` (the **pin**, Step 6.8) already exists, this is a re-import: read `remote` / `ref` from it and prefer Workflow 9, which handles changed files.
2. Clone into `.cache/sa-skills/adr-catalog/` — project-relative, gitignored, and already granted under `.cache/sa-skills/**`:
   ```bash
   git clone --depth 1 --branch <ref> <catalog_url> .cache/sa-skills/adr-catalog
   ```
   When the directory already exists, compare `git -C .cache/sa-skills/adr-catalog remote get-url origin` with `catalog_url`. Same → refresh it (`git -C … fetch --depth 1 origin <ref>` then `git -C … checkout --force --detach FETCH_HEAD`). Different → the user changed the URL: delete the clone and clone again. Never merge two remotes into one clone.
3. Record `commit` = `git -C .cache/sa-skills/adr-catalog rev-parse HEAD`. It goes into the pin.
4. Select the edition matching the project's `<!-- DOC_LANGUAGE: -->` marker — `es` → the `es/` subdirectory, anything else → the clone root. Import exactly one edition; never both. `edition_dir` is the directory the remaining steps read.

**Changing the catalog URL later**: the user says "change the ADR catalog URL to <url>" (or edits `remote` in the pin by hand). The next Workflow 9 run sees the mismatch in step 2, re-clones, and re-pins. No other file records the URL — `docs/11-references.md` cites the in-project `adr/` location, not the remote.

**Permissions**: `Bash(git clone *)` and `Bash(git -C .cache/sa-skills/adr-catalog *)` — `/setup` adds both from `.claude/settings.json.example`. The clone path is fixed so the grant can be narrow. `Bash(bun *)` covers the CLI below.

#### Step 6.2: Enumerate and filter by range

Select only files whose ID falls in **001–100**. Files numbered 101+ in the source are project ADRs of some other project and MUST NOT be imported. Non-ADR files in the catalog (`README.md`, index files, knowledge-source notes, `_to_delete/`) are not imported.

**One exception**: `COVERAGE_MAP.json`, when the edition carries one, **is** imported alongside the ADRs. The catalog keeps **one map per language edition, beside that edition's ADRs** — `<root>/COVERAGE_MAP.json` for `en`, `<root>/es/COVERAGE_MAP.json` for `es`. Import the map from `edition_dir` only; the other edition's map describes ADR text the project does not hold. It records which compliance requirements each decision can satisfy and under what predicate, and a contract's inherited verdict depends on that reading — so copying the decisions without the reading leaves an audit trail that shows what was cited but not what made it count. The root edition's map is the derivation of record; a translated edition's map is a **rendering** of it with the same codes, strengths and ratification, so importing either edition grants the same coverage. Import both together or neither: if the catalog holds ADRs and no map, say so and continue; if it holds a map and the ADR import is skipped, stop rather than half-apply. The imported map is **read-only in the project** for the same reason an imported ADR is — a local edit forks the institutional reading. Project ADRs (101+) take their own separate local map.

#### Step 6.3: Collision check (BLOCKING)

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts diff <edition_dir> . --sa-skills [sa_skills_dir]
```

On a first import every entry in `changes[]` must be `added`. Anything else means a local file already occupies the institutional range: `removed` is a file the catalog does not know, and `amended` / `status_only` / `cosmetic` / `superseded` is an ID already taken. STOP and report — do not overwrite. An existing project file in the institutional range is a scope defect the user resolves first (usually by renumbering it into 101+). When a pin exists, the right tool is Workflow 9, not this step.

#### Step 6.4: Copy without overwrite

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts apply <edition_dir> .
```

Without `--overwrite` an existing file is skipped and reported in `skipped_existing` — the no-clobber contract. Never `mv` and never edit inside the clone; the catalog remains the source of record.

#### Step 6.5: Repair links broken by the move (BLOCKING)

Relative links inside the imported files were written for their original location and silently break once the depth changes. After copying, scan the imported files for parent-relative link targets (`](../…)`) and resolve each one:

- Target now resolves from `adr/` → leave it.
- Target does not resolve, and the link text already names the file → collapse the link to a code span, keeping the reference and dropping the dead link.
- Target does not resolve and the reference matters → rewrite it to the imported sibling.

Sibling links between imported ADRs (`](ADR-0NN-….md)`) resolve unchanged once the whole range is imported — which is the reason Step 6.2 imports the range rather than only the cited subset.

#### Step 6.6: Verify

Report the count imported, then confirm: every ADR link in `adr/` and `docs/` resolves on disk; the institutional and project ranges are both intact; `institutional_numbers` is now non-empty, so Step 2.1b computes the next institutional number correctly.

#### Step 6.7: Update the reference index

If `docs/11-references.md` records the catalog by absolute path, replace that path with the in-project location. A machine-local path left in a committed document is the defect this workflow exists to remove.

> **Drift caveat** — imported ADRs are *copies*. They do not track the institutional catalog. When the Architecture Team publishes changes, run **Workflow 9** — it is the only path that replaces an existing institutional file, and it carries the change into the architecture. Never hand-edit an imported institutional ADR in the project: institutional content is owned by the Architecture Team, a local edit forks the standard, and Workflow 9 detects the edit against the pin and blocks until it is resolved.

#### Step 6.8: Write the pin

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts pin . \
  --remote <catalog_url> --ref <ref> --edition <en|es> \
  --commit $(git -C .cache/sa-skills/adr-catalog rev-parse HEAD)
```

`adr/.institutional-catalog.json` records the remote, ref, edition, commit, and the SHA-256 of every institutional file and of the coverage map as written. It is what turns the next sync into a diff between two commits instead of a file-by-file guess, and what lets Workflow 9 tell a catalog change from a local hand-edit. **Commit it with `adr/`.** The clone under `.cache/` is disposable; the pin is not. It is written before the index because Workflow 7 reads it for the index's catalog line.

#### Step 6.9: Regenerate the ADR index

Run Workflow 7. Step 6.2 deliberately does not import the catalog's own `README.md` — it is a foreign index describing a different directory — so an import that skips this step leaves the project's entire institutional range index-less, and every consumer that reads `adr/README.md` degrades on the very next run. The regenerated index carries the catalog line from the pin, so a reader sees which commit the institutional rows reflect.

---

### Workflow 7 — Sync ADR Index (`adr/README.md`)

**Trigger**: "sync ADR index", "regenerate ADR index", "rebuild adr/README.md" — or automatically as the final step of Workflows 1, 2, 3, 4, 6 and 9 (see the ADR Index Rule). A catalog sync that leaves the index untouched shows the old status, the old title and no successor for every row it changed — the index is the first place a reader looks after a sync, so it is regenerated last.

**Why it exists**: it is the ADR index every reader opens first, and the development and enterprise compliance readers name it in their read set.

**Run**: `bun [plugin_dir]/skills/architecture-definition-record/scripts/adr-index.js <project_root> --write`. It enumerates the ADR files, reads each one's id, title, status, date and successor, reads the catalog pin and writes the whole file; the extraction rules are in the script's header. Without `--write` it prints the file.

#### Output — `adr/README.md` (full regeneration — never a merge)

```markdown
# Architecture Decision Records

**Total**: 64 · **Institutional (001–100)**: 58 · **Project (101+)**: 6
**Institutional catalog**: `https://git.example.com/architecture/adr-catalog.git` @ `main` · edition `es` · commit `8f3c2a1` · synced 2026-09-02
**Last Synced**: 2026-09-02

| ID | Title | Status | Scope | Date | Superseded By |
|----|-------|--------|-------|------|---------------|
| ADR-001 | Estrategia de nube híbrida | Accepted | Institutional | 2024-05-10 | — |
| ADR-101 | Respaldo del caché de pedidos | Proposed | Project | 2026-08-30 | — |
```

Rules:

- Rows sorted by ID ascending; counts computed from the enumeration.
- The **Institutional catalog** line is copied from the catalog pin (`catalog-diff-cli.ts show-pin`), and omitted when the project imported no catalog: `remote`, `ref`, `edition`, the first 7 characters of `commit`, `synced_on`. It is the only provenance a reader of the index gets, and it is what an auditor compares across two projects to ask whether they hold the same institutional text. Omitted when there is no pin.
- The file is **machine-layer English** — heading, labels, column headers, `Scope` values and `Status` values never localize (see Documentation Language above). Only the Title column carries `doc_language` text, copied verbatim from each ADR's H1.
- Regenerate the whole file every sync. Never hand-edit, never merge, never preserve manual additions — anything a reader wants in the index belongs in an ADR file, where the next sync picks it up.

---

### Workflow 8 — Coverage map (not in this skill)

Deriving `COVERAGE_MAP.json` — which compliance requirements each institutional decision can satisfy — is the compliance
plugin's work, and it ships with an organization's compliance plugin when there is one. This skill only carries the map as
data: Workflow 6 imports it beside the ADRs, Workflow 9 diffs it and names the requirement codes whose reading changed.

---

### Workflow 9 — Sync Institutional Catalog

**Trigger**: "sync institutional ADRs", "update institutional catalog", "pull ADR catalog", "the Architecture Team published new ADRs", "change the ADR catalog URL to <url>" — or Workflow 6 finding a pin already in place.

**Objective**: bring the project's institutional range and coverage map up to the catalog's current commit, and carry every change into the architecture — citations of a superseded decision migrate to its successor, an amended decision's derived facts are rewritten where they are cited, and the compliance and handoff consequences are named. Workflow 6 cannot do this: its no-clobber contract is what makes a first import safe, and it is exactly what a re-import must break.

#### How the catalog changes — and what each change means here

Institutional ADRs are **amended in place or superseded**. The catalog never simply deletes one. The classifier in `utils/catalog-diff.ts` names seven outcomes; each maps to one action:

| `kind` | What the catalog did | What this workflow does |
|---|---|---|
| `added` (no `supersedes`) | New decision | Copy. No propagation — nothing cites it yet. Report any `docs/` text that already cites the id, since that citation now resolves. |
| `added` (with `supersedes`) | Successor of a superseded decision | Handled together with its predecessor's `superseded` entry — one supersede pair, one propagation. |
| `superseded` | Status → `Superseded by ADR-new` | **Workflow 4 Step 4.3**: every `per [ADR-old]` citation in `docs/`, `docs/components/`, `handoffs/` migrates to `[ADR-new]`, derived facts follow the new Decision, Section 12 marks the old row Superseded and adds the new one. |
| `amended` | Context / Decision / Consequences text changed, same id | **Workflow 3 Step 3.3** with fact deltas from `changed_sections`. Citations keep the id; passages that restate the decision are rewritten. |
| `status_only` | Status line changed (Accepted → Deprecated, Proposed → Accepted) | **Workflow 3 Step 3.3**, status-change path. |
| `cosmetic` | Wording outside the substantive sections, or a rename | Copy. If `renamed`, rewrite every link to the old filename. No checklist. |
| `removed` | File gone from the catalog | **Never deleted.** A removal violates the amend-or-supersede rule: report it for the Architecture Team, mark each citation `<!-- ADR-NNN withdrawn from catalog (<date>) — needs a replacement decision -->`, keep the file. |

The substantive sections are located by their English name, their localized name (the record vocabulary of `scripts/shared/record-structure.js` — `## 1. Contexto`, `## 2. Decisión`) or their `<!-- SECTION: -->` anchor, **whatever the heading style**: `## Context`, `## 1. Context`, `## 1) Context` and `### Context` all resolve, and `###` sub-headings stay inside their `##` section. When no substantive heading is recognised on either side of a pair, the code classifies it `amended` with `changed_sections: ["(unreadable)"]` — never `cosmetic` — and `warnings[]` carries `<id>: no Context / Decision / Consequences heading recognised …`: its citations are checked like any amendment's, and the heading style is worth fixing.

Two flags cut across kinds. `renamed` — same id, different slug — always adds a link rewrite. `local_drift` — the local file no longer matches the hash the pin recorded — is a hand-edit of an imported ADR and **blocks** Step 9.5.

#### Step 9.1: Read the pin (BLOCKING)

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts show-pin .
```

`null` → the catalog was never imported through Workflow 6; run it instead. Otherwise take `remote`, `ref`, `edition`, `commit`, `clone_dir` from the pin. If the user supplied a new URL, use it in place of `remote` — the mismatch is what makes Step 9.2 re-clone.

#### Step 9.2: Refresh the clone

Run Workflow 6 Step 6.1 items 2–4 with the pin's values (or the new URL). Record `new_commit`. Resolve `edition_dir` from the pin's `edition`, never from a fresh language inference — the project already holds one edition and must keep holding it.

#### Step 9.3: Classify

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts diff <edition_dir> . --sa-skills [sa_skills_dir]
```

Exit 0 → nothing differs. If `new_commit` still moved (a commit elsewhere in the repo), rewrite the pin (Step 9.8), regenerate the index (Workflow 7) so its catalog line moves, and stop with "already in sync at <new_commit>". Exit 1 → read the JSON: `changes[]`, `coverage`, `summary`, `warnings[]`.

**The judge on the `cosmetic` pairs** — `judge` in the JSON. The default engine is `agent`: `judge.note` names a
worksheet — does each pair's removed / added text change what the ADR decides, why, or what follows? Hand it to the
`sa-skills:reviewers:worksheet-judge` subagent (it writes the answers file beside it), then run the same command again with `--answers`: the pairs judged
substantive become `amended` (`changed_sections: ["(judged)"]`). `engine: "none"` means sa-skills was not found — the
`cosmetic` verdicts stand unjudged; say so in the Step 9.4 summary. Print every entry of `warnings[]` before the summary; a `no Context / Decision / Consequences heading recognised` warning means the classifier could not see that ADR's sections, so it is already `amended` (`(unreadable)`).

**Save the JSON** to `.cache/sa-skills/adr-catalog-sync/diff.json` (the final run, after `--answers`): Step 9.6's citation checklist reads it.

#### Step 9.4: Present the sync summary and stash the deltas — before any write

```
═══════════════════════════════════════════════════════════
INSTITUTIONAL CATALOG SYNC — <remote> @ <ref>
<pin.commit> → <new_commit>   edition: <es>
═══════════════════════════════════════════════════════════
Superseded   2   ADR-012 → ADR-041 · ADR-015 → ADR-042
Amended      3   ADR-007 (Decision) · ADR-020 (Decision, Consequences) · ADR-033 (Context)
Status-only  1   ADR-009  Accepted → Deprecated
Added        4   ADR-041 · ADR-042 (successors) · ADR-043 · ADR-044
Cosmetic     6   (2 renamed — links will be rewritten)
Removed      1   ADR-018  ⚠ cited in 3 files — will be marked, not deleted
Unchanged   47

Coverage map: changed — 5 entries (3 ratified, 1 unratified, 1 edited)
  affected codes: SEC02, SRE01, SRE04, CLD01 → contracts: security, sre, cloud

⚠ Local drift: ADR-010 was edited in this project after the last sync.
═══════════════════════════════════════════════════════════
```

**Local drift blocks.** For each drifted file the user chooses: `discard` — the catalog wins and the local text is lost; or `abort` — stop the sync so the local change is moved into a project ADR (101+) first. There is no merge: institutional text is not the project's to change.

**Stash the fact deltas now**, while the old text is still on disk. For every `superseded`, `amended` and `status_only` entry read the local file (old) and the catalog file (new) and write the Phase 1d comparison — changed parameters, added/removed obligations, status transition — to `.cache/sa-skills/adr-catalog-sync/<id>.md`. For a supersede pair compare the old Decision with the successor's Decision. Step 9.5 overwrites the old text; Step 9.6 reads the stash.

Wait for the user's go-ahead on the summary. Nothing has been written yet.

#### Step 9.5: Apply

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts apply <edition_dir> . --overwrite
```

`written[]` lists every file replaced or added, `renamed_from[]` the old filenames deleted, `left_in_place[]` the `removed` ADRs kept. Then run Workflow 6 Step 6.5 (link repair) over `written[]` — the imported text was written for the catalog's depth, not the project's.

#### Step 9.6: Impact propagation — one consolidated pass

**First, the citation checklist — by code, never by topic:**

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts citations .
```

It lists every line of `ARCHITECTURE.md`, `docs/` (the changelog excluded) and the project ADRs (101+) that cites an
`amended`, `superseded` or `status_only` ADR by its literal id, into `.cache/sa-skills/adr-catalog-sync/citations.md`.
**Every row is accounted for** in the Phase 2 checklist and the Phase 4 report: edited (a restated fact changed — the
stash says which) or unaffected (the line cites the decision without restating what changed). A topic scan finds more
places to look; it never replaces a row. Measured: a sync that searched by subject edited the two passages using the
decision's vocabulary and missed two in the same section that quoted it.

Then run Step 3.3 in **batch mode**, feeding it every entry that needs one:

- **Supersede pairs** (`superseded` + its `added` successor): Phase 1 greps for both ids; Phase 3 migrates `per [ADR-old](../adr/ADR-old-slug.md)` to `per [ADR-new](../adr/ADR-new-slug.md)` and rewrites the derived facts from the stash. When the new Decision changes something the old one fixed (a retention figure, a mandated product, a boundary), that is a content update, not a citation swap — Phase 2 distinguishes the two per file, exactly as Step 4.3 does.
- **Amended**: Phase 1b topic scan uses the changed sections' keywords; Phase 3 rewrites passages that restate the decision. An amendment that only tightens Context needs no `docs/` edit unless a passage quotes it — say so in the "No Updates Required" block rather than inventing a change.
- **Status-only**: the Step 3.3 status path (deprecated/rejected markers, Section 12 status column).
- **Renamed**: rewrite every `ADR-NNN-<old-slug>.md` link target across `docs/`, `handoffs/`, `adr/` — including inside other institutional ADRs just written, which the catalog already updated, and project ADRs (101+), which it did not.
- **Removed**: place the `withdrawn` marker beside each citation; list the file under "manual review" with the Architecture Team as the owner. If nothing cites it, report it and offer deletion — do not delete unasked.

Phase 2 presents **one** checklist grouped by ADR. Phases 3–5 (execute, report, Asset Regeneration Advisory) run once over the union. Compliance output, when a compliance plugin wrote any, is **not** edited here — Step 9.7 names it.

#### Step 9.7: Name the downstream consequences

Both consumers below fingerprint what they read, so they will regenerate on their own next run. The sync's job is to say so, with specifics, so the user can choose to run them now:

- **Compliance** (when a compliance plugin is installed) — `coverage.affected_codes` are requirement codes whose inherited verdict just changed, and every `amended` / `superseded` / `status_only` ADR with status `Accepted` on either side may change a contract that cites it. List them; the compliance plugin regenerates what it fingerprints on its next run.
- **Handoff kit** — `handoffs/CROSS_CUTTING_STANDARDS.md` is synthesized from institutional ADRs and cites them rule by rule. When it exists and any Accepted institutional ADR changed, the context builder's payload hash moves and the next `generate dev handoff` regenerates it (and any Seam or Component Specification whose `related_adrs` include a changed id). Offer it.

#### Step 9.8: Write the pin

```bash
bun [plugin_dir]/skills/architecture-definition-record/utils/catalog-diff-cli.ts pin . \
  --remote <remote> --ref <ref> --edition <edition> --commit <new_commit>
```

Written after propagation, so the recorded hashes are those of the files as they now stand, and before the index, so Workflow 7 can print the new commit.

#### Step 9.9: Index, Section 12 and report

Run **Workflow 7** — not optional, and not "if anything changed": every `superseded`, `amended`, `status_only`, `added`, renamed and `removed` row reads differently after Step 9.5, and the catalog line must show `<new_commit>`. The index is regenerated wholesale, so a `renamed` ADR loses its old filename row and a `superseded` one gains its successor in the last column without any per-row bookkeeping.

Update `ARCHITECTURE.md` Section 12: status column for every `status_only` and `superseded` row, a new row for every `added` ADR the architecture now cites, `Superseded by ADR-new` on the old row of each pair.

```
═══════════════════════════════════════════════════════════
INSTITUTIONAL CATALOG SYNC — COMPLETION REPORT
═══════════════════════════════════════════════════════════
Catalog: <remote> @ <ref>   <old_commit> → <new_commit>
Applied: 16 written · 2 renamed · 1 left in place (removed) · coverage map updated

Propagated:
[x] 9 files — citations migrated ADR-012 → ADR-041 (14 references)
[x] docs/07-security-architecture.md — ADR-007 amendment: key rotation 90d → 30d
[ ] docs/09-operational-considerations.md — deselected, manual review

Withdrawn from catalog (manual — Architecture Team):
⚠ ADR-018 — cited in docs/05, docs/components/03, handoffs/interfaces/… (marked)

Next runs will regenerate:
• compliance: CC-security, CC-sre, CC-cloud (codes SEC02, SRE01, SRE04, CLD01)
• handoff kit: CROSS_CUTTING_STANDARDS.md, 2 seams (related_adrs include ADR-012)

Index regenerated: adr/README.md — 64 rows · catalog line @ <new_commit>
Pin written: adr/.institutional-catalog.json — commit it with adr/.
═══════════════════════════════════════════════════════════
```

> **Why the pin and the classifier are code, not prose.** A sync that lets the model decide what changed by reading two directories will, on a 60-file catalog, miss a rename, call a status flip an amendment, or overlook that an imported file was edited locally last month. Each of those turns into a wrong checklist in Step 9.6 and a citation that points at the wrong decision. The classifier decides the bucket; the model decides what the bucket means for this architecture.

---

### Workflow 10 — Compact ADRs

**Trigger**: "compact ADRs", "reduce ADR verbosity", "restyle ADRs", or Workflow 12 of `architecture-docs` handing over
the project ADRs over budget.

**Scope**: project ADRs (101+) only. Institutional ADRs (001–100) are copies of the catalog and are never rewritten
here; in catalog mode every ADR is in scope (`workflows/catalog-mode.md` § Compacting an ADR).

**Standard**: `ADR_GUIDE.md` § Decision Body and Amendment Log — the body states the decision in force, per-section
budgets, one Review History row per amendment.

1. **Baseline and measure** — commit or stash unrelated changes to `adr/`, record `git rev-parse HEAD`, then:
   - `bun [plugin_dir]/scripts/shared/record-budgets.js adr/ADR-1*.md` → the `adr-*` findings
     (section, body, log-entry lengths);
   - optional (`architecture-docs`; without it, say so): `bun [sa_skills_dir]/skills/architecture-docs/scripts/prose-check.js <project_root> --scope records` → edit-marker
     comments (`S-HIST-02`), dated narration (`S-HIST-01`), hedges, length — the log sections are skipped — and a
     localized structure or anchor comment (`S-STRUCT-01`).
   Report per ADR: words now, the sections over budget, the narration count. Stop for confirmation.
2. **Rewrite each ADR in place**, one `Edit` per passage, never a whole-file `Write`:
   - delete edit-marker comments;
   - dated narration in the body → the current state; the change, if not already there, becomes **one** Review
     History row (date · reviewer · `Amended` · what changed, ≤ 30 words, with the section it touched);
   - a Review History row that argues → one line; the argument goes into the body, rewritten in place, or is dropped
     when the body already states it;
   - an argument another ADR decides → one sentence and a link to that ADR (`fact-locate.js` confirms the target
     states it before the passage is deleted; without `architecture-docs`, read the target):
     optional — `bun [sa_skills_dir]/skills/architecture-docs/scripts/fact-locate.js <project_root> --removed "<text>" --target adr/ADR-NNN-….md#Decision`;
   - Alternatives: ≤ 3, one table (option · why not); Consequences: bullets, one consequence each.
   The rule is **never drop a decision, a constraint or a qualifier**: `Proposed` stays `Proposed`, a severity, a
   "no verificado", an unmeasured threshold stay as they were.
3. **Review** — restore every qualifier the rewrite dropped; without `architecture-docs`, compare by hand:
   optional — `bun [sa_skills_dir]/skills/architecture-docs/scripts/qualifier-check.js <project_root> --base <baseline> --file adr/…`;
   re-run `record-budgets.js` and `prose-check.js --scope records` until the ADRs are within budget or the remaining
   findings are named with a reason.
4. **Sync the index** (Workflow 7) and report words before → after per ADR.

### Workflow 11 — Amend an ADR (catalog mode)

**Trigger**: "amend ADR-NNN", "change the value in ADR-NNN", "update the institutional ADR", in a catalog repository.
The whole workflow — the five outcomes of a change, the in-place rewrite, broadening, the editions, coverage — is
`workflows/catalog-mode.md` § Workflow 11. In a consuming project an institutional ADR is never amended: the change
goes to the catalog, and the project gets it through Workflow 9.

---

## Integration with Other Skills

| Skill | ADR Interaction | Delegation Required? |
|-------|----------------|---------------------|
| `architecture-docs` | Reads ADRs for context; delegates creation to this skill; **delegates institutional catalog import to Workflow 6**; **receives downstream update requests during ADR change propagation (Step 3.3 / 4.3)** | YES for create; YES for import; YES for propagation edits |
| `architecture-docs-export` | Reads `adr/*.md`, exports to .docx | NO (read-only) |
| `architecture-component-guardian` | Reads ADRs for alignment context | NO (read-only) |
| `architecture-dev-handoff` | Cross-Cutting Standards is synthesized from institutional ADRs; Seams and Component Specifications cite them; **receives update requests during ADR change propagation (Step 3.3 / 4.3 / 9.6)**; payload hashes move after a Workflow 9 sync, so the next kit run regenerates the affected parts | YES for propagation edits |

---

## Success Criteria

- [ ] ADR file written to `adr/ADR-NNN-slug.md` with correct naming convention
- [ ] For institutional catalog import (Workflow 6): cloned from a URL into `.cache/sa-skills/adr-catalog/`, range 001–100 only, one edition and that edition's `COVERAGE_MAP.json`, no file overwritten, every parent-relative link repaired, `docs/11-references.md` carries no machine-local absolute path, and `adr/.institutional-catalog.json` written
- [ ] For institutional catalog sync (Workflow 9): summary and fact-delta stash shown before any write, local drift resolved (never merged), `apply --overwrite` then link repair, one consolidated propagation checklist with supersede citations migrated to the successor, `removed` ADRs marked and kept, compliance/handoff consequences named with contract and file specifics, index regenerated, pin advanced to the new commit
- [ ] Template populated: no placeholder data in comparison tables
- [ ] Status field set correctly
- [ ] ARCHITECTURE.md Section 12 table updated if requested
- [ ] For supersede operations: old ADR marked `Superseded by ADR-NNN`, new ADR references old one
- [ ] For status changes and supersede: Documentation Impact Propagation checklist generated and presented (Step 3.3 / 4.3)
- [ ] All approved propagation items completed or marked with `<!-- PROPAGATION PENDING -->` / `<!-- ADR-NNN deprecated -->` tracking markers
- [ ] For propagation with handoff impact: Asset Regeneration Advisory displayed when asset-impacting keywords detected in fact-deltas (Phase 5)
