---
name: greycat
description: "GreyCat full-stack development for graph-based language with built-in persistence and MCP server capability. CRITICAL WORKFLOW - After generating or modifying ANY GreyCat backend code (.gcl files), IMMEDIATELY run 'greycat-lang lint' to get linting feedback and fix all errors before proceeding. Use when: (1) working with .gcl files or GreyCat projects, (2) using persisted nodes and indexed collections (nodeList, nodeIndex, nodeTime, nodeGeo), (3) creating data models, services, or abstract types, (4) writing API endpoints with @expose, @permission, @tag, or @volatile decorators, (5) implementing parallel processing with Jobs, await(), or PeriodicTask, (6) integrating React frontends with @greycat/web SDK or TypeScript type generation, (7) running GreyCat CLI commands (greycat serve/test/run/install/lint), (8) debugging GreyCat applications or working with transactions, (9) exposing functions as MCP tools with @tag(\"mcp\"). NOT for: general graph databases (Neo4j, ArangoDB), generic React apps, or SQL databases."
---

# GreyCat Backend Development

Graph-based language with built-in persistence. Not a database—an evolving coded structure.

## Commands

```bash
greycat install      # download libs
greycat test         # run tests
greycat serve        # start :8080 (HTTP + MCP server)
greycat-lang lint    # check for errors
greycat-lang fmt     # format GCL files
```

## Claude Code LSP Integration

**Install the `greycat-lsp` plugin** for enhanced `.gcl` file editing with IDE features:

| Feature | Description |
|---------|-------------|
| Code Completion | Intelligent suggestions for types, functions, fields |
| Go to Definition | Jump to symbol definitions (LSP tool) |
| Find References | Find all usages of a symbol (LSP tool) |
| Hover | Type information and documentation |
| Diagnostics | Real-time error detection (on save) |
| Formatting | Auto-format `.gcl` files |

**Prerequisite:** `greycat-lang` binary must be in PATH (`greycat-lang --version` to verify).

**LSP tools available:** Use `goToDefinition`, `findReferences`, `hover`, `documentSymbol` on `.gcl` files.

## Development Workflow

**⚠️ CRITICAL: Always lint after code generation**

When generating or modifying GreyCat backend code (.gcl files):

1. **Generate/modify** the code
2. **Immediately run** `greycat-lang lint` to get linting feedback
3. **Fix any errors** reported by the linter before proceeding

This ensures code quality and catches errors early. **NEVER skip this step** when working with GreyCat backend code.

```bash
# Example workflow
# 1. Make changes to backend/src/model/city.gcl
# 2. Run linter immediately
greycat-lang lint
# 3. Fix any reported errors
# 4. Continue development
```

## Architecture

**Backend (GreyCat .gcl)**
- `project.gcl` - Entry point, libs, permissions, roles, main(), init()
- `backend/src/model/` - Data models + global indices
- `backend/src/service/` - XxxService abstract types (::create, ::find)
- `backend/src/api/` - @expose + @permission functions, @volatile response types
- `backend/src/edi/` - Import/export

**project.gcl example:**
```gcl
@library("std", "7.6.0-dev");
@library("explorer", "7.6.0-dev");  // enables graph navigation in explorer UI
@include("backend");  // includes all .gcl files in backend/ recursively

@permission("app.admin", "app admin permission");
@permission("app.user", "app user permission");

@role("admin", "app.admin", "app.user", "public", "admin", "api", "debug", "files");
@role("public", "public", "api", "files");
@role("user", "app.user", "public", "api", "files");

@format_indent(4);
@format_line_width(280);

fn main() { }
```

**@include Rules:**
- **ONLY use `@include` in `project.gcl`** — does NOT work in other `.gcl` files
- `@include("folder")` recursively includes ALL `.gcl` files in that folder

**Essential Libraries:**
- `@library("std", "7.6.0-dev")` — Standard library (required)
- `@library("explorer", "7.6.0-dev")` — Graph navigation UI at `/explorer` (recommended for development)

**Conventions:** GCL: snake_case files, PascalCase types | Unused vars: `_prefix` | Tests: `*_test.gcl`

## Types

**Primitives:** `int` (64-bit, `1_000_000`), `float` (`3.14`), `bool`, `char`, `String` (`"${name}"`)
**Time:** `time` (μs epoch), `duration` (`5_s`, `7_hour`), `Date` (UI, needs timezone)
**Geo:** `geo{lat, lng}` | Shapes: `GeoBox`, `GeoCircle`, `GeoPoly` (`.contains(geo)`)

```gcl
var list = Array<String>{}; var map = Map<String, int>{};  // ✅ use {}, NOT ::new()
@volatile type ApiResponse { data: String; }  // non-persisted
```

## Nullability

All types non-null by default. Use `?` for nullable:
```gcl
var city: City?;                    // nullable
city?.name?.size();                 // optional chaining
city?.name ?? "Unknown";            // nullish coalescing
data.get("key")!!;                  // non-null assertion

if (country == null) { return null; }
return country->name;               // ✅ no !! needed after null check
```

**⚠️ Cast + coalescing needs parens:**
```gcl
// WRONG: answer as String? ?? "default"
// RIGHT:
(answer as String?) ?? "default"
```

**⚠️ NO TERNARY OPERATOR** — use if/else:
```gcl
var result: String;
if (valid) { result = "yes"; } else { result = "no"; }
```

## Nodes (Persistence)

Nodes = 64-bit refs to persistent containers. Core persistence mechanism.

```gcl
type Country { name: String; code: int; }
var obj = Country { name: "LU", code: 352 };  // RAM only
var n = node<Country>{obj};                    // persisted

*n;              // dereference
n->name;         // ✅ arrow: deref + field (NOT (*n)->name)
n.resolve();     // method
n->name = "X";   // modify object field
node<int>{0}.set(5);  // primitives use .set()
```

**Use node refs for sharing**: `type City { country: node<Country>; }` (light, 64-bit) vs embedded object (heavy)

**Ownership**: Objects belong to ONE node only. For multi-index, store node refs:
```gcl
var by_id = nodeList<node<Item>>{};
var by_name = nodeIndex<String, node<Item>>{};
var item = node<Item>{ Item{} };
by_id.set(1, item); by_name.set("x", item);  // both point to same node
```

**Transactions**: Atomic per function, rollback on error.

**For advanced topics:** See [references/nodes.md](references/nodes.md) for deep dive on transactions, indexed collection sampling, and complex persistence patterns.

## Indexed Collections

| Persisted | Key | In-Memory |
|-----------|-----|-----------|
| `node<T>` | — | `Array<T>`, `Map<K,V>` |
| `nodeList<node<T>>` | int | `Stack<T>`, `Queue<T>` |
| `nodeIndex<K, node<V>>` | hash | `Set<T>`, `Tuple<A,B>` |
| `nodeTime<node<T>>` | time | `Buffer`, `Table`, `Tensor` |
| `nodeGeo<node<T>>` | geo | `TimeWindow`, `SlidingWindow` |

```gcl
// nodeTime - interpolates between points
var temps = nodeTime<float>{};
temps.setAt(t1, 20.5);
for (t: time, v: float in temps[from..to]) { }

// nodeIndex - uses set/get (NOT add)
var idx = nodeIndex<String, node<X>>{};
idx.set("key", val); idx.get("key");

// nodeList
var list = nodeList<node<X>>{};
for (i: int, v in list[0..100]) { }

// nodeGeo
var geo_idx = nodeGeo<node<B>>{};
for (pos: geo, b in geo_idx.filter(GeoBox{...})) { }
```

**Sampling** large time-series: `nodeTime::sample([series], start, end, 1000, SamplingMode::adaptative, null, null)`
Modes: `fixed`, `fixed_reg`, `adaptative`, `dense`

**Array sorting**:
```gcl
cities.sort_by(City::population, SortOrder::desc);  // ✅ native typed sort
// or
buildings.sort_by(Building::value, SortOrder::desc);
```

**⚠️ CRITICAL: Initialize Collection Attributes**
Non-nullable `nodeList`, `nodeIndex`, `nodeTime`, `Array` attributes **MUST be initialized**:
```gcl
// ✅ Correct — initialize collections on creation
var city = node<City>{ City{
    name: "Paris",
    country: country_node,
    streets: nodeList<node<Street>>{}   // ⚠️ MUST initialize!
}};
```

## Module Variables

Root-level vars must be nodes/indexes → auto-persisted:
```gcl
var count: node<int?>;
fn main() { count.set((count.resolve() ?? 0) + 1); }
```

**Global indices are auto-initialized**: Module-level `nodeIndex`, `nodeList`, `nodeTime`, `nodeGeo` are automatically initialized by GreyCat — no `{}` needed:
```gcl
// ✅ Global indices — no initialization needed
var cities_by_name: nodeIndex<String, node<City>>;
var all_users: nodeList<node<User>>;

// ⚠️ Collection ATTRIBUTES in types still need initialization
```

## Model vs API Types

**In model files** — store node refs, declare global indices first:
```gcl
// ✅ Global indices first, then types
var cities_by_name: nodeIndex<String, node<City>>;

type City {
    name: String;
    country: node<Country>;           // ✅ node ref (light, 64-bit)
    streets: nodeList<node<Street>>;  // ✅ store refs, not objects
}
```

**In API files** — return `Array<XxxView>` with `@volatile`, never nodeList:
```gcl
@volatile  // non-persisted, postfix "View" for API responses
type CityView {
    name: String;
    country_name: String;
    street_count: int;
}

@expose  // ⚠️ REQUIRED for API endpoints to be callable via HTTP
@permission("public")  // ⚠️ takes String, not identifier
fn getCities(): Array<CityView> { ... }  // ✅ Array<View>, not nodeList
```

**⚠️ CRITICAL: API functions must have `@expose`** — without it, the function cannot be called via HTTP even if it has `@permission`.

**MCP Server Exposure** — Optionally expose functions as MCP tools using `@tag("mcp")`:
```gcl
@expose
@tag("mcp")  // exposes this function as an MCP tool
@permission("public")
fn searchCities(query: String): Array<CityView> { ... }
```

**⚠️ Use `@tag("mcp")` very sparingly** — only for high-value APIs that are meaningful for AI agent interaction (e.g., search, lookups, key operations). Most API endpoints should NOT be exposed as MCP tools.

## Functions & Control Flow

```gcl
fn add(x: int): int { return x + 2; }
fn noReturn() { }  // no void type
var lambda = fn(x: int): int { x * 2 };
for (k: K, v: V in map) { }  // ✅ prefer for-in
for (i, v in nullable?) { }  // ✅ use ? for nullable
```

## Services Pattern

```gcl
// service/country_service.gcl — avoids naming conflicts
abstract type CountryService {
    static fn create(name: String, code: String): node<Country> { ... }
    static fn find(name: String): node<Country>? { return countries_by_name.get(name); }
}
// Usage: CountryService::create(...) vs fn createCountry() in API
```

## Abstract Types & Inheritance

```gcl
abstract type Building {
    address: String;
    fn calculateTax(): float;  // abstract - must implement
    fn getInfo(): String { return address; }  // concrete - shared
}
type House extends Building {
    fn calculateTax(): float { return value * 0.01; }
}

var buildings: nodeIndex<String, node<Building>>{};
for (addr, b in buildings) { b->calculateTax(); }  // polymorphic
```

**Key:** `abstract type` has fields + abstract/concrete methods. Use `node<BaseType>` for polymorphism, `is` for type checks. Concrete methods cannot be overridden.

## Logging & Error Handling

```gcl
info("msg ${var}"); warn("msg"); error("msg");
try { op(); } catch (ex) { error("${ex}"); }
```

## Parallelization

```gcl
var jobs = Array<Job<ResultType>> {};
for (item in items) {
    jobs.add(Job<ResultType> { function: processFn, arguments: [item] });
}
await(jobs, MergeStrategy::last_wins);  // execute in parallel
for (job in jobs) { results.add(job.result()); }
```

**Key:** `Job<T>` generic, use `MergeStrategy::last_wins`, no nested await.

**Async:** `curl -H "task:''" -X POST http://localhost:8080/fn` or `PeriodicTask::set(...)`

**For production:** [references/concurrency.md](references/concurrency.md)

## Testing

Run with `greycat test`. Test files: `*_test.gcl` in `./backend/test/`.

```gcl
@test
fn test_city_creation() {
    var city = City::create("Paris", country_node);
    Assert::equals(city->name, "Paris");
}

@test
fn test_building_creation() {
    var building = Building::create("123 Main St", BuildingType::Residential);
    Assert::equals(building->buildingType, BuildingType::Residential);
}

fn setup() { /* runs before tests */ }
fn teardown() { /* cleanup after tests */ }
```

**Assert methods**: `Assert::equals(a, b)`, `Assert::equalsd(a, b, epsilon)`, `Assert::isTrue(v)`, `Assert::isFalse(v)`, `Assert::isNull(v)`, `Assert::isNotNull(v)`

**For comprehensive testing guide:** See [references/testing.md](references/testing.md) for advanced Assert methods, setup/teardown patterns, and test organization.

## Common Pitfalls

| ❌ Wrong | ✅ Correct | Why |
|----------|-----------|-----|
| `Array<T>::new()` | `Array<T>{}` | std types use `{}` |
| `(*node)->field` | `node->field` | `->` already dereferences |
| `@permission(public)` | `@permission("public")` | takes String |
| `@permission("api") fn getX()` | `@expose @permission("api") fn getX()` | API functions need @expose |
| `for(i=0;i<n;i++) list.get(i)` | `for (i, v in list)` | type inference |
| `nodeList<City>` | `nodeList<node<City>>` | store refs, not objects |
| `fn getX(): nodeList<...>` | `fn getX(): Array<XxxView>` | API returns Array+View |
| `nodeIndex.add(k, v)` | `nodeIndex.set(k, v)` | nodeIndex uses set/get |
| `for(i, v in nullable_list)` | `for(i, v in nullable_list?)` | use `?` for nullable |
| `fn doX(): void` | `fn doX()` | no void type |
| `City{name: "X"}` (missing collections) | `City{name: "X", streets: nodeList<...>{}}` | init non-nullable collections |

### Acceptable Double-Bang Patterns

Using the non-null assertion operator (double-bang) is acceptable for global registry lookups where data is guaranteed to exist:
```gcl
var config = ConfigRegistry::getConfig(key)!!;  // ✅ OK — populated at init
```

## ABI & Database

**DEV MODE:** Delete deprecated fields. Reset `gcdata/` on schema changes. Add non-nullable fields → make nullable: `newField: int?`

```bash
rm -rf gcdata && greycat run import  # ⚠️ DELETES DATA - ask confirmation
```

Docs: https://doc.greycat.io/

## Full-Stack Development

Building React frontends with GreyCat backends?

**[references/frontend.md](references/frontend.md)** provides a comprehensive 1,013-line guide covering:
- @greycat/web SDK setup and configuration
- TypeScript type generation and integration
- Authentication and authorization patterns
- React Query integration and custom hooks
- Error handling and best practices

This is the most detailed reference in the skill package - start here for frontend development.

## Local LLM Integration

Building AI-powered applications with local language models?

**[references/ai/llm.md](references/ai/llm.md)** covers the complete llama.cpp integration:
- Model loading (GGUF files, GPU offload, split models)
- Text generation and chat completion
- Embeddings for semantic search
- Advanced Context and Sampler APIs
- LoRA adapter fine-tuning

```gcl
@library("ai", "7.5.1");
var model = Model::load("llama", "./model.gguf", ModelParams { n_gpu_layers: -1 });
var result = model.chat([ChatMessage { role: "user", content: "Hello!" }], null, null);
```

## Library References

Complete GCL type definitions and API documentation for all GreyCat libraries are available in the references directory.

**See [references/LIBRARIES.md](references/LIBRARIES.md)** for the complete catalog of std, ai, algebra, kafka, sql, s3, opcua, finance, powerflow, and useragent libraries.
