---
name: repurposing-research-program
description: "Run or resume a deterministic, source-backed pathology-first programme that identifies existing-drug repurposing hypotheses for a supplied genetic disease and optional gene."
---

# Repurposing Research Program

Identify existing drugs whose established actions could plausibly alter a specific, evidence-backed
element of disease pathology. Do not require a prior disease-drug association. Treat every result
as an experimental hypothesis, never clinical advice or proof of efficacy.

## Instruction ownership

- Use this file only for programme orchestration and the major stage barriers.
- Use the current controller packet as the operative worker task, scientific decision contract,
  result schema, and validation target.
- Use `AGENTS.md` for general scientific conduct, routine-research authorization, and communication.
- Use the references at the end of this file for maintainer-facing architecture, result fields, and
  source-service behavior. They explain the controller; they do not add parallel worker criteria.

Do not combine similar wording from several files into an implied stricter or broader rule. Report a
real conflict between a packet and the installed controller as a controller defect.

## Run the programme

Use the installed `scripts/orchestrate_program.py` for every controller action, invoked from this
skill folder or by its absolute path. Install the pinned runtime dependencies once with
`python -m pip install -r requirements.txt`.

1. Start a fresh run unless the user explicitly asks to resume a compatible run. Choose one run
   folder and reuse it for every command. Supply the exact MONDO ID when known:

   ```powershell
   python scripts/orchestrate_program.py init <run-folder> --disease "<disease>" [--gene <gene>] [--mondo MONDO:...]
   ```

2. Call `next`:

   ```powershell
   python scripts/orchestrate_program.py next <run-folder>
   ```

   If it returns `needs_controller` with progress, call `next` again. If it returns an agent packet,
   use the persisted packet path and returned worker prompt exactly.

3. Start one fresh `fork_turns=none` agent for that packet. Give it this `SKILL.md`, its sibling
   `AGENTS.md`, the worker prompt, the persisted packet, and only read-only context explicitly
   exposed by the packet. Keep only this one packet worker active, wait for it to finish without
   polling or repeated nudges, and retire it before starting another. Do not give it prior packet
   content or a previous worker thread. The worker starts from `result_contract.result_template`,
   researches to the depth the evidence requires, and returns one JSON result.

4. Validate and submit the same ready packet:

   ```powershell
   python scripts/orchestrate_program.py validate <run-folder> <result.json>
   python scripts/orchestrate_program.py submit <run-folder> <result.json>
   ```

   If validation fails, preserve the research, amend only the reported invalid field and direct
   dependants, and validate again. Validation never accepts or mutates a result. Report a genuine
   controller defect as a defect. Record a scientific limitation that prevents contract satisfaction
   as a gap. Do not work around either.

5. Repeat `next -> fresh agent -> validate -> submit` in the foreground. Keep the supervisor to
   controller operations; packet research belongs to the fresh worker. Do not replace the loop with
   a persistent or background supervisor. Use `status` for read-only progress checks. If model
   transport reports a temporary rate limit, honour `Retry-After` and resume from persisted state.
   When supervisor context becomes large, continue from `status` in a fresh task.

6. When status is `ready_to_build`, run:

   ```powershell
   python scripts/orchestrate_program.py build <run-folder>
   ```

Resume only when the case objective, stage sequence, and result contracts match the installed
controller. Otherwise start a new run. Accepted results are immutable and content-addressed.

## Stage sequence

The controller advances linearly through:

1. deterministic Monarch and DisMech screening;
2. compact source-sentence adjudication when screening flags free text;
3. pathology-only source normalization;
4. `pathology_landscape_scan` for the shallow Asta landscape pass;
5. `pathology_coverage_expansion` for the single Undermind coverage challenge;
6. one constrained curation packet;
7. one deep pathology-research packet per curated research concept;
8. a frozen living evidence graph;
9. one global packet that identifies up to ten material open pathology questions;
10. one global packet that researches every question;
11. one global packet that synthesizes and challenges unexpected biological connections;
12. one candidate-seed packet per researched concept;
13. deterministic UniChem lookup and one identity-review packet when needed;
14. one standardized hypothesis-packet folder and fresh scientific report worker per candidate;
15. one closed-corpus scoring and bounded-exclusion pass;
16. deterministic scoring, ranking, and output construction.

Asta and Undermind are required only in their named stages. Their presence in the sequence is not a
general preference for research tools or sources. All other research follows the evidence question
in the current packet.

## Programme barriers

- Keep pathology construction treatment-blind. The isolated source-adjudication packet is the only
  packet that may contain flagged treatment-bearing source sentences.
- Begin candidate generation only after curation, required pathology research, and graph freezing.
- Derive rescue strategies from the frozen pathology before searching for drugs.
- Keep pathology evidence and drug-action evidence separate; a paper directly linking the drug to
  the disease is not required.
- Let curation alone decide pathology identity, splitting, merging, and research eligibility.
- Let candidate review research viability and write the final scientific hypothesis prose without scoring or excluding.
- Let the final scoring pass use only the completed candidate-local hypothesis packets; it may not search, add evidence, or rewrite the hypothesis prose.
- Let Python own ordering, receipts, hashes, packet lineage, validation, persistence, aggregation,
  ranking, and outputs. Workers create research judgments only.

The exact scientific gates and result fields for each barrier live in the emitted packet and are
documented once in `references/packet-contract.md`.

## References

- Read [architecture.md](references/architecture.md) when changing stage ownership, controller
  state, evidence flow, status semantics, or module boundaries.
- Read [packet-contract.md](references/packet-contract.md) when changing worker tasks, scientific
  gates, result fields, validation rules, or final audit semantics.
- Read [source-adapters.md](references/source-adapters.md) before changing source ingestion,
  bibliography or UniChem transport, or the Asta/Undermind service protocols.

## Handoff

Report status, retained source count, pathology profile count, raw and deduplicated candidate
counts, material gaps, and the experimental-use policy. Report `source_edges` as source edges and
researched `assertions` as assertions; before pathology-node research the assertion count is zero.
For a completed run, link `outputs/summary.md`, `outputs/candidates.csv`,
`outputs/candidate_exclusions.csv`, and `outputs/candidate_cards.md` in the final handoff.
