---
name: design-column
description: "Checks a single axially loaded, braced column against the capacity your standard's values produce, with every step of the arithmetic shown: slenderness from your effective length factor, capacity from the expression or table row you supply, demand over capacity at the end. Trigger on \"column check\", \"column size\", \"post size\", \"axial capacity\", \"slenderness check\", \"KL/r\", \"design-column\", or a pasted column load with a trial section. Works with any design standard. The user names the standard and method and supplies the load combinations, the effective length factor, the section and material properties, and the capacity expression or its tabulated value, by typing, pasting, or naming a file; the skill never supplies an engineering value, a buckling curve, or a section from memory or web search. Concentric axial load on a braced member only; combined bending needs your interaction equation or it stops. Preliminary sizing, never a substitute for the Engineer of Record."
license: MIT
metadata:
  title: "Design Column"
  summary: "Check an axially loaded column with the values your standard gives"
  discipline: "structure-mep"
  tags: "Design, Analysis"
---

# Design Column

Take a load, a length, and a trial section, and show the arithmetic that
says whether the column carries it. The slenderness arithmetic is the same
everywhere. The buckling curve, the factors, and the properties are not, so
they come from you.

## Scope and limits — read first

**What this does.** Combines your loads under your combinations, computes
slenderness from the effective length factor you supply, evaluates the
capacity expression you supply with your material and section values in it,
and reports demand over capacity with every step visible.

**What this does not do.**

- **It does not know any engineering values.** No effective length factors,
  no buckling curves or column formulas, no material strengths, no section
  properties, no resistance or safety factors. Every one comes from you,
  cited. That is the design, not a gap.
- **It does not pick K.** The effective length factor is a judgment about
  restraint, and it changes the answer more than most inputs; you supply it
  and it is printed beside the result.
- One member, one storey segment, braced against sway, concentric axial
  load. Sway frames, stepped or tapered members, and built-up sections stop
  the run.
- Combined axial and bending runs only if you supply the interaction
  equation from your standard, written out. Otherwise it stops rather than
  checking the axial term alone and calling it done.
- It does not size base plates, connections, or splices, and it does not
  check fire resistance.
- It does not generate loads and does not chase load paths down a building;
  the load at the top of this column is yours.

**What you need before starting.** The design standard and edition, the
method, the unbraced lengths about each axis, your K, the loads and
combinations, and the section, material, and capacity values from your own
tables.

## Workflow

### Step 1. Establish the standard and the method

Ask, in one message:

> 1. Which design standard governs, and which edition?
> 2. Which design method: limit states with factored loads, allowable
>    stress, partial factors, or another?
> 3. Material: steel, sawn timber, glulam, or reinforced concrete.
> 4. How will you supply values? Type them, paste the table, or name a file.

If the answer to 2 is unclear, stop; a capacity from one method against
loads from another is wrong by the size of the factors.

### Step 2. Collect geometry and loads

Unbraced length about each axis, and the K you assign to each, with a word
on the restraint that justifies it. Loads by source, unfactored. Bracing
that differs by axis is normal; bracing that is unclear stops the run.

Anything unstated is missing. Never substitute a typical value, and never
assume a load is zero because it was not mentioned.

### Step 3. Collect the values

Accept a typed value with its citation, a pasted table, or a file. If none
arrives, the run stops at that value and says so.

| Value | Needed for |
|-------|------------|
| Load combinations, written out | Factoring the loads |
| Section area and radii of gyration, both axes | Slenderness and capacity |
| Material strength and modulus | Capacity |
| The capacity expression or tabulated capacity, cited | Capacity |
| Resistance, safety, or adjustment factors, each named | Capacity |
| Slenderness limit, if your standard sets one | The slenderness check |

A tabulated capacity is welcome: paste the row, name the table, and the
check uses it directly, printed with its citation.

### Step 4. Compute, showing every step

```
Loads
  <each load, as given, with units and source>
Combination used            <written out, cited>
  factored axial load       <arithmetic>
Slenderness
  KL/r, each axis           <arithmetic>
  governing axis            <which and why>
  limit (if supplied)       <as given, cited> — <pass/fail>
Capacity
  <each input, cited>
  expression, as supplied   <written out>
  capacity                  <arithmetic>
Ratio
  demand / capacity         <value>
```

Every input line carries where it came from. If any input is unverified,
the result for that line reads `unverified`, not a number.

### Step 5. If no trial section was given

Do not name one. Report what the demand implies instead: the capacity the
section must deliver at your factors, and, where the expression allows it,
the section property that capacity implies. Then say plainly to pick a
section from your own tables and come back with it.

### Step 6. Report

The ratio, the governing axis, the slenderness result, and the list of
anything unverified. Then:

> Every factor, property, and expression here came from you. I did the
> arithmetic and supplied no engineering values. This is a preliminary check
> of a braced, concentrically loaded member, and it is not a design. The
> Engineer of Record designs the column.

### Step 7. Save, if asked

Ask whether to write the calculation to a file and where. Write it
directly, including the arithmetic. There is no template and no script.

## Rules

- **Never supply an engineering value**, and never evaluate a buckling
  formula you were not handed. There are none in this file.
- **Never pick K.** Print the user's K and their reasoning beside the
  result.
- **Never check the axial term alone when bending exists.** Interaction
  equation or stop.
- **Confirm the design method before collecting values**, and never mix
  methods.
- **Show the arithmetic.** Stop on a missing value rather than proceeding
  with a placeholder.
- Never convert units, and never round an input to a neater figure.
- Say on every run that this is preliminary and not a design.

## Anti-patterns

- Supplying K = 1.0 as a harmless default. It is a restraint judgment, not
  a default.
- Recalling a column formula because the standard is familiar. Editions
  move; the formula comes from the user's edition or not at all.
- Naming a trial section because the load and length make it obvious.
- Running the check about one axis because the other "clearly" does not
  govern.
- Reporting a ratio when one of its inputs was unverified.

## Resources

None. This skill is one file. Output is written directly at the path you
name.
