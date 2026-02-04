---
name: insurance-plan-analyzer
description: Analyzes and compares health insurance plans (individual vs group), calculates costs, verifies networks, and generates formatted comparison reports for decision-making
version: 1.0.0
author: Paragroup LLC
---

# Insurance Plan Analyzer Skill

## Purpose
This skill automates the process of comparing health insurance options, calculating total costs, analyzing coverage differences, and generating comprehensive decision reports for employees and small businesses.

## When to Use This Skill
Invoke this skill when the user:
- Needs to compare multiple insurance plans
- Has quotes from different insurance agents or carriers
- Wants to analyze individual marketplace vs. small group insurance
- Needs cost projections and savings calculations
- Requires formatted comparison reports
- Is making employee benefits decisions

## Key Capabilities

### 1. Data Extraction
- Extract plan details from emails, PDFs, or text
- Identify: premiums, deductibles, OOP maximums, copays, coinsurance
- Recognize carriers (Horizon, UHC, AmeriHealth, Oscar, Aetna, etc.)
- Extract employer/employee contribution splits

### 2. Cost Analysis
- Calculate total annual costs
- Compare employer contribution requirements
- Project employee out-of-pocket costs
- Compute tax savings (pre-tax vs after-tax)
- Calculate ICHRA reimbursement scenarios
- Identify subsidy eligibility (ACA affordability rules)

### 3. Coverage Comparison
- Compare deductibles, OOP maximums, copays across plans
- Identify coverage gaps or advantages
- Analyze plan types (PPO, EPO, HMO, HDH)
- Evaluate network coverage

### 4. Special Considerations
- H-1B visa holder eligibility for subsidies (affordability rule: >9.12% of income)
- ICHRA (Individual Coverage HRA) setup and benefits
- Doctor network verification requirements
- Small group ACA compliance (owner cannot be only insured)
- Pre-tax vs after-tax payment structures

### 5. Report Generation
- Create formatted text reports for Notepad++ viewing
- Generate comparison tables with proper column alignment
- Provide executive summaries with clear recommendations
- Include implementation timelines and next steps
- Format for easy sharing with employees and stakeholders

## Input Format

### Required Information:
```
EMPLOYEE DATA:
- Name, DOB, visa status (if applicable)
- Spouse and dependent details
- Annual household income
- Current insurance (if any)
- Location (ZIP code)

QUOTE DATA:
- Carrier name
- Plan name and type (PPO/EPO/HMO)
- Monthly premium
- Deductibles (individual/family)
- Out-of-pocket maximums
- Copays (PCP, specialist, ER, etc.)
- Coinsurance split
- Employer/employee contribution split

REQUIREMENTS:
- Doctor network requirements
- Coverage effective date
- Budget constraints
- Special considerations (H-1B, ICHRA, etc.)
```

## Output Format

### Standard Comparison Report Includes:
1. Executive Summary with clear recommendation
2. Cost Comparison Table (all plans side-by-side)
3. Annual Savings Analysis
4. Coverage Details Comparison
5. Special Considerations (visa, tax, network)
6. Pros/Cons Analysis for each option
7. Implementation Timeline
8. Next Steps and Contacts

### Formatting Standards:
- Fixed-width text formatting for Notepad++
- Tables with proper column alignment using spaces
- Section headers with clear visual separators (=== lines)
- Numbered lists for action items
- ✓/✗ symbols for quick visual scanning
- ⭐ symbols to highlight best options

## Calculation Methods

### ACA Affordability Rule:
```
Threshold = Household Income × 9.12%
If Employee Share > Threshold → Coverage is "Unaffordable"
If Unaffordable + Employer Sponsors H-1B → May qualify for subsidies
```

### Total Annual Cost:
```
Annual Cost = (Monthly Premium × 12) + (Employer Contribution × 12)
```

### Tax Savings Calculation:
```
Assumed Tax Rate = 30% (federal + state + FICA)
Tax Savings = Premium × Tax Rate
Net Cost = Premium - Tax Savings
```

### ICHRA Savings:
```
Employee Premium = Full Premium
Company Reimburses = X% of Premium (tax-free)
Employee Net Cost = Premium - Reimbursement
Company Cost = Reimbursement (tax-deductible)
```

## Example Usage

### Example 1: Basic Comparison
```
User: "I have 3 insurance quotes. Can you compare them?"
Skill: Extracts data, creates comparison table, calculates costs, recommends best option
```

### Example 2: H-1B Subsidy Analysis
```
User: "My H-1B employee makes $132k. Can he get marketplace subsidies?"
Skill: Applies 9.12% rule, checks if employer coverage unaffordable, determines eligibility
```

### Example 3: Individual vs Group Decision
```
User: "Should we do group insurance or individual marketplace?"
Skill: Compares costs, analyzes tax benefits, considers ICHRA, provides recommendation
```

## Best Practices

### When Analyzing Plans:
1. Always verify doctor network acceptance
2. Consider visa status implications for subsidies
3. Calculate both monthly and annual costs
4. Factor in tax benefits (pre-tax payroll vs after-tax)
5. Include ICHRA as an option for individual insurance
6. Check ACA compliance for small group plans

### When Making Recommendations:
1. Prioritize total cost savings
2. Consider employee experience and ease
3. Evaluate tax efficiency
4. Account for special circumstances (visa, doctor networks)
5. Provide multiple options (best, good, acceptable)
6. Include implementation complexity in decision

### Report Formatting:
1. Use fixed-width formatting for tables
2. Align columns properly with spaces (not tabs)
3. Keep lines under 80 characters for Notepad++ viewing
4. Use clear section separators
5. Bold recommendations with ⭐ symbols
6. Include contact information for next steps

## Common Scenarios

### Scenario 1: Small Business (2-10 employees)
- Compare individual + ICHRA vs small group
- Calculate minimum employer contribution (10% in NJ)
- Analyze which is more cost-effective
- Consider administrative burden

### Scenario 2: H-1B Employee Coverage
- Check subsidy eligibility (affordability rule)
- Verify visa status doesn't affect coverage
- Calculate with and without subsidies
- Include CHIP eligibility for US citizen dependents

### Scenario 3: Doctor Network Critical
- Filter plans by specific doctor acceptance
- Verify network status with carriers
- Provide alternatives if doctor not in preferred network
- Suggest doctor flexibility if significant savings available

### Scenario 4: Tight Budget Constraints
- Focus on lowest total cost options
- Explore Bronze vs Silver vs Gold tiers
- Calculate affordability impact on subsidies
- Consider higher deductible plans with HSA

## Key Takeaways for Users

### Cost Savings Opportunities:
- Individual marketplace often cheaper than small group (especially for small companies)
- H-1B employees may qualify for subsidies if employer coverage "unaffordable"
- ICHRA allows tax-free reimbursement of individual premiums
- Pre-tax payroll deductions save ~30% in taxes

### Compliance Requirements:
- Small group minimum employer contribution: 10% in NJ
- ACA rule: Owner cannot be only person covered in small group
- H-1B subsidy eligibility: Employer must sponsor visa + coverage must be unaffordable

### Decision Factors:
- Total cost (not just premium)
- Doctor network acceptance
- Employee tax benefits
- Administrative simplicity
- Professional benefit image

## Resources and References

### Subsidy Eligibility:
- ACA Affordability Percentage: 9.12% of household income (2025)
- H-1B Subsidy Exception: Unaffordable employer coverage allows marketplace subsidies

### NJ Small Group Requirements:
- Minimum 2 employees (1 non-owner)
- Minimum 10% employer contribution
- Cannot exclude owner if non-owner covered

### Tax Benefits:
- Group insurance: Pre-tax payroll deduction
- ICHRA: Tax-free employer reimbursement
- Both: Employer contribution is business tax-deductible

### Common Carriers:
- Horizon Blue Cross Blue Shield (NJ largest)
- UnitedHealthcare / Oxford
- AmeriHealth
- Oscar Health
- Aetna CVS Health

## Version History
- v1.0.0 (Oct 2025): Initial release with H-1B analysis, ICHRA support, NJ small group rules
