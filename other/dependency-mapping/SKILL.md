---
name: dependency-mapping
description: >
  Map symbol dependencies, callers, and blast radius before editing code.
  Load when the user asks what depends on a symbol, what breaks if they change
  something, blast radius of a change, reverse dependencies, or which tests
  cover a function. Also triggers on "who calls this", "impact of changing",
  "dependency map", "what uses this", "find callers", or before any non-trivial
  edit when safe-change is not yet active. Pairs with codebase-understanding
  for broad architecture; this skill is symbol-scoped and edit-gated.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: alexsarrell/synapse-farsight, emberloom/cartograph, agentralabs/agentic-codebase
  resources:
    references:
      - IMPACT-QUERIES.md
      - examples.md
---
# Dependency Mapping

You answer three mandatory impact questions before any non-trivial code edit: what depends on this symbol, what breaks if it changes, and which tests cover it. Output is an evidence-backed impact report — not guesses from file names.

## Hard Rules

Never edit code — map only. Editing routes to `safe-change`.
Answer all three impact questions in `references/IMPACT-QUERIES.md` with cited paths before any edit elsewhere.
Prefer LSP or tree-sitter when available; fall back to ripgrep and import tracing — document which ladder rung you used.
Tag every claim `[EXTRACTED]` (read in source) or `[INFERRED]` (structural guess).
If scope is whole-repo architecture, call `codebase-understanding` first, then return here for symbol-level blast radius.

---

## Workflow

### Step 1 — Scope the target

Identify: symbol name, file path, change type (signature, behavior, rename, delete). Ask ONE question if ambiguous: "Which symbol or file should I map?"

### Step 2 — Run the capability ladder

1. **LSP** — go-to-references, find-references when the host exposes them.
2. **tree-sitter / AST** — import/call edges when a parser is available.
3. **Text search** — ripgrep for symbol name, qualified imports, string literals (routes, config keys).
4. **Test map** — search `test/`, `__tests__/`, `*_test.*`, `*.spec.*` for imports or describe blocks naming the symbol.

Record ladder rung in the report.

### Step 3 — Answer the three-question gate

Read `references/IMPACT-QUERIES.md`. Fill every row with evidence. If any row is unknown, mark `[AMBIGUOUS]` and list what to verify — do not proceed to edits until resolved or user accepts risk.

### Step 4 — Emit impact report

Use the output format below. State risk: `low` | `medium` | `high` with a plain-language reason.

### Step 5 — Hand off

If the user will edit next, recommend `safe-change` with this report attached.

---

## Gotchas

- Re-exports and barrel files (`index.ts`) hide real callers — trace through export chains.
- Dynamic dispatch (`getattr`, plugin registries, DI containers) may miss static references — flag as `[INFERRED]` gap.
- Generated code and lockfiles are not callers — exclude them.
- A symbol with zero static callers may still break via reflection, config, or API contracts.

---

## Output Format

```markdown
## Impact report — [symbol] in [file]

Capability ladder: [LSP | tree-sitter | text-search]
Risk: [low | medium | high] — [one sentence]

| Question | Answer | Evidence |
|----------|--------|----------|
| What depends on this? | [callers/importers] | [paths] |
| What breaks if I change it? | [breaking surfaces] | [paths] |
| Which tests cover it? | [test files] | [paths or NONE] |

Affected files: [list]
Recommended verify: [typecheck command] + [test command or "none — behaviorVerified: false"]
```

---

## Examples

Teaser: User asks "what breaks if I rename `validateSkill`?" → report lists 4 importers in eval-pipeline + 2 tests; risk medium.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "File name tells me enough" | Blast radius needs import/call evidence. |
| "I'll find callers after I edit" | That's how builds break. |
| "No tests means low risk" | No tests means **unverified** risk — flag `behaviorVerified: false`. |
| "Whole repo scan is faster" | Symbol scope only; use codebase-understanding for architecture. |
| "Dynamic calls don't matter" | Flag them — they are the #1 missed breakage. |

## Verification

- [ ] All three impact questions answered with paths
- [ ] Capability ladder rung stated
- [ ] Risk enum assigned with reason
- [ ] No code edits performed

## Red Flags

- Impact report with zero cited paths
- HIGH risk assigned without listing breaking surfaces
- Edit started before three-question gate complete

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 2 family)

## Impact Report

```
Dependency mapped: [symbol] | Risk: [level] | Callers: N | Tests: N | Ladder: [rung]
Handoff: [safe-change recommended | map-only complete]
```
