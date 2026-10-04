---
name: design-doc-template
description: Use when asked to record an approved or sufficiently converged design in the standard design-doc format. Use mak:dev-kickoff first if requirements or approval remain unresolved.
---

# Design Doc Writing Guide

All design docs follow this guide's section structure and writing rules.
Template file: `${CLAUDE_PLUGIN_ROOT}/skills/design-doc-template/assets/design-doc.template.md` (in English; produce the actual document in the user's language — or the project's documented language policy — keeping the structure).

---

## When to Use

- Recording a new feature, component, or architecture decision
- Planning a change spanning multiple files
- **Single-concern work whose upfront analysis fits one document, even if split across multiple PRs** — handle with a master doc + per-PR sub-docs (see §Multi-PR Work below)
- Recording already-organized options and a recommendation in design-doc form
- Fixing a design confirmed after mak:brainstorming / mak:dev-kickoff into an official document

## Section Structure

### Required sections (keep order)

| # | Section | Core question |
| :--- | :--- | :--- |
| 1 | Purpose / Non-goals | Why do this? What is out of scope? |
| 2 | Current State Analysis | What is the state now? What is the problem? |
| 3 | Design Direction | How will it be solved? What are the options? |
| 4 | Scope of Changes | Which files/components change? |
| 5 | Verification Plan | How will it be verified? |
| 6 | Decisions Needed | What must be chosen before approval? |
| 7 | Assumptions / Unverified Areas | What was assumed or not confirmed? |
| 8 | References | Related files, commits, external docs |

### Optional sections

- `Implementation Checklist` — when a stepwise task list is needed
- `Schema / Type Definitions` — when data-structure changes are included

## Writing Rules

### Meta block (top of file, no YAML frontmatter)

```
> Target: <files or modules being changed>
> Related rules: <paths of related convention docs>
> Date: YYYY-MM-DD
> Status: draft (needs approval before implementation) | approved | in progress | done
```

### Option comparison table

When there are 2+ options, always compare in a table. Bold the recommendation.

```markdown
| Option | Description | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **A. <name>** (recommended) | ... | ... | ... |
| B. <name> | ... | ... | ... |
| C. <name> | ... | ... | ... |

**Recommendation**: **A**. <1–2 sentence reason>
```

### "Assumption" notation

Unconfirmed facts and assumptions must be explicitly marked.

```markdown
- **Assumption**: <unconfirmed fact>. Verify during implementation.
- **Unreviewed**: <item not yet examined>.
```

### Scope-of-changes table columns

```markdown
| # | File | Change type | Content |
| :-- | :--- | :--- | :--- |
| 1 | `<file path>` | create / modify / delete | <summary of change> |
```

Change types: `create` / `modify` / `delete` / `move` / `rename`

### Save location — SSOT for all mak skills/agents

This rule is the **single source of truth** for where design docs live. Other mak skills and agents refer to this rule instead of restating paths.

1. If the project's CLAUDE.md or agent rules specify a design-doc path → use that path
2. Otherwise → `.claude/mak/plan/` (create the directory if it does not exist)

### File naming

- General design: `<topic-slug>.md` (e.g. `auth-flow.md`)
- Roadmap phase: `phase<N>-<topic>.md` (e.g. `phase3-audit-log.md`)
- If a file with the same slug exists, add a `-v2`, `-v3` suffix and reference the previous version's path at the top of the new file

### Multi-PR work — master doc + per-PR sub-docs

Large single-concern work split across PRs (e.g. structural refactor, sequential expansion) is handled inside this skill. **If the upfront analysis fits one document, a design doc suffices even for multi-PR work.**

- **Master doc** — pins decisions, policies, the **PR dependency graph**, and overall consistency only. No per-file/per-line detail.
- **Per-PR sub-doc** — written at each PR's entry. Contains that PR's changed files/lines and verification steps; state at the top that **the master doc wins** on conflict. Do not start implementation (mak:coder delegation) before the sub-doc exists.
- **Naming** — master and sub-docs share an axis. If tied to a roadmap section: master `<roadmap-section>-<slug>.md` / sub-doc `<roadmap-section>-<n>-<slug>.md`; otherwise master `<topic-slug>.md` / sub-doc `<topic-slug>-<n>-<slug>.md`. (Project doc-path conventions take precedence.)

### Verification plan — Step → verify table (§5.0)

For multi-step work, include this table as §5.0 inside §5 Verification Plan. Single-step work may state a one-line success criterion instead.

```markdown
### 5.0 Success Criteria / Step → verify

| # | Step | verify (success criterion) | Status |
| :-- | :--- | :--- | :--- |
| 1 | <step description> | <measurable verification> | ✅ done |
| 2 | <step description> | <measurable verification> | ▶ in progress |
| 3 | <step description> | <measurable verification> | ⬜ todo |
```

Success criteria must be verifiable (no vague criteria like "it just works").

**Step status column** — write every row as `⬜ todo` when the doc is created. Advancing a row is the **implementer's** job, not this skill's: whoever implements the step (the `mak:coder` agent, or the main thread implementing directly) moves it **only after its verify criterion actually passes** (`▶ in progress` for the row being worked). This column is the document's progress record: it lets `mak:dev-resume` read how far work got instead of inferring it from commits and code. Keep it here only — the meta block's `Status` tracks the **document** (draft/approved/in progress/done), this column tracks **each step**, and no other place restates either.

## Quality Checklist

Self-check after writing:

- [ ] All "TBD", "TODO", and incomplete sentences removed?
- [ ] No contradictions between sections?
- [ ] Scoped to a single implementation cycle?
- [ ] Every question in §6 has a recommendation?
- [ ] All assumptions/uncertainties recorded in §7?
- [ ] No files missing from the §4 scope table?
- [ ] At least one simpler alternative in the option comparison?
- [ ] No unrequested features / speculative flexibility or configuration / impossible-scenario error handling / excessive abstraction?
- [ ] Every file/line in §4 directly connected to the user's request?
- [ ] §5.0 contains a measurable success criterion or `Step → verify` table?

## References

- Template: `${CLAUDE_PLUGIN_ROOT}/skills/design-doc-template/assets/design-doc.template.md`
- Style reference: existing design docs under the project's design-doc path
