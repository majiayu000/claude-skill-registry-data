---
name: s4ag-soil
description: "Entry point for soil health decisions. Use when the user mentions soil tests, fertility, amendments, cover crops, compaction, soil biology, carbon, drainage, or says anything like 'my soil is', 'what should I add', 'soil test results', 'how do I improve my soil', or 'why are my crops struggling'."
allowed-tools: [Read]
---

# Soil

Soil decisions are biology decisions. The mineral chemistry on a soil test tells you what's there; the soil food web tells you whether the system can use it. Before adding any input, the right question is: does this feed or kill the biology? A healthy food web — bacteria, fungi, protozoa, nematodes, earthworms — produces every nutrient a crop needs. Your job is to feed the food web, not the crop.

**How this skill works:** Recommendations depend on your specific situation, so each sub-tool pauses at a **Checkpoint** to confirm the assumptions it's about to build on — soil type, climate, crops, budget, organic or conventional. A plan built on a wrong assumption wastes money in the field, so confirm the checkpoint before acting on the output. Each sub-tool ends with **Next steps** — the skills worth running once you've acted on this one.

---

## Expert Lineage

*The thinkers whose frameworks underpin this skill — and what they specifically discovered that changes how you farm.*

**Elaine Ingham — Soil Food Web**
Ingham mapped the complete trophic structure of living soil and established the fungi-to-bacteria ratio as the diagnostic lens: bacteria-dominated soils suit annuals; fungi-dominated soils suit perennials and trees. Her most actionable finding: most "nutrient deficiency" problems are food web problems — the biology to cycle available nutrients has been killed. Soluble synthetic fertilisers feed the crop while bypassing and slowly collapsing the food web. Before adding any input, ask whether it feeds or kills the biology.

**William Albrecht — Mineral Balance**
Albrecht at the University of Missouri spent forty years correlating soil mineral content with crop quality and animal health. He developed the cation saturation ratios that define balanced soil mineral chemistry: calcium at 60–75% of CEC, magnesium at 10–15%, potassium at 2–5%. His key insight: yield and nutritional density are separate variables. You can maximise yield on imbalanced soils — the food produced is nutritionally hollow. Read ratios, not just levels.

**Neal Kinsey — Albrecht in Practice**
Kinsey refined the Albrecht method through decades of farm-level consulting. His specific contribution: the relationship between minerals matters more than absolute levels. A soil with adequate calcium but excess magnesium behaves calcium-deficient because Mg displaces Ca on exchange sites and tightens soil structure. *Hands-On Agronomy* is the practitioner's manual for this.

**Jeff Lowenfels & Wayne Lewis — The Rhizosphere**
Their framework: 90% of soil biological activity happens in the few millimetres immediately surrounding plant roots. Each plant species has a unique microbial signature in its rhizosphere, selecting for specific bacteria and fungi through root exudate chemistry. This means plant diversity directly drives microbial diversity, and monocultures impoverish biology as surely as pesticides do.

**Christine Jones — Liquid Carbon Pathway**
Jones identified the fastest mechanism for moving photosynthetic carbon into deep soil: root exudates pumped directly into mycorrhizal fungal networks. Plants can allocate 30–40% of their photosynthetic output this way when the fungal network is intact. Her most counterintuitive finding: fungicide use damages soil carbon accumulation more than tillage — it severs the mycorrhizal pipeline that moves carbon underground.

---

## Which tool fits

| You need to... | Tool |
|---|---|
| Interpret a soil test report | test-interpretation |
| Decide what amendments to apply and how much | amendment-planning |
| Choose cover crops for your situation | cover-crop-selection |
| Diagnose and address compaction | compaction-diagnosis |
| Build a long-term fertility programme | fertility-planning |

## Routing Decision

- **Have soil test numbers and don't know what they mean** → test-interpretation
- **Know what's low, unsure what to add or how much** → amendment-planning
- **Planning cover crops, unsure what to choose** → cover-crop-selection
- **Suspect compaction — poor drainage, shallow roots, hard pan** → compaction-diagnosis
- **Want a season-by-season fertility strategy** → fertility-planning
- **Unclear** → test-interpretation first; it reveals what else is needed

---

## Test Interpretation

*Makes sense of a soil test report through the Albrecht/Ingham lens.*

Ask the user to share their soil test numbers. A standard soil test reports mineral chemistry only — it tells you almost nothing about the food web. For a complete picture: run a standard test for minerals, and an Ingham-method biological assessment (active bacteria, active fungi, protozoa, nematode counts) for biology. The mineral test shows what's there; the biological test shows whether the system can cycle it.

Work through numbers in this order:

**1. pH — it controls availability of everything else.**
- Below 6.0: nutrient lockout likely even if levels look adequate. Lime is usually the first move.
- 6.0–7.0: ideal for most crops. Work with what's here.
- Above 7.5: micronutrient availability drops. Sulphur applications may help.

**2. Organic matter (OM).**
- Below 2%: building OM is the priority — it governs biology, water retention, and nutrient cycling.
- 2–5%: working range — maintain and build.
- Above 5%: strong biological base; focus on mineral balance rather than OM addition.

**3. Major nutrients (NPK).**
- Nitrogen: don't read it from a test — too mobile. Use OM trend and crop response as proxies.
- Phosphorus: below 20 ppm (Mehlich-3) warrants attention; above 80 ppm, adding more is wasted money.
- Potassium: below 120 ppm is deficient; watch the K:Mg ratio (ideally 2:1 to 4:1).

**4. Secondary nutrients.**
- Calcium: should be 60–75% of CEC. Below this, soil structure and plant health suffer.
- Magnesium: 10–15% of CEC. High Mg relative to Ca tightens soil and competes with Ca uptake.
- Sulphur: often overlooked; below 10 ppm warrants attention, especially in sandy soils.

**5. Micronutrients.**
- Flag critically low values (boron, zinc, manganese are common culprits).
- Fix pH and OM first — many micronutrient issues resolve without direct application.

**Checkpoint — confirm before finalising:**
- Which test method produced these numbers (Mehlich-3, Olsen, Morgan)? Thresholds shift between methods.
- What crops are you growing on this ground, and are they annuals or perennials?
- Do you have any biological assessment, or minerals only?

Stop and confirm these before producing the interpretation — the same number means different things under a different test method or crop.

**Output:**
```
SOIL TEST INTERPRETATION
pH: [value] — [status and implication]
Organic matter: [value]% — [status and priority]

MAJOR NUTRIENTS
P: [value ppm] — [status]
K: [value ppm] — [status]

SECONDARY NUTRIENTS
Ca: [% CEC] — [status]
Mg: [% CEC] — [status / ratio note]
S: [value ppm] — [status]

MICRONUTRIENTS
[any flagged deficiencies]

PRIORITY ORDER
1. [first action — usually pH or OM]
2. [second action]
3. [third action]

WHAT TO IGNORE FOR NOW
[numbers that don't need action yet — why]
```

**Next steps:**
- Run **amendment-planning** (within this skill) to turn the priority list into a costed input plan.
- `/s4ag-composting` — build the organic matter and biology a low-OM test calls for.
- `/s4ag-regenerative` — if the test reflects years of synthetic inputs, plan the wider transition.

---

## Amendment Planning

*Decides what to add, in what form, and how much — without defaulting to the most expensive option.*

Ask: what does the test show is low? What crops are being grown? What's the budget? What's available locally?

**Decision sequence:**

**1. Fix pH before adding nutrients.** Lime raises pH; sulphur lowers it. Incorrectly-pH'd soil wastes every amendment you apply.

**2. Choose amendment form based on speed and system:**
- Fast-acting (soluble): results this season; higher cost; feeds crop, bypasses food web.
- Slow-release (rock minerals, composts): builds over 2–5 years; feeds the system.
- Biological (compost, inoculants): restores the food web; the highest-value investment if biology is degraded.

*Transition note: if the farm has used soluble synthetics for years, biological recovery takes 1–3 seasons. Continue conventional inputs alongside biological amendments during this period — don't remove the crutch before the system can walk without it.*

**3. Common amendments by deficiency:**

| Deficiency | Conventional option | Biological/slow option |
|---|---|---|
| Low pH | Ag lime, dolomite (if Mg also low) | Same — lime is lime |
| High pH | Elemental sulphur | Sulphur + acidifying organic matter |
| Low P | Single superphosphate (fast) | Rock phosphate, bone meal |
| Low K | Muriate of potash (fast) | Sulphate of potash, greensand, kelp |
| Low Ca | Gypsum (no pH change), lime (raises pH) | Gypsum, calcite |
| Low Mg | Epsom salt (fast, foliar) | Dolomite, serpentine rock |
| Low S | Ammonium sulphate | Gypsum |
| Low B | Borax (use carefully — narrow margin) | Borax — no slow alternative |

**4. Rate calculation:** Use soil test recommendation where provided. Without one: start conservatively, retest in 12 months. Overapplication of minerals is harder to fix than underapplication.

**Checkpoint — confirm before finalising:**
- Is conventional (fast, soluble) acceptable, or organic-only? This determines which column of the amendment table applies.
- What's the budget per acre/ha, and what's available from a local supplier?
- Has this ground had years of soluble synthetics — meaning biology needs a transition period rather than a hard switch?

Stop and confirm — recommending rock phosphate to someone who needs a fast in-season response (or superphosphate to a certified-organic grower) wastes the recommendation.

**Output:**
```
AMENDMENT PLAN
[Deficiency]: Apply [product] at [rate per acre/ha]
  Timing: [when to apply]
  Form: [granular/liquid/foliar]
  Expected timeline: [when to expect improvement]

TOTAL COST ESTIMATE: [£/$ per acre/ha]

RETEST DATE: [12 months from now]
```

**Next steps:**
- `/s4ag-composting` — make biological amendments on-farm instead of buying them.
- Run **fertility-planning** (within this skill) to schedule these inputs across the rotation.
- `/s4ag-korean-natural-farming` — if cutting input cost is the priority, build fertility from local materials.

---

## Cover Crop Selection

*Chooses the right cover crop for the situation.*

Ask: what is the primary goal? What season is available? What equipment is available for termination?

**Match goal to species:**

| Goal | Species to consider |
|---|---|
| Fix nitrogen | Clover, vetch, field peas, fava beans, hairy vetch |
| Break compaction | Daikon radish, tillage radish, chicory, deep-rooted ryegrass |
| Build organic matter fast | Winter rye, oats, sorghum-sudan, buckwheat |
| Suppress weeds | Winter rye (allelopathic), buckwheat, dense oats |
| Feed soil biology | Diverse mixes — 5+ species outperforms monocultures |
| Winter soil cover | Winter rye, hairy vetch, crimson clover, field peas |
| Quick summer gap-fill | Buckwheat (6–8 weeks to flower), sorghum-sudan |
| Attract beneficials | Phacelia, buckwheat, crimson clover, mustard, coriander |

**Termination method matters:**
- Roller-crimper: effective only at flowering/seed set; suits no-till; kills without soil disturbance.
- Mowing: faster; may regrow; effective for annual species.
- Incorporation: fastest breakdown; disrupts biology; avoid if reducing tillage is a goal.
- Winter-kill: easiest option — choose frost-sensitive species (buckwheat, sorghum, phacelia) if no equipment.

**Food web note:** Diverse mixes feed diverse microbial communities. Single-species cover crops are better than bare soil; five-species mixes are better than single species. Each plant species feeds a different bacterial and fungal population in its rhizosphere.

**Checkpoint — confirm before finalising:**
- What climate zone / region are you in? Sowing windows and winter-kill behaviour depend on it.
- What equipment do you have for termination (roller-crimper, mower, none)?
- What crop follows this cover, and when does it need the ground?

Stop and confirm — a winter-kill species recommended to someone who needs a spring-terminated cover, or a frost-hardy rye to someone with no termination kit, creates a problem rather than solving one.

**Output:**
```
COVER CROP RECOMMENDATION
Primary goal: [goal]
Season: [season available]

Recommended species: [species or mix]
Seeding rate: [kg/ha or lb/acre]
Sowing window: [dates]
Termination method: [method and timing]

Expected benefits:
- [benefit 1]
- [benefit 2]
```

**Next steps:**
- `/s4ag-seasons` — slot the cover crop into the rotation so the ground is never left bare.
- Run **fertility-planning** (within this skill) to credit the cover's nitrogen to the following crop.
- `/s4ag-composting` — pair the terminated cover with compost for the fastest OM build.

---

## Compaction Diagnosis

*Identifies compaction, its cause, and how to fix it.*

**Step 1: Field observation.**
Poor drainage after rain? Shallow roots when pulling plants? Crops yellowing in wheel tracks? Puddles forming in low spots? Any of these warrants investigation.

**Step 2: Penetrometer test.**
Insert a penetrometer until it meets resistance — compaction layer is where it stops.
- 15–25cm: likely tillage pan.
- 25–45cm: subsoil compaction.
- Below 45cm: beyond mechanical remedy; biological-only.

**Step 3: Spade test.**
Dig 30cm, examine structure.
- Compacted: horizontal layers, few roots penetrating, grey or blue-grey mottling (anaerobic).
- Healthy: vertical pores and channels, earthworm tunnels, roots following pores freely.

**Solutions by compaction type:**

| Type | Depth | Cause | Remedy | Timeline |
|---|---|---|---|---|
| Surface | 0–15cm | Tillage, foot traffic, rain impact | Permanent beds, mulch, reduce tillage | 1–2 seasons |
| Tillage pan | 15–25cm | Repeated tillage at same depth | One-time subsoiling or deep-rooted covers (daikon) | 1 season mechanical; 2–3 biological |
| Subsoil | 25–45cm | Heavy equipment on wet soil | Deep-rooted cover crops; time — not machines | 3–5 years |
| Structural | All depths | Low OM, biology loss | OM building and biology restoration | 3–7 years |

**Critical rule:** Never subsoil wet soil — it smears rather than fractures. Only work when dry enough that soil fractures along natural planes.

**Checkpoint — confirm before finalising:**
- Is the soil currently wet or dry? No mechanical remedy should be recommended on wet soil.
- What's the likely cause — equipment traffic, tillage, livestock, low OM? The remedy follows the cause.
- Do you want a mechanical fix this season, or a biological fix over several?

Stop and confirm — recommending subsoiling without knowing soil moisture risks making the compaction worse.

**Output:**
```
COMPACTION DIAGNOSIS
Type: [surface / tillage pan / subsoil / structural]
Depth: [cm]
Likely cause: [cause]

Recommended remedy: [remedy]
Timeline to improvement: [timeline]
Do not: [what to avoid]
```

**Next steps:**
- Run **cover-crop-selection** (within this skill) to choose a deep-rooted biological decompactor.
- `/s4ag-water` — compaction and drainage problems are often the same problem; check water movement.
- `/s4ag-earthworks` — if compaction tracks with runoff and erosion, address the landscape water pattern.

---

## Fertility Planning

*Builds a season-by-season fertility programme.*

Ask: what crops are in rotation? What does the soil test baseline show? What's the budget? Organic or conventional?

**Framework:**

**1. Set the baseline.** Current test → identify what's deficient, adequate, and excessive.

**2. Map crop nutrient demands:**
- Heavy feeders (brassicas, corn, alliums, squash): high N, moderate P and K.
- Medium feeders (tomatoes, peppers, root veg): moderate NPK.
- Light feeders (herbs, salad leaves, legumes): low N, balanced minerals.
- N-fixers (legumes): credit the following crop with 30–80 kg N/ha depending on stand.

**3. Plan inputs against crop sequence:**
- Apply slow-release amendments (rock minerals, compost) in autumn — they need time to mineralise.
- Apply fast-release inputs close to planting for in-season responsiveness.
- Match compost timing to crop demand, not to calendar convenience.

**4. Build organic matter year on year:**
- Every 1% OM increase releases ~20–30 kg N/ha/year through mineralisation.
- Cover crops + compost builds faster than either alone.
- The food web does the nutrient cycling — feed it rather than replacing it with purchased fertility.

**5. Track and adjust:**
- Retest every 2–3 years.
- Watch crop response as the leading indicator — plants show deficiency before tests do.
- Record inputs applied, timing, and crop performance.

**Checkpoint — confirm before finalising:**
- What's the full crop rotation and sequence for the planning period?
- Organic or conventional — and is there a soil test baseline to plan against?
- What's the annual fertility budget?

Stop and confirm the rotation and baseline — a fertility plan without the crop sequence is guesswork.

**Output:**
```
FERTILITY PLAN — [Year]

ROTATION: [crop sequence]

AUTUMN INPUTS
[input]: [rate] [timing] [purpose]

SPRING/PRE-PLANT INPUTS
[input]: [rate] [timing] [purpose]

IN-SEASON
[input]: [rate] [timing] [purpose]

COVER CROP WINDOWS
[period]: [species] [nitrogen credit to following crop]

ESTIMATED COST: [£/$ per acre/ha]

INDICATORS TO WATCH
- [crop response to watch for]
- [soil indicator to monitor]

RETEST DUE: [date]
```

**Next steps:**
- `/s4ag-seasons` — lock the input timings into the year-round crop calendar.
- `/s4ag-composting` — supply the OM-building side of the plan from on-farm materials.
- `/s4ag-regenerative` — set the multi-year trajectory this annual plan is one step of.
