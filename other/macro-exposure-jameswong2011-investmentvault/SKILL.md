---
name: macro-exposure
description: Tag a thesis's implicit macro bets — the macro variables its bull case is secretly levered to (AI capex, rates, FX, China decoupling, memory/HBM cycle, energy, regulation) with direction and magnitude. Use when user says "macro exposure", "what macro is [TICKER] betting on", "macro bets", or "rate exposure for [TICKER]".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$macro-exposure`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** Lead with the bet and its direction, no hedge words, tables over prose.

Surface the **implicit macro bets** inside one thesis — the macro variables the position is levered to whether or not the thesis names them. The output is the atom the `portfolio-macro-exposure` workflow fans out to find portfolio-wide concentration in a single macro variable dressed up as diversification.

## Arguments
`SKILL_ARGS` = a ticker or thesis name. If empty, ask which thesis.

## Read-only
This skill REPORTS analysis; it does not modify vault files. To persist, the user asks explicitly.

## Mental Models gate (MANDATORY — AGENTS.md)
Read `[[Mental Models/Generalist - Overview]]` + matching `Industry -`/`Lens -` files. Apply the READING PROTOCOL and run the **base-rate / outside view adversarially**: a macro bet the thesis treats as a sure thing is exactly where the outside view should attack.

## Method  (single source of truth — the `portfolio-macro-exposure` workflow reads this section)
1. **Read the thesis** + skim Related Research and any linked `Macro & Technology/` notes. Read `_graph.md` once for sector/cluster context.
2. **Extract each macro variable the bull case needs**, from a standard palette (extend as the thesis warrants): AI / datacenter capex, interest rates, USD / FX, China market access & export controls, the memory / HBM cycle, energy & power availability, fiscal / stimulus, regulatory regime, consumer / enterprise IT spend.
3. **For each, record**: **direction** (thesis needs it up / down / stable), **magnitude** (load-bearing / contributory / minor), **horizon** (already priced / 6–18mo / structural), and **stated vs unstated** (named in the thesis or a hidden assumption).
4. **Flag the single biggest unstated macro bet** — the variable the thesis is most exposed to but least explicit about. That hidden bet is where correlated portfolio risk accumulates.

## Output (solo run)
A macro-bet table — columns: **Macro variable | Direction | Magnitude | Horizon | Stated? | Transmission (how it hits the thesis)** — then one line naming the biggest *unstated* bet. No filler.

## Workflow reuse
`portfolio-macro-exposure` (`.claude/workflows/portfolio-macro-exposure.js`) fans this `## Method` out across every thesis, then aggregates into a concentration view: which single macro variable the largest share of bull cases (weighted by conviction) depend on. Keep `## Method` the single source of truth.
