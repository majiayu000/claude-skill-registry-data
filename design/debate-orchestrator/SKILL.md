---
name: debate-orchestrator
description: Orchestrates formal debates with proposition and opposition sides, coordinating debaters and judges through structured exchanges. Use when running debate exchanges, managing debate rounds, or continuing interrupted debates.
---

# Debate Orchestrator

Manages formal debate execution through deterministic state tracking and resumability.

## State Machine

Debates cycle through 2 phases per exchange:

| current_phase | Action Required |
|---------------|-----------------|
| `awaiting_arguments` | Spawn both debaters in parallel |
| `awaiting_judgment` | Spawn judge to evaluate all new arguments |

After judgment: cycle repeats with `current_exchange` incremented.

**Key Properties:**
- No "complete" state - orchestrator decides when to stop based on requested exchange count
- Parallel execution - both sides argue simultaneously each exchange
- Resumable - read state, execute required action, repeat
- Exchange 0 is special (opening) - both sides produce 3 independent arguments
- Exchange 1+ are rebuttal - sides produce single arguments with attacks/defends

## Running Exchanges

### 1. Read State

Check `{debate}/debate.md` frontmatter (JSON format):
```json
{
  "current_exchange": 0,
  "current_phase": "awaiting_arguments"
}
```

Extract motion from the `# Motion` section (first markdown heading after frontmatter).

### 2. Determine Exchange Type

**Opening Exchange**: `current_exchange == 0`
- Both debaters produce 3 independent arguments simultaneously
- Judge scores all 6 arguments

**Rebuttal Exchange**: `current_exchange >= 1`
- Both debaters produce 1 argument simultaneously
- Judge scores both new arguments

### 3. Execute Based on Phase + Exchange Type

#### Opening Exchange (Exchange 0)

When `current_exchange == 0` and `current_phase == awaiting_arguments`:

**Load template:**

Read `templates/debater-opening.md` from this skill's directory.

**Spawn both debaters in parallel:**

Use a single message with two Task tool invocations to spawn both debaters simultaneously.

For each side (`proposition` and `opposition`):

1. Substitute placeholders in template:
   - `{motion}`: Extracted motion text
   - `{side}`: Side name (`proposition` or `opposition`)

2. Spawn debater:
   ```
   Use Task tool with subagent_type: "debater"
   Prompt: [substituted template content]
   ```

**Process outputs:**

After both debaters complete:

1. Write proposition output to `/tmp/prop_arg.json`
2. Write opposition output to `/tmp/opp_arg.json`
3. Execute the python package `debate_ops`: `python3 {skill_base_dir}/debate_ops process-exchange {debate} 0 --prop-file /tmp/prop_arg.json --opp-file /tmp/opp_arg.json`

Check result JSON for errors or warnings. On errors, state remains unchanged - report to user and halt. On warnings, note them and continue.

The script creates 6 argument files: `prop_000a.md`, `prop_000b.md`, `prop_000c.md`, `opp_000a.md`, `opp_000b.md`, `opp_000c.md`

State automatically updates to `current_phase: awaiting_judgment`.

**Judge opening arguments:**

When `current_exchange == 0` and `current_phase == awaiting_judgment`:

**Load template:**

Read `templates/judge.md` from this skill's directory.

**Substitute placeholders:**

- `{argument_files}`: Space-separated list of all 6 opening arguments:
  ```
  @{debate}/arguments/prop_000a.md @{debate}/arguments/prop_000b.md @{debate}/arguments/prop_000c.md @{debate}/arguments/opp_000a.md @{debate}/arguments/opp_000b.md @{debate}/arguments/opp_000c.md
  ```
- `{motion}`: Extracted motion text

**Spawn judge:**

```
Use Task tool with subagent_type: "judge"
Prompt: [substituted template content]
```

**Process output:**

1. Use Write tool to save agent output to `/tmp/judge.json`
2. Execute the python package `debate_ops`: `python3 {skill_base_dir}/debate_ops process-judge {debate} --json-file /tmp/judge.json`

Check result JSON for errors or warnings. On errors, state remains unchanged - report to user and halt. On warnings, note them and continue.

State automatically updates to `current_phase: awaiting_arguments`, `current_exchange: 1`.

#### Rebuttal Exchange (Exchange 1+)

When `current_exchange >= 1` and `current_phase == awaiting_arguments`:

**Build argument context:**

1. List all files in `{debate}/arguments/`
2. Separate into proposition and opposition arguments:
   - Proposition: Files matching `prop_*.md`
   - Opposition: Files matching `opp_*.md`
3. Filter to arguments from previous exchanges only:
   - Extract exchange number from filename (e.g., `prop_003` → exchange 3)
   - Include only arguments where exchange < current_exchange
4. Sort by exchange number (chronological order)

**Load template:**

Read `templates/debater-rebuttal.md` from this skill's directory.

**Spawn both debaters in parallel:**

Use a single message with two Task tool invocations to spawn both debaters simultaneously.

For proposition debater:
- Substitute placeholders:
  - `{motion}`: Extracted motion text
  - `{side}`: `proposition`
  - `{exchange}`: Current exchange number
  - `{your_arguments}`: Newline-separated list: `@{debate}/arguments/prop_000a.md`, `@{debate}/arguments/prop_000b.md`, etc.
  - `{opponent_arguments}`: Newline-separated list: `@{debate}/arguments/opp_000a.md`, `@{debate}/arguments/opp_000b.md`, etc.

For opposition debater:
- Substitute placeholders:
  - `{motion}`: Extracted motion text
  - `{side}`: `opposition`
  - `{exchange}`: Current exchange number
  - `{your_arguments}`: Newline-separated list of opposition arguments
  - `{opponent_arguments}`: Newline-separated list of proposition arguments

**Process outputs:**

After both debaters complete:

1. Write proposition output to `/tmp/prop_arg.json`
2. Write opposition output to `/tmp/opp_arg.json`
3. Execute the python package `debate_ops`: `python3 {skill_base_dir}/debate_ops process-exchange {debate} {current_exchange} --prop-file /tmp/prop_arg.json --opp-file /tmp/opp_arg.json`

Check result JSON for errors or warnings. On errors, state remains unchanged - report to user and halt. On warnings, note them and continue.

State automatically updates to `current_phase: awaiting_judgment`.

**Judge rebuttal arguments:**

When `current_exchange >= 1` and `current_phase == awaiting_judgment`:

**Load template:**

Read `templates/judge.md` from this skill's directory.

**Substitute placeholders:**

- `{argument_files}`: Space-separated list of both new arguments:
  ```
  @{debate}/arguments/prop_{current_exchange:03d}.md @{debate}/arguments/opp_{current_exchange:03d}.md
  ```
- `{motion}`: Extracted motion text

**Spawn judge:**

```
Use Task tool with subagent_type: "judge"
Prompt: [substituted template content]
```

**Process output:**

1. Use Write tool to save agent output to `/tmp/judge.json`
2. Execute the python package `debate_ops`: `python3 {skill_base_dir}/debate_ops process-judge {debate} --json-file /tmp/judge.json`

Check result JSON for errors or warnings. On errors, state remains unchanged - report to user and halt. On warnings, note them and continue.

State automatically updates to `current_phase: awaiting_arguments`, `current_exchange` incremented.

### 4. Decide When to Stop

After each phase, check if you should continue:
- Read the updated state from `{debate}/debate.md`
- Compare current exchange number to requested total exchanges
- If sufficient exchanges completed: stop and report
- Otherwise: loop back to step 1

The state itself doesn't track "completion" - you decide when done based on user request.

## Error Handling

Processing scripts return:
```json
{
  "success": true/false,
  "argument_id": "prop_001" | ["prop_000a", "prop_000b", "prop_000c"],
  "errors": ["fatal errors"],
  "warnings": ["non-fatal warnings"]
}
```

**On errors:**
- State remains unchanged - can safely retry
- Report error to user
- Ask how to proceed (retry, skip, abort)

**On warnings:**
- Note them
- Continue execution
- Mention warnings in completion summary

Note: By default the `tmp` files get deleted by the script. But if you face errors while writing to a `tmp` file because it already exists, just `Read` it and try again.

## Resumability

Execution can be interrupted at any point and resumed by reading state:
- State indicates exactly what phase is needed next
- Execute that phase
- State updates atomically on success
- On failure, state remains unchanged - retry is safe

## Completion Report

When requested exchanges complete, report current state:

```
✓ Completed {N} exchanges for '{debate_slug}'

**Current Scores** (zero-sum tug-of-war):
- Proposition: {total} ({count} arguments)
- Opposition: {total} ({count} arguments)

**Next steps**:
- Continue debating: `/debate-run {debate_slug} X` to run X more exchanges
- Generate report: `/debate-report {debate_slug}` to create comprehensive analysis with visualizations
```

Extract totals and counts from `cumulative_scores` in `{debate}/debate.md` frontmatter.
Total exchanges = current_exchange from debate.md.

**Note on zero-sum scoring:** Positive total = winning, negative total = losing, zero = even. One side typically has positive total, the other negative (tug-of-war).
