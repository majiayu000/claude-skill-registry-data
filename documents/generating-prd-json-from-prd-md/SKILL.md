---
name: generating-prd-json-from-prd-md
description: Generates prd.json task tracking file from PRD.md requirements document. Use when initializing Ralph loop or when the user asks to convert PRD to JSON format for autonomous execution.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Bash
  model: haiku
  stability: development
---

# PRD to JSON Conversion

Hybrid approach: Python script parses, AI validates and corrects.

## Workflow

1. **Dry-run parser** (Bash tool) — catch parser issues before writing

```bash
python ralph/scripts/generate_prd_json.py --dry-run
```

Check output for: declared vs parsed story count mismatch, missing stories, empty acceptance/files. If issues found, fix PRD markdown or note for manual correction in step 3.

1. **Run parser** (Bash tool)

```bash
python ralph/scripts/generate_prd_json.py
```

Script handles: PRD.md parsing, `(depends: ...)` extraction, content hashing, state preservation.

1. **Validate** (Read tool)
   - Read `ralph/docs/prd.json` (script output)
   - Read `docs/PRD.md` (cross-reference)
   - Check against Validation Checklist

2. **Correct errors** (Write tool, if needed)
   - Fix issues found
   - Recompute `content_hash` if title/description/acceptance changed
   - Write corrected `ralph/docs/prd.json`

3. **Report**
   - Story count and status
   - Corrections made
   - Suggest: `make ralph_run`

## Validation Checklist

For each story, verify:

- [ ] `id` follows STORY-XXX format
- [ ] `title` is 3-7 words, matches PRD.md feature
- [ ] `description` is non-empty
- [ ] `acceptance` array is non-empty
- [ ] `files` array contains valid paths (if specified in PRD.md)
- [ ] `content_hash` is 64-char hex string
- [ ] `depends_on` references valid STORY-XXX IDs (no circular deps, no self-refs)

Cross-reference with PRD.md:

- [ ] All `#### Feature N:` headings have corresponding stories
- [ ] Story order matches PRD.md feature order
- [ ] `(depends: STORY-XXX)` syntax correctly parsed

## Common Issues to Correct

| Issue | Correction |
| ------- | ------------ |
| Empty acceptance | Extract from description or PRD.md feature |
| Invalid depends_on reference | Remove non-existent story IDs |
| Circular dependency | Remove one direction |
| Missing content_hash | Recompute from title+description+acceptance |
| Duplicate story IDs | Renumber sequentially |

## prd.json Schema

See `ralph/docs/templates/prd.json.template` for structure and fields.

## Usage

```bash
make ralph_prd_json
```

## Next Steps

```bash
make ralph_init    # Validate environment
make ralph_run     # Start Ralph loop
```
