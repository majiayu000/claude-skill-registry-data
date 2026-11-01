---
name: design-elevator
description: "Holds the architectural space an elevator installation needs from the consultant's or manufacturer's data: the hoistway, the pit below the lowest landing, the overrun above the highest, the machine and controller wherever the product puts them, and the lobby and door dimensions at every level. Works the constraints that decide the building — what the pit does to the foundation, what the overrun does to the roof or the height limit, and where the machine has to be if there is no machine room. Trigger on \"elevator pit depth\", \"lift overrun\", \"machine room-less\", \"how big is the hoistway\", \"elevator shaft coordination\", \"design-elevator\", or an elevator specification handed over to fit into a building. Carries no dimensions, no capacities, no speeds and no code requirements; every one comes from the manufacturer, the elevator consultant, or the code you quote. It does not do traffic analysis and does not replace the elevator consultant or the Architect of Record."
license: MIT
metadata:
  title: "Design Elevator"
  summary: "Hold space for the shaft, the pit, the overrun, and the machine"
  discipline: "structure-mep"
  tags: "Design"
---

# Design Elevator

The elevator is drawn as a rectangle on the plan. The things that move the
building are above and below it: a pit that reaches under the lowest floor and
into the foundation, and an overrun that pushes past the highest floor and often
past the height limit.

## Scope and limits — read first

**What this does.** Holds the architectural space for the whole installation
from data you supply, and works the pit, the overrun and the machine location as
the three constraints that reach outside the shaft.

**What this does not do.**

- **It carries no dimensions.** Not a hoistway size, not a pit depth, not an
  overrun, not a car dimension, not a door width, not a clearance. Every one
  comes from the manufacturer's data for the specific product, from the elevator
  consultant, or from code text you quote. **Products differ substantially and a
  remembered figure is a wrong one.**
- **It does no traffic analysis.** How many cars, at what speed and capacity, is
  the elevator consultant's, and it comes to this as an input.
- It does not select a product or a manufacturer.
- It does not design the shaft enclosure's rating. `design-fire-barrier` does.
- It does not cover lift pressurisation, firefighter operation, or emergency
  power beyond naming them as separate requirements.
- It does not replace the elevator consultant or the Architect of Record.

**What you need before starting.** The consultant's recommendation: how many
cars, capacity, speed, type. The manufacturer's dimensional data, or the
consultant's preliminary dimensions. The building: levels served, floor-to-floor,
what is below the lowest landing and above the highest. The code's requirements
for the type proposed. Accessibility requirements from the standard you quote.

## Workflow

### Step 1. Establish the product and the building

Ask, in one message:

> 1. What has the consultant recommended: how many cars, capacity, speed, type
>    (traction, hydraulic, machine room-less), and is a product assumed?
> 2. Do you have dimensional data, and from whom?
> 3. Which levels are served, and what is the floor-to-floor at each? Is the top
>    or bottom floor different?
> 4. What is below the lowest landing: soil, a basement, occupied space, a water
>    table?
> 5. What is above the highest landing: roof, occupied space, a height limit, a
>    planning constraint?
> 6. Is there room for a machine room, or is this machine room-less?
> 7. Any goods, stretcher, firefighter or vehicle lift requirements?

Question 4 and 5 are where the money is. Everything else is a rectangle.

### Step 2. Hold the hoistway, and everything that shares it

| Element | Dimension | Source | Note |
|---|---|---|---|

- Clear hoistway, per car and for a bank.
- Divider beams between cars in a bank.
- Rail brackets and what they fix to, which is a structural interface.
- The counterweight, and which side it runs on. It takes plan space and it
  decides which wall the doors can be in.
- Whether anything else may share the hoistway. Usually very little may, and a
  conduit or a sprinkler routed through it is a common and rejected coordination
  shortcut.

### Step 3. Work the pit, and what it does to the building below

The pit is a hole below the lowest floor and it lands in the foundation:

- Pit depth, from the data, and what governs it for this product.
- What is directly under it. Occupied space under a pit carries its own
  requirements; quote them.
- Groundwater: does the pit go below the water table? Point at
  `design-below-grade-assembly` and at `geotech-report-review`. A pit in water is
  a waterproofing problem with no access for repair.
- Pit drainage or a sump, and where it discharges. Many jurisdictions restrict
  what may drain from a pit.
- Access to the pit: a ladder, a light, a stop switch, and how a person gets in.
- The structural interface: the pit floor takes impact loads, and the structural
  engineer needs to know.

### Step 4. Work the overrun, and what it does above

- Overrun above the highest landing, from the data.
- What that does to the roof: a bulkhead, a projection above the parapet, or a
  penetration through an occupied floor above.
- **Against the height limit.** Elevator overruns and bulkheads are treated
  differently by different zoning texts: some exempt them, some do not, some
  exempt them up to a limit. Quote the text; this decides whether the building
  works.
- Whether the overrun is visible, and what it does to the elevation and to any
  planning constraint.
- Access to the machine, if it is up there.

### Step 5. Locate the machine, controller and everything else that has to live somewhere

Machine room-less does not mean nothing is needed:

- Where does the machine sit, and can it be reached for service?
- Where does the controller go? It usually needs a wall somewhere near the top
  landing, in a space that has to be accessible, and this is discovered late.
- Where does the disconnect go, and does the electrical room know?
- Where is the fire service key switch, the phone line, the emergency power
  connection?
- If there is a machine room: its size, its access, its ventilation or cooling,
  and whether anything foreign may pass through it. Point at
  `design-electrical-room` for the room's own electrical requirements.

### Step 6. Work the landings

- Lobby depth at each landing, and against the accessibility standard you quote.
- Door width and the clear opening, against accessibility and against what has
  to be moved through it: furniture, beds, equipment.
- Sill, threshold and the floor finish at every landing.
- Where a lift lobby is required by code as a separate enclosure, and what that
  does to the plan.
- What happens at the discharge level.

### Step 7. Report

| | Required | Available | Difference |
|---|---|---|---|
| Hoistway | | | |
| Pit depth | | | |
| Overrun | | | |
| Machine / controller | | | |
| Lobby | | | |

Then:

- Every `not supplied` dimension, counted, with who supplies it.
- The pit against the ground conditions, and whether the water question is
  answered.
- The overrun against the height limit, with the zoning text quoted or marked
  open.
- Everything that has to reach the structural engineer.
- Every code and accessibility question raised and not answered.

### Step 8. Save, if asked

Ask whether to write the take-off to a file and where.

## Rules

- **Never supply a dimension.** Not a pit depth, not an overrun, not a hoistway
  size. Products differ and the figure has to come from the product.
- Work the pit and the overrun before the hoistway plan.
- Quote the zoning text on how the overrun counts against height, or mark it
  open.
- Ask what is below the pit and above the overrun, every run.
- Locate the controller and the disconnect, even where there is no machine room.
- Send pit loads and openings to the structural engineer.
- Never do traffic analysis.

## Anti-patterns

- Recalling a pit depth or an overrun for a lift type.
- Drawing the hoistway and leaving the pit and overrun to the shop drawings.
- Assuming an overrun is exempt from the height limit.
- Treating machine room-less as needing no space at all.
- Putting a pit below the water table without raising it.
- Routing a conduit or a sprinkler through the hoistway.
- Sizing the door for the code and not for what has to be moved.
- Discovering the controller location during ceiling coordination.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
