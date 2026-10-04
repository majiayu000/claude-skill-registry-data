---
name: sandcastle
description: Orchestrate AI coding agents (Claude Code, Codex, OpenCode) in isolated sandboxes using the @ai-hero/sandcastle SDK. Use when the user needs to (1) run agents AFK in Docker/Podman containers, (2) build multi-agent pipelines with plan-execute-review patterns, (3) run parallel agents on separate worktrees, (4) create iterative agent loops with maxIterations, (5) extract structured output from agent runs, (6) set up sandcastle in a new or existing project, or (7) write prompt files with template args and shell expressions.
---

# Sandcastle

Sandcastle (`@ai-hero/sandcastle`) orchestrates AI coding agents inside isolated sandbox environments. It manages git worktrees, boots containers, runs agents with structured prompts, collects commits, and merges results back to branches — all from a single `run()` call.

## Installation

```bash
npm i @ai-hero/sandcastle
npx sandcastle init          # scaffolds .sandcastle/ with Dockerfile and prompt templates
npx sandcastle docker build-image   # builds the Docker image from .sandcastle/Dockerfile
```

## Quick Start

```typescript
import { run, claudeCode } from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";

const result = await run({
  agent: claudeCode(),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
});

console.log(result.commits);   // [{ sha: "abc123" }, ...]
console.log(result.branch);    // branch the agent worked on
```

## Core Concepts

### The Four Entry Points

| Function | Use Case |
|---|---|
| `run(options)` | One-shot agent invocation. Full lifecycle managed automatically. |
| `createSandbox({ branch, sandbox })` | Reusable sandbox on an explicit branch. Call `.run()` multiple times. |
| `createWorktree({ branchStrategy })` | Independent git worktree. Call `.run()`, `.interactive()`, or `.createSandbox()`. |
| `interactive(options)` | Interactive terminal session with an agent. Human-in-the-loop. |

### Agent Providers

```typescript
import { claudeCode, codex, opencode, pi } from "@ai-hero/sandcastle";

claudeCode()                           // default: claude-opus-4-7
claudeCode("claude-sonnet-4-6")        // specify model
claudeCode("claude-sonnet-4-6", { effort: "low" })  // with options
codex("o4-mini")
```

### Sandbox Providers

Sandbox providers are **subpath imports** — not from the main entry point:

```typescript
import { docker }    from "@ai-hero/sandcastle/sandboxes/docker";
import { podman }    from "@ai-hero/sandcastle/sandboxes/podman";
import { vercel }    from "@ai-hero/sandcastle/sandboxes/vercel";
import { daytona }   from "@ai-hero/sandcastle/sandboxes/daytona";
import { noSandbox } from "@ai-hero/sandcastle/sandboxes/no-sandbox";
```

Two categories:
- **Bind-mount** (docker, podman): mount the worktree into a container. Default branch strategy: `head`.
- **Isolated** (vercel, daytona): sync files into a remote environment. Default branch strategy: `merge-to-head`.
- **noSandbox**: host-only, no isolation. **Only valid with `interactive()`** — `run()` and `createSandbox()` reject it.

### Branch Strategies

| Strategy | Behavior | Default For |
|---|---|---|
| `{ type: "head" }` | Agent writes directly to host working directory. Bind-mount only. | docker, podman |
| `{ type: "merge-to-head" }` | Temp branch, auto-merged back to HEAD on completion. | vercel, daytona |
| `{ type: "branch", branch: "feat/x" }` | Commits land on a named branch. Optional `baseBranch`. | — |

## Pipeline Patterns

### Pattern 1: Simple One-Shot

```typescript
await run({
  agent: claudeCode(),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
});
```

### Pattern 2: Iteration Loop

Agent runs multiple iterations, checking for a completion signal between each:

```typescript
await run({
  name: "worker",
  agent: claudeCode("claude-sonnet-4-6"),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
  maxIterations: 5,
  branchStrategy: { type: "merge-to-head" },
  copyToWorktree: ["node_modules"],
  hooks: {
    sandbox: {
      onSandboxReady: [{ command: "npm install" }],
    },
  },
});
```

The agent sees a completion signal instruction in the prompt. When it outputs `<promise>COMPLETE</promise>` (default), iteration stops. Otherwise it runs up to `maxIterations`.

### Pattern 3: Sequential Reviewer

Reuse one sandbox for implement → review → fix cycles:

```typescript
const sandbox = await createSandbox({
  branch: "feature/my-branch",
  sandbox: docker(),
});

await sandbox.run({
  agent: claudeCode("claude-sonnet-4-6"),
  promptFile: "./.sandcastle/implement.md",
});

await sandbox.run({
  agent: claudeCode("claude-opus-4-7"),
  promptFile: "./.sandcastle/review.md",
});

await sandbox.close();
```

### Pattern 4: Parallel Agents

Multiple agents work in parallel on separate worktrees, then a merge agent combines results:

```typescript
const tasks = issues.map(async (issue) => {
  const wt = await createWorktree({
    branchStrategy: { type: "branch", branch: `fix/${issue.id}` },
  });

  const result = await wt.run({
    agent: claudeCode("claude-sonnet-4-6"),
    sandbox: docker(),
    prompt: `Fix issue: ${issue.title}\n\n${issue.description}`,
  });

  await wt.close();
  return result;
});

const results = await Promise.allSettled(tasks);
```

### Pattern 5: Structured Output

Extract typed data from agent runs:

```typescript
import { Output } from "@ai-hero/sandcastle";
import { z } from "zod";

const result = await run({
  agent: claudeCode("claude-opus-4-7"),
  sandbox: docker(),
  promptFile: "./.sandcastle/plan.md",
  maxIterations: 1,   // required for structured output
  output: Output.object({
    tag: "plan",
    schema: z.object({
      issues: z.array(z.object({
        title: z.string(),
        priority: z.enum(["high", "medium", "low"]),
      })),
    }),
  }),
});

console.log(result.output.issues);  // fully typed
```

The prompt **must** contain the XML tag (e.g., `<plan>`) — sandcastle validates this at startup. The agent wraps its structured response in that tag. Also available: `Output.string({ tag })` for plain string extraction.

### Pattern 6: Interactive Then Automated

Explore interactively, then automate implementation:

```typescript
const wt = await createWorktree({
  branchStrategy: { type: "branch", branch: "feature/new" },
});

await wt.interactive({
  agent: claudeCode("claude-opus-4-7"),
  sandbox: noSandbox(),  // noSandbox only valid with interactive()
});

await wt.run({
  agent: claudeCode("claude-sonnet-4-6"),
  sandbox: docker(),
  promptFile: "./.sandcastle/implement.md",
});

await wt.close();
```

## Prompt System

### Inline Prompts

```typescript
await run({
  agent: claudeCode(),
  sandbox: docker(),
  prompt: "Refactor the auth module to use dependency injection",
});
```

Inline prompts skip all processing — no `{{KEY}}` substitution, no shell expressions. Passing `promptArgs` with an inline prompt is an error.

### Prompt Files

```typescript
await run({
  agent: claudeCode(),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
  promptArgs: { ISSUE_TITLE: "Fix login bug", ISSUE_BODY: "Users can't log in" },
});
```

Prompt files support two features:

**1. Template arguments** — `{{KEY}}` placeholders replaced from `promptArgs`:

```markdown
Fix the following issue:
Title: {{ISSUE_TITLE}}
Body: {{ISSUE_BODY}}
```

**2. Shell expressions** — `` !`command` `` evaluated inside the sandbox before each iteration:

```markdown
The current test output is:
!`npm test 2>&1 | tail -50`

The current git diff is:
!`git diff`
```

Shell expressions run per-iteration, so each iteration sees fresh state.

**Built-in args** (auto-injected, cannot be overridden): `{{SOURCE_BRANCH}}`, `{{TARGET_BRANCH}}`.

**Processing order**: Prompt file resolution → Arg substitution (host, once) → Shell expansion (sandbox, per iteration).

## Configuration

### Docker Options

```typescript
docker({
  imageName: "my-custom-image",
  containerUid: 1000,
  containerGid: 1000,
  mounts: [
    { hostPath: "~/.npmrc", sandboxPath: "~/.npmrc", readonly: true },
    { hostPath: "./secrets", sandboxPath: "/app/secrets" },
  ],
  env: { NODE_ENV: "development", CI: "true" },
  network: "host",
  selinuxLabel: "z",
})
```

### Hooks

Lifecycle hooks run commands at specific points:

```typescript
await run({
  agent: claudeCode(),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
  hooks: {
    host: {
      onWorktreeReady: [{ command: "cp .env.local .sandcastle/.env" }],
      onSandboxReady: [{ command: "echo 'sandbox is up'" }],
    },
    sandbox: {
      onSandboxReady: [
        { command: "npm install", timeoutMs: 120_000 },
        { command: "npm run build", sudo: false },
      ],
    },
  },
});
```

**Execution order**: `copyToWorktree` → `host.onWorktreeReady` (sequential) → sandbox created → `host.onSandboxReady` + `sandbox.onSandboxReady` (parallel).

### Timeouts

| Parameter | Default |
|---|---|
| `idleTimeoutSeconds` | 600 (10 min) |
| Hook commands | 60s (per-hook `timeoutMs`) |
| Git setup | 10s |
| Commit collection | 30s |
| Merge to host | 30s |
| Shell expression expansion | 30s |
| `timeouts.copyToWorktreeMs` | 60s |

### Completion Signal

```typescript
await run({
  completionSignal: "<done>FINISHED</done>",  // custom signal
  // or: completionSignal: ["<done>FINISHED</done>", "<done>SKIPPED</done>"],
  // default: "<promise>COMPLETE</promise>"
});
```

### Cancellation

```typescript
const controller = new AbortController();
setTimeout(() => controller.abort("timeout"), 300_000);

await run({
  agent: claudeCode(),
  sandbox: docker(),
  prompt: "Fix all lint errors",
  signal: controller.signal,
});
```

### Automatic Cleanup

Both `Sandbox` and `Worktree` support `Symbol.asyncDispose`:

```typescript
await using sandbox = await createSandbox({
  branch: "feature/x",
  sandbox: docker(),
});
// automatically cleaned up when scope exits
```

## RunResult

Every `run()` returns:

```typescript
{
  iterations: IterationResult[];     // per-iteration details
  completionSignal?: string;         // matched signal, or undefined if maxIterations hit
  stdout: string;                    // combined agent output
  commits: { sha: string }[];       // commits made by agent
  branch: string;                    // branch agent worked on
  logFilePath?: string;              // log file path (file logging mode)
  preservedWorktreePath?: string;    // set when worktree had uncommitted changes
  output?: T;                        // present when Output config was provided
}
```

## Session Management

Claude Code sessions can be captured and resumed across runs:

```typescript
import { hostSessionStore, transferSession } from "@ai-hero/sandcastle";

const result = await run({
  agent: claudeCode("claude-opus-4-7"),
  sandbox: docker(),
  promptFile: "./.sandcastle/prompt.md",
});

// Resume a prior session in a new run
await run({
  agent: claudeCode("claude-opus-4-7"),
  sandbox: docker(),
  promptFile: "./.sandcastle/continue.md",
  resumeSession: "session-id-from-prior-run",
  maxIterations: 1,  // required when resuming
});
```

## CLI Commands

```bash
npx sandcastle init                    # scaffold .sandcastle/ directory
npx sandcastle docker build-image      # build Docker image from .sandcastle/Dockerfile
npx sandcastle docker remove-image     # remove the Docker image
npx sandcastle podman build-image      # build with Podman
npx sandcastle podman remove-image     # remove Podman image
```

`sandcastle init` offers templates:
- **blank** — minimal single `run()` call
- **simple-loop** — iteration loop picking work items
- **sequential-reviewer** — implement-then-review via `createSandbox()`
- **parallel-planner** — plan/execute/merge with parallel agents
- **parallel-planner-with-review** — parallel planner plus review phase

## Critical Rules

1. **Sandbox providers are subpath imports** — `import { docker } from "@ai-hero/sandcastle/sandboxes/docker"`, never from the main entry point.

2. **`noSandbox()` only works with `interactive()`** — `run()` and `createSandbox()` reject it. AFK work requires real isolation.

3. **`head` strategy is incompatible with isolated providers** — throws at runtime. Use `merge-to-head` or `branch` instead.

4. **`copyToWorktree` is incompatible with `head` strategy** — head mode bind-mounts the host directory directly, no worktree exists.

5. **`resumeSession` requires `maxIterations: 1`** — resume applies to iteration 1 only.

6. **Structured output requires `maxIterations: 1`** — and the XML tag must appear in the prompt text. Sandcastle validates both at startup.

7. **Inline prompts skip all processing** — no `{{KEY}}` substitution, no `` !`command` `` expansion. Passing `promptArgs` with an inline `prompt` is an error.

8. **Built-in prompt args** (`SOURCE_BRANCH`, `TARGET_BRANCH`) **cannot be overridden** — attempting to do so is a runtime error.

9. **Docker UID must match image UID** — sandcastle runs a pre-flight check and errors on mismatch. Default is host UID or 1000.

10. **Worktrees are preserved on error** — if the agent leaves uncommitted changes or an error occurs, the worktree is not cleaned up. The path is returned in `preservedWorktreePath`.

See [references/api-types.md](references/api-types.md) for full type signatures and [references/prompt-system.md](references/prompt-system.md) for prompt file details.

## Deliverables

When asked to build a sandcastle pipeline:

1. **Pipeline script** — TypeScript file using sandcastle's API (e.g., `pipeline.ts` or `.sandcastle/run.ts`)
2. **Prompt files** — `.sandcastle/*.md` prompt templates with `{{ARG}}` placeholders and `` !`command` `` expressions as needed
3. **Docker setup** — `.sandcastle/Dockerfile` if not already present (or instruct user to run `npx sandcastle init`)
4. **package.json script** — e.g., `"pipeline": "npx tsx .sandcastle/run.ts"`

## Verification

After generating a pipeline:

1. Confirm `@ai-hero/sandcastle` is in `package.json` dependencies
2. Confirm sandbox provider imports use subpath syntax
3. Confirm prompt files exist at the referenced paths
4. Confirm any `{{ARG}}` placeholders in prompts have matching `promptArgs`
5. If using Docker: confirm `.sandcastle/Dockerfile` exists or `sandcastle init` was run
6. If using structured output: confirm `maxIterations: 1` and the XML tag appears in the prompt
