---
name: ami-analyze-pr-comments
description: Analyzes code review comments left by other developers on an active Pull Request, extracting pending tasks, suggestions, and offering to reply.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: PR Comment Analyzer

Optional input: a PR number or PR link. Without one, target the PR of the current branch.

When invoked, act as a **PR Comment Analyst**.

## Workflow

### 1. Identify and Prepare Target PR
- **Determine PR:** If `pr_number` or `pr_link` is provided, use it as the target. If not, use the GitHub CLI (e.g., `gh pr status`) to find the active PR for the current branch. If no PR is associated with the current branch, halt and ask the user to provide a PR number.
- **Checkout Branch:** Ensure the local workspace is on the correct branch for the target PR. If the current local branch (`git branch --show-current`) already matches the target PR branch, avoid redundant checkouts. If switching branches is required, verify that the working tree is clean first to prevent overwriting uncommitted work.
- **Verify Ownership:** Check the PR author. If the author does not appear to match the current user, warn them and ask for explicit confirmation before proceeding (since this skill is primarily designed for authors addressing their own reviews).

### 2. Extract Comments
- Use GitHub CLI or API to extract all review comments from the target PR, capturing comment content, location (file and diff hunk), thread IDs, resolution status, and the reviewer's username (`author.login`).
- **Bot Exclusion Invariant:** Automatically identify and ignore automated bot comments (e.g., accounts ending with `[bot]`, `codecov`, `vercel`, `github-actions`, `dependabot`). Do NOT draft replies to bots and NEVER tag a bot handle (`@...[bot]`). Treat automated bot reports strictly as read-only build/test signals if relevant, never as conversational review feedback.
- If there are no comments, let the user know and terminate the skill.

### 3. Categorize Feedback
- Group the comments into three distinct categories:
  - **Blocking:** Issues that must be resolved before merging.
  - **Suggestions:** Recommended improvements or alternatives.
  - **Questions:** Items requiring user clarification or input.

### 4. Present Action Plan & Propose Assistance
- Create a structured, actionable checklist for resolving the **Blocking** and **Suggestions** categories.
- **Analyze Suggestion Blast Radius:**
  - **Adjacent Caller Invariants:** Before proposing or applying a fix suggested by a reviewer (e.g., handling nulls or altering return types), analyze adjacent callers and functions to ensure the fix does not break unmentioned contracts.
  - **Uncommented Alternative Branches:** Check if reviewer comments on primary branches reveal issues that also impact error, fallback, or retry branches that were not explicitly cited.
- For **Questions**, clearly list the items needing the user's answers or input.
- Propose how you can assist with the resolution:
  - **Apply Code:** Offer to automatically apply any suggested code snippets or fixes to the local repository.
  - **Reply:** Offer to draft and submit replies to the comments.
- **Wait for the user's input**, approval of the proposed actions, and answers to any pending questions before proceeding.

### 5. Execute Actions & Stack Synchronization
- **Apply Changes:** Modify the local files to apply the approved code suggestions and fixes.
- **Stacked PR Restacking:** If the current branch is an intermediate layer in a **Stacked PRs** hierarchy (e.g., managed via `gh stack` or Graphite `gt`), remind the user (or offer) to execute the appropriate stack resync command (`gh stack sync` or `gt restack` / `gt sync`) after committing fixes, ensuring clean cascading rebases across dependent upper layers without introducing phantom conflicts.
- **Draft & Submit Replies:**
  - Draft replies based on the applied fixes and the user's answers.
  - **Mandatory Reviewer Tagging:** Explicitly tag the human reviewer being answered at the beginning of each reply using their GitHub handle (e.g., `@<username>`).
  - **Multi-Reviewer Thread Invariant:** If multiple human reviewers participated in the same thread, tag the original thread author and any reviewer whose specific suggestion was adopted (e.g., `@reviewerA @reviewerB`). Never tag bot accounts.
  - **Professional Tone Invariant (Anti-Colloquialism Policy):** All drafted replies MUST maintain a strictly professional, respectful, concise, and technical tone in any human language (English, Spanish, etc.). Strictly avoid informal colloquialisms, slang, casual greetings, or casual fillers (e.g., do not use terms like "bro", "crack", "amigo", "cheers mate", "onda", "genial crack", "ok compa", or similar informal phrasing), regardless of whether the reviewer phrased their comment informally.
  - **Language Alignment:** Reply in the same human language (e.g., Spanish if the review was conducted in Spanish, English if in English), while strictly maintaining the professional technical register specified above. Present the drafts for review before submitting. If the user approves the drafts, submit them directly using the GitHub CLI/API.
- **Track Progress:** Check off items from the action plan as they are completed.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
