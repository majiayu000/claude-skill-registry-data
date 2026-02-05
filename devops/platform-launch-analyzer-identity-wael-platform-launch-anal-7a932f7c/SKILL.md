---
name: platform-launch-analyzer
description: Comprehensive platform viability assessment tool based on Azoulay & Tucker's framework. Use when evaluating platform business ideas, assessing platform-market fit, preparing for investor pitches, or deciding between platform vs traditional business models. Analyzes coring, seeding, tipping, network effects, and competitive dynamics.
---

# Platform Launch Analyzer

A comprehensive assessment tool for evaluating platform business viability based on the Azoulay & Tucker Platform Strategy framework. This skill helps entrepreneurs make data-driven decisions about whether to pursue a platform strategy.

## Quick Start

For a 5-minute viability check:
```bash
python scripts/quick_check.py
```

For a comprehensive assessment:
```bash
python scripts/platform_assessment.py --interactive
```

## When to Use This Skill

Use this skill when:
- Evaluating a new platform business idea
- Deciding between platform vs. traditional business model
- Preparing for investor pitches
- Assessing competitive positioning
- Identifying weaknesses in platform strategy
- Planning platform launch sequence

## Core Components

### Assessment Scripts

#### Quick Check (5 minutes)
`scripts/quick_check.py` - Rapid pass/fail assessment covering:
- Critical requirements (must-pass)
- Major indicators (key success factors)
- Red flags identification

Run this first to determine if deeper analysis is warranted.

#### Comprehensive Assessment (20 minutes)
`scripts/platform_assessment.py` - Detailed evaluation across six dimensions:
1. Core Definition (Coring) - Platform design quality
2. Network Effects - Growth potential
3. Seeding Strategy - Launch viability
4. Competitive Dynamics - Market positioning
5. Value Creation - Problem-solving clarity
6. Pricing Strategy - Monetization approach

Generates detailed report with:
- Numerical scores by category
- Specific strengths and risks
- Strategic recommendations
- Next steps guidance

### Usage Modes

**Interactive Mode** (Recommended for first-time use):
```bash
python scripts/platform_assessment.py --interactive
```
Guides you through questions with explanations.

**Batch Mode** (For multiple assessments):
```bash
python scripts/platform_assessment.py --input assessment.json --output report.txt
```
Use templates in `assets/` folder.

**JSON Output** (For integration):
```bash
python scripts/platform_assessment.py --input assessment.json --format json
```
Structured data for further analysis.

## Reference Guides

Load these references when diving deep into specific areas:

### Platform Design
**`references/coring_checklist.md`** - Comprehensive guide covering:
- The 5 essential coring questions
- Platform core coherence test
- Governance design patterns
- Control mechanisms
- Common coring failures

Use when: Designing or refining platform core

### Launch Strategy  
**`references/seeding_strategies.md`** - Tactical playbook including:
- Overcoming chicken-egg problem
- Marquee user acquisition
- Geographic concentration strategies
- Stand-alone value creation
- Incentive design
- Industry-specific tactics

Use when: Planning go-to-market strategy

### Competition Analysis
**`references/competitive_dynamics.md`** - Strategic framework covering:
- WTAoM (Winner-Take-All or Most) assessment
- Competitive tactics (offensive/defensive)
- Tipping point indicators
- Platform war patterns
- Exit strategies

Use when: Analyzing competitive landscape

## Assessment Examples

### Using Templates

1. Copy template:
```bash
cp assets/assessment_template.json my_platform.json
```

2. Edit with your platform details

3. Run assessment:
```bash
python scripts/platform_assessment.py --input my_platform.json
```

### Learning from Examples

Study successful platform assessments:
- `assets/example_airbnb.json` - How AirBnB would score

## Interpreting Results

### Overall Scores
- **75-100%**: Strong viability - proceed with confidence
- **60-74%**: Moderate viability - address weaknesses first
- **45-59%**: Questionable - significant challenges
- **<45%**: Weak viability - reconsider platform approach

### Category Thresholds
Critical categories (must score >50%):
- Core Definition
- Network Effects
- Seeding Strategy

Important categories (should score >40%):
- Competitive Dynamics
- Value Creation
- Pricing Strategy

### Red Flags (Automatic Concerns)
- Undefined platform sides
- No solution to chicken-egg problem
- Weak network effects
- No differentiation from competitors
- Unclear monetization path

## Advanced Usage

### Comparative Analysis
Run assessments for multiple variations:
```bash
# Assess marketplace model
python scripts/platform_assessment.py --input marketplace_model.json --output marketplace_report.txt

# Assess SaaS-platform hybrid
python scripts/platform_assessment.py --input hybrid_model.json --output hybrid_report.txt
```

### Sensitivity Analysis
Test different scenarios:
1. Best case (strong network effects)
2. Base case (moderate assumptions)
3. Worst case (weak network effects)

### Iteration Tracking
Save assessments over time:
```bash
# Name with dates
python scripts/platform_assessment.py --input platform.json --output reports/2024_01_assessment.txt
```

## Decision Framework

Based on assessment results:

### GREEN LIGHT (Score >75%)
1. Proceed with detailed business planning
2. Build MVP/prototype
3. Begin marquee user recruitment
4. Seek seed funding

### YELLOW LIGHT (Score 60-74%)
1. Address identified weaknesses
2. Run focused experiments
3. Refine platform core
4. Re-assess in 30 days

### RED LIGHT (Score <60%)
1. Consider pivot options
2. Evaluate traditional business model
3. Study successful platforms in space
4. Major redesign if proceeding

## Best Practices

### Before Assessment
- Have clear platform concept
- Identify both/all sides
- Understand target users
- Research competitors

### During Assessment
- Be honest about weaknesses
- Don't inflate scores
- Consider worst-case scenarios
- Think 10x scale implications

### After Assessment
- Share report with advisors
- Address weaknesses systematically
- Re-assess after major changes
- Track scores over time

## Common Pitfalls

**Platform Envy**: Not every business should be a platform. Score <60% suggests traditional model may be better.

**Core Lock-in**: Platform cores are sticky. Design carefully before launch.

**Subsidy Trap**: Sustainable unit economics essential. Don't rely on endless subsidies.

**Feature Creep**: Focus on core interaction, not features.

## Quick Reference Card

```
MUST HAVE:
✓ Clear sides definition
✓ Identified value unit  
✓ Network effects potential
✓ Chicken-egg solution
✓ Differentiation

WARNING SIGNS:
✗ 3+ sides at launch
✗ No stand-alone value
✗ Pure subsidy-based growth
✗ Commodity offering
✗ No control mechanisms

VALIDATION METHODS:
• Paper prototype test
• Wizard of Oz test
• Cohort analysis
• Unit economics model
• Competitive analysis
```
