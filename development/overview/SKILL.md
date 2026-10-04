---
name: overview
description: "Cross-technology entry point for agentic AI: choosing the implementation layer (harness vs Agent SDK vs raw model API vs managed agents), workflow-vs-agent architecture and the five workflow patterns, multi-agent orchestration, context engineering, comparing the coding-agent harness landscape (Claude Code, OpenAI Codex, GitHub Copilot, Cursor, pi, Google Gemini CLI), and enterprise agent rollout. WHEN: \"how should we build this agent\", \"agent or workflow\", \"agent architecture\", \"prompt chaining\", \"orchestrator-workers\", \"evaluator-optimizer\", \"multi-agent orchestration\", \"handoffs vs agents-as-tools\", \"context engineering\", \"context rot\", \"compaction\", \"Claude Code vs Codex vs Copilot vs Cursor vs Gemini CLI\", \"which coding agent should we standardize on\", \"rolling out AI agents across the enterprise\". NOT for operating or configuring any one harness — Claude Code (claude-code), OpenAI Codex (codex), GitHub Copilot (github-copilot), Cursor (cursor), pi (pi). NOT for building on a specific agent SDK — Claude Agent SDK (claude-agent-sdk), OpenAI Agents SDK (openai-agents-sdk), Google ADK (google-adk). NOT for Messages API mechanics (claude-api), the MCP spec or servers (mcp), authoring SKILL.md files (agent-skills), picking a model (model-selection), prompt injection and AI governance (ai-security), isolation/egress mechanics (sandboxing), model tuning or datasets (fine-tuning, training-datasets), or eval harnesses (evals)."
license: MIT
---

# Agentic AI — Domain Overview

The routing skill for cross-cutting "how should we build this with AI agents?" questions. It owns four decisions that come *before* any product-specific work: which layer to build on, whether the thing is a workflow or an agent, how to orchestrate multiple agents, and how to budget context. It also carries the cross-vendor harness comparison and enterprise rollout guidance.

Always answer the layer and workflow-vs-agent questions first, then hand off to the specific sibling skill. Never re-derive a sibling's depth here — this skill is the map, not the territory. Comparison and selection are what this skill owns; the moment a question becomes "how do I configure/run *this* tool", route it to that tool's own skill.

## Routing map

| The question is about… | Go to |
|---|---|
| Configuring/deploying the Claude Code harness (settings, permissions, hooks, subagents, plugins, headless CI) | `claude-code` |
| Operating OpenAI Codex — CLI, `config.toml`, approvals/sandbox, `codex exec`, Codex cloud | `codex` |
| Operating GitHub Copilot — IDE/agent mode, the coding agent, Copilot CLI, enterprise policies | `github-copilot` |
| Operating Cursor — modes, rules, permissions, hooks, cloud/background agents, `cursor-agent` | `cursor` |
| Operating pi (pi.dev) — TUI/print/RPC/SDK modes, settings, extensions, provider switching | `pi` |
| Building a custom agent in TypeScript/Python on the Claude Agent SDK | `claude-agent-sdk` |
| Building an agent on the OpenAI Agents SDK (Python `openai-agents` / TS `@openai/agents`) | `openai-agents-sdk` |
| Building an agent on Google ADK (LlmAgent, workflow agents, tools, sessions) | `google-adk` |
| Raw Messages API — model IDs, tool use, streaming, caching, batches, structured outputs | `claude-api` |
| MCP itself — spec, transports, primitives, OAuth, writing or consuming servers | `mcp` |
| Writing a `SKILL.md`, progressive disclosure, skill authoring | `agent-skills` |
| Which frontier model / capability tier across Anthropic, OpenAI, Google | `model-selection` |
| Prompt injection, tool poisoning, OWASP GenAI risks, AI governance frameworks | `ai-security` |
| Isolation and egress control mechanics for running agents safely | `sandboxing` |
| Training or tuning a model (LoRA/QLoRA/GRPO, hosted tuning APIs) | `fine-tuning` |
| Building training data (formats, quality, synthetic data) | `training-datasets` |
| Measuring models, agents, or skills — graders, LLM-as-judge, regression suites | `evals` |
| SIEM/EDR/WAF/SAST platform tooling | the marketplace's `security` plugin |
| Kubernetes/container runtime depth under an agent platform | the marketplace's `containers` plugin |

## Decision 1 — pick the layer

Always name the layer explicitly before designing anything. Four layers exist; teams routinely pick one heavier than their problem needs.

| Situation | Layer | Why |
|---|---|---|
| Interactive development, one-off terminal tasks, a human in the loop | **CLI harness** (Claude Code, Codex CLI, Gemini CLI) | Batteries-included agent loop, filesystem config, zero code to write |
| You want an agent but not to implement the tool loop | **Agent SDK** (Claude Agent SDK, OpenAI Agents SDK) | The harness's loop, tools, context management, and guardrails embedded in your own process |
| You need full manual control of every model call and tool execution | **Raw model API** (Anthropic Client SDK / Messages API, OpenAI Responses API) | Bespoke orchestration that doesn't fit an agent-loop's assumptions |
| Long-running or async agents, and you don't want to run sandbox/session infra | **Managed Agents** (Anthropic-hosted REST API) | Anthropic runs the agent and the sandbox |

Directives:

- Always start at the harness when a human is driving. Reach for the SDK only when the work must run headless, at scale, or inside a larger system. Every step down the ladder is code you now own forever.
- The Claude Agent SDK is "Claude Code as a library" — same loop, tools, and context management, in **Python and TypeScript only**. From any other language, drive the CLI as a subprocess with `-p --output-format json` rather than reimplementing the loop.
- Never assume harness config is lost when you move to the SDK: skills, commands, memory, and plugins still load from `.claude/` and `~/.claude/`.
- If you are building a product on the Agent SDK, check the branding and auth constraints before you name it — "Claude Code" branding is not permitted for third parties, and claude.ai login cannot be offered inside a third-party SDK product without prior approval.

Read `references/layer-selection.md` when the user is weighing SDK-vs-API, comparing Anthropic's four-way split against OpenAI's Responses-API-vs-Agents-SDK split, or asking what the five agent primitives are.

## Decision 2 — workflow or agent

The line is control flow, not sophistication:

- **Workflow** — LLMs and tools orchestrated through *predefined code paths*.
- **Agent** — the LLM *dynamically directs its own process* and tool usage.

Directives:

- Always find the simplest thing that passes evaluation — often a single well-tooled LLM call, frequently a workflow, sometimes not an agentic system at all. Every autonomous turn adds latency, tokens, and the chance an early mistake propagates.
- Use an agent only for open-ended problems with an unpredictable number of steps where you cannot hardcode the path but *can still verify progress*. No verification signal means no agent.
- Never deploy an agent outside a sandboxed environment with guardrails — autonomy implies trusting its decisions, so bound the blast radius mechanically. Hand the mechanics to `sandboxing`.
- Build the augmented LLM first: one model plus curated retrieval, tools, and memory, with clear documented interfaces. MCP is one way to wire in third-party tools.

The five workflow patterns, in ascending autonomy:

| Pattern | Use when |
|---|---|
| **Prompt chaining** | The task decomposes into fixed sequential subtasks; accuracy matters more than latency; add programmatic gates between steps |
| **Routing** | Inputs fall into distinct categories handled better separately, and classification is reliable |
| **Parallelization** | Independent subtasks (sectioning) or repeated attempts aggregated for confidence (voting) |
| **Orchestrator-workers** | Subtasks cannot be predicted in advance — a central LLM decomposes, delegates, then synthesizes |
| **Evaluator-optimizer** | Clear evaluation criteria exist and iterative critique measurably improves the output |

Orchestrator-workers is the first genuinely agentic pattern: it differs from parallelization precisely because the subtasks are not predefined.

Read `references/workflow-patterns.md` for each pattern's mechanism and worked examples, the three agent design principles, and the tool-definition (agent-computer interface) rules.

## Decision 3 — orchestration, only after one agent demonstrably fails

Start with one agent whenever you can. Add specialists only when they demonstrably improve capability isolation, policy isolation, prompt clarity, or trace legibility — premature splitting adds prompts and traces without improving the workflow.

Three failure modes justify separate context windows, and they are the diagnostic to look for before splitting:

1. **Agentic laziness** — the agent stops before finishing a complex multi-part task after partial progress.
2. **Self-preferential bias** — it favors its own prior findings when independent verification is what's needed.
3. **Goal drift** — fidelity to the original objective decays across many turns.

Named orchestration patterns worth reaching for by name:

- **Classify-and-Act** / **Routing** — classify, then dispatch to a specialized agent.
- **Fan-Out-and-Synthesize** — parallel agents, structured merge at a synchronization barrier.
- **Adversarial Verification** — a separate rubric-driven verifier judges the primary agent's output.
- **Tournament** — N differing approaches, pairwise judged.
- **Loop Until Done** — repeat until explicit stop conditions, never a fixed iteration count.
- **Generate-and-Filter** — many candidates, then quality-filter and dedupe.
- **Handoffs** (decentralized) — control transfers wholly to a specialist for that branch.
- **Manager pattern** (centralized) — the orchestrator keeps control and calls specialists as bounded tools, synthesizing the final answer itself.

Constraints that make multi-agent work in practice: set explicit per-subagent token budgets; keep resource-intensive commands out of parallel branches so branches don't contend; isolate overlapping work in separate git worktrees; give verification agents a skeptic persona so they don't rubber-stamp; keep each specialist's job narrow and its handoff description short and concrete.

Never apply this to routine day-to-day work — multi-agent orchestration consumes far more tokens than a single agent and only pays off on complex, high-value tasks.

Read `references/orchestration.md` for the dynamic-workflows model, the full pattern catalog with mechanisms, and the handoff-vs-manager code shapes.

## Decision 4 — engineer the context

Context engineering is curating and maintaining the optimal set of tokens across the *whole* inference budget: system prompt, tool definitions, tool results, memory, retrieved data, and history — not just the opening instructions.

- Treat context as a finite resource with diminishing returns. **Context rot** is real: attention quality degrades as tokens compete, because self-attention creates n² pairwise relationships. A bigger window does not make extra context free.
- Write system prompts in the "Goldilocks zone" — sectioned with XML tags or Markdown headers, minimal at first, extended only in response to observed failure modes. Never pre-emptively encode imagined edge cases.
- Curate tools: self-contained, minimal functional overlap, unambiguous parameters. Bloated tool sets degrade tool-selection accuracy.
- Prefer a few diverse canonical few-shot examples over exhaustive edge-case enumeration.
- Default to **just-in-time retrieval**: hold lightweight identifiers (paths, URLs, queries) and load the data through tools at runtime. Pre-loading everything is the single most common context-budget mistake.
- Use **compaction** for long-horizon tasks — summarize history near the limit, preserving architectural decisions while dropping redundant tool output. The tension is recall vs precision.
- Use **structured note-taking** (e.g. a `NOTES.md`) for state that must survive dozens of tool calls.
- Use **subagents** for focused exploration in a clean window, returning ~1,000–2,000 token condensed summaries to the coordinator.

Read `references/context-engineering.md` for the full principles plus how a shipping harness implements them mechanically (skill description-vs-body loading, session persistence, the post-compaction skill re-attachment budgets).

## Harness landscape

This section is the comparison grid only. Operational depth for each harness lives in its own skill — `claude-code`, `codex`, `github-copilot`, `cursor`, `pi` — so answer "which one / how do they differ" here and route "how do I configure or run it" there. Gemini CLI has no dedicated skill; its coverage below and in `references/harness-landscape.md` is its only home.

Three major CLI coding-agent harnesses are compared below as of 2026-08-05. They have converged on the same shape — a memory/instruction file, a layered config file, MCP for external tools, a sandbox plus approval policy, a headless mode, and admin-managed enterprise overrides — so evaluate on that grid rather than on feature lists.

| Axis | Claude Code | OpenAI Codex CLI | Google Gemini CLI |
|---|---|---|---|
| Instruction file | `CLAUDE.md` + auto memory | `AGENTS.md` / `AGENTS.override.md` | `GEMINI.md` (filenames configurable, incl. `AGENTS.md`) |
| Config | `settings.json` (user / project / local / managed) | `config.toml` (user / project / system, plus profiles) | `settings.json` (system / workspace / user / defaults) |
| MCP config | `claude mcp add`, `.mcp.json`, scoped local/project/user | `[mcp_servers.<name>]` in `config.toml`, `codex mcp add` | `mcpServers` in `settings.json` |
| Safety model | Permission modes + hooks | `sandbox_mode` × `approval_policy` | `GEMINI_SANDBOX` mechanism + approval mode |
| Headless | `claude -p` (JSON output) | `codex exec --json` | `gemini -p` |
| Enterprise | Managed settings, managed MCP | `requirements.toml` (enforced) + `managed_config.toml` (defaults) | System `settings.json` + policy engine + wrapper script |

Directives:

- Standardize on one harness per org, then encode team rules in the instruction file and enforce them through the managed/system config layer — not through onboarding docs. Only Codex's `requirements.toml` and Gemini's system settings are *enforced*; managed defaults are merely starting values a user can change.
- Always keep required team guidance in the checked-in instruction file, not in per-user "memories" — memories are a recall layer, not the source of truth for rules that must always apply.
- Never run any harness with sandboxing and approvals both disabled (`--yolo`, `danger-full-access`, YOLO mode) outside an already-hardened, disposable environment. Running arbitrary model-generated shell commands requires sandboxing, resource limits, command filtering, and logging before production use.
- Nested instruction files beat root ones in both Codex and Gemini (later in the concatenation wins), so scope overrides by directory rather than growing one large file.

Read `references/harness-landscape.md` for per-harness install, auth, config keys, sandbox mechanisms, headless flags, and enterprise controls — at comparison depth. Beyond the grid, go to the owning skill: `claude-code`, `codex`, `github-copilot`, `cursor`, or `pi`.

## Enterprise adoption

- Be deliberately strategic, not broad-and-shallow. Sustained returns come from deployments that compound; assume no deployment compounds automatically.
- Target revenue-generating capability, not only cost reduction, and encode institutional knowledge into systems so value accumulates.
- Keep human-in-the-loop oversight at critical decision points. Compress high-friction information workflows while deliberately preserving human judgment where decisions are made — do not automate the decision away.
- Map upskilling to specific organizational processes rather than generic AI-literacy training.
- Phase the rollout (a structured six-month rollout is the vendor-suggested shape for a platform like Claude Cowork) instead of an enterprise-wide big-bang.

Read `references/enterprise-adoption.md` before advising on rollout governance; it also records which vendor material was *not* verifiable, so you don't state unverified specifics as fact.

## Anti-patterns

- Building an agent when a workflow (or one augmented LLM call) passes eval — the default failure of new agent projects.
- Splitting into multiple agents before a single agent has demonstrably failed on laziness, bias, or goal drift.
- Pre-loading every possibly-relevant document instead of just-in-time retrieval.
- Growing tool sets without curation, then blaming the model for wrong tool selection.
- Treating tool definitions as an afterthought — they deserve the same rigor and testing as prompts.
- Relying on a subagent's report being trustworthy: reports can carry untrusted text from files, web pages, and command output. Restrict what a subagent can reach; see `ai-security` for injection handling.
- Fixed iteration counts where explicit stop conditions belong.

## Reference files

- `references/layer-selection.md` — harness vs Agent SDK vs Client SDK vs Managed Agents; OpenAI's Responses-API-vs-Agents-SDK split; the five agent primitives; SDK licensing/branding constraints. Read for "what should we build on?"
- `references/workflow-patterns.md` — the five workflow patterns in detail, agent implementation principles, tool/agent-computer-interface design rules. Read when designing the control flow.
- `references/orchestration.md` — dynamic workflows, the six Claude Code orchestration patterns, OpenAI handoffs vs manager pattern, multi-agent context budgets. Read when one agent is not enough.
- `references/context-engineering.md` — context rot, system-prompt strategy, JIT retrieval, compaction, note-taking, subagent summaries, and how Claude Code enforces skill-content token budgets. Read for token-budget and long-horizon-task questions.
- `references/harness-landscape.md` — Claude Code, Codex CLI, and Gemini CLI: install, auth, config format, memory files, MCP wiring, sandbox/approval models, headless mode, enterprise controls. Read for harness selection or migration, not for operating a harness — `claude-code`, `codex`, `github-copilot`, `cursor`, and `pi` own that depth.
- `references/enterprise-adoption.md` — enterprise rollout pillars, production lessons, and explicitly flagged coverage gaps. Read for org-level adoption advice.

## Diagnostic scripts

- `scripts/01-harness-inventory.sh` — read-only inventory of which agent harnesses are installed and which instruction/config/MCP files exist for the current project and user. Run it before advising on harness standardization or migration.

## Sources

- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/claude_code_docs_map.md
- https://code.claude.com/docs/en/agent-sdk/overview
- https://code.claude.com/docs/en/mcp.md
- https://code.claude.com/docs/en/skills.md
- https://code.claude.com/docs/en/hooks.md
- https://code.claude.com/docs/en/sub-agents.md
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code
- https://claude.com/blog/building-ai-agents-for-the-enterprise
- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/agents/orchestration
- https://developers.openai.com/api/docs/guides/tools-local-shell
- https://github.com/openai/codex/blob/main/README.md
- https://github.com/openai/codex/blob/main/docs/config.md
- https://learn.chatgpt.com/docs/config-file/config-basic
- https://learn.chatgpt.com/docs/sandboxing
- https://learn.chatgpt.com/docs/agent-approvals-security
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/non-interactive-mode
- https://learn.chatgpt.com/docs/enterprise/managed-configuration
- https://learn.chatgpt.com/docs/extend/mcp?surface=cli
- https://github.com/google-gemini/gemini-cli
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/enterprise.md

Fetched: 2026-08-05
