---
name: dev-factory
description: Orchestrate the full end-to-end development workflow (Research -> Design -> Code -> Test)
agent: dev-factory
argument-hint: "[feature-description]"
pass-full-context: true
pass-conversation-history: true
---

# /dev-factory

Build a new feature by running the full development lifecycle, culminating in the MVP test factory.

Target feature: $ARGUMENTS

## Usage

- `/dev-factory "add user profiles"` initiates the development workflow for the requested feature.

The workflow:
1. Researches the codebase context.
2. Drafts and reviews a technical design.
3. Writes tests and implementation code (TDD).
4. Invokes the `mvp-test-factory` for final E2E validation.
