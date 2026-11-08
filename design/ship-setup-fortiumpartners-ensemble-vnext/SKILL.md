---
name: ship-setup
description: >
  Interviews the owner, one topic at a time, and writes `.claude/rules/ship.md` — the
  ordered string of shipping steps (push, open a pull request, review rounds, merge,
  release, and whatever the contracts directory offers) that `/ship-build` runs. Offers the
  most common string first so accepting it is one answer, asks each offered step's own
  parameters, and, on the owner's yes, installs the workflow that resumes a parked run when
  a reviewer approves. Owner-invoked only — no command or agent may reach it.
when_to_use: >
  Reach for this right after `/init-project` ships `ship.md` with no step under `## Ship`,
  when `/ship-build` reports it only pushed because there is no policy, or any time the owner
  wants to change how this project ships. Not for running a ship (that is `/ship-build`) and
  not for reading the file (any agent does that directly).
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# ship-setup

`.claude/rules/ship.md` is owner-governed: it is the standing authorization for every
outward-facing act `/ship-build` takes (a merge, a deploy, a command run on the owner's
behalf). This skill is the only way it gets written or changed — running it IS the owner's
approval of each step it records, so there is no confirmation step after the interview.
Until it has run, `ship.md` lists no step and `/ship-build` only pushes.

## When it applies

- A new project, right after `/init-project` copies the template with an empty `## Ship`.
- `/ship-build` ended by saying there is no policy and how to set one.
- Any time the owner wants to add, drop, reorder or re-parameterise a step.

## Inputs

| Input | Where it comes from |
|---|---|
| The current file | `.claude/rules/ship.md`, or `template.md` (this skill's own directory) when the file is absent |
| The current shape | `template.md` — the shipped template, with its worked examples |
| The steps on offer | one file per step, `.claude/contracts/ship-primitive-<name>.md`; the list of steps is the list of files. Never a list held in this skill |
| What a step asks | each contract's front matter `params:`, its `## Input` text and, when present, its `## Setup` section — see Per-step questions |
| Whether a deploy command exists | `readFullDeploy` in `.claude/lib/functional-verification.js`, run over `.claude/rules/verification.md` section 2 |
| Whether the project has a design | `docs/ui/*/design-map.json` |
| The workflow template | `ensemble-ship-resume.yml` (this skill's own directory) |

## Topics

One `AskUserQuestion` call per topic, detected value first, then the current file's value
where it differs, then "keep". Skipping a topic leaves that part of the file untouched.

1. **The default string.** Offer it first, as the first option, so accepting it is one
   answer. It is the string labelled "the default string" in `template.md`'s examples: push,
   open a pull request, a bounded review-and-fix block, merge, release, then the after-shipping
   steps. Show the whole string in the question. If the owner accepts it, go to Per-step
   questions for the values it leaves blank (the `release` environment, command and identity);
   otherwise go to topic 2.
2. **Build the string.** Offer the steps from the contracts directory, in the order the owner
   chooses, using each contract's one-line description (the line under its heading). Two are
   special-cased by what the project has, not by name in the contract:
   - `sync-design` is offered only when `docs/ui/*/design-map.json` exists. With no design, it
     is not offered and is not mentioned as a gap.
   - `await-approval` is offered with its trigger. Choosing it also raises the trigger workflow
     (topic 4).
   A repeating block is written as `repeat` with indented `- <step>` lines, no nesting; it is
   the sequencer's own construct, not a contract.
3. **After shipping.** The steps the owner wants run once the work is merged or released, from
   the contracts whose `section:` is `after` or `any`.
4. **The trigger workflow.** Asked only when the chosen string contains `await-approval`. Say
   what it does in one sentence (a reviewer's approval runs `/ship-build --resume` in GitHub
   Actions), where its credential lives (the repository secret `ANTHROPIC_API_KEY`, which the
   owner adds themselves — this skill never sees or writes the value), and that it only takes
   effect once the file is on the default branch. On a yes, install it (see Writing); on a no,
   write the string without `trigger=github-actions` so nothing claims a trigger that is not
   there.

Re-running on a filled file asks only what changed: a step the contracts now offer that the
file does not use, a parameter a contract gained, or a value the file leaves blank. Everything
else is left alone and listed as unchanged in the closing summary.

## Per-step questions

For every step the owner chose, ask for each parameter its contract declares. Read them from
the contract, never from this file: `params:` in the front matter lists them, where `name=value`
is optional with that default, `name=` is optional with none, and a bare `name` is required.
Quote the contract's `## Input` text beside the question and offer its default as the first
option. A step whose contract declares a parameter this skill has never heard of is asked
that parameter all the same — a new step needs no edit here.

A contract may also carry an optional `## Setup` section: extra things to ask or warn about
for that step. Read it and ask what it says; its absence means nothing more to ask.

What the contracts declare today, so the owner is not surprised (the contract is the
authority, not this list):

- **`repeat`** — `rounds` (default 2), the most passes the block makes. `until` is left out: a
  `repeat` with no `until=` takes the one its body's contract declares.
- **`collect-findings`** — `bar` (default `significant`), the level of finding the work must
  fix before it ships; below it, findings are recorded and filed, not fixed.
- **`release`** — `env`, `command`, `identity`:
  - `env`: ask which environment, as named in `verification.md` section 1. Where exactly one
    environment declares a full-deploy command, offer it.
  - `command`: ask only where `readFullDeploy(<verification.md text>, <env>)` returns no
    command. Where it returns one, say that `release` will reuse it and ask nothing. Where it
    returns none, ask for the command to run; with no answer, leave `release` out rather than
    write a step that stops every run.
  - `identity`: ask for a command that prints the commit the deployed environment is running,
    and say plainly that **it must report the commit released from this work**, not merely the
    environment's latest build — the release check compares its output to the commit the run
    pushed, and a command that reports something else fails every release.
- **`run`** — the command, verbatim, to the end of the line.

## Writing

Once every topic has an answer, write the whole file at once in the template's shape: the
template's preamble kept verbatim, `## Ship` and `## After shipping` filled in the line format
`N. <step> key=value key="quoted value"`, and the template's `## Examples (not run)` section
kept as it is. There is no preview step and no second confirmation. A part the interview did
not change keeps its content verbatim.

On a yes to the trigger workflow, also write `.github/workflows/ensemble-ship-resume.yml` as a
copy of `ensemble-ship-resume.yml` from this skill's directory, unchanged. That is the only
other file this skill writes.

After writing, re-parse with the sequencer, so there is one parser and not a second one here:

```
node .claude/lib/ship-sequencer.js parse --policy .claude/rules/ship.md
```

Any entry in its `errors` is this skill's own defect: report each in ISSUES, with the line
number, rather than leaving a file the next `/ship-build` would refuse.

## Never

- **Write a credential's value.** Name where one lives (a repository secret's name, a vault
  item, an environment variable's name) — never the token, password or key. If an answer looks
  like a value rather than a location, do not write it; ask for the location.
- **Edit any file other than `.claude/rules/ship.md`** and, on the owner's yes, the workflow
  file. Never `.claude/settings.json`, never `verification.md`, never a contract.
- **Contact or probe anything.** Detection reads files in the repository; it makes no network
  call and runs no deploy, merge or push.
- **Start a ship.** Running `/ship-build` is the owner's own next invocation.

## Readout

Ends with the framework's standard four-section readout (STATE / DECISIONS / ISSUES / NEXT,
`.claude/rules/command-status.md`). STATE lists the string written, step by step, whether the
workflow was installed, and what stayed unchanged. DECISIONS lists every default applied where
no answer came in. ISSUES lists parse errors from the re-check, a `release` left out for want of
a command, and a workflow written but not yet on the default branch (the owner must merge it,
and add the secret, before it fires). NEXT gives `/ship-build` when a policy now exists.

Then the `═══ COMMAND COMPLETE: /ship-setup ═══` banner, and a call to
`.claude/hooks/notify-complete.sh ship-setup complete "<one-line summary>"` — the same close
every workflow command uses, so the run-state marker `autonomy.md`'s Judgment B depends on is
actually cleared.
