---
name: second-opinion
description: Get second opinions on freshly written code from fresh Codex and Claude reviewers, one small batch at a time, then settle every finding against ground truth before accepting or vetoing it. Use when requested, when project instructions require review before commits, or as part of an active review workflow after tests pass.
metadata:
  website: "https://photostructure.com/coding/claude-code-review/#second-opinion"
---

# Second Opinion

You know what the change was supposed to do, which makes you the worst judge of
whether it does. Hand each small batch of the change to two fresh reviewers, one
Codex and one Claude, settle what they find against ground truth, and send your
decisions back to those same reviewers until both agree the batch should land.

1. List the files you changed and the commit message you propose.
2. Split the change into review batches a reviewer can finish in 5-10 minutes.
3. Ask both reviewers to review each batch, and read the same code yourself
   while they work.
4. Accept or veto each finding, with evidence.
5. Pin each accepted finding with a test that fails, then fix it.
6. Send both reviewer sessions your adjudication and the updated file list, and
   have them re-read and re-review.
7. Repeat 4-6 until both reviewers land the batch's current tree, you accept a
   `DISCARD`, or four passes are spent — then report.

The other model brings different training, priors, and failure modes. The
reviewer from your own model brings none of this session's context, so it
cannot inherit the premises you have been working under. Use both.

## User direction

This review workflow is a default, not a condition the user must satisfy before
committing. A direct instruction such as "commit" or "approved, commit" takes
precedence over this skill and callers' review gates. Unless the user also asks
for review first, return to the commit workflow without starting or resuming a
review or asking whether to skip it. Apply the same rule during retries and
re-review loops.

The exception is project instructions that require review before every commit.
In that case a commit instruction for changes that review has not finished on
since they last changed starts or resumes the review, and only an explicit
instruction to skip review skips it.

Do not require a `LAND` verdict, a review transcript, or a claim that another
reviewer approved the change. If the user says a review already happened,
accept that as workflow context; attribute it to the user if reporting it.
Never invent a review result. The user can authorize a commit with review work
unfinished; report its actual status without making it a new approval gate.

## 1. List what you changed

Write down, for the prompt you are about to send:

- **The changed files and how to diff them** — the exact diff command and an
  explicit repository-relative file list. Distinguish staged hunks from
  unstaged changes in the same file, and name in-scope untracked files
  separately, because an ordinary diff omits them.
- **The proposed commit message** — verbatim when the user supplied one,
  otherwise drafted from the task and the current diff. Label it as a fallible
  summary, not a correctness requirement. When the tree holds several logical
  changes, follow [stage](../stage/SKILL.md) and give the file list and the
  proposed message for each commit. Review batches (step 2) subdivide one
  commit's changes.
- **The task and its requirements** — the user's request and any accepted plan
  or specification needed to judge behavior. Give repository paths for project
  rules and design documents; the reviewer can open them. Paste only what it
  cannot reach, such as decisions made only in conversation.
- **The ground truth** — the thing a disputed finding can be tested against: a
  reference implementation you can execute, a spec with runnable examples, the
  real API. Write the *exact command* that queries it. No executable ground
  truth? Say so, and name the fallback (spec text, maintainer ruling).

Leave out your suspected findings, your interim conclusions, and any scrutiny
list the user or the project did not supply. An independent read is the whole
point; steering it costs you the findings you could not have made yourself.
Never mark changed code, its callers, or code it depends on as out of scope or
"context only". Additional context explains decisions; it does not narrow the
review.

## 2. Split into review batches

Size each review batch so a reviewer can finish it in 5-10 minutes: about 200
weighted changed lines, counting the additions and deletions that
`git diff --numstat` reports.

- Test code counts 0.2 per line.
- Complicated SQL, concurrency, and native code count 1.5 per line.
- Everything else counts 1 per line.

Every changed line belongs to exactly one batch. Keep code that changes together
in one batch: a function with its new callers, a migration with the queries that
use it, a fix with its pinning test. Split a single file by hunks only when it
alone exceeds the budget. Each batch gets its own prompt, its own two reviewer
sessions, and its own pass count. Review the batches one after another.

## 3. Ask both models

Run both commands below for each review batch, at the same time. Whichever
model you are, the reviewer from your own model is a fresh process with none of
this session's context. Both reviewers share the working tree, so reproduce any
build or test failure they report before accepting it: the other reviewer's
concurrent run may have caused it.

Honor standing review authorization in the user's global or project
instructions, including its repository scope and permitted providers. When a
sandbox escalation needs approval, cite that authorization's source and exact
wording in the request, along with the review scope and destination. A saved
memory that has not been read is not evidence available to the approval
reviewer. Do not ask the user to repeat authorization that already covers the
action. This skill does not itself grant permission to disclose code, and
standing authorization does not override a host-policy denial.

Both commands run under a supervisor that kills the reviewer after 15 minutes of
silence and reaps its whole process group. The window is deliberately generous:
a working review goes quiet for a couple of minutes at a stretch, and a review
can run a slow build or test suite.

Write the complete reviewer prompt to a fresh UTF-8 temporary file with the
host's file-writing tool. Do not interpolate supplied text into a shell command:
commit messages and pasted context can contain quotes, dollar signs, backticks,
or command substitutions. The supervisor replaces the exact `{prompt}` argument
with the file's contents as one literal process argument. Delete the temporary
file after the reviewer exits.

**The Codex reviewer:**

```bash
python3 "<this-skill>/scripts/run_with_idle_timeout.py" \
  --prompt-file "<prompt-file>" -- \
  codex exec \
  -C "<target-repository>" \
  --sandbox workspace-write \
  -c 'model_reasoning_effort="xhigh"' \
  --json \
  --output-last-message "<review-file>" \
  "{prompt}" \
  > "<events-file>"
```

`workspace-write` lets the reviewer run the project's typecheck, build, and
tests to prove a finding. It can write inside the repository and the temporary
directory; every other path is read-only and the network is off. When the
project's tests write elsewhere or need the network, add
`-c 'sandbox_workspace_write.writable_roots=["<path>"]'` or
`-c 'sandbox_workspace_write.network_access=true'` to both Codex commands, as
the project's guidance directs.

Begin the prompt file with `$coding:review`, including for a staged diff.
Invoke plain `codex exec`, not the `review` subcommand: that substitutes
Codex's built-in review prompt and cannot load this marketplace's skill. Name
the diff range in the prompt itself — "the uncommitted changes", "the changes
since `<sha>`". Codex needs the coding plugin installed:

```bash
codex plugin marketplace add photostructure/coding-skills
codex plugin add coding@photostructure
```

Do not pass `--ephemeral`: the session must remain resumable for the re-review.
`--output-last-message` captures the clean review while the JSONL stream keeps
the supervisor fed. After a clean exit, record the session ID:

```bash
jq -sr '[.[] | select(.type=="thread.started") | .thread_id] | last // empty' "<events-file>"
```

**The Claude reviewer:**

Run the command with the target repository as its working directory. Resolve
`<coding-plugin-root>` to the plugin directory that contains this skill so the
spawned process does not depend on user- or repository-scoped plugin settings.

```bash
python3 "<this-skill>/scripts/run_with_idle_timeout.py" \
  --prompt-file "<prompt-file>" -- \
  claude -p "{prompt}" \
  --plugin-dir "<coding-plugin-root>" \
  --permission-mode auto \
  --disallowedTools Edit Write NotebookEdit \
  --model opus \
  --effort xhigh \
  --output-format stream-json --verbose \
  > "<events-file>"
```

`--permission-mode auto` lets the reviewer run the project's typecheck, build,
and tests, with Claude Code's classifier refusing risky commands.
`--disallowedTools` removes the file-editing tools. `--output-format
stream-json` is what keeps the supervisor fed — plain `-p` prints nothing at all
until it finishes. Both the reasoning and the tool calls stream, so watch the
file to see what the reviewer is chewing on. Extract the review after a clean
exit:

```bash
jq -r 'select(.type=="result").result' "<events-file>"
```

Claude persists print-mode sessions unless `--no-session-persistence` is set.
Do not set it. Record the session ID:

```bash
jq -sr '[.[] | select((.type=="system" and .subtype=="init") or .type=="result") | .session_id // empty] | last // empty' \
  "<events-file>"
```

Begin the prompt file with `/coding:review`, including for a staged diff. The
`-p` prompt must begin with the slash command so Claude invokes the skill
directly. An unavailable slash command is a plugin-loading failure even when
Claude exits 0.

Use xhigh effort for both reviewers. Small batches keep each review short.

Claude.ai OAuth may need to rewrite its credential store when refreshing an
expired token. On Codex hosts whose filesystem sandbox can read but not write
`~/.claude`, the command may return an expired-token 401 even though
`claude auth status` reports logged in or the same command works in the user's
terminal. In that specific case, retry the exact supervised command once with
the host's narrow filesystem-sandbox escalation (`sandbox_permissions:
require_escalated` where available) so Claude can refresh its existing
credential. Do not read, print, copy, or manually rewrite the credential. If
the escalated retry fails, use the unauthenticated fallback below.

These command shapes depend on Claude print-session persistence and `--resume`,
and on Codex JSON events, `--output-last-message`, and `exec resume`. Revalidate
them against a real diff when those CLI options change. Do not substitute a
similarly named built-in review mode without the same validation.

After the skill invocation, the prompt file carries the step 1 inputs:

```text
Review the batch below and return the full report to me, the calling agent. I
will accept or veto each finding and send you the results. Do not apply fixes,
and do not ask the user to adjudicate.

Diff command: <exact command, and any hunk limits>
Changed files:
<explicit list, marking in-scope untracked files>
This is review batch <n> of <m>. The other batches change: <files, or "none">.
Read them where they interact with this batch; they are reviewed separately.

Proposed commit message (fallible summary, not a requirement):
<complete message, or one per commit with its files>

Task and requirements: <text, or repository paths>
Additional context: <decisions made only in conversation, or "none">
Ground truth: <exact command, or the fallback>

Read the current diff and files from the repository. Review the full scope and
its interactions, and keep commit-message and grouping advice in Commit notes,
separate from the findings. You may run the project's typecheck, build, and
tests, or a reproducer in the temporary directory, to prove a finding. Do not
edit tracked files. Another reviewer is reviewing this checkout at the same
time and may build and test too: follow the project's shared-checkout rules,
do not clean or delete shared build outputs while another run may be using
them, and rerun any failure a concurrent run could explain before reporting it.
```

Name the review skill; never ask the reviewer to run `second-opinion`. If the
spawned CLI cannot load the coding plugin, rerun it with the full text of
[`../review/references/single-pass.md`](../review/references/single-pass.md)
pasted into the prompt instead of naming the skill.

Resolve `<this-skill>` to this skill's directory. Run both commands in the
background and poll each job until it exits:

- **0** — read the review and record the CLI, repository, batch, session ID,
  pass count, and finding IDs in your task notes. Keep that handle through fixes
  and handoffs; never select a reviewer with `--last` or `--continue`, which can
  attach to unrelated work. A missing session ID does not invalidate the pass,
  but it forces the fresh-session fallback in step 6.
- **124 with the supervisor's `idle timeout:` diagnostic** — the reviewer went
  silent for 15 minutes. Discard the partial review, say so, and finish your own
  pass.
- **124 without that diagnostic** — the reviewer CLI itself returned 124.
  Report its status and finish your own pass; do not call it an idle timeout.
- **a fast non-zero with a CLI usage or unknown-option diagnostic** — the
  invocation is stale. Report it as a bug in this skill; never let it pass as
  "no issues found".
- **127 or an authentication error** — for an expired Claude.ai OAuth error
  from Codex, use the one-time sandbox-escalation retry above. Otherwise, or if
  that retry fails, use the fallback below. These are environment failures, not
  bugs in this skill.
- **0 with an `Unknown command`, a missing-skill result, or a final review that
  does not begin with the required LAND, REVISE, or DISCARD verdict** — the CLI
  did not run the shared method. Treat it as a plugin-loading failure, not a
  clean review, and use the pasted-method fallback above. Allow ordinary
  Markdown decoration around the verdict text.
- **any other non-zero** — report the status and finish your own pass.

**Read the new code yourself while the reviewers run** — you are the third
reviewer, and the only one who knows the full context of what the change was
supposed to do. Hold your edits until both reports arrive. The reviewers read
the repository live, so a file that changes mid-pass gives them a tree that
never existed. Write down what you find and adjudicate it in step 4.

If either CLI is not installed or not authenticated, say so plainly and run
that reviewer as a task-local subagent of a model you can reach, given the same
prompt and the full text of
[`../review/references/single-pass.md`](../review/references/single-pass.md).
Save its handle and send the follow-up prompts to that same subagent. Its
findings count, but its verdict is not that model's verdict: the step 7 report
marks that model's slot as missing.

## 4. Adjudicate every finding

First set aside every concern that is only about the commit message, or about
grouping, splitting, or ordering otherwise-valid content. Those are commit
notes, not findings: no severity, no accept, no veto, no pinning test. If they
are all that any review raised, the verdict is `LAND`.

The verdict does not decide what you adjudicate. A `LAND` carrying findings
still carries findings: settle every one. An empty findings list ends the work,
not the word `LAND`.

Then settle each remaining finding — both reviewers' and your own. An
Unexplained finding follows its own rule below. For every other finding:

1. Build the empirical test: run ground truth and the new code on the same
   input, and compare. A finding you cannot test this way becomes an open
   question, not a silent acceptance.
2. **Accept** only when ground truth confirms the bug.
3. **Veto** only when ground truth confirms the code is right, or the finding
   demands fidelity nothing requires — mirroring a reference implementation's
   internals on a path no contract pins, for instance.
4. When the diagnosis is right but the proposed fix is mediocre, take the better
   fix. Reviewers identify problems; you own the remedy.

An Unexplained finding means the reviewer could not say why an added or
modified function or branch exists from the code, tests, documentation, and
commit message. No
ground truth settles it. Answer the reviewer's question instead:

- **Veto** when the answer is already in the code, tests, documentation, or
  commit message. Cite where.
- **Accept** when it is not, and put the answer there: a clearer name, a test,
  a comment, or the commit message. Simplifying the code until no answer is
  needed also settles it.
- If you cannot answer the question either, trace what the code does until you
  can, then accept or veto as above. A defect found this way is settled like
  any other finding.

Reviewer confidence, eloquence, and *agreement between reviewers* are not
evidence. Two models converging on the same wrong finding is common; one command
against ground truth beats both.

**When two or more fixes are defensible and nothing chooses between them, ask
the user.** Give the finding, each alternative with its tradeoff, and your
recommendation if you have one, then wait for direction. Ground truth settles
whether the code is wrong; it usually does not settle which correct design to
adopt, and that choice is the user's.

Your own context of settled decisions and corrected premises catches
plausible-but-wrong findings a fresh reader cannot — that is why you adjudicate.
It can also *contain* the defect: a wrong premise this session has carried since
birth, which is exactly what the independent pass is for. So a veto of yours
carries no special weight. It needs the same recorded evidence as anyone's.

## 5. Pin, then fix

**Every accepted finding gets a pinning test** whose expected values come from
ground truth; paste the command that produced them into the test's comment. Run
it against the unfixed code and confirm it fails, then apply the fix. An
accepted Unexplained finding whose fix changed no behavior — a rename, a
comment, or a commit-message change — needs no pinning test. Every test the
fixes could affect must pass again, not just the new pinning tests.

## 6. Re-review in the same sessions

Continue this loop only while review remains in scope under **User direction**.

Send your adjudication to both of the batch's reviewers, even when you vetoed
everything and changed no code. If you applied fixes, wait until every test
they could affect passes. Re-read the complete current scope yourself, and ask
each reviewer to do the same:

```text
Re-read and re-review the complete current scope from the repository, then
return the normal verdict and findings. Do not rely on what you read last pass,
and do not limit the review to the fixes.

Author notes:
Accepted <ID>: <diagnosis, the fix and its location, how it was validated>
Vetoed <ID>: <the concrete evidence that the code is right>
Open <ID>: <what is still unsettled, and what would settle it>

Files now in play: <updated file list, including files the fixes touched>
Proposed commit message: <current complete message>
Changed requirements or ground truth: <updates only, or "unchanged">

Keep existing finding IDs and give new issues new IDs. Report each prior
finding as resolved, still present, or disputed. If you think a veto is wrong,
say what evidence would settle it. Do not apply fixes, and do not ask the user
to adjudicate.
```

Use `none` for an empty list. Do not repaste requirements the session already
has. Include findings from your own read when they explain a fix.

Resume the recorded session in the same repository, through the same supervisor,
with its exact session ID. Do not fork it or start a new session for an ordinary
follow-up. For a Claude reviewer:

```bash
python3 "<this-skill>/scripts/run_with_idle_timeout.py" \
  --prompt-file "<follow-up-prompt-file>" -- \
  claude -p "{prompt}" \
  --resume "<session-id>" \
  --plugin-dir "<coding-plugin-root>" \
  --permission-mode auto \
  --disallowedTools Edit Write NotebookEdit \
  --model opus \
  --effort xhigh \
  --output-format stream-json --verbose \
  > "<next-events-file>"
```

For a Codex reviewer:

```bash
python3 "<this-skill>/scripts/run_with_idle_timeout.py" \
  --prompt-file "<follow-up-prompt-file>" -- \
  codex exec \
  -C "<target-repository>" \
  --sandbox workspace-write \
  resume \
  -c 'model_reasoning_effort="xhigh"' \
  --json \
  --output-last-message "<next-review-file>" \
  "<session-id>" \
  "{prompt}" \
  > "<next-events-file>"
```

Apply the same exit-status and output-validity checks as the first pass. If the
CLI cannot resume the recorded session, launch a fresh one with the original
prompt updated for the current scope, plus the prior report, its finding IDs,
and every accept and veto with its evidence. Record the replacement handle and
disclose that continuity was unavailable. A resume failure does not justify
skipping the re-review.

Then return to step 4 for the new reports. **Stop when** both reviewers return
`LAND` on the batch as it now stands and every finding from all three reads is
either accepted and fixed or vetoed with evidence. A `LAND` does not cover code
you changed after that reviewer's last read: if adjudication changed the tree,
run one more pass, subject to the cap. **Stop earlier** when you
adjudicate a `DISCARD` as correct — the change should not land at all. Preserve
that verdict and report it; do not re-review a settled decision.

Stop at four review passes per batch either way. If the fourth leaves accepted
fixes or disputed findings, finish the authorized fixes and tests, then report
the cap and what is still unsettled; do not describe unreviewed fixes as a clean
pass.
Skip the loop entirely when the first pass raised nothing substantive and no
code changed.

## 7. Report the verdicts

Summarize for the user (and for whatever plan or PR document tracks this work):
every substantive finding, accepted **and** vetoed, with one-line evidence for
each verdict, and which model raised it. Record vetoes especially — the next
session will rediscover the same "bug" and must not re-litigate it.

Begin with one top-level `Verdict: LAND | REVISE | DISCARD` line, then one line
per review batch with its files, its pass count, and each model's final verdict:
`Batch 2 (src/a.ts, src/a.spec.ts): 2 passes; Codex LAND, Claude LAND`. Only a
reviewer launched through that model's CLI fills its slot. Otherwise write why
the slot is empty, for example `Codex missing (CLI not installed; Claude
subagent LAND)` or `Claude missing (idle timeout)`. Project policy may act on
these lines. If no review raised a substantive finding, use `LAND`, follow it
with `No issues found.`, and do not invent ledger rows. Otherwise list the
accepted and vetoed
findings under their original IDs, even when the final verdict is `LAND`, and
state any unresolved questions or unreviewed fixes separately.

The ledger repeats the final verdict in each row so a copied or aggregated row
still reads correctly:

| ID | Scope | Model | Finding | Severity | Accept/Veto | Evidence (one line) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |

After the ledger — or after `No issues found.` when there are no rows — add a
brief `Commit notes` section when either model proposed a warranted message or
grouping improvement. Name the model, state the specific reason, and give the
complete improved message. For a split, identify every independently committable
group and give each group's complete message. These notes have no severity and
cannot change the verdict.

## Scratch files

Any copy this workflow makes — of the repo, of a build-output directory, of a
file you replay edits onto — belongs in the operating system's temporary
directory, in a fresh directory named for the project and the purpose. Never
inside the checkout, and never under a home directory.

Delete it before you finish. A repo or build-output copy runs to gigabytes,
nothing reaps a home directory, and the out-of-disk failure that eventually
follows surfaces somewhere unrelated — a test suite that hangs, a build that
dies mid-link — costing far more to diagnose than the copy ever saved.

## Adapting for your project

- **Name the ground truth explicitly** — e.g. "the vendored reference
  implementation via `./third-party/tool/run`", "CPython 3.12 via
  `uv run python -c ...`", "the RFC's test vectors". Step 4 is only as strong as
  this.
- **Say how to name the diff range** the way your project talks about it — "the
  changes on this branch vs `develop`", "everything since the last tag".
- **Optional review focus** belongs in project guidance. Keep it a starting
  point; the reviewers still examine the full scope independently.
- **Name sandbox needs**: paths outside the repository that the project's tests
  write, and whether they need the network, so callers add them to the Codex
  commands.
- **Callers welcome**: other skills (`gitplan`, `tpp-orchestrate`) reference this
  file as their review gate. Keep the gate generic here; put workflow-specific
  bookkeeping (where verdicts get recorded, commit conventions) in the calling
  skill.
