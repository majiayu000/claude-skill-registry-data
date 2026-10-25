---
name: ami-review-peer-pr
description: Use ONLY when reviewing Pull Requests authored by OTHER PEOPLE (peer review). It focuses on generating code review observations with criticality levels and drafting review comments for teammates. If reviewing your OWN Pull Request or branch to apply local fixes before publishing, use ami-review-self-pr instead.
allowed-tools: Bash, Read, Grep
---

# Skill: PR Peer Reviewer

When invoked, act as a **PR Peer Reviewer**.

## Workflow

### 1. Context and Validation
- Identify the Pull Request to be reviewed.
- Verify that you are in the correct local repository. **CRITICAL:** You MUST check out the PR's branch locally using `gh pr checkout <number>` BEFORE performing any analysis. If you do not check out the PR's branch, you will analyze the wrong code.
- Identify the author of the PR. **CRITICAL:** The PR must belong to someone else. The author must NOT be the user currently invoking this skill. If you detect that the user is reviewing their own PR, branch, or code, **IMMEDIATELY STOP**, explain the difference between both skills, and recommend switching to **`ami-review-self-pr`** (which is explicitly designed to audit your own work and apply concrete fixes directly to your files instead of just leaving comments). Offer to execute `ami-review-self-pr` right away.

### 2. Understand the Goal, Ingest PR Body & Repository Context
- **PR Metadata & Acceptance Criteria Ingestion:**
  - Query and read the PR title, body description, labels, and milestone:
    ```bash
    gh pr view <number> --json title,body,labels,milestone
    ```
  - Methodically analyze the author's stated motivation, scope, and acceptance criteria (e.g., task checkboxes `- [ ]` / `- [x]`, specification lists).
  - Maintain an internal traceability checklist: verify whether the changes in the diff actually deliver every promised feature, constraint, or bug fix declared in the PR description. Any missing requirement must be flagged as a `[Requirement Gap]`.
- **Repository Documentation Ingestion:**
  - Ingest foundational project context from `README.md`, `docs/`, Architectural Decision Records (`docs/adr/`), and architecture specifications (`docs/architecture/`).
  - Validate that the diff respects established project conventions, design patterns, and architectural boundaries.

### 3. Review Mode Selection
- Support two distinct review operational modes:
  - **Code Review Mode (Default):** Static inspection of code changes, architecture, logic, error paths, and requirements fulfillment. Fast with zero execution overhead.
  - **Full Review Mode (Dynamic):** Complete static analysis plus dynamic test discovery, test suite execution, and build/typecheck validation.
- **Mode Negotiation UX:**
  - By default, select `Code Review Mode`.
  - If the user did not explicitly request `Full Review Mode` upon invocation, clearly inform the user:
    "[Mode: Code Review] Conducting static code and requirements analysis. To run dynamic repository tests and build validation, request Full Review Mode."

### 4. Dynamic Test Execution & Security Caution (Full Review Mode Only)
- When operating in `Full Review Mode`:
  - **Security Caution Gate (Untrusted Third-Party Code):**
    - Before executing dynamic tests or build commands on a peer's PR branch, assess security risks. Code from forks or external contributors could execute untrusted scripts or malicious install hooks.
    - Advise the user: "[Security Notice] Full Review executes code from peer branch '<branch>'. Ensure the PR source is trusted before running tests locally."
    - Verify package manifests for suspicious scripts prior to invocation.
  - **Stack-Agnostic Test Runner Discovery:**
    - Detect the project's test command by scanning root manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.sln`, `Makefile`). Prompt the user if ambiguous.
  - **Execution & Verdict Impact:**
    - Execute the test suite. If any test fails:
      - Mark the failure as a `[BLOCKER]` issue.
      - Capture the failing test names, assertion messages, and stack traces to include directly in the review report.
      - Recommend a verdict of "Request Changes" based on broken tests.

### 5. Inspect Existing Reviews & Discussions
- Before analyzing the code deeply or formulating any judgment, inspect all existing peer reviews, approvals, change requests, and discussion comments on the PR:
  - Query existing review statuses and conversation threads via GitHub CLI:
    ```bash
    gh pr view <number> --json reviews,comments,reviewRequests
    ```
  - Fetch detailed inline code comments and threads:
    ```bash
    gh api repos/:owner/:repo/pulls/<number>/comments
    ```
- **Analyze Existing Peer Feedback:**
  - What have other reviewers (engineers, codeowners, automated bots) already flagged, requested, approved, or questioned?
  - Has the PR author already responded, provided context, or committed fixes addressing those concerns?
  - Are there unresolved debates, pending architectural questions, or contentious design choices?
- **Deduplication & Consensus Rules:**
  - **Avoid Redundancy:** Do NOT duplicate comments or re-flag issues already raised by other reviewers, unless explicitly corroborating an unaddressed `[BLOCKER]` / `[CRITICAL]` flaw or offering a concrete missing code solution.
  - **Factor Consensus into Verdict:** Incorporate the state of prior discussions into your assessment (e.g., verify if changes requested in earlier reviews were genuinely resolved in the latest commits).

### 6. Clarification and Interactive QA
- Before analyzing the code deeply, determine if you fully understand the PR's intent and architectural context.
- If there is any ambiguity or missing context, **ASK THE USER**. Ask as many questions as needed to ensure you completely understand the context, domain, and objective of the PR before proceeding. Wait for their answers.

### 7. Strict Code Analysis & Stack-Aware Evaluation
- Once all questions are answered and the context is clear, review the PR diff.
- **Stacked PR Awareness:** Check if the PR is an intermediate or top layer in a **Stacked PRs** sequence (by checking `baseRefName`).
  - If reviewing multiple dependent PRs in a stack, advise reviewing from the bottom up (foundational base PR first) to maintain structural context.
  - Ensure diff analysis is isolated **exclusively against the PR's direct parent branch (`baseRefName`)**, evaluating only incremental layer deltas without compounding changes from earlier layers.
- Observe **ONLY** the code that is introduced (added) or removed (deleted) in the PR. Avoid commenting on pre-existing code that is out of scope, unless it directly interacts with the new changes in a problematic way.
- Analyze the changes for code quality, potential bugs, edge cases, security, performance, and best practices.
- **Validate every path, not just the happy path.** Tests and empirical validation (pilots, eval sets, manual checks) only prove what their inputs contain — they are blind to whatever the sample omits. So reason beyond them:
  - **All execution paths.** Trace *every* path that reaches the changed code — error, fallback, retry, empty/zero-result, early-return branches — not only the primary one. Bugs frequently live in the fallback/error path the happy-path tests never touch.
  - **Data-flow of each input.** For every value the new code consumes: where does it originate? Does it survive a re-request/retry? Which pre-existing validation runs *before* the change, and does it therefore only guard the original or first element (e.g. `results[0]`) and not the candidate the new code selects? The bug is often the interaction between new code and a guard that no longer covers it.
  - **Future callers & de-facto vs enforced gating.** Ask "who else could trigger this tomorrow?" A behavior that is safe today only because a single caller feeds it (one country, one flag, one payload shape) is *de-facto* gated, not enforced in code. If the change alters returned data/state, require explicit opt-in per case rather than silent activation-by-payload.

### 8. Adversarial Falsification Audit ([Falsification Check])
- **Trigger Condition:** Execute this audit whenever preliminary analysis identifies any candidate `[BLOCKER]`, `[CRITICAL]`, or `[MAJOR]` issue.
- **Adversarial Objective:** Actively attempt to disprove and falsify the severity of your own finding before presenting it to the user or author. Assume the null hypothesis: *"This suspected issue cannot manifest in production or is already mitigated by surrounding architecture."*
- **Falsification Probes:**
  - **Upstream Perimeter & Middleware Guards:** Check route definitions, gateway middleware, DTO validation schemas (e.g., Zod, Marshmallow, Pydantic, FluentValidation), and input sanitizers. Does an upstream guard prevent the pathological input from ever reaching the modified code?
  - **Type System Enforcements:** Inspect compiler settings and type declarations. Do strict null checks, sum types, or non-nullable contracts prevent the hypothesized invalid state at compile time?
  - **Framework & Runtime Invariants:** Does the runtime framework provide automatic isolation, SQL parameterization, transaction rollbacks, or lifecycle cleanup that neutralizes the concern?
  - **Database & Storage Constraints:** Inspect data schemas. Do `NOT NULL` constraints, unique indexes, foreign key cascades, or ACID guarantees prevent the anomalous data condition?
  - **Caller Topology & Call-Site Constraints:** Is the modified routine private or internal? Verify all concrete call sites across the codebase: does any current or anticipated caller actually supply unvalidated arguments?
- **Adjudication Rules:**
  - **Fully Disproved:** If upstream guards, type invariants, or caller constraints make the defect impossible in practice, **DISCARD** the observation entirely. Do not escalate non-issues.
  - **Partially Mitigated:** If the issue can only trigger under contrived or non-standard conditions due to existing upstream protections, **DOWNGRADE** the severity to `[MINOR]` or `[NITPICK]`, explicitly noting the partial guard in place.
  - **Withstood Falsification:** If the defect survives active falsification, retain the `[BLOCKER]`, `[CRITICAL]`, or `[MAJOR]` rating. In the observation, explicitly append a `[Falsification Check: Verified]` note explaining why upstream guards and framework invariants fail to mitigate the risk.

### 9. Generate Quality Observations and Recommendation
- Output a comprehensive list of observations based on your analysis.
- For every observation, you MUST indicate its criticality level (e.g., `[BLOCKER]`, `[CRITICAL]`, `[MAJOR]`, `[MINOR]`, `[NITPICK]`).
- Include any `[Requirement Gap]` observations if the PR diff fails to meet criteria described in the PR description.
- Include any `[Test Failure]` observations if running in Full Review Mode and dynamic tests failed.
- Include `[Falsification Check: Verified]` evidence for all surviving high-severity findings, and summarize any discarded or downgraded observations.
- Provide clear reasoning for your observations and, when applicable, suggest code snippets or alternative approaches to resolve the issue.
- **Recommendation:** Based on your findings, clearly recommend to the user what the final verdict should be ("Approve", "Comment", or "Request Changes") and justify your recommendation.

### 10. Publishing the Review
- Wait for the user to confirm their final decision regarding the verdict.
- **CRITICAL:** Before preparing the final comments, **ASK THE USER** to confirm the desired **tone** (e.g., formal, friendly, constructive) and **language** (e.g., English, Spanish) for the actual PR comments.
- Once they decide on the verdict, tone, and language, **OFFER** to automatically upload the review directly to the PR (e.g., using GitHub CLI `gh pr review`).
- Give them the option to publish the issues found as **inline comments** on the specific lines of code, and/or leave a **global comment** detailing the verdict.

#### Pre-Publish Freshness Gate (Concurrency & Drift Check)
- **CRITICAL:** Before executing any remote review command (`gh pr review` or posting comments), perform an immediate live freshness check to prevent posting outdated feedback:
  1. **Check for Code Drift / New Commits:**
     - Query the remote PR head commit and fetch remote updates:
       ```bash
       gh pr view <number> --json headRefOid,updatedAt
       git fetch origin <pr-branch>
       ```
     - Compare the latest remote `headRefOid` against the commit SHA analyzed locally.
     - If new commits or a force-push occurred while drafting the review:
       - **HALT immediately.** Inform the user: "New commits have been pushed by the author since the review began (HEAD moved to `<new-sha>`)."
       - Diff the newly introduced changes against the analyzed commit:
         ```bash
         git diff <analyzed-sha>..<new-sha>
         ```
       - Check if the author's new commits already resolved your drafted observations, or introduced new defects.
       - Update your drafted comments accordingly and re-confirm the verdict with the user before publishing.
  2. **Check for Concurrent Peer Feedback / New Comments:**
     - Re-query latest PR reviews and comments:
       ```bash
       gh pr view <number> --json reviews,comments
       ```
     - Check if any new reviews (approvals, change requests) or comments were posted by teammates while your review was being prepared.
     - If new peer feedback arrived:
       - Inform the user of the new comments or status changes.
       - Check if the new feedback overlaps with or contradicts your drafted review.
       - Adjust your drafted comments with the user's approval.
  3. **Publish Execution:**
     - Only after verifying code freshness and confirming there are no conflicting concurrent updates, draft the comments according to the chosen tone and language, and execute the commands to publish the review.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
