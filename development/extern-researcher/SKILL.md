---
name: extern-researcher
description: |
  Research external open-source repositories to learn patterns and implementations.
  This skill should be used when agents need to study external codebases, check for
  existing research before cloning, manage temporary workspaces, and persist findings
  to the global thoughts system. Triggers include: studying external repos, learning
  from open source, cloning for pattern research, or checking what has been researched.
---

# Extern Researcher

## Overview

Enable agents to efficiently study external open-source repositories by leveraging existing
research first, using temporary workspaces for clones, and persisting findings to the global
thoughts system.

## When to Use

- When needing to study patterns or implementations from external repositories
- When checking if a repository has already been researched
- When cloning an external repo for temporary study
- When persisting research findings about external code
- When cleaning up temporary workspace after research is complete

## Key Concepts

### Research-Centric Model

The catalog tracks **research studies**, not cloned repositories. Clones are temporary
workspaces; research is the persistent artifact.

### Directory Structure

```
thoughts/global/extern/           # Persistent research storage
├── catalog.md                    # Global research catalog (markdown + YAML frontmatter)
└── repos/{org-repo}/             # Research documents per repository

{any-project}/.extern/            # Temporary workspace (disposable)
└── {org-repo}/                   # Cloned repos for study
```

### Catalog Format

The catalog at `thoughts/global/extern/catalog.md` uses markdown with YAML frontmatter:

```yaml
---
type: extern-research-catalog
version: 1.0
last_updated: YYYY-MM-DD
total_repos_studied: N
total_studies: N

repos:
  - name: "org/repo"
    url: "https://github.com/org/repo"
    first_studied: "YYYY-MM-DD"
    study_count: N
    topics: ["topic1", "topic2"]
---
```

## Scripts

Execute via justfile or directly with uv:

### Via Justfile (Recommended)

```bash
just -f {base_dir}/justfile <recipe> [args...]
```

| Recipe | Arguments | Description |
|--------|-----------|-------------|
| `list` | | List all research in catalog |
| `search` | `term` | Search catalog by repo or topic |
| `stats` | | Show catalog statistics |
| `add-study` | `repo url topic document context` | Add a new study to catalog |

### Direct Execution

```bash
uv run {base_dir}/scripts/catalog.py <command> [args...]
```

| Command | Arguments | Description |
|---------|-----------|-------------|
| `list` | | List all research studies |
| `search` | `<term>` | Search by repo name or topic |
| `stats` | | Show catalog statistics |
| `add-study` | `--repo --url --topic --document --context` | Add new study |

## Core Workflow

### Phase 1: Discovery (ALWAYS FIRST)

Before cloning any repository:

1. **Read the global catalog**: `thoughts/global/extern/catalog.md`
2. **Search for the repo** by name, URL, or topic
3. **If found**:
   - Read existing research documents
   - Evaluate: Is this sufficient for current needs?
   - If YES: Use existing research, skip cloning
   - If NO: Proceed to Phase 2, noting what gaps exist
4. **If not found**: Proceed to Phase 2

### Phase 2: Workspace Initialization

If cloning is needed:

1. **Check if `.extern/` exists** in current project
2. **If not, create it**:
   ```bash
   mkdir -p .extern
   ```
3. **MUST copy AGENTS.md template** to workspace:
   ```bash
   cp {base_dir}/assets/workspace-agents.md .extern/AGENTS.md
   ```
   This provides agent guidance for future sessions working in this directory.
4. **Ensure .gitignore** includes `.extern/`

### Phase 3: Clone Repository

1. **Parse the input** (URL, clone command, org/repo format)
2. **Derive directory name**: `{org}-{repo}` (lowercase, kebab-case)
   - `https://github.com/facebook/react` → `facebook-react`
   - `https://github.com/vercel/next.js` → `vercel-next-js`
3. **Clone with shallow depth** (unless full history needed):
   ```bash
   git clone --single-branch --depth 1 {url} .extern/{org-repo}/
   ```
4. **Verify success**

### Phase 4: Research

1. **Focus on the specific question/topic**
2. **Use appropriate subagents**:
   - `codebase-pattern-finder` - Find implementations, usage examples
   - `codebase-analyzer` - Deep dive on specific components
   - `codebase-locator` - Find files by purpose/feature
3. **Document findings** with file:line references
4. **Note connections** to current project needs

### Phase 5: Persist Research

1. **Create research document**:
   - Location: `thoughts/global/extern/repos/{org-repo}/`
   - Filename: `{YYYY-MM-DD}_{topic-slug}.md`
   - Use the research document template below

2. **MUST update global catalog using the script** (not manual file edits):
   ```bash
   just -f {base_dir}/justfile add-study \
     "org/repo" \
     "https://github.com/org/repo" \
     "Topic studied" \
     "repos/org-repo/YYYY-MM-DD_topic.md" \
     "Why this was studied"
   ```
   The script ensures consistent catalog formatting and validates entries.

3. **Sync thoughts** if configured:
   ```bash
   thoughts sync
   ```

### Phase 6: Cleanup (Optional)

When workspace is no longer needed:

1. **Confirm with user** before deletion
2. **Remove .extern/ directory**:
   ```bash
   rm -rf .extern/
   ```
3. **Research remains** in thoughts/global/extern/

## Research Document Template

When creating research documents, use this structure:

```markdown
---
date: {ISO timestamp}
repo: "{org}/{repo}"
url: "{full URL}"
topic: "{research topic}"
context: "{why this was studied}"
project: "{project that prompted this}"
tags: [extern-research, {domain-tags}]
---

# {Topic}: {Repo Name}

## Research Question

{What we set out to learn}

## Key Findings

### Finding 1: {Title}

{Description with code examples and file:line references}

### Finding 2: {Title}

{...}

## Applicable Patterns

{How these findings could apply to our work}

## References

- `{file}:{line}` - {description}
```

## Suitable Subagents

| Agent | Use Case |
|-------|----------|
| `codebase-pattern-finder` | Find implementations, usage examples |
| `codebase-analyzer` | Deep dive on specific components |
| `codebase-locator` | Find files by purpose/feature |
| `web-search-researcher` | Additional context about the project |

## Important Constraints

1. **ALWAYS check catalog first** - Never clone without checking existing research
2. **Workspace is temporary** - Do not store valuable data in .extern/
3. **Research is permanent** - Always persist to thoughts/global/extern/
4. **Update catalog** - Every study must update the global catalog
5. **Respect clone depth** - Use shallow clones unless full history needed
6. **Use org-repo naming** - Include organization to avoid conflicts

## Error Handling

- **Catalog not found** → Create initial catalog at `thoughts/global/extern/catalog.md`
- **Clone fails** → Check URL format, network, permissions; report to user
- **Research exists but stale** → Proceed with new research, reference existing findings
- **Workspace already exists** → Reuse existing .extern/, check if repo is already cloned
