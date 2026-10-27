---
name: iru-review-github-issue
description: "/iru-review-github-issue <issue-number> or /iru-review-github-issue draft:<path> (draft file: first line '# <title>', rest the body); optional kind: functional|documentation overrides auto-detection. Reviews a GitHub issue against a quality checklist and returns classified findings (gap / pending / inconsistency / doubt), each with the exact question to ask, plus size signals hinting at /iru-split-github-issue. Read-only: on an existing issue it posts a comment or edits the body only after explicit confirmation. GitHub-only. Use before picking up an issue with /iru-issue, or as the review loop of /iru-draft-github-issue."
model: sonnet
---

# Review GitHub Issue

Review one GitHub issue (or a local draft of one) for gaps before anyone builds from it. This skill reports
findings; it never guesses an answer for the author, and it changes nothing on GitHub without explicit confirmation.

The checklist lives in `reference/issue-quality-checklist.md` (relative to this skill's directory); read it in full
before Step 3. Item ids below (C1, D1, DOC2, S1...) refer to that file.

## Step 1 — Resolve the input and fetch the issue

Parse the arguments:

- `<issue-number>` (digits, optionally prefixed with `#`): an existing issue.
- `draft:<path>`: a local Markdown file. The first line is `# <title>`; the rest is the body. Read it with `Read`.
  If the file does not exist or has no title line, tell the user and stop.
- optional `kind: functional|documentation`.
- Neither form: ask the user (plain text) which issue number or draft path to review, then continue.

For an existing issue only, confirm the repository is hosted on GitHub: use `git remote get-url origin` and check it
matches `github.com` or a GitHub Enterprise Server domain. If the host is something else, or there is no remote, say
this skill only reviews GitHub issues and stop. (A draft file needs no host check.)

Fetch an existing issue with:

```bash
gh issue view <n> --json number,title,body,labels,comments,state,url
```

If `gh` is missing or unauthenticated, search for GitHub MCP tools (`ToolSearch` "github issue") and read the same
fields. Comments matter: a later comment may correct or contradict the body. If the issue is closed, note it and
continue.

## Step 2 — Detect the kind

Use the `kind` argument if given. Otherwise:

- `documentation` if the issue has the `documentation` label, or the title/body is about writing pages, guides,
  diagrams or a bibliography rather than changing behaviour;
- `functional` otherwise (features, bugs, enhancements).

If it is genuinely ambiguous, choose `functional` and add a `doubt` finding asking which kind it is.

## Step 3 — Run the checklist

Apply the checklist items for the detected kind: Common, plus Development (functional) or Documentation
(documentation), plus Size signals.

- Verify technical details: for every file, class, method, endpoint or config key the issue names, check it exists
  with `Read`, `Glob` or `grep`, and that it behaves as described. Do not trust the text.
- Verify links: fetch every cited URL with `WebFetch` to confirm it resolves and is about the claimed subject.
  Resolve each `#N` reference with `gh issue view <n> --json number,title,state`.
- Prefer resolving a doubt from the codebase over asking, but record the finding anyway when the issue text itself
  is still incomplete; the author must update the issue.
- Never invent an answer. Every finding states what is wrong and the exact question the user would need to answer.
- Classify each finding as `gap`, `pending`, `inconsistency` or `doubt` using the definitions at the end of the
  checklist.

Verdict: `ready` when there are no findings; `needs-work` otherwise. Size signals alone never make a `needs-work`
verdict; they go in `Suggestions:`.

## Step 4 — Emit the result

Print exactly this block, with nothing between its lines, using one `- [...]` line per finding (or `- none` when
there are none) and `Suggestions: none` when there is nothing to suggest:

```
Verdict: ready | needs-work
Kind: functional | documentation
Findings:
- [gap|pending|inconsistency|doubt] <section> — <what is wrong> — Question: <exact question for the user>
Suggestions: <optional improvements that are not blockers>
```

Rules for the block:

- Replace the alternatives with the actual values (for example `Verdict: needs-work`); keep the field names,
  order and the ` — ` separators unchanged.
- **A caller skill receives this block unchanged.** When another skill (such as `iru-draft-github-issue` or
  `iru-split-github-issue`) invoked this one, return the block as the result with no reformatting, summarising or
  reordering, so the caller can parse it. Put any commentary after the block, never inside it.

## Step 5 — Offer follow-up actions (existing issues only)

Skip this step for `draft:<path>` input and when the verdict is `ready`. When this skill was invoked by another
skill, skip it as well (the caller applies resolutions).

Otherwise ask via `AskUserQuestion`:

- **Leave the issue untouched** (the findings above are the deliverable).
- **Post the findings as a comment** - write the block to a temp file and run `gh issue comment <n> --body-file <path>`.
- **Edit the issue body** - propose the revised body, show it, and on a second confirmation run
  `gh issue edit <n> --body-file <path>`. Only add content the user supplied; never fill gaps with guesses.

Execute only the option the user picked. If `gh` is unavailable, use GitHub MCP tools. Never comment or edit
without this confirmation.

## Step 6 — Report

Tell the user the verdict and the number of findings per class. For an existing issue say what, if anything, was
posted or edited. If size signals fired, remind them `/iru-split-github-issue <n>` can split the issue. When the
verdict is `ready`, say the issue can be picked up with `/iru-issue <n>`.

## Verification

Read-only calls were exercised against `albertoirurueta/ai-catalog`:

- `gh issue view <n> --json number,title,body,labels,comments,state,url` works; `labels` and `comments` are arrays
  (empty when none) and a closed issue still returns normally (`state: CLOSED`). With `--json id` the value is the
  GraphQL node id (a string like `I_kwDO...`), not the numeric REST id.
- A nonexistent issue fails with `GraphQL: Could not resolve to an issue or pull request with the number of <n>`
  (non-zero exit); treat it as "issue not found" and stop.
- `gh issue view <n> --json number,title,state` (used to resolve `#N` references) works.

The review itself never writes. The follow-up paths of Step 5 (`gh issue edit`, `gh issue comment`) are written from
the GitHub CLI documentation and are unverified, because no scratch repository was available.
