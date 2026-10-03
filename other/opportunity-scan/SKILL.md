---
name: opportunity-scan
description: Propose two or three pieces of work the user could own end to end, instead of threads to reply to. It starts from the metrics leadership watches (themes, OKRs, planning docs, meeting notes such as Granola), then sweeps the org's connected surfaces (chat, tickets, docs, PRs, meeting notes) over the last month for recurring pain, silent degradation, ownership gaps, unanswered invitations, metric gaps and leadership priorities, adds the problems /flagrare:impact-scan handed off, checks that nobody already owns each one, keeps only work that moves a named metric and that the user's seat can move, and ranks it by impact and against the user's promotion map (what they want more and less of, which open rubric row it closes, who cares and whether they have seen the user's work, whether it can land before the target cycle). Each proposal comes with evidence links, a hypothesis and success metric set before building, the smallest first step, and a short pitch for the manager that fits how the company decides. Keeps at most one initiative active, and only after manager alignment. Runs about monthly. Use when the user says "opportunity scan", "what should I own", "what could I lead", "find me a project", "what problem should I pick up", "what would move the needle", "I want to own something end to end", or asks for work that would show next-level scope. Also trigger from /flagrare:career when the scan is due.
---

# Opportunity Scan

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook. See `/flagrare:write-docs`.

> **Plain words.** In anything the user reads, use the plain names in `<plugin root>/lib/career/GLOSSARY.md` ("Senior behaviors", not "rubric rows"; "your written case", not "packet"; "the project you own", not "initiative"). The first time a term appears, say what it means in a few words and add the company's own word in parentheses when the user will hear it at work.

Impact-scan finds threads to weigh in on. The next level asks for more: finding a problem nobody assigned, and owning it through to a result someone can measure. This skill looks for those problems on purpose, checks nobody already owns them, and brings back two or three proposals the user could take to their manager.

The failure modes it must never enable:
- **Grabbing someone else's work.** A problem already owned is not an opportunity. The owner check runs before anything is proposed, and a proposal that skipped it is cut.
- **Going around the people who decide.** A proposal fits how the company makes decisions: if a PM drives the decision document, the first step feeds evidence into that document, never a competing one.
- **Pitching on a guess.** Every claim in a proposal has a link, or is marked as a check to run first.
- **Spreading thin.** At most one initiative is active, and it only counts as the user's after their manager agrees.
- **Busywork dressed as a project.** A fix that moves no metric the company watches, or that someone will do anyway, is not worth owning. Every proposal names the metric it moves, its baseline and a target, the way a product engineer frames a bet; anything that can't goes on a short "fixes worth mentioning" line instead.

**This skill never posts, sends, or publishes anything.** Sweeps are read-only, and the pitch is a draft for the user.

## Library and state

Helper scripts live at `<plugin root>/lib/career/`, where the plugin root is two directories above this skill's base directory. Run them as `python3 <plugin root>/lib/career/<script>.py ...`. They only read and print JSON. Write every state file with the Write tool, reading it first if it exists: a sandboxed shell cannot write under `~/.claude/skills`.

- `initiatives.py context --home "$HOME" --today <YYYY-MM-DD>`: everything the ranking reads (see step 1).
- `initiatives.py propose --home "$HOME" --today <date> --id <slug> --title "<plain words>" --evidence <link> [--evidence <link> ...] --proposal '<json>'`: plans `initiatives.json` with a proposal.
- `initiatives.py status --home "$HOME" --today <date> --id <slug> --status <status> [--aligned-with "<who>"] [--note "<why>"]`: plans one status change.
- `initiatives.py run --home "$HOME" --today <date>`: plans `opportunity-state.json` with this run's date.

A script that refuses (exit code 2) prints the reason; tell the user in plain words and do not work around it. The state files' shapes are in `<plugin root>/lib/career/STATE.md`.

## Setup (every run)

1. **Load state.** Run `python3 <plugin root>/lib/career/career_state.py plan --home "$HOME"` and apply each `write` action with the Write tool, reading the target first if it exists. **Never delete anything.**
2. **Config.** Read `~/.claude/skills/flagrare/config.json`. This skill sweeps the same surfaces as impact-scan and reuses its onboarding: surfaces, domains, target behaviors and audience come from `skills["impact-scan"]` (or the older `skills["senior-scan"]`). If neither block has `onboarding_complete: true`, run the onboarding in `<plugin root>/skills/impact-scan/SKILL.md` (identity, career target, domains, surfaces; skip voice and board if the user wants to move on) and save it under `skills["impact-scan"]`. This skill's own block, `skills["opportunity-scan"]`, holds `cadence_days` (default 30) and, optionally, `weights` for the ranking (step 4).

## Workflow

**Called by `/flagrare:career`.** When the arguments say this run comes from the career coordinator, run only when `due`, and end at the proposals digest without the closing question; the coordinator asks once at the end, and when the user answers about a proposal, record it with step 6. Before returning, in both interactive and scheduled runs, record every proposal that is not already in `initiatives.json` as a candidate with one sighting (`python3 <plugin root>/lib/career/career_state.py candidate --home "$HOME" --id <slug> --title "<problem>" --evidence <its strongest link> --today <date> --details '<json>'`, where the details are the drafted `problem`, `hypothesis`, `metric`, `baseline`, `target`, `lever`, `first_step`, `pitch`, `owner_check` and the step 4 `score`, so the board can show and rank them while the user decides; reuse the id of a handed-off candidate or a dismissed problem instead of making a new one), so the proposals survive until the user decides, then run `initiatives.py run` and write `opportunity-state.json` with the Write tool so the cadence counts from today. When the arguments also say `scheduled`, never ask anything. Keeping, dismissing and activating always wait for the user.

### 1. Context and cadence

Run `initiatives.py context`. It prints:

- `has_map`, and from the promotion map: `target` (`target_level`, `cycle`, `why`, `more_of`, `less_of`), `open_rows` (rubric rows not yet done), `unseen_people`, `decision_process` (`artifact`, `usual_driver`), and `packet_deadline`. `more_of` and `less_of` are lists by design; for the single-valued facts (`target_level`, `cycle`, the `decision_process` fields, `packet_deadline`), a list means the map's sources disagree: show every option, never pick one.
- `initiatives`: the `active` one (or null), `proposed` and `candidates` (each ranked: highest score first, unscored last, with `rank` `{total, max, is_fix}`) and `dropped` (each with `seen_again`: seen since it was dismissed).
- `cadence`: `last_run`, `days_since`, `cadence_days`, `due`, `next_due`, and `window_start`, the first day to sweep (the last run, or 30 days back the first time, never more than 90 days back).
- `fallback`: the impact-scan config's `target_behaviors`, `domains` and `audience`.
- `priorities`: the company's themes and the metrics leadership watches, from the promotion map, each with `metric`, `baseline`, `target`, `owner_team` and `user_lever` (`owner` when the user's seat owns the metric's main input, `input` when their systems feed it, `none` when the lever sits in another team).

**Cadence.** When the user asked for this scan, run it even if it is not due. When `/flagrare:career` or a schedule started it and `due` is false, stop and say when it is next due (`next_due`).

**Without a map** the scan still runs. Ranking uses the configured target behaviors and domains; the "which open row" and "before the target cycle" factors are skipped; the first step defaults to bringing the problem to the manager. Say once, in the digest header, that `/flagrare:promotion` would sharpen the ranking.

**With an active initiative**, open the digest with a one-line check-in on it (what the last evidence shows, and whether it looks done). New proposals are still made, but none can become active until the current one is done or dropped.

### 1b. Metrics first (before the sweep)

Build the list of metrics this scan ranks against before looking at any finding, so impact decides the ranking instead of breaking ties.

- Start from `priorities` in the context.
- Add what the docs say leadership watches now: themes and strategy documents, OKRs, squad plans, launch posts with numbers. Search the docs surface for them first, before ranking; this search can run in the same message as the sweeps, but finish the list before step 4.
- Add what meeting notes say (when a meeting-notes surface is configured): priorities stated in planning meetings, all-hands and 1:1s with the user's manager.

For each metric, write one line: the metric, its baseline with a source (or `Check first:` and where the number lives), the team that owns it, and the user's lever from their seat (`owner`, `input` or `none`, judged from their domains and the systems they work in). Keep it to the five or six that matter most.

### 2. Sweep

Spawn **one read-only sweep subagent per configured surface** (including a meeting-notes surface such as Granola, when configured), all in the same message so they run concurrently, over `window_start` to today. Each gets its surface's scope, the domain map with keywords, the exclusions and the user's identity. Sweeps never post, react or comment.

Every sweep hunts the same five signals:

- **Recurring pain:** the same question asked again, repeat incidents with one cause, support toil, a manual step people keep doing by hand.
- **Silent degradation:** something getting slower, flakier or more expensive with nobody assigned (a flaky test everyone reruns, an alert everyone mutes, a metric trending the wrong way).
- **Ownership gaps:** a new integration or partner nobody supports, a team missing a skill it needs, work orphaned by a reorg or a departure.
- **Unanswered invitations:** "someone should look at this", "would love help with", a proposal waiting for a volunteer.
- **Leadership priorities:** themes documents, OKRs, planning docs, a new leader's stated focus. Search the docs surface for them; they tell you which problems will be noticed.
- **Metric gaps:** a metric from step 1b that is off target or unmeasured where the user's systems are an input (a partner-facing number nobody tracks, a funnel step that leaks, a complaint rate leadership quotes).

From meeting notes, take priorities, decisions and problems people raised; never quote what someone said about another person, and never surface private remarks.

Each finding comes back as: the problem in plain words, every evidence link, who is affected, who has talked about it, which metric from step 1b it touches (if any) and any number that sizes it, and any sign of an owner (an assignee, a ticket in progress, someone saying "I'm on it", a roadmap or planning doc that already schedules it).

Add the `candidates` from `initiatives.json` (the problems impact-scan handed off) to the findings, and any `dropped` item with `seen_again: true`, marked as dismissed before.

### 3. Owner check (hard filter)

For every finding, check whether someone already owns it before ranking it:

- search open tickets for the problem's keywords and linked incidents;
- search open PRs touching the systems involved;
- read the latest messages in the thread or channel where it was raised.

Record what you checked in one sentence (it becomes the proposal's `owner_check`). If someone owns it, or a roadmap or planning doc already schedules it (it will be done anyway), cut it and name the owner or the plan on the digest's **Cut** line; if the owner has gone quiet for weeks, it can stay, as "offer to help or take over", never as the user's own. A finding you could not check is cut too, with the reason.

### 4. Rank

Three more hard filters first:

- **No metric:** a finding that moves no metric from step 1b is not a proposal. If it is still worth fixing, it goes on the digest's "Fixes worth mentioning" line, one short line each.
- **No lever:** when the metric's lever sits in another team (`user_lever` `none` and nothing in the user's seat feeds it), it goes on the "Offer to help" line with the owning team, never as the user's own project.
- **Small or scheduled:** a fix a teammate would do in their normal work this month, or one already on a plan, is cut with that reason.

Then score each survivor 0-2 on these factors (the key in parentheses is the name the score is stored under). Impact counts double, so the most is 18:

- **Impact (`impact`, x2):** how much the metric would move, sized from a number with a source (orders, partners, revenue, a complaint rate). A guess with no number scores 0 and gets a `Check first:` for where the number lives.
  Size it with `/flagrare:measure-impact` (`before <the problem's strongest link> quick nosave called by /flagrare:opportunity-scan`), only for findings that survived the hard filters, at most the top 3: its baseline, or its comparable scaled by the right base, with the confidence level, is the impact reason. A baseline it reports as unknown scores 0 here and carries its `Check first:`. Nothing is saved at this point.
- **Lever (`lever`):** the user's seat owns the input (2), feeds it (1).
- **Fit (`fit`):** it matches what the user wants more of, and is not something they want less of (with no map: their configured target behaviors).
- **Rubric (`rubric`):** it closes one of the `open_rows`; pick the row from `open_rows` only, never invent one (no map: skip, score 1).
- **Who notices (`who_notices`):** people who would notice the result, with extra weight when they are in `unseen_people` (with no map: the configured `fallback.audience`).
- **Standing (`standing`):** the user knows the area (one of their domains, systems they have worked in).
- **Evidence (`evidence`):** how often it came up and from how many places; a handed-off candidate with `seen_count` 2 or more starts at 2.
- **Timing (`timing`):** it can show a result before the `packet_deadline` (no map or no deadline: skip, score 1).

Write each score down with a one-line reason, as `score` in the proposal: `{"impact": {"value": 2, "why": "about 300 partners a month ask where their money is"}, ...}`. The reason names the number, person or link behind the value, so the user can argue with it. The library adds the total and sorts by it (`rank` in `context`: `total`, `max`, and `is_fix` when impact is 0), and the board shows the ranking with each reason. A user who weighs factors differently sets `skills["opportunity-scan"].weights` (whole numbers 1 to 3 per factor, for example `{"fit": 2}`), and the library applies them; never re-weigh by hand.

Drop anything scoring 0 on Impact, Standing or Evidence. Keep the top 3. Fewer than three good ones is a fine result: say so instead of padding with small fixes.

**Rank the ones already waiting too.** Candidates and earlier proposals without a `score` (the `rank.total` in `context` is null) get scored the same way in this run, so the board's ranking covers everything on the table. Record them with `career_state.py candidate --details` (a candidate) or `propose` (a kept proposal), adding the `score` and keeping every field already there.

### 5. Proposals

The digest is short: the user should know what each proposal is from its first line.

```
## Opportunity scan: <date>, window <window_start> to <today>. <caveats: surfaces skipped, no map, not due but run on request>
<one line on the active initiative, when there is one>
<Still on the table: each earlier `proposed` item, one line each with its title and when it was proposed, when there are any>

### 1. <the outcome, for whom: "Partners understand what they earned", not "Fix the payout page">, <total> of <max>
**Moves:** <metric> from <baseline, with its source> to <target> by <date, the written case's deadline when there is one>. **Your lever:** <what in your seat moves it>.
**Evidence:** <links, each with three words on what it shows>
**Owner check:** <what was searched, in one sentence, and who owns it, if anyone>
**The bet:** We believe <change> will <result> because <reason>. **Success:** <how the metric is measured, decided before building>. (<rubric row id>, only with a map)
**Rough impact:** <who gets what, in numbers where you have them>. **Who cares:** <people or teams, and why now>.
**First step:** <the smallest step, fitted to how decisions are made>
**Pitch for your manager:** <three sentences at most, in the user's voice>

(repeat, at most 3)

**Offer to help:** <finding: the owning team, and what you'd bring>; ...
**Fixes worth mentioning:** <small fix: one line>; ...
**Cut:** <finding: reason (owned by X, already planned, could not verify, no standing)>; ...
```

Rules:

- **Fit the local decision process.** When `decision_process.usual_driver` is a PM or product role, the first step feeds evidence to them for their `artifact`, and the pitch offers to own the engineering side. When it names engineering, the first step can be a short written proposal. Without a map, the first step is bringing it to the manager.
- **Nothing on an unchecked claim.** Numbers and causes in a proposal come from a link. When one is missing, write `Check first:` with the single check instead of the claim.
- **The hypothesis comes before the build.** A proposal without a success metric is not ready: say what data would show it worked, and where that data lives.
- **Scope to what the user controls.** The target is the part of the metric the user's work can move. When a bigger change upstream decides the rest (a platform migration, another team's launch), say so and aim at what is reachable.
- **Plain words.** No ticket keys or channel ids in the headline; they go in the evidence links. Rubric row ids go in parentheses after the hypothesis, only with a map.
- **Pitch in the user's voice.** Read `~/.claude/skills/flagrare/career/voice.md` when it exists. First person, no preamble, no flourish.

Earlier proposals the user kept but has not started stay on the "Still on the table" line, not in the three new slots; ask whether any is now agreed with the manager or should be dropped.

Stop after the Cut line. Ask which proposals to keep, which to dismiss, and whether any is already agreed with their manager.

### 6. Record

After the user answers, write each change with the Write tool, one script call at a time (each reads the file the previous one wrote):

- **Keep:** `initiatives.py propose` with the fields below. Start from the candidate's `draft_proposal` when it has one, draft any required field it lacks (`pitch` and `lever` often are), carry its `score` over, and show the user the full proposal before recording it. For a handed-off candidate, reuse its id so its sightings carry over. For a problem the user dismissed before, compare this run's findings with the `dropped` entries in step 2: when the user keeps one that has not been seen since it was dismissed, run `status --status candidate` first, then `propose`.
- **Dismiss:** for an item already in `initiatives.json` (a handed-off candidate, an earlier proposal, a dismissed problem seen again), `initiatives.py status --status dropped --note "<why, in the user's words>"`; it will not come back unless it is seen again. A new finding from this run that the user dismisses is simply not recorded (under the coordinator it was already recorded as a candidate, so dismiss it through the script like any other entry). A handed-off candidate the user neither keeps nor dismisses stays a candidate and comes back next run.
- **Agreed with the manager:** keep it first (`propose`, if it is not already proposed), then `initiatives.py status --status active --aligned-with "<who>" --note "<where or how it was agreed>"`. Only a proposal can become active, only one at a time, and never without the user saying their manager agreed. Do not suggest skipping that conversation. Then save its bet: run `/flagrare:measure-impact` with `before <the proposal's strongest evidence link> quick called by /flagrare:opportunity-scan`, reusing the proposal's `metric`, `baseline` and `target`, so the bet is followed after launch. Kept proposals are not saved, so the ones never started do not come back as bets waiting for a launch.
- **Finished or abandoned** (when the user says so later): `--status done` or `--status dropped`.
- **Bring back a dismissed problem** that has not been seen again (only when the user asks): `--status candidate` first, then `propose`.

The `--proposal` JSON holds: `problem`, `hypothesis`, `metric`, `impact`, `who_cares`, `why_now`, `first_step`, `pitch`, `owner_check`, `lever` (what in the user's seat moves the metric), `baseline`, `target`, `by`, `decision_fit` (how the first step fits the decision process), `score` (step 4, checked by the script), and `rubric_rows` (ids from `open_rows`, empty without a map). The script refuses a proposal missing `problem`, `hypothesis`, `metric`, `first_step`, `pitch`, `owner_check` or `lever`.

Finally run `initiatives.py run` and write `opportunity-state.json`, even when nothing was kept, so the cadence counts from today. If a write fails, say so: the next scan would re-propose the same things.

When an initiative becomes active, suggest logging its milestones as contributions with `/flagrare:impact-scan` as they land; the contributions log stays the evidence trail.
