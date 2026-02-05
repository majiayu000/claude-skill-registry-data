---
name: repo-explore
description: Clone and explore external GitHub repositories to understand how libraries, frameworks, or dependencies work. Use when user provides a GitHub URL (github.com/owner/repo), asks "how does X library work", wants to look at source code for a dependency, asks about implementation details of an external package, or says "explore", "look at", or "check out" a repository. Automatically checks out the matching version tag when the repo is a dependency in the current project.
---

# Repo Explore Skill

Explore external GitHub repositories by cloning them locally and using the Explore agent for comprehensive codebase analysis.

## Cache Location

```
~/.cache/claude/repos/<owner>/<repo>/
```

## Workflow

### 1. Parse Repository URL

Extract owner and repo from various formats:
- `https://github.com/owner/repo`
- `git@github.com:owner/repo.git`
- `owner/repo` (shorthand)
- `github.com/owner/repo`

### 2. Check Cache

```bash
ls ~/.cache/claude/repos/<owner>/<repo>/
```

- **If exists**: Check if update needed (see `update-reference.md`)
- **If not exists**: Proceed to clone

### 3. Clone Repository

```bash
mkdir -p ~/.cache/claude/repos/<owner>
git clone https://github.com/<owner>/<repo>.git ~/.cache/claude/repos/<owner>/<repo>
```

### 4. Version Detection (CRITICAL)

**Before exploring, check if this repo is a dependency in the current working directory.**

Consult `version-detection.md` for:
- Which dependency files to check
- How to extract versions from each format
- How to map versions to git tags

If a matching version is found:
```bash
cd ~/.cache/claude/repos/<owner>/<repo>
git fetch --all --tags
git checkout <tag>
```

Common tag formats to try:
- `v1.2.3`
- `1.2.3`
- `release-1.2.3`
- `release/1.2.3`

### 5. Explore with Explore Agent

**ALWAYS use the Task tool with `subagent_type=Explore` for answering questions about the repository.**

Do NOT manually browse files when the Explore agent can do it. The Explore agent is optimized for:
- Finding files by patterns
- Searching code for keywords
- Understanding codebase architecture
- Answering questions about how code works

Example:
```
Task(
  subagent_type="Explore",
  prompt="""In ~/.cache/claude/repos/owner/repo/, find how authentication is implemented.

Requirements for your response:
- Include code snippets with file paths and line numbers
- Show key type definitions and function signatures
- End with a 'Key Files for Further Exploration' table with columns: File, Purpose, Start Here If...
"""
)
```

### 6. Response Format Requirements

**When answering questions about the repository, responses MUST include:**

#### Code Snippets
- Include relevant code snippets that directly support the answer
- Show actual type definitions, function signatures, and key logic
- Use proper syntax highlighting with language identifier
- Include file path and line numbers for each snippet:
  ```go
  // File: pkg/controller/foo.go:42-58
  func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
      // ... relevant code
  }
  ```

#### File Recommendations for Further Reading
At the end of every response, include a **"Key Files for Further Exploration"** section:

```markdown
## Key Files for Further Exploration

| File | Purpose | Start Here If... |
|------|---------|------------------|
| `pkg/apis/v1/types.go` | Core type definitions | You want to understand the data model |
| `pkg/controller/main_controller.go` | Main reconciliation logic | You want to understand the control flow |
| `docs/design.md` | Architecture decisions | You want high-level understanding |
```

**Guidelines for file recommendations:**
- Prioritize files by relevance to the question asked
- Include 3-7 files (not too few, not overwhelming)
- Add context on WHY each file is useful
- Include "Start Here If..." guidance to help with future exploration
- Order from most fundamental to most specific

#### Response Structure Template
```
1. Brief answer summary (2-3 sentences)
2. Detailed explanation with inline code snippets
3. Architecture/flow diagrams if helpful (ASCII or description)
4. Key Files for Further Exploration table
5. Optional: Related topics the user might want to explore next
```

### 7. Updates

For refreshing the repository or switching versions, consult `update-reference.md`.

## Important Notes

- Always verify the checkout succeeded before exploring
- If the user asks about a specific version, checkout that version even if not a dependency
- For private repos, the clone will work if the user has git credentials configured
- Large repos may take time to clone; inform the user
