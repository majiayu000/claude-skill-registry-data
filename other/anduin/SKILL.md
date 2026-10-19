---
name: anduin
description: Use when the user runs /anduin <tracker> <project> [--filter <id-or-query>] [--max N] [--ready] [--dry-run] [--confirm]. The council→forge pipeline as one composite sweep — it rides /glorfindel (plan stage) then /aule (skeleton+forge stage) in sequence over a project, then prints one combined report ending in a plain STIRRED/QUIET verdict. The forge stage runs UNATTENDED BY DEFAULT (--auto --max 3); pass --dry-run or --confirm to gate it. Sequential by construction, so the two stages never contend. Run it alone for a single pass, or wrap it in /amon-sul anduin … for an adaptive, single-timer watch of the whole pipeline.
purpose: Runs the council-then-forge pipeline as one composite sweep over a tracker project.
user_invocable: true
stage: vigil
composes: glorfindel:dispatch, aule:dispatch
---

# Anduin — The Great River

Anduin, the Great River, ran the length of the land from the Misty Mountains to
the Sea, carrying all things downstream on one current. So this skill: it carries
a project's tickets down the one channel from council to forge — Glorfindel rides
the plan stage, then Aulë rides the skeleton-and-forge stage — in a single pass,
on one current, never two boats jostling.

## Ethos

- **One channel, two stages, in order.** Anduin runs the council sweep first, the
  forge sweep second, within one invocation. Because they take turns under one
  call, they never run concurrently and never contend — the cure for "two watches
  fighting" is sequence, not merger.
- **Anduin conducts; the riders still ride.** Anduin posts nothing and forges
  nothing of its own. Every comment, verdict, state change, and PR is Glorfindel's
  or Aulë's doing, gated exactly as those skills gate them. Anduin only orders the
  two and sums their reports.
- **The decider sorts the tickets.** Both stages sweep the same scope; the
  skeleton-rung decider gives each ticket exactly one action, so Glorfindel acts on
  plan-rung tickets and Aulë on skeleton/forge-rung tickets. No ticket is claimed
  twice in one pass.
- **A single pass, not a loop.** Anduin sweeps once and reports. The adaptive
  cadence is `/amon-sul`'s to provide — `/amon-sul anduin …` rides Anduin on the
  back-off ladder with one wakeup slot, so the whole pipeline watches itself
  without two schedules colliding.

## Argument parsing

`/anduin <tracker> <project> [--filter <filter>] [--max N] [--ready] [--dry-run] [--confirm]`

| Argument | Required | Meaning | Stage |
|---|---|---|---|
| `<tracker>` | yes | `youtrack` (alias `yt`) or `jira` | both |
| `<project>` | yes | Project shortName / key (e.g. `URD`, `MET`) | both |
| `--filter <filter>` | no* | Tracker-aware scope, same semantics as `/glorfindel` | both |
| `--max N` | no | Forge cap per pass. **Default 3** (≤10). | forge only |
| `--ready` | no | Open PRs ready-for-review (default draft). | forge only |
| `--dry-run` | no | Plan/report only; post nothing, forge nothing. Opts the forge **out** of auto. | both |
| `--confirm` | no | Prompt before each council post and each PR-open. Opts the forge **out** of auto. | both |

> **The forge runs unattended by default.** Anduin gives the forge stage
> `--auto --max 3` unless you pass a gate flag. So bare `/anduin youtrack URD`
> (or `/amon-sul anduin youtrack URD`) **opens real PRs with no further prompt**,
> up to 3 per pass. To watch without forging, pass `--dry-run`; to forge with a
> per-PR prompt, pass `--confirm`. There is no `--auto` flag to type — it is the
> default; the gate flags are how you turn it *off*.

Anduin parses these once and routes them to the two riders:

- **Council (`/glorfindel`)** receives `<tracker> <project> --filter <filter>`, plus:
  - **No gate flag given** → append `--auto`. On Jira this skips Glorfindel's post-safety prompt so the council ride runs unattended; on YouTrack it is a harmless no-op (no such gate). This is what keeps the **Jira** pipeline hands-off — without it, the council stage would halt at its post-safety prompt every tick.
  - **`--dry-run` given** → append `--dry-run`. Plans, posts nothing.
  - **`--confirm` given** → append `--confirm`. Prompts before each post.
  - It ignores `--max` / `--ready` (forge-only).
- **Forge (`/aule`)** receives `<tracker> <project> --filter <filter>`, plus:
  - **No gate flag given** → append `--auto --max <N, default 3>` and `--ready` if set. The forge runs unattended.
  - **`--dry-run` given** → append `--dry-run` (and `--max` / `--ready` if set). No `--auto`. Nothing forges.
  - **`--confirm` given** → append `--confirm` (and `--max` / `--ready` if set). No `--auto`. Each PR-open prompts.

  `--dry-run` and `--confirm` are mutually exclusive with the default auto, and with each other (`--dry-run` wins if both somehow appear). They are the only way to disable unattended operation on either stage.

*Filter resolution follows `/glorfindel`'s rule — explicit `--filter` wins; else
`default_filters.md` keyed by `<tracker>:<project>`; else stop with that skill's
missing-filter error.

### The filter must straddle Open *and* In Progress

This is the one trap of the pipeline. Council transitions an approved ticket to
its `forth` state (for URD, `In Progress`) — which **drops it out of a
`state:Open` filter**. If both stages share `--filter state:Open`, the forge stage
never sees the ticket the council just approved, and the pipeline stalls at the
skeleton rung.

Use a filter that includes both, so the same scope feeds both stages and the
decider sorts each ticket to its rung:

- **YouTrack:** `--filter "#Unresolved"` (every non-resolved state), or an explicit
  `--filter "state: Open, {In Progress}"`.
- **Jira:** `--filter "statusCategory != Done"` (or an explicit `status in (Open, "In Progress")`).

If the resolved filter is `state:Open` (or any single-state scope that excludes the
`forth` state), warn the user once that the forge stage will not see council-advanced
tickets, and suggest the broad filter above. Proceed if they confirm; the council
stage still works, only the hand-off stalls.

### On Jira

Both stages support Jira — Anduin passes `<tracker>` straight through. Two
differences from YouTrack to know:

- **Two rungs by default, three on request.** On Jira the default flow is council →
  forge directly: Glorfindel drafts `[COUNSEL vN]`, the human posts `[FORTH]`, and
  Aulë forges on `[COUNSEL]+[FORTH]`. The skeleton rung is opt-in there — started by
  `/celebrimbor jira <project> --ticket <id> --skeleton`, never by a sweep — and once
  a `[SKELETON]` stands, Aulë routes the ticket by `jira-skeleton-rung.py` and forges
  only after the skeleton's own `[FORTH]`. Anduin sequences the stages the same way.
- **Unattended is smoothed by `--auto`.** Glorfindel and Aulë each guard Jira with a
  post-safety prompt; Anduin's default appends `--auto` to **both** stages, so an
  unattended `/anduin jira PSG` (or `/amon-sul anduin jira PSG`) runs hands-off
  rather than halting at those prompts each tick. Pass `--dry-run` / `--confirm` to
  put the guards back. State mapping and filters use Jira's vocabulary (numeric
  transition IDs for `forth` / `forged`; JQL for the filter).

## Workflow

### 1. Ride the council (Glorfindel)

Invoke `/glorfindel` through the Skill tool with the gate flag resolved per the
defaulting rule above:

- **No gate flag** → `/glorfindel <tracker> <project> --filter <filter> --auto` — unattended (the `--auto` skips Jira's post-safety prompt; no-op on YouTrack).
- **`--dry-run`** → `/glorfindel <tracker> <project> --filter <filter> --dry-run`.
- **`--confirm`** → `/glorfindel <tracker> <project> --filter <filter> --confirm`.

Let it do its whole job — list, per-ticket council machinery, post `[PLAN]` /
`[COUNSEL]` / refine, transition on `[FORTH]`, and its own aggregate report. Hold
that report.

### 2. Ride the forge (Aulë)

Then invoke `/aule` through the Skill tool with the forge flags resolved per the
defaulting rule above:

- **No gate flag** → `/aule <tracker> <project> --filter <filter> --auto --max <N|3> [--ready]` — unattended forging, the default.
- **`--dry-run`** → `/aule <tracker> <project> --filter <filter> --dry-run [--max N] [--ready]`.
- **`--confirm`** → `/aule <tracker> <project> --filter <filter> --confirm [--max N] [--ready]`.

Let it do its whole job — list, rung-dispatch each qualifier to `/celebrimbor`
(skeleton or forge), close any already-forged ticket whose PR/MR has merged (step
5b — move to the `merged=` state, thread a `[METTA]` note), its gate, and its
aggregate report. Hold that report.

Council first is deliberate: a plan or skeleton approved earlier this pass is
transitioned and ready, so the forge stage can pick it up in the **same** pass
rather than waiting for the next.

### 3. Combined report and verdict

Print one block carrying both stages' summaries verbatim-in-spirit (do not
re-run either), then a final plain verdict line the watcher can read:

```
**Anduin — pipeline pass of <tracker>:<project>**

— Council (Glorfindel): <one-line tally from its report>
— Forge (Aulë):        <one-line tally from its report>

Anduin — STIRRED   (or)   Anduin — QUIET
```

Decide the verdict:

- **STIRRED** if *either* stage produced anything beyond its quiescent outcomes:
  - Council stirred if any ticket read `drafted`, `answered`, `dry-run`, `forth`,
    `forged`, `nay`, `farewell`, `talked-out`, or `error` — i.e. anything other than
    `quiet` / `untouched`. (`answered` is real movement — Erestor posted a `[PEDO]`
    reply — even though the plan itself did not redraft.)
  - Forge moved if any ticket read `forged`, `closed`, `aborted`, `answered`,
    `dry-run`, or `error`, **or** qualifiers remain for the next forge pass. Aulë's
    outcome vocabulary carries no `skeleton-drafted` state — a skeleton-rung dispatch
    that succeeds reports `forged` like any other; `aborted` counts as movement too,
    since it is retryable work still waiting, not silence. A `closed` outcome — Aulë
    laying a merged ticket to rest — is movement as much as a forge is.
- **QUIET** only when neither of the above held — council reported nothing but
  `quiet` / `untouched` (or swept nothing), and forge reported none of `forged`,
  `closed`, `aborted`, `answered`, `dry-run`, or `error`, with zero qualifiers
  remaining.

The verdict line is the contract `/amon-sul` reads to set its streak. Always emit
exactly one of the two tokens.

## Rules

- **Anduin never posts, transitions, or forges of its own.** It only orders the two
  riders and sums their reports. Every write is Glorfindel's or Aulë's.
- **Sequential, always.** The forge sweep begins only after the council sweep
  returns. Never dispatch them in parallel — the sequence is the whole point.
- **Forge blast radius is the default, by design.** Unlike `/aule` — where `--auto`
  must be typed — Anduin forges unattended *unless gated*. Bare `/anduin` opens up
  to `--max` (default 3) real PRs per pass, and `/amon-sul anduin …` does so every
  tick the road stirs, with no flag in the invocation to signal it. This is the
  chosen default; the brakes are `--dry-run` (forge nothing) and `--confirm`
  (prompt per PR). Prefer a `--dry-run` pass first to see what would forge before
  arming an unattended watch.
- **One pass per invocation.** Anduin does not self-schedule. For a loop, wrap it
  in `/amon-sul anduin …`; the watcher owns the cadence and the single wakeup.
- **A stage error does not sink the other.** If the council sweep errors, still ride
  the forge (it reads the tracker afresh); if the forge errors, the council's posts
  already stand. Record both outcomes in the combined report.
- Do not surface tracker or forge tokens in logs, responses, or saved files.
