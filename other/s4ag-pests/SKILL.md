---
name: s4ag-pests
description: "Pest and disease management. Use when the user describes a pest, disease, or crop damage problem, or asks how to control something eating or damaging their crops. Also use for: 'what's wrong with my plants', 'holes in leaves', 'wilting', 'yellow leaves', 'white powder', 'black spots', 'insects on my crops', or any request to identify or control a farm pest or disease."
allowed-tools: [Read]
---

# Pests & Disease

Most pest and disease problems are symptoms of plant stress, and most plant stress is a symptom of food web dysfunction. Before reaching for any spray — biological or chemical — the most useful question is: why is this plant stressed enough to attract this pest? That said, when a crop is under immediate attack, the immediate answer comes first. This skill uses the IPM (Integrated Pest Management) ladder: start at the lowest intervention level that solves the problem, move up only when needed.

**How this skill works:** The wrong treatment wastes money and often kills the beneficials that would have solved the problem, so each sub-tool pauses at a **Checkpoint** to confirm what it's assuming — the actual pest, the crop, the urgency, organic or conventional. Confirm the checkpoint before acting. The one exception is genuine emergency: if a crop is under immediate attack with harvest imminent, the answer comes first and the framing waits. Each sub-tool ends with **Next steps** — the skills worth running once the immediate problem is handled.

---

## Expert Lineage

*The thinkers whose frameworks underpin this skill — and what they specifically discovered that changes how you farm.*

**Mary Louise Flint & Steve Dreistadt — Natural Enemies and IPM**
Their *Natural Enemies Handbook* is the primary reference for beneficial insect identification and deployment. Their key contribution to practice: the economic threshold concept — pest populations must reach a level where the cost of damage exceeds the cost of control before intervention is justified. Most pest populations never reach this threshold. The default response to a pest sighting should be monitoring and assessment, not spraying. Beneficial insects need pest populations to survive; eliminating pests eliminates their natural enemies.

**Eliot Coleman — Prevention Through Plant Health**
Coleman's case across forty years of market gardening: a healthy plant grown on a functional soil food web resists pest and disease pressure in ways that a nutritionally deficient plant cannot. Better cell wall integrity (adequate silicon, calcium, potassium), better secondary metabolite production, and better systemic acquired resistance all come from plant health, which comes from food web function. Cultural prevention — variety selection, rotation, timing — is cheaper and more reliable than any spray, biological or chemical.

**Jeff Gillman — Evidence-Based Assessment**
Gillman's *The Truth About Organic Gardening* provides the most honest comparison of organic and conventional interventions available. His most practically important finding: several organic interventions are harder on beneficial insects than targeted synthetic options. Pyrethrin, rotenone, and copper are not inherently safe because they're "natural." The question is evidence of efficacy and impact — read label claims sceptically and choose interventions with documented effectiveness and known biology impact.

**Elaine Ingham — Biology as Primary Pest Prevention**
Ingham's soil food web framework explains the mechanism behind Coleman's observation: plants grown on a functioning food web receive nutrients in the forms and concentrations they're adapted to — not the excess nitrogen and phosphorus of synthetic fertility that produces soft, fast-growing, pest-attractive tissue. A healthy food web also produces diverse antibiotic compounds through microbial activity that suppresses soil-borne pathogens. Address the food web before reaching for any spray.

---

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify what pest or disease you have | identification |
| Decide whether the damage warrants intervention | threshold-assessment |
| Use prevention and cultural controls | cultural-controls |
| Deploy beneficial organisms | biological-controls |
| Apply an approved organic spray | organic-interventions |
| Use conventional chemistry | conventional-options |

## Routing Decision

- **Don't know what it is yet** → identification first
- **Know what it is, unsure whether to act** → threshold-assessment
- **Planning ahead or preventing recurrence** → cultural-controls
- **Crop under attack, want least intervention** → biological-controls
- **Need to spray, want to avoid synthetics** → organic-interventions
- **Crop under immediate threat, harvest imminent, need fastest result** → conventional-options

**On urgency:** A farmer saying "there are aphids all over my brassicas and I'm harvesting tomorrow" gets Level 4/5 immediately, with a one-line note on prevention for next season. The IPM ladder is a planning tool, not a gate — deliver the answer at the right level for the urgency.

---

## Identification

*Diagnoses what the pest or disease is before acting.*

The identification protocol before any intervention: what does the damage look like, where on the plant, what time of year, what else is in the area? Treating without identification wastes inputs and often kills beneficials while missing the actual pest.

**Damage pattern diagnosis:**

| Symptom | Likely cause | Confirm by |
|---|---|---|
| Holes in leaves — irregular, ragged edges | Caterpillars, slugs, beetles | Check undersides at night; look for frass |
| Holes in leaves — small, regular, round | Flea beetles (brassicas especially) | Look for tiny shiny beetles jumping when disturbed |
| Leaf curl, distortion at growing tips | Aphids, virus, broad mite | Check undersides and growing points with hand lens |
| Yellow leaves — lower, older leaves first | Nitrogen deficiency, root damage, overwatering | Pull plant, check roots for rot or pests |
| Yellow leaves — upper, newer leaves | Iron/manganese deficiency (usually pH-related) | Soil pH test |
| Yellow patches between veins (interveinal chlorosis) | Magnesium or iron deficiency | Soil test; check pH |
| White powdery coating on leaf surface | Powdery mildew | Wipes off easily; spreads in warm dry weather |
| Grey fuzzy coating (botrytis) | Grey mould — Botrytis cinerea | High humidity, poor air circulation; check ventilation |
| Black or brown spots | Blight, bacterial, fungal leaf spot | Pattern and speed of spread; weather (blight in wet) |
| Wilting despite adequate moisture | Root rot, Pythium, vine weevil larvae, crown rot | Pull plant — check roots; vine weevil = C-shaped grub |
| Stem rot at base of seedlings | Damping-off (Pythium, Rhizoctonia) | Overwatering; poor drainage; crowded seedlings |
| Deformed or discoloured fruit | Virus, calcium deficiency, irregular watering | Check pattern: widespread = systemic; localised = physiological |
| Silvery streaks on leaves | Thrips | Look for tiny insects along veins under magnification |
| Sticky residue on leaves (honeydew) | Aphids, scale, whitefly above | Check underside of leaves above sticky area |

**Soil food web diagnostic note:** many pest and disease problems correlate with food web disruption. Excess nitrogen (soft, lush tissue), synthetic pH amendments, and fungicide use all increase pest susceptibility. Before treating the symptom, ask whether the soil biology has recently been disturbed.

**Checkpoint — confirm before finalising:**
- Ask for a photo or close description before naming the cause — symptoms overlap heavily across pests, deficiencies, and disease.
- What crop, what part of the plant, and how fast is it spreading?
- Is this an emergency (harvest imminent, crop collapsing)? If so, flag it and move straight to control.

A misidentification sends the farmer to the wrong treatment. Confirm the ID — or state your confidence level honestly — before recommending action.

**Output:**
```
PEST/DISEASE IDENTIFICATION

Crop affected: [crop]
Symptom: [damage description]
Location on plant: [where damage appears]
Season/timing: [when noticed]

Likely cause: [pest or disease]
Confidence: [High / Medium / Low]
If Low, alternatives to consider: [list]

Recommended next step: [threshold-assessment / immediate intervention / cultural-controls]
```

**Next steps:**
- Run **threshold-assessment** (within this skill) to decide whether this even warrants treatment.
- If confidence is low: `/s4ag-soil` — many "pest" symptoms are nutrient or biology problems in disguise.

---

## Threshold Assessment

*Decides whether the level of damage actually warrants intervention.*

The economic threshold concept: pest populations must cause damage whose cost exceeds the cost and risk of the intervention before treatment is justified. Most pest populations — especially early in the season with beneficials present — never reach threshold. The default is to monitor and wait.

**Factors that raise the threshold (tolerate more damage):**
- Early season, crop has recovery time
- Beneficial insects visibly present (parasitic wasps, ladybirds, lacewings)
- Crop is growing vigorously and compensating
- Damage is cosmetically bad but not reducing yield
- Intervention would harm beneficials

**Factors that lower the threshold (act sooner):**
- Harvest is within 2–4 weeks
- Crop is young transplant with limited leaf area to lose
- Damage is on developing fruit or flowers (not just leaves)
- Rapid increase in pest numbers observed over 3–5 days
- Disease is spreading (vs. static damaged area)

**Common thresholds (as guidelines — adjust to crop value and context):**
- Aphids: 10–20 per leaf on most crops; 3–5 per plant on salad crops with imminent harvest
- Caterpillars: 1 per young transplant; 3–5 per established brassica before economic damage
- Spider mites: act early in polytunnel crops (cucumber, tomato) at first colony; tolerate low levels in field crops
- Slugs: 1 slug per plant on young transplants; tolerate higher numbers in established crops
- Powdery mildew: intervene at first signs in susceptible crops (courgette, cucumber); tolerate light infection on established brassicas late in season

**Checkpoint — confirm before finalising:**
- How much damage, on how much of the crop, and is the pest population rising or stable over the last few days?
- How long until harvest, and what's the crop worth? Both move the threshold.
- Are beneficials already visibly present? If so, intervention may do more harm than good.

Confirm the scale and trend before advising — "spray" and "wait" are opposite calls that hinge on these facts.

**Output:**
```
THRESHOLD ASSESSMENT

Pest/disease: [name]
Crop: [crop and growth stage]
Current damage level: [description]
Trend: [increasing rapidly / stable / decreasing]

Economic threshold: [guidance for this crop/pest combination]
Decision: [Intervene now / Monitor for 5–7 days / No action needed]
Rationale: [why]

If monitoring: watch for [specific trigger that would prompt intervention]
```

**Next steps:**
- If no action needed: run **cultural-controls** (within this skill) to prevent recurrence next season.
- If action needed: run **biological-controls** (within this skill) — the lowest-intervention effective option first.

---

## Cultural Controls

*Uses prevention and management practices to reduce pest and disease pressure without inputs.*

Cultural controls are the most cost-effective pest management available — they prevent problems rather than responding to them. They work best when planned before planting, not after damage appears.

**Rotation:** Most soil-borne diseases and some pests (clubroot, allium white rot, nematodes) build up in soil when the same crop family is grown repeatedly. Minimum 3-year rotation between families on the same ground. Longer (5–7 years) for persistent problems like allium white rot.

**Variety selection:** Disease-resistant and locally-adapted varieties can eliminate the need for fungicide programmes entirely. For brassicas: clubroot-resistant varieties on infected ground. For tomatoes: choose varieties with resistance to blight (Blight F1), TMV, and fusarium. For salad: choose mildew-resistant lettuce varieties for polytunnel production.

**Timing:** Avoid pest peaks through timing. Carrot fly has two peaks (May and August in UK) — sowing in June avoids the first peak. Flea beetles damage is worst in dry spring weather — establishing brassicas in autumn or under fleece avoids worst pressure. Brassica caterpillar damage tracks butterfly activity — cover under mesh to exclude oviposition.

**Physical barriers:**
- Insect-proof mesh (0.8mm) over brassicas: excludes cabbage white butterfly, cabbage root fly, flea beetle
- Fleece (30–35 g/m²): protects against flea beetle and carrot fly; also provides frost protection
- Copper tape/rings around container plants: deters slugs and snails (variable effectiveness)
- Sticky traps (yellow for whitefly and fungus gnats; blue for thrips): monitoring tool, not a control

**Companion planting:** Evidence-based companions that have demonstrated pest management effect:
- Nasturtium as an aphid trap crop near brassicas (draw aphids away from crop)
- Basil near tomatoes: some evidence of reduced thrips damage
- Alliums near carrots: traditional but limited evidence for carrot fly deterrence
- Phacelia, buckwheat, and umbellifers near any crop: attract and retain beneficial insects

**Sanitation:** Remove diseased plant material promptly — grey mould, blight, and viral disease spread through infected tissue left in the field. Don't compost diseased material unless the compost heap reaches 60°C+. Rotate tools between areas when disease pressure is high.

**Checkpoint — confirm before finalising:**
- What's the rotation, the growing environment (field, polytunnel, covered), and the climate zone? Timing advice depends on all three.
- Is this prevention for next season, or are you also dealing with an active problem now?

Confirm the system before recommending rotation and timing changes — generic advice won't fit the farm's constraints.

**Output:**
```
CULTURAL CONTROLS FOR [pest/disease]

Immediate (this season):
- [action and timing]

Next season (prevention):
- [rotation change]
- [variety to trial]
- [timing adjustment]
- [physical barrier to use]

Companion planting:
- [companion species and rationale]

Sanitation:
- [specific action]
```

**Next steps:**
- `/s4ag-seasons` — bake the rotation and timing changes into the year-round plan.
- `/s4ag-soil` — address the plant stress (often excess N or weak biology) behind recurring pressure.
- `/s4ag-biodiversity` — build permanent beneficial-insect habitat for season-on-season control.

---

## Biological Controls

*Deploys beneficial organisms to suppress pest populations.*

Biological controls work best as part of a planned system — not as a rescue treatment after a population has crashed. They require living pests to reproduce, so early deployment at low pest density gives better results than late deployment at high density.

**Habitat for beneficials (cheapest and most durable approach):** Create and maintain flowering strips of umbellifers (dill, fennel, coriander), phacelia, buckwheat, and native wildflowers near crops. These provide nectar and pollen for adult beneficial insects, who then lay eggs near pest populations. Parasitic wasps, hoverflies, and lacewings are the primary beneficials — their adults need nectar; their larvae eat aphids, caterpillars, and scale.

**Purchased beneficial organisms:**

| Target pest | Biological agent | Form | Key conditions |
|---|---|---|---|
| Aphids (glasshouse) | Aphidius colemani, Aphidoletes aphidimyza | Release cards/sachets | 15–28°C; best in polytunnel |
| Red spider mite | Phytoseiulus persimilis | Release sachets | >15°C; humidity >60% |
| Whitefly | Encarsia formosa | Release cards | >18°C; indoor environment |
| Vine weevil larvae | Steinernema kraussei (nematode) | Soil drench | Soil temp >5°C; moist soil |
| Caterpillars | Bacillus thuringiensis var. kurstaki (Btk) | Spray | Active larvae; ingested by caterpillars |
| Leatherjackets | Steinernema carpocapsae (nematode) | Soil drench | Moist soil; >12°C |
| Thrips | Amblyseius cucumeris | Release sachets | >15°C; indoor |
| Scale insects | Metaphycus helvolus | Release cards | >22°C; indoor |
| Soil pathogens | Trichoderma harzianum | Drench or seed treatment | Biologically active soil; preventive |
| Powdery mildew | Bacillus subtilis (Serenade) | Spray | Preventive; warm dry conditions |

**Soil biology as biological control:** Ingham's food web framework. A functioning soil food web — diverse bacteria, nematodes, microarthropods — suppresses soil-borne pathogens (Pythium, Fusarium, Rhizoctonia) through competition and antibiosis. Rebuilding the food web through compost additions and cover crops reduces damping-off, root rot, and soil-borne disease pressure more durably than any purchased biological agent.

**Checkpoint — confirm before finalising:**
- Field or protected environment, and what's the temperature range? Most purchased beneficials have strict temperature and humidity windows.
- How advanced is the infestation? Beneficials need living prey — they fail if deployed too late on a crashed population.
- Is the timeline (days to effect) acceptable, or is faster action needed?

Confirm conditions before recommending a release — a beneficial deployed outside its window is wasted money.

**Output:**
```
BIOLOGICAL CONTROL PLAN

Target pest: [pest]
Crop: [crop and environment — field / polytunnel]

Habitat approach: [what flowering strips or habitat to establish]

Purchased agent (if appropriate):
Agent: [organism]
Source: [supplier recommendation]
Timing: [when to release — early / at first detection]
Rate: [per m² or per plant]
Conditions required: [temperature, humidity]
Expected result timeline: [days to see effect]
```

**Next steps:**
- If biological control is too slow for the situation: run **organic-interventions** (within this skill).
- `/s4ag-biodiversity` — turn one-off beneficial releases into permanent resident populations.
- `/s4ag-composting` — make the compost and tea that suppress soil-borne pathogens biologically.

---

## Organic Interventions

*Applies approved organic sprays as Level 4 on the IPM ladder — when cultural and biological controls are insufficient or too slow.*

Organic does not mean harmless. Evaluate each intervention on its efficacy, biology impact, and residual — not on whether it is "natural." Some organic inputs cause significant harm to beneficials and soil biology at normal use rates.

**Common organic interventions:**

| Product | Target | Biology impact | Limitation |
|---|---|---|---|
| Neem oil (azadirachtin) | Broad insect (aphids, scale, whitefly, caterpillars) via IGR | Moderate — avoid applying during peak bee foraging; degrades quickly | Slow-acting (3–7 days); needs repeat applications; preventive more than curative |
| Copper sulphate / copper hydroxide | Blight, downy mildew, bacterial diseases | Accumulates in soil — long-term application causes copper toxicity; harms earthworms | Approved organic but not benign; use minimum effective rate; avoid on same ground annually |
| Sulphur | Powdery mildew, spider mite | Harmful to predatory mites (Phytoseiulus) and some beneficials; phytotoxic above 27°C | Do not apply in hot weather; incompatible with some fungicides; do not apply within 2 weeks of oil sprays |
| Pyrethrin | Broad-spectrum contact insecticide | Harmful to most beneficials including beneficials; breaks down in 12–24 hours | Broad spectrum — kills pests and beneficials alike; use as last resort before conventional |
| Spinosad | Caterpillars, thrips, leafminer | Lower beneficial impact than pyrethrin; some bee risk at application; resistance risk in thrips | Rotate with other modes of action; do not apply during flowering |
| Insecticidal soap (potassium soap) | Soft-bodied insects (aphids, mites, whitefly) | Low residual; low biology impact | Contact-only — thorough coverage required; no residual protection; may cause phytotoxicity on some crops |

**Checkpoint — confirm before finalising:**
- Is the operation certified organic, and if so under which scheme? Approved inputs vary between certifiers.
- Current weather and crop stage — sulphur is phytotoxic above 27°C; several sprays harm bees during flowering.
- Have cultural and biological options genuinely been exhausted, or is this jumping the ladder?

Confirm certification status and conditions — an input that breaches the farm's certification, or scorches the crop, is worse than no spray.

**Output:**
```
ORGANIC INTERVENTION

Pest/disease: [target]
Product: [product name]
Active ingredient: [active]
Application rate: [rate and dilution]
Timing: [when to apply — time of day, growth stage, weather conditions]
PHI (pre-harvest interval): [days]
Repeat application: [yes/no — interval]

Biology impact: [what this does to soil and beneficial populations]
Better alternative if available: [more targeted option, or biological control]
```

**Next steps:**
- `/s4ag-soil` — reduce the plant stress that's driving repeat infestations.
- `/s4ag-certification` — if organic certification is a goal, confirm this input keeps you compliant.
- Return to **cultural-controls** (within this skill) to prevent next season's recurrence.

---

## Conventional Options

*Level 5 on the IPM ladder — when crop loss is imminent and lower-intervention options are insufficient or too slow.*

Conventional chemistry is the answer when: the crop will fail without intervention, harvest is imminent and there is no time for slower options, or the pest population has exceeded all other control options. Reaching for conventional as a first response rather than a last resort destroys the beneficial population that would prevent the next problem.

**Principles for conventional use within an IPM programme:**
- Choose the most selective option available — target the pest, spare the beneficials.
- Respect the economic threshold — don't spray at first sighting.
- Rotate modes of action (FRAC/IRAC codes) to prevent resistance.
- Observe PHI and re-entry intervals — they protect human health.
- Apply at the right growth stage and time of day (avoid bee foraging hours).

**Common conventional interventions by pest category:**

*Aphids:* Pyrethroids (broad spectrum; harm all beneficials) or pirimicarb (selective aphicide; spares most beneficials — prefer this). Systemic neonicotinoids are effective but have well-documented pollinator impacts — avoid in flowering crops.

*Caterpillars:* Indoxacarb or chlorantraniliprole (diamide group) — effective on caterpillars, lower bee toxicity than pyrethroids. Bt (Bacillus thuringiensis) should be tried first.

*Fungal diseases:* Trifloxystrobin (strobilurin) or tebuconazole (triazole) for broad-spectrum fungal. Rotate between FRAC groups to prevent resistance. Note: strobilurins are highly toxic to aquatic organisms — observe buffer zones near water.

*Slug and snail:* Metaldehyde is being withdrawn in many markets due to wildlife toxicity — use ferric phosphate (Sluggo, Iron phosphate) which is approved organic and safer for wildlife and soil biology.

**Checkpoint — confirm before finalising:**
- Confirm the pest ID is solid — a broad-spectrum spray on a misidentified problem kills beneficials for nothing.
- Is the crop flowering, near water, or close to harvest? Bee toxicity, aquatic buffer zones, and PHI all gate the choice.
- What's legally approved for this crop in the user's region? Approvals and withdrawals vary by jurisdiction and change often.

Confirm ID, timing, and local approval before naming a product — this is the highest-consequence level of the ladder.

**Output:**
```
CONVENTIONAL CONTROL

Pest/disease: [target]
Active ingredient: [active]
Product class: [IRAC/FRAC group if relevant]
Application window: [timing and growth stage]
PHI: [days before harvest]
Re-entry interval: [hours]
Resistance management: [rotate with — mode of action to alternate]

Biology impact: [what this input does to soil biology and beneficial populations]
Sustainable alternative at this level: [specific more-selective product or biological control option]
```

**Next steps:**
- `/s4ag-soil` — the durable fix: reduce the plant stress that made the crop vulnerable.
- Return to **cultural-controls** (within this skill) to design out the problem before next season.
- `/s4ag-biodiversity` — rebuild the beneficial populations a broad-spectrum spray will have knocked back.
