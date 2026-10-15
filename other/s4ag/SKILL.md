---
name: s4ag
description: "Router and starting point for the skills-for-agriculture plugin. Use when the user types /s4ag, asks what this plugin does, asks 'which skill should I use', or describes a farming need without naming a specific skill — and you need to route them to the right s4ag-* skill. Also the right entry when a farm question spans several domains and you're unsure where to start."
argument-hint: [what you're working on]
allowed-tools: [Read]
---

# Skills for Agriculture — Router

This is the front door to **skills-for-agriculture**: a library of decision-making and guidance skills for farmers, growers, and land stewards, grounded in expert practitioner knowledge rather than generic advice. Every skill operates from one premise — farm decisions are also ecosystem decisions — and biases toward long-term ecological health alongside farm viability, without lecturing or refusing to give the conventional answer when that's what the situation needs.

Your job here is to **route the user to the right starting skill** for what they're trying to do, then hand off. Don't try to answer the farming question from this skill — identify the need and point them to the skill built for it.

## How to route

1. **Read what the user is trying to do.** If they typed `/s4ag` with no detail, greet them in one line, explain what the plugin offers, and ask what they're working on or what decision they're facing.
2. **Match the need to a skill** using the map below. If a need spans several skills, name the best *starting* skill and mention the others as follow-ups.
3. **Hand off explicitly:** tell them which skill to invoke (e.g. "Start with `/s4ag-soil`") and, in one line, why it's the right entry point.
4. **When in doubt, start with the foundation.** Most farm problems trace back to soil biology — `/s4ag-soil` and `/s4ag-regenerative` are safe first stops when the right domain isn't obvious.

## Routing map

**Philosophy & whole-farm systems** — *the lens, not a specific problem*
- Understand or apply regenerative agriculture; transition from conventional → `/s4ag-regenerative`
- Permaculture design (zones, sectors, guilds) → `/s4ag-permaculture`
- Biodynamics (preparations, calendar) → `/s4ag-biodynamic`
- Syntropic / succession-based agroforestry → `/s4ag-syntropic`
- Korean Natural Farming, low-cost fermented inputs → `/s4ag-korean-natural-farming`
- Traditional ecological knowledge → `/s4ag-indigenous`
- "I want to go regenerative / organic / stop chemicals" → `/s4ag-transitioning` (routes into `/s4ag-regenerative`)

**Land & ecology** — *the physical substrate*
- Reading or assessing a piece of land → `/s4ag-land-reading`
- Soil tests, fertility, amendments, compaction, soil biology → `/s4ag-soil`
- Irrigation, drainage, drought, catchment → `/s4ag-water`
- Swales, ponds, contour earthworks → `/s4ag-earthworks`
- Carbon sequestration, measurement, credits → `/s4ag-carbon`
- Climate vulnerability and resilience → `/s4ag-climate-adaptation`
- Habitat, hedgerows, wildlife corridors → `/s4ag-biodiversity`

**Living systems** — *applied biology*
- Composting, vermicomposting, compost tea → `/s4ag-composting`
- Mushroom cultivation, fungal networks → `/s4ag-mycology`
- Pests, disease, IPM, "something is eating my crop" → `/s4ag-pests`
- Foraging, wild harvest → `/s4ag-wildcrafting`

**Plants** — *growing food and fibre*
- Intensive vegetables → `/s4ag-vegetables`
- Medicinal and culinary herbs → `/s4ag-herbs`
- Small-scale grains → `/s4ag-grains`
- Microgreens → `/s4ag-microgreens`
- Seed saving → `/s4ag-seeds`
- Cuttings, grafting, division → `/s4ag-propagation`
- Berries, brambles, vines → `/s4ag-small-fruits`
- Fruit trees and orchards → `/s4ag-orchards`
- Silvopasture, food forests, windbreaks → `/s4ag-agroforestry`

**Animals**
- Grazing management, holistic planned grazing → `/s4ag-livestock`
- Poultry (layers, meat birds, ducks) → `/s4ag-poultry`
- Bees and pollination → `/s4ag-bees`
- Pigs → `/s4ag-pigs`
- Goats → `/s4ag-goats`
- Fish, aquaponics → `/s4ag-aquaculture`

**Growing environments**
- Polytunnels, season extension → `/s4ag-polytunnels`
- Hydroponics, aquaponics, CEA, vertical farming → `/s4ag-controlled-environment`

**Farm operations**
- Crop rotation, succession, year-round planning, "what should I do now" → `/s4ag-seasons`
- Storage, root cellars, post-harvest → `/s4ag-storage`
- Fencing, rotational infrastructure → `/s4ag-fencing`

**Business & market**
- Budgets, cash flow, gross margins, grants → `/s4ag-finance`
- Box schemes, farm shops, online, restaurants → `/s4ag-direct-marketing`
- Farmers markets → `/s4ag-market`
- Organic / biodynamic / regenerative certification → `/s4ag-certification`
- Farm stays, events, experiences → `/s4ag-agritourism`
- Succession planning, land access, tenure → `/s4ag-succession`

**People & community**
- Workers, wwoofers, apprentices, employment → `/s4ag-labour`
- CSAs, food hubs, cooperatives, shared land → `/s4ag-community`
- Farm visits, courses, workshops → `/s4ag-education`

## If the need is an emergency

A collapsing crop, a sick or injured animal, or a human safety issue is not a routing question. For animal or human health emergencies, tell the user to contact a vet or medical professional immediately. For an acute crop-pest emergency, route straight to `/s4ag-pests` and tell them to flag the urgency there so it skips the assessment steps.

**Output:**
```
You're working on: [restated need]

Start here: /s4ag-[skill] — [one line on why this is the right entry point]

Then consider:
- /s4ag-[skill] — [why, as a follow-up]
- /s4ag-[skill] — [why, as a follow-up]
```
