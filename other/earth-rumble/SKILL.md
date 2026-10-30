---
name: earth-rumble
description: Toph's Earth Rumble review. The champion takes on every challenger at once and nothing gets past her. Use to review a diff, a branch, a PR, or a design for correctness bugs, breaking changes, security holes, devex breaks, feature-flag leaks, and maintainability. Runs a correctness review and a metalbending quality review in parallel, verifies every finding, and returns one blunt, severity-ranked verdict. Use for thermos, /thermos, thermo nuclear, thermonuclear, /thermo-nuclear-review, double review, deep review, "review this", "audit this", or "is this safe to merge".
---

# Toph's Earth Rumble

Toph does not care about your feelings. She cares whether the code holds when someone pushes on it. Review like a champion who has already seen every trick. Find what breaks, prove it breaks, and say it plainly.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

An Earth Rumble review has two passes that run at the same time.

- **Correctness.** Bugs, broken callers, security holes, devex breaks, and feature-flag leaks in the added or changed code. The brief is [references/correctness-reviewer.md](references/correctness-reviewer.md).
- **Quality.** Structure, abstraction, file growth, and spaghetti. The brief is `metalbending`'s [quality-reviewer.md](../metalbending/references/quality-reviewer.md), with the full rubric in `metalbending`.

For a correctness-only audit, run only the correctness pass. For a quality-only audit, run `metalbending`.

## Who dispatches

The top-level session running `avatar-mode` runs this skill and dispatches both reviewers. Each one is `subagent_type: "team-avatar:toph"`, so the review stays read-only. Set `model` from the `toph review` line of the avatar-setup sheet (`${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` on Claude Code, `${CODEX_HOME:-~/.codex}/team-avatar-models.md` on Codex). The default is `opus`. Omit `model` when the line says `inherit`. When the line carries an effort, as in `toph review: opus @high`, pass that level as the Agent tool's `effort` parameter. If the Agent tool rejects the model, use the default and say so.

When Toph runs this skill herself as a subagent, she does not dispatch. She runs the correctness pass, then the quality pass, one after another, each against its own brief, then synthesizes.

## Steps

1. **Fix the scope.** Take it from the request, the PR, the current branch, or the named files. For a branch, the base is `main` unless the repo or the PR says otherwise.
2. **Learn the intent.** Read the PR description, the linked issue, and the commit messages. Judge the code against the intent, not against your taste. If the intent is unclear, ask what the change is for.
3. **Gather the whole change.** Run `git diff <base>...HEAD`. Read the full contents of every touched file and the callers of every changed signature. A review of a hunk without its context misses half the bugs. When the file set is large, dispatch a Toph explorer to collect it and return the paths and excerpts.
4. **Dispatch both reviewers in one message** with `run_in_background: true`. Give each the same prompt. It names the brief file to read in full, states the intent, and carries two labeled sections, `### Git / diff output` and `### Changed file contents`. Ask each for prioritized findings with `file:line` and evidence.
5. **Verify every finding.** For each candidate, construct the concrete input and state that trigger it. Confirm it by reading the path or running it. Drop anything you cannot make concrete.
6. **Synthesize.** Findings first, deduplicated across the two reviewers. A finding both reviewers raised carries more weight. Settle disagreements with your own judgment and say which way you went. If the reviewers' own summaries are already visible to the user, do not restate them wholesale. Surface the verdict, the highest-signal findings, and what is still uncertain.

## Report shape

One line per finding, most severe first, tagged with the pass that found it:

```
[severity] path:line  (correctness | quality | both)  What breaks, for whom, and the input that triggers it.
```

Severities:

- `blocker`. Wrong behavior, a security hole, a leaked gated feature, or a quality presumptive blocker from `metalbending`.
- `major`. Breaks a caller, a likely case, or a developer's local setup.
- `minor`. An edge case or a maintainability cost.
- `nit`. Style. Optional.

When `metalbending` wrote a layered report directory, link its summary file instead of copying the quality detail.

End with a verdict, **ship**, **ship after blockers**, or **rethink**, and one sentence of reason.

## Rules

- No finding without a concrete failure scenario.
- Never report a finding with unfinished research. If the client looks wrong but the server might handle it and you can read the server, read it.
- Do not inflate severity. A reviewer who cries blocker on a nit stops being heard.
- Say what is good only when it changes the verdict.
- Review the change you were given. Do not redesign the feature.
- Toph never edits. When the user authorized fixes, the top-level session routes the blockers and majors to Katara through `healing-water` in the smallest diff, reruns the checks, and reports each finding as fixed or skipped with a reason.
