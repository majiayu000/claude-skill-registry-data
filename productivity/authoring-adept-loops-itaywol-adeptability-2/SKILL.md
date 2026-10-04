---
name: authoring-adept-loops
description: Compose a loop — a scheduled system that discovers work, hands it to agents, verifies with an independent evaluator, persists state, and reschedules itself. Apply when the user wants automation that runs on a timer, a triage/babysitter routine, or asks about `adept loop add`.
allowed-tools: [Bash, Read, Edit, Write]
---


# Composing a loop with adept

A loop is a system that prompts agents so a human doesn't have to: each turn it
**discovers** work, **hands off** to an agent, **verifies** the result, **persists** state,
and **reschedules**. Skip any move and the loop fails a predictable way — no verification is
an agent nodding at itself; no persistence starts from scratch every morning; no schedule is
a script someone forgets to run.

adept manages two of the six parts as canonical, synced resources — **skills** (discovery
knowledge) and **agents** (the generator/evaluator pair). The rest (worktrees, connectors,
memory files, schedules) belong to the harness and repo; this skill tells you how to wire
them together.

## Scaffold the composition

```bash
adept loop add ci-triage --workflow
```

creates:

- `skills/ci-triage/` — discovery skill (triage template: Read → Judge → Write → Hand off →
  Stop). `activation: manual` on purpose: the *automation* invokes it by name; it must not
  auto-fire in normal sessions.
- `agents/ci-triage-reviewer.md` — evaluator agent (adversarial template: assume broken,
  act don't read, PASS/REJECT verdict).
- `.github/workflows/adept-loop-ci-triage.yml` — cloud cron skeleton (only with
  `--workflow`); fill in the harness invocation + auth secret.

Then edit the scaffolds, `adept agent check ci-triage-reviewer`, `adept sync`.

## The five moves, mapped

| Move | Where it lives | adept's part |
|---|---|---|
| Discovery | triage **skill** — what to read, how to judge noise vs. actionable | `adept skill add <id> --template triage` |
| Handoff | one git worktree per finding (`claude --worktree`, Codex background worktree) | skill's "Hand off" section emits the task lines |
| Verification | evaluator **agent**, different instructions (ideally different model) than the maker | `adept agent add <id> --template evaluator` |
| Persistence | `./state/<id>.md` committed to the repo — the agent forgets, the repo does not | skill's "Write" section owns it |
| Scheduling | cloud cron (machine off, ≥1h interval) or local `/loop`/automations (machine on, minute-level) | `--workflow` skeleton |

## Non-negotiables (the parts that produce safety, not output)

- **Independent evaluator.** An agent grading its own work praises it. Keep maker and
  checker separate; tune the checker skeptical; make it verify by *acting* (run tests, click
  the page), and let a stop condition (e.g. Claude Code `/goal`) be judged by a fresh model.
- **The Stop section.** The skill's boundary ("Never merge. Never delete. Uncertain →
  `./inbox/` for a human") is the one thing the loop cannot infer. Leave it out and the loop
  merges with confidence it has not earned.
- **Human review stays.** PRs open, never auto-merge. The pause is a permanent feature, not
  scaffolding to remove once trusted.
- **Cap before you ship.** Per-run budget, daily budget, max retries — set them before the
  first unattended run, because one bug spinning idle overnight otherwise becomes a bill.
- **Grow parallelism last.** Prove the evaluator catches real mistakes on one finding
  end-to-end before letting five agents run at once.

## Four silent costs (watch for them, tell the user)

Verification debt (unreviewed output), comprehension rot (code nobody read), cognitive
surrender (nobody says "this is wrong" anymore), token blowout (retries all night). They
reinforce each other; the guard for all four is a check that can say "no" plus a human who
still reads a sample daily.

See [[authoring-adept-skills]] for the discovery skill's craft, [[authoring-adept-agents]]
for evaluator design, and [[using-adept]] for the CLI. `adept loop add --help` is the source
of truth for flags.
