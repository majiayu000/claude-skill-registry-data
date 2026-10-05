---
name: one-sheet-writer
description: "Produces a single-page sales document for a completed or nearly completed documentary, formatted for use at festival markets, in distributor meetings, and in international sales conversations."
status: stable
category: tv-documentary
subcategory: business
version: 1.0
eval_score: 4.5
tags: [documentary, business, sales, distribution, festival, one-sheet]
---
# One Sheet Writer

## What This Skill Does
Produces a single-page sales document for a completed or nearly completed documentary, formatted for use at festival markets, in distributor meetings, and in international sales conversations.

## When To Use This Skill
- Your documentary is complete or in late post-production and you need a leave-behind document for distribution meetings
- You are attending a festival market (Cannes Docs, IDFA Market, Hot Docs Forum) and need a professional sales one-sheet
- A distributor or sales agent has asked for a one-sheet before deciding whether to screen the film
- You need to update your one-sheet with new festival credits or awards

## What You Need To Provide
**Required:**
- Film title and tagline (or ask the assistant to draft a tagline from your description)
- Runtime and completion/release year
- A description of the film (2–4 sentences is enough)
- Director name and production company
- Genre and target audience (e.g., "feature documentary, broad theatrical/SVOD audience")

**Optional:**
- Festival selections and awards (list them all — the assistant will format and prioritize)
- Broadcaster or platform acquisitions already made
- Key reviews or critical quotes (include the full quote and the publication name)
- Distribution or sales agent already attached
- Website URL or contact email
- Country of production and language
- Key financiers or funders to credit (if required by their agreement)

## How the Assistant Approaches This
1. Leads with the film's visual identity in text: title formatted prominently, tagline (or a generated one) immediately beneath, followed by the key technical specs in a single line
2. Writes the film description as a two-paragraph sales synopsis — first paragraph establishes the story and characters, second paragraph positions the film's emotional and editorial impact and its audience
3. Formats festival selections and awards as a clean, visually organized list, prioritizing the most prestigious entries and any prizes won
4. Adds a critical quotes block if quotes are provided, selecting the most specific and credible ones (avoids generic superlatives)
5. Closes with a credits and contact block: director, producer, production company, sales agent or distributor (if any), contact information

## Output Format
- Length: one page worth of content (approximately 300–400 words of body text, plus formatted credits and awards blocks)
- Structure: Title / Tagline / Specs → Film Description (2 paragraphs) → Festival & Awards → Critical Quotes (if available) → Credits → Contact
- Tone: editorial and assured — a one-sheet reads like a confident press release, not a pitch
- Formatting: designed for a designer to drop into a visual layout; clean section labels, no unnecessary punctuation or decoration
- All blocks clearly labeled so a designer knows where each element sits on the page

## Quality Criteria
- [ ] The tagline is one sentence that captures the film's emotional or thematic core — not a logline and not a genre descriptor
- [ ] The film description is specific enough to distinguish this film from any other documentary on a similar subject
- [ ] Festival selections are formatted with year and award tier (Competition, Special Presentation, World Premiere) where available
- [ ] If critical quotes are included, each quote is attributed to a named critic and named publication — no anonymous praise
- [ ] The contact block includes at minimum a company name and either an email or a URL

## Example

### Input
- **Title:** The Weight of Salt
- **Runtime:** 82 minutes · **Year:** 2025
- **Description:** A documentary following a salt harvester on a remote Sicilian island over the course of one season — the last member of a family that has worked the same salt flats for five generations. The film is shot almost entirely in silence, following the rhythm of manual labor and the changing light across the flats.
- **Director:** Elena Ferrante-Russo *(fictional name for this example)*
- **Production company:** Terra Viva Films
- **Genre:** Feature documentary
- **Target audience:** Art-house theatrical, international festival audience
- **Festival selections:**
  - IDFA 2025 — International Competition (World Premiere)
  - CPH:DOX 2026 — Nordic:DOX Competition
  - Hot Docs 2026 — World Showcase
- **Awards:** IDFA — Special Jury Award for Cinematography
- **Critical quotes:**
  - "A film of extraordinary patience and visual precision." — *Sight & Sound*
  - "One of the most quietly devastating documentaries of the year." — *The Hollywood Reporter*
- **Contact:** contact@terraviva.it · www.terraviva.it

### Output

---

**THE WEIGHT OF SALT**
*The last harvest.*

82 min · Documentary · 2025 · Terra Viva Films · Italy

---

**THE FILM**

On a remote Sicilian island, a single man harvests salt by hand from the same flats his family has worked for five generations. He may be the last. *The Weight of Salt* follows one complete season on the flats — from the first flooding of the basins in spring to the final harvest in late summer — in a film that unfolds almost entirely without words, at the pace of the labor itself.

Shot over eight months with a single cinematographer and no crew larger than three, the film is a study in what endures when an economy, a technology, and a way of life have all moved on. Its subject is the salt. Its real subject is time.

---

**FESTIVAL SELECTIONS & AWARDS**

IDFA 2025 · International Competition · World Premiere
**IDFA Special Jury Award — Cinematography**

CPH:DOX 2026 · Nordic:DOX Competition

Hot Docs 2026 · World Showcase

---

**CRITICAL RECEPTION**

*"A film of extraordinary patience and visual precision."*
— Sight & Sound

*"One of the most quietly devastating documentaries of the year."*
— The Hollywood Reporter

---

**CREDITS**

Director: Elena Ferrante-Russo
Producer: [Producer name]
Production Company: Terra Viva Films
Country of Production: Italy
Language: Italian / No Dialogue

Sales & Distribution enquiries: contact@terraviva.it
www.terraviva.it

---

## Known Limitations
- The assistant cannot verify that festival credits are formatted according to the specific conventions preferred by each festival — for official festival catalogues, check with the festival's sales & industry office for their preferred credit line format
- If the film has no festival history yet (pre-release), the one-sheet will rely entirely on the film description and creative credits; this is a weaker document and the assistant will flag this
- Tagline quality depends heavily on the description provided — a flat or vague description will produce a weak tagline; the more specific the input, the stronger the tagline
- This skill produces copy for a one-sheet layout; actual design (typography, image placement, visual identity) requires a graphic designer working from this copy

## Related Skills
- [broadcaster-pitch-writer](../broadcaster-pitch-writer/SKILL.md)
- [press-kit-generator](../../post-production/press-kit-generator/SKILL.md)
- [festival-synopsis-writer](../../localization/festival-synopsis-writer/SKILL.md)
- [logline-creator](../../development/logline-creator/SKILL.md)
