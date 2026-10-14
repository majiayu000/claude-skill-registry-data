---
name: unused-import-implementation
description: Diagnose and resolve newly added but unused imports by inferring intent from surrounding code and implementing the missing use case. Use when linting or review reports an unused import and the import appears intentional or recent, and the goal is to complete behavior rather than remove code.
agent:
  display_name: "Unused Import Implementation"
  short_description: "Implement contextual use for unused imports"
  default_prompt: "Analyze unused imports, infer intent from surrounding code, and implement a real use case instead of deleting imports by default."
---

# Unused Import Implementation

## Objective

Turn unused-import findings into completed behavior when intent is inferable from local context. Prefer implementing the missing use case over deleting imports.

## Workflow

1. Confirm scope.
Identify each unused import and whether it was recently added in the same change.

2. Infer intent from nearby code.
Inspect function names, TODOs, comments, call sites, variable names, tests, and adjacent modules.

3. Choose an implementation path.
Implement one concrete use that matches the inferred intent:
- Parse/validate/transform input with the imported helper
- Add missing service call, serializer, or mapper usage
- Wire imported type/class into object construction or dependency flow
- Add missing error handling, logging, or formatting step

4. Implement minimally and safely.
Use the import in production code first. If intent is test-only, add targeted tests that use the related behavior.

5. Verify behavior.
Run relevant lint/tests and confirm the import is now meaningfully used.

## Guardrails

- Do not remove an unused import as the first action.
- Remove an import only when evidence shows it is accidental or obsolete.
Evidence includes: mismatched feature scope, dead code path, duplicate utility, or explicit replacement.
- Avoid fake usage (no placeholder calls or no-op references).
- Keep changes narrow and aligned to existing architecture.

## Response Contract

When applying this skill, report:
- Inferred intent and evidence used
- Implemented use case
- Validation performed
- Any imports removed and explicit reason

## Bundled Script

Copy `find-unused-imports.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/unused-import-implementation/scripts/find-unused-imports.ps1 .ai_scripts/
```

Scans Python/JS/TS files for unused imports, then suggests implementation paths based on nearby comments, function names, and TODOs:

```powershell
.ai_scripts\find-unused-imports.ps1 -ProjectPath src/ -FileFilter "*.py"
```

## Cross-references

- **no-dead-code-removal** — Both address code you added that seems unused. unused-import-implementation completes the intended usage; no-dead-code-removal prevents deletion.

- **safe-code-modifications** — Both verify an import is truly unused before acting.

- **anti-phantom-symbols** — Intended usage should reference real symbols.
- **skill-loader** — Apply the capped selection policy when deciding which implementation-safety skills should also be active for unused imports.
