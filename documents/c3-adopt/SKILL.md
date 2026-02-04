---
name: c3-adopt
description: Use when bootstrapping C3 documentation for any project - guides through Socratic discovery and delegates to layer skills for document creation
---

# C3 Adopt

## ⛔ CRITICAL GATE: Check Existing State First

> **STOP** - Before ANY adoption work, execute:
> ```bash
> ls -la .c3/ 2>/dev/null || echo "NO_C3_DIR"
> cat .c3/README.md 2>/dev/null || echo "NO_CONTEXT"
> ```

**Based on output:**
- If "NO_C3_DIR" → Fresh project, proceed with scaffolding
- If `.c3/` exists with content → Ask user: update, backup+recreate, or abort?
- If `.c3/` exists but empty → Proceed with scaffolding

**⚠️ DO NOT read existing ADRs** during adoption:
- ADRs are historical records from past decisions
- For fresh adoption, they add confusing context
- If rebuilding, user will specify what to preserve

**Why this gate exists:** Blindly creating `.c3/` can overwrite existing documentation.

**Self-check before proceeding:**
- [ ] I executed the commands above
- [ ] I know whether .c3/ exists
- [ ] If exists: I asked user what to do

---

## Overview

Bootstrap C3 architecture documentation through Socratic questioning and delegation. Works for existing codebases and fresh projects.

**Announce:** "I'm using the c3-adopt skill to initialize architecture documentation."

---

## Scenario Detection

| Scenario | Signal | Path |
|----------|--------|------|
| Fresh project | No `.c3/`, no code | Questions → Scaffold → Document |
| Existing codebase | Code exists, no `.c3/` | Explore code → Questions → Document |
| Rebuild needed | `.c3/` exists, user wants reset | Backup → Fresh start |

---

## V3 Structure (MANDATORY)

```
.c3/
├── README.md                     ← Context (c3-0) IS the README
├── TOC.md                        ← Table of contents
├── settings.yaml                 ← Project settings
├── c3-1-{slug}/
│   ├── README.md                 ← Container 1
│   └── c3-101-{slug}.md          ← Component inside container
├── c3-2-{slug}/
│   └── README.md                 ← Container 2
└── adr/
    └── adr-YYYYMMDD-{slug}.md    ← ADRs
```

**File Path Rules:**

| Level | Path | Example |
|-------|------|---------|
| Context | `.c3/README.md` | `.c3/README.md` (ONLY this) |
| Container | `.c3/c3-{N}-{slug}/README.md` | `.c3/c3-1-backend/README.md` |
| Component | `.c3/c3-{N}-{slug}/c3-{N}{NN}-{slug}.md` | `.c3/c3-1-backend/c3-101-api.md` |
| ADR | `.c3/adr/adr-{YYYYMMDD}-{slug}.md` | `.c3/adr/adr-20251216-auth.md` |

---

## Process

### Phase 1: Detect

Already done via Critical Gate.

### Phase 2: Discover (Socratic Questions)

**For fresh projects:**
- "What problem does this system solve?"
- "Who are the users/actors?"
- "What are the major deployable parts?"

**For existing codebases:**
- Explore code structure first
- "I see X, Y, Z directories. What are the major containers?"
- "How do these parts communicate?"

### Phase 3: Scaffold

```bash
# Create base structure
mkdir -p .c3/adr

# Create container folders based on discovery
mkdir -p .c3/c3-1-{slug}
mkdir -p .c3/c3-2-{slug}

# Create empty README (will be filled by c3-context-design)
touch .c3/README.md
```

### Phase 4: Delegate to Layer Skills

**INVOKE each skill in order:**

| Order | Skill | Creates |
|-------|-------|---------|
| 1 | **Use Skill tool → c3-context-design** | `.c3/README.md` |
| 2 | **Use Skill tool → c3-container-design** | `.c3/c3-{N}-*/README.md` |
| 3 | **Use Skill tool → c3-component-design** | `.c3/c3-{N}-*/c3-{N}{NN}-*.md` |
| 4 | **Use Skill tool → c3-config** | `.c3/settings.yaml` |

### Phase 5: Generate TOC

After all docs created:
```bash
# Run TOC generator
./scripts/build-toc.sh
# Or manually create TOC.md
```

---

## ⛔ Enforcement Harnesses

### Harness 1: V3 Structure (No V2 Patterns)

**Rule:** Use V3 hierarchical structure. V2 flat structure is prohibited.

| Prohibited (V2) | Required (V3) |
|-----------------|---------------|
| `context/c3-0.md` | `.c3/README.md` |
| `containers/c3-1.md` | `.c3/c3-1-{slug}/README.md` |
| `components/c3-101.md` | `.c3/c3-1-{slug}/c3-101-{slug}.md` |

🚩 **Red Flags:**
- Creating `context/`, `containers/`, or `components/` folders
- Any file named `c3-0.md`
- Components outside their container folder

### Harness 2: Skill Delegation (No Hallucination)

**Rule:** INVOKE layer skills. Never create C3 docs directly.

| Anti-Pattern | Correct Action |
|--------------|----------------|
| Writing `.c3/README.md` content directly | Use Skill tool → c3-context-design |
| "c3-container-design would create..." | Invoke the skill |
| Creating docs without skill invocation | Always delegate to layer skill |

🚩 **Red Flag:** Write tool used on `.c3/` files without prior Skill tool invocation

---

## Verification Checklist

Before claiming adoption complete, execute:

```bash
# Verify V3 structure
ls .c3/README.md                           # Context exists
ls -d .c3/c3-[1-9]-*/                       # Container folders exist
ls .c3/c3-[1-9]-*/README.md                 # Container READMEs exist

# Verify no V2 patterns
ls .c3/context/ 2>/dev/null && echo "ERROR: V2 context folder"
ls .c3/containers/ 2>/dev/null && echo "ERROR: V2 containers folder"
ls .c3/components/ 2>/dev/null && echo "ERROR: V2 components folder"
```

- [ ] Critical gate executed (existing state checked)
- [ ] User scenario confirmed (fresh/existing/rebuild)
- [ ] Discovery questions completed
- [ ] V3 structure scaffolded
- [ ] Layer skills INVOKED (not described)
- [ ] All verification commands pass
- [ ] TOC generated

---

## 📚 Reading Chain Output

**At the end of adoption, output a reading chain for the newly created docs.**

Format:
```
## 📚 Your New C3 Documentation

**Start here:**
└─ .c3/README.md (c3-0) - System overview

**Then explore containers:**
├─ .c3/c3-1-{slug}/README.md - [description]
├─ .c3/c3-2-{slug}/README.md - [description]
└─ ...

**Key components to understand:**
├─ c3-101 - [why this is important]
└─ c3-201 - [why this is important]

*Reading chain generated from docs created during adoption.*
```

**Rules:**
- List docs in logical reading order (context → containers → key components)
- Explain WHY each doc matters (not generic)
- Help user navigate their new documentation

---

## Related

- `references/discovery-questions.md` - Socratic question templates
- `references/v3-structure.md` - File structure conventions
- `references/archetype-hints.md` - Container type patterns
