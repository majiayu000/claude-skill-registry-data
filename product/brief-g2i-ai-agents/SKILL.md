---
name: brief
description: Create a product brief document for a feature or project.
---

# Brief

## Invocation

This skill is performed in the `Product Owner` persona. If you are not already running as `Product Owner` (for example, the user invoked `/brief` directly), read `subagents/product-owner.md` and adopt its role guidance for the rest of this task. Stay in the current chat—do not delegate to a subagent.

## Objective

Create a product brief and save it to `docs/briefs/{project-name-slug}.md`.

## Instructions

1. Explain the brief creation process and ask for the feature or project name.
2. **Quick codebase grounding.** Once you have a working name, dispatch one research subagent with a prompt like: "Does anything resembling `{feature name}` already exist in this repo? Return a short structured summary with file paths and line ranges, current behavior, and obvious gaps. Do **not** paste file contents." Use the returned summary to sharpen scope and out-of-scope items in the questions below. Do not rabbit-hole on implementation; this pass exists only to keep the brief honest.
3. Ask questions one at a time to capture:
   - core problem or goal
   - target user or audience
   - non-negotiable requirements or constraints
   - out-of-scope items (cross-reference the discovery summary so you don't redefine something that already exists)
   - success metrics
   - business context or motivation
4. Read `templates/product-brief-template.md` and follow its structure.
5. Save the completed brief to `docs/briefs/{project-name-slug}.md`.
6. End with the brief path, the key decisions captured, and the recommended next step: `/spec`.
