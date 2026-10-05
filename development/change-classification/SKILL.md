---
name: change-classification
description: "Classify code changes as in-context, uncertain, or out-of-context using primary signals (branch diff, issue keywords, active tasks), secondary signals (directory proximity, test naming), and red-flag patterns (secrets, large binaries). Use when preparing commits or reviewing staged changes. This skill MUST be consulted because committing without classification is how out-of-context changes, secrets, and unintended modifications reach the repository."
allowed-tools: Bash, Read, Grep
context: fork
agent: Explore
---

# Change Classification

## Contract

Iron law: classify before committing — every changed file gets a classification; unclassified files are not staged. Invoked by `/flow:commit` (Phase 2 CLASSIFY, cross-check), `/flow:start` (CODE phase per-task gate, step 8), `/flow:address` (after fixes), `/flow:debug`, and `/flow:pr` (pre-flight). Returns a finding-first table — File | Classification | Signal | Notes — with each file marked in-context, uncertain, out-of-context, or RED FLAG, plus first-touch notes and proposed atomic commit groups. Permitted skips: none. Red-flag files are blocked regardless of context; uncertain or out-of-context files go to the user via a six-field AskUserQuestion escalation before any commit.

## Signals

Evaluate in order: red flags, primary, secondary, default → uncertain.

| Category | Signal | Result |
|----------|--------|--------|
| Red flag | `.env`, `.env.<environment>` (not `.env.example` / `.env.sample`, which are committable templates), `credentials*`, `*secret*`, key files | BLOCK — never commit |
| Red flag | `*.lock`, `package-lock.json`, files >1MB, auto-generated | WARN — verify intentional |
| Primary | In branch diff (`git diff --name-only $DEFAULT_BRANCH...HEAD`) | in-context |
| Primary | Path matches issue title/body keywords | in-context |
| Primary | Path referenced in a TaskList task, or same top-level directory as task files | in-context |
| Secondary | Sibling of an in-context file; test companion (`foo.rb` ↔ `foo_test.rb`) | lean in-context |
| Secondary | Config/dotfile/manifest in project root | uncertain |
| Secondary | Unrelated directory, no link to issue or tasks | out-of-context |

Boy Scout cleanup (lint, format, typo, obvious bug) in a file already in the branch diff is the `boy-scout` subtype of in-context and uses the `improve` commit type. Weights, thresholds, and commit-type inference: `references/classification-signals.md`.

### First-Touch Detection

A file is "first touch" when `git log $DEFAULT_BRANCH..HEAD -- file` is empty AND it has >50 lines added. Note it regardless of classification; it gets extra review attention.

## Output Format

```markdown
| File | Classification | Signal | Notes |
|------|---------------|--------|-------|
| src/auth/login.rb | in-context | matches issue keywords | |
| src/utils/format.rb | out-of-context | unrelated directory | first-touch |
| .env.local | RED FLAG | secret pattern | NEVER COMMIT |
```

## Out-of-Context Handling

Uncertain or out-of-context files never get staged silently. Present them with the six-field escalation (`references/escalation-format.md`) offering: (1) include as a separate `improve:`/`chore:` commit when the change is Boy Scout cleanup; (2) exclude — leave unstaged for a separate branch. During `/flow:start` CODE, resolve them at task time, not commit time. Automatic changes (lock files) still need classification.

## Atomic Commit Grouping

Group in-context files by logical unit (model + migration + test), then by type (feat separate from refactor), then by top-level directory. Each group gets one conventional commit with an accurate message.
