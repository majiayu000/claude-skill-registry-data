---
name: agni-kai
description: Zuko's Agni Kai for bakeoffs. The formal firebending duel, where competing implementations fight under the same rules and a judge declares the winner. Use for arena, /arena, "arena this", "throw it in the arena", "bakeoff", or when one attempt at a nontrivial design or artifact would lock in the wrong shape. Spawns N parallel candidates at the same task, picks a base with a cross-judge, and grafts the strongest parts of the losers into it.
---

# Zuko's Agni Kai

An Agni Kai has rules. Both duelists face the same ground, under the same sun, and a witness declares who won. Zuko learned the hard way that the fight you walk into unprepared is decided before it starts. A bakeoff is the same. Every candidate gets the same task, a judge scores them against a rubric written before the fight, and the winner absorbs the best moves of the ones it beat.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before you launch anything. Only the top-level session dispatches. When you run as a dispatched character, produce the candidates yourself, one after another, judge them yourself against the rubric, and say that the duel had no independent judge.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate produces.
2. Derive the rubric. Write 3 to 6 concrete, gradeable criteria for what success looks like on this task. The rubric is the picker's tool in Phase D. Candidates see only the task, never the rubric. If a criterion is a measured number, vet it with `steady-flame`.
3. Pick the runners from the `panel` line of the avatar-setup sheet (`${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` on Claude Code, `${CODEX_HOME:-~/.codex}/team-avatar-models.md` on Codex). If the sheet or the line is missing, run one each on the defaults in [Models](#models). An `inherit` entry means the parent model, so omit `model` for it.
   - Dispatch each runner as the character whose discipline fits the artifact (`team-avatar:sokka` for a design, `team-avatar:appa` or `team-avatar:katara` for code, `team-avatar:iroh` for prose), with `model` set from its panel entry.
   - If the Agent tool rejects a configured entry, run that seat on its family's default and say so. Families go by model name, such as Opus, Fable, or Sonnet. With no family match, use Zuko's line from the sheet. If the tool rejects a default, use the closest valid name of the same family from its error message.
   - Spawn more runners when the duel covers several design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive.
   - Set each runner's effort as [Reasoning effort](#reasoning-effort) describes.
4. Give each candidate its own output location, a git worktree where possible and otherwise `/tmp/agni-kai-<slug>/candidate-<n>/`, so no two candidates share a file.

## Phase B: Fan out

Spawn all N candidates in one message with `run_in_background: true`. Each brief carries the task, the path to the shared grounding, its own output path, and instructions to produce the artifact plus a short rationale naming the alternatives it considered and what it rejected.

If a candidate produces no output, proceed with N minus 1 and note the dropout.

## Phase C: Cross-judge

After every Phase B candidate completes, choose one model from the `panel` line (or the defaults in [Models](#models) when the line is missing). Prefer a different model family from the parent's. Dispatch one read-only judge as `team-avatar:toph` on that model. Toph sees the rubric and the candidates by path label, scores each criterion, and recommends a base with a rationale. She runs while you read in Phase D. Never spawn her while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before you pick. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or the smaller API (Laziness Protocol, Air in `four-elements`).

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base. That is usually one or two things per candidate, not most of it. Fold each graft in by hand so the result stays coherent under one mental model (Redesign from First Principles, Water in `four-elements`). Do not paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was underspecified. Reframe and run the duel again rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output (Prove It Works, Earth in `four-elements`). If verification finds a problem the duel missed, either Phase A was wrong (reframe and rerun) or a candidate caught it and you missed the graft (go back to Phase E). Do not paper over it.

## Output

One synthesized artifact, with a short synthesis note beside it. The note names the base and why, the judge's verdict, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.

## Models

Runners and the judge both draw from the `panel` line. Its default, used when the sheet or the line is missing, is `opus`, `fable`, `sonnet`, `haiku`.

## Reasoning effort

A panel entry may carry an effort after its model, as in `opus @high`. Levels on Claude Code are `low`, `medium`, `high`, `xhigh`, and `max`. Which ones apply depends on the model. An entry without `@` takes the sheet's `default effort` line, and `session` when the sheet has no such line. `session` sets no effort, so the dispatch is the usual one. Strip the suffix before reading the model. On Claude Code, pass the level as the Agent tool's `effort` parameter. On Codex, pass it as `spawn_agent`'s `reasoning_effort`. Raise a seat one step for the hardest or subtlest work, and lower it for routine generation, but keep each seat's model so the panel stays diverse.
