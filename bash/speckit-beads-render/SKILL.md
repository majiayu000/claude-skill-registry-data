---
name: speckit-beads-render
description: Render tasks.md as a compatibility projection of Beads
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Sidekick contributors
  source: beads:commands/speckit.beads.render.md
---

## User Input

```text
$ARGUMENTS
```

Render a read-compatible `tasks.md` from the current feature's Beads graph when a core Spec Kit command requires it.

1. Resolve the current feature directory with `.specify/scripts/bash/check-prerequisites.sh --json --require-spec`.
2. Preview the generated Markdown:

   ```bash
   python3 .specify/extensions/beads/scripts/beads_tasks.py render \
     --project-root "$PWD" --feature <feature-directory-name>
   ```

3. If the user requested a file—or the next command requires `tasks.md`—write the projection:

   ```bash
   python3 .specify/extensions/beads/scripts/beads_tasks.py render \
     --project-root "$PWD" --feature <feature-directory-name> \
     --output <FEATURE_DIR>/tasks.md --apply
   ```

The generated file must say that it is derived from Beads. Do not infer status from an existing `tasks.md`; closed Beads issues render checked and all other statuses render unchecked. Re-render when compatibility consumers need a fresh snapshot, and never edit the generated checklist as the execution source of truth.