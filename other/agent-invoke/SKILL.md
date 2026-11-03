---
name: agent-invoke
description: Run an owner's ad-hoc request for delegated work as a properly configured background subagent — picks the model from doctrine by where the judgment lives, writes a brief that makes the agent commit its own output, holds the Mac awake for the run, reads the run's own report in full and verifies what came back against the repo rather than relaying it, and leaves the completion message to the SubagentStop hook that fires whether or not anyone remembers. Use this whenever the owner asks for work to be handed to an agent or done in the background, including phrasings that never say "agent" — "invoke an agent to…", "I want to research…", "look into X and report back", "have something draft a plan", "go do X while I'm away", "spin something up for this". Prefer it even for a single one-off delegation, since the model choice and the commit requirement are exactly what a hand-assembled launch forgets.
when_to_use: Fires on any owner request to delegate work rather than do it inline, and on any request for research or investigation whose result the owner expects to come back to. Also fires when the owner asks for a plan or design to be produced for a later run to consume. Do not use it for work already owned by a launcher or a pipeline stage that spawns its own agents — the kaizen cold-read launcher, the development chain, skill-evals — those carry their own launch, model, and notification rules. Do not use it for work small enough to simply do inline.
license: MIT
metadata:
  author: Eyal Golan
  version: "1.16.3"
  created: "2026-07-26"
  category: orchestration
  tags: subagent, delegation, background-work, notification, research
  risk: safe
---

# agent-invoke

## Purpose

The owner says *"get an agent to do X"* and three things have to be assembled correctly before
anything runs: which model, a brief that survives being read cold, and something holding the Mac
awake. Hand-assembled, the same pieces get rebuilt each time, and the model choice is the one the
owner only discovers was wrong afterwards.

**The fourth thing used to be here and is not any more.** A notification reaching the owner after
they have walked away was this skill's step to remember, and remembering it worked six times in
nine. It is now `.claude/hooks/subagent_stop_notify.py`, which fires on every `delegate` stop —
every run this skill starts — with nobody in the loop. What Step 6 still owes is a correction when
the repo disagrees with what the run claimed.

This skill is the launch procedure. It does not decide *what* the agent should do; the owner's
request is that. It decides how the run is configured, what the brief must carry, and what happens
when the agent comes back.

**One shape only: an Agent-tool subagent, run in the background.** It runs inside this session, so
the harness hands completion back to you here, and the `SubagentStop` hook reaches the owner
independently of that. Detached `claude --bg` runs are a different mechanism with their own launchers
under `<CORE>/tools/` and their own PID-polling completion detection; do not reach for them here.

**One agent: `delegate`** (`<CORE>/../skills/interactive/.claude/agents/delegate.md`), spawned with an explicit `model:` from Step 1. It sits in this skill's own group, so the `--add-dir` / `/add-dir` on `<CORE>/../skills/interactive/` that reaches this skill gives a session `delegate` to spawn too. Not the built-in `general-purpose` — that carries no contract, so every discipline a
delegated run owes has to be retyped into each brief and drifts between launches. `delegate` holds
them once: verify against files opened this session with citations, measure rather than estimate,
surface what it will not settle, commit its own work through the builder, stay inside the fence, and
report in a shape the caller can verify. What stays in the brief is the *job*; what lives in the
agent is what is true of every job.

`delegate` pins **no** model, and that is why Step 1 is not optional. An unpinned agent inherits the
model of the session that spawned it — so omitting `model:` does not choose a tier, it hides the
choice behind whoever happened to launch the run. Passing it explicitly is what makes the cost follow
the work.

Reach for a **posture** agent instead (`architect`, `cpo`, `developer`, …) only when the task wants
that role's loader stack and its `Role:` on the commit. A one-off exploration does not — and the tell
that you have picked wrong is finding yourself writing "do NOT produce your usual X" into the brief.

---

## Step 1 — Read the request for its task shape

The model follows from where the judgment lives, so name the shape before anything else.
`<CORE>/doctrine/governance/model_assignment.md` § *Runs with no standing slot* owns the rule and
the tiers — an ad-hoc subagent has no slot to inherit a `model:` from, so the choice is per-run.
Read it; the routing below only maps the owner's phrasing onto the shapes it defines, and where the
two ever disagree, doctrine wins.

| What the owner is asking for | Where the judgment lives |
|---|---|
| Research, investigation, "look into X", a design or plan others will execute | authoring / deciding — the output is consumed as authored |
| Applying a decision already made — a rebuild against a stated referent, a migration, a sweep | applying a decided plan, with the return verified |
| One mechanical transformation over many files, each independently checkable | a checkable transformation at volume |

A request that spans shapes takes the **highest** one it touches. The reason is asymmetric cost:
under-powering the deciding half of a task produces confident work that has to be redone, while
over-powering the mechanical half only costs tokens.

Never write a model name into a brief from memory or from an example — resolve it through doctrine
at launch time, so a tier reassignment there reaches every future run of this skill. The **resolved**
tier does go in the brief, per Step 4; what is forbidden is the remembered one.

## Step 2 — Decide where the output lands, before launching

Every run commits something, and what it produces decides where that goes. Work that changes files
has no destination question for its *output* — the files are the answer. Work that produces only
findings needs one, because a finding that lives in a transcript dies with the session.

**Every run has a second destination, whatever it produces: its report.** That one is never skipped,
so even a run whose output is code has a decision to make here.

**Ownership first, artifact kind second.** Two rows below can match one run — a design *and* a managed
project's work is both — and the answer is always the project. **If the work belongs to a managed
project, it lands in that project's `docs/` and its journey; `docs/proposals/` is for work no project
owns.** Read the rows in that order or the artifact-kind row matches first and the run files a
project's own work outside it. This is not hypothetical: a run on 2026-08-24 routed a design to
`docs/proposals/` for exactly that reason, against the owner's standing position that plans belong in
the journey (`system/projects/product-experience/docs/how_will_the_plan_be_presented.md`).

| What the run produces | Where it lands |
|---|---|
| Changes to existing files | those files — nothing to decide |
| Research, an investigation, a design — **that no managed project owns** | `docs/proposals/<slug>/`, as `research.md` or `rationale.md` |
| A plan for a later implementation run — **that no managed project owns** | `docs/proposals/<slug>/ad_hoc_plan.md`, beside its rationale |
| A record of a managed project's own work | `system/projects/<name>/docs/` |
| **A route** — seeds, and the stations they carry | `system/projects/<name>/journey/nemawashi/unpicked/`. A seed goes in **`unpicked/`**, never the seedbed root — lifting one to the root is a *pick*, and picking is the PM's call, not an agent's. **Do not author station files**: exactly one station is active per project and opening one is also the PM's move, so the stations live as checklist items on the seed. A route crossing several projects writes a seed in each, and the owning project is decided by that project's Agari |
| A plan a managed project owns, for a later implementation run | that project's journey — `<CORE>/doctrine/setup/kensaiapp_structure.md` § Root, `docs/proposals/`, owns where in it |
| **The run report** — `delegate-report.md`, which **every** run writes | keyed to what the run belongs to: the managed project, the proposal, the skill, whatever it was. **Decide it and name it.** |

`docs/proposals/<slug>/` is one folder per proposal holding an `ad_hoc_plan.md` and its reasoning, with
`archive/` for retired ones. A run that produces both a plan and the thinking behind it writes both
there — the reasoning is what makes the plan reviewable later, and splitting them across locations
is how a plan ends up with no findable why.

**The run report** is `delegate-report.md`, and `<CORE>/roles/delegate_contract.md` § *The run report*
owns what goes in it — do not restate its sections here or in the brief. What this step owes is the
**path**, keyed to whatever the run belongs to: a managed project's `docs/`, the proposal folder, the
skill's own folder, wherever the work sits. There is no fixed home, because a run's subject is not
predictable — it may update a skill, produce a proposal, or touch neither.

**It goes in a per-run subfolder — `<home>/<run-slug>/delegate-report.md`** — where `<run-slug>` is a
short kebab-case name for what the run did (`register-skill`, `register-evals`). The filename never
varies, so `delegate_contract.md`'s fixed name holds, and the folder is what separates runs.

**This is already how it works everywhere a run produced a proposal**, and the rule is written down
here only because the other destination never got the same shape. Counted 2026-08-17: 14 reports live
at `docs/proposals/<slug>/delegate-report.md` — the proposal folder *is* the run's folder, and the
filename never varies. The runs that write into `system/projects/<name>/docs/` had no such folder, so
the second one into `dev-skills` had to invent a suffix; the invention is written down nowhere, so a
third run invents a different one and the set ends up distinguished by names no rule produced.

The subfolder also gives a run somewhere to put anything else it produces about itself, which a
suffixed file has no room for.

**The agent never invents the destination; the brief names it.** An agent asked where its output
belongs will answer plausibly, and plausible-but-wrong is a misfiled artifact nobody finds again. If
the request does not settle it, ask the owner — a one-line question is cheaper than the search. This
holds for the report exactly as it holds for the output.

## Step 3 — Hold the Mac awake

Start keep-awake **before** launching, and record the PID:

```bash
nohup caffeinate -i -s -t 14400 >/dev/null 2>&1 & echo $!
```

Kill it in Step 6 when the run lands.

This is needed because nothing else provides it. Claude Code does spawn its own `caffeinate -i -t
300`, but it is a one-shot five-minute timer that is not renewed — measured 2026-07-26 across a
7-minute window of continuous background activity, during which the timer expired and no
replacement appeared for the remaining six minutes. A subagent run that outlasts five minutes is
otherwise unprotected, and an idle-sleeping Mac stalls the session the agent runs inside.

Two details worth their reasons. `-s` is there because `-i` alone blocks only idle sleep, which is
the weaker of the two guarantees. The four-hour `-t` is a backstop, not the mechanism — the kill in
Step 6 is the normal release, and the timeout only matters if this session dies mid-run and never
gets to it. Bounding it means a crashed session cannot leave the machine awake indefinitely.

This differs from `<CORE>/launchers/cold-read/launcher.sh` and its siblings, which bind `caffeinate -w` to a
detached process's PID. That works there because a detached run *is* a process. An Agent-tool
subagent is a branch inside this session with no PID of its own, so there is nothing to bind to and
the release has to be explicit.

## Step 4 — Write the brief

The agent gets one shot at understanding the task and cannot ask a follow-up question mid-run. A
brief that reads clearly to its author and ambiguously to a stranger is the single most common way
these runs fail. Write it for someone with no memory of this conversation.

Every brief carries:

- **The working directory**, absolutely, and an instruction to run everything from there.
- **The model tier you resolved in Step 1, named**, with the one-line reason it was picked. The tier
  is passed in the spawn call, which the agent cannot see — so an agent told nothing reports the
  model it *happened* to inherit, which its own contract asks it to say out loud. That report is the
  only durable record of what the run cost and why, and "inherited" is not an answer to either. It
  also lets the agent object: a tier that does not fit the work is a thing to surface, and it cannot
  surface what it was never told.
- **The job**, in one paragraph, before any detail.
- **The constraints that must not be violated**, stated as constraints rather than mixed into
  narrative. Anything read-only, anything out of scope, anything not to run.
- **Its own citations, quoted.** A claim this brief makes *about a file* carries the text it claims,
  not only the line numbers: `path/to/file.md:L12-L20 "the sentence that is actually there"`. Line
  numbers alone cannot be checked by anything — the six wrong citations in `15848b6` were every one of
  them *in range*, pointing at text that had moved. `.claude/hooks/brief_anchor_guard.py` opens each
  cited range before the spawn and **denies the launch** when the quote is not there, naming where the
  sentence actually sits. It owns what it checks; do not restate its rules here.
- **Where its output belongs, by section.** A brief that commissions a file — a document, a seed, a
  station, a skill — names the section of `<CORE>/doctrine/setup/kensaiapp_structure.md` that governs
  where that file lives, not the file itself. It is 900 lines with 18 named sections, and measured
  over 584 real briefs, 94 of the 111 that name it point at the whole thing while 33 of the 40 that
  commission a file never name it at all. Pointing at a haystack and pointing at nothing fail the same
  way: the run invents a location. Nothing enforces this — a hook cannot see what a run is about to
  write — so it is on you. (The section *index* reaches every run through
  `.claude/hooks/manifest_salience.py`; naming the right one is what the brief adds.)
- **What to read first** — the specific files, with what each one is for. An agent left to find its
  own sources will find different ones each run. **This list starts at the task→doctrine map.**
  Resolve the job through `<CORE>/doctrine/task_map.md` *before* writing the brief, and name what it
  routes to and what each file governs. Retrieval that happens only in your context does not reach
  the agent — the brief is what it actually works from, and a brief that names no doctrine is an
  instruction to reason from recall. Where the map returns nothing for a task it claims to cover,
  that is a defect to report, not an absence of doctrine to write around.
- **How to verify** — that claims about a file are made after opening it this session and cited as
  `path:Lstart-Lend`, never from recall.
- **The commit instruction**, per Step 5.
- **The report path** — where `delegate-report.md` lands, from Step 2. Only the path: what the report
  must contain is the delegate's own contract (`<CORE>/roles/delegate_contract.md` § *The run report*),
  and a brief that re-describes its sections is a copy that drifts the first time the contract changes.
  The agent's closing message is a pointer to that file, not a second telling of it.

**Before you write it, read what previous briefs left out:**

    python3 <CORE>/tools/brief_gaps.py --repo .

That is every gap a delegated run recorded about its own brief, read off the run reports themselves —
stale line numbers, a tool that was named and not granted, a read list nobody could finish, a premise
inherited from a seed and never checked. It is computed, not maintained, so it cannot drift from the
reports. A gap that keeps appearing is not yours to work around: it belongs in this step, or in the
guard, or somewhere that is not the brief at all.

Two things that reliably improve the return, both learned from runs that needed them:

- **Give the reasoning behind a constraint, not just the constraint.** An agent that knows *why* a
  file is read-only handles a case the brief did not anticipate; one told only *that* it is
  read-only either stops or guesses.
- **Say explicitly that ambiguity is surfaced, not settled.** Without that, an agent silently
  resolves the fork it hit, and the decision surfaces later as a defect rather than as a question.

Say what the brief is *for*, not what produced it. Context about why the work is being commissioned
is useful to the agent and does not belong in the artifacts it writes — mark it as such.

## Step 5 — The commit instruction the brief carries

The agent commits its own work. This is a requirement placed **inside the brief** — not something
this session does afterwards — because the agent is the only actor that knows what it changed and
why, and a commit written by anyone else loses the reasoning.

The mechanics belong to `<CORE>/doctrine/governance/commit_via_builder.md` — the staged-set guard,
`--staged`, the flag forms — and the brief points there rather than restating any of it. Restating is
how a brief ends up teaching a tool contract the tool has since changed. One thing belongs in the brief
itself because it is about the *run* rather than the tool: **no `--skill` unless a producing skill
actually ran**, or the commit claims a `Skill-Version:` that never produced anything.

Ask for **one commit per coherent unit** rather than one commit for the run. A single commit
covering four unrelated changes cannot be reverted in pieces and its body cannot explain itself.

**Prefer not to run two committing agents against the same repo at once — but a busy repo is not a
blocker.** The builder's staged-set guard refuses a commit whose staged set it was not told about, so
a second actor's staged work no longer rides along silently; it produces a loud refusal naming the
undeclared paths. Sequencing is still the clean default, because a refusal costs the agent a turn it
has to spend diagnosing someone else's index. But if a run is already in flight, the correct move is to
launch and let the guard do its job — not to wait indefinitely. Tell the brief that a refusal naming an
unfamiliar path means another session is active, and that the answer is to report it, never to reach
for `--take-index`.

## Step 6 — When it lands

The harness notifies when the agent finishes. Then, in order:

1. **Release keep-awake** — `kill <pid>` from Step 3.
2. **Read `delegate-report.md`** — the whole file, at the path Step 2 fixed. Not the agent's closing
   message, and not a grep of the file for the section you expect to care about.

   This step exists because Step 4 deliberately makes the closing message a *pointer* rather than a
   second telling. So the run's findings, its open questions, what it could not settle and what it
   measured live in that file and **nowhere else** — a caller who reads the summary and skips the
   file gets only the parts the agent chose to repeat, which is the one account not written to be
   checked. It is also what the next step is run against: the report is the claim, the repo is the
   check, and you cannot check a claim you have not read.
3. **Verify before believing.** Check the commits exist and their scope matches what was asked:
   `git log --oneline <base>..HEAD`, `git diff --stat <base>..HEAD`, and a direct check of any
   constraint the brief declared — if something was read-only, prove it is byte-identical. An
   agent's summary is a claim about the repo, and the repo is available. This is not distrust; it is
   that a subagent reporting on its own work is the one reader who cannot see it fresh.

   Verify the report's **load-bearing** claims too, not only the commits — the ones that would
   change what the owner does next. A finding stated with a citation is still a claim until the
   citation is opened.
4. **Do not send a completion message — the hook already did.** `.claude/hooks/subagent_stop_notify.py`
   fires on every `delegate` stop, which is every run this skill starts, and posts the agent's own
   closing message before you regain control. Sending a second is two messages per run for one event.

   This step used to be the send, and it was the thing that did not hold: read and followed six
   times out of nine in one evening, with all three misses in the busiest stretch. The rule did not
   need better prose, it needed a surface, and it has one — so the obligation moved rather than
   being duplicated.

   **The one message still yours is a correction, not an arrival.** When Step 3's verification
   contradicts what the run claimed, the channel is now holding an account the repo disproves, and
   that is the one thing the hook can never know. Send then, saying what the repo actually shows.
5. **Report to the owner** what you verified, distinguishing it from what the agent claimed, and
   surface every question the report raised — each one, from the file, not from the closing message.
   Folding them into a summary is how a fork the agent correctly refused to settle gets settled by
   omission.

If verification contradicts the agent's summary, the repo wins — say so plainly and name the gap.

---

## What this skill is not for

- **Work a launcher already owns.** The kaizen cold-read launcher and the development chain spawn
  their own agents with their own model rules and
  completion handling. Running this on top of them duplicates the launch and confuses attribution.
- **Work small enough to do inline.** A launch costs a brief, a verification pass, and a
  notification. Below that threshold, doing the work directly is faster and easier to correct.
- **Deciding what the work should be.** This skill configures a run; it does not scope it. If the
  request is too vague to write a brief from, that is a question for the owner, and asking it is
  cheaper than launching an agent that guesses.
