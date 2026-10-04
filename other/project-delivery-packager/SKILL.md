---
name: project-delivery-packager
description: Experimental skill for preparing, organizing, or reviewing a software, data, AI, RAG, knowledge-base, API, deployment, client handoff, acceptance, or internal project delivery package. Use for producing README files, deployment steps, API docs, database/schema notes, test command lists, acceptance checklists, delivery inventories, version notes, demo scripts, troubleshooting guides, and sanitized handoff materials.
---

# Project Delivery Packager

Use this skill to turn a working project into a handoff-ready delivery package. The package should help another person deploy, test, understand, accept, and maintain the system without relying on private chat history.

Status: experimental. For the first real use on a new project type, produce a delivery plan or audit first and ask for confirmation before restructuring files, creating many docs, or packaging for external sharing.

## Core Workflow

1. Determine delivery type:
   - code package, deployment package, API service, data pipeline, RAG/knowledge-base system, model demo, acceptance package, or project archive.
   - identify recipient: client, teammate, teacher, ops engineer, reviewer, or future self.

2. Inspect existing artifacts:
   - README, scripts, configs, API routes, database/schema files, test files, sample data, generated outputs, docs, and deployment notes.
   - do not expose secrets, private endpoints, tokens, client-sensitive data, or raw private datasets.

3. Create the delivery map:
   - read `references/delivery-structure.md` before adding files.
   - separate source code, docs, examples, tests, deployment files, and generated outputs.

4. Write handoff docs:
   - README, quick start, environment variables, install steps, run commands, API reference, data contract, database notes, and troubleshooting.
   - read `references/doc-templates.md` when drafting docs.

5. Add acceptance materials:
   - test command list, smoke-test plan, sample input/output, known limitations, delivery inventory, and change log.
   - read `references/handoff-qa.md` before final delivery.

6. Verify:
   - run lightweight commands when feasible.
   - if tests cannot run, explain why and provide manual verification steps.

## Output Modes

- `delivery-plan`: outline the delivery folder and required docs without editing files.
- `build-delivery-pack`: create or update docs and package structure.
- `review-delivery-pack`: audit an existing delivery package for missing handoff material.
- `acceptance-pack`: produce acceptance checklist, test commands, sample cases, and delivery inventory.
- `sanitize-for-sharing`: identify private details that must be removed before public or client sharing.

## Default Delivery Folder

```text
delivery_package/
  README.md
  docs/
    deployment.md
    api.md
    data_contract.md
    database.md
    test_commands.md
    troubleshooting.md
  examples/
    sample_input/
    sample_output/
  scripts/
  tests/
  delivery_inventory.md
  acceptance_checklist.md
```

Use this shape when creating a standalone delivery package. For an existing repo, add only missing docs and avoid disruptive restructuring.

## Privacy And Client-Safety Rules

- Never include real API keys, cookies, passwords, internal tokens, private hostnames, or personal data.
- Replace sensitive values with placeholders such as `YOUR_API_KEY`, `HOSTNAME`, or `CLIENT_SAMPLE_ID`.
- Do not publish raw client data. Use sanitized samples or synthetic examples.
- When the user asks to upload, publish, or share a delivery package, stop and confirm the exact target and privacy boundary first.

## Final Response Contract

When delivering, report:

- package path or changed files;
- what a recipient should run first;
- what tests or smoke checks were performed;
- what remains manual or environment-dependent;
- any red flags about secrets, missing data, or unclear acceptance criteria.
