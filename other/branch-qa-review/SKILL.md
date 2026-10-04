---
name: "Branch: QA Review"
description: "Assess branch readiness for PR submission: full review methodology plus the checks only a local checkout allows"
when_to_use: "Before opening a PR, when you want everything pr-review would later flag caught now, grounded in exact git facts and a real test/typecheck/lint run."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: branch
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash(git:*)", "Bash(~/.claude/library/scripts/branch-facts.sh:*)", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Bash(deno:*)"]
disallowed-tools: ["Edit", "Write", "NotebookEdit"] # assesses readiness, never fixes
arguments: ["base"]
argument-hint: "[base branch (default main)]"
---

Assess whether this branch is ready to be submitted as a reviewable pull request. Three layers: the mechanical facts, the gate run and the same review methodology `pr-review` applies after the PR exists. Anything that would surface in the PR review should surface here, one step earlier.

## Step 0: Facts

Gather the exact numbers first: `"$HOME"/.claude/library/scripts/branch-facts.sh $base` (blank `$base` = the script's default, `main`) emits JSON (ahead/behind, conventional-commit and branch-name compliance, WIP commits, diff size, conflict markers, TODOs and console.logs added, test files touched, svu bump). Judge from these facts; the steps below are the judgement layer, not fact-gathering to repeat by hand.

## Step 1: Run the gate

Discover the project's test, typecheck and lint commands from `package.json` (or the ecosystem equivalent) and run all three. This is the one check only a local checkout can perform, the whole reason to review before the PR instead of after, so never skip it or substitute a static skim of test files. Distinguish failures the branch caused from pre-existing breakage (run the same check on the base branch when unclear); pre-existing breakage is reported, never blamed on this branch.

## Step 2: Review the code with pr-review's methodology

Load the `pr-review-dry_run` skill and run its full methodology against this branch: foci (correctness, security, conventions, reinforcement), taxonomy (🔴/🟠/🟡/🟣), scope classification and its conventions-research step (`CLAUDE.md`, `.claude/**/*`, `docs/`). The local diff `git diff <base>...HEAD` (the same `$base`, default `main`) substitutes for its `gh pr diff` step; everything else applies unchanged.

Do not re-derive or abbreviate that methodology here. A thinner duplicate of it is exactly what this skill used to carry, and it routinely missed what the PR review then caught: structured per-focus passes find what "check for obvious bugs" skims past.

One addition the diff alone can't show: for every changed export, function signature or component prop, Grep for its callers and confirm they still hold. Changed-contract breakage lives outside the diff.

## Step 3: Branch mechanics

From the Step 0 facts, briefly:

- Conventional-commit compliance, atomicity, no WIP/fixup/junk commits
- Branch name: `<prefix>/<short-description>`, prefix from the canonical set (matches CLAUDE.md §8.6): `feat`, `fix`, `enhance`, `refactor`, `test`, `docs`, `config`, `chore`, `ci`, `deps`, `hotfix`, `spike`, `agents`; breaking-change branches use `<prefix>/breaking-<description>`

## Step 4: Breaking changes

- Removed or renamed exports, functions, types or components
- Changed function signatures (required parameters added/reordered)
- Modified return types in a widening direction
- Database schema changes (columns removed/renamed, constraints changed)
- HTTP API changes (routes, methods, request/response shapes)
- New required environment variables
- Changed component props (removed, renamed, type-changed, newly required)

## Verdict: defined, not vibed

| Verdict | Criteria |
|---|---|
| **Blocked** | Unresolved conflict markers, or a red gate that predates the branch (needs a human call before any PR makes sense) |
| **Needs Work** | Any 🔴 finding (per `pr-review-dry_run`'s `<blocking-gate/>` closed trigger list, not a severity judgement made here), a red gate this branch caused or WIP/fixup commits |
| **Ready** | Green gate and nothing above 🟠/🟡; remaining findings are listed as improvements, not blockers |

## Output Format

### Verdict

**Ready** | **Needs Work** | **Blocked**, with the one-line reason from the mapping above.

### Gate

Test / typecheck / lint results, and whether any failure predates the branch.

### Findings

The Step 2 findings in taxonomy order, file and line references included. Omit if none.

### Branch Health

Branch name compliance, commit message quality, commit atomicity.

### Breaking Changes

Any detected, with context. Flag format:
> ⚠️ Breaking change: consider `feat!:` or `BREAKING CHANGE:` footer

Omit if none.

### Recommended Next Steps

Ordered list: blockers first, then improvements, then nice-to-haves.

---

If the verdict is **Ready**, offer to run the `pr-create` skill immediately, forwarding `base <branch>` when `$base` isn't main so the PR opens as a stacked layer on the same base this review judged, rather than silently targeting main.
