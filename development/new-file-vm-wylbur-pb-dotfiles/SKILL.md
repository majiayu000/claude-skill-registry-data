---
name: new-file
description: Create new files with proper headers and verify necessity
---

# New File Creation Skill

## Purpose
Ensures new files are only created when necessary and always include proper headers with author attribution, dates, and license information in the correct comment format.

## When This Activates
- User asks to create a new file
- About to use Write tool for a file that doesn't exist
- Keywords: "create file", "new file", "add file", "write to"

## Instructions

### Phase 1: Verify Necessity

1. **Check if File Exists**
   Before creating, check if file already exists:
   ```bash
   ls -la /path/to/file
   # or
   test -f /path/to/file && echo "exists" || echo "new"
   ```

2. **Search for Similar Functionality**
   - Could this content go in an existing file?
   - Is there a similar file we should edit instead?
   - Use glob/grep to find related files:
   ```bash
   find . -name "*similar_name*"
   grep -r "similar_function" .
   ```

3. **Ask User if Uncertain**
   If there's ANY doubt about whether to create new vs edit existing:
   - "I found existing file X with similar purpose. Should I edit that instead or create new file Y?"
   - "Should I create new file X for Y purpose?"

### Phase 2: Determine File Type and Comment Format

4. **Identify Language/Format**
   Based on file extension, determine comment syntax:

   | Extension | Comment Format | Example |
   |-----------|----------------|---------|
   | `.py` | `#` | Python |
   | `.sh` `.bash` | `#` | Shell script |
   | `.js` `.ts` `.jsx` `.tsx` | `//` or `/* */` | JavaScript/TypeScript |
   | `.sql` | `--` | SQL |
   | `.md` | `<!--  -->` | Markdown (HTML comments) |
   | `.yaml` `.yml` | `#` | YAML |
   | `.json` | _(no comments)_ | JSON (no header) |
   | `.toml` | `#` | TOML |
   | `.rs` | `//` | Rust |
   | `.go` | `//` | Go |
   | `.c` `.cpp` `.h` | `//` or `/* */` | C/C++ |

### Phase 3: Generate Proper Header

5. **Create Header with Correct Format**

   **Template:**
   ```
   <comment-start>
   Author: PB and Claude
   Date: YYYY-MM-DD  (for code) or Day DD Mon YYYY (for docs)
   License: (c) HRDAG, YYYY, GPL-2 or newer

   ------
   relative/path/to/file
   <comment-end>
   ```

   **Important Rules:**
   - **Path MUST be relative** to project root, NOT absolute
   - **Date format**:
     - Code files: `2025-11-03`
     - Documentation: `Sun 03 Nov 2025`
   - **Year**: Current year
   - **Spacing**: One blank line after header before content

### Phase 4: Create File

6. **Write File with Header + Content**
   ```
   <header>

   <actual file content>
   ```

## Language-Specific Examples

### Python (.py)
```python
# Author: PB and Claude
# Date: 2025-11-03
# License: (c) HRDAG, 2025, GPL-2 or newer
#
# ------
# claude-mem/src/tools/example.py

import sys

def example():
    pass
```

### Shell Script (.sh)
```bash
#!/usr/bin/env bash
# Author: PB and Claude
# Date: 2025-11-03
# License: (c) HRDAG, 2025, GPL-2 or newer
#
# ------
# scripts/deploy.sh

set -euo pipefail

echo "Deploy script"
```

### TypeScript (.ts)
```typescript
// Author: PB and Claude
// Date: 2025-11-03
// License: (c) HRDAG, 2025, GPL-2 or newer
//
// ------
// src/lib/helper.ts

export function helper() {
  // implementation
}
```

### Markdown (.md)
```markdown
<!--
Author: PB and Claude
Date: Sun 03 Nov 2025
License: (c) HRDAG, 2025, GPL-2 or newer

------
docs/guide.md
-->

# Guide Title

Content here...
```

### SQL (.sql)
```sql
-- Author: PB and Claude
-- Date: 2025-11-03
-- License: (c) HRDAG, 2025, GPL-2 or newer
--
-- ------
-- migrations/001_initial.sql

CREATE TABLE example (
  id SERIAL PRIMARY KEY
);
```

### YAML (.yml, .yaml)
```yaml
# Author: PB and Claude
# Date: 2025-11-03
# License: (c) HRDAG, 2025, GPL-2 or newer
#
# ------
# config/settings.yml

setting: value
```

## Special Cases

### JSON Files
JSON doesn't support comments, so **skip the header**:
```json
{
  "name": "example",
  "version": "1.0.0"
}
```

### Shebang Scripts
For executable scripts, **shebang comes BEFORE header**:
```bash
#!/usr/bin/env bash
# Author: PB and Claude
# Date: 2025-11-03
# License: (c) HRDAG, 2025, GPL-2 or newer
#
# ------
# bin/run.sh

echo "Script content"
```

### Configuration Files
For `.env`, `.gitignore`, `.editorconfig` etc. - **skip header** (these are config, not code)

## Common Patterns

### Date Formatting
```python
from datetime import datetime

# For code files:
date_str = datetime.now().strftime("%Y-%m-%d")  # 2025-11-03

# For documentation:
date_str = datetime.now().strftime("%a %d %b %Y")  # Sun 03 Nov 2025
```

### Path Calculation
```bash
# Get relative path from project root
# If current dir: /home/pball/projects/claude-mem/src/tools
# And file: /home/pball/projects/claude-mem/src/tools/example.py
# Header path should be: src/tools/example.py

# Use project-relative paths, NOT absolute paths!
```

## Rules

### ✅ Always Do
- Check if file exists before creating
- Search for similar functionality first
- Use correct comment format for language
- Include author, date, license, path
- Use relative paths in header (never absolute)
- Use correct date format (code vs docs)
- Leave blank line after header

### ❌ Never Do
- Create new file without checking if similar exists
- Use absolute paths in header (`/home/pball/...`)
- Wrong comment syntax for language
- Mix date formats (use consistent style)
- Forget the "------" separator line
- Skip the header (except JSON/config files)

### ⚠️ Special Attention
- **Markdown files**: Use `<!-- -->` HTML comments, NOT `#`
- **Shebang scripts**: Shebang first, THEN header
- **JSON files**: No header (JSON doesn't support comments)
- **Config files**: Usually skip header (.env, .gitignore, etc.)
- **Date format**: Code uses `YYYY-MM-DD`, docs use `Day DD Mon YYYY`

## Decision Tree

```
New file requested
    │
    ├─> File exists?
    │   ├─> Yes → STOP, suggest editing instead
    │   └─> No → Continue
    │
    ├─> Similar file exists?
    │   ├─> Yes → ASK user: edit existing or create new?
    │   └─> No → Continue
    │
    ├─> Determine file type (extension)
    │   └─> Select comment format
    │
    ├─> Generate header
    │   ├─> Author: PB and Claude
    │   ├─> Date: (format based on file type)
    │   ├─> License: (c) HRDAG, YYYY, GPL-2 or newer
    │   └─> Path: relative/path/to/file
    │
    └─> Write file with header + content
```

## Workflow Summary

1. User requests new file creation
2. Check if file already exists → if yes, suggest editing
3. Search for similar files → if found, ask user
4. Determine language/extension → select comment format
5. Generate proper header with relative path
6. Create file with header + content
7. Confirm creation to user

## Success Criteria

- No new files created when editing existing would suffice
- Every new file has proper header (except JSON/config)
- All paths are relative, never absolute
- Correct comment syntax for each language
- Consistent date formatting
- User approves creation when similar files exist
