---
name: mechanical-design-principles
description: |-
  Guides mechanical design decisions toward elegant, manufacturable, serviceable solutions with a strong bias toward tool-less assembly, monolithic parts, and form-follows-function. Provides the design rules (the WHAT and WHY — overhang, wall thickness, snap-fit sizing, tolerances, material matching). Load when the user designs mechanical parts, enclosures, housings, brackets, mounts, assemblies, or any 3D-printed component — particularly important for FDM with engineering filaments (ABS, ASA, PC, PA-CF, PETG-CF). Trigger on phrases like "design a housing", "build an enclosure", "how should I mount", "I'm designing a part", "3D print", snap-fit/press-fit questions. Do NOT load alone for iterative design conversations (load `design-first-iteration` alongside), for CAD workflow / parameter tables (use `cad-construction`), or for CAD-automation code (use `cad-api-scripting`).

---

# Mechanical Design Principles

A design philosophy that treats every feature as a justified decision, favors elegant simplicity over accumulated complexity, and designs for manufacturability from the first sketch. FDM-focused but broadly applicable.

The foundation is two stances: **form follows function** (every feature earns its place by serving the mechanism) and **minimum interface count** (fewer parts, fewer fasteners, fewer joints wherever possible).

## Read the whole skill before applying

This skill has seven core principles, supporting principles, anti-patterns, decision heuristics, and worked examples — all load-bearing. Stopping at the first few principles risks missing rules that prevent common design mistakes (e.g., Principle 4 on manufacturing, Principle 5 on parameters, the decision heuristics for tolerances). Read to the end.

## Relation to other skills

- For the **conversation framework** (how to iterate, when to verify orientation, how to structure decisions): load `design-first-iteration` alongside this skill. This skill gives the rules; design-first gives the process.
- For **CAD workflow** (parameter tables, component decomposition, construction sequencing): use `cad-construction`. That skill consumes the rules from this one and applies them in a CAD session.
- For **CAD automation / scripting** (Python, OpenSCAD, API code): use `cad-api-scripting`.

## The Seven Principles

### 1. Form follows function — every feature earns its place

Every geometric feature must trace back to a specific functional requirement. If you cannot articulate why a feature is there — what force it carries, what tolerance it guarantees, what access it enables, what behavior it produces — then the feature is decorative at best, structural debt at worst.

**Abstract rule:** Before adding geometry, state the function. If the function is unclear, don't add the geometry.

**FDM concrete application:**
- Thickened zones should correspond to mechanical load paths (snap-fit roots, clip arms, mount interfaces), not aesthetic preferences
- Ribs and bosses belong only where stress or stiffness is needed
- Radii and fillets at stress concentrations (where two perpendicular surfaces meet under load), not merely "everywhere for the look"
- Fasciae and skirts should hide something specific (a seam, a cable path, a connector) — not be there for appearance alone

**Test:** For every feature on the part, ask "what happens if I remove this?" If the answer is "nothing" or "it looks worse", the feature probably shouldn't exist. If the answer is "the seal leaks" or "the board rattles" or "the user cuts their hand", the feature is justified.

### 2. Tool-less assembly wherever possible

Screws are failure points: they require pre-drilled holes, insert threads or heat-set inserts, correct torque, thread locker, service access for the driver. Every screw is a place where assembly can go wrong. Prefer snap-fits, press-fits, bayonet mounts, magnetic latches, or print-in-place mechanisms whenever structural and safety requirements allow it.

**Abstract rule:** A user or servicer should be able to assemble and disassemble the product with their hands alone, or with a single standard tool (plastic card, small flat screwdriver). Screws appear only when required by mechanical load, legal/safety standard, or thermal constraints.

**FDM concrete application:**
- **Snap-fits with defined engagement** (e.g., 1.5–2 mm interference, 25–30° insertion ramp) carry surprisingly high loads when designed correctly
- **Print-in-place mechanisms** (a single print produces a moving assembly) eliminate multi-part joint tolerances — key parameter is the gap: 0.4 mm for FDM 0.6 mm nozzle, 0.3 mm for 0.4 mm nozzle
- **Bayonet connections** for serviceable assemblies that need many cycles
- **Screws justified only when:** 230V AC / mains connections (safety), load paths exceeding ~100 N per joint, parts expected to cycle > 1000 times
- Sacrificial features (plastic card slots for snap release) make tool-less disassembly possible without compromising hold strength

**Common failure mode:** Reaching for screws reflexively when a snap-fit would work. Screws feel "more professional" but often introduce more problems than they solve.

### 3. Monolithic before assembled

One part is better than two fastened parts, which is better than three, and so on. Every interface between two parts introduces a tolerance stackup, an assembly step, a failure mode, and a loose fastener that can vibrate out. If a feature can be integrated into the main body without compromising the print, integrate it.

**Abstract rule:** Before designing a separate component, ask whether it can be a feature of an existing part. Draw the boundary at printability and service requirements, not at how the part would have been made in injection molding.

**FDM concrete application:**
- Cable guides, board-retention clips, alignment pins, strain reliefs — all should be printed features of the main housing, not separate pieces
- Integrated hinges via print-in-place with a 0.4 mm gap
- Integrated living hinges in thin TPU or PP regions
- Mounting bosses grown from the main body, not snapped in later
- Multi-color/multi-material features (logos, indicators) as part of the main print where possible
- Exception: parts with genuinely different material requirements (a hard structural shell + soft elastomer seal). Even then, consider whether the soft part can be printed in place rather than separately molded

**The trap of "assembled because that's how it's done":** Injection-molded products often have separate parts because the tooling required it. FDM has no such constraint — but designers trained on injection-molding patterns carry the assembly assumption forward.

### 4. Design for manufacturing from the first sketch

Manufacturing constraints are not afterthoughts. Print orientation, overhang angle, layer adhesion direction, material flow, and support requirements all shape what geometry is possible. A design that ignores these constraints will either fail to print or will print with compromises that undermine the original intent.

**Abstract rule:** While sketching, continuously ask: "how is this made, and what forces will the manufacturing process impose on the geometry?"

**FDM concrete application:**
- **Overhang rule:** surfaces sloping more than 45° from vertical need support. Design with overhangs below 45° wherever possible, or orient the part so overhangs become vertical
- **Bridge distance:** short bridges (< 5 mm) print cleanly; longer bridges sag. If a bridge is needed, keep it short
- **Support avoidance:** print orientation is a design decision. Choose the orientation first, then design geometry that's compatible
- **Layer adhesion is weak:** anisotropic strength means critical load paths should run parallel to layers, not across them. Snap-fit arms should bend around a layer, not through them
- **Wall thickness = n × perimeters × nozzle diameter:** 0.6 mm nozzle × 4 perimeters = 2.4 mm wall. Thickness in between (e.g., 2.0 mm with 0.6 mm nozzle) produces either gaps or over-extrusion. Snap dimensions to this grid
- **First-layer surface is different from other surfaces:** it's usually flatter, may have elephant's foot, may have brim residue. Don't put precision surfaces on the first layer
- **Smallest feature ~ nozzle diameter:** details smaller than the nozzle can't be reliably produced. 0.6 mm nozzle → minimum feature size ~ 0.5–0.6 mm

**Common failure mode:** Designing the "ideal" geometry in CAD and discovering later that it requires 40% support volume, 8-hour print time, and post-processing work that destroys the surface finish.

### 5. Parametric construction from day one

Every dimension should be a parameter, every derived dimension should be an expression. When the user inevitably asks "what if we make the housing 10 mm wider?", a parametric model updates in seconds. A non-parametric model requires redoing the CAD from scratch.

**Abstract rule:** There are no "magic numbers" in a design. Every number is either a user-set parameter or a derivation from other parameters.

**FDM concrete application:**
- Use tools like Fusion 360's parameter system (`Modify → Change Parameters`) and reference parameters in every sketch dimension
- Name parameters descriptively: `housing_width`, `window_x = (housing_width - window_width) / 2`, not `d1`, `d2`
- Group parameters by category in the parameter table (housing dimensions, window dimensions, seal parameters, snap parameters, board positions)
- Make tolerance parameters explicit: `board_tolerance`, `seal_tolerance`, not hardcoded into feature dimensions
- Nozzle-dependent parameters link back to a `nozzle_diameter` parameter: `wall_thickness = 4 * nozzle_diameter`. Then a nozzle change propagates automatically
- Keep a reference document (a parameter table) alongside the CAD model that lists all parameters with descriptions — for future self and collaborators

**Common failure mode:** Hard-coding dimensions in individual sketches, then hunting through 30 features to change them when a parameter shifts.

### 6. Design the service case, not just the use case

The product will be assembled once, but may need to be serviced many times. Designing for serviceability means thinking through the disassembly sequence early: what tool is needed, what part has to come off first, can components be replaced individually, is access physically possible.

**Abstract rule:** Before finalizing a design, run through a mental disassembly. "If the display dies in 3 years, how does a technician replace it?" If the answer requires destroying a part, the design is incomplete.

**FDM concrete application:**
- **Layered access:** outer shell with snap release → inner structural frame → modular subassemblies. Most-serviced parts at the outer layer
- **Asymmetric snap release:** snaps that release from a specific access direction (plastic card slot, small screwdriver notch) rather than pure compression that might require specialized tools
- **Cable disconnection before structural removal:** cable connectors should be accessible without removing a structural member first
- **Labeled orientation:** if a part is orientation-sensitive, mark it (arrow, embossed text, keyed geometry) rather than relying on the technician's memory
- **Fastener consistency:** if screws are needed, use one size throughout the product. Mixed fasteners ("2× M3×8, 4× M2.5×6, 1× M4×10") get lost in the field within the first service cycle

**Heuristic:** Sketch the "exploded view" of the product, showing each part pulled out in its disassembly order. If the exploded view is awkward, the design is awkward.

### 7. Minimum interfaces, redundant at critical points

Every interface (joint, fastener, seal, mating surface) introduces a tolerance to manage and a failure mode to worry about. Reduce interfaces where possible — but at points where failure would be catastrophic (safety-critical seals, load-bearing mounts), use redundancy.

**Abstract rule:** Count the interfaces in your design. Challenge each one: can it be eliminated by merging parts, or is it carrying real function? For the interfaces that survive, identify which are catastrophic if they fail — those need redundancy.

**FDM concrete application:**
- **Tolerance stackup:** each interface adds ±0.1 to ±0.3 mm uncertainty in FDM. A 5-interface chain can accumulate ±1 mm — often enough to break a design. Interface count directly determines precision
- **Redundant snaps:** critical latches should have 2+ independent snap engagements. The example from a real project: three identical ramp-snaps at 120° around a cylinder, any one of which would hold, but all three together provide generous safety margin
- **Double-sealed interfaces:** where water or dust entry is critical, use two seals in series (labyrinth + gasket, for example)
- **Single-purpose interfaces:** a bolt should carry load OR locate a part, not both — carrying both functions makes tolerances fight each other
- **Minimum 3 points for alignment:** exactly 3 points is deterministic (a plane is defined by 3 points); 4+ points introduce over-constraint and unpredictable contact

**Heuristic:** For each joint, draw a free-body diagram. If forces act on the joint from more than one direction, decompose into separate joints each handling one direction.

### 8. Component-first: place purchased parts before drawing housing

Lay out the bought-in components — speakers, driver boards, batteries, fans, sensors — as fixed geometry first, with their real outlines, mount patterns, connector orientations, and clearance volumes. Then design the housing **around** them. Conflicts (cable routing, mount-hole collisions, clearance violations, thermal hot-spots near electronics) become visible immediately, and the necessary attachment features (snaps, bosses, slots) emerge from the geometry rather than being retrofitted.

**Abstract rule:** No housing surface is drawn before every functional internal component is in place as a constructive reference. The housing is the last thing to be designed, not the first.

**FDM concrete application:**
- Import or build a **simplified solid** for each purchased component: bounding box plus mount-hole pattern plus connector cone (the volume the cable + connector needs to extract)
- Position components by **function** (driver firing direction, button reach, port access, thermal flow) before any housing surface exists
- Run a **clearance check** — minimum 0.5 mm air gap between components, 2 mm to housing wall, 5 mm to thermal-sensitive surfaces
- Boss/snap features **inherit position** from the component — `mounting_boss_x = driver_position_x + bcd/2`, not a literal number
- Cable channels are designed as **explicit volumes**, not "we'll find a way later"

**Failure mode without component-first:** the housing has the right outer shape but the bought components don't fit, fights with mount holes, cables pinch on closure. Discovering this at first prototype costs a full re-print cycle.

**See also:** Principle 5 (Parametric construction) — component positions become primary parameters that the housing references.

### 9. Print-bed constraint as hard design boundary

Build-volume of the target printer is a **hard geometric constraint** that must shape decomposition before the first sketch is drawn. A part exceeding the bed by 5 mm is not "almost printable" — it is unprintable until split or scaled. Do the split decision **at the design table**, with a strategy that turns the seam into a feature, not at the slicer where it becomes a hidden compromise.

**Abstract rule:** Know the printer's `(X, Y, Z)` build volume before sketching. Each component must fit individually. If a logical component exceeds the volume, split at a designed location — never let the slicer auto-split.

**FDM concrete application:**
- **Reference build volumes:** Bambu Lab H2D ≈ 280 mm Z, Bambu X1C ≈ 250 mm Z, Prusa MK4 ≈ 210 mm Z. Always check the actual printer in use.
- **Split locations as design features:** at an LED ring (translucent acrylic conceals the seam), at a material change (carbon-fiber-reinforced lower section + glass-fiber upper), at a structural ring that doubles as alignment + sealing groove. Industry examples: premium speaker designs hide splits at LED rings or at metal-to-fabric transitions
- **Sealing strategy at split:** if the assembly must be airtight (acoustic enclosure, IP-rated housing), the split needs a TPU O-ring groove or labyrinth seal — designed in, not added later
- **Pedestal as reserve:** the foot of a tall part can absorb 30–80 mm of "extra height" the printer can't take in one piece, while keeping the visible body monolithic. Example from a tall speaker housing: 110 mm pedestal + 280 mm body = 390 mm total, body prints in one job at the 280 mm Z-max bed of a typical large printer

**Anti-pattern:** Designing without checking the build volume, then "scaling down by 10 % in the slicer". Scales every dimension including the threaded inserts and the bought-component cutouts. Always splits, never scales.

## Supporting Principles (apply as needed)

Beyond the seven core principles, a handful of supporting heuristics apply in specific situations:

### Force flow in straight lines

Loads should travel from application point to reaction point along the shortest, most direct path. Indirect load paths introduce bending moments in parts that were designed to carry compression, and they waste material. When you draw the load path on a sketch, it should look like a river — straight, gradually widening where loads accumulate, narrowing where they don't.

### Poka-Yoke (mistake-proofing) by geometry

If there's a wrong way to assemble a part, eventually someone will. Design asymmetries — a notch, an offset hole, an angled key — that make wrong assembly physically impossible rather than just mentally avoidable. Connectors (electrical and mechanical) should be shaped so they can only mate one way.

### Material matches the load profile

Use the right material for each function: rigid polymer (ABS, ASA, PC) for structural parts; elastomer (TPU) for seals and dampers; metal for thermal, electrical, or high-load interfaces. Don't force one material to do a job another does better. Multi-material parts (printed or assembled) are often cheaper and better than a single material compromise.

### Haptic quality is functional

Edges that will be touched should be radiused (R0.5–R1.0 mm is the typical sweet spot). Insertion surfaces should have chamfers (1.5 × 45° is a generous, forgiving chamfer). These aren't decorative — they're the difference between a product that feels good to use and one that feels cheap or hostile.

### Symmetry and repetition reduce cognitive load

If you can use the same feature four times instead of four different features, do so. The same snap geometry on all 4 sides of a housing is easier to design, easier to print, easier to service, and easier to document than 4 different ones. Repetition is not laziness — it's a design discipline.

### Sacrifice features rather than structural elements

If something will fail under abuse, let it be a replaceable minor feature (a snap tab that breaks off cleanly and can be re-printed) rather than a structural element (a hinge pivot that destroys the whole housing). Design the failure mode, don't let it design itself.

## Anti-patterns to avoid

**Over-featured design.** Adding ribs "for strength" without calculating where stress actually occurs. Often makes parts heavier without making them stronger.

**Injection-molding mindset in FDM.** Designing multi-part assemblies because that's how the factory would have done it. FDM removes that constraint — use the freedom.

**Screw proliferation.** Using screws for every fastening because it "feels solid." Creates service nightmares and assembly cost.

**Hardcoded dimensions.** Building a CAD model where every number is a literal rather than a parameter. First design change wastes hours.

**Support-heavy geometry.** Designing the ideal geometry first, then discovering it needs supports everywhere. Re-orientation or re-design usually wins.

**Single-purpose parts that could merge.** Two parts that are always used together and have compatible requirements should often become one part. Evaluate at every design review.

**Features without force paths.** A bolt that doesn't correspond to a load, a rib that doesn't run along a stress line. Parts accumulate decorative geometry that fights the engineer's intent.

**Ignoring the service case.** A product that's hard to service is a product that gets replaced instead of repaired. In many markets this is no longer acceptable.

## Decision heuristics — quick reference

- **Joint type?** Start with snap-fit. Move to screws only if load, safety, or cycle count demands it.
- **Part count?** Start at 1. Add parts only when printability, service, or material mix forces separation.
- **Wall thickness?** n × perimeters × nozzle diameter. Don't invent thicknesses off this grid.
- **Corner radius?** R0.5–R1.0 on touched edges; R at stress concentrations; chamfer on insertion surfaces.
- **Tolerance?** 0.3–0.5 mm on parts that mate by sliding; 0.1–0.2 mm on parts that mate by pressing; print-test any critical tolerance.
- **Support?** Reorient first, redesign second, add supports as last resort.
- **Parameter?** Every dimension. No exceptions. Every derived dimension is an expression.
- **Orientation mark?** Anything orientation-sensitive gets a visible mark (arrow, text, keyed feature).
- **Convex outer profile (rotationally-symmetric bodies)?** For revolve profiles with a max-radius bulge somewhere along the length, validate that `dR/dz` decreases monotonically past the bulge — no slope reversal. A spline that meanders produces a visible waist (concave middle), which almost never matches the design intent. Quick check: list slopes between adjacent control points. Each slope past the bulge must be more negative than the previous one. If not, drop or move the offending control point.
- **Print-section joint as feature, not seam?** When the build volume forces a split, place the joint at a designed feature — a translucent LED ring, a metallic insert, a TPU O-ring channel, an alignment groove. The "seam" becomes part of the look. Picking the joint location at the design table, not at the slicer, is the difference between a product and a printed part.

## Examples from real design sessions

**Example 1: Redundant snaps instead of a single large snap**
> Task: Hold a cylindrical body inside a tube with rotational freedom but axial constraint.
> Naive: Single large snap-arm on the inside of the tube gripping a ring groove on the cylinder.
> Principled: Three identical ramp-snaps at 120°, each engaging the same ring groove. Each snap needs only 1/3 the force, all three together center the cylinder automatically, and the geometry is symmetric and print-friendly.

**Example 2: Print-in-place over post-assembly**
> Task: A clip-body that mounts into a tube, stays rotatable, and cannot be pulled out.
> Naive: Print tube and clip separately, assemble with snap or retainer ring.
> Principled: Print the clip-body in one piece (cylinder + connecting web + dovetail all monolithic), and print the tube with the retaining snaps print-in-place. First-time assembly inserts the clip, the snaps engage in the ring groove, the assembly is permanent but serviceable.

**Example 3: Integrated seal groove, not glued gasket**
> Task: Seal a display window against an ABS housing.
> Naive: Flat TPU gasket, glued around the window with silicone.
> Principled: L-shaped seal groove machined into the ABS inner corner, TPU seal with matching L-profile dropped in from behind, rim of ABS housing hides the seal from the outside. No adhesive, field-replaceable, UV-protected by the ABS rim.

**Example 4: Parametric housing, not hard-coded**
> Task: 3D-printed enclosure for a specific PCB.
> Naive: Start with the PCB dimensions and draw the housing at those exact measurements.
> Principled: Set up parameters (`pcb_width`, `pcb_height`, `clearance`, `wall_thickness`, `nozzle_diameter`), then derive everything (`housing_inner_width = pcb_width + 2 * clearance`, `housing_outer_width = housing_inner_width + 2 * wall_thickness`, `wall_thickness = 4 * nozzle_diameter`). When the PCB revision comes with different dimensions, change 2 parameters and rebuild.

## When to use this skill

Use this skill whenever the user engages in mechanical design work, particularly:
- Enclosures, housings, brackets, mounts, adapters
- 3D-printable parts and assemblies
- Mechanical interfaces (snap-fits, press-fits, hinges, slides)
- CAD construction sessions (load alongside `cad-construction`)
- Design reviews of existing mechanical designs
- Material or fastener selection

For iterative design conversations, load this skill **alongside** `design-first-iteration` — they complement each other. This skill is the content (rules and heuristics); design-first is the process (conversation framework, pre-design checklist, verification habits).

The principles apply broadly, but concrete examples and numerical rules assume FDM 3D printing with a 0.4 or 0.6 mm nozzle and engineering filaments (ABS, ASA, PC, PA-CF, PETG-CF). For injection molding, sheet metal, or CNC machining, the principles translate but the specific numbers do not.
