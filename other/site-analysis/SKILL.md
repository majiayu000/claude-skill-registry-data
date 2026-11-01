---
name: site-analysis
description: "Reads a site for the things that will decide the building rather than for a set of diagrams: what is fixed and cannot move, what the approach and the ground do to where a building can sit, where the sun and the weather come from, what the neighbours and the context require, and what has to be found out before anything is committed. Separates observation from inference throughout, and ends with the list of what is still unknown and who answers it. Trigger on \"site analysis\", \"read this site\", \"what does the site tell us\", \"first visit to the site\", \"site-analysis\", or a new site with nothing decided yet. Carries no climate data, no zoning limits and no soil values; `climate-zone-mapper`, `seismic-lookup`, `wind-snow-lookup` and `zoning-summary` collect those and this reads what they found for what it means. It is not a survey and does not replace the surveyor, the civil engineer, or the Architect of Record."
license: MIT
metadata:
  title: "Site Analysis"
  summary: "Read a site for what it decides, before anything is drawn on it"
  discipline: "design-building-types"
  tags: "Pre-Design, Analysis"
---

# Site Analysis

Site analysis usually produces a sheet of diagrams that nobody refers to again:
a sun path, a wind rose, a noise arrow. The useful version answers a different
question. Not what is on the site, but what the site has already decided, and
what still has to be found out before anyone commits.

## Scope and limits — read first

**What this does.** Works the site for its decisions: what is immovable, where a
building can physically go, what the approach and the ground allow, what the
context requires, and what is unknown. Keeps observation and inference separate,
and ends with a list of questions rather than a set of diagrams.

**What this does not do.**

- **It collects no data.** `climate-zone-mapper`, `seismic-lookup` and
  `wind-snow-lookup` record site values; `zoning-summary` and `/test-far` hold
  the zoning; `lookup-flood-zone` the flood designation; `survey-review` and
  `geotech-report-review` read the surveyor's and the engineer's documents. This
  reads what they found for what it means to the design.
- **It is not a survey.** Nothing here is measured.
- It does not test feasibility against zoning arithmetic. `test-fit` does.
- It does not design. `parti-study` takes what this produces.
- It does not replace the surveyor, the civil engineer, or the Architect of
  Record.

**What you need before starting.** The site: an address, a survey if there is
one, and a visit if one has happened. The programme, or an idea of it. Whatever
data has been collected. Whether the site is bought, optioned, or being
considered.

## Workflow

### Step 1. Establish what is fixed, before looking at anything else

Ask, in one message:

> 1. What is fixed and cannot be moved? Boundaries, easements, rights of way,
>    existing structures to remain, protected trees, a required frontage, an
>    existing access point.
> 2. What is fixed by others but might be negotiable? A curb cut, a utility
>    connection, a party wall agreement, a setback with a variance path.
> 3. What data exists already, and from what document?
> 4. Has anyone visited, and what did they notice that no drawing shows?
> 5. Is the site committed, or is this part of deciding whether to buy?
> 6. What is the programme, roughly, and how big is it against the site?

**Question 5 changes the exercise.** For a site being considered, the job is to
find the thing that kills it, fast. For a site already bought, the job is to
find what it decides.

### Step 2. Work the ground and the approach

These two decide where a building can go more than anything on a sun diagram:

- **Levels.** Where is it high and low, and by how much? What does that do to
  the entrance, the accessible route, the parking, and where a basement is
  possible or unavoidable? Point at `civil-drawing-review`.
- **What is under it.** Rock, water, fill, contamination, a previous building.
  Point at `geotech-report-review`, and say plainly if no report exists.
- **Drainage.** Where does water arrive from, cross, and leave? What is
  downstream and who owns it?
- **Approach.** How do people and vehicles reach it, from which direction, and
  what do they see as they come? Point at `site-access-study`.
- **Services.** Where does each utility come from, at what capacity, and what
  does connecting cost? This is a common late surprise on rural and infill
  sites both.

### Step 3. Work the sun, the weather and the outlook, as decisions

Not as diagrams. For each, say what it decides:

- **Sun.** Which faces get it, when, and which parts of the site are in shadow
  from what. Then: which rooms want it and which do not, and whether the site's
  good orientation and its good view are the same direction. They usually are
  not, and that conflict is a design decision worth naming now. Point at
  `shadow-study` and `daylight-study`.
- **Wind and weather.** Prevailing direction, driving rain, snow drift and where
  it lands, and what that does to entrances and outdoor space.
- **Outlook.** What is worth seeing, what is not, and what will change. A view
  over a neighbouring site is a view until that site is built on. Point at
  `view-analysis`.
- **Noise and nuisance.** Roads, rail, flight paths, plant, a neighbour's use,
  and what time of day each matters.

### Step 4. Work the context and the neighbours

- What the surrounding buildings do: their height, their setback, their
  materials, where their windows and entrances face.
- What overlooks the site and what the site would overlook. Privacy runs both
  ways and it is the most common objection.
- What the neighbours will care about: light, view, traffic, noise,
  construction. Point at `entitlement-tracker` if approvals are discretionary.
- Whether there is a pattern the site sits in, and whether following it or
  breaking it is a choice anyone has made deliberately.
- Anything protected: heritage, trees, habitat, a viewshed.

### Step 5. Separate what was observed from what was inferred

Every finding above gets marked:

| Finding | Observed / From a document / Inferred | Source |
|---|---|---|

**Inference is where site analysis goes wrong.** A wind direction assumed from
the region, a soil condition assumed from the neighbourhood, a service capacity
assumed from a nearby building: each is reasonable and each has broken a scheme.
Count them.

### Step 6. Report

- **What kills the scheme, if anything.** First, and plainly. On a site being
  considered this is the whole report.
- What is fixed, and what is negotiable with whom.
- What the ground and the approach decide.
- The sun-and-view conflict, if there is one.
- What the neighbours will raise.
- The observed / document / inferred counts.
- **What has to be found out, ordered by what it unblocks**, with who answers
  each and how long it takes. A survey, a geotechnical investigation, a utility
  enquiry, a pre-application meeting.

Close by saying nothing was measured or tested here.

### Step 7. Save

Ask where. It is read back at every stage, and again when somebody asks in a
year why the building sits where it does.

## Rules

- **Ask whether the site is committed** before anything else. It changes the
  exercise.
- Work the ground and the approach before the sun.
- Every finding is marked observed, from a document, or inferred.
- Name the conflict between the good orientation and the good view, where there
  is one.
- End with what has to be found out, ordered by what it unblocks.
- Never collect data here. Name the skill that does.

## Anti-patterns

- Producing a sheet of diagrams that decides nothing.
- A sun path with no statement of what it means for the plan.
- Assuming soil, wind or service capacity from the neighbourhood.
- Reading the site and not the approach to it.
- Ignoring what the site overlooks, which is half the privacy question.
- Treating a view over an empty neighbouring site as permanent.
- Leaving the unknowns unlisted, so they are discovered in sequence rather than
  commissioned at once.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
