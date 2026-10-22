---
name: quick-fix
description: >-
  Makes a small, obvious fix directly, without the feature pipeline: a typo, a reversed
  condition, a missing null check, a stray import, or a patch or minor dependency bump. One
  concern, usually under 20 lines, in C# or Lit/TypeScript. Escalates to the feature
  pipeline if the fix turns out bigger.
user-invocable: true
argument-hint: <describe the fix>
---

# quick-fix

For the trivial stuff: the kind of bug where opening `feature-explore` → `feature-design` → `feature-plan`
→ `feature-build` would be absurd. This skill is deliberately outside the `feature-*` pipeline
naming — it's an escape hatch *around* the pipeline, not a phase in it.

## Scope

- IN: one-spot fixes a competent engineer would commit straight to the default branch without
  ceremony. Single concern, usually under ~20 lines. A dependency version bump counts: one
  package, or one group of dev-only ones, with no code change beyond the version.
- OUT: anything that needs a design call, touches a public method's signature (that's the
  `[Obsolete]`-proxy discipline in `umbraco-package-conventions`/`umbraco-backoffice-
  conventions`, not a quick-fix), renames a backoffice manifest `alias` (a silent breaking
  change per `umbraco-backoffice-conventions`), changes behavior across modules, or needs
  more than one new test. A bug fix may add one regression test for the bug. If it smells like any of that, **stop and escalate** —
  suggest `feature-plan` (if a plan folder already covers this area) or `feature-explore` (if it
  doesn't).

## Argument

`$ARGUMENTS` describes the fix in the user's words (e.g. "remove the unneeded try/catch in
GetItemAsync", "fix the typo in the login button label"). If empty, ask one short clarifying
question.

For a bug fix, it may also include a repro: the steps or test that show the bug. A bug fix
is one that changes behavior someone saw go wrong. Typos, comments, and dead code aren't.

## Loop

1. **Locate.** Find the exact site. If the description is ambiguous or matches multiple
   places, ask before guessing.
2. **Confirm it's actually small.** If reading the surrounding code reveals the fix is
   non-trivial (touches a class/component boundary, changes a public contract, needs new
   branches of test coverage), **stop and escalate** — tell the user this isn't a quick-fix
   and suggest `feature-plan`. If you can't say what's causing the bug, stop and suggest
   `investigate-bug` instead: a quick fix needs a known cause.
3. **Consult skills selectively.** Only load a skill if the fix genuinely touches its
   territory:
   - `umbraco-performance`: only if the fix touches a cache or a per-request or per-save
     path.
   - `umbraco-extensibility`: only if the fix touches a background job or another extension
     point.
   - `umbraco-env-sync`: only if the project syncs with Umbraco Deploy or uSync and the fix
     adds an entity, changes a synced one, or touches the sync code.
   - `umbraco-dependencies`: only if the fix adds or bumps a NuGet or npm package.
   - `umbraco-dotnet-testing`: only if the fix adds or changes an integration test on Umbraco's
     test base classes.
   - `umbraco-backoffice-testing`: only if the fix adds or changes a backoffice element test or
     a Playwright test.
   - **`umbraco-security`: always, if the fix touches auth, user input, the
     Management API, secrets, or `unsafeHTML`/`unsafeSVG`.** "Quick" doesn't exempt a fix from
     these — they're non-negotiable in this plugin regardless of diff size.
   - No `builder` dispatch. You make the edit yourself; the fix is too small to hand off.
4. **Reproduce it, for a bug fix.** Use the repro you were given, or write one from the
   description. Run it through the real entry point, in the order `feature-build`'s "Smoke
   the real entry point" step gives, and see it fail. The real entry point applies whether or
   not the code is on a screen: a value converter or a handler is reached through the
   backoffice or an API request too. If no e2e test covers the path and the project has an
   e2e suite, write the repro as the one regression test this fix may add; otherwise use the
   demo site.
5. **Apply the edit.** Use `Edit`, not `Write`. Match surrounding style.
6. **Look for the same bug elsewhere.** Name the cause, not just the line (a missing
   permission check, an unscoped query, an unlocalized label). Then grep for sibling code with
   the same cause: other endpoints on the same controller or base type, other components using
   the same pattern. Also check whether an earlier fix for the same cause already added a
   helper this fix should reuse. List what you find in the hand-off; don't silently widen the
   fix. If the right answer is one shared fix across several places, that's no longer a quick
   fix, so escalate as in step 2.
7. **Verify.** Run the project's build/test if fast. If slow or absent, run the narrowest
   check that proves the fix (the single related test, or a targeted build of just the
   changed project). Run the lint/format check from `CLAUDE.md` on the changed files. Then:
   - **A bug fix:** run step 4's repro again, the same way, and see it pass. A slow suite is
     no reason to skip this; it's one path, not the suite.
   - **Anything else a person can see or call** (a screen, a Management API endpoint, a
     property editor): smoke it through the real entry point the same way.

   If the real entry point can't be run at all (no e2e suite, no demo site, or the site won't
   start), say so in the hand-off as "not verified end to end", with why. Never leave it out
   silently.
8. **Review.** Unless the change is text only (a typo, a comment, a log string, a label),
   dispatch one `reviewer` subagent (Agent tool, `subagent_type: reviewer`) against the
   uncommitted diff, with the fix description as its task. Small diffs still break things a
   person doesn't see from the changed lines: a public signature, a caller in another file, a
   manifest `alias`. Fix any Critical or Important finding yourself and review again until
   `PASS`, giving each re-review the round's diff and previous findings, as in
   `feature-build`'s "Recurse" step. If a finding shows the fix isn't small after all, or it
   still fails after three rounds, stop and escalate as in step 2.
   If a finding was a repeatable mistake a future `builder` would likely make on another
   task, write it to `.claude/memory/` (type: `gotcha`) once fixed, the same as
   `feature-build` does.
9. **Report and ask before committing.** Show the diff summary and propose a one-line commit
   message, following `git-workflow`'s Conventional Commits format. Do **not** commit unless
   the user says go — committing straight to the default branch is a shared-state action, per
   `git-workflow`'s always-ask-before-touching-main rule for AI agents.

## Hand off

One sentence: what changed, what you verified (tests, the repro failing before and passing
after, or "not verified end to end" and why, review verdict), awaiting commit confirmation
(or confirming the commit if the user pre-authorized it). Then list any places with the same
bug from step 6, one line each.
