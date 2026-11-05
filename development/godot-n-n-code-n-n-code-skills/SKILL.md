---
name: godot
description: Godot 4 game and tool development, explanation, review, and debugging across 2D/3D, scenes, resources, GDScript, C#, and C++ GDExtension with godot-cpp. Use for native integration, gameplay/UI, profiling, testing, and exports in Godot. Not for other engines, generic C++ work, or full engine-fork development; recognize Godot 3/GDNative separately rather than silently porting it.
---

# Godot

Apply this domain overlay to Godot-specific decisions. Give native integration
particular depth without making C++ the default language for every task. Preserve
the project's language, renderer, build system, and supported versions unless the
requested change needs a deliberate adjustment.

## Select the activity

- **Explain:** answer the concept directly, with a small example when useful.
  A conceptual question needs no repository, executable, or installation.
- **Design:** propose the relevant scenes, responsibilities, interactions, and
  validation. Resolve consequential choices; a design request alone makes no edits.
- **Review or diagnose:** inspect sources and supplied evidence, report concrete
  findings and uncertainty. Keep source-only reviews free of project execution.
- **Implement or fix:** trace the affected behavior, make scoped source changes,
  and verify the relevant layers within the request's authorization.

Infer the activity from the request. Reuse existing authorization; ask only for
missing information that materially affects the result. For a new project, honor
the user's language and platform choices; clarify a consequential unresolved
language choice rather than silently choosing C++ or GDScript.

## Ground project-dependent work

1. Read applicable instructions and working-tree changes. Locate `project.godot`,
   relevant scenes/scripts/resources, autoloads, addons, and existing test/build
   entrypoints. Inspect only the subsystem needed for the task.
2. Establish the intended Godot version from project/CI documentation and reconcile
   it with the executable when running tools. Project format/features are clues,
   not an exact patch-version lock. Record the renderer and target platforms when
   they affect the work. Recognize Godot 3/GDNative before using Godot 4 guidance.
3. For C++, independently identify the godot-cpp revision, target Godot API, native
   build configuration, and `.gdextension` mapping. Read the C++ reference before
   changing native code, registration, build configuration, or loading behavior.
4. Trace the source-to-behavior path: script/native class, scene instantiation,
   resources, input/signals, and any export boundary touched. Fix the demonstrated
   cause; do not introduce event buses, pools, autoloads, or migrations by default.
5. Choose checks that can demonstrate the requested behavior. Distinguish what
   source inspection predicts from what actually compiled, loaded, ran, or rendered.

Use version-matched official documentation and the pinned dependency's own
documentation/source for material API or toolchain decisions. `stable` is a moving
alias; `latest` can describe unreleased features. Do not upgrade a project to make
an example fit. When sources disagree, identify their versions and verify the
specific API/build option rather than combining incompatible instructions.

## Read selectively

| Task needs | Reference |
|---|---|
| Scene structure, lifecycle, resources, imports, UIDs, or source edits | [Projects, scenes, and resources](references/projects-scenes-resources.md) |
| C++ GDExtension, binding compatibility, ownership, registration, builds, or native loading | [GDExtension and C++](references/gdextension-cpp.md) |
| GDScript, C#, or script/native interoperability | [Scripting integration](references/scripting-integration.md) |
| Gameplay, physics/input, UI, animation/audio, rendering, or performance choices | [Gameplay and presentation](references/gameplay-presentation.md) |
| Executing checks, interpreting failures, debugging, or producing exports | [Debugging, testing, and export](references/debugging-testing-export.md) |
| Maintaining technical claims or locating authoritative documentation | [Sources](references/sources.md) |
| Maintaining this skill's routing and behavioral checks | [Evaluation procedure and expectations](references/trigger-evals.md); [raw fixtures](references/behavior-fixtures.md) |

Do not load every reference for an ordinary task. Maintenance cases and grading
criteria are not game-development instructions.

## Execution and composition

Opening/importing a project can run editor plugins, tool scripts, and native
extensions and write metadata. Native builds and tests execute project tooling.
Read the validation reference before those actions; keep them within the request's
scope. Source-only review is not authorization to import, launch, build, or install.
When execution is authorized, continue necessary checks without repeated approval
requests. Missing tools justify an explicit validation gap, not invented success.

Use existing capabilities; no particular MCP server, editor automation tool, test
addon, or IDE is assumed. Adding dependencies, changing engine versions, generating
assets, and publishing builds are separate choices, not automatic consequences of
using this skill.

For C++ implementation/review, compose with `coding-guidance-cpp` when available.
Godot's allocation, `RefCounted`, node ownership, and threading contracts govern
engine objects; generic ownership advice does not override them. Ordinary C++
types still benefit from portable C++ guidance. This skill retains the essential
engine-specific rules and works without that companion.

Full engine-fork/module development needs a separately scoped workflow. Explain
the GDExtension/module tradeoff when relevant; do not rebuild the engine merely
because a native integration is unfamiliar.

## Finish with evidence

Report the answer or source changes, relevant versions, checks actually performed,
and remaining uncertainty. Separate compilation, import/parsing, project tests,
runtime, visual checks, and exported-artifact checks. A successful native build
does not prove extension loading; a headless launch does not prove visual or
interactive correctness. Do not claim untested platforms or cross-host skill
installation compatibility.
