---
name: quiet-signal-design
description: Apply or audit the approved Quiet Signal core visual language when the user explicitly asks for Quiet Signal styling on a defined website, interface, poster, social graphic, report, presentation, or other design artifact. This skill supplies visual identity and rule checks; it does not plan content, invent platform requirements, or run a production pipeline.
---

# Quiet Signal Design

Quiet Signal is a visual style contract. It is not a content generator, layout template, platform kit, compiler, renderer, runtime, or end-to-end production workflow.

For every accepted task, read [references/SPEC.md](references/SPEC.md) completely before making visual decisions. Treat it as the only normative source. Do not recover rules from older installations, private implementations, screenshots, or memory when they differ from the specification.

## Choose one mode

### Apply

Use Apply when the user asks to create or restyle a defined artifact in Quiet Signal.

Before designing, establish only the information required by the actual deliverable:

- design object and intended outcome;
- supplied content and protected facts or functions;
- required structure or behavior, when any;
- target environment, dimensions, and technical limits;
- requested delivery depth.

Proceed when these are sufficiently clear. Ask one concise question only when a missing item would materially change the artifact. Do not turn this into a setup interview.

Apply the specification to color, typography, spacing relationships, geometry, surfaces, imagery, motion, hierarchy, and emphasis. Local layout choices needed to realize the artifact are allowed, but they belong to that artifact and must not be presented as Quiet Signal rules.

If platform-specific requirements are absent, either use constraints explicitly supplied by the user or state the exact unverified boundary. Do not invent a Web, Xiaohongshu, poster, slide, report, or app Kit inside this skill.

### Audit

Use Audit when the user asks whether an existing artifact follows Quiet Signal.

Inspect the actual artifact when access permits. Report:

- conforming decisions;
- violations, each tied to a specific `SPEC.md` section or Token;
- uncertain items that cannot be judged from available evidence;
- the smallest useful corrections.

Do not edit an audited artifact unless the user also asks for changes.

## Preserve the boundary

- Preserve supplied content, facts, functions, and required structure unless the user explicitly asks to change them.
- Do not write content strategy, split a narrative, choose a platform, or define product behavior on the user's behalf.
- Do not introduce Pattern, Composition, Recipe, Adapter, Compiler, Renderer, Runtime, Schema, pipeline state, or staged artifact requirements.
- Do not copy a source product's screens, feature layouts, or product motifs. Existing work can be evidence, but it is not a template.
- Do not force different formats into one shared layout. Consistent style and repeated composition are not the same thing.
- Do not expand the core specification to repair an incomplete brief or a missing platform Kit.

## Deliver clearly

Deliver the artifact or audit requested by the user, plus only the notes needed to explain material Quiet Signal decisions and unresolved boundaries. Do not expose internal taxonomies or create maintenance artifacts the user did not request.

When a new visual rule is genuinely needed, keep it as a candidate and request visual approval before treating it as part of Quiet Signal.
