---
name: cad-api-scripting
description: |-
  Generate and debug scripting code for CAD system APIs — Python for commercial CAD platforms, OpenSCAD language scripts, and equivalent programmatic modeling interfaces. Load this skill when the user wants to automate CAD construction, generate geometry programmatically, produce parameter-import scripts, or write reusable CAD macros. Trigger on phrases like "write me a Python script for...", "CAD macro", "OpenSCAD file", "parametric script", "API import for parameters", "script to generate geometry". Do NOT load for manual CAD construction guidance (sketch-by-sketch, feature-by-feature) — that is the cad-construction skill. Do NOT load for pure design exploration without code output — that is design-first-iteration. Complements cad-construction: construction defines WHAT to build, this skill handles HOW to build it programmatically.
---

# CAD API Scripting

A skill for generating, reviewing, and debugging code that drives CAD systems programmatically. Covers Python-based APIs (commercial CAD platforms), declarative languages (OpenSCAD), and similar scripting interfaces.

## When to use

- User has a finished or near-finished design and wants to translate it into a reusable script
- User wants to import a parameter table into a CAD system from JSON/CSV
- User wants to generate repetitive geometry algorithmically (grids, arrays, variant families)
- User is debugging an existing CAD script
- User wants to expose a design as a configurable OpenSCAD module

## When NOT to use

- User is still exploring design options → `design-first-iteration`
- User wants step-by-step manual CAD guidance → `cad-construction`
- User wants general mechanical design principles → `mechanical-design-principles`
- User wants firmware code or web backend code → other engineering skills

## Workflow

### Phase 1: Clarify the target platform

Before writing a single line, confirm:

1. **Which CAD platform / scripting language?**
   - Commercial (Fusion 360, SolidWorks, Onshape, Inventor, NX) — almost always Python or JavaScript-based
   - Open-source (FreeCAD, Blender for CAD, OpenSCAD, CadQuery, Build123d)
   - Declarative (OpenSCAD, JSCAD)
2. **Which API version / library version?** APIs change. An older Fusion 360 script may not run on the current API.
3. **Goal of the script:** one-shot generation, reusable module, parameter-import utility, test harness?

If the user is unclear, ask 1–2 targeted questions. Do not assume.

### Phase 2: Sketch the code structure before writing

For non-trivial scripts, outline in plain text first:

```
- Setup (imports, app/document handle, parameter loading)
- Parameter definitions (from file or hardcoded)
- Helper functions (reusable geometry operations)
- Main construction sequence (sketches, features, assembly)
- Error handling and cleanup
- Save / export step
```

This structure sketch is the place to catch missing inputs, unclear naming, or scope creep — not the middle of a 200-line script.

### Phase 3: Write the code

Principles:

- **Parametric from the start.** Every dimension is a named variable or parameter, never a literal in the middle of code. If the user has a parameter table from `cad-construction` (three-tier structure), mirror that structure in the code rather than inventing a new one.
- **Guard the obvious failure modes.** Check that the document exists, that the target component is found, that a selection is non-empty. Fail with a clear message, not a stack trace.
- **Keep one unit system throughout.** If the CAD system works in cm internally (Fusion 360), convert at the boundary, then keep code in mm (or whatever the user thinks in). Document the convention at the top of the file.
- **Comment intent, not mechanics.** `# Create a 3 mm fillet on the top edge to soften the grip surface` is useful. `# Call addByThreeEdges()` is not — the code already shows that.
- **Naming:** use descriptive names consistent with the parametric convention (`housing_wall_thickness`, not `wt`). Match the names the user is already using in their parameter table — do not re-invent.

### Phase 4: Test plan, even for one-shot scripts

Before handing the script over:

- State explicitly which parameter values were assumed in testing
- Note edge cases the script does NOT handle (zero-width features, negative offsets, etc.)
- If the script modifies an existing document: warn about undo behavior

## Language-specific notes

### OpenSCAD

- Declarative, no loops with state. Think in unions, differences, intersections, and modules.
- Use `$fn`, `$fa`, `$fs` deliberately — cheap during design, expensive during export
- Modules with default parameters enable library-style reuse: `module housing(width=100, height=40, wall=2.4) { ... }`
- For parametric designs with many variants, expose a `Customizer` section at the top with `// [Range]` and `// [dropdown]` annotations
- Version-pin the OpenSCAD version assumption in a comment (dev snapshot vs stable differ in available features)

### Python-based commercial CAD APIs

General patterns (apply across Fusion 360, Inventor, NX, SolidWorks Python wrappers):

- **App and document handles first.** Most APIs require getting the app object, then the active document, then the root component — establish these once at the top.
- **User parameters over feature parameters.** User parameters (project-level named values) survive model regeneration. Feature-local values do not.
- **Transactions / undo grouping.** Wrap related operations in a single undo group so the user can undo the whole script in one step.
- **Error handling with try/except at the outer level**, logging which step failed. Commercial APIs tend to throw informative exceptions — catch them, report them, do not swallow them.
- **Unit handling varies:** some APIs expose values in internal units (often cm), others in document units. Always check, document the convention, and convert at the boundary.

### Parameter-Import scripts (common use case)

When generating a script that reads a JSON/CSV parameter table and writes them into the CAD system's user parameters:

- Source of truth is the parameter table from `cad-construction` (JSON / CSV / Markdown) — the script does not invent parameters
- Preserve the three-tier structure if the table has it (primary / derived / tolerance). Some CAD systems let you group or tag parameters; use that if available.
- Each parameter needs: name, value, unit, optional comment
- If a parameter already exists in the document: update its value, do not create duplicate
- If a parameter name contains invalid characters for the target system: sanitize with a documented rule, not silently
- At the end: summary log of which parameters were created vs updated vs skipped

### OpenSCAD / declarative DSLs

- Emphasis on pure functions and modules
- Customizer-compatible parameter blocks at the top
- `assert()` for preconditions the caller must meet

## Testing and handover

A script is not done when it runs once. Before declaring complete:

- Run with at least one edge-case parameter set
- Verify the output geometry visually (export to STL or screenshot the CAD window)
- Document the command to run the script (how to invoke it in the CAD system)
- Note the assumed API/language version

## Anti-patterns

- **Hardcoding dimensions in the middle of a script.** If a number appears in code that isn't at the top as a parameter, something is wrong.
- **Silent failures.** If a feature can't be created, the script must say so, not continue with an incomplete model.
- **Coupling to the current document state.** A good script works in a fresh document. If it depends on "this is the third component in the tree", it's fragile.
- **Over-abstraction.** Writing a framework when a 30-line script would have done. Match the complexity to the actual problem.
- **Mixing unit systems without conversion.** Producing parts 10× or 0.1× their intended size is the classic API unit bug. Guard against it.
- **Writing code before confirming the platform.** Different APIs, same concept, incompatible code.

## Handover checklist

Before delivering a script:

- [ ] Target platform and API version documented at the top of the file
- [ ] All dimensions exposed as named parameters
- [ ] Error handling at the outer level
- [ ] Unit convention documented
- [ ] Tested with at least one realistic parameter set
- [ ] Invocation command / setup instructions provided

## Bundled helper tool

For Fusion 360 specifically, this bundle ships a parameter-table generator:

```bash
${CLAUDE_PLUGIN_ROOT}/tools/generate_fusion360_parameters.py <parameters.json> <output.py>
```

Input is a JSON list of parameter objects (`{name, value, unit, comment}`); output is a Fusion 360 add-in script that calls `userParameters.add(...)` for each entry. Names and units are strictly validated and string fields are emitted via `repr()` so the generator is safe against malformed or hostile input.

See the docstring of `generate_fusion360_parameters.py` for the full input schema.
