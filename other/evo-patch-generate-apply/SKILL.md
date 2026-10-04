---
name: evo-patch-generate-apply
description: Generates git-compatible unified diff patches from original and modified file contents, writes them to numbered patch files, and applies them to the repository using git apply or GNU patch. Use when you need to create code patches, apply fixes to source files, or automate code modifications via diff/patch workflow.
---

# Patch Generate & Apply Skill

Generates and applies unified diff patches for code fixes.

## When to Use

- You need to generate a patch file from code changes
- You need to apply a .diff/.patch file to a repository
- Automating code fixes via the diff/patch workflow

## Workflow

1. **Generate diff** using `generate_unified_diff()` with a/b prefixes
2. **Handle EOF** using `handle_no_newline_at_eof()` for POSIX compliance
3. **Write patch** using `write_patch_file()` to create patch_N.diff
4. **Apply patch** using `apply_patch()` with git apply and fallbacks
5. **Validate** using `validate_patch_applied()` to confirm changes
6. **Batch apply** using `apply_all_patches()` for multiple patches

## Key Functions

All functions are in `scripts/patch.py`:

- `generate_unified_diff(original, modified, file_path)` - Creates git-compatible unified diff
- `handle_no_newline_at_eof(diff_lines)` - Adds missing EOF newline markers
- `write_patch_file(diff_content, output_dir, index)` - Writes patch_N.diff
- `apply_patch(patch_path, target_dir)` - Applies via git apply with fallbacks
- `validate_patch_applied(file_path, expected_content)` - Confirms patch worked
- `apply_all_patches(patch_dir, target_dir)` - Applies all patches in order

## Important Notes

- Use splitlines(keepends=True) to preserve trailing newlines
- Always add a/ and b/ prefixes for git apply compatibility
- Handle "No newline at end of file" marker manually
- git apply uses -p1 by default to strip a/ b/ prefixes
- Use --3way flag as fallback for context mismatches

## Reference

See `references/domain_reference.md` for detailed domain knowledge.
