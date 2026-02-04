---
name: categorizing-files
description: "Defines the standard 8-category taxonomy for classifying project files: Config, Tests, Docs, Scripts, Source Code, Data, AI Tooling, and Other. REFERENCE THIS SKILL whenever categorizing files, auditing project structure, or answering 'what types of files are here.' Apply these categories and patterns whether using the bundled script or manual analysis."
---

# File Categorization

## Categories

| Category | Description |
|----------|-------------|
| **Config** | Configuration files for tools, environments, and build systems |
| **Tests** | Test files, fixtures, and testing utilities |
| **Docs** | Documentation, READMEs, and guides |
| **Scripts** | Standalone executable scripts and automation |
| **Source Code** | Core application/library source files |
| **Data** | Data files, datasets, and static assets |
| **AI Tooling** | AI/ML configs, prompts, and agent definitions |
| **Other** | Files that don't fit other categories (fallback) |

---

## Category Mapping Rules

**Always use exactly these 8 categories** — do not invent new ones like "Schema", "Database", or
"Reference Data." Map edge cases as follows:

| File Type | Category | Reasoning |
|-----------|----------|-----------|
| SQL DDL (CREATE TABLE) | Docs | Documents database structure |
| SQL DML (INSERT/SELECT) | Data | Contains or queries data |
| .duckdb, .sqlite files | Data | Database storage |
| schema.json, openapi.yaml | Docs | Specification/contract files |
| Shell scripts (.sh) | Scripts | Executable automation |
| requirements.txt | Config | Dependency configuration |

---

## Directory Exclusion

When scanning directories, the script uses layered exclusion to prevent wasting tokens on useless output:

**Layer 1: Always Excluded** (non-negotiable)
- `node_modules/`, `bower_components/`, `jspm_packages/`
- `.git/`, `.svn/`, `.hg/`
- `__pycache__/`, `.pytest_cache/`, `.tox/`, `.mypy_cache/`
- `venv/`, `.venv/`

**Layer 2: .gitignore** (if present and parseable)
- Respects project-specific exclusions
- Requires `pathspec` library; warns if unavailable

**Layer 3: Extended Defaults** (fallback when no .gitignore)
- `dist/`, `build/`, `out/`, `_build/`, `target/`
- `vendor/`, `coverage/`, `.nyc_output/`, `htmlcov/`
- `env/`, `*.egg-info/`

**Layer 4: Escape Hatches**
- `--include-ignored`: Bypass Layers 2-3 (but NOT Layer 1)
- `--include-all`: Bypass ALL layers (use with extreme caution)

**Important:** `.env` as a FILE is categorized as Config. `.env` as a DIRECTORY is excluded.

When reporting results, explain which exclusion path was used:
> "Excluded 3 directories via Layer 1 (always-exclude), 2 via .gitignore"

---

## Categorization Priority

Apply rules in this order (first match wins):

1. **Directory path**: `tests/` → Tests, `src/` → Source Code, `docs/` → Docs, `references/` → Docs
2. **Schema/spec files**: `schema.json`, `openapi.yaml` → Docs (see patterns.md for full list)
3. **Filename pattern**: `test_*.py` → Tests, `*.config.js` → Config
4. **Extension**: `.sh` → Scripts, `.csv` → Data, `.py` → Source Code
5. **Content analysis** (if still ambiguous): Check for test assertions, CLI parsing, etc.

---

## Categorization Algorithm

```text
function categorize(filePath, content):

  # PHASE 1: Filename + directory rules
  category = byLocationOrExtension(filePath)
  if category != UNKNOWN: return (category, "High")

  # PHASE 2: Frontmatter refinement
  fm = extractYAMLFrontmatter(content)
  if fm indicates config: return (CONFIG, "Medium")
  if fm indicates ai_tooling: return (AI_TOOLING, "Medium")

  # PHASE 3: Content structure analysis
  if looksLikeTest(content): return (TESTS, "Medium")
  if looksLikeScript(content): return (SCRIPTS, "Medium")
  if looksLikeSource(content): return (SOURCE_CODE, "Medium")
  if looksLikeDocs(content): return (DOCS, "Medium")
  if looksLikeData(content): return (DATA, "Medium")

  # PHASE 4: Keyword detection (fallback)
  kw_category = detectByKeywords(content)
  if kw_category: return (kw_category, "Low")

  return (OTHER, "Low")
```

---

## Pattern Matching Details

For complete pattern reference, see [references/patterns.md](references/patterns.md):
- Directory patterns (test/, src/, config/, etc.)
- Filename patterns (*.config.js, test_*.py, etc.)
- Frontmatter indicators
- Content structure signals
- Keyword detection rules

---

## Output Format

For each file, provide:

```markdown
### [Filename]

- **Category**: [Config | Tests | Docs | Scripts | Source Code | Data | AI Tooling | Other]
- **Confidence**: [High | Medium | Low]
- **Reasoning**: [Why this category was chosen]
- **Recommended Location**: [Suggested directory if misfiled, or "Correct" if well-placed]
```

**Confidence Guidelines:**
- **High** (>95%): Strong directory + extension match (Phase 1)
- **Medium** (>80%): Frontmatter or content structure match (Phases 2-3)
- **Low**: Keyword match or no clear signals (Phase 4)

---

## Content Analysis Caveats

When using `--analyze-content` (Phases 2-4):

- **False positives from examples**: Files containing test keywords as *examples* (like documentation showing `assert` or `describe()`) may be miscategorized as Tests
- **Sampling limits**: Large files (>5KB) are sampled from the beginning, not fully analyzed
- **Binary files**: Non-text files are skipped and categorized as Other
- **Keyword ambiguity**: Common words like "class" or "function" appear in both Source Code and Docs

**Recommendation**: Use Phase 1 (path-based) categorization for speed and reliability. Enable `--analyze-content` only for ambiguous files or when you need higher accuracy on edge cases.

---

## Examples

### Example 1: Clear Categorization

**User:** What category is `src/utils/helpers.py`?

**Response:**
```markdown
### src/utils/helpers.py
- **Category**: Source Code
- **Confidence**: High
- **Reasoning**: Located in `src/` directory; `.py` extension; module structure
- **Recommended Location**: Correct
```

### Example 2: Misfiled Resource

**User:** Categorize `customers.csv` in root directory.

**Response:**
```markdown
### customers.csv
- **Category**: Data
- **Confidence**: High
- **Reasoning**: CSV extension; tabular structure detected
- **Recommended Location**: `data/customers.csv`
```

### Example 3: Ambiguous File

**User:** What category is `notes.txt`?

**Response:**
```markdown
### notes.txt
- **Category**: Other
- **Confidence**: Low
- **Reasoning**: Prose content; no structural markers; could be Docs if formalized
- **Recommended Location**: Manual review needed — consider `docs/` if documentation
```

### Example 4: Project Inventory

**User:** Categorize all files in this project.

**Response:**
```
Config (5):
  - .gitignore
  - pyproject.toml
  - docker-compose.yml

Source Code (12):
  - src/main.py
  - src/utils/helpers.py

Tests (4):
  - tests/test_main.py
  - tests/conftest.py

Docs (2):
  - README.md
  - docs/API.md

AI Tooling (1):
  - .claude/skills/categorizing-files/SKILL.md

Other (1):
  - notes.txt (Low confidence — review needed)

Excluded 2 directories: 1 via Layer 1 (always-exclude), 1 via .gitignore
```

---

## Optional: Automated Script

For large directories or programmatic use, the bundled script implements this methodology with
automatic directory exclusion (skips node_modules/, venv/, .git/, etc.):

```bash
# Basic usage
python scripts/categorize.py [path]

# Enable content analysis (Phases 2-4)
python scripts/categorize.py --analyze-content [path]

# Include .gitignore-excluded files (bypass Layers 2-3)
python scripts/categorize.py --include-ignored [path]

# Include ALL files including node_modules (use with caution)
python scripts/categorize.py --include-all [path]
```

For a single file:
```bash
python scripts/categorize.py myfile.py
# Output: myfile.py: Source Code (High)
```

For a directory:
```bash
python scripts/categorize.py .
# Output: Grouped list by category with exclusion summary
```

See `scripts/categorize.py` for implementation details and programmatic API.
