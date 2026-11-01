---
name: wind-snow-lookup
description: "Assembles the site environmental criteria block a project needs before any structural or envelope design starts: wind, snow, seismic, ice, rain, and flood parameters, each recorded with the source it came from. Trigger on \"wind speed for this site\", \"ground snow load\", \"site hazard parameters\", \"design criteria block\", \"seismic parameters\", \"rainfall intensity\", \"wind-snow-lookup\", or a pasted site location with a request for design values. Works in any jurisdiction. The skill knows which parameters a design needs and what each one feeds; the values come from the user's own code maps, official hazard tool, or authority, supplied by typing, pasting, or naming a file. It never supplies a hazard value from memory or from web search, and reports every parameter it could not source as a gap. Returns mapped parameters only, never design pressures or loads."
license: MIT
metadata:
  title: "Wind Snow Lookup"
  summary: "Assemble the site hazard criteria a design needs"
  discipline: "code-life-safety"
  tags: "Compliance, Pre-Design"
---

# Wind Snow Lookup

Build the site criteria block, one parameter at a time, with a source on every
line. Which parameters a design needs is knowable in advance. What they are for
your site is not, so they come from you.

## Scope and limits — read first

**What this does.** Works through the environmental parameters a structural and
envelope design needs, asks for each, records where each came from, and prints a
criteria block with a gap list. It tells you what a parameter feeds, so you can
tell whether you still need it.

**What this does not do.**

- **It does not look up hazard values.** It has no maps, no tables, and no
  coordinates-to-value function. Every value comes from you, out of your code's
  maps, your jurisdiction's hazard tool, or a letter from the authority. That is
  the design, not a gap.
- **It returns mapped parameters, never design loads.** A basic wind speed is
  not a design pressure. A ground snow load is not a roof snow load. Converting
  one to the other needs exposure, topography, importance, thermal, and shape
  factors, and that is a design step this skill does not take.
- It does not geocode an address, and it does not infer a site from a project
  name.
- It does not know which hazards apply to your region. It asks.
- It does not replace the Engineer of Record or the authority.

**What you need before starting.** The site location, the governing loading
standard and its edition, the risk or importance category, and access to
whatever your jurisdiction publishes the values in.

## Workflow

### Step 1. Establish the standard and the site

Ask, in one message:

> 1. Which loading standard governs, and which edition? The edition matters more
>    than usual here, because hazard maps get redrawn between them.
> 2. Site location, as precisely as you have it, and whether the authority
>    requires a specific point.
> 3. Risk or importance category, and what set it.
> 4. Which hazards apply to this project and this region? Wind, snow, seismic,
>    ice, rain, flood, tsunami, or others your code carries.
> 5. Where will the values come from: your code's maps, a hazard tool your
>    jurisdiction publishes, or a document you have. Name it, and I will record
>    it as the source on every line it supplies.

Record the standard, the edition, and the source. All three print on the block,
because a hazard value without its edition and its source is not usable a year
later.

### Step 2. Collect one value per parameter

Work through the hazards named in Step 1. For each parameter, say what it is for
before asking, so a parameter that turns out to be unnecessary gets dropped
rather than guessed.

| Parameter | Feeds |
|-----------|-------|
| Basic wind speed, at the risk category | Wind pressure calculation |
| Wind exposure category | Wind pressure calculation |
| Topographic factor inputs, if the site needs them | Wind pressure calculation |
| Ground snow load | Roof snow load calculation |
| Snow importance and thermal conditions | Roof snow load calculation |
| Mapped seismic accelerations | Seismic base shear |
| Site class, or the geotechnical basis for it | Seismic base shear |
| Seismic design category | Detailing and system limits |
| Ice thickness and concurrent wind | Ice load on exposed elements |
| Rainfall intensity, at the return periods your code names | Roof drainage and rain load |
| Flood design elevation | Siting, envelope, and finished floor level |

Accept a typed value with its source, a pasted table or tool output to read it
out of, or a file to read. If none arrives, the parameter goes on the gap list.
Do not offer a value, do not search for one, and do not interpolate between two
values the user gave for nearby points.

### Step 3. Print the criteria block

```
SITE DESIGN CRITERIA — <project>
STANDARD: <as supplied>        EDITION: <as supplied>
SITE: <as supplied>            RISK/IMPORTANCE: <as supplied>
SOURCE: <as supplied>          RECORDED: <date>

<parameter>   <value>   <source>   <what it feeds>
...

GAPS: <count>. Listed below with what each one is needed for.
ALL VALUES SUPPLIED BY <name>. NONE WERE LOOKED UP BY THIS TOOL.
```

The gap count goes on the block, not underneath it. A criteria block that omits
what is missing gets copied onto a drawing as if it were complete.

### Step 4. Save, if asked

Ask whether to write the block to a file and where. Write it directly. There is
no template and no script.

## Rules

- **Never supply a hazard value.** Not from memory, not from a search, not from
  a figure in this file. There are none in this file.
- **Never convert a mapped parameter into a design load.** That is a separate
  calculation with inputs this skill does not collect.
- **Never interpolate.** Between two map contours, between two nearby sites,
  between two editions. If the value is between things, the user reads it off
  the map, not this tool.
- **Record the edition on every line.** Hazard maps are redrawn between
  editions, and a value carried forward silently is the failure mode here.
- **Print the gap count on the block itself**, every time.
- Never geocode, and never accept a project name as a location.

## Anti-patterns

- Giving a wind speed or snow load for a city because it is a familiar figure.
  These are exactly the numbers that feel well known and are jurisdiction and
  edition specific.
- Searching the web for a site's design values. Search finds which standard
  governs; it does not read a map for a coordinate.
- Turning a ground snow load into a roof snow load, or a basic wind speed into a
  pressure, because the user asked for the second thing.
- Interpolating between contour lines or between two nearby coordinates.
- Producing a criteria block with no gap count, so a partial set reads complete.
- Bundling a hazard map or table into this skill later. It has none on purpose,
  and a bundled hazard value goes stale on the next map revision while still
  looking authoritative.

## Resources

None. This skill is one file. Output is written directly at the path you name.
