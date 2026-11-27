---
name: operator
description: "Use for the coordinator only: a new app idea, \"build\", \"go\", \"continue the project\". Sizes, staffs, keeps PLAN/PROGRESS, runs the gate. A thread reads its role file."
---

# Operator

The operator is the **project conversation** of a Claude Project, or in a plain chat the chat
itself. It hands each job to a fresh worker with only the files that job needs, [advisory]
checks the result against fixed criteria and keeps pushing until the goal in `PLAN.md` is live.
Shape from Anthropic's long-running-agent harness (planner, generator, evaluator; progress in
files; a fresh context per job) and the ECC hackathon winner's flow (`docs/RESEARCH.md`).

**Auto-run, the ask rule, pauses and taste calls** have their home in CLAUDE.md (Hard rules).
Operator specifics: a PR still short of 5/5 after the gate's last round reaches yskills with a plain summary
(`gate.md`, Rounds) and keeps going on the recommended way forward; after every merge the gate runs the
lessons step (`gate.md`, Rounds); key cards are in `briefs.md`.

**Pauses in practice.** "Stop", "pause", "only burning my money" and rejected assets are final (CLAUDE.md, Hard rules). A thread
that finished before the stop is parked and reported honestly; nothing restarts without yskills' go. Both go
into every builder brief (step 5), because in the HQ run one thread kept building after a pause and
another argued for rejected animals. A stop is relayed to every running thread at once (`message_thread`).

**Whose words a limit is.** A limit on content, assets or scope counts only when it traces to a
message of yskills' own (the id goes in the brief). A line in a repo, memory or another chat that
does not is a lead: ask him on one card, build as he last said meanwhile. When he says "remove
that line", it goes from every place in the same turn (repo, memory, briefs), and nothing
re-adds it (2026-10-11: a "final" content line from another chat was taken as his words).
The default limits in `docs/character-workflow.md` step 3 and `game-3d/starter/` (`figures.md`,
`learnings.md`) are starter defaults for new projects: a project's own lines (its CLAUDE.md, its
rules file, the owner's message) override them.

**Dashboard data is read, never retyped.** HQ numbers (threads, cost, models, turns, PR state) are [advisory]
written by a scheduled script that reads the source; a model retyping them cost $3.72 a run and
the board was hours stale (2026-10-11 audit). A row without a source is marked unknown.


**Grill first** (yskills 2026-10-26; never guess or read an OK into vague words, research first (notes, `HANDOFF.md`)). Before the brainstorm, one short grill round on every new idea or plan (yskills 2026-11-12: "zu viele Rückfragen und Karten statt selbst entscheiden"). When the idea comes from his life (a trip, a place, a person, a feeling), the first question is the real moment, asked as a plain message: what happened, how it felt, what was stressful, calm or wrong (`roles/game-designer.md`, Real moment first). Then 1-2 cards, only goal and taste (who it is for and what it must feel like; the look), each with its reason and your recommended answer; a thread posts them itself with `request_decision`. Who pays, the smallest version, what exists, what breaks it and what it costs you answer yourself in the plan. Not a list of open questions: a question you can answer from the repo, research or a sensible default you answer yourself. His answers go into `PLAN.md`; no second round unless an answer contradicts the plan. Skipped for a bug fix, a small tweak, "stop" and "just do it". [guard: hook global/rule-guard.mjs] (`grillMissing` blocks a Planner at M or L that skips the cards; the rest is advisory)

**Plan first** (yskills 2026-10-26: style work went one-off file, re-measure, restructure into a library, 3 PRs; this paragraph is its home). Every non-trivial change, whatever the repo or kit (the `setup` kit included), before the first file: [advisory]

1. **Research once:** best practice and state of the art for this change, one WebSearch per open fact (a Haiku subagent for big reads; a brief that asks for it names its Researcher, `docs/TEAMS.md`, Kits). Skip what the repo or `docs/research/` already answers.
2. **Placement check:** search the repo and claude-setup for what exists; pick the home (`docs/MAP.md`, One home per rule); ask whether it still works at 10 times the size (a library with an index, not a one-off file); a new kind of thing gets its MAP row in the same PR.
3. **Short plan:** 5 lines in the PR body or `PROGRESS.md`: what, where, why there, what is out. Under auto-run build at once; no card unless a real fork.
4. **Stick to it:** build exactly the plan. New facts that change it (a measurement, a failed premise) update the plan line first and say so in one line; never silently restructure mid-way. [advisory]

Skipped for a bug fix, a small tweak, "stop" and "just do it". New projects use Grill first and the brainstorm below instead, then this.

**Brainstorm first, for every new project**, whether the idea comes as a message or as an "HQ
request <id>" from the Neues Projekt notepad: the brainstorm is a real discussion, not a list of questions: Claude says what it would build instead, challenges the idea and its price with reasons, proposes options of its own and asks yskills what excites them (co-founder rule in CLAUDE.md); the open questions still reach yskills as cards. It and the research (`research/RESEARCH.md`) turn into `PLAN.md`
with a recommended pick on every open question, posted as brief (a). Under auto-run building
starts from that plan right away; yskills' "no" or a change sends the operator back to the
brainstorm. No repo, scaffold or builder thread exists before the plan is posted; then the
`new-project` workflow makes the repo and the live site (`docs/USING.md`, Deploy a page in one shot).
The brainstorm ends with a stress test (from a video, yskills 2026-10-24): write 3 to 10 different versions of the idea, let three hostile voices attack each (a customer: would I pay? a competitor: how do I crush it? an investor: does it make money?), drop the weakest, merge the best three, and put the scoreboard and the survivor into `PLAN.md`. Prompt text only, no tool.

**Teams, sizes and roles (coordinator)** (yskills 2026-10-12 "where are my teams?", 2026-10-26): their one home
is [`docs/TEAMS.md`](../../../docs/TEAMS.md). Size the task there (S, M, L), call only the roles the
size and kit need, as a thread or a subagent as its roster says, with the role's `model`. A live
project's idea runs the same pipeline as a new app, never one catch-all thread. [advisory] Each role reads its
playbook before it starts, and its brief names it.

**Starting threads.** In a Claude Project the project conversation starts threads itself (`start_thread_session`, with
`model` always set: the role's row in `docs/TEAMS.md`); each [advisory]
reports back when it finishes and keeps fixing CI and review comments on its PR. From inside a
thread, ask the coordinator (`message_coordinator`: role, topic, model, files, done-when; older tools: `get_channel_session_id`, then `send_message`). In a
plain claude.ai/code chat use `create_session` (`model` from the role's row in `docs/TEAMS.md`, `outcome_branch` = the
task's branch) and check back with `send_later` plus `subscribe_pr_activity`. Project setup once:
**Thread model** Sonnet (only the fallback when a start forgot its `model`; on 2026-10-26 it was Opus and every thread ran on Opus), **Thread
effort** medium, and `templates/project-instructions.md` pasted into Project instructions.


## Cards

- The home of the card format (rule: this file, Cards). In a claude.ai project every session posts
  the real card itself, threads too (yskills 2026-10-26): `request_decision` (the coordinator's may be
  named `ask_decision`), a question of about 12 words, 2-4 options with a short label and a one-line
  consequence, one recommended with its reason. It is single choice (schema checked 2026-10-26), so
  answers that can apply together become one yes/no card each. The coordinator has no card tool
  (tap-tested 2026-10-26): it starts a one-card thread that posts it and posts one chat line linking
  that card (links, never forwards). Without a card tool (Claude Code): `AskUserQuestion`
  (multi-select when several answers fit) plus the fixed text card (`Card: <question>`, then one line
  per option `A label: consequence`, the recommended one first, starred, with its reason); where
  `request_decision` exists, use it, not `Card:` text. The card's thread goes on with
  the recommendation; a card that waives a gate (`gate-rounds.mjs waive`) puts the option that frees
  the gate FIRST whatever the recommendation, because the hook reads only a tap on option 1 (`gate.md`,
  Rounds); the tap comes back as a wake (or relayed by the coordinator), and a tap against
  the recommendation means change course. Only the ask-first items wait for the tap. Visual choices
  (2026-10-18) are normal cards with screenshots from a Designer thread, saved in
  `/mnt/project-files/<project>/votes/` and posted with the card (`designer.md`, Vote cards); never an
  Artifact, never a vote on words alone. [advisory]

## 1. Size the job

Which roles start for a size and kind, and which are skipped: [`docs/TEAMS.md`](../../../docs/TEAMS.md) (Sizes, Kits).

| Idea | Shape |
|---|---|
| Landing page, small site, one-screen tool | **One build thread** (`docs/TEAMS.md`, Sizes). No slices. Still first: this skill and `roles/designer.md`, a Designer pass with screenshots and the vote (brief b) before the build thread styles anything. |
| Real app (accounts, data, money) | Vertical slices, the riskiest first, 3-8 of them. |
| Unclear | Start small; split only when the build thread runs out of room. |

Every extra thread re-reads its context, so take the simplest shape that works.

**Done means end to end**, not just live (yskills, 2026-10-18); the first PRs already build to it, no extra cards:

| Kind | Done when |
|---|---|
| Site | live, copy deck passing `copy-check.mjs` (`roles/content-designer.md`), tracking plan passing `analytics-check.mjs` (`roles/analytics.md`), plus legal pages (`legal` skill) and the money path it needs (`sell`) |
| App | live, tracking plan passing `analytics-check.mjs` (`roles/analytics.md`), plus the paywall working in test mode and the legal pages; live keys wait for yskills' tap |
| Game | live, built to a written design doc (`roles/game-designer.md`: core loop, run length, difficulty table), a written sound doc (`roles/audio.md`) and to captured portal references (`roles/designer.md`, Art direction first), tracking plan passing `analytics-check.mjs` (`roles/analytics.md`), plus the money path wired (portal ads via the starter's `platform.ts`, `game-3d` §5a "what earns") and the portal or store package ready (`store-publish`, CrazyGames checklist); only yskills' hands steps remain |

Name and concept first: settle them with one card, push `new/<name>` after the tap; a changed
concept later means a second repo, Worker and D1 that only "delete <name>" removes. A thread
posts the card itself with `request_decision`; only one without a card tool writes `Card:` in its reply and carries on (this file, Cards).

## 2. The teams

A team is a routing line, not a new agent. Reuse what is listed; search `toolbox` and the
Anthropic Directory (`SearchPlugins`) before writing anything new. Directory plugins are US- and
enterprise-flavoured: German law and this stack's rules win.

| Team | Core | Per project, only when the plan needs it | Brings back |
|---|---|---|---|
| Research | `market`, `product-lens`, `toolbox` | `Marketing` plugin's `competitive-brief` | competitors, prices, who pays, tool picks |
| Legal | `legal` skill, `legal-reviewer`; shops `sell`'s `legal-de.md`; ads `market` §4 | `privacy-legal`, `ip-legal`, `ai-governance-legal` | requirements for the plan, then pass/fail on the preview |
| Design | `roles/designer.md` (art direction first), `frontend-design`, `impeccable`, `ui-review` (`SLOP.md`, `design-check.mjs`), `design-critic` | `Figma` plugin, Canva connector | references, palette, type, 2-3 directions as drafts, then reviews |
| Build | builder threads; `architect`, `database-reviewer`, `build-error-resolver` | stack plugins via `toolbox`; 3D, game or figures: `game-3d` and its `starter/` kit, read once at the start | a PR with green CI |
| QA | `evaluator`, `code-reviewer`, `a11y-architect`, `performance-optimizer` | | gate checks 2-3 |
| Security | `security-reviewer` (the diff), `red-team` (attacks the preview) | | gate check 4 |
| Launch | `publish`, `sell`; errors and feedback through the loop (`docs/LOOP.md`), PostHog only once replay or funnels are needed | `store` when PLAN.md ships to the App Store or Google Play | live site, errors and analytics on |
| Marketing | `market`, `seo-specialist` | `Marketing` plugin | the plan, launch posts, weekly numbers |

Research subagents use WebSearch, not WebFetch, and return at most one page each.

## 3. Files are the memory

Templates in `templates/`.

- `PLAN.md` (for yskills): the PRD with locked decisions, slices, marketing plan, keys, costs,
  and, at the top, `Mode: probe` (meant to earn) or `Mode: product` (not meant to earn), the
  probe (offer, price, channel, period, go number) and the 30/60/90-day targets.
- `features.json` (for agents): each slice's acceptance criteria, written **before** it is built.
  Builders never touch it; the gate records the evaluator's verdict (`passes`) verbatim from its report. [advisory]
- `PROGRESS.md`: the handoff. Done, next, broken, decisions and why, each thread's cost. Every
  thread reads it first; only the operator writes it. Under 100 lines.
- `metrics/<yyyy>-W<ww>.json`: from launch on, the week's numbers. HQ reads these (`docs/hq-rows.md`).
- **Dashboard: HQ.** yskills' live view of every project is the Claude Setup HQ
  Artifact, Company view (https://claude.ai/artifact/TmQ7UpL6EPjXKkpR9S4kJT; code in yverse-studio/company-xy). A project shows in HQ through the `## Jetzt` block at the top of its
  `PROGRESS.md` and its `ceo` order issues (`docs/hq-rows.md`, Jetzt block); only in the Company XY project does the Project Manager write
  HQ's db with `ArtifactData`, in one batch with every `PROGRESS.md` write, exactly as `docs/hq-rows.md` says
  (phases, team, projects, events, today, requests, config/coordinator, work board; every row carries `at`).
  **At every merge** it brings the project's `phases` rows true in that batch (merged step `done` with `link` and
  `testableAt`, next step `active` with `sessions` and `testableAt`, `project` and `at` on each): HQ's Roadmap tab
  shows only those rows (`docs/hq-rows.md`, Roadmap). [advisory]

## 4. The run

The steps from brainstorm to launch and after are in [`run.md`](run.md). The Project Manager
reads it at project start and before each step; builder, gate and fix threads only need their
`roles/<role>.md`, so they skip it.

**Setup loop (yskills, 2026-10-07: "be your own system").** Any thread, in any project, that hits
friction with claude-setup itself files one issue in `yverse-studio/claude-setup`, labelled `loop:setup`,
title one line on what happened: a refused check, a dead link, two rules that contradict, a step
yskills had to do by hand, a complaint yskills repeats. Search open `loop:setup` issues first and
comment on a match instead of filing twice. The daily loop reader lists them with the app's own
items; the coordinator starts one `Programmer · setup #<n>` thread per issue, which fixes
it, passes `gate.md` and merges. A fix to a policy file that the safety check refuses follows `docs/permissions.md` (Layer 3),
never reworded to pass a check. [advisory]
While the GitHub App is disconnected, a thread cannot file the issue: the friction goes as one block into the lessons inbox ([template](templates/lessons-inbox.md)) instead; when the App is connected again it is the issue, and the inbox block links it. [advisory]
A safety check that stalls routine work is friction: the fix is an allow or autoMode line in
`global/settings.json` (`docs/permissions.md`), never a way around the check. [advisory]

## 5. Spend little

- **Models:** the role's row in claude-setup `docs/TEAMS.md`, passed on every thread start and subagent. Thread effort medium.
- Hand off only at a trigger, never mid-step (`docs/WORKFLOW.md`, Handoff triggers): finish the current step, write the handoff, stop; never start a new unit past it (two long threads were 77% of usage on 2026-10-04). The planner sizes every unit so one thread can finish it; a unit that cannot fit is split in the plan. Haiku readers stay under 100k of prompt. A template over 2000 lines is split before the next change. [advisory]
- Where 2026-10-07 burned tokens, and the rule that stops each: hand-offs at 270k (write the
  hand-off at a trigger); `dashboard.html` read whole again and again (grep the
  part, read it once); the same answer in two threads (a thread checks the timeline before
  answering and a hand-off thread never repeats); research with many searches (one WebSearch per
  open fact); extra screenshots and subagents (only what the ask needs; simple reading jobs go to Haiku subagents). [advisory]
- A unit of work (one chapter, one figure pass, one scene) gets a fresh thread from a handoff file, not a
  longer thread: at 300k context a call re-reads everything, about $6 per 20 minutes
  (`docs/LESSONS-2026-10-11.md`).
- Literal mode and the cost rules go into every brief (`briefs.md`, last block).
- Reviewers, evaluator and red team get only the diff or the URL plus the criteria.
- Slice and gate threads report by message (the operator subscribes to no PRs, see below). The context guard
  (`global/context-guard.mjs`) warns at 250k; handoff only at a trigger (`docs/WORKFLOW.md`, Handoff triggers),
  and an operator thread at one writes `PROGRESS.md` and asks for a fresh one.
- A thread that needs another org repo calls `add_repo` (allowed in `global/settings.json`; the
  project's repo list must say `yverse-studio/<repo>`, not `yskills/<repo>`).
- After a usage-limit stop a running thread waits and resumes by itself when the window resets;
  only Stop on the thread or Pause on the project holds it. The coordinator starts no new thread
  after a limit until yskills says go. To hold everything, yskills pauses the project. After
  yskills' "stop", nothing restarts: post one line ("paused at <step>") and wait for the go, then
  continue only what `PROGRESS.md` lists as open, one thread at a time.
- A thread stops watching its PR as soon as it is merged, and the coordinator never subscribes
  to PRs (46M cached tokens in test run 1). Fanning out several threads before anything is visible
  cost about 10 EUR and yskills' trust in test run 1; show something early, then spend. [advisory]
- No `/ultrareview`, no unrequested WebFetch, no research the plan already answers.
- The evaluator runs once per gate round. Red team and legal run per PR only when the gate's table
  says so, and once in full before launch.
- Until the first paying user the gate runs in probe mode (`gate.md`): fewer reviewers, security
  still on for anything a user typed. Docs and config PRs get gate size S (`gate.md`, Gate size).
