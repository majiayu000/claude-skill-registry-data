---
name: skill-catholic-liturgy-tool
description: Catholic liturgical CLI tool
---

# When to use

- When you need daily liturgical information (readings, celebrations, colors)
- When you need to look up Catechism of the Catholic Church paragraphs
- When you need rosary prayers and mysteries for a specific day
- When you need liturgical data for a specific date
- When you need JSON output for scripting or automation

# catholic-liturgy-tool Skill

## Purpose

This skill provides access to the `catholic-liturgy-tool` CLI for Catholic liturgical calendar data, daily readings, rosary prayers, and Catechism access.

## When to Use This Skill

**Use this skill when:**
- Looking up today's or a specific date's liturgical information
- Searching or looking up Catechism (CCC) paragraphs
- Getting rosary prayers and mysteries
- Automating liturgical data retrieval with JSON output

**Do NOT use this skill for:**
- Tasks unrelated to Catholic liturgy
- Quick syntax lookups (use slash commands instead)

## CLI Tool: catholic-liturgy-tool

A command-line interface for Catholic liturgical information.

### Installation

```bash
# Clone and install
git clone https://github.com/dnvriend/catholic-liturgy-tool.git
cd catholic-liturgy-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Start

```bash
# Today's liturgy
catholic-liturgy-tool

# Specific date
catholic-liturgy-tool date 2025-12-25

# Catechism lookup
catholic-liturgy-tool ccc 2559

# Today's rosary
catholic-liturgy-tool rosary
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### today - Today's Liturgical Information

Display liturgical color, celebration, readings, saints, and rosary mysteries.

**Usage:**
```bash
catholic-liturgy-tool today [OPTIONS]
```

**Options:**
- `--json` - Output JSON (pipe to jq for processing)
- `--full-text, -t` - Include full scripture texts
- `--detail, -d` - Include explanations for colors, seasons, ranks
- `--no-cache` - Bypass cache, fetch fresh data
- `--no-color` - Disable ANSI color codes
- `-v/-vv/-vvv` - Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
catholic-liturgy-tool today              # Human-readable output
catholic-liturgy-tool today --json       # JSON for scripting
catholic-liturgy-tool today -t           # Include full texts
catholic-liturgy-tool today --json | jq '.readings'
```

---

### date - Specific Date Lookup

Display liturgical information for a specific date.

**Usage:**
```bash
catholic-liturgy-tool date DATE [OPTIONS]
```

**Arguments:**
- `DATE` - ISO format date (YYYY-MM-DD)

**Examples:**
```bash
catholic-liturgy-tool date 2025-12-25    # Christmas
catholic-liturgy-tool date 2025-04-20    # Easter
catholic-liturgy-tool date 2025-11-01 --json | jq '.celebration'
```

---

### ccc - Catechism Lookup

Look up Catechism of the Catholic Church paragraphs by number, range, or keyword.

**Usage:**
```bash
catholic-liturgy-tool ccc [REFERENCE] [OPTIONS]
```

**Arguments/Options:**
- `REFERENCE` - Paragraph number (2559) or range (2559-2561)
- `--search, -s` - Search keyword in CCC text
- `--limit, -l` - Max search results [default: 10]
- `--json` - Output JSON

**Examples:**
```bash
catholic-liturgy-tool ccc 2559           # Single paragraph
catholic-liturgy-tool ccc 2559-2565      # Paragraph range
catholic-liturgy-tool ccc -s "prayer"    # Search for keyword
catholic-liturgy-tool ccc -s "trinity" --json | jq '.[0].text'
```

---

### rosary - Rosary Prayers and Mysteries

Show complete rosary guide with prayers and mysteries.

**Usage:**
```bash
catholic-liturgy-tool rosary [OPTIONS]
```

**Options:**
- `--day` - Weekday: monday|tuesday|...|sunday
- `--mystery, -m` - Mystery: joyful|sorrowful|glorious|luminous
- `--prayers, -p` - Show prayers only, omit mysteries
- `--json` - Output JSON

**Examples:**
```bash
catholic-liturgy-tool rosary                # Today's mysteries
catholic-liturgy-tool rosary --day monday   # Joyful (Monday)
catholic-liturgy-tool rosary -m sorrowful   # Sorrowful mysteries
catholic-liturgy-tool rosary -p             # Prayers only
catholic-liturgy-tool rosary --json | jq '.mysteries'
```

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. Logs output to stderr.

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info | Development |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
catholic-liturgy-tool today -v     # INFO level
catholic-liturgy-tool today -vv    # DEBUG level
catholic-liturgy-tool today -vvv   # TRACE level
```

---

### Shell Completion

Native shell completion for bash, zsh, and fish.

**Installation:**
```bash
# Bash (add to ~/.bashrc)
eval "$(catholic-liturgy-tool completion generate bash)"

# Zsh (add to ~/.zshrc)
eval "$(catholic-liturgy-tool completion generate zsh)"

# Fish
catholic-liturgy-tool completion generate fish > \
    ~/.config/fish/completions/catholic-liturgy-tool.fish
```

---

### Pipeline Composition

Compose commands with Unix pipes for workflows.

**Examples:**
```bash
# Extract liturgical color
catholic-liturgy-tool today --json | jq -r '.celebration.color'

# Get gospel reference
catholic-liturgy-tool today --json | jq -r '.readings.gospel'

# List all CCC paragraphs about prayer
catholic-liturgy-tool ccc -s "prayer" --json | jq '.[].number'

# Get first mystery name
catholic-liturgy-tool rosary --json | jq '.mysteries[0].title'
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Command not found**
```bash
# Verify installation
catholic-liturgy-tool --version

# Reinstall if needed
cd catholic-liturgy-tool
uv tool install . --reinstall
```

**Issue: Cache stale data**
```bash
# Bypass cache
catholic-liturgy-tool today --no-cache
```

**Issue: API errors**
```bash
# Enable verbose logging to see details
catholic-liturgy-tool today -vv
```

### Getting Help

```bash
# Show help
catholic-liturgy-tool --help

# Command-specific help
catholic-liturgy-tool today --help
catholic-liturgy-tool ccc --help
catholic-liturgy-tool rosary --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments, validation failed)
- `2`: Server error (API error, network issue)

## Output Formats

**Default Output:**
- Human-readable formatted output with optional colors
- Varies by command

**JSON Output (`--json` flag):**
- Machine-readable structured data
- Perfect for pipelines and scripting
- Available on all commands

## Best Practices

1. **Use verbosity progressively**: Start with `-v`, increase to `-vv`/`-vvv` only if needed
2. **Leverage JSON output**: Use `--json | jq` for scripting and automation
3. **Install shell completion**: Better CLI experience with tab completion
4. **Use cache wisely**: Default caching improves performance; use `--no-cache` when needed

## Resources

- **GitHub**: https://github.com/dnvriend/catholic-liturgy-tool
- **PyPI**: https://pypi.org/project/catholic-liturgy-tool/
