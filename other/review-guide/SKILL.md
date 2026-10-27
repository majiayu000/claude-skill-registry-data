---
name: review-guide
description: >
  Computes a PR's Tier floor and unplanned-changes list with a bundled
  read-only script, then writes the PR's Tier line and Review guide (decisions
  not in the plan, files to read closely vs skim, what to check by hand). Use
  at /feature step 9 before opening the PR, or when the user asks for a review
  guide for the current branch.
license: MIT
compatibility: Requires git and a POSIX sh with awk.
metadata:
  author: André Cunha
---

# /review-guide

Gives a reviewer a short guide to where to look in a PR, split by trust: a
script computes the parts that must be trustworthy, and you write the parts
that need judgment. `/feature` step 9 calls this skill; it can also be run on
its own. It returns text for the caller to place. It never opens, edits or
comments on a PR.

## Input

- The default branch (`AGENTS.md` → *Commands*)
- The plan source, one of: the plan file's absolute path (the one `/feature`
  step 1d wrote, or `--from-plan` read); `--plan-reapproved` (a `--from-plan`
  run re-approved at step 2, so its saved plan is stale); or nothing (no plan
  file was saved). Run standalone with none given → ask for the path or "none"
- The approved plan text's **Tier** line and the session's context (deviations,
  decisions made while implementing)

## Steps

### 1. Run the script

`sh ${CLAUDE_SKILL_DIR}/review-guide.sh <default-branch> [<plan-file> | --plan-reapproved]`

- Any non-zero exit, any stderr, empty stdout, an unexpanded
  `${CLAUDE_SKILL_DIR}` or a missing script → STOP per `AGENTS.md` Rule 2;
  never guess a path or work around it
- A `not computed` reason other than `no plan file` or the re-approved one →
  tell the user before going on
- Syntax, exit codes and limits are in the script's header comment

### 2. Tier line

`**Tier:** <n> — <reason>`

- n = the higher of the plan's tier and the script's floor (2 when it lists
  sensitive paths). A user-set tier shows both values (`1 (set by user;
  derived 2) → 2`)
- The plan's tier is the approved plan text's `**Tier:**` line (inside
  `/feature`, the one in context). Standalone, read it from the given plan
  file; with no plan, n is the floor, marked "no plan tier"
- The reason names each sensitive area touched, as a fact
- Floor above the plan's tier → tell the user before the PR opens:
  `/feature` step 4's `opus` override may not have been applied, and step 9's
  second look applies

### 3. Review guide

For the reviewer; commit SHAs are allowed here.

- The script's stdout, verbatim, first
- **Decisions not in the plan**: one line each; every unplanned path
  accounted for, or "None"
- **Read closely** / **Skim**: paths, one line why each
- **Check by hand**: what to try in the running app, or "nothing: no UI or API
  surface"

## Output

The Tier line and the Review guide. The caller puts the Tier line in the PR
description and the guide at the top of the first comment. Run again, and
replace both, after any commit made once the PR is open.

## Rules

- Never alter, trim or contradict the script's output; an omission in your own
  parts must stay visible next to it
- Never put the plan file's absolute path in the output: the script prints the
  basename only
