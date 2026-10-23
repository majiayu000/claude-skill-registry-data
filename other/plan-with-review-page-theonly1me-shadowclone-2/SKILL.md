---
name: plan-with-review-page
description: 'Use before a change that touches many files, needs many steps, or has open design choices. Also use it when the user says "plan this first", "what is your approach?", or "do not code yet". Explores the code read-only, asks one round of decisions with the recommended option first, and writes one plan. Builds a self-contained HTML review page from a template, and checks the page with a validator. Not for checking finished work (use `verify-and-review`).'
metadata:
  shadowclone-category: workflow
  shadowclone-section: workflow
  shadowclone-applies-when: before a change that has many steps or open design choices
---
# Plan With a Review Page

## Use when

A change touches many files, needs many steps, or has a design choice that belongs to the user. An approved plan stops work in the wrong direction. A small and clear change does not need this skill.

## Gates

1. Are you read-only until the user approves? Before approval, write only the plan file and the review page.
2. Did you read the code, the documents, and the history before you asked? Never ask what the code can answer.
3. Did you ask one round of at most 4 questions, each with 2 to 4 options and the recommended option first?
4. Is each risky behavior choice in that round, such as a skip, a block, a fallback, or a default?
5. Is there one plan file for this conversation, with each skipped step still visible and its reason?
6. Does the review page pass `scripts/validate-page.mjs` with 0 errors?

## Process

### Explore

1. Read the code that the request touches, and the instructions of the repository for that code.
2. Find the functions and patterns that the change can use again.

### Ask

1. List each open decision about scope, behavior, edge cases, data, release, and tests.
2. Ask the decisions in one round of at most 4 questions. Put the recommended option first, with one reason.
3. If an answer is not clear, ask again. Do not guess.

### Write

1. Put the plan at `/tmp/agent-artifacts/<repo>/<date>-<slug>/plan.md`. If the sandbox blocks `/tmp`, use the temporary folder of the agent.
2. Write the context, the decisions with their source, the approach, the files, the steps, and the verification commands.
3. Copy `assets/review-page.html` to the same folder as `index.html`. Edit only the JSON block with the id `plan`, and replace each value that starts with `TEMPLATE:`.
4. Add Mermaid source in `diagram` when the change has more than two parts. The page shows the source as text, and draws it when the pinned Mermaid file loads.
5. Run `node scripts/validate-page.mjs <page>`. If Node is not available, run the script with `bun`. Fix each error.
6. Give the user both paths, the approach, and the main risk. Wait for approval.

### Execute

1. Do the steps in order. After each step, update its status in the page and in the plan.
2. If a fact changes a decision, stop. Update the plan, and ask again.
3. Keep a step that you skip in the list, with the status `skipped` and the reason in its note.

## Example

**Situation:** The user asks for a sync command that updates installed skills. Some installed copies contain edits that the user made.
**Easy route:** Plan to replace each copy with the new version, and do not ask.
**Hidden cost:** The plan hides a choice that deletes the work of the user. The user finds the loss after the release.
**Best route:** Put the choice in the question round: keep each edited copy and list it (recommended), or replace it and save a backup. Record the answer in the plan.
**Evidence:** The decision table of the page shows "Edited copies: keep and list" with the source "user". The validator printed "validate-page: 0 errors in 1 file".

## Guardrails

- Approval covers only the steps in the plan. Ask before a step that the plan does not list.
- Never commit the plan or the review page to a repository.
- Keep the review page self-contained. Do not add scripts, styles, or fonts from the network.
- Do not open a decision again unless a new fact changes it.
- Keep the plan short enough to scan. Write the recommended approach, not each option that you considered.

## Completion

- The plan path and the review page path.
- The validator command and its result line.
- The question round, with the recommended option first in each question.
- Each step with its status, and each skipped step with its reason.
