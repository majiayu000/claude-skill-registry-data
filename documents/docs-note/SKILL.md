---
name: docs-note
description: Record a change to a binding doc (a feature spec or an architecture spec) as a one-line change note, and fold notes at release. Use whenever a task changes the behaviour a spec describes, when the Stop hook says code changed without docs, or when a release branch must fold notes into one version row per doc.
model: sonnet
effort: medium
---

# Docs — change note and fold

Runs `scripts/docs_fold.py` (DOCSPEC §7). A branch never edits a version or the Versions table.

```bash
F="${CLAUDE_PLUGIN_ROOT}/scripts/docs_fold.py"
python3 "$F" note --doc features/import --task IW21 --change minor --section 3 \
  --text "Step 3 shows sure matches first (owner decision D4, 2026-10-30)."
python3 "$F" note --doc architecture/security --task SEC4 --change patch --text "Wording."
python3 "$F" note --doc features/import --task IW25 --change minor --breaking --text "Old route removed."
python3 "$F" pending                                  # exit 1 while notes wait
python3 "$F" fold --release RELEASE-131 --dry-run     # release branch only; then without --dry-run
```

`--change` takes `minor` when behaviour is added or changed, and `patch` for wording and doc fixes. Use `--breaking` (major) when something users or other apps relied on is gone. Write one line: what changed, the section, the reason. Then update the doc body in the same branch.

Fold only on the release branch, once per release. The fold bumps each doc once and writes one row.
