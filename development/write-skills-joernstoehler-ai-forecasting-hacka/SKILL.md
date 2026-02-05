---
name: write-skills
description: Create or update SKILL.md files for this repo. Use when authoring skills in .codex/skills/.
---

# Write Skills

## Required reference

- Read and follow the `skill-creator` skill. It is the canonical guidance for skill structure and workflow.
- The file path may change across Codex installations; locate it via the skills list rather than hardcoding a path.

## Repo policy

- Keep skill names hyphen-case, lowercase, <=64 chars, and avoid consecutive hyphens.
- Prefer small, focused SKILL.md bodies; move large details into references.
- Do not package into `.skill` files; this repo is the sole source of truth.
- Skills must describe the current `main` branch only (no “this used to be…” notes).

## Instruction budget

- Instruction count: we minimize the number of simultaneously explicit instructions that agents have to pay attention to. Studies show agents' performance degrades if they have to focus on 50 instructions at once. Tactics:
  - Grouping: we group instructions and facts that are useful for similar tasks together. We split knowledge that's not frequently needed together into separate files. This way agents can triage what to read based on their current task.
  - Default behavior: we don't write instructions unless we must change the agents' behavior. Their default behavior follows many best practices already, and superfluous instructions just waste our tight instruction budget.
  - Clarity: we write instructions in a clear, literally correct, actionable way to get the best out of our limited instruction budget.
  - Popular: we pick specific, professional, popular conventions, workflows, tools, patterns, terminology. Agents are familiar with these from training, need no further explanations, and know how to apply them without paying high attention. This reduces the impact on our instruction budget, though there always is some cost.

## Readability

- Readability: agents read files in chunks of <=250 lines and <=10kB, so we stay below these limits per file.
- Naming: we use expressive, conventional names for files, to help agents triage what to skip based on filenames alone.

## Approval

- Approval: any edits to the onboarding and reference materials must be reviewed and accepted by the project owner. Use `<!-- comments -->` to add inline commentary to explain edits.
