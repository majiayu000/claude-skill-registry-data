---
name: mcp-toolchain-manager
description: 'Detect frontend tool capabilities, report gaps, verify official setup sources, plan approval-gated MCP changes, or update project/mcp-profile.md. Prefer capabilities over provider names; never install or configure without approval.'
id: 'agents.skills.mcp-toolchain-manager.skill'
title: 'MCP Toolchain Manager'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'mcp-toolchain-manager'
tags:
    - 'agents/skill-package'
    - 'agents/tooling'
    - 'workflow/mcp'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[skills/goal-planner/SKILL|Goal Planner]]'
    - '[[skills/execution-plan-manager/SKILL|Execution Plan Manager]]'
    - '[[skills/project-onboarding-adapter/SKILL|Project Onboarding Adapter]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# MCP Toolchain Manager

## Purpose

Detect, explain, validate, and record tool capabilities needed by WebDev Agent Kit skills without turning tool setup into automatic or unsafe behavior.

This skill exists to keep MCP usage deliberate. It identifies which capabilities are required for the current workflow, which providers are already available, which providers are missing, what each missing capability blocks, which fallback is allowed, and what official source must be verified before installation or configuration is proposed.

## When To Use

Use this skill when:

- a selected skill declares capability dependencies in `tool-capabilities-manifest.json`;
- a task requires rendered UI verification, official documentation lookup, project context retrieval, visual references, GitHub metadata, or another external capability;
- the agent needs to audit available vs missing MCP servers, native tools, connectors, or fallbacks;
- the user asks what MCP servers or tools are required for the skill pack;
- the user asks to install, configure, validate, or troubleshoot MCP tools;
- `project/mcp-profile.md` must be created or refreshed;
- a missing tool limitation must be reported before fallback behavior.

Use this skill in `Standard Workflow` or `Deep Workflow` when tool capability affects the current slice.

It may also be used in `Lightweight Workflow` only when the user directly asks about MCP/tool availability or when a missing already-required capability prevents a narrow task from being verified.

## When Not To Use

Do not use this skill just because a task exists.

Do not use this skill for:

- one small bug when no external tool is needed;
- one obvious type error;
- one small styling adjustment that does not require rendered verification;
- documentation-only edits unrelated to MCP/tooling;
- generic planning that does not depend on tool capabilities.

Do not install tools from this skill unless the user explicitly approved that installation in the current task context and the official source was verified.

Do not use this skill to implement frontend code, write tests, scaffold projects, create UI library setups, or access production systems.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/tool-capability-model.md`.
3. Read `common/mcp-installation-policy.md` when installation or configuration is in scope.
4. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
5. Read `tool-capabilities-manifest.json` for selected skills and capabilities.
6. Read `common/codex-official-docs-policy.md` only when `openai_platform_docs` is active.
7. Read selected `agents/openai.yaml` files only when Codex UI or invocation metadata matters; never use them as capability declarations or availability evidence.
8. Read `project/mcp-profile.md` when it exists and the task needs durable tool state.
9. Read `project/verification-profile.md` only when verification commands influence tool needs.
10. Do not read all skills or all YAML files during normal routing.

## Tool Contract

- May read `tool-capabilities-manifest.json`, selected skill metadata, Codex UI metadata when relevant, and local-only `project/mcp-profile.md`.
- May read or update `project/mcp-profile.md` when durable tool state is needed.
- May search official documentation only to verify installation sources or current client/tool docs.
- For active OpenAI questions, prefer a callable official OpenAI Developer Docs MCP provider, then the official web fallback; do not call either for generic frontend facts.
- Must prefer declared capabilities over server-name assumptions.
- Must not install MCP servers without explicit user approval.
- Must not change Codex, Claude, Cursor, VS Code, MCP, shell, package manager, or project configuration without explicit user approval.
- Must not run package installs.
- Must not access production systems or secrets.
- Route live design inspection to `design-screenshot-spec`; this skill maps
  provider availability and does not acquire design content or edit canvases.

## Core Tool Capabilities

Core capability vocabulary is defined in `common/tool-capability-model.md` and `tool-capabilities-manifest.json`.

Expected high-value capabilities:

```text
project_files
command_execution
current_library_docs
web_platform_docs
rendered_visual_evidence
openai_platform_docs
client_platform_docs
repo_metadata
design_reference_files
```

Conditional design acquisition through `design-screenshot-spec`:

```text
live_design_source
```

Prefer callable Figma MCP reads; fall back to browser/computer use with canvas
pointer interaction and property-panel screenshots. Screenshot-only input needs
no live provider. The capability excludes design writes and automatic setup.

Core does not mean always installed or always used. Use only what the current workflow needs.

## Workflow

1. Identify the active task and selected skill chain.
   - Use prompt intent routing first.
   - Do not expand a lightweight task into tool setup unless the user asked for tool setup or the missing capability blocks required verification.

2. Collect required capability declarations.
   - Inspect `tool-capabilities-manifest.json` for selected skills.
   - Treat it as the only bundle source for required, conditional, optional, and blocked capabilities.
   - Inspect `agents/openai.yaml` only when Codex UI or invocation metadata must be aligned.
   - Record required, required-when-in-scope, optional, and blocked capabilities.
   - Do not scan every skill unless onboarding or full toolchain audit is explicitly requested.

3. Determine need for the current slice.
   - Required for this slice.
   - Required only when visual QA or another conditional workflow is in scope.
   - Useful but optional.
   - Not needed.
   - Explicitly blocked.

4. Compare capabilities with available providers.
   - Callable in the current session registry, including native host tools.
   - Recorded as validated in the local-only project profile.
   - Directly confirmed by the user only for supplied design references.
   - Missing.
   - Approved for install.
   - Installed and validated.
   - Skipped.
   - Blocked.
   - Unknown.

5. Explain missing capability impact.
   - State what cannot be verified or automated without the capability.
   - State the allowed fallback and confidence level when fallback is allowed.
   - Do not claim tool-based verification if the provider is missing.
   - Do not treat `package.json`, lockfiles, local Playwright dependencies, or a running dev server as proof of MCP availability.
   - Do not treat client config, provider names, or `agents/openai.yaml` as proof of availability.

6. Verify official install source when installation is relevant.
   - Use accepted sources from `common/mcp-installation-policy.md`.
   - Reject random snippets, search summaries, unofficial forks, and generated guesses.

7. Ask approval before installation or configuration changes.
   The approval request must name:
   - capability;
   - provider/server name;
   - target client and config scope;
   - reason;
   - official source;
   - install/config action;
   - expected validation step;
   - risks or scope.

8. Record toolchain state.
   Update `project/mcp-profile.md` only when durable state is useful for the project.

9. Hand off.
   Return to the selected frontend skill with:
   - capabilities available now;
   - missing capabilities;
   - active providers;
   - approved fallbacks;
   - verification limits.

## Project MCP Profile Output

When writing or updating `project/mcp-profile.md`, use these sections:

```text
Client
Capability State
Configured MCP Servers
Missing Capabilities
Optional Capabilities
Blocked Capabilities
Official Sources Verified
Approval State
Validation Results
Allowed Fallbacks
Confidence Impact
Last Updated
```

Tool entry shape:

```text
Capability
Status
Provider
Availability Evidence
Required By
Reason
Current Task Need
Official Source
Install Approved
Validation
Fallback
Confidence Impact
Notes
```

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return a Toolchain Report with:

```text
Task
Workflow Level
Selected Skill Chain
Required Capabilities
Available Capabilities
Available Providers
Missing Capabilities
Optional Capabilities
Blocked Capabilities
Official Sources Verified
Approval Needed
Allowed Fallbacks
Confidence Impact
MCP Profile Update
Next Skill Or Next Step
```

## Validation Gates

Before finishing, verify:

- no tool was installed without explicit approval;
- no config was changed without explicit approval;
- no package install was performed;
- official sources are recorded for proposed installations;
- missing capability limitations are explicit;
- fallback confidence is honest;
- `project/mcp-profile.md` was updated only when durable state is useful;
- server names were not treated as capabilities;
- local dependencies, config entries, provider names, or running servers were not reported as MCP availability;
- optional provider absence did not trigger installation work;
- no UI component library or testing skill was introduced;
- no production systems or secrets were accessed.

## Trigger Evals

Should trigger:

- "Check which MCP servers this skill pack needs."
- "Do we have Playwright MCP available for visual QA?"
- "Set up the MCP tools, but show me the official install sources first."
- "Update project/mcp-profile.md after onboarding."
- "This skill requires rendered visual evidence and MDN; tell me what is missing."
- "Which capabilities are missing for Cursor visual QA?"

Should not trigger:

- "Fix this TypeScript error."
- "Change this local CSS background color."
- "Run visual QA now with the browser tool that is already available."

## Reference Map

- `common/codex-official-docs-policy.md`
- `common/tool-capability-model.md`
- `common/mcp-installation-policy.md`
- `tool-capabilities-manifest.json`
- `common/prompt-intent-routing-rules.md`
- `project/mcp-profile.md`
