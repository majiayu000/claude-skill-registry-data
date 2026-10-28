---
name: write-agent-benchmarks
description: >-
  Build and run benchmarks that measure an AI AGENT's behaviour — scenarios,
  checklists, judged runs. Use when authoring or evaluating agent benchmark
  scenarios. Not for code performance benchmarks (deno bench, criterion) or
  ordinary test suites.
---

# Universal Agent Benchmarking Skill

## 1. Context & Philosophy

This skill defines a universal, language-agnostic standard for benchmarking Autonomous AI Agents. The goal is to objectively measure an agent's ability to solve real-world tasks, whether they are coding, data analysis, or conversational.

### Core Principles

1. **Evidence-Based Verification**: We do not trust the agent's words. We verify its actions.
   - **Bad**: The agent says "I fixed the bug." -> Judge believes it.
   - **Good**: The agent says "I fixed the bug." -> Judge runs the test suite in the environment and verifies the exit code is 0.
2. **Strict Isolation**: Test run MUST execute in a completely isolated environment (Docker, VM, etc.). This ensures a clean, reproducible state and prevents side effects.
3. **Black Box Protocol**: The benchmark knows *nothing* about the agent's internals (prompts, tools, language). It only observes:
   - **Input**: User Query + Environment State.
   - **Output**: New Environment State + Response Text.
4. **Determinism**: Benchmarks should be reproducible. Mock external network calls where possible and use fixed seeds.
5. **Universal Applicability**: The standard applies to any agent type:
   - **CLI/IDE Agents**: Interact via shell/files.
   - **API Agents**: Interact via HTTP/JSON.
   - **Chat Agents**: Interact via conversation.

## 2. Evaluation Modes

The system supports three primary evaluation modes:

1. **Quality Evaluation (Checklist-based)**:
   - **Goal**: Verify if an agent meets minimum quality standards.
   - **Method**: Evaluates a single agent against a predefined checklist of criteria (Critical Errors vs Warnings).
   - **Use Case**: CI/CD pipelines, regression testing.

2. **Model Selection (Pairwise Comparison)**:
   - **Goal**: Determine which LLM/Model performs best.
   - **Method**: **LLM-as-a-Judge Side-by-Side (SBS)**. The Judge compares outputs from two models and selects a winner.

3. **Version Comparison (Regression Tracking)**:
   - **Goal**: Measure impact of changes to prompt or logic.
   - **Method**: Compare current version (HEAD) against a baseline (BASE).

## 3. Interaction Strategies

Choosing the right interaction strategy is critical for stable benchmarks.

### 3.1 Atomic Request Verification (Step-by-Step)
- **Method**: Send a single input, wait for output, verify immediately.
- **Best for**: Stateless APIs, simple function calling agents, or deterministic workflows where the agent's path is fixed.
- **Limitation**: Fails with autonomous agents that might "think" for 3 steps before acting. If you expect a file write on Step 1, but the agent does it on Step 2, the test fails falsely.

### 3.2 User Emulation (End-to-End Session)
- **Method**: The Runner starts a session and acts as a **Simulated User**. It observes the agent's loop without interfering until the agent signals completion or asks for input.
- **Best for**: Autonomous agents, complex problem solvers, and chat-based assistants.
- **Reasoning**: In an autonomous loop, we cannot predict *when* the agent will perform the target action (e.g., writing a file). It might first explore, then plan, then act.
- **Protocol**: The Runner waits for the agent to say "I'm done" or "I need X", providing replies via the Simulated User persona, and only verifies the final state after the session ends.

## 4. Architecture & Requirements

A robust benchmarking system consists of five key modules.

### 4.1 The Environment (Sandbox)

The isolated state container where the task is performed. It is not limited to a file system.

- **File System Context**: A directory with files (for coding tasks).
- **Network Context**: Mock servers or intercepted HTTP traffic (for API tasks).
- **Data Context**: Ephemeral databases (e.g., Postgres, Redis containers) for data tasks.
- **Browser Context**: Headless browser instances (for web agents).
- **Lifecycle**: Must support `Setup` (initial state), `Reset` (between runs), and `Teardown`.

### 4.2 The Runner (Orchestrator)

The central controller managing the test lifecycle.

- **Interface Adapters**: Adapts the Agent's native output to the Environment.
  - *Shell Adapter*: Executes bash commands.
  - *SQL Adapter*: Executes SQL queries against the Data Context.
  - *HTTP Adapter*: Sends requests to the Network Context.
- **Concurrency**: Should run multiple scenarios in parallel.

### 4.3 The Simulated User (Persona)

For interactive agents that ask clarifying questions.

- **Role**: Replaces the human in the loop.
- **Persona**: Defined by a specific goal, knowledge level, and constraints (e.g., "Junior Dev who doesn't know Docker").
- **Behavior**: Provides consistent, deterministic answers to the agent's questions during the run.

### 4.4 The Judge (Evaluator)

The logic that determines if a test passed or failed based on **Evidence**.

- **Artifact Evidence**: Files created, DB rows inserted, resources deployed.
- **Interaction Evidence**: API logs, tool call arguments, HTTP request bodies.
- **Semantic Evidence**: The quality/accuracy of the text response (evaluated by LLM).

### 4.5 Observability (The Trace)

Complete capture of the agent's lifecycle in a **single human-readable file** (e.g., `trace.md` or `trace.json`).

- **Must Capture**: Full conversation history, exact Judge prompts/responses, command outputs, environment diffs.
- **Normalization**: Output should be normalized for consistent evaluation.

## 5. Workflow: Creating a New Benchmark

Follow this process to add a new benchmark scenario.

### Step 1: Define the Goal

What specific capability are you testing?

- _Example_: "Can the agent fix a syntax error?" or "Can the agent negotiate a price?"

### Step 2: Design the Environment (Pre-condition)

Create the initial state.

- **Static Setup**: Copy fixture files, seed database with initial rows.
- **Dynamic Setup**: Start mock servers, configure environment variables.

### Step 3: Define the Task (Trigger)

Write the prompt that instructs the agent.

- _Prompt_: "Run the script and fix errors" or "Book a flight to Paris".

### Step 4: Define Success Criteria (Post-condition)

How do we know it worked?

1. **Hard Check (Artifact)**: File `script.py` runs with exit code 0.
2. **Hard Check (State)**: Database table `users` has 1 new row.
3. **Soft Check (Semantic)**: Agent's explanation is polite and accurate.
4. **Interaction Check**: Agent called `GET /api/v1/flights` with correct parameters.

### Step 5: Register

Add the scenario to your Runner's registry.

## 6. Workflow: Running & Debugging

### Execution Loop

1. **Init**: Runner prepares the Environment (Docker, DB, Mocks).
2. **Seed**: Runner executes Scenario Setup.
3. **Act**: Agent runs in the environment.
   - *Interactive Loop*: Agent <-> Simulated User.
   - *Command Loop*: Agent <-> Environment (Shell/API).
4. **Stop**: Agent signals completion or timeout.
5. **Evidence**: Runner collects state diffs (git, DB dump) and logs.
6. **Judge**: Runner passes Evidence to the Judge.
7. **Report**: Result is saved. Environment is destroyed.

### Debugging Failures

If a benchmark fails, check the **Trace**:

1. **Did the Setup work?** Check initial environment state.
2. **Did the Agent try?** Check logs for actions/tool calls.
3. **Did the Simulated User confuse the Agent?** Check the conversation log.
4. **Did the Judge hallucinate?** Check the Judge's reasoning against the actual evidence.

### Before editing the skill under test — verify the infrastructure

When a scenario fails, especially a `verbatim_relay` / `mock-reached-agent`
check, do NOT jump straight to rewriting SKILL.md — the test infrastructure
is the most common culprit (e.g. a mocked tool invoked by absolute path
bypasses the PATH shadow, so the real binary runs and the scenario "passes"
on synthesis, not relay).

Mock mechanism (ACP): `scenario.mocks` is a static one-response-per-tool
map. The runner writes a stub per tool into a `mockbin/` dir prepended to
the agent's `PATH` (`writeMockBin`, `acp/mock_bin.ts`); each stub prints the
canned text to stdout+stderr and exits 0. So when the agent runs the tool
**by name**, it gets exactly the mock text — IDE-agnostic, no hooks.

Run this checklist first:

1. **Stub installed?** `ls <workDir>/mockbin/` should show an executable
   `<tool>` (mode 755). Absence → the scenario declared no `mocks`, or
   `mockbin` was not prepended to `PATH`.
2. **Tool invoked by name?** The shadow only fires when the command resolves
   through `PATH`. An absolute/relative path (`/usr/bin/<tool>`, `./<tool>`)
   or a shell builtin bypasses the stub. Confirm the body calls the bare
   name (`curl …`, not `/usr/bin/curl …`).
3. **Sentinel in mock text?** The canned output MUST carry a unique token
   (e.g. `[benchmock-<6-hex>]`) **absent** from the skill's SKILL.md and
   examples. Grep the judge output for it: present → the stub ran and the
   agent quoted it; absent → synthesis, NOT relay. Only robust relay signal.
4. **No test-fitting.** Never add a skill rule that preserves a bench-only
   artifact (e.g. "keep the `MOCK:` prefix") — real CLIs don't emit it, and
   teaching the agent to preserve it corrupts real behaviour. Let the mock's
   **distinctive content** prove the relay, not the framing.

Only after steps 1–4 pass is it safe to edit SKILL.md. Skipping this
wastes bench cycles and frequently introduces regressions.

## 6.1 Trigger Scenarios for Skills (FR-ACCEPT.TRIGGER)

Execution scenarios prove "when skill X runs, it works." They do NOT prove that the model picks skill X for a relevant query, or that it stands down for an unrelated one. **Trigger scenarios** close that gap: they verify description-matching correctness.

### Scope and shape

- **Applies to:** every skill under `framework/<pack>/skills/*`. Commands (`commands/`) carry `disable-model-invocation: true` and are out of scope.
- **Per skill:** exactly 3 scenarios — 1 positive, 1 adjacent-negative, 1 false-use-negative.
- **Layout:** sibling folders to existing scenarios:
  ```
  framework/<pack>/skills/<skill-id>/benchmarks/
    trigger-pos-1/mod.ts
    trigger-adj-1/mod.ts
    trigger-false-1/mod.ts
  ```
- **Scenario id:** `<skill-id>-trigger-<pos|adj|false>-1` (the trailing `-1` is preserved for backward compatibility with trace tooling; only `n=1` is permitted).
- **Coverage check:** `scripts/check-trigger-coverage.ts` (wired into `deno task check`) fails if any of the 3 are missing, or if stray `trigger-{type}-{2,3,...}` directories exist.

### Picking queries

With N=1, each query carries the full description-match weight for its class — pick the phrasing most likely to expose a description regression.

- **Positive (`trigger-pos-1`):** a natural, short user query that matches the skill's description. **No `/skill-name` prefix** (that bypasses description-matching), no over-specified jargon, no hints at internal mechanics. Pick the phrasing a typical user would write — the least-jargonized form — so the test stresses description match, not exact wording.
- **Adjacent-negative (`trigger-adj-1`):** a query for which a *different, neighboring* skill is the correct match. Pick the most-likely confusion candidate from the same pack or with overlapping vocabulary. Typical confusion patterns: a "fix this test" skill vs. a "review my diff" skill (overlap on "I broke something"); a single-task planner vs. a multi-phase epic planner (overlap on "plan"); a current-session reflection vs. a historical-sessions reflection (overlap on "reflect").
- **False-use-negative (`trigger-false-1`):** a query inside the skill's general domain but with the wrong intent. Recommended patterns: surface vocabulary that matches but the actual ask is something else (e.g., a planning skill receiving "plan" in a non-software-task sense; a bug-diagnosis skill receiving a "speed up the test runner" perf request); reverse-intent traps (e.g., write *new* tests vs fix *failing* ones). **Do NOT use meta-questions about the skill itself** ("what does X cover?", "how does X work?", "when should I use X?") as false-use — under Claude Code these are legitimately answered by *reading* the skill's `SKILL.md`, so the agent will rightly load it and the judge will record activation. Treat meta-questions as positives or omit them.

### Checklist contract

Every trigger scenario carries exactly **one critical** checklist item.

- Positive (`trigger-pos-*`):
  ```ts
  checklist = [{
    id: "skill_invoked",
    description: "Did the agent load and act on `<skill-id>` in response to this query? Look in the trace for a `Skill` tool call or a read of the skill's `SKILL.md` for `<skill-id>`.",
    critical: true,
  }];
  ```
- Negative (`trigger-adj-*` and `trigger-false-*`):
  ```ts
  checklist = [{
    id: "skill_not_invoked",
    description: "Did the agent AVOID loading `<skill-id>`? For this query the skill is not appropriate; the agent should either invoke a different skill or respond directly without reading `<skill-id>/SKILL.md` or calling the `Skill` tool with `<skill-id>`.",
    critical: true,
  }];
  ```

### Template (`mod.ts`)

```ts
import { AcceptanceTestScenario } from "@acceptance-tests/types.ts";

export const TriggerPos1 = new class extends AcceptanceTestScenario {
  id = "<skill-id>-trigger-pos-1";
  name = "<short label, e.g. 'natural investigate query'>";
  skill = "<skill-id>";
  agentsTemplateVars = { PROJECT_NAME: "Sandbox" };
  userQuery = "<natural user query>";
  checklist = [{
    id: "skill_invoked",
    description:
      "Did the agent load and act on `<skill-id>` in response to this query? Look in the trace for a `Skill` tool call or a read of the skill's `SKILL.md` for `<skill-id>`.",
    critical: true,
  }];
}();
```

### RED-phase verification

Before scaling, write one positive scenario and run it; confirm the judge correctly fails the run when the skill's `description` is mangled to be unrelated. Then revert the description. This validates the pattern end-to-end. See SRS `FR-ACCEPT.TRIGGER`, SDS §3.4.2.

## 6.2 Agent Scenarios — Wrapped, Not Standalone

Subagents (files under `framework/<pack>/agents/<name>.md`) MUST be tested **through their wrapping skill scenario**, not as standalone `AcceptanceTestAgentScenario` runs. The framework spawns the main runtime in `-p` mode with `userQuery` as the user message; the agent `.md` file is copied to `.claude/agents/` only as a *template the main runtime may dispatch to*. There is no path that loads the subagent's body as a system prompt for direct execution. A standalone `AcceptanceTestAgentScenario` therefore tests the main runtime's behaviour given access to the agent template — NOT the agent's body.

Two consequences:

1. Use a wrapping skill's `via-subagent`-style scenario (parent skill → `Agent`/`Task` tool → subagent → mocked CLI → relay back). Checklists should gate on the parent-side dispatch (`worker_subagent_invoked`) and the relay signal (`mock_content_relayed`), both of which ARE observable from the flat trace.
2. If no wrapping skill exists, the subagent is not testable in this framework — write the wrapper first, then the scenario.

Precedent: existing worker-style subagents in the framework have no `acceptance-tests/` directory of their own; they are tested only via their orchestrating skill's scenarios.

### Flat-trace caveat for subagent scenarios

The transcript `AcpAgent` accumulates over the ACP session does NOT preserve parent-vs-subagent nesting. When a parent invokes `Agent(subagent_type=...)`, the subagent's internal `Bash` calls appear at the same top-level as the parent's tool calls. Avoid checklist items like "no `Bash("codex …")` in the parent" — the judge cannot distinguish parent-side from worker-side Bash from the flat trace alone. Instead gate on the presence of the `Agent`/`Task` dispatch and on the relay-content signal; together they imply the worker did the work.

## 6.3 Mock Pitfalls

### Mocks fire on PATH resolution, not command shape

The PATH-shadow stub fires whenever the mocked tool name resolves through `PATH` — regardless of env prefixes, pipes, or subshells. `CLAUDECODE="" codex exec "$P"`, `echo "$P" | codex exec -`, and `( codex … )` all hit the stub. (An improvement over the retired `PreToolUse(Bash)` hook, which parsed only the first bare word and missed those forms.)

What DOES bypass the stub:

- **Absolute/relative paths.** `/usr/bin/codex` or `./codex` skip `PATH` → the real binary runs. In the sandbox this usually surfaces as an auth error (e.g. Codex 401) that looks like a setup bug, not a mock-miss. Invoke the **bare tool name** (`codex exec "$P"`).
- **Shell builtins** (`echo`, `cd`) aren't `PATH`-resolved, so they can't be shadowed — but they're not real targets either, so this rarely matters.
- **Non-zero exit can't be mocked.** The stub always exits 0. To simulate failure, encode it in the canned text (e.g. `bash: curl: command not found`).

### Relay-verification checklists must gate on substantive content, not on framing

The stub prints **exactly** the canned text you put in `scenario.mocks` — there is no auto-injected harness prefix. So whatever framing you add (e.g. `[benchmock-xxx] CODEX-MOCK: <body>`) you control yourself. Agents under a courier rule (verbatim relay of a child runtime's stdout, common in cross-IDE or LLM-as-judge skills) will reasonably strip such prefix-looking tokens as harness artefacts — that is correct behaviour per such a contract, not a relay failure.

To verify relay actually happened, embed a **deliberately-absurd phrase** inside the mock body and check for that phrase in the final answer. The phrase must be:

- (a) absent from any SKILL.md or agent body in the project,
- (b) implausible as a free-form completion from the model's weights given the user query.

Examples drawn from passing scenarios: `alphabetise your tuples on Wednesdays`, `octopus-shaped type definitions`, `tag mutable state with marigold-coloured comments`, `alphabetise trailing semicolons before lowercase Friday refactors`.

Prefix-style framing tokens (`[benchmock-xxx]`, `<TOOL>-MOCK:`) fail as relay signals: they read as harness artefacts, and the courier rule permits stripping them. Don't gate on them — gate on the absurd phrase inside the body.

## 7. Universal Result Schema

To ensure cross-platform compatibility, benchmark results must follow a standard JSON schema.

```json
{
  "scenario_id": "string",
  "outcome": "pass|fail",
  "score": 0-100,
  "metrics": {
    "duration_ms": 1200,
    "cost_usd": 0.01,
    "steps_taken": 5,
    "tokens_used": 1500
  },
  "evidence": {
    "artifacts": ["file_paths"],
    "logs": ["log_entries"]
  },
  "checklist": [
    { "id": "check_1", "status": "pass", "reason": "..." }
  ]
}
```

## 8. Configuration Principles

1. **Preset-Based Management**: Manage LLM configurations as named presets.
2. **Role Separation**: Distinguish between **Agent** (tested), **Judge** (evaluator), and **Simulated User** (context provider).
3. **Reproducibility**: Enforce deterministic behavior (e.g., `temperature: 0`).

## 9. Assets & References

- **[examples/scenario-example.md](assets/scenario-example.md)**: Template for defining scenarios.
- **[acceptance-tests/config.json](acceptance-tests/config.json)**: Main configuration file for models and presets.
