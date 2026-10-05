---
name: rehab-estimator
description: >
  Estimate rehab costs for investment properties. Produces itemized cost breakdowns for full rehab (flip) and wholetail exit strategies, calibrated to local labor rates. Generates Excel workbook. Trigger for: rehab estimate, rehab cost, renovation budget, scope of work, SOW, flip budget, wholetail cost, "how much to fix", repair estimate, or any request to estimate renovation costs for a property.
---

# Rehab Cost Estimator

Produces professional, itemized renovation cost estimates for investment properties. Two exit strategies analyzed side-by-side: **Full Rehab** (investor flip to retail) and **Wholetail** (light cosmetic for quick sale to another investor or retail-lite buyer).

All pricing is calibrated to the **local market** where the property sits — not national averages.

### Single-Estimate Approach

This skill produces ONE cost estimate per line item — not a Low/Mid/High range. The estimate targets the **low-to-mid range** of real-world contractor pricing (roughly the 35th percentile between Low and Mid reference prices in rehab-categories.md). This keeps estimates conservative and closer to what actual contractor bids come back at, based on real deal calibration data showing that Low/Mid/High ranges led to over-estimation. When in doubt, lean toward the lower end — real contractors tend to come in closer to low than mid on most line items.

## When to Read Reference Files

This skill uses progressive disclosure. Read these files at the specific steps indicated:

| File | When to Read | What It Contains |
|------|-------------|-----------------|
| `references/real-deal-calibration.md` | **Step 2 (FIRST — before scoping)** | **CRITICAL**: Verified unit prices from a real contractor SOW, scoping rules, and the 60-65% Rule sanity check. This file overrides all other pricing when there's a conflict. |
| `references/rehab-categories.md` | Step 3 (Scope of Work) | Complete line-item categories with calibrated $/unit for every repair item |
| `references/local-pricing-guide.md` | Step 4 (Local Pricing) | How to research and apply local labor/material adjustments by market |
| `references/finish-tiers.md` | Step 3 (Scope of Work) | Defines 4 finish tiers (Builder, Mid, Investor-Flip, Retail-Premium) with material specs |
| `references/wholetail-vs-rehab.md` | Step 3 (Scope of Work) | Exactly which items differ between wholetail and full rehab scopes |
| `scripts/generate_rehab_excel.py` | Step 6 (Deliverables) | Generates the Excel workbook with all sheets |

## Workflow Overview

```
Step 1: Gather Property Intel
Step 2: Photo & Condition Analysis
Step 2.5: Read Calibration Data (MANDATORY — read real-deal-calibration.md before scoping)
Step 3: Build Scope of Work (read rehab-categories.md, finish-tiers.md, wholetail-vs-rehab.md)
Step 4: Localize Pricing (read local-pricing-guide.md)
Step 5: Cross-Reference Comps (validate against Bucket B finishes)
Step 5.5: Calculate Full Deal Costs (financing, holding, buying, selling)
Step 6: Generate Deliverables (run scripts)
Step 7: Present to User
```

---

## Step 1: Gather Property Intel

Collect these inputs from the user. Some may come from uploaded files (comp reports, inspection reports, MLS listings), photos, or conversation:

**Required:**
- Property address (full: street, city, state, zip)
- Square footage (GLA)
- Bed/bath count
- Year built
- Current condition description OR photos

**Helpful but optional:**
- Comp report or ARV (from the comping skill or user-provided)
- Purchase price / contract price
- Specific known issues (roof age, HVAC status, foundation, etc.)
- User's target exit strategy preference
- User's budget constraints
- Whether the user has a GC or is self-managing
- **Financing details** (loan type, LTV, interest rate, points) — defaults to hard money assumptions if not provided
- **Hold time estimate** (months from purchase to sale) — will be dynamically calculated from rehab scope + comp DOM if not provided
- **Comp report days-on-market (DOM)** — if the comping skill was run, pull median DOM from Bucket B renovated comps to estimate resale timeline
- **Property tax amount** (annual) — will research if not provided
- **Whether property has HOA fees**

If the user provides a comp report (especially one from the real-estate-comping skill), extract:
- Bucket A median PPSF (unrenovated)
- Bucket B median PPSF (renovated)
- Renovation premium percentage
- What finishes the renovated comps had (if noted in comp comments)
- Subject property condition notes

---

## Step 2: Photo & Condition Analysis

If the user provides property photos or an inspection report, analyze them systematically. Go room by room, system by system:

### Exterior Checklist
| Component | What to Look For |
|-----------|-----------------|
| **Roof** | Missing/curled shingles, age indicators, moss/algae, flashing condition, gutter state |
| **Siding** | Cracks, rot, peeling paint, missing sections, material type (vinyl, wood, brick, fiber cement) |
| **Windows** | Single vs double pane, frame condition, fogging between panes, operability |
| **Foundation** | Visible cracks, bowing, water staining, settlement signs |
| **Concrete** | Driveway/walkway condition, heaving, major cracks |
| **Landscaping** | Overgrowth, grading issues, drainage concerns |
| **Garage** | Door condition, opener, structural concerns |

### Interior Checklist
| Component | What to Look For |
|-----------|-----------------|
| **Kitchen** | Cabinet condition, countertop material/condition, appliance age/working, layout functionality |
| **Bathrooms** | Tile condition, fixture age/style, vanity condition, toilet, tub/shower condition |
| **Flooring** | Type throughout (carpet, hardwood, vinyl, tile), condition, subfloor concerns |
| **Walls/Ceilings** | Drywall condition, cracks, water stains, texture type, paint condition |
| **Doors/Trim** | Interior door condition, hardware, baseboard/casing condition |
| **Electrical** | Panel type/age (fuse box vs breaker), outlet count, visible wiring issues |
| **Plumbing** | Pipe material visible (copper, PEX, galvanized, poly), fixture condition, water pressure |
| **HVAC** | System type, age, condition, ductwork visible |
| **Water Heater** | Type, age, capacity |

For each item, assign a condition rating:
- **Good** — Functional and presentable, no work needed
- **Fair** — Functional but dated, cosmetic update recommended for flip
- **Poor** — Needs replacement or significant repair
- **Missing/Failed** — Non-functional or absent, must address

---

## Step 2.5: Read Calibration Data (MANDATORY)

**Read `references/real-deal-calibration.md` NOW** — before building any scope of work.

This file contains verified unit prices from a real contractor SOW and the scoping rules that prevent over-estimation. Key rules:

### Scoping Discipline — Room-by-Room, NOT System-by-System

Real contractors scope by walking room to room and noting ONLY what each room needs. The skill must do the same:

1. Walk each room from the inspection photos
2. For each room, note ONLY what visibly needs to change
3. Common per-room items: paint, flooring, outlets/switches ($100/room), light fixtures, doors
4. NOT common: new windows (only if damaged/failed), trim (only if damaged)

### DO Scope:
- Items visibly damaged, broken, or missing
- Items outdated enough to hurt resale (old cabinets, dated fixtures when comps show modern)
- Code requirements (smoke detectors, GFCI outlets in wet areas)
- Cosmetic updates that comps show (LVP flooring, updated lighting)
- **Appliances** — ALWAYS include a full appliance package in the full rehab scope when renovated comps show updated appliances (almost always). This is the most commonly missed category. Typical SS package: fridge ($1,400) + dishwasher ($550) + microwave ($300) + stove ($700) = $2,950. Typical W/B package: fridge ($650) + dishwasher ($450) + microwave ($250) + stove ($450) = $1,800. Include even if existing appliances "work" — dated appliances kill buyer perception in a flip.
- **AC unit** — include when the existing system is >15 years old OR when the unit looks visibly dated/worn in photos, even if technically functional. Budget $2,800 for AC replacement. Buyers and inspectors flag old HVAC systems. Exception: if confirmed replaced within 2-3 years, exclude it.
- **Smoke detectors** — always include in any full rehab. Budget $30/ea × (bedrooms + 1 per floor). Code requirement.

### DON'T Scope:
- **HVAC** if confirmed newer (≤3 years old) by seller, listing, or visible manufacturer date — note "recently replaced, pending inspection"
- **Full panel upgrade** unless evidence of undersized (fuse box, < 100 amp)
- **System-wide outlet replacement** — only replace in rooms being renovated
- **All baseboard replacement** — only where visibly damaged or missing. But DO add shoe mold wherever new flooring is installed.
- **Staging, photography, permits** — these are NOT contractor costs (separate budget items)
- **Roof** — do NOT include roof replacement in the base estimate unless the roof is actively failing (visible holes, tarps, severe structural sag). Instead, note as "⚠️ Needs inspection — budget $7,000-$12,000 separately if replacement required." The roof is the single largest line item that inflates estimates when included speculatively. Real investors verify roof condition before committing this cost. If the user specifically asks to include the roof OR provides evidence of active failure, include it.
- **Every window** — only replace damaged, single-pane, or failed-seal windows. Count from photos, don't assume all need replacing. When photo evidence is ambiguous, estimate conservatively — err on the LOWER count and note uncertainty.
- **Garage door** — do NOT include garage door replacement ($1,000-$1,700) unless the door is visibly broken (panels missing, severe damage, won't open). A dated-looking garage door alone is not sufficient reason to replace. Note as optional: "⚠️ Garage door replacement if needed: $1,000-$1,700."
- **Speculative exterior items** — do NOT add tuckpointing, gutter repair, or other exterior items unless they are CLEARLY visible in photos as damaged or failing. Age alone is not enough to include these. Only scope soffit/fascia patches where visible damage is confirmed.

### Demo & Cleanup Scoping
Do NOT default to "full house demo + 2 dumpsters" unless the property genuinely requires gut-level demolition. Most investor flips need targeted demo, not a full gut:
- **Light cleanup** = general cleanup + hauling ($1,000-$1,500) — for houses needing cosmetic updating but not trashed
- **Moderate demo** = targeted demo (kitchen cabinets, bath tile, old flooring) + 1 dumpster ($2,000-$3,000) — most common for standard flips
- **Full demo** = gut demo + 2 dumpsters ($4,000-$5,000) — ONLY for hoarder houses, fire damage, or true gut-to-studs
Ask: "How much am I ripping out?" If the answer is "kitchen cabinets, bathroom tile, and old carpet" — that's moderate demo at most.

### The 60-65% Sanity Check

After building the estimate, check $/SF against these benchmarks:
- **$25-35/SF** = Standard investor flip (not a gut) in a Tier 2 market
- **$40-55/SF** = Heavy renovation with systems (plumbing, electrical, HVAC)
- **$60-80/SF** = Full gut-to-studs rebuild only

**If your estimate exceeds $40/SF on a standard flip, you are almost certainly over-scoping.** Go back and ask: "Would a real contractor actually replace this, or would they leave it alone?"

### Paint Estimation Rule

Quote paint as a SINGLE all-in rate (walls + trim + ceilings combined):
- Calculate: GLA × 3.5 = total paintable wall SF
- Apply rate: $2.00-$3.00/SF (Tier 2) or $3.00-$4.50/SF (Tier 1/HCOL)
- Add primer at HALF the total SF × $2.00/SF only if needed (dark colors, stains, smoke)
- **Do NOT break paint into 3 separate line items** (walls, trim, ceiling)

---

## Step 3: Build Scope of Work

**Read `references/rehab-categories.md` now** — it contains every line item with calibrated pricing.
**Read `references/finish-tiers.md` now** — it defines material quality levels.
**Read `references/wholetail-vs-rehab.md` now** — it defines scope differences.

Build TWO parallel scopes of work:

### Full Rehab Scope
Target: Retail-ready, matches or exceeds renovated comps (Bucket B). The goal is to produce a home that competes with the best renovated comps in the market. Think "HGTV ready."

Finish level: **Investor-Flip Grade** (see finish-tiers.md) unless comp analysis suggests otherwise.

Include every item rated Fair or worse. Also include items rated Good that are visually dated even if functional (e.g., brass fixtures in a 2025 market, oak cabinets when comps show white shaker).

### Wholetail Scope
Target: Clean, functional, move-in ready but NOT retail-show-ready. Buyer is often another investor or a budget-conscious retail buyer. The goal is maximum ROI with minimum spend — fix what's broken, clean what's dirty, and don't over-improve.

Finish level: **Builder Grade** to **Mid Grade** (see finish-tiers.md).

Only include items rated Poor or Missing/Failed, plus:
- Deep clean throughout
- Fresh paint (walls and trim)
- Basic flooring if carpet is stained/worn
- Any safety/code issues
- Curb appeal basics (pressure wash, basic landscaping)

### Pricing Hierarchy — Repair Cheat Sheet First

The company's **Repair Cheat Sheet** is the standard estimating tool. It defines how the team budgets deals. The AI MUST produce estimates that align with the cheat sheet's methodology and pricing — NOT the contractor SOW line-item detail. The contractor SOW (in real-deal-calibration.md) is verification data showing that cheat sheet prices are in the right ballpark, but the **cheat sheet is the budgeting standard**.

**Pricing source priority (highest to lowest):**
1. **User-provided pricing** — always overrides everything
2. **Repair Cheat Sheet prices** — the company's estimating standard (see table below)
3. **real-deal-calibration.md verified prices** — contractor verification data (use only when cheat sheet has no price for an item)
4. **rehab-categories.md reference prices** — national reference fallback (adjust by local cost index)

**Key Cheat Sheet prices (Tier 2 / Dayton, OH baseline):**

| Item | Cheat Sheet Price | Unit | Notes |
|------|------------------|------|-------|
| LVP / LVT | $3.50 | SF | Standard investor-grade. Only use $5.50 (Lifeproof premium) when ARV > $300K or comps show premium flooring |
| Carpet | $3.00 | SF | Standard. Only use $4.25 when ARV > $300K |
| Tile | $12.00 | SF | Consistent across all sources |
| Interior paint | $3.00 | SF | All-in rate (walls + trim + ceiling) |
| Primer | $2.00 | SF | Apply to ~50% of paintable area when needed |
| Drywall (new) | $5.00 | SF | Cheat sheet method. Do NOT use $105/sheet unless gut-level demo |
| Drywall punch repair | $250.00 | EA | Per occurrence |
| Kitchen cabinets (larger, rip+replace) | $3,900.00 | EA | Standard for most flips |
| Kitchen cabinets (smaller, rip+replace) | $2,900.00 | EA | Galley or small kitchens |
| Countertop (granite, small) | $2,500.00 | EA | Lump sum for standard kitchen |
| Full bath renovation | $4,000.00 | EA | Standard full bath |
| Light fixtures (whole house) | $1,000.00 | EA | Lump sum, not per-fixture |
| Outlets/switches (whole house) | $400.00 | EA | Lump sum, not per-room |
| Interior door slab | $220.00 | EA | Replace only damaged doors |
| Exterior door | $700.00 | EA | Standard size |
| Misc trim (whole house) | $500.00 | EA | Lump sum for shoe mold, baseboard, misc |
| Window (vinyl replacement) | $550.00 | EA | Price is correct; QUANTITY must be conservative |
| General cleanup | $1,000.00 | EA | Light cleanup for standard flips |
| Soffit patch | $100.00 | EA | Per section |
| Fascia patch | $100.00 | EA | Per section |

**Granularity rule:** When the cheat sheet uses a **lump sum** (e.g., "Light fixtures: $1,000"), estimate as a lump sum — do NOT itemize individual fixtures. When the cheat sheet uses **per-unit pricing** (e.g., "Windows: $550/EA"), estimate per-unit with a conservative quantity. Match the cheat sheet's level of detail.

### Quantity Estimation

For each line item, estimate quantities based on:
- **Square footage** — flooring, paint, drywall (use GLA + waste factor)
- **Room counts** — bathrooms, bedrooms drive fixture counts
- **Linear feet** — trim, baseboard (estimate from room perimeters: typical 12x12 room = 48 LF minus doors/windows)
- **Unit counts** — doors, windows, outlets, fixtures (estimate from bed/bath count and typical home layout)
- **Photos** — use visible evidence to refine estimates

Typical estimation shortcuts when exact measurements aren't available:
| Item | Estimation Method |
|------|------------------|
| Interior paint | GLA × 3.5 = paintable wall SF. Multiply by cheat sheet rate: **$3.00/SF** (Tier 2) or $4.00/SF (Tier 1/HCOL). Single line item covering ALL rooms including secondary spaces — do NOT break into separate entries for main vs secondary areas. Do NOT add paint registers/vents separately (covered by contingency). |
| Primer | (GLA × 3.5) × 0.5 = primer SF (only where needed: dark colors, stains, smoke). Multiply by $2.00/SF. |
| Flooring | Estimate total SF by room type: LVP areas (living, kitchen, dining, hallways, secondary spaces) + Carpet areas (bedrooms) + Tile areas (bathrooms, laundry). Use **cheat sheet prices**: LVP $3.50/SF, Carpet $3.00/SF, Tile $12.00/SF. Only use premium LVP pricing ($5.50/SF Lifeproof) when ARV > $300K and comps specifically show premium flooring brands. Include 10% waste factor for LVP/tile. |
| Trim (all types) | Use cheat sheet lump sum: **$500** for whole-house misc trim (shoe mold, baseboard, casing). Do NOT itemize linear footage unless the user specifically requests a detailed SOW. The $500 lump covers shoe mold in rooms with new flooring plus baseboard repairs where visibly damaged. |
| Interior doors | (Bedrooms × 1) + (Bathrooms × 1) + 2 (closets per bedroom) + 2 (utility). Only replace if damaged — not all doors in the house. |
| Electrical | Use cheat sheet lump sum: **$400** for whole-house outlet/switch updates in a standard flip. Only itemize per-room ($100/room) when doing extensive electrical work in 6+ rooms. |
| Light fixtures | Use cheat sheet lump sum: **$1,000** for whole-house light fixture updates. Do NOT itemize individual fixtures unless the user specifically requests it or the home has 15+ fixtures to replace. |
| Drywall | Use cheat sheet method: estimate **SF of drywall needed × $5.00/SF** for standard flips. For a cosmetic flip, total drywall is typically $500-$1,000 (100-200 SF of new drywall). Add $250 for punch repair if needed. Only use per-sheet pricing ($105/sheet, 10-15 sheets) when there is **visible evidence of widespread water damage, structural repairs, or gut-level demolition**. Most flips need spot repairs, not full sheets in every room. |
| Windows | **Count from photos, not assumptions.** Only replace if damaged/failed/single-pane. A typical 3/2 ranch has 12-15 windows total — usually only **50-65% need replacement** (6-10 windows). Over-counting by even 3 windows = $1,650 error at $550/ea. **Always round DOWN** and note the uncertainty. Count only windows with CLEAR evidence of failure. |
| Kitchen fixtures | For standard flips, budget kitchen fixtures (faucet, sink, disposal, backsplash, pulls, ice maker) as a **$500-800 allowance** — do NOT itemize each fixture separately. Itemized kitchen fixtures add ~$1,300 of over-detail that doesn't match how the team budgets deals. Only itemize if the user specifically requests line-item kitchen pricing. Total kitchen budget = cabinets (cheat sheet price) + countertop (cheat sheet price) + fixtures allowance ($500-800). |
| Underlayment | Cement board under bathroom tile: included in the bathroom renovation lump sum. Do NOT add as a separate line item (covered by contingency). |
| Appliances | ALWAYS include for full rehab when comps show updated appliances. SS package: fridge ($1,400) + dishwasher ($550) + microwave ($300) + stove ($700) = $2,950. W/B package: $1,800. Do NOT skip this just because existing appliances "work." |
| AC unit | Include at $2,800 when system is >15 years old or looks dated. Exclude ONLY if confirmed ≤3 years old. Separate from furnace — AC is the most commonly flagged item in buyer inspections. |

### CRITICAL: Complete Room Inventory

The most common scoping error is forgetting transitional and secondary spaces. After scoping all main rooms, do a second pass:

| Forgotten Space | Typical Needs | Approx Cost |
|----------------|---------------|-------------|
| Back porch/Sunroom | Paint, LVP, shoe mold, light fixture, drywall, possibly storm door | $1,500-2,500 |
| Mud room/Utility room | Paint, LVP, shoe mold, cabinet pulls, light fixture, door | $700-1,200 |
| Foyer/Entry | LVP, shoe mold, baseboard, smart locks, paint exterior door | $400-700 |
| Hallway(s) | LVP, shoe mold, light fixtures, switches | $700-1,200 |
| Laundry area | Paint, flooring, possibly shelving | $300-600 |

**Rule**: Every space a buyer walks through must look finished. If it has walls and a floor, it needs to be in the scope.

### Small Items — Covered by Contingency

Do NOT add a separate "small items" category. Items like caulk, registers, underlayment, storm doors, ice maker kits, and cabinet pulls are covered by the **contingency percentage** (15-20%). Itemizing these separately on top of contingency double-counts them and inflates the estimate by $400-700.

The only exception: if the user specifically asks for a fully itemized SOW with every small item broken out, then include them — but reduce the contingency to 10% to avoid double-counting.

---

## Step 4: Localize Pricing

**Read `references/local-pricing-guide.md` now.**

National averages are a starting point, not the answer. Every market has different labor rates and material availability. The local-pricing-guide contains the methodology for adjusting costs based on:

1. **Geographic cost index** — use RSMeans or similar regional multipliers
2. **Metro vs rural** — labor availability affects rates
3. **State/local permit costs** — varies dramatically
4. **Market-specific material costs** — lumber varies by region, concrete by climate zone
5. **Seasonal factors** — winter construction in cold climates costs more

Use web search to find current labor rates for the specific city/metro area:
- Search: `"{city} {state}" contractor labor rates {current_year}`
- Search: `"{city} {state}" renovation cost per square foot {current_year}`
- Search: `"{metro area}" home renovation costs {current_year}`
- Search: `"cost of living index" "{city}" OR "{metro area}"`

Apply the local adjustment multiplier to every line item's labor component. Materials adjust less dramatically but still vary by region (10-20% swing in lumber/concrete).

---

## Step 5: Cross-Reference Against Comps

This step ensures the rehab budget makes economic sense. If the user provided comp data (especially from the real-estate-comping skill):

### Validate the Spread
```
Renovation Spread = Bucket B Median PPSF - Bucket A Median PPSF
Market Premium = Spread × Subject GLA = What the market pays for renovation

Full Rehab Budget should be 40-70% of Market Premium
  → If budget > 70% of premium: warn — thin margin, risk of over-improvement
  → If budget < 40% of premium: great margin, but verify scope isn't too light
```

### Match Comp Finishes
Look at what the renovated comps (Bucket B) actually had:
- If comps had granite counters, budget granite (not laminate)
- If comps had LVP flooring, budget LVP (not carpet or tile)
- If comps had stainless appliances, budget stainless
- The rehab should MATCH the renovated comps, not exceed them — over-improvement kills ROI

### Wholetail Validation
```
Wholetail Target Price = Bucket A Median PPSF × Subject GLA + 10-15% (light premium for clean/functional)
Wholetail Spread = Wholetail Target - Purchase Price - Wholetail Rehab Cost
```

---

## Step 5.5: Calculate Full Deal Costs

A rehab estimate without the full deal cost picture is dangerously misleading. The renovation cost is often less than half the total cost of doing the deal. Financing, holding, and transaction costs can easily add $25K-40K+ to the total, and ignoring them makes profit projections look much better than reality.

The skill must calculate ALL deal costs — not just ARV minus purchase minus rehab. Real investors use a full deal analyzer that accounts for every dollar in and out.

### When to Calculate

Calculate full deal costs whenever the user provides (or you can determine) both:
- A purchase price or contract price
- An ARV or estimated sale price

If either is missing, still produce the rehab estimate but note in caveats that deal analysis requires purchase price and ARV.

### Financing Costs

If the user provides specific financing terms, use those. Otherwise, apply these **hard money defaults** (the most common financing for flips):

| Parameter | Default | Notes |
|-----------|---------|-------|
| Loan amount | Purchase + Rehab (100% LTV) | Hard money typically finances acquisition + rehab |
| Interest rate | 12% annual | Standard hard money rate in 2025-2026 |
| Points | 0% | Conservative — many lenders charge 1-3% |
| Hold time | Dynamically calculated (see below) | Rehab duration + marketing/sale period |

**Hold Time Calculation (Dynamic):**

Instead of a static 4-month default, calculate hold time from the scope of work and comp data:

```
Total Hold Time = Rehab Duration + Marketing/Sale Period

Rehab Duration = estimated from scope complexity (see table below)
Marketing/Sale Period = median DOM from Bucket B renovated comps (if available)
                        OR default 45-60 days if no comp DOM available
```

**Rehab Duration Benchmarks (by scope):**

| Scope Complexity | Typical Duration | Indicators |
|-----------------|-----------------|------------|
| Light cosmetic (wholetail) | 2-3 weeks | Paint, clean, minor repairs only |
| Moderate cosmetic | 4-6 weeks | Kitchen/bath refresh, flooring, paint throughout |
| Full cosmetic | 6-8 weeks | Full kitchen/bath remodel, all flooring, paint, fixtures |
| Full rehab (no structural) | 8-12 weeks | Everything above + windows, HVAC, electrical, plumbing updates |
| Major rehab (structural) | 12-16 weeks | Foundation, roof, load-bearing walls, additions |

Round up to the nearest month for calculation. Add 2-4 weeks buffer for permitting delays in markets that require permits for rehab work.

**Marketing/Sale Period:**
- If the comping skill was run, pull median DOM from the **Bucket B (renovated) comps**. This is the most accurate predictor of how long a renovated property takes to sell in that specific market.
- If DOM data is available: Marketing/Sale Period = Bucket B median DOM (convert to months by dividing by 30, round up)
- If DOM data is NOT available: Default to 1.5 months (45 days) for Tier 2 markets, 1 month for hot markets, 2 months for slow markets
- Add 30 days for closing process on top of DOM (buyer financing, inspections, etc.)

**Example (dynamic calculation):**
- Full cosmetic rehab → 2 months rehab duration
- Bucket B median DOM = 28 days → ~1 month marketing + 1 month closing = 2 months sale period
- **Total hold time = 4 months**

**Example (no comp DOM available):**
- Full rehab, no structural → 3 months rehab duration
- No DOM data → default 1.5 months marketing + 1 month closing = 2.5 months → round to 3 months
- **Total hold time = 6 months**

If the user provides a specific hold time, always use that instead of calculating.

**Financing cost formula:**
```
Loan Amount = Purchase Price + Rehab Cost
Monthly Interest = Loan Amount × (Annual Rate / 12)
Total Financing Cost = Monthly Interest × Hold Time (months)
```

Example: $202,000 loan × (12% / 12) = $2,020/month × 4 months = $8,080

### Holding Costs (Monthly)

Research or estimate these based on the property's location:

| Item | How to Estimate | Typical Range |
|------|----------------|---------------|
| Property taxes | Search county auditor for annual amount, divide by 12 | $150-$500/mo |
| Insurance | Investor/builder's risk policy | $150-$250/mo |
| Utilities — Gas | Seasonal, minimal during rehab | $50-$100/mo |
| Utilities — Water | Needed for construction | $50-$100/mo |
| Utilities — Electric | Needed for construction | $50-$100/mo |
| HOA/Condo fees | Only if applicable | $0-$400/mo |
| Other (lawn, security) | Minimal | $0-$75/mo |

**Total holding = Monthly total × Hold time (months)**

Hold time here uses the dynamically calculated total (rehab duration + marketing/sale period) from the financing section above. This means holding costs scale accurately with the actual project timeline rather than a static assumption.

For a Tier 2 market (Midwest), typical monthly holding is $700-$1,000/month.

### Buying Transaction Costs

| Item | How to Calculate | Typical |
|------|-----------------|---------|
| Escrow/Attorney fees | Fixed | $750-$1,200 |
| Title insurance | ~0.77% of purchase price (tiered by state) | $800-$1,500 |
| Title search | Often bundled with title insurance | $0-$500 |

Note: Title insurance uses state-regulated tiered rate schedules — not a flat percentage. The ~0.77% rate is calibrated from real Ohio closings and is a reasonable default for Tier 2 markets. Rates vary by state.

### Selling Transaction Costs

| Item | How to Calculate | Typical |
|------|-----------------|---------|
| Realtor fees | 5-6% of sale price (ARV) | Largest selling cost |
| Title insurance | ~0.64% of sale price (tiered by state) | $1,000-$2,500 |
| Escrow/Attorney fees | Fixed | $750-$1,200 |
| Recording fees | Fixed | $300-$500 |
| Transfer/Conveyance tax | Varies by state (0.10-0.15% typical) | $200-$500 |
| Home warranty | Buyer incentive | $500-$750 |

### True Profit Calculation

```
Net Profit = ARV
           - Purchase Price
           - Rehab Cost
           - Financing Costs
           - Holding Costs
           - Buying Costs
           - Selling Costs

True ROI = Net Profit / (Purchase Price + Rehab Cost + Financing + Holding + Buying)
```

This is the number that matters. A deal that looks like $46K profit on simple math might actually be $31K after all costs — that's a 32% reduction. Getting this wrong means making bad buying decisions.

---

## Step 6: Generate Deliverables

Compile all analysis into a JSON data structure, then run both report generators.

### Data Structure

```json
{
  "property": {
    "address": "string",
    "city": "string",
    "state": "string",
    "zip": "string",
    "county": "string",
    "gla": 0,
    "beds": 0,
    "baths": 0.0,
    "year_built": 0,
    "lot_size": "string",
    "property_type": "string",
    "condition_summary": "string"
  },
  "comp_reference": {
    "arv": 0,
    "bucket_a_ppsf": 0.0,
    "bucket_b_ppsf": 0.0,
    "renovation_premium_pct": 0.0,
    "market_premium_dollars": 0,
    "comp_finish_notes": "string",
    "purchase_price": 0
  },
  "condition_assessment": [
    {
      "category": "string",
      "item": "string",
      "condition": "Good|Fair|Poor|Missing",
      "notes": "string",
      "photo_reference": "string"
    }
  ],
  "local_pricing": {
    "city": "string",
    "state": "string",
    "cost_index": 0.0,
    "labor_rate_multiplier": 0.0,
    "material_rate_multiplier": 0.0,
    "notes": "string",
    "sources": ["string"]
  },
  "rehab_estimate": {
    "scope": "Full Rehab",
    "finish_tier": "Investor-Flip Grade",
    "categories": [
      {
        "category": "string",
        "items": [
          {
            "item": "string",
            "include": true,
            "qty": 0,
            "unit": "string",
            "unit_cost": 0.0,
            "total": 0.0,
            "notes": "string"
          }
        ],
        "category_total": 0.0
      }
    ],
    "subtotal": 0,
    "contingency_pct": 0.10,
    "contingency": 0,
    "grand_total": 0,
    "cost_per_sf": 0.0
  },
  "wholetail_estimate": {
    "scope": "Wholetail",
    "finish_tier": "Builder to Mid Grade",
    "categories": [
      "...same structure as rehab_estimate categories..."
    ],
    "subtotal": 0,
    "contingency_pct": 0.05,
    "contingency": 0,
    "grand_total": 0,
    "cost_per_sf": 0.0
  },
  "deal_analysis": {
    "arv": 0,
    "purchase_price": 0,
    "rehab_cost": 0,
    "wholetail_cost": 0,
    "hold_time_months": 4,
    "hold_time_breakdown": {
      "rehab_duration_weeks": 0,
      "rehab_duration_months": 0,
      "comp_dom_days": null,
      "marketing_period_months": 0,
      "closing_period_months": 1,
      "source": "calculated|user_provided",
      "notes": ""
    },
    "financing": {
      "loan_amount": 0,
      "ltv_pct": 1.0,
      "interest_rate_annual": 0.12,
      "points_pct": 0,
      "monthly_interest": 0,
      "total_financing_cost": 0,
      "notes": "Hard money, 100% LTV on purchase + rehab"
    },
    "holding_costs": {
      "property_taxes_monthly": 0,
      "insurance_monthly": 0,
      "hoa_monthly": 0,
      "gas_monthly": 0,
      "water_monthly": 0,
      "electric_monthly": 0,
      "other_monthly": 0,
      "total_monthly": 0,
      "total_holding": 0
    },
    "buying_costs": {
      "escrow_attorney": 900,
      "title_insurance": 0,
      "title_insurance_pct": 0.0077,
      "total_buying": 0
    },
    "selling_costs": {
      "realtor_pct": 0.05,
      "realtor_fees": 0,
      "title_insurance": 0,
      "title_insurance_pct": 0.0064,
      "escrow_attorney": 900,
      "recording_fees": 400,
      "transfer_tax": 0,
      "transfer_tax_pct": 0.0012,
      "home_warranty": 750,
      "total_selling": 0
    },
    "rehab_total_all_in": 0,
    "wholetail_total_all_in": 0,
    "rehab_net_profit": 0,
    "wholetail_net_profit": 0,
    "rehab_roi_pct": 0.0,
    "wholetail_roi_pct": 0.0,
    "mao_75_pct": 0,
    "rehab_margin_vs_premium": 0.0
  },
  "recommendations": ["string"],
  "caveats": ["string"]
}
```

### Generate Reports

Install dependencies if needed:
```bash
pip install openpyxl --break-system-packages
```

1. Save the JSON data to a temp file
2. Run `scripts/generate_rehab_excel.py <output_path> <json_path>` to create the Excel workbook

---

## Step 7: Present to User

Present the key findings in conversation BEFORE linking the files. Structure:

### Summary Format
```
## Property: [Address]

### Condition Highlights
[3-5 most significant findings from photo/inspection analysis]

### Cost Estimates (Local pricing for [City, State])

| | Full Rehab | Wholetail |
|---|---|---|
| **Estimate** | $XX,XXX | $XX,XXX |
| **$/SF** | $XX.XX | $XX.XX |

### Full Deal Analysis (if ARV/purchase price available)
| Cost Category | Full Rehab | Wholetail |
|---------------|-----------|-----------|
| ARV (Sale Price) | $XXX,XXX | $XXX,XXX |
| Purchase Price | $XXX,XXX | $XXX,XXX |
| Rehab Cost | $XX,XXX | $XX,XXX |
| Financing Costs | $X,XXX | $X,XXX |
| Holding Costs (X mo) | $X,XXX | $X,XXX |
| Buying Costs | $X,XXX | $X,XXX |
| Selling Costs | $XX,XXX | $XX,XXX |
| **Total All-In Cost** | **$XXX,XXX** | **$XXX,XXX** |
| **Net Profit** | **$XX,XXX** | **$XX,XXX** |
| **ROI** | **XX%** | **XX%** |
| MAO (75% Rule) | $XXX,XXX | — |

### Top 5 Budget Line Items
[Largest cost items to set expectations]

### Recommendations
[2-3 strategic observations]
```

Then link the deliverable:
- Excel workbook (itemized breakdown with all sheets)

---

## Contingency Guidelines

| Property Condition | Rehab Contingency | Wholetail Contingency |
|-------------------|------------------|----------------------|
| Good/Fair overall, post-1990 | 10% | 5% |
| Good/Fair overall, pre-1990 | 15% | 7% |
| Poor condition, any age | 15-20% | 10% |
| Pre-1970 (lead paint, galvanized, cast iron risk) | 20% | 10% |
| Unknown/limited photos | 20% | 10% |
| Known foundation/structural | 20-25% | 15% |

**Default contingency for most flips: 15-20%.** The 10% default was found to underestimate real-world surprises. Real investors like Aaron use 20% contingency as their standard — this gives a buffer for the items you can't see in photos (behind walls, under floors, in the crawlspace). Only use 10% when the property is newer (post-1990) and you have comprehensive photos showing good overall condition.

Older properties (pre-1970) often have hidden costs: asbestos abatement, lead paint, knob-and-tube wiring, galvanized plumbing, cast iron drain lines. Flag these in the estimate when year_built suggests risk.

---

## Key Principles

1. **Scope like a contractor, not an inspector** — Real contractors only replace what's broken, damaged, or too dated to sell. They do NOT replace every outlet, every door, all trim, or every window just because they're in the house. The #1 cause of over-estimation is over-scoping. When in doubt, leave it out.

2. **The 60-65% Sanity Check** — After building your estimate, divide total by GLA. If $/SF exceeds $40 on a standard flip (no systems work), you are over-scoping. Go back and cut items a real contractor would skip.

3. **Local pricing matters** — A $30/hr labor market (Dayton, OH) produces fundamentally different budgets than a $65/hr market (San Francisco). Always localize. The calibration file provides Tier 2 (Midwest) benchmarks.

4. **Mirror the comps** — The rehab finish level should match what sold in Bucket B. Over-improving beyond what comps support is the #1 rookie mistake.

5. **Wholetail is a real strategy** — Not every deal needs a full rehab. Sometimes $8K in paint, flooring, and cleaning nets more ROI than a $45K full gut. Present both options so the investor can choose.

6. **Photos > assumptions** — When photos are available, use what you can actually see. When they're not, disclose that estimates are based on age/condition assumptions and widen the contingency.

7. **Permits, staging, and photos are NOT contractor costs** — Never include these in the renovation estimate. They are separate budget line items in the deal analysis, not the SOW.

8. **Paint is one line item** — Real contractors quote paint as a single all-in $/SF rate. Never split into walls + trim + ceilings as 3 separate line items.

9. **One estimate, not three** — Produce a single cost per line item targeting the low-to-mid range. Real contractors give you one number, not a range. Three-tier estimates create analysis paralysis and the mid tends to over-estimate. If there's genuine uncertainty on a specific item (e.g., roof condition unknown), note the uncertainty in the item's notes field and widen the contingency percentage instead.

10. **75% Rule for MAO** — Max Allowable Offer = ARV × 75% − Rehab Cost. This replaces the traditional 70% rule to reflect realistic deal economics — the 70% rule is overly conservative and causes investors to pass on viable deals.

11. **Rehab cost is NOT profit** — A deal's true profit = ARV minus ALL costs: purchase, rehab, financing, holding, buying transaction costs, and selling transaction costs. Financing + holding + transaction costs typically add $25K-40K+ on top of the rehab budget. Showing profit as just "ARV minus purchase minus rehab" gives investors a dangerously inflated view that leads to bad buying decisions. Always calculate and present the full deal cost picture.
