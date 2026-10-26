---
name: julia
description: Use when writing Julia programs — command-line tools with ArgParse, HTTP API clients with HTTP.jl and JSON3, numerical scripts, package environments with Project.toml and Manifest.toml, and Pkg.test in Docker. Also use when Julia start-up latency (time to first execution) dominates a short script, or when an environment resolves differently on another machine.
---

# Julia

Default: current stable Julia from the official tarball or `juliaup`, a project environment per tool (`Project.toml` + committed `Manifest.toml`), `Test` stdlib, `Pkg.test()` as the single test entry point.

## Setup

1. `julia --project=. -e 'using Pkg; Pkg.generate("Tool")'`, then `Pkg.add(["HTTP", "JSON3", "ArgParse"])`.
2. Always run with `--project=.` (or set `JULIA_PROJECT`), otherwise the global environment is used and versions drift.
3. Commit `Manifest.toml` for applications so the exact dependency set is reproducible; omit it for libraries.

## API client tools

- Read tokens from environment variables only; refuse to start if missing, and never print them.
- **Default to a dry run.** List what would be changed; require an explicit `--apply` to perform writes or deletions.
- Respect rate limits: read `Retry-After` on HTTP 429 and sleep; cap retries.
- Paginate until the cursor is empty; never assume one page is everything.
- Before deleting anything, show how the targets were identified (e.g. inspect one example first, then list all matches) so a human can confirm the selector.

```julia
using HTTP, JSON3
function get_json(url; token)
    r = HTTP.get(url, ["Authorization" => "Bearer $token"]; status_exception=false, retry=false)
    r.status == 429 && (sleep(parse(Int, HTTP.header(r, "Retry-After", "1"))); return get_json(url; token))
    r.status == 200 || error("HTTP $(r.status)")
    JSON3.read(r.body)
end
```

## Numerical work

- Write type-stable functions (check with `@code_warntype`); avoid global variables in hot loops or wrap them in `const`.
- Preallocate arrays and use in-place functions (`mul!`, `.=`) for loops.
- Benchmark with `BenchmarkTools.@btime`, not `@time` on the first call (which includes compilation).

## Testing

- `test/runtests.jl` with `@testset`s; `julia --project -e 'using Pkg; Pkg.test()'`.
- Mock HTTP by passing the request function as an argument, so tests run offline.

## Verification loop

1. `Pkg.instantiate()` from a clean checkout succeeds.
2. `Pkg.test()` passes (also inside `docker build` for a clean environment).
3. Run the tool in dry-run mode against the real API before any `--apply`.

## Pitfalls

- **Time to first execution:** the first call of each function compiles; a short CLI may spend most of its time compiling. Accept it for occasional tools, or use precompilation (`PrecompileTools`) / a system image for frequent ones.
- **1-based indexing** and column-major arrays: iterate the first index in the inner loop.
- **Integer overflow** wraps silently for `Int`; use `BigInt` or checked arithmetic where values can grow.
- **Strings are UTF-8 with byte indices:** `s[2]` may error on multibyte text; use `eachindex`, `nextind` or `collect(s)`.
- **`using` inside functions** is not allowed; load packages at top level.
