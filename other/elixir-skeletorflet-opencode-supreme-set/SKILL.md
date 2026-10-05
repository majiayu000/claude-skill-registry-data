---
name: elixir
description: Elixir language skill covering OTP, Phoenix, Ecto, pipe operator, pattern matching, and Mix. Use when building Elixir applications.
trigger: elixir, phoenix, ecto, otp, genserver, supervisor, elixir pipe, elixir pattern matching, mix, liveview
---

## elixir

### Core Concepts
- OTP: GenServer for stateful server processes, Supervisor for fault tolerance trees, Application for system startup
- Pattern Matching: = operator is match not assignment, pin operator (^) matches existing value, case/function clause destructuring
- Pipe Operator: |> chains function calls, first argument flows as next function's first parameter, improves readability
- Immutability: all data is immutable, rebinding name to new value, persistent data structures for efficiency

### Phoenix & Ecto
- Phoenix: HTTP + WebSocket framework, router (pipeline/browser/api scopes), controllers, LiveView for real-time UI
- LiveView: server-rendered reactive UI, stateful processes, OTA updates via WebSocket, no JS required
- Ecto: database wrapper and query generator, schemas map to DB tables, changesets for validation, Repo for queries
- Contexts: bounded module groups for domain logic, explicit public interfaces, prevent leaky dependencies

### Tooling
- Mix: project generator, dependency management, custom tasks, test runner with ExUnit
- IEx: interactive shell with recompilation, debugger, process inspection
- Hex: package registry, publishes libraries, dependency resolution

### Common Patterns
- Supervised process tree (Application -> Supervisor -> Children)
- Enum.map/Enum.filter with pipe for data transformation
- with/else for complex pipeline error handling
- Phoenix PubSub for real-time messaging across nodes
