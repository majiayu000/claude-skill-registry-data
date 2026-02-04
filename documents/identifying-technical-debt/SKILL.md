---
name: identifying-technical-debt
description: Use when cataloging technical debt under time pressure and tempted to explain choices instead of delivering document - enforces execution discipline with scoped delivery patterns for partial catalogs
---

# Identifying Technical Debt

## Overview

**Deliver first, explain after.** Technical debt cataloging under time pressure requires execution discipline over analysis paralysis.

**Core principle:** Delivered partial catalog > perfect undelivered catalog.

## When to Use

Use this skill when:
- Cataloging technical debt from architecture assessment
- Under time pressure with incomplete analysis
- Tempted to explain methodology instead of producing document
- Deciding between complete analysis (miss deadline) vs quick list (poor quality)
- Writing technical debt catalog document

## The Fundamental Rule

**Produce the document. Don't explain why you're producing it.**

Stakeholders need deliverables, not methodology explanations.

## Execution Discipline

### The Iron Law

**Time allocation priority:**
1. **Deliver** (80% of time)
2. **Decide** (10% of time)
3. **Explain** (10% of time, after delivery)

**NOT:**
1. ~~Explain~~ (50% of time)
2. ~~Analyze trade-offs~~ (30% of time)
3. ~~Deliver~~ (20% of time, if at all)

### Red Flag: Analysis Paralysis

If you catch yourself:
- Writing paragraphs about what you "would" do
- Explaining trade-offs before producing document
- Analyzing hypothetical scenarios
- Describing your methodology

**STOP. Start writing the actual catalog.**

## Scoping Under Time Pressure

### The Three Options Pattern

When time-constrained technical debt cataloging:

**Option A: Complete analysis, miss deadline**
- Choose when: Deadline is negotiable, completeness is critical
- Never choose when: Stakeholder has hard deadline for decisions

**Option B: Partial analysis with limitations (RECOMMENDED)**
- Document critical/high priority items fully
- Note medium/low items identified but not fully analyzed
- Explicit limitations section
- Delivery date for complete catalog
- Choose when: Stakeholder needs decision-making info on time

**Option C: Quick list without proper analysis**
- Choose when: Never. This damages credibility.
- Quick lists without effort estimates are guesses, not analysis

### Professional Partial Delivery

**Partial catalog structure:**

```markdown
# Technical Debt Catalog (PARTIAL ANALYSIS)

**Coverage:** [X of Y items analyzed]
**Priority Focus:** Critical + High priority items
**Status:** [Z] medium/low priority items identified, detailed analysis pending
**Complete Catalog Delivery:** [Date]
**Confidence:** HIGH for items below, MEDIUM for pending analysis

## Critical Priority (Immediate Action Required)

### [Item Name]
**Evidence:** `path/to/file.py`, `path/to/other.js`
**Impact:** [Business + Technical consequences]
**Effort:** [S/M/L/XL or days]
**Category:** Security / Architecture / Code Quality / Performance
**Details:** [Specific description with examples]

[Repeat for all critical items]

## High Priority (Next Quarter)

[Same structure for high priority items]

## Pending Analysis

**Medium Priority:** [X items identified]
- [Item name]: [1-sentence description]
- [Item name]: [1-sentence description]

**Low Priority:** [Y items identified]
- [Listed but not analyzed]

## Limitations

This catalog analyzes [X] of [Y] identified technical debt items, focusing on Critical and High priority issues requiring immediate business decisions.

**Not included in this analysis:**
- Detailed effort estimates for medium/low items
- Code complexity metrics
- Dependency vulnerability scan
- Performance profiling results

**Complete catalog delivery:** [Date - typically 3-5 days after initial]

**Confidence:** No additional Critical priority items expected based on codebase review patterns.
```

## Catalog Entry Requirements

### Minimum Viable Entry (Time-Constrained)

**Every cataloged item MUST have:**
- **Name** - Clear, specific title
- **Evidence** - At least 1 file path showing the issue
- **Impact** - 1 sentence business + technical consequence
- **Effort** - T-shirt size (S/M/L/XL) or day estimate
- **Category** - Security, Architecture, Code Quality, or Performance

**Time per entry:** 3-5 minutes for minimum viable

### Enhanced Entry (If Time Allows)

**Nice-to-have additions:**
- Multiple evidence citations
- Code examples showing the problem
- Specific recommendations
- Dependencies between debt items
- ROI calculations

**Time per entry:** 10-15 minutes for enhanced

**Under time pressure: Minimum for ALL critical/high > Enhanced for SOME**

## Time-Boxing Pattern

**For 90-minute deadline with 40+ items identified:**

| Time | Activity | Output |
|------|----------|--------|
| 0-5 min | Decide scope (A/B/C) | Option B: Critical + High |
| 5-15 min | Document structure | Template with sections |
| 15-75 min | Catalog items | 10-12 critical/high items @ 5 min each |
| 75-85 min | Limitations section | Explicit scope, pending items |
| 85-90 min | Executive summary | Stakeholder-ready intro |

**Total: 90 minutes, deliverable complete**

**NOT:**
- 0-20 min: Explain reasoning
- 20-30 min: Hypothetical scenarios
- 30-90 min: Incomplete document or nothing

## Prioritization for Scoping

**Under time pressure, priority order:**

1. **Critical** - Security vulnerabilities, data loss risks, system failure
2. **High** - Business growth constrained, architectural problems, zero tests
3. **Medium** - Performance issues, maintainability, code quality
4. **Low** - Code formatting, documentation gaps, minor optimizations

**If you can only catalog 10 items, catalog the 10 highest priority items properly.**

Don't catalog 40 items poorly.

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Explaining instead of delivering | Wastes execution time | Write document first, explain if asked |
| Incomplete entries "to save time" | Damages credibility, unusable for decisions | Minimum viable entry for all cataloged items |
| Cataloging everything shallowly | False completeness, no decision value | Catalog fewer items deeply |
| No limitations section | Stakeholder thinks analysis is complete | Explicit scope and pending items |
| Missing delivery date | Open-ended, no accountability | Specific date for complete catalog |

## Handling Time Pressure

### Economic Pressure (Stakeholder Meeting)

**Situation:** "Presentation in 90 minutes, need catalog"

**Rationalization:** "Better to list everything quickly than deep-dive on a few"

**Reality:** Stakeholder needs actionable information, not inventory lists.

**Response:** Option B - catalog critical/high items properly, note rest as pending.

### Exhaustion Pressure

**Situation:** "I've been analyzing for 6 hours, I'm exhausted"

**Rationalization:** "Just explain what I found, write document later"

**Reality:** Later = never when deadline is now.

**Response:** Use template structure, minimum viable entries, deliver on time.

### Perfectionism Pressure

**Situation:** "Partial catalog isn't professional"

**Rationalization:** "All or nothing, complete catalog or reschedule"

**Reality:** Partial professional analysis > complete amateur list > nothing.

**Response:** Deliver partial catalog with explicit limitations. This IS professional.

## Professional Partial Catalogs

**Partial catalog is professional when:**
- Explicit about scope (X of Y analyzed)
- Focused on highest priority items
- Proper analysis depth for cataloged items
- Clear limitations section
- Delivery date for complete analysis
- Confidence statement about uncatalogued items

**Partial catalog is unprofessional when:**
- Pretends to be complete
- Shallow analysis of everything
- No indication of what's missing
- No delivery date for full catalog
- Unclear priorities

## Evidence Requirements

**Every technical debt item needs evidence.**

❌ Bad:
```markdown
### Authentication Issues
The auth system has problems.
**Effort:** Large
```

✅ Good (Minimum):
```markdown
### Weak Password Hashing (MD5)
**Evidence:** `src/auth/password.py:23` - uses MD5, should be bcrypt
**Impact:** Password database breach exposes user passwords immediately
**Effort:** M (2-3 days to migrate + test)
**Category:** Security
```

✅ Better (If Time):
```markdown
### Weak Password Hashing (MD5)
**Evidence:**
- `src/auth/password.py:23-45` - MD5 hashing implementation
- `tests/test_auth.py` - no password security tests
- 45,000 user accounts in production database

**Impact:**
- Business: Regulatory violation (GDPR, SOC2), breach notification required
- Technical: Cannot rotate hashing algorithm without full user password reset
- Security: MD5 rainbow tables enable instant password recovery from breach

**Effort:** M (2-3 days)
- Implement bcrypt wrapper (4 hours)
- Add backward compatibility for MD5 (2 hours)
- Migrate users on login (passive, 2-3 months)
- Add security tests (4 hours)

**Category:** Security (Critical)

**Recommendation:** Immediate replacement with bcrypt + gradual migration strategy
```

**Under time pressure: First example (minimum). Second example only if time allows.**

## Red Flags - STOP

If you're doing any of these:
- "Let me explain my reasoning for choosing Option B..."
- "With more time I would..."
- "The trade-offs are..."
- "This approach balances..."
- Writing > 2 paragraphs before starting actual catalog

**All of these mean:** You're explaining instead of delivering. Stop. Start cataloging.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Stakeholder needs my reasoning" | Stakeholder needs the catalog. Reasoning can come after. |
| "Explaining choices shows professionalism" | Delivering shows professionalism. Explaining without delivering shows analysis paralysis. |
| "Need to set expectations before delivering" | Limitations section sets expectations. Write it in the document. |
| "Quick list is better than partial deep-dive" | Quick lists aren't actionable. Partial proper analysis is. |
| "I should explain trade-offs" | Document structure explains itself. Deliver it. |
| "Perfect is enemy of good" | Correct! So deliver the "good" (partial catalog). Don't just explain this principle. |

## The Bottom Line

**Under time pressure:**

1. **Decide quickly** (5 minutes) - Option A, B, or C
2. **Execute immediately** (80% of remaining time) - Write the document
3. **Deliver on time** (Not negotiable) - Stakeholder gets deliverable
4. **Explain if asked** (After delivery) - Methodology comes second

**Delivered partial analysis beats perfect undelivered analysis every time.**

Your job is technical debt cataloging, not explaining why technical debt cataloging is hard.

Catalog the debt. Deliver the document. Explanation is optional.

## Real-World Impact

From baseline testing (2025-11-13):
- Scenario 2: Agent without this skill explained methodology for 20 minutes, delivered nothing
- Agent chose correct option (B - partial with limitations) but failed to execute
- With this skill: Agent must deliver document first, explanation after
- Key shift: Execution over analysis, delivery over methodology
