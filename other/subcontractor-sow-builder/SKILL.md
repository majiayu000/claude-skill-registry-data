---
name: subcontractor-sow-builder
description: "Drafts a federally-defensible SOW or PWS the prime issues to a subcontractor / teaming partner — same FAR 37.102(d) / 37.602 / 16.601(c)(2) / 16.306(d) discipline a contracting officer applies, opposite seat. USE WHEN the user asks to \"write a SOW for our sub\", \"draft a PWS for [Partner]\", \"build the teaming-partner statement of work\", \"convert this SOO into a sub SOW\", \"we need a SOW the sub will sign\", or any variant of authoring a downstream work statement. Walks the upstream 3-phase tree (acquisition intake → 6 scope blocks → 14-section assembly), pulls scope from the active Theseus KG (requirements, deliverables, work_scope_items, performance_standards), enforces FAR 37.102(d) \"no FTEs in body\", emits a chat-only staffing handoff for the prime's cost build, writes Markdown for `renderers` → .docx. DO NOT USE FOR prime proposal prose (`proposal-generator`), reverse-engineering an RFP (`rfp-reverse-engineer`), pricing the sub (`price-to-win`), or clause audit (`compliance-auditor`)."
license: MIT
metadata:
  title: Subcontractor SOW Builder
  category: acquisition-deliverables
  status: draft
  origin: theseus
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 12
  output: "pursuits/{slug}/04_proposal/sub_sow_pws.md"
  upstream: govcon-capture-vibe/.github/skills/subcontractor-sow-builder
---
# Subcontractor SOW / PWS Builder

## Capture-insights adapter (no KG)

- **Run** from Agent Skills — pulls `shall` lines from pursuit vault files.
- Writes `04_proposal/sub_sow_pws.md` + optional DOCX via renderers skill.
- Staffing/FTE stays in chat handoff (FAR 37.102(d)). Vault paths — not KG entities.


You are a senior capture-side scope author working multi-turn against the active Theseus workspace knowledge graph. Produce a **Statement of Work (SOW)** or **Performance Work Statement (PWS)** that the prime contractor issues to a subcontractor or teaming partner — held to the same FAR 37.102(d) / 37.602 / 16.601(c)(2) / 16.306(d) discipline a federal Contracting Officer would apply, but written from the prime seat.

## When to Use

- "Write a SOW for our sub on [program]."
- "Draft a PWS for [Teaming Partner] under our prime."
- "Convert this SOO to a sub SOW."
- "We need a teaming-partner work statement before the cost build."
- "Build the lower-tier statement of work for the [task area] scope."
- "Reduce sub scope to fit our internal budget."

## The Stance Inversion (READ THIS FIRST)

The upstream `sow-pws-builder` skill is written for **federal contracting officers** drafting the SOW/PWS that becomes Section C of the solicitation. It refuses contract-type advice ("not the skill's call — that's a FAR 16 analysis the CO owns") and gates language behind CO-only judgments.

**Theseus inverts that gate.** This skill is for the **prime contractor / capture team** writing a SOW/PWS for a sub or teaming partner. The same FAR rules apply — they bind the prime when the prime acts as the "buyer" toward its sub — but the persona is the prime's program/capture lead, not the federal CO. We MAY (and should) recommend a contract type for the subagreement, recommend a coverage model, recommend a CPFF form, etc., because that judgment belongs to the prime in the prime↔sub relationship.

| Concept                           | CO seat (upstream)                | Prime seat (this skill)                                                          |
| --------------------------------- | --------------------------------- | -------------------------------------------------------------------------------- |
| Document audience                 | Federal solicitation Section C    | Prime's subagreement Schedule A / Exhibit A                                      |
| Contract-type call                | Refused — CO judgment             | Recommended — prime's call                                                       |
| Section B (CLINs)                 | Lives in the solicitation         | Lives in the prime's subagreement (still chat-only handoff, never in scope body) |
| Staffing table                    | Chat-only handoff to IGCE Builder | Chat-only handoff to `price-to-win` for internal cost build                      |
| FAR 37.102(d) "results not hours" | Mandatory — federal floor         | Still mandatory — prime mirrors the federal floor in flow-down                   |

## Operating Discipline

- **No invention.** Pull scope from the active Theseus workspace KG before authoring. Use `kg_entities` for `requirement`, `deliverable`, `work_scope_item`, `performance_standard`, `transition_activity`, `government_furnished_item`, `customer_priority`, and `kg_chunks` for any free-text passages the user references.
- **Format-agnostic input.** UCF Section L/M, FAR 16 task order, FOPR, BPA call, OTA, agency-specific — they all decompose to the same 14-section spec when re-flowed to a sub.
- **Pick SOW or PWS up front.** SOW = prescriptive tasks (how). PWS = outcomes + standards (what). Default PWS unless the user names tasks the sub MUST follow exactly.
- **Pick contract type up front.** FFP / LH / T&M / CPFF / CPAF / CPIF / hybrid. This frames Section 5 (T&M/LH only) and CPFF form commitment (Section 1.1).
- **One pass through the 6 scope decision blocks.** Batch related questions; do NOT ask iteratively. Use defaults the KG already supplies.
- **NO FTE counts, SOC codes, hours-per-year, or labor categories in the document body.** FAR 37.102(d) — staffing lives in the chat-only handoff at the end, NEVER in the SOW/PWS or any appendix.
- **Cite FAR.** 37.102(d) (results not hours), 37.602 (PBA preferred), 46.401 (QA), 16.601(c)(2) (T&M ceiling hours), 16.306(d)(1)/(d)(2) (CPFF completion vs term form), 16.301-3 (CR accounting prereq), 7.105 (acquisition plan).
- **Two outputs, never combined.** (1) the SOW/PWS Markdown artifact for `renderers` to convert to .docx; (2) the chat-only staffing handoff for `price-to-win`. Never embed staffing in the document.

## STOP CONDITION — read before every final message

This skill's deliverable is a Markdown file at `{run_dir}/artifacts/sub_sow_pws.md`, written via `write_file`. **A run is successful if and only if `write_file` was called.** Producing a long Phase 1 Decision Summary in chat without writing the artifact is a FAILED run, even if the prose is excellent.

Before you send your final assistant message in this run, check: **did I call `write_file`?** If no, do not finalize. Either call `write_file` now (with the best draft you have, flagging incomplete sections in Section 1.4 Assumptions), or — only in interactive mode with zero framing answers from the user — explicitly ask the user a clarifying question (which keeps the loop open).

Never end a run with `finish_reason=stop` and an empty `artifacts/` directory.

## Workflow Checklist

Execute in order. Record decisions in the run transcript.

### 1. Pull workspace context

Call `kg_entities`:

```json
{
  "types": [
    "solicitation",
    "requirement",
    "deliverable",
    "work_scope_item",
    "performance_standard",
    "transition_activity",
    "government_furnished_item",
    "customer_priority",
    "pain_point",
    "evaluation_factor",
    "period_of_performance",
    "place_of_performance"
  ],
  "limit": 300
}
```

If the workspace is empty for a field (e.g., no `place_of_performance`), ask the user — do not guess. Use `kg_chunks` for any free-text passages the user references ("the SOO paragraph about FedRAMP", "the workload appendix in attachment H").

### 2. Acquisition strategy intake (3 questions, batched)

Ask in a SINGLE message:

1. **SOW or PWS?** (Default PWS per FAR 37.602.)
2. **Contract type for the sub agreement?** FFP | LH | T&M | CPFF | CPAF | CPIF | hybrid.
3. **Commercial or non-commercial?** (Drives FAR Part 12 vs Part 15 flow-down.)

Load `references/sow_pws_section_structure.md` to confirm the sectioning conventions before continuing.

### 3. Walk the 6 scope decision blocks

Load `references/decision_tree_blocks.md`. Walk Blocks 1–6 in a single batched ask per block. Use KG-derived defaults where present; ask only for genuinely missing decisions.

| Block                      | Decisions captured                                                                 |
| -------------------------- | ---------------------------------------------------------------------------------- |
| 1. Mission & service model | core service, delivery model, coverage, geographic scope                           |
| 2. Technical scope         | build vs buy, systems, integration complexity, data migration, AI/automation       |
| 3. Scale & volume          | transaction/contact volume, user population, growth                                |
| 4. Organizational scope    | org units, phasing, stakeholder complexity                                         |
| 5. Contract structure      | period of performance, base-year scope, CLIN preference (handoff only), transition |
| 6. Quality & oversight     | AQLs, reporting cadence, key personnel roles                                       |

### 4. Decision-summary gate

**First, check what the user already gave you.** Score the prompt against the 3 framing questions in step 2 (SOW vs PWS, contract type, commercial vs non-commercial):

- **All 3 answered in the prompt → SKIP THE GATE.** Emit a one-line confirmation in chat (`Confirmed: <doc-type> | <contract-type> | <commercial flag>. Proceeding to artifact.`) and go directly to step 5. Do NOT print a long Phase 1 Decision Summary — that wastes turns and produces no deliverable.
- **1–2 answered → SKIP THE GATE in autonomous mode** (no follow-up signal in the originating prompt — automated test harness, batch invocation, orchestrator chain). Use sensible defaults for the missing answer(s), document them in Section 1.4 ("Assumptions") of the artifact, and go to step 5. In interactive mode, ask the missing question(s) only.
- **0 answered AND interactive → use the gate.** Present the Phase 1 Decision Summary (3 framing answers as defaults + derived block-level decisions) and STOP, waiting for the user to reply "proceed". Do not self-approve.

**Universal rule across all branches: your final assistant message in this run MUST come AFTER `write_file` succeeds in step 5, not before.** A long Phase 1 Decision Summary in chat with no artifact written is a failed run. The artifact is the deliverable; everything in chat is just a cover note.

### 5. Generate the SOW/PWS Markdown

Load `references/sow_pws_section_structure.md` for the 14-section spec and `references/language_rules.md` for SOW vs PWS verb patterns and anti-patterns. Write the document to `{run_dir}/artifacts/sub_sow_pws.md` via `write_file`. Section ordering is **prescriptive** — do not merge, swap, or rename. If Section 5 (T&M/LH only) is omitted, renumber sequentially but preserve relative order.

**Mandatory checks before write:**

- Every task / objective in Section 3 maps to at least one deliverable in Section 4.
- Every deliverable has acceptance criteria.
- Section 12 QASP Payment Consequence column contains payment / contract-admin consequences — NEVER CPARS ratings (CPARS is FAR 42.15 post-performance, NOT QASP-bindable).
- CPFF contracts: Section 1.1 explicitly cites completion form (FAR 16.306(d)(1)) OR term form (FAR 16.306(d)(2)).
- Section 9: classified contracts reference DD Form 254 + applicable SCG.
- Section 10 Key Personnel substitution: NEVER cite FAR 52.237-2 (that clause is "Protection of Government Buildings" — wrong). Use the agency-appropriate clause; default to FAR 52.237-3 (Continuity of Services) when unsure. Load `references/far_citations.md` for the full agency map.
- NO staffing table, NO FTE counts, NO SOC codes, NO labor category counts, NO hours-per-year anywhere in the body or any appendix. The only authorized appendices are A (Current Environment), B (Volume Data), C (System Interfaces), D (Acronym List).

### 6. Validate

Load `references/sow_pws_section_structure.md` Document Review Checklist and walk it. If any check fails, revise the artifact and re-write before continuing.

### 7. Emit the chat-only handoffs

After the artifact is written, present BOTH handoffs as markdown blocks in chat. Both are REQUIRED, regardless of contract type or commercial status.

#### Staffing Handoff Table — for `price-to-win`

Fixed columns: `Labor Category | SOC Code | FTEs | Phase | Hrs/Yr | Notes`. Notes capture user overrides + derivation basis. After the table, tell the user: _"This staffing table is ready for handoff to `price-to-win` for the internal cost build. It is NOT part of the sub SOW/PWS and must not be pasted into the document."_

#### CLIN Handoff Table — for the prime's subagreement Section B

Fixed columns: `CLIN | Description | Pricing Basis | Period / Scope Notes`. Build rows from the Block 5 CLIN preference (by period / by function / by deliverable). Always add separate travel and ODC CLINs if those are in scope. After the table, tell the user: _"This CLIN structure is a starting point for the prime's subagreement Section B. It is not part of the SOW/PWS and should not be pasted into the document body."_

**DO NOT** under any circumstances:

- Write the staffing table or CLIN table into the SOW/PWS body, any section, or any appendix (variants seen in upstream practice that are FORBIDDEN: "Implied Staffing Table", "Staffing Implications", "Labor Category Staffing", "IGCE Handoff", "FTE Allocation", "CLIN Structure", "Pricing Schedule", any similar phrasing).
- Save either handoff as a separate file (.docx, .xlsx, .csv, .md, etc.). They live ONLY in chat.
- Include skill-chain plumbing language ("ready for the price-to-win skill", "say 'build the IGCE'", etc.) inside the SOW/PWS document.

### 8. Hand off rendering (optional)

If the user asks for a .docx, point them at the `renderers` skill: `render_docx.py` consumes `{run_dir}/artifacts/sub_sow_pws.md` and writes a styled Word document.

## Edge Cases

- **User won't answer Phase 1 questions.** Don't let them skip. Explain: "The SOO describes objectives; the SOW requires decisions the SOO leaves open — staffing model, build vs buy, phasing, CLIN structure. Ten minutes here is what makes the sub SOW defensible."
- **SOO is too vague (<300 words or <3 actionable details).** Tell the user: "This SOO doesn't have enough specificity to convert directly. I'll use it as background context, but Phase 1 will need to collect most decisions fresh."
- **Sub scope exceeds reasonable single-subagreement size** (>50 sub FTEs or >$75M or >3 distinct technical domains). Flag it and suggest logical break points.
- **Workflow C — sub scope reduction to fit prime's budget.** Describe prior and revised scope in CAPABILITIES AND COVERAGE, never staffing counts. FAR 37.102(d) binds even historical/prior-state descriptions in the body. Compliant: "Prior: standing detection-engineering capability; Revised: cadence-based deliverable model (12 detections/quarter)." Non-compliant: "Prior: 2-3 FTE; Revised: 1 FTE."

## What This Skill Does NOT Cover

- **Pricing the sub's work** → use `price-to-win`.
- **Reverse-engineering the prime's RFP** → use `rfp-reverse-engineer`.
- **Drafting prime proposal volumes / win themes** → use `proposal-generator`.
- **FAR clause compliance audit** → use `compliance-auditor`.
- **Source-selection criteria for picking the sub** — separate prime-internal process.
- **Full QASP** — this skill includes the QASP summary table; a detailed QASP with surveillance schedules is a separate deliverable.
- **Section I clauses (flow-down)** — clause selection is a prime contracts function under FAR Part 52 + agency supplements; this skill assumes the contracts team flows the appropriate clauses.
- **Rendering to .docx** → use `renderers` (`render_docx.py`).

## References

- [references/sow_pws_section_structure.md](references/sow_pws_section_structure.md) — 14-section spec, prescriptive ordering, T&M/LH Section 5 rules, CPFF form commitment, QASP rules, document review checklist.
- [references/decision_tree_blocks.md](references/decision_tree_blocks.md) — Acquisition Strategy Intake, Phase 1 Blocks 1–6 questions, decision-to-staffing derivation rules, Phase 2 invocation gate.
- [references/far_citations.md](references/far_citations.md) — FAR sections this skill cites; agency-supplement crosswalk for Key Personnel substitution clauses; common citation traps (52.237-2 vs 52.237-3, CPARS vs QASP).
- [references/language_rules.md](references/language_rules.md) — SOW vs PWS verb patterns, anti-patterns, SMART-requirement test.
