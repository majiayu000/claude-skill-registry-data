---
name: documentation-consistency
description: Verify documentation is up-to-date and consistent across all files. Check for broken links, outdated references, deprecated content, and mismatched.
---

# Documentation Consistency Check

Systematically audit all documentation to ensure consistency, accuracy, and alignment with the current state of the codebase.

## When to Use This Skill

Use this skill when you need to:

- Audit documentation for accuracy
- Check for broken or outdated links
- Find references to non-existent files or functions
- Verify version numbers are consistent
- Remove deprecated or stale content
- Ensure documentation matches codebase structure
- Prepare for a release

**Trigger phrases**: "check documentation", "audit docs", "find broken links", "update documentation", "docs consistency", "stale documentation", "outdated references"

## What This Skill Does

### Consistency Audit Process

1. **Cross-Reference Validation** - Verify all references point to existing files
2. **Version Consistency** - Check version numbers match across files
3. **Structure Alignment** - Ensure documented structure matches actual files
4. **Link Verification** - Test all internal and external links
5. **Content Freshness** - Identify potentially outdated content
6. **Deprecation Cleanup** - Remove references to deleted/renamed items

## Instructions

### Step 1: Identify All Documentation Files

```bash
# Find all markdown documentation files
find . -name "*.md" -type f | grep -v node_modules | grep -v .venv | grep -v __pycache__

# Common documentation files to check:
# - README.md
# - CHANGELOG.md
# - docs/DEVLOG.md
# - docs/*.md
# - .codex/context/*.md
# - guides/*.md
```

### Step 2: Check Internal Links

Verify all markdown links point to existing files:

```bash
# Find all markdown links in a file
grep -oE '\[.*?\]\([^)]+\)' README.md

# Extract just the paths
grep -oE '\[.*?\]\([^)]+\)' README.md | sed 's/.*(\([^)]*\))/\1/' | grep -v "^http"

# For each path, verify the file exists
for link in $(grep -oE '\[.*?\]\([^)]+\)' README.md | sed 's/.*(\([^)]*\))/\1/' | grep -v "^http"); do
  if [ ! -f "$link" ] && [ ! -d "$link" ]; then
    echo "BROKEN: $link"
  fi
done
```

### Step 3: Verify Version Consistency

Check that version numbers match across all files:

```bash
# Search for version patterns
grep -rn "version" --include="*.md" --include="*.toml" --include="*.json" --include="*.yaml" .

# Common version locations:
# - pyproject.toml: version = "X.Y.Z"
# - package.json: "version": "X.Y.Z"
# - README.md: badges, headers
# - CHANGELOG.md: ## [X.Y.Z]
# - __version__.py or __init__.py
```

### Step 4: Validate Project Structure References

Compare documented structure to actual file system:

```bash
# Get actual project structure
find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" | head -50

# Compare with documented structure in README.md
# Look for:
# - Directories mentioned that don't exist
# - Files mentioned that have been removed
# - Missing documentation for new files/directories
```

### Step 5: Check for Deprecated References

Look for references to items that no longer exist:

#### Functions and Classes
```bash
# Find function/class references in docs
grep -rE "(def |class |function )\w+" docs/ README.md

# Verify each referenced function/class exists in codebase
# Flag any that can't be found
```

#### File References
```bash
# Find file path references
grep -rE "(`[^`]+\.(py|js|ts|go|java|cs|cpp|c|h)`)" --include="*.md" .

# Check each referenced file exists
```

#### Configuration Options
```bash
# Find configuration references
grep -rE "(config\.|settings\.|options\.)" --include="*.md" .

# Verify documented options match actual config files
```

### Step 6: Audit External Links

```bash
# Find all external links
grep -rEoh "https?://[^)\"' >]+" --include="*.md" . | sort -u

# Test each link (optional - may take time)
# curl -s -o /dev/null -w "%{http_code}" URL

# Common issues:
# - 404 (page not found)
# - 301/302 (redirects - may need updating)
# - SSL errors
```

### Step 7: Check for Stale Content

Look for indicators of outdated documentation:

#### Date Markers
```bash
# Find date references
grep -rE "(January|February|March|April|May|June|July|August|September|October|November|December) 20[0-9]{2}" --include="*.md" .
grep -rE "202[0-3]-[0-9]{2}" --include="*.md" .  # Old dates

# Flag anything older than 6-12 months for review
```

#### TODO/FIXME Comments
```bash
# Find outstanding documentation TODOs
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.md" .
```

#### Placeholder Text
```bash
# Find unfilled placeholders
grep -rE "\[.*?\]|\{.*?\}|<.*?>" --include="*.md" . | grep -v "http"
grep -rE "TBD|TBA|Coming soon|TODO" --include="*.md" .
```

### Step 8: Generate Consistency Report

Create a summary of all issues found:

```markdown
# Documentation Consistency Report

## Generated: YYYY-MM-DD

### Summary
- **Files Audited**: X
- **Issues Found**: Y
- **Critical**: Z
- **Warnings**: W

### Broken Links
| File | Line | Broken Link | Suggested Fix |
|------|------|-------------|---------------|
| README.md | 45 | [link](old/path.md) | Update to new/path.md |

### Version Mismatches
| File | Current | Expected |
|------|---------|----------|
| README.md | 1.0.0 | 1.2.0 |

### Deprecated References
| File | Line | Reference | Issue |
|------|------|-----------|-------|
| docs/api.md | 23 | `old_function()` | Function removed in v1.1.0 |

### Stale Content
| File | Section | Last Updated | Notes |
|------|---------|--------------|-------|
| docs/setup.md | Installation | 2023-06 | May need update |

### Missing Documentation
| Item | Type | Notes |
|------|------|-------|
| new_module.py | Module | No documentation found |

### Recommendations
1. **High Priority**: Fix broken links in README.md
2. **Medium Priority**: Update version references
3. **Low Priority**: Review stale content in docs/
```

## Common Documentation Issues

### Issue Categories

| Category | Examples | Severity |
|----------|----------|----------|
| Broken Links | 404s, wrong paths | High |
| Version Mismatch | Old versions in badges/text | High |
| Missing Files | Referenced files deleted | High |
| Deprecated APIs | Old function names | Medium |
| Stale Content | Outdated instructions | Medium |
| Unfilled Placeholders | [TODO], TBD | Low |
| Typos | Misspelled file names | Low |

### Fix Patterns

#### Broken Internal Link
```markdown
# Before (broken)
See [installation guide](docs/install.md)

# After (fixed - file moved)
See [installation guide](guides/installation.md)
```

#### Version Update
```markdown
# Before
![Version](https://img.shields.io/badge/version-1.0.0-blue)

# After
![Version](https://img.shields.io/badge/version-1.2.0-blue)
```

#### Deprecated Reference
```markdown
# Before
Use `old_api_call()` to fetch data.

# After
Use `new_api_call()` to fetch data. (Note: `old_api_call()` was deprecated in v1.1.0)
```

## Automation Script Template

```python
#!/usr/bin/env python3
"""Documentation consistency checker."""

import os
import re
from pathlib import Path

def find_markdown_files(root_dir: str) -> list[Path]:
    """Find all markdown files in project."""
    excludes = {'node_modules', '.venv', '__pycache__', '.git'}
    files = []
    for path in Path(root_dir).rglob('*.md'):
        if not any(ex in path.parts for ex in excludes):
            files.append(path)
    return files

def extract_internal_links(content: str) -> list[str]:
    """Extract internal links from markdown content."""
    pattern = r'\[.*?\]\(([^)]+)\)'
    links = re.findall(pattern, content)
    return [l for l in links if not l.startswith(('http', '#', 'mailto'))]

def check_link_exists(link: str, base_path: Path) -> bool:
    """Check if linked file exists."""
    target = base_path.parent / link
    return target.exists()

def audit_documentation(root_dir: str) -> dict:
    """Run full documentation audit."""
    results = {
        'broken_links': [],
        'version_mismatches': [],
        'stale_content': [],
        'todos': []
    }

    for md_file in find_markdown_files(root_dir):
        content = md_file.read_text(encoding='utf-8')

        # Check links
        for link in extract_internal_links(content):
            if not check_link_exists(link, md_file):
                results['broken_links'].append({
                    'file': str(md_file),
                    'link': link
                })

        # Check for TODOs
        if 'TODO' in content or 'FIXME' in content:
            results['todos'].append(str(md_file))

    return results

if __name__ == '__main__':
    results = audit_documentation('.')
    print(f"Broken links: {len(results['broken_links'])}")
    print(f"Files with TODOs: {len(results['todos'])}")
```

## Quality Checklist

Before completing documentation audit:

- [ ] All internal links verified and working
- [ ] Version numbers consistent across all files
- [ ] No references to non-existent files/functions
- [ ] External links tested (at least critical ones)
- [ ] Placeholder text filled or removed
- [ ] TODOs addressed or documented for follow-up
- [ ] Deprecated content removed or marked
- [ ] Documentation structure matches codebase
- [ ] Dates updated where applicable
- [ ] Consistency report generated

## Related Skills

- `version-upgrade` - Version update workflow
- `code-commit-workflow` - Commit best practices
- `technical-documentation` - Documentation writing

---

**Version**: 1.0.0
**Last Updated**: December 2025


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
