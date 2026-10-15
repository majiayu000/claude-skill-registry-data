---
name: write-evidence
description: Write a content string to a target path inside the `.garura/` folder whitelist. Enforces whitelist compliance at the write boundary. Used by the scriber agent.
user-invocable: false
model: haiku
allowed-tools: Write, Bash
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# write-evidence

Model-invocable skill for writing evidence, checkpoint, and status files on behalf of plays. Called exclusively by the `scriber` agent.

## Purpose

Write a content string to a target path inside the `.garura/` folder whitelist. Reject any path outside the whitelist. Create parent directories if needed. Return a structured result.

This skill is the single chokepoint for evidence writes in Garura. No other skill or agent writes directly to evidence/checkpoint/status paths. This makes folder-whitelist compliance auditable.

## Input

Receive from the scriber agent:
- `target_path` (string, required) — absolute or project-relative path where content should be written
- `content` (string, required) — the body to write (markdown or YAML)
- `metadata` (object, optional) — fields to stamp into the file header: `play_name`, `issue_number`, `step`, `timestamp`
- `allow_overwrite` (boolean, optional, default `false`) — if `false`, appends a timestamp suffix to `target_path` on collision

## Process

### 1. Validate the target path

Check `target_path` matches one of the whitelist patterns (list below). If it does not, return immediately with:

```yaml
status: failed
failure_reason: whitelist_violation
attempted_path: "{target_path}"
details: "target_path is outside the .garura/ folder whitelist"
```

Whitelist patterns (regex-friendly):

```
^\.garura/core/(?!memory/).*$
^\.garura/product/(product|ux|arch)/.*$
^\.garura/project/issues/[^/]+/(specs|evidence|checkpoint|context|review|status)/.*$
```

`.garura/core/memory/` is gitignored and managed elsewhere — scriber does not touch it.
`status/` is the machine-local sixth key (ADR 021): a permitted write target for resume
markers, but gitignored (`**/status/`) — it never rides a commit.

### 2. Compute final path (handle collisions)

- If `allow_overwrite` is `true` OR the target file does not exist: use `target_path` as-is.
- If `allow_overwrite` is `false` AND the target file already exists: append a timestamp suffix before the extension. Example: `spec.md` → `spec-20260414-201500.md`. Use UTC timestamp in `YYYYMMDD-HHMMSS` format.

### 3. Ensure parent directory exists

```bash
mkdir -p "$(dirname "{final_path}")"
```

Only run this inside `.garura/` — the whitelist check already confirmed the path is inside. If `mkdir` fails (permission denied), return:

```yaml
status: failed
failure_reason: permission_error
attempted_path: "{final_path}"
details: "{mkdir stderr}"
```

### 4. Stamp metadata header (if new file + metadata provided)

If this is a new file (collision handling already applied) AND `metadata` is non-empty AND `content` does not already begin with an HTML comment header, prepend an audit header:

```markdown
<!-- Written by scriber | play={play_name} | issue={issue_number} | step={step} | timestamp={timestamp} -->
```

If `content` already begins with `<!--` (caller supplied its own header), do NOT prepend. Idempotence.

### 5. Write the file atomically

Use the `Write` tool to write the (possibly header-stamped) content to `final_path`.

### 6. Measure and return

- `bytes_written` = length of the final content (after header prepend)
- `duration_ms` = approximate wall-clock since step 1 (not required to be precise)

Return:

```yaml
status: completed
written_path: "{final_path}"
bytes_written: {int}
duration_ms: {int}
```

## Output

Return a structured result via the standard skill output channel. On success:

```yaml
status: completed
written_path: "<absolute or project-relative path>"
bytes_written: <int>
duration_ms: <int>
```

On failure:

```yaml
status: failed
failure_reason: "whitelist_violation" | "permission_error" | "disk_error"
attempted_path: "<path>"
details: "<human-readable detail>"
```

## Constraints

- NEVER write to paths outside the whitelist. The first thing you do is validate.
- NEVER overwrite an existing file when `allow_overwrite` is `false` — append a timestamp suffix instead.
- NEVER use `git add`, `git commit`, or any git command. This skill writes files only; git is `repo-orchestrator`'s domain.
- NEVER read files from outside the whitelist as part of template expansion (template expansion is scriber's concern, not this skill's).
- NEVER prepend a metadata header if `content` already starts with one.
- ALWAYS run `mkdir -p` on the parent directory before writing, to handle fresh issue directories.
- ALWAYS return a structured YAML result — never raw prose or plain error text.

## Version

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Category | infra |
| Created | 2026-04-14 |
| Related | `core/components/agents/scriber.md`, `docs/adr/017-folder-whitelist.md` (pending) |
