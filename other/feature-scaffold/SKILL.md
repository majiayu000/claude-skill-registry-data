---
name: feature-scaffold
description: Workflow to add a use case (command, query, integration-event consumer) to an existing module exactly as the Architecture Profile prescribes — generate files with scripts/New-Slice.ps1 from templates (zero boilerplate output), then fill TODO(ai) markers, wire, test and verify. Use whenever adding an endpoint, feature, use case, handler or consumer to a module.
user-invocable: false
---
# Feature Scaffold

## 1. Resolve (read, don't ask, unless missing)
Module entry → `recipe`, `domain_logic`, `cqrs`; conventions → `endpoint_placement`, `data_access.read`.
The feature must fit the module `purpose`; otherwise stop → architect.
Use case name = business verb phrase (`IssueInvoice`, `ListOverdueInvoices`, `OnInvoiceIssued`).

## 2. Generate (never type boilerplate)
```powershell
pwsh scripts/New-Slice.ps1 -RootNamespace <system.root_namespace> -Module <M> -Feature <F> -UseCase <U> `
  -Kind command|query|consumer -Recipe <recipe> [-ReadAccess dapper|ef] [-EndpointPlacement slice|host] `
  [-Event <IntegrationEvent>] [-Route <route>] [-Policy <M.Action>] [-SrcRoot src/Modules]
```
The script prints created paths only and refuses to overwrite. Recipe → layout:
| Recipe | Output | Shape |
|---|---|---|
| clean-sliced | `<M>/<Root>.Modules.<M>.Application/Features/<F>/<U>/` | multi-file |
| sliced-domain | `<M>/<Root>.Modules.<M>/Features/<F>/<U>/` | multi-file |
| hexagonal-integration | `<M>/<Root>.Modules.<M>/Features/<U>/` | multi-file |
| pure-slices | `<M>/<Root>.Modules.<M>/Features/<F>/<U>.cs` | single file |

## 3. Fill
Replace only `TODO(ai)` markers with targeted edits. Domain-model modules: add/extend the aggregate method + error + domain event first (RULE placement), with its unit test.
Persistence per `sql-server-data-access`; read-side index if the query needs one.

## 4. Wire & verify
Endpoints/handlers are discovered by convention (`IEndpoint` scan, `*Handler` registration). Cross-module: only `exposes` of other modules.
Build → slice integration test (+ consumer idempotency test) → architecture tests. `grep -rn "TODO(ai)" <slice path>` must return nothing.

## Template adaptation (once per repository)
Templates assume SharedKernel types `Result`, `IEndpoint`, `ValidationFilter<T>`, `ToHttpResult()`, `ISqlConnectionFactory`, `IIntegrationEventHandler<T>`. If the repository names them differently, edit `assets/templates/**` once — never work around it per slice.
