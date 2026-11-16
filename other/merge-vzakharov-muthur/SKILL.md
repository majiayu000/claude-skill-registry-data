---
description: Merge the branch's PR — the one entry for an operator's ask to merge, "merge", "мерджи", "land it", in any words. A branch not yet finalized runs `/finalize and merge`; a finalized one runs `/check-merge` and merges under the same gate, or syncs the advanced base in with `/sync-branch` and stands down. Invoke as `/merge [<branch|#PR|PR-url>] [no vet]`. "Merge main" — the base into the branch — is `/sync-branch`, not this.
---

**Open the reply by naming the path taken** — land prep, or the check of a
finalized branch — since the operator asked for a click, and either path can end
in a stand-down rather than a merge.

## Argument shape

- **Target** (optional, first token): a branch name, `#NNN`, or a PR URL. Load
  `@.claude/skills/from-branch/SKILL.md` and follow it to attach to `<target>`
  first, as `/finalize <target>` does. No target → the current branch.
- **`no vet`** (optional): rides unchanged to whichever of `/finalize` and
  `/sync-branch` runs below.
- **Changes asked alongside** — this skill is reached by an ask in words as
  often as by the command, and "fix the typo and merge" asks for a diff too.
  That holds the merge: the ask was written before the diff it would merge
  existed, so make the changes, run `/finalize` without the flag, and report
  that the merge was held and that `/merge` lands it once the operator has
  looked — `@.claude/skills/finalize/merge.md` § "The flag" says why.

## Finalized?

**Finalized means the PR is ready for review and its
`<!-- finalize-attestation <sha> -->` comment names the current head** — or a
head past it only by `.claude/costs/sessions/`, which
`@.claude/skills/finalize/attest.md` § "What makes it worth trusting" counts as
the same head. Anything short of that is a diff no run has verified.

## Not finalized → land prep

Load `@.claude/skills/finalize/SKILL.md` and follow it with `and merge` (and
`no vet`, when given). Its step 8 holds the gate.

## Finalized → check, then the same gate

Load `@.claude/skills/check-merge/SKILL.md` and run it **once**. Its hand-back
on an advanced base is taken here rather than by its standalone deliberation.

- **`contained`** → walk `@.claude/skills/finalize/merge.md` § "Step 8 — the
  gate" over this run. Only its step 5 (the squash reconcile), step 6 (the
  check), "Anywhere" and, on a `no vet` attestation, "Under `no vet`" entries
  can fire; the rest describe steps this run never ran. **The attestation itself
  is part of the gate here**, because the land-prep run's own steps are what
  would have stood it down: a line short of green — the vet run, CI, a bucket
  left undispatched for any reason but the diff not reaching it — or a two-shot
  stop it records, stands this run down. The skips a `no vet` attestation
  records are its mode, not such a line, and a `Verified` SHA trailing the
  marker stands nothing down: that judgment is written in the attestation being
  merged on. Pass → `@.claude/skills/finalize/merge.md` § "Merging", whose step
  7 is already up. Fail → its § "Standing down".
- **`advanced`** → load `@.claude/skills/sync-branch/SKILL.md` and follow it,
  then let `/check-merge` Step 3 reconcile the squash record on the merged head.
  Stand down per `@.claude/skills/finalize/merge.md` § "Standing down", naming
  step 6. What clears it is `/merge` again: the head is now past its
  attestation, so that run is `/finalize and merge`, which verifies the merged
  head.
- **`merged`, `closed` or `error`** → report it and stop, as `/check-merge`
  does.
