---
name: sr-save
description: >
  Phase 9 of the SRS workflow. Saves all project context to _context/ files
  so future sessions can resume without re-reading the full SRS.
---

# sr-save

Goal: distil the entire project into compact, re-loadable context files.
A future session should be able to load just `_context/` and have full project understanding.

---

## Step 0 — Identify Project

Ask the user: "Which project to save context for? (slug)"

Read all available files in `projects/{slug}/`.
Run `python .codex/scripts/srs_validator.py --dir projects/{slug}/srs/ --stats` and use its
counts for quality_standards.md / session-notes.md below instead of recounting by hand.

---

## Step 1 — Write Context Files

Write all files under `projects/{slug}/_context/`:

### vision.md

```markdown
# Vision — {Project Name}

## Problem Statement
{what problem does this system solve? 2–3 sentences from spec §1}

## Solution Summary
{what the system does, for whom, and the core value proposition}

## Success Metrics
{how we measure success — from spec §1 or brainstorm}

## Constraints
{top 3 hard constraints — tech, timeline, compliance}
```

### features.md

```markdown
# Features — {Project Name}

## IN Scope (v1.0)
| Feature | Priority | Key FRs | Notes |
|---------|----------|---------|-------|
{every confirmed in-scope feature, one row each}

## OUT of Scope (v1.0 — Deferred)
| Feature | Reason | Target version |
|---------|--------|---------------|
{every explicitly excluded feature}
```

### tech_stack.md

```markdown
# Tech Stack — {Project Name}

## Confirmed Stack
| Layer | Technology | Constraint type |
|-------|-----------|----------------|
{language, framework, DB, cloud, CI/CD — from spec §5}

## Integration Points
| System | Protocol | Direction | Auth |
|--------|----------|-----------|------|
{every external system — from SRS §3.1.3}

## Compliance Requirements
{applicable regulations + specific technical obligations}
```

### glossary.md

```markdown
# Glossary — {Project Name}

Copy of Appendix A from the SRS. Every term, acronym, abbreviation.
Include: domain terms | project-specific terms | role names | system names
```

### quality_standards.md

```markdown
# Quality Standards — {Project Name}

## Confirmed NFR Targets
| ID | Characteristic | Target | Status |
|----|---------------|--------|--------|
{all NFRs from SRS §3.3 — confirmed targets and [TBD] items}

## Validation Status
Validator verdict: {COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT}
Open warnings: {count}
```

### session-notes.md

```markdown
# Session Notes — {Project Name}

## Key Decisions Made
{numbered list — every explicit scope, tech, or design decision from brainstorm}

## Assumptions
{numbered list — from spec §8, with invalidation risk level}

## Open Items
{all [TBD] items — copied from appendix-b-open-issues.md}

## Next Steps
1. Resolve open items in appendix-b (see quality_standards.md for owners)
2. Dev team walkthrough of SRS §3.2 (functional requirements)
3. QA team review of GWT acceptance criteria
4. Architecture review of NFR targets before sprint planning

## SRS Location
projects/{slug}/srs/ — {N} section files
Master index: projects/{slug}/srs/00-master-index.md
```

---

## Step 2 — Final Summary

Output the complete workflow completion summary:

```
╔══════════════════════════════════════════════════╗
║           SRS Workflow Complete                  ║
╠══════════════════════════════════════════════════╣
║ Project:     {name}                              ║
║ Slug:        {slug}                              ║
║ Location:    projects/{slug}/                    ║
╠══════════════════════════════════════════════════╣
║ Brainstorm:  projects/{slug}/brainstorm.md       ║
║ Spec:        projects/{slug}/spec.md             ║
║ Plan:        projects/{slug}/plan/ (12 files)    ║
║ SRS:         projects/{slug}/srs/  (11 files)    ║
║ Improvement: projects/{slug}/improvement-report.md ║
║ Context:     projects/{slug}/_context/ (6 files) ║
╠══════════════════════════════════════════════════╣
║ FRs:         {total} ({E} Essential / {C} Cond / {O} Opt) ║
║ NFRs:        {total} ({confirmed} confirmed / {TBD} TBD)  ║
║ Verdict:     {COMPLIANT | PARTIALLY COMPLIANT}   ║
║ Open items:  {count}                             ║
╚══════════════════════════════════════════════════╝

Share with your team:
  SRS  → projects/{slug}/srs/00-master-index.md
  Risks→ projects/{slug}/improvement-report.md
```
