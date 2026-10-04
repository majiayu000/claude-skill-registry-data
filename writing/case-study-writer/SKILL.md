---
name: case-study-writer
description: Write public-safe case studies from private projects, automations, agent workflows, internal tools, demos, or client-facing systems. Use when the user asks to turn project work into a case study, create client proof, write a sanitized GitHub case study, summarize an internal system publicly, document an automation without sharing source code, or explain a workflow while removing credentials, raw prompts, logs, databases, client data, local paths, and private implementation details.
---

# Case Study Writer

## Overview

Use this skill to turn private project work into public-safe proof: concise case studies that explain the problem, workflow, outcome, and adaptation value without exposing source code, credentials, raw prompts, logs, databases, client data, or private implementation details.

## Workflow

1. Clarify the public artifact target: GitHub case study, website system page, portfolio note, demo companion, or README section.
2. Read `references/case-study-template.md` and use its section order unless the destination already has a stronger house style.
3. Read `references/safety-boundary-examples.md` before writing the opening boundary note and final Safety Boundary section.
4. Extract only public-safe facts:
   - Problem the system solves.
   - What the system does at workflow level.
   - Human review and approval points.
   - General stack categories when useful.
   - Outcome stated qualitatively or with approved aggregate numbers.
   - What a similar client could adapt.
5. Rewrite private details into generic, reusable language. Do not copy raw notes, prompts, logs, exports, database rows, or source code.
6. Produce the case study in Markdown and include a short safety verdict: `BLOCK`, `REVIEW`, or `READY`.

## Case Study Shape

Use these sections by default:

- Title
- Boundary note
- Public page or demo links, if already approved and live
- Problem
- What The System Does
- Workflow
- Outcome
- What Can Be Adapted For Clients
- Safety Boundary

Keep the case study short enough to scan quickly. Prefer six to eight workflow steps and three to five client-adaptation bullets.

## Safety Rules

- Never include source code, private prompts, API keys, credentials, databases, logs, exports, client messages, account identifiers, local paths, or screenshots with private UI.
- Do not name clients, prospects, internal codenames, domains, or people unless the user confirms they are approved for public use.
- Use broad stack categories such as Python, SQLite, browser automation, queue dashboard, or LLM API instead of exact private architecture when details are not needed.
- Mention human approval explicitly when the system drafts, scores, publishes, sends, spends, or changes a system of record.
- If the user provides risky source material, return `BLOCK` with removal instructions before writing the publishable draft.

## Output Format

Return:

1. Safety verdict: `BLOCK`, `REVIEW`, or `READY`.
2. Short note on what was excluded or generalized.
3. The Markdown case study.
4. Remaining checks before publication.

If the user asks you to edit files, write the draft into the requested location or a sanitized staging folder, then recommend running a public-safety scan before commit.
