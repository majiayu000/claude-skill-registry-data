---
name: auto-fix
description: When reviewing code, generate the complete corrected version — not just the issues, but the exact fixed code ready to copy-paste.
---

# Auto-Fix Protocol

## Rule
Every review that returns ⚠️ WARNING or ❌ BLOCKED MUST include a complete corrected version of the code at the end of the review.

## Format

After the standard review verdict and issues list, add:

### Fixed Version

\`\`\`[language]
[Complete corrected code here — the ENTIRE file/function/component, not just the changed lines]
\`\`\`

Then add:

### Changes Made

1. [Line X]: [What changed and why]
2. [Line Y]: [What changed and why]
...

## Rules for Auto-Fix
1. The fixed version must be COMPLETE — copy-pasteable, not a diff or snippet
2. Include all imports, type definitions, and dependencies
3. Add inline comments only on the lines you changed: `// FORGE: [reason for change]`
4. If the fix requires new files (e.g., a Zod schema file, a middleware file), generate those too
5. If the fix requires database changes (RLS policies, functions, migrations), include the SQL
6. The fixed version must pass your own review — run through your 8-point checklist mentally before outputting it
7. If a fix is ambiguous (multiple valid approaches), provide the safest option and note the alternatives

## Fix Quality Standards
- The fix must not introduce new issues
- The fix must maintain existing functionality (don't break what works)
- The fix should follow the existing code style (don't reformat everything)
- Type safety must be strict (no any, proper generics)
- Error handling must be comprehensive
- Security must be defense-in-depth

## When NOT to Auto-Fix
- ✅ APPROVED reviews (nothing to fix)
- Architecture-level issues that require design discussion (flag these, don't rewrite the architecture)
- When the fix requires information you don't have (API keys, business logic decisions) — note what's needed

## Example

If the review found:
- No auth middleware
- Missing Zod validation
- No error handling

The fixed version includes ALL THREE fixes applied, not each one separately. The developer should be able to replace their code with the fixed version in one action.

## Changelog
- 2026-03-20: Initial protocol
