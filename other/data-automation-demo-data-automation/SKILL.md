---
name: data-automation-demo-data-automation
description: Use when running data automation workflows for data-automation-demo.
---

# data-automation-demo-data-automation

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Data automation workflows for repeatable extraction, validation, and reporting.

## Workflow
- Locate source data, expected schema, and output format
- Run extraction or transformation on a small sample first
- Validate counts, types, and important edge cases
- Generate the report and document assumptions

## Commands
- install: `npm install`
- test: `npm test`
- data:validate: `npm run data:validate`
- data:extract: `npm run data:extract`
- data:report: `npm run data:report`

## Principles
- Preserve raw inputs before transforming data
- Validate schemas, row counts, and representative samples
- Separate generated reports from source data
