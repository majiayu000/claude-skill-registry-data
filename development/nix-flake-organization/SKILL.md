---
name: nix-flake-organization
description: Use when reorganizing Nix flakes, flake-parts outputs, NixOS modules, nix-darwin modules, or Home Manager modules into a thin flake/ public surface with implementation under src/.
---

# Nix flake organization

Keep `flake/` as the public output layer and `src/` as the implementation layer. The flake tree names, routes, and re-exports outputs; feature behavior, module bodies, package derivations, app scripts, and helper logic live under `src/<name>/...`.

Apply [codebase-design](../codebase-design/SKILL.md) within those boundaries:
keep each feature's implementation together and extract only to hide complexity
or enable useful reuse. Nix output adapters are meaningful public entrypoints;
additional internal forwarding files need their own purpose. Preserve Nix's
roles rather than imposing TypeScript `models/` and `services/` directories.

## When to use

- A user asks to reorganize or refactor a Nix flake layout.
- Flake outputs are crowded into `flake.nix` or mixed with implementation code.
- NixOS, nix-darwin, Home Manager, or flake-parts modules contain business logic directly in output wiring files.
- A repo needs a clear split between public flake API and implementation internals.

## When NOT to use

- The task is only to add one package, app, or module without changing repo layout.
- The repo is not a Nix flake.
- The user explicitly wants a different established project layout preserved.

## Canonical prompt

Use this improved prompt when turning the request into an implementation plan:

> Reorganize this repo so its public flake surface lives in a top-level `flake/` directory: `flake/apps`, `flake/packages`, `flake/lib`, and `flake/modules/{flake-parts,home-manager,darwin,nixos}` where applicable. Keep `flake.nix` as a minimal entrypoint and keep every file under `flake/` thin: it may declare output names, import implementation files, compose flake-parts modules, and adapt public calling conventions, but it must not contain derivation logic, app scripts, option/config bodies, service behavior, or helper implementations. Keep those implementation details together in feature-oriented `src/<name>/...` paths. Preserve existing output attribute names during structural moves; follow the repository's compatibility policy when changing the public interface. Verify with `nix flake show`, `nix flake check`, and representative package/module evals or builds.

## Target shape

Prefer this structure, adapting names to the existing repo:

```text
flake.nix
flake/default.nix
flake/apps/default.nix
flake/packages/default.nix
flake/lib/default.nix
flake/checks/default.nix       # if checks exist
flake/devShells/default.nix    # if devShells exist
flake/overlays/default.nix     # if overlays exist
flake/modules/flake-parts/default.nix
flake/modules/home-manager/default.nix
flake/modules/darwin/default.nix
flake/modules/nixos/default.nix
src/<name>/app.nix
src/<name>/package.nix
src/<name>/lib.nix
src/<name>/modules/flake-parts.nix
src/<name>/modules/home-manager.nix
src/<name>/modules/darwin.nix
src/<name>/modules/nixos.nix
```

`flake/modules/flake-parts` belongs beside the platform module families when flake-parts modules exist, even if the user's shorthand example omits it.

Feature-oriented means grouping by domain concept, not by output type. If a concept `vpn` has a package, app, and NixOS module, keep them under `src/vpn/`. If a package has no associated modules, `src/<pkg-name>/package.nix` is fine. When a repo is already organized by platform, preserving that structure under `src/` is acceptable, but do not mechanically recreate the whole `flake/` tree under `src/`.

## Thin layer rule

| Location                    | Allowed                                     | Not allowed                                       |
| --------------------------- | ------------------------------------------- | ------------------------------------------------- |
| `flake.nix`                 | Inputs, minimal `outputs`, import `./flake` | Package/module implementation                     |
| `flake/apps`                | App output names and imports                | Shell scripts, wrappers, runtime behavior         |
| `flake/packages`            | Package output names and imports            | `mkDerivation`, overlays, build logic             |
| `flake/lib`                 | Public helper re-exports                    | Helper implementations                            |
| `flake/checks`              | Check output names and imports              | Test harness implementation                       |
| `flake/devShells`           | Dev shell output names and imports          | Tool setup logic, shell hooks                     |
| `flake/overlays`            | Overlay output names and imports            | Package overrides and build logic                 |
| `flake/modules/flake-parts` | flake-parts imports and module composition  | `perSystem` build logic, derivations, app scripts |
| `flake/modules/*`           | Public module exports and imports           | Options, `config`, assertions, services           |
| `src/<name>/...`            | All implementation details                  | Public output schema decisions                    |

Thin does not mean empty. A thin file can adapt calling conventions, pass `inputs`, `self`, or `pkgs`, and preserve public attribute names. It should be understandable without reading implementation details.

Keep configured file limits. If a cohesive module exceeds one, first look for an
independent responsibility; otherwise document a narrow increase or exception.
Keep options, defaults, assertions, and configuration local when they explain
one feature, even when that makes a module longer.

For module outputs, thin means the `flake/modules/<platform>/default.nix` file is a re-export point. It imports the full module from `src/` and wires it into the public output attribute. It does not mean splitting options from config inside a single module; options and config stay together in `src/<name>/modules/<platform>.nix`.

```nix
# flake/modules/nixos/default.nix
{ ... }:
{
  flake.nixosModules.vpn = import ../../../src/vpn/modules/nixos.nix;
}

# src/vpn/modules/nixos.nix
{ config, lib, pkgs, ... }:
{
  options.services.vpn = { ... };
  config = lib.mkIf config.services.vpn.enable { ... };
}
```

In flake-parts repos, `perSystem` often owns `packages`, `apps`, `checks`, and `devShells`. Keep `perSystem` composition thin in `flake/modules/flake-parts`; package derivations still belong in `src/<name>/package.nix`, app behavior in `src/<name>/app.nix`, and dev shell/check implementation in `src/<name>/...`. Do not define the same output through both direct `flake/packages` wiring and flake-parts `perSystem` wiring.

## Migration workflow

1. Inventory current public outputs: `packages`, `apps`, `lib`, `checks`, `devShells`, `overlays`, `nixosModules`, `darwinModules`, `homeManagerModules`, and flake-parts imports.
2. Preserve the public output schema first. Move files without renaming output attributes unless the user requested a breaking change.
3. If current outputs are interleaved in one file, first separate each output family enough that it can move independently; avoid a big-bang rewrite.
4. Create the `flake/` directories as output shims and move one output family at a time.
5. Move implementation into feature-oriented `src/<name>/...`; avoid recreating the `flake/` tree under `src/` unless the repo is already platform-oriented.
6. Keep shared implementation in `src/<name>/lib.nix` or `src/shared/<name>.nix`, not in `flake/lib`.
7. Follow the repository's compatibility policy for renamed outputs. Keep aliases only when that policy requires them; otherwise update consumers and remove obsolete paths.
8. Give outputs without an example directory, such as `formatter`, their own thin `flake/<output>/` shim or leave them in the nearest existing composition file; do not fold them into unrelated directories.
9. Verify after each family move with `nix flake show`, `nix flake check`, and targeted builds/evals.

## Common mistakes

- Moving `flake.nix` into `flake/`; Nix expects `flake.nix` at the repo root.
- Treating `flake/` as the new implementation home instead of a thin public layer.
- Hiding implementation in `flake/lib` because it feels like a shared bucket.
- Putting option declarations, `config`, assertions, or services in `flake/modules/*`.
- Forgetting that `packages.${system}` and `apps.${system}` are system-specific while module outputs usually are not.
- Putting `perSystem` build logic in `flake/modules/flake-parts` instead of importing implementations from `src/<name>/...`.
- Creating both direct output wiring and flake-parts `perSystem` wiring for the same derivation without a deliberate compatibility reason.
- Creating circular imports between `flake/lib`, `flake/modules`, and `src`.
- Changing public output names during a move-only refactor.
- Skipping verification because the change looks like only path shuffling.

## Templated scripts

When packaging shell scripts, keep reusable script logic in its own source file instead of embedding long scripts inline in Nix strings. Use Nix only to substitute package-specific defaults.

Prefer nixpkgs-style `@name@` placeholders with `replaceVars`:

```nix
writeTextFile {
  name = "tool";
  destination = "/bin/tool";
  executable = true;
  text = builtins.readFile (replaceVars ./tool.sh {
    default_config = builtins.toJSON config;
  });
}
```

In the script, group all Nix substitutions at the top and make runtime values overrideable by arguments or environment variables:

```sh
default_config() {
  cat <<'JSON'
@default_config@
JSON
}

: "${TOOL_JQ:=jq}"

tool_config() {
  if [ -n "${TOOL_CONFIG_JSON:-}" ]; then
    printf '%s\n' "$TOOL_CONFIG_JSON"
  else
    default_config
  fi
}
```

This keeps scripts usable outside Nix, makes the Nix coupling easy to audit, avoids quote-heavy inline shell strings, and matches current nixpkgs conventions now that `substituteAll` has been replaced by `replaceVars`.

## Review checklist

- `flake/` files are mostly imports, attr names, re-exports, and public calling-convention adapters.
- `src/<name>/...` contains derivations, scripts, options, config, services, assertions, and helpers.
- Existing public output names still work or have deliberate migration notes.
- Module families are separated: `home-manager`, `darwin`, `nixos`, and `flake-parts` do not leak platform-specific logic into each other.
- Verification commands cover both system-specific outputs and module evaluation paths.
- Templated scripts live in standalone files, use `@name@` placeholders via `replaceVars`, and keep Nix-specific defaults grouped at the top with environment/argument overrides for reusable behavior.

## Tools

None. This is a pure prompt and review skill. Use the repo's existing Nix commands for verification.

## Reference

No separate reference files. Use the canonical prompt, thin layer rule, migration workflow, and review checklist above.
