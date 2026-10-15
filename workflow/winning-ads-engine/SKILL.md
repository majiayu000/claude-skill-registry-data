---
name: winning-ads-engine
description: The complete winning-ads methodology in a single reference — competitor ad intelligence, own-creative diagnosis, psychological hook grading, cross-source pattern synthesis, and shoot-ready brief generation, plus the orchestration logic that sequences all five. Use when the user wants the full end-to-end pipeline from market research to production brief, asks how the winning-ads process works as a whole, or needs the combined methodology in one place rather than a single narrow step. For a single step — just competitor ads, just a hook list, just a brief — the individual skills in this pack are the better fit.
---

# Winning Ads Skill Pack

Six GoMarble skills that take you from "what's working in the market" to a shoot-ready ad brief: competitor intelligence, your own creative diagnosis, a psychological hook framework, pattern synthesis across both, brief generation, and one orchestrator that routes the whole pipeline.

Each skill below is a standalone `SKILL.md` — install individually (see README for how), or use this file as a single reference document. The orchestrator (`winning-ads-orchestrator`) is the entry point for full end-to-end requests; the other five are also directly triggerable on their own for narrower asks.

**Pipeline:**
```
competitor-ad-intelligence  ─┐
                              ├──> winning-pattern-synthesis ──> ad-brief-generator
own-creative-diagnosis      ─┤
                              │
creative-psychology-hooks   ─┘
```
All five are orchestrated by `winning-ads-orchestrator`.

---


---

---
name: winning-ads-orchestrator
description: The master workflow for going from "find winning ad ideas for X" to a shoot-ready creative brief. Routes through competitor-ad-intelligence, own-creative-diagnosis, creative-psychology-hooks, winning-pattern-synthesis, and ad-brief-generator in order, adapting to what data sources are actually available. Use this whenever the user asks broadly for winning ad ideas, a competitive+creative teardown, "what should we make next," or any request that spans research and production rather than a single narrow step — that's the signal to run the full pipeline instead of just one component skill.
---

# Winning Ads Orchestrator

The entry point for the winning-ads skill pack. Decides which component skills to run, in what order, and what to do when a step's data isn't available — rather than making the user manually invoke five separate skills.

## When to use this skill

- "Find me winning ad ideas for [product/brand]"
- "Do a competitive + creative teardown and give me briefs to shoot"
- "What should we test next and give me the script"
- Any request where the end goal is production-ready creative, not just one analysis step

For narrow single-step requests ("just show me competitor ads," "just tell me why this ad is underperforming," "just give me hooks"), go straight to the relevant component skill instead of running the full pipeline — don't force every request through all five steps.

## Pipeline

```
1. competitor-ad-intelligence   (GoMarble MCP required)
2. own-creative-diagnosis       (MCP preferred, CSV/screenshot fallback)
3. creative-psychology-hooks    (no data source needed)
4. winning-pattern-synthesis    (consumes outputs of 1-3)
5. ad-brief-generator           (consumes output of 4)
```

## Step 0: Scope and data-availability check

Before running anything, establish in one pass:
- Is GoMarble MCP connected? If not, step 1 (competitor intel) cannot run — say so, and confirm whether to proceed with steps 2-5 using own-creative + psychology only, or stop and ask the user to connect it.
- What's the product/brand/category and target audience?
- Does the user want the full pipeline output, or just the research (steps 1-2) without a brief yet?

State the plan in one short paragraph before executing — which steps will run, which will be skipped and why, e.g.:
> "GoMarble MCP is connected, so I'll pull competitor ads for [category] (step 1), diagnose your own top performers (step 2), grade hooks psychologically (step 3), synthesize into ranked directions (step 4), and brief the top 2-3 (step 5)."

## Step 1-2: Run research in parallel where possible

Competitor intelligence (step 1) and own-creative diagnosis (step 2) don't depend on each other — gather both before synthesizing. If MCP isn't available for one but is for the other, proceed with whichever is available and flag the gap rather than blocking the whole pipeline.

## Step 3: Psychological grading

Apply `creative-psychology-hooks` to the hooks/angles surfaced in steps 1-2 (grade, don't regenerate from scratch — the goal here is explaining *why* observed patterns work, feeding step 4). Only generate wholly new hooks at this stage if steps 1-2 turned up thin results and fresh ideation is needed to fill the batch.

## Step 4: Synthesize

Run `winning-pattern-synthesis` over whatever combination of steps 1-3 completed. Note explicitly in the synthesis output which inputs were available vs skipped.

## Step 5: Brief

Run `ad-brief-generator` on the top-ranked 2-3 directions from synthesis, unless the user asked for research only. Confirm format/length constraints before generating if they weren't established earlier in the conversation.

## Handling partial runs

- No MCP at all → competitor intel is fully blocked. Run own-creative diagnosis (if data available) + psychology hooks + a synthesis that's explicitly own-account-only, and say plainly that competitor whitespace can't be assessed without GoMarble MCP.
- No own ad account data (new brand/account) → own-creative diagnosis is blocked. Run competitor intel + psychology + a synthesis based on competitor patterns and psychological soundness only, flagged as unvalidated-for-this-account.
- Neither available → this pack can't meaningfully run past `creative-psychology-hooks`. Say so and offer cold ideation instead of pretending to synthesize.

## Output

The orchestrator's final output is whatever the last executed step produces (typically the brief set from `ad-brief-generator`), preceded by a one-paragraph recap of what ran, what was skipped, and why — so the user can see the provenance of the final recommendation without re-reading every intermediate step.


---

---
name: competitor-ad-intelligence
description: Pull and analyze what competitors are actively running in ads — creative angles, hooks, formats, and spend/velocity signals — using GoMarble MCP's ads library tools. Use this whenever the user asks "what are competitors running," wants competitor ad research, asks to find/track a competitor's ads, or wants a competitive creative teardown before briefing new ads. REQUIRES GoMarble MCP connection — this skill cannot run without it (no CSV/screenshot fallback exists for live competitor ad data).
---

# Competitor Ad Intelligence

Turns GoMarble's Ads Library MCP tools into a structured competitive-creative brief: what competitors are running right now, what patterns repeat across their winners, and what that implies for your own account.

## When to use this skill

- "What is [competitor] running on Meta/Google right now?"
- "Find competitors for [brand] and show me their ads"
- "Research the ad landscape for [category/product]"
- Before any new creative brief — as the competitive-context input into `winning-pattern-synthesis`

## Hard requirement

This skill only works through GoMarble MCP. If GoMarble MCP is not connected in the current session, say so explicitly and stop — do not attempt to approximate this with web search or general knowledge of a brand's marketing. Competitor ad library data is not something the model can infer or recall reliably; the whole value is that it's live.

## Tools (GoMarble MCP `ads_library_*`)

| Tool | Use for |
|---|---|
| `ads_library_search_brands` | Resolve a brand name to a brand ID before pulling ads |
| `ads_library_find_competitors` | AI + web-search assisted competitor discovery when the user gives a brand but not a competitor list |
| `ads_library_get_ads_by_brand_id` | Pull a brand's ad set with filtering/pagination |
| `ads_library_discover_ads` | Keyword/filter-based ad discovery across the whole database (category research, not brand-specific) |
| `ads_library_analyze_ad` | Deep single/multi-ad analysis — creative breakdown + duplicate-variation detection |
| `ads_library_get_brand_analytics` | Brand-level spend/volume/velocity stats |

## Workflow

### Step 1: Establish scope
Confirm with context already available (don't ask if it's inferable):
- Target brand(s) — the user's own account, or the competitor(s) named
- Category, if no specific competitor is named yet
- Platform(s) — Meta, Google, or both
- What they actually want: a landscape scan, a deep-dive on 1-2 named competitors, or ongoing tracking

### Step 2: Resolve brands
- If competitors are named: `ads_library_search_brands` to resolve each to a brand ID
- If competitors are not named: `ads_library_find_competitors` using the user's brand/category — this does its own research, so don't pre-guess competitors from training data
- If it's a category scan with no specific brand: skip straight to `ads_library_discover_ads` with category/keyword filters

### Step 3: Pull the ads
- Per competitor: `ads_library_get_ads_by_brand_id` — pull a meaningful sample (aim for enough to see repeated patterns, not just the newest 2-3 ads)
- Cross-check spend/scale with `ads_library_get_brand_analytics` — an ad running at high spend/long duration is a stronger "this is working" signal than one running briefly at low spend. Duration and apparent scale are the closest proxy available to competitor performance (the model has no access to their actual metrics).

### Step 4: Analyze the creative
For the ads worth analyzing in depth (longest-running, highest apparent spend, or most-duplicated), run `ads_library_analyze_ad`:
- Extract: hook (first 3 seconds / first line), core angle, format, offer/CTA, visual style
- `ads_library_analyze_ad` also surfaces duplicate variations of the same ad — a brand running many variants of one core concept is a strong signal that concept is a winner. Note variation count per concept.

### Step 5: Pattern-tag every ad reviewed
Don't just describe ads one by one — tag each with:
- **Angle** (problem-agitation, social proof, comparison, founder-story, before/after, price/offer-led, etc.)
- **Hook mechanism** (question, bold claim, pattern interrupt, UGC-style testimonial opener, etc.)
- **Format** (single video, single image, carousel, catalog)
- **Signal strength** (running long / many variants = strong; new/single variant = untested)

## Output Format

```
### Competitor Ad Intelligence: [Category/Brand(s)]

Scope: [brands reviewed, platform(s), date pulled]

Per-competitor summary:
| Brand | Ads reviewed | Dominant angle | Dominant format | Scale signal |
|---|---|---|---|---|

Cross-competitor patterns (repeat across 2+ brands):
- [Pattern]: seen in [brands], likely working because [reasoning based on scale/variant signals]

Notable single-brand standouts:
- [Brand]: [what's unusual/aggressive about their approach]

Whitespace (patterns competitors aren't using):
- [gap the user could test]

Caveats:
- This reflects what's live/visible in the ads library, not verified performance data — treat scale/duration as a proxy signal, not ground truth.
```

## Guardrails

- Never present a competitor's ad copy or creative as something to copy verbatim — this is pattern/angle intelligence for inspiration, not a rip-and-replace source. Feed patterns into `winning-pattern-synthesis` and `ad-brief-generator` for original creative.
- Don't overstate confidence — "running for 40 days with 6 variants" is a real signal; a single ad seen once is not evidence of anything.
- If `ads_library_find_competitors` returns brands the user doesn't recognize as real competitors, flag that rather than silently including them.


---

---
name: own-creative-diagnosis
description: Diagnose why the user's own Meta ad creatives are (or aren't) working using Hook Rate / Hold Rate / CTR scenario analysis, format-specific rules, and pattern recognition across top performers. Use whenever the user asks why a creative isn't performing, wants to know what's working across their winning ads, needs a Pareto/creative teardown of their own account, or is planning variations of a winning ad. Works via GoMarble MCP (preferred), a Meta Ads Manager CSV export, or user-shared screenshots/creative files — degrades gracefully by source.
---

# Own Creative Diagnosis

Diagnoses the user's own ad creative performance: which ads are winning, why, and what pattern to replicate. Adapted from the Meta Ads Creative Analysis framework — the numeric half (Hook/Hold/CTR) works from any data source; the qualitative half (the actual creative) always needs to be supplied directly since no export contains creative content.

## When to use this skill

- "Why isn't this ad working?"
- "What's working across my top ads?"
- "Help me plan variations of [winning ad]"
- As the "own creative" input into `winning-pattern-synthesis`, alongside `competitor-ad-intelligence`

## Step 0: Data Inventory

Identify the source before anything else:

| Priority | Source | Notes |
|---|---|---|
| 1 | GoMarble MCP (`facebook_get_adaccount_insights`, `facebook_get_ad_creative_details`) | All rules work directly |
| 2 | Ads Manager CSV export | Numeric metrics work if video columns enabled; creative content is NEVER in a CSV — must be shared separately |
| 3 | Screenshots / copy-paste | Spot-checks only |

State what's available and missing in one short line before proceeding. If GoMarble MCP is connected, default to it — never ask the user for a CSV export first, as it exists already.

**Default account:** unless the user specifies otherwise, use their default Meta ad account. In all output, reference campaigns/ad sets/creatives by name only — never surface account IDs or account names.

## Step 1: Establish the Pareto set

Sort ads by spend descending; keep the set where cumulative spend ≤ 90% of total. This is the "top performers" pool everything else in this skill draws from.

## Step 2: Format-agnostic first pass

Apply to every Pareto ad:

| Profile | Diagnosis | Action |
|---|---|---|
| High CPM (≥30% above Pareto avg) + low PCM (≥30% below target) | Expensive audience, not converting | Recommend pausing |
| Low CTR (≥30% below Pareto avg) + low PCM | Not resonating | Check comments first; if fine, recommend stronger-CTA variations |
| Good metrics (within 20% of avg, PCM above avg) | Working | Candidate for variation — carry into Step 4 |

## Step 3: Video-specific diagnostic scenarios

For video ads, classify using Hook Rate / Hold Rate / CTR:

- **Hook Rate** = 3-second views ÷ video plays. Good ≥40%, average 26–39%, poor <25%.
- **Hold Rate** = ThruPlays ÷ 3-second views, benchmarked against a 90-day account average.
- **CTR** benchmarks: good ≥1.25%, average 0.65–1.24%, poor <0.65%.

| Scenario | Hook | Hold | CTR | Root cause | Fix |
|---|---|---|---|---|---|
| 1 | ≥40% | Poor | Avg | People stop scrolling but drop off after 3s — missing key info | Keep the hook, rebuild seconds 3+: show product sooner, quicker pacing, tie back to hook's promise |
| 2 | 26–39% | Avg | Avg | Nothing stands out anywhere | Priority: rebuild the hook first (check visual relevance, directness, audience fit), then improve hold |
| 3 | <25% | Any | Any | Not stopping the scroll — nothing else matters until fixed | Document current hook, compare against Pareto winners' hooks, rebuild: different visual open / text overlay / audio / question vs statement |
| 4 | ≥40% | >avg+25% | <0.65% | Watching the whole video, not clicking — CTA is weak | Check comments for negative sentiment first; if clean, strengthen CTA (more prominent, clearer, urgency/scarcity, landing-page alignment) |

## Step 4: Format-specific rules

- **Single image**: same high-CPM/low-CTR pause logic as Step 2; good metrics → variation candidate
- **Single video**: apply Step 3 scenarios
- **Catalog/Advantage+ ads**: Meta doesn't provide per-product conversion data — use spend+CTR as a proxy Pareto. High CPM+low PCM → test a different product set or remove products pushing CPM up. Low CTR+low PCM → identify and remove low-CTR products.

## Step 5: Pattern recognition across winners

Across the Pareto set's good-performing ads, extract and log the actual creative content (ask the user to share video/image files or descriptions — this cannot come from any export):

- Common angle (which selling points repeat)
- Common format (video vs image vs carousel)
- Common hook mechanism
- Common copy structure/tone/length

This output is the direct input to `winning-pattern-synthesis`.

## Guardrails

- Never recommend pausing the ad with the highest conversion volume in its ad set, regardless of budget share — that's the algorithm working correctly.
- Minimum signal before any performance judgment: 3–5 conversions/week per ad set.
- Budget/scale recommendations are out of scope for this skill — it diagnoses creative, not delivery mechanics.
- Never invent Hook/Hold/CTR numbers if the data isn't available — state what's missing and ask for it, or proceed on qualitative creative review only and say so.

## Output Format

```
### Creative Diagnosis: [Account/Campaign scope]

Pareto set: [N ads, cumulative spend ≤90%]

Per-ad diagnosis:
| Ad | Hook | Hold | CTR | PCM | Scenario | Verdict |
|---|---|---|---|---|---|---|

Winning patterns (shared across top performers):
- Angle: ...
- Hook: ...
- Format: ...
- Copy: ...

Recommendations:
1. [ad-specific fix, with metric justification]
2. ...
```


---

---
name: creative-psychology-hooks
description: Generate ad hook and angle ideas grounded in a structured creative psychology framework (TEEP, valence/intensity mapping, the Baader Hook Framework, micro-moment mapping) rather than generic brainstorming. Use whenever the user wants new hook ideas, ad angles, script openers, or wants existing hooks graded/critiqued on psychological mechanism. No data source required — this is a standalone ideation lens that can run with or without ad account access, and combines with competitor or own-creative pattern data when available.
---

# Creative Psychology Hooks

Generates and grades ad hooks/angles using a structured psychological framework instead of vibes-based brainstorming. Works standalone for cold ideation, or as the "why would this work" lens applied on top of patterns surfaced by `competitor-ad-intelligence` and `own-creative-diagnosis`.

## When to use this skill

- "Give me hook ideas for [product]"
- "Why would this angle work / not work psychologically?"
- Grading a batch of hooks before they go into a creator brief
- As the psychological-mechanism layer inside `winning-pattern-synthesis`

## Step 1: Gather product/audience context

Before generating anything, confirm (infer from conversation where possible, ask only what's missing):
- Product/offer and its core benefit
- Target audience — who specifically, and what state they're in when they see the ad (scrolling passively vs actively searching)
- Primary objection or hesitation this audience has toward the category
- Tone constraints, if any (brand voice, platform norms)

## Step 2: Apply the framework

### TEEP (Thought → Emotion → Expression → Physiology)
For each candidate hook, trace the chain it's meant to trigger in the viewer:
- **Thought**: what cognitive frame does the opening line/visual plant? ("this is about me," "this is a problem I have," "this is surprising")
- **Emotion**: what feeling follows from that thought?
- **Expression**: what does that emotion look/sound like — the tone, pacing, visual choice that should carry it
- **Physiology**: what physical reaction is being aimed for — lean in, laugh, wince, nod. This is the tell for whether a hook will actually stop a scroll.

A hook that skips straight to Expression without a real Thought→Emotion chain behind it reads as hollow or clickbait — flag these.

### Valence / Intensity Mapping
Plot each hook on two axes:
- **Valence**: positive (aspiration, relief, humor) vs negative (fear, frustration, FOMO)
- **Intensity**: low (mild curiosity) vs high (urgent, provocative)

High-intensity negative hooks (fear/frustration) convert attention fast but risk brand fatigue and backlash if overused — pair with the audience's actual tolerance, not just raw stopping power. Low-intensity positive hooks are safer but weaker at interrupting scroll. Recommend a spread across the matrix per batch, not five hooks all in the same quadrant.

### Baader Hook Framework
Classify each hook by mechanism, not just topic:
- **Pattern interrupt** — visually or verbally breaks the expected feed rhythm
- **Open loop** — poses a question/tension the viewer needs resolved
- **Direct claim** — bold, specific, falsifiable-sounding statement
- **Identity call-out** — names the exact audience ("if you have curly hair...")
- **Social proof lead** — opens with someone else's result/reaction, not the brand's claim

Every hook in a batch should be tagged with its mechanism. A batch that's 80% one mechanism isn't actually a diverse test — flag that too.

### Micro-Moment Mapping
Identify the specific real-world moment the hook is trying to interrupt or attach to (e.g. "just noticed hair thinning in a photo," "scrolling in bed frustrated with current routine"). Hooks anchored to a concrete, specific moment consistently outperform generic "are you tired of X" openers — push for specificity here.

## Step 3: Generate

Produce hooks in batches of 8–10 by default (adjust if the user asks for fewer/more). Spread deliberately across:
- Valence/intensity quadrants
- Baader mechanisms
- At least 2 distinct micro-moments

## Step 4: Grade (when reviewing existing hooks)

For each hook, output: TEEP chain (does it hold together?), valence/intensity position, Baader mechanism, micro-moment specificity, and a one-line verdict on why it would or wouldn't stop a scroll for this audience.

## Output Format

```
### Hook Set: [Product/Audience]

Context: [product, audience, objection, tone]

| # | Hook | Mechanism | Valence/Intensity | Micro-moment | Why it works |
|---|---|---|---|---|---|

Coverage check: [mechanisms used, quadrants covered, any gaps]
```

## Guardrails

- Don't force every hook into every framework layer if it doesn't fit — a strong hook that's hard to TEEP-trace cleanly is still worth including; note the ambiguity rather than distorting the analysis.
- Avoid defaulting to fear/negative-valence hooks purely because they're easier to generate — deliberately include positive-valence options.
- This skill produces angles and hook lines, not full scripts — hand off to `ad-brief-generator` for shoot-ready briefs.


---

---
name: winning-pattern-synthesis
description: >
  Cross-reference competitor ad patterns against the user's own winning creatives and psychological hook analysis to find validated overlap and untested whitespace. Use whenever the user wants to know what to actually build next — after competitor research and/or own-creative diagnosis have already run, or when they explicitly ask "what should we test" or "what's the whitespace." This is a synthesis skill — it consumes the outputs of competitor-ad-intelligence, own-creative-diagnosis, and creative-psychology-hooks rather than pulling new data itself.
---

# Winning Pattern Synthesis

Takes the outputs of the other three analysis skills and turns them into a ranked set of creative directions worth actually building — the step between "here's what we found" and "here's what to brief."

## When to use this skill

- "What should we test next?"
- "Where's the whitespace vs competitors?"
- Any time competitor intel + own-creative diagnosis have both run and the user wants a single synthesized direction rather than two separate reports
- As the step before `ad-brief-generator`

## Inputs

This skill doesn't fetch new data — it reasons over what's already been produced:
- **Competitor patterns** from `competitor-ad-intelligence` (angles, hooks, formats, scale signals)
- **Own winning patterns** from `own-creative-diagnosis` (what's already proven in the account)
- **Psychological grading** from `creative-psychology-hooks` (mechanism, valence/intensity, micro-moment)

If one or more inputs are missing, say explicitly which are missing and whether to proceed with a partial synthesis or run the missing skill(s) first. Competitor-only or own-creative-only synthesis is possible but weaker — flag it as partial.

## Step 1: Build the pattern matrix

Lay out every distinct pattern (angle × hook mechanism × format) found across both sources in one table, tagging each occurrence:

| Pattern | Seen in competitors? | Seen in own winners? | Scale/strength signal |
|---|---|---|---|

## Step 2: Classify each pattern

- **Validated overlap** — pattern works for both competitors (running long/many variants) AND the user's own account (strong Hook/Hold/PCM). Highest-confidence bet — double down.
- **Competitor-only** — competitors are running it at scale, user hasn't tested it. Whitespace worth testing, but unproven for this specific audience/account — flag as a test, not a guaranteed winner.
- **Own-only** — works for the user but no competitor is doing it. Could be a genuine differentiator, or could mean it's a narrow/account-specific fluke — note both possibilities.
- **Neither** — untested by anyone visible. Highest risk/highest potential differentiation; only surface if the user wants aggressive experimentation, not as a default recommendation.

## Step 3: Rank by confidence and apply psychological lens

For each pattern surfaced, pull in the Baader mechanism / valence-intensity classification from `creative-psychology-hooks` if hooks for that pattern were graded — this tells the user *why* a validated pattern is working, not just *that* it is, which matters for briefing variations correctly.

Rank output: Validated overlap first, then competitor-only whitespace, then own-only differentiators. Cap at the top 5–7 directions unless the user asks for the full list — a synthesis that recommends everything recommends nothing.

## Step 4: Flag conflicts

If a pattern is a competitor favorite but has performed poorly in the user's own account (or vice versa), don't average it out — call out the conflict directly and suggest a hypothesis for the divergence (audience difference, execution quality, offer mismatch).

## Output Format

```
### Winning Pattern Synthesis: [Product/Category]

Inputs used: [competitor intel / own diagnosis / psych grading — note any missing]

Top directions:
1. [Pattern] — VALIDATED OVERLAP
   - Competitor signal: [brands, scale]
   - Own signal: [ad, metrics]
   - Mechanism: [Baader tag, valence/intensity]
   - Recommendation: [double down / new variant angle]

2. [Pattern] — COMPETITOR WHITESPACE
   - ...

Conflicts worth noting:
- [Pattern]: strong for competitors, weak in our account — possible reason: [hypothesis]

Not recommended right now:
- [pattern seen but low-confidence, and why]
```

## Guardrails

- Never present competitor-only patterns with the same confidence as validated overlap — they're untested hypotheses for this account, not proven winners.
- Don't let this skill turn into a restatement of the two input reports — its entire value is the cross-reference and ranking. If there's no real overlap or conflict to surface, say that plainly rather than padding the output.
- Hand off the final ranked list directly to `ad-brief-generator` — don't re-derive angles from scratch there.


---

---
name: ad-brief-generator
description: Turn ranked creative directions (from winning-pattern-synthesis, or any validated angle/hook) into shoot-ready UGC/creator briefs — hook line, shot list, VO/copy direction, and CTA. Use whenever the user asks for a creator brief, script, shot list, or says a direction is ready to hand off for production. This is the final production-facing output of the winning-ads pack.
---

# Ad Brief Generator

Converts a validated creative direction into a brief a creator or editor can shoot from directly — no further interpretation needed on their end.

## When to use this skill

- "Turn this into a brief"
- "Write the script/shot list for [direction]"
- The final step after `winning-pattern-synthesis` has ranked directions, or directly off a single hook from `creative-psychology-hooks`

## Inputs needed

- The direction: angle, hook, mechanism (from synthesis or psychology skill output)
- Format: UGC talking-head, B-roll+VO, static image, carousel
- Any brand-specific constraints: tone, banned claims/words, required disclaimers, existing creator relationships
- Length target (15s, 30s, static, etc.) if the platform/placement is known

If the format template the user wants isn't established in this conversation, ask once before generating — don't guess a template structure only to redo it.

## Brief Structure

### Header
- Direction name / angle
- Source: validated overlap / competitor whitespace / own-differentiator / cold psychology hook (carry this through from synthesis — production should know the confidence level)
- Format + target length

### Hook (0–3s)
- Exact line or visual direction, not a vague description
- Delivery note (tone, pacing, on-camera vs voiceover, text overlay if any)

### Body
- Beat-by-beat shot list for video (what's shown, what's said, timing)
- For static/carousel: panel-by-panel breakdown
- Explicitly carry forward what `own-creative-diagnosis` flagged as working (e.g. "keep hook, change pacing after 3s" scenarios) if this brief is a variation of an existing winner rather than a fresh concept

### CTA
- Exact line
- Visual treatment (on-screen text, verbal, both)
- Any urgency/scarcity element if the diagnosis called for stronger CTA

### Copy (for the ad unit itself, separate from video VO)
- Primary text
- Headline
- Any compliance/disclaimer requirements

## Variation Set

Don't generate a single brief in isolation — generate the brief plus 2-3 named variation directions per the standard test order:
1. Copy variation (same angle, different words)
2. Angle variation (different selling point, same format)
3. Hook variation (same body, different opener) — pull alternates straight from `creative-psychology-hooks` output if available

## Output Format

```
### Creative Brief: [Direction Name]

Source: [validated overlap / whitespace / differentiator / cold ideation]
Format: [UGC / B-roll+VO / static / carousel] · Length: [target]

HOOK (0-3s)
[Line + delivery direction]

BODY
[Beat/shot list or panel breakdown]

CTA
[Line + treatment]

COPY
Primary text: ...
Headline: ...

VARIATIONS TO TEST ALONGSIDE
1. [Copy variant]
2. [Angle variant]
3. [Hook variant]
```

## Guardrails

- Never fabricate a specific claim, stat, or testimonial in the copy — placeholder clearly (`[insert verified stat]`) rather than inventing one.
- Flag anything that reads close to a competitor's specific creative execution (not just angle/pattern) rather than an original take built from the pattern.
- Keep briefs specific enough to shoot from — "make it relatable" is not a brief; "open on hands struggling to open packaging, cut to product in 2s" is.

