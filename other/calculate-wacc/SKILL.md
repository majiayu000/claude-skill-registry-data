---
name: calculate-wacc
description: Use when calculating the Weighted Average Cost of Capital for a company to use as the discount rate in valuation or capital budgeting decisions
source: Modigliani & Miller "The Cost of Capital, Corporation Finance" (1958); Damodaran "Investment Valuation" (2012); CFA Institute Level II curriculum
tags: [corporate-finance, wacc, valuation, cost-of-capital]
verified: true
---

# Calculate WACC

Calculate the Weighted Average Cost of Capital (WACC) to establish the appropriate discount rate for discounted cash flow valuation or capital budgeting decisions.

## Why This Is Best Practice

**Adopted by:** CFA Institute (200,000+ members) teaches WACC as the standard discount rate for equity valuation; investment banks (Goldman Sachs, JPMorgan, Morgan Stanley) use WACC in all DCF valuation models; corporate finance teams at public companies use WACC for capital allocation decisions.
**Impact:** Using an incorrect discount rate causes valuation errors of 20–50% — a WACC that is 1% too low overstates value by 10–25% in a typical 5-year DCF; Damodaran's research shows WACC is the most error-prone step in DCF analysis.
**Why best:** WACC is the theoretically correct discount rate for the firm as a whole because it reflects the blended required return of all capital providers weighted by their contribution to the capital structure, incorporating the tax shield on debt.

Sources: Modigliani & Miller "The Cost of Capital, Corporation Finance and the Theory of Investment" (1958, 1963); Damodaran "Investment Valuation" 3rd ed. (2012); CFA Level II — Corporate Issuers curriculum.

## Steps

1. **Determine the target capital structure** — use the market-value weights of debt and equity, not book values. For public companies: market cap (shares × price) for equity; book value of debt adjusted to market value. For private companies: use industry median capital structures or peer comparables.

2. **Calculate the Cost of Equity (Ke) using CAPM** — Ke = Risk-Free Rate + Beta × Equity Risk Premium (ERP). Risk-Free Rate: use the current 10-year (or 30-year for long-duration assets) government bond yield. ERP: use Damodaran's annually updated equity risk premium (~4–5.5% for US). Beta: use the company's 5-year monthly regression beta against a market index; unlever/re-lever for private companies using peers.

3. **Adjust beta for leverage (Hamada equation)** — Unlevered Beta (βu) = Levered Beta (βL) ÷ (1 + (1 − Tax Rate) × (D/E)). To re-lever to target capital structure: βL = βu × (1 + (1 − Tax Rate) × (D/E)). This step is required when using peer betas for private company or restructuring analysis.

4. **Add size and specific risk premiums if applicable** — for small-cap or private companies, add a size premium (Duff & Phelps / Kroll CRSP size premium: 0.5–5% for micro-cap), a company-specific risk premium (CSRP: 0–5% for concentration, key-person dependence, customer concentration risk).

5. **Calculate the Pre-Tax Cost of Debt (Kd)** — use the yield to maturity (YTM) on the company's existing publicly traded bonds. For private companies without rated debt, use: risk-free rate + appropriate credit spread based on synthetic credit rating (estimate from interest coverage ratio).

6. **Calculate the After-Tax Cost of Debt** — After-Tax Kd = Pre-Tax Kd × (1 − Marginal Tax Rate). Use the marginal (not effective) corporate tax rate. This reflects the tax deductibility of interest (the debt tax shield). For jurisdictions with no interest deductibility, use pre-tax Kd.

7. **Calculate WACC** — WACC = (E/V × Ke) + (D/V × Kd × (1 − Tax Rate)), where V = E + D (total firm value), E = market value of equity, D = market value of debt. Example: 60% equity × 10% Ke + 40% debt × 5% Kd × (1 − 25% tax) = 6.0% + 1.5% = 7.5% WACC.

8. **Adjust for country risk if applicable** — for companies with significant operations in emerging markets, add a Country Risk Premium (CRP) per Damodaran: CRP = (Sovereign Spread) × (Equity Market Volatility / Bond Market Volatility). Apply CRP to the cost of equity for each geography proportionally.

9. **Triangulate and sanity check** — compare your WACC to: (a) industry median WACCs from Damodaran's annual WACC database; (b) implied WACCs from comparable company valuations; (c) the company's stated hurdle rate. A WACC that is 200bp above or below the industry median requires explanation.

10. **Document all assumptions** — WACC is highly sensitive to inputs; document every assumption with its source. A 1% change in ERP changes WACC by ~60bp for an all-equity firm. Provide a sensitivity table showing WACC at high/mid/low values for key inputs.

## Rules

- Always use market-value weights, not book-value weights — book equity is an accounting artifact, not a measure of what equity investors require.
- Use the marginal tax rate, not the effective tax rate — WACC captures the prospective tax shield on new debt, not historical taxes paid.
- Never use WACC to discount projects with materially different risk profiles than the company — use project-specific discount rates (APV method) instead.
- WACC is for total firm valuation (DCF to the firm); for equity valuation (DDM), use the cost of equity directly.

## Common Mistakes

- **Using book value capital structure weights** — book equity reflects historical accounting costs, not current market value; this is the most common WACC error.
- **Using the wrong risk-free rate** — using a short-term T-bill rate (3-month) instead of a long-term government bond yield for long-duration assets understates WACC.
- **Circular reference in WACC calculation** — market value of equity depends on WACC, which depends on weights that depend on market value of equity; resolve using iterative calculation in Excel or fix the capital structure.
- **Ignoring hybrid securities** — convertible debt, preferred stock, and warrants have different costs; treat each based on its economic substance (debt or equity).

## When NOT to Use

- When valuing a single project that differs significantly from the company's overall risk profile (use APV or project-specific rate).
- When the company has no debt or minimal debt (simply use the cost of equity; WACC = Ke when D/V ≈ 0).
- When the company is in financial distress (WACC assumes the firm is a going concern; distressed firms require different valuation approaches).

## Disclaimer

This skill is for educational and analytical purposes only and does not constitute financial advice. Consult a qualified financial advisor before making investment or capital budgeting decisions.