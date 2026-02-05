---
name: eld-record-memory-collector
description: Collect and verify project information for pce-memory with multi-model validation using Codex CLI. Use when gathering project context, onboarding to a new codebase, or building a knowledge base. Triggers on "collect project info", "build knowledge base", "index this project", or "remember this codebase".
---

# PCE Memory Collector

Collect project information with multi-model verification to ensure accuracy.

## Workflow

```
Loop 1: Collect   →  observe(ttl=7, unverified)
Loop 2: Verify    →  Codex cross-check → observe+extract(verified)
Loop 3: Validate  →  hash/diff check → feedback
```

## Loop 1: Initial Collection

1. Scan project structure:
   ```bash
   scripts/scan_project.py <project_path>
   ```

2. Read key files and record with observe:
   ```
   observe(
     source_type="file",
     content="<extracted info>",
     source_id="<file_path>",
     ttl_days=7,
     boundary_class="public|internal",
     tags=["unverified", "<category>"]
   )
   ```

3. Categories: `project-info`, `architecture`, `dependencies`, `api`, `config`

## Loop 2: Multi-Model Verification

Cross-validate with Codex CLI:

```
mcp__codex-cli__codex(
  prompt="Verify this claim against the file content:
    Claim: <claim_text>
    File: <file_path>
    Content: <file_content>

    Respond: MATCH | MISMATCH | PARTIAL
    Reason: <brief explanation>"
)
```

**Decision Matrix:**

| Codex Result | Action |
|--------------|--------|
| MATCH | `observe(..., extract={mode: "single_claim_v0"})` → permanent |
| PARTIAL | Refine claim, re-verify |
| MISMATCH | Discard (let ttl expire) |

## Loop 3: Hash-Based Validation

Run validation script:
```bash
scripts/validate_claims.py <project_path>
```

The script:
1. Activates all project claims
2. Computes current file hashes
3. Compares with stored provenance
4. Outputs: `VALID | OUTDATED | MISSING`

Send feedback:
```
feedback(claim_id, signal="helpful|outdated", score)
```

## Quick Start

```
1. scan_project.py /path/to/project     # Discover files
2. [Manual] Read files, observe         # Loop 1
3. [Codex] Cross-validate               # Loop 2
4. validate_claims.py /path/to/project  # Loop 3
```

## Scripts

- `scripts/scan_project.py` - Scan project and output key files
- `scripts/validate_claims.py` - Hash-based claim validation

## References

- `references/pce_memory_api.md` - pce-memory tool reference
