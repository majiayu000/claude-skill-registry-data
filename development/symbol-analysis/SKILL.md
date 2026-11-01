---
name: symbol-analysis
description: "Answers C# structure questions with puck references and declarations: which types derive from, implement or override a symbol, who references it, safe to delete or rename. Text: content-search."
---

# Symbol analysis

Use compiler-backed evidence for C# structure. Text matching cannot resolve
aliases, overloads, extensions, generic instantiations, or name collisions.
Treat repository-specific examples as snapshots; re-run the command against the
current tree before relying on one.

| Question | Command |
|---|---|
| Who references it, is it dead, is a delete safe | `puck references <name> --no-doc`, then `puck search -M 0 -l <name>` for files no project compiles; build the affected projects before declaring a delete safe |
| What implements this interface or member | `puck references <name> --implementers` |
| What overrides this member | `puck references <name> --overrides` |
| What derives from this type | `puck references <name> --derived` |
| Two same-named symbols: which is which | `puck references <name> --declarations`, then narrow with `--containing <namespace-or-type>` |
| What a file or tree declares, members, base lists, attributes, crefs | `puck declarations --members <path>` (add `--kind`, `--name`, `--base`, `--attribute`, `--doc`); parse-only, so it needs no build and sees uncompiled files, but proves no usage |
| Literal, config or non-C# content | `content-search` |
| Whether a refactor still compiles | Build the affected project |
| `.puck` DSL name resolution (state, prototype, placement, camera names, imports) | Neither verb parses `.puck`; use `puck lint` (`PUCK_LINT_00x`) and the DSL's LSP, see `puck-dsl` |

## Start the CLI from a clean checkout

Run from the repository root with the checkout's own CLI build, never a
published copy or the global `puck` tool, both of which lag the head. Copy
`src/Puck.Cli/bin/Release/net11.0/` to a scratch directory named for your lane
and run the copy, so the running tool never locks the build output another
build needs:

```text
dotnet <lane>-cli/Puck.Cli.dll <verb> <arguments>
```

If that build is absent, build it (`dotnet build src/Puck.Cli -c Release
-nodeReuse:false`) and copy it
([verification](../verification/SKILL.md#run-verbs-from-your-own-cli-copy));
`dotnet run` on the project runs the build in place and locks its output, so it
is not a substitute for the copy.

`references` loads the whole solution. A fresh worktree is unrestored, and the
load then fails with exit 2 and a message counting the projects that carry no
`obj/project.assets.json`: run `dotnet restore Puck.slnx -nodeReuse:false` at the
worktree root and retry. `declarations` needs neither a restore nor a build.

## Evidence rules

- Inventory a family with `declarations`, then query named symbols one at a
  time. An empty-name `references "" --contains --containing <family>` can
  retain gigabytes of workspace and reference state while searching every
  matching member; narrowing the containing name does not make that broad
  query cheap. Use `search` for a textual family inventory.
- `references` loads a project graph and resolves symbols. Narrowing with
  `--project` changes the closure and therefore the question.
- Read the definition on each `ref` line: it is the resolved symbol, which is
  not always the one queried. Constructing a type reports under its constructor,
  and an interface-dispatched call reports under the interface. `--strict` keeps
  only the queried symbol's own group, so it hides every construction site.
- Documentation `cref` locations count as references; `--no-doc` drops them. A
  symbol whose only references are crefs is a dead-code candidate.
- A symbol that looks unused by name can be used through an extension method or
  a `using` alias, and one that looks used can be a name collision. Check the
  member, not only the containing type (`AllocatorExtensions` has no references
  while its `Alloc` method has many).
- Rename safety: a text count undercounts, because a `using Alias = ...;`
  hides the type's name at its uses. Take the `references` list, then build the
  affected projects after the rename; the compiler is the full check.
- `references` cannot see files no project compiles (the quarantined
  `experimental/` trees, file-based apps). "Zero references" means zero compiled
  references: pair a deletion decision with `puck search -M 0 -l <name>`.
- `declarations` parses syntax without a build and can see those files, but it
  matches names and cannot prove semantic usage. A missing path is an error
  (exit 2), never an empty inventory.
- A partial workspace load is not a clean answer. Use `--allow-partial` only
  when explicitly accepting and reporting incomplete evidence.
- Inspect ambiguity and resolved-definition output before acting on a short
  symbol name. Several `partial` declarations of one type report one line each.
- `references`/`declarations` parse the C# project graph only; nothing in
  `Puck.Cli`'s analysis verbs parses `.puck`. Treat a `.puck` name question as
  out of scope rather than assuming a text search is the only fallback.

## Load the full reference selectively

Read [references/complete-reference.md](references/complete-reference.md) for
exact flags and output, solution/project closure traps, documentation behavior,
generated and inactive-code limits, verified edge cases, and the Release-mode
file-based Roslyn app fallback.

## Related skills

| Question | Skill |
|---|---|
| Literal, config or non-C# text; exhaustive file lists | `content-search` |
| `.puck` name diagnostics, `puck lint` | `puck-dsl` |
| Whether a deletion or rename also leaves stale docs | `boy-scout` |
