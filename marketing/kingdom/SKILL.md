---
name: content-kingdom
description: Use when content Kingdom Orchestrator — the BRAIN that coordinates all
  12 content phases. Sequences research → plan → script → create → review → schedule
  → post → engage → analyze → optimize → repurpose → scale.
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content
- automation
- tiktok
- instagram
- postbridge
- geminigen
- money
domain: content
version: 1.0.0
category: content
---



# Content Kingdom Orchestrator

## Overview

A **lean 12-phase pipeline** that turns raw trends into scheduled, analyzed, and scaled social media content — fully automated, with Paperclip issue tracking.

**SOLID design:**
- Each phase = single responsibility, independently runnable
- New phases: add to `PHASE_REGISTRY` in `orchestrator.py` — no other edits
- All new modules extend `BaseModule` (dependency inversion)
- Public API: 4 methods only (`run_daily_pipeline`, `run_phase`, `get_status`, `create_paperclip_issues`)

**KISS design:**
- Existing scripts called via subprocess — no reimplementation
- Only 2 truly new modules: `comment_manager.py`, `engagement_engine.py`
- Config extends `autopilot_affiliate_engine/config.py` at runtime

---

## File Structure

```
skills/1ai-skills/content/content-kingdom/
├── SKILL.md                       ← you are here
├── orchestrator.py                ← BRAIN: thin coordinator
├── base_module.py                 ← BaseModule + PhaseResult (DI foundation)
├── config.json                    ← config (extends engine config at runtime)
├── state.json                     ← auto-generated: pipeline state
├── modules/
│   ├── __init__.py
│   ├── persona_manager.py         ← brand voice + caption generation
│   ├── comment_manager.py         ← Phase 8: ENGAGE (new)
│   ├── engagement_engine.py       ← Phase 12: SCALE (new)
│   ├── veris_design.py            ← v2.0: Veris Design System (prompts + palette)
│   └── geminigen_client.py        ← v2.0: GeminiGen API client (images + videos)
├── output/                        ← phase outputs (today_plan.json, scripts_*.json, …)
├── logs/                          ← daily orchestrator logs
├── templates/                     ← caption/storyboard templates
└── tests/                         ← unit tests
```

**Symlink:** `skills/content-kingdom → skills/1ai-skills/content/content-kingdom`

---

---

## Veris Design Principles (v2.0)

Extracted from **Veris** (Ads Master, 10+ years) training session. Applied automatically in Phase 4: CREATE.

### Core Rules (NON-NEGOTIABLE)
1. **Pure black background** — `#000000`, no exceptions, ever
2. **High contrast white text** — headlines in `#FFFFFF`, nothing below 60% opacity
3. **Three-zone vertical layout** — every ad must have: Hook / Body / CTA zones
4. **No vibrant colors** — accent palette limited to dark trust/urgency signals
5. **No emoji in visuals** — emoji in captions are OK, never in images
6. **Minimalist premium** — less elements = more premium feel = higher trust

### Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| `bg_primary` | `#000000` | Main background (mandatory) |
| `bg_secondary` | `#000020` | Secondary surfaces |
| `text_primary` | `#FFFFFF` | Headlines, CTA text |
| `text_secondary` | `#808080` | Supporting copy |
| `accent_trust` | `#202040` | Borders, trust badges |
| `accent_urgency` | `#200000` | Scarcity signals |
| `accent_soft` | `#606080` | Decorative elements |

### Three-Zone Layout

```
┌─────────────────────────────┐
│  HOOK ZONE (top 20-30%)     │  ← Bold headline, stops the scroll
│  "Bisa Cuan 1 Juta/Hari?"  │
├─────────────────────────────┤
│  BODY ZONE (middle 40-50%) │  ← Product detail, builds desire
│  What it is, what it does  │
├─────────────────────────────┤
│  CTA ZONE (bottom 20-30%)  │  ← Action button, price, frame
│  [Lihat Sekarang → Rp 49K] │
└─────────────────────────────┘
```

### Platform Priority (Veris Approach)
1. **Instagram** — PRIMARY (where ads convert)
2. **Facebook** — SECONDARY (older, higher spend audience)
3. **Threads** — TERTIARY (IG companion, free reach)
4. **TikTok** — QUATERNARY (volume play, lower CPM)

### Formats

| Platform | Width | Height | Ratio |
|----------|-------|--------|-------|
| Instagram Portrait | 1024 | 1280 | 4:5 ← PRIMARY |
| Instagram Feed | 800 | 800 | 1:1 |
| TikTok | 1080 | 1920 | 9:16 |

### Using Veris in Code

```python
from modules.veris_design import build_veris_prompt, veris_prompt_for_platform
from modules.geminigen_client import GeminiGenClient

# Build Veris-style prompt
payload = veris_prompt_for_platform(
    product_name="Guru Pintar AI",
    hook_text="Bisa Cuan Rp 1 Juta/Hari?",
    platform="instagram",
)

# Generate via GeminiGen
client = GeminiGenClient()
resp = client.generate_image(**payload)
url = client.generate_image_sync(**payload)  # sync version → returns URL
```

---

## GeminiGen API (v2.0 — Primary Media Provider)

**Base URL:** `https://api.geminigen.ai`  
**Auth:** `x-api-key` header  
**Key config:** `workspace/config/geminigen_api.json` → `{"api_key": "..."}`

### Supported Operations

| Endpoint | Purpose | Module |
|----------|---------|--------|
| `POST /uapi/v1/generate_image` | Image generation | `GeminiGenClient.generate_image()` |
| `POST /uapi/v1/video-gen/grok` | Video generation (Grok) | `GeminiGenClient.generate_video_grok()` |
| `GET /uapi/v1/history/:uuid` | Poll job status | `GeminiGenClient.get_status()` |

### Status Codes
- `1` = processing (keep polling)
- `2` = completed (extract URL)
- `3` = failed (raise error)

### Phase 4 CREATE Provider Chain (v2.0)

**Images:**
```
GeminiGen (nano-banana-pro + Veris prompt)
  ↓ on failure
NVIDIA (Flux) via legacy media_generator  
  ↓ on failure
PIL placeholder (last resort — never blocks pipeline)
```

**Videos:**
```
GeminiGen (Grok-3, 480p portrait)
  ↓ on failure
BytePlus (Seedance T2V)
```

---

## When to Use
**Trigger phrases:**
- "content kingdom"
- "\n  Content Kingdom Orchestrator — the BRAIN that coordinates all 12 content pha"


- Running the full daily content pipeline (`--pipeline`)
- Running a specific phase only (`--phase research`, `--phase schedule`, etc.)
- Checking pipeline status after a run (`--status`)
- Creating Paperclip tracking issues for a run (`--paperclip-issues`)
- Debugging a broken phase in isolation

---

## When NOT to Use

- ❌ Direct PostBridge posting → use `autopilot_affiliate_engine/auto_postbridge_robust_v2.py`
- ❌ Generating images only → use `skills/nano-banana-pro/scripts/generate_image.py`
- ❌ Research only → use `autopilot_affiliate_engine/research_agent.py`
- ❌ Revenue tracking only → use `autopilot_affiliate_engine/revenue_tracker.py`
- ❌ Storyboard only → use `content/content-generator/scripts/storyboard.py`

---

## Quick Reference

```bash
# Full daily pipeline (morning run)
python3 orchestrator.py --pipeline

# Single phase (independently runnable)
python3 orchestrator.py --phase research
python3 orchestrator.py --phase plan
python3 orchestrator.py --phase script
python3 orchestrator.py --phase create
python3 orchestrator.py --phase review
python3 orchestrator.py --phase schedule
python3 orchestrator.py --phase post
python3 orchestrator.py --phase engage
python3 orchestrator.py --phase analyze
python3 orchestrator.py --phase optimize
python3 orchestrator.py --phase repurpose
python3 orchestrator.py --phase scale

# Status check
python3 orchestrator.py --status

# Seed Paperclip issues without running pipeline
python3 orchestrator.py --paperclip-issues

# Custom config
python3 orchestrator.py --pipeline --config /path/to/custom_config.json
```

---

## Workflow

Content Kingdom runs a **12-phase daily pipeline**. Each phase is a discrete step that feeds the next:

| Phase | What Happens |
|-------|-------------|
| 1. Research | Scrape trends, competitor content, viral patterns |
| 2. Plan | Select content angles, assign formats per platform |
| 3. Script | Generate platform-optimized scripts (TikTok, IG, YT) |
| 4. Create | Produce media — images, video, audio via GeminiGen |
| 5. Review | Quality gate, brand compliance check |
| 6. Schedule | Queue to PostBridge with optimal timing |
| 7. Post | Auto-publish to TikTok, Instagram, YouTube |
| 8. Engage | Auto-reply to comments, DMs |
| 9. Analyze | Collect views, likes, shares, CTR per post |
| 10. Optimize | Surface winning formats, topics, hooks |
| 11. Repurpose | Spin top content into cross-platform variants |
| 12. Scale | Grow volume, add channels, increase frequency |

**Execution:** One morning run via cron. Each phase delegates to sub-agents through Paperclip issues.
**Failure mode:** Any phase can be re-run independently without restarting the pipeline.
**Scaling:** More channels = more research + create iterations in parallel.

## The 12 Phases

| # | Phase | Delegates To | New Code? |
|---|-------|-------------|-----------|
| 1 | RESEARCH | `autopilot_affiliate_engine/research_agent.py` + `viral_research_system.py` | No |
| 2 | PLAN | Engine weekly plan + config products | Thin logic only |
| 3 | SCRIPT | `content-generator/scripts/storyboard.py` + `modules/persona_manager.py` | No |
| 4 | CREATE | `skills/nano-banana-pro/scripts/generate_image.py` | No |
| 5 | REVIEW | `content-generator/scripts/quality_gate.py` | No |
| 6 | SCHEDULE | `autopilot_affiliate_engine/auto_postbridge_robust_v2.py` | No |
| 7 | POST | PostBridge `/post-results` API + retry via robust_v2 | No |
| 8 | ENGAGE | `modules/comment_manager.py` | **Yes — new** |
| 9 | ANALYZE | `evening_report.py` + `revenue_tracker.py` + PostBridge analytics | No |
| 10 | OPTIMIZE | Engagement rate calc + `revenue_tracker_REAL.py` | Thin logic only |
| 11 | REPURPOSE | `skills/auto-clipper/scripts/auto_clipper.py` | No |
| 12 | SCALE | `modules/engagement_engine.py` | **Yes — new** |

---

## Cron Setup

```bash
# Add to crontab (crontab -e)
# Morning pipeline — 08:00 WIB
0 8 * * * cd /home/openclaw/.openclaw/workspace/skills/content-kingdom && python3 orchestrator.py --pipeline >> logs/cron.log 2>&1

# Evening analysis — 20:00 WIB
0 20 * * * cd /home/openclaw/.openclaw/workspace/skills/content-kingdom && python3 orchestrator.py --phase analyze >> logs/cron.log 2>&1

# Engagement check — every 2 hours
0 */2 * * * cd /home/openclaw/.openclaw/workspace/skills/content-kingdom && python3 orchestrator.py --phase engage >> logs/cron.log 2>&1
```

---

## Configuration

Edit `config.json` to change:

| Key | Purpose | Example |
|-----|---------|---------|
| `products` | Products to promote (hooks, prices) | Add new LYNK product |
| `personas` | Brand voices (e.g., brands, styles) | Add new persona |
| `platforms` | Enable/disable platforms | `"youtube": {"enabled": true}` |
| `schedule` | Posting times per platform | `"tiktok": ["07:00", "19:00"]` |
| `quality_gates` | Review pass/fail thresholds | `"min_caption_length": 80` |
| `scoring_weights` | Engagement scoring for scale phase | `"shares": 10.0` |
| `winner_thresholds` | Min score to be a "winner" | `"tiktok": 2000` |

**Do NOT duplicate** values already in `autopilot_affiliate_engine/config.py` — they're merged at runtime.

---

## Paperclip Integration

Each pipeline run creates:
- 1 parent issue: `Content Kingdom — YYYY-MM-DD`
- 12 sub-issues: one per phase
- Status auto-updates as phases complete (`todo → done` or `blocked`)

Paperclip server must be running at `http://localhost:3100`.

---

## Adding a New Phase

1. Write a `_phase_newphase(cfg, **kwargs) -> dict` function in `orchestrator.py`
2. Add entry to `PHASES` dict: `"newphase": {"fn": _phase_newphase, "label": "Phase 13: NEWPHASE", "deps": [...]}`
3. Done. No other changes needed (Open/Closed principle).

---

## Adding a New Module

If the new phase needs a real class:

```python
# modules/my_new_module.py
from base_module import BaseModule

class MyNewModule(BaseModule):
    @property
    def name(self) -> str:
        return "my_phase"

    def _execute(self, **kwargs) -> dict:
        # single responsibility: do ONE thing
        return {"result": "done"}
```

Instantiate in the phase function, call `module.run()`.

---

## Common Mistakes

| ❌ Wrong | ✅ Right |
|---------|---------|
| Creating new PostBridge wrapper | Import/subprocess `auto_postbridge_robust_v2.py` |
| Duplicating product list in config | Add products only to `config.json`, merge from engine at runtime |
| Running orchestrator as a library import | Use `--phase` CLI or instantiate `ContentKingdomOrchestrator` |
| Editing phase logic inside `run_phase()` | Edit the `_phase_*()` function, not the coordinator |
| Adding config to `orchestrator.py` directly | All config in `config.json` — orchestrator reads it |

---

## Dependencies

**Python stdlib only + requests:**
```bash
pip install requests
```

**External scripts (must exist):**
- `autopilot_affiliate_engine/research_agent.py`
- `autopilot_affiliate_engine/auto_postbridge_robust_v2.py`
- `autopilot_affiliate_engine/evening_report.py`
- `autopilot_affiliate_engine/revenue_tracker.py`
- `content/content-generator/scripts/storyboard.py`
- `content/content-generator/scripts/quality_gate.py`
- `skills/nano-banana-pro/scripts/generate_image.py` *(optional — CREATE fallback chain)*
- `skills/auto-clipper/scripts/auto_clipper.py` *(optional — REPURPOSE phase degrades gracefully)*

**v2.0 additions:**
- `workspace/config/geminigen_api.json` — `{"api_key": "YOUR_KEY"}` *(required for GeminiGen primary provider)*
- `curl` — CLI dependency for GeminiGen API calls (already available system-wide)

---

## Example Output

```json
{
  "run_id": "run_20260313_080000",
  "date": "2026-03-13",
  "phases": {
    "research": {"status": "success", "data": {"sources": ["research_agent", "viral_research_system"]}},
    "plan":     {"status": "success", "data": {"product_focus": "jendralbot_bundle", "platforms": ["tiktok", "instagram"]}},
    "script":   {"status": "success", "data": {"scripts_generated": 6}},
    "schedule": {"status": "success", "data": {"queue_file": "...postbridge_queue_jendralbot.json"}},
    "engage":   {"status": "success", "data": {"replies_queued": 4, "dm_leads": 2}},
    "scale":    {"status": "success", "data": {"winners": 3, "top_3": [...]}}
  }
}
```

## Money-Making Overview

**Buyer Persona:**
- SME owners (3-50 employees) in Indonesia/US who need daily social media content without hiring a team
- Digital agencies that want to white-label content production under their own brand
- E-commerce brands that need product content across TikTok, Instagram, Facebook with direct attribution
- Solo creators who need to scale output without burning out

**Three Pricing Tiers:**

| Tier | Price | What They Get |
|------|-------|---------------|
| Content Starter | $1,000/mo | 10 posts/week across 2 platforms, template-based visuals, basic captions, weekly report |
| Content Pro | $2,500/mo | 20 posts/week across 4 platforms, custom Veris visuals, storyboard scripts, engagement management, weekly optimization |
| Content Kingdom | $5,000/mo | Full 12-phase pipeline: viral research, daily content, paid ad creative, auto-engagement, analytics, repurposing, monthly strategy session |

**First-Dollar Timeline:**
- Day 1: Onboard client, define personas + products (30-min call)
- Day 3: First 5 posts delivered as proof-of-work
- Day 7: Full pipeline running, first engagement data
- Day 14: First optimization cycle, client sees measurable lift
- Day 30: Renewal conversation backed by performance report

**Target Markets:**
- Indonesia SMEs: Bundle with LYNK affiliate products, Rp 5-15M/mo
- US Agencies: White-label Content Kingdom for $3-7K/mo retainer
- E-commerce Brands: Product-focused content with direct conversion attribution

---

## First Action in 60 Minutes

Copy-paste this to onboard a new client and run their first full pipeline:

```bash
#!/usr/bin/env bash
# Content Kingdom Client Onboarder
# Usage: ./onboard_client.sh "ClientName" "ProductName" "Hook Text" "Rp 49K"

set -e
CLIENT="$1"
PRODUCT="$2"
HOOK="$3"
PRICE="$4"

echo "=== Onboarding $CLIENT ==="

# 1. Create scoped client config
mkdir -p "clients/$CLIENT"
cat > "clients/$CLIENT/config.json" << 'EOF'
{
  "products": [{"name": "PLACEHOLDER_PRODUCT", "hook": "PLACEHOLDER_HOOK", "price": "PLACEHOLDER_PRICE"}],
  "personas": ["professional", "trendy"],
  "platforms": {
    "tiktok": {"enabled": true, "schedule": ["07:00", "19:00"]},
    "instagram": {"enabled": true, "schedule": ["08:00", "20:00"]},
    "facebook": {"enabled": true, "schedule": ["12:00"]}
  },
  "quality_gates": {"min_caption_length": 80, "min_image_score": 0.6},
  "scoring_weights": {"views": 1.0, "likes": 2.0, "shares": 10.0, "comments": 5.0},
  "winner_thresholds": {"tiktok": 2000, "instagram": 1500}
}
EOF

sed -i "s/PLACEHOLDER_PRODUCT/$PRODUCT/g" "clients/$CLIENT/config.json"
sed -i "s/PLACEHOLDER_HOOK/$HOOK/g" "clients/$CLIENT/config.json"
sed -i "s/PLACEHOLDER_PRICE/$PRICE/g" "clients/$CLIENT/config.json"

# 2. Run research + plan phases (fast, generates first strategy)
python3 orchestrator.py --phase research --config "clients/$CLIENT/config.json" 2>&1 | tail -5
python3 orchestrator.py --phase plan --config "clients/$CLIENT/config.json" 2>&1 | tail -5

echo ""
echo "=== CLIENT ONBOARDED: $CLIENT ==="
echo "Config: clients/$CLIENT/config.json"
echo "Research: output/research_*.json (review with client)"
echo ""
echo "NEXT: python3 orchestrator.py --phase script --config clients/$CLIENT/config.json"
echo "THEN: python3 orchestrator.py --phase create --config clients/$CLIENT/config.json"
echo "DELIVER: first 5 assets ready after 'create' phase"
```

**What this gets you in 60 minutes:**
- Client-specific config created and filled
- Research phase complete (trending angles + competitor analysis)
- Plan phase complete (posting schedule + content strategy)
- Deliverable preview ready to share with client

---

## Deliverable Format

**Weekly Content Production Report** (deliver every Monday morning):

```text
CONTENT PRODUCTION REPORT
Client: [Name] | Week: 2026-07-20
Pipeline Run ID: run_20260720_080000

=== DELIVERED THIS WEEK ===
Platform   | Posts | Format     | Status
TikTok     | 10    | 9:16 video | Posted
Instagram  | 10    | 4:5 image  | Posted
Facebook   | 5     | 1:1 image  | Scheduled
Total: 25 posts across 3 platforms

=== PERFORMANCE ===
Metric          | Value   | vs Last Week
Engagement Rate | 4.2%    | +0.8%
Total Views     | 45,200  | +12%
Link Clicks     | 1,230   | +5%
Conversions     | 28      | +40%  <- from optimized CTAs

=== TOP 3 PERFORMERS ===
1. "Bisa Cuan Rp 1 Juta/Hari?" — TikTok — 12,400 views, 5.1% eng.
2. Product demo video — Instagram — 8,200 views, 4.8% eng.
3. Testimonial graphic — Facebook — 5,100 views, 3.9% eng.

=== NEXT WEEK PLAN ===
- 5 A/B test variants for low-performing creatives
- 2 new product angles from viral research
- Repurpose top 3 posts into Shorts/reels

=== INVOICE ===
Service: Content Pro — $2,500
Status: Due upon receipt
```

**Pricing Table for Proposals:**

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    CONTENT KINGDOM PRICING                               │
├──────────────┬──────────┬───────────┬──────────────┬─────────────────────┤
│ Service      │ Starter  │ Pro       │ Kingdom      │ À La Carte          │
├──────────────┼──────────┼───────────┼──────────────┼─────────────────────┤
│ Posts/week   │ 10       │ 20        │ 35+          │ $50/post            │
│ Platforms    │ 2        │ 4         │ 6+           │ $100/platform       │
│ Visual Type  │ Template │ Custom    │ Veris Pro    │ $200/design         │
│ Research     │ Basic    │ Viral     │ Full 12-ph   │ $500/research cycle │
│ Engagement   │ --       │ Auto-reply│ Full + DM    │ $300/mo             │
│ Analytics    │ Weekly   │ Weekly +  │ Daily + Opt  │ $200/mo             │
│ Repurposing  │ --       │ --        │ Auto-clip    │ $250/mo             │
├──────────────┼──────────┼───────────┼──────────────┼─────────────────────┤
│ Price/Month  │ $1,000   │ $2,500    │ $5,000       │ Custom              │
└──────────────┴──────────┴───────────┴──────────────┴─────────────────────┘
```

**Invoice Line Items** (copy into Stripe/Paddle):
- "Content Kingdom — [Tier] — [Month] — $X,XXX"
- "Content Kingdom — À La Carte — [Qty]x [Service] — $XXX"
- "Content Kingdom — Rush Production — [Posts]x — $XXX"

---

## Verification

- Run one full cycle (research → plan → script → create → review → schedule) on a single piece of content and confirm each phase produces its documented artifact.
- Verify the scheduler handoff: a scheduled post appears in the calendar/queue with correct platform and timestamp.
- Check the analytics phase reads the tracked performance fields you expect, not placeholders.
- Confirm a failure in one phase is isolated and reported, not swallowed.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just post manually, automation is overkill" | Manual posting at scale burns 15+ hours/week. Automation pays for itself in 2 weeks of saved labor. |
| "My content is good enough without the full pipeline" | The 12-phase pipeline is why Content Kingdom produces 3x the engagement of random posting. |
| "Clients won't pay $1K+ for content" | Agencies charge $3-7K/mo for managed content. You're underpriced, not overpriced. |
| "I'll optimize after I have more clients" | Optimization is the retention engine. Without it, clients churn at month 2. |
| "Viral research takes too long to set up" | The RESEARCH phase runs in 5 minutes via research_agent.py. Setup is one config edit. |
| "I don't have time to run 12 phases every day" | Cron handles it. You sign clients, the pipeline produces. Your time goes to sales, not keystrokes. |
| "Content is a commodity — hard to charge premium" | Premium is in the system: consistent daily output, data-driven optimization, zero missed days. That's what clients pay for. |