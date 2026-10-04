---
name: review-gate
description: >
  Independent multi-agent review that decides whether a frename change (code PR or design doc) may
  merge. Use before opening or merging any agent-made PR, after every fix round, and when asked to
  "review", "gate" or "check if this is ready for main".
---

# Review gate

The author of a change never judges it. Reviewers are subagents started with fresh context: they get
the issue, the design doc (if any), the commit SHA under review, and the diff against `main` — not
the author's reasoning. Run them in parallel. A verdict applies to that SHA only.

## Reviewers

Code PR — all three, every round:

1. **Correctness** — tries to break the change. Reads the diff and the code around it, looks for
   logic errors, panics/`unwrap` in production paths, data loss (renames, XMP writes, comment
   sidecars, undo), Windows path issues, race conditions in async tasks, regressions in untouched
   callers. Runs the local gate. Where it suspects a bug it writes a failing test to prove it.
   Checks `git diff origin/main... -- '*.rs' '*.toml' 'rust-toolchain*' '.cargo/**' '.github/**'` for weakened
   gates: removed or loosened asserts, new `#[ignore]`, deleted tests, `cfg` that hides a test on
   the CI platforms, CI steps or flags removed or relaxed. Each is a blocker unless the issue
   requires it. Any change to a guarded file (list in `nightly` → Trust) that the issue does not
   explicitly ask for is a blocker.
2. **Design and quality** — could this be simpler, smaller, more in line with the codebase? Checks
   Iced Elm architecture rules (`.cursor/skills/iced-elm-architecture`), core/UI separation, naming,
   duplication, dead code, scope creep beyond the issue, missing tests for new core behaviour.
3. **Product** — does it do what the issue and design ask, from the editor's point of view?
   Keyboard flow, discoverability, consistency with existing UI, README and `version.md` text
   (short, user language, per `readme` skill). For UI changes it looks at the screenshots and checks that
   the PR body shows every screen the change touches (a missing or wrong screenshot is a `major`
   finding). New UI text has keys in every shipped language.

Design doc (advisory only, one round, never blocks; see `nightly` step 3) — reviewers 2 and 3, judging the design: missing flows, edge cases, simpler
alternatives, feasibility (is every format/API claim sourced?).

## Verdict format

Each reviewer returns:

```
VERDICT: APPROVE | CHANGES_REQUIRED
FINDINGS:
- [blocker|major|minor] file:line — problem — concrete failure scenario — suggested fix
```

APPROVE is allowed with only `minor` findings. Any `blocker` or `major` means CHANGES_REQUIRED.
A finding without a concrete failure scenario or a concrete improvement is dropped.

## Loop

1. Fix every blocker/major (and minors that are cheap and clearly right).
2. Re-run the local gate.
3. Start a **new** round with fresh reviewers (never reuse a reviewer that saw an earlier round —
   it anchors on its old findings). Give them the full current diff.
4. Repeat until all three approve in the same round. Four rounds without that → the change is
   finished as far as possible and left unmerged for the owner (`nightly` → "Owner review").

Record every round in the PR description: SHA, each reviewer's verdict, findings count, what was fixed.
