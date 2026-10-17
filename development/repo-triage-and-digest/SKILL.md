---
name: repo-triage-and-digest
description: Two-stage GitHub intake. GitDiagram supplies structure links. Gitingest supplies a size-capped text digest for any model.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: none
  - Registry: KB-Skills, Domain 2
---

# Repo Triage and Digest

Build GitDiagram links, then a path-filtered Gitingest digest. The same tools run over MCP stdio for any model client.

## Trigger

Analyze, inspect, or ingest a third-party GitHub repository.

## Input Schema

- `repositoryUrl`: GitHub repository URL or `owner/repo`. Required.
- `targetModules` or `includePatterns`: directories to keep, for example `src/*`.
- `excludePatterns`: globs to drop. Default drops tests, docs, lockfiles, vendor, and `dist`.
- `maxFileSizeKb`: per-file cap. Default `50`.
- `localRoot`: directory to digest on disk. Omit it to return the Gitingest URL only.
- `authToken`: optional private-repo token. The pipeline never writes it and never returns it.

## Output Schema

- `visualArchitecture.interactiveDiagramUrl`: `https://gitdiagram.com/owner/repo`
- `visualArchitecture.explainerVideoUrl`: `https://gitdiagram.com/owner/repo/videos`
- `ingestionDigest`: summary, directory tree, pruned files, and file text when `localRoot` is set

---

**For Setup, Requirements, Inputs/Outputs, Error Codes, Testing:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
