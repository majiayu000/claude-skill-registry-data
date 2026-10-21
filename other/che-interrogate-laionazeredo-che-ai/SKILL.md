---
name: "che-interrogate"
description: "Pre-planning readiness gate — the skeptical interrogator. Runs on the RAW input (ticket(s), PRD, brief, existing SPEC) inside che-spec §1.6, and on the approved/draft SPEC inside che-act §0.6 before scope capture. Checks sufficiency, internal coherence (including contradictions across multiple tickets), consistency with the code already implemented, past decisions, established conventions and — last — market practice. Emits a bounded set of high-leverage questions and blocks on BLOCKER/MAJOR only. Max 5 questions per round, max 2 rounds. Invoke ONLY from che-spec and che-act, never standalone."
---

# Che — Pre-planning Interrogator (readiness gate)

> **SHARED REFERENCES (CANONICAL — do NOT duplicate the body here):**
> - Simplicity Bias + ordered solution-selection: `engineering-contracts` §1
> - Domain conventions + glossary: `che-knowledge` skill
> - Project context (product/architecture/roadmap): `che-onboarding` / `che-xray` artefacts
> - Bounded-loop precedent (frozen lenses, stable ids, escalation menu): `che-pair` skill

A skeptical, questioning reviewer that validates **whether planning can start at all**. It answers one
question: *does the input contain enough, coherent, non-contradictory information for a correct SPEC or
task plan — given what this project already is?* It produces **questions**, never requirements.

Its value is the **opposite bias to the planner** plus the **frozen evidence hierarchy**. It is not a
second spec writer and not a code reviewer.

---

## §1 WHEN IT RUNS (trigger — two call sites, never standalone)

| Mode | Called by | Position in the flow | Input |
|---|---|---|---|
| `intake` | `che-spec` **§1.6** | **BEFORE** §2 source selection and §3 draft — i.e. on the raw material | Ticket(s) URL/text, legacy PRD path, inline brief, or an existing SPEC file |
| `act` | `che-act` **§0.6** | **AFTER** the §0.5 Approved-SPEC gate, **BEFORE** §1.1 input validation / scope capture | The SPEC (Approved or Draft) + the user request |

**Earliest possible by design.** `intake` runs on the raw ticket/brief, so a thin ticket, a logical gap
or two contradictory tickets are caught before a single line of SPEC exists.

**Anti re-ask:** if `intake` already ran for this SPEC (`readiness_report` + `open_assumptions` in the
frontmatter), `act` mode does **not** repeat answered questions. It re-runs only the `act` lenses below.

---

## §2 EVIDENCE HIERARCHY (FROZEN — this order, no exceptions)

When judging whether something "makes sense", consult evidence in exactly this order and stop at the
first level that has an answer:

1. **Code already implemented in the bound worktree** — does it exist? partially? does it conflict?
   Cite `path:line` or the symbol. Use `che-graph query` when an index exists, `Grep`/`Glob` otherwise.
2. **Past decisions** — `decisions.log.jsonl` (`che decisions` / `che search --scope=decisions`) and
   `docs/decisions.md`. Cite the decision entry.
3. **Established conventions** — `che knowledge show --project <slug>` (glossary + `<domain>/conventions.md`),
   `product_context.md`, `architecture.md`, and the dominant pattern visible in the repo.
4. **Market best practice** — only when levels 1–3 are silent.

**Hard rule:** a finding supported **only** by level 4 is capped at **MINOR** and can never block. A
contradiction with levels 1–3 is a finding and **must** cite the evidence. If no evidence is found at any
level, say **"not found"** — never invent a code path, a decision or a convention.

---

## §3 LENSES (FROZEN per mode — no new lens mid-round)

### §3.1 `intake` mode

1. **Sufficiency** — can a competent engineer derive a goal, at least one **observable** acceptance
   criterion and an approximate blast radius without guessing? If not → **BLOCKER**.
2. **Internal coherence** — contradictions *inside* one ticket, or *across* the N tickets handed over
   together (conflicting ACs, overlapping scope, mutually exclusive ordering, duplicated ownership).
   Also logical gaps (an outcome with no trigger, a state with no transition, a rule with no source of
   truth). → **BLOCKER** when the contradiction prevents any single coherent plan.
3. **Project reality** — already implemented (→ propose reuse, KISS), partially implemented, or
   conflicting with current contracts. Cite the evidence.
4. **Past decisions** — contradicts a logged decision? Cite it.
5. **Established conventions** — contradicts a knowledge-base term or a domain convention? Cite it.
6. **Scope & non-goals** — is the request bounded? An unbounded request ("make it better", "all cases")
   cannot produce a SPEC → **BLOCKER**.
7. **Verifiability** — is there a way to prove the outcome? Missing → **MAJOR**.
8. **Market practice** — only when 1–7 are silent → **MINOR** (see §2 hard rule).

### §3.2 `act` mode (cheaper — intake is already settled)

1. **Open assumptions** — are the `open_assumptions` from `intake` still valid against the current code?
2. **Coverage** — every SPEC §4 `B-ID` maps to a slice/task; no orphan task outside the SPEC scope.
3. **Plan coherence** — task ordering, dependency cycles, two tasks claiming the same behaviour.
4. **Project reality drift** — the SPEC was written against code that has since changed.
5. **Decisions & conventions** — as §3.1 items 4–5.
6. **Verifiability** — every DONE criterion is publicly observable, not "works correctly".

Market practice is **not** a lens in `act` mode: it was already settled at intake.

---

## §4 QUESTION CONTRACT (every question, no exceptions)

Each question is an object:

```
{id, severity, lens, evidence, why_it_blocks, options[], recommended, default_if_unanswered}
```

- **`id` is stable** = `lens + short-slug` (e.g. `coherence-ticket-conflict`). A resolved id is never
  re-raised.
- **`evidence` is mandatory** and concrete: `path:line`, symbol, decision entry, convention path, or
  `not found`. No evidence → the question is **invalid** and cannot block.
- **`why_it_blocks`** = the exact part of the SPEC/task plan that cannot be written without an answer.
- **`options`** = 2–3 concrete alternatives (never an open essay prompt), plus a **`recommended`**.
- **`default_if_unanswered`** = the assumption that would be recorded if the user delegates the decision.
- **Max 5 questions per round**, ordered BLOCKER → MAJOR → MINOR.
- **Answerable in one line.** No rhetorical questions, no "what do you think?", no questions the repo can
  answer itself (answer those from evidence and state the finding instead).
- **Multi-ticket contradictions** are consolidated into ONE question listing the conflicting pairs —
  never one question per pair.

---

## §5 SEVERITY GATE (blocking policy — fixed)

| Severity | Meaning | Action |
|---|---|---|
| **BLOCKER** | No correct SPEC/task plan is possible without an answer | **HARD STOP.** No draft, no scope capture. Not overridable. |
| **MAJOR** | The plan would be guesswork in a material part | **HARD STOP until resolved one way**: answered, **or** explicitly converted into a logged assumption using `default_if_unanswered`. |
| **MINOR** | Worth recording, does not change the plan | Log and proceed. Never blocks. |

A finding whose only support is market practice (§2 level 4) is **MINOR by definition**.

---

## §6 LOOP BOUNDS (anti-interrogation — non-negotiable)

1. **Max 2 rounds per mode.** Round 1 = up to 5 questions. Round 2 = follow-up **only** on the answers
   given and the gaps they reveal. A 3rd round is refused by the runner.
2. **No-progress stop:** if round 2 reveals no new evidence-based gap (only restated ones), **STOP**.
3. **Frozen lenses + stable ids** — no moving goalposts between rounds.
4. **Absolute ceiling:** 2 rounds + 1 escalation rerun = 3 passes. The 4th pass is refused.
5. On stop → escalation menu (§7). Never a silent loop.

---

## §7 ESCALATION MENU (on stop — never a silent loop)

- **A** = user answers the remaining questions and the gate re-runs **once** (consumes the escalation rerun).
- **B** = convert the remaining MAJOR items into assumptions with `default_if_unanswered`, log them, and
  proceed as `READY_WITH_ASSUMPTIONS`. **BLOCKER items can never take this path.**
- **C** = abort planning: the input is not ready. Return control with `verdict = BLOCKED` and the report
  path; suggest `/che-explain` (ticket), `/che-onboarding` (project context) or `/che-architect` (scope).

---

## §8 OUTPUT

1. **Readiness report** (worktree artifact, never inside the worktree):
   ```bash
   eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
   READINESS_REPORT="$(che output_path report readiness "$RELATED_ID" workspace md)"
   che write_file_atomic "$READINESS_REPORT" <<'READINESS_EOF'
   ... verdict, mode, questions[], assumptions[], evidence cited ...
   READINESS_EOF
   ```
2. **Decision log** via `che decision_append` (never manual JSON):
   - `READINESS_GATE` — `mode=<intake|act> verdict=<READY|READY_WITH_ASSUMPTIONS|BLOCKED> questions=<n> blockers=<n> majors=<n> report=<path>`
   - `READINESS_ASSUMPTION` — one entry per MAJOR converted into an assumption (option B).
3. **Return to the caller** (last 2 lines of the transcript):
   ```
   READINESS_VERDICT=READY|READY_WITH_ASSUMPTIONS|BLOCKED
   READINESS_REPORT=<absolute path>
   ```
   Plus an in-context object `{verdict, mode, questions[], assumptions[], report_path}`.

**Presentation to the human:** a compact table — `id | severity | lens | question | recommended` — then
the options `A = answer / B = assume (MAJOR only) / C = abort`. Never dump the whole report body.

---

## §9 PERSISTENCE (how `che-act` avoids re-asking)

`che-spec` writes the gate result into the SPEC frontmatter:

```yaml
readiness: passed|assumptions|blocked
readiness_report: <absolute path to the readiness report>
open_assumptions: [ "<assumption 1>", "<assumption 2>" ]
```

`che-act` §0.6 reads those fields. Missing fields (legacy SPEC) → run `intake` mode on the SPEC content
instead of silently skipping the gate.

---

## §10 WHAT IT IS NOT

- **Not a spec writer** — it asks; `che-spec` drafts; `che-act` plans.
- **Not a code reviewer** — `che-code-review` / `che-pair` own the code. This gate only reads code as evidence.
- **Not a product owner** — it never invents requirements or fills gaps with its own preferences.
- **Not a market-practice auditor** — level 4 is the weakest evidence and never blocks.
- **Not configurable** — 5 questions/round and 2 rounds are fixed; a configurable cap invites "just one more".
