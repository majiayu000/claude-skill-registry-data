---
name: relay
description: Generate and run a relay thread file in `relay-system/<date>/<slug>.md` — a turn-based, file-based review loop between two Claude Code agents (a Producer who builds, a Reviewer who critiques and proposes fixes the author applies) so a human stops copy-pasting output between two windows. Use this whenever the user wants to "set up a relay", run a "producer/reviewer" or "worker/reviewer" loop, have "two agents" review each other's work in a shared file, "hand off" between agents without pasting, or cut copy-paste and stray artifacts across AI sessions. Also use it to START a relay (scaffold the dated file) or to TAKE A TURN in an existing one (read the file, act only on your turn, append your block, flip the pointer). Trigger even if the user only describes two Claude windows shuttling text back and forth.
---

# Relay

Two agents, one file, no copy-paste.

A relay is a turn-based review loop carried entirely inside a single Markdown file that both agents can read and append. One agent **builds** (Producer), the other **reviews and proposes** (Reviewer). They never message each other — they read the file, take their turn, and flip a pointer. The human serializes turns by nudging the next window — or, with CLI-driven mode, a single Claude session calls `agy` or `codex` as a subprocess and the human's role collapses to zero. The file is the shared bus, the change-log, and the decision record all at once.

Three handoff modes, each a first-class option: **manual nudge** (portable, works with any tool), **hands-free poll** (all-Claude, two sessions), and **CLI-driven** (one session orchestrates, calls agy/Codex as subprocess). Manual is the default — the other two are opt-in.

This skill does two things: **start** a relay (scaffold the dated file from the template in the Appendix) and **take a turn** in an existing one. The **Producer always starts it** — the same step that creates the dated folder and file also writes turn 1. The Reviewer never creates the file; it only reads and appends.

**Honest caveat — independence is only as good as the second agent.** Two Claude sessions share a model and much of the same repo context, so they share blind spots: a same-model relay catches what a fresh pass with fresh framing catches, not what a truly independent reviewer would. For genuinely independent eyes, run a *different* model in the Reviewer window (e.g. Codex, or a different Claude tier). The file-based protocol is model-agnostic by design — any agent that can read and append the file can take a turn.

**Composes with `phase-qa` for plan/spec-doc reviews.** When the artifact is a planning, spec, or roadmap doc (not code), build the Reviewer's checklist with the `phase-qa` skill first, and seed the relay's Definition of Done from it. Critically, give *completeness* its own dedicated turn with an explicit **omission-diff** instruction — "list every claim in the source doc that has no equivalent in the target; report the gap, don't summarize." A reviewer asked the easy direction (find overclaims / errors) will satisfice and miss silent *drops* — the classic failure when one doc is a compression or merge of another. The relay is the transport; `phase-qa` owns the rubric — keep them composed, not coupled.

## When to use

- The user says "set up a relay", "start a relay", "run a producer/reviewer loop", "two-agent review", "have one agent review the other".
- The user is shuttling output between two Claude windows by hand and wants to stop.
- A piece of work needs an independent review pass and the user has a second Claude Code session available in the same repo.
- The user asks to take the next turn / continue a relay that already exists.

## The loop

```
Producer (build + request)  →  Reviewer (review + propose + verdict)
        ↑                                          │
        └──────  Producer (decide + implement)  ←──┘
```

One round = a Producer turn + a Reviewer turn. The relay ends when the Reviewer's verdict is **Approved**, or escalates to the human at the max round if it is still not Approved.

## File location

`relay-system/<YYYY-MM-DD>/<slug>.md`

- One folder per day; multiple relays per day live side by side, each with its own slug.
- Slug = short, lowercase, hyphenated topic — derive it from the artifact filename when obvious (`detect_abuse.py` → `detect-abuse`), otherwise ask the user for a 2–4 word topic.
- If today's target path already exists, derive a unique sibling (`<slug>-2`, `<slug>-3`, ...) instead of overwriting the earlier relay.
- `relay-system/` is local working scratch, not the artifact. Whether to track or `.gitignore` it is the operator's call: gitignore it to keep history quiet (recommended for public repos), or track it in a private repo if you want the relay thread in history. Either way, both agents always read it on disk in the same worktree — only the **artifact** must stay git-tracked, since ground rule 8's `git diff` handoff runs against the artifact, not this log.

---

## Mode 1 — Start a relay (Producer only)

1. Gather three things (pull from context first; ask only what's missing): the **artifact under review** (a local path — or a PR, in which case **check the branch out locally first**, since the direct-edit and `git diff` mechanics assume the artifact is in the shared working tree), a one-line **Definition of Done**, and a **slug**.
2. Get today's date and create `relay-system/<date>/` if it doesn't exist (this also creates `relay-system/` on first ever use).
3. If `relay-system/<date>/<slug>.md` already exists, pick the next unused `-2`, `-3`, ... suffix instead of overwriting it.
4. Write `relay-system/<date>/<slug>.md` using the template in the **Appendix** below. Fill `<TITLE>`, the Setup fields, and `Started`. Leave `NEXT: Producer`, `STATUS: Open`, `ROUND: 1 / 5`.
5. Take Round 1 immediately (Mode 2) — you're the Producer and you have the request. Folder, file, and turn 1 are all one step.
6. Commit, then tell the user the path and to carry it to window B with: *"take the Reviewer turn on `<path>`."*

If the user asks to take a turn but the file doesn't exist yet, you're in this mode — scaffold first.

## Mode 2 — Take a turn

1. **Read the whole file.** Setup, ground rules, and every prior turn.
2. **Check it's your turn.** The user tells you your role ("act as the Reviewer"). If `NEXT` ≠ your role, reply `Not my turn — NEXT is <role>.` and stop. Do not write anything.
3. **Do your role's work:**
   - **Producer:** build or update the artifact, then write your block. On later rounds, decide every Reviewer proposal *with the operator* — implement, modify, or decline — and log each disposition before adding new work.
   - **Reviewer:** review against the Definition of Done. **Do not edit the artifact** — it isn't yours to change. Write each issue as a graded finding, attaching a concrete suggested fix wherever you can (so the Producer can apply it in one step). Set a verdict.
4. **Append your block** at the bottom, directly above the marker line. Never edit earlier turns.
5. **Update the header:** flip `NEXT`; bump `ROUND` when a Producer opens a new cycle; set `STATUS` (`Approved` ends the relay; `Escalated` if the max `ROUND` ends without `Approved`).
6. **Commit your turn:** `relay(<slug>): <role> r<N>`, then fill the hash into your block's `Commit:` line. This is what lets the operator `git diff` exactly which proposals the Producer implemented — the safety net behind every applied change. A **Reviewer turn never changes the artifact**: if the relay log is gitignored (the common case) it writes `Commit: none (comments only)`; if the log is *tracked*, the Reviewer still commits the log (rule 9 — no uncommitted state across a handoff) and records that hash. The Producer's turn carries the actual artifact diff — or `Commit: none (comments only)` if it too touched no tracked files.
7. **Report to the human** using the format in **Reporting to the human** below — TLDR first, sorted findings last, then the hand-off. The human nudges; they never paste.

### Turn block formats

Append exactly one of these per turn.

**Reviewer:**
```
### Round N · Reviewer · <timestamp>
**Verdict:** Approved | Changes requested | Blocked
**Basis:** behaviorally proven (<what I ran / observed>) | textual only (read, not run) | N/A — non-executable artifact
**Prior fixes:** (when re-reviewing) <ref> — behaviorally proven | textually fixed | unverified
**Findings & proposals:** (I propose; I do not edit the artifact)
- [Blocker] <finding @ file:line> — Proposed fix: <concrete suggested edit, or "author's call">
- [Should] <finding> — Proposed fix: <…>
- [Nit] <finding> — Proposed fix: <…>
- [Pass] <thing I checked and found sound — evidence it's checked, not assumed>
  (or "none — approved as-is")
**Answers:** (respond to the Producer's "Re-review this" / open questions, point by point — or "none asked")
- <their question> → <direct answer>
**Commit:** <log hash if this log is tracked, else "none (comments only)"> — the Reviewer never edits the artifact
```

**Basis is mandatory on every verdict.** An `Approved` can never silently mean "I read the diff and it looked fine." If correctness rides on runtime behavior and nothing was run, the strongest honest verdict is `textual only` — a flagged, weaker approval the operator sees. `Prior fixes:` is where the Reviewer says whether the Producer's claimed fixes are `textually fixed` (the code now reads correctly) or `behaviorally proven` (confirmed to actually run / pass) — the distinction that stops doc approval from outrunning implementation reality.

**Verdict semantics.** `Changes requested` and `Blocked` keep the relay open for a Producer turn to dispose of the proposals; `Approved` **closes** it. So a Reviewer that wants its proposals actioned *in-thread* must set `Changes requested`, not `Approved` — any `[Nit]` left on an `Approved` verdict is the author's discretion, handled out-of-band after the relay closes.

**Producer (rounds 2+):**
```
### Round N · Producer · <timestamp>
**Decisions on proposals:** (operator-approved)
- [Blocker] <quote/ref> — Implemented → <what I changed @ file:line> · Proof: <cmd→result | "textual only" | "none"> | Modified → <what & why> · Proof: <…> | Declined → <one-line rationale>
- [Should] <quote/ref> — Implemented | Modified | Declined + why · Proof: <…>
**Did:** <further changes>
**Verification:** ran <cmd> → <result> · skipped <X> (why) · impossible <Y> (why) — or "N/A — non-executable artifact"
**Re-review this:** <what changed / where to look>
**Commit:** <hash or "none (comments only)">
```

(The Round 1 Producer block ships pre-stubbed in the template.)

**The Producer's `Verification:` line is mandatory and one line.** `skipped` and `impossible` are first-class — "tests pass" with no command is theater, but "skipped the race test (no harness yet)" is honest and reviewable, and an omitted line is a visible blank. Per-finding `Proof:` says how each implemented fix was confirmed. The contract scales to the artifact: a pure doc or design answers `N/A — non-executable artifact` in one token and the overhead disappears exactly where the relay already excels.

## Guardrails

- **Never act out of turn**, and never edit a prior turn. The header pointer and the marker are load-bearing — respect them. (The one exception: immediately after committing, you may fill in your *own* just-written turn's `Commit:` line with the hash. Nothing else in a prior block is ever touched.)
- **Only one window acts at a time — the pointer is honor-system, not a lock.** Both windows share one working tree. The human serializes by nudging one window at a time; never start a turn while the other window may still be mid-edit, or the shared file and tree can be clobbered.
- **Clean tree at every handoff.** Before you flip `NEXT`, commit (or stash) all your changes — never hand off with uncommitted edits sitting in the working tree. A dirty tree means the next agent reads your half-finished state as if it were the artifact.
- **Smallest change that satisfies the finding.** A proposal — and the fix that implements it — is the narrowest change that resolves the finding; don't rewrite the artifact wholesale.
- **Only the author writes.** The Reviewer never edits the artifact — it proposes, and the Producer (the original author), with the operator, implements. Every change flows through one consistent hand, and the independent check stays independent: the reviewer never grades its own edits.
- **No proposal left undecided.** On its turn the Producer logs a disposition — Implemented / Modified / Declined (+ reason) — for every proposal before adding new work. A Declined Blocker is contested, not skipped (see below).
- **Verify the finding before disposing of it.** The Producer independently checks each proposal against the source before implementing — a finding can be wrong, or worse than flagged. Real relays open the turn with "verified every claim against the repo before deciding"; that check is what makes a disposition trustworthy, not just polite.
- **No ignored Blockers.** The Producer resolves or explicitly contests each one — never skips it.
- **Evidence contract — state your proof every turn.** The Producer logs `Verification:` (what it ran / skipped / couldn't run); the Reviewer logs a verdict `Basis:` — `behaviorally proven` or `textual only` — and classes prior fixes `textually fixed` vs `behaviorally proven`. One line each, mandatory. It keeps a clean `Approved` from outrunning what was actually executed, and deflates to `N/A — non-executable artifact` for pure docs.
- **Reconcile every "Implemented" against the artifact before you hand off.** A disposition is a *claim* until the file proves it. Before flipping `NEXT`, the Producer re-reads the artifact (or `git show <its own commit>`) and confirms each `Implemented → @ file:line` actually resolves to the changed line — a claimed edit that silently didn't land is caught here, one step before it reaches the Reviewer. Cite the line **as it appears in that turn's commit diff**, so an `Implemented` with no matching hunk is false on its face.
- **The closing `Approved` is verified against the file, never the log.** Before the Reviewer sets `Approved` it re-reads the **artifact itself** — not the relay thread, not the Producer's `Decisions on proposals:` block — and confirms every prior `Implemented` finding is actually present and complete. Any claimed-implemented fix that is missing or partial flips the verdict to `Changes requested` with a `[Blocker] claimed-implemented-but-absent @ file:line`. For a **non-executable artifact (a design-spec, plan, or roadmap doc)** this file-reconciliation is the *only* backstop the relay has — a `textual only` basis is fine and expected, but the read must be against the artifact, not against claims about it.
- **Don't loop forever.** If the same Blocker is contested twice, escalate to the human rather than ping-pong. Honor the max round.
- **Assume nothing is shared.** The two agents have separate memory; if a decision matters, it goes in the file.

## Hands-free handoff (opt-in, all-Claude only)

By default the human serializes the relay with a one-line "your turn" nudge — and that nudge is the **lock**: it guarantees the previous turn is committed before the next begins. You can automate the nudge away **only when both windows are Claude Code sessions**, by replacing it with a *guarded poll* — each window watches the file and takes its turn the moment it's genuinely ready, never on a clock.

**Why not a fixed timer.** A "fire in N minutes" timer swaps a readiness *condition* for a guess: too short and the next turn fires on a half-finished, uncommitted tree (the clobber rule 9 exists to prevent); too long and you waited for nothing. The trigger you want is "it's my turn and the tree is clean," not "N minutes elapsed."

**The guard (non-negotiable).** A polling window takes its turn only when **both** hold:
1. `NEXT` names its role, **and**
2. the working tree is clean — the other window has already committed (`git status --porcelain` shows nothing for the artifact).

If either is false it does nothing and waits for the next tick. The *condition* is now the lock, so "one window at a time" still holds — and the order is unchanged: do the work → commit → flip `NEXT`, so a poller never sees `NEXT` flip before the commit lands.

**Setup.** Opt in at relay start by running a guarded `/loop` in each Claude window:
```
# Reviewer window
/loop 60s take the Reviewer turn on relay-system/<date>/<slug>.md ONLY if NEXT is Reviewer and the tree is clean; otherwise do nothing and wait
# Producer window
/loop 60s take the Producer turn on relay-system/<date>/<slug>.md ONLY if NEXT is Producer and the tree is clean; otherwise do nothing and wait
```
Record the mode in the file so each window knows it's live — set Setup's `Handoff:` to `hands-free poll (all-Claude)`. A short interval (≈60s) keeps the prompt cache warm; the other window's edits aren't harness-tracked, so polling is the correct way to notice them.

**Stop conditions.** A polling window stops when `STATUS` is `Approved` or `Escalated`, or after a bounded number of idle ticks with no change — then it escalates to the human rather than spinning forever. Honor the max `ROUND` exactly as in manual mode.

**Stays manual when** you have no CLI runner for the Reviewer tool, or want the human as an explicit checkpoint between turns. For non-Claude tools that have a `-p` / `--print` mode (agy, Codex), see **CLI-driven handoff** below — that section covers fully automated single-session relays with no second window needed.

### Self-closing loops (avoid stray cron housekeeping)

A `/loop`-created cron job is **per-session, in-memory, and auto-expires after 7 days** — far too long for a short review relay, and easy to forget. Make each loop **self-closing** so no one has to remember to clean it up:

- **Bake a deadline / tick-budget into the loop**, not just a stop-on-`Approved`. The loop should end on the *first* of: `STATUS` terminal (`Approved`/`Closed`/`Escalated`), **a wall-clock deadline (e.g. 30 min)**, or N idle ticks. A deadline also kills the "idles forever because the peer window died" failure mode.
- **The loop deletes its own job on stop.** On a stop decision the polling turn runs `CronList` → finds its job (match it by the relay-file path in the prompt, since the turn doesn't know its own ID at creation) → `CronDelete`s it, then ends. Without this the cron keeps firing (harmlessly idling) until the 7-day expiry or the session closes.
- **If a tick-driven runner is involved** (a polling guard, if one is wired up), give it the deadline so it emits the stop decision itself (`--deadline <epoch>` / `--max-idle-ticks N`); then the one stop path (`DECISION: stop → CronDelete self`) covers Approved, expiry, and stall uniformly.

**Cross-session caveat (load-bearing).** Cron jobs live in the session that created them. **You cannot stop another window's loop from yours** — `CronList`/`CronDelete` only see the current session. So every window's loop must self-close (deadline + self-delete), or be stopped *in its own window*; there is no central "kill all loops." This is why self-expiry matters more here than for a single-window loop.

**Use cases:** short hands-free review relays (set a 30-min deadline — most relays finish in 2–4 rounds well under that); unattended overnight polls (longer deadline, but still bounded); any multi-window all-Claude relay where several loops run at once and manual cleanup of each would be error-prone.

## CLI-driven handoff (single-session, agy / Codex)

A single Claude Code session can drive both roles — it takes the Producer turn itself, then calls `agy -p` or `codex` as a subprocess for the Reviewer turn, parses the output, and appends it to the relay file. No second window, no human nudge between rounds.

**When to use.** You have `agy` or `codex` installed, want fully automated review from one session, and trust the output enough to proceed without a human checkpoint between turns. Manual is still the default — this is opt-in. Set `Handoff: cli-driven (agy)` or `cli-driven (codex)` in Setup so any agent reading the file knows which tool is driving the Reviewer.

**How it works.**

1. Producer takes its turn and writes its block normally.
2. Producer reads the relay file + artifact and calls the CLI tool, passing both as the prompt:
   ```bash
   RELAY=$(cat relay-system/<date>/<slug>.md)
   ARTIFACT=$(cat <artifact-path>)
   RESULT=$(agy -p "You are the REVIEWER in a relay review. Read the relay thread and artifact, then take your Reviewer turn. Output ONLY the block to append (starting with '### Round N · Reviewer …'), nothing else.

   === RELAY THREAD ===
   $RELAY

   === ARTIFACT ===
   $ARTIFACT")
   ```
3. Assert non-empty output (see gotchas below), then append the result directly above the `<!-- ↓↓↓ NEXT TURN -->` marker.
4. Update `NEXT` and `STATUS` in the header.
5. Loop until `STATUS: Approved` or max round.

The embedded **▶ TAKE YOUR TURN** block in the relay file is the Reviewer's full instruction set — pass the file verbatim and the tool knows what to do without extra scaffolding.

### agy-specific gotchas (load-bearing)

1. **Silent failure under Claude Code's Bash sandbox.** `agy -p` exits 0 with *empty* output when its backend network is blocked — it does NOT error. A sandboxed call reads as a successful empty turn. Always run agy with `dangerouslyDisableSandbox: true` **and** assert non-empty output before appending:
   ```bash
   if [ -z "$RESULT" ]; then echo "ERROR: agy empty — sandbox or auth issue"; exit 1; fi
   ```
2. **Timeout is a Go duration string, not seconds.** Use `--print-timeout 2m`, not `--print-timeout 120`.
3. **No JSON or token output.** `agy` returns plain text only — no usage numbers, no structured output flag. The relay is cost-blind when agy is the Reviewer.

### Codex-specific gotchas

1. **Needs sandbox disabled.** Codex CLI requires keychain access and `chatgpt.com` network — both blocked under Claude Code's sandbox. Run with `dangerouslyDisableSandbox: true`.
2. **Auth mode.** When using `auth_mode=chatgpt`, turns are billed via the ChatGPT subscription, not API credits.

## Reporting to the human (chat reply, not the file)

The relay **log** (the turn block you appended) and your **chat reply** are two different documents with two different jobs — the log is the durable record, the chat reply is what the human actually reads to decide what to do next. Keep them separate, and shape the chat reply like this:

1. **TLDR — one line, at the very top.** Round, role, verdict/status, and what happens next: *"Round 2 Reviewer done — Changes requested, 1 Blocker. Producer's turn next."* This **is** the hand-off nudge, just promoted to the first line instead of the last — the human should never have to read past line one to know the result.
2. **One short framing sentence**, in your own voice — *"Reviewing `evidence.py` against the DoD…"* — only if it adds something the TLDR didn't already say. Skip it when it would just restate the TLDR.
3. **If there are findings to report, close with them sorted by grade** — `[Blocker]` → `[Should]` → `[Nit]` → `[Pass]`, in that fixed order, never chronologically or interleaved with prose. One line each, with a `file:line` and the proposed fix inline:
   ```
   [Blocker] auth.py:42 — token isn't validated before use → Proposed fix: check `token.valid` before the call.
   [Should] evidence.py:88 — magic number, extract a constant.
   ```
4. **Skip step 3 entirely** for 0–2 trivial findings, or a clean `Approved` with nothing to report — plain prose is fine. Don't force a sorted list where there's nothing to sort (same threshold `linear` uses for its own numbered-step format).

This doesn't change what goes *in* the log — the log still uses the turn block formats above, verdict semantics are unchanged, and the Reviewer's `Approved`/`Changes requested`/`Blocked` distinction still governs whether the relay is open or closed. This section only governs how you *talk about* that log to the human.

## What success looks like

The human's entire role collapses to two actions: *"start a relay"* and *"your turn."* No text shuttled between windows, no extra notes outside the relay thread, no lost context — just one dated, git-diffable Markdown file holding the full review thread and every decision, ending cleanly on **Approved** or a clear escalation.

---

## Appendix — relay thread template

Write this verbatim to `relay-system/<date>/<slug>.md` when starting a relay, filling the `<…>` fields. Newest turns append at the **bottom**, above the marker; the header and ground rules stay pinned at the top.

The **▶ TAKE YOUR TURN** block is embedded in the template so a non-Claude agent (Codex, Gemini) that never loaded this skill can act correctly **from the file alone** — the operator's whole job stays a one-line nudge ("take your turn on `<file>`"), never a pasted wall of instructions. This base skill stays **partially manual** (a human nudges each turn); automating the nudge itself is the job of the `xyz`/relay-automation add-on, not this portable skill.

```markdown
# RELAY · <TITLE>
<!--
  Single source of truth for this two-agent relay.
  Read this ENTIRE file before doing anything. Act only on your turn.
-->

NEXT: Producer
STATUS: Open
ROUND: 1 / 5

## ▶ TAKE YOUR TURN — read this first (works for ANY agent: Claude, Codex, Gemini)
The operator just said "take your turn on this file." Everything you need is **in this file** — don't wait for pasted instructions.
1. **Read this whole file** (header, Setup, Ground rules, every turn in the Log).
2. **Check it's your turn:** `NEXT` (top) names the role to act. Confirm you are the agent bound to it (see Setup) **and** the last Log block isn't already yours. If not → STOP and reply "wrong window — nudge the <other> window."
3. **Do your role's work** on the artifact named in Setup (read the real files / the latest `git show <last commit>` diff; cite `file:line`):
   - **Reviewer:** review vs the Definition of Done → graded findings (`[Blocker]`/`[Should]`/`[Nit]`/`[Pass]`), each with a concrete proposed fix → set a **Verdict** (Approved | Changes requested | Blocked). Do **not** edit the artifact; you only append findings here. **Before you set `Approved`, re-read the artifact file itself** (not this log) and confirm every prior `Implemented` fix is actually present and complete — any that is missing or partial → set `Changes requested` with a `[Blocker] claimed-implemented-but-absent @ file:line` instead. For a doc artifact this file check is the only backstop there is. **A finding that asks for a behaviour change is a generalization unless you can paste the concrete input — a row, a value, a `file:line` — that fails under the current code** (GH-681). Every `[Blocker]` or `[Should]` requesting a behaviour change MUST carry `Observed input:`, `Affected scope:` and `Falsifier:` lines; a `[Blocker]` must cite an observed failure. The Producer may disposition a request lacking these as `Declined — unproven generalization`.
   - **Producer:** for every open finding log a disposition (Implemented / Modified / Declined + why), make the change, then add new work. **Before you flip `NEXT`, re-read the artifact and confirm each `Implemented → @ file:line` actually landed in the file** — cite the line as it appears in your commit diff. A claim you can't point to in the file is not done.
4. **Append ONE block** at the very bottom, directly **above** the marker line (`<!-- ↓↓↓ NEXT TURN ... -->`). Never edit earlier turns. Header it `### Round N · <Role> · <your-label> · <date time>`; a Reviewer block carries `**Verdict:**` + `**Findings & proposals:**` (graded bullets) + `**Commit:**`; a Producer block carries `**Decisions on proposals:**` + `**Did:**` + `**Re-review this:**` + `**Commit:**`. (Need the exact shape? Mirror the most recent block of the other role above.)
5. **Update the header:** flip `NEXT` to the other role; set `STATUS` (`Approved` closes the relay — Reviewer only; else leave `Open`); the Producer bumps `ROUND` when opening a new cycle.
6. **Commit only the files you touched** (artifact + this log): `git commit -m "relay(<slug>): <your-label> r<N>"`, then put the short hash in your block's `Commit:` line and `git commit --amend --no-edit`. Push if the team shares a remote.
7. **Stop.** Tell the operator your one-line result (e.g. "Changes requested, 1 Blocker — Producer's turn").

## Setup
- Artifact under review: <PATH or PR URL>
- Definition of Done: <ONE LINE — the bar the Reviewer checks against>
- Producer: <name/agent>   ·   Reviewer: <name/agent>
- Handoff: manual nudge   <!-- options: "manual nudge" · "hands-free poll (all-Claude)" · "cli-driven (agy)" · "cli-driven (codex)" — see skill -->
- Started: <YYYY-MM-DD>

## Ground rules
1. This file is the single source of truth. If it isn't written here, assume the other agent doesn't know it. The two agents may be different tools (e.g. Claude and Codex) and never share memory.
2. Read the whole file. Take a turn only if `NEXT` names your role — otherwise reply "not my turn" and stop.
3. One turn = one block appended at the very bottom, above the marker. Never edit earlier turns. Then update `NEXT`, `STATUS`, `ROUND` at the top. (Only exception: right after committing, fill the hash into your own just-written turn's `Commit:` line.)
4. Stay tight. Requests and findings are bullets, not essays.
5. **The Reviewer never edits the artifact.** It proposes graded findings, each with a concrete suggested fix where possible. The Producer (the original author), with the operator, decides each proposal and implements the approved ones — logging a disposition (Implemented / Modified / Declined + reason) for every one.
6. Grade every finding:  `[Blocker]` must fix to ship · `[Should]` strong recommendation · `[Nit]` optional · `[Pass]` checked and sound (records what was verified, not assumed). Answer the Producer's "Re-review this" questions in an `Answers:` block.
7. The Reviewer posts a Verdict every turn. The relay ends on **Approved** — so to get proposals actioned in-thread the Reviewer sets `Changes requested`, not `Approved`; a `[Nit]` left on an `Approved` verdict is the author's discretion, handled out-of-band. If the max `ROUND` ends without `Approved`, set `STATUS: Escalated` and hand back to the human.
8. End your turn by committing it: `relay(<slug>): <role> r<N>`, then fill the hash into your `Commit:` line — so the other agent can `git diff` exactly what changed. If your turn touched no tracked files (comments-only, or this log is gitignored), write `Commit: none (comments only)`.
9. **One window at a time, clean tree at every handoff.** Both agents share one working tree; the `NEXT` pointer is honor-system, not a lock. Never start a turn while the other window may still be editing, and never flip `NEXT` with uncommitted changes left in the tree — commit or stash first, so the next agent never inherits half-finished state.
10. **Evidence contract — state your proof every turn.** The Producer logs a one-line `Verification:` (what it ran / skipped / couldn't run); the Reviewer logs a verdict `Basis:` — `behaviorally proven` (ran/observed) or `textual only` (read, not run) — and classes any prior fix `textually fixed` vs `behaviorally proven`. An `Approved` can't silently mean "looked fine on read": if correctness rides on runtime behavior and nothing ran, `textual only` is the strongest honest verdict. Scales to the artifact — a pure doc answers `N/A — non-executable artifact`.
11. **Reconcile claims against the file, not this log.** A disposition is a claim until the artifact proves it. The Producer, before flipping `NEXT`, re-reads the artifact (or `git show <its commit>`) and confirms each `Implemented → @ file:line` actually landed — citing the line as it appears in the commit diff. The Reviewer, before it may set `Approved`, re-reads the **artifact itself** and confirms every `Implemented` finding is present and complete; any missing or partial one flips the verdict to `Changes requested` with a `[Blocker] claimed-implemented-but-absent @ file:line`. For a non-executable artifact (design-spec / plan doc) this file check is the only backstop — so the closing approval is never granted on the log's word alone.

## Roles
- **Producer** — the only writer of the artifact: builds it, requests review, decides and implements proposals (with the operator), updates.
- **Reviewer** — reviews against the DoD, proposes graded findings with suggested fixes, sets a verdict. Never edits the artifact.

---
## Log

### Round 1 · Producer · <YYYY-MM-DD HH:MM TZ>
**Did:** <what you built/changed — 1–3 bullets>
**Review this:** <specific focus areas / what to scrutinize>
**Verification:** ran <cmd> → <result> · skipped <X> (why) · impossible <Y> (why) — or "N/A — non-executable artifact"
**Open questions:** <or "none">
**Commit:** <hash or "none (comments only)">

<!-- ↓↓↓  NEXT TURN GOES ABOVE THIS LINE — keep this marker last  ↓↓↓ -->
```
