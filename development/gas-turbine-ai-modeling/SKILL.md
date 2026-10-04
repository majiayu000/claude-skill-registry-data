---
name: gas-turbine-ai-modeling
description: Guide AI agents to build, inspect, debug, repair, or review staged MATLAB/Simulink thermodynamic models for gas turbines, especially three-shaft gas turbines. Use when a task involves gas turbine design-point calculation, steady-state thermodynamic modeling, dynamic rotor/volume/combustor modeling, compressor or turbine characteristic maps, MATLAB scripts, Simulink subsystem architecture, model validation, NaN/Inf repair in dynamic Simulink models, or converting hand-built thermal system modeling experience into reusable AI modeling procedures.
---

# Gas Turbine AI Modeling

## Purpose

Use this skill to make AI modeling of gas turbines staged, modular, traceable, and physically checkable. Treat the model as a thermodynamic system that must be built in layers, not as a single block diagram or a direct formula dump.

The default reference case is a three-shaft gas turbine with low-pressure compressor, high-pressure compressor, combustor, high-pressure turbine, low-pressure turbine, power turbine, cooling/bleed flows, rotor dynamics, volume pressure dynamics, and compressor/turbine characteristic maps. Treat it as a deep reference workflow, not as the only valid gas turbine architecture.

## Core Workflow

Always work in this order unless the user explicitly narrows the task:

1. Identify the application scenario, gas turbine structure, working-fluid assumptions, required dynamic depth, and control objective.
2. Confirm the theory/formula sources, or perform traceable literature/source research when formulas are missing.
3. Build or inspect the design-point solver.
4. Convert the design-point calculation to a Simulink design-point model.
5. Convert the design model to a steady-state input-output thermodynamic model.
6. Add dynamic states only after the steady model is validated.
7. Add control only after the open-loop plant initializes and behaves correctly.
8. Validate each stage against the previous stage before adding complexity.

Do not jump directly from user requirements to a dynamic Simulink model. For complex gas turbines, the design point provides the state table, normalized reference values, initial conditions, and physical scale of the later model.

At major stage gates, stop and ask the user to confirm the result before proceeding, unless the user explicitly asked for a read-only plan or fully autonomous exploratory draft.

## Required Modeling Discipline

Before writing or changing code, state the task goal, known facts, necessary assumptions, and verification standard. Distinguish:

- Design requirements: power class, compressor pressure ratio, turbine inlet temperature, efficiencies, pressure losses.
- Application and control target: power generation, propulsion, mechanical drive, hybrid system, grid-connected, islanded, speed control, power control, thrust control, or temperature/surge limiting.
- Design-point outputs: state-point table, air flow, fuel flow, specific work, component powers, bleed/cooling flow coefficients.
- Steady model inputs: air flow, fuel flow, shaft speeds or pressure ratios, component efficiencies, pressure losses.
- Dynamic states: rotor speeds, volume pressures, combustor temperature or fuel/air thermal response.
- Empirical data: compressor maps, turbine maps, fitted neural-network maps, curve fits, or lookup tables.
- Evidence sources: user-provided formulas, textbooks, papers, engineering standards, validated open-source implementations, or assumptions.

Keep units explicit. Use K for temperature, MPa or Pa consistently for pressure, kg/s for mass flow, kW for power, and document any conversion.

## Reference Selection

Load only the reference files needed for the current task:

Minimum reference bundles:

| Task type | Start with |
| --- | --- |
| New project or incomplete request | `references/requirements-and-scope-triage.md`, `references/requirements-intake-template.md`, `references/three-shaft-workflow.md` |
| Formula or property selection | `references/literature-and-formula-evidence.md`, `references/component-equation-templates.md`, `references/gas-property-and-combustion.md`, `references/equations-and-units.md` |
| Existing Simulink audit | `references/model-evidence-audit.md`, `references/dynamic-iteration-map.md`, `references/initial-condition-registry.md`, `references/validation-checklist.md` |
| Existing model repair | `references/existing-model-debug-and-repair.md`, `references/trim-and-initialization.md`, `references/common-pitfalls.md` |
| Map fitting or replacement | `references/characteristic-map-fitting.md`, `references/off-design-matching.md` |
| Control integration | `references/control-integration.md`, `references/control-application-patterns.md`, `references/validation-checklist.md` |
| Delivery or external review | `references/deliverable-definition.md`, `references/modeling-output-templates.md`, `references/model-maturity-and-delivery.md` |

- Before choosing formulas or architecture, read `references/requirements-and-scope-triage.md`.
- When the user request is incomplete or a new project needs structured intake, read `references/requirements-intake-template.md`.
- When formulas, fuel/gas properties, control strategy, or map conventions are missing, read `references/literature-and-formula-evidence.md`.
- To distinguish project-specific rules, generic templates, and external toolkit usage, read `references/source-provenance-and-toolkit-integration.md`.
- For a public placeholder example of expected three-shaft artifacts, read `references/sample-three-shaft-case.md`.
- For source-backed component formula patterns, read `references/component-equation-templates.md`.
- For air/gas properties, fuel-air ratio, combustion efficiency, variable heat capacity, or gas composition, read `references/gas-property-and-combustion.md`.
- For overall modeling order and stage gates, read `references/three-shaft-workflow.md`.
- For MATLAB design-point scripts and state-point calculation, read `references/design-point-solver.md`.
- For Simulink conversion, subsystem interfaces, algebraic-loop handling, and steady-state transition, read `references/simulink-staging.md`.
- For off-design steady matching or dynamic map/flow/shaft matching, read `references/off-design-matching.md`.
- For dynamic rotor, volume, combustor, compressor-map, and turbine-map modeling, read `references/dynamic-modeling.md`.
- Before claiming a model is complete or deciding whether a MATLAB/Simulink wrapper is enough, read `references/model-maturity-and-delivery.md`.
- Before implementing rotor, volume, combustor, or characteristic-map equations, read `references/equations-and-units.md`.
- Before building a dynamic model with multiple feedback loops, read `references/dynamic-iteration-map.md`.
- Before creating or reviewing a large existing `.slx` model, read `references/model-evidence-audit.md`.
- When an existing dynamic `.slx` model cannot simulate, reports `NaN`/`Inf`, fails at an integrator, or needs repair, read `references/existing-model-debug-and-repair.md`.
- When implementing dynamic feedback loops one by one, read `references/dynamic-loop-build-protocol.md`.
- When design-point initial values do not produce zero dynamic residuals, read `references/trim-and-initialization.md`.
- Before adding speed, power, fuel, load, or propulsion control, read `references/control-integration.md`.
- For application-specific controller patterns, such as islanded generation, grid-connected generation, shipboard DC microgrid, mechanical drive, or propulsion, read `references/control-application-patterns.md`.
- Before moving across major model stages, read `references/stage-gates-user-confirmation.md`.
- Before adding `Memory`, `Delay`, `Unit Delay`, integrators, or other feedback state blocks, read `references/initial-condition-registry.md`.
- For compressor/turbine characteristic map fitting, normalization, neural-network maps, or lookup-table replacement, read `references/characteristic-map-fitting.md`.
- For the minimum required artifacts and design-point-to-dynamic mapping, read `references/deliverable-definition.md`.
- When producing stage-gate summaries, loop contracts, initial-condition registries, validation reports, or repair reports, read `references/modeling-output-templates.md`.
- For compact workflow examples and common failure patterns, read `references/case-library.md`.
- For model verification and result checks, read `references/validation-checklist.md`.
- For common AI mistakes and modeling failure modes, read `references/common-pitfalls.md`.
- When testing this skill or preparing an external AI review, read `references/skill-validation-tasks.md`.

## MATLAB and Simulink Tool Use

When a `.m` file is involved, use MATLAB MCP static analysis or execution when useful and safe. When a `.slx` model is involved, use Simulink Agentic Toolkit model-reading tools or MATLAB Simulink APIs to inspect subsystem hierarchy, ports, block types, solver settings, workspace variables, and dynamic blocks.

For a first-pass read-only audit of an existing `.slx`, consider running `scripts/audit_simulink_gasturbine.m` from MATLAB to generate dynamic-state, lookup/map, function-block, routing, and named-candidate tables before editing. Treat the script output as evidence collection, not proof of physical correctness. If direct Simulink tools are unavailable, use the fallback sequence in `references/source-provenance-and-toolkit-integration.md`.

When editing Simulink models, use the Simulink Agentic Toolkit workflow:

1. Use `model_overview` or equivalent to understand the top-level model.
2. Use `model_read`, `model_query_params`, and parameter resolution where available before editing.
3. Plan the data flow and physical variable interfaces.
4. Edit one subsystem level at a time.
5. Re-read and verify the modified scope.
6. Simulate or run focused checks with MATLAB/Simulink tools when safe and relevant.

Do not treat a Simulink model as only a drawing. Inspect the executable relationships among blocks, signals, parameters, initial conditions, and solver settings.

## Output Expectations

For modeling tasks, produce artifacts that another engineer or AI can audit:

- A clear state-point and parameter table.
- Named subsystem interfaces and signal meanings.
- A list of assumptions and unresolved parameters.
- A design-point to steady/dynamic mapping table.
- A mapping from design-point quantities to steady/dynamic initial conditions.
- A validation report comparing design-point, steady-state, and dynamic initial outputs.
- For dynamic Simulink models, an iteration map, loop-by-loop build log, and initial-condition registry.

For skill improvement tasks, add reusable rules to the most specific reference file instead of expanding `SKILL.md` unnecessarily.
