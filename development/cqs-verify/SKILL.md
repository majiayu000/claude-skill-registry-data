---
name: cqs-verify
description: Verify all cqs features work. Run on session start and after compaction.
---

# Verify cqs

Quick functional test of all cqs command categories. Exercises the full tool to build grounded understanding of what it does — not just what docs say.

## When to run

- **Session start** (after reading tears)
- **After context compaction**
- **After any release or binary update**

## Process

Run each command, check for errors. Report pass/fail summary.

```bash
# Redirect stderr to suppress tracing noise in JSON output
echo "=== cqs verify ===" && echo "Version: $(cqs --version 2>&1)"

# 1. Search (semantic)
echo "1. search:" && cqs "error handling" --json -n 3 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS ({len(r[\"results\"])} results)')" 2>&1 || echo "  FAIL"

# 2. Name lookup
echo "2. name-only:" && cqs "Store" --name-only --json -n 3 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS ({len(r[\"results\"])} results)')" 2>&1 || echo "  FAIL"

# 3. Read
echo "3. read:" && cqs read src/lib.rs 2>/dev/null | head -1 | grep -q . && echo "  PASS" || echo "  FAIL"

# 4. Callers
echo "4. callers:" && cqs callers search_filtered --json 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS ({r[\"count\"]} callers)')" 2>&1 || echo "  FAIL"

# 5. Callees
echo "5. callees:" && cqs callees search_filtered --json 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS ({r[\"count\"]} callees)')" 2>&1 || echo "  FAIL"

# 6. Explain
echo "6. explain:" && cqs explain search_filtered --json 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS (callers:{len(r.get(\"callers\",[]))}, callees:{len(r.get(\"callees\",[]))})')" 2>&1 || echo "  FAIL"

# 7. Impact
echo "7. impact:" && cqs impact search_filtered --json 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS (callers:{len(r.get(\"callers\",[]))}, tests:{len(r.get(\"tests\",[]))})')" 2>&1 || echo "  FAIL"

# 8. Stats
echo "8. stats:" && cqs stats --json 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS ({r[\"total_chunks\"]} chunks)')" 2>&1 || echo "  FAIL"

# 9. Health
echo "9. health:" && cqs health --json 2>/dev/null | python3 -c "import sys,json; print('  PASS')" 2>&1 || echo "  FAIL"

# 10. Doctor
echo "10. doctor:" && cqs doctor 2>/dev/null | grep -c "✓" | xargs -I{} echo "  PASS ({} checks)"

# 11. Notes
echo "11. notes:" && cqs notes list --json 2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'  PASS ({r[\"count\"]} notes)')" 2>&1 || echo "  FAIL"

# 12. Dead code
echo "12. dead:" && cqs dead --json 2>/dev/null | python3 -c "import sys,json; print('  PASS')" 2>&1 || echo "  FAIL"
```

## Rules

- Any FAIL = investigate before starting work
- Don't skip commands — the point is to exercise the full tool
- Report the summary to the user: "cqs verify: 12/12 pass, N chunks, N notes"
