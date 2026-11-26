---
name: kdp-niche-research
description: Validate Amazon KDP niches for profitability and timing before writing — BSR benchmark scoring, demand thresholds, competition signals, seasonal/hot/evergreen classification, and competitor-catalog mining. Use when the user asks whether a book idea/niche/keyword is worth publishing, when to publish it, or how to find profitable niches and series potential.
triggers:
  - kdp niche
  - niche research
  - niche validation
  - book timing
  - bsr analysis
  - profitable niche
  - اختيار نيتش
personas:
  - MARKETING
  - DOC
  - FREELANCE
tech_stack: []
derived_from: original — methodology facts synthesized from public KDP practitioner frameworks (see docs/studies/study-ecosystem-scan-2026-11-25.md)
---

# KDP Niche Research

[OBJ] Decide with evidence whether a book niche is worth writing, and when to publish it. Never write the book first and validate later.

## Core doctrine

A niche is a keyword readers already search for and already buy in. You are not inventing demand — you are measuring it. Every profitable indie catalog title is a keyword someone else already validated with real sales; mining those catalogs is the highest-ROI research method available.

## Validation workflow (in order)

### 1. Demand check
- Estimate Amazon search volume for the seed keyword and 5–10 close variations (Amazon autocomplete, keyword tools, or DataForSEO-style APIs).
- **Demand floor: ~200+ monthly Amazon searches** for the seed phrase. Below that the niche cannot carry a book alone.
- Related keywords are not noise — they are your **series map**. 5–10 related viable keywords = a series, not a book.

### 2. BSR competition scoring
Pull the top 20 search results for the keyword and score against these benchmarks:

| Signal | Target | Meaning |
|--------|--------|---------|
| Top-20 books under 5,000 BSR | at most 5 | more = entrenched bestsellers, too competitive |
| Top-20 books under 30,000 BSR | most of the page | sweet spot — demand exists, indie-winnable |
| Top-10 books under 100,000 BSR | at least 7 | minimum viable demand floor |
| Self-published titles on page 1 | 2–3 minimum | proves an indie can rank here |
| Amazon result count for the keyword | under ~3,000 | lower = easier to rank |

Self-published detection: publisher field reads "Independently published", price in the $2.99–4.99 band, keyword-stuffed title, template-looking cover.

### 3. Beatability signals
Weak competition is visible: bad covers, keyword-less titles, few reviews, no series, abandoned author pages. Two or more top-10 books with these signals = the niche is beatable with better execution.

### 4. Platform split
A keyword dead on Kindle may be alive in print or audio. Check each format separately: Kindle is the most competitive, paperbacks reward reference/practical books, audiobooks are under-served in most niches (few results = opportunity).

## Timing classification — when to publish

| Class | Pattern | Strategy |
|-------|---------|----------|
| Hot/trending | demand spike, short window | publish fast or skip; do not build series on it |
| Evergreen | steady year-round demand | compounding asset; series-worthy |
| Seasonal | predictable annual spike (gardening in spring, planners in December, exam prep cycles) | publish 4–6 weeks BEFORE the spike so ranking/reviews are in place when demand lands |

Use Google Trends + Amazon autocomplete drift to classify. A healthy portfolio mixes evergreen base-load with seasonal spikes.

**New-release window:** Amazon's new-release visibility roughly covers the first 30 days (up to 90 for strong performers). Launch timing matters more than perfection — a seasonal book that misses its window waits a year.

## Verdict format

Always end with a structured verdict: demand score, competition score, beatability signals, platform split, timing class, series potential — then `VIABLE / BORDERLINE / TOO COMPETITIVE / DEAD` with the numbers that forced it. No vibes.

## Rules

1. [REQ] Validate before writing; never retrofit validation onto a finished manuscript.
2. [REQ] Mine 2–3 successful indie author catalogs in adjacent niches before concluding research — their titles are pre-validated keywords.
3. [REQ] Score all three formats (ebook/paperback/audio) before killing a niche.
4. [REQ] Seasonal decision = publish date minus 4–6 weeks minimum.
5. [PROHIBIT] Declaring a niche viable without BSR data and demand numbers — "I think people want this" is not evidence.
