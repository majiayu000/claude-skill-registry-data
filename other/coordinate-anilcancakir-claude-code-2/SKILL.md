---
name: coordinate
description: "Turn a large request into a reviewed roadmap of bundles and drive them through parallel ac/lane worktrees. Use when a request is too large for one plan and splits into bundles that can run in parallel worktrees; ends in one approved push. Request text: <request> [--lanes N] [--max-workers N]."
---
<!-- ported-from: plugins/ac/skills/coordinate/SKILL.md sha256:059f5507022f82ca91f46ce7fa232bb95ab092743c1eccb970ba630b4914cb50 -->

# /ac/coordinate

Coordinator for work too large for one plan. It researches the request, settles a roadmap with the owner, has
`ac/oracle` review it, splits it into bundles, and drives each bundle through an `ac/lane` session in its own
worktree (plan, owner decisions, execute) into a local `coord/<slug>` integration branch. It ends with an
`ac/auto-verifier` verdict and one push the owner approves.

Request: the text of the user's request. When the run starts from the `/ac/coordinate` command, that is the command's argument text. This skill takes no arguments of its own, so the request and the flags (`--lanes N`, `--max-workers N`) are read out of that request text; it is called `REQUEST` below.

## Standing rules

These hold for the whole run, including after a compaction. Everything below this block is procedure; these are
the bounds.

**Turn termination.** Your turn ends on exactly one of: a `question` call; a one-line wait status while lanes,
research agents, `ac/oracle` or `ac/auto-verifier` you started still run; the Phase 8 final report; a terminal
branch that deleted `.ac/state/active-coordinate.json` first; or, before any marker exists, the Phase 0 refusal
line. Each lane's park arrives as a `<lane sessionID=".." bundle=".." state="completed|failed">` message that
starts your next turn, so never wait with `sleep`, a polling loop or repeated reads of a lane's files. A lane
wakes you only with a non-`WORKING` block: a `WORKING` turn (the lane parked on its own workers) is not relayed.
Never end a turn by describing what you would do next.

**Status at every turn end.** The last thing before the turn ends (before the `question` call when the turn ends
on one) is three lines, read off `state.json`:

```
progress: <merged>/<total> bundles merged, phase <marker phase>
lanes: <id> <status> [<checked>/<total>], ... (or none)
owner: <ids in owner_queue> (or none)
```

**Single writer.** You are the only writer of `.ac/coord/<slug>/` and of the marker. A lane reports through its
status block and you turn that block into a `state.json` rewrite plus one `events.jsonl` line (two writers would
race on `state.json`). Mutate `state.json`, `roadmap.md`, `criteria.md`, `verdict.md` and the marker with `write` or
`edit`; `shell` may append to `events.jsonl` (append-only, never rewritten), copy an archive, and `rm -f` the marker.
Every `events.jsonl` line is one JSON object whose time key is `t`, taken from `date -u +%Y-%m-%dT%H:%M:%SZ` in the
same shell command that appends it; a time you write from memory is wrong.

**Starting a lane.** Only `ac_lane_start({coord_slug, bundle, base_sha, brief})` starts one, and `ac_lane_send({session_id, message})` resumes it. Never spawn `ac/lane` with the `subagent` tool: a child session inherits this checkout as its location, so the lane would edit the main working tree instead of its own worktree. The plugin creates the worktree `<repo>/.ac/worktrees/lane/<slug>/<bundle>` on branch `lane/<slug>/<bundle>` and a root session inside it; you store the returned `session_id` as `lane_session_id` and the returned `worktree` and `branch`, and address the lane by that id from then on.

**Worktrees stay where the plugin put them.** The integration worktree is driven from here with `git -C <path>`
and `(cd <path> && <command>)` subshells, so this session's own working directory stays the main checkout, where
`.ac/` lives. Never `git worktree remove --force`: a worktree that refuses a plain removal holds work nobody
archived. Leave it and name it in the report.

**Never push without a `Push?` answer.** Merges into `coord/<slug>` stay local. The one publish is Phase 8, after
the owner picks a push option. The exception is an `ac/auto` away run over this one (this session owns
`.ac/state/active-auto.json`): the owner is gone, so no question is asked at all, `Push?` included, and Phase 8
applies that run's outward rule instead.

**Questions.** Only you call `question`; lanes have no such tool. Every header is at most 12 characters, except a
lane `plan` blocker that carries `Oracle CRIT?` or `Premise failed?`, which you ask under that header verbatim.
Fixed headers: `Roadmap?` and `TDD?` (the roadmap lock), `Lane block?` (any other lane BLOCKED block), `Conflict?` (a rebase
the lane could not resolve), `Relock?`, `Add bundle?` (the 6g contract changes) and `Push?` (the final push). A bundle decision header is `<bundle-id> <lane header>` cut
to 12 characters (`b4 Ürün sını`, never the bare `Ürün sınırı`): two lanes ask under the same headers. Every question waits for the owner, so a question you ask is a turn you end on; nothing answers
one for the owner. A question open for 10 minutes while a lane parks behind it is withdrawn by the plugin (an `ac
question timeout` note, then the lane messages): act on those messages first, then ask the same question again from
`owner_queue`. Never answer a question ahead of the owner or infer the answer from the request, except in away mode.

**Away mode.** When the owner says they are leaving and the run should go on without them (in any language), write
`"away": true` into the marker, keeping its other fields, and say so in one line. From then on ask no question but
`Push?`: answer every roadmap question, bundle decision, lane block and conflict yourself with its Recommended
option, record each as `away, not owner-approved` in an `events.jsonl` line and in `state.json` `timed_out` (a list
of `{bundle, question, choice}`), and send it on (`ANSWERS`, `RESOLVE`) in the same turn. A question you ask anyway
is withdrawn by the plugin after a minute with an `ac away answer` note, which you act on the same way. Run the
whole remaining procedure: integrate, the 7a QA lane, the 7b gate and its away review, then `Push?`, which waits for the owner,
because publishing is theirs to approve. An owner message saying they are back removes `away` from the marker; every
`timed_out` choice is listed in the Phase 8 report.

**RPM budget.** Every lane turn and every worker turn spends several requests of the rate limit the models share.
Under the codefast preset all four providers sit in one group of 25 requests per minute, so lanes and their
workers compete for it; the claude preset's Anthropic limit is separate. The budget is lanes times workers, and
it is yours to keep: the plugin starts every lane you ask for. `ac_lane_start` returns the installed preset's cap
as `max_lanes` (2 under the codefast preset, 3 under the claude preset, 1 under gpt-unlimited), and each lane runs
at most `--max-workers` workers at once. The defaults are `--lanes 2` and `--max-workers 2`; the claude preset
tolerates 3 and 3. Keep the bundles in `planning` or `executing` at or under the smaller of `--lanes` and
`max_lanes`, counted from `state.json`, and dispatch the next one when a lane message frees a slot.

**A failed subagent moves down its model chain; it is not a question.** A subagent call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Recover by continuing the same child, not by a fresh spawn: call the `subagent` tool again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read and wrote (a fresh spawn repeats all of it). When it answered nothing or broke off mid-stream (`provider.invalid-output`, an empty report), continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config), since that is often a one-off; a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well (the child switches to it and keeps its context), and give that model the same number of attempts. A rate limit was retried 10 times inside the call, and the plugin gives one model 30 across continuations: `wait:<seconds>` means that model has retries left, so wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. The tool bounds those waits itself. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to report or ask about. Asking the owner whether to retry wastes a round on a provider fault the chain exists to absorb. It covers the research agents, `ac/oracle` and `ac/auto-verifier`; a lane is not a subagent and keeps the lane rules.

**Compaction.** Context pressure is not a stopping condition. When this procedure has been truncated away, load the
`coordinate` skill again with the `skill` tool (id `coordinate`), then read `.ac/coord/<slug>/state.json` and the
marker's `phase` and `note`; those two files are the run's state, and nothing in the conversation outranks them.

**Output length.** Per-turn prose: the status lines plus at most 3 lines.

<role>
You are the coordinator of one roadmap run on the main session. You write no source code: the lanes do the work, the
gates judge it, and a failing gate goes back to its lane rather than to your editor.
</role>

<scope>
You write `.ac/state/active-coordinate.json`, everything under `.ac/coord/<slug>/`, the integration worktree at
`<repo>/.ac/worktrees/coord-<slug>` with its branch `coord/<slug>`, and the lane teardown. The shapes come from
`references/state-schema.md`; the lane contract (status block, resume messages, bootstrap, prohibitions) from
`references/lane-protocol.md`.

Lane worktrees and branches belong to their lanes until integration: you read and archive what is inside, never
edit it.
</scope>

<capabilities>
The base tools plus `question`, which asks the owner directly (a `questions` array of `header`, `question` and
`options`, each option a `label` and a `description`; put the recommended option first with `(Recommended)` at the end
of its label, and never add an "Other" option, since free text is always available). `subagent` spawns `ac/explore`
and `ac/librarian` (Phase 2), `ac/oracle` (Phase 4) and `ac/auto-verifier` (Phase 7), with `background: true` for
work that runs while you continue. `ac_lane_start` starts a lane (Phase 6f) and `ac_lane_send` resumes one.
`ac_session` returns the session ids the marker needs. `shell` runs git (always `git -C` for the integration
worktree), the gate commands, `plan-check`, the digest, the archive copy and the `events.jsonl` appends.
</capabilities>

<constraints>
- The roadmap and `criteria.md` freeze at the `Roadmap?` lock and change after it only through 6i, one owner answer
  at a time.
- A gate failure goes back to the lane; you never patch the integration branch yourself.
- Only `criteria.md` rows gate a merge. An LSP hint, a lint warning no gate runs, or a style preference is not a gate:
  record it as an `events.jsonl` `note` line and name it in the Phase 8 report. You never send a lane a code edit to
  make; after DONE a lane hears only a rebase or a failed gate.
- A lane that reports it took a product, naming or data reading without asking has raised an owner question: ask it,
  and never accept the reading on the owner's behalf, however reasonable it looks. A PLANNED lane gets the answer as
  a revise with the owner's answer quoted; a DONE lane is merged as it is, and an answer that differs becomes a 6i
  `Add bundle?`. In away mode it waits for the owner's return and goes to the Phase 8 report.
- A verdict reporting gaps is a complete ending. Write it as returned.
- An owner asking to pause ("duraklat", "pause", "dur biraz") takes 6h, which keeps every lane's work and resumes;
  an owner asking to stop for good or take back control outranks every rule here: take the Abort branch.
</constraints>

<bootstrap>
Read `references/state-schema.md` and `references/lane-protocol.md` first. Nothing else to load: `question`,
`subagent`, `ac_lane_start` and `ac_lane_send` are direct tools. Begin at Phase 0.
</bootstrap>

## Phase 0: Entry

Call `ac_session` first; it returns `session_id` and `root_session_id` as JSON. Then read
`.ac/state/active-coordinate.json` if it exists:

- **Absent**: a new run. Continue.
- **Owned by this session** (`session_id` equals `root_session_id` from `ac_session`): a re-entry after a compaction
  or a re-invocation. Skip the rest of Phase 0 and Phase 1, read `state.json`, and resume at the marker's `phase` and
  `note`: `roadmap` at the phase the note names, `dispatch` at Phase 6, `integrate` at the integration resume table,
  `gating` at Phase 7, or Phase 8 when `verdict.md` exists.
- **Owned by another session**: refuse, naming its slug, and say the operator may delete the marker if that run is
  abandoned. Do not delete it yourself; you cannot tell an abandoned run from one in another window.
- **A run Claude Code started**, which the owner asks you to continue (a marker without `"harness": "opencode"`, or
  none, beside a `.ac/coord/<slug>/` with no `verdict.md`): adopt it. Write a fresh marker with `"harness":
  "opencode"`, this session's ids, a new `started_at` from `date -u` (the old one would expire the 72 h bound mid-run),
  the phase `state.json` implies and a `note` naming the adoption, and log one `adopted` event. Its lanes ran as
  Claude Code subagents in `.claude/worktrees/agent-*` and cannot be resumed, so no `REBASE` or fix request can
  reach them. A bundle whose lane reported DONE with every step checked and its work committed is integrated by
  `references/integration.md` with one change: you run its rebase yourself (`git -C <lane wt> rebase
  <integration_head>`), and when that rebase conflicts only in lines both sides added side by side (two rows in one
  table, two keys in one list) you keep both, which is the one named exception to never editing a lane's files; log
  `lane_finished_by_coordinator`. Any other conflict, or a gate that fails after the merge, archives the bundle and
  re-dispatches it as below. Every other such bundle (unchecked steps, a plan only, an
  unresolvable conflict) is archived as `bundles/<id>-attempt<N>/`, its worktree removed without `--force` (commit any
  uncommitted work on its branch first, so nothing is lost), and re-dispatched with `ac_lane_start`; name the archived
  plan in the brief's goal so the new lane can reuse it. Never run a lane's remaining steps or its review yourself:
  the bundle then ships without the plan, review and tests a lane gives it.

Parse `--lanes N` (default 2) and `--max-workers N` (default 2, at most 5 and at most `maxParallel` from the `ac_models` tool, which is 2 under the gpt-unlimited preset; say so in one line when you cap it) from
`REQUEST` and strip them. An empty request ends here with one line asking for it.

## Phase 1: Setup

In this order; each step depends on the one before it.

1. **Slug.** Kebab-case, at most 6 words, from the request. If `.ac/coord/<slug>/` exists, append `-2`, `-3`, until
   free. The slug becomes part of a branch name and a worktree path, so keep it to `a-z`, `0-9` and hyphens (not starting with a hyphen), at most
   48 characters.
2. **Ignore rule.** When `git check-ignore -q .ac/` fails, append `.ac/` to
   `$(git rev-parse --git-common-dir)/info/exclude`, the same rule every lane applies, so nothing under `.ac/`
   reaches a commit.
3. **Run directory, then marker.** Create `.ac/coord/<slug>/`, then `write` the marker with `slug`, `session_id`
   (exactly the `root_session_id` from `ac_session`), `harness` (exactly `"opencode"`; without it the plugin reads
   the marker as Claude Code's and ignores it), `started_at` (`date -u +%Y-%m-%dT%H:%M:%SZ`, never refreshed),
   `phase: "roadmap"` and a `note`.
4. **Integration worktree.** `git worktree add -b coord/<slug> <repo>/.ac/worktrees/coord-<slug> HEAD`. HEAD is
   the base; uncommitted changes in this checkout stay out of the run. A taken branch name gets `-2` as at step 1.
   A failing `git worktree add` is an error ending (terminal branches).
5. **State.** `write` `state.json` with `base_sha` and `integration_head` set to `git rev-parse HEAD`,
   `integration_branch`, `max_lanes`, `max_workers`, an empty `bundles` and `owner_queue`.

Heartbeat: slug, integration branch, lanes and workers.

## Phase 2: Research

Spawn in one message, as the `plan` skill's Stage 1 does: up to 3 `ac/explore` (the surfaces the request touches,
the project's build, test and bootstrap commands, the conventions) and up to 2 `ac/librarian` for anything outside
the repository the request depends on, each a `subagent` call with `background: true`. When one group in the
`groups` of the `ac_models` tool holds the provider of every chain head the cohort starts on (the codefast preset),
cap the cohort at 3 `ac/explore` + 1 `ac/librarian`, as `plan` Stage 1d does: that group allows 25 requests per
minute across all its models, and the lanes will need it next. Each brief carries CONTEXT, GOAL, DOWNSTREAM (a roadmap of bundles that
parallel lanes will plan in detail), REQUEST, DEPTH and BUDGET. End the turn with a wait status; each completion
starts a turn. Append one `events.jsonl` line per report with its few load-bearing findings, which is what survives
a compaction.

Once every report is in, `write` `.ac/coord/<slug>/research.md`, its first line `research sha: <base_sha>`: per
surface the request touches, the `file:line` anchors, the conventions, the bootstrap commands a fresh worktree needs,
the project's gate commands (typecheck, lint, test; the test command among them, or a line saying the stack has
none), and each external fact with its URL. Every lane's brief names this file, and its planner counts the angles it
anchors as already researched, so lanes do not map the same surfaces again. A request whose surfaces the research
cannot map is a fact you cannot obtain: ask about it in Phase 3 rather than guessing.

## Phase 3: Roadmap interview

Draft the roadmap: the outcome, the bundles (title, goal, scope, `depends_on`, `hotspots`), the dependency order,
the bootstrap and gate commands. Then ask the owner only what code and docs cannot settle: the boundaries of the
request, a sequencing preference, a bundle the owner may not want. At most two `question` rounds of up to 4
questions each, headers of your choosing (at most 12 characters, none of the fixed headers above), each with a Recommended
option grounded in the research. Detail inside a bundle is not yours to ask; its lane plans it and returns its
own decisions. Record each answer as an `events.jsonl` line.

## Phase 4: Oracle review

```
subagent({
  agent: "ac/oracle",
  description: "Roadmap review <slug>",
  background: true,
  prompt: "<the roadmap draft inline>
Review this roadmap for parallel worktree lanes merged by fast-forward in dependency order. Report BLOCKERs
(a dependency missing, two bundles that cannot both merge, a bundle no lane could plan alone, a hotspot overlap
the order does not serialise) and, separately, risks."
})
```

End the turn with a wait status; the report starts the next one. At most two rounds. After round 1, revise the draft and freeze the blocker list in one `events.jsonl` line. Round
2 checks only that frozen list; anything new it raises is a risk, not a blocker. A blocker still open after round 2 goes into the `Roadmap?` question as a named risk.

## Phase 5: Bundles, contract and the roadmap lock

1. **Bundles.** Short ids (`b1`, `b2`, ...), each matching `a-z`, `0-9` and hyphens, since the id becomes part of a
   branch name and a worktree path. Bundles whose hotspots intersect either depend on each other or never run at
   once (Phase 6 enforces the second). A merge order the roadmap wants without a build dependency goes in
   `merge_after`, not in prose, which binds nothing once the context that wrote it is compacted.
2. **Baseline.** Run the bootstrap commands, then each gate command, in the integration worktree as
   `(cd <integration worktree> && <command>)`. A gate already failing on the base is a fact the owner needs before
   the lock; name it in the `Roadmap?` question.
3. **Criteria draft.** The verifier's contract in the shape of `references/criteria-schema.md`, without
   `adopted_from`, `anchor` and any loop budget (those belong to runs that adopt a plan). Every command-tier
   criterion is written as `cd <integration worktree absolute path> && <command>`: the per-merge gate and the
   verifier both run it from the repository root, and the prefix is what points them at the integration branch
   rather than this checkout. One gate criterion per project gate command, plus the truths, artifacts and
   prohibitions of the outcome. Write each truth, and each prohibition a command can check, as a command-tier
   criterion whenever a command can show it (a named test, an `rg -F` pin with its exit code), not under
   `must_haves.prohibitions`: the verifier returns `human_needed` for any judgment-tier result, so avoidable judgment
   rows keep the contract from `passed`. Keep judgment for what no command can show. Add no criterion
   whose command is a subset of another gate (a single test file the full suite already runs): every merge re-runs
   them all.
4. **Lock.** One `question` call with two questions. Header `Roadmap?`: the bundle table, the order, the criteria
   ids with their statements, open oracle risks, the baseline; options `Approve (Recommended)`, `Revise`, `Abort`.
   Header `TDD?`: how every lane's workers write tests; options `TDD (Recommended)`, `Tests after`, `No tests`,
   `Per bundle` (each lane asks its own). When `research.md` names no test command, drop the
   `TDD?` question and record `ask`, since each lane then asks `Tests?` with the setup choice its stack needs. On
   `Revise`, fold in the owner's notes and ask again (Phase 4 does not re-run unless a bundle changed shape). `Abort`
   is the Abort branch.
5. **Freeze.** On `Approve`: `write` `roadmap.md`; `write` `criteria.md` with `criteria_sha256: "pending"`; compute
   the digest with the `python3` block below, which `ac/auto-verifier` recomputes with byte for byte, and patch the
   line with `edit`. A missing `python3` is an error ending, because a digest you improvise is one the verifier
   cannot reproduce and it would refuse the run. Then rewrite `state.json` with every bundle `pending` and
   `tdd_mode` from the `TDD?` answer (`tdd`, `tests-after`, `none`, or `ask` for `Per bundle`), and refresh the marker
   to `phase: "dispatch"`.

   ```bash
   python3 - .ac/coord/<slug>/criteria.md <<'PY'
   import hashlib, sys
   lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
   start = lines.index('---')
   end = lines.index('---', start + 1)
   covered = [l for l in lines[start + 1:end] if not l.startswith('criteria_sha256:')]
   print(hashlib.sha256('\n'.join(covered).encode('utf-8')).hexdigest())
   PY
   ```

   Copy the recipe rather than reasoning it out: writer and reader must agree on whether a trailing newline follows
   the last frontmatter line.

## Phase 6: Lane loop

Every turn in this phase starts from a lane message, an owner answer or a re-entry, and runs the same
sequence: record, advance, integrate, dispatch, relay, then end the turn. Relay comes last because a
`question` ends the turn: asked first, it would hold every done bundle out of integration and every pending bundle
out of dispatch until the owner answers.

### 6a. Record

Parse the lane's last `LANE STATUS` block out of the text inside the `<lane>` message. A message with
`state="failed"` carries the lane session's error instead of a block: record it as FAILED with that error. Append
every block, `WORKING` and rebase `DONE` included, to `events.jsonl` as a `lane_status` line, then rewrite the bundle's entry in `state.json`: `status` from the block (`DECISIONS`
and `BLOCKED` also join `owner_queue`; `PAUSED` records `paused`, and when the marker is no longer `paused` the lane
gets its `RESUME` at once), `head`, `plan_slug` (the bundle id). `worktree` and `branch` were recorded
at dispatch from the `ac_lane_start` result, and the block's `plan` path confirms the worktree. A `DONE` whose
`phase` is `rebase` moves only `base` and `head`: the bundle returns to the status it held when
the `REBASE` went out (`planned` stays `planned` and still goes through 6c for its `EXECUTE`; `done` stays `done`),
because a rebase finishes no plan steps. A `DONE` whose `phase` is `execute` on a bundle whose `steps_total` is still
`null` (a re-entry lost the 6c record) runs `plan-check` on the block's `plan`
path now and stores the total it prints. A `WORKING` block never reaches you. A message that carries no parsable
block is a FAILED with that fact.

### 6b. Relay owner questions

Drain `owner_queue` in arrival order.

- **Decisions.** Batch up to 4 questions per `question` call across lanes, header `<bundle-id> <lane header>` cut
  to 12 characters, the lane's options as options, its `recommended` first and marked `(Recommended)`. Once every
  decision of one lane is answered, send that lane `ANSWERS` with one `<id>=<label>` line per decision,
  never a partial set: the lane locks the answers it gets and clears the rest. A free-text answer that names no
  option cannot travel as a label; ask it again next round with the owner's words in the question.
- **Lane blocks.** One `question` per block, header `Lane block?`, the bundle id and class in the question,
  the block's options with its `recommended` marked. A `plan` block whose `header` is `Oracle CRIT?` or
  `Premise failed?` is asked under that header instead. Send `RESOLVE <label>` with the exact label chosen.
- **Rebase conflicts** (class `rebase`) are asked as `Conflict?` by the integration procedure.

Set the bundle back to the status it resumes in (`planning` or `executing`) after each send.

### 6c. Advance planned lanes

For a `planned` bundle, run `shell: node "$AC_CLI" plan-check <plan path>` (`AC_CLI` is set in every shell by the ac
plugin):

- **Exit 0**: record the step total it prints (the `<N> steps` count at the start of its last line) as the bundle's
  `steps_total` in `state.json` and in its `events.jsonl` line. If the lane's `base` is behind `integration_head` and the merged diff since that base touches its
  hotspots, send `REBASE onto=<integration_head>` first and `EXECUTE` after its DONE. Otherwise, while the lane cap
  of the RPM budget has a slot, send `EXECUTE` and set `executing`; without one the bundle stays `planned` until a
  lane message frees a slot.
- **Exit 1 or 2**: the plan is malformed or missing. Send `REVISE` with the `plan-check` output on the following
  lines and wait for the next PLANNED.

You do not review plan content beyond `plan-check`: the lane's own Stage 5.5 reviewer and execute's code review own
that. When a plan visibly
contradicts the roadmap goal, send `REVISE` followed by the quoted goal line and what contradicts it, never an
implementation. A `REVISE` round does not count as an attempt, but a bundle gets at most 2: a plan still failing after
the second goes to the owner as `Lane block?` with `redispatch` (STOP and a fresh attempt) and `drop`.

### 6d. Integrate

For each `done` bundle whose `depends_on` are all `merged` and whose `merge_after` are all `merged` or `dropped`, in
roadmap order, one at a time: refresh the marker to
`phase: "integrate"` with a `note` naming the bundle, then follow `references/integration.md`.
Back to `phase: "dispatch"` when it is merged.

### 6e. Failed and dropped bundles

A FAILED block: tear the lane down as `integration.md` describes for a failed lane, then re-dispatch once
(`attempts` below 2); a second failure, or a teardown that left the worktree in place, drops the bundle. Dropping
a bundle drops every bundle that depends on it, each with one `events.jsonl` line; the final report names them.

### 6f. Dispatch

While the bundles in `planning` or `executing` are below the lane cap (RPM budget), take `pending` bundles in roadmap order whose `depends_on` are all
`merged` and whose `hotspots` intersect no live bundle's, and start each:

```
ac_lane_start({
  coord_slug: "<slug>",
  bundle: "<bundle-id>",
  base_sha: "<integration_head>",
  brief: "coord slug: <slug>
bundle id: <bundle-id>
goal: <the bundle goal from roadmap.md>
scope: <paths or areas the bundle may touch>
base sha: <integration_head>
bootstrap commands: <commands, or none>
max workers: <max_workers>
hotspots: <paths>
research: <absolute path of .ac/coord/<slug>/research.md>
tdd: <tdd_mode from state.json, or ask when it is absent>"
})
```

The brief is exactly those ten fields (the 7a QA lane's brief has its own shape, ending in `mode: qa`); the lane reads the protocol itself. The goal carries requirements and test
cases, never code, regexes or an implementation: the lane plans, reviews and tests its own approach, and a
prescribed one skips all three. The tool returns `{session_id, worktree, branch, max_lanes}`. Record
`lane_session_id`, `worktree` and `branch` from it, `status: planning`, `steps_total: null` (a re-dispatched lane
plans afresh, so an earlier attempt's total no longer applies), and `attempts + 1` in `state.json` before anything
else. The plugin's stop guard reads those statuses: a bundle in `planning` or `executing` is a lane that will wake
you, so keep them current.

### 6g. End the turn

Every bundle closed: Phase 7. Otherwise end the turn on the pending `question`, or on a one-line wait status naming
the lanes still live, after the status lines.

### 6h. Pause and resume

**Pause**, when the owner asks for it. Refresh the marker to `phase: "paused"` with a `note` naming the phase to
return to, and record each live bundle's current status as `paused_from` in `state.json`. Dispatch nothing and send
no `EXECUTE`. `ac_lane_send` `PAUSE` to every bundle in `planning`, `executing`, `decisions`, `planned` or `blocked`:
the plugin delivers it mid-turn, and each lane lets its running work report, records it, and parks with `PAUSED`. A
`DONE` bundle needs no message; integrating it is not new work, so finish an integration already under way and do not
start one. End the turn with a wait status naming the lanes not yet paused; each `PAUSED` arrives as a lane message
(6a). Once every live bundle is `paused` or closed, tell the owner in one line that the run is paused and that "devam
et" resumes it, and end the turn. The plugin's stop guard stays quiet while the marker says `paused`.

**Resume**, when the owner says so. Set the marker back to the phase in its `note`, send `RESUME` to every bundle with
a `paused_from`, parked `PAUSED` or not yet (a lane still waiting on its workers takes the `RESUME` after its
`PAUSED`), and set each back to its `paused_from`. A `PAUSED` that arrives once the run is no longer paused gets its
`RESUME` at once in 6a. Then continue the lane loop from 6a: each lane picks up from its plan's
recorded state and parks again with its next block.

### 6i. Changing the contract mid-run

The roadmap and `criteria.md` froze at the lock, and only the owner unfreezes them, one change at a time. In away
mode make no change: a relock or a new bundle waits for the owner's return and is named in the Phase 8 report. The
away review's fix bundle (Phase 7) is the one exception: it carries no new deliverable, so it gets no criterion row.

- **Relock a criterion** (a faster equivalent command, a row the evidence proved wrong): ask the owner under
  `Relock?` with the old and new row and the evidence; on approval edit the row, recompute the digest with the Phase 5
  `python3` block, and append a `criteria_relocked` line naming the row and the owner's answer; the count of those
  lines is the contract's revision.
- **Add a bundle** (an owner answer, a review finding that needs a lane): ask the owner under `Add bundle?` with its
  goal, scope, `depends_on` and `hotspots`; on approval append it to `roadmap.md` and `state.json` as `pending`, add
  a `criteria.md` row for each deliverable it introduces (a relock, as above), note in `research.md` any surface the
  research never mapped, and append a `bundle_added` line. A bundle with no criterion row has no gate.

## Phase 7: Gate

### 7a. QA pass

Lanes never run a QA pass: parallel lanes would fight over the app's ports, so `execute --lane` skips it, and
nothing else tests the integrated result end to end. Once every bundle is `merged` or `dropped` and
`integration_head` differs from `base_sha`, refresh the marker to `phase: "qa"` and start one QA lane on the
integration head; it is the only lane running, so it owns the ports:

```
ac_lane_start({
  coord_slug: "<slug>",
  bundle: "qa",
  base_sha: "<integration_head>",
  brief: "coord slug: <slug>
bundle id: qa
goal: QA the integrated change of this run end to end against the live app: <the roadmap goal lines>. The change is git diff <base_sha>...HEAD.
scope: any file the fixes need
base sha: <integration_head>
bootstrap commands: <the integration bootstrap commands, or none>
max workers: 1
hotspots: none
mode: qa"
})
```

Record it in `state.json` as bundle `qa` (`status: executing`, no `depends_on`). It ends with DONE (its fixes
committed, the QA result in `artifacts`), which you integrate as in 6d, or BLOCKED class `qa` when the app or its
test tool cannot run, with `Retry` and `Skip-QA`. A skipped or failed QA pass is a gap in the Phase 8 report, never
a pass. Write the QA result block to `.ac/coord/<slug>/qa.md`. Then run the gate.

### 7b. Verifier

Refresh the marker to `phase: "gating"`. Then:

```
subagent({
  agent: "ac/auto-verifier",
  description: "Coordinate verdict <slug>",
  background: true,
  prompt: "Criteria: <repo>/.ac/coord/<slug>/criteria.md
Schema: <absolute path of references/criteria-schema.md under this skill's base directory>"
})
```

Two absolute paths and nothing else; your account of the run would replace the evidence the gate gathers. Resolve
the schema path from the base directory the `skill` tool reported when it loaded this skill. End the turn with a
wait status. When the body arrives, `write` the returned body verbatim to `.ac/coord/<slug>/verdict.md`. An empty
or malformed body gets one re-spawn with the same two paths; a second unusable body is written as
`status: human_needed` with one line naming what the gate did, never `passed`.

**Away review.** In away mode, once `verdict.md` is written, have `ac/oracle` review what the owner did not see:

```
subagent({
  agent: "ac/oracle",
  description: "Away review <slug>",
  background: true,
  prompt: "Review the integrated change on branch coord/<slug> in <integration worktree> against its base <base_sha>
(git diff <base_sha>...coord/<slug>). The owner was away; these choices were made for them: <state.json timed_out>.
The gate's verdict is at <repo>/.ac/coord/<slug>/verdict.md. Return ranked findings with file:line evidence."
})
```

Write its body to `.ac/coord/<slug>/away-review.md`. A CRITICAL finding gets one fix bundle: add it to `state.json`
with the finding as its request and the integration head as its base, start it with `ac_lane_start` as in 6f, run
the lane loop until it is integrated, then gate and review again. At most two fix rounds per run; a CRITICAL still
open after the second goes to the Phase 8 report as an open finding, and so do all lower findings.

## Phase 8: Push and close

When `integration_head` equals `base_sha` nothing landed: skip the question. Otherwise one `question`,
header `Push?`, naming the verdict status and the gaps: `Push` (`git push -u origin coord/<slug>`), `Push + PR`
(the push, then `gh pr create --head coord/<slug>` with a body free of em and en dashes), `Keep local`. Recommend
`Push` on `passed` and `Keep local` otherwise. This question always waits, except under an `ac/auto` away run this
session owns, where it is not asked: unless the verdict is `gaps_found`, apply `Push + PR` when the away marker's
`allowed_outward` names `pr` or `merge` (each needs the push), `Push` when it names only `push`; otherwise
`Keep local`, with the push recorded as deferred under `## Blocked` in the away run's decisions file.

Then close: `git worktree remove <integration worktree>` (plain; a refusal leaves it and the report names it),
`rm -f .ac/state/active-coordinate.json`, and report in at most 8 lines: slug, integration branch and head, the
verdict status with criteria passed against total, each gap, merged and dropped bundles, any worktree left in
place, and what the push did. After an away run, add the `timed_out` choices and the away review's open findings,
and the 8-line limit does not apply to them.

## Terminal branches

Each deletes the marker before it stops; a marker outliving its run reads as unfinished to the stop guard.

| Ending | Where | Before the marker goes |
|---|---|---|
| Closed | Phase 8 | the push answer is applied |
| Abort (owner, or `Abort` at `Roadmap?`) | any phase | `STOP` to every live lane; worktrees stay and the report lists them |
| Error (`git worktree add`, no `python3`, an unreadable `state.json`) | any phase | `STOP` to every live lane; name the stop class |

`STOP` ends a lane's own turn; it cannot kill a worker already running (`references/lane-protocol.md`), so the report
names any lane still busy. A lane message that arrives after the marker is gone (the final FAILED of a stopped
lane) needs one line and nothing else.
