---
name: semgrep
type: tool
description: >
  Semgrep is a fast static analysis tool for finding bugs and enforcing code standards.
  Use when scanning code for security issues or integrating into CI/CD pipelines.
---

# Semgrep

Semgrep is a highly efficient static analysis tool for finding low-complexity bugs and locating specific code patterns. Because of its ease of use, no need to build the code, multiple built-in rules, and convenient creation of custom rules, it is usually the first tool to run on an audited codebase. Furthermore, Semgrep's integration into the CI/CD pipeline makes it a good choice for ensuring code quality.

**Key benefits:**
- Prevents re-entry of known bugs and security vulnerabilities
- Enables large-scale code refactoring, such as upgrading deprecated APIs
- Easily added to CI/CD pipelines
- Custom Semgrep rules mimic the semantics of actual code
- Allows for secure scanning without sharing code with third parties
- Scanning usually takes minutes (not hours/days)
- Easy to use and accessible for both developers and security professionals

## When to Use

**Use Semgrep when:**
- Looking for bugs with easy-to-identify patterns
- Analyzing single files (intraprocedural analysis)
- Detecting systemic bugs (multiple instances across codebase)
- Enforcing secure defaults and code standards
- Performing rapid initial security assessment
- Scanning code without building it first

**Consider alternatives when:**
- Multiple files are required for analysis → Consider Semgrep Pro Engine or CodeQL
- Complex flow analysis is needed → Consider CodeQL
- Advanced taint tracking across files → Consider CodeQL or Semgrep Pro
- Custom in-house framework analysis → May need specialized tooling

## Quick Reference

| Task | Command |
|------|---------|
| Scan with auto-detection | `semgrep --config auto` |
| Scan with specific ruleset | `semgrep --config="p/trailofbits"` |
| Scan with custom rules | `semgrep -f /path/to/rules` |
| Output to SARIF format | `semgrep -c p/default --sarif --output scan.sarif` |
| Test custom rules | `semgrep --test` |
| Disable metrics | `semgrep --metrics=off --config=auto` |
| Filter by severity | `semgrep --config=auto --severity ERROR` |
| Show dataflow traces | `semgrep --dataflow-traces -f rule.yml` |

## Installation

### Prerequisites

- Python 3.7 or later (for pip installation)
- macOS, Linux, or Windows
- Homebrew (optional, for macOS/Linux)

### Install Steps

**Via Python Package Installer:**

```bash
python3 -m pip install semgrep
```

**Via Homebrew (macOS/Linux):**

```bash
brew install semgrep
```

**Via Docker:**

```bash
docker pull returntocorp/semgrep
```

### Keeping Semgrep Updated

```bash
# Check current version
semgrep --version

# Update via pip
python3 -m pip install --upgrade semgrep

# Update via Homebrew
brew upgrade semgrep
```

### Verification

```bash
semgrep --version
```

## Core Workflow

### Step 1: Initial Scan

Start with an auto-configuration scan to evaluate Semgrep's effectiveness:

```bash
semgrep --config auto
```

**Important:** Auto mode submits metrics online. To disable:

```bash
export SEMGREP_SEND_METRICS=off
# OR
semgrep --metrics=off --config auto
```

### Step 2: Select Targeted Rulesets

Use the [Semgrep Registry](https://semgrep.dev/explore) to select rulesets:

```bash
# Security-focused rulesets
semgrep --config="p/trailofbits"
semgrep --config="p/cwe-top-25"
semgrep --config="p/owasp-top-ten"

# Language-specific
semgrep --config="p/javascript"

# Multiple rulesets
semgrep --config="p/trailofbits" --config="p/r2c-security-audit"
```

### Step 3: Review and Triage Results

Filter results by severity:

```bash
semgrep --config=auto --severity ERROR
```

Use output formats for easier analysis:

```bash
# SARIF for VS Code SARIF Explorer
semgrep -c p/default --sarif --output scan.sarif

# JSON for automation
semgrep -c p/default --json --output scan.json
```

### Step 4: Configure Ignored Files

Create `.semgrepignore` file to exclude paths:

```
# Ignore specific files/directories
path/to/ignore/file.ext
path_to_ignore/

# Ignore by extension
*.ext

# Include .gitignore patterns
:include .gitignore
```

**Note:** By default, Semgrep skips `/tests`, `/test`, and `/vendors` folders.

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Using `--config auto` on private code | Sends metadata to Semgrep servers | Use `--metrics=off` or specific rulesets |
| Forgetting `.semgrepignore` | Scans excluded directories like `/vendor` | Create `.semgrepignore` file |
| Not testing rules with false positives | Rules generate noise | Add `# ok:` test cases |
| Using generic `# nosemgrep` | Makes code review harder | Use `# nosemgrep: rule-id` with explanation |
| Overusing ellipsis `...` | Degrades performance and accuracy | Use specific patterns when possible |
| Not including metadata in rules | Makes triage difficult | Add CWE, confidence, impact fields |

## Limitations

- **Single-file analysis:** Cannot track data flow across files without Semgrep Pro Engine
- **No build required:** Cannot analyze compiled code or resolve dynamic dependencies
- **Pattern-based:** May miss vulnerabilities requiring deep semantic understanding
- **Limited taint tracking:** Complex taint analysis is still evolving
- **Custom frameworks:** In-house proprietary frameworks may not be well-supported

## Reference material

**[references/customization.md](references/customization.md)** — writing custom rules and configuration

**[references/advanced.md](references/advanced.md)** — advanced usage and CI/CD integration

## Related Skills

| Skill | When to Use Together |
|-------|---------------------|
| **codeql** | For cross-file taint tracking and complex data flow analysis |
| **sarif-parsing** | For processing Semgrep SARIF output in pipelines |

## Resources

### Key External Resources

**[Trail of Bits public Semgrep rules](https://github.com/trailofbits/semgrep-rules)**
Community-contributed Semgrep rules for security audits, with contribution guidelines and quality standards.

**[Semgrep Registry](https://semgrep.dev/explore)**
Official registry of Semgrep rules, searchable by language, framework, and security category.

**[Semgrep Playground](https://semgrep.dev/playground/new)**
Interactive online tool for writing and testing Semgrep rules. Use "simple mode" for easy pattern combination.

**[Learn Semgrep Syntax](https://semgrep.dev/learn)**
Comprehensive guide on Semgrep rule-writing fundamentals.

**[Trail of Bits Blog: How to introduce Semgrep to your organization](https://blog.trailofbits.com/2024/01/12/how-to-introduce-semgrep-to-your-organization/)**
Seven-step plan for organizational adoption of Semgrep, including pilot testing, evangelization, and CI/CD integration.

**[Trail of Bits Blog: Discovering goroutine leaks with Semgrep](https://blog.trailofbits.com/2021/11/08/discovering-goroutine-leaks-with-semgrep/)**
Real-world example of writing custom rules to detect Go-specific issues.

### Video Resources

- [Introduction to Semgrep - Trail of Bits Webinar](https://www.youtube.com/watch?v=yKQlTbVlf0Q)
- [Detect complex code patterns using semantic grep](https://www.youtube.com/watch?v=IFRp2Y3cqOw)
- [Semgrep part 1 - Embrace Secure Defaults, Block Anti-patterns and more](https://www.youtube.com/watch?v=EIjoqwT53E4)
- [Semgrep Weekly Wednesday Office Hours: Modifying Rules to Reduce False Positives](https://www.youtube.com/watch?v=VSL44ZZ7EvY)
- [Raining CVEs On WordPress Plugins With Semgrep | Nullcon Goa 2022](https://www.youtube.com/watch?v=RvKLn2ofMAo)
