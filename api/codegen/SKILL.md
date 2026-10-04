---
name: codegen
description: Regenerate OpenAPI spec then frontend API client for Skoleoverblikket. USE when user says 'codegen', 'swagger gen', 'regenerate api', 'run codegen', 'generate api client', 'regenerate spec', 'regenerate openapi', or after controller/model/endpoint changes.
---

Run in order — openapi-ts depends on the spec being current:

1. `dotnet build api/Skoleoverblikket.Api/Skoleoverblikket.Api.csproj` — regenerates `openapi/Skoleoverblikket.Api.json` via `OpenApiGenerateDocumentsOnBuild`
2. `cd web && npm run api:generate` — generates typed client from the spec

Report success or paste errors verbatim.

## Never read or grep the generated files

`web/src/api/generated/*` barrel imports are single lines of 12,000–15,000
characters (every endpoint in the API on one line). One `grep` match dumps
~7k tokens into context; `Read` on the whole file is far worse.

Do not verify codegen output by reading it. The `npm run api:generate` exit
code and `npx tsc --noEmit` already prove the client is valid.

If you must confirm a specific symbol landed, truncate every line:

```bash
grep -n "MySymbol" web/src/api/generated/sdk.gen.ts | cut -c1-120 | head -5
```

Same signal, ~600 chars instead of ~27,000.
