---
name: "Red: Branch"
description: "Adversarial review of a branch diff written as the colleague trying to get it rejected, aimed at one or two named readers"
when_to_use: "Before a branch goes up as a PR, when branch-qa_review's structured pass isn't hostile enough: find what gets it rejected, on the terms of the specific reviewers who will reject it."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: red
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(git:*)", "Bash(~/.claude/library/scripts/branch-facts.sh:*)", "Bash(mkdir:*)", "Bash(ls:*)", "Bash(rg:*)", "Bash(grep:*)", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Bash(deno:*)", "Bash(python3 \"$HOME\"/.claude/library/scripts/red-personas.py:*)"]
argument-hint: "<base branch> [persona] [persona] [-- what else would get this rejected]"
---

# Sabotage a branch

You want this branch rejected. This is the same stance as `branch-qa_review`
turned hostile and reader-aimed: not a thinner pass, a meaner one, run through
specific reviewers rather than a checklist.

The methodology itself (persona resolution, the nine-field schema, field
ordering, the report skeleton, discipline rules, refine-then-save) lives in
`~/.claude/library/references/red/methodology.md`. Read it now and execute it;
this file adds only what is unique to the branch path.

**On `Write`:** kept, gated to the same approval-only save path `red-doc` uses
(Step 5 below). Everything before that save is print-only, same as
`branch-qa_review`'s fully read-only stance; the difference is this skill
writes its dossier to disk once, on explicit approval, rather than never. It
never edits the branch it is reviewing.

## Step 1: Parse `$ARGUMENTS`

**Base is required; persona is not.** Requiring base is what removes the
ambiguity a single token used to carry: with base mandatory, one token can
only be the base branch, never a persona guess. `/red-branch cedric` means
"diff against a branch called `cedric`, reviewed by Goblin": if no such
branch exists, `branch-facts.sh`/`git diff` fail loudly on the bad ref, which
is an acceptable failure mode; if the failure looks like it might actually be
a persona name instead, say so rather than only reporting a missing branch.

Zero tokens: base is missing. Print tersely and stop:

```
Usage: /red-branch <base branch> [persona] [persona] [-- failure conditions]
```

The one exception: the single literal token `personas` still prints the
roster and stops, per its own line below: that is a deliberate roster
lookup, not a missing base branch.

One or more tokens: positional, in this order. Nothing here is prompted for
interactively.

```xml
<arguments>
    <positional n="1" name="base" required="true">
        Base branch to diff against. No default: an unstated base used to
        collide with an unstated persona, so base is now always required.
    </positional>
    <positional n="2,3" name="personas" required="false">
        Resolved per the methodology's Step 1/1a/1b/1c, via
        `python3 "$HOME"/.claude/library/scripts/red-personas.py` called with
        `--scope branch`. **Default: `goblin`** when none is named — Jason's
        own review stance, scoped to both doc and branch. `cedric` is also
        scoped to both doc and branch (one forensic stance, domain-specific
        Reads/Skips/Stake/Trigger for each); `bob` is doc-only and does not
        transfer as-is. Further branch-specific personas (the maintainer who
        owns the touched module, the reviewer who never opens a test file)
        get defined the same way on first need.
    </positional>
    <positional n="4+" name="failure-conditions" required="false">
        Free text: extra information about what would get this specific
        branch rejected. Anything after a bare `--`, or any remaining argument
        that is not persona-shaped. Fold it into every pass, and give it its
        own section when it introduces criteria the standing sections do not
        already cover.
    </positional>
</arguments>
```

`/red-branch personas` prints the roster from the personas file and stops.

## Step 2: Facts and the diff

`"$HOME"/.claude/library/scripts/branch-facts.sh $base` emits JSON: ahead/behind, conventional-commit and
branch-name compliance, WIP commits, diff size, conflict markers, TODOs and
console.logs added, test files touched, svu bump. These are facts to cite, not
findings on their own; a fact becomes a finding once you show what it does to
a specific reader (a non-conventional commit is nothing to Bob, evidence of
sloppiness to Cedric).

Read the full diff, `git diff $base...HEAD`. Then read what it touches beyond
the diff itself: for every changed export, function signature or component
prop, **Grep for its callers and confirm they still hold**: this is
`branch-qa_review`'s Step 2 addition, adopted here because changed-contract
breakage lives outside the diff and a hostile reviewer who only reads the diff
misses exactly the class of bug that ships. Where a claim is checkable by
running something (a test, a typecheck, a quick script), run it rather than
reasoning about it, per `pr-handle_review`'s Step 3.

Research project conventions in `CLAUDE.md`, `.claude/**/*` and `docs/*` before
critiquing implementation, per `pr-review-dry_run`'s Step 3: a convention
violation is a real finding, a stylistic disagreement with an established
project practice is not.

## Step 3: The passes

Run each of these over the whole diff, plus the persona-pass from the
methodology. Keep going until a full pass turns up nothing new. Never pad: an
item you cannot cite by `file:line` does not exist.

Four named passes, carried in from `pr-review-dry_run`'s foci so the dossier
format's reorganisation does not cost coverage:

- **Correctness.** Will this break anything: logic errors, edge cases, race
  conditions, off-by-ones, null/undefined paths not handled. Includes the
  changed-contract check from Step 2.
- **Security.** Injection, auth/authz gaps, secrets in the diff, unsafe
  deserialisation, anything that widens an attack surface.
- **Convention violations.** Checked against `CLAUDE.md`, `.claude/**/*` and
  `docs/*` per Step 2. Only violations of an *established* practice; a
  reasonable choice the project has no stated position on is not one.
- **Reinforcement.** What is actually right: a genuinely good call, a test
  that catches something real, a refactor that removes a footgun. This
  matters for the same reason `red-doc`'s real-defects section matters: a
  purely hostile dossier that never says what holds up reads as noise, not
  signal, and the author cannot tell the bugs from the debating points.

### Named failure conditions

Only when positional 4 supplied criteria the passes above do not already
cover. Same evidence discipline.

## Step 4: The report

Follow the methodology's report skeleton. Title is `Sabotage dossier:
{branch name}`. Evidence sections are, in order: Section 1 correctness
(`C1`, `C2` …), Section 2 security (`S1`, `S2` …), Section 3 convention
violations (`V1`, `V2` …), Section 4 reinforcement (numbered, not hostile;
this section is the one place the dossier is allowed to be generous), then the
per-persona sections and named failure conditions per the shared skeleton.

This dossier format organises and ranks findings differently from
`pr-review-dry_run`'s 🔴/🟠/🟡/🟣 taxonomy, but must not find less: if a run of
this skill on a branch misses something `/branch-qa_review` would have caught
on the same branch, that is a coverage regression in this file or in
`methodology.md`, not an acceptable trade for the dossier's reader-first
structure.

**Scope boundary:** this skill reports. It does not fix. Splitting review from
repair is why `branch-qa_review` stays read-only; the same reasoning holds
here even though this file keeps `Write` for the save step.

## Step 5: Refine, then save

Follow the methodology's refine-then-save protocol. The target-slug for the
save path is the branch name with `/` replaced by `-`.
