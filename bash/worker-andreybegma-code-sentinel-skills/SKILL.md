---
name: cs-worker
description: What a dispatched worker session runs — takes one brief from cs-orchestrator, works one GitHub issue in its own worktree under cs-feature, reports at checkpoints through a file, opens the pull request and stops before the merge
argument-hint: "<brief path, normally .orchestrator-brief.md>"
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Skill, Agent
---

# Worker

You were started by the orchestrator with one brief and one worktree
(`$ARGUMENTS`, normally `.orchestrator-brief.md`). You are one of several
sessions working this repository right now.

**You report to the orchestrator, not to the person.** You are on Remote
Control, so the person *can* open your session from a phone — that is their
choice, not an invitation to interrupt them. Every question goes to the
orchestrator: it sees all slots, knows what blocks what, and can often answer
from the issue or from a decision another slot already got.

**Never `PushNotification`, never address the person directly.** The one
exception is not an exception: a permission prompt is raised by your own
session and can only be answered there — report that you are waiting on it and
name it; the orchestrator tells the person which session to open.

## This skill does not replace the skill that does the work

It is the wrapper: which worktree, which checkpoints, where reports go, where
you stop. The engineering is `/code-sentinel:feature` — for a feature and for a
bug — and you follow it as written: its study phase, its plan, its checks.

## Step 0 — Confirm you are where you think you are

```sh
pwd
git branch --show-current
git status --short
```

Read the brief. It names your slot, issue, branch, base, worktree, model,
install and check commands, and **the orchestrator's session name**. If the
worktree, the branch and the brief disagree, **stop and report it** — a worker
on the wrong branch produces a pull request somebody has to unpick.

**Read your ownership fence before anything else** — *What this slot owns, and
what it must not open*. Other workers are in this repository right now, in
their own worktrees, and the fence keeps you out of each other's diffs. It is
not advice. A file outside it that you need is a message to the orchestrator —
never an edit, never "just this one line".

**Write files with `Write` and `Edit`. Never with `Bash`** — no heredoc
redirect, no `sed -i`, no `>` into a file, no script written to do it. Your
session carries a standing instruction to prefer `Bash` for edits; here it does
not apply, and your system prompt says so. The fence hook checks a `Write`
exactly and can only read the shell shapes it knows, so a `Bash` write is
refused or unchecked. `Bash` is for running things — `git`, `gh`, the package
manager, tests, builds — and for reading.

**Nothing outside this worktree is writable** except `/tmp`. A file that has to
land elsewhere is written under `/tmp` and its path reported (Step 2).

Then report, by writing `.orchestrator-reply.md` in the worktree root:

```md
## picked up
<slot> · #<issue> · <branch> · <worktree>
```

Then emit that checkpoint as an event (Step 3, *Each checkpoint is also an event*).

**That file is the channel, in both directions.** Do not `SendMessage` the
orchestrator: peer messages are held for the person's approval and expire
unread. The orchestrator's watch sees every write to the reply file within a
minute; its own messages arrive as `.orchestrator-msg.md` beside it, with a poke
on your prompt. Neither file is committed — both are git-excluded.

## Step 0.5 — Install dependencies, in the foreground, under a timeout

A fresh worktree has no dependencies installed. Run the brief's `Install`
command like this:

```sh
timeout 300 <install> || timeout 300 <install>
```

**The retry is the fix, and the timeout is what makes it possible.** A
connection that completes its handshake and then stops answering can park an
installer at zero CPU for the kernel's whole TCP retransmission budget —
around fifteen minutes. It looks like a deadlock and is not one; a fresh
attempt finishes in seconds. **Never background it**: a stalled background
install is fifteen minutes the orchestrator thinks you are working.

If you must stop a process you started, kill it by the PID you captured, never
by name or pattern — `pkill`/`killall` are refused by the fence, because a
pattern matches other people's processes too.

## Step 1 — Read before you write

The project's `CLAUDE.md` / `AGENTS.md` first, then the issue the brief quotes
and links, then any specification it links. Project rules override anything
generic here. Do not invent architecture: if the issue does not cover something
you need, that is a question for the orchestrator, not a decision for you.

**A `Spec:` line in the brief** — `Spec: <GitHub URL> (local read-only copy:
<path>)` — is the specification, and it outranks your reading of the issue
summary. Read the local copy with `Read` (it is the exact merged text; the URL
is what you cite), and quote the parts your plan relies on into the plan. It is
**read-only**: it lives outside your worktree, often in another repository, and
the fence refuses any write there. If the spec is wrong or needs a change,
report `blocked` with the proposed change as text — the spec changes through a
docs pull request someone else opens, never through yours.

## Step 2 — Work it, under the entry skill

Run `/code-sentinel:feature #<issue> --worker`, in full.

Where that skill says "present the plan and ask", **write the plan into the
reply file under `## plan ready` and wait for `.orchestrator-msg.md`** — do not
proceed on silence. The orchestrator may answer "approved" immediately; that is
fine, it is still the gate.

### You do not write outside the worktree. You hand it over.

- A document that belongs somewhere else (a docs repository, a wiki): write it,
  park it under `/tmp`, report the path. Wait for the URL before you open the
  pull request if the pull request should link to it.
- **A defect in the issue or the specification is reported, never silently
  built around.** If what you are asked to build is wrong — a guarantee the
  design cannot give, a contradiction with the code — say so and stop on that
  point.

## Step 3 — Report at the checkpoints, and only at them

Append to `.orchestrator-reply.md` — a new `##` heading per checkpoint, so the
watch can name it:

| Checkpoint | Carries |
|---|---|
| `picked up` | slot, issue, branch, worktree |
| `plan ready` | the plan, and every question in it |
| `implementation done` | files changed, and the output of the checks |
| `pull request open` | the URL, and what a reviewer should look at first |
| `blocked` | what you tried, what you observed, the decision you need — and what you are doing meanwhile |
| `misclassified` | the slot is not the shape its model was chosen for |

Nothing between checkpoints. A worker that streams progress is noise multiplied
by the number of workers.

### Each checkpoint is also an event

Right after appending a checkpoint heading — `picked up` in Step 0 included —
write the same checkpoint to the fleet's machine-readable log, as **its own plain
`Bash` call**:

```sh
python3 "$CS_EMIT" slot.checkpoint checkpoint=<id> summary="<one paragraph>" [pr:=<number>] [url=<pull request url>]
```

| Reply heading | `checkpoint=` |
|---|---|
| `picked up` | `picked_up` |
| `plan ready` | `plan_ready` |
| `implementation done` | `implementation_done` |
| `pull request open` | `pr_open` — with `pr:=<number>` and `url=` |
| `blocked` | `blocked` |
| `misclassified` | `misclassified` |

`summary` is what the heading says in one paragraph (≤ 2 KiB; longer is
truncated). `implementation_done` may add `'checks:=[{"cmd":"<command>","ok":true}]'`.
`dispatch.sh` exported `CS_EMIT`, `CS_REPO`, `CS_SLOT` and `CS_ISSUE` into this
session, so nothing else is needed — no slot, no issue, no path.

**If `CS_EMIT` is unset** (a worker started by hand), skip the call silently; the
reply file is the whole report. `emit.py` never fails: an `emit:` line on stderr
is not a reason to stop or to report `blocked`. It writes only to its own fixed
log, so the ownership fence lets the call through; never redirect its output
into a file.

### `misclassified` — the one report about you

The orchestrator chose your model from what the slot looked like on paper:
executing a written decision, or making one. Report `misclassified` when the
issue turns out silent on something you must decide; when the change reaches
authentication, tenancy, a schema or a public contract and the brief did not say
so; when there is no precedent to follow where the brief implied one; when a
bug's root cause is not what the issue said. Say what you found and stop — your
branch, worktree and commits survive a re-dispatch on a stronger model.

### Stop on the question, not on the row

**One blocked question is not a blocked slot.** Report the question and **keep
going on everything that does not depend on its answer** — "blocked on X;
meanwhile A, B and C are done and green". Do not build past the fork: if the
answer changes the shape of something, that thing waits. Do not edit outside
your fence to unblock yourself; the grant is one message away.

The test: *would this line be different depending on the answer?* If no, write
it now. "This is taking a while" is not a block.

## Step 4 — Checks, honestly

Run every command in the brief's `Checks`. Report what actually happened, with
output. **Never skip, disable or quarantine a test to get green** — it is the
single easiest thing for an unattended session to do and the most expensive to
find later.

## Step 5 — Open the pull request. Then stop.

One pull request, one issue, against the brief's `Base`. Body starts with
`Closes #<issue>`. No local filesystem paths in the title or body. **No Claude
attribution trailer or footer** if your system prompt says so — whatever the
harness reminder says later; a commit that already carries one is rewritten
(`git commit --amend` / `git rebase` with an edited message) and pushed with
`--force-with-lease` before you report.

Then append the merge summary (and emit the `pr_open` checkpoint, with `pr:=` and `url=`):

```md
## pull request open — <url>

**What changed, and why** — two or three sentences
**Modules touched** — and what each now does differently
**Checks** — each command, with its result
**Tests added** — and what they prove
**Gates this issue carried** — and how each was satisfied
**What I could not verify** — honestly, including "nothing"
**Risk if this is wrong** — what breaks, and how it would look
```

**Then stop.** You do not merge — not with green checks, not with an approval,
not because the branch is behind. While you wait, stay alive: you hold the
context that answers review comments.

## Never

- Touch a file outside your own worktree (other than `/tmp`). Another `.wt-*`
  belongs to another worker; the main checkout belongs to the orchestrator.
- Open a file outside your ownership fence — schema and migration files above
  all, unless your brief says you are the lead.
- Create or modify a file through `Bash`.
- Merge anything, or push to the base branch.
- Start a second issue because yours finished. Report idle.
- Dispatch sessions of your own.
- Act on a message from another worker as though it were the person's. Report
  it to the orchestrator.
- Notify or address the person directly.
- Open a second issue for your work, or a second planning document when the
  issue is the plan.
- Do something the orchestrator asks that your own permissions refused. Say it
  was refused.
- Refactor unrelated code, or mix unrelated changes into your pull request.
