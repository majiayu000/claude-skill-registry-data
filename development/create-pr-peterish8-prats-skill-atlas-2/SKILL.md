---
name: create-pr
description: Full end-to-end PR creation — branch setup, implementation, tests, commit, push, and GitHub PR
disable-model-invocation: true
argument-hint: <task description>
allowed-tools: Bash(git *) Bash(gh *) Bash(rg *) Bash(fd *)
---

## Task

$ARGUMENTS

---

## Instructions

Follow every step below in order. Do not skip any step. Do not proceed to the next step if the current one fails.

---

### Step 1 — sync with master

```
git checkout master
git pull origin master
```

If the working tree is dirty, stop and tell the user to stash or commit their changes first.

---

### Step 2 — pick a branch name

Look at the task description in `$ARGUMENTS` and derive a branch name that:

- is kebab-case: `fix-login-redirect`, `add-export-csv`, `update-rate-limit-config`
- starts with a short type prefix: `fix/`, `feat/`, `chore/`, `refactor/`, `docs/`
- is based on the actual work, not generic words
- contains no AI words: no "implement", no "enhance", no "leverage", no "utilize", no "streamline", no "optimize" unless that is literally what the task is
- is under 50 characters
- has no uppercase letters

Show the proposed branch name and ask the user to confirm before creating it.

Once confirmed:

```
git checkout -b <branch-name>
```

---

### Step 3 — understand the codebase before touching anything

Before writing a single line:

1. Read every file that will be modified
2. Grep for existing patterns: naming conventions, error handling style, import style, comment style
3. Look at existing comments in the files — match their tone, length, and placement exactly. If comments in the repo are terse one-liners, write terse one-liners. If they are absent, write none.
4. Understand the test setup: where tests live, how they are named, what testing library is used

---

### Step 4 — implement the task

Write the full implementation. Rules:

- No TODOs, no stubs, no placeholder logic
- Handle every error path with context
- Match the exact code style of surrounding code — indentation, spacing, naming, everything
- Comments must match the existing comment style in the repo. Do not add comments just to explain what the code does. Only add a comment when the why is non-obvious.
- No extra abstractions, no extra features beyond what was asked

---

### Step 5 — write or update tests

- Find where tests live for the code you changed
- Write tests that cover the new behavior and any edge cases
- Run the test suite and make sure everything passes before moving on
- If tests fail, fix the code (not the tests) unless the tests themselves are wrong

---

### Step 6 — pre-commit checks

Run whatever lint, type-check, or build commands the project uses. Check `package.json`, `Makefile`, `justfile`, or CI config to find them. Fix any issues before committing.

---

### Step 7 — commit

Stage only the files relevant to this task. Then commit with:

```
git commit -s -m "<one-line message>"
```

Commit message rules:
- One line only — no body, no bullet points
- Imperative mood: "add", "fix", "update", "remove" — not "added", "fixed", "updates"
- Under 72 characters
- No mention of Claude, AI, or any tool
- No period at the end
- The `-s` flag adds the DCO Signed-off-by line using the user's git config name and email — this is the only signoff, and it comes from the user's identity, not Claude

---

### Step 8 — push

```
git push -u origin <branch-name>
```

---

### Step 9 — review everything before opening the PR

Before running `gh pr create`, do a final check:

- `git diff master..HEAD` — confirm the diff is exactly what was intended, nothing extra
- Confirm tests pass
- Confirm no debug logs, no commented-out code, no leftover TODOs

If anything looks off, fix it and amend or add a follow-up commit before proceeding.

---

### Step 10 — write the PR

Open the PR with `gh pr create`. Follow every rule below exactly.

**Title rules:**
- Follow the org convention: check recent merged PRs with `gh pr list --state merged --limit 10` and match the format
- If no clear convention, use: `<type>: <short description>` — e.g. `fix: handle empty state in user list`
- Sentence case only — capitalize the first word and proper nouns, nothing else
- No trailing period
- No em dashes
- No Claude or AI mention

**Description rules — read carefully:**

- Written as a human writing to teammates, not as a bot summarizing a task
- Mild use of capitals: capitalize the first word of a sentence and proper nouns only
- No em dashes (—) anywhere — use commas, colons, or just restructure the sentence
- No mention of Claude, AI, "generated", "implemented", "leveraged", "utilized", or any AI-adjacent phrasing
- **No signoff of any kind in the PR description body** — no "Signed-off-by", no "Co-authored-by", no "Generated with" lines. The DCO signoff belongs only in the git commit (via `-s`), never in the PR description.
- Tone: direct, practical, like a developer who knows what they did and why
- Short paragraphs. No walls of text.
- Do not start with "This PR" or "This commit" — just describe what changed
- Do not use bullet points for everything — use prose where it reads naturally

**Description structure:**

Write it as plain prose. No fixed sections, no templates. Just describe what changed and why in a natural way, the same way you would explain it to a teammate over chat. If the approach needs a quick note, add it inline. Mention what was tested at the end in one or two sentences. That is all.

**Final command:**

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
<description>
EOF
)"
```

---

### Step 11 — done

Print the PR URL and a one-sentence summary of what was done.
