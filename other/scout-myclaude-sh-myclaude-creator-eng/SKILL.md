---
name: scout
description: >-
  Research a domain before building products. Tests Claude's baseline knowledge,
  identifies gaps, scans the marketplace, runs deep research, and recommends the
  optimal product setup. Use when: 'scout', 'research domain', 'what should I build for',
  'analyze domain', or before /create for any non-trivial product.
argument-hint: "{domain or query}"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash(myclaude *)
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Scout — Domain Intelligence & Setup Recommendation

> Before you build, understand the territory. This skill researches what Claude already knows,
> what's missing, what exists in the marketplace, and recommends exactly what to build.

**When to use:** Before /create for any serious product. When exploring a new domain. When
the creator says "what should I build for X?" or "scout X".

**When NOT to use:** For marketplace browsing without building intent (use /explore).
For building products (use /create→/fill). For mapping YOUR expertise (use /map).

**CLI contract:** This skill declares `Bash(myclaude *)` permission but delegates all marketplace queries to /explore. No direct CLI invocations here. See `references/cli-contract.md` for unified error handling when /explore is invoked as a sub-step.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. **Creator profile guard:** Read `creator.yaml` from project root. If missing → respond:
   "Profile not found. Run `/onboard` first (~3 min)." and **stop**.
1b. **Load UX vocabulary:** Load `references/ux-vocabulary.md` — translate all internal terms (MCS, DNA, scaffold, forge) before any creator-facing output. Vocabulary guard applies to all output in this skill.
1c. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after scout, suggest /create), #15 (research injection triggers), #16 (scout intelligence reuse).
2. **Maintain creator persona:** Adapt language, depth, and examples to `profile.type` and
   `technical_level` throughout. Load `references/quality/engine-voice-core.md` at the start
   of every /scout invocation — every user-facing line honors the ✦ signature, three tones,
   and six anti-patterns. Load the full `references/quality/engine-voice.md` only when
   rendering the final report delivery (a peak moment — the Creator just watched 2-5 minutes
   of research consolidate into a concrete recommendation).
3. **Parse arguments:** Read `$ARGUMENTS` for domain query.
   If no arguments → ask via AskUserQuestion: "What domain do you want me to research?"
4. **Intent check:** Ask via AskUserQuestion (single select):
   "What's your goal for this domain?"
   - "Build products for myself" → personal setup, skip pricing
   - "Build products for the marketplace" → include pricing + market scan emphasis
   - "Just explore — not sure yet" → lighter report, skip recommendation details
5. **Sanitize slug:** lowercase, alphanumeric + hyphens, 3-40 chars.
6. **Brownfield check:** Glob `workspace/scout-{slug}.md`. If exists → ask:
   "A scout report for '{domain}' already exists ({date}). Refresh it or reuse?"
7b. **Load entity ontology for type recommendation:** Read `references/entity-ontology.md` §SCOUT_INTELLIGENCE, §INTELLIGENCE_GRADIENT, §COMPOSITION, §HEURISTICS, §ISOMORPHIC. Use these to inform the setup recommendation:
    - Map domain signals to recommended product types per §SCOUT_INTELLIGENCE (single task→skill, advisory→minds, distinct specialties→squad, etc.)
    - Use §INTELLIGENCE_GRADIENT to explain WHY a type is recommended: "This domain needs judgment in routing, so squad is better than workflow."
    - Use §COMPOSITION to suggest how recommended products compose: "The skill handles execution while the mind advises."
    - Use §HEURISTICS to guard against over-recommendation: if a single skill suffices, don't recommend a squad
    - Use §ISOMORPHIC for creator-friendly explanations: "You need an advisor (minds) for thinking and a skill for doing."
    - Use §COMPOSITION_PRINCIPLES to suggest how recommended products compose: convergence-by-independence for squads, symbiosis for mind+skill pairs
    - Use §TRANSVERSAL_AXES to calibrate Nature and Depth per recommended product
    - For MCS-3 targets, consider §INTELLIGENCE_PIPELINE hermeneutic spiral as pre-forge method
7. **Gate check:** Read `config.yaml` → `gates.confirm_create` (default: true).
   If true → "I'll research '{domain}'. This involves generating a baseline, analyzing gaps,
   searching the marketplace, and running web research. Takes 2-5 minutes. Continue?"

---

## Execution — 6-Step Intelligence Protocol

Load and execute the full protocol from `.claude/agents/scout-agent.md` with:
- `domain`: the parsed domain query
- `slug`: the sanitized slug
- `creator`: the loaded creator.yaml profile
- `language`: creator's language (from creator.yaml or detected from input)
- `intent`: personal / marketplace / explore (from step 4)

**Critical gate between Steps 2→3:**
After gap analysis completes, PAUSE and show the creator:
```
Gap Analysis Complete — {domain}

  {critical_count} critical gaps | {significant_count} significant | {minor_count} minor

  Top gaps:
  1. {gap_1_summary} (critical)
  2. {gap_2_summary} (significant)
  3. {gap_3_summary} (significant)

  Next: marketplace scan + web research on these gaps (~{N} searches).
  Continue, adjust focus, or stop here?
```
Only proceed to Steps 3-6 after creator confirms.

---

## Post-Execution

After the protocol completes:
1. Verify `workspace/scout-{slug}.md` was written (Glob check)
2. **Compute value estimates for each recommended product:**
   For each product in the setup recommendation (Section 5), estimate a preliminary value score using the Intelligence Layer formula (`config.yaml → intelligence.pricing`):
   - **depth:** Infer from MCS target in the recommendation (MCS-2 → 2, MCS-3 → 3, cognitive mind → +1)
   - **uniqueness:** Estimate from gap severity coverage (all critical gaps → 3, mixed → 2, minor only → 1)
   - **coverage:** Count gaps the product addresses from Section 2
   - **market:** Use Section 3 market position (blue_ocean → 2, moderate → 1, saturated → 0)
   
   Map the estimated `VALUE_SCORE` to a price range using `config.yaml → intelligence.pricing.price_map`.
   
   Append to each recommended product in the report output:
   ```
   Value estimate: {value_score}/12 → ${range[0]}-${range[1]} ({strategy})
   ```
   
   **Epistemic caveat (always shown):** "Value estimates are preliminary — based on gap coverage and market position. Actual value_score is computed by /validate Stage 8 after content is filled."

3. **Portfolio connection check (back-reference from /validate):**
   Read `STATE.yaml → workspace.products[]` AND `STATE.yaml → mcs_results`. For each recommended product:
   - Check if any existing product is in the same domain or has overlapping capability.
   - If existing product has `mcs_results` with `overall_score`: "Your {slug} covers {domain} at {score}%. New product should focus on gaps {slug} doesn't cover — zero overlap = maximum delta."
   - If existing product has `baseline_delta`: "Your {slug} addressed {delta}% of known gaps. Scout for complementary coverage."
   If found: "This connects to your existing {existing_slug} ({existing_type}). Building here extends your {domain} coverage."
   If the recommended products would bring the domain product count to `>= bundle_suggestion_threshold` (from `config.yaml → intelligence.portfolio`): "With these additions, you'd have {N} products in {domain} — consider bundling them for complete coverage."

4. **Vocabulary guard (mandatory before rendering):** Before emitting any creator-facing text in step 4, translate internal terms per ux-vocabulary.md. Specifically: "gap severity" → "how much is missing", "baseline delta" → "what Claude already knows vs. what's needed", "market saturation" → "how crowded this space is", "blue_ocean" → "wide-open opportunity". For non-developer creators (profile.type != "developer" and != "hybrid"), these plain-language substitutions are required. For developer/hybrid creators, technical terms may appear but must include a brief inline gloss on first use.

5. Show the setup recommendation summary using engine voice:
   ```
   Scout complete. {N} gaps found, {M} researched, {P} products recommended.

   Recommended setup:
   {product_list_with_types_and_value_estimates}
   
   {portfolio_connection_note if applicable}

   Your expertise goes in next — accept this setup?
   /create {first_type} to start building.
   ```
6. Update STATE.yaml `last_scout` field (not current_task — scout reports are not products)
