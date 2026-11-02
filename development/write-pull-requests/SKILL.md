---
name: write-pull-requests
description: Use when opening or updating a pull request — produces a bug-fix or feature description reviewers from junior to CTO can follow end to end.
---

# Write Pull Requests

The description is the cheapest review tool the author controls: it decides whether the
reviewer follows the change or reverse-engineers it. Two fixed shapes, filled from the
diff and from output that actually scrolled by — never from memory of what you meant to
build.

## 1. Audit — what does the branch ship, and does a PR exist?

```bash
BASE=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)   # or: git symbolic-ref --short refs/remotes/origin/HEAD
git log "origin/$BASE"..HEAD --oneline
git diff "origin/$BASE"...HEAD --stat  # or: git show <sha>, for a PR shipping one existing commit
ls .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md \
   .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null
gh pr view --json number,title,body 2>/dev/null
```

Change nothing yet. Three findings decide the rest:

- **The diff is the source of truth.** Describe what the branch ships — including the
  commit you forgot — not what you remember working on.
- **A repo template wins.** If `.github/` defines a PR template, fill *its* sections in
  *its* order, and carry this skill's discipline into whatever slot asks for testing or
  verification. The shapes below apply only when the repo has none.
- **An existing PR means update, not create.** Step 5 edits it in place; never open a
  duplicate. If the body already matches what the branch now ships, exit — nothing to do.

## 2. Decide the shape

One question: does the branch **restore intended behavior** (bug fix) or **change or
extend it** (feature)? Mixed branches lead with the dominant shape and carry the
remainder under Notes. Edge cases (refactors, mixed branches): `./pr-patterns.md`.

## 3. Fill the sections — exactly these, in this order

**Bug fix:**

1. **Problem** — the user-visible symptom, in plain words: what broke, who hit it.
2. **Root cause** — the mechanism actually found, not the first suspicion.
3. **Fix** — what changed, and why this way.
4. **Tests** — coverage added or extended; name the test that now catches the bug.
5. **Verification** — the commands run and their observed output. Evidence, never
   claims (`./pr-patterns.md`).
6. **Notes** — tradeoffs, follow-ups, review hints.

**Feature:**

1. **Summary** — two or three sentences a CTO reads first: what ships, why it matters.
2. **Problem** — the need, in plain words: what couldn't be done before.
3. **Solution** — the approach chosen; the rejected alternative in one line when the
   diff or commits record one — "Rejected: none recorded" is honest too.
4. **Implementation** — the shape of the change in the code: key files, seams touched.
5. **Tests** — coverage added or extended.
6. **Verification** — commands run and observed output.
7. **Notes** — tradeoffs, follow-ups, review hints.

Non-trivial PRs close with the merge checklist, posted unticked (skip it for one-line
fixes and when the repo template has its own):

```markdown
## Before merge
- [ ] Manual review
- [ ] Smoke tested
- [ ] Pipeline green
```

A box is ticked by whoever verified it — the reviewer for the manual read, the author or
CI for the rest. A pre-ticked box with nothing behind it is decoration, not evidence.

No invented headings, no omissions: content that fits no section goes under Notes or
stays out. For Verification, run the commands *now* and paste the lines that prove the
point; anything not run is declared — "Not run: needs staging" — an honest gap beats a
fabricated pass. Write the assembled body to a temp file (`mktemp`, keep its path in `BODY`); step 5 posts that file. Any
attribution trailer your tooling requires goes last, after the checklist; it is not a
section.

## 4. Self-check against the audience contract

Read the draft as the three readers of `../_shared/audience.md`:

- **Junior** — can they follow Problem → Fix (or Solution) without tribal knowledge?
  Every internal codename expanded on first use?
- **Senior** — does every claim have its evidence under Tests or Verification? A bare
  claim gets its proof moved in, or gets softened to what the evidence supports.
- **CTO** — do the headings and first lines alone carry outcome and risk?

Plain prose throughout. A sentence that reads like a release announcement gets rewritten
as a fact.

## 5. Create or update

Show the title and body for approval first — pushing and opening a PR publish the draft.

```bash
git push -u origin HEAD               # if not yet pushed
gh pr create --title "<subject>" --body-file "$BODY"
# or, when step 1 found an existing PR:
gh pr edit <number> --body-file "$BODY"
```

The title carries the branch's dominant commit subject; a subject past ~72 characters
is compressed — keep the `type(scope):` and the one concern
(`../write-commit-messages/SKILL.md`). Editing the existing body in place is this skill's idempotency: a re-run regenerates the
description from the current diff and lands on the same PR.

## 6. Verify

```bash
gh pr view
```

Expected: one PR for the branch; six (bug fix) or seven (feature) sections in the fixed
order, closed by the Before-merge checklist (non-trivial PRs) — or the repo template's own; every
Verification entry is a command plus its observed output, not an adjective.

## References
- ./pr-patterns.md — why evidence beats assertion, Problem vs Summary, the shape decision, a filled example, when to deviate.
- ../_shared/audience.md — the junior-to-CTO contract step 4 checks against.
- ../write-commit-messages/SKILL.md — the commit subjects the title and Summary draw from.
