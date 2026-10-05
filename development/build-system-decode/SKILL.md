---
name: build-system-decode
description: This skill should be used when the user mentions "build system", "Makefile", "Bazel", "Gradle", "Maven", "Nx", "Turborepo", "monorepo", "build targets", "how to build", "which command", "build one package", or "affected/changed projects". It provides a methodology for reading and driving common build systems and monorepos, listing targets, reading the dependency graph, and building or testing a single package without building the world.
---

# Build System Decode

## Purpose
A repeatable way to understand and drive an unfamiliar build, so you can answer "what can I run, what does it do, and how do I build/test just my package?" without holding the whole dependency graph in your head. Detect the tool from its manifest, use the tool's own introspection instead of hand-parsing config, and always find the narrowest command that gets your package green.

## Detection: manifest → build system
| Manifest file(s) | Build system | Introspection command |
|------------------|--------------|-----------------------|
| `Makefile` | Make | `make help`, `make -qp`, grep `.PHONY` |
| `BUILD(.bazel)`, `WORKSPACE`, `MODULE.bazel` | Bazel | `bazel query //...` |
| `build.gradle(.kts)`, `settings.gradle` | Gradle | `./gradlew tasks --all` |
| `pom.xml` | Maven | `mvn help:describe`, `<modules>` |
| `package.json` `scripts` + lockfile | npm/pnpm/yarn | read `scripts`, `<pm> run` |
| `nx.json`, `project.json` | Nx | `nx graph`, `nx show projects` |
| `turbo.json` | Turborepo | `turbo run build --dry` |
| `CMakeLists.txt` | CMake | `cmake --build . --target help` |
| `Cargo.toml` (`[workspace]`) | cargo | `cargo metadata`, `--workspace` |
| `go.mod`, `go.work` | go build | `go list ./...` |

A repo often has **two layers**: a top-level orchestrator (Make, Nx, Turbo, Bazel) driving per-language builds underneath. Identify both.

## The three questions to answer
1. **What targets exist?** Use the tool's list/query command, never invent a target. Distinguish real build/test/lint targets from convenience aliases.
2. **What depends on what?** Get the graph from the tool (`bazel query 'deps(...)'`, `gradle :p:dependencies`, `nx graph`, `cargo metadata`). Find the difference between "build the world" and "build my package + only its deps."
3. **How do I build/test one package?** Every ecosystem has a scoping flag, the single most useful thing to a newcomer. Make it the headline (see `build-systems.md`).

## Decision checklist
1. Detect the tool(s) from the manifest table above; cite the file.
2. Run the introspection command to enumerate real targets.
3. Pull the dependency graph from the tool, not by eye.
4. Identify the single-package build/test command and the affected/changed command.
5. Note required bootstrap (toolchain fetch, `bazel sync`, lockfile verification) before the first build works.

## Additional Resources
### Reference Files
- **`references/build-systems.md`**: per build tool (Make, Bazel, Gradle, Maven, npm/pnpm/yarn, Nx, Turborepo, CMake, cargo, go): how to list targets, read the dependency graph, and build/test exactly one package, with the concrete commands.
- **`references/monorepo-patterns.md`**: workspaces, project graphs, affected/changed detection, task pipelines/caching, and how tasks are wired across packages in each major monorepo toolchain.
