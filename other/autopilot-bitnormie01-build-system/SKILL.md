---
name: autopilot
description: >
  Use this to run an ENTIRE hackathon campaign hands-off in ONE session — intake the user's
  constraints (which steps, demo video, submission, budget: $0 or funds-allowed), lock them as a
  committed campaign contract, then dispatch and verify every pipeline step (0a extract → 0
  idea-forge → 1 architect → 2 build → 2.5 demo video → 3 gates + submission) autonomously, with
  every consent pre-collected and identity-bound up front. Trigger it when the user says "build the
  full project autonomously", "run the whole pipeline hands-off", "autopilot this hackathon",
  "take <event> end to end", or pastes prompts/INVOKE_AUTOPILOT.md. The only mid-run interactions
  are hard stops (floor items, identity mismatches, capability gaps). Do NOT use it when the user
  wants approval touchpoints between steps — that's the guide (interactive mode, the default for a
  first campaign) — and never self-trigger it: full autonomy is always the user's explicit ask.
---

# Autopilot — the full-campaign autonomous mode

## What this is

Guide mode hands the user a kickoff per step and verifies each baton with them. This seat performs
those handovers itself: it collects the campaign's decisions and consents **once, up front**, locks
them as a **campaign contract** (`../references/campaign-contract.md` — read it in full; it is this
seat's law), then dispatches, verifies, and green-lights every contracted step to a submitted
project. It is a **mode, not a pipeline step**: same pipeline, same artifacts, same doctrine as
guide mode — only the seat that turns the crank changes. You are a **user-side seat**
(`../references/roles.md`): you hold the whole map, you prepare/dispatch/verify every step, and you
execute contract-consented gates in your concierge capacity — you never weaken a gate, never answer
beyond the contract, and never touch the never-consentable floor.

**Announce at start:** "I'm using the autopilot skill — I'll collect and lock your campaign
constraints once, then run the whole pipeline hands-off against them, stopping only for hard
blockers."

## Boot

1. **Resolve/sync the project repo** (contract field 7; `../references/repo-bootstrap.md`) — create
   it per the protocol when none exists. Detect pipeline state from committed artifacts (a
   contract, runsheet, tollgate report, or batons may already exist — this is how you **resume**,
   see below).
2. **Load or run the intake.** A committed, locked contract → load it and continue from the
   runsheet's step status. None → run the intake protocol in
   `../references/campaign-contract.md` §Intake protocol: ingest the kickoff, derive what's derivable
   (including the **live identity read** for the submission/upload accounts), ask **only the gaps**
   in batches of ≤4 specific derived questions, read the whole contract back once, and on the
   user's single confirmation stamp it **LOCKED**, commit, push. The contract commit precedes the
   first dispatch.
3. **Run the campaign tollgate** (`../references/tollgate.md`) — normally you are this campaign's
   first pipeline session: probe the full matrix for the contracted steps **plus row 17** (subagent
   MCP reach — autopilot campaigns only) **and row 18** (model/effort routing, incl. the effort
   mechanism and the settings that defeat routing — `../references/model-routing.md`; write its
   Routing section), write/commit/push the report. If a campaign report already exists (the campaign
   began in guide mode and switched here), verify and **extend that report** — re-probe the
   session-scoped rows plus rows 17 and 18, update stamps — never fork a second; one report per
   campaign. Because this session persists campaign-long, its session-scoped rows stay valid for
   every step you dispatch — re-probe them cheaply before each browser-heavy dispatch and after any
   reconnect. Hard-stop on your own failing hard rows; report the rest per the protocol.
4. **Open the runsheet** — guide format and path (`docs/guide/<YYYY-MM-DD>-<event-slug>-runsheet.md`),
   so a guide session opened later reads the same campaign state. Record the contract path, the
   tollgate verdicts, the step plan, and this session's own settings (the model id you stated + the
   effort the user set; `../references/model-routing.md` §Seat settings' autopilot row). Commit.

## Step execution modes

| Step | Mode | Notes |
|---|---|---|
| 0a extract | subagent | context-heavy crawl; MCP reached per row 17 |
| 0 idea-forge | subagent | inputs pre-filled from the contract via its confirm-and-proceed path (build capacity keeps its kit default — the autonomous pool + the builder) |
| 1 architect | subagent | contract-driven dialogue + approval loop (below) |
| preflight gates | subagent — concierge, `MODE: preflight` | field 12's checklist = the green-lit classes |
| 2 build | **inline** — load and run `../orchestrator/SKILL.md` in this session | executors are themselves subagents; only one dispatch level is assumed anywhere in this design |
| 2.5 demo | subagent | consents/fields from the contract; falls back inline per Row-17 fallback |
| 3 closing + submission | subagent | identity re-verified before the submit |

Running Step 2 inline extends the kit's documented in-session exception (architect→orchestrator):
you already hold the kernel-side duties, and the executor-per-task subagent model is unchanged.

**Every dispatch** = the step's own `INVOKE_*.md` template, filled from the contract, with the
**`AUTOPILOT CAMPAIGN` block** prepended (`../references/campaign-contract.md` §Dispatch block):
the contract path + the slice of locked fields that step consumes + the BLOCKED-with-question
escalation instruction. You answer a returned BLOCKED **only from the locked contract**; a question
the contract can't answer is a hard stop (or a logged substitution, per field 14).

**Row-17 fallback:** if the boot probe shows subagents cannot reach this session's MCP tools, the
MCP-dependent steps (0a, 2.5, 3) run **inline** in this session instead — same doctrine, with
context triage (prefer inline-late, after the build). Where context won't allow it, apply field 14:
stop and hand the user that one step as a classic guide-mode kickoff. Degrading one step to manual
is a reported limitation, never a silent skip.

**Routing** (`../references/model-routing.md`): bind every dispatch per the tollgate report's
Routing section (row 18). Step seats and your other spawns (the independent frame/audio review,
probes) bind per §Seat settings — per-spawn `model` always, per-spawn
`effort` when the Routing section shows `per-spawn` (else the spawn inherits your own effort,
logged as degraded); a Step-3 dispatch that would execute any `human_gate: true` task binds `top`
(the pin rule). Step 2's tasks run per their manifest `effort`/`model_tier` fields, with the same
binding, effort floors, logging, and escalation ladder the orchestrator doctrine specifies. The
contract's **field 16** may pin campaign-wide; a pin never overrides a `top` pin, and
`routing: inherit` (row-18 FAIL, or any non-Claude-Code harness) means every dispatch simply
inherits — routing is never a blocker and never a hard stop.

## The run loop

For each contracted step, in pipeline order:

1. **Assemble and dispatch** per the table above.
2. **Verify the baton with the guide's checklist for that step** (`../guide/SKILL.md`
   §Step-by-step playbook) — from the synced repo, never from the subagent's word: pack INDEX gaps
   + spot-checked judging weights; brief fields complete + your **calendar-fit call**; spec/plans/
   manifest validation clean + human-gate coverage + submission draft + appended stack rows; green
   build's money shot demonstrated; script/video QC; ledger evidence per gate. You verify by
   INDEX/headers/spot-checks — never ingest full artifacts; keep this session lean.
3. **Record the verdict in the runsheet**, commit, proceed. A failed verification re-dispatches
   with concrete corrections — **bounded at 2 re-dispatches per step**, then hard stop.

Specific protocols:

- **Calendar-fit remediation (after Step 0):** the winner doesn't fit the deadline → re-run
  idea-forge **once** with tighter inputs (`safe-feasible`, fewer tracks — the guide's documented
  remediation, performed by you); still doesn't fit → hard stop.
- **Design approval (Step 1) — the hard gate survives; the approver is you.** The architect
  subagent answers its brainstorming questions from the contract + brief, records each in the
  spec's `Design decisions` section, and returns the design summary. You review it for **contract
  conformance** — tracks, budget, must-have demo features, out-of-scope respected — and approve or
  re-dispatch with concrete corrections, **bounded at 2 rework loops**, then hard stop. Your
  approval must cite the contract fields you checked; rubber-stamping is forbidden. The same
  pattern approves the demo script (Stage 1 of 2.5) — contract conformance plus the script schema's
  locked-headings check (`../references/demo-script-schema.md`).
- **Human-gated tasks in Step 2 (inline orchestration):** a task whose class is enumerated in
  field 12 (e.g. testnet deploy with the burner key) is executed **by you, in your concierge
  capacity** — restated in one line, run with the granted tooling, evidence into the gate ledger,
  exactly as a consented concierge gate. A class **not** enumerated → the task pauses (hard stop).
  Executor subagents still never run a gated step.
- **Before dispatching 2.5:** note in the runsheet that recording will take over the desktop
  foreground (a do-not-disturb window) — a courtesy announcement, not a consent; the consent is
  the contract's field-12 recording pre-consent.
- **Outward publishes** (video upload, submission, repo-public flip): re-read the live logged-in
  identity first (`../references/campaign-contract.md` §Identity verification). Match → proceed
  silently. Mismatch or logged-out → hard stop with what was found. Never log in, never switch
  accounts.
- **Budget:** enforce the locked field 5 everywhere (`../references/campaign-contract.md` §Budget)
  — `$0` means a paid-resource assumption anywhere in a brief/spec/plan fails your conformance
  review; `funds-allowed` caps planning and still pauses every payment moment for the human.

## Hard stops (the only mid-run interactions)

Triggered by: a never-floor item; an identity mismatch; a capability gap (SMS-OTP, an on-device
tap); a contract-impossible situation under `stop-and-wait`; loop bounds exhausted; a budget
conflict. Behavior: update the runsheet with the exact blocker + the fix hint, **notify** (field
15 — in-session always; the environment's push/notification tool when available), and **wait**.
Resuming is the user's message; you never time out into a riskier path, and a declined/parked item
stays parked.

## Resumability

Your memory is the committed artifacts — contract, runsheet, tollgate report, gate ledger, batons.
A compacted or restarted autopilot session re-boots from the synced repo (Boot 1–4 detect
everything) and continues from the runsheet's step status. Only session-scoped grants
(tollgate rows 5–8, 12, 17 — plus row 18, whose tier bindings were verified in the dead session)
need re-granting/re-probing in the new session — re-run those rows,
update the report, resume.

## When the campaign finishes

Verify the submission confirmation with your own eyes (screenshot evidence into the ledger), close
the runsheet (repo, deployed addresses, video URL, submission confirmation link), notify, and
report: what ran, every step verdict, **every consented act with its evidence**, and everything
parked or declined. The campaign's audit trail is the ledger + runsheet + contract — a reader can
reconstruct every outward action and the exact consent line that authorized it.

## Boundaries

- **The contract is your entire authority.** If you can't point at the contract line that
  authorizes an act, the act is not authorized — pause instead. Never solicit amendments; never
  broaden an enumeration; never re-ask a locked answer.
- **The never-consentable floor is absolute** — the full list lives in
  `../references/campaign-contract.md` §Never-consentable floor; cite it, don't work from memory.
  Headline items: mainnet, real funds, the user's main wallet, payment/KYC, credential entry,
  secrets in artifacts.
- **Never weaken a pipeline gate** — the design-approval, gate re-runs, scope checks, QC loops,
  and identity checks all still run; autonomy moved the approver, not the bar.
- **Never self-trigger.** Full autonomy is the user's explicit ask, every campaign.
- **State comes from the synced repo** — verify batons from artifacts, never from a subagent's
  claim (same rule as the orchestrator's "re-run the gate yourself").

## When NOT to use this skill

- A first campaign on this kit, or anything security-sensitive the user wants eyes on — recommend
  **guide mode** (approval touchpoints between steps) and say why.
- The user wants to make the calls mid-flight (track choice after seeing the pack, watching the
  demo cut before upload) — guide mode gives them exactly those touchpoints.
- No hackathon/event campaign at all — a plain build wants the architect → orchestrator flow, not
  a campaign contract.
