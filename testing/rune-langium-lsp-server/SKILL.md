---
description: "Embed a Rune DSL language server behind a WebSocket or custom connection\nadapter. Use when: Embedding a Rune DSL language server in a web application via WebSocket."
name: rune-langium-lsp-server
---

# @rune-langium/lsp-server

Embed a Rune DSL language server behind a WebSocket or custom connection
adapter.

Use `createRuneLspServer()` when you need diagnostics, hover, completion, and
go-to-definition for `.rosetta` files in an editor or web app. Reach for
`createConnectionAdapter()` when tests or nonstandard transports need to plug
into the same server lifecycle.

## When to Use

**Use this skill when:**
- Embedding a Rune DSL language server in a web application via WebSocket → use `createRuneLspServer`
- Running a standalone LSP server process bridging to a VS Code / Theia client → use `createRuneLspServer`
- Integration-testing LSP features (hover, completion, diagnostics) → use `createRuneLspServer`
- Wiring a custom `@lspeasy/server` instance into Langium in tests or advanced embedding scenarios where `createRuneLspServer()` does not fit. → use `createConnectionAdapter`

**Do NOT use when:**
- Parsing `.rosetta` files in a script — use `createRuneDslServices()` and `parse()` / `parseWorkspace()` instead (no LSP overhead). (`createRuneLspServer`)
- Creating multiple servers in the same process — each server maintains its own Langium workspace index; sharing a workspace across servers requires custom `ServiceRegistry` wiring. (`createRuneLspServer`)
- Normal usage — prefer `createRuneLspServer()` which calls this internally. (`createConnectionAdapter`)

API surface: 2 functions, 2 classes, 2 types, 2 constants

## Quick Reference

**LSP Server:** `createRuneLspServer` (Create a fully-wired Rune DSL LSP server backed by `@lspeasy/server`), `createConnectionAdapter` (Create a `vscode-languageserver`-compatible `Connection` backed by an
`@lspeasy/server` `LSPServer`), `RuneLspServer` (A fully-wired Rune DSL LSP server instance)
**cf-durable-object-transport:** `DurableObjectWebSocketTransport`
**document-update-handler:** `RuneDocumentUpdateHandler`
**lsp-model.d:** `LspModelUpdate` (Incremental semantic documents followed by the complete current URI set), `LSP_MODEL_SYNC_METHOD` (@rune-langium/lsp-server — LSP server for Rune DSL powered by Langium
and @lspeasy/server), `LSP_REQUEST_TIMEOUT_MS` (Request budget includes reconstruction of dependency models after cold wake)

## References

Load these on demand — do NOT read all at once:

- When calling any function → read `references/functions.md` for full signatures, parameters, and return types
- When using a class → read `references/classes.md` for properties, methods, and inheritance
- When defining typed variables or function parameters → read `references/types.md`
- When using exported constants → read `references/variables.md`

## Links

- Author: Pradeep Mouli <pmouli@mac.com> (https://github.com/pradeepmouli)