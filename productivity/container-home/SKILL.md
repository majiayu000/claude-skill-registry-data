---
name: container-home
description: Answer questions, assist with planning, and help with design decisions for Mick's off-grid shipping container lake home project. Trigger when the user mentions the container home, lake home, Stewart County, LBL, the expansion, solar system, septic permitting, or retirement property.
version: 1.1.0
---

# Container Home

## Do Not Use When

- Do not use as a substitute for licensed engineering, permitting, electrical, structural, septic, or legal signoff.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

Use this skill when the user is asking about Mick's off-grid shipping container lake home at Land Between the Lakes near Dover, Tennessee.

## Trigger When

- The user mentions the container home, lake home, container house, or container expansion
- The user mentions Stewart County, Dover TN, or LBL
- The task involves solar, septic permitting, water, off-grid systems, welding, fabrication, or layout decisions for this property
- The user wants project-aware Facebook post copy about the build

## Intent

Provide project-specific context and guidance for the current build, the planned expansion, and the broader retirement-property strategy without making the user restate the full background every time.

## Current Structure

- Two 40-foot high cube containers welded side by side
- Current living area is about 640 square feet
- The right wall and back wall are underground and reinforced with H-beams
- The structure is livable now and used as a weekend retreat
- Construction has been almost entirely owner-built and mostly solo

## Systems

- Solar: 500W+ array, 4x105Ah battery bank, 2000W Renogy inverter, 12V distribution
- Planned solar upgrade: 15 kW for full-time residence use
- Water: own water supply on the property
- Waste: incinerator commode currently, no septic system yet
- Interior: framing, cedar finish, plumbing rough-in, propane refrigerator, and related work already underway

## Expansion Plan

- Two additional 40-foot containers will expand the main living area to about 1,280 square feet
- A third container is planned as a gym on the other side of the deck
- An additional container is planned for storage expansion
- Septic permitting in 2026 is a critical path item before full-time occupancy
- The long-term goal is a full-time retirement residence, not a rental or flip

## Retirement Context

- The property is part of an early retirement plan built around geographic arbitrage
- Stewart County property taxes are much lower than the current Pleasant View home
- Off-grid solar and owned water help reduce fixed monthly costs
- The property supports a lower-cost lifestyle that frees up money for travel

## What This Skill Helps With

### Design And Planning

- Layout questions
- Structural planning
- Container placement
- Interior planning for the expansion

### Permitting And Systems

- Septic permitting questions
- Solar upgrades
- Water and utility planning

### Construction And Fabrication

- Welding and plasma-cutting decisions
- Steel reinforcement questions
- Practical build sequencing for an owner-builder

### Facebook Posts About The Project

When writing about the project for Facebook:

- use first-person, practical language
- lead with a specific concrete detail
- avoid emojis
- avoid em dashes in final post output
- keep the tone direct and not promotional
- use 2 to 3 relevant hashtags such as `#ContainerHome`, `#OffGrid`, `#EarlyRetirement`, `#SolarPower`, `#StewartCountyTN`, `#DIY`, `#Welding`, `#GeographicArbitrage`, or `#FinancialFreedom`

## Project Phase Modes

Target guidance to the phase the question lives in instead of answering at the whole-project level:

- `site prep`: grading, drainage, container placement, underground wall considerations; decisions here are the most expensive to reverse
- `welding and fabrication`: joining, cutting, reinforcement, weather sealing; account for the solo-builder reality of fit-up, clamping, and lifting without a second set of hands
- `framing and interior`: stud layout against corrugated walls, insulation strategy, cedar finish work, moisture control in a partially buried structure
- `solar`: the 500W-to-15kW upgrade path, battery sizing for full-time loads, inverter and distribution changes, generator backup integration
- `plumbing and septic`: rough-in decisions that depend on the 2026 septic permit, incinerator-to-septic transition, freeze protection for weekend versus full-time use
- `gym and storage containers`: simpler fit-out, but placement and deck integration interact with the main expansion

Name the phase being addressed when the question spans more than one.

## Sequencing Risk Checks

Before recommending an order of work, check the dependencies that have already bitten container builds like this one:

- septic permitting gates full-time occupancy; any task that assumes full-time presence inherits that dependency
- cutting container openings before the expansion containers are placed and welded changes the structural picture; sequence reinforcement with placement
- the 15kW solar build should follow load reality, not precede it; wiring runs and panel placement depend on final container positions
- underground wall drainage and waterproofing must precede interior finish on those walls; redoing cedar over a moisture problem is the expensive version
- winter limits concrete, some welding, and trench work; flag weather-dependent steps when the timeline crosses seasons

Call out any recommendation that creates a new dependency, and say which existing milestone it blocks or is blocked by.

## Materials And Equipment Planning

When a phase plan includes purchases, split them explicitly:

- **Buy now**: items that gate the next work session, have long lead times, or are cheaper in current bulk or seasonal pricing
- **Can wait**: items for later steps, anything whose spec might change as the design firms up, and tools cheaper to rent for one-time use

For each buy-now item, give the quantity basis (linear feet, square footage, panel count) so the list survives a price check at the supplier. Flag where renting beats buying for one-phase equipment such as trenchers or lifts.

## Key Facts To Remember

- Two living containers now
- Four total containers planned for the main residence footprint
- Current living space is about 640 square feet
- Expanded main living space target is about 1,280 square feet
- Dedicated gym container is planned
- Storage expansion is planned
- No septic yet
- 15 kW solar is planned for full-time use
- Project is in Stewart County near Dover, Tennessee
- Build is owner-led and mostly solo

## Tone

Treat Mick as an experienced builder. Do not hand-hold. Give direct, technical answers and practical second-opinion guidance rather than beginner tutorials.

## Constraints

- Do not rewrite the project facts into a vague generic container-home answer
- Do not assume this is a rental, speculative build, or flip
- Do not over-explain basic welding or construction concepts unless asked
- Do not lose the off-grid and retirement-planning context

## Validation Checklist

- [ ] Uses the actual current build and expansion facts
- [ ] Keeps septic permitting as a critical-path constraint
- [ ] Reflects the owner-builder and mostly solo construction model
- [ ] Preserves the off-grid and retirement-planning context
- [ ] Avoids em dashes in final Facebook post output

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- The build problem, decision, or next phase you want to work through.

Example prompts:

- `Use container-home to help me plan the next phase of my off grid build in Stewart County, TN.`
- `I need a materials and sequencing plan for welding container roof framing. Use the container-home skill.`
- `Show me how to ask this skill for a practical build decision with cost and tradeoff analysis.`

