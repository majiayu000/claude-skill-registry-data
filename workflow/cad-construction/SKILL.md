---
name: cad-construction
description: |-
  Use after the design concept is settled (via design-first-iteration or equivalent) and the user is ready to translate it into parametric CAD geometry — component decomposition, parameter hierarchy, construction sequencing. Primary platform Fusion 360; the workflow also applies to SolidWorks, Onshape, FreeCAD, Inventor. Consumes design rules from `mechanical-design-principles`. Trigger on phrases like "now I'm building this in CAD", "create a construction plan", "parameter table for the model", "how do I decompose the project into components", "plan sketches and features". Do NOT load during open design exploration (use `design-first-iteration`), for CAD-automation scripts or parameter-import code (use `cad-api-scripting`), or alone when the user needs design rules (load `mechanical-design-principles` alongside).

---

# CAD Construction

A structured workflow for translating a finalized design into a parametric CAD model. This skill assumes the design exploration phase is done — the concept is decided, the remaining work is turning it into geometry.

## When to use this skill

- The design concept is settled (possibly via design-first-iteration) and implementation can start
- The user needs to plan component decomposition before opening CAD
- The user wants a parameter table structured before sketching begins
- The user needs a step-by-step construction sequence (sketches → features → assembly)
- The user wants a construction plan document they can follow or hand over

## When NOT to use

- Open exploration of design options → `design-first-iteration`
- General mechanical design rules (overhang, wall thickness, snap-fits) → `mechanical-design-principles`
- Writing scripts or Python code for CAD automation → `cad-api-scripting`
- Reviewing an existing CAD model for quality issues → use a dedicated design-review pass with CAD context

## Workflow — 4 phases

### Phase 1: Requirements consolidation

The design exploration has already happened. This phase is about **confirming and writing down** the requirements that will drive the CAD work — not re-opening decisions.

**Inputs to capture:**
- Primary function (what the part must do)
- Secondary requirements (nice-to-have, optional features)
- Environmental conditions (temperature, moisture, UV, vibration, IP rating if relevant)
- Manufacturing method (FDM 3D print, SLA, CNC, injection molding — each has different CAD implications)
- Unresolved conflicts carried over from design phase (if any — flag them explicitly)

**Output:** A short requirements block at the top of the construction plan. Not a re-exploration.

**Clarifying questions (if gaps remain):** Max 2–3 targeted questions for truly unresolved aspects. Example:
- "IP rating confirmed at IP65, or still IP54 as earlier?"
- "Final material choice — ABS or ASA?"
- "Tool-less opening stays as requirement?"

### Phase 2: Component decomposition

Break the assembly into **logical components** — each component is a unit that will have its own sketches, features, and manufacturing.

**Tree structure (generic, applies to most CAD systems):**
```
Main Assembly
├── Component 1 (e.g., housing bottom)
│   ├── Body: main structure
│   └── Body: mounting features
├── Component 2 (e.g., housing lid)
└── Purchased parts (screws, inserts, seals, electronics)
```

**For each component, define:**
- **Function:** what it does mechanically / functionally
- **Material:** PLA / PETG / ASA / ABS / PA-CF / aluminum / steel / etc.
- **Manufacturing method:** FDM 3D print, SLA, CNC, sheet metal, injection
- **Critical interfaces:** where it mates with other components (tolerances come from these interfaces)
- **Manufacturing constraints:** print orientation, support strategy, post-processing needs

**Purchased parts list:**
- Fasteners (type, size, length, count)
- Threaded inserts (heat-set / press-fit, M-size)
- Seals (O-rings with dimensions, gaskets)
- Electronics if relevant (part numbers help later)

**Rule:** Start with the fewest components that make the design buildable. Every additional component adds a tolerance stackup and an assembly step. See `mechanical-design-principles` → Principle 3 ("Monolithic before assembled") and Principle 7 ("Minimum interfaces") for the underlying reasoning. Justify each split.

### Phase 3: Parameter design

The most important phase. A well-parameterized model can adapt to new requirements in minutes; a hard-coded one takes hours to change. See `mechanical-design-principles` → Principle 5 ("Parametric construction from day one") for the underlying rationale.

**Parameter hierarchy — three tiers:**

#### Tier 1: Primary parameters (independent)
Base dimensions that fundamentally define the design. These are the values the user actually thinks about and adjusts:
```
main_length = 120 mm
main_width = 85 mm
main_height = 40 mm
```

#### Tier 2: Derived parameters (formulas)
Values computed from Tier 1. Never hard-coded — always expressions:
```
wall_thickness = nozzle_diameter * 4         # 4 perimeters
inner_height = main_height - wall_thickness * 2
seal_groove_width = seal_diameter * 1.05
```

#### Tier 3: Tolerances and fastener specs
Manufacturing-specific values, grouped separately so they can be adjusted independently:
```
screw_diameter = 4 mm                  # M4
heat_insert_diameter = 5.2 mm          # M4 heat-set + 0.2 mm tolerance
clearance_fit_tolerance = 0.3 mm       # moving parts
press_fit_tolerance = -0.15 mm         # permanent fits
```

**Naming convention:** `category_description`. Descriptive names, no abbreviations like `w1`, `d2`. Examples:
- `housing_wall_thickness` (not `wt`)
- `mounting_screw_spacing`
- `tolerance_clearance_fit`

**Reference values for FDM 3D print tolerances:**
See `mechanical-design-principles` → Decision heuristics for the authoritative tolerance grid (press fits, clearance fits, heat-set inserts, O-ring grooves). Use those values here — do not re-derive.

### Phase 4: Construction sequence

A step-by-step plan the CAD session will follow. This is the document that turns "I know what I'm building" into "I know which sketch to draw next."

**Template structure:**

**Step 1: Setup**
- Create new design / document
- Create user parameters (from Phase 3 table)
- Create top-level component structure (from Phase 2)

**Step 2: Main geometry (for each major feature)**
- **Sketch:** plane, geometry, constraints, dimensions (referencing parameters by name)
- **Operation:** extrude / revolve / loft / sweep, with parameters
- **Result:** what body / feature this produces

**Step 3: Detail features**
- Fillets and chamfers (with parameters, not literal radii)
- Holes (location, size, depth — all parameterized)
- Grooves, pockets, ribs
- Thread features if applicable

**Step 4: Sub-components and assembly**
- Sub-component creation and positioning
- Joints / mates / constraints between components
- Interference checks

**Step 5: Manufacturing annotations**
- Print orientation with justification
- Support strategy (where, why)
- Post-processing steps (insert pressing temperature, sanding zones, etc.)

## Output format

The deliverable of this skill is a **construction plan document** — markdown-first, optionally expanded into an interactive HTML tool for parameter editing.

**Minimum viable construction plan:**
- Requirements block (Phase 1 output)
- Component tree with per-component specs (Phase 2 output)
- Parameter table with three tiers (Phase 3 output)
- Construction sequence (Phase 4 output)

**Template:** see `assets/construction_plan_template.md` in this skill folder.

**Interactive tool (optional):** if the user wants live parameter adjustment, an HTML artifact with a parameter editor and live calculation of derived values. Good match for mobile / handy-friendly review during CAD work.

## Best practices

### Parametrization discipline
- Every dimension comes from a parameter. If a literal number appears in a sketch, something is wrong.
- Hierarchy: primary → derived → tolerances. Never mix the levels.
- Naming: descriptive always. The parameter table should be readable by someone who didn't build the model.

### Design for manufacturing in the CAD sequence
Manufacturing constraints (print orientation, overhang angle, layer adhesion direction, wall-thickness grid) are covered in detail by `mechanical-design-principles`. This skill applies those rules in the CAD sequence — specifically:
- **Print orientation is decided in Phase 2**, together with component decomposition, not deferred to export.
- **Every component's critical surfaces** are identified against the chosen orientation before sketching begins.
- **Support-requiring geometry** is redesigned here, not accepted as "we'll just add supports later."

For the underlying rules (45° overhang, wall-thickness = n × perimeters × nozzle, layer-adhesion anisotropy) see `mechanical-design-principles` Principle 4.

### When to not parameterize
- Logos, serial number plates, cosmetic text — not worth parameterizing.
- One-off test parts that will never be iterated — parameters add friction for no benefit. But this is a trap: "one-off" parts often turn out to need iteration.

## Anti-patterns

- **Starting CAD without a parameter table.** Every dimension ends up hard-coded, and the first design change wastes an afternoon.
- **Over-decomposition.** Splitting into 8 components because "that's how it would be molded." FDM doesn't have injection-mold constraints. See `mechanical-design-principles` → Principle 3.
- **Premature detailing.** Adding fillets and chamfers before the main shape is proven. Fillets go in late.
- **Hard-coded tolerances.** `5.2 mm` for an M4 insert is a magic number. `M4_nominal + tolerance_insert` is the same value, expressed as intent.
- **Ignoring print orientation until export.** Leads to geometry that can't be printed without aggressive support.

## Handover checklist

Before calling a construction plan complete:

- [ ] Requirements block written (confirmed, not re-opened)
- [ ] Every component has: function, material, manufacturing method, critical interfaces
- [ ] Purchased parts list with sizes and counts
- [ ] Parameter table with three tiers, all names descriptive
- [ ] Construction sequence written step by step
- [ ] Print orientation stated and justified
- [ ] Unresolved issues flagged explicitly (not hidden)
