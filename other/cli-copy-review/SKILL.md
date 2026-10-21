---
name: cli-copy-review
description: Dev-only review of user-facing CLI interface copy in `src/cli/tui/*.js`, `src/cli/*.js` error paths, and `bin/cli.js` help/usage text. Surfaces three failure modes — copy/behavior mismatch, jargon, missing next-action — as a punch list the maintainer addresses before `/grant-commit`. Read-only; no writes to source. Conditionally seeded by `/triage` between `/memory-sync` and `/grant-commit` when the request will touch CLI surfaces.
---

<!-- DEV-ONLY SKILL — this file lives in `.claude/skills/cli-copy-review/` of the
     baseline repository for the maintainer's own workflow. It is excluded from
     the shipped template by `scripts/build-template.sh` Stage 1.5 (no
     `owner: baseline` frontmatter → pruned from `obj/template/`). End-user
     projects never see this skill. -->

# /cli-copy-review — review user-facing CLI copy before shipping

You are reviewing the user-facing text strings in the baseline's CLI for three failure modes the maintainer wants caught before each release:

1. **Copy/behavior mismatch** — the string promises behavior the code does not perform.
2. **Jargon** — internal terminology leaking into end-user text.
3. **Missing next-action** — the string reports a problem or partial result without telling the user how to address it.

This skill is a **quality gate**, not a phase. It sits between `/memory-sync` and `/grant-commit` when the workflow has been seeded with a `Run /cli-copy-review for <slug>` task by `/triage`. It is read-only: it surfaces findings; the maintainer addresses them in subsequent conversation turns and re-runs the skill until clean.

## When to use

- The workflow's task list contains `Run /cli-copy-review for <slug>` (seeded by `/triage` because the request will touch user-facing CLI surfaces).
- The maintainer types `/cli-copy-review` ad hoc before shipping a release.

## Inputs

Capture user-facing strings from these source files:

- `src/cli/tui/*.js` — clack-based prompts. Every string passed to `prompts.intro`, `prompts.outro`, `prompts.log.*`, `prompts.cancel`, and `prompts.select` (the `message` field plus each `options[].label` and `options[].hint`).
- `src/cli/*.js` — domain-layer errors. Every string passed to `Error(...)` and similar constructors that propagates to stderr via the CLI's top-level error handler. Include strings emitted via `console.error` or `process.stderr.write` from non-TUI modules.
- `bin/cli.js` — top-level argparse output, help/usage text, and error formatting.

Skip:
- Strings inside `.claude/hooks/`, `.claude/skills/`, `.claude/commands/`, `.claude/agents/` — baseline-internal text, not end-user CLI surface.
- Internal logging not surfaced to the user (e.g., `harness_continuation.log` writes).
- Test files under `tests/`.

## Procedure

1. **Enumerate** every user-facing string in the source files listed above. Record file path, line number, and the exact string content.

2. **For each string**, evaluate the three failure modes:

   **(a) Copy/behavior mismatch.** Read the surrounding code and trace the actual control flow. Does the string accurately describe what happens next?

   Concrete example we hit on 2026-05-20: `src/cli/tui/upgrade.js:61` warned that tier-2/tier-3 customized files would "fall back to the binary prompt," but `merge.js:dispatchCustomized` in dry-run mode short-circuits at lines 144-147 before reaching `resolveBase`, so those files never appeared in `collectUserChoices`'s conflict list — the promised prompt never fired and the files were silently kept-mine. Always trace from the string to the behavior to verify.

   **(b) Jargon.** Would a downstream user, reading this string fresh without ever having opened the source tree, understand what it means and what to do? Flag internal vocabulary that has no meaning outside this codebase: `manifest_version`, `tier-2`, `tier-3`, `BASE-content`, `BASE recovery`, `INCOMING`, `stage_ts`, `oldManifest`, `newManifest`, `SKIP_CUSTOMIZED`, etc. Suggest plain-language replacements where you can.

   **(c) Missing next-action.** When the string reports a problem, a partial result, or a state the user must act on, does it tell them what to do?

   Examples of strings missing a next-action:
   - "Applied 1; 3 skipped." (Skipped why? What should the user do about the 3?)
   - "BASE-content recovery unavailable." (How does the user enable it?)

   Compare with strings that already carry a next-action:
   - The pending semantic-merge stage warning ends with "Open Claude Code and run /upgrade-project to reconcile."

3. **Produce a punch list** grouped by file, ordered by line number. Per-finding format:

   ```
   src/cli/tui/upgrade.js:61
     string: "legacy manifest_version: 1 detected; BASE-content recovery unavailable. Tier-2 / tier-3 files will fall back to the binary prompt."
     issues:
       - copy/behavior mismatch — promises binary prompt, but dispatchCustomized short-circuits in dry-run (merge.js:144-147) so the prompt never fires; tier-2/3 files are silently kept-mine
       - jargon — "manifest_version", "BASE-content recovery", "Tier-2 / tier-3" are all internal vocabulary
       - missing next-action — does not tell the user how to recover BASE for legacy installs
     suggested rewrite (illustrative; maintainer to confirm):
       "Your previous install predates version-tracked manifests, so smart three-way merges aren't possible for customized files. You'll be prompted yes/no per file instead. (To enable smart merges next time, add `baseline_version: \"<your-version>\"` to .claude/.baseline-manifest.json.)"
   ```

4. **Report verdict.** Either `CLEAN` (no findings, workflow proceeds to `/grant-commit`) or `NEEDS_REVIEW` (N findings, maintainer addresses and re-runs).

## Constraints

- **Read-only.** This skill never edits source files. The maintainer reviews the punch list and edits in subsequent conversation turns. After edits, re-run `/cli-copy-review` until it reports `CLEAN`.
- **No archival artifacts.** Findings live in the conversation only. The workflow's `/document` and `/archive` phases have already run by the time this gate fires; this review sits before `/grant-commit` as a quality check, not a phase that produces docs.
- **No commits.** Findings drive maintainer edits; the maintainer commits via the normal `/grant-commit` + `/commit` flow once the review is `CLEAN`.
- **Scope is the shipped CLI surface only.** Do NOT review strings inside hooks, skills, commands, or agents — those are baseline-internal text, not end-user CLI.
- **Suggested rewrites are illustrative.** When the maintainer's intent is ambiguous, propose 1-2 alternatives rather than picking one arbitrarily. The maintainer decides; this skill surfaces.

## Output

After running, summarize:

```
# /cli-copy-review — <slug>

Reviewed: <N> strings across <M> files.
Findings: <K> (copy/behavior mismatch: <a>, jargon: <b>, missing next-action: <c>).
Verdict: CLEAN | NEEDS_REVIEW

<per-finding details from step 3>
```

If `CLEAN`, tell the maintainer: "All user-facing CLI copy passes review. Proceed to `/grant-commit`."

If `NEEDS_REVIEW`, tell the maintainer: "<K> finding(s) to address. Edit the surfaced strings, then re-run `/cli-copy-review` to confirm clean."
