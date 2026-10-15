---
name: nix-perf
description: Use this when a flake's `nix develop` / `direnv allow` / `nix flake archive` is slow on a fresh checkout (the "first time takes 10 minutes" complaint). Diagnoses where the time actually lives and how to shrink the flake.lock input graph without changing build outputs.
---

# Diagnosing slow flake first-fetch

## Triage which operation is actually slow

Before optimizing anything, pin down which command the user runs and time each on a **fresh** state (cleared eval cache + cold `/nix/store` for an honest measurement):

| Command | What it does | Bottleneck |
|---|---|---|
| `nix develop --command true` | Lazy: fetches only inputs whose outputs the devShell eval touches | Eval + minimal substitution |
| `nix print-dev-env` | Same laziness as above; what plain nix-direnv `use flake` invokes | Same as above |
| `nix flake archive --no-write-lock-file` | Eager: fetches every node in flake.lock into the store | Total lock-graph size |
| `nix build .#default` | Eval + realize closure | Eval + builds not in cache |

The "direnv takes 10 minutes" complaint usually maps to `nix flake archive` (nix-direnv with input pre-caching enabled, or wrappers that warm the store for offline use), not to `nix print-dev-env`. **Confirm which one is slow before you start optimizing** — lazy eval is invariant to lockfile bloat; eager archive isn't.

## Inspect lockfile shape

Use `nix run nixpkgs#jq` on `flake.lock` to extract:

- **Total node count** (`.nodes | keys | length`) — gross size of the input graph
- **Unique `narHash` count** (`[.nodes[].locked.narHash] | unique | length`) — actual number of distinct sources nix would fetch on a cold machine. Duplicate nodes pointing at the same store path don't add fetches.
- **Top duplicated repos** — group nodes by `original.repo` / `original.url`, sort by count. Many copies of `nixpkgs`, `flake-utils`, `flake-parts`, `nix-systems/default` is normal; very large counts mean missing `follows`.
- **Recursion / self-cycles** — search for any input whose downstream lists the current flake (or an older tag of it) as one of *its* inputs. The lockfile resolver expands these into N stacked copies and explodes transitively. This is the single biggest cause of pathological flake.lock blow-up in practice.

## Reduce the graph with `follows`

For each transitive duplicate that has a sibling at the root, add `inputs.X.inputs.Y.follows = "Y"`. You can chain: `inputs.A.inputs.B.inputs.C.follows = "C"`. The rules:

- **Safe**: pointing a downstream's dev-tooling (`flake-parts`, `flake-utils`, `git-hooks-nix`, `treefmt-nix`, `fourmolu-nix`, `nix-systems`) at the root's copy. These are eval-only and version-tolerant.
- **Safe**: collapsing a self-recursion. If `foo` lists `your-flake` as an input, follow the inner `your-flake`'s sub-inputs back to the root (`inputs.foo.inputs.your-flake.inputs.bar.follows = "bar"`). Also follow `inputs.foo.inputs.your-flake.inputs.foo.follows = "foo"` to break the recursion at one level.
- **Risky**: re-following a downstream's `nixpkgs` or `haskell-flake` to a *different revision* than what its lockfile pinned. This changes hash propagation and triggers cabal/Haskell rebuilds. Only do it if you're explicitly bumping that downstream.
- **Useless**: following inputs that the downstream resolves to the same `narHash` you'd pick anyway. Lockfile gets renumbered, fetch count doesn't change.

After each change run `nix flake lock` and re-measure both node count and unique-narHash count. Commit only changes that move the unique-narHash number.

## Measurement methodology

For cold-fetch numbers, use a fresh VM. On juspay infrastructure: `pu create --name X`, ship the repo snapshot with `git archive <ref> | ssh X 'tar -x -C /tmp/...'`, time the operation, then `pu destroy X` and recreate for the next sample so `/nix/store` starts empty. Don't try to simulate cold by deleting paths from a live `/nix/store` — the nix-daemon protects flake-input paths as live roots and `--ignore-liveness` doesn't always evict them.

For eval-only numbers (no fetch), keep `/nix/store` warm and clear `~/.cache/nix/eval-cache-v*` between runs. Median of 3–5 runs.

Always record both numbers separately. Eval improvements and fetch improvements look very different and conflating them produces misleading PR descriptions.

## Diminishing returns

Stop optimizing when the remaining lockfile duplicates are at *distinct* revisions (different repos pinning different `nixpkgs` revs, for instance). Further consolidation requires bumping inputs, which is a separate decision from input-graph hygiene.

## Companion docs

- `nix-for-dev` (this repo) — flake.nix structure conventions (zero-inputs + npins)
- `nix-health` (this repo) — substituters, max-jobs, trusted-users checks that also gate first-fetch speed
- [Flakes reference: input attributes](https://nix.dev/manual/nix/2.31/command-ref/new-cli/nix3-flake.html#flake-inputs) — `follows`, `flake = false`, etc.
