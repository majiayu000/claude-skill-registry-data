---
name: jade-recipe-1.7-1.8-thread-stop-removal
description: >-
  Inspects .stop() calls flagged by THREAD_STOP_DISABLED for actual Thread.stop()
  usage. Most calls are custom .stop() methods in JADE's own classes (Timer.stop(),
  client.stop(), HTTPServer.stop()), not java.lang.Thread.stop(Throwable). Marks
  false positives as SKIPPED. If actual Thread.stop() is found, defers for
  manual review via JADE-MODERNIZATION-DEFERRED marker. Invoked by
  jade-core-rule-dispatcher.
arguments: [--file, --line]
---

# jade-recipe-1.7-1.8-thread-stop-removal

Inspects `.stop()` calls flagged by `THREAD_STOP_DISABLED`. Java 8 disabled
`Thread.stop(Throwable)` for safety; most `.stop()` calls in JADE are custom
methods on application-level classes (e.g., `Timer.stop()`, `HTTPServer.stop()`,
`UDPMonitorServer.stop()`, `PersistentDeliveryManager.stop()`).

## Invocation

```
python .claude/skills/java-migration-skill-registry/1.7-to-1.8/jade-recipe-1.7-1.8-thread-stop-removal/scripts/apply.py --file <path> --line <N>
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success (FIXED or SKIPPED) |
| 2 | Failure (file not found, line out of range) |
| 3 | Environment error |

## Output

One JSON line to stdout:
```json
{"status": "FIXED|SKIPPED|FAILED", "changes": N, "warnings": [], "errors": [], "diff_summary": "..."}
```

## Transform behavior

1. Scans flagged line and nearby lines for the `// JADE-FLAG:THREAD_STOP_DISABLED` marker
2. Finds the associated code line with the `.stop()` call
3. Checks if it matches `Thread.stop(` or `thread.stop(` pattern (actual Java Thread.stop)
4. If actual Thread.stop(): rewrites flag to `// JADE-MODERNIZATION-DEFERRED:THREAD_STOP_DISABLED` for manual review
5. If custom .stop(): rewrites flag to `// JADE-MODERNIZATION-DEFERRED:THREAD_STOP_DISABLED` with informational note
6. All writes use tmp-file + atomic rename
