---
name: kb-search
description: Search the empirical Knowledge Base for the best-fit architecture and technology learnings given a product's conditions. Use during context-building in the realize lenses (/arch, /run, /ux, /agentic) when you need to know what worked before for a product in this situation — its stage, scale, persistence, and monetization. Reads the architecture/ and technology/ shelves (the condition-matched, "what works for us" engine), distinct from search-kb which routes work to a domain. Returns the learnings that fit, with recommendation, rationale, and provenance.
version: 0.1.0
user-invocable: false
---

# kb-search

The KB is a bank of **empirical learnings** — for a product in a given
situation, what capabilities and what architecture worked best, and when to
evolve. This skill finds the learning that fits. See
`core/components/memory/knowledge/_DESIGN.md` for the full design.

**V1 note:** the script only serves structure. **You** do the matching — read
the Conditions and judge fit. The script does not rank for you; that is
deliberate (the V1 engine; a server will rank later).

## Inputs

A **condition profile** for the product you are building context for, read from
its ProductOS — as many of these as you know:

- `stage`: prototype | internal | public | monetized
- `users`: one | small-team | public
- `persistence`: none | some | full
- `monetization`: none | lead-capture | paywall
- plus any free-text intent ("quick demo for one teammate")

## How to use

The script lives at `scripts/kb_search.py` (Python 3, no dependencies). Pass
`--kb-root` if the KB is not at the default deploy path.

1. **Get the map.** Run `index` — it returns every learning's id, title,
   conditions facets, evolve_when links, and provenance as JSON.

   ```bash
   python3 scripts/kb_search.py index
   ```

2. **Match by reasoning.** Read the conditions of each entry and pick the one(s)
   whose situation matches the product's profile. This is judgment, not keyword
   matching — "quick demo for one teammate" matches a `stage: prototype,
   users: one` learning even with no shared words. Prefer higher-provenance
   learnings (proven across more products) when several fit.

3. **Fetch the learning.** Run `get <id>` for the chosen learning to read its
   full Recommendation and Rationale.

   ```bash
   python3 scripts/kb_search.py get architecture/single-user-throwaway
   ```

4. **Follow evolution.** Use the learning's `evolve_when` to see what to climb
   to as the product's conditions change.

`grep <terms>` exists as a coarse pre-filter to narrow candidates when the
manifest is large — it is NOT the matcher; step 2 always is.

## Output

Return the selected learning(s) with: the recommendation (capabilities +
architecture), the rationale, the provenance, and the evolve-when pointers — so
the calling play (e.g. /realize) can apply them.

## Forward compatibility

When the KB moves to a server, this skill's script swaps its internals from the
local files to a `kb` CLI; the inputs, the steps, and the output shape do not
change.
