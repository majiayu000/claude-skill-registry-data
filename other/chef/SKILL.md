---
name: chef
description: Weekly nutrition-variety advisory built from a photo-logged meal history. Reports distinct plant count, protein rotation, and absent food groups. Use when running the chef-weekly heartbeat, or when asked about eating variety, plant diversity, or meal monotony.
---

# Skill: chef (weekly nutrition-variety advisory)

**Use when:** the `chef-weekly` heartbeat fires, or someone asks about their
eating variety, plant diversity, or meal monotony.

**One-line scope:** a weekly, observational **variety** report built from
photo-logged meals. It reports what was eaten. It never reports what anyone is.

## What v1 does - the defensible core

1. **Plant count.** Distinct plant species over the trailing window against a target of 30, per the American Gut Project (McDonald 2018, mSystems, n approximately 10,000: 30+ distinct plants per week associates with greater gut-microbial diversity than 10 or fewer). A COUNT is immune to the portion-estimation error that kills photo-derived micronutrient math - grams do not change whether a leek was eaten.
2. **Variety and rotation.** Protein and headline-dish frequency, flagging monotony and suggesting rotation. Framed as variety and interest, which is the thing that actually drives adherence.
3. **Gap board.** Food groups absent from the window, ranked by how easy each is to add. An observation about the log, never a claim about a body.
4. **Next week's shape.** Three to five concrete, locally available suggestions, one of them a New Plant of the Week - a species not seen in the window.

## Hard refusals - encode these, never cross them

- **Never diagnose or hint at a deficiency.** Not "you may be low in X", not "you could be short on X". That word requires bloodwork.
- **Never recommend a supplement**, by dose, brand, or in general.
- **Never recommend a calorie target, a deficit, or a weight-loss protocol.**
- **Never construct a restriction, elimination, or fasting protocol.**
- **Never assert a physiological state from food** - not microbiome composition, not inflammation, not micronutrient status.
- **Never do micronutrient, vitamin, or deficiency quantification.** Deliberately deferred: per-item portion grams are produced by an equal-split heuristic, so any nutrient figure derived from them is a division wearing a lab coat.
- **Never frame low-mercury fish repetition as a mercury problem.** Salmon at roughly 0.022 ppm is about 7x below the FDA 0.15 ppm Best Choices threshold; cod and shrimp likewise. Their repetition is a VARIETY point only. The mercury frame is legitimate ONLY for genuinely high-mercury species (swordfish, tuna, king mackerel, shark, marlin) recurring three or more times, and even then with the real ppm attached.

These are not stylistic preferences. This skill reads a food diary and talks
back about it, which is exactly the shape of a tool that drifts into clinical
claims it has no basis for. The refusals are the reason it is safe to run
unattended.

## Where the pieces live

| Piece | Path | Purpose |
|---|---|---|
| Gate | `scripts/gather-chef-weekly.sh` | Fires only on the report day, with enough logged days, once per ISO week |
| Analyzer | `scripts/chef_plant_count.py` | Deterministic mapping and counts |
| Taxonomy | `data/plant-taxonomy.json` | Free text to canonical species, non-plant list, FDA high-mercury table |
| Prompt | `scheduled-tasks/chef-weekly-prompt.md.template` | The heartbeat prompt |
| State | `<state_dir>/chef-weekly-state.json` | ISO-week dedup |

Extend the `plants` map as new foods show up. `unresolved_tokens` in the
analyzer output is the candidate list.

## Data dependency

This skill reads the meal tables written by the companion food-logging plugin
(`bfl_meals`, `bfl_days` by default, overridable via `meals_table` and
`days_table`). It writes nothing back. Without that plugin, or an equivalent
schema, there is nothing to count.

## Reading the number honestly

**Report `distinct_plant_count` as it comes back. Do not adjust it upward.**

The taxonomy has been corrected once already for exactly this: it was counting
red onion and green onion as two species, romaine and iceberg and "mixed greens"
as three, and "mixed vegetables" as a plant despite naming no species. The
result was consecutive weeks reporting above target against a log that showed
the target reached once in four months.

An inflated counter is a participation trophy. If the number jumps because
something changed in the taxonomy or the parser, say which change caused it
rather than letting it read as progress.

## Standing footer on every chef report

> Observational. Built from photo-logged meals with substantial portion error.
> Reports what was logged, not nutritional status. Nothing here is medical advice -
> for anything about deficiency, supplements, or targets, that is a doctor and a
> blood panel.

## Escalation - the only one

If the log shows a genuinely stark pattern, such as a food group absent for 30
or more days, state the observation and suggest raising it at the next routine
medical visit. Do not name a nutrient. Do not prescribe a fix.

## Deliberately deferred

Do not build these without an explicit decision:

- **Micronutrient and vitamin quantification** - blocked on per-item portion truth.
- **Deficiency inference** - permanently out. Requires bloodwork.
- **Microbiome composition claims** - not measured by a food log.
- **Recipe generation and meal scheduling** - only after the counts are trusted.
