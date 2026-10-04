---
name: testing-skills
description: >
  Testing, debugging, and verification lifecycle: TDD, systematic debugging, unit/integration/E2E testing patterns, pre-completion verification, behavioral evaluations for agent logic, and webapp testing with Python Playwright scripts.
---

# Testing & Quality

Meta-skill consolidating testing and quality assurance expertise. Each sub-skill below is a
full standalone skill with its own instructions, scripts, and references.
Match the user's intent to the most specific sub-skill, then read its
SKILL.md and follow its instructions completely.

## Sub-Skills

### test-driven-development
- **Description:** Use when implementing any feature or bugfix, before writing implementation code
- **Path:** `.subSkills/test-driven-development/SKILL.md`

### systematic-debugging
- **Description:** Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- **Path:** `.subSkills/systematic-debugging/SKILL.md`

### javascript-testing-patterns
- **Description:** Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and TDD
- **Path:** `.subSkills/javascript-testing-patterns/SKILL.md`

### e2e-testing-patterns
- **Description:** Master end-to-end testing with Playwright and Cypress to build reliable test suites that catch bugs and enable fast deployment
- **Path:** `.subSkills/e2e-testing-patterns/SKILL.md`

### verification-before-completion
- **Description:** Use when about to claim work is complete, fixed, or passing — requires running verification commands and confirming output before making success claims
- **Path:** `.subSkills/verification-before-completion/SKILL.md`

### behavioral-evals
- **Description:** Guidance for creating, running, fixing, and promoting behavioral evaluations for agent decision logic
- **Path:** `.subSkills/behavioral-evals/SKILL.md`

### webapp-testing
- **Description:** Testing local web applications using Python Playwright scripts, frontend automation, browser screenshots, console log capture, and server lifecycle management
- **Path:** `.subSkills/webapp-testing/SKILL.md`

## Routing Instructions

1. Read the user's request carefully.
2. Match their intent against the sub-skill descriptions above.
3. Read the matched sub-skill's SKILL.md at the given path and follow its instructions completely.
4. If the intent clearly spans multiple sub-skills, start with the primary match and note the others for follow-up.
5. If no specific sub-skill matches but the request is clearly in this domain, use the default sub-skill.
6. **Default sub-skill:** test-driven-development

## Disambiguation

- "write tests" / "add tests" / "TDD" → test-driven-development
- "debug" / "failing test" / "unexpected behavior" / "bug" → systematic-debugging
- "Jest" / "Vitest" / "Testing Library" / "mock" → javascript-testing-patterns
- "Playwright" / "Cypress" / "E2E" / "end-to-end" → e2e-testing-patterns
- "verify" / "before commit" / "check it works" / "done?" → verification-before-completion
- "eval" / "agent behavior" / "decision logic" / "prompt steering" → behavioral-evals
- "webapp testing" / "test local web app" / "Python Playwright" / "frontend automation" / "browser screenshot" → webapp-testing
