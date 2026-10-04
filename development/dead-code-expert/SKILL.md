---
name: dead-code-expert
description: This skill should be used when the user wants to find, audit, or remove dead code, unused imports, unused functions, unused variables, duplicate implementations, or simplify a codebase. Works across all programming languages. Relevant when the user says "find dead code", "remove dead code", "remove unused imports", "find duplicate code", "simplify this codebase", "find unused functions", "find unused code", "remove commented out code", "what code is unused", "find orphaned files", "detect duplicate implementations", "find unreachable code", "clean up this codebase", or "audit for unused code".
---

# Dead Code Expert

Find and eliminate dead code, duplicate implementations, and unnecessary complexity across any programming language. Every finding explains WHY the code is dead and the concrete cost of keeping it (cognitive overhead, build time, misleading developers, masking bugs).

## How to Think About Dead Code

Before flagging anything, identify which category it belongs to:

- **Layer 1 -- Certainly Dead:** Unreachable code after return/break/throw, unused private functions, unused local variables, imports with zero references. Safe to remove immediately.
- **Layer 2 -- Probably Dead:** Exported functions with no callers in the project, commented-out code blocks, `#[allow(dead_code)]` / `// eslint-disable unused` suppressions, permanently-off feature flags. Verify before removing.
- **Layer 3 -- Suspiciously Alive:** Code that LOOKS dead but may be used via reflection, serialization, framework magic, dynamic dispatch, or public API surface. Investigate before touching.
→ *Consult [false-positives reference](references/false-positives.md) for the full 10-category checklist and scoring framework.*

When dead code is found, reframe it as a design question:

| Dead Code Pattern | Don't Just Say | Ask Instead |
|---|---|---|
| Unused function | "Delete it" | Why was it written? Is there a missing caller? |
| Duplicate implementation | "Remove one" | Which is canonical? Why did duplication happen? |
| Commented-out block | "Delete it" | Is there in-progress work? Check git blame. |
| Unused abstraction layer | "Inline it" | Was it speculative generality? |
| Dead feature flag | "Remove the branch" | Is there a deprecation process to follow? |

## Detection Process

When scanning for dead code, work through these categories in order.

1. **Unused Imports** -- Imports/includes/requires with no reference in file.
→ *Consult [grep patterns](references/grep-patterns.md) for per-language detection.*

2. **Unused Variables & Parameters** -- Assigned but never read (dead stores).
3. **Unused Functions & Methods** -- Defined but never called.
4. **Unused Classes & Types** -- Defined but never instantiated or referenced.
→ *Consult [detection catalog](references/detection-catalog.md) for categories 2-6 with per-language tools.*

5. **Unreachable Code** -- Code after return/break/throw, dead branches (always-true/false conditions).
6. **Commented-Out Code** -- Code blocks in comments (not documentation).

7. **Duplicate / Dual Implementations** -- Same logic implemented twice differently.
8. **Speculative Generality** -- Abstractions used in exactly one place, interfaces with single implementation, unused parameters kept "for future use".
→ *Consult [duplicate code reference](references/duplicate-code.md) for clone types, dual implementation patterns, and DRY escalation.*

9. **Dead Test Code** -- Skipped tests, unused fixtures, orphaned test files.
10. **Debug Artifacts** -- `console.log`, `print()`, `dbg!()`, `TODO`/`FIXME` markers left in production code.

## Thinking Prompts

Before removing code, work through:

1. **Is this genuinely dead?** Check for reflection, serialization, dynamic imports, framework conventions, public API consumers.
→ *Consult [false-positives reference](references/false-positives.md) before every medium-confidence removal.*
2. **Why does this exist?** Check `git log` / `git blame`. If someone wrote it recently, it might be in-progress work. If it's years old with no references, it's dead.
3. **What's the cost of keeping it?** Cognitive overhead for every developer who reads it. Misleading grep results. False confidence from tests that exercise dead paths. Build time for code nobody uses.

## Confidence Levels

Label every finding:

- **certain** -- Compiler/linter confirms it (unused import, unreachable after return). Remove immediately.
- **high** -- No references found in project-wide search. Remove after quick verification.
- **medium** -- Might be used via dynamic means (reflection, templates, string-based lookup). Investigate first.
- **low** -- Potentially used by external consumers (library public API, plugin interface). Do not remove without understanding consumers.

## Output Format

Group findings by file. For each finding:
1. File path and line number
2. Confidence level
3. Category (from the 10 categories above)
4. **What is dead** -- name the specific symbol, block, or pattern
5. **Why it's dead** -- the evidence (zero references, unreachable, etc.)
6. **Cost of keeping it** -- cognitive overhead, misleading results, build time, masking bugs
7. Recommended action (delete, inline, consolidate, investigate)

End with a prioritized summary: certain items first, then high confidence, then medium.

## The AI Slop Test

If a codebase uses AI coding tools, check for AI-specific dead code fingerprints: copy-pasted logic across services, wrapper functions adding nothing, single-impl interfaces, commented-out "previous attempts", excessive restating comments, phantom edge case handling, reimplemented stdlib, orphaned files, refactoring avoidance (`v2`/`_old`/`_legacy` naming), security theater in tests, and unnecessary backward compatibility shims kept after a migration is complete.
→ *Consult [AI slop patterns](references/ai-slop-patterns.md) for the full catalog with detection commands and scorecard.*

## Safe Removal & Prevention

→ *Consult [safe removal strategies](references/safe-removal.md) for phased approach, library API considerations, and monorepo concerns.*
→ *Consult [prevention practices](references/prevention.md) for CI rules, review checklists, and cultural norms.*

## Language Detection

Detect the project language from file extensions, config files, and directory structure. For multi-language projects, scan each language independently.
→ *Consult [language tools](references/language-tools.md) for per-language tool configs and compiler settings.*

---

Approach every finding as a meticulous code archaeologist. Dead code is not just clutter -- it misleads, it hides bugs, it wastes every developer's time. Hunt with precision, verify with evidence, remove with confidence. The best line of code is the one you delete.
