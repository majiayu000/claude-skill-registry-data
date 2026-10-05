---
name: read-docs
description: Search internal project docs (docs/, README.md, CLAUDE.md, *.md) for patterns, conventions, architecture. Use proactively before features, in new code areas, or when debugging.
argument-hint: <keywords or topic>
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Read Docs

Search internal documentation for project-specific information.

## Usage

```
/read-docs auth                    # Search for auth-related docs
/read-docs database schema         # Search for database/schema docs
/read-docs                         # List available documentation
```

## Search Strategy

1. **Check for docs/ folder** - Primary documentation location
2. **Search filenames** - Glob for keyword matches in file names
3. **Search contents** - Grep for keyword matches in file contents
4. **Prioritize results**:
   - Exact filename match (e.g., "auth" → `docs/auth.md`)
   - Filename contains keyword (e.g., "auth" → `docs/authentication-guide.md`)
   - Content matches (e.g., "auth" mentioned in `docs/architecture.md`)

## Locations Searched

In order of priority:

1. `docs/**/*.md` - Primary documentation
2. `CLAUDE.md` - Project conventions
3. `README.md` - Project overview
4. `*.md` in project root - Other documentation

## Gotchas
- The search cap of 5 files means relevant docs can be silently skipped. If the most relevant doc ranks 6th, it will be listed but never read.
- Trust code over docs when they conflict — docs may describe an intended design that was never implemented or was later changed.

## Workflow

### With keywords:

1. Search filenames for keyword matches:
   - Glob pattern: `docs/**/*{keyword}*`

2. Search file contents for keyword matches:
   - Grep pattern: `{keyword}` path: `docs/` and root `*.md` files

3. Rank matches by priority:
   - Exact filename match (e.g., "auth" → `docs/auth.md`)
   - Filename contains keyword (e.g., "auth" → `docs/authentication-guide.md`)
   - Content match with keyword in a heading (e.g., `## Auth` in `docs/architecture.md`)
   - Content match in body text

4. Read up to 5 top-ranked matches and summarize findings.

5. For multi-word queries (e.g., "database schema"), search each word separately AND as a phrase. Prioritize files that match all words over files matching only one.

6. If more than 5 files match, list the remaining filenames without reading them so the user knows what else is available.

### Without keywords:

List available documentation:
- Glob pattern: `docs/**/*.md`
- Glob pattern: `*.md` (root-level docs)

Present a structured overview of available documentation:

1. Group files by directory (e.g., `docs/api/`, `docs/guides/`, root-level)
2. For each file, show the filename and its first heading (or first non-empty line if no heading exists)
3. If more than 20 files exist, summarize by directory with file counts and list only the top-level structure instead of enumerating every file

## Output

Summarize findings:
1. **Documents found** - List with brief description of each
2. **Key information** - Relevant excerpts for the query
3. **Related docs** - Other documents that may be useful

## Examples

**Search internal docs before implementing auth feature:**
> /read-docs auth

Searches `docs/` filenames and contents for auth-related documentation. Finds `docs/auth.md` and references in `docs/architecture.md`, then summarizes relevant patterns, token handling conventions, and any documented gotchas before you start coding.

**Check for documented gotchas before refactor:**
> /read-docs database migration

Searches for migration-related docs and surfaces any documented pitfalls, required steps, or past issues logged in `docs/log/`. Presents key findings so you can avoid known problems during the refactor.

## Troubleshooting

### No docs/ folder found in project
**Solution:** Fall back to searching root-level `.md` files (README.md, CLAUDE.md, CONTRIBUTING.md). If the project has no documentation at all, use `research-tech` for external references or check inline code comments via Grep for conventions.

### Documentation is stale or contradicts code
**Solution:** Trust the code over the documentation when they conflict. Note the discrepancy in your response so the user can update the docs, and verify behavior by reading the actual source files rather than relying on the outdated documentation.

## Notes

- This skill is for internal project docs, not external library docs
- For external library documentation, use `research-tech`
- If no docs/ folder exists, search root .md files only
