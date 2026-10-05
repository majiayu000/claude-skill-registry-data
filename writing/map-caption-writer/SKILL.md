---
name: map-caption-writer
description: "Writes a precise, context-rich caption for a published map that tells readers what geographic area is shown, what the map is measuring or illustrating, and why it matters to the story."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [caption, map, geography, visual journalism, location, articles]
---
# Map Caption Writer

## What This Skill Does
Writes a precise, context-rich caption for a published map that tells readers what geographic area is shown, what the map is measuring or illustrating, and why it matters to the story.

## When To Use This Skill
- A map is ready for publication in print or digital and needs an accompanying caption
- A locator map, data map, or route map will appear alongside an article and the relationship between the visual and the story needs to be made explicit
- The map covers an area many readers may not recognise, requiring orientation
- A map shows change over time (e.g., territorial shifts, migration routes, flood extent) and the before/after needs to be explained in text
- A social media post will include a map image and needs a standalone caption that works without the full article

## What You Need To Provide
**Required:**
- What geographic area the map covers (country, region, city, or specific zone)
- What the map is showing (locations of events, a data variable by area, a route, a boundary change, a risk zone, etc.)
- Why this is relevant to the story (one sentence of editorial context)

**Optional:**
- Key locations, labels, or markers on the map that you want the caption to reference
- Data source or cartographic source if the map uses a specific dataset
- Time period the map represents (especially important for historical or change-over-time maps)
- Preferred length (short: one sentence; standard: two sentences; extended: three to four sentences for complex geographic context)

## How the Assistant Approaches This
1. Opens by orienting the reader geographically — naming the area shown and anchoring it relative to a recognisable reference point if the location may be unfamiliar to the target audience
2. States clearly what the map is measuring or illustrating and what the most significant geographic pattern or finding is (not a neutral description, but the editorial point the map makes)
3. Adds source attribution and any essential note about time period, projection, or data boundary that a reader needs to interpret the map correctly

## Output Format
One to three sentences plus an optional source line, totalling 25–70 words for standard captions. Lead sentence orients and names the phenomenon. Second sentence (if used) gives the editorial significance or describes the most important feature shown. Source line on a new line if a data source or map provider should be credited. No headline. Neutral, informative tone — no dramatic or promotional language. Specific place names over vague references.

## Quality Criteria
- [ ] The geographic area is named and, where needed, anchored with a recognisable reference point
- [ ] The caption states what the map shows, not just what type of map it is ("a shaded relief map of...")
- [ ] The most important geographic finding or pattern is named explicitly
- [ ] Time period is specified if the map represents a specific moment or range
- [ ] The caption can stand alone — a reader who cannot see the map still understands the editorial point
- [ ] No redundancy with labels or titles already visible on the map face

## Example

### Input
Geographic area: The Salcedo River delta region in the fictional country of Maraverde, in the southern hemisphere
What the map shows: Areas of the delta that have been flooded in each of the past three rainy seasons, shown as overlapping shaded zones. Each season is a different colour. The map also marks the locations of six villages that fell within flood zones in at least two of the three seasons.
Editorial context: Part of an investigation into why disaster relief funding has not reached repeatedly affected communities
Data source: Regional Hydrological Authority, seasonal flood reports 2023–2025

### Output
The Salcedo River delta, in southern Maraverde, has flooded in the same communities in each of the past three rainy seasons — a pattern that officials acknowledge but that has yet to trigger sustained relief funding. Six villages (marked) fell within designated flood zones in at least two of the three seasons shown, with the 2025 flood extent (darkest shading) reaching its largest recorded boundary.

Source: Regional Hydrological Authority, seasonal flood reports 2023–2025

## Known Limitations
- This skill cannot read map image files — you must describe what the map shows; a vague description will produce a vague caption
- For maps covering areas likely to be unfamiliar to the publication's readership, you should specify a reference point ("in the northwest of the country, bordering X") in your input rather than leaving orientation entirely to the skill
- Does not advise on map design, projection choices, or colour accessibility — those are art direction decisions
- Highly technical maps (bathymetric, actuarial, satellite-composite) may need an additional methodology note that falls outside standard caption length; flag this and request an extended caption

## Related Skills
- [infographic-caption-writer](../infographic-caption-writer/SKILL.md)
- [location-brief-writer](../../../tv-documentary/pre-production/location-scout-brief/SKILL.md)
- [sidebar-fact-box-writer](../../../magazine-journalism/writing/sidebar-fact-box-writer/SKILL.md)
