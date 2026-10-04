---
name: personas
description: >-
  Workflow-wide thinking modes for EPCI. 6 personas adapt Claude's behavior
  globally: questions asked, priorities, code patterns, MCP preferences.
  Use when: scoring algorithm detects domain match, keywords files stack detection.
  Not for: trivial questions, ideation sessions (use brainstormer instead).
allowed-tools: [Read, Glob, Grep]
---

# EPCI Personas — Workflow Thinking Modes

## Overview

6 personas defining **global thinking modes** that influence the entire EPCI workflow.
Unlike brainstormer personas (local facilitation), these affect all phases.

**Activation**: Via `--persona-X` flag or auto-activation scoring.

| Persona | Icon | Focus | Flag |
|---------|------|-------|------|
| [Architect](references/architect.md) | 🏗️ | System thinking, patterns, scalability | `--persona-architect` |
| [Frontend](references/frontend.md) | 🎨 | UI/UX, accessibility, Core Web Vitals | `--persona-frontend` |
| [Backend](references/backend.md) | ⚙️ | APIs, data integrity, reliability | `--persona-backend` |
| [Security](references/security.md) | 🔒 | Threat modeling, OWASP, compliance | `--persona-security` |
| [QA](references/qa.md) | 🧪 | Tests, edge cases, coverage | `--persona-qa` |
| [Doc](references/doc.md) | 📝 | Documentation, clarity, examples | `--persona-doc` |

## Persona vs Subagent

| Aspect | Persona | Subagent |
|--------|---------|----------|
| **Scope** | Entire workflow | Validation point |
| **Timing** | During generation | After generation |
| **Role** | Thinking mode | Verification |
| **Output** | Influences code | Verdict (APPROVED/REJECTED) |
| **Activation** | Auto or `--persona-X` | Always at checkpoints |

## Auto-Activation Algorithm

### Scoring Formula

```
Score = (keyword_score × 0.4) + (file_score × 0.4) + (stack_score × 0.2)
```

Each component is 0.0-1.0, resulting in final score 0.0-1.0.

### Thresholds

| Score | Action |
|-------|--------|
| > 0.6 | Auto-activate persona |
| 0.4-0.6 | Suggest to user at breakpoint |
| < 0.4 | No activation |

### Keyword Detection

For each persona, count matching keywords in brief:

```
keyword_score = min(1.0, matching_keywords / 3)
```

| Persona | Trigger Keywords |
|---------|-----------------|
| architect | architecture, design, pattern, scalability, DDD, domain, modular |
| frontend | component, UI, UX, responsive, accessibility, CSS, React, Vue |
| backend | API, database, service, endpoint, repository, migration, REST |
| security | vulnerability, threat, auth, encryption, OWASP, compliance, JWT |
| qa | test, coverage, quality, edge case, validation, TDD, BDD |
| doc | document, README, wiki, guide, API docs, changelog, tutorial |

### File Pattern Detection

Match impacted files against persona patterns:

```
file_score = matching_files / total_files
```

| Persona | Trigger File Patterns |
|---------|-----------------------|
| architect | `**/Architecture/**`, `**/Domain/**`, `**/patterns/**` |
| frontend | `*.jsx`, `*.tsx`, `*.vue`, `*.css`, `**/components/**` |
| backend | `**/Controller/**`, `**/Service/**`, `**/Repository/**`, `**/Entity/**` |
| security | `**/auth/**`, `**/security/**`, `**/payment/**`, `**/password/**` |
| qa | `**/tests/**`, `*.spec.*`, `*.test.*`, `**/fixtures/**` |
| doc | `*.md`, `**/docs/**`, `README*`, `CHANGELOG*` |

### Stack Detection

Match detected stack against persona affinity:

| Persona | Stack Affinity |
|---------|---------------|
| architect | Any (universal) |
| frontend | React, Vue, Angular, Svelte |
| backend | Symfony, Django, Spring, Laravel, Express |
| security | Any (universal) |
| qa | Any (universal) |
| doc | Any (universal) |

```
stack_score = 1.0 if stack matches affinity else 0.5
```

### Example Scoring

**Brief**: "Add user authentication endpoint with JWT"

```
Persona: backend
├── Keywords: "endpoint" ✓, "JWT" (→ security too)
│   → keyword_score = 1/3 = 0.33
├── Files: Controller, Service expected
│   → file_score = 0.8 (estimated)
└── Stack: Symfony
    → stack_score = 1.0

Score = (0.33 × 0.4) + (0.8 × 0.4) + (1.0 × 0.2) = 0.65 → AUTO-ACTIVATE

Persona: security
├── Keywords: "authentication" ✓, "JWT" ✓
│   → keyword_score = 2/3 = 0.67
├── Files: auth/** expected
│   → file_score = 0.6
└── Stack: Any
    → stack_score = 0.5

Score = (0.67 × 0.4) + (0.6 × 0.4) + (0.5 × 0.2) = 0.61 → AUTO-ACTIVATE
```

**Result**: Both backend and security score > 0.6. Display both as suggestions, recommend highest.

## MCP Integration (F12 Active)

Each persona automatically activates preferred MCP servers for enhanced context:

| Persona | Primary MCP | Secondary MCP | Auto-Trigger |
|---------|-------------|---------------|--------------|
| architect | Context7 | Sequential | Pattern analysis |
| frontend | Magic | Playwright | UI generation, E2E |
| backend | Context7 | Sequential | API patterns |
| security | Sequential | - | Threat analysis |
| qa | Playwright | - | E2E tests |
| doc | Context7 | - | Doc standards |

**Status**: MCP integration active (F12 implemented). See skill `mcp` for details.

### Fallback Behavior

If MCP unavailable:
```
⚠️ [MCP] Context7 not configured. Using web search for documentation.
```

Continue workflow with web search fallback.

## Priority Hierarchies

Each persona applies a specific priority order when making decisions:

| Persona | Priority Order |
|---------|---------------|
| architect | Maintainability > Scalability > Performance > Features |
| frontend | User needs > Accessibility > Performance > Aesthetics |
| backend | Reliability > Security > Performance > Features > Convenience |
| security | Defense in depth > Least privilege > Audit > Usability |
| qa | Prevention > Detection > Correction > Speed |
| doc | Clarity > Completeness > Brevity > Format |

## Coexistence with Brainstormer Personas

**Key Distinction**:

| Aspect | F09 Personas (6) | Brainstormer Personas (3) |
|--------|------------------|---------------------------|
| Scope | Entire EPCI workflow | `/brainstorm` only |
| Activation | `--persona-X` or auto | `mode [name]` command |
| Role | Global thinking mode | Facilitation style |
| Personas | architect, frontend, backend, security, qa, doc | Architecte 📐, Sparring 🥊, Pragmatique 🛠️ |

**No Conflict**: They operate at different levels:
- User activates F09 persona (e.g., `--persona-backend`)
- Within that context, brainstormer can use its 3 facilitation personas
- F09 influences WHAT is prioritized, brainstormer influences HOW facilitation happens

## Integration Points

### In /brief (Step 4.5)

After complexity evaluation, before output generation:
1. Run scoring algorithm for all 6 personas
2. If score > 0.6: Auto-activate, display in breakpoint
3. If score 0.4-0.6: Suggest in breakpoint
4. Pass persona context to Feature Document §1

### In /epci (All Phases)

- **Phase 1**: Persona influences planning priorities
- **Phase 2**: Persona affects code review focus, subagent selection
- **Phase 3**: Persona guides documentation emphasis

### Display in Breakpoints

```
┌─────────────────────────────────────────────────────────────────────┐
│ FLAGS: --think-hard (auto) | --persona-backend (auto: 0.72)        │
```

## Quick Reference

### Activation

```bash
# Explicit activation
/epci --persona-backend

# Auto-activation (based on brief content)
/brief "Add REST API for user management"
# → --persona-backend auto-activated (score: 0.68)

# Override auto-activation
/epci --persona-security  # Explicit always wins
```

### Checking Active Persona

In any breakpoint, active persona shown in FLAGS line with source:
- `(explicit)` — User specified with flag
- `(auto: X.XX)` — Auto-activated with score
- `(suggested)` — Score 0.4-0.6, user can accept

---

*EPCI Personas v1.0 — F09 Implementation*
