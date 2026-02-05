---
name: skill-aws-knowledge-tool
description: CLI tool for querying AWS Knowledge MCP Server
---

# When to use
- When you need to search AWS documentation programmatically
- When you need to read and convert AWS docs to markdown
- When you need to discover related AWS documentation

# AWS Knowledge Tool Skill

## Purpose

This skill provides access to the `aws-knowledge-tool` CLI - a command-line interface for querying the AWS Knowledge MCP Server. Use it to search, read, and discover AWS documentation programmatically.

## When to Use This Skill

**Use this skill when:**
- You need to search AWS documentation with full-text search
- You need to read AWS documentation pages as markdown
- You need to discover related documentation recommendations
- You need structured/JSON output for processing

**Do NOT use this skill for:**
- Writing new AWS documentation (read-only)
- Deploying AWS resources (documentation only)
- AWS CLI operations (use AWS CLI instead)

## CLI Tool: aws-knowledge-tool

The `aws-knowledge-tool` is a CLI tool for querying the AWS Knowledge MCP Server to search, read, and discover AWS documentation.

### Installation

```bash
# Clone and install
git clone https://github.com/dnvriend/aws-knowledge-tool.git
cd aws-knowledge-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Start

```bash
# Search AWS documentation
aws-knowledge-tool search "Lambda function URLs"

# Read documentation page
aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# Get recommendations
aws-knowledge-tool recommend "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### search - Search AWS Documentation

Search across AWS documentation, blogs, solutions library, architecture center, and prescriptive guidance.

**Usage:**
```bash
aws-knowledge-tool search QUERY [OPTIONS]
```

**Arguments:**
- `QUERY`: Search query text (required)
- `--limit N` / `-l N`: Maximum results (default: 10)
- `--offset M` / `-o M`: Skip first M results for pagination (default: 0)
- `--json`: Output JSON format for processing
- `--stdin`: Read query from stdin (for pipelines)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Basic search
aws-knowledge-tool search "S3 versioning"

# With pagination
aws-knowledge-tool search "Lambda" --limit 10 --offset 20

# JSON output
aws-knowledge-tool search "DynamoDB" --json

# Pipeline usage
echo "CloudFormation" | aws-knowledge-tool search --stdin --json
```

**Output:**
Returns list of results with: `title`, `url`, `context`, `rank_order`

---

### read - Read AWS Documentation

Fetch and convert AWS documentation pages to markdown format.

**Usage:**
```bash
aws-knowledge-tool read URL [OPTIONS]
```

**Arguments:**
- `URL`: AWS documentation URL (required)
- `--start-index N` / `-s N`: Starting character index for pagination
- `--max-length M` / `-m M`: Maximum characters to fetch
- `--json`: Output JSON format
- `--stdin`: Read URL from stdin
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Read full document
aws-knowledge-tool read "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# With pagination (large docs)
aws-knowledge-tool read "https://docs.aws.amazon.com/..." \
  --start-index 5000 --max-length 2000

# Pipeline from search
aws-knowledge-tool search "Lambda" --json | \
  jq -r '.[0].url' | \
  aws-knowledge-tool read --stdin
```

**Output:**
Returns markdown-formatted documentation content.

**Supported domains:**
- `docs.aws.amazon.com`
- `aws.amazon.com`

---

### recommend - Get Documentation Recommendations

Discover related documentation through four recommendation types.

**Usage:**
```bash
aws-knowledge-tool recommend URL [OPTIONS]
```

**Arguments:**
- `URL`: AWS documentation URL (required)
- `--type TYPE` / `-t TYPE`: Filter by recommendation type
  - `highly_rated`: Popular pages within same AWS service
  - `new`: Recently added pages (useful for finding new features)
  - `similar`: Pages covering similar topics
  - `journey`: Pages commonly viewed next by other users
- `--limit N` / `-l N`: Max results per category (default: 5)
- `--offset M` / `-o M`: Skip first M per category (default: 0)
- `--json`: Output JSON format
- `--stdin`: Read URL from stdin
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Get all recommendations
aws-knowledge-tool recommend "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"

# Filter by type (find new features)
aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --type new

# JSON output with limit
aws-knowledge-tool recommend "https://docs.aws.amazon.com/..." --json --limit 3

# Pipeline usage
aws-knowledge-tool search "Lambda" --json | \
  jq -r '.[0].url' | \
  aws-knowledge-tool recommend --stdin --type similar
```

**Output:**
Returns dict with recommendation categories and their pages (title, url, context).

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. All logs output to stderr.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
# INFO level - see operations
aws-knowledge-tool search "Lambda" -v

# DEBUG level - see detailed info
aws-knowledge-tool search "Lambda" -vv

# TRACE level - see all internals
aws-knowledge-tool search "Lambda" -vvv
```

---

### Shell Completion

Native shell completion for bash, zsh, and fish.

**Installation:**
```bash
# Bash (add to ~/.bashrc)
eval "$(aws-knowledge-tool completion bash)"

# Zsh (add to ~/.zshrc)
eval "$(aws-knowledge-tool completion zsh)"

# Fish (save to completions)
aws-knowledge-tool completion fish > ~/.config/fish/completions/aws-knowledge-tool.fish
```

---

### Pipeline Composition

Compose commands with Unix pipes for powerful workflows.

**Examples:**
```bash
# Search → Extract URL → Read
aws-knowledge-tool search "Lambda" --json | \
  jq -r '.[0].url' | \
  aws-knowledge-tool read --stdin

# Search → Extract URL → Get similar docs
aws-knowledge-tool search "S3" --json | \
  jq -r '.[0].url' | \
  aws-knowledge-tool recommend --stdin --type similar

# Save search results to file
aws-knowledge-tool search "DynamoDB" --json > results.json

# Read and save as markdown
aws-knowledge-tool read "https://docs.aws.amazon.com/..." > lambda-docs.md
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Command not found**
```bash
# Verify installation
aws-knowledge-tool --version

# Reinstall if needed
cd aws-knowledge-tool
uv tool install . --reinstall
```

**Issue: No results from search**
- Check your search query is specific enough
- Try broader search terms
- Use `--json` to see full response

**Issue: URL validation error**
- Ensure URL is from `docs.aws.amazon.com` or `aws.amazon.com`
- Check URL is accessible in browser first

**Issue: Connection timeout**
- Check internet connection
- AWS Knowledge MCP Server may be temporarily unavailable
- Try again with verbose flag: `-vv`

### Getting Help

```bash
# Show help
aws-knowledge-tool --help

# Command-specific help
aws-knowledge-tool search --help
aws-knowledge-tool read --help
aws-knowledge-tool recommend --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments, validation failed)
- `2`: Server error (API error, network issue)
- `3`: Network error (connection failed, timeout)

## Output Formats

**Default (Markdown):**
- Human-readable formatted output
- Search: ranked list with titles, URLs, context
- Read: markdown content
- Recommend: grouped by category with titles, URLs

**JSON (`--json` flag):**
- Machine-readable structured data
- Perfect for pipelines and processing
- Consistent structure across commands

## Best Practices

1. **Use JSON for pipelines**: Enable `--json` when piping to other tools
2. **Pagination for large results**: Use `--limit` and `--offset` for controlled fetching
3. **Progressive verbosity**: Start with `-v`, increase to `-vv`/`-vvv` only if needed
4. **Save frequent searches**: Cache JSON results to avoid repeated API calls
5. **Compose commands**: Leverage Unix pipes for powerful workflows

## Resources

- **GitHub**: https://github.com/dnvriend/aws-knowledge-tool
- **AWS Knowledge MCP Server**: https://knowledge-mcp.global.api.aws
- **MCP Specification**: https://modelcontextprotocol.io
