---
name: offer-maker
description: Create, fix, and optimize offers, extract message angles for RSA composition, and generate variants. Use to build offers, craft angles, or compare competitor offers.
argument-hint: "[create|angles|competitor|diagnose|variants]"
---

# Offer Maker Skill

Creates, fixes, and optimizes offers. Extracts message angles for RSA composition. 5 execute actions.

**CRITICAL: All questions to the user MUST use the `AskUserQuestion` tool with selectable options.** Never ask questions as plain text in the terminal. For every question, provide 2-4 concrete answer options the user can select from. When asking for specific data (e.g., dream outcome, guarantee terms), generate realistic example answers as selectable options based on the vertical and context you've read. The user can always pick "Other" for custom input. Use `multiSelect: true` when multiple answers apply. Group related questions into a single AskUserQuestion call (up to 4 questions per call) to minimize back-and-forth.

| Action | Command | What it does |
|--------|---------|-------------|
| Create offer | `/offer-maker create` | Interactive 4-pillar offer design → write to business.md |
| Craft angles | `/offer-maker angles` | Extract 6 message angles → write to offer-angles.md |
| Competitor comparison | `/offer-maker competitor` | Build offer comparison matrix vs. top 3 competitors |
| Diagnose weak elements | `/offer-maker diagnose` | Read audit results → prioritized fix list |
| Generate variants | `/offer-maker variants` | Generate A/B test headline variants per angle |

## Command Format

```
/offer-maker                    # Menu of available actions
/offer-maker create             # E01: Create irresistible offer
/offer-maker angles             # E02: Craft offer angles
/offer-maker competitor         # E03: Competitor offer comparison
/offer-maker diagnose           # E04: Diagnose weak elements
/offer-maker variants           # E05: Generate angle variants
```

**Examples:**
- `/offer-maker create` — Design or redesign the offer from scratch
- `/offer-maker angles` — Extract angles for RSA composition (most common)
- `/offer-maker angles --campaign "Non-Brand Search"` — Target specific traffic
- `/offer-maker angles --refresh` — Re-extract even if angles exist
- `/offer-maker competitor` — Compare your offer against competitors
- `/offer-maker diagnose` — Get specific fixes for audit failures
- `/offer-maker variants` — Generate headline variants for testing

---

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `context/business.md` | Yes (all actions) | Vertical, offer, pricing |
| `context/brand.md` | Yes (E01, E02) | Brand context for pre-population |
| `context/offer-angles.md` | For E05 | Existing angles (variants need something to vary) |
| `context/competitor-ads/*.csv` | For E03 | Competitor ad copy |
| `context/analysis/offer-audit.md` | For E04 | Audit results to diagnose |
| `context/google-ads/data/search-terms.csv` | Optional (E02) | Customer language for phrases |

---

## Process

---

### Phase 0: Route & Prerequisites

1. **Parse subcommand:**
   - `create` → E01 (read `reference/execute-offer-creation.md`)
   - `angles` → E02 (read `reference/execute-offer-angles.md`)
   - `competitor` → E03 (read `reference/execute-competitor-comparison.md`)
   - `diagnose` → E04 (read `reference/execute-diagnose-weak.md`)
   - `variants` → E05 (read `reference/execute-angle-variants.md`)
   - No subcommand → present menu with AskUserQuestion

2. **Load business.md** — extract vertical. If missing, STOP: tell user to run `/business-context-gatherer` first.

3. **Check prerequisites per action:**

| Action | Prerequisites |
|--------|--------------|
| E01 (create) | business.md + brand.md |
| E02 (angles) | business.md + brand.md. Offer should be solid (suggest E01 if no offer section in business.md) |
| E03 (competitor) | `context/competitor-ads/*.csv` (suggest `/competitor-scraper [domain]` if missing) |
| E04 (diagnose) | `context/analysis/offer-audit.md` (suggest `/offer-audit` if missing) |
| E05 (variants) | `context/offer-angles.md` (suggest E02 if missing) |

---

### Phase 0.5: Peer Context Pull (Mode 2 — Enrichment, No Gate)

**Applies to all execute actions (E01–E05). Read-only. Never blocks generation. Biases output.**

This phase pulls fresh peer audit findings to enrich the offer-generation step. Findings change *what* gets generated (pricing tier, urgency intensity, differentiation angle, phrasing), not *whether* it gets generated. There is no score gate, no hard-block, and no abort. Dirty M-layer (tracking) and B-layer (strategy) audits surface as informational notes only.

**Freshness rule:** the date in the report's header is canonical. If a peer report header date contradicts the file mtime, surface the contradiction to the user — never auto-pick.

#### 0.5.1 — Walk the 10-peer freshness table

For each peer report file below, check existence + freshness against today's date (`2026-05-02` at the time of writing — always use the current date at run time). Compare report header date first; fall back to file mtime if the header lacks a date. A report is **fresh** if it falls inside the window; **stale** if outside; **missing** if the file does not exist.

| Peer skill | Report file | Fresh window | Highest-leverage signal for offers |
|---|---|---|---|
| `/quality-score-auditor` | `context/analysis/quality-score-audit.md` | ≤ 7 days | LPE / AR alignment |
| `/search-term-auditor` | `context/analysis/search-term-audit.md` | ≤ 7 days | Top converting n-grams for offer phrasing |
| `/keyword-auditor` | `context/analysis/keyword-audit.md` | ≤ 7 days | Theme alignment |
| `/budget-auditor` | `context/analysis/budget-audit.md` | ≤ 7 days | Budget context (which campaigns to focus offer on) |
| `/bidding-auditor` | `context/analysis/bidding-audit.md` | ≤ 7 days | Posture context |
| `/competitive-analyst` | `context/analysis/competitive-audit.md` | ≤ 14 days | Differentiation vs competitor offers |
| `/lp-auditor` | `context/analysis/lp-audit.md` | ≤ 14 days | Offer placement / hero clarity / message match |
| `/tracking-specialist` | `context/analysis/tracking-audit.md` | ≤ 30 days | Informational warning if dirty |
| `/strategy-specialist` | `context/analysis/strategy-audit.md` | ≤ 30 days | Break-even / posture for offer pricing tier |
| `/account-auditor` | `context/analysis/account-audit.md` | ≤ 30 days | Account-level posture/structure |

#### 0.5.2 — Extract findings into a peer-context buffer

For each **fresh** peer report, read it and extract ONLY the findings relevant to offer construction. Quote the exact text into an internal peer-context buffer keyed by peer skill. Skip stale and missing reports silently (do not warn — peer reports are optional). Examples of what to extract per peer:

- **`/strategy-specialist`** — break-even CPA/ROAS, posture (growth vs. efficiency), goal targets, payback window, viability score. These directly drive offer pricing tier and urgency intensity.
- **`/competitive-analyst`** — competitor offer landscape (lead offer types, urgency mechanics, trust patterns), impression-share gaps, auction-insights overlap. Drives **differentiation angle** — the most distinctive offer-maker enrichment.
- **`/lp-auditor`** — hero clarity score, offer-placement findings, message-match gaps, above-fold offer presence. Drives placement recommendations on the new offer.
- **`/quality-score-auditor`** — Landing Page Experience module findings, Ad Relevance handoff queue, ECTR handoff queue with `ar_status` and `recommended_action` columns. Drives offer-LP alignment and ECTR-improving framings.
- **`/search-term-auditor`** — top converting n-grams, customer-language phrases. Drives offer **phrasing** (e.g., if "emergency roof repair" is a top n-gram, the offer copy adopts that exact language).
- **`/keyword-auditor`** — theme alignment, top-performing themes. Confirms the offer ladders into existing keyword themes.
- **`/budget-auditor`** — budget-limited campaigns, allocation skew. Indicates which campaigns the offer should prioritize.
- **`/bidding-auditor`** — bid-strategy posture per campaign, learning state. Cross-references strategy-specialist's posture signal.
- **`/account-auditor`** — account-level structure, naming consistency, defaults.
- **`/tracking-specialist`** — completeness/tag-health module scores. Surfaces only as an informational note.

#### 0.5.3 — Quality Score Auditor handoff (special-case for `angles` and `variants`)

If `/quality-score-auditor` is fresh AND the action is `angles` or `variants`:

1. Read the `## Handoff Queue — Expected CTR (→ /offer-maker + /rsa-maker)` section. Columns: `ad_group | campaign | keywords_below_avg | impressions | class | ar_status | recommended_action`.
2. If the queue has rows, surface to the user:

   > "**QS Auditor handoff active.** {N} ad groups flagged with ECTR Below Avg / Average. The QS auditor recommends crafting angles that lean harder on: `{recommended_action}`. I'll bias angle extraction toward ECTR-improving framings."

3. If any row shows `ar_status=BELOW_AVG`, surface (informational only — no block):

   > "Note: {N} rows have AR Below Avg. ECTR fixes on these are symptom-treatment; consider running `/rsa-maker` against the Ad Relevance handoff queue first. Proceeding with offer angles regardless."

4. **COMPETITOR-class ECTR rows** — bias angles toward LP-driven offer strength (differentiation, risk reversal) rather than relevance messaging. Note this in the angles output.

#### 0.5.4 — Surface informational notes (M-layer / B-layer dirty)

Walk the buffer for low-score / dirty signals on **measurement** and **business** layers. These do NOT block generation; they are informational so the user knows the offer is being built on imperfect inputs:

- **M-layer (tracking dirty)** — if `/tracking-specialist` is fresh AND any module score < 70 OR completeness flags missing primary conversions:
  > "Heads-up: tracking audit shows {finding}. Offer outputs will still generate, but downstream conversion attribution may be unreliable until tracking is cleaned up."
- **B-layer (strategy dirty)** — if `/strategy-specialist` is fresh AND viability score < 70 OR break-even signals missing:
  > "Heads-up: strategy audit shows {finding}. Offer pricing-tier recommendations will fall back to brand.md / business.md defaults rather than peer-derived break-even math."

#### 0.5.5 — No-peer-data graceful path

If zero peer reports are fresh, skip the peer-context surface silently and proceed with the action using only `business.md` + `brand.md` as inputs. The skill must always work standalone.

#### 0.5.6 — Hand the buffer to the generation phase

The peer-context buffer (a structured map of `{peer_skill → extracted_findings}`) is passed to whichever E-action is running. The action MUST consume the buffer per the rules below.

---

### E01: Create Irresistible Offer

**Read `reference/execute-offer-creation.md` for detailed flow.**

Summary:
1. Confirm vertical (Lead Gen / SaaS / Ecommerce)
2. Walk through 4-pillar interview (Value, Uniqueness, Urgency, Trust)
3. Use vertical-specific question sets
4. Validate against Offer Audit Checklist (target: 12+/15)
5. Write offer section to business.md (ask permission first)
6. If score <12: flag gaps and suggest specific fixes

**Peer-context bias (from Phase 0.5 buffer):**
- **`/strategy-specialist`** — break-even CPA/ROAS and posture drive **pricing tier** and **urgency intensity**:
  - *Growth posture* → bias toward more aggressive offers (deeper discounts, stronger guarantees, bolder urgency).
  - *Efficiency posture* → bias toward conservative, value-led offers (bundle value, soft urgency, ROI framing over discounting).
  - Break-even unit economics constrain how deep a discount the offer can plausibly carry.
- **`/competitive-analyst`** — competitor offer landscape drives **differentiation** (the most distinctive enrichment for offer-maker):
  - If competitors all lead with "free trial" → bias the new offer's Uniqueness pillar away from free trial toward an alternative (e.g., paid pilot with money-back, results-based guarantee, longer eval window).
  - If competitors all lead with "% off" → bias toward fixed-dollar value, value-add bundles, or risk reversal.
  - Surface the competitor lead-pattern explicitly during the Uniqueness interview question.
- **`/lp-auditor`** — hero-clarity / offer-placement findings drive **placement recommendations** appended to the offer (e.g., "this offer must appear above the fold, hero-aligned, with the guarantee within one scroll").
- **`/quality-score-auditor`** — LPE module findings drive **offer-LP alignment** instructions (the new offer must use language that matches the LP's H1/sub-H1).
- **`/search-term-auditor`** — top converting n-grams drive offer **phrasing** (e.g., if "emergency roof repair" leads → the offer's headline language uses that exact phrase rather than a generic synonym).
- **`/budget-auditor`** — budget-limited campaigns drive **scope** (e.g., if only one campaign is budget-healthy, scope the offer's traffic-temp targeting to that campaign first).
- **`/bidding-auditor`** — confirms or contradicts strategy-specialist posture; if they conflict, surface and let the user pick.

**Output:** Updated `context/business.md` (Offer section), with a **Cross-skill context applied** sub-section listing which peer findings shaped which pillar choices (Value / Uniqueness / Urgency / Trust / Placement).

---

### E02: Craft Offer Angles

**Read `reference/execute-offer-angles.md` for detailed flow.**

Summary:
1. Check if `context/offer-angles.md` exists:
   - Exists + complete + no `--refresh` → Skip to Phase 3 (reprioritize)
   - Exists but incomplete OR `--refresh` → Start from Phase 0
   - Does not exist → Start from Phase 0
2. Phase 0: Classify traffic temperature
3. Phase 1: Document offer facts (pre-populate from brand.md, interview for gaps)
4. Phase 2: Extract 6 message angles with headline-ready phrases
5. Phase 3: Prioritize for traffic temperature
6. Phase 4: Validate via angle quality checklist
7. Write to `context/offer-angles.md`

**Peer-context bias (from Phase 0.5 buffer):**
- **`/competitive-analyst`** — competitor lead-angle landscape biases the **6 angles' framing** toward differentiation. If 4 of 6 default angles overlap heavily with competitor lead messaging, swap 2 of them for less-saturated framings (e.g., outcome-guarantee, contrarian-positioning, anti-pattern). Surface the avoided framings in the output.
- **`/search-term-auditor`** — top converting n-grams override generic phrasing in the headline-ready phrases. If a top n-gram exists for a vertical-relevant theme, the angle's primary headline phrase MUST contain that n-gram verbatim (subject to RSA character limits).
- **`/quality-score-auditor`** — the QS handoff queue (see Phase 0.5.3) biases angle selection toward **ECTR-improving framings** (offer strength, urgency, differentiation) for COMPETITOR-class rows. AR Below Avg rows surface as informational (no block).
- **`/lp-auditor`** — message-match findings constrain angles to language compatible with the current LP H1/sub-H1. If LP message-match score is low, surface a warning in the output recommending `/lp-optimizer` after RSA composition.
- **`/strategy-specialist`** — posture biases urgency intensity across all 6 angles (growth → punchier urgency hooks; efficiency → softer, ROI-led hooks).
- **`/keyword-auditor`** — confirms the angles ladder into top-performing keyword themes. Surface a note if any of the 6 angles target a theme with no live keyword coverage.
- **`/budget-auditor`** — drives traffic-temperature **prioritization** in Phase 3 (e.g., if cold-traffic campaigns are budget-starved, demote cold-temp angles in the priority order).

**Output:** `context/offer-angles.md`, with a **Cross-skill context applied** sub-section listing which peer findings shaped which angles (per-angle attribution where possible).

---

### E03: Competitor Offer Comparison

**Read `reference/execute-competitor-comparison.md` for detailed flow.**

Summary:
1. Read `context/competitor-ads/*.csv` files
2. Extract competitor offer elements across 4 pillars
3. Build comparison matrix: our offer vs. top 3 competitors
4. Identify advantages, parity, and disadvantages per pillar
5. Generate positioning recommendations

**Peer-context bias (from Phase 0.5 buffer):**
- **`/competitive-analyst`** — when fresh, its competitor offer landscape and impression-share gaps **augment** the CSV-derived comparison: prefer competitive-analyst's structured findings over raw CSV inference where they conflict, and surface the auction-insights overlap as a fourth dimension in the comparison matrix.
- **`/strategy-specialist`** — posture frames the **positioning recommendations** at the bottom (growth posture → "outflank" recommendations; efficiency posture → "differentiate without escalating spend" recommendations).
- **`/lp-auditor`** — message-match findings flag whether the recommended positioning is even deliverable on the current LP.

**Output:** `context/analysis/competitor-offer-comparison.md`, with a **Cross-skill context applied** sub-section listing which peer findings shaped which recommendations.

---

### E04: Diagnose Weak Elements

**Read `reference/execute-diagnose-weak.md` for detailed flow.**

Summary:
1. Read `context/analysis/offer-audit.md` (from `/offer-audit`)
2. Extract all FAIL and WARN items
3. Map each to specific fix action using gap tables
4. Present prioritized fix list with difficulty ratings
5. Optionally: walk user through fixing each element interactively

**Peer-context bias (from Phase 0.5 buffer):**
- **`/strategy-specialist`** — re-rank fix priority by economic leverage. Fixes that lift conversion-rate (Trust pillar) jump priority when break-even is tight; Value-pillar fixes (deeper discount, more bonuses) jump priority when posture is growth.
- **`/competitive-analyst`** — when an audit FAIL overlaps with a competitor's known strength, surface that overlap and recommend a differentiation-style fix rather than a parity-style fix.
- **`/lp-auditor`** — Trust-pillar fixes that require LP changes get a "requires `/lp-optimizer` follow-up" note.

**Output:** Displayed to user (interactive fixes). May update `context/business.md` if user approves. Includes a **Cross-skill context applied** sub-section in the displayed fix list noting which peer signals re-ranked which fixes.

---

### E05: Generate Angle Variants

**Read `reference/execute-angle-variants.md` for detailed flow.**

Summary:
1. Read `context/offer-angles.md`
2. For each of the 6 angles, generate 3-5 alternative headline phrases
3. Vary framing: different emotional hooks, different specifics, different structures
4. All variants must be <=30 characters
5. Optionally use search terms for customer language

**Peer-context bias (from Phase 0.5 buffer):**
- **`/search-term-auditor`** — top converting n-grams seed at least one variant per angle that uses the n-gram verbatim (subject to 30-char limit). This is the biggest lever for variant quality.
- **`/quality-score-auditor`** — for ECTR-flagged ad groups (Phase 0.5.3), bias variants toward stronger differentiation/urgency framings; ensure each angle has at least one variant tuned for ECTR lift.
- **`/competitive-analyst`** — avoid variants that mirror competitor lead-phrases verbatim; variants should sit in white space.
- **`/strategy-specialist`** — posture frames urgency intensity in variants (growth → punchier; efficiency → softer).

**Output:** Appended variant section in `context/offer-angles.md`, with a **Cross-skill context applied** sub-section noting which n-grams seeded which variants and which variants are ECTR-tuned.

---

## After Any Action

1. **Log to memory:** Append entry to `context/memory/YYYY-MM-DD.md`
2. **Suggest next step:**
   - After E01 → "Run `/offer-audit` to validate, then `/offer-maker angles` to extract angles"
   - After E02 → "Run `/rsa-maker` to compose RSAs from these angles"
   - After E03 → "Review comparison and run `/offer-maker create` to strengthen weak pillars"
   - After E04 → "Fix the items above, then re-run `/offer-audit` to verify"
   - After E05 → "Use variants in `/rsa-maker` for A/B testing"

---

## Integration Points

### Uses (reads from):
- `context/business.md` — Offer details, vertical, pricing
- `context/brand.md` — Value prop, USPs, trust signals (pre-population)
- `context/google-ads/data/search-terms.csv` — Customer language for phrases
- `context/competitor-ads/*.csv` — Competitor offers (E03)
- `context/analysis/offer-audit.md` — Audit results (E04)

**Peer audit reads (Phase 0.5 — Mode 2 enrichment, no gate):**
- `context/analysis/quality-score-audit.md` — LPE / AR / ECTR handoff queue (≤ 7 days)
- `context/analysis/search-term-audit.md` — Top converting n-grams for offer phrasing (≤ 7 days)
- `context/analysis/keyword-audit.md` — Theme alignment (≤ 7 days)
- `context/analysis/budget-audit.md` — Budget context (≤ 7 days)
- `context/analysis/bidding-audit.md` — Posture context (≤ 7 days)
- `context/analysis/competitive-audit.md` — Differentiation vs competitor offers (≤ 14 days) — **highest-leverage peer for offer-maker**
- `context/analysis/lp-audit.md` — Offer placement / hero clarity / message match (≤ 14 days)
- `context/analysis/tracking-audit.md` — Informational warning if dirty (≤ 30 days)
- `context/analysis/strategy-audit.md` — Break-even / posture for offer pricing tier (≤ 30 days)
- `context/analysis/account-audit.md` — Account-level posture/structure (≤ 30 days)

### Produces (writes to):
- `context/business.md` — Offer section (E01, E04)
- `context/offer-angles.md` — Message angles (E02, E05)
- `context/analysis/competitor-offer-comparison.md` — Comparison matrix (E03)

### Downstream consumers:
- `/rsa-maker` — Uses `context/offer-angles.md` for RSA composition
- `/offer-audit` — Validates offer quality after E01
- `/landing-page-builder` — Uses offer angles for LP copy
- QS analyzers — Reference angles for copy recommendations
