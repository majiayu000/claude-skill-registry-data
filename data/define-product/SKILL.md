---
name: Define Product
description: Create user-centric product definitions by analyzing the repository, inferring product goals and user needs, clarifying ambiguities through structured questioning, and generating comprehensive product.md documentation. Use when the user mentions "product definition", "define product", "product strategy", or needs to document user personas, pain points, and user journeys.
---

# Define Product Skill

@.claude/shared-imports/CoD_Σ.md
@.claude/shared-imports/project-intel-mjs-guide.md

## Overview

This skill generates user-centric product definitions (`product.md`) by combining intelligence-first repository analysis with structured user clarification.

**Critical Boundary**: product.md must be PURELY user-centric with NO technical implementation details.

---

## Workflow

### Step 1: Intelligence Gathering

Run intelligence queries to understand the codebase:

```bash
# Project overview
project-intel.mjs --overview --json

# Search for product signals
project-intel.mjs --search "README" --json
project-intel.mjs --docs "product" --json
```

Analyze:
- README files and documentation
- Package metadata (package.json, cargo.toml, etc.)
- Code structure patterns (auth, org management, social features)
- UI patterns (large fonts, high contrast → accessibility needs)

### Step 2: Infer Product Characteristics

Based on intelligence, infer:

**Product Type**:
- B2B signals: SSO, org/team management, audit logs, RBAC, subscription billing
- B2C signals: Social auth, personal profiles, gamification, push notifications

**Primary Users**:
- Developers (API docs, SDKs, developer tools)
- Marketing teams (campaigns, analytics, email)
- Elderly/accessibility (large fonts, simplified UI, reminders)
- Executives (dashboards, reports, ROI metrics)

**Core Problem**:
- Data aggregation (scattered info across tools)
- Workflow automation (manual, repetitive tasks)
- Accessibility (complex tasks for users with specific needs)
- Communication (team collaboration pain points)

### Step 3: Clarify Ambiguities (Max 5 Questions)

If signals are conflicting or unclear, use `AskUserQuestion` tool:

**Question Priority**:
1. Product type (if B2B vs B2C ambiguous)
2. Primary user persona (who matters most?)
3. Core problem being solved
4. Key differentiator ("our thing")
5. Most critical pain point

**Question Format**:
```python
AskUserQuestion(questions=[{
  "question": "Is this product primarily B2B or B2C?",
  "header": "Product Type",
  "multiSelect": False,
  "options": [
    {
      "label": "B2B (Business-to-Business)",
      "description": f"Enterprise/team product. Evidence: {b2b_signals}"
    },
    {
      "label": "B2C (Business-to-Consumer)",
      "description": f"Consumer-facing. Evidence: {b2c_signals}"
    }
  ]
}])
```

### Step 4: Define 3 Personas (Jobs-to-be-Done)

For each persona, gather:

**Demographics**: Age range, location, tech savviness, accessibility needs

**Pain Points** (JTBD Framework):
```markdown
**Pain #: [Short title]**
- **Pain**: [Specific frustration - be concrete]
- **Why it hurts**: [Impact: time lost, money wasted, stress caused]
- **Current workaround**: [How they cope today - tools, hacks, manual work]
- **Frequency**: [Daily, weekly, monthly]
```

**Pain Resolution Mapping**:
```
Pain 1 → [Our Solution Feature] → [Measurable Outcome]
```

### Step 5: Map 2-3 User Journeys

Using CoD^Σ notation (from @.claude/shared-imports/CoD_Σ.md):

**Standard Journey**:
```
Awareness ≫ Interest ≫ Research → Decision ≫ Onboarding → First Use ≫ First Value ∘ Habit
```

For each step, define:
- User action or system response
- Information/guidance needed
- Pain point addressed
- Success indicator

### Step 6: Generate product.md

Use template at `@.claude/templates/product.md`.

Include:
- Product overview and value proposition
- 3 personas with demographics, psychographics, pain points
- Pain-to-resolution mapping
- 2-3 user journeys with CoD^Σ notation
- Journey-to-pain mapping
- "Our Thing" (key differentiator)
- North Star Metric

### Step 7: Validate

**CRITICAL - Check for violations**:

❌ **MUST NOT Contain**:
- Tech stack: "React", "Python", "PostgreSQL", "AWS"
- Architecture: "Microservices", "REST API", "GraphQL"
- Frameworks: "Next.js", "FastAPI", "Django"
- Infrastructure: "Kubernetes", "Docker", "Lambda"

✓ **MUST Contain**:
- 3 personas with complete JTBD pain points
- Pain-to-resolution mapping with measurable outcomes
- 2-3 user journeys with CoD^Σ notation
- "Our Thing" clearly articulated
- North Star Metric (quantifiable user outcome)

**Key Anti-Patterns**:

| ❌ Wrong (Technical) | ✓ Right (User-Centric) |
|---------------------|------------------------|
| "We'll use React for fast UI" | "Users need responsive, lag-free interface" |
| "PostgreSQL for data integrity" | "Users need reliable, accurate data they can trust" |
| "Microservices for scale" | "Users need instant search across millions of items" |
| "OAuth 2.0 authentication" | "Users need to log in with company credentials" |

---

## Example

See complete B2B SaaS example:
- [examples/b2b-saas-product.md](examples/b2b-saas-product.md)

This shows:
- Full persona definitions with JTBD pain points
- Complete pain-to-resolution mapping
- User journeys with CoD^Σ notation
- NO technical decisions

---

## Next Steps

After product.md is created, use `/generate-constitution` to derive technical principles FROM the user needs documented here.

---

## Key Reminders

1. **Intelligence FIRST** - Use `@.claude/shared-imports/project-intel-mjs-guide.md` patterns
2. **User-Centric ONLY** - NO tech stack, architecture, or implementation
3. **Evidence-Based** - Every claim traces to intelligence query or user input
4. **CoD^Σ Journeys** - Use `@.claude/shared-imports/CoD_Σ.md` notation
5. **Validate Boundary** - Verify no technical decisions leaked in
