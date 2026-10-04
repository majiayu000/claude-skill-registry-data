---
name: rest-api-generator
description: 'ATC REST API source generator and CLI for producing server endpoints, C# clients, and TypeScript clients from OpenAPI specifications. Use when the user asks to generate a REST API from an OpenAPI spec, scaffold server handlers, create typed HTTP clients, generate TypeScript clients with React Query hooks, configure API security or rate limiting, set up caching or resilience, version an API, generate webhooks, merge multi-part OpenAPI specs, or migrate from the old atc-rest-api-generator CLI.'
---

# ATC REST API Source Generator

A **Roslyn Source Generator** and CLI tool that automatically generates production-ready REST API server and client code from OpenAPI specifications. Zero CLI commands for server generation — install the NuGet package, add your YAML spec, create marker files, and build.

> **Key differentiator:** Compile-time code generation with type-safe results, contract-enforced handlers, and full OpenAPI 3.x support including security, rate limiting, caching, resilience, and versioning — all configured via OpenAPI extensions.

Detailed reference material lives in the `references/` folder — load on demand.

---

## References

| Reference | When to load |
|---|---|
| [Marker Files](references/marker-files.md) | Configuring `.atc-rest-api-server`, `.atc-rest-api-server-handlers`, `.atc-rest-api-client` |
| [CLI Reference](references/cli-reference.md) | CLI commands, TypeScript generation, migration, options management |
| [Server Generation](references/server-generation.md) | OpenAPI patterns, server endpoints, handlers, type-safe results |
| [Client Generation](references/client-generation.md) | C# TypedClient, EndpointPerOperation, TypeScript with fetch/Axios/React Query/Zod |
| [Security](references/security.md) | JWT, OAuth2, API Key, OpenID Connect, role-based authorization |
| [Rate Limiting & Caching](references/rate-limiting-caching.md) | Rate limiting algorithms, Output Caching, HybridCache, cache invalidation |
| [Resilience & Versioning](references/resilience-versioning.md) | Retry, circuit breaker, timeout, API versioning strategies |
| [Validation & Analyzer Rules](references/validation-rules.md) | DataAnnotations, FluentValidation, analyzer rule reference |

---

## 1. Quick Start — Source Generator (Server)

### Step 1: Install the NuGet package

```xml
<PackageReference Include="Atc.Rest.Api.SourceGenerator" Version="*" />
```

### Step 2: Add the OpenAPI spec

Place the YAML/JSON file (e.g. `PetStore.yaml`) in the project root or a subfolder.

### Step 3: Create marker files

Create one or more JSON marker files in the project root to control generation:

**`.atc-rest-api-server`** — Server contracts (models, endpoints, type-safe results):
```json
{
  "generate": true,
  "validateSpecificationStrategy": "Strict",
  "useServersBasePath": true,
  "useMinimalApiPackage": "Auto",
  "useValidationFilter": "Auto",
  "useGlobalErrorHandler": "Auto"
}
```

**`.atc-rest-api-server-handlers`** — Handler scaffolds:
```json
{
  "generate": true,
  "validateSpecificationStrategy": "Strict",
  "stubImplementation": "throw-not-implemented"
}
```

**`.atc-rest-api-client`** — C# client contracts:
```json
{
  "generate": true,
  "validateSpecificationStrategy": "Strict",
  "generationMode": "TypedClient",
  "generateOAuthTokenManagement": true
}
```

### Step 4: Build

```bash
dotnet build
```

Generated code appears in `obj/` as source-generated files. No manual steps needed.

### Step 5: Wire up in Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddAtcRestApi();       // Register generated endpoints
builder.Services.AddAtcHandlers();      // Register handler implementations
var app = builder.Build();
app.UseAtcRestApi();                    // Map endpoints
app.Run();
```

See [Marker Files](references/marker-files.md) for all configuration options.

---

## 2. Quick Start — CLI Tool

Install globally:
```bash
dotnet tool install -g atc-rest-api-gen
```

### Scaffold a server project

```bash
atc-rest-api-gen generate server \
  --specificationPath PetStore.yaml \
  --outputPath ./src \
  --projectName MyApi
```

Project structure options: `SingleProject`, `TwoProjects`, `ThreeProjects` (default).

### Generate a C# client

```bash
atc-rest-api-gen generate client \
  --specificationPath PetStore.yaml \
  --outputPath ./src/MyApi.Client \
  --projectName MyApi.Client \
  --generationMode TypedClient
```

Generation modes: `TypedClient` (single client class) or `EndpointPerOperation` (one interface per endpoint, uses `Atc.Rest.Client`).

### Generate a TypeScript client

```bash
atc-rest-api-gen generate client-typescript \
  --specificationPath PetStore.yaml \
  --outputPath ./src/ts-client \
  --client-type fetch \
  --hooks react-query \
  --zod \
  --scaffold
```

Client types: `fetch` (default), `axios`. Hooks: `none`, `react-query`. Add `--zod` for Zod schema validation.

See [CLI Reference](references/cli-reference.md) for all commands and options.

---

## 3. Core Concepts

### Type-Safe Results

Every generated endpoint returns a discriminated union result type that enforces handling all possible HTTP responses at compile time:

```csharp
public class GetPetResult : ResultBase
{
    public static GetPetResult Ok(Pet pet) => new(200, pet);
    public static GetPetResult NotFound(string? message = null) => new(404, message);
}
```

Handlers must return the correct result type — no `IActionResult` escape hatch.

### Three-Layer Architecture

1. **Atc.Rest.Api.Generator** (netstandard2.0) — Shared extractors, services, configuration
2. **Atc.Rest.Api.SourceGenerator** (netstandard2.0) — Roslyn `IIncrementalGenerator` implementations
3. **Atc.Rest.Api.Generator.Cli** (net10.0) — CLI tool for scaffolding and validation

### Marker File System

Marker files are JSON configuration files that control what gets generated:

| Marker File | Purpose |
|---|---|
| `.atc-rest-api-server` | Server contracts: models, endpoints, results |
| `.atc-rest-api-server-handlers` | Handler scaffolds with stub implementations |
| `.atc-rest-api-client` | C# client contracts |

### OpenAPI Extensions

The generator uses custom `x-` extensions to configure features beyond standard OpenAPI:

| Extension Prefix | Feature |
|---|---|
| `x-authorize-roles` | Role-based authorization |
| `x-ratelimit-*` | Rate limiting configuration |
| `x-cache-*` | Caching (Output Cache or HybridCache) |
| `x-retry-*` | Resilience (retry, circuit breaker, timeout) |
| `x-return-async-enumerable` | IAsyncEnumerable streaming |

---

## 4. Security Configuration

Supports standard OpenAPI security schemes plus ATC extensions:

| Scheme | OpenAPI Type | Extension |
|---|---|---|
| JWT Bearer | `http` / `bearer` | — |
| OAuth2 | `oauth2` | — |
| API Key | `apiKey` | — |
| OpenID Connect | `openIdConnect` | — |
| Role-based | Any | `x-authorize-roles: "Admin,User"` |

Quick example — JWT with role-based auth:
```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

paths:
  /admin/settings:
    get:
      security:
        - BearerAuth: []
      x-authorize-roles: "Admin"
```

See [Security](references/security.md) for OAuth2 scopes, token management, and error handling.

---

## 5. Rate Limiting, Caching & Resilience

All configured via OpenAPI extensions at document, path, or operation level.

**Rate Limiting** — algorithms: `fixed`, `sliding`, `token-bucket`, `concurrency`:
```yaml
x-ratelimit-policy: "standard"
x-ratelimit-permit-limit: 100
x-ratelimit-window-seconds: 60
x-ratelimit-algorithm: sliding
```

**Caching** — Output Caching or HybridCache:
```yaml
x-cache-type: output          # or "hybrid"
x-cache-expiration-seconds: 300
x-cache-tags: ["pets"]
x-cache-vary-by-query: ["status"]
```

**Resilience** — retry, circuit breaker, timeout (Polly v8):
```yaml
x-retry-max-attempts: 3
x-retry-backoff: exponential
x-retry-use-jitter: true
x-retry-timeout-seconds: 30
x-retry-circuit-breaker: true
```

See [Rate Limiting & Caching](references/rate-limiting-caching.md) and [Resilience & Versioning](references/resilience-versioning.md).

---

## 6. API Versioning

Three strategies configured in the server marker file:

| Strategy | URL Example | Marker Setting |
|---|---|---|
| QueryString | `/pets?api-version=1.0` | `"versioningStrategy": "QueryString"` |
| UrlSegment | `/v1/pets` | `"versioningStrategy": "UrlSegment"` |
| Header | `X-Api-Version: 1.0` | `"versioningStrategy": "Header"` |

Requires `Asp.Versioning.Http` package. See [Resilience & Versioning](references/resilience-versioning.md).

---

## 7. Webhooks & Multi-Part Specs

**Webhooks** — enable in the server marker file:
```json
{
  "generateWebhooks": true,
  "webhookBasePath": "/webhooks"
}
```

**Multi-Part Specs** — merge multiple OpenAPI files:
```json
{
  "multiPartConfiguration": {
    "enabled": true,
    "files": ["pets.yaml", "orders.yaml", "users.yaml"]
  }
}
```

---

## 8. Migration from Old CLI

Migrate from the deprecated `atc-rest-api-generator`:

```bash
# Validate first
atc-rest-api-gen migrate validate --projectPath ./src

# Dry run
atc-rest-api-gen migrate execute --projectPath ./src --dry-run

# Execute migration
atc-rest-api-gen migrate execute --projectPath ./src
```

Changes: project renames, namespace updates, parameter name migration, file restructuring. See [CLI Reference](references/cli-reference.md) for details.

---

## 9. Validation & Spec Checking

```bash
atc-rest-api-gen validate schema --specificationPath PetStore.yaml
```

Three validation levels: `None`, `Standard`, `Strict`. The generator includes 60+ analyzer rules (ATC_API_* prefix) covering naming, security, schema, and operation validation. See [Validation & Analyzer Rules](references/validation-rules.md).

---

## 10. Recommended Packages

| Package | Purpose |
|---|---|
| `Atc.Rest.Api.SourceGenerator` | Core source generator (required) |
| `Atc.Rest.MinimalApi` | Validation filters, global error handler |
| `Atc.Rest.Client` | For EndpointPerOperation client mode |
| `Asp.Versioning.Http` | API versioning support |
