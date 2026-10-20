---
name: pr-review
description: Review a pull request and post ONE consolidated review comment that updates in place across re-reviews — each pass collapses the prior review into a `<details>` block instead of stacking new comments, so the thread stays clean and diffable. This is the reason to reach for it over `/code-review --comment` (which posts fresh inline threads every time). Wraps the built-in /code-review for analysis; adds modes (local print vs push), continuity (re-reads the last review), and history collapse. Use when asked to "review this PR", "/pr-review", "/pr-review push", "/pr-review local", "post a review", or "re-review after my changes".
---

# /pr-review — review a PR, locally or pushed

**Why this and not `/code-review --comment`:** that posts a fresh batch of inline threads
on every run, so a PR you review three times accumulates three layers of comments. This
skill maintains **one** consolidated comment that updates in place — each re-review
collapses the previous one into a `<details>` block and posts the new one, so the thread
stays clean and two reviews are easy to diff.

The actual code analysis is delegated to the built-in **`/code-review`** skill; on top of
it this skill adds:

- **one-comment-in-place** — a single marked comment, re-reviews update rather than stack,
- **modes** — `local` (default, print only) vs `push`,
- **continuity** — re-reading the previous review before writing a new one,
- **history** — collapsing the prior pushed review into a `<details>` block.

It is project-agnostic: it needs only `gh` authenticated against the PR's repo. Nothing
about a specific org, board, or notifier is baked in.

## Invocation & modes

```
/pr-review              → local mode (default)
/pr-review local        → local mode, explicit
/pr-review push         → push mode
/pr-review push <PR>    → push mode against a specific PR (number or URL)
```

- **local** (default): run the review and **print** it in the terminal. Makes **no**
  GitHub write of any kind. Use this to iterate before sharing. **Local mode does not
  require an open PR** — if the branch has none, review the uncommitted/unpushed working
  diff (`git diff` against the base branch) instead. This is the common pre-push loop: see
  the findings before you've opened a PR at all. Always say *which* diff you reviewed (PR
  #N, or the working diff against `<base>`).
- **push**: run the review and **post** it to the PR as a single marked comment, after
  collapsing the previous pushed review (see *Push*). If the branch has no open PR, stop and
  say so — there's nothing to post to.

If a PR is in scope, fetch its identity once and substitute the values **inline** into the
commands below — `OWNER/REPO`, `N` (number), `SHA`, `URL`, plus `CID` (a comment id from
Step 1) and the new review's `H`/`M`/`L` counts (from Step 3). These are literal
substitutions, not shell variables — state doesn't survive across separate tool calls.

```bash
gh repo view --json owner,name --jq '.owner.login+"/"+.name'
gh pr view --json number,headRefOid,url            # current branch's PR…
gh pr view <PR> --json number,headRefOid,url       # …or the explicit one for `push <PR>`
```

In the `push <PR>` case, pass that same `<PR>` to every `gh pr …` command below — the bare
`gh pr view`/`gh pr comment` target the current branch, which may not be the PR you mean.

## Step 1 — Re-read the previous review (always, both modes)

A re-review must build on the last one, not start cold. Find the previous review from
**either** source, preferring whichever is newer:

1. **In this conversation** — if you already posted/printed a pr-review earlier in this
   session, that text is the previous review.
2. **On the PR** — look for our marked review comment:

   ```bash
   me=$(gh api user -q .login)
   gh api "repos/$OWNER/$REPO/issues/$N/comments" --paginate \
     -q '.[] | select(.user.login=="'"$me"'" and (.body|test("<!-- pr-review")))
         | {id, body, marker:(.body|capture("<!-- pr-review(?<m>[^>]*)-->").m)}'
   ```

   The marker carries the prior counts and head sha, e.g.
   `<!-- pr-review high=3 med=5 low=2 sha=8d18493 -->`. This match returns **every** marked
   comment — including ones already collapsed (`collapsed=1`) by past runs. The "previous
   review" is the **newest non-collapsed** one (sort by comment `created_at`); the
   `collapsed=1` ones are history, and the marker — never comment position — is what
   identifies them.

**Stateless short-circuit (head sha unchanged).** If the previous review's marker `sha`
equals the PR's current head sha, **no commits have landed since that review** — a fresh
analysis would reproduce the same findings. Don't re-run `/code-review`: re-emit the prior
review verbatim (in push mode, that means the existing comment already stands — say so and
stop without posting a duplicate). This is the cheap, memory-free guard: the head sha, not
any remembered state, tells you whether re-review is even warranted. Only when the head sha
has moved do you proceed to Step 2.

Use the previous review to:

- **Not re-litigate** findings the diff has since addressed — check whether each prior
  finding's code still matches; if it's been fixed, mark it resolved rather than
  re-reporting it.
- **Carry forward** still-open findings so they keep stable identifiers/wording.
- **Keep the same format** (section order, severity labels, heading style) as the previous
  review so a reader can diff the two.

If there is no previous review anywhere, this is the first review — proceed fresh.

## Step 2 — Analyze

Run the built-in **`/code-review`** skill over the PR's diff to get the raw findings. Pick
the effort from the request (default the skill's normal level; honor "thorough"/"quick").
Use its local review path, **not** the `ultra` cloud mode — this skill is the cheap,
in-session loop. Do **not** pass `/code-review --comment`: this skill owns the posting and
formats one consolidated comment instead of inline threads.

Treat `/code-review`'s output as raw material — map whatever it returns into the severities
below; don't assume a fixed output shape, since it can change between versions.

**Fallback — don't hard-depend on the sub-skill.** If `/code-review` is unavailable, errors,
or its invocation has changed, don't abort: review the diff directly yourself
(`gh pr diff "$N"`, or `git diff <base>` for the working-diff case) against the same severity
rubric. The analysis is the goal; `/code-review` is just the preferred engine for it. Say in
the output which engine produced the findings.

Map each finding to a severity:

- **High** — correctness bug, data loss, security issue, or anything that can break at
  runtime.
- **Med** — notable but non-breaking: efficiency, missed reuse, fragile patterns, unhandled
  edge cases.
- **Low** — nits: style, naming, comments, minor cleanups.

Reconcile against Step 1: drop findings the diff already resolved, keep open ones, add new
ones.

## Step 3 — Format (stable across iterations)

Always render the review in this shape so successive reviews are comparable:

```markdown
## Review — <repo>#<n> @ <short-sha>

**Grade <G>/5 <emoji> — <H> High / <M> Med / <L> Low**

### 🔴 High
- **<title>** — `<file>:<line>` — <what & why it matters>

### 🟡 Med
- **<title>** — `<file>:<line>` — <what & why>

### ⚪ Low
- **<title>** — `<file>:<line>` — <what & why>

_No findings in a severity → write "None." under its heading. If the whole review is clean,
say "No issues found." and still show the count line (0 High / 0 Med / 0 Low)._
```

**Merge grade.** The header carries a `<G>/5` grade — a **deterministic function of the
counts** (and the nature of the High findings), so two reviews of the same diff always grade
the same. It's a reading aid that restates the counts, not a separate judgment call:

| Grade        | When                                                                  |
| ------------ | --------------------------------------------------------------------- |
| **5/5 🟢**   | Clean — 0 High / 0 Med / 0 Low.                                        |
| **4/5 🟢**   | Only Low findings.                                                    |
| **3/5 🟡**   | At least one Med, no High.                                            |
| **2/5 🔴**   | A single High that is neither a security nor a data-loss bug.        |
| **1/5 🔴**   | More than one High, or any High that is a security or data-loss bug. |

Pick `<emoji>` from the grade's row (🟢 for 4–5, 🟡 for 3, 🔴 for 1–2).

The **count portion** (`<H> High / <M> Med / <L> Low`) of that header is the compact summary
reused verbatim as the collapse header in Step 4; the grade is re-derived from the counts each
run, so it never needs to be stored in the marker.

## Step 4 — Emit

The `gh` commands below are **illustrative**, not prescriptive — use whatever GitHub access
you have (the `gh` CLI, a GitHub MCP server, the REST API directly). What's contractual is
the *effect*: list comments to find our marked review, PATCH the prior one into a collapsed
`<details>`, post the new one with a fresh marker. The marker — not the tool — is the source
of truth.

### local mode

Print the formatted review (Step 3) in the terminal. Stop. No GitHub write.

### push mode

1. **Collapse the previous pushed review**, if one exists on the PR (from Step 1's comment
   listing). Edit that comment so its whole body is wrapped in a `<details>` block whose
   `<summary>` is the prior review's compact count, and keep its marker intact:

   ```markdown
   <details><summary>Previous review — 3 High / 5 Med / 2 Low (collapsed)</summary>

   …original body…

   </details>
   <!-- pr-review high=3 med=5 low=2 sha=8d18493 collapsed=1 -->
   ```

   Pull the counts from the previous comment's marker (no re-parsing needed). Pipe the
   collapsed body to the PATCH over **stdin** via a **quoted** heredoc (`<<'EOF'`, with
   `-F body=@-`) so backticks, `$`, and `!` stay literal and no temp file is touched:

   ```bash
   gh api -X PATCH "repos/OWNER/REPO/issues/comments/CID" -F body=@- <<'EOF'
   <details><summary>Previous review — 3 High / 5 Med / 2 Low (collapsed)</summary>

   …original body…

   </details>
   <!-- pr-review high=3 med=5 low=2 sha=8d18493 collapsed=1 -->
   EOF
   ```

   Only collapse comments not already marked `collapsed=1`. If the previous review came
   only from conversation context (never pushed), there's nothing on the PR to collapse —
   skip this.

2. **Post the new review** as a fresh comment, with a marker carrying the new counts and
   head sha (7 chars) so the next run can collapse it. Pipe the same quoted heredoc to
   `--body-file -` (stdin) so the review markdown is posted verbatim, not shell-evaluated:

   ```bash
   gh pr comment N -R OWNER/REPO --body-file - <<'EOF'
   …formatted review (Step 3)…

   <!-- pr-review high=H med=M low=L sha=8d18493 -->
   EOF
   ```

   Print the comment URL. (Never inline the review via `--body "$body"`: it contains
   backticks and `$` and would be evaluated by the shell.)

At most one expanded pr-review comment lives on the PR at a time; older ones remain as
collapsed `<details>` so the history is preserved but quiet.

## Notes

- `push` needs write access to the PR's repo; `local` needs only read. Any authenticated
  GitHub path works (`gh`, MCP, REST).
- The marker (`<!-- pr-review … -->`) is the source of truth for finding our prior review
  and its counts — never rely on comment position or first/last ordering.
- **Prefer a cheap durable signal over remembered state.** The head sha (short-circuit in
  Step 1) and "does this finding's code still match" (reconciliation) both reconstruct what
  to do from the PR itself, so the review stays correct even with zero session memory of the
  prior run — a wiped context can't make it re-litigate a fixed finding or double-post an
  unchanged one.
- **Never interpolate review text into a shell string.** Review bodies always contain
  backticks (`` `<file>:<line>` ``) and may contain `$`/`!`, so any double-quoted
  `--body "$body"` or `-f body="…"` gets command-substituted or mangled. Always pipe a
  **quoted** heredoc (`<<'EOF'`, delimiter unindented) to stdin — `gh pr comment --body-file -`
  / `gh api -F body=@-` — so the text is read as data, with no temp file to clean up or
  permission-prompt on. Any equivalent path (MCP, REST with a JSON body) is fine too.
- `push` posts one **consolidated** comment, not inline threads. If you want inline
  per-line comments instead, use `/code-review --comment` directly.
- Severity mapping is a judgment call; when unsure between two levels, pick the lower one
  and say why in the finding.
