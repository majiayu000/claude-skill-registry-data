---
name: agent
description: Agent primitives and autonomous behaviors — fan-out, delegate, broadcast, research, solve, consensus, swarm for Claude Code native multi-agent orchestration
---

<Purpose>
Two layers of agent capability on top of Claude Code's native Agent tool:
1. **Primitives** — Reusable patterns (fan-out, delegate, broadcast) for direct agent control
2. **Autonomous Behaviors** — Goal-driven agent activities (research, solve, consensus, swarm) where agents self-direct, discover, and collaborate via stigmergy

Key distinction from x-op: x-op = leader-controlled strategies. x-agent = agent-autonomous execution.
</Purpose>

<Use_When>
- User wants to send a task to multiple agents in parallel
- User says "fan-out", "delegate", "broadcast", "ask N agents"
- User wants agents to explore/research autonomously ("research this", "investigate freely", "find out about")
- User wants agents to solve a problem without step-by-step direction ("figure out why", "fix this somehow")
- Other xm skills need agent primitives
- User wants direct agent control without a full strategy
</Use_When>

<Do_Not_Use_When>
- User wants a leader-controlled strategy with fixed phases (use /xm:op instead)
- Single simple task (just use Agent tool directly)
- User says specific strategy names like "refine", "tournament", "debate" (use /xm:op)
</Do_Not_Use_When>

# x-agent — Agent Primitives & Autonomous Behaviors

Structured agent primitives and autonomous behaviors on top of the Claude Code native Agent tool.
No external dependencies. Works with Claude Code alone.

```
x-agent
├── Primitives          fan-out, delegate, broadcast, status
├── Autonomous          research, solve, consensus, swarm
├── Team                Team Leader → Members hierarchy
└── (cross-cutting) Role Presets — 15 presets injected into all layers
```

**Design philosophy:**
- x-op = conductor with a score (leader controls every phase)
- x-agent = jazz band (agents listen to each other and adapt)

## Mode Detection

Read mode from `.xm/config.json` (`mode` field). Default: `developer`.

**Developer mode**: Use technical terms (fan-out, delegate, broadcast, collect, verdict, assumption). Concise.

**Normal mode**: Use simple Korean for all user-facing output.
- Term mapping: "fan-out" → "동시 실행", "delegate" → "위임", "broadcast" → "전체 전달", "board" → "게시판"
- Term mapping: "verdict" → "판정", "role" → "역할", "team" → "팀", "stigmergy" → "간접 협동"
- Use polite register (~하세요 체), prioritize key information first

### Korean output style (avoid AI-slop)

Universal (both modes): drop empty intensifiers (매우/완벽하게/강력한/원활하게/혁신적인) without a specific claim, no forced rule-of-three or "~뿐만 아니라 ~까지", no hedged non-conclusions — end on a concrete fact/number/next action.
Developer mode: terse, lead with the result, no 권고형 결말 pile-up ("~해야 한다" 연속).
Easy/normal mode: accessible Korean — polite guidance (~해 보세요); keep commands/flags/proper-nouns in English, write domain terms as Korean(original) on first use; universal rules still apply.

## Arguments

User provided: $ARGUMENTS

## Routing

First word of `$ARGUMENTS`:
- `fan-out` → [Primitive: fan-out]
- `delegate` → [Primitive: delegate]
- `broadcast` → [Primitive: broadcast]
- `status` → [Primitive: status]
- `team` → [Team: subcommand routing]
- `research` → [Autonomous: research]
- `solve` → [Autonomous: solve]
- `consensus` → [Autonomous: consensus]
- `swarm` → [Autonomous: swarm]
- `flow` → [Subcommand: flow]
- `list` or empty input → [Subcommand: list]

---

## Subcommand: list

```
x-agent — Agent Primitives & Autonomous Behaviors

Primitives:
  fan-out <prompt> [options]     Send same prompt to N agents in parallel
  delegate <role> <prompt>       Send to one agent with a specific role
  broadcast <prompt> [options]   Send different context to each agent
  status                         Show active background agents

Autonomous:
  research <topic> [options]     Autonomous exploration — agents discover, share, re-explore
  solve <goal> [options]         Autonomous problem-solving — agents try, adapt, converge
  consensus <topic> [options]    Peer deliberation — agents debate and self-converge
  swarm <goal> [options]         Stigmergy — agents claim, execute, post tasks to shared board

Flow (Workflow backend — max parallelism):
  flow "<goal>" [options]        Decompose → topo-batch fan-out (queued, 1000 max) → schema merge
    --agents N                   Target leaf count (advisory)
    --op <preset>               Fixed roster: review | research | score | red-team
    --no-merge                   Return raw leaf results without the merge step

Team:
  team create <name> [--template <t>]   Create a team (from template or dynamic)
  team list                             Show active teams
  team status [name]                    Team progress report
  team assign <team> <goal>             Assign goal to team → TL executes
  team report [name]                    Request report from TL
  team coord <from> <to> <message>      Route cross-team message
  team disband [name]                   Disband a team
  team templates                        List available team templates

Primitive Options:
  --agents N                     Number of agents (default 3)
  --model sonnet|opus|haiku      Agent model (default sonnet)
  --background                   Run in background (default for fan-out)
  --foreground                   Wait for result (default for delegate)
  --role <name>                  Agent role/description
  --roles "r1,r2,r3"             Per-agent role presets (comma-separated)
  --context <text>               Additional context to inject
  --cross-vendor                 Run each agent on a different model vendor (fan-out/broadcast)

Autonomous Options:
  --agents N                     Number of agents (default 3; consensus: 4)
  --model sonnet|opus|haiku      Agent model (default sonnet)
  --budget N                     Max rounds per agent (default 5; consensus: 4)
  --depth shallow|deep|exhaustive  Exploration depth (default deep)
  --focus <hint>                 Focus area hint (optional)
  --web                          Allow web search (default: code-only)

Role Presets:
  explorer       Codebase exploration, structure mapping          (haiku)
  se             Implementation, refactoring, testing             (sonnet)
  sre            Infrastructure, monitoring, SLO, incidents       (sonnet)
  architect      System design, trade-offs, ADR                   (opus)
  reviewer       Code review, quality, maintainability            (sonnet)
  security       OWASP, vulnerabilities, auth/authz               (sonnet)
  debugger       Error tracing, root cause, regression isolation  (sonnet)
  optimizer      Performance profiling, caching, query tuning     (sonnet)
  documenter     API docs, README, changelog, onboarding          (haiku)
  verifier       Evidence-based completion checks, test adequacy  (sonnet)
  planner        Structured consultation, work plan generation    (opus)
  critic         Plan review, gap detection, simulation           (opus)
  test-engineer  Test strategy, TDD, coverage, flaky hardening   (sonnet)
  build-fixer    Build/type error resolution, minimal diffs       (sonnet)
  team-leader    Hierarchical team management, coordination      (opus)

Examples:
  /xm:agent fan-out "Find bugs in this code" --agents 5
  /xm:agent delegate security "Security review of src/auth.ts"
  /xm:agent broadcast "Review from your perspective" --agents 3
  /xm:agent research "Redis pub/sub limits and alternatives" --budget 5
  /xm:agent solve "CI-only test failure in auth module" --agents 3
  /xm:agent consensus "JWT vs Session for auth" --agents 4
  /xm:agent swarm "Increase test coverage to 80%" --agents 5 --budget 10
  /xm:agent flow "Analyze refactor impact across the token-capture path" --agents 6
  /xm:agent flow --op review --target HEAD
  /xm:agent team create eng --template engineering
  /xm:agent team assign eng "Implement payment system"
```

---

## Primitive: fan-out

**Send the same prompt to N agents in parallel and collect all results.**

### Parsing

From `$ARGUMENTS`:
- After the first word = prompt (full text inside quotes)
- `--agents N` = number of agents (default 3)
- `--model sonnet|opus|haiku` = model (default sonnet)
- `--role <name>` = agent role description (default: "agent")
- `--roles "se,sre,security"` = per-agent role presets (comma-separated)
- `--context <text>` = additional context injection
- `--cross-vendor` = run each agent on a different model vendor via `xm panel cross` (opt-in, graceful single-vendor fallback). Default without the flag: `.xm/config.json` `cross_vendor.agent` ?? `cross_vendor.default`; `--no-cross-vendor` forces single — see `references/cross-vendor.md`

### --roles option

When `--roles "se,sre,security"` is specified, each agent gets its corresponding role preset:

```
Agent 1: se preset injected + common prompt
Agent 2: sre preset injected + common prompt
Agent 3: security preset injected + common prompt
```

Without `--roles`, the default behavior applies (identical prompts).
If the number of roles in `--roles` differs from `--agents N`, the roles count takes precedence.

### Execution

**Invoke N Agent tools in a SINGLE message — one call per agent.** That is what makes them
concurrent. ALWAYS set `run_in_background: false` — it defaults to TRUE, and a backgrounded call
returns only the agent's name, not its result; that is how a fan-out silently reports empty
results. `subagent_type` is `general-purpose` — never a plugin-qualified type the host may lack.

```
Agent tool 1: {
  description: "agent-1: {role}",
  subagent_type: "general-purpose",
  run_in_background: false,
  prompt: "{context if provided}\n\n{prompt}",
  model: "{model}"
}
... (N total, same shape, same prompt)
```

### Result collection

Verify N results for N dispatched agents first. An agent that returned nothing — or a generic
greeting instead of work — never received its prompt: re-dispatch it, don't report it empty.
When all agents complete:
1. Organize each agent's result with numbering
2. Output consolidated results to the user:

```
📡 [fan-out] {N} agents completed

## Agent 1
{result}

## Agent 2
{result}

## Agent 3
{result}

---
💡 Commonalities: {common patterns identified by the leader}
⚡ Differences: {key differences}
```

---

## Primitive: delegate

**Delegate to a single agent with a specific role and receive the result immediately.**

### Parsing

From `$ARGUMENTS`:
- Word after `delegate` = role
- Remainder = prompt
- `--model sonnet|opus|haiku` = model (default sonnet; judgment roles like "architect" inherit the session model)
- `--background` = run in background (default: foreground)
- `--context <text>` = additional context

### Automatic model routing

| Role keyword | Model |
|------------|------|
| architect, analyst, critic, planner, reviewer, security, debugger | **omit `model`** — runs on the harness-inherited default (session/parent model; never below opus in measured sessions) |
| se, sre, optimizer, executor, builder, fixer, tester, verifier, test-engineer, build-fixer | sonnet |
| explorer, documenter, scanner, linter | haiku |

Explicit `--model` overrides automatic routing. Never pass the literal string `"inherit"` as a model value — inherit is expressed only by omitting the parameter.

### Automatic role preset injection

When the role name in delegate matches a registered preset, that preset's system prompt is automatically injected into the agent prompt:

Examples:
- `/xm:agent delegate sre "Inspect this service"` → SRE checklist included in the prompt
- `/xm:agent delegate explorer "Map the codebase"` → Exploration strategy included in the prompt
- Unknown role → default delegate behavior without preset

### Execution

```
Agent tool: {
  description: "{role}",
  prompt: "{context}\n\n## Role: {role}\n{prompt}",
  run_in_background: false (foreground),
  model: "{auto-routed model}"
}
```

### Result

```
📌 [delegate] {role} ({model}) completed

{agent result}
```

---

## Primitive: broadcast

**Send to multiple agents simultaneously, each with a different context/role.**

### Parsing

From `$ARGUMENTS`:
- After `broadcast` = common prompt
- `--agents N` = number of agents (default 3)
- `--roles "security,performance,logic"` = per-agent roles (comma-separated)
- `--model` = model
- `--context` = common context
- `--cross-vendor` = pair each role with a different model vendor via `xm panel cross` — see `references/cross-vendor.md`

When preset names are used in `--roles`, the corresponding specialized prompts are automatically injected.

### Automatic role assignment when unspecified

When `--roles` is omitted, roles are auto-assigned based on agent count:

| N | Auto-assigned roles |
|---|---------|
| 2 | analyst, critic |
| 3 | security, performance, logic |
| 4 | security, performance, logic, architecture |
| 5+ | security, performance, logic, architecture, testing, ... |

### Execution

Same rule as fan-out: all N calls in ONE message, each with `run_in_background: false` (it
defaults to TRUE) — the Result section below consolidates every role's output.

```
Agent tool 1: {
  description: "agent-1: {role_1}",
  subagent_type: "general-purpose",
  run_in_background: false,
  prompt: "{context}\n\n## Your Role: {role_1}\n{prompt}\n\nAnalyze from the {role_1} perspective.",
  model: "{model}"
}
Agent tool 2: { ...same shape with {role_2}... }   // one call per role, all in one message
```

### Result

Verify one result per dispatched role; re-dispatch any role that returned nothing.

```
📡 [broadcast] {N} agents ({roles}) completed

## 🔒 Security
{result}

## ⚡ Performance
{result}

## 🧩 Logic
{result}
```

---

## Primitive: status

Show the list of agents currently running in the background.

```
📊 [status] Active agents

  🔵 agent-1: security review     running (45s)
  🔵 agent-2: performance check   running (45s)
  ✅ agent-3: logic review         completed (32s)
```

This information is tracked from Claude Code's internal state. No separate storage required.

---

## Role Presets

See `references/role-presets.md` — catalog of agent role presets (name, description, model, prompt template). Used by x-agent primitives and x-op strategies when assigning agent roles.

---

## Team System

Hierarchical team structure: Director (user) → Team Leader → Members.

> Detailed documentation: [TEAM.md](./TEAM.md) — team definition format, communication protocols, TL Protocol, subcommand details, built-in templates.
> When executing a `team` command, read TEAM.md and follow the instructions in the relevant section.

```
Director (user + leader Claude)
  ├── Team Leader (opus, named agent) → manages members via fan-out/delegate/broadcast
  └── Cross-team: Director routes TL ↔ TL messages
```

| Command | Action |
|------|------|
| `team create <name> [--template <t>]` | Create a team (template or dynamic) |
| `team list` | List active teams |
| `team status [name]` | Team progress report |
| `team assign <team> <goal>` | Assign goal to team → TL executes |
| `team report [name]` | Request report from TL |
| `team coord <from> <to> <msg>` | Route cross-team message |
| `team disband [name]` | Disband a team |
| `team templates` | List available templates |

Built-in templates: `engineering`, `design`, `review`, `research`, `fullstack` (`.xm/teams/`)

---

## x-op vs x-agent: When to Use Which

| Situation | Use | Why |
|-----------|-----|-----|
| Known unknowns — you know what angles to explore | **x-op** (investigate, review) | Leader assigns angles, structured phases |
| Unknown unknowns — you don't know what you'll find | **x-agent** (research) | Agents self-discover, board-driven adaptation |
| Structured debate with roles | **x-op** (council, debate) | Leader mediates, weighted voting |
| Organic agreement — best argument wins | **x-agent** (consensus) | Peer positions on board, self-revision |
| Known task list to parallelize | **x-op** (distribute) | Leader splits and assigns upfront |
| Emergent tasks discovered during work | **x-agent** (swarm) | Agents add tasks to board dynamically |
| Fixed hypothesis → falsification | **x-op** (hypothesis) | Leader collects → assigns verification |
| Try different approaches, learn from failures | **x-agent** (solve) | Agents post attempts, adopt/abandon on board |

## How x-op uses primitives

x-op strategies use x-agent primitives internally (design intent — x-op implements its own agent management):

| x-op strategy | Primitive used |
|-----------|------------------|
| refine (diverge) | fan-out |
| refine (converge/verify) | fan-out (voting/verification) |
| tournament (compete) | fan-out |
| tournament (vote) | fan-out |
| chain | delegate (sequential) |
| review | broadcast (per-perspective) |
| debate (opening) | delegate x 2 (PRO/CON) |
| debate (rebuttal) | delegate x 2 |
| debate (verdict) | delegate x 1 (JUDGE) |
| red-team (attack) | fan-out |
| red-team (defend) | fan-out |
| brainstorm | fan-out |
| distribute | broadcast (per-subtask) |
| council | fan-out → broadcast → fan-out |

## How x-build uses this

x-build's `run` command uses x-agent:

| x-build command | Primitive used |
|----------------|------------------|
| `run` (step execution) | fan-out or broadcast (different prompts per task) |
| `plan` (AI decomposition) | delegate (planner role, opus) |
| `quality` (verification) | delegate (verifier role) |
| `run --team` (team execution) | team assign (TL uses fan-out/delegate internally) |

---

## Subcommand: flow

See [flow.md](./flow.md) — high-parallelism backend that runs fan-out work through the deterministic **Workflow tool** (queued, up to 1000 agents, JSON-schema-forced merge, dependency levels, background + resume) instead of manual Agent-tool calls. Decompose modes: (a) inline-scout — leader decomposes and shows a human-checkable plan (default for generic `flow "<goal>"`); (b) in-script roster — engine's first agent emits the leaf list (default for `--op` presets). The engine `flow/flow-template.mjs` is read and passed inline as the Workflow `script`; the leader persists the return to `.xm/flow/`. Use for unattended diverge→merge; NOT for x-op strategies that gate on AskUserQuestion mid-run.

For step-by-step composition where the user controls each step, chain primitives directly (`fan-out` → `delegate architect` → `broadcast`) — same shape as x-op's `chain`.

---

## Autonomous: research

See `autonomous/research.md` — agents self-direct exploration via stigmergy (shared board.jsonl); each round: read board→frame question→explore→post finding→judge; supports `--agents`, `--budget`, `--depth shallow|deep|exhaustive`, `--focus`, `--web`; leader cross-validates findings (2+ agents = HIGH confidence) vs x-op investigate's pre-assigned angles.

---

## Autonomous: solve

See `autonomous/solve.md` — agents try different angles (read board→frame→try→post attempt/insight/abandon/adopt→verify); early termination when any agent posts "solved"; supports `--agents`, `--budget`, `--target`, `--verify`; board accumulates failed attempts so no agent repeats a dead end vs x-op hypothesis's leader-assigned falsification.

---

## Autonomous: consensus

See `autonomous/consensus.md` — agents independently post positions (hold/revise/challenge/concede) to a shared board each round; convergence emerges naturally; supports `--agents`, `--budget`, `--perspectives`; leader detects FULL/STRONG/PARTIAL/NO CONSENSUS outcome vs x-op council's leader-mediated voting.

---

## Autonomous: swarm

See `autonomous/swarm.md` — agents self-select tasks from a shared JSONL board (claim→execute→post result→add discovered tasks); supports `--agents`, `--budget`, `--seed`; dynamic load balancing and emergent task discovery vs x-op distribute's fixed upfront split.

---

## Trace Recording

Tracing is automatic: the trace-session hook writes `session_start` when the skill is invoked, one `agent_step` per Agent tool call made before the assistant turn ends, and `session_end` at the turn's Stop hook. Do not hand-write those three row types; `fan_out`/`synthesize` stay LLM-written, metadata only, as x-trace describes.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this sequentially, parallelism is overhead" | For N independent tasks, sequential is N× time. Parallelism overhead is fixed; serialization cost is linear in N. Measure before assuming. |
| "This is too small to delegate" | Delegation isn't about task size — it's about context isolation. Small tasks that stuff the main context window cost more than a subagent run. |
| "Delegating costs tokens" | Not delegating costs context window, which costs the entire session. Subagent tokens are cheap; a polluted main context is expensive and unrecoverable. |
| "I'll just stuff the files into my context" | Context stuffing is how sessions degrade. Delegate the reading, keep the reasoning. The main agent should hold judgment, not raw data. |
| "Broadcast is for research, not real work" | Broadcast is for anything where multiple independent perspectives help. If three agents looking at the same thing would help, it's a broadcast. |
| "Swarm is overkill for this" | Swarm is for 5+ genuinely independent exploration paths. If you have 5+, it's not overkill — it's the right primitive. |
| "Fan-out results are hard to merge" | The fan-out primitive returns structured results so merging is part of the contract. If you're hand-merging, you're using it wrong. |
