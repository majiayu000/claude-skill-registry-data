---
name: design-parapet
description: "Works a parapet as the junction of two assemblies rather than as a wall that continues past the roof: takes the wall build-up and the roof build-up you already have, then carries each of the four control layers (water, air, vapor, thermal) up the inside face, over the top and down the outside, naming where each one transfers from one assembly to the other and what happens at the coping, the through-wall flashing, the corners and every interruption. Trigger on \"design a parapet\", \"parapet detail\", \"coping\", \"where does the air barrier turn at the roof\", \"through-wall flashing at the parapet\", \"parapet thermal bridge\", \"design-parapet\", or a wall and a roof named with a request for how they meet at the top. Supplies the ordering and transfer logic and the questions each condition has to answer; supplies no height, no thickness, no slope, no code requirement and no proprietary product. Requires the two assemblies as input and does not design either of them."
license: MIT
metadata:
  title: "Design Parapet"
  summary: "Carry the wall and roof control layers around the one corner that leaks most"
  discipline: "envelope-performance"
  tags: "Design"
---

# Design Parapet

A parapet is not a wall that keeps going. It is the place where two different
assemblies have to hand four control layers to each other, around three changes
of direction, at the most exposed point on the building. It is also usually the
worst thermal bridge on the enclosure and the most reliable source of leaks. It
earns its own pass.

## Scope and limits — read first

**What this does.** Takes an already-designed wall assembly and an already-
designed roof assembly and works the junction between them. For each of the four
control layers it names the plane in the wall, the plane in the roof, and the
physical transfer between the two: where they lap, in which direction, and what
holds the lap. Then works the coping, the through-wall flashing, the corners and
every place the parapet is interrupted.

**What this does not do.**

- **It supplies no numbers.** No parapet height, no coping slope, no flashing
  extension above the roof, no thickness, no fastener spacing, no code
  requirement.
- **It does not design either assembly.** It needs both as input. Run
  `design-wall-assembly` and `design-roof-assembly` first, or bring the two
  build-ups you already have. A parapet worked without knowing where the wall's
  air barrier lives is a drawing, not a design.
- It does not check the arithmetic. The parapet is where the thermal bridge is
  worst, and quantifying it is not done here. Name it and hand it over.
- **It does no structural work.** Parapet stability, wind load, back-up
  attachment, the fixings that hold the coping down in a storm: engineering.
- It does not decide the guard requirement, the height needed to screen
  equipment, or the fall protection strategy. Those set the height and they come
  to this as constraints.
- It does not resolve the roof warranty at the perimeter, which is often the
  strictest condition the manufacturer imposes.
- It does not replace the enclosure consultant or the Architect of Record.

**What you need before starting.** The wall assembly, layer by layer, with its
four control layers located. The roof assembly, the same. The parapet height and
what sets it. Whether anything sits on or is fixed to the parapet. Whether the
roof drains toward it, and where the overflow goes.

## Workflow

### Step 1. Take both assemblies and what sets the height

Ask, in one message:

> 1. The wall build-up, inside to outside, with the four control layers located.
> 2. The roof build-up, deck upward, with the same.
> 3. What sets the parapet height: a guard, equipment screening, a datum, the
>    roof drainage, or all of them?
> 4. Is the parapet backed by the wall structure continuing up, or by something
>    added on top of it?
> 5. Does the roof drain toward this parapet? Where does overflow go, and is it
>    through the parapet?
> 6. Is anything fixed to or through the parapet: davits, anchors, lightning
>    protection, signage, railings, window washing?
> 7. What is already fixed: a coping profile from the facade module, a cladding
>    already dimensioned, a height already agreed with planning?

If either assembly is missing, stop and say so. The parapet cannot be worked
against an unknown.

### Step 2. Carry each control layer around the corner and name the transfer

One row per control layer. The two middle columns are the point of this skill:

| Control layer | Plane in the wall | Plane in the roof | How they transfer | Lap direction |
|---|---|---|---|---|

- **Water.** The wall sheds down its drainage plane; the roof holds water on its
  membrane. Name the through-wall flashing that collects what runs down inside
  the parapet, and where it discharges. A parapet with no through-wall flashing
  drains into the wall below it.
- **Air.** This is the transfer most often drawn as a dotted line and never
  resolved. Name the physical material that connects the wall's air barrier to
  the roof's, over the top of the backup or around it, and say what holds it
  there.
- **Vapor.** Whether the two assemblies' vapor strategies are compatible at this
  junction, or whether the parapet creates a pocket closed from both sides.
- **Thermal.** Where the insulation goes around the parapet, or the fact that it
  does not. If the backup structure runs through uninsulated, state plainly that
  the parapet is a continuous linear thermal bridge along the whole roof
  perimeter, and that it has not been quantified here.

State explicitly for each row whether the parapet is insulated on the inside
face, the outside face, over the top, or wrapped. The answer changes all four
rows.

### Step 3. Work the top, and read the gaps

The coping is the roof of the parapet and it fails the way roofs fail.

| Element | Its job | Value needed from you |
|---|---|---|

Then read between:

- Which way does the coping slope, and toward what? A coping draining outward
  stains the facade; draining inward loads the roof.
- What is under the coping, and is it a continuous waterproof layer in its own
  right, or is the coping the only barrier?
- How are the coping joints made, and what happens at those joints when the
  metal moves?
- Do the coping fixings penetrate a control layer, and what closes each one?
- Does the coping overhang enough to throw water clear on both faces?

### Step 4. Work the corners and the interruptions

Name every one, with what each control layer does there:

- Outside corners and inside corners, where the coping and the flashing both
  have to turn.
- Every place the parapet changes height or steps.
- Every scupper or overflow through the parapet.
- Every anchor, davit base, railing post or lightning conductor that passes
  through the top or the face.
- Where the parapet ends: a return, an adjoining building, an expansion joint.
- Where the roof membrane turns up the inside face and terminates, and what
  holds that termination.

An empty list means one was forgotten.

### Step 5. Name what fails first

For the parapet, report failure behaviour rather than a drying direction, since
the parapet is where both assemblies are least able to dry:

- If the coping leaks, where does the water go, and does it appear inside or
  disappear into the wall?
- If the air barrier transfer is not made, where does the leak show as a stain,
  and in what season?
- If the through-wall flashing has no discharge, what does the wall below look
  like in two winters?

### Step 6. Report, and hand off

The control layer transfer table, the coping table with its notes, the corners
and interruptions, then the failure behaviour. Close with the hand-offs, every
time:

- The thermal bridge here has not been quantified, and it runs the full length
  of the roof perimeter.
- Structural design of the parapet and its fixings is open.
- Air barrier continuity around the whole building belongs to
  `air-barrier-trace`, and this is one of the junctions it will check.
- The roof manufacturer's perimeter requirements have not been read.

Count the open values on the face of the output. Then ask whether to write the
detail to a file and where, and write it directly, tables included.

## Rules

- **Never supply a number.** Not a height, not a slope, not a flashing
  extension, not a fastener spacing, not as a placeholder.
- **Never recall a code or a manufacturer requirement.** Guard heights,
  flashing extensions above the roof and perimeter fastening patterns all come
  from documents you quote.
- Refuse to proceed without both assemblies. This skill is a junction, and a
  junction needs two sides.
- Name the physical material that makes each control layer transfer. A dotted
  line on a section is not a transfer.
- State where the insulation goes around the parapet, every run.
- Name every corner and interruption even when the answer is short.
- Say on every run that the thermal bridge has not been quantified.

## Anti-patterns

- Drawing the parapet as the wall continuing up, with the roof arriving at it.
  Two assemblies meet here and both change.
- Showing the air barrier as continuous across the top without naming what
  makes it continuous.
- Omitting the through-wall flashing because the coping is assumed watertight.
  Copings are joints in a line; they leak by design.
- Recalling how far a membrane has to turn up above the roof surface. That is
  code and manufacturer text.
- Quoting a clause found by web search.
- Calling the parapet resolved with an empty corners list.
- Treating the coping slope direction as a detail rather than a decision about
  which face gets stained.
- Running `air-barrier-trace` from inside this skill. It is a hand-off.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
