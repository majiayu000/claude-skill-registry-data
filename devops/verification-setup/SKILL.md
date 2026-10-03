---
name: verification-setup
description: >
  Interviews the owner, one topic at a time, and writes `.claude/rules/verification.md` —
  the environments, resource capacity, refresh/deploy commands, test identities, tooling,
  known gaps, and coverage floor the functional-verification loop needs to run for real.
  Detects what it can from the repository first and offers that as the default; the owner
  answers or keeps the current value. Recommends a coverage floor from this project's own
  past verification runs. Owner-invoked only — no command or agent may reach it.
when_to_use: >
  Reach for this right after `/init-project` ships the file unfilled, whenever a readout or
  `/refine-verification` names a need against `.claude/rules/verification.md`,
  or any time the owner wants to change what the file says. Not for reading the file (any
  agent does that directly) and not for a run that only needs to check whether it is filled
  (`check-verification-unfilled`, `functional-verification.js`).
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# verification-setup

`.claude/rules/verification.md` is owner-governed: infrastructure policy, not something a
model should guess at. This skill is the only way it gets written or changed — running it
IS the owner's approval, so there is no separate confirmation step once the interview is
done.

## When it applies

- A new project, right after `/init-project` copies the template unfilled.
- A readout — `/implement-trd`, `/verify-build`, or a phase gate — that named this skill
  because `check-verification-unfilled` found a missing section.
- A `/verify-build --fix` run recorded a need against the file (`/refine-verification`
  names such needs in its diagnosis; it never records or edits anything there).
- Any time the owner wants to change what the file says, filled or not.

## Inputs

| Input | Where it comes from |
|---|---|
| The current file | `.claude/rules/verification.md`, or `template.md` (this skill's own directory) when the file is absent |
| The current shape | `template.md` — the shipped template, current as of the last install or refresh |
| What sections are missing | `check-verification-unfilled` (`functional-verification.js`), read for `missingSections` |
| Repo signals | `package.json` scripts, `docker-compose*`, `.env*.example` (key names only — see Never), `vercel.json`, `railway.json`/`railway.toml`, `.claude/verification-notes.md`, `CLAUDE.md` |
| Installed detectors | `tooling-detector`, `framework-detector`, `test-detector`, `cloud-provider-detector`, whichever exist under `.claude/skills/` in this project — used when present, never assumed |
| A coverage-floor recommendation | `recommend-coverage-floor .trd-state` (`functional-verification.js`), reading every `*/verification-state.json` |
| Recorded needs | `.trd-state/*/discovered.jsonl` rows whose `file` is `.claude/rules/verification.md` — the needs `/verify-build --fix` records |

## Topics

One `AskUserQuestion` call per topic, in the file's own order, so the interview reads the
way the file does rather than jumping around:

1. **§1 Environments** — name, URL/reach, purpose, and the three permission columns (may
   write data?, may deploy?, may restart?).
2. **§1a Resource capacity** — how many of each resource may exist at once, and how the loop
   tells instances apart when more than one exists.
3. **§2 Refresh and deploy** — the fast refresh run after every debug pass, and the full
   deploy run once at the end.
4. **§3 Test identities** — where each credential *lives* (a vault item, an env key, a file
   path) — never its value.
5. **§4 Tooling** — what verification tooling is actually installed and configured today.
6. **§5 What cannot be verified here** — the gaps, stated plainly, so they read as a stated
   limit rather than a silent pass.
7. **§5a Coverage floor** — see Coverage floor, below.
8. **§5b Never unattended** — see Never unattended, below.
9. **§6 Multi-repo** — only when the system spans more than one repository.

Each call offers, in this order: the detected value (marked as detected, with its source),
then the file's current value where it differs from the detection, then "keep". An answer of
"keep" — or skipping the topic — leaves that section's current content untouched; nothing is
rewritten just because the topic was visited.

The three permission columns, the §1a counts, and whether a gap in §5 is permanent are
owner-only: nothing in the repository can tell the skill whether staging may be written to.
These default to the template's own example row for that environment kind, labelled "not
detectable — the conservative default" rather than presented as a real detection.

**Re-running on an already-filled file asks only what changed.** A topic is asked again only
when: its section is missing from the current file, the repo's detected evidence now differs
from what the file says, or a recorded need (see Inputs) names it. Every other topic is left
alone and listed as unchanged in the closing summary — a re-run is a targeted update, not a
second full interview.

## Coverage floor

The question itself tells the owner what the floor is before asking for a value, in these words or close to them:
"The coverage floor is the share of the success definition's criteria that must be proven (met) before a verification run may report satisfied; a run that proves less than this reports insufficient-coverage instead, even with no open gaps."
It is asked in the same `AskUserQuestion` call that carries the table and recommendation below, so the owner sees the definition, the working and the recommended value together.

Shown as one small table, one row per past run this project has: feature, proven/total
criteria, and the proven share. Then the recommendation itself, with the reasoning that
produced it in one line — which run was lowest, and what its share rounded down to the
nearest 5% — because that is showing the owner the working, not just the number. When the
lowest satisfied run proved very little of its own criteria, the skill says so plainly, with
that run's own figures, and leaves the decision to the owner rather than filing the number
past them. With no past run that ended `satisfied`, the recommendation is "no floor
recommended yet — none of this project's runs has ended satisfied; a floor can be added
after the first ones do." Any answer is accepted at this topic, including `none`, but it is
written as `Coverage floor: <N>%` or `Coverage floor: none` — the only two forms
`read-coverage-floor` parses. An answer of `0.6` or `60` is written as `60%`, and the
recommendation (a fraction in the CLI's output) is offered as a percentage too.

## Never unattended

§5b is the list of paths `/plan --implement` will never build without the owner watching.

The question itself states that in one sentence before asking for a value: "Never-unattended
paths are folders `/plan --implement` will never build without you watching — nothing is
written without your answer." It is asked in the same `AskUserQuestion` call that carries the
detected default below, so the owner sees the reasoning and the proposal together.

The detected default is every folder that EXISTS in this repository whose path matches
`auth`, `payments`, `billing`, `migrations`, `secrets`, or `infra`/`prod` (substring match,
same as the brake itself) — offered as a starting list for the owner to edit, never written
as-is without an answer. With no matching folder in the repo, the default is `Paths: none`.

Any answer is accepted, including `none` or an edited list, but it is written in exactly the
two forms `readNeverUnattended` parses: one `- <fragment>` bullet per path, or a single
`Paths: none` line — never both in the same file, and never a bullet or a `Paths:` value left
empty.

## Writing

Once every topic has an answer (an explicit value, "keep", or an owner-only default), the
whole file is written at once, in the current shape. There is no preview step and no second
confirmation — invoking this skill was the approval. A section the interview did not change
keeps its owner-authored content verbatim.

After writing, the skill re-runs `check-verification-unfilled`, `read-coverage-floor`, and
`read-never-unattended` against the file it just wrote. A non-empty `missingSections`, a
floor that reads `invalid`, or a never-unattended list that reads `invalid`, is the skill's
own defect — report it in ISSUES rather than silently shipping a file the next check would
flag.

## Never

- **Write a credential's value.** Only a vault item name, an env key name, or a file path —
  never a password, token, or connection string. If an answer to a topic looks like it holds
  a value rather than a location, do not write it; ask for the location instead.
- **Contact or probe an environment.** Detection reads files already in the repository; it
  never makes a network call to confirm a URL is reachable or a service is up.
- **Edit any file other than `.claude/rules/verification.md`.** Not the template, not a rule
  file, not a TRD — one file, always.
- **Start a verification run, or any other command.** Writing the file is this skill's whole
  job. Running `/verify-build`, `/implement-trd`, or anything else that reads the file it just
  wrote is the owner's own next invocation to make.

## Readout

Ends with the framework's standard four-section readout (STATE / DECISIONS / ISSUES / NEXT,
`.claude/rules/command-status.md`). STATE lists what changed, section by section, and what
stayed unchanged. DECISIONS lists every owner-only default applied where no answer came in.
ISSUES lists anything the topics left blank, plus anything the post-write re-check found.
NEXT gives the next command a filled file makes possible — typically `/verify-build` or
`/implement-trd`.

Then the `═══ COMMAND COMPLETE: /verification-setup ═══` banner, and a call to
`.claude/hooks/notify-complete.sh verification-setup complete "<one-line summary>"` — the
same close every workflow command uses, so the run-state marker `autonomy.md`'s Judgment B
depends on is actually cleared.
