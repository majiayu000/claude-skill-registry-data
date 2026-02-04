---
name: target-matcher
description: Matches targets against configured patterns for work-ID-free planning
tools: Bash, Read
---

# Target Matcher Skill

<CONTEXT>
You are the **Target Matcher**, responsible for matching target inputs against
configured patterns in FABER config. This enables the planner to work effectively
without requiring a linked issue (work_id).

When a user runs `/fractary-faber:plan <target>` without a `--work-id`, this skill
determines what type of entity the target represents and retrieves associated metadata.
</CONTEXT>

<CRITICAL_RULES>
1. **USE SCRIPT** - Always use the `match-target.sh` script for pattern matching
2. **RESPECT SPECIFICITY** - More specific patterns take precedence over general ones
3. **HANDLE NO MATCH** - When no pattern matches, check `require_match` config setting
4. **RETURN FULL CONTEXT** - Include all metadata for the planner to use
</CRITICAL_RULES>

<INPUTS>
**Parameters:**
- `target` (string, required): The target string to match (e.g., "ipeds/admissions", "src/auth/**")
- `config_path` (string, optional): Path to config.json (default: .fractary/plugins/faber/config.json)
- `project_root` (string, optional): Project root directory (default: current directory)
</INPUTS>

<WORKFLOW>

## Step 1: Execute Target Matching

Run the match-target.sh script:

```bash
plugins/faber/skills/target-matcher/scripts/match-target.sh \
  "$TARGET" \
  --config "$CONFIG_PATH" \
  --project-root "$PROJECT_ROOT"
```

## Step 2: Parse Result

The script returns JSON with:
- `status`: "success", "no_match", or "error"
- `match`: The matched target definition with metadata
- `all_matches`: All matching definitions (for debugging)
- `message`: Human-readable result message

## Step 3: Return Target Context

Return the match result for use by the planner.

</WORKFLOW>

<PATTERN_MATCHING>

## Supported Patterns

The matcher supports glob patterns:
- `*` - Matches anything except `/`
- `**` - Matches any number of path segments
- `?` - Matches single character
- `[abc]` - Character class

**Examples:**
| Pattern | Matches | Does Not Match |
|---------|---------|----------------|
| `ipeds/*` | `ipeds/admissions`, `ipeds/finance` | `ipeds/data/2023` |
| `src/**` | `src/auth/login.ts`, `src/utils.ts` | `test/auth.ts` |
| `plugins/*/` | `plugins/faber/`, `plugins/repo/` | `plugins/faber/skills` |
| `*.md` | `README.md`, `CLAUDE.md` | `src/readme.md` |

## Specificity Rules

When multiple patterns match, specificity determines the winner:

**Scoring Formula:**
```
score = (literal_prefix_length * 100) - (wildcard_count * 10) - definition_index
```

**Example:**
- `src/auth/**` → prefix=9, wildcards=1, index=0 → score=890
- `src/**` → prefix=4, wildcards=1, index=1 → score=389
- Winner: `src/auth/**` (higher score)

**Tie-Breaking:**
If two patterns have identical scores, the first defined pattern wins.
A warning is logged about the ambiguity.

</PATTERN_MATCHING>

<OUTPUTS>

## Success Match
```json
{
  "status": "success",
  "input": "ipeds/admissions",
  "match": {
    "name": "ipeds-datasets",
    "pattern": "ipeds/*",
    "type": "dataset",
    "description": "IPEDS education datasets for ETL processing",
    "metadata": {
      "entity_type": "dataset",
      "processing_type": "etl",
      "expected_artifacts": ["processed_data", "validation_report"]
    },
    "workflow_override": null,
    "score": 490,
    "specificity": {
      "literal_prefix_length": 5,
      "wildcard_count": 1,
      "definition_index": 0
    }
  },
  "all_matches": [...],
  "message": "Matched 'ipeds/admissions' to 'ipeds-datasets'"
}
```

## No Match (with default)
```json
{
  "status": "no_match",
  "input": "unknown/path",
  "match": {
    "name": null,
    "pattern": null,
    "type": "file",
    "description": "Default target type (no pattern matched)",
    "metadata": {},
    "workflow_override": null
  },
  "all_matches": [],
  "message": "No pattern matched 'unknown/path', using default type 'file'"
}
```

## Error (require_match=true)
```json
{
  "status": "error",
  "input": "unknown/path",
  "match": null,
  "all_matches": [],
  "message": "No target definition matches 'unknown/path'. Configure targets in .fractary/plugins/faber/config.json"
}
```

</OUTPUTS>

<ERROR_HANDLING>

| Error | Action |
|-------|--------|
| Config not found | Return no_match with default type |
| No targets section | Return no_match with default type |
| Invalid JSON | Return error status |
| No match + require_match=true | Return error status |

</ERROR_HANDLING>

<INTEGRATION>

## Used By
- `faber-planner` agent - To resolve target context before creating plans

## Configuration
Targets are configured in `.fractary/plugins/faber/config.json`:

```json
{
  "targets": {
    "definitions": [
      {
        "name": "ipeds-datasets",
        "pattern": "ipeds/*",
        "type": "dataset",
        "description": "IPEDS education datasets",
        "metadata": {
          "entity_type": "dataset",
          "processing_type": "etl"
        }
      }
    ],
    "default_type": "file",
    "require_match": false
  }
}
```

See the config schema at `plugins/faber/config/config.schema.json` for full documentation.

</INTEGRATION>
