---
name: docs-snippets
description: Documentation snippet synchronization. Use when adding code examples to documentation, syncing snippets from samples to docs, verifying docs are in sync with code, working with #region docs:* markers, asking "are we ready to commit?", or preparing releases. Ensures code in documentation is compiled and tested.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(pwsh:*, powershell:*, dotnet:*)
---

# Documentation Snippets Skill

Code examples in documentation must be **compiled and tested**. This skill manages the sync between sample projects and documentation.

## When to Use This Skill

- Adding code examples to documentation
- Syncing docs after code changes
- Verifying docs are current
- **"Are we ready to commit?"** - run the checklist
- Preparing a release

## Quick Reference

### Project Structure

```
{Project}/
├── docs/
│   ├── *.md                                    # Documentation
│   ├── release-notes/                          # Version notes
│   ├── todos/                                  # Active plans
│   │   └── completed/                          # Done plans
│   └── samples/
│       ├── {Project}.Samples.DomainModel/      # Domain with #region snippets
│       ├── {Project}.Samples.DomainModel.Tests/
│       ├── {Project}.Samples.Server/           # Server Program.cs
│       └── {Project}.Samples.BlazorClient/     # Client Program.cs
└── scripts/
    └── extract-snippets.ps1
```

### Key Commands

```powershell
# Verify docs are in sync (CI-safe)
.\scripts\extract-snippets.ps1 -Verify

# Update docs with latest snippets
.\scripts\extract-snippets.ps1 -Update

# List all snippets
.\scripts\extract-snippets.ps1
```

### Region Marker Format

**In C# files:**
```csharp
#region docs:{doc-file}:{snippet-id}
// code here
#endregion
```

**In Markdown:**
```markdown
<!-- snippet: docs:{doc-file}:{snippet-id} -->
```csharp
// replaced by extract-snippets.ps1
```
<!-- /snippet -->
```

### Ready to Commit Checklist

```
[ ] dotnet build                              # Code compiles
[ ] dotnet test                               # Tests pass
[ ] .\scripts\extract-snippets.ps1 -Verify    # Docs in sync
[ ] If release: version updated, release notes created
```

## Detailed Guides

| Guide | Purpose |
|-------|---------|
| [01-snippet-regions.md](01-snippet-regions.md) | How to mark code with `#region docs:*` |
| [02-documentation-sync.md](02-documentation-sync.md) | Syncing snippets to documentation |
| [03-skill-sync.md](03-skill-sync.md) | Syncing snippets to Claude skills |
| [04-verification.md](04-verification.md) | Verification layers and CI integration |
| [05-ready-to-commit.md](05-ready-to-commit.md) | Full pre-commit checklist |
| [06-todos-and-plans.md](06-todos-and-plans.md) | Markdown plans in `docs/todos/` |
| [07-release-notes.md](07-release-notes.md) | Release notes in `docs/release-notes/` |

## Projects

| Project | Samples Location | Status |
|---------|------------------|--------|
| Neatoo | `docs/samples/` | Migration needed |
| KnockOff | `docs/samples/` | Migration needed |
| RemoteFactory | `docs/samples/` | Not started |
