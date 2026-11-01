---
name: site-access-study
description: "Studies everything that has to reach a site and finds where two of them want the same frontage: lists every arrival — people, cars, deliveries, refuse, fire apparatus, utilities, moving vans, coaches — traces each from the public way to where it has to end up, and reports the conflicts, the curb cuts that will not be granted, and the frontage the project has already spent. Trigger on \"site access study\", \"how does the truck get in\", \"where does the fire access go\", \"can we get a curb cut here\", \"loading and refuse access\", \"site-access-study\", or a site plan with a question about how anything reaches it. Carries no dimensions, no turning radii, no fire apparatus requirements and no curb cut standards; all come from the jurisdiction, the fire department and the utility. It does no traffic engineering and no swept path analysis, and does not replace the civil engineer or the Architect of Record."
license: MIT
metadata:
  title: "Site Access Study"
  summary: "Work out how vehicles, services, and fire access reach the site"
  discipline: "code-life-safety"
  tags: "Design"
---

# Site Access Study

Every project has less frontage than it needs. Cars, deliveries, refuse, fire
apparatus, utilities and the front door all want the same edge, and the ones
that lose are the ones nobody listed at the start.

## Scope and limits — read first

**What this does.** Lists every arrival the site has to accept, traces each from
the public way to its destination, and reports where two compete for the same
frontage or cross each other. Names what the jurisdiction and the fire
department have to confirm, and when.

**What this does not do.**

- **It carries no dimensions.** No turning radii, no aisle widths, no apparatus
  access dimensions, no curb cut spacing, no grade limits. All from the
  jurisdiction, the fire department, the utility, or the design vehicle
  standard your civil engineer uses.
- **It does no traffic engineering.** Trip generation, capacity, queuing, and
  the traffic impact study are `senior-traffic-engineer`'s and the traffic
  engineer's.
- **It does no swept path analysis.** It asks whether a vehicle can make a
  movement and names who confirms it with software.
- It does not design the parking layout or the service yard.
- It does not check zoning counts. `/test-parking` and `/count-loading-berths`
  do.
- It does not replace the civil engineer or the Architect of Record.

**What you need before starting.** The site plan with the frontages and the
public ways. The programme and what it generates. The jurisdiction. The fire
department's access requirements, if you have them. Existing curb cuts, and any
constraint on the frontage: trees, poles, hydrants, transit stops, bike lanes,
crossings, historic paving.

## Workflow

### Step 1. List every arrival before looking at the site

Ask, in one message:

> 1. Who and what arrives here? Go beyond cars: pedestrians, cyclists, transit,
>    drop-off, taxis and rideshare, accessible parking, service deliveries,
>    refuse and recycling, moving vans, coaches, fire apparatus, utility access,
>    landscape maintenance, window cleaning, and anything this programme
>    generates specifically.
> 2. For each: how often, at what hours, and what vehicle?
> 3. What frontages does the site have, and what is on each: transit, bike lane,
>    crossings, trees, hydrants, poles, existing curb cuts?
> 4. What does the jurisdiction control on each frontage, and is any of it a
>    different authority? A state route or a rail crossing has a different
>    owner.
> 5. What does the fire department require, and have they been asked?
> 6. What is already fixed: an existing curb cut, a required transit easement, a
>    building line?

**The list in question 1 is the study.** Anything not on it will arrive anyway
and take frontage from something that was planned.

### Step 2. Trace each arrival, public way to destination

One row per arrival:

| Arrival | Frequency | Vehicle | From which street | Through what | Ends at | Leaves how |
|---|---|---|---|---|---|---|

`Leaves how` is a column because reversing is the constraint that kills
schemes. Note every movement that requires reversing, and whether it reverses
into or out of the public way.

### Step 3. Find the frontage competition

Lay the arrivals over the frontage and report what wants each part of it:

| Frontage segment | Wants it | Conflicts | Who wins, and what it costs the loser |
|---|---|---|---|

Then count the curb cuts required and say plainly that each one is a permission,
not a design decision. Jurisdictions limit the number, the width and the
spacing, and they refuse. A scheme with three curb cuts on one frontage should
know now.

### Step 4. Work fire access as its own pass

Fire access is the constraint that most often forces a scheme change and it is
usually checked last:

- Where does apparatus need to get to, and how close to the building?
- Can it get there, turn, and leave? Is a turnaround needed?
- What are the grade and surface loading requirements, and does the proposed
  surface carry them? A fire lane over a podium or a landscaped deck is a
  structural requirement.
- Where are the hydrants and the fire department connection, and are they within
  reach of each other and of apparatus?
- Does the fire access route conflict with anything else on the list: parking,
  the accessible route, the loading movement, a gate?
- Has the fire department been asked, and what did they say? Log it as verbal or
  written.

### Step 5. Work the accessible route across every arrival

For each arrival that involves people: where do they get out, and can they reach
the entrance? The accessible route from accessible parking and from the drop-off
gets traced, and every place it crosses a vehicle route gets named. Point at
`civil-drawing-review` for the slopes and at the accessibility standard for the
requirements.

### Step 6. Report

- The arrivals list, with any that were added during the study marked, because a
  late addition is the finding.
- The frontage competition table.
- Every movement that requires reversing, and where.
- Every curb cut, with a note that each is a permission.
- The fire access findings, separately.
- Every conflict between an accessible route and a vehicle route.
- What has to be confirmed and by whom: the jurisdiction, the fire department,
  the traffic engineer, the civil engineer with swept path software.
- What has to be asked before the scheme is fixed rather than after.

### Step 7. Save, if asked

Ask whether to write the study to a file and where.

## Rules

- **Never supply a dimension, a radius, a grade limit, or an apparatus
  requirement.**
- List every arrival before looking at the site, including refuse and
  maintenance.
- Note every reversing movement and whether it involves the public way.
- Treat every curb cut as a permission, and say so.
- Give fire access its own pass, every run.
- Never state that a vehicle can make a turn. Name who confirms it.
- Mark fire department and jurisdiction positions verbal or written.

## Anti-patterns

- Studying cars and forgetting refuse, moving vans and maintenance.
- Assuming a curb cut will be granted because there is room for it.
- Checking fire access after the scheme is fixed.
- Assuming a landscaped area can carry apparatus.
- Performing swept path analysis.
- Treating a state route or a rail frontage as the city's to permit.
- Letting the accessible route cross a loading movement without naming it.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
