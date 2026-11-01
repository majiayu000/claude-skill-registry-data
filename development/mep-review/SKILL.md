---
name: mep-review
description: "Reviews a mechanical, electrical, and plumbing drawing set against the architectural and structural drawings across eight coordination axes: shafts and risers, ceiling and plenum depth, equipment rooms, horizontal distribution, intake and exhaust, service entries, maintenance access, and document coordination. Trigger on \"MEP review\", \"MEP coordination\", \"check the MEP set\", \"will the ducts fit\", \"plenum depth\", \"shaft coordination\", \"is there room for the equipment\", or a shared MEP sheet with a fit question. The skill supplies no dimensions of its own: every clearance, depth, and area comes from the drawings or from you. Writes a dated review file and appends to a project index, with every unverified axis counted on the face of the review. Does not size equipment and does not replace the Engineer of Record."
license: MIT
metadata:
  title: "MEP Review"
  summary: "Read an MEP set for space, routing, and coordination conflicts"
  discipline: "structure-mep"
  tags: "Design"
---

# MEP Review

Walk an MEP set through eight coordination axes, in the order a set actually
gets checked, and write the result to a dated file that says what was compared
against what.

This is the architect's read on someone else's drawings. It finds the places
where two sheets disagree about the same cubic foot of building, and it finds
them by reading, not by modelling.

## Scope and limits — read first

**What this does.** Takes an MEP set together with the architectural and
structural drawings it is supposed to fit inside, compares them across eight
axes, and writes a review that names the two sheets behind every conflict.

**What this does not do.**

- **It does not know any dimensions.** No plenum depth, no shaft size, no
  equipment room area, no clearance in front of a panel, no duct velocity, no
  ventilation rate, no separation between an intake and an exhaust. Every one of
  them comes from the drawings or from you. That is the review, not a gap.
- **It does not run clash detection.** There is no model here. It reads
  drawings, which means it finds conflicts a section or a dimension reveals and
  misses conflicts that only a model would show. Say so in the report rather
  than implying coverage the method does not have.
- It does not size or select equipment, calculate loads, or check a system
  against an energy or ventilation standard.
- It is not a code check. Rated shaft enclosures, required exhaust, and fire
  damper locations belong to `code-compliance-review` and to the AHJ.
- **The Engineer of Record designs the systems.** This review raises questions
  for that engineer. It does not answer them on the engineer's behalf.

**What you need before starting.** The MEP sheets, the architectural background
and reflected ceiling plan at the same revision, the structural framing plan,
the project phase, and the clearances your project or your consultant requires.

## Workflow

### Step 1. Bootstrap if needed

If `docs/mep-reviews/` does not exist, create it along with
`docs/mep-reviews/index.md` holding a single heading and nothing else.

### Step 2. Anchor the set

Before looking at anything, record and repeat back:

- Project name, phase, and the area or level under review.
- Every sheet in play, by number, with its revision date.
- Which disciplines are present and which are missing.
- Whether the architectural background and the MEP sheets carry the same
  revision date.

**Revision dates decide whether a conflict is real.** Two sheets at different
dates disagreeing is not a finding, it is a stale background. Say which it is
before writing anything down. If the dates differ, the whole review is
provisional and the report has to say so at the top.

Ask for anything missing. Do not proceed on an assumed sheet.

### Step 3. Apply the eight axes

Work them in order. Each axis produces one of three results: a finding, a pass
with the source of the limit named, or unverified because the drawing or the
value needed for it was not supplied. Never a fourth.

**1. Shafts and risers.** Count them. Check each one runs floor to floor without
jogging into a beam or a stair, and that it terminates somewhere: a roof
penetration, a louvre, a mechanical room. Compare the shaft as drawn on the
architectural plan against what the MEP sheets route through it. A shaft that
carries four services on one floor and three on the next is the finding.

**2. Ceiling and plenum depth.** Take the depth from the section, not the
schedule. Add up what has to occupy it at the tightest point: structure, duct
including insulation and hangers, sprinkler main, lighting, conduit, and the
clearance between them. **Check the worst location, not the typical one.** The
typical section is drawn where everything fits.

**3. Equipment rooms.** Area, clear height, and the door. Then the route: how
the largest single piece of equipment gets in on day one, and how it gets out
when it is replaced. A room reachable only through a finished corridor with a
turn in it is a finding even when the room itself is large enough.

**4. Horizontal distribution.** Follow the mains from the source to the far end
of the floor. Look at every point where a duct or pipe crosses a beam, a girder,
a shear wall, or another main. Note where the drawing shows a penetration and
where it simply shows the duct passing through structure that is not on the MEP
sheet.

**5. Intake, exhaust, and flues.** Where the building takes air in, where it
puts air out, and what is near each. Check them against operable windows,
occupied terraces, the property line, and each other. Ask for the separation the
project is working to before measuring anything; a relief hood near an intake is
a finding against that separation, not against a number this skill supplies.

**6. Service entries and metering.** The utility side: where power, water, gas,
and sewer enter, where the meter, transformer, or backflow assembly sits, and
what clearance the utility demands around it. Utility clearances come from the
utility, not from this skill and not from the code.

**7. Maintenance access.** Every valve, damper, filter, VAV box, and cleanout
against the ceiling type below it. Access panels in a hard ceiling have to be
drawn on the reflected ceiling plan to exist. If they are not on the RCP, they
are not in the project.

**8. Document coordination.** MEP against architectural background, against the
RCP, and against the structural framing plan. Then schedules against plans: a
unit on the schedule that is not on a plan, a unit on a plan that is not on the
schedule, a tag that does not match. Finish with revision dates across the set.

### Step 4. Write the review

Filename:

`docs/mep-reviews/<YYYY-MM-DD>-<slug>-mep.md`

Slug rule: lowercase, `[^a-z0-9-]` removed, 40 characters maximum, from the
project plus the level or area reviewed. Suffix `-<n>` if the date and slug
already exist.

Every finding carries three things: the two sheets that disagree, what each one
shows, and the dimension or clearance the conflict is measured against together
with where that value came from. A finding with no value behind it is an
observation, and it goes in a separate list under that name.

The head of the review states the sheets and their revision dates. The foot
states how many axes were checked and how many were unverified.

### Step 5. Update the index

Append one line to `docs/mep-reviews/index.md`:

`- <YYYY-MM-DD> — <project>, <area> — <n> findings, <n> unverified — <filename>`

A list rather than a table, on purpose. Nothing here has to stay aligned.

### Step 6. Report

Give the counts: axes checked, findings raised, observations without a value
behind them, axes unverified. List the unverified axes with what each one needs
to close. Close with:

> Every dimension in this review came from you or from the drawings. Unverified
> axes were not checked at all, and reading drawings does not find what only a
> model would show.

## Rules

- **Never supply a dimension.** Not a plenum depth, not a clearance, not a room
  size, not from memory and not from a manufacturer's page. Ask, or mark the
  axis unverified.
- **Name both sheets in every finding.** A conflict that cannot be traced to two
  documents is an opinion.
- **Check revision dates before calling anything a conflict.** Different dates
  mean a stale background until proven otherwise.
- **An axis missing its drawing is unverified, not passed.** Silence about an
  axis reads as a pass to whoever gets the review.
- Route anything about rated enclosures, required exhaust, or damper locations
  to `code-compliance-review` rather than answering it here.

## Anti-patterns

- Reading the typical section and calling the plenum clear. The tight spot is
  somewhere else, and it is the only spot that matters.
- Treating a plenum as empty because the structure is not drawn on the MEP
  sheet. Absence from one discipline's drawing is not absence from the building.
- Quoting a clearance from memory because it "is standard". Clearances vary by
  utility, by manufacturer, by jurisdiction, and by the equipment actually
  specified.
- Calling a conflict on two sheets at different revision dates.
- Reporting eight axes when three of the drawings were never supplied.
- Sizing anything. The moment the review proposes a duct size it has stopped
  being a review and started being an engineering opinion nobody asked for.

## Resources

This skill bundles no reference files, and that is deliberate: every value it
would hold is project-specific or jurisdiction-specific.

Related tools in the catalog:

- `code-compliance-review` for rated assemblies, required exhaust, and the life-safety side
  of the same drawings.
- `constructability-review` for the builder's read on the same set.
- `senior-mep-engineer` for a risk-flagged gut check rather than a full axis
  walk.
