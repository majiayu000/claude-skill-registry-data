---
name: battle-map
description: Sokka's battle map, the decision trail he keeps so anyone can see how the campaign was won. Use for show-me-your-work, /show-me-your-work, "show me your work", "keep a decision log", "audit trail", long or unattended runs, multi-phase work, or anything a human reviews after stepping away. Keeps one TSV row per decision (what, why, evidence, result), local by default and committed when a reviewer needs it to trust the result.
---

# Sokka's battle map

Sokka marks every move on the map as it happens. Where the team went, why, and what they found there. When someone walks into the tent hours later, the map tells them the whole campaign without a word from him. Keep one map, and keep it honest.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## The format

One TSV file, one row per decision. Cells stay on one line. Evidence is a pointer, not prose.

Copy [references/decision-log-template.tsv](references/decision-log-template.tsv) (the header row) to start a clean log. The columns:

- **ts.** ISO 8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, in one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly, not as a jargon tag.
- **evidence.** A link or path that proves it. A commit SHA, a PR number, a `file:line`, or an artifact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or the predicate state, such as `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, or `open`.

An example, plain-spoken so a reviewer reads it at a glance.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Log a row

Write each row the way you would tell a teammate what you did. Plain words, concrete actions, no AI speak or abstract jargon. The rules in `tea-time` apply to log text too.

Use the helper:

```sh
bash scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
```

The path is relative to this skill's folder. The script stamps `ts`, writes the header on first use, strips stray tabs and newlines, and prefixes any cell that starts with `=`, `+`, `-`, `@`, or `"` with a single quote, so a spreadsheet never runs a cell as a formula. It writes each row in one system call when `perl` is available, so parallel writers do not interleave rows. A bare `printf` that appends a row works too. Mind the same bytes when cells come from generated or user-supplied text.

Log decision points and checkpoints, not every action:

- A fork chosen.
- A unit completed, with its verification result.
- A pivot or revert, with its trigger.
- A blocker surfaced.
- A gate fixed.

For loop runs, log one row per iteration. Skip the trivial and the self-evident.

## Runs and start rows

A run is one agent conversation, including its later turns and any summary of it. A pickup, a replacement agent, or a new chat starts a new run.

When a run adds to a log that already has rows, its first row has phase `start`. So does its first row after another run's `start` row. A run that comes back to a log in a later turn first reads the log's last rows to see whether another run wrote since. A `start` row names the `ts` range of the earlier rows this run did not write. Its evidence names this run, such as its agent id. Use phase `start` for nothing else.

## Where it lives

By default the log is a working artifact and stays out of git. Keep it at `decisions.tsv` in the work dir, or at `.audit/<task-slug>.tsv` when several efforts run at once.

Commit it only when the work is ambitious enough that a reviewer needs the trail to trust the result.

## Rules

- Append only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence that committed scripts produce over hand-made one-offs (Encode Lessons in Structure, Fire in `four-elements`).

## Audit the log against the transcript

At the end of the run, before you hand back, check that the log told the truth. Read this run's own transcript and nothing else.

- **Claude Code.** The per-project transcripts directory, `~/.claude/projects/<encoded-cwd>/`, where `<encoded-cwd>` is the working directory with `/` replaced by `-`. Do not glob across `~/.claude/projects/`. That reads unrelated private chats.
- **Codex.** This session's rollout file under `${CODEX_HOME:-~/.codex}/sessions/`. Open only this session's file.

Walk this run's rows against what actually happened. Each stretch of this run's rows begins at one of its `start` rows, or at the first row if this run created the log. It ends at the next `start` row of another run.

- Check that every row maps to a real decision or action.
- Check that each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but is not logged is a gap. Add it.

Correct the log, not the story. The audit never edits or removes a row, even an invented one. When a row records neither a real decision nor a real action, or its claim or evidence is wrong, add a row that supersedes it with what actually happened and a pointer that resolves. This audit does not check rows outside this run's stretches. If this run's own work shows one of them is wrong, supersede it like any wrong call.

## Cross-model review of the trail

Before you hand back, dispatch Toph (`subagent_type: "team-avatar:toph"`) on a model family different from the one that did the work. Pick that model from the `panel` line of the avatar-setup sheet. Self-review is no substitute. Pick the reasoning effort for the job as `avatar-mode` describes. Toph reads the trail and this run's transcript, then flags what the user should pay attention to. She does not redo the work. She scans for what is weak or risky.

- Decisions logged with weak or absent evidence.
- Verification steps skipped, or claimed without proof in the transcript.
- Choices that look risky in hindsight (premature, scope-creeping, papering over a symptom).
- Gaps the user would miss on a casual skim.

When this skill runs inside a character that is itself a subagent, that character does not dispatch. It does the scan itself in a separate pass, labels the review as same-model, and says so in the reply.

Every reply for a run that produced a trail ends with an "Attention" section. Lead with the reviewer's model on its own line (`reviewed by <model>`), then list each flag with the rows or moments it points to. "No flags" is a valid value. The model name is not optional.

## Read the trail

Read top to bottom, follow the evidence pointers, and spot-check. GitHub renders a committed TSV as a table. In a terminal, run `column -s$'\t' -t decisions.tsv`.

## Composing this skill

Other skills route their audit trail here instead of inventing one. Name `battle-map` and let it own the format. Do not restate the columns.
