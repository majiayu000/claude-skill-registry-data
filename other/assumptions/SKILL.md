---
name: assumptions
description: Extract a thesis's load-bearing assumptions and scan for internal contradictions — the falsifiable claims the bull case requires, what would falsify each, and where the thesis's own Risks / Bear Case / research already argue against it. Use when user says "assumptions", "what must be true", "load-bearing assumptions", or "does [TICKER] contradict itself".
model: opus
effort: high
allowed-tools: Read Grep Glob WebSearch WebFetch Bash(date * defuddle *)
---

**Follow CLAUDE.md Writing Standards strictly.** Lead with the assumption and what falsifies it, no hedge words, tables over prose.

Extract the **load-bearing assumptions** of one thesis — the falsifiable claims that must hold for the bull case to work — and flag where the thesis already contradicts itself. The output is the atom the `vault-contradictions` workflow fans out to find where one thesis's bull premise is another thesis's bear premise.

## Arguments
`$ARGUMENTS` = a ticker or thesis name. If empty, ask which thesis.

## Read-only
This skill REPORTS analysis; it does not modify vault files. To persist, the user asks explicitly.

## Mental Models gate (MANDATORY — CLAUDE.md)
Read `[[Mental Models/Generalist - Overview]]` + matching `Industry -`/`Lens -` files. Apply the READING PROTOCOL: each assumption is a hypothesis to test, and **agreement across the thesis's own sections is a trigger to disconfirm**, not to trust — hunt the single falsifying datapoint.

## Method  (single source of truth — the `vault-contradictions` workflow reads this section)
1. **Read the thesis** in full — Summary, Key Non-consensus Insights, Bull Case, Bear Case, Risks, Outstanding Questions, Conviction Triggers — plus its Related Research. Read `_graph.md` once for cluster peers.
2. **Enumerate the load-bearing assumptions**: the specific, falsifiable claims the bull case requires (e.g. "HBM pricing holds through 2026", "CoWoS stays capacity-constrained", "Company X keeps design-win Y"). Each must be a claim that could be shown false, not a vibe.
3. **For each assumption record**: **what falsifies it** (the concrete datapoint / event), whether it is **stated or implicit**, and its **criticality** (thesis breaks / weakens / cosmetic).
4. **Internal-contradiction scan**: for each assumption, check whether the thesis's OWN `## Bear Case` / `## Risks` / `## Outstanding Questions` or a linked research note already argues against it. A high-conviction thesis whose bull assumption is contradicted by its own risk section is the strongest single-name red flag.
5. **Portability tag** (for the workflow): mark assumptions that are really claims *about the industry* (not just this company) — e.g. "memory oversupply arrives in 2H26" — since those are the ones that can clash with another thesis that assumes the opposite.

## Output (solo run)
An assumptions ledger — columns: **Assumption | Falsifier | Stated? | Criticality | Internally contradicted? (where)** — then a one-line verdict on whether stated conviction is supported by the surviving assumptions. No filler.

## Workflow reuse
`vault-contradictions` (`.claude/workflows/vault-contradictions.js`) fans this `## Method` out across every thesis, then finds cross-thesis clashes (thesis A's bull assumption = thesis B's bear assumption) and adversarially verifies each is a real contradiction, not a framing difference. Keep `## Method` the single source of truth.
