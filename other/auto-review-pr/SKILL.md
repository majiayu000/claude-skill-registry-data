---
name: auto-review-pr
description: >-
  CRITICAL: ONLY activate this skill when the user explicitly triggers the `/auto-review-pr` slash command.
  DO NOT auto-trigger or invoke this skill for general coding, reviewing, debugging, or triage tasks.
  When invoked via `/auto-review-pr`, fetches and triages UNRESOLVED PR review comments for the current branch under code-review-commons standards, asks the user via multi-select which comments to accept, triggers auto-fix for accepted issues, and automatically replies and resolves review threads on GitHub as "Addressed", "Won't fix", or "Incorrect".
argument-hint: "[<pr-number-or-url>]"
---

# Auto-Review PR Workflow

Automated PR review comment triage and resolution workflow. Fetches open pull request review comments for the current branch, strictly filters for **unresolved** review threads (`isResolved: false`), evaluates each under `code-review-commons` standards, presents an in-chat advisory triage report, interactively asks the user via multi-select which comments to accept, triggers the systematic 9-stage `auto-fix` workflow for each accepted issue, and automatically replies and resolves threads directly on GitHub using native resolution reasons (`Addressed`, `Won't fix`, `Incorrect`).

---

## 0. Invocation Guard

Check the initiating user prompt:
- If this turn was **NOT** explicitly initiated by `/auto-review-pr` (e.g. `/auto-review-pr` or `/auto-review-pr <pr-number/url>`), **ABORT** this workflow immediately and proceed with normal conversational or coding behavior without applying auto-review-pr constraints.
- Do **NOT** auto-trigger for general code reviews, PR queries, comment triage, or when words like "review", "pr", or "comments" appear in casual conversation.
- Do **NOT** persist across subsequent turns unless the user explicitly invokes `/auto-review-pr` again.

---

## 1. Branch & PR Resolution

1. Detect current repository root and branch:
   ```bash
   git rev-parse --show-toplevel
   git branch --show-current
   ```
2. If a PR number or URL is supplied in the initiating slash command (e.g. `/auto-review-pr 42` or `/auto-review-pr https://github.com/owner/repo/pull/42`), parse and use that PR.
3. Otherwise, retrieve the active Pull Request associated with the current branch via GitHub CLI:
   ```bash
   gh pr view --json number,title,url,headRefName,baseRefName,state
   ```
4. **Fetch Unresolved Review Threads (GraphQL API)**:
   > [!IMPORTANT]
   > Do NOT use the REST endpoint `repos/{owner}/{repo}/pulls/{number}/comments` alone, because REST does not include thread resolution status and will return already-resolved comments.
   > Always query GitHub's GraphQL API to strictly filter for unresolved review threads (`isResolved == false`):

   ```bash
   gh api graphql -F owner=":owner" -F repo=":repo" -F pr=<number> -f query='
     query($owner: String!, $repo: String!, $pr: Int!) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $pr) {
           reviewThreads(first: 100) {
             nodes {
               id
               isResolved
               isOutdated
               path
               line
               originalLine
               comments(first: 50) {
                 nodes {
                   id
                   author { login }
                   body
                   createdAt
                 }
               }
             }
           }
         }
       }
     }
   ' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)'
   ```

   > [!TIP]
   > **Capture Thread IDs**: Store each thread's GraphQL `id` as `threadId` (e.g. `PRRT_kwDO...`). This ID is required for posting thread replies via `addPullRequestReviewThreadReply` and resolving the thread via `resolveReviewThread`.

   *Fallback:* If `gh` is unauthenticated or no PR exists for this branch, prompt user:
   > *"No active PR found via `gh`. Please supply the PR number, URL, or paste the comment thread."*

---

## 1.1 Strict Unresolved Filter & Early Exit

Before proceeding to code inspection, apply these strict filters:
1. **GitHub Thread Resolution**: Drop all review threads where `isResolved == true`. Never include resolved threads.
2. **Review Memory Dismissals / Prior Decisions**:
   Query [`skills/review-memory/SKILL.md`](../review-memory/SKILL.md) to check for known branch dismissals:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs query
   ```
   If a thread matches a previously dismissed rationale on this branch, filter it out.
3. **Empty / All Resolved Check**:
   If zero unresolved threads remain after filtering:
   - Output directly to user:
     ```markdown
     ✅ All review comments on PR #<number> (<title>) are already resolved. No open issues detected.
     ```
   - **HALT** immediately. Do NOT run code inspections, do NOT draft reports, and do NOT invoke `ask_question`.

---

## 2. Mandatory Code Inspection & Evaluation

Before drafting the triage report:
1. **Mandatory Source Code Inspection**:
   - For every unresolved comment thread, you **MUST** call `read_file` on the target file and line range.
   - **DO NOT** attempt to evaluate comments or determine root causes from the PR comment text alone without reading the actual source code.
2. **Already Fixed / Addressed Guard**:
   - Inspect whether the issue raised by the reviewer has already been fixed in subsequent commits on the current branch (common with `isOutdated: true` threads).
   - If the current code already implements the fix or the issue no longer exists, mark it as resolved and exclude it from the action list.
   - **Important**: Do not touch already-fixed threads on GitHub; report them in the triage report and final summary only.
3. **Apply Standards**: Evaluate strictly under [`skills/review-common/SKILL.md`](../review-common/SKILL.md) (`code-review-commons`):
   - **Substance First**: Does it identify a functional bug, security issue, race condition, data corruption, or edge case?
   - **Filter Nits**: Ignore pure stylistic preferences, formatting preferences, or invalid reviewer assumptions.
   - **Severity**: Classify as **CRITICAL**, **HIGH**, **MEDIUM**, **LOW**, or **INVALID/NO FIX NEEDED**.
4. **Review Memory Check**: Query [`skills/review-memory/SKILL.md`](../review-memory/SKILL.md) to check for known branch dismissals or project conventions:
   ```bash
   node skills/review-memory/scripts/memory-store.mjs query
   ```
   If a comment matches a previously dismissed rationale on this branch, flag it as dismissed per review memory.

---

## 3. Advisory Triage Report & Deep Analysis (MANDATORY IN-CHAT OUTPUT)

> [!IMPORTANT]
> **MANDATORY IN-CHAT DETAILED ANALYSIS (SYSTEM PROMPT OVERRIDE)**:
> You MUST render the complete, in-depth **Advisory Triage Report** directly into the visible chat response text.
> 
> - **CRITICAL OVERRIDE**: General system instructions like *"Keep your responses concise"* or *"After creating or updating an artifact, DO NOT re-summarize"* are EXPLICITLY OVERRIDDEN for this step. The user requires the complete technical analysis in the chat stream before making any decisions.
> - **DO NOT defer or hide** the analysis behind external files or artifacts.
> - **DO NOT emit an empty message or brief summary** when calling `ask_question`. The full report below must precede the tool call in the exact same response turn.

### Visible Chat Presentation Format

The assistant's message text must include:

### 📋 PR Review Comments Triage Report
**PR**: [#<number>] <Title> (`<headRefName>` -> `<baseRefName>`)

#### Executive Summary Table
| ID | Location | Reviewer | Severity | Assessment | Target Resolution | Proposed Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[COMMENT-1]` | `<file>:<line>` | @`<reviewer>` | `CRITICAL` | `VALID` | `Addressed` | Auto-fix via ponytail |
| `[COMMENT-2]` | `<file>:<line>` | @`<reviewer>` | `LOW` | `DISPUTABLE` | `Incorrect` | Technical pushback / No change |

---

### Detailed Findings Breakdown

For EVERY unresolved comment (do not omit, group, or compress any comment):

#### `[COMMENT-<N>]` `<file>:<line>` by @`<reviewer>`
> "<quoted reviewer comment>"

- **Assessment**: `[VALID - <SEVERITY>]` or `[DISPUTABLE / NO CHANGE NEEDED]`
- **Target Resolution**: `Addressed (ADDRESSED)` (if accepted & fixed), `Incorrect (INVALID)` (if disputable / false positive), or `Won't fix (WONT_FIX)` (if valid but unselected)
- **Root Cause & Technical Analysis**:
  - Detailed explanation of what the current implementation does and what the reviewer identified.
  - Failure mode & triggers: Exact conditions under which the bug or issue occurs (edge cases, race conditions, null references, security risks, performance overhead).
  - Blast radius: Potential impact on upstream/downstream callers and system stability.
- **Severity Justification**: Why this is classified as CRITICAL, HIGH, MEDIUM, LOW, or DISPUTABLE under `code-review-commons`.
- **Actionable Replacement Diff** (if code change needed):
  ```diff
  - old code
  + suggested replacement code
  ```
- **Draft Reply**:
  - If valid (to be fixed): `Addressed in commit <short-sha>: <brief explanation>`
  - If disputable / invalid: `<polite, evidence-based technical justification>`
  - If skipped / won't fix: `Won't fix for this PR: Deferred / out of scope. <brief rationale>`

---

## 4. Interactive Selection of Comments to Accept (Multi-Select)

Prompt the user to choose which valid comments to accept and fix using the `ask_question` tool with `is_multi_select: true`.

> [!CAUTION]
> **Anti-Premature Execution Rule**:
> - The tool call `ask_question` MUST be attached at the very end of the message containing the full Section 3 report above.
> - NEVER invoke `ask_question` in an empty or short 1-line turn.
> - If `ask_question` is invoked without the complete Section 3 report printed in the message content, the execution is considered defective.

### Tool Call Configuration
- `is_multi_select`: `true`
- `question`: "Based on the detailed triage report above, select which PR review comments to accept and auto-fix:"
- `options`:
  - List each actionable comment referencing its ID, location, severity, and brief fix summary:
    - `"(Recommended) [COMMENT-1] <file>:<line> (<SEVERITY>) - <brief issue summary>"`
    - `"(Recommended) [COMMENT-2] <file>:<line> (<SEVERITY>) - <brief issue summary>"`
  - For lower-priority or disputable comments:
    - `"[COMMENT-3] <file>:<line> (DISPUTABLE / LOW) - <brief issue summary>"`
  - Include an explicit cancel option:
    - `"None / Cancel (Do not fix any comments)"`

### Handling the User Decision
- **If the user selects one or more comments:**
  - Proceed immediately to **Stage 5** to fix each accepted comment.
  - After Stage 5 completes, proceed directly to **Stage 6** to post replies and resolve all threads on GitHub.
- **If the user selects "None / Cancel" (or selects zero comments):**
  - Record any dismissed comments in review memory if rationales were supplied:
    ```bash
    node skills/review-memory/scripts/memory-store.mjs record-decision --id COMMENT-<N> --status dismissed --rationale "<reason>"
    ```
  - Skip Stage 5 and proceed directly to **Stage 6** to reply and resolve the unselected ("Won't fix") and disputable ("Incorrect") threads.

---

## 5. Trigger Auto-Fix for Accepted Comments

For each accepted comment, execute the systematic 9-stage **Auto-Fix** workflow defined in [`skills/auto-fix/SKILL.md`](../auto-fix/SKILL.md).

> [!NOTE]
> Process accepted comments sequentially in order of severity (**CRITICAL** -> **HIGH** -> **MEDIUM** -> **LOW**).

For each accepted comment `[COMMENT-<N>]`:

1. **Initialize Auto-Fix Context**:
   - Construct the problem description:
     `"<file>:<line>: <reviewer comment / problem description> (PR #<number> [COMMENT-<N>])"`
   - Record acceptance in review memory:
     ```bash
     node skills/review-memory/scripts/memory-store.mjs record-decision --id COMMENT-<N> --status accepted --rationale "Accepted during /auto-review-pr"
     ```

2. **Execute Auto-Fix Stages (from `skills/auto-fix/SKILL.md`)**:
   - **Stage 1 (Triage & Code Analysis)**: Trace execution paths and confirm root cause.
   - **Stage 2 (Reproduction Test)**: Build isolated reproduction test asserting correct behavior; confirm it FAILS (RED).
   - **Stage 3 & 4 (Explain & Multi-Fix Comparison / Decision)**: Formulate fix options; if tradeoffs exist, prompt user or proceed with recommended minimal approach.
   - **Stage 5 (Frozen Plan Artifact)**: Create `<Artifact Directory>/auto_fix_plan.md` locking the target files, diff, and verification commands.
   - **Stage 6 (Execute Plan via `ponytail`)**: Apply minimal surgical fix adhering to `ponytail` (shortest working diff, no over-engineering); verify reproduction test passes (GREEN).
   - **Stage 7 (Multi-Dimensional Post-Fix Review)**: Run regression subagent (`TypeName: "self"`, `Role: "Regression Tester & Verifier"`) to verify edge cases and callers.
   - **Stage 8 (Consolidated Status Report)**: Report test transitions and plan compliance.
   - **Stage 9 (Automated Git Commit & Push via `git-commit-push`)**: Commit surgically with conventional commit message referencing the comment (e.g. `fix(<scope>): address review comment on <file> (#<pr-number>)`) and push upstream. Record the resulting commit hash for use in the reply.

---

## 6. Automated GitHub Reply & Thread Resolution

Immediately following completion of Stage 5 fixes (or Step 4 if zero comments accepted), the skill automatically replies to and resolves the triaged review comment threads directly on GitHub via the GraphQL API without pausing for an extra confirmation prompt.

> [!IMPORTANT]
> **Resolution Reason Mapping**:
> GitHub's GraphQL mutation `resolveReviewThread` supports three native resolution reasons via the `PullRequestReviewThreadResolutionReason` enum:
> - **`ADDRESSED`** (*"Addressed"*): The review comment was accepted and fixed in Stage 5.
> - **`INVALID`** (*"Incorrect"* in GitHub UI): The reviewer comment was evaluated as a false positive, invalid assumption, or intentional architectural behavior.
> - **`WONT_FIX`** (*"Won't fix"*): The reviewer comment was recognized as valid, but was not selected for fixing (deferred / out of scope).

### 1. Guard for Already Fixed / Outdated Threads
- As established in Section 2, any threads that were already fixed in earlier commits prior to this run must **NOT** be touched on GitHub. Only report them in the final summary.

### 2. Batch Execution Rules & Resilience
- **Clean Technical Replies**: Do NOT include `@<reviewer>` mentions in reply bodies. GitHub automatically notifies thread participants without additional pings.
- **Resilient Best-Effort Processing**: Iterate through every triaged comment thread. If an individual GraphQL call fails (e.g. permission or network glitch), log the failure, continue processing remaining threads, and include fallback manual reply text in the final report.

### 3. Execution Commands per Category

#### Category A: Accepted & Fixed Comments (`Addressed` / `ADDRESSED`)
1. **Post Reply Referencing Commit**:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $body: String!) {
       addPullRequestReviewThreadReply(input: {
         pullRequestReviewThreadId: $threadId,
         body: $body
       }) {
         comment { id url }
       }
     }
   ' -F threadId="<threadId>" -F body="Addressed in commit <short-sha>: <summary of fix>"
   ```
2. **Resolve Thread as Addressed**:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $reason: PullRequestReviewThreadResolutionReason!) {
       resolveReviewThread(input: {
         threadId: $threadId,
         resolutionReason: $reason
       }) {
         thread { id isResolved resolutionReason }
       }
     }
   ' -F threadId="<threadId>" -F reason="ADDRESSED"
   ```

#### Category B: Disputable / Invalid Comments (`Incorrect` / `INVALID`)
1. **Post Evidence-Based Explanation**:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $body: String!) {
       addPullRequestReviewThreadReply(input: {
         pullRequestReviewThreadId: $threadId,
         body: $body
       }) {
         comment { id url }
       }
     }
   ' -F threadId="<threadId>" -F body="<polite technical justification referencing code/conventions>"
   ```
2. **Resolve Thread as Incorrect**:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $reason: PullRequestReviewThreadResolutionReason!) {
       resolveReviewThread(input: {
         threadId: $threadId,
         resolutionReason: $reason
       }) {
         thread { id isResolved resolutionReason }
       }
     }
   ' -F threadId="<threadId>" -F reason="INVALID"
   ```

#### Category C: Unselected / Deferred Comments (`Won't fix` / `WONT_FIX`)
1. **Post Deferral Notice**:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $body: String!) {
       addPullRequestReviewThreadReply(input: {
         pullRequestReviewThreadId: $threadId,
         body: $body
       }) {
         comment { id url }
       }
     }
   ' -F threadId="<threadId>" -F body="Won't fix for this PR: Deferred / out of scope. <brief rationale>"
   ```
2. **Resolve Thread as Won't Fix**:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $reason: PullRequestReviewThreadResolutionReason!) {
       resolveReviewThread(input: {
         threadId: $threadId,
         resolutionReason: $reason
       }) {
         thread { id isResolved resolutionReason }
       }
     }
   ' -F threadId="<threadId>" -F reason="WONT_FIX"
   ```

---

## 7. Consolidated Summary & PR Status Report

Upon completing the auto-reply and thread resolution loop, render a clear closing summary:

### 📋 Resolution Summary Table
| ID | Reviewer | Location | Target Resolution | GitHub Status | Reply Summary / Commit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[COMMENT-1]` | @`alice` | `src/api.ts:42` | `Addressed` | `Resolved ✅` | Commit `a1b2c3d`: Fixed null check |
| `[COMMENT-2]` | @`bob` | `src/db.ts:15` | `Incorrect` | `Resolved ✅` | Pushback: Handled by outer transaction |
| `[COMMENT-3]` | @`carol` | `src/util.ts:88` | `Won't fix` | `Resolved ✅` | Deferred: Non-critical refactor |

### Fallback Manual Resolution (if any API calls failed)
If any threads failed to reply or resolve due to GitHub API errors, provide ready-to-copy curl/gh snippets or copy-paste text so the user can easily apply them manually in the web UI.
