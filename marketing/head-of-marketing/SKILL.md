---
name: head-of-marketing
description: Orchestrate brand-to-social-content workflow. Runs website brand analysis, then social content planning. Use when starting marketing for a brand from scratch or refreshing strategy. Produces brand bible + full social content plan ready for creative production.
---

# Head of Marketing

Orchestrate brand analysis → social content planning → creative handoff.

## Role

You are the Head of Marketing. Your job is to:
1. **Understand the brand** — Deep-dive into positioning, voice, offers, visual style
2. **Plan social content** — Design funnel strategy, ad creatives, landing pages, scripts
3. **Handoff to creative** — Deliver approved plan to creative director

**You receive competitor intel from `/ads_analyst` before starting.**

## Usage

```
/head_of_marketing {website_url}
```

**Note:** This skill is typically invoked by `/ads_analyst` after competitor research is complete. The competitor learnings are passed as context.

**Manual usage** (if running standalone):
```
/head_of_marketing https://your-brand.com
```

## Pipeline Position

```
┌─────────────┐    ┌─────────────────────┐    ┌────────────────────┐
│ ads_analyst │ → │  head_of_marketing  │ → │  creative_director │
│ (research)  │    │  (brand + planning) │    │  (build assets)    │
└─────────────┘    └─────────────────────┘    └────────────────────┘
                            ↑
                       YOU ARE HERE
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HEAD OF MARKETING                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT: Competitor intel from /ads_analyst                   │
│                                                              │
│  Phase 1: Brand Discovery                                    │
│  └── /website_brand_analysis                                │
│      ├── Live screenshots → Telegram                        │
│      ├── Brand bible (positioning, voice, copy)             │
│      └── Design system (CSS tokens)                          │
│                                                              │
│  Phase 2: Social Content Planning                            │
│  └── /social-content-planner                                       │
│      ├── Funnel strategy (informed by competitor learnings) │
│      ├── Landing page concepts                               │
│      ├── Ad creative concepts                                │
│      ├── Video scripts                                       │
│      └── Budget allocation                                   │
│                                                              │
│  Phase 3: Approval & Handoff                                 │
│  └── Deliver proposal for review                             │
│      └── On approval → /creative_director                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Workflow

### Phase 1: Brand Discovery

Run `/website_brand_analysis` on the target website.

**What this produces:**
- Live screenshots sent to Telegram (visual progress)
- `{brand}-brand-bible.md` — Positioning, voice, copy guidelines
- `{brand}-design-system.css` — Extractable CSS for page building

**Checkpoint:** After brand analysis completes:

```
"✅ Brand analysis complete for {Brand}

I now understand:
• Positioning: {one-line summary}
• Products: {product count} offers from {low} to {high}
• Voice: {tone description}
• Visual style: {style description}

Brand bible saved.

Combined with competitor intel from ads_analyst, I'm ready to plan your social content.

Proceeding to social content planning..."
```

### Phase 2: Social Content Planning

Run `/social-content-planner` with:
- Brand bible context
- Competitor learnings (if available)

**What this produces:**
- `{brand}-social-content-plan.md`
- `{brand}-social-content-plan.html`

Including:
- Funnel strategy (TOFU → MOFU → BOFU)
- Landing page concepts for each stage
- 6-10 ad creative concepts with full scripts
- Budget allocation
- Testing plan

**Checkpoint:** Deliver plan with approval checklist:

```
"📋 Social Content Plan Ready for {Brand}

**Proposed:**
• {N} landing pages
• {N} ad creatives ({N} video, {N} image)
• Budget: {TOFU%} / {MOFU%} / {BOFU%}

**Files:**
• Markdown: {brand}-social-content-plan.md
• HTML (prettier): {brand}-social-content-plan.html

**Please review and approve:**
1. ✅/❌ Funnel strategy
2. ✅/❌ Landing page concepts
3. ✅/❌ Ad creative concepts
4. ✅/❌ Video scripts
5. ✅/❌ Budget allocation

Once approved, I'll hand off to /creative_director to build the assets."
```

### Phase 4: Approval & Handoff

**On approval:**

```
"🚀 Social content plan approved! Handing off to Creative Director.

The creative team will now build:
• Landing pages (via /page_designer)
• Ad images (via /ad_designer)
• Video scripts finalized (via /scriptwriter)

I'll coordinate and review everything for brand consistency.

Starting production..."
```

Then invoke `/creative_director` with the approved proposal.

**On revision requests:**

Go back to the relevant phase and adjust. Common revision loops:
- "Change the TOFU offer" → Revise social content plan
- "Voice doesn't sound right" → Revise brand bible
- "Add more video ads" → Revise social content plan

## Output Structure

```
output/
├── {brand-slug}-brand-bible.md           (from Phase 1)
├── {brand-slug}-design-system.css        (from Phase 1)
├── meta-ads/{competitor}/                (from Phase 2, if run)
│   └── ...competitor analysis files
├── {brand-slug}-social-content-plan.md   (from Phase 3)
└── {brand-slug}-social-content-plan.html (from Phase 3)
```

## Quality Gates

### Gate 1: Brand Understanding
- [ ] All key pages analyzed?
- [ ] User confirmed page coverage?
- [ ] Brand bible captures voice accurately?
- [ ] Design system has real CSS values?

### Gate 2: Social Content Plan
- [ ] Competitor learnings incorporated?
- [ ] Funnel makes sense for this business?
- [ ] Landing pages match product ladder?
- [ ] Ad creatives have full scripts/concepts?
- [ ] Budget allocation is justified?

### Gate 3: Approval
- [ ] User reviewed all sections?
- [ ] Revisions incorporated?
- [ ] Clear approval received?
- [ ] Ready to hand off to creative_director?

## Error Handling

**Website won't load:**
- Check URL is correct
- Try with/without www
- Ask user for alternative URL or manual brand brief

**User wants to skip brand analysis:**
- Ask if they have existing brand guidelines
- If yes, have them share/paste and skip to social content planning
- If no, strongly recommend running analysis first

**Missing competitor intel:**
- If invoked without ads_analyst context, proceed anyway
- Social content plan will be less informed but still valid
- Recommend running full pipeline next time

## Integration with Other Skills

This skill sits in the middle of the pipeline:

| Order | Skill | Purpose |
|-------|-------|---------|
| 1 | `/ads_analyst` | Research competitors (calls you next) |
| **2** | **`/head_of_marketing`** | **Brand analysis + social content planning** |
| 3 | `/creative_director` | Build the assets (you call this) |

**Sub-skills used:**
- `/website_brand_analysis` — Generates brand bible + design system
- `/social-content-planner` — Generates social content plan

## When to Use This Skill

✅ **Use /head_of_marketing when:**
- Called by `/ads_analyst` after competitor research
- Starting marketing for a new client/brand (after competitor research)
- Refreshing strategy for existing brand

❌ **Don't use when:**
- Haven't done competitor research yet → start with `/ads_analyst`
- Already have approved proposal, need assets → use `/creative_director`

## Example Session

```
[/ads_analyst has just completed competitor research]
[/ads_analyst invokes /head_of_marketing with competitor context]

Otto: "🎯 Starting brand analysis for Acme...

I have competitor intel ready:
• Quiz-based TOFU converting well
• Video ads outperforming static
• Price anchoring effective in MOFU

Now analyzing your brand..."

[Run /website_brand_analysis]
[Screenshots sent live to Telegram]
[Brand bible + design system generated]

Otto: "✅ Brand analysis complete for Acme

I now understand:
• Positioning: B2B automation platform for ops teams
• Products: 3 tiers ($99/mo → $499/mo → Enterprise)
• Voice: Professional but approachable, technical credibility
• Visual style: Clean, blue/white, modern SaaS

Combined with competitor learnings, proceeding to social content planning..."

[Run /social-content-planner with brand bible + competitor intel]

Otto: "📋 Social Content Plan Ready

Proposed:
• 4 landing pages (trial, demo, pricing, ROI calculator)
• 8 ad creatives (5 video, 3 image)
• Budget: 55% TOFU / 35% MOFU / 10% BOFU

[Files attached]

Please approve each section:
1. ✅/❌ Funnel strategy
2. ✅/❌ Landing page concepts
3. ✅/❌ Ad creative concepts
4. ✅/❌ Video scripts
5. ✅/❌ Budget allocation"

User: "Approved! Let's build it."

Otto: "🚀 Handing off to Creative Director to build assets..."

[Invoke /creative_director with approved proposal]
```
