---
name: auto
description: "Away mode: carry the run in progress, or a new request, to completion unattended, ending at one verification gate. Use when the user runs /ac/auto or says in any language they are leaving and the work should go on until done, even while another flow is active; not for open-ended audits. Request text: [request, and any outward action allowed while away: push, merge, pr, release, deploy]."
---
<!-- ported-from: plugins/ac/skills/auto/SKILL.md sha256:9beb3203555f64bb3d85f9ecbcfca639c5d3f712def2a377797f2adfb670e529 -->

# /ac/auto

Away mode. It carries the run already going in this session to its end while the user is gone, takes the
recommended option wherever that run would ask, performs only the outward actions the user named, and ends at one
verdict written by a gate that did none of the work. With nothing running it starts a new run from the request.

Request: the text of the user's request. When the run starts from the `/ac/auto` command, that is the command's
argument text; this skill takes no arguments of its own, so the request and the outward actions it names are read
out of that text.

## Standing rules

These hold for the whole run, including after a compaction; the procedure follows them.

**Carry, never decline.** Pick the source at 0b and continue it where it is. Another flow being active is the
normal case, not a conflict: never refuse because of it, and for sources (a) to (d) never open a second run, a
second marker or a new branch. Only a marker owned by another session refuses (0a).

**No questions while away.** Do not call the `question` tool, and do not let a flow you carry call it either: the
user is gone. The ac plugin denies the call while the marker lives. Where a flow would ask, take the option it marks Recommended (a flow gate's default),
apply it, and add one line under `## Decisions` in the decisions file:
`time | source | question | chosen option | why | not user-approved`. A plan skill interview still open locks its
remaining nodes with their Recommended options, which the away marker triggers (1c).

**True blockers stop only their part.** A destructive or irreversible action, an outward action the user did not
name, a finding that the plan or roadmap is wrong, and a missing secret or credential are not decided for the user.
Add one line under `## Blocked` in the decisions file (`time | source | what | why blocked`), take the option
that stops only that part (leave the step unchecked and skip its dependents, keep a lane's bundle in its queue),
and continue every independent part. When nothing independent remains, the source has reached its end.

**Outward actions only when named.** The marker's `allowed_outward` (1c) lists what the user's words allowed, out
of `push`, `merge`, `pr`, `release` and `deploy`. Perform an outward action only when its value is listed, and only
after the gate: at Phase 4, or under a coordinator source at its Phase 8, which publishes in place of `Push?`. No
other flow publishes while away: the `commit` skill skips its push under this marker. The ac plugin's shell guard
enforces the git and gh verbs and always denies force pushes and remote deletes, `git reset --hard`, `git clean`
outside a dry run, whole-tree checkouts and restores, `rm -rf`, `sed -i` and `perl -i`; a deploy command is
project-specific, so only this rule gates it. A denied command is recorded under
`## Blocked` as deferred, never worked around.

**Turn termination.** A turn ends on exactly one of: the Phase 4 closing report; a terminal branch that deleted
the marker first; or a one-line wait status while subagents or background shells you started still run (each
completion or exit notification starts the next turn; never wait with `sleep` or a polling loop). While the marker
exists and the verdict does not, the ac plugin hands a turn that ended any other way back with what the run owes,
3 times per phase; over a coordinator run that run's own guard owns the stop until its marker is gone. Never end
a turn by describing what you would do next, and never hand the rest to a fresh session.

**Budgets are the user's.** A criteria file this skill writes carries `turn_budget` (default 40) and
`failure_budget` (default 0.2, a fraction of plan steps), or the numbers the user stated; never invent another.
Increment the marker's `turns_used` at each control point you regain. Reaching the turn budget, or failed steps
exceeding the failure budget, stops new work: record it under `## Blocked` and go to the gate. A coordinator
source carries no budgets of its own; its slot and attempt bounds are the bounds.

**A stop needs a name.** A part that cannot proceed names its class: a fact you cannot obtain, a decision only the
user can make, or a gate you cannot pass. Context pressure is none of them: compaction summarises and the run goes
on. When this procedure has been truncated away, load the `auto` skill again with the `skill` tool; 0a resumes from
the marker.

**A failed subagent moves down its model chain; it is not a question.** A subagent call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Recover by continuing the same child, not by a fresh spawn: call the `subagent` tool again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read and wrote (a fresh spawn repeats all of it). When it answered nothing or broke off mid-stream (`provider.invalid-output`, an empty report), continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config), since that is often a one-off; a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well (the child switches to it and keeps its context), and give that model the same number of attempts. A rate limit was retried 10 times inside the call, and the plugin gives one model 30 across continuations: `wait:<seconds>` means that model has retries left, so wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. The tool bounds those waits itself. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to record under `## Blocked`; the user is away, so it is never a question. It covers `ac/auto-verifier`.

**The user outranks everything.** A user asking to stop, pause or take back control: delete
`.ac/state/active-auto.json` and stop. A user saying they are leaving is the opposite request, and starts here.

**Files.** Mutate files with `write` or `edit`, never through `shell` (`python3 -c`, a `cat >` heredoc, `sed -i`);
the one exception is removing a file with `shell`: `rm -f <path>`. Per-turn prose is at most 3 lines plus the
closing report.

<scope>
You write the marker `.ac/state/active-auto.json`, the decisions file `.ac/away/<slug>/decisions.md`, and for every
source but (a) the run directory `.ac/auto/<slug>/` with `criteria.md` and `verdict.md`; the shapes are in
`references/criteria-schema.md` (relative to this skill's base directory), which you read first. A coordinator run
keeps its own directory, criteria and verdict under `.ac/coord/<slug>/`. Everything else belongs to the flow you
carry: plans to the `plan` skill, `active-execution.json` and source code to the `execute` skill and its workers,
`.ac/coord/` to the `coordinate` skill. Under (d) the work in the conversation is yours to finish, as it was before
the user left.
</scope>

## Phase 0: Re-entry and source

### 0a. Re-entry

Call the `ac_session` tool first; it returns `session_id` and `root_session_id` as JSON. The root id is this
session's identity for everything below. Then read `.ac/state/active-auto.json` if it exists:

- **Owned by this session** (`harness` is `"opencode"` and `session_id` equals the `root_session_id` from
  `ac_session`): a re-entry, from a compaction, the plugin's stop note or a second `/ac/auto` (whose new request
  only adds to `allowed_outward`). Skip to the marker's `phase`, reading its `note`. `executing` loads nothing
  while the source still runs in context (its own marker exists, or under (d) the work is unfinished); once it has
  ended, refresh the marker to `gating` and go to Phase 3.
- **Owned by another session** (another `session_id`, or a marker without `harness`, which Claude Code wrote): when
  its `started_at` is past the plugin's age bound (24 hours, 72 with `source: coordinate`), every guard already
  treats it as dead: overwrite it at 1c and log one `## Decisions` line naming the stale slug, because refusing
  would strand a user who has already left. Otherwise refuse in one line naming its slug: a live run in another
  window and an abandoned one look the same, so do not delete it.
- **Absent**: continue.

### 0b. Pick the source

Take the first match, in this order, so the most specific running flow wins:

| Source | Evidence | Criteria | Continue with | Branch |
|---|---|---|---|---|
| (a) coordinate | `.ac/state/active-coordinate.json` owned by this session (its `session_id` is your `root_session_id`) | its `.ac/coord/<slug>/criteria.md`, frozen at its `Roadmap?` lock | the coordinator run, from its `state.json` | current |
| (b) execute | `.ac/state/active-execution.json` owned by this session (its `root_session_id` is yours) | the plan, 1b | the run in context; load nothing | current |
| (c) plan | a plan skill run in this conversation: a checkpoint, a review in flight, or a written plan with an unchecked step and no `report.md` | the plan, 1b | Phase 2 | current |
| (d) ad-hoc | unfinished work in the conversation, none of the above | the conversation goal, 1b | the work, in context | current |
| (e) new | nothing above unfinished; the request names a task | the request, through admission (1a) | the `plan` skill with `--auto` | `auto/<slug>` |

A marker of either kind owned by another session is that session's run: it is not a source, and (a) or (b) does
not match on it. When the conversation's work is already complete and the request names no new task, there is
nothing to carry: end on a closing report of what is done, with no marker and no run directory.

## Phase 1: Freeze

### 1a. Slug, allowed outward, admission

- **Slug**: the coordinator slug under (a), the plan slug under (b) and (c), otherwise kebab-case from the goal or
  request, at most 6 words. Outside (a), when `.ac/auto/<slug>/` exists append `-2`, then `-3`.
- **`allowed_outward`**: the values the user's words name, read from the `/ac/auto` request and from the source
  run's own request (the coordinator's request, the plan's request, the conversation's ask), in any language:
  "push" allows `push`; "PR" or "pull request" allows `pr` and `push`; a release or tag allows `release`; "merge
  edip deploy et" allows `merge` and `deploy`. Then add what a named action needs to land: `merge` adds `push`, and
  `pr` too when the repository merges through pull requests (otherwise the merge is a local `git merge` into the
  base branch followed by a push of it); `deploy` adds `push` when the deploy is push-triggered (a workflow that
  runs on a push to the base branch). A negated or deferred mention ("don't push yet", "push etme") grants
  nothing, and nothing named means an empty list; never infer a value from what would be convenient.
- **Admission, source (e) only.** Draft the `must_haves` and `criteria` blocks in full first. A request whose done
  cannot be stated before the work exists ("clean up the codebase", "make it faster" with no number) is refused in
  at most 5 lines naming the criteria that could not be enumerated and the alternative (an audit run that produces
  criteria, then a run against them). Nothing is written before this test passes.

### 1b. Run directory, criteria and digest

Under (a) skip this step: the coordinator froze its criteria at its lock with this same digest. Otherwise create
`.ac/auto/<slug>/` first, because the plugin's stop guard treats a marker without its directory as malformed and
goes inert. Then `write` `criteria.md` in the schema's exact shape with `criteria_sha256: "pending"`, from the
source:

- **(b) and (c), a plan file**: copy every `### Definition of Done` item and every step's `Done when` command
  verbatim, one criterion each, with `anchor: "<plan path>:<line>"` and `adopted_from: execute` or `plan`. A shell
  command becomes `verification: command` with the exit code its wording states (a "prints nothing" `rg` passes on
  exit 1); prose becomes `judgment`. Do not merge, reword, narrow or drop one: copied text with its anchor is what
  shows a criterion predates the work. When (c) is still an interview, write the directory and the marker now and
  `criteria.md` as soon as the plan file exists, before its first wave runs.
- **(d)**: the conversation's goal written as the request, `adopted_from: adhoc`; the gate caps it at
  `human_needed`, because the session that did part of the work also wrote what done means.
- **(e)**: the admission draft from 1a.

Budgets per the Standing rule. Then compute the digest over the frontmatter minus its own line with `shell` and
patch that one line with `edit`. Use this recipe as written (`ac/auto-verifier` and the `coordinate` skill recompute
with the identical bytes; implementations disagree on a trailing newline):

```bash
python3 - .ac/auto/<slug>/criteria.md <<'PY'
import hashlib, sys
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
start = lines.index('---')
end = lines.index('---', start + 1)
covered = [l for l in lines[start + 1:end] if not l.startswith('criteria_sha256:')]
print(hashlib.sha256('\n'.join(covered).encode('utf-8')).hexdigest())
PY
```

No `python3` is a gate you cannot pass: delete what you wrote and stop; never improvise a digest. From here the frontmatter is the contract and is never edited; prose below the delimiter is free.

### 1c. Marker and decisions file

`write` `.ac/state/active-auto.json` with the schema's fields: `slug`, `session_id` (exactly the
`root_session_id` the `ac_session` tool returned, never derived or recalled; the root id scopes every guard to this
session and its workers), `harness` (exactly `"opencode"`; without it the plugin reads the marker as Claude Code's
and ignores it), `started_at` (`date -u +%Y-%m-%dT%H:%M:%SZ` through `shell`, never refreshed), `turns_used: 0`,
`phase` (`planning` for (c) and (e) before a plan exists, otherwise `executing`), `source` (`coordinate`,
`execute`, `plan`, `adhoc` or `new`), `source_ref` (the coordinator or plan slug, omitted for (d) and (e)),
`allowed_outward`, `decisions: ".ac/away/<slug>/decisions.md"`, and a `note` that starts
`away: no questions; plan questions lock with their Recommended options.` so the `plan` skill asks nothing.

Then `write` the decisions file:

```markdown
# Away run <slug>

Source: <source> <source_ref>. Allowed outward: <values, or none>.

## Decisions

## Blocked
```

Add each line at the end of its section with `edit`. Refresh `turns_used`, `phase` and `note` at every control point.

### 1d. Branch, source (e) only

`shell`: `git switch -c auto/<slug>` (append `-2` when taken). Uncommitted changes follow the switch; do not stash
or commit them. A failed switch is a terminal branch. Every other source stays on the branch it is on: a switch
mid-run would split one run's history across two branches.

One heartbeat line: the source, the slug, the budgets, `allowed_outward`.

## Phase 2: Carry the source

The flow you carry keeps its own procedure; these rules ride on top of it.

- **(a) coordinate.** Continue from `state.json` at the marker's phase; when its body is no longer in context,
  load the `coordinate` skill again, whose Phase 0 resumes an owned run. A `Roadmap?`, `TDD?` or bundle decision
  takes its Recommended option. `Lane block?`, `Conflict?`, `Relock?` and `Add bundle?` are true blockers: record
  them, keep the bundle in `owner_queue`, and keep dispatching and integrating the rest. Its Phase 7 is this run's
  gate, and its `Push?` is not asked: unless its verdict is `gaps_found`, apply `Push + PR` when `allowed_outward`
  holds `pr` or `merge`, `Push` when it holds only `push`; otherwise `Keep local`, the push recorded as deferred.
  Its Phase 8 close follows, then Phase 4 here for whatever remains (a merge, a deploy).
- **(b) execute.** Never load the `execute` skill: a second load restarts its wave loop and loses the failure
  history that lives in context. It keeps `AUTO_MODE` once your
  marker appears, and its final commit goes `--no-push` because the marker exists.
- **(c) plan.** A checkpoint: write `Request: --auto <checkpoint slug>` as one line, then load the `plan` skill with
  the `skill` tool; the slug goes in verbatim and never the topic (the plan skill re-derives the slug from
  its request). A plan whose reviewer is still running: wait for it and continue
  the plan's own flow; never adopt a plan before its review lands. A written plan nobody executed: write
  `Request: <slug> --auto` as one line, then load the `execute` skill, the one load of execute this skill makes,
  because no plan run exists to chain it.
- **(d) ad-hoc.** Finish the work in context under the project's working rules, against the frozen criteria.
- **(e) new.** Write `Request: --auto <request>` as one line, then load the `plan` skill; its Stage 6a chains the
  `execute` skill, so never load execute yourself.

When the source reaches its terminal state (its report or verdict written, its marker gone, or no independent part
left), refresh the marker to `phase: "gating"`.

## Phase 3: Gate

Under (a) the coordinator's Phase 7 already ran the gate; go to Phase 4. Otherwise recompute the digest with the
1b recipe and compare it to `criteria_sha256`. A mismatch means the contract changed after it was fixed: delete
the marker, name the mismatch and stop rather than gate against a file of unknown provenance. A decision taken
while away that diverges from a criterion is one line of prose below the delimiter, never a frontmatter edit.

```
subagent({
  agent: "ac/auto-verifier",
  description: "Away-run verdict",
  prompt: "Criteria: <absolute path>/.ac/auto/<slug>/criteria.md
Schema: <absolute path of references/criteria-schema.md under this skill's base directory>"
})
```

Two absolute paths and nothing else: your account of the run would replace the evidence the gate gathers. Resolve
the schema path from the base directory the `skill` tool reported when it loaded this skill. `write` the returned
body verbatim to `.ac/auto/<slug>/verdict.md`; that write releases the plugin's stop guard whatever the verdict
says. An unusable body gets one re-spawn; a second one is written as `status: human_needed` with one line naming
what the gate did, never `passed`. A verdict reporting gaps is a complete ending: never go back to make it pass.

## Phase 4: Outward actions and close

1. **Outward actions.** Each value in `allowed_outward` the run has not already performed: `push` pushes the
   current branch (`git push -u origin <branch>`), `pr` opens one (`gh pr create`, a body free of em and en
   dashes), `merge` merges that PR (`gh pr merge`), or in a repository without pull requests merges locally into the base
   branch and pushes it, `release` cuts the release the request named, `deploy` runs the
   deploy the request or the project's docs name (none found is a missing fact, recorded under `## Blocked`). On a
   `gaps_found` verdict none runs: each is recorded as deferred. Report each command's result.
2. **Close.** Delete `.ac/state/active-auto.json`. The plugin keeps its stop-guard count in memory, keyed on the
   marker's `started_at`, so the next run starts with a fresh budget and there is no counter file to remove.
3. **Report.** What finished (steps or bundles, the branch and its head); the verdict's `status`, criteria met
   against total, each gap in one line and the verdict path; every line under `## Decisions`, one each; every line
   under `## Blocked`, deferred outward actions included; what was pushed, merged or deployed. A
   `proposed_overrides` entry stays a suggestion until the user answers it; only their answer fills `accepted_by`.

## Terminal branches

Each deletes `.ac/state/active-auto.json` before it stops.

| Ending | Where |
|---|---|
| Verdict written and Phase 4 done | Phase 4 |
| The user asked to stop, pause or take back control | anywhere |
| Digest mismatch, no `python3`, a failed branch switch, a source that aborted before its gate | Phase 1 to 3 |

A refusal at 0a or 1a, and a (d) whose work was already complete, wrote nothing, so they leave nothing to clean up.
