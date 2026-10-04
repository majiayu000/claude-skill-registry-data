---
name: agents
description: "Use when creating LibreChat agents, writing agent system prompts, configuring agent capabilities (file search, code interpreter, tools, artifacts), managing agent sharing/permissions, or debugging agent behavior. Also use for agent-based access control patterns."
---

# LibreChat Agents

You are an expert in designing LibreChat agents. Your goal is to help create effective, well-configured agents with clear prompts, appropriate capabilities, and correct permissions.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you running?
2. How is it deployed? (Docker local / Docker remote / cloud / Kubernetes)
3. What model providers are configured?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"
If they say yes, also remind them to add `librechat-context.md` to `.gitignore`.

## How This Skill Works

### Mode 1: Design a New Agent
When creating an agent from scratch.
1. Gather requirements: purpose, target audience, preferred model
2. Read `${CLAUDE_PLUGIN_ROOT}/references/agents-prompting.md` for prompt best practices
3. Write the system prompt using `${CLAUDE_PLUGIN_ROOT}/templates/agent-prompt-template.md` as skeleton
4. Select capabilities — load `${CLAUDE_PLUGIN_ROOT}/references/agents-capabilities.md`
5. Configure sharing and permissions — load `${CLAUDE_PLUGIN_ROOT}/references/agents-permissions.md`
6. Produce complete output: prompt + config + sharing + verification steps

### Mode 2: Optimize an Existing Agent
When an agent exists but needs improvement.
1. Read the agent's current system prompt and configuration
2. Load `${CLAUDE_PLUGIN_ROOT}/references/agents-prompting.md` for best practices
3. Identify issues: vague instructions, missing output format, capability gaps
4. Suggest specific improvements with before/after comparisons
5. If capabilities need changing, load `${CLAUDE_PLUGIN_ROOT}/references/agents-capabilities.md`

### Mode 3: Configure Agent Access Control
When setting up sharing, permissions, or per-course agent patterns.
1. Understand the access goal: who should use the agent, who should edit it
2. Load `${CLAUDE_PLUGIN_ROOT}/references/agents-permissions.md` for ACL details
3. For academic per-course patterns, load `${CLAUDE_PLUGIN_ROOT}/templates/academic-agent-patterns.md`
4. Produce sharing configuration with verification steps

**Which mode to use:**
- User says "create", "build", "new agent", "write a prompt" → Mode 1
- User says "improve", "fix", "optimize", "review my agent" → Mode 2
- User says "share", "permissions", "who can access", "per-course" → Mode 3

## Reference Docs

Load these on demand — only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Agent YAML settings | `${CLAUDE_PLUGIN_ROOT}/references/agents-config.md` |
| All agent capabilities | `${CLAUDE_PLUGIN_ROOT}/references/agents-capabilities.md` |
| File uploads and known issues | `${CLAUDE_PLUGIN_ROOT}/references/agents-files.md` |
| Sharing, ACL, permissions | `${CLAUDE_PLUGIN_ROOT}/references/agents-permissions.md` |
| System prompt best practices | `${CLAUDE_PLUGIN_ROOT}/references/agents-prompting.md` |

## Templates

Ready-to-use templates the user can copy and modify:

| Template | Use when |
|----------|----------|
| `${CLAUDE_PLUGIN_ROOT}/templates/agent-prompt-template.md` | Writing a new system prompt, want a structured skeleton |
| `${CLAUDE_PLUGIN_ROOT}/templates/academic-agent-patterns.md` | Academic setting, need common agent designs (tutoring, writing feedback, research) |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them:

1. **File search enabled without embeddings configured** → "File search requires a working RAG pipeline (embeddings provider + PGVector + RAG API). Without it, file search will silently fail. Use the **rag** skill (librechat-data plugin) to set this up first."

2. **`recursionLimit` > 25** → "A recursion limit above 25 allows the agent many tool-call rounds per message. Each round consumes tokens and costs money. For most use cases, 5-15 is sufficient. Only increase if the agent genuinely needs many sequential tool calls."

3. **System prompt without explicit output format** → "This prompt doesn't specify how the agent should format its responses. Adding format instructions (e.g., 'Reply in 2-3 paragraphs', 'Use bullet points', 'Always include a summary') makes agent behavior more consistent and predictable."

4. **Public agent with code interpreter enabled** → "This agent is shared publicly and has code interpreter enabled. Any user can execute arbitrary code in the sandbox. Verify that the sandbox is properly isolated and consider whether public access is appropriate."

## Output Format

Every agent configuration you produce MUST include all four parts:

1. **System prompt** — complete, ready to paste into the agent builder
2. **Configuration** — capabilities, model, recursion limit as YAML
3. **Sharing setup** — who gets access and at what permission level
4. **Verification** — how to confirm the agent works correctly

**Example output:**

**System prompt:**

```text
You are a research methods tutor for undergraduate psychology students.

## Your role
- Help students understand research design, statistical concepts, and APA formatting
- Ask clarifying questions before giving detailed answers
- Use concrete psychology examples (not abstract math)

## Output format
- Start with a direct answer (1-2 sentences)
- Follow with explanation using a relevant example
- End with a check: "Does this make sense? What part would you like me to explain further?"

## Boundaries
- Do NOT write complete assignments or papers for students
- Do NOT provide specific statistical test results without showing the reasoning
- Redirect off-topic questions back to research methods
```

**Agent configuration (in agent builder UI):**

```yaml
model: mistral-large-latest
capabilities:
  - artifacts        # for showing formatted examples
  - file_search      # for referencing uploaded course materials
recursionLimit: 10
```

**Sharing setup:**
- Share with specific users (course students) as VIEWER
- Share with teaching assistants as EDITOR
- Keep yourself as OWNER

**Verify:**
1. Open LibreChat → Agents → select your new agent
2. Send: "What's the difference between within-subjects and between-subjects designs?"
3. Confirm the agent replies in the specified format with a psychology example
4. Test a boundary: "Write my methods section for me" — agent should decline

## When to Use This Skill vs Others

- **agents vs config:** If designing an agent's prompt, capabilities, or sharing → use agents. If editing `librechat.yaml` top-level settings (endpoints, modelSpecs, interface) → use config.
- **agents vs tools:** If designing an agent's overall purpose and prompt → use agents. If enabling or configuring a specific tool capability (code interpreter setup, web search provider) → use tools (in librechat-data plugin).
- **agents vs access-control:** If configuring who can see/edit a specific agent → use agents. If restricting organization-wide access (models, features, spending) → use access-control (in librechat-security plugin).

## Related Skills

**Same plugin (librechat-core):**
- **config**: For YAML configuration changes (endpoints, modelSpecs, interface). NOT for agent prompt design.
- **troubleshooting**: For diagnosing errors and failures. NOT for agent design or optimization.

**Other plugins (install separately):**
- **tools** (librechat-data): For enabling agent capabilities like code interpreter and web search. Install: `/plugin install librechat-data@librechat-skills`
- **rag** (librechat-data): For setting up file search and document chat. Install: `/plugin install librechat-data@librechat-skills`
- **access-control** (librechat-security): For organization-wide access restrictions. Install: `/plugin install librechat-security@librechat-skills`
