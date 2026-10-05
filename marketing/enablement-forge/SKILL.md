---
name: enablement-forge
description: 'Sales and marketing enablement asset creation system that generates structured materials from pitch decks to objection handlers to ROI calculators. Use when: sales enablement, create battle cards, pitch deck, sales assets, talk tracks, objection handling, sales collateral, marketing assets.'
---

# Enablement Forge (CRAFT System)

Production engine that takes positioning, competitive intelligence, and journey data and turns them into ready-to-use sales and marketing assets.

## When to Use
- Pre-launch asset creation
- Sales team onboarding materials
- New persona/segment asset builds
- Competitive displacement campaigns
- Quarterly asset refresh

## What You'll Need
**Critical inputs (ask if not provided):**
- Product being sold
- Target buyer persona(s)
- Sales motion (PLG, sales-led, hybrid)

**Nice-to-have:**
- Position Lock output (messaging backbone)
- Battle Scanner output (competitive intelligence)
- Journey Architect output (stage-specific needs)

## Process

### Step 1: Asset Inventory Matrix
Map required assets by journey stage x asset type:

| Asset Type | G1-G2 Awareness | G3 Consideration | G4 Conviction | G5-G7 Post-Sale |
|-----------|----------------|------------------|---------------|-----------------|
| **Pitch materials** | Elevator pitch | Demo script, 1-pager | Executive deck | QBR template |
| **Competitive** | Category POV | Comparison sheet | Displacement guide | Competitive alert |
| **Evidence** | Industry report | Case study | ROI analysis | Success story |
| **Technical** | Architecture overview | Integration guide | Security whitepaper | API docs |
| **Enablement** | Discovery questions | Talk tracks | Objection handler | Expansion playbook |
| **Self-service** | Assessment tool | Interactive demo | ROI calculator | Health check tool |

### Step 2: CRAFT Brief per Asset
For each priority asset:

| Field | What It Defines |
|-------|----------------|
| **C**ontext | What situation triggers need for this asset? |
| **R**ole | Who uses it? (AE, SDR, SE, CSM, prospect, marketing) |
| **A**sset-type | Specific format (deck, 1-pager, video script, calculator) |
| **F**ormat | Structural template with sections and word counts |
| **T**rigger | What event signals this asset should be deployed? |

### Step 3: Asset Prioritization
Score each asset:
- **Usage frequency** (1-5): How often will this be used?
- **Deal impact** (1-5): How much does it affect win rates?
- **Creation effort** (1-5): How much effort to produce?

**Asset Priority** = (Frequency x Impact) / Effort

Phase assets into:
- **Must-have for launch**: Priority 5.0+
- **Fast-follow (30 days)**: Priority 3.0-4.9
- **Backlog**: Below 3.0

### Step 4: Content Generation
For each top-priority asset, produce:
- Structured outline with section-by-section content
- Key messages (from Position Lock cascade)
- Proof points (from Battle Scanner evidence)
- Persona-specific variants where needed
- Design/format notes for production team

## Output
Save to `outputs/enablement-[YYYY-MM-DD].md`

### Deliverables:
1. **Asset Inventory Matrix**: Complete map of all needed assets with priority scores
2. **CRAFT Briefs**: Detailed creation briefs for top-priority assets
3. **Asset Content Drafts**: Structured drafts for must-have assets
4. **Enablement Playbook**: When and how to deploy each asset by selling scenario

## Chain Connections
- **Next skill**: Run `partner-blueprint` to create partner-specific asset variants
- **Also feeds**: `launch-command` (assets are a launch readiness gate), `growth-loop` (post-sale assets)
- **Enhanced by**: Run after `position-lock` + `battle-scanner` + `journey-architect`
