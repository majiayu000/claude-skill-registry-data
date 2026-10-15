---
name: s4ag-water
description: "Water decisions for farms — irrigation system selection, when and how much to irrigate, drought resilience, drainage problems, water harvesting, and water quality. Use when the user says anything like 'my soil is too wet', 'I need to irrigate', 'we had a dry summer', 'drainage is poor', or 'how do I collect rainwater'."
allowed-tools: [Read]
---

# Water

Water management is a biological problem as much as an infrastructure problem. Before investing in hardware — pipes, pumps, tiles, tanks — ask whether the soil biology is working. A healthy food web builds aggregate structure that infiltrates water faster, and organic matter that holds it longer. In many cases, building soil OM by 1–2% solves an irrigation problem more cheaply than installing a new drip system. Start with the biology, then invest in infrastructure for what biology cannot fix.

**How this skill works:** Each sub-tool pauses at a **Checkpoint** to confirm the assumptions it is about to build on before producing output. A recommendation built on a wrong assumption wastes time and money — confirm the checkpoint before acting. Each sub-tool ends with **Next steps** — the skills worth running once you have acted on this one.

---

## Expert Lineage

*The thinkers whose frameworks underpin this skill — and what they specifically discovered that changes how you farm.*

**P.A. Yeomans — Keyline Design**
Yeomans spent thirty years on his New South Wales properties developing a systematic method for reading how water moves across any landscape. His core finding: water in an agricultural landscape defaults to the lowest point and exits the farm. The Keyline system redistributes water laterally across the slope, saturating the landscape rather than draining it. His specific tool — the keyline point, located just below the valley floor where slope transitions — allows a farmer to design water distribution across an entire property from a single correctly placed line. Before spending money on any water storage or irrigation infrastructure, map how water actually moves on the property.

**Brad Lancaster — Rainwater Harvesting for Drylands**
Lancaster demonstrated in Tucson, Arizona that a household and small farm could meet most of its water needs from rainfall alone through systematic earthwork and vegetation design — in a place that receives less than 300mm annually. His specific contribution: every drop of rain that falls on the property should be considered a resource to capture before it becomes runoff. The sequence he established — slow it, spread it, sink it, store it, use it — applies equally to farm-scale water management. The least expensive water is rain you keep on your land.

**Gary Zimmer — Biological Farmer**
Zimmer connected soil biology directly to farm water economics in quantifiable terms. His specific finding: every 1% increase in soil organic matter adds approximately 170,000 litres of plant-available water per hectare. In practical terms, a farm at 1% OM irrigating 50mm per week can, at 3% OM, irrigate 30mm per week for the same crop response. The soil improvement pays the irrigation bill. Before adding infrastructure, build the water-holding capacity in the soil.

**Judith Schwartz — Water in Plain Sight**
Schwartz documented the farm-scale connection between land management and water cycle function. Her key finding: degraded landscapes with bare soil, compacted ground, and absent perennial vegetation are net exporters of water — rainfall runs off rather than infiltrating. Farms that restore ground cover and soil biology become net importers of water — rainfall infiltrates, recharges groundwater, and supports plant growth through dry periods. The direction of the water cycle on your farm is determined by your management decisions.

**Elaine Ingham — Soil Food Web and Water**
Ingham's structural finding: fungal hyphae and bacterial biofilms physically bind soil particles into aggregates — the macro-pores between those aggregates are the channels through which water infiltrates and air circulates. A degraded, low-biology soil collapses its aggregate structure and becomes compacted and impermeable. Restoring the food web physically rebuilds infiltration capacity. Fungicide application — even at labelled rates — measurably reduces fungal hyphal length in soil, directly reducing aggregate stability and therefore water infiltration.

---

## Which tool fits

| You need to... | Tool |
|---|---|
| Choose between irrigation system types | irrigation-selection |
| Know when and how much to irrigate | irrigation-scheduling |
| Prepare for or manage drought conditions | drought-planning |
| Fix a drainage problem | drainage |
| Collect and store rainwater on the farm | water-harvesting |
| Test water or address water quality concerns | water-quality |

## Routing Decision

- **Building or replacing an irrigation system** → irrigation-selection
- **System exists, unsure when to run it or how long** → irrigation-scheduling
- **Facing a dry season or want to drought-proof the farm** → drought-planning
- **Fields stay wet too long after rain, poor crop establishment** → drainage
- **Want to capture rainfall and reduce dependency on bore or mains** → water-harvesting
- **Using water from a dam, bore, or river and unsure if it's safe** → water-quality
- **Unclear** → start with irrigation-selection to establish system context, then routing becomes obvious

---

## Irrigation Selection

*Matches an irrigation system type to the crop, soil, and site conditions.*

The right irrigation system is the one that puts water where roots are, when roots need it, without wetting foliage or compacting soil. Each system type has a different cost profile, labour demand, and water efficiency. The table below allows a direct comparison; the decision sequence follows.

**System comparison:**

| System | Water efficiency | Capital cost | Labour | Best for | Avoid when |
|---|---|---|---|---|---|
| Drip (subsurface) | Very high | High | Low | Vegetables, perennials, orchards | Rocky soils; heavy clay that blocks emitters |
| Drip (surface tape) | High | Medium | Medium | Row vegetables, annual crops | Rodent pressure; perennial plantings |
| Overhead sprinkler | Medium | Medium | Low-medium | Pasture, establishing cover crops, frost protection | Foliar disease-prone crops; windy sites |
| Micro-spray / wobbler | Medium-high | Medium | Low | Orchards, wide-row perennials | High-pressure systems without filtration |
| Flood / border | Low | Low | High | Pasture, rice; only where water is abundant | Water-scarce conditions; soils with poor infiltration |
| Hand-held / manual | Low | Very low | Very high | Small beds, nursery, establishment watering | Any scale beyond a home garden |

**Decision sequence:**

1. **Identify the crop type.** Vegetables and row crops: drip is usually correct. Orchards and perennial systems: micro-spray or subsurface drip. Pasture: overhead or flood where water is available. Mixed systems: zone the property by crop type and match systems per zone.

2. **Assess the soil.** Heavy clay: slow infiltration rate means slow application rates prevent runoff — drip or micro-spray. Sandy soils: water moves fast and deep — subsurface drip or frequent short overhead cycles. Loam: most systems work.

3. **Assess water source and pressure.** Town/mains pressure: any system. Gravity-fed dam or tank: check head pressure before selecting — drip requires minimum 1 bar. Bore or pump-fed: calculate flow rate and match system to available volume.

4. **Consider the food web.** Overhead irrigation wets foliage and can suppress foliar fungi (a secondary benefit in some diseases, a problem in others). More critically, flood and overhead irrigation can compact soil surface under heavy application — soil aggregate destruction reduces future infiltration. Drip irrigation preserves surface aggregates and concentrates biological activity around emitter zones.

**Transition note:** Moving from flood to drip irrigation is the most impactful single water-saving change on most vegetable and orchard operations. The capital cost can be recovered in water savings in 2–5 years in water-scarce regions.

**Checkpoint — confirm before finalising:**
- What crop or enterprise is this system serving? The crop type determines the system type.
- What is the water source — mains, bore, dam, river — and what is the pressure and flow rate available?
- Is organic certification a consideration? Some emitter cleaning chemicals are not permitted.

Recommending a drip system without confirming available pressure, or an overhead system on a disease-prone vegetable crop, creates an expensive problem.

**Output:**
```
IRRIGATION SYSTEM RECOMMENDATION

Farm context: [crop type / enterprise]
Water source: [source, pressure, flow rate]
Soil type: [soil]

RECOMMENDED SYSTEM: [system type]
  Configuration: [layout description — drip tape spacing, sprinkler spacing, etc.]
  Filtration required: [yes/no — type]
  Approximate capital cost range: [low/medium/high, or $/ha estimate]
  Labour requirement: [hours/week during irrigation season]

ALTERNATIVE IF BUDGET IS CONSTRAINED: [alternative system]

WHAT TO AVOID: [system type and reason]

NEXT DESIGN STEP: [what to measure or confirm before purchasing]
```

**Next steps:**
- Run **irrigation-scheduling** (within this skill) to set run times and frequency for the selected system.
- `/s4ag-soil` — improving OM before installing irrigation reduces the system capacity needed.
- `/s4ag-earthworks` — if the site has water storage potential, design catchment before finalising supply infrastructure.

---

## Irrigation Scheduling

*Determines when to irrigate and how much to apply — without over- or under-watering.*

Over-irrigation is at least as common as under-irrigation on most farms. Saturated soil drives out oxygen, anaerobic conditions kill aerobic biology, and roots suffocate. Under-irrigation creates crop stress at critical growth stages and reduces yield. The goal is to keep soil moisture in the range roots can access — typically field capacity to around 50% plant-available water depleted.

**Reading soil moisture — three methods in order of cost:**

**1. Feel and look test (free).**
Take a soil sample from root zone depth. Squeeze a handful.
- Leaves wet hands, ribbon easily: at or above field capacity. Do not irrigate.
- Forms a ribbon but does not wet hands: in range. Irrigate only if forecast is dry.
- Falls apart, does not ribbon, dusty: below 50% depletion. Irrigate now.

**2. Tensiometer or gypsum block (low cost).**
Install at root zone depth (typically 20–30cm for vegetables, 40–60cm for perennials). Read daily.
- Tensiometer 0–10 kPa: field capacity — too wet to irrigate.
- 10–30 kPa: ideal range for most crops. Irrigate when approaching upper end.
- 30–60 kPa: drying out — irrigate now for most vegetables; some deficit irrigation crops (olives, grapes) can go to 60–80 kPa.
- Above 60 kPa: stress zone. Irrigate immediately for most crops.

**3. Evapotranspiration (ET) scheduling (moderate cost).**
Use local weather station ET data (many irrigation authorities publish this). Replace the previous day's ET minus any effective rainfall.
- Typical summer ET: 4–8mm/day depending on temperature, humidity, and wind.
- Effective rainfall: rain events above 5mm count; below 5mm, assume most evaporates before infiltrating.

**Crop-specific adjustments:**

| Crop stage | Water demand relative to ET |
|---|---|
| Germination / establishment | High — keep surface moist until established |
| Vegetative growth | 70–90% ET replacement |
| Flowering / fruit set | 100% ET replacement — most critical period |
| Fruit fill | 80–100% ET |
| Ripening / harvest | 60–70% ET — some deficit increases Brix in many fruits |
| Cover crop / fallow | 0% — rely on rainfall |

**Food web note:** Soil biology requires air as well as water. The pore spaces in well-aggregated soil hold both — but if soil is irrigated past field capacity and held saturated, aerobic bacteria and fungi die and anaerobic bacteria dominate. Schedule irrigation to allow the soil to breathe between events. The 24–48 hours of drying between irrigations is not wasted time — it is oxygen replacement that the food web needs.

**Checkpoint — confirm before finalising:**
- What crop and growth stage are we scheduling for? Demand varies by stage.
- What is the soil type? Sandy soils need more frequent, shorter runs; clay needs longer intervals and slower application.
- Is there a functioning soil moisture monitoring tool in place, or are we relying on visual assessment?

Scheduling without knowing growth stage or soil type produces a number that may be correct or dangerously wrong.

**Output:**
```
IRRIGATION SCHEDULE

Crop: [crop name]
Growth stage: [stage]
Soil type: [soil]
System type: [drip / overhead / other]

CURRENT SOIL MOISTURE: [reading or assessed status]

IRRIGATION EVENT
  Frequency: [every X days]
  Run time: [minutes/hours]
  Volume per event: [mm or litres/m2]
  Best time of day: [morning recommended to reduce evaporation and foliar disease]

ET REPLACEMENT TARGET: [mm/day]
  Effective rainfall this week: [mm]
  Irrigation required this week: [mm]

NEXT SOIL MOISTURE CHECK: [date]

SIGNS TO WATCH FOR
  Under-watering: [crop indicator]
  Over-watering: [crop indicator]
```

**Next steps:**
- Run **drought-planning** (within this skill) if the season ahead is forecast dry and the schedule needs to become a rationing plan.
- `/s4ag-soil` — building OM reduces the volume and frequency of irrigation required.
- `/s4ag-vegetables` or `/s4ag-orchards` — crop-specific water demand at each growth stage.

---

## Drought Planning

*Builds drought resilience before dry conditions arrive, and manages water rationing once they do.*

Drought planning has two phases: preparation (before the dry season or dry period begins) and rationing (once soil moisture is depleted and supply is constrained). These require different actions. Preparation is about soil and system; rationing is about prioritisation and loss minimisation.

**Phase 1: Preparation — do these before the dry season.**

**1. Increase soil water-holding capacity.**
Every 1% of soil OM holds approximately 170,000 litres/ha of additional plant-available water. A farm at 1% OM and a farm at 3% OM receive the same rainfall but the 3% OM farm has twice the buffer to draw on. Increasing OM is the most cost-effective drought-proofing investment available — cheaper than any tank or bore deepening.

Actions to increase OM: compost additions (3–5 t/ha/year moves OM measurably over 3–5 years), permanent cover crops in fallow periods, reduced tillage (every tillage event oxidises OM), and deep-rooted species that add OM at depth.

**2. Mulch exposed soil.**
Bare soil loses water to evaporation at a rate of 3–6mm/day in summer. A 10cm organic mulch layer reduces this to 0.5–1mm/day. For market gardens and orchards, mulching between rows is the fastest way to reduce irrigation demand. Suitable mulches: wood chips (feeds fungal food web), straw, compost, living mulch (low-growing cover crop between rows).

**3. Shade the soil surface.**
High plant canopy cover reduces soil temperature, which reduces evaporation. In vegetable systems, close plant spacing and tall neighbours reduce exposed soil. In orchard and perennial systems, understorey plantings serve the same function and build food web biology.

**4. Improve catchment efficiency.**
Check that every rainfall event is being captured and infiltrating. Clear any areas of compaction that cause runoff. Install or improve water harvesting infrastructure before the dry season (→ run **water-harvesting** sub-tool). Fill storage capacity before the dry season begins — do not wait.

**5. Know your minimum viable water needs.**
List enterprises by water demand and decide in advance which ones get priority if supply is constrained. This decision is emotionally difficult in crisis — make it now.

**Phase 2: Rationing — during drought conditions.**

**Prioritise by enterprise and growth stage:**

| Priority | Enterprise / stage | Rationale |
|---|---|---|
| 1 | Perennials at fruit set or fruit fill | Loss at this stage is permanent yield loss |
| 2 | Transplanted annuals in establishment | Stress now means poor season; transplant investment wasted |
| 3 | Perennials in vegetative growth | Can tolerate mild stress; recovery is fast |
| 4 | Direct-sown annuals | Delay sowing until rain; do not establish into drought |
| 5 | Pasture and cover crops | Allow dormancy rather than irrigate — grasses recover |
| Last | Standing cover crops / green manures | Allow to die back and mulch — they add OM in death |

**Deficit irrigation:**
Once in rationing mode, apply 60–70% of ET replacement rather than 100%. Most crops can tolerate 30–40% deficit without significant yield loss if it is imposed consistently rather than allowing boom-bust soil moisture cycles. Boom-bust is more stressful to both plants and soil biology than consistent mild deficit.

**Food web note:** Dry soil slows biological activity, but does not kill it — most bacteria and fungi can survive extended dry periods in spore or dormant form. The critical mistake during drought is irrigating enough to activate biology but not enough to sustain it — repeated wetting and drying cycles do more biological damage than sustained dryness. If rationing, wet deeply and infrequently rather than lightly and frequently.

**Checkpoint — confirm before finalising:**
- Are we in preparation mode (dry season approaching) or rationing mode (drought underway)?
- What is the current water supply volume — how many days of irrigation remain at current use rates?
- Which enterprises cannot survive drought without irrigation? Which can be sacrificed or put into dormancy?

Mixing preparation and rationing advice without knowing which phase applies produces confusing output.

**Output:**
```
DROUGHT PLAN

Phase: [PREPARATION / RATIONING]
Current water supply estimate: [days remaining at current use rate]

IMMEDIATE ACTIONS (this week)
1. [action]
2. [action]
3. [action]

PRIORITY WATER ALLOCATION
[Enterprise 1]: [volume/frequency] — [rationale]
[Enterprise 2]: [volume/frequency] — [rationale]
[Enterprise 3]: hold — allow to dry down

SOIL WATER-HOLDING CAPACITY IMPROVEMENT
Target OM: [current %] → [target %]
Actions: [compost rate / mulch plan / cover crop plan]
Timeline: [seasons to reach target]

INFRASTRUCTURE TO INSTALL BEFORE NEXT DRY SEASON
- [action]
- [action]
```

**Next steps:**
- Run **water-harvesting** (within this skill) to maximise capture of any rainfall that does occur.
- `/s4ag-soil` — the OM-building plan is the long-term drought-proofing plan.
- `/s4ag-climate-adaptation` — drought is one element of broader climate risk; plan the full exposure.

---

## Drainage

*Diagnoses drainage problems and identifies the right fix for each type.*

Poor drainage is not always a water problem — it is usually a soil structure problem, a compaction problem, or a landscape water management problem. Before installing tile drains or cutting ditches, identify the cause. Structural drainage problems solved with infrastructure keep the infrastructure bill coming every decade; structural drainage problems solved at the source stay fixed.

**Step 1: Identify the drainage problem type.**

Observe the field during and after a significant rainfall event. Where does water pond? How long does it stay? Does it pond at the surface or does water rise from below?

| Observation | Likely cause |
|---|---|
| Water ponds in tyre tracks and wheel lines | Compaction — surface or tillage pan |
| Water ponds uniformly across the field | Low permeability subsoil or impermeable clay layer |
| Water rises from below after rain | High water table — landscape drainage issue |
| Water runs off the surface without soaking in | Surface compaction or hydrophobic soil |
| Water ponds at one low spot | Landscape topography — needs redirecting |
| Fields drain slowly but eventually clear | Moderate compaction or clay subsoil — manageable |

**Step 2: Match remedy to cause.**

**Surface compaction / hydrophobic soil:**
- Immediate: aerate with tines or chisel plow (only when dry).
- Biological: deep-rooted cover crops (daikon, chicory, deep ryegrass) break surface compaction over 1–2 seasons.
- Long-term: increase OM — every improvement in aggregate structure improves infiltration rate. Avoid working wet soil.

**Tillage pan:**
- Mechanical: one-time subsoiling or ripping at the depth of the pan (confirm depth with penetrometer first; 25–35cm is typical). Only when soil is dry enough to fracture, not smear.
- Biological: daikon radish or tillage turnip species penetrate 40–60cm; as they decompose, they leave channels that persist.
- Long-term: change tillage depth annually so the pan is not re-created at the same depth.

**High clay content / low permeability subsoil:**
- Surface drainage: grade or reshape surface to remove ponded water laterally to a drain or outlet before it infiltrates (for fields where the problem is severity of ponding, not total drainage).
- Tile drainage: perforated pipe installed at 0.8–1.2m depth, spaced 10–20m apart, outlets to a drain. Effective but expensive — $1,500–$4,000/ha depending on spacing and depth.
- Biological drainage: deep-rooted species do not crack clay as hard materials do, but continuous root channels plus increasing OM progressively improves clay structure over 3–7 years. Slower but free.

**High water table:**
- Open drains: cut to below the water table and maintain continuously. Low capital, high maintenance.
- Raised beds: raise the growing zone above the water table. Practical for vegetables; less so for broadacre.
- Mole drainage: through clay subsoils, a mole plough creates unlined channels at depth — lower cost than tile but shorter-lived (5–10 years).

**Food web lens:** Waterlogged soils are anaerobic. Anaerobic conditions kill aerobic bacteria and fungi — the organisms responsible for nutrient cycling, aggregate structure, and plant health. Every week of waterlogging is a week of food web depletion. Draining fields quickly after rain events is not just a crop establishment issue — it is a biological management issue. Prioritise solutions that remove water quickly and allow soil to re-aerate.

**Checkpoint — confirm before finalising:**
- Is the problem surface, shallow (tillage pan), or deep (water table / subsoil)? Each requires a different tool.
- Is the soil currently wet or dry? No mechanical drainage work should be done on saturated soil.
- What is the budget — infrastructure (tile drainage) or biological/long-term improvement?

Recommending tile drainage for a surface compaction problem, or biological drainage for a high water table, misallocates the investment.

**Output:**
```
DRAINAGE DIAGNOSIS

Problem type: [surface compaction / tillage pan / clay subsoil / high water table / topographic]
Evidence: [observation]

RECOMMENDED REMEDY
  Immediate action: [what to do this season]
  Medium-term action: [1-3 seasons]
  Long-term action: [biological — OM building, cover crops]

WHAT TO AVOID: [e.g., "do not subsoil on wet soil", "do not install tile before addressing compaction"]

COST ESTIMATE: [low/medium/high — or rough $/ha if tile drainage recommended]

INDICATORS OF IMPROVEMENT
- [what to observe to confirm the remedy is working]
```

**Next steps:**
- `/s4ag-soil` — compaction and low OM are the root cause of most drainage problems; fix the biology.
- `/s4ag-earthworks` — if landscape water movement is the issue, earthwork design solves it at source.
- Run **drought-planning** (within this skill) — farms that fix drainage often discover they also need to store the water they were losing.

---

## Water Harvesting

*Identifies and implements simple water collection and storage options matched to the farm context.*

Water harvesting means capturing rainfall where it falls and holding it on the property as long as possible before it exits as runoff or evaporation. Every farm has some harvesting opportunity — the question is which approach fits the landscape, the scale, and the budget.

**The harvesting hierarchy — cheapest first:**

**1. Soil infiltration (free).**
The most effective water harvesting is soil that absorbs and holds rainfall rather than shedding it. A compacted, low-OM soil sheds 80–90% of rainfall as runoff. A well-structured 4–5% OM soil absorbs and holds most of it. Before any infrastructure investment, ask: is the soil capable of receiving and holding the rain that falls on it?

Actions: address compaction (→ **drainage** sub-tool), build OM (→ `/s4ag-soil`), install permanent ground cover.

**2. On-contour earthworks — swales and berms (low-medium capital).**
A swale is a level trench cut along a contour, with the excavated soil forming a berm on the downslope side. Water flowing down the slope fills the swale and infiltrates slowly rather than running to the lowest point and off the property. Swales do not drain — they pool and sink. Do not install swales where the water table is already high.

Design rules: the swale must be level (not draining) — use an A-frame or laser level. Overflow spillway must be designed to handle the maximum rainfall event. Plant the berm immediately with deep-rooted species to stabilise it.

**3. Roof and hardstand catchment — tanks and cisterns (medium capital).**
Every 100m2 of roof area yields approximately 1,000 litres per 10mm of rainfall. For a 200m2 shed roof: 2,000 litres per 10mm. Calculate the catchment area, multiply by annual rainfall, and that is the theoretical yield. Practical yield is 70–85% after accounting for the first-flush effect and evaporation losses.

Storage sizing: calculate the longest annual dry period (months without reliable rain), multiply by daily water demand, and size the tank to bridge that gap. For domestic or stock use, this is typically 10,000–50,000 litres. For irrigation supplementation, storage requirements are much larger and the economics need separate analysis.

**4. Farm dams and ponds (high capital, long life).**
A dam or pond stores surface runoff from a defined catchment area. Sizing rule of thumb: 10:1 catchment-to-storage ratio in 500mm rainfall regions; 20:1 in 300mm regions. Dams require engineering assessment, often regulatory approval, and significant capital. Their advantage is volume — a well-sited dam is the most cost-effective large-volume water storage on most farms.

Siting priorities: locate at the head of a drainage line to capture the maximum catchment area; locate where the dam wall is short relative to the volume stored (check the ratio of wall length to storage volume); locate on impermeable geology or clay soils to minimise seepage.

**5. Integrated catchment design.**
Advanced water harvesting integrates all of the above: soil infiltration captures small events; swales slow medium events; dams capture large events; tanks store roof water for domestic use. Yeomans' keyline design is the systematic approach to integrating all five elements across a whole property.

**Food web connection:** Water harvesting that emphasises soil infiltration rather than surface storage also feeds the food web. Water moving through well-structured soil — rather than across the surface and into a dam — carries oxygen, distributes dissolved organic matter, and maintains the moisture levels at which bacteria and fungi are most active. A farm designed to infiltrate rainfall is a farm designed for biological activity.

**Checkpoint — confirm before finalising:**
- What is the primary water use that this harvesting is meant to supply — irrigation, stock water, domestic, or drought buffer?
- What is the annual rainfall and what is the dry season duration? This determines storage volume requirements.
- Is there a slope gradient suitable for contour earthworks, or is the land flat? Flat land cannot use swales.

Recommending swales on flat land, or sizing a tank for irrigation supplementation without knowing the scale of the irrigation system, produces an unusable plan.

**Output:**
```
WATER HARVESTING PLAN

Annual rainfall: [mm]
Dry season: [months]
Primary use: [irrigation / stock / domestic / buffer]

RECOMMENDED APPROACH
  Stage 1 (this season): [action — lowest cost, highest return]
  Stage 2 (next season): [action]
  Stage 3 (as capital allows): [action]

CATCHMENT CALCULATION (if tank/dam)
  Catchment area: [m2]
  Annual theoretical yield: [litres]
  Storage volume recommended: [litres]

EARTHWORKS NOTE: [swales applicable or not — reason]

APPROVALS REQUIRED: [yes/no — check local regulations for dams over [threshold]]

ESTIMATED COST RANGE
  Stage 1: [$ estimate]
  Stage 2: [$ estimate]
```

**Next steps:**
- `/s4ag-earthworks` — swale and dam design requires earthworks planning for safe execution.
- Run **drought-planning** (within this skill) — water harvesting is most valuable in context of a drought resilience plan.
- `/s4ag-land-reading` — reading the landscape water patterns before designing catchment infrastructure.

---

## Water Quality

*Assesses water quality for irrigation or stock use and identifies treatment options.*

Water quality matters for three reasons: plant health (some contaminants inhibit growth or accumulate in produce), soil biology (chlorine, high salinity, and some minerals damage the food web when applied through irrigation), and human and animal health (microbial contamination and nitrates). The first question before using any water source for irrigation is: what is in it?

**When to test:**
- New water source (dam, bore, river, recycled water) before first use.
- Existing source if crop health has declined without other explanation.
- After any event that could contaminate the source (flood, upstream land-use change, chemical spill).
- Annually for bores and dams used for drinking water or food crop irrigation.

**What to test for:**

| Parameter | Why it matters | Action threshold |
|---|---|---|
| pH | Low pH (<5.5) can damage roots and equipment; high pH (>8.0) can lock out nutrients | Target 6.5–7.5 for irrigation |
| EC (electrical conductivity) | Proxy for total dissolved salts; high EC reduces osmotic water availability to plants | Below 1.5 dS/m for most crops; below 0.8 dS/m for salt-sensitive crops |
| Sodium adsorption ratio (SAR) | High-Na water destroys clay soil structure | Below 6 for most soils |
| Bicarbonate | High bicarbonate raises soil pH over time | Below 2 meq/L — treat with acid injection if above |
| Chlorine | Town water chlorine kills soil biology | Above 1 ppm — off-gas for 24 hours before use or use carbon filter |
| Nitrate | High nitrate in bore water can indicate contamination | Irrigation: generally fine; drinking: above 10 mg/L is unsafe |
| Iron / manganese | Blocks drip emitters; can cause foliar symptoms | Iron above 0.2 ppm — filter before drip systems |
| E. coli / coliforms | Human health risk in any water used on edible crops | Zero tolerance for produce that contacts water |
| Heavy metals | Accumulate in soil over time; contaminate produce | Requires specific testing if industrial land use upstream |

**Chlorine and the food web:** Town water delivered through mains is chlorinated to prevent human pathogen growth. Applied directly to soil through irrigation, chlorine kills aerobic soil bacteria and fungi at and around the emitter zone — every irrigation event is a biological suppression event. If using town water for irrigation, either off-gas it (hold in an open tank for 24 hours), use a carbon filter on the line, or apply water to the soil surface rather than injecting into the rhizosphere.

**Common treatment options:**

| Problem | Treatment |
|---|---|
| High pH | Acidify with citric acid, acetic acid, or sulphuric acid — inject at the header |
| Low pH | Raise with potassium bicarbonate or calcium carbonate — test carefully |
| High EC / salinity | Blend with lower-EC source; improve soil drainage to leach salts; switch to more salt-tolerant varieties |
| High SAR | Apply gypsum (calcium sulphate) to soil — displaces sodium and improves structure |
| Chlorine | Off-gas tank; carbon inline filter |
| Iron / manganese | Sediment filter + oxidising filter; aeration tank |
| Microbial contamination | UV sterilisation; chlorination; do not use untreated for direct produce contact |
| High bicarbonate | Acid injection at header; monitor soil pH annually |

**Checkpoint — confirm before finalising:**
- Do you have a water test result, or are we identifying what to test for? These require different outputs.
- What is the water being used for — food crop irrigation (direct contact), stock water, pasture irrigation, or domestic use? Risk thresholds differ significantly by use.
- Is this bore, dam, river, or mains water? Source determines which contaminants are most likely.

Recommending treatment without a test result, or applying food-crop thresholds to pasture irrigation, creates unnecessary cost or missed risk.

**Output:**
```
WATER QUALITY ASSESSMENT

Source: [bore / dam / mains / river / recycled]
Intended use: [food crop / stock / pasture / domestic]

TEST RESULTS SUMMARY
pH: [value] — [status]
EC: [dS/m] — [status]
SAR: [value] — [status]
Chlorine: [ppm] — [status]
[Other parameters as tested]

CONCERNS IDENTIFIED
1. [parameter] — [risk] — [recommended action]
2. [parameter] — [risk] — [recommended action]

TREATMENT PLAN
  [treatment] — [installation point] — [estimated cost]

RETESTING SCHEDULE: [annually / after each dry season / trigger conditions]

FOOD WEB NOTE: [chlorine / salinity / other impacts on soil biology if relevant]
```

**Next steps:**
- `/s4ag-soil` — high-salinity or high-SAR irrigation water degrades soil structure over time; monitor and address proactively.
- Run **irrigation-selection** (within this skill) — water quality determines which system components (filters, acid injectors) must be included.
- `/s4ag-earthworks` — if contamination is from an on-property source (old dam, contaminated runoff), address the source through landscape design.
