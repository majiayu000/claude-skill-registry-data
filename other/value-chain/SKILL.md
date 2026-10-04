---
name: value-chain
description: Map a thesis's position in its value chain — who it buys from, sells to, and competes with; where the bottleneck and pricing power sit; and whether it owns a critical layer. Use when user says "value chain", "supply chain position", "where does [TICKER] sit", or "who are [TICKER]'s suppliers/customers".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$value-chain`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** Lead with the bottleneck and who holds pricing power, no hedge words, tables over prose.

Map where one company sits in its value chain and **where the pricing power actually is**. The output is the node the `portfolio-supply-chain` workflow fans out to assemble the portfolio's full chain graph and find single points of failure.

## Arguments
`SKILL_ARGS` = a ticker or thesis name. If empty, ask which thesis.

## Read-only
This skill REPORTS analysis; it does not modify vault files. To persist, the user asks explicitly.

## Mental Models gate (MANDATORY — AGENTS.md)
Read `[[Mental Models/Generalist - Overview]]` + matching `Industry -`/`Lens -` files. The **Value Layer Monopoly** lens is central: does the company own a layer of the stack everything above must pay to traverse, and is that mispriced? Apply the READING PROTOCOL.

## Method  (single source of truth — the `portfolio-supply-chain` workflow reads this section)
1. **Read the thesis** + its Industry Context / Related Research + the sector note (from `sector:`). Read `_graph.md` once for peers already in the vault.
2. **Locate the company on its chain**, naming real entities (not roles):
   - **Upstream** — critical suppliers / inputs / tool or IP providers it depends on.
   - **The company's own layer** — what it makes, and whether that layer is a chokepoint (sole/near-sole supplier) or commoditized.
   - **Downstream** — direct customers and the end-demand they serve.
   - **Competitors / substitutes** — at its layer, and adjacent layers threatening to integrate into it.
3. **Locate the bottleneck & pricing power**: which node in this chain can raise price without losing volume, and is it this company or someone up/downstream of it? Note the trajectory (gaining / losing).
4. **Flag single points of failure**: any node whose disruption cascades to this thesis (and, for the workflow, which *other* vault names touch that same node).

## Output (solo run)
A chain map (upstream → company's layer → downstream, with named entities), a **bottleneck / pricing-power verdict** (who holds it, direction), and a single-points-of-failure list. Prefer a compact table plus one diagram-in-prose line. No filler.

## Workflow reuse
`portfolio-supply-chain` (`.claude/workflows/portfolio-supply-chain.js`) fans this `## Method` out, then stitches the per-thesis chains into one portfolio graph (optionally a `.canvas` file) exposing shared suppliers, shared customers, and cross-thesis single points of failure. Keep `## Method` the single source of truth.
