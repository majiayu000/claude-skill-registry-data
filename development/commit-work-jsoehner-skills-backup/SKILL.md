---

name: commit-work

description: |

  "Create high-quality git commits: review/stage intended changes, split into logical commits, and write clear commit messages (including Conventional Commits). Use when the user asks to commit, craft a commit message, stage changes, or split work into multiple commits."



  "Create high-quality git commits: review/stage intended changes, split into logical commits, and write clear commit messages (including Conventional Commits). Use when the user asks to commit, craft a commit message, stage changes, or split work into multiple commits."



---



# Commit work



## Goal

Make commits that are easy to review and safe to ship:

- only intended changes are included

- commits are logically scoped (split when needed)

- commit messages describe what changed and why



## Inputs to ask for (if missing)

- Single commit or multiple commits? (If unsure: default to multiple small commits when there are unrelated changes.)

- Commit style: Conventional Commits are required.

- Any rules: max subject length, required scopes.



## Workflow (checklist)

1) Inspect the working tree before staging

   - `git status`

   - `git diff` (unstaged)

   - If many changes: `git diff --stat`

2) Decide commit boundaries (split if needed)

   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.

   - If changes are mixed in one file, plan to use patch staging.

3) Stage only what belongs in the next commit

   - Prefer patch staging for mixed changes: `git add -p`

   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`

4) Review what will actually be committed

   - `git diff --cached`

   - Sanity checks:

     - no secrets or tokens

     - no accidental debug logging

     - no unrelated formatting churn

5) Describe the staged change in 1-2 sentences (before writing the message)

   - "What changed?" + "Why?"

   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.

6) Write the commit message

   - Use Conventional Commits (required):

     - `type(scope): short summary`

     - blank line

     - body (what/why, not implementation diary)

     - footer (BREAKING CHANGE) if needed

   - Prefer an editor for multi-line messages: `git commit -v`

   - Use `references/commit-message-template.md` if helpful.

7) Run the smallest relevant verification

   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on.

8) Repeat for the next commit until the working tree is clean



## Deliverable

## Anti-Patterns & Safety Warnings



| Avoid | Why | Instead |

|-------|-----|---------|

| Vague Commit Messages | Context is lost, hard to track changes | Write clear what/why summaries |

| Committing Unfinished Code | Breaks build, creates noise | Use git stash or save in temporary branch |

| Unresolved Conflict Markers | Committing `<<<<<<<` corrupts code | Run search check before staging |

| Accidental Secrets | Credentials leak risk | Scan staged lines before commit |

| Raw Commit Lists | Cryptic output, ignores context | Summarize outcomes human-readably |



### Git Recovery & Verification Failures

If compilation or tests fail immediately after committing, run:

```bash

git reset HEAD~1

```

This moves the changes back to unstaged while preserving your code edits.



## References & Templates

- **MANDATORY**: If staging a complex feature with multi-paragraph messages, you **MUST** read [commit-message-template.md](references/commit-message-template.md) for layout guidelines.

- **Do NOT load** external commit guidelines if creating standard short bugfix messages.


