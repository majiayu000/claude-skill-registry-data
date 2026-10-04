---
name: tech-to-pm-translator
description: |
  Convert technical developer documentation into PM/designer-friendly context documents. Reads engineering docs (architecture refs, API docs, runbooks, ADRs, READMEs) and produces structured, code-free knowledge base files that non-engineers can use to understand systems, file better bugs, write better specs, and have informed conversations with engineers. Triggers on: "translate docs for PMs", "make this PM-friendly", "convert tech docs", "create PM context", "non-engineer version", "explain this for PMs", "designer-friendly docs", "/tech-to-pm".
---

# Tech-to-PM Translator

Converts technical developer documentation into structured, code-free knowledge base documents that PMs, designers, and other non-engineers can use to understand systems without reading code.

## Philosophy

This is a **translation** skill, not a **summarization** skill.

- **Summarization** loses detail. A PM reading a summary still can't answer questions.
- **Translation** reframes the same information for a different audience. A PM reading a translated doc can understand what breaks, why, and who to talk to.

The output preserves technical accuracy while stripping implementation detail and adding decision-support framing.

## When to Activate

- User says "translate docs for PMs", "make this PM-friendly", "convert tech docs"
- User says "create PM context from these docs", "non-engineer version"
- User says "explain this system for PMs/designers", "create onboarding docs"
- User has technical markdown files and wants them accessible to non-coders
- After a team writes architecture docs and wants broader org understanding

## Input

Required:
- **Source path**: Directory or glob pattern containing technical docs (e.g., `.claude/ref/`, `docs/architecture/`, `**/*.md`)

Optional:
- **Output path**: Where to write the translated docs (default: alongside source or user-specified)
- **Audience**: "pm" (default), "designer", "stakeholder", "new-hire" (adjusts framing depth)
- **Project name**: For context-specific terminology and ownership mapping
- **Existing context**: Path to existing PM docs to avoid duplication and maintain consistency

## Output Documents

The skill produces up to four document types depending on source material:

| Document | When Generated | Purpose |
|----------|---------------|---------|
| **Platform Guide** | Always | How the system works end-to-end: user flows, data pipelines, integrations |
| **Bug Anatomy** | When source docs cover components, failure modes, or debugging | Bug families, filing guide, priority framework, engineer communication tips |
| **Migration/Change Landscape** | When source docs describe transitions, deprecations, or active migrations | What's changing, dependency map, decision framework for fix depth |
| **Architecture Overview** | When source docs cover infrastructure, deployment, or system design | Updated tech architecture in PM-friendly terms |

Each document follows a strict format. See [Output Templates](#output-templates) below.

## Execution

### Step 1: Discover and Classify Source Docs

Read all files matching the source path. Classify each into categories:

| Category | Signals | Example Files |
|----------|---------|---------------|
| Architecture | Routing, middleware, data flow, infrastructure | routing.md, middleware.md, cicd.md |
| Data Systems | Databases, CMS, APIs, query languages | sanity.md, graphql.md, search-filters.md |
| UI/Frontend | Components, styling, state management | ui-styling.md, i18n.md |
| Operations | Testing, deployment, monitoring, tech debt | testing.md, cicd.md, tech-debt.md |
| Transitions | Migration plans, deprecation, feature flags | transitions-*.md |
| Features | User-facing functionality: forms, auth, tracking | forms.md, auth.md, tracking.md, seo.md |
| Reference | Lookup tables, file maps, troubleshooting | file-map.md |

Report classification to user before proceeding:
```
Found {N} technical documents:
- {X} architecture docs
- {Y} data system docs
- {Z} transition/migration docs
- ...

Will generate: Platform Guide, Bug Anatomy, Migration Landscape
Proceed? [Y/n]
```

### Step 2: Extract Knowledge Atoms

For each source document, extract:

1. **Systems**: What exists, what it does, who owns it
2. **Flows**: How data/requests move through the system (user action to outcome)
3. **Failure modes**: What breaks and why (explicit or inferable from troubleshooting sections)
4. **Constraints**: Rules, limits, known issues, tech debt
5. **Transitions**: What's being replaced, what's replacing it, current status
6. **Ownership**: Which team/person owns which area
7. **Terminology**: Domain-specific terms that non-engineers need defined

### Step 3: Check for Existing PM Context

If an existing context path is provided:
- Read existing PM docs
- Identify overlaps and gaps
- Flag outdated information in existing docs
- Report: "Existing docs cover X and Y. Source docs add Z. Existing doc A needs updating."

### Step 4: Generate Translated Documents

Apply the [Output Templates](#output-templates) and [Translation Rules](#translation-rules) to produce each document.

### Step 5: Cross-Reference and Index

- Add `## Related` sections linking documents to each other
- If an index file exists (like `00-core-essentials.md`), update it with new entries
- Report what was created and what was updated

---

## Translation Rules

These rules govern how technical content becomes PM-friendly content.

### The Five Transformations

| Technical Pattern | PM Translation | Example |
|------------------|----------------|---------|
| Code snippet or config | Table or plain English description | `middleware.ts` chain → "13 steps that process every request" |
| Implementation detail | "What it does" + "When it matters" | MD5 sharding → "Programs are split across databases. If data seems missing, it might be in a different shard." |
| File paths and function names | "Who owns it" + "What area" | `handlers/search/searchRequestBuilder.ts` → "Search team, query construction" |
| Error handling code | "What breaks and why" symptom table | `catch (e) { fallback }` → "If X fails, the system shows Y instead" |
| Architecture decisions (ADRs) | Decision + impact + "what it means for you" | "We chose Kevel because..." → "Ads are served by Kevel. Never cache ad responses (breaks revenue tracking)." |

### Hard Rules

1. **Zero code.** No code blocks, no file paths, no function names in the output. Tables, ASCII flowcharts, and prose only.
2. **Every section gets a "PM Takeaway" or "What This Means for You" callout.** This is the translation anchor.
3. **Symptom-first, not system-first.** Organize by "what you'll encounter" not "how it's built."
4. **Include failure modes.** Engineers document happy paths. PMs need to know what breaks. If the source doesn't document failures, infer from troubleshooting sections, tech debt inventories, and known issues.
5. **Ownership always included.** Every system area maps to a team or person. If unknown, flag it as "ownership unclear: check with engineering lead."
6. **Decision support, not implementation.** "Should I file this bug?" not "How do I fix this bug?"
7. **Preserve warnings.** If the source says "NEVER do X" or "CRITICAL: Y", translate the constraint, don't drop it. Example: "Never cache Kevel responses" → "Ad responses must never be cached. Caching breaks revenue pacing and forecasting."

### Audience Adjustments

| Audience | Depth | Focus | Extra |
|----------|-------|-------|-------|
| PM (default) | Full system understanding | Bug filing, prioritization, spec writing, stakeholder communication | Include "how to communicate with engineers" tips |
| Designer | Visual system + constraints | Component library, breakpoints, styling systems, i18n/RTL rules | Include design tokens, responsive breakpoints, text expansion rules |
| Stakeholder | Business impact only | What it does, what's changing, risk areas | Remove all technical details, focus on timelines and impact |
| New-hire | Onboarding depth | Everything + glossary + "where to find more" | Add context that insiders take for granted |

---

## Output Templates

### Platform Guide Template

```markdown
# {Project Name} Platform Guide (For {Audience})

> How the platform actually works, explained without code.

## How a {Primary User Action} Works
[End-to-end flow as numbered steps or ASCII diagram]
[PM Takeaway callout]

## How {Core System 1} Works
[Pipeline or flow description]
[Key concepts table: Concept | Explanation]
[Common gotchas / "What PMs Should Know" table]

## How {Core System 2} Works
[Same pattern]

... (one section per major system area)

## Non-Functional Requirements
[Targets table: Category | Target | Current Status]

## Quick Reference: Who Owns What
[Area | Squad/Team | Key People]

## Glossary
[Term | Meaning - only terms non-engineers need]
```

### Bug Anatomy Template

```markdown
# Bug Anatomy for {Audience}

> How to understand, file, and prioritize bugs without being an engineer.

## The Bug Families
[One subsection per family, each with:]
  ### {Family Name}
  [What breaks: 1-line description]
  [Symptom | Likely Cause | Severity - table, 4-5 rows]
  [Who owns it]
  [Key context for this family]

## Why Bugs Become Non-Reproducible
[Reason | Frequency | Example - table]

### What Survives {Migrations/Changes}
[Category | Why It Persists - table]

## How to Write a Great Bug Report
[Minimum viable bug report: Field | What to Include | Why]
[Common filing mistakes: Mistake | Impact - table]

## How to Prioritize Bugs
[Revenue-impact matrix: Level | Bug Type | Example]
[The "Is It Actually a Bug?" checklist]

## Communicating With Engineers
[Instead Of | Say - phrase substitution table]
[Questions Engineers Will Ask You - prepare these answers]
```

### Migration Landscape Template

```markdown
# {Migrations} (For {Audience})

> What's changing and what it means for your work.

## Why This Matters for {Audience}
[1-paragraph analogy or framing]

## Migration 1: {Name}
### What's Changing
[Before | After - table]
### What It Means for {Audience}
[Filing bugs, prioritization, timeline, ownership]

## Migration 2: {Name}
[Same pattern]

## The Decision Framework: How Deep Should a Fix Go?
[Flowchart: Is this code being replaced? → YES/NO branches]
[Safe to Invest In - table]
[Fix Minimally - table]

## How the Migrations Interact
[ASCII dependency diagram if applicable]

## {Audience} Checklist: Before Filing or Prioritizing
[Numbered checklist of questions to ask]
```

---

## Quality Checks

Before finalizing output, verify:

- [ ] **Zero code** in any output document
- [ ] **Every section** has a PM Takeaway or "What This Means" callout
- [ ] **All ownership** mapped (team + person where possible)
- [ ] **Failure modes** included (not just happy paths)
- [ ] **Warnings preserved** from source docs (never cached, never do X)
- [ ] **Cross-references** link documents to each other
- [ ] **Index updated** if one exists
- [ ] **Glossary** covers all domain terms used in the output
- [ ] **Tables over paragraphs** wherever structured data exists
- [ ] **No file paths or function names** leaked into output

---

## Examples

### Example 1: KAS Study Program Sites

**Input:** 18 developer reference files in `.claude/ref/` covering routing, middleware, CMS, search, auth, forms, i18n, tracking, testing, CI/CD, tech debt, and three migration plans.

**Output:** 4 documents in `domain-context/`:
- `15-educations-platform-guide.md`: How educations.com works (pages, search, forms, translations, tracking, auth, CMS)
- `16-bug-anatomy-for-pms.md`: Six bug families, filing guide, prioritization matrix, engineer communication tips
- `17-migration-landscape.md`: Three migrations explained, decision framework, dependency diagram
- `02-tech-architecture.md`: Updated architecture overview (refreshed from v12 to v16)

### Example 2: API Service (Hypothetical)

**Input:** OpenAPI spec + README + architecture decision records + runbook.

**Output:**
- Platform Guide: How the API serves data, authentication flow, rate limits, error codes in plain English
- Bug Anatomy: "API returns 500" family, "Data not updating" family, "Auth rejected" family
- Architecture Overview: Service diagram, dependencies, deployment pipeline

---

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Summarize by removing detail | Translate by reframing for the audience |
| Include code "for reference" | Describe what the code does in plain English |
| Use file paths as identifiers | Use system area names ("the search pipeline", "the lead form system") |
| Write a wall of prose | Use tables, checklists, and short callouts |
| Document only happy paths | Include failure modes, common mistakes, and known issues |
| Assume the reader knows engineering terms | Define every term in a glossary section |
| Create one giant document | Split into focused documents by purpose |
