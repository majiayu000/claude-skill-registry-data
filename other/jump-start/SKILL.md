---
name: jump-start
description: Creates an entire new project from one prompt. Takes a project name plus a brief, clarifies only what would change the architecture, publishes a design artifact and re-confirms after every revision, then runs an unattended multi-agent OPM build in Claude Code's auto-accept permission mode, verifies it, and leaves the app running locally or on a device or simulator. Use when the user runs /opm:jump-start <project-name> <brief> or asks to build a whole new project from a description.
argument-hint: <project-name> <project brief>
disable-model-invocation: true
---

# Jump-start

One prompt in, a running project out. The developer is involved at exactly
three points: the brief, the design approval loop, and the go-ahead for the
unattended build. Everything after the go-ahead runs without questions.

Invocation text is in `$ARGUMENTS`. Helper script:
`sh "${CLAUDE_PLUGIN_ROOT}/scripts/dev-server.sh"` (start, stop, status).

## Gates

| Gate | Passes only when |
|---|---|
| G1 Brief | Project name and a brief that answers the architecture questions, or explicit assumptions written down |
| G2 Design | The developer chose "Approve" on the latest artifact revision, not an earlier one |
| G3 Build | The developer confirmed the build plan AND said the permission mode is set |
| G4 Done | `opm:verification-before-completion` passed and the app is reachable |

Never skip a gate. Never treat silence or an implicit "sounds good" as passing one.

## Phase 0: parse and set up

1. First whitespace-separated token of `$ARGUMENTS` is the project name. Normalise it to kebab-case. Everything after it is the brief.
2. If the brief is shorter than about 20 words, ask one question: "What should `<name>` do, for whom, and on which platform (web, mobile, API)?" Then continue with the answer.
3. Directory: if the current directory is empty and already named `<name>`, use it. Otherwise create `./<name>/`. If a non-empty `./<name>/` exists, stop and ask whether to resume (see Resuming) or pick another name.
4. Inside the project: `git init -b main`, write `docs/specs/brief.md` from `templates/brief.md`, filling what the brief gives and marking the rest `TBD`.

## Phase 1: understand, brainstorm only if required

Score the brief against this checklist. A gap counts only if the answer would change the stack, the data model or the screen list.

| Question | Counts as a gap when |
|---|---|
| Who uses it | Unknown and the product could be consumer or internal |
| Platform | Web, mobile, API or a mix is not stated and cannot be inferred |
| Core flows | Fewer than two end-to-end flows can be named |
| Data | The main entities cannot be listed |
| Auth | Sign-in requirement is unknown for a multi-user product |
| Integrations | A named third party (payments, maps, chat) lacks a provider |
| Realtime or offline | The brief hints at live updates or offline use without saying so |
| Constraints | Compliance, budget or deadline that forces a stack choice |

- Zero or one gap: write the assumptions into `docs/specs/brief.md` under "Assumptions" and continue.
- Two or more gaps: invoke `opm:brainstorming` on the bounded path, restricted to those gaps, at most five questions, one at a time. Never ask about something the brief already answers.

## Phase 2: choose the stack

A stack named in the brief always wins. Otherwise use the defaults:

| Brief says | Stack |
|---|---|
| Web app | Next.js App Router, TypeScript, Tailwind, Vitest, Playwright |
| API only | Fastify + TypeScript + Vitest; FastAPI + uv + pytest when the brief says Python |
| Mobile app | Flutter, Riverpod, Firebase (Auth, Firestore) |
| Mobile and web | Flutter for mobile, Next.js for web, shared Firebase project |
| Data | Firebase by default; Postgres + Prisma when relational needs are explicit |

Record the choice and the reason in the design. Load the matching patterns skill
(`opm:react-patterns`, `opm:python-patterns`, `opm:flutter-patterns`) before designing.

## Phase 3: design artifact, confirm after every change

Build the design from `templates/design-outline.md`: overview and goals,
personas and user flows, screen inventory with low-fidelity wireframes (inline
SVG or bordered HTML boxes), navigation map, data model with relations,
architecture diagram, API or contract list, stack with reasons, milestone
outline, open assumptions.

Publishing:
- If the Artifact tool is available, load the `artifact-design` skill first. For UI-heavy products load `design` instead and lay screens out as artboards. Keep the artifact title stable and republish the same file for every revision so the link never changes.
- If there is no Artifact tool, write `docs/design/index.html` and open it with `open` (macOS) or `xdg-open` (Linux).

Approval loop, repeated until approved:
1. Share the link and a five-line summary of what the design commits to.
2. Ask with AskUserQuestion: "Approve design and start the build" or "Request changes" (free text).
3. On changes: revise, republish, list what changed in three bullets, and ask again. Every revision gets its own approval question, even a one-word tweak.
4. On approval: write the markdown mirror to `docs/specs/YYYY-MM-DD-<name>-design.md`, record the artifact link in it, commit.

## Phase 4: authorise the unattended build

Explain in about five lines: the phases that will run, that no further
questions will be asked, that decisions will be logged instead, the estimated
time, and how to stop (interrupt the session, or `dev-server.sh stop` later).

Then ask one confirmation question with these options and free text for
preferences: time budget (default 4 hours), and for mobile the target
(connected device, iOS simulator, Android emulator, or auto).

Permission mode. Claude Code cannot change its own permission mode and OPM does
not write permission rules on the developer's behalf. Tell the developer to pick
one of the built-in options and to reply when it is set:

1. Press Shift+Tab until the mode indicator shows auto mode. Recommended. Every action still passes Claude Code's safety classifier.
2. In a sandbox or container, restart with `claude --permission-mode bypassPermissions` inside the project directory and run `/opm:jump-start <name>` again; Resuming picks up from the approved design.
3. Stay in default mode and approve prompts as they appear. The build still works, it is just not unattended.

Wait for the developer's reply. Do not start Phase 5 before it. From here on:
no questions. Decisions go to `docs/milestones/<milestone>/DECISIONS.md`
(`templates/decisions.md`) under the `opm:milestone-planning` deviation rules.

## Phase 5: plan

Invoke `opm:milestone-planning` for milestone `v0.1`. Required shape:

- Phase 0, foundation: scaffold from the official generator, lint, format, typecheck, unit tests, a CI workflow, `.env.example`, README, and a health route or hello screen. Must be green before anything else.
- Feature phases: one vertical slice per core flow from the screen inventory, ordered by dependency.
- Hardening phase: error and empty states, loading states, accessibility basics, seed data, security review fixes.

Plans hold two to four tasks, declare `files_modified`, and get `wave` numbers
so independent plans run in parallel.

## Phase 6: build, multi-agent

For each phase, for each wave:

1. Dispatch one general-purpose subagent per plan in a single message so they run in parallel. Each brief contains only: the plan text, the interfaces it consumes, the stack rules from the patterns skill, the repository path, and the instruction to follow `opm:executing-plans` inline mode with `opm:tdd-workflow` per task and to commit per task. Never paste the whole roadmap or the chat history.
2. If the Workflow tool is available, the developer opted in to orchestration by invoking jump-start, so a wave may run as a workflow instead of parallel Agent calls.
3. After the wave: run build and tests. If red, dispatch one fix subagent with the failing output and the files involved. Do not start the next wave on red.
4. After the phase: write SUMMARY files, update STATE.md, append to `docs/milestones/v0.1/PROGRESS.md`, commit.

Subagents may not ask the developer anything. If a plan is blocked, the
orchestrator decides, logs the decision, and moves on. Only stop the run for
the four stop conditions in `opm:executing-plans`.

## Phase 7: verify

1. Run `opm:verification-loop` on the whole project.
2. Dispatch `code-reviewer`, `security-reviewer` and `silent-failure-hunter` in parallel on the full tree.
3. Fix every CRITICAL and HIGH finding, then rerun the loop.
4. Run `opm:verification-before-completion`. G4 needs real output, not a summary.

## Phase 8: run it

Web or API:
```
sh "${CLAUDE_PLUGIN_ROOT}/scripts/dev-server.sh" start --project "<abs path>" --name web --url http://localhost:<port> -- <dev command>
```
On `READY`, smoke-test two or three routes with curl, and run Playwright if configured. Keep the process running.

Mobile (Flutter):
1. `flutter devices`.
2. Pick the target in this order: the developer's stated preference, a connected physical device, an already booted simulator or emulator, then boot one (`open -a Simulator` and wait until `flutter devices` lists it, or `flutter emulators --launch <id>`).
3. Start detached: `dev-server.sh start --project "<abs path>" --name mobile -- flutter run -d <device id>` (no `--url`).
4. Confirm from `.opm/mobile.log` that the app launched. Keep it running.

If the app cannot start, treat it as a failing verification: fix, then retry.

## Phase 9: finish

1. Run `opm:compound-learnings` if anything non-obvious was learned.
2. Commit everything.
3. Report using `templates/final-report.md`: what was built, the URL or device, how to stop, test and review numbers, known gaps and assumptions, next steps.
4. Optional: `/opm:explainer-video <path>` turns this into a narrated explainer.

## Resuming

When invoked in a directory that already has jump-start artefacts, continue
from the right point instead of starting over:

| Found | Resume at |
|---|---|
| `docs/specs/brief.md` only | Phase 1 |
| A design mirror in `docs/specs/` but no `docs/milestones/` | Phase 4 |
| `docs/milestones/v0.1/STATE.md` | Read STATE.md and PROGRESS.md, then Phase 6 at the first incomplete wave |
| All phases complete in STATE.md | Phase 7 |

## Red flags

| Thought | Reality |
|---|---|
| "The design is obvious, skip the artifact" | The artifact is how the developer catches wrong assumptions cheaply. Build it. |
| "They approved the previous version, this tweak is fine" | Every revision needs its own approval. Ask. |
| "I'll ask the developer one quick question mid-build" | The developer walked away. Decide, log it, continue. |
| "Tests can come after the features" | Every task follows `opm:tdd-workflow`. |
| "Skip the foundation phase, go straight to features" | Green tooling first or every later wave fights the setup. |
| "One big subagent can do the whole phase" | One plan per subagent keeps context small and failures local. |
| "It compiled, so it runs" | G4 needs the app reachable and smoke-tested. |

## Safety

- Nothing leaves the machine: no deploys, no publishing, no pushes to a remote, unless the brief asked for it explicitly.
- Secrets only in `.env`, never committed; `.env.example` documents the keys.
- The build stays inside the project directory. Global installs need a logged decision.
- The developer chooses the permission mode. Do not suggest ways around prompts beyond the three built-in options.
