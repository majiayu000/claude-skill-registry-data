---
name: scaffold-experiment
description: Set up complete experimental infrastructure for all runs in a designed experiment. Orchestrates parallel generation of fine-tuning configs (via scaffold-torchtune) and evaluation configs (via scaffold-inspect). Use after design-experiment to prepare configs before running experiments.
---

# Scaffold Experiment

You help users automatically set up the complete experimental infrastructure - both fine-tuning and evaluation configurations - for all runs in a designed experiment.

## Your Task

Orchestrate the scaffolding process by reading tool specifications from experiment_summary.yaml and launching the appropriate subagents in parallel:

1. Read experiment_summary.yaml to identify which tools are being used
2. Launch the appropriate preparation subagent (currently only `scaffold-torchtune`)
3. Launch the appropriate evaluation subagent (currently only `scaffold-inspect`)
4. Wait for both subagents to complete and report their results

This ensures the entire experiment is ready to execute from training through evaluation. The subagents run in parallel in separate context windows since their outputs do not depend on one another.

**Current tool support:**
- **Preparation:** torchtune only (via `scaffold-torchtune` subagent)
- **Evaluation:** inspect-ai only (via `scaffold-inspect` subagent)

**Future tool support:** This orchestrator is designed to route to different worker subagents based on tool choices documented in experiment_summary.yaml. Future iterations may support additional frameworks.

## Workflow

1. **Locate experiment** - Find the experiment directory (usually current directory or ask user)
2. **Verify experiment_summary.yaml exists** - Ensure design phase is complete
3. **Read tool specifications** - Parse experiment_summary.yaml to identify preparation and evaluation tools
4. **Validate tool support** - Ensure the specified tools have corresponding worker subagents
5. **Launch preparation and evaluation subagents in parallel** - Use Task tool to launch both simultaneously
6. **Wait for both subagents to complete** - Each will report back when done
7. **Create orchestration log** - Document the scaffolding process in `scaffold-experiment.log`
8. **Report combined summary** - Show user complete status of both scaffolding phases

## Finding the Experiment

**If user runs skill without arguments:**
- Check if current directory contains `experiment_summary.yaml`
- If not, ask user for the experiment directory path

**If user provides a path:**
- Use that path as the experiment directory

## Verification Before Starting

Before beginning scaffolding, perform **minimal structural validation**:

1. **experiment_summary.yaml exists:**
   ```bash
   ls {experiment_dir}/experiment_summary.yaml
   ```
   If missing, report error and suggest running `design-experiment` skill first.
   DO NOT launch subagents.

2. **experiment_summary.yaml is readable:**
   ```python
   import yaml
   with open(f"{experiment_dir}/experiment_summary.yaml") as f:
       config = yaml.safe_load(f)
   ```
   If unreadable or invalid YAML, report error. DO NOT launch subagents.

**Note on validation division:**
- **Skill validates:** Structure only (file existence, readability, tool recognition)
- **Agents validate:** Domain-specific content (parameters, paths, configuration)

The subagents (scaffold-torchtune, scaffold-inspect) will perform complete validation of:
- Required parameters presence and validity
- Path accessibility
- Configuration correctness
- Environment settings from claude.local.md

## Tool to Subagent File Mapping

This orchestrator routes to different subagent specifications based on tool choices in experiment_summary.yaml:

**Preparation tools:**
- `torchtune` → [optimizers/torchtune_agent.md](optimizers/torchtune_agent.md)

**Evaluation tools:**
- `inspect-ai` → [evaluators/inspect_agent.md](evaluators/inspect_agent.md)

**Adding new tools:** Create the corresponding agent file (optimizers/{tool}_agent.md or evaluators/{tool}_agent.md) and add to this mapping.

## Reading Tool Specifications

Read experiment_summary.yaml to determine which subagents to launch.

**See [parsing.md](parsing.md) for:**
- How to parse the tools section
- Tool to subagent mapping logic
- Error handling for missing/unsupported tools
- Logging examples

## Orchestration Steps

### How to Launch Worker Subagents

**IMPORTANT:** Use the `Task` tool to launch worker subagents (NOT the `SlashCommand` tool).

**Correct approach for parallel execution:**

Launch both subagents in a single message with multiple Task tool calls. This runs them in parallel.

**Example:**
```
I'll launch both the torchtune and inspect-ai scaffolding subagents in parallel.

[Use Task tool with subagent_type="scaffold-torchtune"]
[Use Task tool with subagent_type="scaffold-inspect"]
```

**Subagent prompts should:**
- Specify the experiment directory path
- Ask the subagent to read experiment_summary.yaml
- Request generation of all necessary configuration files
- Ask for a detailed log file (scaffold-torchtune.log or scaffold-inspect.log)
- Request a summary report of created files and any errors

**Why this matters:**
- Worker subagents like `scaffold-torchtune` and `scaffold-inspect` are launched via the Task tool
- They run in separate context windows (not the main conversation)
- They execute independently and report back when complete
- Running them in parallel saves time since they don't depend on each other

### Step 1: Launch Preparation Subagent

Invoke the appropriate preparation subagent based on tool specification in experiment_summary.yaml.

**For torchtune:** See [optimizers/torchtune_agent.md](optimizers/torchtune_agent.md) for:
- Complete prompt template
- Subagent responsibilities and execution details
- Expected output structure
- Error handling

Launch the subagent using the Task tool with the prompt template from the agent file.

### Step 2: Launch Evaluation Subagent

Invoke the appropriate evaluation subagent based on tool specification in experiment_summary.yaml.

**For inspect-ai:** See [evaluators/inspect_agent.md](evaluators/inspect_agent.md) for:
- Complete prompt template
- Subagent responsibilities and execution details
- Expected output structure
- Error handling

Launch the subagent using the Task tool with the prompt template from the agent file.

### Step 3: Wait for Subagent Completion

**After launching both subagents in parallel:**
- Each subagent will execute autonomously in its own context window
- You will receive a report back from each subagent when it completes
- The reports are returned as tool results from the Task tool calls
- Do NOT proceed until both subagents have reported back

**Processing subagent reports:**
1. Read the response from scaffold-torchtune subagent
   - Extract list of created runs
   - Note any errors or warnings
   - Identify path to scaffold-torchtune.log
2. Read the response from scaffold-inspect subagent
   - Extract list of created evaluation scripts
   - Note any errors or warnings
   - Identify path to scaffold-inspect.log
3. Verify both subagents completed successfully or note failures

## Logging

Create an orchestration log at `{experiment_dir}/scaffold-experiment.log` that records the high-level scaffolding process.

**See [logging.md](logging.md) for:**
- Complete log format specification
- Action types and when to log them
- What to log vs what goes in subagent logs
- Example log entries for all scenarios
- Error handling patterns

**Key principle:** The orchestration log tracks coordination and timing. Detailed implementation goes in subagent logs (scaffold-torchtune.log, scaffold-inspect.log).

## Error Handling

**If experiment_summary.yaml not found:**
- Report error to user
- Suggest running `design-experiment` skill first
- Do not proceed

**If optimization subagent fails:**
- Log the failure with details from subagent report
- Ask user: "Fine-tuning scaffolding failed. Do you want to continue with evaluation scaffolding?"
- If yes, evaluation can still be scaffolded for base model runs
- If no, stop and report failure

**If evaluation subagent fails:**
- Log the failure with details from subagent report
- Note that fine-tuning can still proceed independently
- Report in summary which evaluations couldn't be configured
- Still consider overall scaffolding partially successful

**If both subagents fail:**
- Report complete failure
- Direct user to individual subagent logs (scaffold-torchtune.log, scaffold-inspect.log)
- Suggest checking experiment_summary.yaml for completeness
- May need to run subagents individually for debugging

**If a subagent doesn't report back:**
- This should not happen with the Task tool
- If it does, report the issue and suggest checking the agent configuration
- User may need to run the subagent manually

## Output Summary

After completing orchestration, provide a comprehensive summary:

```markdown
## Scaffold Experiment Complete

Successfully scaffolded experiment:
`/scratch/gpfs/MSALGANIK/niznik/cap_4L_lora_lr_sweep_2025-10-22/`

### Fine-Tuning Configurations (scaffold-torchtune)

✓ 2 runs configured successfully

**Created runs:**
- Llama-3.2-1B-Instruct_rank4/
- Llama-3.2-1B-Instruct_rank8/

**Each run contains:**
- setup_finetune.yaml (configuration)
- finetune.yaml (torchtune config)
- finetune.slurm (SLURM script)

### Evaluation Configurations (scaffold-inspect)

✓ 2 evaluation scripts configured successfully

**Created evaluations:**
- Llama-3.2-1B-Instruct_rank4/eval/capitalization_epoch0.slurm
- Llama-3.2-1B-Instruct_rank8/eval/capitalization_epoch0.slurm

**Each evaluation directory contains:**
- {task}_epoch{N}.slurm (SLURM script)
- logs/ (for inspect-ai output)

### Logs Created

- `scaffold-experiment.log` - Orchestration log (this process)
- `scaffold-torchtune.log` - Fine-tuning scaffolding details
- `scaffold-inspect.log` - Evaluation scaffolding details

### Next Steps

**Recommended workflow:**
1. Review the generated configurations (optional)
2. Run `run-experiment` skill to execute the complete workflow:
   - Fine-tuning via `run-torchtune`
   - Evaluation via `run-inspect`
3. Run `analyze-experiment` skill to interpret results (planned)

## Validation Before Completion

Before reporting success, verify:
- ✓ experiment_summary.yaml was found and read
- ✓ Optimization subagent was launched and reported back
- ✓ Evaluation subagent was launched and reported back
- ✓ Both subagent log files exist (i.e., scaffold-torchtune.log, scaffold-inspect.log)
- ✓ Run directories exist with expected structure (check 1-2 examples)
- ✓ Evaluation directories exist with expected structure (check 1-2 examples)
- ✓ Orchestration log was created

**Note:** You don't need to verify every file - the subagents have already done detailed verification. Just spot-check a few directories to confirm the structure is correct.

## Important Notes

### Orchestration Principles

- This skill **orchestrates** rather than implements - it launches autonomous subagents
- Each subagent maintains its own detailed log
- The orchestration log tracks high-level flow and timing
- Subagents can be run independently if needed (outside of this skill)
- Partial success is acceptable (e.g., fine-tuning configs generated but eval fails)

### Parallel Execution

- Launch both subagents in a **single message** with multiple Task tool calls
- Do NOT launch them sequentially in separate messages
- The subagents run independently in separate context windows
- They can work simultaneously because their outputs don't depend on each other
- Wait for both to complete before proceeding to create the orchestration log

### Subagent Communication

- Each subagent receives its own prompt with specific instructions
- Subagents have full access to tools (Read, Write, Edit, Bash, etc.)
- Subagents report back once in a final message when complete
- You cannot send follow-up messages to subagents
- If a subagent needs more information, include it in the initial prompt

### Error Recovery

If scaffolding fails:
1. Check orchestration log (scaffold-experiment.log) for high-level flow
2. Check individual subagent logs (scaffold-torchtune.log, scaffold-inspect.log) for details
3. Fix the issue (e.g., missing inspect-ai task script, incorrect paths in claude.local.md)
4. Re-run this skill (subagents should handle existing files gracefully)
5. Or run individual subagents directly via Task tool for targeted fixes
