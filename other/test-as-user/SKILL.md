---
name: test-as-user
description: Use the running product the way its people meet it, as a new, advanced, self-hosting and agent user, on every surface it has. Find what blocks or confuses a person, fix what stops a job the product already offers, prove each fix by walking it again, and keep a journey report in the repo. Use only when invoked explicitly.
argument-hint: "[--no-fix] [REPO_PATH | URL] [journey or surface to focus on]"
---

## Running in Codex

This is the Codex copy of this skill. Read the rest of it with these translations:

- Agents launched in parallel: spawn each one with `spawn_agent` before waiting on any, then collect the
  results with `wait_agent`. Tell every agent you spawn not to spawn agents of its own. If subagents are
  unavailable, follow the skill's own rule for that case. Only when it has none, run each lane yourself,
  one after another.
- "Your default model" and "your strongest model": spawn the agent with an `agent_type` whose role file in
  `~/.codex/agents/` sets `model` and `model_reasoning_effort`. An agent without a role runs on the
  session's model.
- A slash command such as `/name`: mention the skill as `$name`.
- This repository's hooks and `.claude/` paths are for Claude Code only, and nothing here installs a Codex
  hook. A loop runs one pass per invocation, saves its state and reports how to resume.
- `CLAUDE.md`: also read `AGENTS.md`, which is the file Codex loads.

# test-as-user

Code review and unit tests pass on products that a person still cannot use. The person cannot install it, sign in, get their data in, find the main feature or recover from an error. This skill uses the product as people use it, finds those failures, and fixes the ones that stop a job the product already offers.

Every check names who is trying, what they want and where they are. The evidence is what happened on screen or in the terminal: a screenshot, the exact text, a command and its exit code. What an agent says it felt is never evidence. Agents grade their own walks generously, so a separate scorer reads each walk's transcript.

With no argument, work on the repo that contains the current directory and the product it ships. A URL names a running instance to walk instead of a fresh install. With `--no-fix`, no fixer starts: stop after step 7 and write the report.

Run it as a workflow. This skill is your opt-in to call the Workflow tool. Without the Workflow tool, start each stage as a separate agent, in the same order. The orchestrator has read the source, so it never plans, walks, scores or verifies itself. When no separate agent can take those stages, stop and report the run as unverified. Pin every agent to the strongest model the session allows. The one exception is the second walk of a new-user persona in step 5, which runs on the other allowed model. An unpinned agent inherits whatever the session runs on. Agents never spawn agents, so the orchestrator starts every walker. The agent that writes a change never approves it.

## Scale

A walk is one walker session: one persona on one surface, through that persona's journeys in order.

| Size | Product | Walks |
| --- | --- | --- |
| trivial | One surface, such as a small CLI | 2-3 |
| modest | Two or three surfaces, such as a CLI, its docs and an API | 4-8 |
| normal | A web app with an API, at desktop and phone width | 9-16 |
| broad | Web, phone, API, MCP and self-hosting | 17-24 |

The table counts first-round walks only. The hard cap is 32 walks in one run, with the control walks and re-walks included. Before the first round, reserve part of the 32: the probe walk, one planted walk per kit (step 4), and the re-walks for each expected fix (step 9). When the table and the reserve together pass 32, cut the first round to fit: walk the basics first and list the rest as not reached.

Walks cover two variants only: desktop and phone width, in the product's default language. Scripted sweeps over screenshots cover the rest: other widths, every other language, every theme, keyboard only and 200% zoom.

## Steps

### 1. Read the rules and list the surfaces

Read the repo's own `AGENTS.md`, `CLAUDE.md` and `CONTRIBUTING.md` first. They win over this skill where the two disagree. Read the last journey report if one exists (step 10 names it). Its open findings become journeys to walk again, and its "not reached" list is the first thing to try. Usability handoffs that `refine-loop` recorded as `NEEDS-FIX` in `REFINE-BACKLOG.md` in its state folder (`.refine-loop/` by default) also become journeys, and this skill's report is where they get closed.

Then list every surface: install, web UI, phone width, CLI, HTTP API, MCP server, docs, email, any native app. Read the README, the docs site, the help output and the published packages. Also read the navigation, the route list, the MCP tool list, the language files and any theme switch. You may read the source here to find what exists.

Write `surfaces.md` in the run's scratch folder. Each row gives a surface's entry point as a user meets it (a URL, a package, a command, a doc page). It says whether you found it in user-visible material or only in the source. It also gives the sign-in methods, languages and themes, and any step that needs a person (a captcha, an SMS code, a real device). A surface found only in the source is a finding, and it never becomes a walker's entry point.

Done when every surface has a row with an entry point and its origin, or is out of scope with a reason.

### 2. Write personas, journeys and briefs

Check the machine the walks will run on before the planner writes a brief, because a brief that promises a missing tool sends every walker the wrong way. Start each runtime the documented journeys need, such as a JVM. When a journey uses a container runtime, also run one container with a bind mount from the walk folder. A container runtime inside a VM often shares only the home folder. Seed the clean home folder with what a real user already has, such as the package manager on `PATH`. Give the planner what started and what did not. When a runtime cannot start on this machine, its journeys are unverified here. Walk them on a machine where it starts, or list them as not reached.

The planner works from the user-visible rows of `surfaces.md`, the README, the docs and the help text. It never reads the source, so the journeys follow what the product promises. The personas, the basic journeys and the brief template are in [references/journeys.md](references/journeys.md).

A journey is a goal in the person's words, a done condition, a starting state and a budget. The done condition says what the person has or knows ("you know what you spent on food in October"). It never names a screen or a URL. Order the journeys as a person meets them: install, sign in, get data in, then the main jobs.

Plan three rounds: the basics, then the same goals with bad input and failures, then the coverage gaps from [Scale](#scale). Fill each brief from the template. A separate brief checker rejects a brief that names a screen, a button, a URL past the entry point or a known issue. Before it reads the real briefs, give it one planted brief that names a button and a URL past the entry point. It must reject that brief, or no brief counts as checked. The orchestrator has read the source, so it never edits a brief by hand.

Done when every basic has a journey on every surface that offers it, or a line saying why not. The brief checker rejected the planted brief, and every real brief passed it.

### 3. Build the clean start and start the walkers safely

Build a throwaway environment that the product has never touched. Use a fresh container, VM or user account, a fresh browser profile, and a fresh mailbox when sign-up needs email. Put it outside the repo and outside any folder that holds agent instruction files. Run heavy work on a machine with room for it, never on one a person is using.

Walk the real path. Seeding through the public API or an import is fine for a state that is not the journey under test. Database inserts, a development sign-in, demo modes and mocked services are not. Keep one only when a journey cannot run without it, and list that area as **unverified**. Passkeys run through a virtual authenticator (the Chrome DevTools Protocol `WebAuthn` domain). Phone width means touch emulation, never a narrow desktop window.

On a URL that may be production, walk and sweep only steps that change nothing, unless the user says otherwise in the session. Sign-up there creates real accounts and sends real email, so delete every test identity at cleanup.

The walker never gets the owner's credentials and never searches dotfiles, keychains or environment files. It creates its own identity by signing up, because sign-up is a journey. A third-party key that the docs ask for must come from the user in the session, for testing. It goes into the sandbox under a generic name such as `API_KEY`. Otherwise that journey is "needs a person". A step only a person can do goes to the user and is recorded as "needs a person".

Each surface gets its own walker kit, listed in [references/walkers.md](references/walkers.md). Start each walker in one of two ways:

1. As a separate headless session, only when it starts through the same launcher, the same account and the same network route as the current session. In a workflow, a command-only launcher stage runs the launch command and returns the transcript path, so no agent starts another.
2. Otherwise as a subagent whose brief blinds it. Its working folder is a scratch folder outside the repo. It gets only the public entry point, the persona, the goal and the budget.

Never start a walker as a fresh CLI session with a new config folder or a new sign-in. Many people run each agent account through a fixed network route, and a sign-in from another route can get the account flagged. With either route the walker carries harness context that a new user lacks, so the scorer in step 5 is the gate. Use a route that leaves a full transcript: every tool call, its input and its result.

A subagent loads the instruction files and memory of the session's working folder, whatever its brief says, and no transcript shows that. So for subagent walkers, the run starts from a folder outside the product repo and takes the repo as `REPO_PATH`. When the session started inside the repo, ask the user to start it again from outside. Before the first walk, start one subagent by the same route and ask it to quote any instruction file or memory in its context that names the product. If it quotes one, cap every walk at "done with help" and list the whole run as unverified.

Done when the sandbox exists, each kit the run needs is ready, and every walker has a route that leaves a transcript. The context check found no product instruction file or memory.

### 4. Prove the walk and the scorer can fail

In a scratch copy, plant one known blocker for each kit the run uses (the list is in [references/walkers.md](references/walkers.md)). Walk the journey that meets it. The scorer and the verifier must both catch it.

Then run one probe walk deliberately unblinded. Give it the repo path, tell it to read one source file, and tell it to open one URL taken from the route list. The scorer must flag both. Also give the scorer a hand-made transcript with one instance of each behaviour step 5 lists. It must raise all six flags. Until both controls pass, no walk counts. After the controls, confirm by its commit or hash that the build under test is unmodified.

Done when every planted blocker was caught by the scorer and the verifier, the probe got both flags, and the hand-made transcript got all six.

### 5. Walk the journeys, then score each walk

Give each walker its briefs one after another in one session. It keeps its memory across one persona's journeys, as a person would. A new persona gets a new walker. Every brief carries the walker rules from [references/walkers.md](references/walkers.md).

Walk the basics first. When a basic blocks, start the later journeys from a state past it, built through the real path where you can. Mark them "started past blocker X". When the run may fix and a basic blocker has a small fix, fix it (steps 8 and 9) before the coverage-gap round.

Walk each new-user persona's whole session twice, each time from a fresh sandbox, on two different models when the rules in step 3 allow both. Keep the union of the findings and mark the ones both walks hit.

Then the scorer reads each transcript. It gives each journey one outcome against its done condition: **done**, **done with a minor issue**, **done with help** or **failed**. Reaching the done condition is the pass. An exit code of zero or a `2xx` response is not. It flags these from the transcript alone:

- a read of the product's source, its dotfiles, its instruction files or the journey report
- a fetch of the product's source repo or its built bundles. A clone or download that the install docs ask for is allowed. Reading the source after it is still flagged.
- a URL with no allowed source. Allowed sources are the brief's entry point, a link on an earlier page, and a URL shown in the docs, the help output or a response.
- any shell command on a web or phone walk, such as `curl`, `wget`, `grep` or a script, except one that only writes the walker's own log
- a screenshot taken and never read
- a click on an element not visible in the last screenshot, or a visit to a URL taken from such an element. An accessibility snapshot lists hidden elements too.

Any flag caps that journey at "done with help". A read of the source or an instruction file voids every pass in that walk, and its failures still count as findings. The scorer also records the time to the first useful result, from transcript timestamps.

Done when every journey has a scored outcome per surface and variant, with its transcript and screenshots.

### 6. Sweep the states the walk does not reach

Sweepers force what a walk misses: failures, bad input, destructive actions, layout and access, languages, agent surfaces, cross-surface truth and promises. The catalogue is in [references/sweeps.md](references/sweeps.md). Run each sweep script first against a known violation and watch it go red. A sweep that never failed proves nothing.

Then two inspectors, blind to each other, read the whole screenshot set for problems that span screens. An inspection finding with no effect in any walk or sweep is at most minor.

Done when every sweep that applies has run, each was seen red once, and every non-pass is a candidate finding with evidence.

### 7. Verify every finding

Each candidate carries its journey, persona, surface, variant and step, and what was expected. It also carries the exact text seen, the evidence path, steps to reproduce, a proposed severity and the walks it hit out of the walks run.

Give the verifier two worked examples first: one real finding, and one tester artefact (a click on a pop-up a person would close). It has no write tools, and its default verdict is "not reproduced". It checks each finding by its class:

- **Defect.** The same input gives the same failure. Replay it from a clean start.
- **Findability or comprehension.** Check the transcript and screenshots: was the way forward visible from where the walker looked? When unsure, run a second fresh walk with the same brief.
- **Intermittent.** Retry it three times. If it does not come back, keep it as "intermittent" with the original evidence.

Before it calls an API broken, the verifier reads the request that the product's own client sends. It returns **reproduced**, **intermittent**, **not reproduced** or **artefact**, with its own evidence and severity. Keep the first two, with the original evidence for an intermittent one. Drop the last two. When the severities differ, keep the higher one. It merges findings by symptom and location, because it has not read the source.

For a security problem (an auth bypass, a data leak), draft a report for the repo's private security channel. Show the user the exact text and send it only on their yes in the session. Fix it only through a private advisory fork, or leave the fix to the user. Never fix it in a public PR. It stays out of the report, PR bodies and screenshots until its fix lands.

Verifiers that each take one group of walks cannot merge findings across groups, and several walkers often report the same line. So before step 8, one merge pass reads every kept finding together.

Done when every candidate is reproduced or intermittent with evidence, or dropped with a reason. With `--no-fix`, go to step 10.

### 8. Fix what makes an existing job doable

The fixer reads the source and merges findings by root cause. It fixes the blockers and majors that stop a job the product already offers or the docs promise. It fixes a minor only when the fix stays inside one screen or one message.

Everything else gets status `NEEDS-FIX` in the report, with its evidence, proposed acceptance criteria and who should take it. A new feature, a redesign or a change to what the product promises goes to the owner. A blocker with an unclear root cause goes to `investigate`. A defect in a dependency gets an upstream issue: draft it, show the user the text, and post it only on their yes in the session.

For each root cause, in severity order:

1. Write the failing path as a test in the repo's existing test stack. Never add a test framework without asking. When no test can express it, the re-walk transcript is the regression evidence, and the PR says so.
2. Make the smallest fix in a worktree, following the repo's own rules. Fixers run in parallel only on files that do not overlap.
3. Run the repo's checks and the new test. A reviewer reads the diff against the finding and the test.
4. Open one PR per root cause with `file-pr`, with screenshots before and after for a UI change and a recording for a flow. Run the text through `readable` when it is installed. Screenshots show test identities and invented data only.

Stop after two fixes in a row are reverted because their reviewer rejected them or their re-walk failed. Stop too when a fix needs a file unrelated to its finding, and report why. Merge only when the user asked for merging in this session.

Done when every verified blocker and major is in a PR or has status `NEEDS-FIX` with a reason.

### 9. Walk it again

A fix is proven when fresh walkers reach the done condition within budget on the fixed build. Use the original brief byte for byte, the same starting state, and as many walks on the same models as the first run. Every one must pass, and the scorer scores them. Rerun the sweep that found the problem too.

Never rerun a failed walk without a change in between. Keep every outcome in the report, so that nobody can pick the one pass. When the fix is deployed and the step is safe to repeat there, walk it once more where users meet it. A finding that comes back reopens its PR, and a new problem goes through step 7.

Done when every fix has its re-walk results attached to its PR.

### 10. Keep the journey report in the repo

Every run reads and updates one living doc in the product repo: `docs/user-journeys.md`, or the path the repo already uses. It holds:

- the surfaces and the personas
- one row per journey, with its surfaces, every outcome of the last run, the date, the commit walked and the time to the first useful result
- the findings: fixed with their PR, open with severity and evidence, `NEEDS-FIX` with who should take each
- the unverified areas: every shortcut a walk used, and every journey not reached with what would reach it
- what held: the journeys tried hard that passed
- what an agent cannot judge: how people feel, a real screen reader, real devices, and numbers that need real users
- a prompt for a person's own walk: "Tell us where you paused, guessed, waited, or saw a result you did not trust."

The report never names a security finding before its fix lands, and never claims that a person's walk happened. Commit only screenshots of test data. Run `readable` over the report when it is installed, and land it through the repo's gate. Then delete the sandboxes, test instances, test identities, worktrees and containers the run made.

Done when the report is pushed, its URL is in your reply, and the run's sandboxes are gone.

## Severity

Rank by what the person loses, never by a score or a grade. A problem matters when it changes a choice, hides progress, blocks a result or costs real time. Any other problem is cosmetic.

| Level | Meaning |
| --- | --- |
| **blocker** | A basic job cannot be finished: install, sign in, get data in, the main job, recovery from an error. Also data lost without warning, a status that says something false, and a core journey that the keyboard alone cannot finish. |
| **major** | The job finishes only with a workaround from outside the product, a promised advanced job fails, a screen is a dead end, or two surfaces show one fact differently. |
| **minor** | The job finishes with extra steps, a wait without feedback, or a message that confuses but lets the person recover. |
| **cosmetic** | No effect on any walk. Reported, not fixed. |

Frequency (walks hit out of walks run) raises priority inside a level. It never drops a blocker.

## Limits

- It builds no new feature and redesigns nothing without the owner.
- It never counts a walk that took a shortcut as covered.
- It posts nothing as the user outside the PRs it opens. It merges, deploys or publishes only on their word in this session.
- It replaces no person. It finds where a flow breaks, not how it feels.
