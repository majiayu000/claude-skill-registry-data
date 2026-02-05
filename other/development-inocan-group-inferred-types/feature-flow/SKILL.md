---
name: feature-flow
description: Guides a user through DDD → BDD → TDD → Git for a single feature, staying code-agnostic and interactive.
allowed-tools: Read, Edit, Glob
---
# Feature Flow Playbook

When the user is talking about "starting a feature", "domain", "scenarios", or "tests":

1. Check docs/workflow/feature-state.json for the current feature and phase.
2. If no feature is active:
   - Suggest `/feature:start "Feature name"` and explain that this will create notes/feature/tdd-plan files.
3. In DDD:
   - Encourage the user to talk through terms, rules, and examples.
   - Use ddd-partner to capture this in domain-notes.md.
4. In BDD:
   - Encourage concrete scenarios.
   - Use bdd-partner and /bdd:feature to refine feature.feature.
5. In TDD:
   - Focus on one small test at a time.
   - Use tdd-partner and /tdd:plan to keep tests derived from scenarios.
6. When the user says a feature is "done":
   - Suggest `/feature:accept` to run tests and optionally commit with git.

Always keep the user involved in decisions and wording.
