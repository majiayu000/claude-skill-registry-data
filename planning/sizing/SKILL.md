---
name: sizing
description: "The EM's first move on any PM ask — size it, then route to plan, shape, roadmap, or dispatch. Fires whenever novel engineering work is asked of the EM, by any combination of words: this is a shape test, not a phrase list. Mutually exclusive with pickup."
description-budget: 260
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
argument-hint: "[PM ask text | nothing — describe the ask inline]"
---

# Sizing — the Fleet Routing Lobby

The EM's first move on any PM ask that isn't a mid-workstream continuation — before
`coordinator:plan`, `coordinator:shape`, or direct dispatch. Framing, incidents, per-step
rationale: `coordinator/docs/wiki/planning/sizing-lobby.md`.

**Dispatch authorization — invoking this skill IS the request.** The dispatches named below are constitutive steps of this skill, not a separate thing to get cleared: invoking a skill requests the actions that skill performs. A harness line permitting dispatch "unless the user requested it" is therefore **satisfied here, not overridden** — no precedence claim is needed and none is made. Re-asking spends the very context the dispatch exists to protect. The rule attaches to skill entry and dissolves no PM-authored gate: keyword-gated skills gate entry, and every gate a skill names for itself still binds — per-session cross-repo-commit assent, ask-before-external-action, and any other this skill's own body names. Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`. Rationale: wiki § Skill rationale.

The t-shirt (`loe.tshirt`) picks a ROOM, not a plan-body cost. No appetite question first.

---

## The flow

**1. Form a t-shirt read** (XS–XXL) of engineering complexity only, never appetite. Calibration
table and the tentativeness guard: wiki. A confident XS/S with a clear PM express-lane signal
skips to Step 3.

**1a. Size what the performer must HOLD, not only how much work it is once held.** A credential, an
authenticated session, a mounted store, a guard-fenced path, an operator at a keyboard: an unnamed
held capability looks like small work until the dispatch returns INCOMPLETE. Name the capability in
the sizing so a blitz can SKIP rather than discover — **the capability, never the route you happened
to try**. Ask once, at gate-writing time: what is the question, and what else would answer it?
Tripwire: `A-SCOPE-FIELD-NAMES-A-SUBJECT-NOT-A-BLAST-RADIUS`.

**1b. Premise-provenance, every non-express-lane sizing.** Does the ask rest on a mechanism
EXECUTED, one only READ, or no mechanism claim at all (`not-applicable`, narrow)? Pass
`--premise-provenance executed|read|not-applicable`; the justification goes in the sizing-object's
`premise.evidence` at Step 4. The engine's `next_move` carries the discharge text.

**2. Substrate probe — L/XL/shaky reads, mandatory on XXL.** Reuse cartography output
(`architecture-survey`/`-audit`); for judgment the engine can't emit, dispatch the
`internet-research-scout` payload. Feed `--probe-signal collapse|raise`,
`--scout-evidence-kind mention-count|change-set|site-count`, and on any `raise`,
`--probe-raise-basis ask-scope|substrate-condition|breadth` — the engine applies only `ask-scope`;
a finding about the *area's* condition, or a uniform touchpoint count, is not a size signal
(discriminator detail: wiki). Chain `coordinator:spike` first if the probe surfaces an unproven
mechanism.

**3. Compute the route — never hand-derive the table.**
Invoke `sizing-assemble` per the ladder in `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` — rung 0 (Shape W,
the `.exe` launcher) on a PowerShell host:

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\sizing-assemble.exe" --tshirt <XS|S|M|L|XL|XXL>`
`--tshirt` is the only required flag; never pass `--appetite` unless the PM volunteered one
verbatim. Always pass `--intent "<PM's words>"` (`--intent-source em-elaborated` if your own
restatement), `--precedent shipped-before|novel`, `--boundary-in-notch yes|no` (§ Appetite guards),
the Step 1b/2 flags as answered, and `--jtbd-unclear`/`--well-trodden-step-change`/`--express-lane`
as warranted. Push the returned `route`/`detents`/`next_move` verbatim.

**4. Write the sizing-object** for any non-express-lane sizing: re-run Step 3's `sizing-assemble`
call with `--write state/sizings/<date>-<slug>.yaml` and `--premise-evidence "<text>"` (Step 1b's justification). It writes the record from its own output and
lands it `routed`; never hand-edit its fields. Undecided direction-class items go in
`surfaced_to_pm`, never folded into `fork`/`xl_exit`. Optionally pass `--name "<short label>"` for
`name` — a few words, whiteboard length; never a slice of `intent`.

**`status`.** An XS has no plan: stamp it `shipped` yourself when the work lands, citing the commit.
S and above: the terminal cascade owns the stamp — never pre-empt or hand-stamp it; it fires **from
the stamping op, not from the landing**; on the self-completing path that op is the chain inside
`dispatch.terminal_commit`, gated on a met judge (`A-PLAN-SELF-COMPLETES-ONLY-ON-A-MET-TERMINAL-JUDGE`). Then read `status` back (never `acted`). Still `routed`
under a plan stamped through the op is a finding; under a hand-landed plan, run the close-out. Detail:
wiki § Step 4. Tripwire: `ACTED-IS-BLIND-TO-THE-DELIVERABLE-CASCADE`.

**4b. Open the flight recorder on the resolved route — every route, before anything downstream.**
`TaskCreate`: one session-goal task naming the ask and the sizing-object path, then **one task per
remaining stage of the chain the route implies, through its terminal** (per-route chains: wiki §
Step 4b). The `plan` chain: plan, plan review, `/execute-plan` (its run judges and stamps),
`/workstream-complete`. Route `spec-dispatch` plans through `/execute-plan` even when light. **Terminal by size:
XS/S close at `quick-wrap`, M and above at `/workstream-complete`.** Where the harness tool is
absent, `coordinator-tasks-mirror` carries it. **Downstream steps ADD to this list, they do not
restart it** — a second session-goal task means a recorder was re-created.

**5. `post_size_prompt_pending` (M+) — ask once, in the PM's register, and stop:** *"Looks like an
X — go with that, split it, cut it, what's up?"* Never a closed fork. Record the answer in
`pm_resolution` — an object, `decided_on: YYYY-MM-DD` required, the answer beside it — and `fork`
when cut/raise-shaped. Expires at plan ratification.

**5b. `route: pm-decision` bundles into the same ask** — the M+ prompt and the XL exit question
are ONE combined PM ask. `xl_exit` stays `null` until the PM picks: `shape`, `roadmap`, or
`accept_multi_session` (only with explicit PM assent; never a silent default). Tests: wiki § Step 5b.

**5c. Turn 1 exit on `route: plan` at M/L — the four-turn loop.** The EM loop is four turns:
sizing (this one), the plan Workflow's return, the execute Workflow's return, and
`dispatch.terminal_commit` plus the close ceremony. Touchpoints are read from `interaction_mode` (hands-on, pm, ceo), never
inferred. Pass `--exit-criterion` and `--interaction-mode` to `sizing-assemble`, and record the PM's
answer with `sizing.accept_exit_criterion` (`pm_quote`, optional amended `statement`, `mode`) —
never by hand-editing the sizing object. In pm and ceo modes the ask says plainly that accepting
it authorizes execution without a further ask. Per-mode asks: wiki § Step 5c. For XL, Step 5b is unchanged.
After acceptance, `emit-wave-fire --from-sizing <repo-relative sizing path> --repo-root <abs repo>
--trail-dir <abs trail dir>` mints the baton itself (never via
/spinoff or /handoff) and prints one `Workflow` line to fire. End the turn: the plan Workflow
(turn 2) runs with no EM in the loop.

**6. Hard gate — the only override that exists.** The t-shirt→route map binds absolutely; no
named-reason override, no ratifier. If a route feels wrong, the size read was wrong: fix the size
with evidence (symmetric resize, or the `plan⇄sizing` return edge) and let the table re-resolve.
`pm-decision` is a routed outcome, not an exception.

---

## Appetite guards — judgment the engine's flags cannot resolve alone

`appetite` is the PM's stated budget, populated only after the size lands. Rationale and
incidents: wiki § `appetite`, § The newer guard flags.

- **A volunteered appetite never moves the estimate.** Size from the work alone.
- **A cross-team dependency is a gate, not a size.** The boundary *ceremony* goes in
  `blocked_by`/`awaiting_gate`, never the t-shirt. Answer `--boundary-in-notch no`.
- **A touchpoint count is not a depth read** (`--probe-raise-basis breadth`, § Step 2).

## Shape is a conditional room, not a second lobby

`route=shape` fires only when the size is large AND the JTBD is unclear, or the space is
well-trodden and the ask wants a step-change — both engine-resolved from
`--jtbd-unclear`/`--well-trodden-step-change`, never an EM gut-call.
