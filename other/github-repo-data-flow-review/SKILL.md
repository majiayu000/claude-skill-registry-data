---
name: folder-data-flow-review
description: Review a GitHub repository or local codebase and build a basic data flow model that traces how data enters, moves through, and exits the system, with a function-level review at each step. Use when Codex needs to inspect application architecture, explain request or event paths, map trust boundaries, summarize important functions in a pipeline, or produce a lightweight security/design review of repo behavior.
---

# Folder Data Flow Review

## Overview

Use this skill to turn an unfamiliar folder or local codebase into a simple, evidence-based data flow model. Focus on the main execution path first, then explain the functions that participate in each stage of the flow.

Prefer a useful partial model over an exhaustive but fragile one. Make uncertainty explicit and label inferred edges clearly.

## Workflow

### 1. Establish the review scope

Identify the smallest meaningful slice of the folder or codebase to model before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- obvious entrypoints such as `main`, server bootstrap files, route registration, handlers, workers, jobs, CLI commands, or webhook consumers

If the folder or codebase is large, choose one of these scopes and say which one you chose:

- one request path
- one background job
- one subsystem or package
- one external integration

### 2. Discover the primary data path

Trace data from input to output. Look for:

- inbound sources: HTTP requests, CLI args, queue messages, cron jobs, webhooks, files, database reads
- transformation steps: parsing, validation, mapping, enrichment, business rules
- storage and retrieval: database queries, caches, object stores, files
- outbound effects: API calls, database writes, queue publishes, emails, logs, rendered responses

Prefer code search over guesswork. Follow concrete call sites, imports, routing tables, and framework wiring.

### 3. Build the data flow model

Represent the flow as a short ordered list or Mermaid diagram. For each step, capture:

- step name
- component or file
- key function or method names
- input data
- output data
- side effects
- trust boundary or external dependency

If the code does not fully prove a connection, mark it as `inferred`.

### 4. Review the functions at each step

For every important function in the flow, review the function instead of only naming it. Capture:

- file path
- function or method name
- role in the flow
- direct callers and important callees, if visible
- expected inputs
- produced outputs
- validation or sanitization performed
- state changes or side effects
- failure modes, assumptions, or security concerns

Keep the review proportional. Summarize helper functions briefly unless they materially affect the flow.

### 5. Surface architectural and security observations

Call out issues that change how the model should be trusted, especially:

- missing validation at boundaries
- hidden side effects
- shared mutable state
- surprising fan-out to multiple systems
- secrets or privileged operations
- error handling gaps
- implicit framework behavior that is easy to miss

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. High-level data flow
3. Step-by-step function review
4. Findings and open questions

If helpful, load `references/review-template.md` and reuse the templates there.

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for route definitions, handlers, service classes, queue consumers, ORM calls, and external API clients
- framework-specific files such as `routes`, `controllers`, `views`, `api`, `server`, `worker`, `jobs`, `handlers`, `consumers`, `middleware`

Prioritize these signals:

- files that connect external input to business logic
- functions that translate or validate data
- functions that persist, publish, or return data
- functions with many callers or many side effects

## Output Rules

Be explicit about evidence quality:

- say `confirmed` when the code directly shows the path
- say `inferred` when the path is likely but not fully wired in the inspected files
- say `not verified` when a dependency or generated layer is missing

Do not pretend to have complete coverage if the repository is large or partially unavailable.

When presenting the data flow, prefer naming real functions and files over generic boxes like "service layer".

## Example Requests

- Review this GitHub repository and build a basic data flow model for the login flow.
- Inspect this repo and explain how webhook payloads move through the system, including the functions involved at each step.
- Map the data flow for this background job and review the key functions for validation, side effects, and risks.
