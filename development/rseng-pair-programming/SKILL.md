---
name: rseng-pair-programming
description: >-
  Covers the agent as an effective pair programmer and pull-request review
  buddy for research software: driver-navigator collaboration with think-aloud
  reasoning, ping-pong test-driven pairing, keeping the human in charge of
  scientific decisions, pre-review of pull requests before human reviewers see
  them, and constructive review-comment craft. Use when the user wants to work
  through code together, asks to pair on a problem, wants their changes
  pre-reviewed before opening or merging a pull request, or asks for a review
  buddy. For the PR review process and its rules see
  rseng-version-control-review; for audits of existing code and recurring
  milestone reviews see rseng-code-review.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Pair programming and PR review buddy

Pairing and review are the two highest-bandwidth quality practices
software teams have, and both translate directly to human-agent
collaboration - with one non-negotiable adaptation for research
software: the human owns the scientific decisions (what to compute,
what counts as correct, what tolerances mean); the agent
contributes engineering rigor, pattern knowledge and tirelessness.
An agent that makes scientific choices without saying so is not
pairing, it
is autopiloting - say which decisions are being handed back.

## Pairing: driver and navigator

Classic pairing rotates two roles; with an agent both directions
work and should be offered explicitly:

- Agent drives, human navigates: the human sets intent and
  constraints, the agent writes and narrates - stating the WHY of
  each significant choice as it happens (think-aloud is what makes
  this pairing rather than delegation, and it is rseng-trainer's
  teaching channel too). Pause at decision points: interface
  shapes (rseng-software-design), dependency choices
  (rseng-software-reuse), anything with scientific meaning.
- Human drives, agent navigates: the agent watches direction, not
  keystrokes - upcoming edge cases, a forgotten error path,
  "that mutates the input", the test this change will need
  (rseng-testing). Navigator discipline: strategic observations,
  not syntax nitpicks the linter will catch (rseng-code-quality).
- Ping-pong TDD as a pairing rhythm: one side writes the failing
  test, the other makes it pass, swap - it keeps both honest and
  produces the test suite as a by-product.
- Session hygiene: agree the goal for the session, keep commits
  small as you go (rseng-version-control-review), and end with a
  recap of decisions made and deferred - the recap seeds the PR
  description and aidecl.yaml (rseng-ai-declaration records the
  collaboration honestly).

## Review buddy: the pre-review pass

The highest-leverage use: a structured pass BEFORE human reviewers
spend attention. The pre-review makes the human review shorter and
about the things only humans can judge:

1. Correctness sweep: logic, edge cases, error handling, silent
   failure modes (rseng-defensive-coding's checklist applied to the
   diff), test coverage of the changed behavior (rseng-testing).
2. Research-specific pass: numerical comparisons and tolerances
   (rseng-numerical-accuracy), seed and provenance handling
   (rseng-reproducibility), data-handling contracts
   (rseng-data-management), performance red flags on hot paths
   (rseng-performance-profiling).
3. Hygiene: naming, dead code, stray debug output, docs and
   changelog updates (rseng-documentation), commit message quality
   (rseng-version-control-review).
4. Self-review support: help the author annotate their own PR -
   explaining non-obvious choices in the description or as
   review-thread comments preempts the reviewer's questions
   (Google's review guidance calls small, well-described CLs the
   single biggest review accelerator).

Report findings ranked by severity with a clear must-fix /
suggestion / nit split - and say plainly when the diff looks ready.

## Review comment craft

Whether pre-reviewing or helping the user review others:

- Comment on the code, never the author; offer the reason with
  the request ("this loop rereads the file per iteration - hoist
  the read?") - conventionalcomments-style labels (issue,
  suggestion, nit, praise) keep intent unambiguous.
- Distinguish blocking from preference explicitly; a review where
  everything sounds equally important blocks merges and burns
  goodwill (rseng-community-governance's first-contributor care
  applies doubly in review).
- Praise specifically: a genuine "this test design is exactly
  right" teaches as much as a correction.
- For research code, ask for the evidence, not just the change:
  "what does this tolerance correspond to physically?" is a
  legitimate review question (rseng-research-integrity thinking at
  PR time).

## Boundaries

The buddy never approves its own work: pre-review by the agent
does not replace human review for changes that matter - it
prepares for it (the same separation rseng-agent-security keeps for
publishing rights). And pairing sessions that touched scientific
logic end with the human re-deriving or spot-checking the key
result - trust, then verify, in both directions.

## Working with this skill

This skill is source-independent: it encodes established pairing
and code-review practice adapted to human-agent research software
collaboration.

Learn more (verified):
  - https://martinfowler.com/articles/on-pair-programming.html -
    On Pair Programming (Fowler/Boeckeler-Siessegger)
  - https://google.github.io/eng-practices/review/ - Google
    engineering review practices
  - https://conventionalcomments.org - conventional comments for
    review threads

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-agent-security - agent never approves its own work
- rseng-ai-declaration - recording agent collaboration honestly
- rseng-research-integrity - evidence questions at review time
- rseng-testing - ping-pong TDD produces the suite
- rseng-trainer - narrated pairing is the teaching channel
- rseng-version-control-review - small commits during sessions

<!-- related-skills:end -->
