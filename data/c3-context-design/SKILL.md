---
name: c3-context-design
description: Use when exploring Context level impact during scoping - system boundaries, actors, cross-container interactions, and high-level concerns
---

# C3 Context Level Exploration

## ⛔ CRITICAL GATE: Load Current Context First

> **STOP** - Before ANY context-level work, execute:
> ```bash
> cat .c3/README.md 2>/dev/null || echo "NO_CONTEXT_DOC"
> cat .c3/settings.yaml 2>/dev/null || echo "NO_SETTINGS"
> ls -d .c3/c3-*/  2>/dev/null || echo "NO_CONTAINERS"
> ```

**Based on output:**
- If "NO_CONTEXT_DOC" → Creating new context (fresh)
- If context exists → Read it completely before proposing changes
- If containers exist → Note them for reference

**⚠️ DO NOT read ADRs** unless user specifically asks:
- Context work focuses on current state, not historical decisions
- ADRs add unnecessary context → hallucination risk
- Only read: Context, Container READMEs (for inventory)

**Why this gate exists:** Context is the root of all C3 docs. Changes here cascade to ALL containers and components.

**Self-check before proceeding:**
- [ ] I executed the commands above
- [ ] I read existing context doc (if exists)
- [ ] I know what containers already exist

---

## Overview

Context is the **eagle-eye introduction** to your architecture. Two core jobs:

1. **What containers exist and what are they responsible for?**
2. **How do containers interact with each other?**

**Position:** ROOT (c3-0) | Parent: None | Children: All Containers

**📁 File Location:** Context is `.c3/README.md` - NOT `context/c3-0.md` or any subfolder.

**Announce:** "I'm using the c3-context-design skill to explore Context-level impact."

---

## The Principle

> **Upper layer defines WHAT. Lower layer implements HOW.**

At Context level:
- I define WHAT containers exist and WHY
- Container implements my definitions (WHAT components exist)
- I do NOT define what's inside containers - that's Container's job

**Integrity rule:** Containers cannot exist without being listed in Context.

---

## Include/Exclude

| Include (Context Level) | Exclude (Push Down) |
|-------------------------|---------------------|
| Container responsibilities | Component details |
| Container relationships | Internal patterns |
| Connecting points (APIs/events) | Implementation |
| External actors | Code references |
| Cross-cutting concerns | File paths |

**Litmus test:** "Is this about WHY containers exist and HOW they relate to each other?"

---

## Exploration Process

### Phase 1: Analyze Change Impact

Already loaded context via Critical Gate. Now analyze:

| Change Type | Action |
|-------------|--------|
| New/remove container | Update inventory, delegate to c3-container-design |
| Protocol change | Update all consumers/providers |
| Boundary change | Full system audit |

### Phase 2: Socratic Discovery

- **Containers:** "What would be separately deployed?"
- **Protocols:** "How do containers talk? What's the contract?"
- **Boundary:** "What's inside vs external?"
- **Actors:** "Who initiates interactions?"

---

## Template

```markdown
---
id: c3-0
c3-version: 3
title: [System Name] Overview
summary: >
  Bird's-eye view of the system, actors, and key interactions.
---

# [System Name] Overview

## Overview {#c3-0-overview}
[System purpose in 1-2 sentences]

## System Architecture {#c3-0-architecture}

` ` `mermaid
flowchart TB
    subgraph System["[System Name]"]
        C1[Container 1 c3-1]
        C2[Container 2 c3-2]
    end

    User((User)) --> C1
    C1 --> C2
` ` `

## Actors {#c3-0-actors}
| Actor | Type | Interacts Via |
|-------|------|---------------|

## Containers {#c3-0-containers}
| Container | ID | Archetype | Responsibility |
|-----------|-----|-----------|----------------|

## Container Interactions {#c3-0-interactions}
| From | To | Protocol | Purpose |
|------|-----|----------|---------|

## Cross-Cutting Concerns {#c3-0-cross-cutting}
- **Auth:** [approach]
- **Logging:** [approach]
- **Errors:** [approach]
```

---

## Diagram Requirement

**A container relationship diagram is REQUIRED at Context level.**

Must show: containers, external systems, protocols, actors.

Use **Mermaid only** - no ASCII art.

---

## ⛔ Enforcement Harnesses

### Harness 1: Template Fidelity

**Rule:** Output MUST match template structure exactly.

**Required sections (in order):**
1. Frontmatter (id, c3-version, title, summary)
2. Overview
3. System Architecture (with Mermaid diagram)
4. Actors
5. Containers
6. Container Interactions
7. Cross-Cutting Concerns

🚩 **Red Flags:**
- Sections missing or reordered
- ASCII diagram instead of Mermaid
- Missing frontmatter fields

### Harness 2: Mermaid Only

**Rule:** ALL diagrams must use Mermaid syntax.

| Prohibited | Required |
|------------|----------|
| `+---+` box drawing | ` ```mermaid ` blocks |
| `├──` tree structures | `flowchart` or `graph` |
| Text-based flows | Proper Mermaid syntax |

---

## Verification Checklist

Before claiming completion, execute:

```bash
# Verify context doc exists
cat .c3/README.md | head -20

# Verify frontmatter
grep -E "^id:|^c3-version:|^title:" .c3/README.md

# Verify mermaid diagram exists
grep -c '```mermaid' .c3/README.md
```

- [ ] Critical gate executed (existing context loaded)
- [ ] Template sections present in correct order
- [ ] Mermaid diagram included (no ASCII)
- [ ] Frontmatter complete (id, c3-version, title, summary)
- [ ] All containers listed with responsibilities
- [ ] Interactions documented

---

## 📚 Reading Chain Output

**At the end of context work, output a reading chain for affected containers.**

Format:
```
## 📚 To Go Deeper

Context (c3-0) defines these containers:

**Containers to explore:**
├─ c3-1-{slug} - [responsibility, why it matters]
├─ c3-2-{slug} - [responsibility, why it matters]
└─ ...

**If this change affected protocols, also read:**
└─ c3-N-{slug} - [which protocol changed]

*Reading chain generated from containers listed in Context.*
```

**Rules:**
- List containers mentioned in Context's inventory
- Highlight which containers are affected by this change
- Never include ADRs unless user asked

---

## Related

- `references/core-principle.md` - The C3 principle
- `defaults.md` - Context layer rules
- `references/container-archetypes.md` - Container types
- `references/diagram-patterns.md` - Diagram guidance
