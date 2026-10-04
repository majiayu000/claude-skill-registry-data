---
name: synthetic-skill
description: Minimal synthetic skill used by the uninstall-info-flow fixture as the on-disk target for the happy-path uninstall and ambiguous-name disambiguation cases. Not a real skill — exists only as a fixture artifact.
---

# Synthetic Skill (fixture)

This skill exists exclusively as a behavioral-fixture artifact for
`tests/fixtures/uninstall-info-flow/`. It has no end-user behavior and is
never installed from the catalog.

The fixture's `initial-state.json` references this single SKILL.md file from
two different `repo` entries (`test-fixtures/repo-a` and
`test-fixtures/repo-b`) to exercise the bare-name disambiguation path in the
uninstall and info flows. This is illustrative, not production-realistic — a
real install would have two distinct on-disk directories under different
skill-roots.
