---
name: offer-decode
description: Decode a tech job offer or CTC breakup into what the candidate actually takes home. It separates fixed, variable, one-time and deferred pay (ESOPs/RSUs), estimates monthly in-hand salary with stated assumptions, flags red flags (bonds, clawbacks, inflated CTC, notice period, non-competes), compares multiple offers side by side, and drafts a negotiation reply. Use when the user has an offer letter, a CTC breakup, wants to compare offers, asks "what is my in-hand salary", or wants to negotiate an offer.
---

# Offer decode

"₹18 LPA" can mean ₹1.05 lakh a month in hand, or ₹80,000 with a ₹2 lakh bond. Candidates routinely pick the worse offer because of how the CTC was written. Decode it properly.

## 0. Inputs

1. Call the Skill tool with "cracked-profile" (country; current location and city matter for rent and professional tax).
2. Get the offer(s): offer letter PDF, CTC annexure, a screenshot, or typed numbers. Read every page. Bonds, clawbacks and notice periods hide in annexures and the fine print.
3. If you're comparing offers, collect all of them before analysing.

## 1. Break it down

For each offer, build this table (annual and monthly):

| Component | Annual | Monthly | Category |
|---|---|---|---|

Categories:
- **Fixed cash**: basic, HRA, special allowance, other fixed allowances
- **Variable**: performance bonus. Note the *target* % and whether it's guaranteed. Ask the user for the company's historical payout. If it's unknown, show 0%, 70% and 100% payout side by side and label it an assumption (the calculator does this).
- **One-time**: joining/sign-on bonus, relocation. Check for clawbacks ("repayable if you leave within 12 months").
- **Deferred / equity**: ESOPs, RSUs. Note the vesting schedule, cliff, strike price (ESOPs), and liquidity (private company ESOPs may never be sellable).
- **Benefits counted in CTC**: employer PF, gratuity, insurance premiums, meal cards, NPS. These are real money but **not in-hand cash**.

**Year-1 cash** = fixed + expected variable + one-time.
**Recurring cash** = fixed + expected variable.
Show both. The headline CTC is neither.

## 2. Estimate in-hand

For India, use [INDIA-CTC.md](INDIA-CTC.md) and run the calculator rather than doing the maths yourself: `python3 scripts/ctc.py --fixed <annual fixed> --variable <annual bonus> --regime both [--rent <annual rent> --metro] [--pt <professional tax>] [--pf capped|full] [--wage-rule basic|labour-code]`. Paste its table. If you change an assumption, rerun it. For other countries, estimate with the main tax and social-security components (e.g. US: federal + state + FICA, 401k if stated), and say which ones you included.

Rules:
- **Tax rules change every year.** If you have a web tool, verify the current slabs for the relevant financial year before computing. If not, use the reference values, name the year they're from, and say so clearly.
- Show the calculation step by step, and state every assumption (tax regime, PF on full basic vs capped, professional-tax state, rent).
- Run arithmetic with the calculator or the shell, never in your head, and show the result.
- End with a **monthly in-hand estimate as a range** (e.g. ₹1.02–1.06 L), not false precision.

## 3. Red flags and fine print

Check and report each one:
- **Service bond / training bond**: amount, duration, enforceability concerns. State the facts and suggest they ask HR to clarify. You're not a lawyer.
- **Clawbacks** on joining bonus or relocation.
- **Variable %** that's high relative to fixed, or with vague payout conditions.
- **Notice period** (60–90 days hurts the next switch), **probation** terms, **non-compete / non-solicit**.
- **Inflated CTC**: insurance, gratuity, or one-time items padding the headline.
- **Joining date and location** flexibility; **relocation** support; **work mode**.
- ESOPs at early startups: high strike, short exercise window, or a 4-year vest with a 1-year cliff. Treat them as a lottery ticket, not salary.

## 4. Compare (if more than one offer)

Side-by-side table: recurring cash, year-1 cash, monthly in-hand, equity (with a "realistic value" note), bond, notice period, role/team, learning, location and cost of living (adjust in-hand for rent differences between cities), and brand/growth. Then a recommendation **with reasoning**, and the one factor that would flip it.

## 5. Negotiate (if they want to)

Draft a short, polite email or message: appreciation → a specific ask (a fixed-pay increase, joining bonus, waived bond, relocation, joining date) → justification (competing offer, market data the user provides, or their unique fit) → flexibility. Note that campus placement offers are usually non-negotiable; off-campus and lateral offers usually are.

## 6. Output

Save the analysis to `$CRACKED_DIR/offers/<company>-<date>.md`. No scorecard for this skill.

End with: "Estimates for planning only, not tax or legal advice. Confirm the final numbers with HR."

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
