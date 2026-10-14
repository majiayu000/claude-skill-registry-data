---
name: docstring-enforcer
description: "Use when adding or revising documentation for Python modules/Django code or exported TypeScript/React utilities. Triggers: docstring, JSDoc, document this file, lib utilities, improve docs, and explain intent."
---

# Docstring Enforcer Skill

Use this skill for meaningful documentation that explains _why_ code exists and _how_ it handles edge cases.

## Rules

### 🐍 Python (Google Style)

- **Standard:** Use Google-style docstrings and PEP 257.
- **Structure:** Include `Args:`, `Returns:`, and `Raises:` only when they provide value. Do not add empty sections.
- **Django Specifics:** Document the "why" behind complex QuerySets or signal receivers. Trivial dunder methods or obvious model fields can remain undocumented if self-explanatory.
- **Intent:** Favor workflow context over repeating the function name (e.g., "Invalidates the cache after user logout" vs "Does logout stuff").

### ⚛️ TypeScript & Next.js (JSDoc Style)

- **Standard:** Use JSDoc for exported utilities, hooks, and complex components.
- **Frontend `lib/` Policy:** ALL shared utilities in `lib/` must include:
  - **@example:** A brief code snippet showing typical usage.
  - **Edge Cases:** Describe behavior for `null`, `undefined`, or empty strings in `@param` or `@returns`.
- **Clarity:** Do not just restate TypeScript types. Explain constraints (e.g., "The string must be a valid ISO-8601 date").

## References

- **Gold Standard (Python):** See `core/models.py` and `core/pipeline.py`.
- **Gold Standard (TS/lib):** See `frontend/src/lib/formatters.ts` (if applicable) for example-driven JSDoc.
- **Context:** Check `docs/DEVELOPER_GUIDE.md` to ensure docs align with overall system architecture.

## Workflow

1. Analyze the file to understand its role in the Django/Next.js bridge.
2. If documentation is missing or outdated, rewrite it using the styles above.
3. Ensure that if a Django API field changes, the corresponding Next.js JSDoc for that field is also flagged for an update.
