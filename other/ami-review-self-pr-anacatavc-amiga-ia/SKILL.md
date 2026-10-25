---
name: ami-review-self-pr
description: Use ONLY when reviewing YOUR OWN Pull Requests, local branches, or work-in-progress code before publishing. Instead of leaving comments, it acts as a stringent Senior Engineer to proactively find flaws and apply concrete code fixes locally. If reviewing a teammate's or another person's Pull Request to leave review comments, use ami-review-peer-pr instead.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: PR Self-Reviewer

When this skill is invoked, you act as a stringent Senior Engineer reviewing the user's own work. Unlike peer reviews, your primary goal is to find flaws and **fix them locally** before anyone else reviews the code.

## Workflow

1. **Context Identification, Validation & Dynamic Diffing:**
   - Ask the user which PR, branch, or specific commit they want you to review.
   - **CRITICAL AUTHORSHIP CHECK:** Identify if the PR or code belongs to another developer or teammate. This skill is exclusively for reviewing and directly fixing the user's OWN code. If the user is trying to review someone else's PR or give peer feedback to a teammate, **IMMEDIATELY STOP**, explain the difference between both skills, and recommend switching to **`ami-review-peer-pr`** (which focuses on interactive QA, criticality observations, and publishing GitHub review comments without altering local files). Offer to invoke `ami-review-peer-pr` right away.
   - If a PR URL or number is provided and belongs to the user, read the diff directly against its configured base branch (`baseRefName`).
   - If it's a local branch, determine its target base branch:
     - **Stacked PR Awareness:** Check if the local branch builds upon an intermediate layer in a **Stacked PRs** chain rather than branching directly from `main` or `master` (e.g., verifying `baseRefName` via GitHub CLI or stacking tools like `gh stack` / Graphite `gt`).
     - Analyze uncommitted changes or recent commits **strictly against its direct parent branch (`baseRefName`)**, preventing redundant review of lower layers in the stack.
   - **PR Description & Acceptance Criteria Ingestion:**
     - If inspecting an active PR, read its body description, title, and milestone via `gh pr view --json title,body,milestone`.
     - Map the proposed diff against the author's own checklist and acceptance criteria (e.g. `- [ ]` / `- [x]`) to ensure no promised item was left half-implemented.
     - Ingest repository architecture documents (`README.md`, `docs/adr/`, `docs/architecture/`) to ensure alignment with repository invariants.
   - **Pre-Review Existing Comments Gate (Comment Analysis Prerequisite):**
     - **Local Branch Bypass:** If reviewing a local branch or uncommitted code with no active remote PR (or if `gh pr view` returns non-zero / no pull request found), immediately bypass this gate and proceed directly to local diff analysis against base branch.
     - **Active PR Inspection:** When inspecting an active PR:
       ```bash
       gh pr view <target> --json comments,reviews
       ```
     - **Resolved & Outdated Comments Bypass:** If all existing comments are already marked resolved in GitHub, belong to outdated diff hunks from earlier commits, or were already processed and resolved in the current session/task, do not block the self-audit.
     - **Unresolved Feedback Gate:** If active, unresolved review comments or change requests from human reviewers remain unaddressed:
       - Inform the user and prioritize resolving external reviewer feedback first.
       - **Mandatory Delegation / Chaining:** Execute or guide through **`ami-analyze-pr-comments`** to extract and categorize observations (Blocking, Suggestions, Questions), apply local fixes, and draft professional responses tagging each reviewer with `@<username>` (strictly avoiding informal colloquialisms).
       - Once existing feedback is processed or acknowledged by the user, resume this skill to conduct the independent self-audit and blind-spot probes on the updated diff.
   - **Review Mode Selection:**
     - Support two operational review modes:
       - **Code Review Mode (Default):** Static analysis of logic, contracts, edge cases, error paths, and clean code standards. Fast and zero-execution overhead.
       - **Full Review Mode (Dynamic):** Static analysis combined with dynamic execution of local test suites and build/typecheck validation.
     - **Mode Negotiation UX:** Default to `Code Review Mode`. Inform the user that static analysis is being performed, and offer to switch to `Full Review Mode` if they want to run the test suite locally.

2. **Strict Self-Audit:**
   - Analyze the diff explicitly looking for:
     - Unfulfilled items from the PR description or missing acceptance criteria (`[Requirement Gap]`).
     - Logic gaps and unhandled edge cases.
     - Hardcoded values or magic numbers.
     - Missing error handling or logging.
     - Potential performance bottlenecks.
     - Missing or outdated tests.
   - **Validate every path, not just the happy path.** Tests and empirical validation (pilots, eval sets, manual checks) only prove what their inputs contain — they are blind to whatever the sample omits. So reason beyond them:
     - **All execution paths.** Trace *every* path that reaches the changed code — error, fallback, retry, empty/zero-result, early-return branches — not only the primary one. Bugs frequently live in the fallback/error path the happy-path tests never touch.
     - **Data-flow of each input.** For every value the new code consumes: where does it originate? Does it survive a re-request/retry? Which pre-existing validation runs *before* the change, and does it therefore only guard the original or first element (e.g. `results[0]`) and not the candidate the new code selects? The bug is often the interaction between new code and a guard that no longer covers it.
     - **Future callers & de-facto vs enforced gating.** Ask "who else could trigger this tomorrow?" A behavior that is safe today only because a single caller feeds it (one country, one flag, one payload shape) is *de-facto* gated, not enforced in code. If the change alters returned data/state, require explicit opt-in per case rather than silent activation-by-payload.

3. **Adversarial Blind-Spot Probe ([Blind-Spot Probe]):**
   - **Trigger Condition:** Execute this probe whenever Step 2 yields zero defects ("clean diff / LGTM") or only trivial styling/cosmetic issues (`[MINOR]`, `[NITPICK]`).
   - **Adversarial Objective:** Break complacency bias by presuming the diff harbors subtle, undetected defects. Actively probe five critical vulnerability dimensions:
     - **Dimension 1 (Concurrency & Asynchronous Timing):** Hunt for race conditions in concurrent execution, unawaited promises/tasks, missing cancellation token handling, stale closures in asynchronous callbacks or reactive hooks, and shared mutable state without synchronization.
     - **Dimension 2 (Boundary Extremes & Zero/Null Invariants):** Stress-test behavior with empty collections (`[]`), empty strings (`""`), zero (`0`), negative values, integer limits (`MAX_SAFE_INTEGER`, overflows), null/undefined states, and malformed structures. Verify whether optional chaining (`?.`) or fallback defaults silently hide broken upstream state.
     - **Dimension 3 (Silent Failures & Partial State Corruption):** Inspect `catch` blocks and fallback routines. Are exceptions swallowed without logging? Does a partial failure leave databases, caches, or state machines half-mutated without rollback or cleanup?
     - **Dimension 4 (Resource & Memory Lifecycles):** Inspect disposal of open handles, database connections, streams, timers, event listeners, and subscriptions. Ensure singletons or long-lived structures do not accumulate unbounded memory references.
     - **Dimension 5 (Malicious Payloads & Injection Surfaces):** Evaluate untrusted inputs against path traversal (`../`), prototype pollution, regular expression denial of service (ReDoS), and unexpected parameter combinations.
   - **Probe Outcomes:**
     - **Defects Detected:** Promote each uncovered issue to an actionable finding and formulate an exact local fix in Step 4.
     - **Zero Defects Detected:** Record a verified `[Blind-Spot Probe: Clean]` certification, confirming that all 5 adversarial dimensions were probed with zero defects found.

4. **Concrete Code Suggestions (KISS & DRY):**
   - Instead of leaving abstract comments (e.g., "Add error handling"), you MUST write the exact code snippet required to fix the issue.
   - **Simplicity First:** Propose the simplest professional fix that completely resolves the issue without introducing architectural bloat or excessive layers.
   - **Extract Duplication to Utilities:** If the fix involves logic repeated across files or methods, refactor and isolate the common routine into a centralized helper (`utils/` or `helpers/`) rather than copying code.
   - Present your findings as a numbered list. For each flaw, provide the proposed code modification.

5. **Dynamic Test Execution & Iterative Remediation Loop (Full Review Mode):**
   - When running in `Full Review Mode`:
     - **Stack-Agnostic Test Runner Discovery:** Inspect root manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.sln`, etc.) to determine the appropriate test command, or ask the user if multiple test suites exist.
     - **Safe Local Execution:** Run the test suite in the local workspace.
     - **Remediation Loop on Failure:**
       - If tests fail, diagnose the root cause immediately: isolate whether the defect is in the newly modified logic or in an outdated test expectation.
       - Formulate the exact fix.
       - Present the diagnosis and propose applying the fix locally:
         "[Test Failure Detected] Summary of failing tests. I have prepared a fix for the affected files. Would you like me to apply this fix and re-run the tests?"
       - If approved, apply the fix to the files and re-execute the test runner until all tests pass.

6. **Proactive Implementation (Code Review Mode):**
   - Ask the user: "Would you like me to apply these fixes directly to the files?"
   - If the user approves, use your file editing tools to apply the exact fixes locally.
   - Once applied, advise the user to amend their commit or push the new changes to their branch.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
