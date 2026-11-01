---
name: design-kitchen
description: "Lays out a domestic or small commercial kitchen from the sequence of work rather than from a triangle: where things arrive, where they are stored, prepared, cooked, served and cleaned, and what has to be within reach of what. Then works the two things that decide whether the layout survives — where the services can actually go, and what the ventilation demands of the plan and the elevation. Trigger on \"kitchen layout\", \"design the kitchen\", \"galley or island\", \"where does the hood vent\", \"kitchen work triangle\", \"design-kitchen\", or a kitchen with appliances chosen and nowhere settled. Carries no clearances, no aisle widths, no appliance dimensions and no ventilation rates; each comes from the code you quote, the accessibility standard, or the appliance's own data. Commercial kitchens beyond a small back-of-house are a specialist consultant's. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Kitchen"
  summary: "Lay out a kitchen around the work that happens in it, and the services"
  discipline: "design-building-types"
  tags: "Design"
---

# Design Kitchen

Kitchens get laid out from a diagram everyone half-remembers and then fail on
two things the diagram does not contain: where the services can physically go,
and where the extract comes out of the building.

## Scope and limits — read first

**What this does.** Establishes the sequence of work the kitchen has to support,
lays out around it, and then tests the layout against the services and the
ventilation, which are the constraints that actually move things.

**What this does not do.**

- **It carries no dimensions.** No aisle widths, no counter or appliance sizes,
  no clearance in front of anything, no ventilation rate, no duct size, no
  clearance to combustibles. Code from the jurisdiction you quote, accessible
  dimensions from the standard, appliance dimensions from the specific product.
- **It is not a commercial kitchen design.** A back-of-house serving a small
  cafe is in scope. A production kitchen has a specialist consultant, health
  department requirements, and equipment schedules that come from them.
- It does not select appliances. Their dimensions and service requirements
  arrive as input.
- It does not detail the joinery. `design-millwork` does.
- It does not size the extract. The mechanical engineer does; this establishes
  where it has to go and what that costs the plan.
- It does not do accessible design compliance. Point at `/test-ada` and the
  standard you quote.
- It does not replace the Architect of Record.

**What you need before starting.** Who cooks and how. The appliances, or the
fact that they are not chosen. Where the services currently are. What is above
and outside the wall the extract would use. Whether accessibility applies.

## Workflow

### Step 1. Take the cooking, not the style

Ask, in one message:

> 1. Who cooks, how many at once, and what kind of cooking? Someone who cooks
>    from raw daily and someone who reheats need different kitchens.
> 2. What appliances, and are they chosen? A specific range, fridge and
>    dishwasher, or generic?
> 3. Is it open to another room, and what does that room have to tolerate:
>    noise, smell, mess in view?
> 4. Where are the services now: water, waste, gas, electrical? What can move
>    and at what cost?
> 5. What is above the kitchen, and which external wall or roof could an extract
>    reach?
> 6. Does the accessibility standard apply? Quote the relevant provisions.
> 7. Does anyone need to sit at it, eat at it, or work at it?

### Step 2. Lay out the sequence, not the triangle

The work triangle describes one kitchen with one cook. Work the sequence
instead, and place around it:

| Stage | What happens | What it needs beside it |
|---|---|---|

- **Arrive.** Shopping comes in. Where does it land, and is that beside the
  fridge and the store?
- **Store.** Cold, dry, and the things used daily versus twice a year.
- **Prepare.** The largest continuous run of counter, and it wants to be beside
  the sink and the bin.
- **Cook.** The range, with somewhere to put a hot pan down on both sides.
- **Serve.** To where, and does the route cross the working area?
- **Clean.** Sink, dishwasher, bin, and drying. This wants to be out of the
  preparation run rather than in the middle of it.

Then place the fixed points in order of how hard they are to move: the extract
route, then the waste, then the water, then the electrical.

For a second cook or a household that gathers in the kitchen, state where the
person who is not cooking stands, and whether they are in the way.

### Step 3. Work the services, because they decide what is possible

| Service | Where it is now | Where it needs to be | Can it move | Cost of moving |
|---|---|---|---|---|

- **Waste** is the hardest. It falls, it needs a route, and in a renovation
  moving a sink across a room can mean the floor. Point at
  `existing-conditions-survey`.
- **Water** follows the waste and is easier.
- **Gas**, if there is any, and whether the jurisdiction is moving away from it.
- **Electrical**: the load of an all-electric kitchen against the existing
  panel. Point at `explain-panel-schedule` and `design-electrical-room`. This
  surprises people in renovations more than anything else.
- **Extract**: below.

### Step 4. Work the extract as a plan and an elevation problem

The constraint that most often moves the range, and it is decided outside the
kitchen:

- Where can the duct actually go, and how far does it run?
- Which external wall or roof does it come out of, and what does the termination
  look like on the elevation? A hood that vents onto the front facade is an
  elevation decision made in a kitchen plan.
- What does it pass through: joists, a rated assembly, another room's ceiling?
  Point at `design-fire-barrier` and `penetration-review`.
- Recirculating instead: what it does not do, and whether the cooking suits it.
- Make-up air, which a strong extract requires and which the code may.
- Clearance to combustibles above the range, quoted, and what it does to the
  joinery.

State plainly if the range position and the extract route are in conflict.
**Moving the range is usually cheaper than moving the duct.**

### Step 5. Check the layout against the things that make it unusable

Run through, with the dimensions you were given:

- Every door and appliance door swing, against each other and against the aisle.
- Two people passing behind someone at the range or the open dishwasher.
- Where the bin is, and whether it is reachable from the preparation run.
- Corners: what is in them and whether it can be reached.
- What is above the counter and whether an average person reaches it.
- If accessibility applies: knee clearance, reach ranges, approach to each
  appliance, and the turning space, all against the quoted standard.
- Where the daylight is and whether the cook faces a wall. Point at
  `daylight-study`.

### Step 6. Report

- The sequence, and where each stage landed.
- The services table with what has to move and what that costs.
- The extract route, its termination on the elevation, and any conflict with the
  range position.
- Every dimension still open, with who supplies it.
- Every check in Step 5 that could not be run for want of a dimension.
- What has to reach the mechanical and electrical engineers.

Then ask whether to write the layout to a file and where.

## Rules

- **Never supply a clearance, an aisle width, an appliance dimension, or a
  ventilation rate.**
- Work the sequence, not the triangle.
- Place the extract route before the range.
- Ask what the existing panel can take, in any renovation.
- Name the extract termination on the elevation, every run.
- Say when moving the range is cheaper than moving the duct.
- Never design a production kitchen. Name the specialist.

## Anti-patterns

- Laying out from a work triangle and stopping.
- Placing the range where it looks best and finding the duct route afterwards.
- Assuming the existing panel takes an induction range and a double oven.
- Moving a sink across a room in a renovation without asking about the waste
  run.
- Recalling a clearance in front of an appliance.
- A hood venting onto the principal elevation, decided in plan.
- Putting the bin outside the preparation run.
- Treating a small commercial kitchen as a large domestic one.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
