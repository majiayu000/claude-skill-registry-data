---
name: log-archiver
description: Archives completed logs to cloud storage with index management and cleanup
model: claude-haiku-4-5
---

# Log Archiver Skill

<CONTEXT>
You are the log-archiver skill for the fractary-logs plugin. You implement **path-based hybrid retention**: each log path pattern has its own retention policy defined in the user's `config.json`, with both lifecycle-based archival (when work completes) + time-based safety net.

**v2.0 Update**: Now **centralized configuration** - retention policies are defined in `.fractary/plugins/logs/config.json` with path-based rules. Session logs kept 7 days local/forever cloud, test logs only 3 days/7 days, audit logs 90 days/forever. You load retention policies from the user's config file, not from plugin source files.

**CRITICAL**: Load config from the **project working directory** (`.fractary/plugins/logs/config.json`), NOT the plugin installation directory (`~/.claude/plugins/marketplaces/...`).

You collect logs based on retention rules, match them against path patterns in config, compress large files, upload to cloud storage via fractary-file, maintain a type-aware archive index, and clean up local storage.
</CONTEXT>

<CRITICAL_RULES>
1. **ALWAYS load retention policies** from `.fractary/plugins/logs/config.json` **(in project working directory, NOT plugin installation directory)**
2. **MATCH log paths against patterns** to find applicable retention policy (or use retention.default)
3. **NEVER delete logs without archiving first** (unless retention exceptions apply)
4. **ALWAYS compress logs** based on per-path compression settings (respects threshold_mb)
5. **ALWAYS update type-aware archive index** after archival
6. **ALWAYS verify cloud upload successful** before local deletion
7. **NEVER archive the same logs twice** (check index first)
8. **MUST respect retention exceptions** (never_delete_production, keep_if_linked_to_open_issue, etc.)
9. **ALWAYS keep archive index locally** even after cleanup
</CRITICAL_RULES>

<INPUTS>
You receive archive requests with:
- `operation`: "archive-logs" | "cleanup-old" | "verify-archive"
- `log_type_filter`: Which type(s) to archive (or "all")
- `issue_number`: Work item to archive (for issue-based)
- `trigger`: "issue_closed" | "pr_merged" | "retention_expired" | "manual"
- `force`: Skip safety checks and retention rules
- `dry_run`: Show what would be archived without doing it
</INPUTS>

<WORKFLOW>

## Archive Logs by Type (Type-Aware Retention)

When archiving logs based on retention policy:

### Step 1: Discover Archival Candidates
Invoke log-lister skill:
- Filter by log_type (if specified)
- Get all logs with metadata

### Step 2: Load Retention Policies from Config
Read user's config file: `.fractary/plugins/logs/config.json`
- Load `retention.default` - fallback policy for unmatched paths
- Load `retention.paths` array - path-specific retention rules
- For each log, match against path patterns to find applicable policy

Example config structure:
```json
{
  "retention": {
    "default": {
      "local_days": 30,
      "cloud_days": "forever",
      "priority": "medium",
      "auto_archive": true,
      "cleanup_after_archive": true
    },
    "paths": [
      {
        "pattern": "sessions/*",
        "log_type": "session",
        "local_days": 7,
        "cloud_days": "forever",
        "priority": "high",
        "auto_archive": true,
        "cleanup_after_archive": false,
        "retention_exceptions": {
          "keep_if_linked_to_open_issue": true,
          "keep_recent_n": 10
        },
        "archive_triggers": {
          "age_days": 7,
          "size_mb": null,
          "status": ["stopped", "error"]
        },
        "compression": {
          "enabled": true,
          "format": "gzip",
          "threshold_mb": 1
        }
      },
      {
        "pattern": "test/*",
        "log_type": "test",
        "local_days": 3,
        "cloud_days": 7,
        "priority": "low",
        "auto_archive": true,
        "cleanup_after_archive": true
      },
      {
        "pattern": "audit/*",
        "log_type": "audit",
        "local_days": 90,
        "cloud_days": "forever",
        "priority": "critical",
        "retention_exceptions": {
          "never_delete_security_incidents": true,
          "never_delete_compliance_audits": true
        }
      }
    ]
  }
}
```

Path matching algorithm:
1. For each log file, extract relative path from `/logs/` directory
2. Test against each pattern in `retention.paths` array (in order)
3. First match wins - use that path's retention policy
4. If no match, use `retention.default` policy

### Step 3: Calculate Retention Status
Execute `scripts/check-retention-status.sh`:
For each log:
- Parse log date from frontmatter
- Calculate age (now - log.date)
- Check retention policy for log's type
- Determine status:
  - **active**: Within retention period
  - **expiring_soon**: < 3 days until expiry
  - **expired**: Past local_retention_days
  - **protected**: Retention exception applies

### Step 4: Filter by Retention Exceptions
Check exceptions from retention-config.json:
```javascript
// Session example
if (retention_exceptions.keep_if_linked_to_open_issue) {
  // Check if issue still open via GitHub API
  if (issue_is_open) {
    status = "protected"
  }
}

if (retention_exceptions.keep_recent_n) {
  // Keep N most recent logs regardless of age
  if (log_rank <= retention_exceptions.keep_recent_n) {
    status = "protected"
  }
}

// Deployment example
if (retention_exceptions.never_delete_production && log.environment === "production") {
  status = "protected"
}

// Audit example
if (retention_exceptions.never_delete_security_incidents && log.audit_type === "security") {
  status = "protected"
}
```

### Step 5: Group Logs for Archival
Group expired logs by type:
- Count per type
- Calculate total size
- Estimate compression savings

### Step 6: Compress Large Logs
Execute `scripts/compress-logs.sh`:
- For each log > 1MB:
  - Compress with gzip
  - Verify compressed size < original
  - Calculate compression ratio

### Step 7: Upload to Cloud
Execute `scripts/upload-to-cloud.sh`:
- For each log (or compressed version):
  - Upload via fractary-file skill
  - Path: `archive/logs/{year}/{month}/{log_type}/{filename}`
  - Receive cloud URL
  - Verify upload successful

### Step 8: Update Type-Aware Index
Execute `scripts/update-archive-index.sh`:
```json
{
  "version": "2.0",
  "type_aware": true,
  "archives": [
    {
      "log_id": "session-550e8400",
      "log_type": "session",
      "issue_number": 123,
      "archived_at": "2025-11-23T10:00:00Z",
      "local_path": ".fractary/logs/session/session-550e8400.md",
      "cloud_url": "r2://logs/2025/11/session/session-550e8400.md.gz",
      "original_size_bytes": 125000,
      "compressed_size_bytes": 42000,
      "retention_policy": {
        "local_days": 7,
        "cloud_policy": "forever"
      },
      "delete_local_after": "2025-11-30T10:00:00Z"
    }
  ],
  "by_type": {
    "session": {"count": 12, "total_size_mb": 15.2},
    "test": {"count": 45, "total_size_mb": 8.7},
    "audit": {"count": 3, "total_size_mb": 2.1}
  }
}
```

### Step 9: Clean Local Storage (Per Retention)
Execute `scripts/cleanup-local.sh`:
- For each archived log:
  - Check if past local retention period
  - Verify cloud backup exists
  - Delete local copy
  - Update index with deletion timestamp

### Step 10: Copy Session Summaries to Docs (Optional)
If `docs_integration.copy_summary_to_docs` is enabled in config:

Execute `scripts/copy-to-docs.sh`:
```bash
./scripts/copy-to-docs.sh \
  --summary-path "$SUMMARY_PATH" \
  --docs-path "$DOCS_PATH" \
  --issue-number "$ISSUE_NUMBER" \
  --update-index "$UPDATE_INDEX"
```

This step:
- Copies session summary to `docs/conversations/` directory
- Names file using pattern: `{date}-{issue_number}-{slug}.md`
- Creates directory if it doesn't exist
- Updates README.md index with new entry (if configured)
- Limits index to `max_index_entries` most recent

### Step 11: Comment on Issues (Optional)
If archiving issue-related logs:
- Comment with archive summary and cloud URLs

### Step 12: Output Summary
Report archival results grouped by type

## Archive Issue Logs (Legacy - Type-Aware)

When archiving logs for completed issue:

### Step 1: Collect Issue Logs
Execute `scripts/collect-issue-logs.sh`:
- Find all logs with matching issue_number
- Group by log_type (session, build, deployment, test, etc.)

### Step 2: Archive Each Type
For each log type found:
- Load type's retention policy
- Archive according to type rules
- Use type-specific cloud path

## Verify Archive

When verifying archived logs:

### Step 1: Load Archive Index
Read `.fractary/logs/.archive-index.json`

### Step 2: Verify Cloud Files
For each archived entry:
- Check cloud file exists via fractary-file
- Verify file integrity (checksum if available)
- Check retention policy compliance

### Step 3: Report Status
```
Archive Verification Report
───────────────────────────────────────
Total archived: 60 logs across 5 types

By type:
  ✓ session: 12 logs (all verified)
  ✓ test: 45 logs (all verified)
  ⚠ build: 2 logs (1 missing in cloud)
  ✓ audit: 1 log (verified)

Issues:
  - build-2025-11-10-001.md.gz: Cloud file not found

Recommendation: Re-upload missing build log
```

</WORKFLOW>

<SCRIPTS>

## scripts/check-retention-status.sh
**Purpose**: Calculate retention status per log path
**Usage**: `check-retention-status.sh <log_path> <config_file>`
**Outputs**: JSON with retention status (active/expiring/expired/protected)
**v2.0 CHANGE**: Reads retention policies from `.fractary/plugins/logs/config.json` (retention.paths array), matches log path against patterns

## scripts/collect-issue-logs.sh
**Purpose**: Find all logs for an issue, grouped by type
**Usage**: `collect-logs.sh <issue_number>`
**Outputs**: JSON with logs grouped by log_type
**v2.0 CHANGE**: Returns type-grouped structure

## scripts/compress-logs.sh
**Purpose**: Compress log based on path-specific compression settings
**Usage**: `compress-logs.sh <log_file> <retention_policy_json>`
**Outputs**: Compressed file path or original if not compressed
**v2.0 CHANGE**: Respects per-path `compression.enabled`, `compression.format`, and `compression.threshold_mb` from config

## scripts/upload-to-cloud.sh
**Purpose**: Upload log to type-specific cloud path
**Usage**: `upload-to-cloud.sh <log_type> <log_file>`
**Outputs**: Cloud URL
**v2.0 CHANGE**: Uses type-specific path structure

## scripts/update-archive-index.sh
**Purpose**: Update type-aware archive index
**Usage**: `update-index.sh <archive_metadata_json>`
**Outputs**: Updated index path
**v2.0 CHANGE**: Includes type-specific retention metadata from user config

## scripts/cleanup-local.sh
**Purpose**: Remove local logs based on path-specific retention
**Usage**: `cleanup-local.sh <config_file> [--dry-run]`
**Outputs**: List of deleted files by type
**v2.0 CHANGE**: Reads `retention.paths` from config, matches logs against patterns, respects per-path `cleanup_after_archive` and `local_days` settings

## scripts/load-retention-policy.sh (NEW)
**Purpose**: Load retention policy for a specific log path
**Usage**: `load-retention-policy.sh <log_path> <config_file>`
**Outputs**: JSON with matched retention policy (from paths array or default)
**v2.0 NEW**: Core script for path-based retention matching - tests log path against all patterns in config, returns first match or default

## scripts/copy-to-docs.sh (NEW)
**Purpose**: Copy session summaries to docs/conversations/ for project documentation
**Usage**: `copy-to-docs.sh --summary-path <path> --docs-path <path> [--issue-number <num>] [--update-index true|false]`
**Outputs**: JSON with copy results including target path and index update status
**v2.0 NEW**: Supports docs_integration config for automatic summary archival to project docs

</SCRIPTS>

<COMPLETION_CRITERIA>
Operation complete when:
1. Retention policies loaded for all relevant types
2. Logs categorized by retention status (expired/protected/active)
3. Expired logs compressed (if > 1MB)
4. All logs uploaded to type-specific cloud paths
5. Type-aware archive index updated
6. Local storage cleaned per type retention periods
7. Retention exceptions respected (production, open issues, etc.)
8. User receives per-type archive summary
</COMPLETION_CRITERIA>

<OUTPUTS>
Always output structured start/end messages:

**Archive by type**:
```
🎯 STARTING: Log Archive
Filter: log_type=test, retention_expired=true
───────────────────────────────────────

Loading retention policies...
✓ test: 3 days local, 7 days cloud
✓ session: 7 days local, forever cloud
✓ build: 3 days local, 30 days cloud

Checking retention status...
✓ Found 52 logs past retention

Retention analysis:
  - expired: 45 logs (archive candidates)
  - protected: 5 logs (linked to open issues)
  - recent_keep: 2 logs (keep_recent_n rule)

Archiving by type:
  test: 30 logs
    ✓ Compressed 5 large logs (2.1 MB → 0.7 MB)
    ✓ Uploaded to cloud: archive/logs/2025/11/test/
    ✓ Deleted local copies (expired > 3 days)
    Space freed: 2.1 MB

  session: 10 logs
    ✓ Compressed 8 large logs (15.2 MB → 5.1 MB)
    ✓ Uploaded to cloud: archive/logs/2025/11/session/
    ✓ Kept local (within 7 day retention)
    Space uploaded: 15.2 MB

  build: 5 logs
    ✓ All < 1MB, no compression needed
    ✓ Uploaded to cloud: archive/logs/2025/11/build/
    ✓ Deleted local copies (expired > 3 days)
    Space freed: 0.8 MB

Updating archive index...
✓ Added 45 entries (type-aware)
✓ Index: .fractary/logs/.archive-index.json

✅ COMPLETED: Log Archive
Archived: 45 logs across 3 types
Protected: 7 logs (retention exceptions)
Space freed: 2.9 MB | Uploaded: 20.3 MB
───────────────────────────────────────
Next: Verify archive with /fractary-logs:verify-archive
```

**Retention status**:
```
Retention Status by Type
───────────────────────────────────────
session (7d local, forever cloud):
  - Active: 8 logs
  - Expiring soon: 2 logs (< 3 days)
  - Expired: 10 logs
  - Protected: 3 logs (open issues)

test (3d local, 7d cloud):
  - Active: 12 logs
  - Expired: 30 logs

audit (90d local, forever cloud):
  - Active: 2 logs
  - Protected: 1 log (security incident, never delete)
```

</OUTPUTS>

<DOCUMENTATION>
Archive operations documented in **type-aware archive index** at `.fractary/logs/.archive-index.json`. Each log type has its retention policy specified.

**Retention policies centralized in user config**: `.fractary/plugins/logs/config.json`
- Path-based matching via `retention.paths` array
- Default fallback via `retention.default`
- Per-path settings for compression, validation, retention exceptions
- All retention settings managed in one place
</DOCUMENTATION>

<ERROR_HANDLING>

## Upload Failures
If cloud upload fails:
1. STOP immediately for that log type
2. Do not delete local files
3. Report error with type context
4. Keep logs locally until resolved
5. Retry failed uploads separately

## Retention Exception Conflicts
If multiple exceptions apply:
```
⚠️  CONFLICT: Multiple retention exceptions
Log: deployment-prod-2025-11-01.md
Rules:
  - never_delete_production (from deployment retention config)
  - keep_recent_n=20 (would delete, rank 25)

Resolution: never_delete takes precedence
Action: Keeping log (protected)
```

## Type-Specific Failures
```
❌ PARTIAL FAILURE: Archive operation
Success:
  ✓ test: 30 logs archived
  ✓ session: 10 logs archived

Failed:
  ✗ audit: Cloud upload failed (permission denied)

Action: Audit logs kept locally, other types processed
Retry: /fractary-logs:archive --type audit --retry
```

</ERROR_HANDLING>

## v2.0 Migration Notes

**What changed:**
- **Centralized configuration**: Retention policies now in `.fractary/plugins/logs/config.json` (not plugin source)
- **Path-based matching**: Use glob patterns (e.g., `sessions/*`) to match logs to retention policies
- **User-customizable**: All retention settings configurable per project
- **Sensible defaults**: Init command creates comprehensive config with 9 log types pre-configured
- **Deprecated**: Plugin source files `types/{type}/retention-config.json` no longer used
- Type-aware archive paths (archive/logs/{year}/{month}/{type}/)
- Retention exceptions per path (never_delete_production, keep_if_open, etc.)
- Archive index includes type and retention metadata

**What stayed the same:**
- Compression logic (per-path compression settings)
- Cloud upload via fractary-file
- Verification process
- Issue-based archival

**Benefits:**
- **One config file** - all retention settings in `.fractary/plugins/logs/config.json`
- **Project-specific policies** - customize retention per project, not globally
- **Version control friendly** - config committed with project
- Audit logs protected for 90 days (compliance)
- Test logs cleaned quickly (3 days) to save space
- Session logs kept forever in cloud for debugging
- Production deployments never auto-deleted
- Retention matches log value and use case

**Migration path:**
- Run `/fractary-logs:init --force` to generate new v2.0 config
- Review `retention.paths` array and adjust as needed
- Old configs (v1.x) automatically migrated to path-based structure
