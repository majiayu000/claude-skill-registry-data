---
name: security-fix
description: >-
  Orchestrates test-driven fixes for Mattermost security tickets (Jira/Atlassian)
  with a Staff Security Engineer mindset: failing secure-behavior tests first,
  then implementation, then security review and edge-case loops, then opening a
  non-draft PR that follows `.github/PULL_REQUEST_TEMPLATE.md` when present, with
  a vague public description (no exploit detail). Use when the user invokes
  /security-fix:security-fix with a mattermost.atlassian.net browse URL, MM-*
  security work, backend permission or authorization bugs, or asks for this
  security TDD workflow.
disable-model-invocation: true
---

# Security fix (TDD, orchestrated)

## Role of the invoking agent

The main agent is **only an orchestrator**. It must **not** write application code, tests, or fixes itself. It delegates every substantive step to **separate** sub agents (one focused task per sub agent). It tracks phases, passes artifacts (ticket summary, file paths, test names, failures), and decides when to loop.

## Invocation

The user provides a Jira ticket URL, for example:

`/security-fix:security-fix https://mattermost.atlassian.net/browse/MM-68140`

Parse the issue key from the path (`MM-68140`). Fetch ticket details via **Atlassian MCP** (or the project's configured Jira integration) so sub agents get title, description, acceptance criteria, suggested remediation, and severity.

Typical scope: **server-side** issues (API handlers, stores, permission checks, role/team/channel scoping).

## Sub agent model

Delegate to sub agents using the **same model as the parent** (inherit model). Do not switch the parent to a different model for delegation unless the user explicitly asks.

## Phase 1 — Reproduction test only (Sub agent A: "failing secure behavior")

**Single responsibility:** Add **only** the test(s) that encode the **expected secure behavior** described in the ticket. Nothing else—no production code changes in this phase.

**Mindset:** Staff Security Engineer writing a **regression contract**. The test expresses what *must* be true for the system to be secure (deny when it should deny, omit when it should omit, etc.).

**Success criterion:** The new test(s) **fail** for the **right reason** (current vulnerable behavior), not compilation errors or flaky setup. If tests are green, the test does not yet reflect the bug—revise until red.

Deliverables back to orchestrator: list of new/changed test files, how to run them, exact failure messages.

## Phase 2 — Fix (Sub agent B: "implement to green")

**Single responsibility:** Analyze the ticket (and codebase) and implement a fix using the **suggested remediation** from Jira **or** a **better** approach if clearly safer or simpler without widening scope.

**Constraint:** The change **must** satisfy **all** tests added in Phase 1. Run the same tests; they must **pass**.

No new tests in this phase unless strictly required to compile or wire the fix (minimal).

Deliverables: summary of code paths touched, rationale if diverging from ticket remediation, confirmation Phase 1 tests pass.

## Phase 3 — Security review and edge cases (Sub agent C: "explore and harden")

**Single responsibility:** Treat Phase 2 as a **candidate** fix. Explore **adjacent and upstream/downstream** code paths (same handler patterns, similar endpoints, shared helpers, store methods) for **edge cases** the ticket did not spell out (e.g. other roles, system admins, guests, DM vs channel, deleted/archived resources, race-ish double calls).

If gaps are found:

1. Add **new** tests that encode secure behavior for those edge cases, with the **expectation they fail** against the current fix if the fix is incomplete.
2. Report back to the orchestrator: failing tests + analysis.

**Orchestrator action:** If Sub agent C added failing tests, spawn **Phase 2 again** (a new Sub agent B run—or same persona—implementing until **all** tests from Phase 1 **and** Phase 3 pass). Then optionally run Phase 3 once more until no new material gaps are found or the user stops the loop.

Sub agent C does **not** replace Phase 1's narrow reproduction; it **extends** coverage for defense in depth.

## Orchestrator checklist

1. Resolve ticket URL → issue key → fetch Jira content.
2. Spawn **Phase 1** sub agent; wait for failing secure-behavior tests only.
3. Spawn **Phase 2** sub agent; wait for green on Phase 1 tests.
4. Spawn **Phase 3** sub agent; collect edge-case test additions and failures.
5. If Phase 3 added failing tests → return to **Phase 2**; then re-run **Phase 3** as needed.
6. Summarize for the user: ticket, test files, production changes, residual risks, suggested **internal** commit message notes if helpful (without the main agent having authored the code).
7. **Open a pull request** (see below)—delegate to a sub agent if the repo uses scripted PR flows; the orchestrator ensures PR policy is followed.

## Pull request (after phases complete)

Once tests pass and the orchestrator has summarized work, **open a PR ready for review** (not a draft), unless the user explicitly asks otherwise.

**Repository PR template:** Before writing the PR body, check whether **`.github/PULL_REQUEST_TEMPLATE.md`** exists at the **root of the repo** where the change lives. If it exists, **use that file as the structure**: same sections and headings (e.g. Summary, Ticket Link, Screenshots, Release Note), fill placeholders, and remove instructional HTML comments so the submitted description is clean. If the file is missing, use a sensible minimal structure (title + short summary + ticket link) that still follows the **public description policy** below.

When a template includes **release notes** or admin-facing text (e.g. `release-note` blocks), apply the **same vagueness** as the Summary—do not describe the vulnerability in detail for end readers of release notes.

**Public description policy (open source):** Mattermost code is public. PR titles and bodies must **not** educate malicious readers about how to exploit the issue. Omit severity labels, exploit recipes, and precise vulnerable behavior from the **GitHub/GitLab** description. Keep that detail in **Jira** and private channels.

| Avoid (too specific) | Prefer (vague but accurate) |
|----------------------|------------------------------|
| Fix medium vulnerability where someone can read any message through `GET /api/v4/xyz` | Fix access issue with `GET /api/v4/xyz` |
| Prevent IDOR allowing arbitrary file download | Tighten authorization on file attachment endpoint |
| Patch SQL injection in search | Harden search query handling |

**Guidelines:**

- Describe **what area** changed (endpoint, feature, permission check) without explaining **how** it was wrong before.
- Linking the Jira ticket in the PR is fine for maintainers; the ticket holds full context.
- Commit messages on the branch should follow the same discipline when they will appear on the public default branch.
- For template sections that do not apply (e.g. **Screenshots** for a backend-only fix), follow what the template says—often a short "N/A" or "No UI changes" line rather than omitting the section, if the template expects every heading present.

## Anti-patterns (orchestrator)

- Implementing or editing app code or tests directly.
- Combining "write test and fix" in one sub agent for the initial fix (breaks TDD discipline for this workflow).
- Skipping Phase 3 for "small" fixes—scope review to the ticket, but still run the security pass.
- **Public PR text** that spells out exploitability, severity, or step-by-step abuse (use Jira for that).
- Opening security-fix PRs as **draft** by default when the intent is to ship review-ready work (use non-draft unless the user wants draft).
- Ignoring **`.github/PULL_REQUEST_TEMPLATE.md`** when that file exists in the target repo (structure PR content to match it).
