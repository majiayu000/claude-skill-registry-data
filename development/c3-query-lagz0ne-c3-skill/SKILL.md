---
name: c3-query
description: |
  This skill should be used when the user asks "where is X", "how does X work", "explain X",
  "show me the architecture", "find component", "what handles X", or references C3 IDs (c3-0, c3-1, adr-*).
  Requires .c3/ to exist. For changes, route to c3-alter instead.
---

# C3 Query - Architecture Navigation

Navigate C3 docs AND explore corresponding code. Full context = docs + code.

## REQUIRED: Load References First

1. `../../references/skill-harness.md` - Routing and red flags
2. `../../references/layer-navigation.md` - How to traverse C3 docs

## Query Flow

```
Query → Clarify Intent → Navigate Layers → Extract References → Explore Code
              │
              └── Use AskUserQuestion if ambiguous
```

---

## Step 0: Clarify Intent

**Ask when:**
- Query vague ("how does X work?" - which aspect?)
- Multiple interpretations ("authentication" - login? tokens? sessions?)
- Scope unclear ("frontend" - whole container or specific component?)

**Skip when:**
- Query includes C3 ID (c3-102)
- Query specific ("where is login form submitted?")
- User says "show me everything about X"

---

## Step 1-2: Navigate and Extract

Follow layer navigation: **Context → Container → Component**

| Doc Section | Extract For Code |
|-------------|------------------|
| Component name | Class/module names |
| `## References` | Direct file paths, symbols |
| Technology | Framework patterns |
| Entry points | Main files, handlers |

---

## Step 3: Explore Code

Use extracted references:
- **Glob**: `src/auth/**/*.ts`
- **Grep**: Class names, functions
- **Read**: Specific files from `## References`

---

## Query Types

| Type | User Says | Response |
|------|-----------|----------|
| Docs | "where is X", "explain X" | Docs + suggest code exploration |
| Code | "show me code for X" | Full flow through code |
| Deep | "explore X thoroughly" | Docs + Code + Related |

---

## Response Format

```
**Layer:** <c3-id> (<name>)

<Architecture from docs>

**Code References:**
- `path/file.ts` - <role>

**Key Insights:**
<Observations from code>

**Related:** <navigation hints>
```
