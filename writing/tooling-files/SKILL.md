---
name: tooling-files
description: "Maps shared repository tooling for files, paths, Git queries, project ownership and Markdown fences. Load before adding or changing a helper in these areas."
---

# Repository file and document helpers

Search by capability before adding a helper ([AGENTS.md](../../../AGENTS.md#core-rules)).
These are the shared homes; callers keep only their domain-specific decisions.
Build architecture, compiler identities, candidate installation and admission route to
[tooling](../tooling/SKILL.md).

| Capability | Home |
|---|---|
| Lexical path containment and host path comparison | `PuckPaths.IsWithin`, `PuckPaths.Comparison` in `src/Puck.Abstractions/PuckPaths.cs` |
| A path's one spelling for a composed or persisted key, where a comparer cannot reach | `PuckPaths.Key` (normalized, upper-cased where the file system folds case); never a hand `ToUpperInvariant` |
| A path relative to a directory, spelled with `/` | `PuckPaths.Relative`; never `Path.GetRelativePath` plus a separator replace, which leaves a backslash on Linux |
| Spell a path with `/` as its only separator, from a project that cannot reference `Puck.Abstractions` | `PortablePath.Slashed` in `src/Puck.Confinement/PortablePath.cs`, which `PuckPaths.Slashed` forwards to; the analyzer allowlist and `build/ProjectArchitecture.cs` keep their own replace, since neither can reference a project |
| Inspect path components for links, below an optional root (the root itself is the caller's choice and never inspected) | `CliTreeFiles.LinkedAncestor` in `src/Puck.Cli.Core/CliTreeFiles.cs` |
| Decide whether a directory contains a path by file identity (a "must not contain" refusal) | `ConfinedDirectory.Contains` in `src/Puck.Confinement/ConfinedDirectory.cs`; `PuckPaths.IsWithin` fails open for aliases |
| Remove an owned directory tree without following descendant links | `ConfinedDirectory.RemoveTree` in `src/Puck.Confinement/ConfinedDirectory.cs` |
| Walk, open, read or delete below a held directory without following links (every component opened relative to its parent's handle) | `ConfinedDirectory.Walk`, `Descend`, `OpenRead`, `DeleteFile` in `src/Puck.Confinement/ConfinedDirectory.cs` |
| Stage, flush, publish or discard complete replacement files | `AtomicFile`, including `PendingWrite`, in `src/Puck.Confinement/AtomicFile.cs` |
| Tell a live writer's staged temporary from an abandoned one (the writer's claim in its name, never its age) | `AtomicFile.IsAbandoned` in `src/Puck.Confinement/AtomicFile.cs` |
| Hold a cache directory to a bound, listing and deleting only beneath it | `CacheRetention` in `src/Puck.Abstractions/CacheRetention.cs` |
| Compare files or a file and bytes with bounded memory | `FileContent` in `src/Puck.Confinement/FileContent.cs` |
| Read an opened file or stream to its end under a byte ceiling, never trusting its length | `FileContent.ReadAtMost` / `ReadAtMostAsync` in `src/Puck.Confinement/FileContent.cs` |
| Decode a file's whole bytes as text the way `File.ReadAllText` does (a byte-order mark picks the encoding) | `FileContent.Text` in `src/Puck.Confinement/FileContent.cs` |
| Record what a compile read, and answer a file's digest or a directory's listing from its stamp (existence, length, last write, creation) while the stamp holds | `CompileInputs` (`Current`, `Digest`, `List`, `ReadAllBytes`, `RacyStampWindow`) in `src/Puck.Assets/CompileInputs.cs`; a poll or a cache validity check never re-hashes an input behind it |
| Copy a directory tree, or selected files beneath it, without following a link in either tree or writing through an existing hard link; `intoEmpty` for a clean copy that replaces nothing | `CliFiles.CopyDirectory` in `src/Puck.Cli.Core/CliFiles.cs` |
| Start a redirected companion process and end its output reads after it exits | `ChildProcess.StartRedirected`, `OpenOutputReader` and `DrainAfterExitAsync` in `src/Puck.Abstractions/ChildProcess.cs` |
| Read source lines or nonempty process-output lines | `CliText` in `src/Puck.Cli.Core/CliText.cs` |
| Query Git, resolve common directories or commits, list unignored files | `CliGit` in `src/Puck.Cli.Core/CliGit.cs`; local reports use `ReadOnlyAsync` |
| Parse NUL-delimited worktree records | `CliWorktree.Parse` in `src/Puck.Cli.Core/CliWorktree.cs` |
| Find an owning project within an optional boundary | `CliProjects.FindOwningProject` in `src/Puck.Cli.Core/CliProjects.cs` |
| Read C# type declarations for project selection | `DeclarationsCommand.ReadTypes` in `src/Puck.Cli.Source/Analysis/DeclarationsCommand.cs` |
| Track Markdown code fences in link and quotation scans | `MarkdownFence` in `src/Puck.Cli.Source/Docs/MarkdownFence.cs` |
| Collect non-XML C# comments and emit line sites | `InlineComments.CollectComments` and `ScanSites` in `src/Puck.Cli.Source/Scan/` |
| Match compiler paths against analyzer allowlist identities | `AnalyzerAllowlistPath` in `src/Puck.Analyzers/AnalyzerAllowlistPath.cs` |

Lexical containment and ancestor inspection do not establish confinement against concurrent path replacement.
Every repository walk that deletes or replaces files (`ConfinedDirectory.RemoveTree`, `CliFiles.CopyDirectory`,
`CacheRetention`) stays beneath a directory handle and never follows descendant links. Tree removal refuses them
by default; run-directory cleanup opts into `removeLinks` to unlink them without touching their targets. The caller owns the selected
root, whose ancestors are resolved by the OS. A path-based `Directory.EnumerateFiles(..., AllDirectories)` follows
junctions and symbolic links, so it never feeds a deletion.

A cleanup never deletes a staged temporary by age alone: a writer can be suspended between staging and
publication for any length of time. `AtomicFile.IsAbandoned` judges the writer's claim (host, process, start time)
carried in the temporary's name.

Batch writers own pending writes until each is committed or disposed. `PendingWrite.Commit(overwrite: false)`
preserves a concurrent winner; replacing that with an existence check followed by an overwriting write does not.
Run [verification](../verification/SKILL.md)'s focused builds and laws for the changed boundary. Deletion and
persisted-data rewrites need the [hazards](../../../docs/development/hazards.md#silent-invariants) review.
