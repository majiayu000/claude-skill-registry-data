---
name: journey-architect
description: 'End-to-end customer journey mapping engine with gated progression model that designs every touchpoint from awareness through advocacy. Use when: customer journey, buyer journey, journey map, touchpoints, conversion funnel, buying process, customer experience mapping.'
---

# Journey Architect (7-GATE Model)

Design the complete customer journey with measurable gates. Maps every touchpoint from first awareness through purchase, activation, and advocacy with friction scoring at each stage.

## When to Use
- Pre-launch journey design
- Conversion funnel optimization
- Content strategy planning
- Sales process design
- Customer experience improvement

## What You'll Need
**Critical inputs (ask if not provided):**
- Product/service being mapped
- Primary buyer persona(s)
- Current sales motion (PLG, sales-led, hybrid)

**Nice-to-have:**
- Market Analyzer segment data
- Existing funnel metrics
- Customer feedback or interview data

## Process

### Step 1: Define the 7 Gates
Each gate represents a cognitive/behavioral milestone customers must pass through:

| Gate | Name | Customer State | Key Question They Ask |
|------|------|---------------|----------------------|
| G1 | **Awakening** | Recognizes they have a problem | "Is this actually a problem worth solving?" |
| G2 | **Exploration** | Begins researching solutions | "What options exist to solve this?" |
| G3 | **Consideration** | Builds a shortlist | "Which 2-3 solutions should I evaluate seriously?" |
| G4 | **Conviction** | Commits to a solution | "Can I justify this purchase internally?" |
| G5 | **Activation** | Starts using the product | "How do I get value from this quickly?" |
| G6 | **Integration** | Product becomes embedded in workflow | "How does this fit into everything else I do?" |
| G7 | **Amplification** | Becomes an advocate | "Who else needs to know about this?" |

### Step 2: Per-Gate Analysis
For EACH gate, document:

**Entry Trigger**: What event causes the customer to enter this gate?
- Example G1: "Budget review reveals 30% waste in current tooling"

**Information Needs**: What content/evidence do they need?
- Example G3: "Feature comparison matrix, pricing transparency, peer reviews"

**Touchpoints**: Where do they interact?
- Example G2: "Web search, peer communities, review sites, analyst reports"

**Friction Points**: What slows them down or causes abandonment?
- Example G4: "Procurement requires security review, no SOC2 documentation available"

**Exit Criteria**: What must be true for them to advance?
- Example G5: "Completed first core workflow within 48 hours of signup"

**Conversion Benchmark**: Target percentage that pass through
- Example: G1->G2: 40%, G2->G3: 25%, G3->G4: 30%, G4->G5: 70%, G5->G6: 50%, G6->G7: 20%

### Step 3: Persona Overlay
Map each persona through the 7 gates separately:
- Where do different personas enter the journey? (not always at G1)
- Which gates do they skip or combine?
- Where do different personas have different friction points?
- Who else is involved at each gate? (champion vs. decision maker vs. blocker)

### Step 4: Friction-to-Fix Scoring
For every friction point identified, score:

| Factor | Scale | Description |
|--------|-------|-------------|
| Severity | 1-5 | How badly does it block progression? |
| Frequency | 1-5 | What % of customers hit this? |
| Fix Difficulty | 1-5 | How hard to resolve? (inverse for priority) |

**Priority Score** = (Severity x Frequency) / Fix Difficulty

Sort descending. Top 10 friction points become the action list.

## Output
Save to `outputs/journey-map-[product]-[YYYY-MM-DD].md`

### Deliverables:
1. **7-Gate Journey Map**: Full lifecycle map with triggers, touchpoints, content needs, and exit criteria per gate
2. **Friction Inventory**: Scored and prioritized list of every friction point across all gates
3. **Persona Path Variations**: How different personas navigate differently through the 7 gates
4. **Content/Asset Requirements**: What content, tools, and experiences are needed at each gate

## Chain Connections
- **Next skill**: Run `battle-scanner` to understand how competitors perform at each gate
- **Also feeds**: `demand-engine` (G1-G2 needs become demand gen strategy), `enablement-forge` (G3-G4 needs become sales assets), `growth-loop` (G5-G7 design becomes retention strategy)
- **Enhanced by**: Run after `market-analyzer` (segment data shapes persona paths)
