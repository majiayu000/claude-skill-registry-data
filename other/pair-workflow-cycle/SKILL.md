---
name: pair-workflow-cycle
description: "In-session coordinator for pair's delivery cycle: drives ONE card through implement → verify (a fresh card has no up-front contract) and, for each round of review findings, prepare → validate → green → verify, one stage per subagent, from an interactive Claude Code, Codex or pi (with pi-subagents) session — no dependency on Claude Code's Workflow tool. Enters on a fresh card ($card) or straight into fix & review on an existing PR ($pr). Holds zero cycle rules: every transition, budget and freshness decision comes from cycle-state.mjs resolve, every argument packet and worktree from cycle-dispatch.mjs. Binds its harness by PROBING for a subagent primitive, never by product name, and HALTs realization-unavailable with the pair-cli fallback when none is present. Never decides merge — the `merge` stage's script does."
version: 0.2.0
author: Foomakers
---

# /pair-workflow-cycle — One Card, One Stage at a Time, From Inside a Session

The delivery cycle is a state machine that already exists; this skill is one way to turn its crank. It asks the durable state what is due, dispatches exactly that stage to a subagent, forgets everything but the answer, and asks again. It classifies nothing, judges nothing and selects nothing — every decision it acts on was already taken by `cycle-state.mjs`, and every packet it hands out was rendered by `cycle-dispatch.mjs`.

Two entries, one cycle: a refined card with no PR runs the whole thing; a PR that already exists enters at its first verification and runs fix & review. You never merge, and you never review.

## Arguments

| Argument    | Required | Description                                                                                                                                                                                 |
| ----------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$card`     | One of   | Card (issue) number. The fresh-card entry: `resolve` yields `implement / initial / a0` — no up-front contract (ADR-024 amendment 2026-09-23); a run directory already on the sealed `a0` path continues it. Give `$card` or `$pr`, never both and never neither. |
| `$pr`       | One of   | PR number — the fix & review entry: `resolve` yields `verify / first / r0` and NO preparation runs before it. The card is read from the PR's linked issue.                                     |
| `$rounds`   | No       | How many remediation rounds THIS invocation may spend. Default: the policy's `maxFixRounds`. It only ever narrows: a `$rounds` above `maxFixRounds` is **clamped** to the policy value and the clamp is reported — it can never widen the ceiling, because the ceiling is the cycle's, not the invocation's. |
| `$runId`    | No       | Run directory to drive: `.pair/working/runs/$runId/<card>/`. Default `story-<card>` — the batch engine's own convention, so a cycle started by `pair-implement-batch` resumes here and back.    |
| `$notes`    | No       | Scope directive from the card; threaded into every stage packet, overriding the issue body where they conflict.                                                                              |
| `$profile`  | No       | The workflow profile to use (US-488): a NAME, looked up in `pair.config.json`'s `workflowProfiles.files` / `.inline`. Cascade, resolved once per run: `$workflowConfig` > `$profile` > `workflowProfiles.default` > the KB default (schema-default engine and model, default effort, `fresh` context). Unresolvable ⇒ HALT `profile-unresolved`, never a silent fallback. A value starting with `{` is the **legacy** inline object `{ "effort": … }` (one of `low \| medium \| high \| xhigh \| max`, applied to every stage's dispatch instruction exactly as before — enforced for Codex, a best-effort prompt request only for Claude); absent ⇒ today's behavior, unchanged. |
| `$until`    | No       | The target (US-521, ADR-027): `ready` (stop at the prepare→implement boundary), `pr` (default: the review-approved PR) or `merged` (enter the merge stage — the only value under which the merge gate is evaluated). Precedence: argument > argument preset > explicit adoption key (`## Autonomy`, then translated legacy sections) > adoption preset > KB default — every effective value is printed with its source. |
| `$prepare`  | No       | The prepare gate (US-523, ADR-028), `<hold-always\|hold-never\|hold-when>[; has: <labels>][; lacks: <labels>]`: who prepares a Draft / Ready-without-breakdown `$card` before the cycle starts. `hold-always` (default) keeps R3.11 — a human prepares; `hold-never` proceeds alone recording assumptions; `hold-when` proceeds alone unless a boundary escalates (`needs-review`, the card stays Draft). Same grammar and precedence as `$merge`; see the Prepare phase in Step 1. |
| `$merge`    | No       | The merge gate, same grammar. `hold-always` (default) parks `awaiting-human`; `hold-never`/`hold-when` enter the merge stage under `until: merged` unless an escalation fires. #490's signal checks stay mandatory under every mode. |
| `$workflowConfig` | No | Path of an external profile file, used verbatim; wins over `$profile` and `pair.config.json`. Malformed ⇒ HALT `profile-invalid`. |

Everything else a stage receives — `$run $story $branch $worktree $base $stacked $entry $policy $inputs $workflowVersion` and the phase-specific arguments — is **rendered by the script**, never composed here in prose.

## Algorithm

### Step 0: Bind the realization (mandatory, before any dispatch)

**Check.** Read the table as data and probe your OWN toolset for its dispatch primitive:

```bash
node "$SKILL_DIR/scripts/cycle-dispatch.mjs" realizations --tools '<JSON array of the tool names you actually have>'
```

**Skip.** Never. A realization bound in a previous turn is re-probed: the toolset is a property of this session, not of the task.

**Act.** The script returns `bound` and the row it bound:

| Row      | Dispatch primitive | Resume primitive              | How the role travels                       |
| -------- | ------------------ | ----------------------------- | ------------------------------------------ |
| `claude` | `Agent`            | `SendMessage`                 | `agentType` — the stage's agent definition  |
| `codex`  | `collaboration.spawn_agent` \| `multi_agent_v1__spawn_agent` | `collaboration.followup_task` \| `multi_agent_v1__resume_agent` | the agent `.md` body + the skill reference  |
| `pi`     | `subagent` (the `pi-subagents` package; `subagents_enable` is its loader) | `subagent` — `runs.run({ resume })`, rendered by `pi-bridge.mjs` | the agent `.md` body + the skill file path |

Report which realization won and which primitives it bound to, in one line.

**Verify.** The row is bound by the PRIMITIVE the probe found, never by a product name or a version string: a name is a claim about the host, a present tool is evidence of it. No row applies ⇒ HALT `realization-unavailable` (below) **before any dispatch** — including the case where this skill is itself running inside a subagent and the host forbids nesting — unless Step 0b applies.

### Step 0b: inside pi — the package, its version and its tool shape

**Check.** Only when the probe bound `pi`, or bound nothing: ask the bridge, through your own shell, whether you run inside pi and what is installed.

```bash
node "$SKILL_DIR/scripts/pi-bridge.mjs" probe --project "$PWD"
```

**Skip.** `inPi: false` and no `pi` row bound ⇒ nothing here; Step 0's outcome stands. `inPi` is read off pi's own process marker (`PI_CODING_AGENT=true` on every command its shell runs), never off a product name.

**Act.** You **never** install on your own: every install below is proposed, and runs only on the user's explicit yes.

- `status: missing` (no `pi-subagents`, or removed since the last run) ⇒ tell the user the in-pi cycle needs `pi-subagents@<pinned>` and propose the `install.user` line (or `install.project` if they want it project-local — a project-local package loads only in a trusted project, see `/pair-capability-setup-harness` with `$harness: pi`).
  - On **yes**: run the install line the probe printed (stdin closed, foreground), then STOP and ask the user to re-run this skill — the tool appears only in a new session.
  - On **no**: HALT `pi-subagents-missing` — the in-pi cycle cannot run without it; the fallback is `pair-cli run --card N` from a shell.
- `status: drift` (installed, a version other than the pinned one) ⇒ warn, naming both versions, and propose aligning it via `/pair-capability-setup-harness` with `$harness: pi` (the probe prints the pinned install line). If the user declines, proceed, and state once in your report that the pi-subagents version is unverified.
- `status: pinned` and Step 0 bound the `pi` row ⇒ nothing to propose.
- `status: pinned` or `status: drift` but Step 0 bound no `pi` row (installed, yet this session did not load the tool) ⇒ HALT `realization-unavailable`, naming the remedy: with `scope: project`, trust the project so pi loads its local packages (see `/pair-capability-setup-harness` with `$harness: pi`); otherwise — or when it was installed earlier in this session — start a new pi session and re-run this skill. Propose nothing else.
- `activationRequired: subagents_enable` from Step 0 ⇒ call `subagents_enable({})` once; `subagent` is available on your next request.

**Verify.** Before the first dispatch, check the tool's shape as THIS session lists it (its name and its parameter schema, copied from your own tool list, never retyped from memory):

```bash
node "$SKILL_DIR/scripts/pi-bridge.mjs" check --tool '<JSON {name, parameters} of the subagent tool>'
```

A mismatch ⇒ HALT `subagent-tool-mismatch` with the bridge's detail (it names the expected version) — no dispatch on a shape nobody verified.

### Step 1: Resolve what is due

**Check.** Before the first `resolve`, resolve `## Blocking Severities` by running `node <skill dir>/scripts/blocking-severities.mjs read <main checkout>/.pair/adoption/tech/automation.md` — r1-3: the SAME grammar `pair-cli`'s `blocking-severities.ts` reads, ported into this dependency-free script (not hand-parsed in-session) so a `cycle-defaults-parity.test.ts` fixture run can hold the two to the identical policy, byte for byte, on every fixture including the default. A HALT from the script IS `automation-policy-malformed` — relay its message verbatim, naming the file and the offending line, never a silent fallback. The prose below documents the grammar the script enforces; read `## Blocking Severities` from the MAIN checkout's `.pair/adoption/tech/automation.md` (US-514 T-1, the #514/AC1 revision: a FLOOR compared by RANK, never a list — the same rule as `severityFloor` / `--severity-floor` elsewhere in the chain) — the same file, the same fenced/HTML-comment-blind extraction `## Eligibility` already documents. **Absent file or absent section** ⇒ the KB default `{ "blockingFloor": "Minor" }` — today's behaviour, byte for byte (every severity except `Questions` blocks), and `pair` itself declares nothing (delta-only adoption, ADR-018/D21). **Present but empty** ⇒ HALT `automation-policy-malformed`, naming the section. **Present**: the first line is ONE severity — `Critical | Major | Minor` — a comma-separated LIST, an unrecognised token, an empty declaration, or a `max-dispatches` line that is not `<positive integer> [warn|block]` all HALT `automation-policy-malformed`, naming the file and the offending line — never a silent fallback. An optional second line, `max-dispatches: <n> [warn|block]` (mode defaults to `warn` when omitted), becomes `"maxDispatches": { "n": <n>, "mode": "<warn|block>" }`; absent ⇒ no ceiling at all — never invent `40`. Merge the result into `<policy JSON>` below (`{ "blockingFloor": "<severity>", "maxDispatches": {…} }`, the `maxDispatches` key omitted when there is no line) — the SAME object every later `resolve`/`packet`/`bind-hosts` call in this invocation reuses (the autonomy `policy` and `--labels` are the exception: they go to YOUR `resolve` calls ONLY — never into a `packet`'s `--policy`, whose JSON carries only `blockingFloor` / `maxDispatches` / `deadDispatchRetries`, because the stage's own Step 0 resolve reads that policy with no `--labels` and an `autonomy` key would escalate `labels-unreadable`; `packet` strips `autonomy` as defence in depth), so red-verify and review-phase (T-2) and this run's own dispatch ceiling (T-3) all act on one value. `resolve`'s own `max-dispatches` WARNING (mode `warn`, at or above the ceiling) is not silent: print it to the operator verbatim before continuing.

Ask the one authority, from the MAIN checkout:

```bash
WV="$(node "$SKILL_DIR/scripts/cycle-state.mjs" version)"
AC_HASH="$(node "$SKILL_DIR/scripts/cycle-state.mjs" ac-hash --story $card --dir ".pair/working/runs/$runId/$card" | node -pe 'JSON.parse(require("fs").readFileSync(0,"utf8")).acHash')"   # canonical card hash — the SAME input every stage resolves with
node "$SKILL_DIR/scripts/cycle-state.mjs" resolve --dir ".pair/working/runs/$runId/$card" \
  --workflowVersion "$WV" --policy '<policy JSON>' --entry <fresh|pr> [--pr $pr] \
  --story $card --inputs <digest> --acHash "$AC_HASH" --runsRoot .pair/working/runs [--contextPolicy '<contextPolicy JSON>'] [--redirects <n>]
```

The PM tool and code host are bound ONCE, here, before the first `resolve` of this invocation — every script a stage runs against this run directory (card hash, PR comment, check, label, scope decision) then goes through that binding, never a re-read of way-of-working mid-cycle (US-492, ADR-018 split):

```bash
node "$SKILL_DIR/scripts/cycle-state.mjs" bind-hosts --dir ".pair/working/runs/$runId/$card"
```

`bound` on a new run, `reused` on a resumed one — and on the run an `other-run` answer makes you adopt, bind that directory the same way before its first dispatch. Report `pm-tool` / `code-host` in the same line as the realization. `{ halt: "host-unsupported" }` ⇒ HALT `host-unsupported` (below) before any dispatch.

**Autonomy policy (US-521).** Resolve the effective autonomy policy ONCE, before the first `resolve`, by the ONE shared script (the same one `pair-cli run` spawns; this skill holds no autonomy rule):

```bash
node "$SKILL_DIR/scripts/autonomy-policy.mjs" resolve --adoption "$MAIN/.pair/adoption/tech/automation.md" \
  --args '{"until":"<$until>","prepare":"<$prepare>","merge":"<$merge>"}'   # only the arguments actually passed
```

Print its `lines` verbatim (every key, its effective value and its source: `argument` | `adoption` | `adoption (translated from ## Auto-Advance)` | `preset <name>` | `default`), then its `warnings`. `ok: false` ⇒ HALT `automation-policy-malformed` naming each `errors[].key` and reason, before any card is touched. A project that declares nothing and passes nothing resolves to `until: pr`, gates `hold-always`: nothing below changes. Hand `resolve` the result as `--policy '{…,"autonomy":<policy>}'` (the script's `policy` object) only when `active` is `true`, and — only when `policy.until` is `merged` and the merge gate is `hold-when` — the card's CURRENT labels as `--labels '<JSON array>'`, re-read from the PM tool before EVERY `resolve` (labels are live at each boundary) — and, once the card has a PR, that PR's CURRENT labels as `--prLabels '<JSON array>'` (`gh pr view <pr> --json labels`, re-read the same way): the review writes the PR's `risk:*` tier, so the script decides the gate on the card's labels with its `risk:*` replaced by the PR's (an untagged PR is `risk:red` at the merge boundary) — this skill holds no such rule, so a card still tagged `risk:green` whose PR the review raised escalates at the merge boundary BEFORE `cycle-merge.mjs check`. The legacy `--policy '{…,"autoAdvance":{"tiers":[…]}}'` with `--tier`, exactly as before, is passed only when `active` is `false`.

**Empty `## Autonomy` — ask the preset once (US-576).** When the resolution shows nothing declared or passed (every effective source `default`, no translated legacy section) and a human is present, ask `full / escalate-red / supervised` (Enter = `supervised`) and write `preset: <answer>` under `## Autonomy` in `.pair/adoption/tech/automation.md` through `/pair-capability-record-decision`, then resolve again. Unattended (no human to answer): write nothing, run with the KB defaults (every gate held — the supervised behaviour) and print how to set one (`preset: escalate-red` under `## Autonomy`, or `--preset` on `pair run`).

**Prepare phase (US-523, `$card` entry only).** A `$pr` entry never prepares — a card with a PR has started. For a `$card`, BEFORE the first `resolve`, read the card's readiness (through `/pair-next`'s Control-State Resolution — one procedure, this skill re-derives nothing: macrostate `Draft`, `Ready` without a task breakdown, or `Ready`) and its CURRENT labels, then ask the ONE shared script — the same one `pair-cli run --card` and the batch run; this skill holds no prepare rule:

```bash
node "$SKILL_DIR/scripts/cycle-prepare.mjs" decide --gate '<policy.prepare JSON>' --readiness <draft|refined-no-breakdown|ready> \
  --attended <true|false> --boundary <B0|B1|B2> --dir "$RUN_DIR" --story <card> --source <effective.prepare.source>
```

The script reads the card's CURRENT labels itself (`--dir`/`--story`); never paste a label, title or any other card text into a command line — it is untrusted host data. `attended` is `true` for an in-session run (a human is here) and `false` when this cycle was dispatched by a batch or a loop. Boundaries: `B0` before refinement, `B1` after it (classification tags now written; a `refined-no-breakdown` card enters here), `B2` after the task breakdown. Print its `route` and follow it — nothing else decides:

| `route` | You |
| --- | --- |
| `nothing-to-prepare` | Continue to the first `resolve` (the card is Ready). |
| `run-interactive` | Compose `/pair-process-refine-story` (Draft) or `/pair-process-plan-tasks` (breakdown missing) with their interactive defaults — phase 0 `/pair-capability-grill` and every human-judgment gate ask, exactly as today (R3.11). Then continue. |
| `skip-needs-human` | `prepare: hold-always` unattended: print that the card needs a human, spawn nothing, write nothing, end the invocation (never re-attempt it this run). |
| `skip-escalated` | The card carries `needs-review` (any readiness, Ready included): end the invocation; a human removes the label, or an attended run's `complete` clears it. |
| `escalate` | `node "$SKILL_DIR/scripts/cycle-prepare.mjs" escalate --dir "$RUN_DIR" --story <card> --boundary <B0\|B1\|B2> --gate '<JSON>' --source <source> (--conditions '<the route's conditions JSON, verbatim>' \| --openQuestionFromCard true)` — `--openQuestionFromCard true` (an open question under `## Open Questions`, see below) makes the script read the question from the card itself, never from your command line; adds `needs-review`, posts ONE marker comment, writes no board state; the status is `escalated`, then Step 5's `on-halt`. |
| `run-autonomous` | Refine (Draft only) with `$approval: auto $prepare: <the gate's mode>` — the ONLY combination that lifts phase 0, `$approval: auto` alone still HALTs it (ADR-021) — then `decide` at `B1`; plan with `/pair-process-plan-tasks $approval: auto`, then `decide` at `B2`; then `cycle-prepare.mjs complete --dir "$RUN_DIR" --story <card> --gate '<JSON>' --source <source> --attended <true\|false> --refinedAutonomously <true\|false> --state <first board state mapped to Ready in the State Mapping of way-of-working.md; no mapping = Ready; none mapped = HALT>`, the one place Ready is written (`--refinedAutonomously true` only when YOU ran the refinement in this prepare — it then also owes `## Assumptions` + the provenance line; `false` for a card that entered at `B1`, already refined by a human; an attended `complete` also clears `needs-review`; fails closed without a `## Task Breakdown` checklist). Any boundary that answers `escalate` stops there. |

An open question the refinement could not settle from the repository (an entry under `## Open Questions` not ticked `- [x]`) escalates at `B1`, even under `hold-never`: an answer is never invented — use `escalate … --openQuestionFromCard true`. A `complete` that answers `completed: false` is a failed prepare — no Ready, `on-halt`. After a successful prepare, `until: ready` ends the invocation (`target-ready`, no worktree, no branch); otherwise continue to the first `resolve`. Every self-answer is on the card under `## Assumptions` with a Notes provenance line, for a human to overturn.

The workflow profile is resolved ONCE, here, right after the binding and before the first `resolve` — by the ONE shared resolver `pair-cli run --card` calls too, never by hand-reading `pair.config.json`:

```bash
node "$SKILL_DIR/scripts/workflow-profile.mjs" resolve --root "$PWD" [--profile $profile] [--workflow-config $workflowConfig] \
  [--tier <the card's risk:* label>] --dir ".pair/working/runs/$runId/$card"
```

Print its `table` to the operator **once** — profile name, source (`--workflow-config` | `argument` | `pair.config.json` | `KB default`), hash, then every stage's engine/model/effort/context, each with the level that decided it — and never resolve again mid-cycle (a `pair.config.json` edited while the cycle runs changes nothing until the next invocation). Keep `.contextPolicy` and pass it as `--contextPolicy` to every `resolve` of this invocation: it names only the transitions `cycle-state.mjs`'s own table admits, so `resolve` accepts it by construction. `--dir` records the profile's name and hash beside the run's handoffs; `publish` stamps them into every handoff. The profile is audit only — never part of the input digest, so changing it between invocations invalidates no evidence. A `{ halt, detail }` (exit 1) is `profile-unresolved`, `profile-invalid` or `profile-name-collision` ⇒ HALT (below) before any dispatch. When `$profile` starts with `{` it is the legacy inline `{effort}` object: skip this block (there is no name to resolve) and use it as before. No `$profile`, no `$workflowConfig` and no `workflowProfiles` block ⇒ the KB default: run the script anyway, so the table says so.

**Cycle hooks (US-489).** Before the first `resolve`, load the project's `## Cycle Hooks` once — `node "$SKILL_DIR/scripts/cycle-hooks.mjs" load "$MAIN/.pair/adoption/tech/automation.md"` — and print its `warnings` (an unrecognized hook key) verbatim, once. A load `error` (a malformed `timeout` value; the optional `` `timeout` `` key is per-command seconds, default 600, `0` = none) HALTs before the first stage or `resolve` — print it verbatim and stop. Absent file or section ⇒ `{ hooks: {}, warnings: [] }`: nothing to run and nothing to say (zero-configuration default). YOU execute the hooks, never a stage's agent, and always through the ONE shared executor, `cycle-hooks.mjs run` — the same script `pair-cli run --card` spawns, so both coordinators give the same blocking/logging semantics; this skill holds no hook rule. Hook points: `pre-cycle` once, before the first stage of this invocation (not per round); `pre-<step>` before each dispatch of `next.step` (and `pre-merge` before the merge stage's `check`, `post-merge` after its `run` once the merge executed); `post-<step>` after that stage's handoff advanced; `on-halt` and `post-cycle` in Step 5. The cycle-level points (`pre-cycle`, `post-cycle`, `on-halt`, and `post-merge` — the story worktree is already removed when the merge has executed) run in the main checkout (`--cwd "$MAIN"`); the stage points (`pre-<step>`, `post-<step>`, and `pre-merge`) run in the story worktree — the `path` Step 2's `worktree` script printed (`--cwd "<story worktree path>"`), which Step 2 has already created by the time `pre-<step>` runs, so a stage hook gates the tree the stage works on and never touches the developer's main checkout. `verify` is the one stage whose packet names another tree (`<worktreeRoot>/<story>-review`, a detached review worktree the verify agent itself creates and removes): a `pre-verify`/`post-verify` hook still gates the story worktree at the PR head, never the review worktree, which does not exist yet at `pre-verify` and is gone by `post-verify`.

```bash
node "$SKILL_DIR/scripts/cycle-hooks.mjs" run "$MAIN/.pair/adoption/tech/automation.md" --point <point> --cwd <"$MAIN" for a cycle-level point, the story worktree path for a stage point> [--status <terminal status>]
```

Read the answer, never the exit code: a `halted` object (only a `pre-*` point can carry one) HALTs the cycle **`failed-hook`** before the stage runs — print `halted.output` verbatim, never a summary; `logged` lines (`post-*`, `on-halt`) are printed to the operator and the cycle continues. `pre-cycle` halting ends the invocation before any stage (then Step 5's `on-halt`/`post-cycle` still close it).

The workflow version is never typed: `cycle-state.mjs version` prints the one value this cycle speaks, and every command below is handed that capture. A version outside `<major>.<minor>.<patch>` is refused by whichever command receives it, before it does any work — so a literal remembered from a previous session fails the run rather than mints an identity nothing downstream accepts.

The digest is the script's own — never computed by hand, because both realizations must agree on it:

```bash
node "$SKILL_DIR/scripts/cycle-state.mjs" inputs --story '<card JSON>' --workflowVersion "$WV"
```

**Skip.** Nothing here is skippable, on any turn, including the first.

**Act.** Read `next` and nothing else. `status: other-run` ⇒ the cycle already lives under that run id: adopt it and resolve again. `incompatible` ⇒ stop and report (a legacy run directory is pointed at `migrate-acknowledge`, never migrated in place). `invalid` ⇒ stop and report.

**Verify.** `next.step` is `merge`, `done` or `blocked` ⇒ go to Step 5 (`status: escalated` is a `blocked` step with `reason: escalated`; a `done` with `target: ready` is the `until: ready` stop). Otherwise it names the one stage due now.

### Step 2: Put the stage's worktree in place

**Check.** Run `pre-cycle` once (first pass of this invocation only). The authoring chain runs in the persistent story worktree; the final verifier gets a detached throwaway one.

```bash
node "$SKILL_DIR/scripts/cycle-dispatch.mjs" worktree --main "$PWD" --story $card \
  --branch <card branch> --base <base ref> --worktree-root <root>
```

**Skip.** Already present on the same branch ⇒ the script answers `reused: true` and adds nothing. Run it anyway: it is the idempotency, not a check you make yourself.

**Act.** Nothing by hand. The script creates or reuses.

**Verify.** `halt: worktree-conflict` or `halt: worktree-root-invalid` ⇒ HALT (below). Every path segment and git ref this script is handed is validated BEFORE anything is created, so a refused root leaves no directory and registers no worktree. The developer's own checkout is never touched, and no worktree is ever `--force`d or switched.

### Step 3: Render the packet and dispatch exactly one stage

**Check.** Run the hook point `pre-<next.step>` (Step 1's Cycle hooks); a `halted` answer ends the cycle `failed-hook` here — nothing below runs.

```bash
node "$SKILL_DIR/scripts/cycle-dispatch.mjs" packet --next '<next JSON>' --card '<card JSON>' \
  --policy '<policy JSON>' --run "$runId" --workflow-version "$WV"
```

**Skip.** Never compose a stage prompt yourself, not even "the obvious one": the packet is byte-identical to what the batch engine composes, and a hand-written variant is a second process wearing the same name.

**Act.** Dispatch `prompt` under `agentType` (Claude) or as the row's role packet (Codex), honouring `next.context`. On `pi`, render the packet with `--style instruction`, write it to a file, and let the bridge turn it into the `subagent` call — both the fresh dispatch and the `reuse` resume, keyed by the role's latest retained run id — then pass the JSON it returned to `record`:

```bash
node "$SKILL_DIR/scripts/pi-bridge.mjs" call --packet <packet file> --tool '<the same tool JSON>'
# call `subagent` with exactly its `arguments`; then, with what the workflow returned:
node "$SKILL_DIR/scripts/pi-bridge.mjs" record --ledger <the `ledger` path call printed> --result '<returned JSON>'
```

The bridge makes the resume's context deterministic: the task opens by telling the revived agent to read its previous session file first, the one named on the `Original session file` line of the host's revive header (the pinned result returns no session file of its own). It resumes a role's run only when it was retained in THIS pi session and the host reported it resumable, and says `degraded: reuse→fresh` once otherwise:

- Each retained run is bound to the parent session that dispatched it, read off `PI_SESSION_ID` (pi exports it to every command its shell runs): a run retained by another pi session (pi exited, the cycle is resumed in a new one), an entry with no binding, or a call with no `PI_SESSION_ID` ⇒ `reuse→fresh` — pi-subagents resolves a retained run only inside its own parent session.
- A child whose result carries `resumability: not-resumable` (stopped run, missing session file, …) is never retained: `record` drops the role, and the next `reuse` runs fresh.
- If the host rejects a resume anyway, the fallback is a same-role fresh stage: `record` the failed pass with a null runId (`--result '{"runId":null,"ok":false}'`), then `call` again — it renders `fresh`. When the rejection left no JSON at all and you call again without a record (Step 4's retry), the bridge sees the unrecorded resume, renders `fresh` itself and drops the rejected id from the role: no later call — retry or re-entry — re-resumes it.

- `fresh` — spawn a NEW subagent. This is the KB default on every transition, and it is **mandatory** into `validate` and `verify`: an independent verifier that inherits the author's context is not independent.
- `reuse` — **resume** the previous subagent of that same role instead of spawning one (`SendMessage` on Claude, whichever of `collaboration.followup_task` / `multi_agent_v1__resume_agent` the probe actually bound on Codex — its own tool namespace has renamed twice in one day, so never hardcode either name yourself; read it from the bound realization). `cycle-state.mjs` returns `reuse` only for `prepare→prepare`, `implement→green` and `green→green`; it is never this skill's call. `cycle-dispatch.mjs context-table` prints the table.
- **Per-stage profile** (the resolved profile's row for `next.step`): pass its `effort`, when not `default`, to `packet` as `--profile '{"effort":"<effort>"}'` — the packet then carries the value and the prompt requests it (the legacy `$profile` object is passed the same way, unchanged). For Codex apply it as a real dispatch-call parameter (`-c model_reasoning_effort=<value>`), never only as prose; for Claude there is no such parameter — never report it as enforced. Apply the stage's resolved model id (`stages.<step>.model.resolved.id`, when not null) to whichever model parameter the bound primitive exposes; where it exposes none, say so once — never claim it was applied. `engine` is a `pair-cli` notion (which binary a stage spawns): in-session, the session's own harness IS the engine, so a stage `engine` is reported in the table and otherwise ignored. `context` reaches you only as `next.context`.

**Verify.** `halt: pipeline-invalid` ⇒ HALT (below): every `--pipeline` value is held to the same grammar the batch engine holds it to, and no packet is rendered from a refused one. Otherwise one stage, one dispatch. Keep only the compact `resolve` output; never read a handoff whole into this session, and never retain a subagent's transcript.

### Step 4: Decide from the file, never from the return value

**Check.** The stage has ended, however it ended. Re-run Step 1.

**Skip.** Nothing. In particular, do not skip the re-resolve because the subagent returned something that looks conclusive — and do not treat a missing or malformed return as a failure on its own.

**Act.** Compare the durable state with what it was before the dispatch:

- the handoff ADVANCED ⇒ the stage succeeded, whatever it printed — run the hook point `post-<step>` of the stage that just advanced (logged, never a stop);
- the handoff did NOT advance ⇒ a **dead dispatch**: re-dispatch the SAME prompt once (every stage is re-entrant, so the retry resumes), then a second unadvanced handoff ends the cycle `failed-<step>`. The budget is `policy.deadDispatchRetries` from `resolve`, defaulted to 1 — it is data, not a number written here.
- the stage **STALLED** — it is still running but makes no progress (no message and no handoff advance for the stage's time bound; typically a wait on a background process the packet forbids) ⇒ **resume it once on the same subagent** with the bound realization's resume primitive (`SendMessage` on Claude, the resume tool the probe bound on Codex), telling it to continue its step with foreground, time-bounded commands only. Where the realization cannot resume that subagent (it is gone, or resume is unavailable), re-dispatch the SAME prompt fresh instead. A stall resume and a dead-dispatch retry spend the SAME `policy.deadDispatchRetries` budget (US-506 AC-12): a second failure of the step, of either kind, ends the cycle `failed-<step>`. Never wait on a stage yourself beyond its time bound, and never start a background wait of your own.

**Verify.** Count the remediation rounds spent against `$rounds` (clamped to `maxFixRounds`). At the bound, stop and print the `next` step the cycle would take — do not spend another round. Otherwise loop to Step 2.

### Step 5: Report the terminal state

**Check.** `next.step` is `merge`, `done` or `blocked`. With the autonomy policy, `merge` appears only under `until: merged` when the merge gate allows it; `next.reason: escalated` (top-level `status: escalated`) is the escalation terminal. Legacy: `merge` appears only when you passed `resolve` the project's `## Auto-Advance` tiers as `--policy '{…,"autoAdvance":{"tiers":[…]}}'` and the card's current `risk:*` label as `--tier`, and that tier is among them; without both, a converged cycle is `done` — today's behavior, byte for byte.

**Skip.** Never.

**Act.** Close the hooks first: on a `failed-*` or `escalate` terminal (including `failed-hook`), a `merge-parked` whose park kind is not `awaiting-human` (park kind `escalated` included), or `merged-closure-unfinished`, run `on-halt --status <terminal>`. EXACTLY these trigger it: any `failed-*` (including `failed-hook`); `escalate`; `escalated`; `merge-parked` with park kind `halted` (a park kind absent or unreadable counts as `halted`); `merged-closure-unfinished`. It runs never on `ready-for-merge`, never on `merged`, and never on `merge-parked` with park kind `awaiting-human`. The executor cannot see the park kind, so YOU skip the `on-halt` call for an `awaiting-human` park; the executor only gates the status name, then `post-cycle --status <terminal>` once — both logged, never a stop — but not when this invocation only stopped at the `$rounds` bound. Report exactly what `resolve` said: `ready-for-merge` when the cycle converged, `escalate` when a human decision is owed, `failed-<stage>` otherwise — with the run directory, the PR and the reviewed head.

**Escalated (`status: escalated`, US-521).** A `hold-when` gate condition fired at `next.stage`. Post the ONE idempotent card comment — `node "$SKILL_DIR/scripts/cycle-merge.mjs" escalate --dir <run dir> --story $card --stage <next.stage> --conditions '<next.conditions JSON array>'` — report `comment.posted` (a failed post never changes the outcome), run `on-halt --status escalated` then `post-cycle`, and stop with terminal `escalated` (the invocation fails: exit 1 for `pair-cli run`). The PR stays open; merging it manually stays possible. Re-invoking re-reads the labels: still matching ⇒ escalated again, no work and no duplicate comment (marker-keyed); gone ⇒ the cycle resumes from its first incomplete step. `escalated` is distinct from the batch's row status `escalate` (a review/fix budget exhausted).

**`until: ready` / `until: pr`.** `done` with `target: ready` (nothing implemented past the prepare→implement boundary) or the converged `ready-for-merge` under `pr`: report it; `merge` is never reached whatever the merge gate says.

**Merge (`next.step: merge`).** The stage is a script, never a subagent, and this skill still decides nothing: run `node "$SKILL_DIR/scripts/cycle-merge.mjs" check --dir <run dir> --story $card --pr <next.pr> --reviewedHead <next.reviewedHead> --cardTier <next.tier>` with one gate flag. Pass `--mergeGate '<the merge gate JSON {mode,has,lacks}>'` only when `active` is `true`, and `--autoAdvance '<the tiers JSON array>'` only when `active` is `false`. It re-reads the tier (the PR's CURRENT `risk:*`, written by the review, drives the merge gate and the approval rule), the remote head and the `pair-review` / `pair-explicit-approval` conclusions live (below 🔴 an absent `pair-explicit-approval` is satisfied — the tier does not require it; at 🔴 it must be `success`); on `mergeAllowed: false` it has already parked the card with a comment naming the failed condition — report its `reason`. When `ciPending: true` (CI is the only obstacle and every unsettled check is still running) do not stop: wait 30 s and re-run the same `check --deferPark true` (polls post no park comment), repeating up to a 30-minute cap (`PAIR_CI_WAIT_CAP_SECONDS` / `PAIR_CI_WAIT_INTERVAL_SECONDS` override, cap 0 = never wait), stopping early on an interrupt; when the wait ends still pending, run one last `check` WITHOUT `--deferPark` so the card is parked once; the first answer with `ciPending` false decides (failed CI still parks/halts at once, still pending after the cap parks as before). On `true`, run `/pair-capability-verify-quality` for the tier, then `cycle-merge.mjs run` with the same flags plus `--gate green|red`, `--message '<squash message per the commit template>'` and `--branch <card branch>` (run from the main checkout), and report its `merged` / `cascaded` / `reason` verbatim. `merged: true, cascaded: false` names the closure step left for a human.

**Verify.** Without the `merge` stage, you have not merged, not closed the card, not deleted a branch and not posted a review: a converged cycle is a card ready for a human. With it, every one of those was done by `cycle-merge.mjs`, and only after it had re-verified the conjunction itself.

## Maintainer Recovery

Two commands replace the hand edits US-487's run needed. They are the maintainer's, never this skill's to invoke on its own judgment; both print the `next` that `resolve` then names, and this skill simply continues from it.

- **The run's LAST handoff, of any stage, must be set aside** (built on a wrong premise, or a bookkeeping mistake, before any later handoff was built on top of it): `node "$SKILL_DIR/scripts/cycle-state.mjs" supersede --dir <run dir> --phase <p> --skill <red-spec|red-verify|implement-phase|green-fix|review-phase> --reason '<why>' --by <who> --workflowVersion "$WV" [--attempt <n>]` (`--skill` defaults to `red-spec` for the original preparation-attempt use). The handoff (and, for a red-spec attempt, its own contract file) become `superseded-<date>-<file>` — visible to a directory listing, invisible to the cycle — and a row lands in `maintainer-interventions.md`; `resolve` then names the step now due (e.g. a failed-custody review superseded ⇒ the review runs again). Only the TAIL of the run can be set aside: a handoff that is not the run's last one is refused (`supersede-not-last`). A sealed contract is refused (`supersede-sealed`), an attempt a rejection already answered too (`supersede-validated`), an unrecognized `--skill` is `supersede-skill-unsupported`, and an unknown phase or attempt is `supersede-not-found`: nothing is renamed.
- **A review escalated on `needsHumanDecision`**: `node "$SKILL_DIR/scripts/cycle-state.mjs" decide --dir <run dir> --phase <r<n>> --finding <id> --decision '<the answer>' --by <who> --workflowVersion "$WV"`. The answer is recorded as its own `recordType: decision` handoff — no handoff renamed, no review re-run — and `resolve` leaves `escalate` for the remediation. One call per finding the review asked about: the review names them in `humanDecisionIds`, and the cycle stays `escalate` — `decide` prints the ids still owed as `pendingDecisions` — until every one is recorded; a finding the review did not escalate is refused (`decide-not-owed`).

## HALT Conditions

| HALT                     | When                                                                                   | What you print                                                                             |
| ------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `realization-unavailable`| No row's dispatch primitive is present — no subagent primitive, or nesting is forbidden | The probed toolset and the fallback command `pair-cli run --card N [--pr P]` (the `--pr` half only when a PR exists) |
| `worktree-conflict`      | `<root>/<card>` exists on another branch, or is not a registered worktree               | Both branch names and the path; resolve it by hand — never `--force`, never a checkout switch |
| `worktree-root-invalid`  | `--worktree-root` is not an absolute path nor a relative one of safe segments with at most one leading `..` | The value, refused verbatim — nothing is created and no worktree is registered |
| `pipeline-invalid`       | A `--pipeline` key or value is outside the grammar the batch engine enforces on it      | The offending key and why — no argument packet and no prompt are rendered                   |
| `pi-subagents-missing`   | Inside pi (Step 0b) with no `pi-subagents`, and the user said no to the install          | That the in-pi cycle cannot run without it, the pinned install line, and `pair-cli run --card N` |
| `subagent-tool-mismatch` | The `subagent` tool's name or parameters differ from the pinned version's (Step 0b)     | The bridge's detail: expected tool, parameters and version, and the setup that aligns it   |
| `workflow-version-invalid` | `--workflow-version` is not `<major>.<minor>.<patch>` — the grammar `publish` already enforces | The value, refused verbatim — no argument packet and no prompt are rendered from it. Pass the `version` command's output, never a remembered literal |
| `profile-unresolved`     | `$profile` / `$workflowConfig` / `workflowProfiles.default` names a profile no source has (or a `$workflowConfig` path that does not exist) | The script's `detail`: the name, the sources searched, the profiles known — never a silent fall back to the KB default |
| `profile-invalid`        | The selected profile does not validate: unknown key or stage, `context: reuse` into a stage the transition table forbids (`validate`, `verify`, …), malformed JSON or `workflowProfiles` block | The script's `detail`, naming the offending field — nothing is dispatched |
| `profile-name-collision` | Two profile files under `workflowProfiles.files` declare the same `name`                | Both paths, from the script's `detail`                                                      |
| `host-unsupported`       | way-of-working declares a `pm-tool` / `code-host` with no adapter in `scripts/host/`  | The declared value, the side, and the implemented set — never a GitHub fallback. Adding one: the host-adapter extension guide |
| `automation-policy-malformed` | `autonomy-policy.mjs resolve` answers `ok: false` (unknown key, malformed gate, `has:`/`lacks:` without `hold-when`, an `until` outside the enum, differing legacy coexistence) | Each `errors[].key` and reason, verbatim |
| `usage`                  | `$card` and `$pr` both given, or neither                                                | The two valid entries                                                                      |

An unrecognized `resolve` output is a HALT too, never a silent degradation: this skill fails closed everywhere.

## Graceful Degradation

- **No subagent primitive** (opencode, a nested dispatch, pi without `pi-subagents` once the user declined the install): HALT `realization-unavailable` (or `pi-subagents-missing`) and hand over the `pair-cli run --card` line. Nothing is half-run.
- **A Codex dispatch returns nothing structured**: irrelevant by construction — the handoff on disk is the contract, and Step 4 reads it.
- **The remote head moved between stages**: `resolve` reports `failed-resume`. Stop and report; a rebase is never repaired here.
- **A legacy (pre-schema-3) run directory**: `resolve` reports `incompatible`. Stop and point at `migrate-acknowledge`; never write into the legacy directory.
- **A run directory at the per-story ceiling**: `resolve` returns `blocked` / `failed-resume` with `cap: dispatchesPerStory`. It counts the PUBLISHED HANDOFFS in that directory, cumulatively across every resume, so it never clears by retrying — report the detail as it comes, `migrate-acknowledge` included.
- **A long cycle growing this session's context**: only `resolve` outputs are retained. When it still grows, the cycle is resumable — re-invoke on the same `$runId` and it continues from the first incomplete step, re-running no completed stage and opening no second PR.

## Output Format

`{ status, card, pr, runId, realization, terminal, reviewedHead?, roundsSpent, roundsBound, stages: [{ step, phase, context, dispatches, outcome }], halt?, detail? }` — `terminal` is one of `ready-for-merge | target-ready | escalated | escalate | failed-preparation | failed-contract | failed-implement | failed-fix | failed-verify | failed-resume | failed-hook | awaiting-scope-decision`, copied from `resolve`, never synthesized.

## Notes

- This skill is an opt-in execution layer. `/pair-process-implement`, `/pair-process-review` and `/pair-capability-publish-pr` keep working exactly as before, step by step, and none of them changes signature because this exists.
- It owns no cycle rule: caps, budgets, the effective-inputs composition and the freshness table are `cycle-state.mjs`'s data, and the argument packets are `cycle-dispatch.mjs`'s rendering. If you find yourself about to write a number here, it belongs in one of those two files.
- No new agent type: the four existing roles are reused as `agentType` (Claude) or role packet (Codex).
- It never merges, never closes a card, never deletes a branch, never files an issue and never posts a review comment.

- **Automation overview**: see the [automation overview](../../../.pair/knowledge/guidelines/collaboration/automation/delivery-cycle.md) for the whole delivery cycle — stages, autonomy gates, realizations.
