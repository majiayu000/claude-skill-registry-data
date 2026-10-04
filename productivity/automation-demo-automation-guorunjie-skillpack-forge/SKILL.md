---
name: automation-demo-automation
description: Use when running automation workflows for automation-demo.
---

# automation-demo-automation

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Automation-ready repo context for repeatable agent workflows.

## Workflow
- Inspect the current repo state and identify the automation entrypoint
- Confirm required inputs, credentials, and output paths
- Run the automation with a dry run or narrow scope first
- Verify outputs and document any skipped step

## Commands
- install: `npm install`
- test: `npm test`
- validate: `npm run validate`
- check: `npm run check`

## Principles
- Define the task inputs, outputs, and success criteria before running automation
- Keep generated changes reviewable and reversible
- Run the smallest reliable verification command before reporting completion
