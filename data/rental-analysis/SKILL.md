---
name: rental-analysis
description: Comprehensive financial analysis for rental property owners considering renting vs. selling their home. Calculates cash flow, key investment metrics (cap rate, IRR, NPV), break-even analysis, and compares rental income scenarios against selling. Generates detailed reports with plain-language explanations suitable for non-experts. Use when homeowners need data-driven insights to decide between renting out their property or selling it.
---

# Rental Property Analysis

Perform comprehensive financial analysis for homeowners deciding whether to rent out their property or sell it. This skill generates detailed reports with financial metrics, cash flow analysis, and rent vs. sell comparisons.

## When to Use This Skill

Use this skill when:
- A homeowner is considering renting out their property
- Someone needs to compare the financial outcomes of renting vs. selling
- Detailed financial metrics are needed (cap rate, IRR, NPV, cash-on-cash return)
- A comprehensive analysis with plain-language explanations is required
- Multiple scenarios need to be evaluated

## How to Use This Skill

### Step 1: Prepare Property Information

Create a YAML configuration file with property details using the template in `assets/property_template.yaml`. The template includes:

**Required information:**
- Property address
- Purchase details (price, year, mortgage balance, interest rate)
- Annual costs (property tax, insurance, HOA)
- Operational assumptions (maintenance %, management fees, vacancy rate)

**Optional information:**
- Current home value estimate (defaults to purchase price)
- Estimated monthly rent (can be looked up via web comps)
- Financial assumptions (appreciation rate, rent growth, hold period)
- Selling scenario parameters (sale costs, tax bracket)

### Step 2: Run the Analysis

Execute the analysis script with the configuration file:

```bash
uv run scripts/analyze_rental.py <config_file.yaml>
```

**Optional: Save report to file:**
```bash
uv run scripts/analyze_rental.py <config_file.yaml> -o report.md
```

### Step 3: Review the Generated Report

The script generates a comprehensive markdown report including:

1. **Property Overview** - Summary of property details and estimates
2. **Monthly Cash Flow Analysis** - Detailed breakdown of income and all expenses
3. **Key Financial Metrics** - Cap rate, cash-on-cash return, IRR, NPV with explanations
4. **Break-Even Analysis** - Time required to recover initial investment
5. **Rent vs. Sell Comparison** - Side-by-side financial comparison with recommendation
6. **Assumptions** - All assumptions used in calculations

Each metric includes plain-language explanations suitable for non-experts.

## Understanding the Financial Metrics

The analysis calculates several key metrics. For detailed explanations of each metric, refer to `references/financial_metrics.md`. Key metrics include:

**Cash Flow Metrics:**
- Net monthly cash flow (income minus all expenses)
- Net Operating Income (NOI)

**Return Metrics:**
- Cap Rate: Property return rate independent of financing
- Cash-on-Cash Return: Return on invested cash (down payment + closing costs)
- Internal Rate of Return (IRR): Average annual return over hold period
- Net Present Value (NPV): Present value of all future cash flows

**Time Metrics:**
- Break-even point: Time until investment is recovered

**Comparison Metrics:**
- Total return from renting vs. net proceeds from selling

## Rental Comps Lookup

When `include_web_comps: true` and `estimated_rent: null`, the script will attempt to fetch rental comparables from web sources. This feature helps estimate market rent for the property.

**Note:** Web scraping requires appropriate API integration or tools like Firecrawl. The script includes placeholder functionality that can be extended with actual web scraping implementation.

**Suggested data sources:**
- Zillow Rental Manager
- Rentometer
- Redfin
- Rent.com
- Local MLS rental data

## Sources & Citations

Every analysis report includes comprehensive source documentation:

### Automatic Citation Tracking

The script automatically tracks and documents:
- **User-provided data**: Property details from configuration file
- **Calculation methods**: Industry-standard real estate financial formulas
- **Market assumptions**: Basis for appreciation rates, vacancy rates, etc.
- **Web-fetched data**: When rental comps or market data are retrieved

### Citations in Reports

Each report includes two citation sections:

1. **Sources & Citations** (if web data was fetched):
   - Lists all external sources with URLs
   - Includes notes about what data was obtained
   - Numbered for easy reference

2. **Data Sources**:
   - Documents where all data originated
   - Lists recommended verification sources
   - Helps users fact-check and follow up

### Example Citation Output

When web data is fetched, citations appear like this:

```markdown
## 📚 Sources & Citations

Data sources used in this analysis:

1. **Zillow Rental Manager** - [https://zillow.com/...]
   - Market rental estimates for comparable properties
2. **Rentometer** - [https://rentometer.com/...]
   - Rental price analysis based on local market data
```

### Extending Citation Tracking

To add citations when implementing web scraping:

```python
analyzer.add_citation(
    source="Source Name",
    url="https://example.com",
    note="Description of what data was obtained"
)
```

This ensures transparency and allows users to verify and explore data sources in detail.

## Example Workflow

```yaml
# property_config.yaml
address: "1234 Example St, Olympia, WA 98501"
purchase_price: 450000
purchase_year: 2021
current_mortgage_balance: 370000
interest_rate: 3.25
loan_term_years: 30
monthly_principal_interest: null
property_tax_per_year: 4100
home_insurance_per_year: 1500
hoa_per_month: 0
maintenance_pct: 1
management_fee_pct: 8
vacancy_rate_pct: 5
desired_start_date: "2025-03-01"
estimated_rent: 2800
include_web_comps: false
current_home_value: 500000
down_payment_original: 20
closing_costs_estimate: 8000
expected_appreciation_rate_pct: 3
expected_rent_growth_pct: 2
compare_against_selling: true
sale_cost_pct: 6
personal_tax_bracket_pct: 24
hold_period_years: 5
```

```bash
uv run scripts/analyze_rental.py property_config.yaml -o analysis_report.md
```

## Helping Users Understand Results

When presenting analysis results:

1. **Start with the bottom line**: Is cash flow positive or negative? What's the recommendation?

2. **Explain the key metrics** in context:
   - Cap rate: Compare to typical market rates (4-10%)
   - Cash-on-cash return: Compare to alternative investments
   - IRR: Factor in time value and appreciation
   - NPV: Whether the investment meets required return threshold

3. **Discuss risk factors**:
   - Vacancy risk
   - Maintenance surprises
   - Market changes
   - Interest rate changes (if ARM)

4. **Consider non-financial factors**:
   - Landlord responsibilities and time commitment
   - Desire to move back later
   - Emotional attachment to property
   - Alternative investment opportunities

5. **Recommend next steps**:
   - Consult with CPA for tax implications
   - Talk to real estate agent about market conditions
   - Review property management options if applicable
   - Consider financing alternatives if needed

## Limitations and Disclaimers

**Important notes:**
- Analysis is based on assumptions and estimates
- Tax calculations are simplified (consult CPA for actual tax liability)
- Doesn't account for all possible scenarios (major repairs, legal issues, etc.)
- Past performance doesn't guarantee future results
- Local market conditions can vary significantly

**Always recommend:**
- Consulting with qualified CPA for tax advice
- Working with real estate attorney for legal questions
- Talking to local real estate professionals for market insights
- Maintaining adequate cash reserves for unexpected expenses

## Technical Details

**Script dependencies:**
- pyyaml: Parse YAML configuration files
- numpy: Numerical calculations
- numpy-financial: Financial formulas (IRR, NPV)
- requests: Web requests for rental comps (future feature)

**Script capabilities:**
- Mortgage payment calculations
- Cash flow projections with growth rates
- Financial metric calculations
- Break-even analysis with appreciation
- Rent vs. sell comparison with tax considerations
- Markdown report generation

## Customization

The analysis can be customized by:
- Adjusting assumptions in the YAML file
- Modifying hold period length
- Changing appreciation/growth rates
- Including/excluding selling comparison
- Adding custom expense categories (edit script)

## Troubleshooting

**Missing estimated_rent and web comps disabled:**
- Either provide `estimated_rent` value or enable `include_web_comps: true`

**Unexpected results:**
- Verify all input values are correct
- Check that percentages are entered correctly (use 3 for 3%, not 0.03)
- Ensure dates are in YYYY-MM-DD format

**Script errors:**
- Ensure all required fields are provided in YAML
- Check YAML syntax is valid
- Verify uv and dependencies are installed
