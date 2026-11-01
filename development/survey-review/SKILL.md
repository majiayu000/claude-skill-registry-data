---
name: survey-review
description: "Reads a land survey the way a design team has to: establishes what kind of survey it is and therefore what it is certified to show, checks it against what the project actually needs, and reports the gaps before a scheme gets built on top of them. Separates what was measured from what was compiled from records, works the boundary, the encumbrances, the topography, the utilities and the datum in that order, and flags every place the drawing shows a line that no instrument supports. Trigger on \"review the survey\", \"is this survey adequate\", \"what's missing from this survey\", \"ALTA survey review\", \"survey-review\", or a survey handed over at the start of a project. Carries no survey standards and no certification requirements; the standard the survey was made to comes from its own certificate. It is not a survey, does not verify a boundary, and does not replace the surveyor or the Architect of Record."
license: MIT
metadata:
  title: "Survey Review"
  summary: "Read a survey for what it does not say, before you design against it"
  discipline: "code-life-safety"
  tags: "Review"
---

# Survey Review

Every dimension in a project is measured from the survey, and the survey is
almost never reviewed. It arrives, it is trusted, and the things it does not
show are discovered by excavation. The review takes an hour and it is the
cheapest hour in the project.

## Scope and limits — read first

**What this does.** Establishes what kind of survey this is and what it is
certified to show, then compares that against what the project needs. Reports
gaps, unsupported lines, and the things shown from records rather than
measurement.

**What this does not do.**

- **It carries no survey standards.** What a given survey type must include
  comes from the standard named in its own certificate. Quote it and the review
  holds the drawing against it.
- It is not a survey and it verifies nothing on the ground.
- It does not read title. `/explain-easement` explains an encumbrance and a
  title attorney reads the instruments. This checks whether what the title
  documents list appears on the drawing.
- It does not do geotechnical work. `geotech-report-review` reads that report.
- It does not locate utilities. Nothing does, short of locating and potholing.
- It does not replace the surveyor or the Architect of Record.

**What you need before starting.** The survey, with its certificate, legend,
notes and revision date. The title commitment, if there is one. What the project
needs the survey for. Any adjoining site information.

## Workflow

### Step 1. Establish what this survey is

Ask, in one message:

> 1. What does the certificate say: what standard, certified to whom, when, and
>    by whom?
> 2. What is the project going to do with it: design, permit, construction
>    layout, closing, all of them?
> 3. Is there a title commitment, and do you have the exception list?
> 4. What is the date, and has anything changed on or around the site since?
> 5. Are adjoining properties, streets or waterways relevant?

**A survey certified for one purpose is often used for another.** A boundary
survey used for grading design, or an old survey used for permit, is the common
failure, and it is a question about the certificate rather than about the
drawing.

### Step 2. Separate measured from compiled

Go through the drawing and mark every category as one of:

- **Measured.** The surveyor observed it.
- **Compiled.** Taken from records: utility records, a previous survey, a plat, a
  municipal map.
- **Unsupported.** A line on the drawing with no note, no reference and no
  instrument behind it.

Report the counts. Utilities are almost always compiled, and treating them as
measured is how a design is drawn over a main nobody has seen.

### Step 3. Work the boundary

- Does the boundary description on the drawing match the legal description in
  the title commitment, word for word?
- Does the traverse close, and is closure stated?
- Are monuments found or set, and are they noted as which?
- Are there gaps, overlaps, or gores with adjoining parcels?
- Are any encroachments shown, in either direction, and is each dimensioned?
- Does the drawing show a boundary line that differs from the deed line, and if
  so is the difference explained?

### Step 4. Work the encumbrances against the title list

One row per title exception:

| Exception | Recorded ref | Shown on survey? | Plottable? | Note |
|---|---|---|---|---|

Three findings come out of this table and all three matter:

- Exceptions listed in title and not shown on the survey.
- Strips shown on the survey with no exception behind them.
- Exceptions the surveyor marked as blanket or not plottable, which means their
  location is unknown and the design cannot avoid them.

### Step 5. Work topography, utilities, and the datum

- **Datum.** Vertical and horizontal, both named. A survey with an assumed datum
  cannot be tied to a flood elevation, a municipal benchmark, or a neighbouring
  project. Say so plainly if that is the case.
- **Contour interval and spot elevations.** Adequate for what the project needs
  to do with them.
- **Coverage.** Does topography extend far enough beyond the boundary to design
  the grading, the access, and the connections?
- **Utilities.** What is shown, whether measured or from records, whether
  inverts are given, and whether size and material are stated. An invert
  missing is a design that cannot be drawn.
- **Trees, structures and features** relevant to what the project will do.
- **Rights of way and street lines**, and whether any dedication or widening is
  proposed.

### Step 6. Report the gaps

- What the project needs that the survey does not show, listed individually.
- Everything compiled that will be relied on as though measured.
- Every unsupported line.
- Title exceptions unresolved, in either direction.
- Whether the survey should be updated, supplemented, or recertified, and to
  whom.

Say plainly which of these has to be resolved before design proceeds and which
can wait, because a request to the surveyor is faster and cheaper before the
scheme exists.

### Step 7. Save, if asked

Ask whether to write the review to a file and where.

## Rules

- **Never supply a survey standard's contents.** Quote from the certificate.
- Mark every category measured, compiled, or unsupported. There is no fourth
  state.
- Check the title exception list against the drawing in both directions.
- Name the datum, or say there is none, on every run.
- Never verify a boundary or a dimension.
- Say what has to be resolved before design and what can wait.

## Anti-patterns

- Reading the drawing and not the certificate.
- Treating compiled utilities as located.
- Using a survey certified for one purpose for another without saying so.
- Reporting only the exceptions missing from the drawing and not the strips with
  nothing behind them.
- Designing grading against an assumed datum.
- Accepting a not-plottable easement as though it were resolved.
- Waiting until the scheme is drawn to ask the surveyor for what is missing.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
