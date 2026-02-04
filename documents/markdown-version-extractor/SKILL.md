---
name: markdown-version-extractor
description: Extracts 'version' or 'uuid' fields from YAML frontmatter using uv.
---

# Markdown Version Extractor

Use this skill to identify the version or UUID of a skill or project stored in Markdown frontmatter. This is a critical dependency for the Version Sync phase of the Persona Protocol.

## Capabilities
- Parses YAML frontmatter using the `python-frontmatter` library.
- Safely extracts versioning identifiers (`uuid` or `version`).
- Provides available metadata keys if the specific version tag is missing.

## Execution Logic
The agent **MUST** use `uv run` and **MUST** provide absolute paths for both the script and the target file.

**Command Template:**

```bash
uv run <absolute_path_to_get_version.py> "<absolute_path_to_target_md_file>"
```

## Guidance for the Agent

1. **NO DIRECT PYTHON**: You are **FORBIDDEN** from calling `python` or `python3` directly. This script uses PEP 723 inline dependencies that require the `uv` runtime.
2. **Absolute Paths**: You must resolve the current working directory to provide the full absolute path for:
   - The script itself.
   - The file being checked.
3. **Version Identifier Priority**:
   - The Registry uses the `uuid` field.
   - Local files may use either `version` or `uuid`.
   - If the script returns a `uuid`, use that for comparison against the registry's `uuid`.
4. **Error Handling**:
   - If the output shows `status: "missing_tag"`, check the `metadata_keys` in the JSON. If neither `uuid` nor `version` exists, consider the skill unversioned and trigger an update.
   - If the file is missing or not Markdown, report a failure.
