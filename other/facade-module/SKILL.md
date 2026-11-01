---
name: facade-module
description: "Divides elevation lengths and heights by a panel module and works the remainder into explicit options: resize every panel equally, absorb the leftover in end or corner panels, or take it in one feature bay, with the arithmetic for each and a check of where mullions land against the structural grid. Trigger on \"panelize\", \"curtain wall module\", \"facade module\", \"mullion spacing\", \"panel layout\", \"facade-module\", or an elevation length paired with a module. Every dimension comes from the user: elevation lengths and floor heights from their drawings, the module and any panel size limits from the manufacturer's literature, the grid from their structural plans. The skill never supplies a manufacturer's maximum panel size or a standard module from memory, does not size mullions or check wind load, does not judge thermal or glare performance, and does not choose between the options it lays out."
license: MIT
metadata:
  title: "Facade Module"
  summary: "Divide an elevation into panels and lay out the leftover, option by option"
  discipline: "envelope-performance"
  tags: "Design, Analysis"
---

# Facade Module

Take an elevation, a module, and the grid behind it, and get back the division
arithmetic: how many panels, what is left over, and the ways the leftover can
be taken, each with what it costs the layout. The choice between them is
design; the arithmetic before the choice is this skill.

## Scope and limits — read first

**What this does.** Divides each elevation length you give by the module you
give, reports panel count and remainder, lays out the remainder-handling
options with their arithmetic, checks where mullions land against your column
grid and your floor heights, and puts the options side by side so the
trade-offs are visible before anything is drawn.

**What this does not do.**

- **It does not know any product.** No manufacturer's maximum panel size, no
  standard module, no typical spandrel height. Module, limits, and every
  dimension come from you and your supplier's literature. That is the design,
  not a gap.
- It does not size anything structural. Mullion depth, anchor spacing, and
  wind load are the facade engineer's, and movement joints are set by the
  structure, not by this arithmetic.
- It does not judge performance. Window-to-wall ratio targets, U-values,
  SHGC, and glare belong with `/test-glazing`, `/test-energy`, and your
  energy modeler.
- It does not pick an option. Each is reported with what it gives up; the
  choice is a design call and stays with you.
- It works in elevation, on flat facades. Curved or faceted geometry needs
  the real setting-out from your model.

**What you need before starting.** Elevation lengths and floor-to-floor
heights from your drawings, the module you want to test (and a second one if
you are comparing), any panel size limits from the manufacturer's literature
with the document named, and the column grid with its relationship to the
facade line.

## Workflow

### Step 1. Collect the dimensions

Ask, in one message:

> 1. The elevations to panelize: each length, and the floor-to-floor heights
>    if the horizontal joints matter too.
> 2. The module, or modules, to test, and where each came from.
> 3. Any hard limits: maximum or minimum panel dimension, from the named
>    manufacturer document. If there are none yet, the run says so and the
>    options carry a note that limits may strike some later.
> 4. The column grid: bay dimensions and where the grid sits relative to the
>    facade line.
> 5. Anything fixed that panels must meet: entries, party walls, expansion
>    joints, corners that must match.

### Step 2. Divide, and show it

Per elevation, per module:

```
<elevation>  <length> / <module> = <count> panels + <remainder>
```

If the division is exact, say so; that elevation needs no options and the run
moves on.

### Step 3. Lay out the remainder options

For each elevation with a remainder, the standard set, each with its
arithmetic:

```
Option 1  resize all equal      <length> / <count+1> = <new module>
Option 2  end panels            <count> x <module> + 2 end panels @ <dim>
Option 3  one feature bay       <count> x <module> + one panel @ <dim>
```

Under each option, one line on what it gives up: the module moves off the
grid, the corners go special, the odd panel lands where it lands. If the user
named fixed points in Step 1, check each option against them. If a
manufacturer limit was supplied, strike the options that break it, quoting
the limit and its document.

### Step 4. Check the grid and the floors

```
bay / module = <value>   mullion on column line: <yes / no / every nth>
floor-to-floor vs horizontal module: <arithmetic, joint at slab: yes / no>
```

A module that divides the bay keeps mullions off the columns' faces or on
them, whichever the user said they wanted; report the fact, not a preference.

### Step 5. Report, and save if asked

One table, elevations by options, counts and odd dimensions in the cells, the
give-up line under each. Close with what is undecidable from here: the
options that survive arithmetic and limits are design-equal until you choose.
Then ask whether to write it to a file and where. Write it directly; there is
no template and no script.

## Rules

- **Never supply a module, a limit, or a panel size.** There are none in this
  file. The manufacturer's literature, named, is the only source of limits.
- Show the division on every line. A panel count without its remainder hides
  exactly the thing the run is for.
- Options that break a supplied limit are struck with the limit quoted, not
  silently dropped.
- Report grid alignment as a fact per option. Whether mullions should land on
  column lines is the user's call.
- Never convert units, and never round an odd panel to a neater figure
  without labeling it as a changed dimension.
- Do not recommend an option.

## Anti-patterns

- Supplying a maximum glass size because the module looks big. Fabrication
  and shipping limits are the supplier's numbers and change by product and
  by year.
- Rounding the leftover into the last panel without saying so. The odd panel
  is the whole finding.
- Averaging the remainder across panels and presenting the result as the
  original module.
- Judging an option "cleaner". The report carries arithmetic and named
  trade-offs; taste stays with the designer.
- Extending the run into mullion sizing, anchor layout, or thermal checks
  because the dimensions are already on the table.

## Resources

None. This skill is one file. Output is written directly at the path you
choose.
