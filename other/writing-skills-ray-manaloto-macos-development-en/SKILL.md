---
name: writing-skills
description: Use when creating, editing, or verifying agent skills before deployment. Emphasizes test-driven skill writing and tight frontmatter.
---

# Writing Skills (Concise)

## Core Principles
- Treat skill authoring like TDD: baseline failure → write skill → verify compliance → refactor.
- Skills live in flat namespaces (e.g., `.claude/skills`). Keep SKILL.md lean; move heavy refs to supporting files.
- Frontmatter: only `name`, `description`; hyphenated name; description is “Use when …”.

## Minimal SKILL.md Structure
1) Frontmatter (name, description)
2) Title and 1–2 sentence overview
3) When to Use (symptoms/contexts + when NOT)
4) Steps / Guidance (succinct, numbered; keep under 500 lines total)
5) References (links/filenames for deeper material)

## TDD Mapping for Skills
- RED: run a pressure scenario; observe agent failure/gaps.
- GREEN: write minimal guidance to close the gaps; rerun scenario.
- REFACTOR: tighten loopholes, clarify triggers, keep concise.

## When to Write a Skill
- Non-obvious techniques you’d reuse across projects.
- Patterns/heuristics that need judgment (not easy to automate with linters).
- Common failure modes you’ve observed in agents.
- Don’t write for one-offs or enforceable-by-linter rules.

## Good Skill Hygiene
- Keep instructions imperative and brief; avoid narratives.
- Prefer numbered steps over prose; add short examples only when needed.
- Link out to heavy references instead of embedding long appendices.
- Ensure tool usage is explicit (names, params, when to call).
- Include “When NOT to use” where applicable.

## Validation Checklist (self-review)
- [ ] Frontmatter present with correct fields only.
- [ ] Description starts with “Use when …” and is specific.
- [ ] ≤500 lines; no filler; supporting docs moved out.
- [ ] Steps are actionable, ordered, and map to the trigger conditions.
- [ ] Tool names/params spelled out; side effects called out.
- [ ] No committed secrets or env-specific instructions.

## Example Skeleton
```
---
name: my-skill
description: Use when fixing flaky HTTP tests that depend on external APIs.
---
# HTTP Test Hardening
## When to Use
- Tests flaky due to network or third-party API
- CI failures with timeouts/429s

## Steps
1) Add VCR/recording (tool: <tool-name>) and update fixtures.
2) Stub auth/IDs via env vars; document in README.
3) Add retry/backoff helper for remaining live calls.
4) Run tests locally + CI to confirm stability.

## References
- docs/vcr-setup.md
- scripts/update-fixtures.sh
```

## Suggested Supporting Files
- `README.md` for examples, longer explanations
- `tools/` for scripts/templates
- `refs/` for large reference material

## Maintaining Skills
- Periodically rerun pressure scenarios; update for new agent behaviors.
- Remove stale sections; keep SKILL.md tight and current.
- Consolidate duplicates; prefer one canonical skill per domain.
