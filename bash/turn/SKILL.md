---
name: turn
description: >
  ACE's turn-of-work entry point. Use when a human says "do a turn" or "check your inbox": process
  what has come in, for runs and program projects alike. Wraps /ace:run pipeline runs; does not
  replace them.
---

# Turn — ACE (stub over the fleet-canonical core)

The turn procedure is fleet-canonical so every agent runs the same, current process, and
improvements ship once (a canopy PR) instead of N backports.

1. **Resolve the installed canopy plugin and check freshness:**
   ```bash
   CANOPY=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['canopy@canopy'][0]['installPath'])")
   bash "$CANOPY/scripts/canopy-update-check.sh"
   ```
   `UPGRADE_AVAILABLE <old> <new>` → tell the human and run `/canopy:update` BEFORE following a
   stale core.
2. **Read `$CANOPY/agent-core/turn.md`** (Read tool, absolute path) and **follow it exactly**,
   bound to the Identity below. Where it says `<slug>`, use this Identity.

## Identity
- Name: **ACE** · slug: `ace` · mailbox: `ace@dimagi-ai.com`
- Email shim: `bin/ace-email` · board: `/agents/ace`

## ACE-local notes (the ONLY hand-edited section — fleet-process changes go to canopy)
- **Entry points:** the turn is the counterpart-facing entry point, for run threads **and** for
  program-project work: questions about, and changes to, live programs ACE supports
  (`skills/partner-on-connect-program`). **`/ace:run` remains the entry point for new builds**;
  a turn does not replace it. A turn may resume a paused run at the instruction of an
  **act**-tier sender, executing the same procedure the pause point defines. Design + counterpart model:
  `docs/superpowers/specs/2026-07-01-agent-operating-model-adoption.md`.
- **EVERY raw `gog` or `canopy email` call goes through `bin/ace-env` — no exceptions**
  (dimagi-internal/ace#2844). gog keeps its OAuth client secret in a FILE keyring whose password
  lives in the plugin-data `.env` and in no shell profile. A session a canopy RUNNER spawns never
  sees it, so an unwrapped call dies with `no TTY available for keyring file backend password
  prompt` and ACE's whole email surface — read AND send — is dead for that turn. `bin/ace-env`
  loads just that pair and execs the command:
  `bin/ace-env gog gmail search …`, `bin/ace-env canopy email read --repo . <threadId>`,
  `bin/ace-env canopy email dangling --repo .`. ACE's own shims (`bin/ace-email`,
  `bin/ace-mark-read`) already load it in-process, so those need no prefix.
  **Do NOT "fix" this with `launchctl setenv`** (canopy email preflight forbids it — it hands the
  password to every process of this user) **or with the runner's LaunchAgent plist**: that reaches
  the runner DAEMON only, never the Emdash-spawned session a turn actually runs in. Measured
  2026-10-12 — plist correctly populated, daemon restarted, `pgrep -P <runner-pid>` zero children,
  session still dead. The daemon's own probe keeps passing, which is why canopy-web's
  `mailboxes_readable` can advertise the mailbox as readable while no turn can read it.
- **Preflight (core Step 1) specifics:** `bin/ace-doctor --installed` — read the `[Auth liveness]`
  block. **Start it in the BACKGROUND and gate the turn on the inbox read instead — the doctor is
  slow AND silent.** It runs ~3-4 minutes (measured 3m39s, 2026-09-01) because it makes live HTTP
  probes per MCP and walks Drive's opp layout, and it pipes through `tee`, so a foreground run
  emits NOTHING until it exits — it just blows the harness 120s Bash timeout and gets backgrounded
  anyway, minus the interim output. Launch it with `run_in_background`, run the inbox pull below
  while it works, and read its verdict before you close. (`--no-live` skips the live probes if you
  only need the static checks.) Each failure names its remediation command. **Read the `TURN-BLOCKING` list, not just the
  aggregate verdict** (dimagi-internal/ace#1189): a revoked Gmail refresh token leaves every inbound
  and outbound path dead while the old aggregate still printed `FAIL: 0 / HEALTHY — ACE works;
  warnings below are non-fatal`, because a Gmail-less machine legitimately still runs most of
  `/ace:run`. **A `PASS gog_auth` is NOT sufficient evidence the inbox works — prove it with a live
  read before you trust it** (dimagi-internal/ace#1338): the probe classifies failure by matching a
  denylist of gog error strings, and gog's "no token for this (mailbox, client) pair" message
  (`No auth for gmail <mailbox>.`) matches none of them, so a mailbox that cannot make a single
  call reports `PASS … live scopes OK`. That is the #1189 gate defeated at its source. So run the
  inbox pull yourself as the real preflight — `bin/ace-env gog gmail search "in:inbox is:unread" -a
  ace@dimagi-ai.com --client "$(canopy email client --repo .)" -j` — and treat an auth error there as TURN-BLOCKING no matter
  what the doctor printed. If the read fails under the configured client, check
  `gog auth tokens list` for a `token:<client>:<mailbox>` key: the pair, not the account, is what
  gog stores, and `gog auth list` collapses to one row per account so it can hide a working token
  (which also misroutes canopy's `reconcile_client` onto a revoked one). The verdict is now
  surface-scoped — `HEALTHY for runs · BROKEN for turns` — and any
  `[TURN-BLOCKING]` item means **this turn cannot do its job**: do NOT proceed to the inbox pull.
  Abort loudly, naming the item and its `fix:` line (they are all one-command remediations:
  `gog login …`, or installing the canopy CLI). A turn that continues past one reads an empty inbox
  and reports "nothing to do", which is indistinguishable from a genuinely quiet mailbox — the
  silent-failure shape this whole preflight exists to prevent. **The `--installed` flag is load-bearing:**
  `ace-doctor` defaults to `MODE=self` and audits whichever copy you invoke, so a bare
  `bin/ace-doctor` run from an emdash worktree audits the *checkout* — which has no `node_modules`
  until someone runs `npm ci` there, and which never executes anything. ACE runs from the installed
  plugin (`~/.claude/plugins/cache/ace/ace/<version>/`), so the checkout's deps are irrelevant to
  whether a turn can run. Auditing the wrong copy yields `FAIL deps` → `Verdict: BROKEN — ACE will
  not function` on a machine that is in fact HEALTHY, every turn, which is how a preflight verdict
  becomes noise people route around. (`agents/ace-orchestrator.md` § preflight already resolves the
  install path for the same reason — this keeps turns consistent with runs.) Gmail as ACE:
  `bin/ace-env gog gmail search "in:inbox is:unread" -a ace@dimagi-ai.com --client "$(canopy email client --repo .)" --json`
  (the mailbox is the literal from `config/agent.json`; the client comes from `canopy email client`.
  The two fleet clients (`canopy`, `canopy-web`) are one app — never type a client name; `canopy email client` picks the one this machine holds a token under. `$ACE_GMAIL_ACCOUNT` /
  `$ACE_GMAIL_CLIENT` were RETIRED with ace#1147 and expand to EMPTY in a shell)
  (doubles as the inbox queue pull). **As a queue pull it names the wrong person: each thread row's
  `date` is the NEWEST message's, its `from` is the OLDEST message's, and nothing in the row says
  so — so never tier or noise-classify a sender off this output.** Take the sender from the
  structured read (`canopy email read <threadId>` → `messages[-1].from`) and use the row only for
  the thread id, subject and date; `skills/inbox-triage` § 1 carries the full rule and the two
  failure shapes (ace#2399). Dead gog auth: **preferred fix is the canopy-web "Connect Google
  mailbox" button** (self-service, no terminal); terminal alternative: `gog login
  ace@dimagi-ai.com --client canopy --services gmail,calendar,drive,docs,slides,sheets,forms` —
  always the FULL scope list, since a narrower `--services` (e.g. just `gmail`) **replaces** the
  grant and drops the other scopes rather than adding to them. **The gog client is a SHARED
  fleet client (`canopy` or `canopy-web`), not per-agent** — same as eva/hal/ada; what's per-agent is the mailbox
  (`--account`). `config/agent.json`'s `gog_client` is the declared preference that `canopy email client` reconciles; setting
  it to `ace` kills every read/send, because no `credentials-ace.json` exists and the remedy it
  prints is an interactive browser OAuth a headless turn can't run (jjackson/ace#1147).
- **Board drain is config-gated and best-effort by design** — its absence NEVER blocks a turn (the
  ace-web vs canopy-web question is deliberately open; see `config/agent.json` `_doc`). If
  `canopy agent --help` works and a workbench token exists, drain per `skills/task-tracker`;
  otherwise note "board: not configured" in the close-out and move on. The core's close-out
  workspace refresh (`canopy agent skills`, `canopy agent turn …`) is best-effort under the same
  gate.
- **Inbound processing (core Step 2) = `skills/inbox-triage` in full:** standing noise table first
  (drain ALL search pages), then per thread — tier the sender (**act** = canopy-web granted the whole of ACE, via `canopy caller tier`;
  **correspond** = derived from the routed run's state; neither = read-only), route to opp/run via
  the comms-log `thread_id` (or to a program project, inbox-triage § 2b step 4), one action,
  approval-gated outbound. Per-sender isolation and tier
  resolution live there.
- **ACE's state layer is Drive, never local:** where the core says "record `thread_id` in your
  state layer", that's the routed run's comms-log (`email-communicator` step 7) — the routing key
  inbox-triage matches inbound threads against. Turn state = comms-logs + `run_state.yaml` for run threads; the board task and the
  `<Program> — program context` doc for program-project threads.
- **Pre-send review = `skills/agent-turn-review`, applied INLINE** — read that file top to bottom
  and run its A/B/C/D checklist yourself. Do NOT dispatch it (or `canopy:agent-turn-review`) via
  the `Skill` tool: that runs the fleet body alone and drops ACE's §D send-path rules. It also
  governs this turn's CLOSING REPORT (§C: open with the decision, not the housekeeping).
  Supersedes the old `self-review`; ACE's `-qa`/`-eval` skills grade artifacts — this is the
  brief-fidelity counterpart for correspondence.
- **Skill self-check (core Step 3) is a CHECKPOINT, not a reminder.** ACE's standing
  issues-as-you-go convention applies inside turns — a confirmed defect or improvement gets a
  GitHub issue filed the moment it's confirmed (`gh issue create`, no `-R`); don't defer to turn
  end, don't fix silently. Also ask: did I repeat work by hand that SHOULD be a skill (or an
  issue)?

  **Mechanism — do this, don't just intend it.** The obligation is the **REQUIRED close-out
  line**: report the outcome on the **Issues filed / skills changed** line —
  `skill-self-check: none` is a valid outcome, an ABSENT line is not. That line needs no tool
  at all, and it is what makes a skipped check visible.

  **The todo is an optional reminder on top of it, and on current models there isn't one.**
  Claude Code **2.1.233** withheld `TodoWrite`, `TaskCreate`, `TaskGet`, `TaskUpdate` and
  `TaskList` from Opus 4.8, Sonnet 5, Fable 5, Mythos 5 and newer unless the operator sets
  `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` — Anthropic's reason being that those models track
  multi-step work without a written checklist and the tool definitions cost context
  ([tools-reference § Task tool availability](https://code.claude.com/docs/en/tools-reference#task-tool-availability)).
  ACE deliberately does not opt in. So absent is the normal case, not an anomaly:
  **do the check, write the close-out, and do NOT announce that a todo was skipped**
  (ace#2210 — that per-turn disclosure was the noise this framing removes).
  **The todo is optional; the check never is** — the distinction ace#2173 drew as
  "SKIP THE TODO, never the check", which inverting the default does not soften.
  Never improvise a substitute tracker, and do not halt the turn.

  **If `TodoWrite` DOES resolve** (an older model, an opted-in operator, or a background /
  web session, which serve the same tools on every model), you may add an item literally
  named **`skill-self-check`** at turn START, before the inbox pull, and keep it `pending`
  for the whole turn. Then the ordering constraint applies as written:
  the close-out may not be written while it is still `pending` —
  mark it `completed` only after you have actually asked both questions above.
  Read that constraint precisely; it bars a close-out written while a check is still
  pending, not one written without a todo.

  This is deliberately the cheap half to lose. The two halves of the checkpoint are not
  equally load-bearing: the **todo** is a reminder, while the **REQUIRED close-out line** —
  and its `none`-vs-ABSENT distinction — is what actually makes a skipped check visible, and
  it needs no tool at all. A turn missing the line is still detectably broken; a turn missing
  only the todo is not. What is NOT available is dropping the check itself and reporting
  `skill-self-check: none`: that line asserts the two questions were asked and answered
  negatively, so emitting it without having asked them is a false claim, not a graceful
  degradation. (Same class as ace#2127, which fixed the orchestrator's copy of this trap and
  left this one — the file a non-orchestrator session actually loads — with no fallback at
  all. There it dropped a progress view; here it gated the close-out, so the turn could not
  legally finish.)

  *Why the ceremony:* this step was prose, and prose lost. `canopy agent-review ace` recorded
  `checklist_gap: skill-self-check` for the 2026-09-02 window — the step was skipped and the turn
  still closed green, so nothing surfaced it. That is exactly what `CLAUDE.md` predicts of an
  unenforced invariant ("prose relies on the model choosing to comply, which fails under load").
  The **close-out line** is the cheapest thing here that is *visible when absent*: skipping the
  check now costs a missing line in the close-out instead of costing nothing at all. The todo was
  originally cast in that role, which only worked while the tool existed — hence the inversion
  above (ace#2210): the enforceable half had to be the half that survives an absent tool.
- **What ACE has TOLD people expires too — run the counterpart-asks probe as part of the skill
  self-check** (dimagi-internal/ace#1896). Resolve the plugin root first, as every bundled-code
  invocation must:

  ```bash
  ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
  node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/probe-counterpart-asks.ts"
  ```

  **Not `npx tsx ...`** — the installed plugin cache's `node_modules/.bin/tsx`
  has shipped as a dereferenced copy instead of a symlink since 0.13.1169 (ace#2252), which makes
  `npx tsx` throw `ERR_MODULE_NOT_FOUND` for any invocation whose cwd/prefix is inside the plugin
  root. Calling `tsx/dist/cli.mjs` directly via `node` sidesteps the broken symlink entirely.

  It scans ACE-authored SENT mail for `ace#N` citations, resolves each against `gh`, and reports
  the ones ACE asserted as live limitations that have since CLOSED — with the thread id, the
  recipients and the citing sentence. Report-only; the correction is a letter, so it goes through
  `skills/inbox-triage` under the normal approval gate like any other outbound.

  *Why it is a step and not a habit:* nobody ever re-reads a sent email, so a limitation asserted
  in one never expires by itself. A partner sequenced 11 days of her own work around ace#1549
  after it closed COMPLETED **43 minutes** after the message that told her it was deliberately
  unfixed. `scripts/probe-upstream-asks.ts` cannot see this — its corpus is repo files, which are
  re-read every session; this corpus is Gmail. **Not the comms-log:** those record `thread_id` +
  `message_id` + recipients + date and a one-line gist, never the body, so the citing sentence is
  not in Drive at all. Naming the issue number in the correction is what retires the finding.
- **Close-out (core Step 4) ACE shape:** mark fully-handled threads read via
  `bin/ace-mark-read <threadId> …` — NOT threads still awaiting a human decision. Summary covers:
  **Board** (drained / not configured) · **Inbox** (per thread: sender, tier, routed run, proposed
  action, approved & done, parked; noise counts by class) · **Open threads by age** (all open
  correspond-tier threads, days-since-last-inbound; >5 days = explicit escalation to the run's
  operator, repeated every turn until resolved) · **Runs advanced** · **Blocked/awaiting** ·
  **Issues filed / skills changed** (this line is REQUIRED and carries the `skill-self-check`
  outcome — see the checkpoint above; omitting it is the failure that checkpoint exists to catch).
- **Gating note:** ACE's hook is plugin-level (fires in every session with ACE installed), so
  `config/gating.json` rails stay NARROW and identity-scoped — see its `_doc` before adding rails.
