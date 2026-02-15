---
name: audit-skills
description: Audits skills for best practice violations including length, checklists, verification steps, and progressive disclosure. Use after creating skills, during reviews, or to improve existing skills. Produces prioritized improvement suggestions.
---

# Audit Skills

Analyze skills in this repository against best practices and produce prioritized improvements.

## Workflow

Copy this checklist and track progress:

```
Audit Progress:
- [ ] Step 1: Discover skills
- [ ] Step 2: Load criteria
- [ ] Step 3: Audit each skill
- [ ] Step 4: Score and prioritize
- [ ] Step 5: Output report
```

### Step 1: Discover Skills

Find all skills in the repository:

```bash
find .claude/skills -name "SKILL.md" -type f 2>/dev/null
```

Record the count for verification later.

### Step 2: Load Criteria

Read [CRITERIA.md](CRITERIA.md) for the full audit checklist.

Read [SCORING.md](SCORING.md) for severity definitions.

### Step 3: Audit Each Skill

For each discovered SKILL.md:

1. **Read the file** - Note line count immediately
2. **Check each criterion** from CRITERIA.md
3. **Record violations** with criterion ID and evidence

Use this template per skill:

```
Skill: <name>
Lines: <count>
Violations:
- <ID>: <brief evidence>
```

### Step 4: Score and Prioritize

Group findings by severity (from SCORING.md):
- **Critical**: Likely to cause execution failures
- **Medium**: Degrades quality but may still work
- **Low**: Polish items

Within each severity, sort by:
1. Most violations in single skill (fix skill holistically)
2. Most common violation across skills (systemic issue)

### Step 5: Output Report

Use this format:

```markdown
# Skill Audit Report

Generated: <date>
Skills audited: <N>
Total findings: <N>

## Critical (fix first)

- **<skill-name>**: <violation summary> (<criterion-id>)
  - Evidence: <quote or line numbers>
  - Suggested fix: <concrete action>

## Medium Priority

...

## Low Priority

...

## Summary by Criterion

| ID | Description | Count |
|----|-------------|-------|
| C1 | Missing checklist | 5 |
| ... | ... | ... |
```

---

**REMINDER**: After completing the audit, verify your report includes all discovered skills. Missing skills indicates incomplete analysis.
