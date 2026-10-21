---
name: double-knuth
description: >
  Generic two-pass "Double-Knuth" review for ANY repo or file set: Pass 1 =
  correctness/bugs on the change (delegates to /code-review when a git diff
  exists, agent-based otherwise), Pass 2 = completeness + cross-file/doc
  consistency — the defect class a diff reviewer structurally cannot see (stale
  counts/enumerations, docs contradicting changed behavior, dead paths, orphaned
  files, contract drift). Read-only: returns a ranked BUG/RISK/NIT list with
  file:line + concrete fixes. Specialized versions take precedence: websites →
  website-review; this skill covers everything else (skill suites, scripts,
  tools, configs). Trigger
  phrases: "double knuth this", "double knuth the code", "double knuth the
  repo", "two-pass review", "consistency review", "did the docs drift",
  "review the whole repo, not just the diff".
---

# Double-Knuth — generic two-pass review

The review standard the website suite already uses, generalized.
Run it at the END of a work batch, after a multi-file fix wave, or before
trusting a new tool — the moments cross-file consistency silently breaks.
Read-only: report findings; fix only when asked.

## Pass 1 — correctness (the change itself)

- **In a git repo with a diff:** run the host's diff-review command if it has
  one (Claude Code: `/code-review`, effort `high` after a fix wave or for new
  analytics, `medium` for routine edits); on hosts without one (e.g. Codex),
  review the diff yourself in a fresh context with the adversarial BUG/RISK/NIT
  prompt. Either way it covers correctness bugs + reuse/simplification.
- **No repo / no diff:** spawn a read-only agent over the changed files (or, if
  the host has no sub-agent primitive, review them in a separate fresh session)
  asking the two killer questions per guard/test/check: *"can this pass while
  the thing it protects is broken?"* (Rule 9) and *"does anything skip
  silently?"* (Rule 12) — hunt latent bugs that green tests cannot see.
- If the artifact has its own gate (test suite, build, linter), it must be green
  BEFORE Pass 1 — the review is not a substitute for the gate.

## Pass 2 — completeness + cross-file/doc consistency

Hunt what no diff can show. Check the repo against its own claims, verifying
every claim against actual file contents (never from memory):

- **Counts & enumerations:** "the four modules", lists of tests/files/steps/
  options anywhere in docs vs what actually exists.
- **Paths & references:** every file path, `cp` source, link, and import that
  any doc or script mentions actually resolves.
- **Docs ↔ behavior:** README/SKILL.md/comments describing behavior that has
  since changed (soft-warn vs hard-fail, defaults, branch names, formats).
- **Orphans, both directions:** files nothing references; references to files
  that no longer exist.
- **Single source of truth:** values claimed to live in one place (config,
  constants) have no hardcoded copies drifting elsewhere.
- **Declared intent vs actual state (config parity):** what a manifest/config
  *declares* vs what is actually present — a recurring bug class the happy path
  never exercises. Check: a `.gitignore` entry for a file that is still tracked
  (`git ls-files` it — `.gitignore` does NOT untrack); a config key consumed in
  code (`getProperty("x")`, an env var, a DI/Koin name, a flavor `BuildConfig`)
  but **missing from one of the build flavors / environments / `.properties`
  files**; a CI/build step invoking a name that doesn't exist (a fastlane *lane*
  absent from the Fastfile, a gradle task, a Make target, a script path); a
  plugin/dependency still referenced after its repo or module was removed.
- **Conventions:** the repo's stated conventions (naming, URL style, error
  handling) hold in every file, including examples inside docs.

Method: deterministic grep sweeps for the terms touched by recent changes
(Rule 5 — code answers what code can answer), PLUS one fresh-eyes read-only
agent for the judgment calls. Fresh eyes matter most when reviewing your own
fixes — the second Knuth must not share the first one's assumptions.

## Output

One ranked list — **BUG** (wrong or self-contradictory now) / **RISK** (breaks
under a normal future change, or a guard that can't fire) / **NIT** — each with
`file:line`, a one-line explanation, and a concrete fix. Then list the checks
that came back **clean**: silence is not coverage (Rule 12).

## After fixes are applied

Re-run the artifact's own gate end-to-end, and **negative-test any new guard**:
deliberately break the thing it protects and watch it fail with the intended
message (Rule 9). A guard that has never fired is a hypothesis, not a guard.
