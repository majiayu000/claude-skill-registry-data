---
name: ha:document
description: Generate module-level and function-level PEP 257 docstrings for Home Assistant integration modules, and TSDoc for ha-frontend Lit components. Use when explicitly asked to write docstring/TSDoc comments — NOT for README or external docs.
effort: low
argument-hint: [plan-file OR feature-name]
---

# Document

Generate documentation for newly implemented features.

## Usage

```
/ha:document .claude/plans/magic-link-auth/plan.md
/ha:document magic link authentication
/ha:document  # Auto-detect from recent plan
```

## Iron Laws

1. **Never remove existing documentation** — Existing docs may reflect design intent that isn't obvious from code alone; update rather than replace
2. **PEP 257 docstring on every module, class, and function** — ruff's `D` rules enforce this in core; the header is a single imperative sentence ending in a period (PS20 — "Please follow PEP8 for docstrings." — MartinHjelmare, https://github.com/home-assistant/core/pull/156401#discussion_r2746284568)
3. **ADRs capture the "why", not the "what"** — Code shows what was built; ADRs explain why this approach was chosen over alternatives
4. **Match the docstring to the function's public API** — Document parameters, return values, and raised exceptions (`ConfigEntryNotReady`, `ServiceValidationError`, ...); callers shouldn't need to read the implementation
5. **DO NOT write rich documentation for untested code** — a lint-satisfying single-sentence docstring is fine, but detailed Args/Raises documentation implies a stable contract; document only after tests confirm the function behaves as described

## What Gets Documented

| Output | Description |
|--------|-------------|
| Module docstring | For new integration modules/classes missing documentation |
| Function/method docstring | For public functions/methods without docs (TSDoc for frontend Lit components) |
| README section | For user-facing features |
| ADR | For significant architectural decisions |

## Workflow

### Step 0: Pre-check (avoid no-op runs)

Run `git diff --name-only HEAD~5 | grep -E '\.(py|ts)$' | grep -v '^tests/' | head -20` to check for new `.py` (integration) or frontend `.ts` files.

If NO new files were added (only modifications), skip the full
audit and report: "No new modules — documentation coverage unchanged."
This prevents 35-message analysis sessions that conclude "PASS" with
zero output (confirmed: session bb0a0454 wasted ~2K tokens on no-op).

1. **Identify** new modules from recent commits or plan file
2. **Check** documentation coverage (module docstrings, function docstrings, TSDoc on Lit components)
3. **Generate** missing docs using templates
4. **Add** README section if user-facing feature
5. **Create** ADR if architectural decision was made
6. **Write** report to `.claude/plans/{slug}/reviews/{feature}-docs.md`

## When to Generate ADRs

| Trigger | Create ADR |
|---------|-----------|
| New PyPI requirement in manifest | Yes |
| New config-entry version bump / migration | Maybe (if migration non-obvious) |
| New coordinator scheduling pattern or stateful in-loop cache | Yes (explain why polling/push/cache is needed) |
| New integration module split | Maybe (if boundaries non-obvious) |
| New auth mechanism (OAuth, reauth flow) | Yes |
| Performance optimization | Yes |

## Integration with Workflow

```text
/ha:plan → /ha:work → /ha:review
       ↓
/ha:document  ← YOU ARE HERE (optional, suggested after review passes)
```

## References

- `${CLAUDE_SKILL_DIR}/references/doc-templates.md` — Module docstring, function docstring, README, ADR templates
- `${CLAUDE_SKILL_DIR}/references/output-format.md` — Documentation report format
- `${CLAUDE_SKILL_DIR}/references/doc-best-practices.md` — PEP 257 and TSDoc documentation best practices
- `${CLAUDE_SKILL_DIR}/references/documentation-patterns.md` — Detailed documentation patterns
