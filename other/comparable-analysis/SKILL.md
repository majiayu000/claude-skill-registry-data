---
name: comparable-analysis
description: Builds a trading comparables set with spread multiples and a benchmark when you need a market read from public peers.
---

# Comparable Analysis Agent

## When to use
Use this when you need a market read from trading peers rather than an intrinsic estimate. Typical triggers: sizing where the market prices a business today, sanity-checking a DCF, or setting an IPO or offer range. Reach for it when the question is what comparable public companies are currently worth on a multiples basis.

## What it does
It produces a trading comps set: a screened peer group with EV/EBITDA, EV/EBIT, and P/E spread on a like-for-like basis, and a benchmark (median and mean) applied to the subject to imply a value range.

## Method
1. Define the subject and screen peers. Build a tight, defensible set.
   - Fix the subject's sector, size, growth, and margin profile, then screen for public companies with similar business models; a short, clean set beats a long, loose one.

2. Pull market and financial data. Gather what each multiple needs.
   - For each peer collect share price, diluted shares, and net debt for equity value and enterprise value, plus LTM and forward EBITDA, EBIT, and EPS.

3. Clean for comparability. Make the metrics like-for-like.
   - Strip non-recurring items (restructuring, litigation, one-off gains), treat stock-based compensation and leases consistently across the set, and calendarize to a common fiscal year end.

4. Compute enterprise value correctly. Keep numerator and denominator consistent.
   - EV equals equity value plus net debt plus minority interest and preferred, less non-operating assets; EV pairs with EBITDA and EBIT, equity value pairs with EPS.

5. Spread the multiples. Lay them out so outliers show.
   - Calculate EV/EBITDA, EV/EBIT, and P/E for each peer on LTM and forward bases, arranged for easy comparison.
   - Pitfall: a peer mid-acquisition or with a distorted single-year metric will skew the set; annotate and consider excluding it.

6. Establish the benchmark. Summarize the set robustly.
   - Take the median and mean of each multiple and note the interquartile range; prefer the median where the set is small or skewed.
   - Good practice: reconcile the LTM and forward reads, since a wide gap usually signals a growth or margin inflection worth explaining.

7. Apply to the subject. Convert multiples into value.
   - Multiply the subject's metric by the low, median, and high peer multiples for an implied range, bridging EV multiples back to equity value where needed.
   - Use the subject's own cleaned metric on the same basis as the peers, so the read is truly like-for-like.

8. Interpret. Place the subject within the range.
   - Explain where it should sit given its growth and margins, and flag any peer to down-weight and why.
   - A faster-growing, higher-margin subject earns a premium to the median; a lagging one deserves a discount, and the interpretation should say which and by how much.

## Inputs
- Subject LTM and forward EBITDA, EBIT, and EPS
- Subject net debt and diluted shares for the bridge
- A candidate peer list, or permission to propose one
- Known non-recurring items to normalize out
- Whether an LTM, forward, or blended read is wanted
- The lease and stock-based-compensation treatment to standardize on
- The common fiscal year end to calendarize the peers onto

## Output format
- A peer-set section describing each company and its computed EV/EBITDA, EV/EBIT, and P/E
- A benchmark section stating the median, mean, and interquartile range per multiple
- The implied value range from applying the low, median, and high multiples to the subject
- A short interpretation of where the subject belongs and which peers were down-weighted
- Describe the comps set in prose, never as a markdown table

## Example
For Northwind Logistics (fictional, illustrative): five peers spread EV/EBITDA of 7.2x to 9.8x with a median of 8.4x, an EV/EBIT median of 11.5x, and a P/E median of 15x. One peer at 9.8x is down-weighted for a pending acquisition that inflates its multiple. Applied to the subject's LTM EBITDA of 120, the median 8.4x implies EV of about 1,010, with a low-to-high band of 865 to 1,175. On a forward basis the median compresses to 7.9x as consensus EBITDA rises. Given faster growth and higher margins than the median peer, the subject is placed just above the median at roughly 8.7x, or about 1,045.
