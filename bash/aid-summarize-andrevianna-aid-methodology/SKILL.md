---
name: aid-summarize
description: >
  Generate kb.html, a single-file visual tour of the Knowledge Base. Use this skill when
  someone non-technical needs to read what the project knows about itself -- a newcomer, a
  stakeholder, anyone who will not open `.aid/knowledge/` directly. It builds one section
  per resolved document from that document's own frontmatter, in a light/dark themed page
  with click-to-expand images and WCAG AA accessibility. Two grades gate approval: script-
  verifiable checks score the machine grade, and an interactive checklist scores the human
  grade, including a mandatory visual review. Idempotent -- re-running on an unchanged
  Knowledge Base does nothing.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit
argument-hint: "[--grade X] override minimum  [--theme default|brand-X]  [--reset]"
---

# Knowledge Base Visual Summary

State machine: PREFLIGHT -> STALE-CHECK -> PROFILE -> GENERATE -> VALIDATE -> MANUAL-CHECKLIST -> FIX -> APPROVAL -> WRITEBACK -> DONE.

Generates a single self-contained `kb.html` from a populated and approved
`.aid/knowledge/` Knowledge Base. The output is a **newcomer-facing product** — visually
rich, plain-language, and distinct from the KB itself (which is a dual-audience technical
artifact for humans + AI agents). The KB's authoring rules (no diagrams, tables/bullets)
apply to the KB; they do NOT constrain the summary's format.

The section set is derived **data-drivenly** from the resolved doc-set
(`discovery.doc_set` in `.aid/settings.yml` intersected with docs present on disk),
one section per resolved doc. Each section's attributes (heading, description, component,
tier, keyword pills, cross-links) come from that doc's frontmatter (`kb-category`,
`objective`, `summary`, `tags`, `see_also`). Section order is deterministic and
reproducible from the same inputs.

**Prerequisite:** `/aid-discover` must have reached `DONE` and the user must have
approved the KB. This skill does NOT validate KB content — that is discovery's job.

**Idempotent:** Running `/aid-summarize` repeatedly on an unchanged KB is a no-op.
It only regenerates the HTML when the KB has been re-reviewed since the last
summarization.

---

## ⚠️ Pre-flight Checks

Run `.aid/runtime/scripts/summarize/summarize-preflight.sh` before any state. It verifies:

1. `.aid/knowledge/STATE.md` exists.
2. `**User Approved:** yes` is present in `.aid/knowledge/STATE.md`.
3. At least one populated KB document exists (`.aid/knowledge/*.md` with real content).
4. Not in Plan Mode (need write access).
5. Node.js >= 22 is available (required for visual-fidelity validation via `validate-visuals.mjs`).

If any check fails, the script exits non-zero with a clear actionable message. Do NOT
proceed; do NOT create any state files.

## Arguments

| Argument | Effect |
|----------|--------|
| `--grade X` | Override the minimum acceptable grade. Format: `[A-F][-+]?`. Without this, runs `bash .aid/runtime/scripts/config/read-setting.sh --skill summary --key minimum_grade --default A` (resolves per-skill override → global `review.minimum_grade` → default `A`). When passed, persist to `.aid/settings.yml` `summary.minimum_grade` via `/aid-config`. |
| `--theme palette=X` | Override color palette (e.g., `--theme palette=brand-acme`). Default uses the canonical palette in `.aid/runtime/templates/knowledge-summary/design-tokens.md`. |
| `--reset` | Force regeneration regardless of staleness check; clears `## Knowledge Summary Status` in `.aid/knowledge/STATE.md`. |

---

## State Detection

⚠️ **Filesystem is the only source of truth.** Always read actual files on disk.

The state-detection logic determines which mode this run executes:

```
1. PREFLIGHT (synchronous gate). Aborts on failure — no further state runs.

2. Read .aid/knowledge/STATE.md §§ Knowledge Summary Status, Summarization History.

3. STALE-CHECK first (always):
   - Compare LAST_KB_CHANGE_DATE (latest entry in STATE.md ## Review History)
     vs LAST_SUMMARY_DATE (latest entry in STATE.md ## Summarization History,
     or the **Last Run** field in ## Knowledge Summary Status).
   - If --reset → mode = GENERATE (force).
   - If kb.html missing → mode = GENERATE.
   - If ## Summarization History missing/empty → mode = GENERATE.
   - If LAST_KB_CHANGE_DATE > LAST_SUMMARY_DATE → mode = GENERATE.
   - If LAST_KB_CHANGE_DATE <= LAST_SUMMARY_DATE AND HTML exists:
       AND STATE.md's `summary_approved` frontmatter scalar is `yes` (or, for an
       un-migrated file, the legacy `## Knowledge Summary Status` `**User Approved:** yes`
       bold line) → mode = DONE-IDEMPOTENT (exit cleanly)
       OTHERWISE → mode = APPROVAL (HTML is current; just need user sign-off)

4. If mode = GENERATE:
   - ## Knowledge Summary Status absent/no Doc-Set Source → run PROFILE first to read
     discovery.doc_set from .aid/settings.yml + domain from .aid/knowledge/STATE.md,
     resolve the section manifest, then GENERATE.
   - ## Knowledge Summary Status has Doc-Set Source → reuse stored manifest; go straight
     to GENERATE.

5. After GENERATE → VALIDATE.

6. After VALIDATE (script-only checks → Machine Grade):
   - Machine Grade < minimum → FIX (loops back to VALIDATE).
   - Machine Grade >= minimum → MANUAL-CHECKLIST.

7. After MANUAL-CHECKLIST (interactive K1/K2/V1 checks → Human Grade):
   - Human Grade < minimum → FIX (loops back to VALIDATE).
   - Human Grade >= minimum AND Machine Grade >= minimum → APPROVAL.

8. After APPROVAL:
   - User says yes → WRITEBACK → DONE.
   - User says no → exit (no writeback; user can fix or --reset).
   - User says changes-needed → record + transition to FIX.
```

**Two-grade model:** the rubric is split into machine-verifiable checks (the AUTO_POOL — COV/T1/T2/T3/L1/L2/H1/A1/A2/A3/A4/A5/C1/C2/S2/NM = 68 pts) and human-judgment checks (the MANUAL_POOL — K1/K2/V1 = 30 pts). COV is the resolved-doc-set coverage check (doc-set completeness gate: < 60% coverage forces Machine Grade F). T1/T2/T3 are the S7 visual-fidelity checks (`validate-visuals.mjs`, Playwright-based) that replace the retired Mermaid D1/D2 checks; they assert readable text, minimal overlap, and correct layout for every authored visual. NM is the no-Mermaid-engine assertion (`validate-html-output.sh`). The script can NEVER auto-pass MANUAL_POOL; the user must run `manual-checklist.sh` and answer the prompts honestly. **V1 (human visual gate) is mandatory — a V1 fail forces Human Grade = F.** When Playwright is unavailable, T1/T2/T3 skip with a SKIP message and V1 carries the full visual-review responsibility (browser rendering required, not source inspection). Overall Grade = `min(Machine_letter, Human_letter)`. A+ requires both Machine and Human grades to be A+ on their respective subsets. See `grading-rubric.md` for the per-subset boundaries.

Print the state-entry line and "you are here" map at the start of each mode:

**PREFLIGHT:**
```
[State: PREFLIGHT] — Verifying prerequisites: KB approved, Node.js available, network reachable.
aid-summarize  ▸ you are here
  [● PREFLIGHT ] → [ STALE-CHECK ] → [ PROFILE ] → [ GENERATE ] → [ VALIDATE ] → [ APPROVAL ] → [ DONE ]
```

**STALE-CHECK:**
```
[State: STALE-CHECK] — Comparing KB review date vs last summary date to determine if regeneration is needed.
aid-summarize  ▸ you are here
  [✓ PREFLIGHT ] → [● STALE-CHECK ] → [ PROFILE ] → [ GENERATE ] → [ VALIDATE ] → [ APPROVAL ] → [ DONE ]
```

**PROFILE:**
```
[State: PROFILE] — Reading doc-set from .aid/settings.yml and domain from .aid/knowledge/STATE.md to derive the section manifest.
aid-summarize  ▸ you are here
  [✓ PREFLIGHT ] → [✓ STALE-CHECK ] → [● PROFILE ] → [ GENERATE ] → [ VALIDATE ] → [ APPROVAL ] → [ DONE ]
```

**GENERATE:**
```
[State: GENERATE] — Building kb.html from resolved doc-set and KB frontmatter (one section per resolved doc).
aid-summarize  ▸ you are here
  [✓ PREFLIGHT ] → [✓ STALE-CHECK ] → [✓ PROFILE ] → [● GENERATE ] → [ VALIDATE ] → [ APPROVAL ] → [ DONE ]
```

**VALIDATE:**
```
[State: VALIDATE] — Running machine-verifiable quality checks (visual fidelity, links, HTML, contrast).
aid-summarize  ▸ you are here
  [✓ PREFLIGHT ] → [✓ STALE-CHECK ] → [✓ PROFILE ] → [✓ GENERATE ] → [● VALIDATE ] → [ APPROVAL ] → [ DONE ]
```

**APPROVAL:**
```
[State: APPROVAL] — Both Machine and Human grades meet minimum; awaiting user approval.
aid-summarize  ▸ you are here
  [✓ PREFLIGHT ] → [✓ STALE-CHECK ] → [✓ PROFILE ] → [✓ GENERATE ] → [✓ VALIDATE ] → [● APPROVAL ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — Summary approved and Summarization History updated.
aid-summarize  ▸ you are here
  [✓ PREFLIGHT ] → [✓ STALE-CHECK ] → [✓ PROFILE ] → [✓ GENERATE ] → [✓ VALIDATE ] → [✓ APPROVAL ] → [● DONE ]
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| PREFLIGHT | `references/state-preflight.md` | inline | → STALE-CHECK |
| STALE-CHECK | `references/state-stale-check.md` | inline | → PROFILE |
| PROFILE | `references/state-profile.md` | inline | → GENERATE |
| GENERATE | `references/state-generate.md` | inline | → VALIDATE |
| VALIDATE | `references/state-validate.md` | inline | → MANUAL-CHECKLIST (grade ≥ min) / → FIX (grade < min) |
| MANUAL-CHECKLIST | `references/state-manual-checklist.md` | inline | → APPROVAL |
| FIX | `references/state-fix.md` | inline | → VALIDATE |
| APPROVAL | `references/state-approval.md` | inline | → WRITEBACK |
| WRITEBACK | `references/state-writeback.md` | inline | → DONE |
| DONE | `references/state-done.md` | inline | → halt |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

> **Note on DONE extraction:** Unlike other AID skills (aid-deploy/aid-execute/aid-detail/aid-plan) which keep DONE inline as a trivial halt-message state, aid-summarize's DONE is a **composite state** (handles both Normal-completion-after-WRITEBACK and DONE-IDEMPOTENT-after-STALE-CHECK branches with distinct messaging). The 38-line state body warrants extraction to `references/state-done.md` per the thin-router principle. This asymmetry is intentional, not a defect.


> **Note — DONE-IDEMPOTENT:** When STALE-CHECK determines the HTML is already
> up-to-date and approved, the router dispatches to the `DONE` row. The
> `references/state-done.md` file contains both the normal-completion body and the
> idempotent-completion body (DONE-IDEMPOTENT variant). The detection logic in
> State Detection step 3 selects which variant to execute.

---

## Quality Gate

The VALIDATE state runs script-verifiable checks (the Machine Grade AUTO_POOL) before
human review. This includes:

- **S7 visual-fidelity gate** (`validate-visuals.mjs`) — Playwright-renders every authored
  visual (inline `<svg>`, `.diagram-box`, infographic containers) and asserts: text readable
  (T1), minimal/zero element overlap (T2), correct basic layout (T3). Replaces the retired
  Mermaid D1/D2 diagram check. A failing visual blocks DONE. When Playwright is unavailable,
  the MANUAL-CHECKLIST V1 human visual gate is mandatory (browser-rendered inspection required;
  HTML/CSS source inspection is not sufficient).
- **HTML self-containment + no-Mermaid-engine assertion** (NM check in `validate-html-output.sh`)
  — confirms the Mermaid runtime engine is absent from the output (D-012 guardrail).
- **Accessibility baseline** (A1/A2/A3/A4/A5), **link correctness** (L1/L2), **HTML validity** (H1),
  and **contrast** (C1/C2, via `contrast-check.mjs`).

See `.aid/runtime/templates/knowledge-summary/grading-rubric.md` for the complete rubric and grade boundaries.

---

## References

- `.aid/runtime/templates/knowledge-summary/prompt.md` — agent guidance for the GENERATE step (long-form)
- `.aid/runtime/templates/knowledge-summary/design-tokens.md` — color palette, typography, spacing
- `.aid/runtime/templates/knowledge-summary/component-css.css` — full reusable CSS (inlined)
- `.aid/runtime/templates/knowledge-summary/lightbox.js` — full reusable JS (theme, lightbox, scrollspy, a11y)
- `.aid/runtime/scripts/summarize/validate-visuals.mjs` — §7 visual-fidelity gate (Playwright-based): T1 readable text, T2 minimal overlap, T3 correct layout for every authored visual (inline `<svg>`, `.diagram-box`, infographic container)
- `.aid/runtime/templates/knowledge-summary/section-templates/` — `kb-category`-keyed rendering hints (retired as project-type profile selectors)
- `.aid/runtime/templates/knowledge-summary/accessibility-checklist.md` — WCAG AA targets, focus trap pattern
- `.aid/runtime/templates/knowledge-summary/grading-rubric.md` — two-grade rubric (Machine + Human), completeness-based grading
- `.aid/runtime/templates/knowledge-summary/html-skeleton.html` — doctype, head, semantic landmarks, noscript (with `{{NOSCRIPT_DOC_LIST}}` placeholder for derived doc list)
- `.aid/runtime/scripts/summarize/grade-summary.sh` — orchestrates AUTO_POOL checks, reads `.aid/.temp/summarize/manual-checklist.json` for MANUAL_POOL, prints Machine + Human + Overall grades
- `.aid/runtime/scripts/summarize/manual-checklist.sh` — validates / scores the MANUAL_POOL result file (`--input PATH` headless mode; `--interactive` for raw-terminal use)
- `.aid/runtime/scripts/summarize/spot-check-facts.sh` — extracts HTML claims, grep-matches against source KB, writes `.aid/.temp/summarize/spot-check-facts.txt` (aids the user's K2 judgment)

---

## Failure modes and recovery

| Symptom | Cause | Recovery |
|---|---|---|
| Preflight aborts: "discovery not approved" | `/aid-discover` not yet at DONE | Run `/aid-discover` until it reaches APPROVAL and approve. |
| PROFILE warns: "discovery.doc_set not found" | KB was produced before feature-014 | Run `/aid-discover` to produce a feature-014-compatible KB, or the skill falls back to reading all `.aid/knowledge/*.md` files alphabetically. |
| GENERATE produces no sections | All doc-set entries missing on disk | Check that `/aid-discover` has run and the KB docs are present in `.aid/knowledge/`. |
| Writeback fails: lock contention | `/aid-discover` running concurrently | Wait, retry; the lock auto-releases. |
| Writeback fails: write error | Disk full / permissions | Manually add the entry to `.aid/knowledge/STATE.md` `## Summarization History`; mark `**Writeback Status:** ok` in `## Knowledge Summary Status`. |
