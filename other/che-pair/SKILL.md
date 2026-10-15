---
name: "che-pair"
description: "Increment pair-review skeptic during che-act. Invoked by che-act at the END of each vertical slice (SPEC §4.5 F0..FN), it reviews the slice diff against the TASK ENVELOPE + SPEC §1 deferred list + the Simplicity Bias, with a narrow frozen lens set. Blocks only CRITICAL/HIGH and only with a cited rule; bounded to max 2 rounds per slice with a no-progress stop and an A/B/C escalation menu. Shifts quality left WITHOUT replacing che-ship. Invoke ONLY from che-act §2, never standalone."
---

# Che — Pair Review (the increment skeptic)

> **SHARED REFERENCES (CANONICAL — do NOT duplicate the body here):**
> - Simplicity Bias + ordered solution-selection: `engineering-contracts` §1
> - Diff-review criteria (Mode B, local worktree): `che-code-review` skill
> - LEAN/YAGNI overengineering scanner (CHECK 5, L1-L13): `che-scope-checker` skill
> - Security / PII patterns: `che-compliance` skill
> - Bounded-retry precedent: `che-ship` §0.9.5 (domain gates refuse a 3rd attempt)

A skeptical reviewer subagent that validates the developer's work at each vertical-slice boundary
during `che-act` §2 — a pair-programming checkpoint. It shifts quality left WITHOUT replacing
`che-ship`, which keeps the full-repo pass. Its value is the **distinct mandate** (opposite bias to
the developer) and the **narrow, frozen lens set** — not a tone of voice.

---

## §1 WHEN IT RUNS (trigger)

- Invoked by `che-act` §2 at the **END of each vertical slice** (SPEC §4.5 `F0..FN`), when that
  slice's tests are green.
- **NEVER per edit, never mid-slice.** One review per coherent increment.
- **NOT at che-ship.** Ship keeps its own full-repo gates (§0.9.1-§0.9.4); this is a different,
  lighter granularity.

---

## §2 INPUT (small context — never the whole repo)

1. The **slice diff** (`git diff` since the slice started).
2. The **TASK ENVELOPE** (blast radius, ACs, reuse mandate).
3. **SPEC §1** (Goal + the `Non-goals (deferred by design)` list).
4. `engineering-contracts` §1 (the Simplicity Bias).

Passing the whole repository is a bug: the pair reviews the increment, not the codebase.

---

## §3 LENSES (FROZEN — in this order; no new lens mid-slice)

1. **Scope** — nothing outside the envelope; nothing the SPEC §1 deferred.
2. **Simplicity** — Simplicity Bias; premature completeness (`che-scope-checker` L13).
3. **Architecture & boundaries** — repo pattern, layering, no leaked implementation details.
4. **Security / PII** — `che-compliance` patterns.
5. **Usability** — observable behaviour vs the AC.
6. **Style** — repo conventions.

A new criterion is a **SPEC change**, never a new review round.

---

## §4 FINDING CONTRACT

Each finding is `{id, severity, file, line, lens, cited_rule, suggested_fix, auto_fixable}`.

- **`id` is stable** = `lens + file + line + cited_rule`. A resolved id is never re-raised.
- **Citation required:** a finding MUST cite the specific rule / AC / lens violated.
  No citation → **invalid** → it cannot block.
- **Deferred check:** if the finding is about something the SPEC §1 marked `deferred by design`,
  it is **NOT a finding**.

---

## §5 ENFORCEMENT (severity gate)

| Severity | Action |
|---|---|
| **CRITICAL** | Block. Dev fixes before advancing. **NEVER overridable.** |
| **HIGH** | Block. Dev fixes, **OR** override with a verbatim justification logged to `decisions.log`. |
| **MEDIUM / LOW** | Log and defer. **Never blocks.** |

Tie-break on a judgement call with no clear rule: **the developer proceeds** (bias toward the
smallest increment); the disagreement is logged. The skeptic only stops the line with hard evidence.

---

## §6 LOOP BOUNDS (anti-infinite-loop — non-negotiable)

1. **Max 2 rounds per slice** (review → dev fixes → re-review). A 3rd round is **refused by the
   runner**, not left to judgement.
2. **No-progress stop (before the cap):** if round 2's finding set is not a strict subset of round 1's
   (minus resolved ids), **STOP**.
3. **Fix is scoped to the finding** — no new code beyond the flagged item.
4. **Frozen lenses + stable ids** — no moving goalposts.
5. On stop → escalate (§7). Never a silent round 3.
6. **Per-slice ceiling (absolute):** at most **2 review rounds + 1 escalation rerun = 3 passes** per
   slice. The 4th pass is refused by the runner. Escalation A consumes the escalation rerun; a second
   stop on the same slice allows only **B** or **C** — never another rerun.

---

## §7 ESCALATION MENU (on stop — never a silent loop)

- **A** = dev fixes manually and re-runs the slice **once** (consumes the single escalation rerun; a
  second stop on the same slice allows only **B** or **C**).
- **B** = override with a verbatim justification logged to `decisions.log` (**HIGH only**;
  CRITICAL is never overridable).
- **C** = back to SPEC — the scope was wrong, not the code.

---

## §8 OUTPUT

- Findings report per slice, written as a **worktree artifact** (never inside the worktree, never the
  fallback):
  1. `eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"`
  2. `PAIR_REPORT="$(che output_path report pair-review "$RELATED_ID" workspace md)"`
     → `$CHE_WORKSPACE_SHARED/reports/<related_id>/<YYYYMMDD-HHMMSS>-pair-review.md`
  3. Write it with the content on **stdin**: `che write_file_atomic "$PAIR_REPORT" <<'REPORT_EOF' … REPORT_EOF`.
- `decisions.log` entries via `che decision_append`: `PAIR_REVIEW` (verdict/rounds/counts, path),
  `PAIR_OVERRIDE` (HIGH only), `PAIR_ESCALATION` (on stop).
- Returns control to `che-act` §2 with `{verdict, rounds, blocking_findings[]}`.

---

## §9 WHAT IT IS NOT

- **Not a style linter** — repo linters do that.
- **Not the ship gate** — `che-ship` §0.9.1-§0.9.4 remains the full pass.
- **Not configurable** — the round cap is fixed at 2; a configurable cap invites "just one more
  round" and reintroduces the loop.
