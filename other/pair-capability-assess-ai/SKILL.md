---
name: pair-capability-assess-ai
description: "Assess AI development tools using resolution cascade (Argument > Adoption > Assessment). Reads AI development guidelines, proposes AI tool choices with versions, writes AI section of tech-stack.md, composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-ai — AI Development Assessment

Evaluate and decide on AI development tools: AI assistants, MCP integrations, AI-specific SDKs, and models. Follows the resolution cascade.

## Arguments

| Argument  | Required | Description                                                                            |
| --------- | -------- | -------------------------------------------------------------------------------------- |
| `$choice` | No       | Override: skip assessment, use this AI tool directly (e.g. `claude-code`, `cursor`) |

## Composed Skills

| Skill              | Type       | Required                                    |
| ------------------ | ---------- | ------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records AI tool decision as ADL       |

## Proposal Target

The rendered adoption content is destined for this section — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — **AI section only**
- **Ownership**: AI section (shared file — /pair-capability-assess-stack owns core sections, /pair-capability-assess-testing owns testing section)

## Adoption File

- **Target**: [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — **AI section only**
- **Ownership**: AI section (shared file — /pair-capability-assess-stack owns core sections, /pair-capability-assess-testing owns testing section)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice. Check for conflicts with existing adoption.
4. **Verify**: Developer confirms. Proceed to Step 3.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) exist and contain a populated **AI** section?
2. **Skip**: If no AI section or empty, go to Path C.
3. **Act**: Read current AI adoption. Confirm it's valid.
4. **Check**: Does a corresponding decision record exist?
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2.

### Step 2: Read Guidelines

1. **Act**: Read AI development guidelines:
   - [AI Development README](../../../.pair/knowledge/guidelines/technical-standards/ai-development/README.md) — maturity model, tool selection matrix, implementation strategies
   - [AI Tools](../../../.pair/knowledge/guidelines/technical-standards/ai-development/ai-tools.md) — tool comparison and configuration
   - [MCP Integration](../../../.pair/knowledge/guidelines/technical-standards/ai-development/mcp-integration.md) — MCP protocol standards
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — AI requirements, team size
   - [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — existing stack (AI tools must integrate)
3. **Verify**: Guidelines and context loaded.

### Step 3: Evaluate Options

1. **Act**: Use the Tool Selection Decision Matrix from guidelines:
   - Evaluate tools on: Code Generation, Context Awareness, Architecture Review, Team Integration, Security/Privacy.
   - Consider: budget, team size, workflow integration, privacy requirements.

2. **Act**: Evaluate AI development areas:
   - **Primary AI assistant**: IDE-integrated tool (Cursor, Copilot, Claude Code, etc.)
   - **Strategic AI**: Architecture review, complex problem-solving tool
   - **MCP integration**: If applicable, MCP servers and protocol adoption
   - **AI-specific libraries**: SDKs, embedding tools, AI frameworks with versions

3. **Act**: Assess team's AI maturity level (from guidelines maturity model):
   - Level 1: Basic AI Assistance
   - Level 2: Integrated AI Workflows
   - Level 3: Strategic AI Architecture
   - Level 4: AI-Native Development

4. **Act**: Present recommendation:

   > **AI Development Recommendation:**
   > - Primary assistant: [tool] — [rationale]
   > - Strategic AI: [tool] — [rationale]
   > - MCP: [yes/no — details]
   > - AI maturity target: Level [N]
   > - Additional tools: [list with versions]

5. **Verify**: Developer approves.

### Step 4: Write Adoption File

1. **Act**: Write or update **only the AI section** of [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md):
   - AI assistants with versions/tiers
   - MCP integrations if applicable
   - AI-specific SDKs and libraries with versions
   - Preserve all other sections (core, testing)
2. **Verify**: AI section written. Other sections preserved.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural`
   - `$topic`: `ai-development-tools`
   - `$summary`: "[Primary tool] adopted as AI development assistant with [maturity level] target"
2. **Verify**: ADL created. Adoption consistent.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    AI Development
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [primary tool + maturity level + additional tools]
├── Adoption:  [tech-stack.md AI section — written | confirmed | updated]
├── Record:    [ADL path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes during Phase 2.
- **Output**: Returns decision summary and adoption file path.

When invoked **independently**:

- Full interactive flow. Developer commits changes.

## Edge Cases

- **tech-stack.md exists but no AI section**: Add AI section, preserve all other content.
- **Project doesn't use AI tools**: Write minimal section noting "AI development tools not adopted — [reason]".
- **Multiple AI assistants**: Document primary and secondary with roles (e.g. primary for coding, secondary for architecture review).
- **MCP adoption requires infrastructure changes**: Recommend composing /pair-capability-assess-infrastructure for infra implications.

## Graceful Degradation

- If AI development guidelines not found, use minimal assessment: ask developer for AI tool preferences.
- If `/pair-capability-record-decision` not installed, warn and skip recording.
- If tech-stack.md doesn't exist, create it with AI section. Warn: "Created tech-stack.md — core sections should be populated by /pair-capability-assess-stack."

## Notes

- AI tool decisions are **non-architectural** → produce ADL. Exception: if MCP integration fundamentally changes system architecture, use ADR.
- **Section ownership**: this skill writes ONLY the AI section of tech-stack.md.
- **Version tracking**: every AI tool includes version or tier (e.g. "Claude Code", "GPT-4o", "Cursor Pro").
- Educational content (AI development principles, best practices, WHY) stays in guidelines.
