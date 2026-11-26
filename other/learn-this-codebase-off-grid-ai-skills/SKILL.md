---
name: learn-this-codebase
description: Get to know an unfamiliar codebase fast. Maps what it does, its modules, entry points, riskiest files, recent changes and the rules not to break, writes it to CODEBASE.md, then answers questions from that map with sources. Use when the user is new to a project or says "onboard me", "where do I start", "how does X work here", "where is the payment logic" or "give me an overview".
---

# Learn this codebase

## 1. Map it once
If `CODEBASE.md` exists and is less than a week behind `git log`, read it and skip to step 2. Otherwise build it:
- **What it is:** README, package manifests, entry points (main files, routes, app delegates, CLI bins).
- **Modules:** top-level folders and what each owns, in one line each. Note how they talk (imports, APIs, events, queues).
- **Data:** where state lives (databases, stores, files) and the main flows through it.
- **Hot spots:** files changed most in the last 90 days (`git log --since=90.days --name-only`), largest files, files with the most importers. These are the risky ones.
- **Tests:** where they are, how to run them, which modules have none.
- **Rules:** anything in `PLAN.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, lint configs and CI that you must not break.
- **Danger zones:** auth, payments, migrations, generated code, anything with "do not edit".

Write it to `CODEBASE.md`, short enough to read in five minutes. Note the commit it was built at.

## 2. Answer from the map, then the code
- Answer with file paths and line numbers. Read the code you cite; never answer about a specific file from memory.
- If the map doesn't cover it, search (`rg`), read, and add what you learned to `CODEBASE.md`.
- For "who knows this", use `git log --follow` and `git blame`.
- Say "not sure" with what you'd check, rather than guess.

## 3. Onboarding someone
Walk them through, in order: what it does, the main modules, the riskiest files and why, what changed in the last 30 days, the rules not to break, where tests are thin. End with "Which area do you want to dig into first?"

Before anyone edits, use `blast-radius`.
