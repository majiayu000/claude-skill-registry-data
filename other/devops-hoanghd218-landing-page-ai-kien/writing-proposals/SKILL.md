---
name: writing-proposals
description: Use when creating or pricing energy consulting proposals including ASHRAE Level 1/2/3 audits, benchmarking services, commissioning, compliance pathway consulting, and performance target analysis. Provides pricing models, cost estimation, scope templates, service definitions, labor hour estimates, and proposal generation. Use when the user mentions proposal writing, pricing services, scoping work, energy audit costs, consulting rates, or needs to generate professional proposals for energy projects.
---

# Energy Consulting Proposal Development

Professional proposal development methodology for energy consulting services including pricing, scoping, service definitions, and proposal generation.

## When to Use This Skill

Invoke this skill when working with:
- **Proposal writing** - Creating professional proposals for energy consulting services
- **Pricing services** - ASHRAE audits, benchmarking, commissioning, compliance consulting
- **Scoping work** - Defining deliverables, timelines, and exclusions
- **Cost estimation** - Labor hours, pricing models (fixed fee vs T&M), complexity factors
- **Service definitions** - ASHRAE Level 1/2/3 audits, benchmarking, compliance pathway consulting
- **Proposal generation** - Using templates and scripts to create formatted proposals
- **Client types** - First-time, repeat, portfolio, institutional clients
- **Competitive pricing** - Market positioning and value propositions

## What This Skill Provides

**Pricing Guidance**:
- Service-specific pricing ranges (by building size and complexity)
- Pricing models (Fixed Fee, T&M with NTE, Tiered)
- Labor hour estimates by service type
- Complexity multipliers and adjustment factors
- Competitive market rates (2025 Denver market)

**Service Definitions**:
- ASHRAE Level 1/2/3 energy audit scopes
- Benchmarking and data verification services
- Compliance pathway consulting
- Performance target analysis
- Scope templates with deliverables and timelines

**Proposal Tools**:

- **COM automation** for reliable Word template processing (Windows)
- Python script for automated proposal generation (cross-platform)
- Microsoft Word proposal templates with placeholders
- Standard proposal components and structure
- Client type-specific approaches
- JSON mapping files for batch processing

## What This Skill Does NOT Cover

- ❌ Regulatory requirements (Energize Denver, building codes) → Use **energize-denver** skill
- ❌ Technical energy modeling or engineering analysis
- ❌ Commissioning procedures or test protocols → Use **commissioning-reports** skill
- ❌ Marketing or business development strategy

## Quick Start

### Pricing a Service

1. **Identify service type** - Audit? Benchmarking? Compliance pathway?
2. **Determine building characteristics** - Size, complexity, data quality
3. **Select pricing model** - Fixed fee, T&M NTE, or tiered
4. **Calculate base price** - See [./pricing-guidelines.md](./pricing-guidelines.md)
5. **Apply adjustments** - Complexity, urgency, client type
6. **Choose payment terms** - Milestone-based or monthly

### Scoping a Project

1. **Review service scope template** - See [./service-types.md](./service-types.md)
2. **Customize tasks** - Add/remove based on client needs
3. **Define deliverables** - Reports, models, presentations
4. **Set timeline** - Account for complexity and deadlines
5. **Identify exclusions** - Clarify what's out of scope

### Generating a Proposal

#### Option 1: COM Automation (Recommended for Windows)

```bash
# Interactive mode - guided workflow
python tools/word-template-automation.py --interactive

# With mapping file - best for complex proposals
python tools/word-template-automation.py template.docx output.docx --mapping mapping.json

# Quick command-line - simple replacements
python tools/word-template-automation.py template.docx output.docx \
  --replace "{{CLIENT}}" "Acme Corp" \
  --replace "{{FEE}}" "$25,000"
```

Why use COM automation?

- ✅ Perfect formatting preservation
- ✅ Works with any template structure
- ✅ Handles headers, footers, tables, images automatically
- ✅ Reliable find/replace using Word's engine
- ⚠️ Windows only (requires Word installed)

See [./tools/README_COM_AUTOMATION.md](./tools/README_COM_AUTOMATION.md) for complete guide.

#### Option 2: Python Script (Legacy)

```bash
python scripts/generate-proposal.py --interactive
```

The script will prompt for:

- Service type
- Building information
- Pricing model
- Contact details
- Output filename

Note: This uses python-docx library with limitations. Consider COM automation for better reliability.

#### Option 3: Manual Creation

1. Use [./templates/proposal-template.docx](./templates/proposal-template.docx)
2. Fill in service-specific scope from [./service-types.md](./service-types.md)
3. Add pricing from [./pricing-guidelines.md](./pricing-guidelines.md)
4. Customize for client situation

### Iterative Feedback System (NEW!)

The conversion tool now learns from your manual corrections and automatically applies them in future conversions.

#### Enable Feedback Collection

```bash
# Convert with feedback enabled
python tools/convert-proposal-to-docx.py proposal.md --feedback

# Or provide feedback later
python tools/collect-feedback.py output.docx
```

#### How It Works

1. **Convert your proposal** - Markdown to Word
2. **Review and note manual fixes** - What did you have to change?
3. **Provide feedback** - Tell the tool what you fixed
4. **System learns** - Analyzes which fixes can be automated
5. **Future conversions improve** - Learned fixes applied automatically

#### What Gets Automated?

- ✅ Style corrections (Normal → Body Text)
- ✅ List formatting (bullets → Body List style)
- ✅ Find/replace patterns (company name consistency, etc.)
- ✅ Spacing adjustments
- ✅ Table formatting
- ✗ Template-specific content (contact info, images)
- ✗ Content requiring judgment (wording changes)

#### Example: First vs. Fifth Conversion

**First Proposal:**

- Manual fixes: 20 minutes
  - Changed 50 "Normal" to "Body Text"
  - Fixed bullet spacing on 32 items
  - Updated contact info

**Fifth Proposal (after feedback):**

- Manual fixes: 2 minutes
  - ✓ Normal → Body Text: **Already done!**
  - ✓ Bullet spacing: **Already done!**
  - Updated contact info (still manual)

**Time saved:** 18 minutes per proposal!

#### Check Template Status

See what's been learned for a template:

```bash
python tools/collect-feedback.py --status proposal-template.docx
```

See [./tools/README_FEEDBACK_SYSTEM.md](./tools/README_FEEDBACK_SYSTEM.md) for complete documentation.

## Service Types

See [./service-types.md](./service-types.md) for complete scope templates.

### Energy Audits

**ASHRAE Level 1 (Walk-Through)**:
- Preliminary assessment, low-cost ECM identification
- Timeline: 3-5 weeks
- Pricing: $5K-$30K (by building size)

**ASHRAE Level 2 (Detailed Analysis)**:
- Comprehensive engineering analysis with energy modeling
- Timeline: 8-12 weeks
- Pricing: $15K-$100K (by building size and complexity)

**ASHRAE Level 3 (Investment Grade)**:
- Detailed engineering with guaranteed savings
- Timeline: 12-16 weeks
- Pricing: $40K-$250K (by building size) or 2-4% of construction cost

### Other Services

**Benchmarking & Data Verification**:
- Annual energy performance data submission
- Timeline: 2-4 weeks
- Pricing: $2K-$12K (by building size and number of meters)

**Compliance Pathway Consulting**:
- Multi-year compliance strategy development
- Timeline: 6-8 weeks
- Pricing: $10K-$35K (by complexity and alternate compliance needs)

**Performance Target Analysis**:
- Baseline verification and target calculation
- Timeline: 2-4 weeks
- Pricing: $3K-$15K (by number of buildings and complexity)

## Pricing Models

### Fixed Fee
**Best for**: Clear scope, predictable effort
**Advantages**: Client budget certainty, incentivizes efficiency
**Risks**: Scope creep, unforeseen complexity

### Time & Materials with Not-To-Exceed (T&M NTE)
**Best for**: Uncertain scope, data quality unknown
**Structure**: Hourly rates by staff level with NTE cap
**Hourly Rates**:
- Principal Engineer: $200-$250/hr
- Senior Engineer: $150-$180/hr
- Project Engineer: $120-$150/hr
- Analyst/Coordinator: $90-$120/hr

### Tiered by Building Size
**Best for**: Portfolio work, multiple similar buildings
**Advantages**: Simple, transparent, volume discounts

See [./pricing-guidelines.md](./pricing-guidelines.md) for detailed pricing by service and building size.

## Pricing Quick Reference

| Service | Small (25k-50k sf) | Medium (50k-100k sf) | Large (100k-200k sf) | Very Large (200k+ sf) |
|---------|-------------------|---------------------|---------------------|---------------------|
| Benchmarking | $2-$3.5K | $3.5-$5K | $5-$7K | $7-$12K |
| Level 1 Audit | $5-$8K | $8-$12K | $12-$18K | $18-$30K |
| Level 2 Audit | $15-$25K | $25-$40K | $40-$60K | $60-$100K+ |
| Level 3 Audit | — | $40-$70K | $70-$120K | $120-$250K+ |
| Compliance Pathway | $10-$15K | $15-$22K | $22-$35K | Variable |
| Target Analysis | $3-$5K | $5-$8K | $8-$15K | Variable |

**Complexity Adjustments**:
- Simple (packaged equipment, good data): Base × 0.8
- Standard (typical building): Base × 1.0
- Complex (central plant, poor data): Base × 1.3
- Very Complex (campus, process loads): Base × 1.5-2.0

**Add-Ons**:
- Rush service (<50% timeline): +25-50%
- Poor data quality: +20-50%
- Portfolio discount (3+ buildings): -15-30%
- First-time client discount: -10-15%

## Proposal Components

Every professional energy consulting proposal should include:

1. **About [Company]** - Standard boilerplate (your company overview)

2. **Project Understanding**:
   - Building/project information
   - Service description and objectives
   - Context (compliance, capital planning, operational improvement)

3. **Scope of Work**:
   - Service-specific tasks (use templates from [./service-types.md](./service-types.md))
   - Timeline and milestones
   - Deliverables (reports, models, presentations)
   - Assumptions and exclusions

4. **Pricing**:
   - Fixed fee OR Time & Materials with NTE
   - Payment terms (milestone-based or monthly)
   - Proposal validity period (typically 90 days)

5. **Qualifications** (optional):
   - Relevant experience
   - Team member bios
   - Similar project examples

6. **Signature Block**: Your contact details

7. **Customer Acceptance**: Sign-off section

## Client Type Strategies

### First-Time Clients
- **Approach**: Competitive pricing to win work
- **Model**: Fixed fee for budget certainty
- **Discount**: Consider 10-15% on first project
- **Upsell**: Position for follow-on work

### Repeat Clients
- **Approach**: Fair pricing, emphasize quality and speed
- **Model**: Can use T&M for trust-based relationship
- **Benefit**: 5-10% loyalty discount or priority scheduling

### Portfolio Clients (Property Managers)
- **Approach**: Volume pricing, multi-year agreements
- **Model**: Tiered by building size with portfolio discount
- **Discount**: 15-30% for 3+ buildings
- **Value Add**: Dashboard reporting, proactive tracking

### Institutional Clients (Universities, Hospitals, Government)
- **Approach**: Detailed scope, competitive bidding
- **Model**: Fixed fee or percentage of construction
- **Requirements**: May require certified DBE/MBE participation
- **Timeline**: Longer procurement cycles

## Labor Hour Estimates

Use these estimates to validate pricing or develop T&M quotes:

**Benchmarking & Data Verification**:
- Small: 8-15 hours
- Medium: 15-25 hours
- Large: 25-40 hours
- Data quality issues: +20-50%

**ASHRAE Level 1 Audit**:
- Small: 30-50 hours
- Medium: 50-80 hours
- Large: 80-120 hours

**ASHRAE Level 2 Audit**:
- Small: 100-160 hours
- Medium: 160-260 hours
- Large: 260-400 hours

**ASHRAE Level 3 Audit**:
- Small: 180-280 hours
- Medium: 280-450 hours
- Large: 450-700 hours

**Compliance Pathway**:
- Basic: 60-100 hours
- Standard: 100-140 hours
- Complex: 140-220 hours

**Multiplier for Final Fee**: Labor hours × blended rate × overhead multiplier (1.8 to 2.5)

## Value Proposition Development

When proposing services, help clients understand the value:

### Cost Avoidance
- Calculate penalty avoidance (for compliance projects)
- Show ROI of audit vs implementation savings
- Compare audit cost to potential ECM savings

**Example**:
```
100k sf building, 25 kBtu/sf shortfall:
  Annual shortfall: 2,500,000 kBtu
  Annual penalty: $1,750,000 (at $0.70/kBtu)
  5-year penalty: $8,750,000

Compliance pathway consulting cost: $25,000
ROI: 350:1
```

### Competitive Positioning
- Emphasize domain expertise (e.g., Energize Denver knowledge)
- Highlight local presence and relationships
- Position full-service capability (benchmarking → audit → implementation → commissioning)

## Proposal Decision Tree

```
1. What service?
   ├─ Benchmarking → $2K-$12K
   ├─ Level 1 Audit → $5K-$30K
   ├─ Level 2 Audit → $15K-$100K
   ├─ Level 3 Audit → $40K-$250K
   ├─ Compliance Pathway → $10K-$35K
   └─ Target Analysis → $3K-$15K

2. What building size?
   ├─ Small (25k-50k sf) → Lower range
   ├─ Medium (50k-100k sf) → Middle range
   ├─ Large (100k-200k sf) → Upper-middle range
   └─ Very Large (200k+ sf) → Upper range

3. What complexity?
   ├─ Simple → Base × 0.8
   ├─ Standard → Base × 1.0
   ├─ Complex → Base × 1.3
   └─ Very Complex → Base × 1.5-2.0

4. What client type?
   ├─ First-time → Competitive (10% discount)
   ├─ Repeat → 5-10% loyalty discount
   └─ Portfolio → 15-30% volume discount

5. What urgency?
   ├─ Standard → Base price
   ├─ Rush → +25-50%
   └─ Critical → +50-100%
```

## Cross-References to Other Skills

**When working with Energize Denver compliance projects**, use the **energize-denver** skill:
- Article XIV requirements and deadlines
- MAI building compliance pathways
- Performance target calculations
- Penalty rates and enforcement
- Timeline extensions and alternate compliance

**When working with commissioning projects**, use the **commissioning-reports** skill:
- Commissioning scope development
- Test protocol requirements
- Report templates and formats

**Example collaborative workflow**:
- User: "Create Energize Denver MAI proposal for print shop"
- **energize-denver**: Identify MAI requirements, production efficiency pathway, Dec 31 deadline
- **writing-proposals** (this skill): Price ASHRAE Level II audit, structure scope, generate proposal

## Supporting Files

**Detailed References**:

- [./pricing-guidelines.md](./pricing-guidelines.md) - Complete pricing models, ranges, and market rates
- [./service-types.md](./service-types.md) - Scope templates for each service offering

**Tools**:

- [./tools/word-template-automation.py](./tools/word-template-automation.py) - **COM automation for Word** (recommended, Windows)
  - [Complete Guide](./tools/README_COM_AUTOMATION.md)
- [./tools/convert-proposal-to-docx.py](./tools/convert-proposal-to-docx.py) - Convert markdown to Word with template
- [./tools/extract-template-styles.py](./tools/extract-template-styles.py) - Analyze template styles
- [./scripts/generate-proposal.py](./scripts/generate-proposal.py) - Automated proposal generation (legacy)

**Templates**:

- [./templates/proposal-template.docx](./templates/proposal-template.docx) - Microsoft Word template
- [./templates/example-mapping.json](./templates/example-mapping.json) - Example placeholder mapping file

## Best Practices

**Pricing Strategy**:
- Always buffer pricing (use upper end of range unless highly confident)
- Document assumptions clearly to manage scope creep
- Be prepared to negotiate 10-15% on competitive bids
- Value over price (emphasize expertise and capability)
- Price first project competitively to win ongoing work

**Scope Development**:
- Use service templates as starting point, customize for client
- Include clear deliverables with specific format (report, model, presentation)
- Define exclusions explicitly (avoid misunderstandings)
- Set realistic timelines with buffer for client responsiveness

**Proposal Writing**:
- Keep it concise (5-15 pages typical)
- Use executive summary for decision-makers
- Make pricing clear and easy to find
- Include visuals where helpful (org chart, timeline)
- Professional formatting matters

**Payment Terms**:
- Small projects (<$10K): 50% kickoff, 50% completion
- Medium ($10K-$50K): 30% kickoff, 40% draft, 30% final
- Large (>$50K): Monthly invoicing
- Net 30 days standard

**Follow-Up**:
- Follow up within 1 week of submission
- Be prepared to present proposal in-person/virtually
- Address questions promptly
- Adjust scope/pricing if needed based on feedback

## Important Notes

**This skill provides general energy consulting methodology**. It does not:
- Replace regulatory knowledge (use **energize-denver** for compliance requirements)
- Provide technical engineering analysis or modeling
- Substitute for company-specific pricing strategy or policy

**Always verify**:
- Current market rates and competitive landscape
- Company overhead and profit margin requirements
- Client budget constraints before finalizing pricing
- Internal resource availability for proposed timelines

**Adapt to your context**:
- These pricing ranges are based on Denver 2025 market
- Adjust for regional differences, company size, expertise level
- Update based on actual wins/losses and market feedback
