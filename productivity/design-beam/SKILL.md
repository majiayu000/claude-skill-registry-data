---
name: design-beam
description: "Sizes a single simply-supported beam in steel, wood, or reinforced concrete for a known span, tributary load, and deflection limit, showing every step of the arithmetic. Trigger on \"size beam\", \"preliminary beam size\", \"pick a section\", \"glulam beam size\", \"concrete beam size\", \"beam deflection check\", \"design-beam\", or a pasted span with loads. Works with any design standard. The user names the standard, the design method, and supplies the load combinations, material properties, section properties, resistance factors, and deflection limit, by typing them, pasting the table, or naming a file. The skill never supplies an engineering value from memory or from web search. Preliminary sizing only, for a fully braced simple span, and never a substitute for the Engineer of Record."
license: MIT
metadata:
  title: "Design Beam"
  summary: "Size a simply-supported beam in steel, wood, or concrete"
  discipline: "structure-mep"
  tags: "Design, Analysis"
---

# Design Beam

Take a span, a load, and a trial section, and show the arithmetic that says
whether it works. The arithmetic is the same everywhere. The factors, the
properties, and the limits are not, so they come from you.

## Scope and limits — read first

**What this does.** Combines your loads with your load combinations, computes
demand, compares it against the capacity you supply, checks deflection against
the limit you supply, and shows every step so an engineer can follow it in a
minute.

**What this does not do.**

- **It does not know any engineering values.** No section properties, no
  material strengths, no resistance or safety factors, no load combinations, no
  deflection limits. Every one of them comes from you. That is the design, not a
  gap.
- **It does not size anything you have not given it a trial section for.** It
  can tell you the section property you need, so you can look up a section that
  has it, but it will not name a section from memory.
- It covers a single simply-supported span, fully braced, uniformly loaded or
  with point loads you locate. Continuous spans, cantilevers, and partial
  bracing stop the run.
- It does not do composite action, torsion, lateral-torsional buckling beyond
  the fully braced case, vibration, connections, fire resistance, prestressing,
  or panel design.
- It does not generate loads. Wind, snow, and seismic values come from your own
  site criteria.
- **It is preliminary sizing, and it is not a design.** The Engineer of Record
  designs the beam.

**What you need before starting.** The design standard and edition, the design
method, your geometry and loads, and the material and section values from your
own tables.

## Workflow

### Step 1. Establish the standard and the method

Ask, in one message:

> 1. Which design standard governs, and which edition? Name the loading standard
>    separately if it is a different document.
> 2. Which design method: limit states with factored loads, allowable stress,
>    partial factors, or another? This decides what I ask for next, so I will not
>    assume.
> 3. Material: steel, sawn timber, glulam, or reinforced concrete.
> 4. How will you supply values? Type them, paste the table, or name a file.

If the answer to 2 is unclear, stop. Running an allowable-stress check with
factored loads, or the reverse, produces a confident number that is wrong by the
size of the factors.

### Step 2. Collect geometry and loads

**Geometry.** Clear span. Tributary width. Confirmation that both ends are
simply supported. Bracing: continuous, or the brace spacing if discrete. Discrete
bracing stops the run unless you confirm the section is fully braced at that
spacing.

**Loads, unfactored and separated by source.** Dead. Live, with the category if
your standard reduces live load by category. Snow. Roof live. Rain. Point or
partial loads with their locations. Self-weight, either included in the dead
load or added after a trial section is chosen, stated either way.

**Deflection.** The limit, as a fraction of span, and which loads it applies to.
Name the row it came from. Camber, if any.

Anything unstated is missing. Never substitute a typical value, and never assume
a load is zero because it was not mentioned.

### Step 3. Collect the values

For each of these, accept a typed value with its citation, a pasted table to
read it out of, or a file to read. If none arrives, the run stops at that point
and says which value it is waiting for. Do not proceed with a placeholder.

| Value | Needed for |
|-------|------------|
| Load combinations, written out | Factoring the loads |
| Live load reduction rule, if any | Reducing live load |
| Material strength values | Capacity |
| Modulus of elasticity | Deflection |
| Adjustment or resistance factors, each named | Capacity |
| Section properties for the trial section | Demand and deflection |
| Deflection limit | Serviceability |

For timber, ask which adjustment factors apply and what each one is, rather than
accepting a single combined figure. A combined factor nobody can decompose is
not checkable.

### Step 4. Compute, showing every step

Print the arithmetic, not the result.

```
Loads
  <each load, as given, with units>
Combination used            <written out, cited>
  factored line load        <arithmetic>
Demand
  moment                    <formula, then arithmetic>
  shear                     <formula, then arithmetic>
Capacity
  <each input, cited>
  moment capacity           <formula, then arithmetic>
  shear capacity            <formula, then arithmetic>
Ratios
  moment demand/capacity    <value>
  shear demand/capacity     <value>
Deflection
  <inputs, cited>
  computed                  <arithmetic>
  limit                     <as given, cited>
  ratio                     <value>
```

Every line of input carries where it came from. If any input is unverified, the
result for that line reads `unverified`, not a number.

### Step 5. If no trial section was given

Do not name one. Instead, rearrange the check and report the section property
required: the section modulus or moment of inertia the demand implies at the
capacity the user's factors give. Then say plainly that they should pick a
section with at least that value from their own tables and come back with it.

This is the one place the skill would be most tempted to recall a section
designation, and it is exactly where a recalled number is least detectable.

### Step 6. Report

The ratios, the governing check, and the deflection result. The list of anything
unverified. Then:

> Every factor, property, and limit here came from you. I did the arithmetic and
> supplied no engineering values. This is preliminary sizing for a fully braced
> simple span, and it is not a design. The Engineer of Record designs the beam.

### Step 7. Save, if asked

Ask whether to write the calculation to a file and where. Write it directly,
including the arithmetic. There is no template and no script.

## Rules

- **Never supply an engineering value.** Not a section property, not a strength,
  not a factor, not a combination, not a deflection limit. There are none in
  this file.
- **Never name a section from memory.** Report the property required instead.
- **Confirm the design method before collecting values**, and never mix factored
  loads with allowable stresses.
- **Show the arithmetic.** A result without its steps cannot be checked, and an
  unchecked structural number is the worst output this catalog can produce.
- **Stop on a missing value** rather than proceeding with a placeholder.
- Never convert units, and never round an input to a neater figure.
- Say on every run that this is preliminary and not a design.

## Anti-patterns

- Naming a trial section because the span and load make it obvious. That is a
  recalled value with an engineer's authority attached to it.
- Filling a resistance factor, a load factor, or a modulus from memory because
  the value is standard. Standards change between editions and between countries.
- Combining timber adjustment factors into one number nobody can decompose.
- Reporting a demand-to-capacity ratio when one of its inputs was unverified.
- Assuming a load is zero because the user did not mention it.
- Bundling a section property table or a factor table into this skill later. It
  has none on purpose.

## Resources

None. This skill is one file. Output is written directly at the path you name.
