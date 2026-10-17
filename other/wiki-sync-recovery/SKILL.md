---
name: wiki-sync-recovery
description: Diagnose a failed GitHub wiki sync (sync-github-wiki.mjs) by matching its log against the four known failure modes and printing the runbook entry for each.
compatibility: |
  - Runtime: Node.js 18+ (no external dependencies)
  - Inputs: a captured wiki-sync log (stdin or --log FILE)
  - Permissions: read:repo
---

# wiki-sync-recovery Specification

**ID**: `wiki-sync-recovery`
**Version**: 0.1.0
**Status**: Experimental
**Owner**: KB / Wiki Sync

---

## Purpose

Turn a failed `npm run wiki:sync` log into an actionable diagnosis. Consolidates
the three fix commits landed 2026-08-29 (`8e7f5603`, `6ecf4cfe`, `d9f0d4dc`) into
a pattern matcher over the script's error output, so a regression is identified in
one step instead of re-derived.

Covered failure modes:

1. `auth-https-url` — clone/push authentication fails because the wiki URL is HTTPS, not SSH.
2. `temp-dir-locked` — pre-clone `fs.rmSync` of `.wiki-publish-temp` throws `EBUSY`/`ENOTEMPTY` on Windows.
3. `missing-root-image` — `validateMarkdownImages` flags a root-relative image reference as missing.
4. `temp-dir-collision` — `git clone` aborts because the temp dir already exists (overlapping runs).

---

## Trigger

```
node scripts/sync-github-wiki.mjs 2>&1 | node skills/wiki-sync-recovery/src/diagnose.mjs
```

Or against a saved log:

```
node skills/wiki-sync-recovery/src/diagnose.mjs --log C:\dev\logs\wiki-sync.log
```

---

## Input Schema

```typescript
interface SkillInput {
  log: string;        // Required. Wiki-sync stdout+stderr, via stdin or --log FILE.
  json?: boolean;     // Optional. Emit machine-readable output instead of text.
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "matched" | "no-match";
  matched: Array<{
    id: string;        // failure-mode id
    title: string;
    commit: string;    // fix commit that addressed it
    cause: string;
    fixed: string;     // where the fix lives (file:line)
    action: string[];  // operator steps if it regressed
  }>;
  timestamp: string;
}
```

Exit codes: `0` at least one mode matched, `1` no match, `2` bad input.

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling).

| Code | Message | Handler |
|------|---------|---------|
| `NO_INPUT` | No log on stdin and no `--log` given | exit 2 |
| `LOG_NOT_FOUND` | `--log` path does not exist | exit 2 |
| `NO_MATCH` | Log matched no known failure mode | exit 1, print known mode ids |

---

## Full Reference

- Runbook, per-mode detail, worked examples: [docs/USAGE.md](./docs/USAGE.md)
- Setup, testing, integration: [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)
