---
name: weekly-synthesis
description: >
  Extract time-window meaning from recent Obsidian notes: emerging thesis,
  contradictions, gaps, exactly one action, exactly one question.
  Load when user asks for weekly synthesis, what recent notes mean, or next action.
  Do NOT use for inbox triage, link-only review, or note promotion.
license: Apache-2.0
compatibility: opencode; requires obsidian-mcp
metadata:
  version: "4.1.0"
  last-reviewed: "2026-05-14"
  owner: r007b34r
---

# weekly-synthesis

## Constraints

- Output is NOT a recap; must contain thesis + evidence
- EXACTLY one action, EXACTLY one question (not zero, not many)
- NEVER let old notes dominate; they are calibration only
- NEVER write synthesis note without user confirmation
- If signal is weak: say "conclusion is uncertain" — do NOT force a thesis
- Default time window: 7 days unless user specifies otherwise

## Trigger Boundary

**Use when:** weekly synthesis, what recent notes mean, emerging thesis, one most valuable next action/question, time-window meaning-making.

**Do NOT use for:**
- Raw material routing → `inbox-triage`
- Link-only or relationship review → `connection-review`
- Project status reporting (not synthesis)
- Promoting result into stable note → `note-promotion`

## Boundaries

- **Owns:** time-window meaning extraction, thesis formation, gap identification
- **Delegates to:** `note-promotion` (synthesis ready for stable note), `opencode-context-maintenance` (thesis reveals drift)
- **Never absorbs:** inbox routing, link-only review, health diagnosis

## Continuations

| Condition | Next skill |
|-----------|-----------|
| User wants to preserve synthesis as stable note | `note-promotion` |
| Thesis or gaps reveal context drift | `opencode-context-maintenance` |
| Insufficient signal; try relationships first | `connection-review` |
| Signal too weak to form any thesis | Escalate to human |

## Companion Skill

All vault operations follow `obsidian-mcp`. Forbidden: `obsidian_patch_note`, `obsidian_append_to_note`. Verify every write through readback.

## Procedure

### Phase 1: Scope
1. Identify time window (default: 7 days; respect user-specified period)
2. `obsidian_list_notes` or `obsidian_search_notes` → notes in window
3. Count and report scope before proceeding

### Phase 2: Read
1. `obsidian_get_note format:"document-map"` → theme distribution
2. Deep-read only notes that support thesis, contradiction, or gap claims
3. Use older notes only for calibration (not primary signal)

### Phase 3: Synthesize

When extracting meaning, read `references/examples.md` for thesis quality calibration.

Six dimensions:
1. **Emerging thesis**: one claim + supporting evidence (or "uncertain" if weak)
2. **Contradictions**: only tensions that matter for reasoning
3. **Gaps**: missing perspective, evidence, decision, or experiment
4. **One action**: exactly one highest-value next move
5. **One question**: exactly one question worth preserving
6. **Follow-up note suggestions**: optional downstream notes

<details>
<summary>Weak Signal Handling (expand when theme stability is low)</summary>

- Fewer than 3 notes in window: report insufficient data, suggest expanding window
- Notes all on different topics: report fragmentation, no forced thesis
- Contradictions only surface-level: report "no meaningful contradictions found"
- Acceptable: "Thesis uncertain. Strongest signal is [X] but evidence is thin."
- One action can be "gather more data on [X]" when signal is genuinely weak

</details>

### Phase 4: Report

When formatting output, read `references/templates.md` for the exact synthesis format.

Do not write synthesis note by default. After user approval, create with `obsidian_write_note overwrite:false` and read back.

## Gotchas

### Gotcha 1: Recap disguised as synthesis
**What happens:** Agent lists what happened this week without extracting meaning
**Why it's wrong:** A recap has zero cognitive return; user already knows what happened
**Correct approach:** Force a thesis claim with supporting evidence, even if uncertain

### Gotcha 2: Multiple actions and questions
**What happens:** Agent returns 3-5 actions and 2-3 questions
**Why it's wrong:** Defeats the purpose of synthesis (focus); user loses signal in noise
**Correct approach:** Force exactly one action and one question; pick highest-value

### Gotcha 3: Old notes dominate the thesis
**What happens:** Agent builds thesis primarily from notes older than the time window
**Why it's wrong:** Recent signal disappears; synthesis becomes rehash of established knowledge
**Correct approach:** Use older notes only as calibration; thesis must be grounded in recent evidence

## Validators (CI only, not runtime)

- `validators/post-check.sh`: Verifies exactly one "One action:" and one "One question:" in output

## Exit Criteria

- Output is not a recap (has thesis + evidence)
- Exactly one action and exactly one question
- Thesis has evidence; contradictions are not forced
- Any written note has been read back and verified
