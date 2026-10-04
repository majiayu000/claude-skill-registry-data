---
name: evo-maven-patch-generation
description: Generates GNU-compatible unified diff patches for proposed code or POM fixes, writes them to numbered patch files, and applies them to the repository.
---

# evo-maven-patch-generation

Generates and applies unified diff patches for Java Maven build fixes.

## Key Functions

- `generate_unified_diff(original_text, modified_text, file_path)` - Basic unified diff
- `make_strict_patch(original_text, modified_text, file_path)` - Strict diff with EOF newline handling
- `write_patch_file(patch_content, patch_path)` - Write patch to disk
- `apply_patch_via_git(patch_path, project_dir)` - Apply via git apply
- `apply_patch_via_patch_command(patch_path, project_dir, strip)` - Apply via patch command
- `apply_patch(patch_path, project_dir)` - Try git apply, fallback to patch
- `modify_file_content(file_path, old_text, new_text)` - Simple text replacement
- `modify_java_source(file_path, modifications)` - Apply multiple replacements to Java file
- `modify_pom_xml(pom_path, property_changes)` - Modify POM properties
- `create_travis_fix_patch(travis_path, old_text, new_text, patch_path)` - Fix .travis.yml

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-maven-patch-generation/scripts')
from utils import (
    make_strict_patch, write_patch_file, apply_patch,
    modify_file_content, create_travis_fix_patch
)

# Fix .travis.yml typo
create_travis_fix_patch('.travis.yml', 'build.pom.xml', 'build-pom.xml', 'patch_1.diff')

# Apply patch
apply_patch('patch_1.diff', '/path/to/project')
```

## Important Notes

- Always use `make_strict_patch` for git-compatible patches (handles EOF newlines)
- Patch files use standard unified diff format compatible with `git apply` and `patch`
- File paths in diffs use `a/` and `b/` prefixes
