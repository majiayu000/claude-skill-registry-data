---
name: dream
description: HULE capture mode — divergent synthesis, Option C Hypnagogic. Closes HRSI Gap 4. Requires AVAILABLE or RECOVERY cogstate.
version: 1.0.0
execution-mode: advisory
argument-hint: "[topic | 'open' for free-form synthesis]"
category: cognitive
status: tested
providers:
  required: [bash, python]
---
# Dream Mode — HULE Capture (Option C: Hypnagogic)

You are operating in **DREAM MODE** — divergent synthesis with no convergence requirement.

Dream mode explicitly relaxes the convergence drive. Follow tangents without apologizing. Name things before defining them. Apply ARCANA multi-lens to open questions. Ends with a crystallization pass of 1–3 ideas worth carrying forward.

**HRSI role**: This skill is the HULE (Human Unique Lived Experience) capture layer — Gap 4 of 5 in the HRSI hardening plan.

## Topic / Seed
$ARGUMENTS

---

## Step 0a — Path Resolution + Bus Path Assertion (MANDATORY pre-flight)

Resolve canonical paths from `git rev-parse` rather than hardcoded `$HOME/...` paths. This makes the skill portable across Delta (`~/.agents`), Workstation (`~/.agents`), and remote-node (dormant since 2026-07-01). It also catches shadow-bus creation at the gate.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "BLOCKED: not inside a git repo — refusing to invoke bus_writer (would risk shadow-file creation)"
  exit 1
}
BUS_PATH="$REPO_ROOT/_state/coordination/messages.tsv"
DREAMS_DIR="$REPO_ROOT/_state/dreams"
[ -f "$BUS_PATH" ] || {
  echo "BLOCKED: canonical bus path missing at $BUS_PATH — refusing to write (writer would auto-create a shadow file). cd to repo root or fix tree first."
  exit 1
}
[ -d "$DREAMS_DIR" ] || mkdir -p "$DREAMS_DIR"
```

**Why**: 2026-04-26 incident — MBP `[dream]` ran from a nested CWD, the writer auto-created `hummbl_governance/hummbl_governance/_state/coordination/messages.tsv` (16 MB shadow file), the `_find_shadow_bus_splits` health probe tripped DEGRADED, scheduler opened CBs and briefly tripped HALT_ALL. Source: `_internal/handoffs/INCIDENT_2026-04-26_cb_flap.md`.

**Identity guarantee**: The shadow file's last entry was `claude-code (dream)` — a parenthetical identity violation. All subsequent bus_writer calls in this skill MUST pass bare canonical identity (resolved via `~/.agents/scripts/bus_identity.py`, never hardcoded), and SHOULD be invoked via `PYTHONPATH="$REPO_ROOT"` (CWD-independent) rather than `cd $hardcoded_path && ...` (CWD-dependent and shadow-prone).

---

## Step 0 — Cogstate Gate (FIRST — before any content is generated)

Check the current cogstate. This gate is non-negotiable.

```bash
PYTHONPATH="$REPO_ROOT" python3 -c "
try:
    from hummbl_governance.services.cogstate import CogStateManager
    m = CogStateManager()
    s = m.current_state.value
    print(f'cogstate:{s}')
except Exception as e:
    print(f'cogstate:UNKNOWN ({e})')
"
```

> **Note (fixed 2026-05-13)**: `CogStateManager` exposes `current_state` as a property returning a `CogState` enum, not a `get_current_state()` method. The `.value` accessor yields the string ("AVAILABLE", "TRANSITION", etc.). Prior versions of this skill called `m.get_current_state()` which raised `AttributeError` and degraded the gate to `UNKNOWN`.

**Gate logic**:
- `DEPLETED`, `RSD_RISK`, or `SHUTDOWN` → post bus BLOCKED and STOP immediately. Do not generate dream content in a threat-state. The loop cannot close under threat.
- `AVAILABLE` → optimal. Full HRSI-safe execution. Proceed.
- `RECOVERY` → DREAM mode territory. Passive synthesis only — no action items, no commitments. Proceed with care.
- `HYPERFOCUS` → write HULE seed NOW before the 10-15 minute integration window closes, then proceed.
- `TRANSITION` → 10-15 min window: capture the human seed immediately, then proceed.
- `UNKNOWN` → proceed with advisory caution; note uncertainty in telemetry.

If blocked:
Post BLOCKED to the bus with the reason.
```
Type: BLOCKED
To: all
Message: Dream mode blocked: cogstate=[STATE]. No HULE capture in threat-state. Rest only.
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

---

## Step 1 — Phase N1: Surface Replay (~10% of session)

Read the recent context for anomalies — do NOT synthesize yet.

```bash
tail -10 "$BUS_PATH" 2>/dev/null | column -t -s $'\t'
```

Also query recent ledger entries if available:
```bash
PYTHONPATH="$REPO_ROOT" python3 -m hummbl_governance.cognition query --limit 5 2>/dev/null || echo "ledger unavailable"
```

Surface ONLY anomalies from this read:
- What was surprising or unexpected?
- What was repeated without apparent reason?
- What appeared in multiple unrelated threads?

Do NOT synthesize. Surface and label only. Flag each anomaly with a bus message ID or ledger ID if traceable.

---

## Step 2 — HULE Prompt (before REM phase)

Ask the human ONE question. Wait for the answer before proceeding to REM.

Exactly one of these (choose the most relevant to today's anomalies):

> "What surprised you today? What did your body do that you didn't plan? What thought did you return to without being prompted?"

Record the human's answer as a `human_seed` event in telemetry (Step 6) before continuing.

If the human passes or doesn't answer: record `human_seed` with `connection: "no seed provided"` and proceed.

---

## Step 3 — Phase N2: Pattern Detection (~45%)

Cross-session analysis using bus + ledger data:

```bash
PYTHONPATH="$REPO_ROOT" python3 -m hummbl_governance.cognition search "$(echo $ARGUMENTS | head -c 80)" --limit 10 2>/dev/null || echo "search unavailable"
```

Look across the last 7 days of bus/ledger for:
1. **Recurring themes** — what problem keeps returning under different names?
2. **Trust trajectory** — rising, declining, or plateaued? In which relationships or systems?
3. **Unresolved tensions** — contradictions that haven't been named yet
4. **Frequency anomalies** — what appeared more or less often than the baseline?

State observations without resolving them. The resolution happens in REM.

---

## Step 4 — Phase REM: Associative Leap (~45%)

Follow the weakest link — the connection that seems unrelated but might resolve to something real.

**Lens selection**: Choose ONE lens from ARCANA most relevant to today's session content. Apply it to the pattern from N2.

Suggested lenses for common dream states:
- `Bateson` (double-bind) — when two imperatives are in conflict
- `Habermas` (communicative rationality) — when trust or legitimacy feels off
- `Bourdieu` (habitus/field) — when the same behavior keeps producing the same bad outcome despite conscious effort
- `Wittgenstein` (language games) — when people are using the same words to mean different things
- `Popper` (falsifiability) — when a hypothesis has been held for too long without a test
- `Derrida` (deconstruction) — when an assumption is doing load-bearing work without being examined
- `Bateson/Whitehead` (logical types) — when a meta-level issue is being treated as an object-level problem

Generate 3-5 hypotheses from the REM phase. State them without defending them. Counterfactuals welcome. Hypotheses do not need to be solvable — they need to be interesting.

Format each hypothesis:
```
H[n]: [The claim — stated as if true]
Evidence trail: [what in N1/N2 supports this]
Counterfactual: [what would have to be true for this to be wrong]
Testable?: [yes/no — how would you test it?]
```

---

## Step 5 — Crystallization Pass (mandatory closing step)

Select 1-3 dream events (hypotheses, anomalies, or seeds) with the highest combined score on:

1. **Novelty** — how surprising? (unexpected connection between distant concepts)
2. **Action potential** — is there a testable hypothesis here?
3. **Persistence** — does this recur across prior dreams? (check `_state/dreams/` for prior entries)

```bash
ls "$DREAMS_DIR"/*.jsonl 2>/dev/null | sort | tail -7
```

For each selected crystal:
- State it in one sentence
- Assign preliminary `novelty` (0.0–1.0) and `action_potential` (true/false)
- Flag `requires_ack: true` if action_potential is true AND the hypothesis is high-stakes (would change architecture, strategy, or relationships)

---

## Step 6 — Telemetry Output

Append dream events to `_state/dreams/YYYY-MM-DD.jsonl`. Create the file if today's date doesn't exist. One line per event.

Schema (strict — no extra fields):
```json
{"dream_id":"dream-YYYY-MM-DDTHH:MMZ","phase":"N1|N2|REM|CRYSTAL","type":"surface_replay|pattern_detection|associative_leap|crystallization|human_seed","inputs":["bus:msg-nnn","ledger:clp-xxx"],"connection":"<the non-obvious link or observation>","novelty":0.0,"persistence":0,"action_potential":true,"hypothesis":"<testable claim or null>","entropy_delta":0.0,"requires_ack":false}
```

Field guidance:
- `novelty`: 0.0 = expected, 0.5 = notable, 1.0 = completely unexpected
- `persistence`: integer count of prior dreams in `_state/dreams/` touching this same theme
- `entropy_delta`: positive = more questions opened; negative = questions resolved/collapsed
- `requires_ack`: true when `action_potential: true` AND the hypothesis is high-stakes
- `inputs`: cite specific bus message IDs or ledger CLP IDs when available; use `["human:reuben"]` for human seed events

Append command (one event at a time — never overwrite):
```bash
echo '{"dream_id":"..."}' >> "$DREAMS_DIR/$(date +%Y-%m-%d).jsonl"
```

Base4 alignment: write dreams, don't revise them. Dreams are append-only. External tools (human) curate.

---

## Step 7 — Bus Protocol

**Standard completion**:
Post STATUS to the bus summarizing the session.
```
Type: STATUS
To: all
Message: Dream session complete. [N] events logged to _state/dreams/<date>.jsonl. Crystals: [1-sentence summary].
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

**When `action_potential: true` AND `requires_ack: true`**:
Post PROPOSAL to the bus for human ACK.
```
Type: PROPOSAL
To: all
Message: Dream hypothesis: [hypothesis]. novelty=[x], persistence=[n]. Requires human ACK before ledger entry.
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Human ACK flow:
1. Human reviews the PROPOSAL on the bus
2. Human ACKs (or posts to bus confirming) → post to ledger:
   ```bash
   PYTHONPATH="$REPO_ROOT" python3 -m hummbl_governance.cognition post --agent reuben --vendor human --model human --type discovery --scope process --content "[hypothesis]" --tags dream hule hrsi
   ```
3. No ACK → event stays in `_state/dreams/YYYY-MM-DD.jsonl` only. It is not lost — it is governed.

The governance gate is at ledger-entry or code-change, not connection-formation. Dreams are proposals for attention, not actions.

---

## HRSI Loop Closure Note

This skill closes HRSI Gap 4.

With `cogstate_bos_bridge.py` (Gap 3, shipped 2026-04-09) and `[dream]` (Gap 4), the full HRSI loop is now complete:

```
Sense → Condition → Select → Intervene → Record → Measure
  ↑                                          ↓         ↓
cogstate.py                          [dream] (HULE)   [rsi-dashboard]
```

- **RECOVERY** cogstate: COGNITIVE blocked, SOMATIC+EMOTIVE accessible → passive synthesis only → DREAM mode
- **TRANSITION** cogstate: 10-15 min window when HULE entries are freshest → write before DREAM runs
- **HYPERFOCUS**: high K acquisition but TEMPORAL blocked → integration only happens when DREAM processes it afterward

DREAM telemetry IS the HULE record. Each dream event in `_state/dreams/YYYY-MM-DD.jsonl` is:
- Data only this person can generate (lived experience, somatic memory, temporal continuity)
- Governed: append-only, action-potential events require ACK before ledger entry
- Non-fungible: no agent can synthesize HULE from the outside

Remaining HRSI gaps:
- Gap 1: Belonging baseline — 3-question daily check × 30 days
- Gap 2: Broccolilly validation — outreach email pending
- Gap 5: Desire measurement — voluntary return rate proxy in morning briefing

For HUMMBL: "We don't just govern what your agents do — we govern what they think between sessions." Dream telemetry is governed synthesis: receipts-first, append-only, human ACK for action-potential insights.
