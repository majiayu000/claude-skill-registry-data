---
name: "crawl"
description: "Deep web crawling using hakrawler and gospider for subdomain discovery, endpoint extraction, and JavaScript analysis. Use this skill when users request to crawl URLs, discover subdomains, extract endpoints, map web applications, or perform reconnaissance tasks. All outputs (categorized results, b..."
---

# Crawl

*Sourced from security-talent-bugskill-ai*

# Web Crawling Skill

## Overview

This skill enables deep web crawling using hakrawler and gospider to discover subdomains, extract endpoints, analyze JavaScript files, and map web application attack surfaces. The skill provides a unified Python wrapper that combines both tools for comprehensive URL discovery and categorization. All bash command outputs (stdout/stderr) are automatically logged for debugging and analysis.

## When to Use This Skill

Use this skill when users request:
- Crawling or spidering a URL or domain
- Subdomain discovery and enumeration
- Endpoint and API discovery
- JavaScript file extraction and analysis
- Web application reconnaissance or mapping
- Bug bounty scoping and enumeration
- Attack surface discovery

**Trigger keywords:** crawl, spider, enumerate, discover subdomains, find endpoints, map application, recon, reconnaissance

## Quick Start

The primary tool is `scripts/crawl.py`, which provides a unified interface to both hakrawler and gospider:

```bash
# Basic crawl - creates crawl_example.com_TIMESTAMP/
python scripts/crawl.py https://example.com

# Deep crawl with subdomain discovery
python scripts/crawl.py https://example.com --depth 3 --subdomains

# Crawl with JS analysis
python scripts/crawl.py https://example.com --js-analysis

# Use only one tool
python scripts/crawl.py https://example.com --tool hakrawler

# Custom output directory and timeout
python scripts/crawl.py https://example.com --output-dir ./results --timeout 600
```

**Note:** The script automatically creates timestamped output directories following the pattern `crawl_{DOMAIN}_{timestamp}/` unless a custom output directory is specified.

## Tool Installation

If the crawling tools are not installed, use the installation helper:

```bash
bash scripts/install_tools.sh
```

Or install manually:
```bash
go install github.com/hakluke/hakrawler@latest
go install github.com/jaeles-project/gospider@latest
export PATH=$PATH:~/go/bin
```

Verify with: `python scripts/crawl.py --install`

## Workflow

### 1. Initial Setup

Before crawling, ensure tools are installed:

```bash
# Check if tools are installed
hakrawler -h && gospider -h

# If not, run the installer
bash scripts/install_tools.sh
```

### 2. Execute Crawl

Run the crawl script with appropriate options based on user requirements:

```python
# For subdomain discovery
python scripts/crawl.py https://example.com --subdomains --depth 2

# For comprehensive endpoint discovery
python scripts/crawl.py https://example.com --depth 3 --js-analysis

# For quick reconnaissance
python scripts/crawl.py https://example.com --tool hakrawler --depth 1
```

### 3. Process Results

The script automatically categorizes and saves results to an organized directory structure:

**Output structure:**
```
crawl_{DOMAIN}_{timestamp}/
├── results/              # Categorized URL lists
│   ├── urls.txt         # All discovered URLs
│   ├── subdomains.txt   # Unique subdomains
│   ├── js_files.txt     # JavaScript files
│   ├── api_endpoints.txt # API endpoints
│   ├── parameters.txt   # URL parameters
│   └── extensions.json  # URLs grouped by file extension
├── logs/                # Bash command logs (stdout/stderr)
│   ├── hakrawler.log   # hakrawler execution log
│   └── gospider.log    # gospider execution log
├── summary.json         # Comprehensive JSON summary
└── REPORT.md           # Human-readable markdown report
```

### 4. Analyze Results

After crawling, analyze the results based on the user's goals:

```bash
# Read summary
cat crawl_example.com_*/summary.json

# Review markdown report
cat crawl_example.com_*/REPORT.md

# Review subdomains
cat crawl_example.com_*/results/subdomains.txt

# Check for interesting endpoints
grep -i "admin\|api\|login\|upload" crawl_example.com_*/results/urls.txt

# Find JavaScript files for further analysis
cat crawl_example.com_*/results/js_files.txt

# Check bash command logs if needed
cat crawl_example.com_*/logs/hakrawler.log
cat crawl_example.com_*/logs/gospider.log
```

## Use Cases

### Subdomain Discovery

When users want to discover subdomains:

```bash
python scripts/crawl.py https://example.com --subdomains --depth 2
```

Then read the `results/subdomains.txt` file from the output directory to provide the list of discovered subdomains, or review the REPORT.md for a formatted overview.

### Endpoint Extraction

When users need to extract all endpoints:

```bash
python scripts/crawl.py https://example.com --depth 3 --js-analysis
```

The script will identify and categorize:
- API endpoints (paths containing /api/, /v1/, /graphql, etc.)
- Regular web pages
- Static resources
- Parameters for further testing

### JavaScript Analysis

When users want to find JavaScript files for secret extraction or endpoint discovery:

```bash
python scripts/crawl.py https://example.com --js-analysis
```

The `results/js_files.txt` output can be passed to other tools like:
- jsluice (use the jsluice skill for deep JS analysis)
- SecretFinder
- LinkFinder

Example integration with jsluice skill:
```bash
# After crawling, feed JS files to jsluice
python3 ~/.claude/skills/jsluice/scripts/batch_analyze.py example.com --urls-file crawl_example.com_*/results/js_files.txt
```

### Bug Bounty Reconnaissance

For comprehensive bug bounty reconnaissance:

```bash
# Initial deep crawl with all options
python scripts/crawl.py https://target.com --subdomains --js-analysis --depth 3 --timeout 600
```

Then analyze the results to identify:
1. Interesting subdomains for further testing
2. API endpoints for authentication/authorization testing
3. JavaScript files for secret extraction
4. Parameters for injection testing

## Tool Comparison

### hakrawler
- **Strengths:** Fast, simple, good for quick enumeration
- **Best for:** Initial reconnaissance, quick scans
- **Limitations:** Less comprehensive than gospider

### gospider
- **Strengths:** More thorough, JSON output, better JS analysis
- **Best for:** Deep crawling, comprehensive mapping
- **Limitations:** Slower than hakrawler

**Default behavior:** Use both tools (`--tool both`) for comprehensive coverage.

## Advanced Usage

### Integration with Other Skills

This skill integrates well with other reconnaissance skills:

1. **After crawling, use jsluice skill** for JavaScript endpoint extraction:
   ```bash
   # Feed JS files to jsluice for deep analysis
   python3 ~/.claude/skills/jsluice/scripts/batch_analyze.py example.com \
     --urls-file crawl_example.com_*/results/js_files.txt
   ```

2. **Feed subdomains to subdomain takeover tools**
   ```bash
   cat crawl_example.com_*/results/subdomains.txt | subdomain-takeover-tool
   ```

3. **Pass API endpoints to authentication testing tools**
   ```bash
   cat crawl_example.com_*/results/api_endpoints.txt | api-testing-tool
   ```

4. **Use parameters list for injection testing**
   ```bash
   cat crawl_example.com_*/results/parameters.txt
   ```

### Custom Filtering

After crawling, apply custom filtering based on user needs:

```bash
# Find specific file types
grep "\.pdf$\|\.xlsx$\|\.docx$" crawl_example.com_*/results/urls.txt

# Find admin panels
grep -i "admin\|dashboard\|panel\|management" crawl_example.com_*/results/urls.txt

# Find upload functionality
grep -i "upload\|file" crawl_example.com_*/results/urls.txt

# Filter by extension using the extensions.json file
jq '.js' crawl_example.com_*/results/extensions.json
```

## Troubleshooting

### Tools Not Found

If crawl.py reports missing tools:
1. Run `scripts/install_tools.sh`
2. Verify `~/go/bin` is in PATH: `echo $PATH`
3. Add to PATH if needed: `export PATH=$PATH:~/go/bin`

### Timeout Issues

For large targets that timeout:
- Increase timeout: `--timeout 900`
- Reduce depth: `--depth 1`
- Use one tool: `--tool hakrawler`
- Crawl subdomains separately

### Permission Denied

Make scripts executable:
```bash
chmod +x scripts/crawl.py scripts/install_tools.sh
```

## Best Practices

1. **Start shallow, go deep:** Begin with depth 1-2, then increase if needed
2. **Use both tools:** Default `--tool both` provides best coverage
3. **Enable subdomain discovery** for comprehensive reconnaissance
4. **Review reports first:** Check `REPORT.md` for human-readable overview, then `summary.json` for detailed statistics
5. **Categorize findings:** Use the categorized output files in `results/` to prioritize testing
6. **Check bash logs:** If tools fail or produce unexpected results, review `logs/hakrawler.log` and `logs/gospider.log` for stdout/stderr
7. **Respect scope:** Only crawl targets within authorized scope
8. **Monitor resources:** Large crawls can be resource-intensive, use timeouts appropriately
9. **Combine with other tools:** Chain crawl results into specialized tools for deeper analysis (especially jsluice for JS files)
10. **Archive outputs:** Each crawl creates a timestamped directory - keep these for historical tracking and comparison

## Resources

### scripts/

- `crawl.py` - Main Python wrapper for hakrawler and gospider with:
  - Unified interface for both tools
  - Automatic bash command logging (stdout/stderr)
  - Result categorization and organization
  - Timestamped output directories
  - JSON summary and markdown report generation
- `install_tools.sh` - Bash script to install hakrawler and gospider via Go

### references/

- `tool_comparison.md` - Detailed comparison of hakrawler vs gospider features, performance, and use cases

## Output Directory Reference

Every crawl creates a structured output directory:

```
crawl_{DOMAIN}_{timestamp}/
├── results/              # Categorized results
│   ├── urls.txt         # All URLs found
│   ├── subdomains.txt   # Unique subdomains
│   ├── js_files.txt     # JavaScript files
│   ├── api_endpoints.txt # Detected API endpoints
│   ├── parameters.txt   # URL parameters
│   └── extensions.json  # URLs grouped by file extension
├── logs/                # Bash execution logs
│   ├── hakrawler.log   # Command, stdout, stderr, return code
│   └── gospider.log    # Command, stdout, stderr, return code
├── summary.json         # Complete crawl statistics and metadata
└── REPORT.md           # Human-readable markdown report
```

**Key features:**
- All bash commands are logged with full stdout/stderr for debugging
- Results are categorized for easy filtering and analysis
- Summary includes tool execution logs for transparency
- Markdown reports provide immediate insights
- Timestamped directories enable historical tracking

