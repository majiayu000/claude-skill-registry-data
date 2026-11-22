---
name: spike-dotnet
description: Validate an assumption or run a quick spike with a .NET file-based app (dotnet run app.cs) - a single throwaway file outside the repo tree, pinned to the repo's package versions when validating repo behavior. Use when a plan step, bug-fix diagnosis, or review claim rests on unverified library/runtime behavior.
disable-model-invocation: false
user-invocable: true
argument-hint: "<the assumption or behavior to validate>"
---

# Spike with a .NET file-based app

When a plan step, bug-fix diagnosis, or review claim rests on an assumption about
library or runtime behavior that hasn't been verified, don't reason from memory —
run it. File-based apps make that a single file: `dotnet run spike.cs`, no project,
no solution pollution. Reference:
https://learn.microsoft.com/en-us/dotnet/core/sdk/file-based-apps

**OPTIONAL: lives in `.agentic/optional-skills/`; onboarding copies it into
`.claude/skills/` for .NET repos. Requires .NET SDK 10+ — check `dotnet --version`.**

## Mechanics

- One `.cs` file, top-level statements. Directives at the top of the file:
  - `#:package <Name>@<Version>` — NuGet reference
  - `#:sdk Microsoft.NET.Sdk.Web` — when the default SDK isn't enough
  - `#:property <Name>=<Value>` — e.g. `LangVersion=preview`
- Run with `dotnet run spike.cs`. If a spike graduates into real code:
  `dotnet project convert spike.cs`, then the normal `/plan` flow — never grow
  production code inside a spike file.

## Rules

1. **Location:** the session scratchpad or OS temp dir — NEVER the repo tree.
   Nothing to commit, nothing to clean out of the solution.
2. **Version fidelity — the step agents get wrong:**
   - Validating THIS repo's behavior → pin `#:package` to the exact versions in
     `Directory.Packages.props` and target the repo's TFM. A spike that passes on
     latest proves nothing about the pinned version the repo actually runs.
   - Evaluating a NEW library for adoption → resolve latest stable (hard rule 4).
3. **One question per spike.** Print expected vs. actual and make the file assert
   its own answer; keep it small enough to read at a glance (~50 lines).
4. **Report real output.** Paste what the run actually printed. A spike that
   didn't run, or was inconclusive, is not evidence — say so plainly.

## Outcome routing

- Settles a decision with alternatives → `/decide`, with the spike's output quoted
  as the evidence for why the losing options lost.
- Reveals a non-obvious trap → `/gotcha`. Evidence must be a REPO path (the
  affected file) — the spike file is ephemeral, so put the key observed output in
  the claim text.
- Merely confirms the assumption → proceed; write nothing (the code is the doc).
