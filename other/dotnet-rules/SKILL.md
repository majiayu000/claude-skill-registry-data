---
name: dotnet-rules
description: Use when writing, reviewing, or modifying C# code in this repository. Loads the .NET engineering rules covering layered architecture, CQRS with Result pattern, strongly-typed IDs, IOptions configuration, and forbidden patterns. Skip for non-code tasks (planning, docs, status updates).
---

# .NET Engineering Rules - Loader

The canonical rules live at `dotnet-rules.md` next to this `SKILL.md`. Read that file in full before generating, modifying, or reviewing any C# in this repository.

## How to use

1. Read `dotnet-rules.md` (sibling of this SKILL.md) end-to-end.
2. Before writing code, mentally check Section 11 (Forbidden Patterns) - common traps:
   - `public List<T>` on entities (use `IReadOnlyList<T>`)
   - `static` services
   - `.Result` / `.Wait()` on Tasks
   - `async void`
   - Returning domain entities from the Application layer
   - `IEnumerable` from repositories (use `IReadOnlyList<T>`)
3. After writing code, run the Section 12 checklist.
4. If your change is non-trivial, the user can run `/dotnet:rule-check` to invoke the `dotnet-rules-checker` subagent for an automated audit of the diff.

## Project-specific overrides

Project-specific overrides of these rules (e.g., "no MediatR", custom Result shape, particular ID strategy) belong in the relevant feature's `docs/<feature>/<feature>.analyzed.md` and are summarized in that feature's `docs/<feature>/<feature>.status.md`. The dotnet-rules-checker reads both before flagging violations.

When a rule and a recorded override conflict, the **override wins** - but only inside this repo, and only for the specific case the override names.

## Reminders that survive the rules doc

- **Layered architecture, no upward references.** `Domain` <- `Application` <- `Infrastructure` <- `EntryPoint`.
- **One type per file**, file name matches the type. Group by feature/aggregate (e.g., `Domain/Invoices/`), not by kind (`Entities/`, `Enums/`).
- **`IOptions<T>` for all configuration access.** No magic strings for config keys.
- **Nullable reference types enabled** in every `.csproj`; same for `ImplicitUsings`.
