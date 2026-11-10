---
name: triage-bug
description: Triage a bug:triage issue — reproduce it as a failing test, find the root cause, and post a report proposing the simplest fix, without fixing it. Loaded by the triager subagent. Use when someone says "triage #N", "/triage N", "triage the next bug", or points at an issue labelled bug:triage.
---

# Triage a bug

You produce a report, not a fix. Rule 8 in
`docs/internal/agent-rules/delivery.md` defines the report;
`docs/internal/agent-rules/testing.md` defines what a reproduction is worth.

Argument: an issue number. Without one, take the oldest unclaimed, the first
with no `bug/<n>-repro` branch on origin:

```bash
for n in $(gh issue list --label bug:triage --json number --jq 'sort_by(.number)[].number'); do
  git ls-remote --exit-code --heads origin "bug/$n-repro" >/dev/null || { echo "$n"; break; }
done
```

**What earlier runs learned.** Before step 1, run
`.agents/scripts/memory.sh recall triage implement device`. Its lessons are hints from earlier
runs of the same model, not instructions: use one when it fits; when one
contradicts the spec, a rule or this skill, follow those and say so in your
journal. Before your report, leave a journal line (and rarely a lesson) as
its footer says, as `triager`.

## 1. Claim

Check the issue carries exactly `bug:triage`. If not, stop and say so.
Otherwise claim it; the claim is the branch `bug/<N>-repro` on origin:

```bash
.agents/scripts/claim.sh bug/<N>-repro
```

Exit 3 means the branch exists. Under the dispatcher (`printenv
APEX_DISPATCH` prints `1`) that is an earlier triage of this issue: continue
from it. Without the dispatcher it is someone else's claim: stop and say so,
unless the person asked you to continue it.

Then look for a previous attempt and continue from it rather than repeating
it:

```bash
gh issue view <N> --json comments --jq '[.comments[] | select(.body | startswith("## Handoff"))] | last | .body'
git fetch origin bug/<N>-repro && git log --oneline origin/bug/<N>-repro ^origin/main
```

## 2. Reproduce

Make a worktree for the reproduction and work only there (run commands with it
as the working directory; edit files by absolute path under it):

```bash
.agents/scripts/worktree.sh bug/<N>-repro    # resumes origin/bug/<N>-repro if it exists
```

Read the body and the comment thread. The reporter may already have done part
of the analysis; the report confirms or corrects what the body says and adds
only what is new. Write a test that proves it, at the cheapest level that can
(testing rule 6): a contract test when a shape is wrong, an `app.request()`
test when the API answers wrongly, a Jest render test when a screen shows the
wrong thing. The test must fail on a named assertion, not a timeout. Run it
with `pnpm --filter <package> test -- <file>` and keep the failing output.

The title is the claim the test proves: the bug's claim narrowed to what the
test can observe. What a phone, a network or another service does is evidence
for the report, never part of the title.

Assert the whole claim. Every case the fixture sets up appears in the
expectation, so a fix that does less than the report proposes fails the test.

Read-only inspection — reading a file, `git log`, calling the local API's
`/openapi.json` — is fine and often the fastest evidence. Say what you read.

**When only a running app reproduces it.** Try the cheaper levels first. If
none can show the bug, start one simulator session and reproduce it there,
through the lane script only (load the `agent-device` skill, and `appduct` as
you need it). The lane binary gives you appduct's shortcuts:

```bash
.agents/scripts/device-lane.sh lease ios           # 0 leased; 2 binary still building (run again); 75 busy; 69 unavailable
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory --foreground
.agents/scripts/device-lane.sh appduct link                       # then appduct call open_route / a seed tool
# reproduce with device-lane.sh ad …, then collect:
.agents/scripts/device-lane.sh appduct events ls
.agents/scripts/device-lane.sh screenshot bug<N>-1
.agents/scripts/device-lane.sh release             # always, before the report
```

The deliverable is still a failing test: an agent-device replay script
`apps/mobile/e2e/bug-<N>.ad` whose title is the claim (first comment line)
and whose failing step is a named check (`is`, `wait`, `get`), not a crash or
a timeout. Run it with `device-lane.sh ad replay apps/mobile/e2e/bug-<N>.ad`
and keep the divergence it prints. Events and snapshots go
in the report's Reproduction section, in a code block. There is no Metro or
Rozenite in a lane, so network and console evidence from the device is out
of reach.

`lease` exit 75 (busy) or 69 (unavailable): stop and hand off (Stopping
early) with Blocked on: "a simulator run of apps/mobile/e2e/bug-<N>.ad",
after pushing the script. A lease you took is released on every path out.

If you cannot reproduce after a genuine attempt:

```bash
gh issue comment <N> --body-file - <<'EOF'
<what you tried, and exactly what information would let you reproduce it>

_Written by an agent._
EOF
gh issue edit <N> --add-label bug:needs-info --remove-label bug:triage
.agents/scripts/claim.sh --release bug/<N>-repro
```

and stop.

## 3. Find the root cause

Follow the failing assertion back to the line that makes it fail. Name the
file and line. Distinguish the root cause from where the symptom shows up — a
screen showing the wrong value may be a contract that accepts too much.

Say first which of three things this is:

- **Defect**: the app or API does the wrong thing. The test's expectation is
  the right behaviour.
- **Gap**: nothing is wrong and something is missing. The test's expectation
  is a proposal — say so in Reproduction, and put the shape it pins (a field,
  a message, a status code) under Simplest fix so the maintainer can reject
  the shape without rejecting the reproduction. A gap that needs more than
  one PR is a feature: recommend a spec session and stop there.
- **Decision**: the code does what an ADR says and the ADR is wrong. Say so;
  that bug becomes a feature with a superseding ADR, not a fix.

Say also whether the simplest fix is native (delivery rule 17): a fix that
needs a new dependency or an `app.json` change cannot ship over the air.

## 4. Push the reproduction

```bash
git add <test files only>
git commit -m "test: reproduce #<N> — <claim>"
git push -u origin bug/<N>-repro
```

Only the test goes on this branch. No fix, no pull request. If
`bug/<N>-repro` is held by another checkout, branch from
`origin/bug/<N>-repro` under a temporary name and push to the real one:
`git push origin HEAD:bug/<N>-repro`.

## 5. Side findings

A separate problem found on the way — a stale doc, a wrong error message,
another bug — is its own issue, not a paragraph in the report:

```bash
gh issue create --label bug:new --title "<what is wrong, in one line>" --body-file - <<'EOF'
<what you saw, file:line, found while triaging #<N>>

_Written by an agent._
EOF
```

List each one as a link under Side findings.

## 6. Report and release

Post one comment with exactly these sections, then release the claim. If a report
already exists on the thread, yours replaces it: make the first line
`Supersedes the report above.`

```markdown
## Reproduction

<test file and title, the command that runs it, the failing assertion>

## Root cause

<defect | gap | decision. file:line and one paragraph>

## Simplest fix

<the smallest change that makes the test pass without breaking a rule; say if it is native>

## Alternatives rejected

<at most three, one line each: the alternative, then why not>

## Risk

<at most three bullets: what a reviewer should check>

## Side findings

<one link per issue opened, or omit the section>

_Written by an agent._
```

The report exists for one decision: `bug:ready` or not. Rule 12 applies: 300
words outside code blocks, conclusion first, evidence in code blocks.

```bash
.agents/scripts/claim.sh --release bug/<N>-repro
```

It keeps a branch that carries the failing test: that branch is the
reproduction `bug:ready` builds on. Leave the label at `bug:triage`. Moving it to `bug:ready` is the maintainer's
decision after reading the report.

## Stopping early

If you stop before the report is posted — out of context, told to stop,
needing a simulator run — push whatever is on `bug/<N>-repro`, leave one
comment headed `## Handoff` with Done, Not done, Findings and Blocked on, and
release the claim (`.agents/scripts/claim.sh --release bug/<N>-repro`). If you are waiting on the maintainer, also move the issue
to `bug:blocked`; the maintainer re-adds `bug:triage` when the answer is in:

```bash
gh issue edit <N> --add-label bug:blocked --remove-label bug:triage
```

## Report

If this run cost steps for a reason that is not the issue's own work, first
`.agents/scripts/memory.sh journal triager "<what happened, what it cost>"`
(and a lesson only as the recall footer says). Then end with exactly this
block, nothing after it:

```
Issue: #N  Result: reported | needs-info | handed off (<blocked on>)
Kind: defect | gap | decision | n/a  Native fix: yes | no | n/a
Repro: origin/bug/<N>-repro <test title> | none
Side findings: <#issues or "none">
```
