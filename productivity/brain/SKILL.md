---
name: brain
description: "Manage the engagement brain. Subcommands: 'init' to set up, 'brief <target>' for pre-flight, 'status' for overview, 'exhausted [target]' to see dead ends."
disable-model-invocation: false
---
Brain management: $ARGUMENTS

Route to the brain tool:
- If "$ARGUMENTS" is "init": run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py init`
- If "$ARGUMENTS" starts with "brief": run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py brief <target>`
- If "$ARGUMENTS" is "status": run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py status`
- If "$ARGUMENTS" starts with "exhausted": run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py exhausted <target>`
- If "$ARGUMENTS" starts with "record": run `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py record <target> <status> <technique> "<details>"`

After running, also launch the `brain` agent to update the MEMORY.md index if any state changed.

## Top-Tier Memory Bar

Bad memory makes the whole suite worse. Record facts as reusable evidence, not diary entries.

For every record, include:
- `target`: canonical host or repo name
- `surface`: endpoint, file, workflow, account role, or component
- `technique`: vuln class plus variant, not just "tested auth"
- `status`: confirmed, partial, exhausted, blocked, duplicate-risk, chain-pending
- `evidence`: request id, file path, response marker, screenshot path, command output, or blocker
- `next_action`: the exact command or test a future session should run

Never store "no bug" without the tested matrix. An exhausted entry must say what was tried and why that evidence is strong enough to skip it later.
