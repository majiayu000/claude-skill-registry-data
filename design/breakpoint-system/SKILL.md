---
name: epci:breakpoint-system
description: >-
  Displays standardized interactive breakpoints with AskUserQuestion integration
  for EPCI v6.0 workflows. Renders ASCII box UI with context, options, and
  proactive suggestions (P1/P2/P3). Supports 8 types: validation, analysis,
  plan-review, phase-transition, decomposition, diagnostic, ems-status, info-only.
  Use when: displaying phase breakpoint, requesting user validation, showing
  diagnostic choices, presenting EMS status. Internal component for EPCI skills.
  Not for: direct user invocation, simple text output without interaction.
user-invocable: false
allowed-tools: Read, AskUserQuestion
---

# Breakpoint System — Unified Interactive Breakpoints

Internal component for displaying standardized breakpoints across EPCI v6.0 workflows.

## Overview

Centralizes all breakpoint display logic for consistency, token economy, and maintainability.

**Benefits:**
- **Unified UX**: Consistent ASCII box format across all skills
- **AskUserQuestion native**: Interactive buttons vs text input
- **Proactive suggestions**: P1/P2/P3 priority system
- **Free response always**: Last option enables custom input

## Supported Types

| Type | Usage | Interactive |
|------|-------|-------------|
| `validation` | Simple choices (Validate/Modify/Cancel) | Yes |
| `analysis` | Questions + suggestions + evaluation | Yes |
| `plan-review` | Metrics + validations + preview | Yes |
| `phase-transition` | End of EPCI phase (E→P→C→I) | Yes |
| `decomposition` | Specs table + modification menu | Yes |
| `diagnostic` | Root cause + ranked solutions | Yes |
| `ems-status` | EMS 5 axes + brainstorm progress | Display only |
| `info-only` | Metrics without interaction | Display only |

## Workflow

1. **Parse** input parameters (type, title, data, ask, suggestions)
2. **Load** template from [references/templates.md](references/templates.md)
3. **Render** ASCII box with variable substitution
4. **Invoke** AskUserQuestion (if interactive type)
5. **Return** user response to calling skill

## CRITICAL: Invocation Protocol

**⚠️ WARNING**: La syntaxe `@skill:epci:breakpoint-system` est **DOCUMENTAIRE SEULEMENT**.
Claude interprète les blocs de code comme des **exemples**, pas comme des **instructions d'exécution**.

### Comment invoquer réellement un breakpoint

Les breakpoints doivent être implémentés **directement** dans les step files avec:

1. **Section BREAKPOINT impérative** (pas dans un bloc de code)
2. **Boîte ASCII affichée** (pas de @skill:)
3. **Appel AskUserQuestion explicite**
4. **Instruction ATTENDS**

### Format impératif correct

```markdown
### X. BREAKPOINT: {Title} (OBLIGATOIRE)

AFFICHE cette boîte:

┌─────────────────────────────────────────────────────────────────────┐
│ {ICON} {TITLE}                                                      │
├─────────────────────────────────────────────────────────────────────┤
│ {CONTENT}                                                           │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Option 1 (Recommended) — description                      │ │
│ │  [B] Option 2 — description                                    │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

APPELLE:
AskUserQuestion({
  questions: [{
    question: "{QUESTION}",
    header: "{HEADER}",
    multiSelect: false,
    options: [
      { label: "Option 1 (Recommended)", description: "..." },
      { label: "Option 2", description: "..." }
    ]
  }]
})

⏸️ ATTENDS la réponse utilisateur avant de continuer.
```

### Syntaxe documentaire (NE PAS UTILISER pour invoquer)

La syntaxe ci-dessous est pour **documentation/référence** uniquement:

```typescript
// DOCUMENTATION ONLY - Claude n'exécute pas ce bloc
@skill:epci:breakpoint-system
  type: {TYPE}
  title: "{TITLE}"
  data: { /* type-specific structure */ }
  ask: {
    question: "{QUESTION}"
    header: "{HEADER}"       // Max 12 chars
    options: [
      {label: "{LABEL}", description: "{DESC}"},
      ...
    ]
  }
  suggestions: [             // Optional
    {pattern: "...", text: "...", priority: "P1|P2|P3", action: "..."}
  ]
```

## Rules

1. **Free response ALWAYS last**: Option "Autre reponse..." mandatory
2. **Max 4 options**: 3 choices + 1 free response
3. **Header max 12 chars**: Truncated if exceeded
4. **(Recommended) marker**: First option if default path
5. **Suggestions sorted**: P1 → P2 → P3, max 3 displayed

## Type Data Schemas

### validation

```typescript
data: {
  context: string,           // Brief context
  item_to_validate: {
    objectif: string,
    contexte: string,
    contraintes: string,
    success_criteria: string
  }
}
```

### analysis

```typescript
data: {
  exploration: {
    stack: string,
    files_impacted: number,
    patterns: string[],
    risks: string[]
  },
  questions: Array<{tag: string, text: string, suggestion: string}>,
  suggestions_ia: {
    architecture: string,
    implementation: string,
    risks: string
  },
  evaluation: {
    category: "TINY" | "SMALL" | "STANDARD" | "LARGE",
    files: number,
    loc_estimate: number,
    risk: "LOW" | "MEDIUM" | "HIGH"
  }
}
```

### plan-review

```typescript
data: {
  metrics: {
    complexity: string,
    complexity_score: number,
    files_impacted: number,
    time_estimate: string,
    risk_level: string,
    risk_description: string
  },
  validations: {
    plan_validator: {
      verdict: "APPROVED" | "APPROVED_WITH_WARNINGS" | "NEEDS_REVISION",
      completeness: string,
      consistency: string,
      feasibility: string,
      quality: string
    }
  },
  skills_loaded: string[],
  preview_next: {
    tasks: Array<{title: string, time: string}>,
    remaining_tasks: number
  },
  feature_doc_path: string
}
```

### phase-transition

```typescript
data: {
  phase_completed: "explore" | "plan" | "code" | "inspect",
  phase_next: "plan" | "code" | "inspect" | "done",
  summary: {
    duration: string,
    tasks_completed: number,
    files_modified: string[],
    tests_status: string
  },
  checkpoint_created: {
    id: string,
    resumable: boolean
  }
}
```

### decomposition

```typescript
data: {
  source_file: string,
  analysis: {
    lines: number,
    total_effort: number,
    structure: string
  },
  specs: Array<{
    id: string,
    title: string,
    effort: number,
    priority: string,
    deps: string,
    status: string
  }>,
  parallelization: number,
  optimized_duration: number,
  sequential_duration: number,
  alerts: string[],
  validator_verdict: string
}
```

### diagnostic

```typescript
data: {
  root_cause: string,
  confidence: number,         // 0.0 - 1.0
  decision_tree: string,      // Path representation
  solutions: Array<{
    id: string,
    title: string,
    effort: string,
    risk: "Low" | "Medium" | "High"
  }>
}
```

### ems-status

```typescript
data: {
  phase: "DIVERGENT" | "CONVERGENT" | "TRANSITION",
  iteration: number,
  ems: {
    score: number,            // 0-100
    delta: string,            // "+12" or "-5"
    axes: {
      clarity: number,
      depth: number,
      coverage: number,
      decisions: number,
      actionability: number
    },
    weak_axes: string[]
  },
  done: string[],
  open: string[],
  commands: string[]          // Available commands
}
```

### info-only

```typescript
data: {
  metrics: Record<string, any>,
  summary: string
}
```

## Execution Steps

### Step 1: Parse Input

Extract and validate:
- `type` (required): Must be one of 8 supported types
- `title` (required): Breakpoint title
- `data` (required): Type-specific structure
- `ask` (optional for display-only): Question configuration
- `suggestions` (optional): Proactive suggestions array

### Step 2: Load Template

Read `references/templates.md` and find section matching type.

### Step 3: Render ASCII Box

1. Build header with icon and title
2. Render content section per type schema
3. Add suggestions block if present (sorted P1→P2→P3, max 3)
4. Add options block with free response last

**Template structure:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ {ICON} {TITLE}                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ {CONTENT SECTION}                                                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES (if present)                                 │
│ [P1] {text} → {action}                                              │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] {Option 1} (Recommended) — {description}                  │ │
│ │  [B] {Option 2} — {description}                                │ │
│ │  [C] {Option 3} — {description}                                │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 4: Invoke AskUserQuestion

For interactive types (not ems-status, info-only):

```typescript
const options = [
  ...ask.options,
  { label: "Autre reponse...", description: "Saisir une reponse libre" }
];

AskUserQuestion({
  questions: [{
    question: ask.question,
    header: ask.header.slice(0, 12),
    multiSelect: false,
    options: options
  }]
});
```

**Fallback if AskUserQuestion fails:**
```
AskUserQuestion indisponible. Veuillez repondre par:
- A, B, C... pour choisir une option
- Ou tapez votre reponse libre
```

### Step 5: Return Response

```typescript
{
  selected: string,        // "A", "B", "C", or "free"
  selectedLabel: string,   // Full label text
  freeText?: string,       // If free response selected
  timestamp: string        // ISO8601
}
```

For display-only types, return `null`.

## Decision Tree

```
INPUT received
    │
    ├─► type IN [validation, analysis, plan-review, phase-transition,
    │           decomposition, diagnostic]
    │       → Interactive mode
    │       → Render + AskUserQuestion
    │       → Return user choice
    │
    ├─► type IN [ems-status, info-only]
    │       → Display-only mode
    │       → Render only
    │       → Return null
    │
    └─► type UNKNOWN
            → Error with supported types list

SUGGESTIONS handling:
    │
    ├─► suggestions[] present AND non-empty
    │       → Sort by priority (P1 first)
    │       → Take max 3
    │       → Insert block before options
    │
    └─► ELSE
            → Skip suggestions block
```

## Error Handling

| Error | Action |
|-------|--------|
| Unknown type | Error message with list of 8 supported types |
| Missing required data | Warning + use defaults where possible |
| AskUserQuestion fails | Fallback to text input parsing |
| Header > 12 chars | Truncate with warning in logs |
| Options > 4 | Error: "Maximum 3 options + 1 free response" |

## Integration Points

### Skills that use breakpoint-system

| Skill | Breakpoint Types Used |
|-------|----------------------|
| `/brainstorm` | ems-status, validation |
| `/spec` | validation, plan-review |
| `/implement` | validation, phase-transition, plan-review |
| `/quick` | validation, diagnostic (SMALL only) |
| `/debug` | diagnostic |
| `/refactor` | plan-review |
| `/factory` | validation |

## Reference Files

- [templates.md](references/templates.md) — ASCII templates per type
- [askuserquestion-guide.md](references/askuserquestion-guide.md) — AskUserQuestion integration
- [suggestions-guide.md](references/suggestions-guide.md) — Proactive suggestions P1/P2/P3
- [examples.md](references/examples.md) — Usage examples by calling skill

## Limitations

This skill does NOT:
- Persist state (delegated to state-manager)
- Implement business logic (stays in calling skills)
- Validate business data (display only)
- Generate suggestions (received as input)

## Anti-patterns à éviter

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| `@skill:epci:breakpoint-system` dans bloc code | Claude ignore l'invocation | Format impératif direct |
| Pas de AskUserQuestion | Pas d'interactivité | Appel explicite obligatoire |
| Pas de ATTENDS | Continue sans réponse | Instruction ATTENDS explicite |
| Breakpoint sans numérotation | Ordre ambigu | Section `### X. BREAKPOINT:` |

## Checklist pour auteurs de skills

Avant de commit un step file avec breakpoint:

- [ ] Section `### X. BREAKPOINT: {Title} (OBLIGATOIRE)`
- [ ] Boîte ASCII affichée en dehors d'un bloc de code exécutable
- [ ] Appel `AskUserQuestion({...})` explicite
- [ ] Instruction `⏸️ ATTENDS la réponse`
- [ ] Pas de syntaxe `@skill:epci:` dans les instructions
