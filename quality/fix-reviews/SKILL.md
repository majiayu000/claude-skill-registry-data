---
name: fix-reviews
description: >-
    Evaluate a pull request's review comments as signals of an underlying pattern, not one-off spot
    fixes — judge each comment against plainworks' engineering baseline, then apply the pattern
    across the whole change set (e.g. one typo comment → sweep every changed file for typos),
    validate, commit the fixes, and resolve the threads. Use when asked to go over, address, or act
    on PR reviews in plainworks.
---

# Fixing PR reviews by pattern

A review comment points at one spot, but it almost always describes a *class* of problem. The value of this skill is **generalization**: treat each comment as a probe into a pattern, fix every instance of that pattern across the change set, and only then resolve the thread.

Act on reviews **only when explicitly asked** — never as a side effect of finishing work.

## 1. Gather the reviews

Identify the PR (current branch's PR unless one is named) and pull every review, inline comment, and thread with its resolution state and node IDs:

```bash
gh pr view --json number,title,url,headRefName
gh pr view <n> --json reviews,comments
gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate   # inline review comments (path/line/body)
```

For resolvable thread IDs (needed in step 5), read the review threads via GraphQL:

```bash
gh api graphql -f query='
  query($owner:String!,$repo:String!,$pr:Int!){
    repository(owner:$owner,name:$repo){
      pullRequest(number:$pr){
        reviewThreads(first:100){ nodes{
          id isResolved isOutdated
          comments(first:20){ nodes{ path body author{login} } }
        }}
      }
    }
  }' -F owner=<owner> -F repo=<repo> -F pr=<n>
```

## 2. Evaluate each comment — the baseline wins

For every comment, decide before touching code:

- **Valid?** Judge it against plainworks' baseline ([`../../copilot-instructions.md`](../../copilot-instructions.md)), not the reviewer's authority. If a suggestion conflicts with the baseline or is simply wrong, **do not apply it** — note why (leave the thread for the maintainer; never argue under their name).
- **What is the real pattern?** Look past the wording to the class of issue:
  - a typo/grammar note → *spelling & wording across all changed prose and TSDoc*
  - a missing timeout/cancellation on one call → *every remote call / stream in the change set*
  - an `any` or unchecked `as` in one signature → *every public surface touched*
  - a module-level singleton / import-time side effect flagged once → *every store/client/session in the diff*
  - a token-in-URL or client-imports-server-auth note → *every auth/transport path touched*
  - a duplicated-concern note → *every place that reinvents a `std` owner*
- **Scope of the sweep.** Default to the PR's change set (`git diff origin/main...HEAD`). Widen to neighbouring files only when the pattern clearly extends there and the fix stays coherent; note the widening. A comment often surfaces a **pre-existing** defect or legacy path in the blast radius (the touched file and its close callers/callees). That is in scope too. Prefer a root-cause redesign over patching the symptom, and delete the superseded code rather than wrapping it. plainworks is alpha: no backward compatibility is owed, and a breaking fix beats a compatible patch.

## 3. Apply the pattern across the change set

```bash
git diff origin/main...HEAD --name-only     # the files in scope
```

- Search the whole change set for the pattern (grep/glob) and fix every occurrence.
- Where a fix changes behavior, do it **test-first** (failing vitest test → fix → green, failure paths included). Keep the fix the simplest correct design, not a bolt-on shim, compat flag, or alias.
- Keep each pattern's fixes cohesive so the follow-up amend reads as one intent.

## 4. Validate — scoped to what changed

Run the smallest gates that cover the touched packages (see the [`validate`](../validate/SKILL.md) skill):

```bash
turbo run test --filter='...[origin/main]'
bun run lint
turbo run typecheck build --filter=@plainworks/<name>
bun run check-boundaries && bun run check-versions
```

Docs/prose-only sweeps need no build/test gates. Never resolve a thread whose fix hasn't been validated.

## 5. Commit, push, and resolve

Commit the fixes using the [`commit`](../commit/SKILL.md) skill — one compact Conventional-Commit message, **no `Co-authored-by` trailer**, no review/plan narration. Keep the branch at **one commit** (amend) unless told otherwise; update the Changeset if the change grew. Then push and resolve the threads you genuinely addressed — no reply comments under the maintainer's name:

```bash
git push
gh api graphql -f query='
  mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}){ thread{ isResolved } } }' \
  -F id=<threadId>
```

Leave unresolved only the threads you deliberately rejected (baseline conflict) or that need a maintainer decision; briefly report those back rather than resolving them silently.

## Baseline

Every fix must still satisfy plainworks' baseline. If acting on a comment would push code below the baseline, reject the comment instead.
