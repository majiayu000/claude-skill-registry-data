---
name: squares-in-squares-campaign
description: "Pack n = 1..1000 unit squares into the smallest square (Kaggle \"Squares in Squares\", score sum L/sqrt(n) - 1). Use when improving, certifying or submitting packings, or when choosing the next search route. Covers the official-metric gates, the solver and MIS tools, the structure of the frontier, and the routes measured dead. The competition closed on 25 Oct 2026."
---

# Plättlileger (squares-in-squares-campaign)

This is the playbook from our campaign. The campaign repository is private, so the file names below
describe its layout; rebuild the same pieces in your own tree. Keep a route journal (frontier, routes, kills) that survives
context compaction, and read it first. Take timestamps from `date`, never estimate them.

## Contract and gates (never skip)
- Metric: `src/official_metric.py` (verbatim Kaggle metric). Float SAT with a 1e-8 undecided band, then mpmath interval SAT at
  50/100/200/500 digits. Exact contacts between non-dyadic decimals are UNDECIDABLE -> rejected -> that n falls to the grid score.
  Every moved contact needs a strictly positive gap (>= ~1e-12 via `src/certify.py`, or >= 1.2e-8 via engine dilation).
- Only `src/harvest.py --base ENS --out NEW CANDS...` may write `submissions/ens*.csv`: it certifies every candidate puzzle (raw AND pandas-float64-rounded rows; stores the f64 rows) with the
  official metric (parallel, float prefilter) and keeps strict improvements.
- Before any submission: `src/gate.py submissions/ensX.csv` must print PASS (schema, raw / pandas-float64 / pandas-str round-trips agree).
- Submitting needs the user to have joined the competition (rules acceptance is theirs). 10 submissions/day; spend them only on gated, strictly better files.

## Tools
- `engine/sqpack` (C++17): exact SAT-penalty L-BFGS + basin hopping; `engine/run.py` certifies (refuses infeasible starts;
  use the binary directly for perturbed starts, then certify). Linux build: `CXX=g++ ./build.sh`. ~10k energy+grad evals/s at n=900.
- `src/mis/`: CP-SAT max-independent-set packers (axis grids + tilted lattices; band templates). Good for skeletons/lattice capacity,
  NOT for the last squares (needs continuous freedom). Use 14 workers per solve; workers=1 is useless.
- `src/addl.py` (add-L transfer: side+1, +2*floor(s)+1 squares, preserves j=n-K^2), `src/perturb.py`, `src/render.py`, `src/score_sub.py`.
- `infra/remote_polish.sh` (mass polish on a rented many-core box; ubuntu:22.04 images pulled reliably, python/cuda
  images stalled) and `infra/intake.sh` (pull all public notebook outputs and harvest).
- Second opinions: `jev-second-perspective` for lever triage, `elicit-research` for literature.

## What the frontier is (measured)
- n=k^2+j. j<=0: L=k. Above j ~ 1.2k nobody beats the grid k+1. Gap mass is at n=400..1000 (0.0997 of 0.105 vs the staff per-puzzle table).
- Classes at k>=20: (A) 45-deg Ellsworth/Goebel block, exact (a+b sqrt2)/2 sides; (B) axis block + 1-2 tilted row-bands
  (rows of m+1 at the minimal angle, (m+1)cos th + sin th = m+c), the EG/Chung-Graham L-frame; (C) multi-angle fault composites.
  Interior strips are identical everywhere; the frontier's edge is a k-independent 1-2 (up to 5-6) square gain at band ENDS and CORNERS
  (fanning angles, axis squares resting on tilted corners, odd-angle corner singles).
- The staff table (the public notebook inversion/squares-in-squares-per-puzzle-leaderboard)
  is a PARTIAL union; refresh daily before pricing routes.

## Dead routes (do not re-run)
Literature (Friedman/Ellsworth/Squares Project n<=324, Goebel/g45 families, EG/CG/WDL/Bui/McClenagan strips, Pythagorean angle menu);
single-lattice MIS for band n; random hole insertion + repair; perturbed-45-degree starts for j=3..9 (wrong family: those are 24.36/33.8-deg
diagonal bands); naive family extrapolation by t.

## What works
- Mass polish from the incumbent on a many-core box (`infra/remote_polish.sh`, 150 s x 8 threads per n): ~45% of n improve slightly;
  ~0.002 score per 140 n. Cheap, steady, gate-safe.
- Adversarial Fable review of every synthesis (it caught the partial-union error and the wrong R2 family).
