---
name: bayesian-workflow
description: Use when performing Bayesian statistical analysis, building probabilistic models, or when the task involves prior specification, posterior inference, or predictive checks.
invocation: user
---

# Bayesian Workflow

The final deliverable must be a Bayesian model: specify priors, perform posterior inference, and evaluate via posterior predictive checks. Non-Bayesian methods may be explored as baselines/context but must not be selected or reported as the solution.

Core principles:
- Start from generative stories: think data-generating process, not just prediction
- Specify priors explicitly and validate via prior predictive checks
- Use full posterior inference (not MLE/MAP)
- Validate models with posterior predictive checks and parameter recovery checks
- Check diagnostics: R-hat, ESS, divergences, trace plots
- Compare models via predictive performance (LOO, WAIC)
- Consider hierarchical structures when data has grouping/repeated measures
- Flag computational issues (identifiability, convergence, misspecification) when relevant

## Communication

Your outputs serve two purposes:

Terminal output:
- Keep users and developers informed of progress in real-time
- Report what you're doing and key decisions as they happen
- Be concise but informative

Written artifacts (reports, logs):
- These are the primary deliverables that users will read retrospectively
- Invoke the `artifact-guidelines` skill to get the full guidelines

## Task Management

You have two complementary tools for tracking work:

**TodoList (TodoWrite tool):**
- Active task tracking during execution
- What's currently in progress, pending, or just completed
- Provides real-time visibility into execution state
- Ephemeral - reflects current session's work
- Use for: each phase, each model, each validation stage
- Update frequently and mark completed immediately

**log.md (file):**
- Persistent record across the entire workflow
- Key decisions and reasoning: why you chose certain paths, skipped models, or revised approaches
- Issues encountered: failures, convergence problems, validation failures
- Phase transitions and iteration loops
- Use for: decision points, failures, alternative evaluations, phase completions

Use TodoWrite tools VERY frequently to ensure you are tracking tasks and giving users visibility into progress. These tools are EXTREMELY helpful for planning and breaking down complex tasks into smaller steps. If you do not use this tool when planning, you may forget important tasks - and that is unacceptable.

It is critical that you mark todos as completed as soon as you are done with a task. Do not batch up multiple tasks before marking them as completed.

Users may configure 'hooks', shell commands that execute in response to events like tool calls, in settings. Treat feedback from hooks, including `<user-prompt-submit-hook>`, as coming from the user. If you get blocked by a hook, determine if you can adjust your actions in response to the blocked message. If not, ask the user to check their hooks configuration.

## Tool Usage

- Proactively use the Task tool with specialized agents when the task matches the agent's description
- When calling multiple tools, invoke independent tools in parallel for efficiency
- For tools with dependencies, call them sequentially - never use placeholders or guess missing parameters
- To run multiple agents in parallel, send a single message with multiple Task tool uses
- Use specialized file tools (Read, Edit, Write) instead of bash commands (cat, sed, echo)
- Reserve bash exclusively for system commands (git, uv)

### Parallel Subagents
Use parallel subagents to explore multiple perspectives simultaneously, particularly for EDA and model design where uncertainty is high. Each instance needs isolated workspace and files to avoid conflicts. Launch all instances at once using multiple Task tool calls in a single message.

Setup: Prepare separate data copies if needed and assign each instance its own output directory (e.g., `eda/analyst_1/`, `eda/analyst_2/`). Give each instance a different focus area.

Execution: Typical count is 2-3 instances. If an instance fails, relaunch once; if it fails again, proceed with successful instances.

After completion: Synthesize findings from all instances and document convergent patterns (all agree) and divergent insights (unique to one).

## Technical Stack and Requirements

### Core Stack
- Bayesian inference: Stan via CmdStanPy, ArviZ for diagnostics
- Package management: `uv` exclusively (never pip)
- Scripts should be self-contained and run with `uv run`

### Bayesian Model Requirements
Every accepted Bayesian model must:
- Use Stan via CmdStanPy for posterior inference with NUTS
- Do not substitute MLE/MAP for full Bayesian inference
- Do not use non-PPL implementations as final models
- Do not label bootstrap-based checks as posterior predictive checks

## File-Based Communication and Folder Structure

### Core Principles
Subagents are ephemeral - they finish their task and disappear forever. Files are the only persistent memory and communication channel between subagents and across phases. This means:

- Each subagent reads inputs from files (data, previous reports, experiment plans)
- Each subagent writes outputs to files (reports, models, diagnostics)
- The main agent orchestrates by directing subagents to read/write specific locations
- Users navigate results through a predictable folder structure

### Canonical Structure
Use this structure unless the task requires deviation:

```
data/                           # source data and copies
eda/                            # Phase 1: Data Understanding
  eda_report.md                 # final synthesis (if solo) or consolidated report
  analyst_1/                    # if parallel: each instance gets own folder
  analyst_2/
experiments/                    # Phases 2-3: Model Design & Development
  experiment_plan.md            # Phase 2 output: proposed models
  experiment_1/                 # one folder per model attempt
    prior_predictive/
    simulation/
    fit/
    posterior_predictive/
    critique/
  experiment_2/
  model_assessment/             # Phase 4: quality metrics and comparison
    assessment_report.md
final_report.md                 # Phase 6 output
log.md                          # running log of decisions and issues
```

### Guidelines
- Phase outputs should be in predictable locations so subsequent phases know where to read
- Each experiment gets its own numbered folder for isolation
- Parallel subagent outputs go in separate folders (analyst_1, analyst_2, designer_1, etc.)
- Always specify exact paths when invoking subagents: where to read inputs and where to write outputs (e.g., "Read data from `data/data.json` and write outputs to `eda/analyst_1/`")
- Keep log.md updated with key decisions, failures, and reasoning

### Subagent Communication
Point subagents to files produced by previous subagents rather than summarizing content yourself. Ask subagents to report what files they created with brief descriptions so you can keep records and pass information along the chain.

Example: Tell model-designer to "Read the EDA report at `eda/eda_report.md`" rather than summarizing the EDA findings yourself.

## Modeling Workflow

### Phase 1: Data Understanding → `eda/`
Invoke `eda-analyst` to explore the data. For complex datasets, run 1-3 instances in parallel with different focus areas, then synthesize results into `eda/eda_report.md`.

### Phase 2: Model Design → `experiments/experiment_plan.md`
Invoke `model-designer` to propose models. Run 2-3 instances in parallel. Assign each a distinct structural hypothesis (e.g., direct effects vs. hierarchical grouping vs. latent dynamics) rather than arbitrary model families. Synthesize their proposals into a unified experiment plan that covers competing mechanisms.

### Phase 3: Model Development and Selection → `experiments/`
Build a population of validated models and iteratively improve until finding the best variant for each model class.

**For each model class from the experiment plan:**

1. **Initial variants**: Start with variants proposed by model-designer (baseline, scientific, extensions)

2. **Validate each variant** by running stages sequentially:
   - `prior-predictive-checker` - fail → skip variant
   - `recovery-checker` - fail → skip variant
   - `model-fitter` - fail → try fix once with model-refiner, then skip
   - `posterior-predictive-checker` - always run
   - `model-critique` - assess and suggest improvements

   **Special case**: If baseline variant fails pre-fit validation (prior or recovery check), try fix once with model-refiner. If still fails, skip entire model class (this signals fundamental mismatch).

3. **Assess population**: If at least one variant validated successfully, invoke `model-selector`
   - Tell it which experiments completed validation (have fit results and LOO)
   - Model-selector compares via LOO/WAIC and determines strategy
   - Keep log.md updated with which models passed/failed each stage

4. **Follow model-selector strategy**:
   - **CONTINUE_CLASS**: Invoke `model-refiner` with critique suggestions to generate new variants, return to step 2
   - **SWITCH_CLASS**: Move to next model class
   - **ADEQUATE**: Invoke `decision-auditor` to verify EDA coverage before accepting
   - **EXHAUSTED**: Invoke `decision-auditor` to verify EDA coverage before accepting

5. **Audit terminal decisions**: When `model-selector` returns ADEQUATE or EXHAUSTED:
   - Invoke `decision-auditor` with: the selector's decision, path to EDA report, path to experiment plan, and list of validated experiments
   - If auditor returns CHALLENGE: review identified gaps, then either explore missing approaches or document why they are not worth pursuing
   - If auditor returns ACCEPT: proceed to reporting

Invoke model-selector after completing initial variants and after each refinement round.

### Phase 4: Reporting → `final_report.md`
Invoke `report-writer` to generate the final report.
