---
name: sba-loans
description: Read the SBA 7(a) and 504 loan FOIA release correctly — what each program requires (the claims a borrower makes), the field traps that silently empty a filter or fake a trend, how to join borrowers to state business-entity filings and parcel records, and how to test claims like business age, owner-occupancy, ownership and collateral stacking. Includes one measured set of screen results and the lesson that charge-off is credit loss, not fraud. Use for "who got an SBA loan", "verify this borrower", "SBA fraud screen", "owner-occupied", "charge-off rates", "just funded", or any join from SBA loans to another layer.
compatibility: >-
  Reads SBA's public FOIA CSVs; joins run locally.
metadata:
  network-hosts: "data.sba.gov"
  network-purpose: "download the 7(a)/504 FOIA release"
---

# SBA loans: what the data says and how to test it

The source is SBA's own FOIA release (data.sba.gov, dataset `7a-504-foia`): public domain, quarterly,
1-4 months behind, one CSV per program and era.

## What the programs require (the claims a borrower makes)

Each requirement is a claim. A useful test compares a claim with a record the borrower doesn't control.

- **7(a)**, up to $5M. For-profit, US, small under the NAICS size standard. Credit elsewhere
  unavailable; ~10% equity injection for a startup or acquisition (see the current SOP 50 10); a
  personal guarantee from every 20%+ owner; global DSCR around 1.15+; all available collateral above
  $50k; real estate at least 51% owner-occupied. Clean on CAIVRS, SAM exclusions and OFAC. Ownership
  and citizenship rules changed in 2025-26: read the current SOP before quoting them.
- **504**, fixed assets only: 10% down (15% for a startup or special-purpose building), **the business
  must occupy the property**, tangible net worth and average net income caps, and job or public-policy
  goals.
- **The lender's real control is the IRS transcript (Form 4506-C).** It checks the P&L. Public records
  can't see income, so record-based tests cover the *other* claims.

## Field traps (each cost a cycle)

- **`Program` is `' 7A'` with a leading space**, and `'504'`. A filter on `'7(a)'` returns nothing.
- **`BorrStreet` is the borrower's address, not the project's.** SBA publishes no site address. It can
  be a home or an accountant, so a parcel mismatch proves nothing on its own.
- **`LoanStatus`**: EXEMPT = active; `PIF` and `P I F` both mean paid in full; CHGOFF; CANCLD and
  NOT FUNDED. **Drop the last two before computing any rate.**
- **A charge-off rate by approval year is maturity, not a trend.** Recent cohorts haven't had time to
  fail. Use a fixed window (e.g. charged off within 36 months of approval) and only cohorts old enough.
- **`BusinessAge` is free-form across eras** ("Existing or more than 2 years old", "New Business or 2
  years or less", "Startup...", "Change of Ownership"). Group variants before comparing.

## Joins that work

- **Borrower -> state business-entity record (Secretary of State):** normalise both names (upper case,
  strip punctuation and legal-form suffixes such as INC, CORP, PLLC, PA, DBA and the limited-liability suffix), keep only names that resolve to **exactly one**
  entity. Expect roughly two thirds to match. Formation date = the entity's earliest filing.
  **Check the registry's terms**: some states allow counts and rates but forbid republishing rows or
  party names.
- **Parcel owner at approval:** the parcel snapshot whose as-of date is nearest the approval date.
  Loans older than your earliest snapshot have no owner-at-approval.
- **Officer link:** two entities sharing a named officer or registered party. Use it for owner <->
  borrower and for one person behind many borrowers.
- **Sale records often carry no buyer or seller names**, so related-party sales are mostly invisible.

## One measured run (a metro, ~7,800 funded loans, baseline charge-off 1.6%)

| Test | Flagged | Charge-off | Read |
|---|---|---|---|
| Borrower owns its parcel (name match or shared officer) | 884 | ~0.2% | the safest borrowers; clear them first |
| 7(a), parcel owner is a homesteaded house | 826 | 3.5% | home-based; highest loss |
| 504, parcel owner is an unrelated person or out of state | 238 | 2.5% | **the occupancy-claim screen**: 504 requires occupying the building |
| Claims 2+ years old, entity formed <2 years before approval | 491 | 0.6% | mostly a newly registered entity wrapping an older business; not a signal alone |
| ...entity formed *after* approval | 70 | 1.4% | same caveat |
| Active loan, entity now inactive at the registry | 384 | n/a | dissolved while owing, or a missed renewal |
| Parcel with loans to 2+ unrelated borrowers within 3 years | 205 parcels / 470 loans | n/a | collateral-stacking candidates |
| One officer behind 3+ borrowing entities | 53 people, 269 loans | 1 loan | multi-unit operators, or a straw-borrower ring |
| Parcel sold <=12 months before approval at >2x assessed | 10 | 0 | mostly multi-parcel deeds or redevelopment; noise |

## The lesson that matters most

**A charge-off is credit loss, not fraud.** None of the flags predicted charge-off, and that says nothing
either way about fraud. The federal SBA prosecutions found for that state over five years were all
PPP/EIDL, and their schemes match the age test and the many-entities test exactly: several entities
formed weeks before applying, many applications across many lenders, entities in relatives' names that
never filed a tax return. The one 7(a) case found was a lender quietly lending the borrower the
required equity injection: a fraud in the lender's file, invisible to public records.

So **validate any fraud screen against labelled positives** (SBA's PPP FOIA release plus US Attorney
press releases), never against 7(a) charge-offs.

## Handling

Loan records name businesses and sometimes sole proprietors. Report counts and patterns; treat any
individual flag as a lead for a professional to check, never as an accusation.
