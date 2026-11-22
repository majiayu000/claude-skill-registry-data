---
name: dashboard
description: "Maps Puck.Dashboard (TypeScript, Vite, React): World Studio, the in-browser engine (Puck.World.Browser), its language server, official builds, drafts, the portal's storage, DuckDB and audit pages."
---

# Dashboard

A map of `src/Puck.Dashboard`, the npm workspace behind the website: World
Studio (edit, check and preview a world's `.puck` sources with the real engine
in the browser) and the signed-in portal pages (Cloud Storage with DuckDB
queries, the audit trail, the documentation page). Two applications ship
together, joined by module federation:

- **The host** (`src/Puck.Dashboard/src/host`): sign-in, the service context,
  the federation host that loads the portal.
- **The portal** (`src/Puck.Dashboard/src/portal`): World Studio and the
  portal pages. `shared/` holds contracts both import; `build/` holds the Vite
  pieces both configurations share.

[Puck.Dashboard](../../../src/Puck.Dashboard/README.md) is the developer
reference: the run commands, the federation, streams and state-machine rules,
the studio machine, the official content model and the limitations. This file
names where each capability lives and the contracts that bite. When it and the
code disagree, the code wins and this file is corrected in the same change.

## Find the owner by what you need

| You need | Owner | Read |
|---|---|---|
| Change what the studio can do or refuse | `src/Puck.Dashboard/src/portal/src/machines/studioMachine.ts`, the one state machine, bound through `src/Puck.Dashboard/src/portal/src/context/StudioContext.tsx`'s hooks | [the studio machine](../../../src/Puck.Dashboard/README.md#the-studio-machine) |
| Ask the engine something (compile, compose, judge, evaluate, cells, the language server) | a `[JSExport]` in `Puck.World.Browser`, decoded once in `src/Puck.Dashboard/src/portal/src/native/engineTypes.ts` | [the export surface](../../../src/Puck.World.Browser/README.md#jsexport-api-surface-as-actually-exported) |
| Boot the engine from verified bytes, once compiled per session | `src/Puck.Dashboard/src/portal/src/native/engineBoot.ts`, `workerBoot.ts` | [the official content model](../../../src/Puck.Dashboard/README.md#the-official-content-model) |
| Load an official build, verify every object, cache it | `src/Puck.Dashboard/src/portal/src/official/officialClient.ts` (`loadOfficial`), `byteStore.ts` (`readThroughVerified`) | [the official content model](../../../src/Puck.Dashboard/README.md#the-official-content-model) |
| Highlighting, completion, hover, outline, formatting, diagnostics for `.puck` | the engine's language server over `lsp`/`lspIdle` (`languagePump.ts`, `lspTransport.ts`), semantic tokens in `components/world/authoring/semanticTokens.ts` | [studio views](../../../src/Puck.Dashboard/README.md#studio-views) |
| Preview, step, jump through snapshots, edit a running row, the console | the studio machine's `PREVIEW_*` events over the world engine (`Compile`, `Judge`, `WriteRow`, `Evaluate`) | [studio views](../../../src/Puck.Dashboard/README.md#studio-views) |
| Topology views and cell geometry | the engine's `Cells` answer, drawn by `UniversalTopologyView` or `SpatialTopology3D` | [studio views](../../../src/Puck.Dashboard/README.md#studio-views) |
| Local drafts | `src/Puck.Dashboard/src/portal/src/document/localDrafts.ts` | [the studio machine](../../../src/Puck.Dashboard/README.md#the-studio-machine) |
| Types for a world document | `src/Puck.Dashboard/src/portal/src/document/worldDefinition.generated.ts`, written by `puck schema` | [run and check](../../../src/Puck.Dashboard/README.md#run-and-check) |
| SQL over the user's storage | `src/Puck.Dashboard/src/portal/src/components/data/duckDb.ts`, per-account secrets in `storageSecrets.ts`, pinned extensions in `src/Puck.Dashboard/src/build/duckdbExtensions.ts` | [querying storage](../../../src/Puck.Dashboard/README.md#querying-storage-with-duckdb) |
| Events over time (supersede, coalesce, poll) | an RxJS stream in a plain module with its sources passed in | [streams](../../../src/Puck.Dashboard/README.md#streams) |
| What the host and portal share | `src/Puck.Dashboard/src/build/federationShare.ts`, the `PortalModule` contract in `src/Puck.Dashboard/src/shared/interfaces.tsx` | [federation](../../../src/Puck.Dashboard/README.md#federation) |
| The look | Mantine themed from `branding/tokens.css` (`portal/src/theme/palette.ts`, `theme.ts`), CSS modules per component | [theme and styling](../../../src/Puck.Dashboard/README.md#theme-and-styling) |
| Serve an official tree locally | `puck official build` and `puck official serve`, proxied at `/official` | [run and check](../../../src/Puck.Dashboard/README.md#run-and-check) |

## Contracts that bite

- **The engine is the only implementation.** The studio has no grammar,
  tokenizer, compiler or ordinal formula of its own: language features come
  from the language server, geometry from `Cells`, checks from the engine's
  compile and composition. A JavaScript reimplementation of the language or of
  engine semantics is a second implementation and a defect.
- **A missing engine capability is added at the engine.** A new question is a
  `[JSExport]` in `Puck.World.Browser` plus its decoder in `engineTypes.ts`; a
  call an older engine lacks throws `EngineCapabilityMissing` by name.
- **Every byte is verified.** Each object is checked against the manifest's
  SHA-256 when fetched and again when read back; a mismatch refuses by name.
  The engine must report the manifest's world schema and generator commit
  before a source runs on it.
- **The generated types are never hand-edited.** After changing the world
  document model, run `puck schema`; `puck schema --check` fails when the file
  drifts, with no Node.js step.
- **A machine decides what may happen next.** A component asks
  `snapshot.can(...)` or a tag, never names a state; an event the machine
  would not take is refused by a guard, never only by a disabled control.
  Outside work runs in invoked actors, and `assign` stays pure.
- **Warnings fail the production build**, as in .NET, unless the
  application's Vite configuration names the warning with its reason.
- **Nothing moves under the pointer.** Content that loads late reserves its
  final space; check a UI change by recording `layout-shift` entries during
  real interactions.
- **Share links and storage URLs are untrusted input.** Only ByteTerrace
  storage accounts get a token, scoped per account; a starter query quotes a
  link as one SQL string.

## Where each contract is enforced

| Contract | Enforced by |
|---|---|
| The portal matches the host's federation contract | TypeScript, against `PortalModule` in `shared/interfaces.tsx` |
| Every shared runtime dependency is in the share | `src/Puck.Dashboard/src/portal/tests/federation.test.cjs`; `strictVersion` turns skew into a named load error |
| The generated world types match the schema | `puck schema --check` (CI's verify workflow) |
| Pinned DuckDB extensions match the engine version | `duckdbExtensions.test.cjs` and the build's hash refusal |
| Every CSS module class a component reads exists | `cssModules.test.cjs` |
| Brand tokens and fonts are wired | `puck branding --check` |

## Open gaps

- **The portal and host talk to Azure directly** (MSAL, Blob Storage), which
  the architecture gate cannot see in an npm project; the fix is a sign-in and
  a store seam the portal is handed
  ([provider independence](../../../docs/plans/open-items.md#provider-independence)).
- A composed-world finding caused by an imported file names the root at line
  0; a source declaring several worlds is checked as one; the limitations
  list in [the README](../../../src/Puck.Dashboard/README.md#limitations)
  holds the rest.

## Verify

From `src/Puck.Dashboard/src`, after `npm ci`:

- `npm --workspace portal run test` runs the regression suite under Node's
  test runner. The engine tests run the published engine and skip by name
  without a local AppBundle (`dotnet publish src/Puck.World.Browser -c Release`)
  or, for tests needing compiled worlds, without an official tree.
- `npm run build` type-checks and builds both applications with warnings as
  errors.
- `puck schema --check` from the repository root after a document-model change.
- Seeing the studio is the [run and check](../../../src/Puck.Dashboard/README.md#run-and-check)
  recipe: publish the CLI and the browser engine, `puck official build` and
  `serve`, then `npm --workspace portal run dev`.

## Look-alikes

- The CLI's `puck lsp` serves the same language server over stdio; the studio
  runs it in the browser engine through `Lsp` and `LspIdle`.
- `Puck.World.Browser` is the engine; the dashboard only hosts it. Engine
  behaviour, payload size and trimming belong to that project's README.
- The documentation website's content is `docs/`; the dashboard only embeds
  the overview at `/docs`.

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-dsl` | The `.puck` language, the language server's behaviour, PUCKnnn diagnostics, `puck schema`. |
| `puck-world` | World documents the studio previews, the browser engine as a World host. |
| `state` | Rules, judge traces, row values and expressions the preview reads and writes. |
| `tooling` | `puck official`, the candidate CLI the dashboard tests install, CI's application assembly. |
| `dotnet-performance` | The browser engine's AOT payload and trimming. |
| `verification` | The private CLI copy and what a passing check proves. |
