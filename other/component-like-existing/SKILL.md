---
name: component-like-existing
description: Bootstrap a new component from an existing one, preserving its provided interfaces and receptacles under a different component name.
argument-hint: "[existing-component-name, new-component-name]"
---

Bootstrapping a new component named $1 from the existing component named $0 involves the
following steps. The intent is to clone the *contract* of $0 — the interfaces it provides
and the receptacles it consumes — while giving it a new component name and its own crate.
Provided interfaces and receptacles are **preserved as-is**: they reference the existing
shared interface definitions in `components/interfaces`. Do **not** create new `I...`
interface files for the clone.

Only the *contract and scaffolding* are carried over — the component declaration, its
`provides:`/`receptacles:`, and the interface `impl` blocks. The method bodies are left
**empty** (`todo!()` stubs); the source's private implementation (helper modules, data
structures, behavioral tests) is **not** copied. The clone also starts a **fresh** spec-kit
session that inherits only the source's constitution.

1. The source component is $0 and the new component is $1. Locate the source component's
   sub-directory under `components/` (the lower-case, hyphen-ized form of $0, or the
   directory whose `define_component!` block declares $0). If it does not exist, return an
   error and stop.

2. If $1 was not supplied, interactively ask the user for the new component name and stop
   until provided. If a directory for $1 (lower-case, hyphen-ized) already exists under
   `components/`, return an error and stop.

3. Read the source component's `define_component!` block and record its `provides:`
   interface list and its `receptacles:` block verbatim. These are preserved unchanged in
   the clone.

4. Create a new sub-directory under `components/` whose name is the lower-case,
   hyphen-ized form of $1.

5. Copy the source component's implementation into the new directory — `src/` and
   `Cargo.toml`. Do **not** copy generated or spec directories: `target/`, `specs/`,
   `.specify/`, `info/`, or the source's `.claude/` directory.

6. Reduce the copied source to a compiling skeleton and rename it:
   - Rename the component type from the $0 name to the $1 name throughout (e.g.
     `FooBarComponent` → `BazComponent`), and update crate-name references, `//!` module
     docs, and doc-comment examples to match.
   - Keep the `define_component!` (and any `define_interface!`) declarations with their
     `provides:` and `receptacles:` entries exactly as recorded in step 3 — the clone
     provides the same interfaces and consumes the same receptacles as $0.
   - Replace the body of **every** method that implements a provided interface with a
     `todo!("$1: <method>")` stub, so the clone compiles but carries none of the source's
     logic.
   - Delete private helper modules, types, and fields that existed only to support the
     source's implementation, keeping `fields:` minimal but sufficient to construct the
     component. Remove any now-unused `use` imports.
   - Replace the source's behavioral tests with a minimal smoke test that constructs the
     component and queries each provided interface via `query_interface!`.

7. In the new `Cargo.toml`, set `[package] name` to the lower-case, hyphen-ized form of $1.
   Preserve all `[dependencies]` from the source (they reflect the interfaces and
   receptacles being kept).

8. Register the new crate in the workspace root `Cargo.toml`:
   - Add the new component path to `members`.
   - If the source component is listed in `default-members`, add the new one there too.
   - Add a `[workspace.dependencies]` entry: `<crate-name> = { path = "components/<dir>" }`,
     mirroring any options (e.g. `default-features = false`) used by the source's entry.

9. Add a permissions file `.claude/settings.json` in the new sub-directory that allows
   access to the component itself, `lib/component-framework`, `components/interfaces`,
   and the directories of any components corresponding to its receptacles. Avoid granting
   access to components that are not directly used. Model it on the source component's
   `.claude/settings.json` if present.

10. Copy into the new component directory's `.claude/skills` only the skills whose names
    match an `include` pattern in `.claude/component-local-skills.json` (patterns support a
    trailing `*` wildcard; other entries match exactly). This allowlist is the single source
    of truth for which skills are component-local — do not hard-code the list here. Skip any
    skill that does not match.

11. Run `specify init . --ai claude` in the new component source directory. This is a
    **fresh** spec-kit session — do not copy the source's specs, plans, tasks, or
    `.specify/sync` artifacts.

12. Copy **only** the source component's constitution into the new component, overwriting
    the freshly-initialized default: copy `.specify/memory/constitution.md` from the source
    to the same path under the new component. Leave all other spec-kit state fresh.

13. Run `specify extension add spec-kit-sync --from https://github.com/bgervin/spec-kit-sync/archive/refs/heads/master.zip`
    in the new component directory.

14. Verify the clone builds with `cargo build -p <new-crate-name>`. Report any errors.
