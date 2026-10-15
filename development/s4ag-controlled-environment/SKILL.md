---
name: s4ag-controlled-environment
description: "Design, set up, or optimise a CEA system — hydroponics, aquaponics, or vertical farming. Use when the user mentions DWC, NFT, ebb-and-flow, grow lights, nutrient solution, aquaponics, or says 'controlled environment', 'indoor growing', 'vertical farm'."
allowed-tools: [Read]
---

# Controlled Environment Agriculture

Controlled environment agriculture (CEA) lets you produce food year-round, independent of outdoor climate — but the capital and operating costs are substantial, and the wrong system for the wrong crop at the wrong scale will lose money reliably. The goal here is to match the right system to your crop, your scale, your budget, and your market before you spend a dollar on hardware. A CEA system that pencils out and is properly managed can produce ten to twenty times the yield per square metre of outdoor growing; one that doesn't fit the context produces expensive salad greens and regret.

**How this skill works:** Each sub-tool pauses at a **Checkpoint** to confirm the assumptions it is about to build on before producing output. A recommendation built on a wrong assumption wastes time and money — confirm the checkpoint before acting. Each sub-tool ends with **Next steps** — the skills worth running once you have acted on this one.

---

## Expert Lineage

*The thinkers whose frameworks underpin this skill — and what they specifically discovered that changes how you farm.*

**Cornell CEA Programme — the institutional benchmark**
Cornell's Controlled Environment Agriculture programme has produced more peer-reviewed guidance on hydroponic crop production than any other institution. Their specific contribution: rigorous Daily Light Integral (DLI) targets by crop, evidence-based nutrient solution formulations, and economic modelling that shows exactly when CEA beats field production economically — and when it does not. Their public-facing research, especially on lettuce and leafy greens, is the most reliable source of seeding density, harvest timing, and yield projections in the field.

**Merle Jensen — controlled environment horticulture foundations**
Jensen at the University of Arizona established the foundational academic framework for CEA in North America. His most actionable finding: environment control precision is the primary yield driver — temperature differentials between day and night (DIF management) can be used to manipulate stem elongation without any chemical intervention, reducing the need for plant growth regulators. His work on nutrient film technique (NFT) systems for arid climates remains relevant for water-limited contexts.

**Will Allen — CEA integrated with community food systems**
Allen at Growing Power demonstrated that aquaponics-based CEA could operate profitably at community scale while producing both protein (tilapia) and high-value greens. His specific finding: the biological nutrient cycle in a well-managed aquaponic system reduces input costs to 30–50% of equivalent hydroponic systems, because fish waste replaces purchased nutrient concentrates. He also demonstrated that CEA biological systems require active microbial management — not sterile control.

**Nate Storey — vertical farming systems design**
Storey, founder of Plenty and earlier Bright Agrotech, demonstrated that vertical farming economics depend almost entirely on light efficiency — the cost per photon delivered to leaves, not the cost of the structure or water. His contribution: spacing, plant density, and spectrum tuning matter more than any other variable in vertical systems. The farms that fail do so because they optimise aesthetics or structure over photon economics.

**Nick Savidov — biological aquaponics research**
Savidov's Alberta Agriculture research established that biologically managed aquaponic systems consistently outperform sterile chemical hydroponic systems in plant health, disease resistance, and long-term yield stability. His mechanism: a diverse microbial community in the root zone provides systemic induced resistance (SIR) against Pythium and other root pathogens — the same mechanism Ingham documents in soil food webs, operating in water.

**Elaine Ingham — the food web exists in water too**
Ingham's soil food web framework applies directly to biological hydroponic and aquaponic systems, even though there is no soil. Beneficial bacteria, fungi, protozoa, and nematodes colonise root zones in any growing medium given the right conditions. Her finding that most "nutrient deficiency" symptoms in soil are actually food web dysfunctions applies equally to CEA: plants showing nutrient stress in a correctly-formulated solution are often experiencing root zone biological failure, not nutrient absence.

---

## Which tool fits

| You need to... | Tool |
|---|---|
| Choose between DWC, NFT, ebb-and-flow, or aquaponics | system-selection |
| Formulate or troubleshoot a nutrient solution | nutrient-management |
| Decide on natural vs supplemental lighting, or choose LEDs | lighting |
| Decide what to grow given the system, scale, and market | crop-selection |
| Calculate whether a CEA investment makes financial sense | economics |

## Routing Decision

- **Just starting out, don't know which system to choose** → system-selection
- **Have a system, struggling with plant health or nutrient problems** → nutrient-management
- **Crops are leggy, pale, or slow — suspect a light problem** → lighting
- **Trying to decide what to grow in an existing or planned system** → crop-selection
- **Evaluating whether to invest in CEA, or whether the current system is viable** → economics
- **Unclear** → system-selection first; it determines what everything else looks like

---

## System Selection

*Matches the right CEA system type to your crop, scale, and budget.*

CEA encompasses several distinct system architectures. Choosing the wrong one for your context is expensive to reverse. Work through this decision in order.

**Step 1: What are you growing?**

| Crop category | Best system fit | Poor system fit |
|---|---|---|
| Leafy greens, lettuce, herbs | NFT, DWC raft, vertical tower | Ebb-and-flow (overkill), aquaponics (slower to establish) |
| Tomatoes, cucumbers, peppers | Dutch bucket (media bed), coir slab | NFT (insufficient root volume), DWC (stem disease risk) |
| Strawberries | NFT, tower systems | Ebb-and-flow |
| Microgreens | Shallow trays with media | Any recirculating system (contamination risk) |
| Mixed greens + fish | Aquaponics | Purely chemical hydroponics (you want the biology) |
| Cannabis / high-value floriculture | Ebb-and-flow, Dutch bucket | NFT (too little root zone buffer) |

**Step 2: What is your scale?**

| Scale | Recommended systems | Notes |
|---|---|---|
| Home / micro (under 10m²) | DWC bucket, small NFT channel, tower garden | Keep it simple — fewer moving parts |
| Small commercial (10–100m²) | NFT gutter system, DWC raft pond, small aquaponics | Raft DWC is the most forgiving for first commercial grows |
| Medium commercial (100m²–1000m²) | Full NFT, raft DWC, Dutch bucket, aquaponics | Automation becomes necessary; invest in monitoring |
| Large commercial (1000m²+) | Vertical farming with LED stacking, fully automated | Requires professional design; do not DIY at this scale |

**Step 3: What is your water situation?**

- Limited water / arid region: hydroponics recirculates 90–95% of water vs. 30–50% loss in field growing. All hydroponic systems are good options.
- Abundant water / municipal supply: consider water cost in economics. Aquaponics uses 90%+ less water than equivalent soil production.
- Well water: test for iron, calcium, bicarbonates before designing a system — high iron clogs emitters; high bicarbonates cause pH drift.

**Step 4: Choose a system**

| System | How it works | Pros | Cons |
|---|---|---|---|
| Deep Water Culture (DWC / raft) | Plants float on styrofoam over aerated nutrient solution | Forgiving, high buffering capacity, fast growth | Large water volume slows adjustment; Pythium risk if aeration fails |
| Nutrient Film Technique (NFT) | Thin film of solution flows along channels past bare roots | Low capital cost, easy to scale, good for leafy greens | Low buffering — errors propagate fast; root zone dries quickly if pump fails |
| Ebb-and-flow (flood and drain) | Growing media flooded periodically, then drained | Flexible media choice, suits large plants | More moving parts; timer failure causes problems |
| Dutch bucket / media bed | Plants in individual containers of coir, perlite, or rockwool | Good for fruiting crops; robust root zone | Higher media cost; less water efficiency than DWC/NFT |
| Aquaponics | Fish waste provides nutrients; plants clean water for fish | Lower ongoing input cost; biological resilience; dual product | Longer to establish; more complex; fish mortality is a crisis |
| Vertical / tower | Plants in vertical stacks with drip or wick irrigation | Maximum space efficiency; visually appealing | Higher capital cost per plant; light distribution is the challenge |

**Checkpoint — confirm before finalising:**
- What specific crop or crop mix are you targeting — and does that match the system you are considering?
- What is your total floor area, ceiling height (for vertical systems), and whether natural light is available?
- Are you building from scratch or adapting an existing space (greenhouse, warehouse, shed)?

A system recommendation without knowing the crop, the space, and the available light is meaningless — these three determine everything else.

**Output:**
```
CEA SYSTEM RECOMMENDATION
Crop: [crop or crop mix]
Scale: [m² or ft²]
Space type: [greenhouse / indoor warehouse / shed / other]

Recommended system: [system name]
Rationale: [2-3 sentences on why this fits]

System components needed:
- [reservoir / channels / raft pond / etc.]
- [pump and delivery]
- [aeration]
- [monitoring: EC meter, pH meter, thermometer]
- [lighting if applicable]

What to avoid: [system type] — because [reason specific to this context]

Estimated capital cost range: [$ range for this scale]
Timeline to first harvest: [weeks from setup]
```

**Next steps:**
- Run **nutrient-management** (within this skill) to formulate the feed programme for the chosen system.
- Run **lighting** (within this skill) if operating indoors or in a low-light space.
- Run **economics** (within this skill) to confirm the investment makes financial sense before purchasing.

---

## Nutrient Management

*Formulates and troubleshoots the nutrient solution for hydroponic and aquaponic systems.*

Hydroponic plants access nutrients dissolved in water. There is no soil food web to buffer, cycle, or supply what is missing — which means you are responsible for everything. The practical challenge is not knowing what to put in; it is keeping the solution balanced, stable, and biologically healthy over time.

**The baseline parameters — monitor these daily:**

| Parameter | Target range (most crops) | Notes |
|---|---|---|
| EC (electrical conductivity) | 1.5–3.5 mS/cm | Seedlings: lower (1.0–1.8). Fruiting crops: higher (2.5–3.5). Herbs: 1.0–2.0. |
| pH | 5.8–6.5 | Outside this range, nutrient uptake fails even if nutrients are present. Check twice daily at first. |
| Temperature (solution) | 18–24°C | Above 26°C, dissolved oxygen drops; Pythium thrives. Below 15°C, root activity slows. |
| Dissolved oxygen | >6 mg/L | Critical in DWC. Check aeration first if plants look stressed. |

**Conventional (synthetic) nutrient management:**

Use a reputable two-part or three-part base nutrient concentrate (e.g., General Hydroponics Flora series, Canna, Athena). Mix to manufacturer's EC target for crop stage. Supplement with:
- Cal-Mag if using RO water or soft water (calcium and magnesium are stripped).
- Iron chelate if pH creeps above 6.8 (iron becomes unavailable above this point).
- Silica (potassium silicate) for stem strength and disease resistance — add first, before other nutrients.

Nutrient solution management sequence: Silica → Cal-Mag → base nutrients → pH adjust.

**Biological (organic/low-input) nutrient management:**

Adding beneficial biology to the root zone changes the system's behaviour — and its resilience.

| Biological input | What it does | When to add |
|---|---|---|
| Mycorrhizal inoculant | Colonises roots; extends nutrient and water uptake area | At transplant or seeding; not compatible with high-phosphorus solutions |
| Beneficial bacteria (Bacillus, Trichoderma) | Suppress Pythium and root pathogens; fix some nitrogen | Add weekly to reservoir; compatible with most nutrients |
| Humic and fulvic acids | Chelate minerals; stimulate root development; feed bacteria | Add with each reservoir change |
| Worm castings extract | Broad-spectrum biological inoculant; plant growth hormones | Weekly foliar spray or reservoir addition |
| Fish emulsion (aquaponics crossover) | N-P-K from biological source; microbial food source | Replace or supplement synthetic base nutrient |

**Ingham lens:** A sterile nutrient solution with no biology is more vulnerable to root disease than a biologically active one. Pythium — the most common hydroponic root pathogen — thrives in exactly the warm, oxygenated, sterile conditions many growers create. Adding beneficial biology competes with and suppresses Pythium. Do not sterilise the entire system with bleach or hydrogen peroxide between crops if the goal is a biological system — sterilise, then immediately re-inoculate.

**Troubleshooting common problems:**

| Symptom | Likely cause | Check first |
|---|---|---|
| Yellow lower leaves | N deficiency or root rot | Check roots (brown = rot); check EC and pH |
| Interveinal chlorosis (yellowing between veins) | Fe, Mn, or Zn deficiency | Check pH — usually above 6.8 |
| Tip burn (lettuce) | Calcium deficiency at the leaf tip | Increase solution flow; check Cal-Mag; check EC |
| Wilting despite correct solution | Root rot (Pythium) or root zone hypoxia | Check dissolved oxygen; inspect roots |
| Stunted growth, purple tinge | P deficiency or cold root zone | Check solution temperature; check pH |
| Slimy roots, brown colour | Pythium / root rot | Check DO; add Trichoderma; reduce temperature |

**Aquaponics nutrient management:**

In an aquaponic system, fish provide the primary nutrient inputs. The key variables:

- Fish stocking density: 20–40 kg of fish per 1000L of system water is the recommended range for a balanced system. Too few fish = nutrient-deficient plants. Too many = ammonia spike, fish stress.
- Ammonia conversion: beneficial bacteria (Nitrosomonas, Nitrospira) convert ammonia → nitrite → nitrate. This nitrogen cycle must be established before fish are added to full density (cycling takes 3–6 weeks).
- pH target for aquaponics: 6.8–7.2 — a compromise between fish preference (7.0–8.0) and plant nutrient uptake (5.8–6.5). Monitor both.
- Supplement if needed: aquaponics systems often run low on iron, potassium, and calcium — add as chelated iron, potassium carbonate, and calcium carbonate as needed.

**Checkpoint — confirm before finalising:**
- Hydroponic (purchased nutrients) or aquaponic (fish-derived nutrients) — or a hybrid biological approach?
- What crop is in the system, and what growth stage? Nutrient targets shift significantly between seedling, vegetative, and fruiting stages.
- Is there an existing nutrient problem to diagnose, or are you formulating from scratch?

A nutrient plan without knowing the crop stage and system type will overfeed or underfeed — both cost yield.

**Output:**
```
NUTRIENT MANAGEMENT PLAN
System type: [hydroponic / aquaponic / biological hydroponic]
Crop: [crop]
Growth stage: [seedling / vegetative / flowering / fruiting]

TARGET PARAMETERS
EC: [mS/cm]
pH: [range]
Solution temperature: [°C]
DO: [>X mg/L]

NUTRIENT SOLUTION (per 100L)
Base nutrient A: [volume mL] ([brand/product])
Base nutrient B: [volume mL]
Cal-Mag: [volume mL]
Silica: [volume mL]
Biological additions: [product and rate]

RESERVOIR MANAGEMENT
Change frequency: [every X days]
Top-up: [with plain pH-adjusted water between changes]
Flush (if any): [protocol]

WATCH FOR
- [symptom to monitor]
- [parameter to check daily]
```

**Next steps:**
- Run **crop-selection** (within this skill) to match nutrient targets to the specific crop's needs.
- `/s4ag-composting` — if shifting toward a biological system, compost tea is the most accessible first biological input.
- `/s4ag-water` — if water quality is affecting the nutrient solution (hardness, iron, bicarbonates), address the source first.

---

## Lighting

*Decides on lighting strategy — natural light, supplemental, or full-spectrum LED — and specifies the right output for the crop.*

Light is the engine of CEA. Every other variable is secondary. A plant receiving inadequate light will not respond to optimised nutrition, perfect EC, or ideal temperature. Before troubleshooting anything else in an underperforming system, confirm that the Daily Light Integral (DLI) is correct.

**Key concepts:**

| Term | What it means | Why it matters |
|---|---|---|
| DLI (Daily Light Integral) | Total moles of photosynthetically active radiation (PAR) received per day — mol/m²/day | The single most important metric for yield prediction in CEA |
| PPFD (Photosynthetic Photon Flux Density) | Instantaneous PAR measurement — µmol/m²/s | What light meters measure; convert to DLI using: DLI = PPFD × photoperiod (hours) × 0.0036 |
| Photoperiod | Hours of light per day | Long-day crops (lettuce): 16–18h. Short-day crops (strawberry fruiting): 8–12h. |
| Spectrum | Wavelengths emitted by the light source | Blue (400–500nm): vegetative growth, compact habit. Red (600–700nm): photosynthesis efficiency, flowering. Full spectrum: closest to sunlight, most flexible. |

**DLI targets by crop:**

| Crop | Minimum DLI | Target DLI | Notes |
|---|---|---|---|
| Lettuce and leafy greens | 12 mol/m²/day | 17 mol/m²/day | Above 20 causes tip burn in sensitive varieties |
| Herbs (basil, parsley) | 12 mol/m²/day | 15–20 mol/m²/day | Basil requires high DLI for essential oil production |
| Tomatoes | 20 mol/m²/day | 25–35 mol/m²/day | High-wire cultivation requires continuous high DLI |
| Cucumbers | 18 mol/m²/day | 22–28 mol/m²/day | |
| Strawberries | 12 mol/m²/day | 15–20 mol/m²/day | |
| Microgreens | 10 mol/m²/day | 12–15 mol/m²/day | Too high causes photoinhibition in young tissue |
| Cannabis (vegetative) | 20 mol/m²/day | 25–35 mol/m²/day | |

**Lighting system options:**

| Technology | Best use case | Efficiency (µmol/J) | Notes |
|---|---|---|---|
| Greenhouse natural light | Any crop where climate allows | Free | Seasonal variation requires supplemental in winter |
| HPS (high-pressure sodium) | Large commercial, where heat is useful | 1.2–1.5 µmol/J | Proven technology; high heat output; high running cost |
| LED full-spectrum | Indoor, vertical, or supplemental | 2.0–3.5 µmol/J | Dominant choice for new installations; wide spectrum flexibility |
| LED targeted spectrum (red/blue) | High-volume leafy green production | 2.5–3.5 µmol/J | Lower cost; works for leafy greens; less flexible |
| CMH (ceramic metal halide) | Small to medium; full spectrum in one lamp | 1.8–2.2 µmol/J | Good spectrum; less efficient than modern LED |

**Calculating what you need:**

To achieve a target DLI over a given photoperiod:

Required PPFD (µmol/m²/s) = Target DLI ÷ (photoperiod hours × 0.0036)

Example: Target DLI of 17 mol/m²/day over 16-hour photoperiod:
Required PPFD = 17 ÷ (16 × 0.0036) = 295 µmol/m²/s

To find how many fixtures you need: measure (or obtain from manufacturer) the PPFD at the canopy for one fixture, then calculate area coverage at that PPFD.

**Supplemental lighting in greenhouse:**

In a greenhouse, measure outdoor DLI for your location and month using a PAR meter or DLI map. When outdoor DLI falls below crop minimum, supplement to close the gap. This is cheaper than full artificial lighting and gives natural spectrum as the base.

**DIF management (temperature-based height control):**

If plants are stretching (elongated internodes), night temperature is too high relative to day temperature. Reduce night temperature by 3–5°C below day temperature to produce compact growth without plant growth regulators. This technique (from Jensen's research) eliminates the need for chemical dwarfing agents.

**Checkpoint — confirm before finalising:**
- Is this a greenhouse (supplemental) or fully indoor (full-spectrum artificial) environment?
- What crop is in the system — and what is the current DLI at canopy level if known?
- What is the ceiling height (for vertical stacking) and the floor area to be lit?

A lighting specification without ceiling height, crop type, and current light measurement is guesswork that may result in under-lit or over-lit systems.

**Output:**
```
LIGHTING RECOMMENDATION
Environment: [greenhouse / indoor warehouse / other]
Crop: [crop]
Target DLI: [mol/m²/day]
Photoperiod: [hours/day]

REQUIRED PPFD AT CANOPY: [µmol/m²/s]

RECOMMENDED FIXTURE
Type: [LED full-spectrum / HPS / CMH / supplemental LED]
Model or specification: [wattage, efficiency rating if known]
Mounting height: [cm above canopy]
Spacing: [fixture spacing for even coverage]
Number of fixtures per [m²]: [number]

PHOTOPERIOD SCHEDULE
Lights on: [time]
Lights off: [time]
Notes: [any DIF management or dark period considerations]

ESTIMATED POWER CONSUMPTION: [kWh/day for the space]
ESTIMATED RUNNING COST: [$/month at local electricity rate if known]
```

**Next steps:**
- Run **economics** (within this skill) — lighting power is typically 40–60% of CEA operating cost; confirm it fits the financial model.
- Run **crop-selection** (within this skill) to confirm the DLI target matches the crop you are growing.
- `/s4ag-polytunnels` — if transitioning from a polytunnel, use this skill to plan supplemental lighting as a lower-cost first step.

---

## Crop Selection

*Identifies which crops make economic and agronomic sense in your CEA system.*

Not every crop belongs in a controlled environment system. The test is simple: does the value per square metre per year justify the capital and operating cost of CEA? CEA makes sense when: (a) the crop commands a premium price, (b) the outdoor growing season is too short or unreliable, or (c) the crop needs consistent quality impossible to achieve outdoors.

**The economics filter — which crops clear the bar:**

| Crop | CEA suitability | Key factor |
|---|---|---|
| Lettuce and leafy greens | Excellent | Fast turnover (21–35 days), high demand, commands freshness premium |
| Basil and fresh herbs | Excellent | High value/kg, fast cycle, difficult to store — premium for local/fresh |
| Tomatoes (premium varieties) | Good — requires fruiting system | High DLI and support systems needed; premium varieties justify cost |
| Cucumbers | Good — requires fruiting system | Similar to tomatoes; yields improve sharply with environment control |
| Strawberries | Good — off-season premium | Off-season production commands premium; requires fruiting trigger management |
| Microgreens | Excellent for small scale | Very high value/kg; short cycle; suited to small indoor spaces |
| Cannabis / medical plants | Excellent (where legal) | Extremely high value/m²; regulation-intensive |
| Root vegetables (carrot, beet) | Poor | Long cycle; low value/m²; better in soil |
| Grain crops | Do not grow | Economics do not work at any scale |
| Legumes (beans, peas) | Poor | Require a lot of space for yield; better outdoors |

**Decision matrix — comparing crops for your system:**

For each candidate crop, estimate:

1. Yield per m² per year (kg)
2. Price per kg (your market)
3. Revenue per m² per year = (1) × (2)
4. Compare against estimated operating cost per m² per year (from economics sub-tool)

If revenue per m² < operating cost per m²: do not grow that crop in this system.

**Variety selection within chosen crops:**

| Crop | Preferred CEA varieties | Notes |
|---|---|---|
| Lettuce | Butterhead (e.g., Buttercrunch, Rex), oakleaf, loose-leaf types | Avoid iceberg in CEA — slow, space-intensive |
| Basil | Genovese types (DWS Eleonora, Italian Large Leaf); Thai basil for diversity | Sweet Thai has higher essential oil at high DLI |
| Tomato | Cocktail and cherry types (Sakura, Suncherry); beefsteak needs very high DLI | Indeterminate, high-wire varieties for commercial |
| Cucumber | Mini/snacking types (Katrina, Nimrod); long English for premium market | Need trellis in any system |
| Strawberry | Day-neutral varieties (Albion, Seascape, Portola) for year-round production | Ever-bearing day-neutral types for continuous harvest |
| Microgreens | Sunflower, peas, radish (fast, high demand); amaranth, mustard (flavour premium) | Diversify mix to reduce single-crop market risk |

**Crop cycling for year-round production:**

In a CEA system with continuous harvest targets, stagger plantings to harvest weekly:
- Divide total growing area into equal sections (e.g., 4 sections).
- Plant one section each week (for a 4-week cycle crop like lettuce).
- Harvest, clean, and replant one section weekly on rotation.
- Result: continuous weekly harvest from a fixed space.

**Checkpoint — confirm before finalising:**
- What is your target market and current price for each candidate crop? A crop that commands a premium in one market may be commoditised in another.
- What system have you chosen (from system-selection)? The system constrains which crops are agronomically feasible.
- Are you growing for household use, local direct sale, restaurant wholesale, or retail — and does that market have a preference for specific varieties?

A crop selection without knowing the price point and the market is incomplete — the economics test cannot be run without market data.

**Output:**
```
CROP SELECTION RECOMMENDATION
System: [system type]
Market: [household / direct / restaurant / retail]

SELECTED CROPS (ranked by value per m²)
1. [Crop] — [variety] — [yield/m²/year kg] × [$X/kg] = [$Y/m²/year]
2. [Crop] — [variety] — [yield/m²/year kg] × [$X/kg] = [$Y/m²/year]
3. [if applicable]

CROPS ASSESSED AND REJECTED
[Crop] — reason: [economics / agronomic mismatch / market not available]

HARVEST SCHEDULE (for continuous production)
Section 1: Plant [date] → Harvest [date]
Section 2: Plant [date + interval] → Harvest [date]
[repeat for all sections]

VARIETY NOTES
[any specific variety guidance for top-ranked crops]
```

**Next steps:**
- Run **economics** (within this skill) to model the revenue against the full cost of the system.
- Run **nutrient-management** (within this skill) to set crop-specific nutrient targets.
- `/s4ag-market` — before committing to a crop mix, verify the local market will absorb the volume at the price needed.

---

## Economics

*Calculates whether a CEA investment makes financial sense — before you spend money, or to diagnose why a current system is underperforming.*

CEA has high capital costs and high operating costs. The only farms that sustain profitability are those that understand the numbers precisely before building. This sub-tool works through the economic model in full.

**Capital cost components (estimate before committing):**

| Component | Cost range (small commercial — 100m²) | Notes |
|---|---|---|
| Structure (greenhouse or warehouse fit-out) | $15,000–$80,000 | Existing structure dramatically reduces this |
| Growing system (NFT channels, DWC raft, Dutch buckets) | $5,000–$25,000 | NFT is lowest; Dutch bucket with drip highest |
| Lighting (if indoor or supplemental) | $8,000–$40,000 | LED full-spectrum at 100m² — highly variable by intensity |
| Irrigation and dosing | $2,000–$10,000 | Basic manual vs. automated dosing systems |
| Climate control (HVAC, fans, CO2) | $3,000–$20,000 | Critical for humid environments; CO2 adds yield in sealed spaces |
| Water filtration / RO | $1,000–$5,000 | If using well or poor-quality mains water |
| Monitoring and automation | $500–$5,000 | EC/pH controllers, environmental sensors |
| **Total estimated capital (100m²)** | **$35,000–$180,000** | Wide range — get supplier quotes for your specific design |

**Operating cost components (annual, 100m² system):**

| Cost item | Annual range | Notes |
|---|---|---|
| Electricity | $6,000–$20,000 | Largest variable — depends on lighting intensity and climate control |
| Nutrients / inputs | $1,500–$5,000 | Biological systems reduce this significantly after establishment |
| Labour | $15,000–$40,000 | Most underestimated cost; skilled CEA labour is not cheap |
| Packaging and delivery | $2,000–$8,000 | Depends heavily on volume and market channel |
| Maintenance, repairs, consumables | $1,000–$3,000 | Pumps, growing media replacement, monitoring equipment |
| **Total estimated operating cost (100m²)** | **$25,500–$76,000/year** | |

**Revenue model:**

| Crop | Yield (100m², year-round) | Price target | Annual revenue |
|---|---|---|---|
| Lettuce (butterhead) | 4,000–6,000 heads | $3–$5/head | $12,000–$30,000 |
| Basil | 500–800 kg | $12–$25/kg | $6,000–$20,000 |
| Cherry tomatoes | 8,000–15,000 kg | $4–$8/kg | $32,000–$120,000 |
| Microgreens | 300–600 kg | $25–$60/kg | $7,500–$36,000 |
| Mixed greens (aquaponics + fish) | 2,000–4,000 kg greens + 300–600 kg fish | $8–$15/kg greens; $10–$20/kg fish | $22,000–$72,000 combined |

**Profitability threshold calculation:**

Break-even revenue = Annual operating cost + (Capital cost ÷ payback period in years)

Example (100m² lettuce system, 5-year payback):
- Capital cost: $80,000 ÷ 5 = $16,000/year
- Operating cost: $40,000/year
- Break-even revenue needed: $56,000/year
- At $4/head, 14,000 heads/year needed from 100m²
- DWC lettuce yields ~4,000–6,000 heads/100m²/year → gap is clear

Implication: at 100m² with lettuce at $4/head, the economics are marginal. Premium varieties at $6–$8/head, or a higher-value crop, are necessary for profitability at small scale.

**When CEA makes economic sense:**

- High-value crops ($20+/kg equivalent) in markets with reliable demand.
- Off-season production where outdoor alternatives are absent and prices spike.
- Very small footprint with very high output — microgreens at 50m² can work.
- Integration with existing enterprise where waste heat (from composting, livestock, industrial process) offsets energy cost.
- Urban or peri-urban location where freshness commands a 30–50% premium over shipped produce.

**When CEA does not make economic sense:**

- Trying to compete on commodity crops (lettuce at $1.50/head) against field production.
- Electricity costs above $0.15/kWh without access to cheap renewables.
- Scaling too fast before the system and the market are proven at small scale.
- Building for community food security without a cost-covering funding model.

**Transition note:** Start with the smallest system that can validate the market, then expand from cash flow rather than capital. Many failed CEA businesses built the full system before they had a single customer.

**Checkpoint — confirm before finalising:**
- What is the local electricity price per kWh? This is the most variable and sensitive input in the whole model.
- What is the confirmed market price for the target crop in this location — not an aspirational price, an actual buyer offering that price?
- Is this a new build, or an existing space being converted? Existing structure can halve capital costs.

Economics modelled on optimistic assumptions justify any project. Use actual quotes and actual buyer commitments.

**Output:**
```
CEA ECONOMIC ANALYSIS
System: [system type]
Scale: [m²]
Primary crop: [crop]

CAPITAL COST
Structure / fit-out: $[X]
Growing system: $[X]
Lighting: $[X]
Climate control: $[X]
Other: $[X]
TOTAL CAPITAL: $[X]

ANNUAL OPERATING COST
Electricity: $[X]
Nutrients and inputs: $[X]
Labour: $[X]
Other: $[X]
TOTAL OPERATING COST: $[X/year]

REVENUE PROJECTION
Yield: [kg or units/year]
Price: $[X per unit]
ANNUAL REVENUE: $[X]

GROSS MARGIN: $[Revenue - Operating cost] ([%])
PAYBACK PERIOD: [years on current projection]
BREAK-EVEN PRICE: $[X per unit] (if revenue projection is uncertain)

RISK FACTORS
- [biggest cost uncertainty]
- [market assumption that needs validation]

RECOMMENDATION: [viable at this scale / marginal — needs X to work / not viable — here's why]
```

**Next steps:**
- Run **crop-selection** (within this skill) to test whether a different crop mix improves the economics.
- `/s4ag-finance` — once the CEA model is viable, build a full farm financial plan including this enterprise.
- `/s4ag-market` — the revenue model depends on confirmed pricing; verify buyer commitments before finalising.
