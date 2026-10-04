---
name: go-docs
description: Go documentation conventions — a doc comment on every exported function, struct, type, and package, package comments in a dedicated doc.go for multi-file packages, godoc style (complete sentences beginning with the identifier's name), and LLM-ready CLI reference generation for cobra tools via a docgen helper built on cobra/doc. Use when writing or reviewing doc comments or godoc in Go code, adding a doc.go or writing a package comment for a Go package, documenting an exported Go API, package, function, or struct, deciding where a package comment or doc.go belongs, or generating markdown CLI documentation for a cobra-based Go tool. Not for OpenAPI/REST API specs.
license: MIT
---

# Go documentation conventions

Doc comments are the API's reference manual: godoc, pkg.go.dev, and editors render them, and LLM
coding agents read them to learn an API. These rules say where they go and what they look like;
for the code itself see the `go-style` skill.

## 1. Every exported identifier gets a doc comment

Every exported function, method, struct and other type, interface, and package-level const or var
(or grouped block) carries a doc comment — no exceptions for "obvious" ones. The comment is a
complete sentence that begins with the identifier's name and states what the caller may rely on:

```go
// Parse splits a KEY=VALUE line into its key and value, trimming whitespace
// around both. It returns an error when the separator is missing.
func Parse(line string) (key, value string, err error) {
```

- Start with the name: `// Loader reads …`, never `// This function reads …`.
- Document behavior and invariants, not implementation — what holds true for the caller.
- Mark deprecations with a `Deprecated:` paragraph so tooling can flag callers.

## 2. Package comments live in doc.go

Every package has exactly one package comment, beginning `Package <name> …`. In a package with
more than one non-test file, put it in a dedicated `doc.go` that holds only the comment and the
package clause, so it never moves when files are reorganized:

```go
// Package keyval stores and parses KEY=VALUE pairs for the demo service.
//
// A Store is safe for concurrent readers; writes must be serialized by the
// caller.
package keyval
```

When the package has a single non-test file, the comment sits at the top of that file instead — a
`doc.go` beside one source file is noise.

## 3. Cobra CLIs generate an LLM-ready reference

A cobra command tree already knows every command, flag, and example — publish it as one markdown
page per command (`mycli.md`, `mycli_serve.md`, …) that humans, search engines, and LLMs can read
(see the [cobra.dev guide](https://cobra.dev/docs/how-to-guides/clis-for-llms/)):

- Expose the root command from the command package, and fill in `Short`, `Long`, an `Example`,
  and `GroupID` on every command — the generators publish exactly that metadata:

  ```go
  // Root exposes the root command for main and the docgen tool.
  func Root() *cobra.Command { return rootCmd }
  ```

- Copy [templates/docgen/main.go](templates/docgen/main.go) to `internal/tools/docgen/main.go`
  and point its import at your command package. It sets `root.DisableAutoGenTag = true` so the
  output is reproducible (no timestamp footer), and renders markdown — optionally with YAML front
  matter — man, or reST via the `github.com/spf13/cobra/doc` generators.
- The helper imports your application's packages, so it lives in the application module and runs
  with `go run` — it is not a pinned developer tool in `tools/go.mod` (see the `go-project`
  skill):

  ```make
  docs: ## Regenerate the CLI reference (docs/cli) from the cobra command tree
  	go run ./internal/tools/docgen -out docs/cli -format markdown
  ```

- Commit the generated `docs/cli` and refresh it whenever commands or flags change, so the
  reference never drifts from the binary.
