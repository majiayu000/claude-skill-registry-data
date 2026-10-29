---
name: docs-review
description: |
  Review a docs page or a docs change-set under content/ against the docs
  rubric: run the mechanical gate (docsnip check, which includes docsnip
  prose, and check-nav), then score six facets (facts and evidence, reader
  altitude, concrete procedures, structure through the model, style,
  citability) and report ranked Blocker / Should-fix / Suggestion findings
  with exact lines. Reports only, never edits. Use when asked to review docs
  changes or a docs PR, or check whether a page is ready for reviewers.
  `lite` runs the gate and facets (a)–(c) only.
argument-hint: 'Optional: page or folder path, PR number, or nothing for git-changed content; optional lite'
---

# docs-review: rubric review for docs pages

The criteria live in
[`docs/design/docs-quality.md`](../../../docs/design/docs-quality.md). This
skill applies them. [`references/checks.md`](references/checks.md) lists what
each facet's reviewer inspects, and which mechanical checks are already
`docsnip`'s job, so don't spend reads re-deriving them.

The review is advisory. It produces scores and ranked findings. Approval and
`status: ready` happen in the review app
([ADR-0002](../../../docs/decisions/ADR-0002-git-ready-is-release.md)). This
skill doesn't touch the page or its status.

## 1. Resolve the scope

- **A path:** that page (or every page under the folder), whole-file.
- **A PR:** `gh pr diff <n> --name-only`, then read each file at the PR head
  (`git show <sha>:<path>`). Never check out or switch branches during a review.
- **Nothing:** `git status --short content/` plus `git diff --name-only main...HEAD -- content/`.

In scope: pages (`content/**/*.md` except README), their `snippets/` (as
evidence, not style), `nav.yml`, `architecture/journeys/`, `compatibility.yml`, and `release.yml`
changes. A renamed page is reviewed at its new path. Record the old path,
because `nav.yml` and inbound links must follow it.

## 2. Run the gate

```bash
uv run docsnip check
node site/scripts/check-nav.mjs
uv run docsnip prose --json
```

A failure here is a **Blocker**. Report it verbatim with the file and line.
Prose warnings become **Should-fix** on changed lines (and Suggestion
otherwise, per step 4). Don't re-flag anything `docsnip prose` already
reported.

Find the page's plan, the yardstick for facets (b) and (d). Use the first of
these that exists: the caller's placement plan; the `## Plan` section of the PR
that drafted it (`gh pr list --head docs/<project>-<slug> --state all --json body
--limit 1`); or its backlog row in `docs/design/<project>-documentation-plan.md`
or its content request. Without any of them, judge the page against its
bucket and say so.

Then read each page's context pack, the way `docs-write` builds it: the
`explains:`/`references:` elements (`uv run docsnip query explain <id>`), the
claims in its scripts, `release.yml`, and the R01 known issues. Facets (a) and
(d) are judged against it.

## 3. Review the facets

For a large change-set, review in parallel with fresh sub-agents, one per
facet or per file, each given its slice of `references/checks.md`, the rubric
facet, and an explicit file list. Don't fork: a fork inherits this context and
re-reviews everything. For one or two pages, review in place.

| Facet | Full | `lite` |
|---|---|---|
| (a) Facts & evidence | ✓ | ✓ |
| (b) Reader altitude & Diátaxis fit | ✓ | ✓ |
| (c) Procedures are concrete | ✓ | ✓ |
| (d) Structure & IA | ✓ | |
| (e) Style (judgment half) | ✓ | |
| (f) Citability | ✓ | |

Each reviewer returns a list: file, exact line (from the file, not the diff),
facet, issue, the rubric rule, and a concrete fix. The sample code itself is
out of scope, since its correctness is the script's test. Its *claims* are in
scope: a page sentence that the script doesn't assert is a facet (a) finding.

## 4. Severity by change scope

When the scope is a change-set, place each finding in one bucket:

1. **On a line the change wrote or edited.** Full severity. A newly added file
   counts as fully authored. Moved-but-unchanged text doesn't.
2. **Caused by the change, wherever it lands.** Full severity. Examples: a
   renamed heading breaks an anchor another page links to, a moved page leaves a
   stale `nav.yml` entry, a new page restates a fact R01 owns, a claim that now
   contradicts a page.
3. **Within three lines of a change.** Report it as `(opportunistic)`, capped at
   Suggestion.
4. **Unrelated, elsewhere.** Don't surface it.

With an explicit path and no diff, every line counts as bucket 1.

Severities:

- **Blocker:** gate failures, a leaked secret, a factual claim contradicted by
  a script or the model, an edit to a generated file, `status: ready` set
  without an approval.
- **Should-fix:** below the rubric's bar: an unbacked claim, wrong altitude, a
  vague procedure, a missing nav entry or `explains:` duplicate, prose
  warnings on changed lines.
- **Suggestion:** worth doing, ship without it.

## 5. Report

Score each facet 0–100 with a one-line rationale. List findings grouped by
file, Blockers first:

```
## content/unitycatalog/how-to/006-manage-volumes/index.md

### Blockers
- Line 88 [a facts]: "the server deletes managed files immediately", but
  volumes.py asserts they survive the cleanup delay. State the delay.

### Should-fix
- Line 41 [c procedure]: "configure the bucket" is not a step; name the policy
  and the action, or mark it as an open question.

### Suggestions
- Line 12 [f citability] (opportunistic): the intro restates the summary.
```

End with: `Reviewed {N} page(s): {B} blockers, {S} should-fix, {U} suggestions.`
Then add a line saying the review is advisory and that approval happens in the
review app.

When a human asked about a PR, ask before posting findings as PR comments, and
post only to lines the PR diff shows.
