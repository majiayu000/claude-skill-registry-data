---
name: c3-design
description: Use when designing, updating, or exploring system architecture with C3 methodology - iterative scoping through hypothesis, exploration, and discovery across Context/Container/Component layers
---

# C3 Architecture Design

## ⛔ CRITICAL GATE: Load Existing Documentation First

> **STOP** - Before ANY exploration or design work, execute:
> ```bash
> cat .c3/README.md 2>/dev/null || echo "NO_CONTEXT"
> cat .c3/TOC.md 2>/dev/null || echo "NO_TOC"
> ls -d .c3/c3-*/  2>/dev/null || echo "NO_CONTAINERS"
> ```

**Based on output:**
- If docs exist → **READ THEM** before forming any hypothesis
- If "NO_CONTEXT" → Fresh project, proceed to Mode Detection

**⚠️ DO NOT read completed ADRs** unless user specifically asks:
- ADRs are historical records, not active guidance
- Reading them adds unnecessary context → hallucination risk
- Only read: Context (README.md), Containers, Components

**Why this gate exists:** Agents that skip existing documentation propose conflicting changes, miss established patterns, and waste user time.

**Self-check before proceeding:**
- [ ] I executed the commands above
- [ ] I read existing .c3/ docs (if they exist)
- [ ] My understanding comes from DOCS, not code exploration

---

## Overview

Transform requirements into C3 documentation through iterative scoping. Also supports exploration-only mode.

**Core principle:** Hypothesis → Explore → Discover → Iterate until stable.

**Announce:** "I'm using the c3-design skill to guide architecture design."

---

## Mode Detection

| User Intent | Mode | Next Step |
|-------------|------|-----------|
| "What's the architecture?" | Exploration | Load TOC → Present overview |
| "How does X work?" | Exploration | Load relevant docs → Explain |
| "I need to add/change..." | Design | Full workflow with ADR |
| "Why did we choose X?" | Exploration | Search ADRs → Present |

### Exploration Mode

Quick read-only navigation:
1. Load `.c3/TOC.md`
2. Present overview based on intent
3. Navigate on demand
4. If user wants changes → Switch to Design Mode

### Design Mode

Full workflow with **mandatory ADR creation**.

> **⛔ DESIGN MODE GATE: Load References**
> ```bash
> # Load skill references (from plugin directory)
> cat references/design-guardrails.md
> cat references/adr-template.md
> ```
> 
> **Self-check before proceeding:**
> - [ ] I read design-guardrails.md (common mistakes, red flags)
> - [ ] I read adr-template.md (ADR structure, required sections)
> - [ ] I understand ADR+Plan are inseparable (no ADR without Plan)

---

## Design Mode Workflow

**IMMEDIATELY create TodoWrite items:**
1. Phase 1: Surface Understanding
2. Phase 2: Iterative Scoping  
3. Phase 3: ADR Creation (MANDATORY)
4. Phase 4: Handoff

### Phase 1: Surface Understanding

Form hypothesis about which layers are affected.

**Input:** User's request + loaded .c3/ docs
**Output:** Written hypothesis statement
**Gate:** Hypothesis formed referencing specific C3 docs

```
Example hypothesis:
"Based on c3-1 (Backend), this change affects Container level.
The user wants to add caching, which impacts c3-102 (Data Layer component)."
```

### Phase 2: Iterative Scoping

Loop until stable: HYPOTHESIZE → EXPLORE → DISCOVER

| Step | Action |
|------|--------|
| Hypothesize | "This change affects [layers/docs]" |
| Explore | Use layer skills to investigate (invoke them, don't describe) |
| Discover | Find actual impacts, adjust hypothesis |

**Gate:** No new discoveries in last iteration → Declare "Scope stable"

### Phase 3: ADR Creation (MANDATORY)

**⛔ NO code changes until ADR file exists.**

Create ADR in `.c3/adr/adr-YYYYMMDD-slug.md`:

```bash
# Determine today's date and create ADR
today=$(date +%Y%m%d)
cat > .c3/adr/adr-${today}-{slug}.md << 'EOF'
---
id: adr-YYYYMMDD-{slug}
title: [Decision Title]
status: proposed
date: YYYY-MM-DD
---

# [Decision Title]

## Status
**Proposed** - YYYY-MM-DD

## Problem/Requirement
[What triggered this decision]

## Exploration Journey
**Initial hypothesis:** [What we first thought]
**Explored:** [What we found at each direction]
**Discovered:** [Key insights]

## Solution
[The approach and why]

## Changes Across Layers
### Context Level
- [c3-0]: [What changes, why]

### Container Level  
- [c3-N-slug]: [What changes, why]

### Component Level
- [c3-NNN-slug]: [What changes, why]

## Verification
- [ ] [Check derived from exploration]

## Implementation Plan

### Code Changes
| Layer Change | Code Location | Action | Details |
|--------------|---------------|--------|---------|

### Acceptance Criteria
| Verification Item | Criterion | How to Test |
|-------------------|-----------|-------------|

## Related
- [Links to affected docs]
EOF
```

**Gate:** ADR file exists on disk

```bash
# Verify ADR was created
ls .c3/adr/adr-*.md
```

### Phase 4: Handoff

Execute handoff steps (from `.c3/settings.yaml` or defaults):
1. Summarize changes to user
2. List next actions
3. Confirm completion

**Gate:** All steps executed with evidence

---

## Layer Skill Delegation

When you identify which layer is affected, **INVOKE** the layer skill:

| Impact | Action |
|--------|--------|
| Container inventory changes | **Use Skill tool → c3-context-design** |
| Component organization | **Use Skill tool → c3-container-design** |
| Implementation details | **Use Skill tool → c3-component-design** |

---

## ⛔ Enforcement Harnesses

### Harness 1: Skill Delegation (No Hallucination)

**Rule:** When work requires a layer skill, INVOKE it. Never describe what it "would do."

| Anti-Pattern | Correct Action |
|--------------|----------------|
| "c3-container-design would create..." | Use Skill tool → c3-container-design |
| "Following c3-component-design patterns..." | Invoke the skill first |
| Summarizing skill output without invoking | Invoke, get real output |

🚩 **Red Flag:** Using layer skill name without Skill tool invocation in conversation

### Harness 2: ADR-Before-Code

**Rule:** NO code changes until ADR file exists in Design Mode.

| Anti-Pattern | Correct Action |
|--------------|----------------|
| "Let me fix this quickly first" | Create ADR first |
| "I'll create ADR after fixing" | ADR before any edit |
| Making code changes in Phase 1-2 | Only read code, don't modify |

🚩 **Red Flag:** Edit/Write tool used before ADR file created

---

## Verification Checklist

Before claiming completion, verify:

```bash
# If Design Mode: Verify ADR exists
ls .c3/adr/adr-*.md 2>/dev/null | tail -1

# Verify no orphaned changes (ADR lists them)
cat .c3/adr/adr-*.md | grep -A20 "Changes Across Layers"
```

- [ ] Critical gate executed (existing docs loaded)
- [ ] Mode detected correctly
- [ ] If Design Mode: All 4 phases completed with gates
- [ ] If Design Mode: ADR file exists with all sections
- [ ] Layer skills invoked (not described)
- [ ] Handoff executed

---

## 📚 Reading Chain Output

**At the end of your work, output a contextual reading chain based on what you discovered.**

Format:
```
## 📚 To Go Deeper

Based on this work affecting [layer/component], relevant reading:

**Ancestors (understand constraints):**
└─ c3-0 → c3-N → c3-NNN (this)

**Siblings (coordinate changes):**
├─ c3-NMM - [why relevant]
└─ c3-NKK - [why relevant]

**Downstream (propagate changes):**
└─ c3-NNNX - [affected by this change]

*Reading chain generated from actual doc relationships.*
```

**Rules:**
- Only include docs you actually read or identified during exploration
- Explain WHY each doc is relevant (not generic)
- Never include ADRs unless user asked about decisions

---

## Related

- `references/design-guardrails.md` - Key principles, common mistakes
- `references/design-phases.md` - Phase details
- `references/adr-template.md` - Full ADR template with examples
- `references/design-exploration-mode.md` - Exploration workflow
