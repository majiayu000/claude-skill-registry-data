---
name: board
description: The layer around the official Multica CLI skill — where the binary hides in a desktop-app install, how to reach it from a bridged Cowork/claude.ai session, the shell and JSON shapes that bite, the platform limits, and how to work a board that is governed by a repository which versions its Multica configuration. Use alongside the official `multica-cli` skill whenever a task touches a Multica board.
---

# Multica: the parts around the command reference

## 0. The command reference is not this skill

Multica publishes the canonical CLI skill at
[`multica-ai/multica-cli`](https://github.com/multica-ai/multica-cli). It is well maintained —
a linter runs its documented commands against the real binary daily, on both the minimum and
latest CLI — and it is the authority on the command surface:

```text
/plugin marketplace add multica-ai/multica-cli
/plugin install multica-cli@multica-cli
```

Go there for: `issue search` semantics, the comment read modes (`--roots-only --summary`,
`--thread --tail`, `--recent` capping *threads* not comments, `--compact`, `--full`), the
working-directory restriction on `--content-file` / `--description-file` / `--attachment`, when
`--parent` is mandatory, the `mention://` side effects, metadata versus custom properties,
subscribers, run inspection and cancellation, sub-issue stages, and PR linking.

**Do not restate any of that here.** Two skills that describe the same commands will disagree
eventually, and the session obeys whichever it read first. This skill covers what that
reference does not, and the moment it starts to overlap, the overlap is the bug.

If the reference is not installed, say so before operating a board — the safe defaults for
mentions, status side effects and comment writes live there.

## 1. Finding the binary in a desktop-app install

The reference assumes `multica` is on `PATH` (a package-manager install). With the desktop app
it is not, and `command -v multica` returning nothing is expected — the reference's very first
step, `multica version`, fails there.

```bash
M="${MULTICA_BIN:-/Applications/Multica.app/Contents/Resources/app.asar.unpacked/resources/bin/multica}"
"$M" --version
ls ~/.multica/profiles       # the profile names on this machine
P="${MULTICA_PROFILE:-<one of those>}"
"$M" --profile "$P" workspace list --output json    # -> [{id, name, slug}, …]
```

Record the version next to any claim you make about the surface. The CLI ships changes almost
daily; the output shapes in §4 were first measured on **v0.4.42**, and everything added since —
the control-character note, the `parent_issue_id` note, the reply-routing rule in §5 — on
**v0.4.44**, between 19 and 20/09/2026.

## 2. Two routes, and only one is direct

**Claude Code on the machine with the desktop app** — run the CLI in the shell. Done.

**A Cowork or claude.ai session bridged to that machine** — the session's own shell runs in a
separate sandbox with only the connected folders mounted. It cannot see `/Applications`, so it
cannot reach the CLI. The route that works is the bridge's shell on the user's machine (on
macOS, an AppleScript `do shell script "…"`), and three things bite there:

- Nested quoting breaks easily — avoid `python3 -c` with inner quotes. Write output to a file
  inside a connected folder and read it from the sandbox.
- That shell reports any non-zero exit as a tool error, even a `which` that finds nothing. End
  with `; echo done`, or `|| true`, when the exit code does not matter.
- The sandbox usually cannot delete files in connected folders. Clean up from the same bridge
  shell that created them.

With the desktop app closed, neither route exists. Say so and move on.

## 3. Shell gotchas that have produced real defects

Mostly zsh, the macOS default:

- **A variable holding several flags becomes one argument.** `"$M" $flags --help` fails. Wrap
  it: `mt(){ "$M" --profile "$P" --workspace-id "$WS" "$@"; }` — or drive the CLI from Python's
  `subprocess`.
- `for x in $VAR` iterates **once**. Use `${=VAR}` or a real array. This has silently produced
  batches of issues carrying an invalid `--workspace a b`.
- zsh arrays are **1-indexed**: `${A[0]}` is empty, which is how an issue gets created with a
  blank field.
- `pipestatus` is lowercase, and `EXIT=$?` after a pipeline measures the *last* command:
  `bash script | tail` gives you `tail`'s exit code. This is not theoretical: on 20/09/2026 an
  `&&` chain continued past a gate harness that had just printed 4 FAIL, because the exit read
  was `tail`'s. Capture first, then test — `OUT="$(cmd 2>&1)"; RC=$?` before any filter — or
  `set -o pipefail`. Reading a gate's verdict out of a pipeline is how a session tells the board
  something passed when it did not.
- **Expand a variable with braces when anything follows it.** `git show $TB:path` appends the
  path to the *variable name*, so zsh looks up `$TB:path` — measured on 20/09/2026, it produced
  the nonexistent ref `tech-676-2-17-1k-changelog-local.sh` and a confusing "not found".
  Write `git show "${TB}:path"`.
- **`tr` with sets of different lengths does not error — it pads.** `tr 'A-Z-' 'a-z'` has 27
  source characters and 26 destination ones, so the extra one (`-`) maps to the last destination
  character: `LAS-114` becomes `lasz114`. On 20/09/2026 this silently pointed 17 evidence
  commands at filenames that did not exist and produced **17 false FAIL**, one step before they
  would have been written to seven issues. Keep the sets the same length, or delete in a pass of
  its own (`tr -d '-'`). The general shape — a shell builtin that mangles instead of failing —
  is the argument for §8's rule that a board write never shares a chain with a step that can
  fail.
- **An unquoted heredoc executes backticks, and prose about the shell is full of them.** Writing
  a board comment with `<<EOF` — unquoted, because you need to interpolate a SHA — makes every
  `` `command` `` in the body a command substitution. On 20/09/2026 a comment whose text
  *mentioned* `` `git ls-files` `` as the name of a tool shipped with **440 lines of repository
  listing** spliced into it, and the two sibling comments in the same batch were clean only
  because they happened to name no commands. Use `<<'EOF'` and substitute the variable parts
  afterwards, or build the file in Python. The rule generalises: the moment a body talks *about*
  shell, the heredoc must be quoted.
- Agent shells often abort on the first non-zero exit. Guard commands whose non-zero exit is a
  normal outcome — a drift check that exits 1 on "differs" — with `|| true` or `set +e`.
- BSD grep has no `\s` (use `[[:space:]]`), and `--include=*.md` needs quoting in zsh.

## 4. Output shapes and cost flags the reference does not state

Measured on v0.4.42, against reference v1.1.0:

- `--limit` caps at **100** (default 50); above it the CLI refuses and tells you to page.
  Paging is subtle: advance `--offset` by the **number of issues in the response you just got**,
  using `has_more` from the JSON — not by your requested page size.
- `issue list --fields id,title,status,…` trims the returned object client-side, explicitly to
  cut agent context cost. It is the cheapest flag on the whole board surface and it is absent
  from the reference.
- `issue children --output json` returns `{stages, total, unstaged}`, not an array. Iterate
  `.stages[]` and check `(.unstaged|length) == 0`; a bare `.[]` walks three heterogeneous
  values without erroring.
- `issue comment list` returns a bare list, not `{comments: […]}`.
- **Any string field a person typed can carry raw control characters** — a comment body, an
  issue description, an agent's instructions — and a strict JSON parser fails on the first
  one. It is intermittent, which is worse than constant: measured on v0.4.44, five outputs
  (`issue get`, `issue list`, `issue comment list`, `agent get`, `project get`) parsed
  strictly, and the sessions of 18–19/09/2026 hit bodies that did not. Parse leniently by
  default, because it costs nothing on clean output and a strict parser dying on the one
  body that carries a control character, in the middle of a batch, is what breaks a chain:
  `json.loads(raw, strict=False)` in Python, or strip `[\x00-\x08\x0b\x0c\x0e-\x1f]`
  before a strict parser or before `jq`.
- `autopilot get` wraps its payload in `{"autopilot": {…}}`; the other `get` commands do not.
- **`--summary` truncates the body to roughly 200 characters, silently.** It is a display
  affordance on `issue comment list`, and `--output json` does not turn it off: the JSON carries
  the shortened string with a trailing `…`. Measured on 20/09/2026 — the same comment reads 201
  characters with `--summary` and 2431 without. Harmless while you are scanning threads, which
  is what the flag is for; wrong the moment you use that read to **verify what you wrote**. A
  session that posts a long comment and then measures it with `--summary` concludes it was
  truncated on the way out, and "fixes" a comment that was already complete. Verify writes with
  a read that has no `--summary`.
- **`issue comment list --thread` prints a cursor line before the JSON.** `Next reply cursor:
  --before … --before-id …` lands on stdout ahead of the array, so a strict parser dies on
  character 1 and the error looks like malformed JSON rather than a prefix. Strip to the first
  `[` (`sed -n '/^\[/,$p'`) before parsing.
- **An issue's parent is `parent_issue_id`, not `parent_id`.** `parent_id` is a real field — on a
  *comment*, where it marks the thread — so a parser that reaches for it on an issue gets `None`
  instead of an error, and the session concludes the issue is top-level. Measured on 20/09/2026
  against LAS-69, which reads as parentless through `parent_id` and is in fact stage 3 under
  LAS-40. When a field comes back empty and the answer matters, print the object's keys before
  believing the absence.
- `status_category` collapses custom review statuses together; only `.status` separates them,
  and `status_name` comes back empty for custom statuses inside `children`.
- `trigger_comment_id` exists only on runs of `kind: comment`. A `direct` run carries
  `attribution: issue_assignment` with `source: direct_human`; one started by an agent on a
  human's behalf carries `source: delegation` with the human `initiator` preserved.
- `issue timeline` answers "when did this reach review" and "how long has it sat here" — the
  reference does not mention it, and its own linter flags that.
- `--content-stdin` / `--description-stdin` / `--context-stdin` exist and the CLI's own help
  recommends them for multi-line bodies. The reference prescribes files only, which is the
  portable choice (stdin mangles non-ASCII on Windows) — on macOS, stdin sidesteps the
  working-directory restriction and leaves no file to clean up.

## 5. What wakes an agent when you comment

The reference covers the `mention://` links. It does not cover the **implicit** routing, and
that is what costs money by accident: a plain comment carrying no mention at all can start a
run. These rules come from Multica's own product documentation and the server's comment-routing
code, not from inference.

- A comment whose **first whitespace-delimited token is `/note`** (case-insensitive) triggers
  nothing at all — mentions inside it included, because the check runs before mentions are
  parsed. It posts as an ordinary comment and the token stays in the body. This is the
  one-command way to write on an issue without waking anyone.
- `@all` notifies every member and switches off the assignee fallback for that comment. It does
  not reach agents: agents have no inbox.
- With neither of those, routing follows the discussion: a reply to an agent's comment goes to
  that agent; a reply inside a discussion an agent already joined stays with that agent; a
  **top-level** comment matching neither goes to the issue's **agent assignee** (the leader,
  when the assignee is a squad). A plain reply to a *member's* comment does not fall back to the
  assignee. Any explicit mention — including of a member — cancels the fallback.
- **"A reply to a member's comment is safe" holds only when the root carries no agent mention.**
  A thread inherits its root: reply inside a discussion whose *root text* mentions an agent, and
  that agent is enqueued — even when both the root and your reply were written by a member, and
  even when your reply mentions nobody. Measured on 19/09/2026 (CLI v0.4.44): five replies by the
  same human to their own comments, under roots that named the Adversarial Reviewer, started five
  extra Reviewer runs and duplicated a whole review round. Before replying in a thread, read the
  root. To amend or complete a review request already posted, start the comment with `/note`; if
  it genuinely needs to wake someone, post a fresh top-level request with the right head and
  cancel the wrong run with `issue cancel-task <run-id>` first. Either way, confirm with
  `issue runs` afterwards — the queue, not your intent, is the record.
- **The assignee fallback fires in any status, closed issues included.** Comments are
  conversational and follow-up questions on finished work are expected behaviour. A terminal
  status is not a safe place to write.
- **A run is not idle just because its status is not `queued`, `running` or `pending`.**
  `waiting_local_directory` is a live state: the run holds a place in the queue waiting for the
  target repository's local checkout, and several runs against the same repository serialise
  behind it. Measured on 20/09/2026, asking three reviews on one repository at once: one ran and
  two sat in `waiting_local_directory` until it finished. A liveness check written as an
  allow-list of busy states reports them as idle — and "no run is alive" is exactly the
  precondition for merging. Decide liveness by a **deny-list of terminal states**
  (`completed`, `failed`, `cancelled`, …) and treat anything unrecognised as alive: an unknown
  status is far more likely to be a new busy state than a new finished one.
- It is skipped when the assignee has no runtime, is archived, you cannot invoke it, or it
  already holds a pending run on that issue — consecutive comments coalesce into the waiting run
  rather than starting a second one.
- `issue comment add` has **no `--no-start`**. That flag exists on `issue status`, `issue assign`
  and `issue update`, and nowhere else. Anything claiming otherwise — including a confident
  answer from a search engine — is wrong; `--help` settles it in one second.

So the recipe for commenting on an agent-assigned issue without starting a run is a `/note`
prefix, not an unassign-comment-reassign dance. The dance works, but it mutates ownership for
the duration and is not needed.

## 6. Platform limits worth knowing before you promise something

- **Workspace isolation is real.** An agent running in one workspace cannot read another; only
  a human profile's CLI sees more than one. Cross-workspace search, dependencies and any
  portfolio view exist *only* through that CLI. When writing anything that governs agents, ask
  whether it assumes an agent can see a neighbouring workspace — if it does, that is a defect.
- **Agents cannot produce artifacts.** In an agent task the artifact tool is disabled and the
  refusal is explicit: `Artifact is disabled for this session, in subagents as well as here`.
  Delegating to a subagent does not work around it. Attach a file to a comment instead.
- **There is no MCP surface on the CLI** — but `agent update` takes `--mcp-config`,
  `--mcp-config-stdin` and `--mcp-config-file`, so agents *consume* MCP servers. The useful
  question is which servers your agents should have, not how to wrap the CLI in one. Pass that
  config by stdin or file: on the command line it lands in shell history and `ps`.
- `agent create --description` caps at 255 characters, and `--instructions` takes a string, not
  a path.
- Scheduled autopilots take a full cron expression and an IANA timezone
  (`autopilot trigger-add --kind schedule --cron … --timezone …`), and `autopilot create` takes
  `--subscriber`. `trigger-add --help` documents the `--timezone` default as UTC (v0.6.1,
  03/10/2026), so a cron written as the hour a person reads it lands hours off unless you pass
  the zone that person lives by: `--cron '0 9 * * 1' --timezone America/Sao_Paulo` for 09:00 on
  Mondays in Brasília. Sub-hourly expressions are writable; whether the server honours a given
  granularity is a test, not a promise.

## 7. When a repository governs the board

A team running Multica seriously keeps its agent instructions, workspace skills, workspace
context and project descriptions **versioned in a repository** and pushes them to the server
through the CLI. If `MULTICA_PLAYBOOK` is set, or the working tree looks like such a repo, that
repository outranks this skill and the reference on everything it declares.

**Read before acting, in this order:** the repo's agent-context file (`CLAUDE.md` / `AGENTS.md`)
for the rules that bind you; the root `README` for what each directory is and which of them
deploy; the per-workspace manifest for ids; and the scripts directory for the drift check and
the deploy tool.

The constraints such a repo almost always encodes — assume them until its own text says
otherwise:

1. **Editing is not deploying.** A file in that repo is operational *text*; the live system
   changes only when `agent update`, `skill update`, `workspace update`, `project update` or
   `autopilot update` runs. A commit changes nothing on the server. Saying "the agent now does
   X" because the file says X, with no deployment, is a false statement about the system.
2. **Deployment is a human act.** Never run those five commands on your own. Propose the diff,
   name the file, and stop. If the repo ships a deploy script, its dry-run is yours to use and
   its apply mode is not.
3. **Ids come from the manifest, never from memory or from a listing you skimmed.** The
   manifest is generated from the server and diffable; that is the point of it. Read it by
   the key it actually uses: agents and skills are keyed by `name:`, projects and autopilots
   by **`title:`** — a `grep 'name: <project>'` finds nothing and says so, which is the good
   case; the bad case is reaching for a listing instead, or for memory.
4. **Measure drift before you claim state.** If the repo ships a drift check, run it and read
   its exit code as state, not as failure — "differs" is the normal condition before a
   deployment.
5. **A committed-but-undeployed change is tracked work, not a paragraph.** Register it wherever
   that repo says pending work lives — a board item, not a heading in a versioned file, which
   is how status silently goes stale.
6. **Text that governs other agents is not yours to change unilaterally.** Behavioural rules,
   status contracts, backlog policy and review thresholds are decisions of whoever owns the
   system. Propose in diff; a taken decision gets recorded where that repo records decisions.
7. **No credentials in any of that text.** Instructions are stored server-side and passed
   through process arguments.
8. **Shared text must not hardcode one workspace's ids.** A registry id from workspace A
   deployed into workspace B points at nothing, and the failure is silent. Render it from the
   manifest, or write the sentence without the id.

Before writing anything into such a repo, ask yourself the two questions it exists to enforce:
does this change behaviour on the server (then it needs a deployment, tracked), and does it
assume an agent can see a workspace it cannot?

## 8. Conduct on the board

The reference covers the mechanics of side effects. These are the habits around them:

- Scoping is a human gate. Promoting an item out of the unscoped column is where a person's
  decision is cheap and changes the outcome; leave it to them, and do not comment on an
  unscoped item — that comment is written to nobody.
- Acts performed with a human's profile are indistinguishable from that human in
  `issue timeline`. When a session acts, leave a dated note saying so, with the hour in the zone
  that person reads, the zone written out, and UTC beside it so the note can be matched against
  the API's stamps, which come in UTC: `18:41 BRT (21:41Z)`, not `18:41` and not `21:41Z` alone.
  When the UTC falls on another calendar day than the local hour, it carries its date, so the
  note is not matched against the wrong day: `22:59 BRT (04/10 01:59Z)`. The date is
  day/month, as a Brazilian reader writes it; a reader used to month/day (the US) would take
  `04/10` for 10 April. An hour with no zone cannot be placed against those stamps.
- Never create a registry object — agent, skill, project, autopilot — casually. It will appear
  in no manifest and no drift check will see it.
- **A write to the board never shares a command chain with a step that can fail.** Verify
  first — the id resolves, the file exists, the status is what you expect — and then write,
  as a command of its own. `|| true` on a probe is fine; `|| true` on the write, or a write
  that runs because the probe before it "succeeded" with garbage, is how a note lands on the
  wrong issue. In zsh, `set -e` does not cover a command substitution nor a Python heredoc:
  guard those with an explicit `|| exit 1`.
- **Before merging a PR that a human session conducted, read `issue runs <ID>` and
  `issue timeline <ID>` on the issue it closes.** An agent run may be alive on the same PR —
  a review round nobody asked for, a conductor about to merge — and two conductors on one PR
  is how a merge lands under the human's login with no record of who decided it. On
  18/09/2026 a human session merged a PR while the conductor agent was still running review
  rounds on it. The stage barrier woke the conductor 2 s after the merge — by the platform's
  own mention in a `system` comment, not by anyone's verdict; the review verdict landed 52 s
  after the merge and woke it again; it opened two follow-up issues at 150 s and 158 s, from
  a verdict that was no longer its to act on
  (measured at the source on 19/09/2026: the PR's `mergedAt`, `issue comment list` on the
  two issues involved, the issues' `created_at`).
- **`/note` writes without waking anyone, and that is all it does: it addresses nothing to
  anyone.** A pending item, a follow-up or a correction that lives only in a `/note` is
  written to nobody — the same failure as a comment on an unscoped item, from the other
  side. Anything that must be done goes where it will be found: a checkbox with a `verify:`
  in the issue description, or an issue of its own.
- **A description write replaces the whole field, and nothing merges it.** `issue update
  --description-*` writes the entire description; the CLI has no compare-and-set (no
  `--if-revision` as of v0.5.3 — `revision` comes back on read and cannot be passed on write).
  Two writers that read, edit and write back erase each other in silence, with no conflict and
  an ordinary `activity` event in the `timeline`. Measured on 21/09/2026 on LAS-69: a session
  marked ten DoD boxes at 16:39:04Z and another added two `verify:` criteria at 17:04:45Z, with
  two more description writes in between; nothing was lost only because of the order. The cost
  grows with the rule above — the more pending work lives as checkboxes in descriptions, the
  more a lost write costs. Three habits close most of the window: **read immediately before
  writing** (never write back a read from earlier in the turn); **change only your
  substring** — exact replacement asserted to occur once, or an append — instead of
  re-emitting an edited copy; and **check the window after writing**, which takes one check for
  each half of it. A write landing *after* yours shows in the content: re-read and compare with
  what you wrote — content, not `updated_at`, ignoring trailing whitespace (on 21/09/2026 a
  trailing newline from `print()` was enough for a false alarm on the first write, which is how
  a check gets abandoned). A write landing *before* yours was erased by yours, so the re-read
  shows your text and only the `timeline` shows it: count the `description_updated` events
  **before reading the description** (`N`) and again after writing (`M`); exactly one new event,
  and that one with your own id as its `actor_id`, means yours alone. Your id is your profile's
  (`user profile get`), except inside an agent task: there the write carries the agent's id,
  `MULTICA_AGENT_ID`, while `user profile get` returns the member who owns the token (v0.5.3,
  24/09/2026: task events on LAS-140 and LAS-141; the CLI sends the variable as `X-Agent-Id`).
  Wait for that one: an event by someone else showing first is not it. A writer with your id
  does look like you — another session on the same profile, the person it belongs to editing in
  the app (see above; not measured: which id an app edit carries), another run of the same
  agent — and while yours is late it passes for yours. The order is the point — a write landing
  between a read and a later count enters `N` while the text in hand is already stale. Measured
  on 24/09/2026 (v0.5.2, on a throwaway issue): every description write logged a
  `description_updated`, even one identical to the stored text, so a write that changes nothing
  must not be sent at all. Two shortcuts
  fail. `revision` also moves on a comment, a reply, a title or status change and on writes the
  `timeline` does not show (47 of 100 `lass` issues had more revisions than visible events on
  24/09/2026), so a jump is not proof of a description write. And `--since` drops the whole
  second it is given (v0.5.3, 24/09/2026, LAS-147: the event at 2026-09-21T20:07:03Z is missing
  from `--since 2026-09-21T20:07:03Z` and present from `--since 2026-09-21T20:07:02Z`), while an
  issue's `updated_at` is, as a rule, the second of
  its last event (96 of 100 `lass` issues on 24/09/2026) — so `--since <updated_at>` is blind to
  the very write that matters; to search by hand, start one second earlier. An erased write has
  nothing to be restored from: the event keeps no text (`details` is empty) and the CLI has no
  history command. Do not write over it again; its author — the event's `actor_type` and
  `actor_id` — re-applies it, and to an agent that request is a mention, which starts a run
  (§5). When that `actor_id` is your own id, the event does not say which of those writers made
  it: ask whoever runs them, which the `timeline` cannot answer. `scripts/patch-description.py`
  in this skill does all of it: it exits 1 without writing when a substring does not occur
  exactly once, an insertion (a replacement whose new text contains the old) or the append is
  already there, or the edits change nothing — so a re-run after an exit 3 writes nothing if an
  edit survived; 2 on `--edits` that are not pairs of two strings, or an empty append; and 3
  when the re-read differs, there is not exactly one new event, or none by your id, printing the
  read's `updated_at`, `revision` before and after, each new event with its author (yours
  marked), and the command that lists them.
