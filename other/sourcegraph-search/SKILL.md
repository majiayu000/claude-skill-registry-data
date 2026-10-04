---
name: sourcegraph-search
description: Search codebases across repositories using Sourcegraph MCP integration — code search, commit history, diffs, symbol navigation, and DeepSearch. Use when a question spans many repositories and a Sourcegraph MCP server is configured.
---

# Sourcegraph Cross-Repo Search

You are a senior engineer helping the user search your company's codebase using
the Sourcegraph MCP server integration. You have access to a private
Sourcegraph instance and can search across all indexed repositories.

---

## TOKEN & COST WARNING

> **STOP AND READ BEFORE PROCEEDING.**
>
> Sourcegraph queries — especially broad cross-repo searches — consume a **large
> number of tokens**. A single exploratory session can burn through a significant
> portion of your daily/monthly Claude Code budget.
>
> **Before running any Sourcegraph query, consider:**
>
> 1. **Do you actually need cross-repo search?** If you're looking in a single
>    repo you already have cloned, use local tools (`Grep`, `Glob`, `Read`)
>    instead — they're free.
> 2. **Can Sourcegraph DeepSearch do this better?** For complex research
>    questions, open DeepSearch directly in your browser at
>    `https://<YOUR_INSTANCE>.sourcegraphcloud.com` and run the query there. It's
>    purpose-built for deep exploration and won't cost Claude Code tokens.
> 3. **Scope your queries tightly.** Always use `repo:` and `file:` filters.
>    Never run unscoped searches across all repositories.
> 4. **Set low result counts.** Use `count` parameters (e.g., `count: 10`) to
>    limit results. You can always fetch more if needed.
>
> If the user asks for a broad or exploratory Sourcegraph task, **warn them**
> about token cost and suggest DeepSearch as an alternative before proceeding.

---

## Prerequisites — MCP Server Setup

The Sourcegraph MCP server must be configured in Claude Code before these tools
will work. If the tools are not available, guide the user through setup.

### Check if Already Configured

```bash
claude mcp list
```

Look for `sourcegraph` in the output. If present, you're good to go.

### Add the Sourcegraph MCP Server

```bash
claude mcp add sourcegraph --scope user --transport http \
  https://<YOUR_INSTANCE>.sourcegraphcloud.com/.api/mcp/v1 \
  --header "Authorization: token {TOKEN}"
```

Replace `<YOUR_INSTANCE>` with your Sourcegraph instance subdomain and `{TOKEN}` with a personal access token.

**To get a token:**
1. Go to `https://<YOUR_INSTANCE>.sourcegraphcloud.com`
2. Sign in with your credentials
3. Navigate to **Settings > Access tokens**
4. Create a new token and copy it

### (Optional) Add the Public Sourcegraph MCP Server

For searching open-source repositories on sourcegraph.com:

```bash
claude mcp add sourcegraph-opensource --scope user --transport http \
  https://sourcegraph.com/.api/mcp/v1
```

No token is required for public repositories.

### Verify

After adding, restart Claude Code and confirm the tools are available:

```bash
claude mcp list
```

You should see `sourcegraph` listed with its HTTP transport URL.

---

## Available Tools

Once the MCP server is configured, the following tools are available. All tool
names are prefixed with `mcp__sourcegraph__`.

### Code Search

| Tool | Use For |
|------|---------|
| `sg_keyword_search` | Exact keyword/literal code search with `repo:`, `file:`, `rev:` filters. Best for known identifiers. |
| `sg_nls_search` | Semantic/natural-language code search. Best for conceptual queries when you don't know exact names. |

### Repository & File Navigation

| Tool | Use For |
|------|---------|
| `sg_list_repos` | Find repositories by name substring. Use to resolve full repo paths. |
| `sg_list_files` | List files and directories within a repo. Use to explore repo structure. |
| `sg_read_file` | Read file contents from a repo. Supports line ranges and specific revisions/branches. |

### Symbol Navigation

| Tool | Use For |
|------|---------|
| `sg_go_to_definition` | Jump to where a symbol (function, class, variable) is defined. |
| `sg_find_references` | Find all usages of a symbol across the codebase. Great for impact analysis. |

### Git History & Diffs

| Tool | Use For |
|------|---------|
| `sg_commit_search` | Search commits by message, author, content, file path, or date range. |
| `sg_diff_search` | Search actual code changes (added/removed lines) across repos. |
| `sg_compare_revisions` | Compare two revisions (branches, tags, commits) in a single repo. |

### People

| Tool | Use For |
|------|---------|
| `sg_get_contributor_repos` | Find which repos a person has contributed to. Good for scoping follow-up searches. |

### DeepSearch

| Tool | Use For |
|------|---------|
| `sg_deepsearch_read` | Read results from a Sourcegraph DeepSearch conversation by URL or token. |

---

## Workflow

### Step 0: Confirm Access

Before running any query, verify the MCP server is available by checking that
the `mcp__sourcegraph__*` tools exist. If they don't, walk the user through
the setup steps above.

### Step 1: Understand the Query

Ask the user what they're looking for. Classify it:

- **Known identifier** (function name, class, config key) -> `sg_keyword_search`
- **Conceptual/exploratory** ("how does auth work", "logging setup") -> `sg_nls_search`
- **Who changed what** -> `sg_commit_search` or `sg_diff_search`
- **Repo discovery** ("do we have a repo for X") -> `sg_list_repos`
- **Impact analysis** ("who uses this function") -> `sg_find_references`
- **Deep research** -> Suggest DeepSearch in the browser first

### Step 2: Scope the Query

Always narrow before searching:

1. **Resolve the repo name** with `sg_list_repos` if needed
2. **Add `repo:` filters** to keyword/NLS searches
3. **Add `file:` filters** if you know the file type or directory
4. **Set result limits** — start small, expand if needed

### Step 3: Execute and Summarize

Run the query, then present results as a concise summary:

- File paths and line numbers for code hits
- Relevant code snippets (don't dump entire files)
- For commit searches: author, date, message, and changed files
- Link back to Sourcegraph URLs when possible

### Step 4: Follow Up

If the user wants to go deeper:

- Use `sg_read_file` to read specific files found in search results
- Use `sg_go_to_definition` to trace symbols
- Use `sg_find_references` for impact analysis
- Suggest DeepSearch for truly open-ended exploration

---

## Tips

- **Repo naming conventions:** Most repos are on GitLab at paths like
  `gitlab.example.com/your-org/<repo-name>`. Use `sg_list_repos` to confirm.
- **Branch searches:** Use `rev:` filter with `repo:` to search specific branches.
  Default is HEAD of the default branch.
- **Regex in keyword search:** Supported in `file:` and `repo:` filters. Use `^`
  and `$` anchors for exact repo matches.
- **Large files:** `sg_read_file` has a 128 KB limit. Use `startLine`/`endLine`
  for large files.

---

**Last Updated:** February 25, 2026
