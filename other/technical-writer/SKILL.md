---
name: technical-writer
description: Write, structure, and maintain all forms of technical documentation — READMEs, API docs, runbooks, architecture decision records (ADRs), changelogs, onboarding guides, and user manuals. Use when the user asks to write or improve documentation, create a README, document an API, write a runbook, produce a changelog, or says "write the docs for this".
---

# Technical Writing

Approach every documentation task as a senior engineer who has joined a new team and could not figure out how to run the project from the existing docs. Write the documentation that would have saved you three hours on your first day.

Documentation is not a formality. It is the interface between your system and the humans who must use, operate, and extend it. Bad documentation costs real time — onboarding time, debugging time, support time. Good documentation compounds: every hour spent writing saves ten hours across the team.

---

## Technical Writing Principles

- **Write for the reader, not the writer.** You know how the system works. Your reader does not. Write for their starting point, not yours.
- **One document, one job.** A document that tries to be a tutorial, a reference, and a how-to guide at the same time fails at all three. Follow the Diataxis framework: every document is exactly one of — Tutorial, How-To, Reference, or Explanation.
- **Accurate beats elegant.** A beautifully written document that describes how the system used to work is worse than an ugly document that is correct. Accuracy first, prose second.
- **Show, don't just tell.** Code examples, command outputs, screenshots, and diagrams are worth more than prose descriptions of the same thing.
- **Docs that are hard to find are docs that do not exist.** Structure matters. A runbook buried five folders deep will not be found at 3am during an incident.
- **Update docs in the same PR as the code.** A doc updated a week after the code change is a doc that was wrong for a week. Stale documentation erodes trust faster than no documentation.

---

## The Diataxis Framework

Every piece of documentation you write falls into exactly one of these four types. Determine the type before writing.

| Type | Question it answers | Audience mindset | Example |
|------|--------------------|--------------------|---------|
| **Tutorial** | How do I learn this? | I am new and want to succeed at something | "Build your first API in 10 minutes" |
| **How-To** | How do I do X? | I know what I want; guide me | "How to deploy to production" |
| **Reference** | What is X? | I need to look up a specific detail | API endpoint reference, CLI flag reference |
| **Explanation** | Why does X work this way? | I want to understand the design | "Why we chose event-sourcing" |

**Never mix types in one document.** A tutorial that stops to explain architecture theory loses the learner. A reference that tries to be a tutorial confuses the expert looking up a flag.

---

## README Standard

The README is the front door of your project. It must be scannable in 30 seconds and answer: what is this, why would I care, and how do I get started.

### README Structure (in order)

```markdown
# Project Name

> One sentence description. What it does and for whom.

## What it does
2–4 sentences. The problem it solves. Why it exists.
Include a screenshot or demo GIF if this has a UI.

## Quick start
The shortest possible path from zero to working.
Must complete in under 5 minutes for a new developer.

```bash
# Installation
npm install -g mytool

# Run it
mytool --help
```

## Documentation
Link to full docs. Don't duplicate them here.

## Development
How to set up the development environment locally.
How to run tests. How to run linting.

## Contributing
How to submit a PR. Coding standards. Review process.

## License
SPDX identifier + link to LICENSE file.
```

**README rules:**
- The Quick Start must actually work — test it on a clean machine before publishing
- No jargon in the first paragraph — assume the reader has never heard of your project
- Screenshots/GIFs for UI projects — a picture replaces three paragraphs
- Badges only if they are green and meaningful (build status, coverage) — not a badge collection
- Keep it short: link out to full documentation rather than duplicating it in the README

---

## API Documentation Standard

### For REST APIs (OpenAPI / Swagger)

Every endpoint must document:
- **Summary** — one line describing what the endpoint does
- **Parameters** — every path, query, and header parameter with type, required/optional, and example
- **Request body** — full schema with all fields, types, required status, and realistic examples
- **Responses** — every status code that can be returned, with full response schema and examples
- **Authentication** — which auth scheme applies
- **Error codes** — every machine-readable error code the endpoint can return, with explanation

**Example endpoint documentation:**

```markdown
## POST /v1/users

Create a new user account.

**Authentication:** Bearer token required. Scope: `users:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ✅ | Full display name. Max 100 chars. |
| email | string | ✅ | Must be unique. Used for login. |
| role | enum | ❌ | `ADMIN` or `MEMBER`. Default: `MEMBER` |

**Example Request:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "ADMIN"
}
```

**Responses:**
- `201 Created` — User created successfully
- `400 VALIDATION_ERROR` — One or more fields failed validation
- `409 DUPLICATE_EMAIL` — An account with this email already exists
- `401 UNAUTHORIZED` — Invalid or missing token
```

---

## Runbook Standard

A runbook is a step-by-step guide for operating a system — deploying it, restarting it, responding to alerts. Runbooks are read under pressure, at odd hours, by engineers who did not write the system. Every runbook must be executable by someone who has never touched the system before.

### Runbook Structure

```markdown
# [System Name] — [Operation] Runbook

## Overview
What this runbook covers. When to use it. Time estimate.

## Prerequisites
- Access required (VPN, SSH keys, IAM roles)
- Tools required (kubectl, awscli, psql)
- Environment variables to set before starting

## Steps

### Step 1 — [Action Name]
**What this does:** One sentence explaining the action and its effect.

```bash
# Command with all flags explained
kubectl rollout restart deployment/api-service -n production
```

**Expected output:**
```
deployment.apps/api-service restarted
```

**If this fails:** What to check, common errors, where to look for more info.

### Step 2 — Verify health
```bash
kubectl get pods -n production -l app=api-service
```
**Expected:** All pods in `Running` state within 2 minutes.

## Rollback
Exact steps to undo everything this runbook did, in reverse order.

## Escalation
If this runbook fails to resolve the issue: who to contact, in what order.
```

**Runbook rules:**
- Every command must be copy-pasteable — no placeholders like `<your-cluster-name>` without telling the reader exactly where to find the value
- Show expected output — the reader must know whether the command succeeded
- Document the "if this fails" path — runbooks written only for the happy path fail in production
- Rollback section is mandatory — never write a runbook that is a one-way door

---

## Architecture Decision Record (ADR) Standard

An ADR captures why a significant technical decision was made. Without ADRs, institutional knowledge lives only in the heads of the engineers who were there.

```markdown
# ADR-0012: Use PostgreSQL for primary data store

**Date:** 2026-01-15
**Status:** Accepted
**Deciders:** [list of people]

## Context
What is the situation that forces a decision? What constraints exist?
(e.g., "We need a primary data store for the new billing service. We are a 
team of 4, deploying on AWS, and need strong ACID guarantees for financial data.")

## Decision
What are we doing?
(e.g., "We will use Amazon RDS for PostgreSQL as the primary data store.")

## Options Considered
| Option | Pros | Cons |
|--------|------|------|
| PostgreSQL (RDS) | ACID, team familiarity, strong tooling | Not as fast as DynamoDB for pure key-value |
| DynamoDB | Serverless, scales to any load | No joins, eventual consistency by default, new to the team |
| MySQL (RDS) | Familiar | No JSON operators, weaker window functions |

## Consequences
**Positive:** Strong consistency for financial data. Team expertise. Rich query language.
**Negative:** We need to manage connection pooling. Vertical scaling limit before sharding needed.
**Risks:** Schema migrations require care at scale. Addressed with: automated migration testing in CI.

## Revisit trigger
If write throughput exceeds 50K TPS or read latency P99 exceeds 100ms under load.
```

---

## Changelog Standard (Keep a Changelog format)

```markdown
# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).
Versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.1.0] — 2026-01-15

### Added
- User export to CSV endpoint (`GET /v1/users/export`)
- Webhook retry with exponential backoff (max 3 attempts)

### Changed
- `GET /v1/users` now returns `cursor`-based pagination (previously offset)
- Error responses now include `requestId` field

### Deprecated
- `offset` and `page` query parameters on `/v1/users` — use `cursor` instead. Will be removed in v3.0.

### Fixed
- Orders with zero-value line items no longer fail validation (#342)
- Concurrent user updates no longer produce duplicate audit log entries (#361)

### Security
- Upgraded `jsonwebtoken` to 9.0.2 (CVE-2022-23529)
```

**Changelog rules:**
- Write for the person upgrading your package — they need to know what breaks and what is new
- Every entry is one line, starting with the changed thing: "Webhook retry" not "We added webhook retry"
- Security entries get their own section — never bury a security fix in "Fixed"
- `[Unreleased]` section is always present and is the working draft for the next release

---

## Writing Style Guide

### Voice & Tone
- **Active voice:** "Run the command" not "The command should be run"
- **Second person:** "You will need" not "The developer will need"
- **Present tense:** "The function returns" not "The function will return"
- **Imperative in instructions:** "Click Save" not "You should click Save"

### Sentence Rules
- One idea per sentence. If a sentence has more than two clauses, split it.
- Maximum 25 words per sentence in instruction steps.
- Never use "simply", "just", "obviously", "clearly" — they make readers feel stupid when they struggle.
- Spell out acronyms on first use: "Application Programming Interface (API)".

### Code Blocks
- Every command in a code block — never inline in prose
- Language tag on every code block (```bash, ```json, ```python)
- Realistic values in examples — never `foo`, `bar`, `test`, or `123`
- Comments in code examples explain the non-obvious parts

### Headings
- Sentence case: "Getting started" not "Getting Started"
- Descriptive: "Configure the database connection" not "Configuration"
- Action verbs for how-to docs: "Deploy to production" not "Production deployment"

---

## Documentation Maintenance Checklist

Run this whenever code changes ship:

- [ ] README Quick Start tested on a clean environment — still works
- [ ] Any new endpoints added to the API reference with full schema and examples
- [ ] Any changed endpoint responses reflected in the API docs
- [ ] Any new environment variables added to `.env.example` with comments
- [ ] Changelog entry written for this release
- [ ] Any new runbook required for the operational change
- [ ] ADR written if a significant architectural decision was made
- [ ] No stale screenshots or outdated command examples
- [ ] All links in docs tested — no 404s

---

## Definition of Done — Documentation

Documentation is not done until:

- [ ] Document type identified (Tutorial / How-To / Reference / Explanation)
- [ ] Written for the reader's starting point, not the author's knowledge
- [ ] All code examples tested — they actually work
- [ ] All commands are copy-pasteable with no unexplained placeholders
- [ ] Realistic examples used throughout (no `foo`, `bar`, `test`)
- [ ] Spelling and grammar checked
- [ ] Reviewed by someone who was not involved in writing it (or the system it describes)
- [ ] Linked from the relevant entry point (README, docs index, API reference)
- [ ] Updated in the same PR as the code change that made it necessary
