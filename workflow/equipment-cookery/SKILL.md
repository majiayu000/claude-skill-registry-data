---
name: equipment-cookery
description: Plan, adapt, troubleshoot, and safety-gate cooking around kitchen equipment, appliances, vessels, heat transfer, capacity, airflow, pressure, microwaves, slow cookers, and tool substitutions.
license: MIT
---

# Equipment Cookery

## Core Workflow
1. Identify the food, target result, equipment available, missing equipment, vessel size/material, heat source, direct-heat exposure, batch size, fill level, airflow, lid/pressure/steam state, altitude, and safety-sensitive ingredients.
2. Run a safety preflight for raw animal products, reheating, holding, pressure canning, slow cookers, microwaves, grills, air fryers, broilers, damaged equipment, incompatible vessels, and missing time-temperature facts.
3. Separate equipment feasibility from culinary quality and food safety. Do not let a tool substitution override thermometer, tested-process, or manufacturer constraints.
4. Map the equipment constraint to the mechanism: heat capacity, surface area, conductivity, radiant heat, airflow, moisture evaporation, steam capture, pressure, agitation, cold spots, recovery time, altitude, or batch sequencing.
5. Recommend practical adjustments: smaller batches, alternate vessels, rack position, preheating, heat-zone changes, lid changes, stirring, rotation, standing time, thermometer checks, longer altitude timing, or a different method.
6. Lead with the decision or highest-leverage equipment change before explaining the mechanism.

## Equipment Guidance
Use `equipment-cookery` when equipment choice, appliance behavior, vessel geometry/material, fill level, surface area, airflow, pressure, microwave heating, slow cooker behavior, or tool substitution drives the result.

For browning and roasting, diagnose crowding, surface moisture, pan material/color, rack position, airflow, preheat, and batch size before changing temperature.

For stovetop substitutions, account for pan diameter, heat retention, burner power, ingredient moisture, batch order, and recovery time between additions.

For ovens, broilers, grills, and air fryers, distinguish radiant heat, convective airflow, surface exposure, rack/basket load, fat flare-ups, smoke risk, and vessel compatibility before changing time or temperature.

For induction, diagnose pan compatibility, pan thickness, hot-spot behavior, burner cycling, response speed, and pan-to-burner size match before changing a recipe formula.

For microwaves, treat uneven heating and cold spots as expected risks. Include covering, stirring, rotating, standing time, and thermometer verification when safety or reheating matters.

For slow cookers, include fill level, lid discipline, thawed ingredients, liquid/steam, high-first-hour or recipe-specific heating guidance, and thermometer checks when meat or poultry is involved.

For pressure cooking and canning, distinguish pressure cookers, electric multi-cookers, and pressure canners. Account for foaming foods, max fill, vent blocking, altitude adjustments, and release method. Do not convert canning processes between equipment types or imply low-acid canning is safe without tested pressure-canner guidance.

For damaged or incompatible vessels, treat physical hazard as a safety issue. Do not recommend broilers, stovetops, grills, toaster ovens, or other direct heat for vessels whose use instructions exclude direct heat. Do not keep using cracked, chipped, or deeply scratched glassware.

Route to `food-safety` when equipment advice touches raw animal products, reheating leftovers, holding temperatures, pressure canning, slow cookers, microwaves with potentially underheated food, grills or air fryers with raw meat or poultry, damaged/incompatible equipment, or uncertain time-temperature history.

## Output Contract
- Food, target result, and equipment constraint
- Safety gate and missing equipment/time-temperature facts
- Equipment state: vessel size/material, heat source, direct-heat exposure, fill level, airflow, lid/steam/pressure, altitude, and batch size
- Mechanism behind the result or risk
- Practical equipment adjustment or substitution path
- Thermometer, timing, standing, holding, or tested-process guidance when safety matters
- Verification cues for safety and quality
- Refusal of unsafe equipment substitutions when needed
- Manufacturer or authoritative-source boundary when vessel compatibility, pressure behavior, preservation, or high-risk equipment use is uncertain

## References
- Read `references/equipment-cookery-checklist.md` when appliances, vessels, heat transfer, capacity, pressure, microwaves, slow cookers, or equipment substitutions drive the culinary decision.
