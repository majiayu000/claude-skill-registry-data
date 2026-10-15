---
name: s4ag-vegetables
description: "Vegetable growing decisions — variety selection, spacing, succession, problem diagnosis, and intensive production. Use when the user says anything like 'what should I grow', 'my crop is failing', 'how do I plan my beds', 'succession planting', 'no-dig', or 'market garden'."
allowed-tools: [Read]
---

# Vegetables

You are trying to grow food reliably, season after season, from the same ground — without wasting seed, missing harvest windows, or watching a crop collapse. This skill structures the decisions that determine whether a vegetable system works: what to grow, when to sow it, how to space it, how to follow one crop with another, and what to do when something goes wrong. The principle underneath every recommendation is the same: the soil that grows the crop matters more than the inputs that feed it. A well-structured, biologically active bed needs less management, not more.

**How this skill works:** Each sub-tool pauses at a **Checkpoint** to confirm the assumptions it is about to build on before producing output. A recommendation built on a wrong assumption wastes time and money — confirm the checkpoint before acting. Each sub-tool ends with **Next steps** — the skills worth running once you have acted on this one.

---

## Expert Lineage

*The thinkers whose frameworks underpin this skill — and what they specifically discovered that changes how you farm.*

**Eliot Coleman — Four-Season Production and System Efficiency**
Coleman demonstrated at Four Season Farm in Maine that intensive organic vegetable production outperforms conventional tilled systems in both yield and net income when correctly managed. His most actionable finding: the growing window can be extended by six to eight weeks each end of the season with low tunnels and cold-hardy variety selection — not expensive infrastructure. He codified the spacing and rotation system that makes continuous harvest possible on small acreage.

**Jean-Martin Fortier — The High-Income Small-Scale Market Garden**
Fortier built a documented case at Les Jardins de la Grelinette that a sub-hectare market garden can generate over $100,000 CAD per year gross revenue on intensive permanent beds. His specific contribution: profitability is driven by the combination of bed-width standardisation, succession timing, and direct marketing — not by scale. His crop planning spreadsheet system is the most practically useful succession scheduling tool available to small-scale producers.

**Charles Dowding — No-Dig and Minimal Disturbance**
Dowding conducted systematic, replicated comparisons of dug versus undug beds over more than a decade and found that no-dig consistently matched or outperformed dug beds for yield while dramatically reducing weed burden. The mechanism Ingham's framework explains: tillage destroys the fungal networks and aggregate structure that deliver water and nutrients to roots. Dowding's primary practical finding: a thick compost mulch applied to the surface replaces all the functions of tillage without its costs.

**Elaine Ingham — Food Web Beneath the Bed**
Vegetable production has the most intensive soil management demands of any farm enterprise, making Ingham's framework the most consequential here. Her specific finding relevant to vegetables: in a functioning food web, bacteria-dominated soils (appropriate for annual vegetables) can produce adequate nitrogen through mineralisation without soluble synthetics — but only when organic matter is adequate and tillage is limited enough to maintain biological continuity. Every tillage pass resets succession; permanent beds allow the biology to accumulate.

**William Albrecht — Nutritional Density as the Goal**
Albrecht's work established that yield and nutritional quality are separate outcomes — a crop can produce maximum yield on a mineral-imbalanced soil while delivering nutritionally hollow food. For vegetable growers, the practical implication is that market differentiation on flavour and shelf life (both proxies for nutritional density) requires attention to mineral balance, not just high-N fertility.

**Masanobu Fukuoka — The Observation Before the Action**
Fukuoka's most transferable insight for vegetable growers is the discipline of watching a crop failure before reaching for an intervention. Most vegetable problems — yellowing, poor germination, slug damage, bolting — have a structural cause in the system that the intervention does not address. Diagnosing before acting prevents the common pattern of applying solutions to symptoms while the underlying cause continues.

---

## Which tool fits

| You need to... | Tool |
|---|---|
| Choose what varieties to grow for your context and goals | variety-selection |
| Work out plant spacing and bed density | spacing-and-density |
| Schedule successions for continuous harvest | succession-planning |
| Know what to sow and plant each month | growing-calendar |
| Diagnose why a crop is failing or underperforming | problem-diagnosis |
| Set up or improve an intensive permanent bed system | intensive-systems |

## Routing Decision

- **Starting a new plot or market garden — what to grow?** → variety-selection, then intensive-systems
- **Existing system, need to plan next season** → succession-planning, then growing-calendar
- **Crop is failing or underperforming right now** → problem-diagnosis first
- **Spacing or yield questions** → spacing-and-density
- **Transitioning from tilled beds to permanent beds** → intensive-systems
- **Unsure** → growing-calendar; it reveals what else is needed

---

## Variety Selection

*Chooses the right varieties for the grower's climate, system, and purpose — market, household, or processing.*

Variety choice has more leverage on outcome than almost any other single decision. The wrong variety for your climate, your market, or your system will underperform regardless of management. Work through this in order:

**1. Define the purpose first.**
- Direct market or restaurant: flavour, appearance, shelf life, and harvest window are primary. Heritage and unusual varieties command premium prices.
- CSA or box scheme: reliability, harvest spread across the season, and ability to fill boxes every week are primary. Some compromise on premium varieties in favour of consistent performers.
- Household / subsistence: flavour and storage quality; yield per bed matters more than appearance.
- Processing or value-adding: specific varieties bred for processing characteristics (high sugar in tomatoes for sauce; high flesh-to-seed in cucumbers for pickling).

**2. Climate and disease resistance.**
Disease-resistant varieties are not a compromise — in humid climates they often outperform nominally superior heritage varieties that succumb to blight, mildew, or clubroot.

| Crop | Climate stress | Resistance to look for |
|---|---|---|
| Tomato | Humid / high rainfall | Blight (Ph-1, Ph-2, Ph-3), leaf mould |
| Lettuce | Hot summers | Heat-bolt resistance; tipburn resistance |
| Brassicas | Clubroot-prone soils | Clubroot resistance (CR) ratings |
| Courgette | Humid conditions | Powdery mildew resistance |
| Spinach | Long days / heat | Bolt-resistant varieties |
| Onion | Wet autumns | White rot avoidance through early maturity |

**3. Match variety to harvest window.**
For any crop grown in succession, select varieties with different maturity dates rather than multiple sowings of the same variety. Lettuce example:
- Early: *Merveille des Quatre Saisons*, *Forellenschluss*
- Main season: *Flashy Trout's Back*, *Little Gem*, *Butterhead* types
- Heat-tolerant: *Jericho*, *Sierra*, *Muir*
- Autumn/overwinter: *Winter Density*, *North Pole*, *Valdor*

**4. Seed source and vigour.**
Open-pollinated and heritage varieties can be saved year on year — important for cost control and local adaptation. F1 hybrids offer uniformity and hybrid vigour but must be repurchased. For a farm with seed-saving as a goal, build the variety list around open-pollinated varieties (→ `/s4ag-seeds`).

**5. Trial allocation.**
No variety should go into full production without a trial year. Allocate 10–20% of bed space to new varieties each year. Trial against your current best performer in the same bed, same sowing date.

**Checkpoint — confirm before finalising:**
- What is the primary market or use for this crop? Market, household, or processing changes the variety criteria substantially.
- What are the main disease pressures in this location — blight, clubroot, downy mildew?
- Is seed saving a goal? This limits hybrid variety recommendations.

If you do not know the disease pressure, recommend disease-resistant varieties by default — the downside of choosing a resistant variety when pressure is absent is minor; the downside of choosing a susceptible variety when pressure is high is complete crop loss.

**Output:**
```
VARIETY SELECTION — [Crop]

PURPOSE: [market / CSA / household / processing]
CLIMATE NOTES: [relevant pressures]

RECOMMENDED VARIETIES
Early: [variety] — [maturity / notes]
Main season: [variety] — [maturity / notes]
Late/overwinter: [variety] — [maturity / notes]

DISEASE RESISTANCE NOTES: [what to look for in seed catalogue listings]

TRIAL VARIETIES THIS YEAR: [1-2 to test against your current best]

SEED SOURCES: [catalogue or supplier recommendation]

SEED-SAVING STATUS: [OP or F1; saveable or not]
```

**Next steps:**
- Run **succession-planning** (within this skill) to schedule multiple varieties for continuous harvest.
- `/s4ag-seeds` — if seed saving from selected varieties is a goal.
- Run **growing-calendar** (within this skill) to slot the chosen varieties into the sowing schedule.

---

## Spacing and Density

*Determines optimal plant spacing and bed density for intensive production without compromising plant health.*

Intensive bed spacing produces more per unit area than traditional row spacing — but only up to a point. Beyond optimal density, air circulation drops, disease pressure rises, and yield per plant falls faster than plant density increases. The relationship is not linear.

**Standard bed width: 75–90cm.**
This is the foundation of the intensive system. All spacing recommendations below assume beds worked from the sides without stepping on soil. Wider than 90cm and you cannot reach the centre without stepping on the bed.

**Equidistant spacing outperforms row spacing.**
Place plants at equal distance in all directions (a triangular grid) rather than in rows. For any given spacing, equidistant planting fits 15% more plants into the bed and distributes root and leaf competition evenly.

**Spacing table by crop and purpose:**

| Crop | Intensive spacing | Notes |
|---|---|---|
| Lettuce (full head) | 25cm | 12–14 heads per 90cm-wide bed metre |
| Lettuce (baby leaf cut-and-come) | Broadcast / 2–3cm | 3–5 cuts before quality drops |
| Spinach / salad leaves | Broadcast / 10–15cm | Thicker = quicker, fewer cuts |
| Carrots | 5cm in-row, 30cm row | Thin to 5cm for roots; broadcast for baby carrot |
| Beetroot | 10cm equidistant | Multi-sow station (3 seeds/station) then thin or sell multiples |
| Radish | 5–7cm equidistant | Can be interplanted as catch crop |
| French beans (dwarf) | 20cm equidistant | 3 staggered rows in 90cm bed |
| Climbing beans | 20cm in double row | Support along bed length |
| Courgette | 90cm–120cm | 1 plant per metre bed length; leaves expand 80cm+ |
| Cucumber (indoor) | 50cm in single row | Train vertically; indeterminate types |
| Tomato (cordon, indoor) | 45–50cm single row | Remove side shoots; train to single stem |
| Tomato (bush, outdoor) | 60cm equidistant | Allow natural form |
| Brassicas (large head) | 50–60cm | Kale, cauliflower, winter squash |
| Brassicas (mini / baby) | 30–35cm | Baby heads; earlier harvest |
| Onion sets | 10cm equidistant | 4 staggered rows in 90cm bed |
| Leeks | 15cm equidistant | Transplant into deep holes |
| Garlic | 15cm equidistant | Interplant with overwintered salad |
| Potatoes | 30cm in double row | Earthing up requires row spacing |

**Interplanting logic:**
Combine a fast crop with a slow crop so the fast crop completes before the slow crop expands.
- Radish between brassica transplants: radish harvested by week 4; brassicas fill in by week 8.
- Lettuce between climbing beans: lettuce harvested before bean canopy closes.
- Garlic underplanted with overwintered spinach or chard: harvested on different timelines.

**Checkpoint — confirm before finalising:**
- What is the bed width? Spacing tables above assume 75–90cm beds worked from outside.
- Are these outdoor beds or under cover? Under cover, some crops (tomatoes, cucumbers) require different spacing due to training systems.
- Is the goal maximum yield per bed or maximum yield per hour of labour? Higher density increases yield per bed but also labour — thinning, harvesting, monitoring.

Spacing recommendations built on assumed bed widths that don't match the actual beds produce planting plans that don't work out in the field.

**Output:**
```
SPACING PLAN — [Bed / Block]

BED DIMENSIONS: [width x length]
SYSTEM: [outdoor / polytunnel / raised bed]

PLANTING LAYOUT
[Crop]: [spacing] [pattern — equidistant / row / broadcast]
  Plants per bed metre: [number]
  Plants per full bed: [number]
  Expected yield per bed: [estimate]

INTERPLANTING COMBINATIONS
[Fast crop] between [slow crop] — harvest [fast crop] by [date]

NOTES ON DENSITY LIMITS: [any crops where not to push closer]
```

**Next steps:**
- Run **succession-planning** (within this skill) to schedule what follows each planting.
- `/s4ag-soil` — high-density plantings make greater demands on soil fertility and biology; check the soil can support it.
- Run **intensive-systems** (within this skill) if the bed infrastructure needs to match the intensive spacing plan.

---

## Succession Planning

*Schedules multiple sowings and plantings so one crop follows another with no bed sitting empty.*

An empty bed is a lost opportunity twice over — revenue gone and soil biology starved of root exudates. Succession planning fills every bed window with the right crop at the right time, from the first spring sowing to the last autumn planting.

**The succession logic:**

**Step 1: Map the bed capacity.**
List every bed and its approximate available season (first frost-free to last frost date, adjusted for covers).

**Step 2: Assign anchor crops.**
Anchor crops are slow-growing, high-value crops that occupy the bed for most of the season and define the schedule around them.
- Tomatoes, peppers, aubergines (planted late spring, finished late autumn under cover)
- Leeks (transplanted July, harvested through winter)
- Winter squash (planted May–June, harvested October)
- Brassicas for winter (transplanted August, harvested November–March)

**Step 3: Fill gaps with fast crops.**
Before anchor crops go in, and after they come out, fill with 4–8 week crops.
- Before tomatoes (planted in June under cover): spinach, radish, lettuce, spring onion
- After squash (cleared October): overwintered spinach, lamb's lettuce, winter salad
- Between leek transplanting (July) and preceding crop clearance: catch crop of radish or turnip

**Succession intervals by crop:**

| Crop | Sowing-to-harvest | Succession interval | Notes |
|---|---|---|---|
| Lettuce (full head) | 6–8 weeks summer / 10–14 weeks spring | Every 2–3 weeks | 6 sowings to cover June–October |
| Radish | 4 weeks | Every 2 weeks | Can run 8+ sowings per season |
| Baby leaf salad | 3–5 weeks | Every 2 weeks | 3–5 cuts per sowing |
| Spinach | 6–8 weeks | Every 3 weeks | Slow in heat; skip July–August |
| French beans (dwarf) | 8–10 weeks | Every 3 weeks | 2–3 sowings covers July–October |
| Beetroot | 8–12 weeks | Every 3–4 weeks | Stores well; later sowings can gap without loss |
| Carrots | 10–16 weeks | Every 4–6 weeks | 3 sowings covers summer-autumn |
| Pak choi / Asian greens | 4–6 weeks | Every 2–3 weeks | Bolts in heat; avoid June–July |
| Courgette | 10 weeks from transplant | 1–2 sowings | Single plant produces 2–4 per week |

**The rolling sowing board:**
Create a physical or written board with:
- Column per bed
- Row per month
- Each cell: what's in it, when it was sown/planted, when it comes out, what goes in next

Review the board weekly during the season. Adjust for actual harvest dates — a slower-than-expected crop pushes the succession back.

**Checkpoint — confirm before finalising:**
- What is the actual growing season for this location — frost dates, last and first?
- How many beds / how much space is available? The succession plan needs to match the capacity.
- Is this for market (maximise continuity and volume), CSA (fill the box weekly), or household (self-sufficiency)?

A succession plan written for a 10-bed market garden applied to a 4-bed kitchen garden will over-plan; a CSA succession that doesn't account for box-filling across all vegetables will produce gluts and gaps.

**Output:**
```
SUCCESSION PLAN — [Season/Year]

GROWING SEASON: [first sow date] to [last harvest date]
BEDS AVAILABLE: [number and size]
PRIMARY GOAL: [market / CSA / household]

BED SCHEDULE (repeat for each bed)
Bed [number]:
  [Month 1–2]: [Crop — sow date — expected harvest — clearance date]
  [Month 3–4]: [Crop — transplant date — expected harvest — clearance date]
  [Month 5–6]: [Crop — sow date — expected harvest — clearance date]

SUCCESSION INTERVALS
[Crop]: Sow every [X] weeks — next sow date after [date]: [date]

GAPS AND RISKS
[Any bed that will sit empty or at risk of gap — what to sow]
```

**Next steps:**
- Run **growing-calendar** (within this skill) to translate the succession plan into monthly action.
- `/s4ag-seasons` — lock the vegetable succession into the whole-farm seasonal plan.
- Run **variety-selection** (within this skill) if the succession reveals you need early, mid, and late varieties of the same crop.

---

## Growing Calendar

*Tells you what to sow, transplant, and harvest each month for a temperate climate.*

This calendar covers a temperate climate with last frost late March to early May, first autumn frost October to November. Adjust forward (earlier) by 2–4 weeks in warmer maritime climates; backward (later) by 2–4 weeks in cold continental or upland climates. All dates are for outdoor growing unless marked (U) for under cover or polytunnel.

**Monthly guide:**

**January**
- Sow (U): onions (long-day varieties), broad beans (modules), chillies and peppers (U — need warmth and long growing season)
- Harvest: stored roots, kale, leeks, cavolo nero, overwintered salad, Brussels sprouts, parsnip

**February**
- Sow (U): tomatoes (modules, heated propagator), aubergines (modules, heat), early lettuce, spinach, peas (modules)
- Harvest: kale, leeks, cavolo nero, sprouting broccoli (early varieties), overwintered salad, chard

**March**
- Sow (outdoor, under fleece or cold frame): broad beans direct, peas direct, early carrots (under fleece), beetroot (early sowings), onions (sets), radish
- Sow (U): basil, cucumbers, courgettes, squash (modules, heat), late brassica transplants for early summer
- Harvest: sprouting broccoli, last leeks and roots, overwintered salad and spinach

**April**
- Sow (outdoor): carrots, beetroot, parsnip (latest safe date for full-size roots), Swiss chard, spinach, lettuce, spring onion, peas, French beans (warmer areas), turnip, fennel
- Transplant (outdoor after hardening): onions, leeks (module-sown), early brassicas
- Harvest: asparagus (established beds from year 3), overwintered spinach, sprouting broccoli, rhubarb

**May**
- Sow (outdoor): French beans direct, climbing beans, courgette direct (second half of month), beetroot, carrots, salad, radish, sweetcorn (second half), kale and brassica transplants for winter
- Transplant (outdoor): tomatoes (outdoor / polytunnel), courgette modules, squash, cucumber (U), peppers (U)
- Harvest: asparagus, salad, spinach, radish, early potatoes (earliest varieties from late May)

**June**
- Sow: climbing beans, beetroot, carrots, salad, turnip, kohlrabi, second courgette sowing
- Transplant: leeks (module-sown into permanent positions), winter brassica transplants (kale, sprouts, PSB, savoy)
- Harvest: broad beans (early sowings), early salads, radish, spinach, courgette (early sowings), early potatoes, strawberries

**July**
- Sow: kale for spring (late July), winter salad (lamb's lettuce, winter lettuce, spinach, chard), turnip, brassica autumn salads, pak choi
- Transplant: leeks, late brassicas
- Harvest: courgette, French beans, climbing beans, tomatoes (U), cucumbers (U), beetroot, carrots, onions (late July/August), garlic (July), peppers (U)

**August**
- Sow: overwintering spinach, lamb's lettuce, winter radish, Japanese onions (for spring), pak choi, late salad
- Transplant: spring cabbages, oriental greens
- Harvest: main-crop beans, courgette, tomatoes, cucumbers, sweetcorn, winter squash (begins ripening), peppers, aubergine, beetroot, carrots, outdoor tomatoes

**September**
- Sow (U): winter salad, baby leaf, oriental greens under cover for winter harvests
- Harvest: tomatoes (outdoor finish), squash (cut and store before first frost), sweetcorn (last), peppers, climbing beans, French beans (last), celeriac, carrots, leeks begin
- Action: plant garlic from mid-month in warmer areas; store squash and onions

**October**
- Sow: garlic cloves (main planting), overwintered broad beans (mild areas)
- Harvest: squash (store), kale, Brussels sprouts begin, PSB foliage, leeks, celeriac, parsnip, carrots (can leave in ground), last outdoor tomatoes and peppers
- Action: clear summer crops; apply compost mulch to cleared beds

**November**
- Harvest: kale, Brussels sprouts, leeks, celeriac, parsnip, stored roots, overwintered salad (U)
- Action: final compost mulch application; plan next season rotation; order seed catalogues

**December**
- Harvest: Brussels sprouts, kale, leeks, stored crops, overwintered salad (U)
- Plan: seed orders for next year; rotation; infrastructure improvements for next season

**Checkpoint — confirm before finalising:**
- What is the USDA hardiness zone or the approximate last / first frost dates for this location? The calendar above assumes a UK/northern European temperate climate or equivalent.
- Is there a polytunnel or cold frames available? Many of the (U) sowings require frost protection.
- What crops are actually being grown? The full calendar is a reference, not a to-do list.

A calendar given without climate adjustment for a grower in zone 9 or zone 4 will give wrong sowing dates and produce crop failures.

**Output:**
```
GROWING CALENDAR — [Month] / [Location / Climate zone]

THIS MONTH
Sow now:
  [Crop] — [method: direct / modules] — [location: outdoor / U]
Transplant:
  [Crop] — [from where] — [spacing]
Harvest:
  [Crop] — [notes on readiness]

COMING NEXT MONTH
Prepare for: [upcoming key tasks]

OVERDUE / AT RISK
[Anything that should have been sown and wasn't — and whether there's a recovery option]
```

**Next steps:**
- Run **succession-planning** (within this skill) to ensure each month flows into the next without gaps.
- `/s4ag-seasons` — integrate the vegetable calendar into the whole-farm year.
- Run **problem-diagnosis** (within this skill) if a current crop in the calendar is not performing.

---

## Problem Diagnosis

*Identifies the cause of a crop failure or underperformance and recommends a response.*

Before reaching for any input — biological, organic, or chemical — diagnose the cause. Most vegetable crop problems have a structural root cause that the intervention will not address. Treating symptoms prolongs the problem.

**Step 1: Characterise the symptom precisely.**

Work through these questions:
1. Which crop and which variety?
2. What part of the plant is affected (roots, leaves, stems, fruit)?
3. How widespread is it — one plant, one bed, one area, whole crop?
4. When did it appear and how fast is it spreading?
5. What are the weather conditions been — wet, cold, hot, drought?
6. What was in this bed last season?

**Step 2: Match symptom pattern to cause category.**

| Symptom pattern | Most likely cause category |
|---|---|
| Uniform yellowing of whole plant | Nitrogen deficiency or waterlogging |
| Interveinal yellowing (green veins, yellow between) | Iron or manganese deficiency; usually pH-related |
| Purple / red discolouration of leaves | Phosphorus deficiency; cold soil temperature |
| Wilting despite moist soil | Root rot (Pythium, Phytophthora) or clubroot |
| Stunted growth, all plants affected equally | Low OM / poor food web; pH problem; compaction |
| Patches of poor growth tracking drainage | Compaction or waterlogging |
| Rapid collapse of individual plants | Damping-off (seedlings) or root lesion nematodes |
| Holes in leaves, visible caterpillars or slugs | Pest feeding — threshold assessment needed |
| Grey mould on stems and leaves | Botrytis — air circulation and humidity problem |
| White powdery coating on leaves | Powdery mildew — variety susceptibility or stress |
| Dark lesions on leaves, wet conditions | Blight (early or late) — variety or spray programme |
| Bolting (premature flowering) | Temperature, day length, or variety mismatch |
| Poor germination | Soil too cold / wet / compacted; old or poor seed |
| Blossom drop (tomatoes, peppers) | Temperature stress or irregular watering |

**Step 3: Apply the Ingham lens before acting.**
Before any spray or amendment: is this a food web problem? Crops grown on low-biology soils are more susceptible to almost every problem in the table above. If the problem is widespread and the soil has a history of tillage and synthetic inputs, the answer may not be a spray but a soil programme.

**Step 4: Decide on response — immediate and structural.**
Every problem diagnosis has two responses:
- **Immediate:** stop the damage now.
- **Structural:** prevent recurrence through the system.

| Problem | Immediate response | Structural response |
|---|---|---|
| Slug damage | Iron phosphate pellets or physical barriers | No-dig mulch; reduce slug habitat; encourage ground beetles |
| Aphids | Soft soap spray; remove with water jet | Increase beneficial habitat; reduce high-N fertility |
| Botrytis | Remove affected material; improve ventilation | Increase plant spacing; reduce overhead watering |
| Damping off | Improve drainage; reduce overhead watering | Better air circulation; drench with dilute compost tea |
| Powdery mildew | Potassium bicarbonate spray (organic) or sulphur | Resistant variety next season; improve air circulation |
| Blight (late) | Remove and destroy affected material | Resistant variety; avoid overhead water; copper (conventional) |
| Nitrogen deficiency | Liquid feed (fish / compost tea) | Improve OM; cover crop rotation; compost addition |
| Clubroot | No immediate remedy — remove and destroy crop | pH above 7.2; strict rotation (7+ years out of brassicas); resistant variety |
| Bolting | Harvest immediately if edible; remove if not | Correct variety for season; shade in heat |

**Checkpoint — confirm before finalising:**
- What is the exact symptom and which part of the plant? The diagnosis table cannot work on a vague description.
- How widespread is it — one plant or the whole bed? One plant is often random; whole beds and patches have structural causes.
- What is the growing system — tilled or no-dig? Low-dig systems have different disease dynamics (less damping-off, more slug habitat in mulch).

Diagnosing from an incomplete symptom description produces the wrong recommendation. If the symptom description is vague, ask for more detail before diagnosing.

**Output:**
```
PROBLEM DIAGNOSIS — [Crop] / [Symptom]

SYMPTOM SUMMARY: [description of what was reported]

MOST LIKELY CAUSE: [cause] — [confidence: high / moderate / possible]
ALTERNATIVE CAUSES: [list if multiple possibilities]

IMMEDIATE RESPONSE
Action: [what to do now]
Product / material: [specific recommendation]
Timing: [when to act]

STRUCTURAL RESPONSE
Prevent recurrence by: [system change]
Timeline: [this season / next season / multi-year]

FOOD WEB NOTE: [whether soil biology is relevant to this problem and what to do]

IF THIS DIAGNOSIS IS WRONG: [what to look for that would change the diagnosis]
```

**Next steps:**
- `/s4ag-pests` — for full IPM decision methodology on pest and disease problems.
- `/s4ag-soil` — if the diagnosis points to soil biology or mineral deficiency as the root cause.
- Run **intensive-systems** (within this skill) if the structural response involves system change.

---

## Intensive Systems

*Designs and manages permanent bed systems — no-dig, broadfork, and the market garden approach — for maximum productivity and soil health.*

The intensive permanent bed system is the foundation of productive small-scale vegetable growing. Its logic: beds are formed once, never walked on again, and managed from fixed paths. Soil structure accumulates. Biology builds. Weed pressure drops year on year. Output per square metre exceeds conventional row-cropped systems within two to three seasons.

**System design:**

**Bed dimensions:**
- Width: 75–90cm (reachable from both sides without stepping on the bed).
- Length: practical for your site — 3m, 6m, 9m, or 12m are common. Longer than 12m becomes awkward to walk around.
- Paths: 30–45cm between beds; wider (60cm) on every 4–5 bed border for wheelbarrow access.

**Orientation:**
- North-south orientation maximises light distribution on taller crops.
- On slopes, run beds across the slope (on contour) to prevent erosion and retain moisture.

**Establishing new beds (no-dig method):**

1. Mow or strim existing vegetation to as short as possible.
2. Lay cardboard (removing tape and staples) directly on vegetation, overlapping edges by 20cm.
3. Apply a 10–15cm layer of well-rotted compost or compost/woodchip mix on top of the cardboard.
4. Mark paths with woodchip or another permanent mulch.
5. Plant or sow immediately into the compost layer — no waiting required.
6. The cardboard suppresses existing vegetation; it breaks down within 4–6 months.

The cardboard-and-compost method works even on heavy grass or light scrub. For dense perennial weeds (docks, bindweed, couch grass), use a 20cm compost layer and a 12-month establishment period before planting.

**Annual bed management (no-dig):**

1. **Clear:** Remove spent crops without pulling or turning. Cut stems at soil level; leave roots to break down in the soil.
2. **Top-dress:** Apply 5–7cm of well-rotted compost or manure (not fresh) to the bed surface after clearing, before the next crop.
3. **Sow or transplant:** Directly into the top-dressed surface.
4. No cultivation, no digging, no turning. The worms and biology do the incorporation.

**Soil biology under this system:**
In a no-dig system with annual compost top-dressing, fungal networks develop across seasons. The Ingham lens: repeated tillage resets soil succession; permanent beds allow it to accumulate. Within 3–5 years of no-dig management, aggregate structure, earthworm populations, and fungal hyphae density are measurably superior to cultivated beds. The practical outcome: better water retention, better disease resistance, and less fertility input required.

**The broadfork alternative:**
Some growers use a broadfork (a two-handled fork with long tines, pressed into the bed by foot) to loosen compacted subsoil without inverting soil layers. This is not tillage — it opens channels without mixing horizons. Use once per season on beds that show compaction; not on beds with good structure.

**Rotation within the permanent bed system:**

Maintain a four-group rotation minimum:
1. Brassicas (cabbages, kale, broccoli, cauliflower)
2. Roots (carrots, parsnip, beetroot, onions, leeks)
3. Legumes (peas, beans) with salads and lettuces
4. Solanums and tender crops (tomatoes, courgette, cucumber, squash)

Mark rotation on a bed plan and move each group forward one position each year. Never grow brassicas in the same bed more frequently than every four years — clubroot will become established and there is no practical remedy once it is.

**Conventional comparison and transition:**

Conventionally tilled beds can transition to no-dig in a single season. Apply the cardboard and compost method on top of cultivated ground. The key shift in mindset: fertility comes from compost added to the surface, not from incorporating materials by tillage. If compost quality is sufficient (fully decomposed, earthy-smelling, dark), the system works immediately.

A grower used to synthetic fertility can transition gradually: begin no-dig management while maintaining existing fertiliser programme; reduce synthetic inputs by 25–30% per year as compost additions build the food web; within 3–4 years, most synthetic inputs can be eliminated if compost quality and quantity is sufficient.

**Tools for the intensive system:**

| Tool | Purpose |
|---|---|
| Wire rake | Level compost top-dressings; draw seed drills |
| Collinear hoe | Precision weeding in tight spacings |
| Stirrup hoe | Fast path and inter-row weed management |
| Broadfork | Subsoil aeration without inversion (as needed) |
| Wheel hoe | High-speed weeding in wider row crops |
| Long-handled dibber | Transplanting modules quickly at correct spacing |

**Checkpoint — confirm before finalising:**
- What is the current state of the growing area — existing cultivated beds, grass, or something else? This determines whether the cardboard-and-compost establishment method applies or whether existing infrastructure is being adapted.
- Is the user willing and able to source compost in the quantities needed (approximately 1 cubic metre per 10 square metres per year for top-dressing)?
- Conventional or organic/no-dig transition? A grower not ready to shift to no-dig needs a tilled-bed system managed as well as possible — not a lecture on why no-dig is better.

Recommending a no-dig system to someone who cannot source compost in adequate quantities produces a system that fails — and the failure gets attributed to no-dig rather than to the missing compost.

**Output:**
```
INTENSIVE SYSTEM PLAN

CURRENT SITUATION: [existing setup]
TARGET: [number of beds / total area]

BED LAYOUT
Number of beds: [number]
Bed size: [width x length]
Path width: [standard / wide for access]
Total productive area: [m2]

ESTABLISHMENT METHOD
[cardboard-and-compost / adapt existing beds / other]
Materials needed: [compost volume required — m3]
Estimated cost: [£/$ for materials]
Timeline: [weeks to plant-ready]

ROTATION PLAN
Group 1 (Brassicas): Beds [list]
Group 2 (Roots): Beds [list]
Group 3 (Legumes + salad): Beds [list]
Group 4 (Solanums + tender): Beds [list]
Rotation direction: [clockwise / forward — describe]

ANNUAL BED MANAGEMENT
Compost required per year: [m3]
Source: [on-farm / purchased]

TOOLS NEEDED: [list of any gaps in current toolkit]
```

**Next steps:**
- `/s4ag-composting` — the intensive system runs on compost; build the supply before scaling the system.
- `/s4ag-soil` — baseline the soil biology and minerals before the first season to track improvement.
- Run **succession-planning** (within this skill) to fill the beds once the system is established.
