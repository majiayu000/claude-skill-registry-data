---
name: skill-reviewer
description: >
  Audit an existing processkit skill against the 5 Skill Killers,
  the Agent Skills standard, and Anthropic's troubleshooting playbook,
  producing a categorized findings report and draft Gotchas.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-skill-reviewer
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: skill-builder
        purpose: "Reference the canonical skill format and the 5 Skill Killers checklist that skill-builder enforces during creation. skill-reviewer applies the same rules to existing skills."
      - skill: index-management
        purpose: "Locate the skill being reviewed and surface related skills it should reference under uses:."
      - skill: event-log
        purpose: "Log skill.reviewed events so the project's audit trail captures review history."
    provides:
      primitives: []
      mcp_tools: []
      assets: []
      processes: [skill-review, gotchas-generation]
    commands:
      - name: pk-skill-audit
        args: "skill-name"
        description: "Run a full 13-category review of the named skill"
---

# Skill Reviewer

## Intro

`skill-reviewer` audits an existing processkit skill against the
canonical format, the 5 Skill Killers, the Agent Skills standard, and
Anthropic's troubleshooting playbook. It produces a categorized findings
report (must-fix / should-fix / nit) and, crucially, **generates draft
Gotchas content for any skill whose Gotchas section is missing, empty,
or generic** — the killer feature that lets one skill-reviewer pass
populate the Gotchas section of every skill in the catalog.

skill-reviewer is the brownfield counterpart to `skill-builder`:
skill-builder is for greenfield (creating new skills), skill-reviewer
is for everything else (auditing, fixing, retrofitting).

## Overview

### When to use skill-reviewer

- The user says *"review the X skill"*, *"check skills/Y"*, *"is this
  skill good"*, *"audit skills/"*, *"lint the X skill"*, or *"generate
  gotchas for X"*.
- A new skill has just been created and you want a second-pass quality
  check before committing.
- The Agent Skills standard or the format spec changed, and existing
  skills need a sweep.
- Bulk operation: **populate Gotchas across the whole catalog** by
  running skill-reviewer over every skill in `src/skills/`.

### The review checklist (13 categories)

For each skill, check all 13 categories. Surface findings under one
of the three severity buckets at the end.

#### 1. Frontmatter compliance (Agent Skills standard)

- Top-level `name` exists, kebab-case, matches the directory name.
- Top-level `name` does NOT contain "claude" or "anthropic" (reserved
  by Anthropic).
- Top-level `description` exists and is < 1024 characters.
- Top-level `description` includes BOTH what AND when (with literal
  trigger phrases the user would say).
- NO XML angle brackets (`<` / `>`) anywhere in frontmatter.
- `metadata.processkit.apiVersion` is present and equals
  `processkit.projectious.work/v1`.
- `metadata.processkit.id` is present and equals `SKILL-<name>`.
- `metadata.processkit.version` is a valid semver string.
- `metadata.processkit.created` is a valid ISO 8601 timestamp.
- `metadata.processkit.category` is one of the registered values
  (`process`, `language`, `framework`, `infrastructure`, `architecture`,
  `design`, `data`, `ai`, `api`, `security`, `observability`,
  `database`, `performance`, `meta`).
- For `category: process`, `metadata.processkit.layer` is an integer
  0-4. For other categories, `layer` is `null` or absent.
- Every `uses:` entry is an OBJECT with a `skill` field AND a `purpose`
  field. Bare strings or missing-purpose entries are must-fix.
- Every skill name listed under `uses:` actually exists in
  `src/skills/`.

#### 2. Section structure

- The body has these four section headings IN THIS ORDER:
  `## Intro`, `## Overview`, `## Gotchas`, `## Full reference`.
- No headings starting with `## Level 1`, `## Level 2`, or `## Level 3`
  (those were dropped in v0.6.0).
- The Intro is 1-3 sentences. Longer is should-fix.
- The Gotchas section is REQUIRED (must-fix if missing).

#### 3. The 5 Skill Killers (Skills Master Class)

| # | Killer | Symptom | Fix |
|---|---|---|---|
| 1 | Description doesn't trigger | Reads like a summary or contains "Use when…" clauses. | Rewrite as a one-sentence imperative (verb-first, under 200 chars). Move trigger phrases to skill-finder's trigger table (Category 9). |
| 2 | Over-defining process | Steps prescribed too rigidly when the agent should have degrees of freedom. | Loosen prescriptive language; distinguish "must" from "should" from "may". |
| 3 | Stating the obvious | Content the agent already knows from general training. | Cut. (BUT: be careful — what's obvious to Claude may not be to Gemini. Provider neutrality wins ties.) |
| 4 | Missing Gotchas | No `## Gotchas` section, empty section, or generic "be careful" content. | Generate draft gotchas — see Step 7 below. |
| 5 | Monolithic blob | SKILL.md > 5000 words. | Push detail to `references/<topic>.md`. |

#### 4. Anthropic troubleshooting playbook (PDF p25-27)

Check for the four diagnoses:

- **Under-trigger** signals: skill doesn't load when it should; users
  manually enabling it; support questions about when to use it. Fix:
  add detail/keywords to the description, especially for technical
  terms.
- **Over-trigger** signals: skill loads for irrelevant queries; users
  disabling it; confusion about purpose. Fix: add negative triggers,
  be more specific.
- **Instructions not followed**: Overview is too verbose, critical
  instructions buried, ambiguous language, or model laziness. Fix:
  put critical instructions at the top; use `## Important` headers;
  prefer code over prose; add explicit encouragement for thorough
  steps.
- **Large context**: SKILL.md too large; too many enabled skills
  simultaneously. Fix: 5000-word ceiling; references/ extraction.

#### 5. Directory structure

- `SKILL.md` exists at the skill root (case-sensitive, exactly that
  name).
- No `README.md` inside the skill folder (any depth).
- No `INDEX.md` inside the skill folder (parent `src/skills/INDEX.md`
  is fine).
- `scripts/` directory exists (may be empty with `.gitkeep`).
- If a `templates/` directory exists, that's a leftover from before
  v0.6.0 — should be `assets/`.
- If `mcp/` exists: `server.py` and `mcp-config.json` are present;
  `SERVER.md` is present (NOT `README.md`).
- If `mcp/` exists: the server name in both `mcp-config.json` and the
  `FastMCP(...)` call in `server.py` is prefixed with `processkit-`.
- If `metadata.processkit.commands` is non-empty: a `commands/`
  directory exists with one file per entry in the list.
- If `commands/` exists but `metadata.processkit.commands` is absent
  or empty: flag as should-fix (orphaned adapter files).
- If harness projection directories exist, `.claude/commands/` and
  `.agents/skills/` contain exactly the same command names as the canonical
  `commands/` files.

#### 6. Description quality

Beyond the < 1024 char length check:

- Description is a **one-sentence imperative** — verb-first (e.g.,
  "Author X", "Review Y for Z", "Generate W"). NOT narrative ("This
  skill helps you…") and NOT passive ("A tool for…"). Violation =
  should-fix.
- Description is **under 200 characters**. Anything longer is usually
  a sign of "Use when…" clauses being smuggled in — should-fix.
- Description does **NOT** contain "Use when the user says…" or
  similar trigger language. Trigger phrases belong in skill-finder's
  trigger-phrase table (Category 9), not here. Violation = must-fix.
- Description starts with the verb, not the noun. "Recommend models"
  beats "Model recommendation skill that recommends models." Violation
  = nit.

#### 7. Generate Gotchas (the killer feature)

If the Gotchas section is missing, empty, or generic, generate a draft.

Process:
1. Read the skill's Overview section to understand what it does.
2. Read the skill's `provides:` block to understand what it produces.
3. Read the skill's `uses:` block to understand what it depends on.
4. For each, ask the five Gotcha-generation questions from skill-builder
   Step 5a:
   - What would an agent get wrong on the first try?
   - What does the agent need to KNOW that the user wouldn't think to
     say?
   - Where would the agent helpfully overshoot?
   - Where would the agent helpfully undershoot?
   - What conventions are unique to this skill that the agent has to
     learn?
5. Draft 5-10 specific, provider-neutral failure modes.
6. Each draft Gotcha must have BOTH a specific failure AND a specific
   countermeasure. Generic items ("be careful", "double-check") are
   not acceptable drafts.
7. Cross-reference Anti-patterns under Full reference if some draft
   items overlap — Gotchas should be agent-only.

For domain skills (language/framework/infrastructure), useful seed
patterns to consider:

- Hallucinated APIs (the agent invents library functions that don't
  exist).
- Stale-syntax (the agent uses syntax from an older language version
  than the project targets).
- Ignoring project-specific conventions in favor of "best practice"
  defaults.
- Skipping verification steps when "the obvious thing" looks right.
- Provider blind spots (agents on harnesses without filesystem access
  hallucinating file contents).

#### 8. Cross-reference quality

- Skills mentioned in Overview/Full reference exist in `src/skills/`
  (no broken references).
- The `uses:` block is consistent with the body — every dependency
  mentioned in the body should appear in `uses:`, and every dependency
  in `uses:` should be referenced at least once in the body with its
  purpose explained.

#### 9. skill-finder registration

- The skill has at least 1 entry in the trigger-phrase table in
  `src/skills/skill-finder/SKILL.md`. Missing = must-fix — a skill
  not in skill-finder is invisible to agents who don't know its name.
- The skill has a one-liner in the appropriate by-category section of
  `skill-finder`. Missing = should-fix.
- The skill's `description:` field does NOT contain "Use when the user
  says…" or similar trigger language — those phrases belong here in
  the trigger table, not in the description. Violation = must-fix
  (cross-links with Category 6).

#### 10. Command adapter hygiene

Run this category only if `metadata.processkit.commands` is non-empty OR
`commands/` directory exists.

- Every entry in `metadata.processkit.commands` has a corresponding
  `commands/<name>.md` file. Missing file = must-fix.
- Every `commands/<name>.md` file has a corresponding entry in
  `metadata.processkit.commands`. Orphan file = should-fix.
- Each processkit command name starts with the reserved `pk-` prefix.
  Unprefixed processkit commands = must-fix.
- The `argument-hint` in each adapter file matches the `args` field in
  the corresponding `metadata.processkit.commands` entry. Mismatch =
  should-fix.
- `.claude/commands/<name>.md` has the same `argument-hint` as the
  canonical adapter. Mismatch = must-fix.
- `.agents/skills/<name>/SKILL.md` exists for each canonical command when
  the project ships `.agents/skills/`. Missing or extra command shims =
  must-fix.
- Each adapter file body is exactly one sentence invoking the skill
  and workflow. Multi-line bodies with workflow steps are should-fix —
  logic belongs in SKILL.md, not in the adapter.
- `allowed-tools` in each adapter is present and scoped narrowly.
  `Bash(*)` without justification = should-fix.
- SKILL.md Overview mentions the commands (one line per command
  referencing the adapter path). Absent mention = should-fix.

#### 11. Security and permission audit

Run this category for all skills (not only those with MCP servers).

**MCP tools** (if `mcp/` exists):

- Every `@server.tool()` has explicit annotations. Missing annotations
  on any tool = must-fix.
- `readOnlyHint: true` on all query / list / get / profile tools that
  do not write state. Missing = should-fix.
- `destructiveHint: true` on any tool that deletes, overwrites, or
  resets persistent state. Missing = must-fix.
- `openWorldHint: true` on any tool that makes HTTP or external API
  calls. Missing = must-fix.
- `idempotentHint: true` on tools where a duplicate call is harmless
  (e.g. delete by ID, set-config to same value). Missing = nit.

**SKILL.md permission surface:**

- If the skill calls MCP tools marked `destructiveHint: true`, the
  Gotchas section mentions that the agent must show the operation to
  the user and confirm before calling. Missing = should-fix.
- If the skill calls MCP tools marked `openWorldHint: true`, the
  Gotchas section notes that external calls are best-effort and
  failures should not be retried silently. Missing = should-fix.
- If the skill ships scripts in `scripts/` that write to the
  filesystem outside the skill's own directory, or make network
  calls, the Overview section includes a **Permissions** note listing
  what the scripts touch. Missing = should-fix.

#### 12. Behavioral completeness

Check that the skill encodes enough to prevent silent execution
failures — cases where the agent understands the workflow but then
fails to execute a step.

- **Skills that direct the agent to create entities** (WorkItems,
  DecisionRecords, Discussions, etc.): the Gotchas section must
  include a rule about calling the tool in the same turn as the
  commitment. Missing = should-fix.
- **Skills with multi-step workflows**: each step that produces a
  persistent artifact (entity, file, commit) should have a
  corresponding Gotcha about not deferring the write. Missing =
  should-fix.
- **All skills**: are Gotchas specific (failure described +
  concrete countermeasure), or are they generic encouragements
  ("be careful", "double-check") with no actionable fix? All-generic
  Gotchas = should-fix.
- **Process skills in particular**: at least one Gotcha must cover
  the gap between verbal commitment ("I'll do X") and execution
  ("called the tool"). Missing = should-fix.

#### 13. Library expert specialization

Run this category when the skill is a library expert, API expert, SDK
guide, framework recipe book, or similar version-sensitive domain skill.

- `metadata.library` exists with `name`, `version`, `homepage`,
  `docs`, and `source_date`. Missing `metadata.library` on a library
  expert = must-fix; missing individual fields = should-fix.
- The Intro or Overview states the version range the skill covers.
  Ambiguous "latest" claims are should-fix unless backed by a live-doc
  workflow.
- Recipe examples use one major version's API at a time. Mixed major
  versions = must-fix because they generate broken copy-paste code.
- Each recipe includes imports, setup, or prerequisites needed to run
  it. Missing runnable context = should-fix.
- The skill has a RAG Escalation or live-doc escalation section that
  says when to leave baked-in recipes. Missing escalation policy =
  should-fix.
- Gotchas include stale API risk and project-version mismatch risk.
  Missing both = should-fix.

### The findings report

After running through all 13 categories, output a structured report:

```markdown
# Review: <skill-name>

## Must-fix (severity: high)

- [Category N] <finding>: <fix>

## Should-fix (severity: medium)

- [Category N] <finding>: <fix>

## Nit (severity: low)

- [Category N] <finding>: <fix>

## Generated Gotchas draft

(Only if Category 7 was triggered.)

[5-10 draft gotchas in the standard format]

## Trigger test cases

(Only generated for skills with weak descriptions.)

Should trigger:
  - "..."
Should NOT trigger:
  - "..."
```

### Bulk operation: gotchas-pass over all skills

To populate Gotchas across the catalog in one batch:

1. Iterate over every `src/skills/*/SKILL.md`.
2. For each, run only Category 7 (skip the other categories for speed).
3. Skip skills whose Gotchas section is already present and substantive
   (≥ 3 specific items, not all generic).
4. Output the draft Gotchas as a patch the user can apply.
5. The user reviews the patch and either accepts it as-is, or polishes
   each draft before committing.

This is the workflow that produced the initial Gotchas content for
processkit's 100+ pre-existing skills (Thread 1 task #4).

A similar bulk pass can be run for **Category 11 (security audit)**:
iterate every skill with an `mcp/` directory and check that all tools
have annotations. Output missing annotations as a patch the user can
apply to each `server.py`.

A bulk pass for **Category 12 (behavioral completeness)** is useful
after any behavioral norm is added to AGENTS.md — verify that the
corresponding skill's Gotchas already encode the same rule.

This skill also provides the `/pk-skill-audit` command for direct
invocation — see `commands/pk-skill-audit.md`.

## Gotchas

Agent-specific failure modes when running skill-reviewer:

- **Treating "Stating the obvious" as license to gut content.** Killer
  #3 says cut what the agent already knows — but provider neutrality
  trumps. If something is obvious to Claude but not Gemini, KEEP IT.
  When in doubt, leave content in.
- **Generating Gotchas that just describe the skill's normal use.**
  *"Always remember to call the function"* is not a gotcha; it's
  documentation. Gotchas describe failure modes and countermeasures,
  not happy paths.
- **Generating identical Gotchas across multiple skills.** Each skill's
  Gotchas should be specific to that skill. If the same item appears
  for python-best-practices and rust-conventions, it's too generic —
  push it into a shared meta-skill or remove it.
- **Reporting nits as must-fix.** "Must-fix" is reserved for things
  that genuinely break the skill (frontmatter invalid, Gotchas
  missing entirely, name colliding with reserved words). Style and
  tone preferences are nits or should-fixes at most. Inflating
  severity trains users to ignore the report.
- **Skipping Category 1 because the file "looks right".** Frontmatter
  bugs are the most common silent failure. ALWAYS run Category 1
  even when the skill body looks polished.
- **Hallucinating Gotchas based on the skill's name alone.** Read the
  Overview and Full reference before drafting Gotchas. A title-only
  draft will produce generic content that the user has to throw
  away.
- **Forgetting to check `uses:` references actually exist.** A typo
  in a skill name under `uses:` (e.g., `index-managment`) silently
  breaks delegation. This is a must-fix that's easy to miss.
- **Reviewing your own work without skepticism.** If skill-reviewer
  is being used to review a skill that skill-builder just created,
  the temptation is to rubber-stamp. Run all 13 categories anyway —
  the whole point of the brownfield/greenfield split is independent
  validation.
- **Skipping Category 10 because no commands/ folder is visible.**
  Category 10 must also run when `metadata.processkit.commands` is
  non-empty even if the `commands/` directory is absent — the absence
  itself is the must-fix finding.
- **Skipping Category 11 for "knowledge-only" skills.** Even skills
  without an MCP server can ship scripts or instruct the agent to call
  external services. Run the SKILL.md permission surface checks for
  every skill, not only those with `mcp/`.
- **Treating missing annotations as a nit.** Missing MCP tool
  annotations are must-fix, not nits. A harness cannot surface
  confirmation prompts for destructive tools if it doesn't know the
  tool is destructive. The user may unknowingly approve state-destroying
  operations.

## Full reference

### Severity definitions

| Severity | Definition | Examples |
|---|---|---|
| **Must-fix** | The skill is broken or non-compliant in a way that prevents it from working. | Missing frontmatter, invalid YAML, missing Gotchas, name collision with reserved words, broken `uses:` reference, `mcp/README.md` violation. |
| **Should-fix** | The skill works but has known quality issues that will cause problems for users. | Generic Gotchas, description without trigger phrases, monolithic SKILL.md > 5000 words, buried critical instructions. |
| **Nit** | Style or tone preference. The skill works fine; reasonable people would disagree on whether to fix. | Verbose Intro (4-5 sentences instead of 1-3), inconsistent capitalization in headings, redundant cross-references. |

### Running skill-reviewer over a skill

Manual flow:
1. Read the SKILL.md file in full.
2. Walk through Categories 1-13.
3. For each finding, classify severity.
4. Generate the report in the format above.

### Running the bulk gotchas-pass

For populating Gotchas across the catalog:

1. Identify the target skills:
   ```
   query_entities(kind="Skill")  # via index-management
   ```
2. For each, check whether the Gotchas section is present and substantive:
   - Present: section heading `## Gotchas` exists.
   - Substantive: 3+ items, each with both a specific failure AND a
     specific countermeasure (not generic).
3. For skills failing the check, generate a Gotchas draft using the
   process in Category 7.
4. Output as a series of patches (one per skill) that can be applied
   in batch.

### Anti-patterns when reviewing

- **Drive-by review.** Skimming the SKILL.md and producing a one-line
  report is worse than no review. Take the time.
- **"Nothing wrong"** as a verdict. There's almost always something
  worth raising as a should-fix or nit. If you found nothing,
  re-read with the 5 Skill Killers in mind.
- **Suggesting rewrites of working code/content.** skill-reviewer
  surfaces problems and proposes specific fixes. It does NOT rewrite
  the whole skill — that's the user's call.
- **Reviewing without checking the format spec.** The canonical
  source of truth is `src/skills/FORMAT.md`. Re-read it if you're
  unsure about a convention.

### Cross-references

- `skill-builder` — the greenfield counterpart; same checklist applied
  during creation.
- `index-management` — query existing skills; locate the skill being
  reviewed; check that `uses:` references resolve.
- `event-log` — log `skill.reviewed` events with the findings count.
- `src/skills/FORMAT.md` — the canonical format spec.
