---
name: nixmap
description: Vimjoyer's Nixmap course (vimjoyer.com/nixmap) as a reference. The Nix language, nixpkgs and packaging (callPackage, override, overrideAttrs, overlays, mkDerivation, build phases, fetchers, writers, wrapping), the nix CLI, NixOS configuration, the module system (options, mkIf, mkDefault/mkForce, mkOption, types), Home Manager, flakes (inputs, follows, flake-parts, systems), and dev shells (mkShell, nix develop, direnv, devenv). Use when writing or explaining Nix code, debugging an evaluation error such as infinite recursion or an option type mismatch, packaging software, or structuring a flake, NixOS or Home Manager config.
---

# Nixmap

Lesson text and code examples from <https://vimjoyer.com/nixmap/>, captured
2026-10-15, split by section. Each file is long, so `rg -n '^## ' references/<file>.md`
to list its lessons, then read only the lesson you need. "Try it" blocks are the
site's interactive exercises; their starting code is kept as an example.

Examples on the site pin `nixos-26.05`. For option names and package
attributes, nixpkgs itself (or `nix eval`) is the source of truth.

| File | Lessons |
| --- | --- |
| `references/basics.md` | What Nix is, declarative config |
| `references/language.md` | Expressions, numbers, strings, indented strings, booleans, comparisons, if/then/else, null, lists and `++`, attribute sets, selection, `or`, `?`, `//`, `rec`, `let … in`, interpolation, `with`, `inherit`, functions (multiple, set, default, `...`, `@` arguments), `builtins`, types, `map`, laziness, `throw`/`assert`, infinite recursion, paths, `import` |
| `references/nixpkgs.md` | Nixpkgs, `pkgs`, package attributes, `lib`, `callPackage`, `override`, `overrideAttrs`, overlays (and in NixOS/flakes), the store, store paths, derivations, first package, C/Python/Rust projects, sharing a package, default package, build phases, `buildInputs` vs `nativeBuildInputs`, hooks and `runHook`, fetchers, choosing source files, upstreaming to nixpkgs, the sandbox, derivations in strings, closures, garbage collection, binary caches, writers, wrapping programs, configs inside a wrapper, nix-wrapper-modules |
| `references/commands.md` | Installing Nix, legacy vs experimental commands, `nix-build`, `nix-shell`, `nix repl`, experimental features, `nix eval`, `nix build`, `nix shell`, `nix run` |
| `references/nixos.md` | `configuration.nix`, `nixos-rebuild`, generations, `environment.systemPackages`, users, services, `hardware-configuration.nix`, NixOS from a flake, several machines in one flake, passing inputs to modules (`specialArgs`), graphics drivers, desktops and window managers, install/configure/flake walkthroughs |
| `references/modules.md` | Modules, options, the `config` argument, `imports`, merging definitions, `mkDefault`/`mkForce`, `mkIf`, conditional imports and infinite recursion, declaring options, option types |
| `references/home-manager.md` | Home Manager, `programs`, `home.file`, HM inside NixOS, NixOS settings in HM (`osConfig`), install, taking your home to another machine |
| `references/flakes.md` | Flakes, flake references, installables, `follows`, packages from a second nixpkgs, flake-parts, systems, flakes only see files in Git |
| `references/devshells.md` | `mkShell`, `devShells`, `nix develop`, direnv, devenv, a devshell walkthrough |
