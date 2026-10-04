---
name: godot-csharp
description: Use when a Godot/.NET task involves writing, refactoring, or translating C# gameplay, tool, editor, resource, or node code and the agent must stay idiomatic to Godot's C# API, avoid GDScript-only assumptions, choose the right engine-facing patterns, and return implementation guidance plus validation notes.
---

# Godot C#

Use this skill when a Godot 4.6 + .NET/C# task requires **writing or refactoring C# that actually fits Godot's engine model**.

This skill is for implementation-minded work. Its job is not to restate generic C# best practices or blindly transliterate GDScript one line at a time. Its job is to choose the right Godot-facing C# patterns — partial classes, lifecycle hooks, typed node access, signals, exports, collections, Variant boundaries, diagnostics, and validation steps — so the resulting code is idiomatic, buildable, and editor-aware.

Prefer this skill when the main risk is writing technically valid C# that still clashes with Godot conventions, engine expectations, or the C# binding surface.

## Purpose

This skill is used to:

- map the task onto the correct Godot object and engine context
- choose idiomatic Godot C# APIs instead of GDScript-first patterns
- recommend the correct patterns for signals, exports, collections, Variant, and lifecycle hooks
- flag diagnostics, rebuild, and editor-visibility pitfalls before they turn into churn
- return a structured implementation brief that another agent can use to edit code confidently

## Use this skill when

Invoke this skill for tasks such as:

- implementing a new `Node`, `Resource`, `RefCounted`, autoload, or tool/editor script in C#
- translating GDScript examples or concepts into C#
- refactoring Godot C# code to be more idiomatic, type-safe, or editor-friendly
- deciding between Godot collections and .NET collections
- wiring signals, exported properties, tool buttons, or signal-awaiting flows in C#
- checking whether Godot C# code is relying on the wrong API naming or engine assumptions

### Trigger examples

- "Help me write this Node script in Godot C#"
- "Translate this GDScript snippet into C#"
- "How should this signal or export look in C#?"
- "Should Godot C# use Array or List here?"
- "Does this C# code follow Godot conventions?"

## Do not use this skill when

Do not use this skill when:

- the main need is runtime failure diagnosis rather than implementation guidance
- the user wants scene or system architecture review more than code-level C# guidance
- the main ask is upgrade sequencing rather than code design
- the task is plain .NET code with no meaningful Godot API or engine boundary
- the user only wants generic C# language tutoring unrelated to Godot

## Pattern

- Primary pattern: **Tool Wrapper**
- Secondary pattern: **Generator**

Why this fit is better than the alternatives:

- the skill packages reusable Godot C# conventions grounded in the official docs
- it still needs to produce a repeatable, structured implementation brief instead of loose advice
- a full Pipeline would add ceremony without enough value, because the ordered checks can live directly in this file

## Inputs

Collect or infer these inputs when available:

- task summary and intended behavior
- target script role: `Node`, `Resource`, `RefCounted`, tool/editor code, autoload, or mixed engine surface
- relevant scene, node, resource, signal, or inspector context
- whether the task is new implementation, translation, or refactor
- snippets or API calls already in play
- current Godot version, .NET target, and export/platform constraints if relevant
- whether editor or inspector exposure is required through `[Export]`, tool scripts, groups, or buttons

If inputs are incomplete, do not block on perfect detail. Infer the smallest safe defaults and call out the assumptions that would change the code shape.

## Workflow

Follow this sequence every time.

### 1. Classify the engine-facing context

Decide what kind of Godot-owned object or surface the task lives in.

At minimum, identify:

- whether the code is a `Node`, `Resource`, `RefCounted`, editor/tool script, or helper used by one of those
- which lifecycle hooks matter: `_Ready`, `_Process`, `_PhysicsProcess`, `_EnterTree`, `_ExitTree`, disposal, or none
- whether scene tree presence, signals, exports, or inspector integration are core to the change

Do not jump straight into syntax. First identify what the engine expects this code to be.

### 2. Map the task onto Godot's C# binding surface

Translate the task into idiomatic Godot C# APIs.

Rules:

- prefer `PascalCase` Godot APIs in C#
- prefer typed accessors like `GetNode<T>()` and `GetNodeOrNull<T>()`
- translate GDScript/global helpers to `GD`, `Mathf`, static singletons, or C# equivalents instead of keeping GDScript spellings
- use properties where the C# API exposes properties instead of getter/setter methods
- call out when string-based APIs such as `Call`, `CallDeferred`, or `Connect` still have naming caveats

If the task starts from GDScript, explicitly note the important API translations rather than assuming them implicitly.

### 3. Choose the right Godot C# patterns

For the touched code, decide the correct patterns in these areas:

- **class shape** — use `public partial class ...` for Godot-owned types
- **naming** — class name matches the `.cs` filename; public members use `PascalCase`; private fields use `_camelCase`
- **signals** — prefer generated C# events with `+=` / `-=`; use `[Signal]` delegates ending in `EventHandler`; use `EmitSignal`; only reach for `Connect()` when flags or cross-language signals justify it
- **exports** — use `[Export]`, relevant `PropertyHint`, grouping attributes, and only Variant-compatible types; keep default values analyzer-friendly
- **lifecycle** — replace `@onready` assumptions with initialization in `_Ready` or another correct hook
- **collections / Variant** — prefer .NET collections when data stays in managed code; use `Godot.Collections` or supported arrays when the engine, exports, or Variants require them; minimize untyped `Variant` use
- **async / await** — use `await ToSignal(...)` for signal waits when appropriate

Keep the selected patterns tied to the real task instead of dumping the whole handbook.

### 4. Surface the high-signal pitfalls before coding

Call out only the pitfalls that materially affect the change.

Common examples:

- new exports, signals, and tool-script changes require a rebuild before the editor reflects them
- struct-valued properties need copy-modify-reassign instead of in-place mutation
- `Call`, `CallDeferred`, `Connect`, and similar string-based engine APIs may still expect snake_case names; prefer `PropertyName`, `MethodName`, and `SignalName` where possible
- exported members, signal delegates, and generic usage must satisfy Godot diagnostics
- tool/editor code that changes exported or inspector-visible state may need `NotifyPropertyListChanged()`

Do not overwhelm the result with unrelated warnings.

### 5. Produce the implementation brief

Return the result using `assets/implementation-brief.md`.

The brief should:

- state the engine context clearly
- identify the chosen C# patterns
- explain any important API mapping from GDScript or generic .NET habits
- give a short implementation sequence another agent can execute
- include only the relevant pitfalls and validation steps

When the user also wants code, keep the code choices aligned with the brief instead of contradicting it.

### 6. Define validation and rebuild steps

After the implementation guidance, define the smallest meaningful verification path.

At minimum, consider:

- whether project assemblies should be rebuilt
- whether the inspector, exports, signals, or tool buttons need editor verification
- which runtime path should be smoke-tested
- one nearby regression guard if the change touches shared engine-facing behavior

If the task affects editor-visible behavior, do not omit the rebuild and visibility checks.

## Output contract

Return the result using `assets/implementation-brief.md` in this section order:

- `Task summary`
- `Engine-facing context`
- `Recommended C# patterns`
- `API mapping notes`
- `Implementation plan`
- `Pitfalls to avoid`
- `Validation and rebuild`
- `Assumptions`

Output rules:

- prefer concrete Godot C# decisions over generic clean-code filler
- explicitly call out when the advice differs from common GDScript patterns
- separate engine constraints from stylistic preferences
- keep `Pitfalls to avoid` short and task-specific
- include rebuild/editor visibility notes whenever exports, signals, tool scripts, or analyzer-sensitive code is involved

## Implementation heuristics

- Prefer idiomatic C# bindings over transliterating GDScript syntax.
- Prefer type-safe events and generic node accessors over stringly-typed calls when possible.
- Prefer .NET collections for internal data and Godot collections only at engine boundaries.
- Prefer clear lifecycle ownership over faux-`@onready` patterns.
- Prefer official Godot diagnostics constraints over clever C# tricks that the binding layer rejects.
- Prefer explicit validation steps when editor-visible behavior is part of the change.

## Companion files

- `references/godot-csharp-notes.md` — distilled official guidance for API mapping, exports, signals, collections, Variant, diagnostics, performance, and editor/build gotchas
- `assets/implementation-brief.md` — reusable template for the final Godot C# implementation guidance

## Validation

A good result should satisfy all of the following:

- the engine-facing context is identified correctly
- the recommended patterns match Godot C# rather than GDScript habits
- exports, signals, collections, and Variant advice are type-safe and engine-aware
- pitfalls mention only relevant high-signal issues
- validation includes rebuild/editor visibility steps when needed
- another agent could implement or review the code without guessing missing Godot-specific constraints

## Common pitfalls

- translating snake_case GDScript calls directly into C#
- forgetting `partial` or class/file-name matching
- using `Godot.Collections` everywhere instead of only at engine boundaries
- exporting unsupported or analyzer-hostile members
- assuming captured-lambda signal handlers always disconnect safely
- mutating struct-returning properties without reassigning them
- skipping rebuild after adding exports or custom signals

## Completion rule

This skill is complete when the agent has:

- identified the engine-facing context
- chosen idiomatic Godot C# patterns
- flagged the main binding, editor, and diagnostic pitfalls
- produced a concrete implementation brief
- defined the validation and rebuild steps for the touched behavior