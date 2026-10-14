---
name: qa-scope
description: >-
  Draft the QA scope and plain-language Given/When/Then test scenarios for a Jira ticket, built from the full ticket, the decisions made in its comments, and the actual code change read commit by commit (open PR, the ticket's merged PR, the branch against its base, or a named commit range). Saves a Markdown draft under docs/, iterates with the user, then posts it to the ticket as a new Jira comment only after explicit approval. Use on "QA scope for PROJ-123", "what should QA test", "write test scenarios for QA", "hand this ticket to QA", "prep the QA handoff", "gherkin scenarios for this ticket", or when a branch is ready for manual testing — even when the user only names the ticket or says "this branch".
argument-hint: "[ISSUE-KEY] [PR number | commit range]"
---

# Jira QA Scope

A manual QA engineer gets a ticket written for developers and a diff they cannot read. What they need is the gap between the two: what the ticket promised, what the team decided later in the comments, and what the code actually changed. This skill closes that gap in words a non-technical tester can act on.

## Assumptions

The skill works on these assumptions. Show them to the user in Step 1, so they can correct one before any work starts.

1. **Jira is the issue tracker.** This is a hard rule. With no working Jira connector, the skill stops in Step 1.
2. **The base branch is the repo's default branch** (`git symbolic-ref --short refs/remotes/origin/HEAD`). The user can name another one.
3. **Commit subjects and PR titles carry the Jira key** (`PROJ-123: Fix the thing.`). The skill uses the key to find the ticket's commits and merged PRs.
4. **The repo glossary can be anywhere.** The skill uses the glossary the user or the repo instructions name. If there is none, it uses `CONCEPTS.md` at the repo root when that file exists. If neither exists, it uses the ticket's own words.
5. **The domain is the repo's own.** The skill brings no product vocabulary. Every domain word comes from the glossary, the ticket or the code.

## Side effects

- Reads Jira through the connector found in Step 1.
- Runs read-only `git` (`fetch`, `log`, `show`, `diff`, `branch`) and read-only `gh pr view` / `gh pr diff` / `gh pr list` / `gh api`. `git fetch` updates remote-tracking refs only; it never touches the working tree.
- Writes one Markdown file under `docs/qa-scope/`. It never stages or commits it.
- Posts **one new comment** to the Jira ticket, and only after the user approves the final draft in this conversation. Never edits the description, existing comments, fields or status.

## Inputs

**Ticket key.** Match `[A-Za-z]+-\d+` and normalize to upper case. Accept a bare key or a browse URL (take the segment after `/browse/`). Use only two sources:

1. A key or URL in the user's message.
2. The current branch name — `feature/PROJ-123-some-description` gives `PROJ-123`. Use it without asking, but name it in Step 1 so the user can correct it.

Nothing found → ask for the key and stop. Never invent a key.

**Change.** What the code under test is, in this order:

1. A commit range or PR number the user named (`abc123..def456`, `#512`).
2. The open PR for the current branch: `gh pr view --json number,url,baseRefName,headRefName`.
3. The PR already merged for the ticket. Ask GitHub, not the commit subjects — a squash, a merge commit and a rebase each leave a different subject, and a rebase leaves no PR number at all:
   - `gh pr list --state merged --search "<KEY>" --json number,title,mergedAt`. PR titles carry the key (assumption 3), so this finds every merge type.
   - Nothing found → `git fetch origin <base>`, then `git log origin/<base> --grep="<KEY>" -i --format=%H`, and for a hit `gh api "repos/{owner}/{repo}/commits/<sha>/pulls" --jq '.[].number'`.
   - Several PRs mean the ticket shipped in parts. Take them all, oldest first.
4. The current branch against `origin/<base>`. Run `git fetch origin <base>` first — the local base branch is often stale, and a stale base puts other people's merged work into the scope.

Without `gh` or a GitHub remote, skip sources 2 and 3 and use the `git log --grep` fallback.

**Commits.** Read every change commit by commit, oldest first, and read each commit's full message (subject and body) together with its diff. The message says why the step was made and what it was meant to do; the diff alone does not. A body often names an edge case, a decision, or a fix to an earlier step that QA must test.

- **PR** (open or merged, any merge type): load it with `gh pr view <n> --json title,body,commits,files`. The PR body counts as a message too. `git fetch origin pull/<n>/head` makes squashed commits readable with `git show <sha>`.
- **Branch**: `git log --reverse origin/<base>..HEAD`, then `git show <sha>` for each.
- **Range**: `git log --reverse <range>`, then `git show <sha>` for each.

A squash merge folds the whole story into one diff. The single commits show the order of the work, fixes to earlier steps, and scope that was added and then taken out. A step that a later commit reverted is not in scope. When a message and its diff disagree, the diff is what ships — note the gap under _Open questions_.

## Workflow

### Step 1 — Check Jira, state the scope

Find a Jira connector before anything else, in this order:

1. A Jira MCP server in the session (for example the Atlassian MCP: `getAccessibleAtlassianResources`, then `getJiraIssue`).
2. A Jira CLI on the `PATH` (`jira`, `acli`).
3. A script or command the repo instructions name for Jira.

Prove it works by reading the ticket's summary. If no connector exists, or the one found asks for login or authorization, stop. Tell the user which connector you found and what it needs. Do not rebuild the ticket from guesses or from the branch name — every scenario would inherit the guess.

Then print the assumptions (from the _Assumptions_ section, with the real values) and the scope as YAML. The same YAML becomes the draft's frontmatter in Step 4.

```yaml
ticket: PROJ-123
ticket_source: branch name
change: PR #512
base: main
glossary: CONCEPTS.md
jira_connector: Atlassian MCP
```

### Step 2 — Load the ticket fully

Fetch the ticket with `summary`, `description`, `status`, `issuetype`, `parent`, `issuelinks` and **all comments**. Also fetch the parent when present, and linked issues only when their summary is not enough.

Then read the comments as a decision log. For each one, ask: does it add, drop, or change a requirement? Build a short internal list:

- **Decided** — scope added or changed in a comment (who, roughly when).
- **Dropped** — something the description asks for that a later comment took out.
- **Open** — a question asked and never answered.

Comments beat the description. A conflict between them goes into the draft under _Open questions_ — QA will test the wrong thing if two people believe different things.

### Step 3 — Read the change

Read the commits of the change, message with diff, as _Commits_ describes. Then get the combined file list (`gh pr diff --name-only`, or `git diff --name-only origin/<base>...HEAD`, or the named range) and read the changed files, not only the hunks, far enough to answer:

- Which **pages or flows** does a user reach this through? Find the routes in the router, the page files or the repo docs. Confirm each route before you write it.
- Which **roles** see different behaviour — an end user, an admin, a support agent, a guest?
- Which **states** does behaviour branch on — account status, permission, feature flag, a setting?
- What changed with **no screen** (webhook, scheduled job, export)? Name the nearest thing a tester can observe: an email, a field on a page, an admin view.
- Which **automated tests** (unit, integration, e2e, any kind) cover this behaviour? Look at the test files in the change and at existing tests for the changed code. You match them to scenarios in Step 4.

Compare this with Step 2. Note ticket items the diff does not touch and diff changes the ticket does not explain — both go to _Open questions_, not into scenarios. Do not audit the code; this is a test plan, not a review.

### Step 4 — Write the draft

Read the glossary from Step 1, if there is one. Every domain word in the draft must be a term defined there, capitalized as it is there, and never an alias the glossary retires. When a term has two meanings, say which one.

Write in simple English: invoke `/cortex-communication:simple-english` when it is available. If it is not, keep sentences under 20 words, one idea per sentence, active voice, no idioms.

Write for a manual tester who has never seen the code. No class names, endpoints, field names, file paths or vendor object ids — except in the _Automated tests_ block. A page is named by its relative URL plus what is on it.

Save to `docs/qa-scope/YYYY-MM-DD-<KEY>-qa-scope.md` with this shape:

```markdown
---
ticket: <KEY>
ticket_source: <user message / branch name>
ticket_status: <status>
change: <PR #n / branch / range>
base: <base branch>
glossary: <path / none>
---

# QA scope: <KEY> — <ticket summary>

## Summary

- **<flow or scenario name>** — <one to three sentences: what to test there and why, no steps>
- <up to 5 items>

---

## What changed

- <1–3 bullets: the behaviour a user sees now, in product words>

## Decisions from the ticket comments

- <decision, and what it means for testing>

## In scope

- <page or flow> — <what to check there>

## Out of scope

- <what looks related but did not change, so QA does not spend time on it>

## Test scenarios

### Scenario: <short name>

- **Given** <who the tester is and the account state, e.g. a signed-in user with the `{user_role}` role>
- **And** <extra setup, if needed>
- **When** <one action the tester takes, e.g. opens `/search?q={search_term}`>
- **Then** <what they must see>
- **And** <extra check, if needed>

**Automated tests:**

- `<path/from/git/root/to/file.spec.ts>`
  - <describe block name>
    - <test name exactly as in the code>

## Open questions

- <contradiction, unanswered comment, or ticket item the change does not cover>
```

Rules for the summary:

- It is the part a busy reader reads alone: a lead planning the test run, or a tester deciding where to start. They must see the whole scope in 30 seconds, without scrolling to the details.
- Write at most 5 items. Each item names one flow or scenario group in bold, then says in plain words what to test there. No Given/When/Then, no steps, no variables.
- Group scenarios to fit the limit. Several scenarios on one flow become one item. A regression check gets its own item only when it is a real risk.
- Order the items as the detailed part orders them: the main change first, regression checks last.
- Write the summary after the detailed part, so the two agree. The horizontal line (`---`) separates them.

Rules for scenarios:

- Write each step as a Markdown list item. Separate lines without list markers merge into one paragraph in Jira and in most Markdown viewers.
- Write each value the tester picks as a variable in backticks and curly brackets: `{user_role}`, `{search_term}`, `{user_email}`. Use snake_case names that say what goes there. The tester then knows which values are theirs to choose, and the same scenario works on every environment.
- One behaviour per scenario. The happy path first, then the states the change branches on, then what must **not** change (a regression check on the nearest neighbour flow).
- `Given` sets up an account state a tester can create or find. When the state is hard to reach (a suspended account, a specific role), say so — they may need an admin or a developer to set it up.
- `Then` is visible: text on a page, a button that appears or goes away, an email, a new row in a list. "The system updates the record" is not a check.
- Scenario count follows the change. A one-line fix earns two or three scenarios; do not pad. Stay high level — steps like "click Save" belong to QA.

Rules for _Automated tests_:

- List a test only when it checks the exact scenario: the same state, the same action and the same result. A test that touches the same code but checks something else is not coverage. A wrong link makes QA skip a check that nobody runs.
- Give the full file path from the git repo root (`git rev-parse --show-toplevel`), never a path relative to a package or the test folder. Several suites can share a spec name — `apps/web/src/search.spec.ts` and `apps/admin/src/search.spec.ts` — and only the full path tells them apart.
- Write the tests as a tree: the file path at the top, then one nested list level per `describe` block, then the test name. Copy each name exactly from the code. Tests in the same file share one file item, and tests in the same block share one block item, so the reader sees which tests belong together. The QA lead uses the list to decide what to run by hand; a developer uses it to find the test.
- No matching test → leave out the _Automated tests_ block for that scenario. This is the one place in the draft where file paths are allowed.

Leave out any section that is empty, except _Summary_ and _Test scenarios_.

### Step 5 — Review loop

Show the file path and the full draft in the conversation. Ask the user to review it. Apply their edits to the file and show the changed parts again. Repeat until they say it is good.

### Step 6 — Post to Jira

When the user approves the draft, ask one direct question: post it to `<KEY>` as a new comment? Post only on a clear yes to that question — approval of the text is not permission to post, and one yes covers one post.

Post through the connector from Step 1 as a new comment, never an edit of an existing one. With the Atlassian MCP, that is `addCommentToJiraIssue` or `addOrEditJiraIssueComment` without a `commentId`, with Markdown content. Send the file content without the frontmatter and the `# QA scope` title line — the ticket already shows the key and summary. No AI or tool attribution in the comment.

Report the comment link. If the post fails, show the error and keep the file; do not retry with a different format without asking.
