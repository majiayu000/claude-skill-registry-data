---
name: project-config
description: >
  The memoized source of truth for HOW a project is structured and run — node
  version (.nvmrc), env setup (.envrc/direnv), package manager, tsconfig, monorepo
  layout, and the exact command to install / run / build / test / lint / migrate
  each app or service. Consult it FIRST — before running, building, testing, setting
  up, or migrating anything, and before briefing a sub-agent that will — instead of
  re-discovering these facts every session. Invoke on any "how do I run/test/build
  X", "set up the env", "which node/pnpm version", or before your first shell command
  in a repo. If a needed config isn't recorded here, find it once and record it
  immediately. Do NOT use for judgment calls: dev-tooling design → infrastructure;
  where logic lives → service-architecture; the test loop → tdd-skill; query tuning
  → database-optimization. This skill only records what is true right now.
---

# Project Config

This skill is a **lookup table, not advice.** Its job is to eliminate the repeated
"where's the node version / how do I run the API service / what sources the env vars"
searches. The concrete answers live in per-project reference files; this file is the
protocol for using and maintaining them. Sibling skills own the *judgment* (see the
description); when they need "the actual command / version / path," they read it here.

## The two gates (always both — they are the whole skill)

**Gate 1 — CONSULT before you act.** Before you run, build, test, lint, migrate, set
up, or boot anything — or reason about tsconfig / module layout / env — read the
relevant project reference file below and use the recorded facts. Why: rediscovery
burns context and gets it wrong (wrong node version, wrong runner config, unloaded
env), and the answer was already paid for once.

If you're about to `grep` for `.nvmrc`, open `package.json` to find a script, or
"figure out how env loads" — stop. Open the reference file first. Only investigate
the repo when the file doesn't answer, and then Gate 2 applies.

**Gate 2 — RECORD on miss, immediately.** The moment you have to *go looking* for a
config this skill doesn't already contain — a run/build/test command, a version, an
env mechanism, a path alias, a service port, an invocation gotcha — **append it to the
right reference file in the same turn**, before moving on. Why: a miss is a bug in
this skill; unrecorded, the next session pays the discovery cost again. Verify the
fact (run it / read it) before recording so we don't cache something wrong. Do not
defer recording to "at the end" — end-of-session recording is how facts get lost.

### Orchestrator rule (sub-agents can't ask)

When delegating work via the Agent tool, **paste the relevant config facts from the
reference file directly into the agent's brief** (node version, how to source env, the
exact run/test/build command, workspace layout). Why: the sub-agent starts with the
answers instead of burning its context rediscovering them — and it cannot pause to ask.
If it still hits a gap, its returned summary must name the missing config so the
orchestrator records it here (Gate 2 by proxy).

## What belongs here vs. not

**Record:** node/tool versions, package manager + version, how env loads (the
*mechanism* and the expected variable **names** — see secrets note), monorepo/workspace
layout, per-app install/run/build/test/lint/format/migrate commands, tsconfig shape &
path aliases, service ports & URLs, dev-server start/restart procedure, publish/release
commands, and any **invocation gotcha** (e.g. "the CLI needs Node 22", "test DB must be a
fresh migrate DB"). Cross-link the deeper writeup (a doc or note) when one exists; this
install's cross-link form is in `LOCAL.md` beside this skill, when your copy keeps one —
*Cross-linking a deeper writeup*.

**Don't record:** secret **values** (never — see below), one-off analysis, architectural
opinions (→ service-architecture), or anything the file already states. Keep entries
terse and command-first.

### Secrets

**Never store an env var's value here** — record only the variable **name** and the
**mechanism** that loads it (e.g. "`direnv allow`, or `set -a; . .envrc; set +a`").
Names like `STRIPE_SECRET_KEY` are fine; values, prefixes, or lengths are not. This
mirrors the global never-print-env-vars rule.

## Project reference files (the index)

Read the file for the project you're working in. Add a new file when work starts in a
project not listed yet: one file per project, beside this skill, named after the project
(`<project>.md`), with a one-line index entry saying what the project is.

This install keeps its index, and adds new entries to it, in `LOCAL.md` beside this
skill, when your copy keeps one — *Project reference files (the index)*. Without one,
list the entries here.

## Common failure modes (stop if you catch yourself doing these)

- **Running a command from memory of "how these projects usually work"** (e.g. `npm
  install` in a pnpm-pinned repo, default-node in a Node-22 repo) instead of consulting
  the file — the reference exists precisely because this repo deviates.
- **Briefing a sub-agent with "figure out how to run the tests"** — paste the recorded
  command; the agent can't ask when it guesses wrong.
- **Discovering a fact the hard way and moving on without recording it** — the next
  session repeats the same dead ends. Record in the same turn.
- **Recording an unverified guess** — a wrong cached fact is worse than a miss; run or
  read it first.
- **Pasting a secret value into a reference file** — names and mechanisms only.

## Before you call this done (any session that touched project tooling)

- Every run/build/test command you executed came from (or is now in) the reference file.
- Any config fact you had to discover this session is recorded, verified, in the right
  file.
- Sub-agent briefs you sent included the concrete config facts, not "go find out".
- No secret values landed in any reference file.

## Maintenance

If any reference file grows past ~250 lines, split it by app/service behind a slim index
(this install's split rule: `LOCAL.md` beside this skill, when your copy keeps one —
*Splitting a reference file*). On handoff / "update skills", do a quick pass: confirm the
recorded commands still match `package.json`/`Makefile`, and fold in anything discovered
this session that isn't captured yet.
