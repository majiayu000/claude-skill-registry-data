---
name: claude-cookbooks
description: Look up examples and patterns from the official Anthropic Claude Cookbooks repository. Use when you need reference implementations, code examples, or best practices for Claude integrations, tool use, agents, prompting techniques, or API usage.
---

<objective>
Access the official Anthropic Claude Cookbooks repository (https://github.com/anthropics/claude-cookbooks) to find reference implementations, code examples, and best practices. This skill helps you find working examples for common Claude integration patterns.
</objective>

<repository_structure>
The Claude Cookbooks repository contains categorized examples:

**skills/** - Claude Code skill examples
- Building custom skills
- Skill patterns and templates
- Progressive disclosure techniques

**misc/** - Miscellaneous examples
- Various integration patterns
- Utility functions

**third_party/** - Third-party integrations
- AWS Bedrock examples
- Google Vertex AI examples
- Framework integrations (LangChain, etc.)

**tool_use/** - Tool calling examples
- Function calling patterns
- Tool definition best practices
- Multi-tool orchestration

**multimodal/** - Vision and document examples
- Image processing
- PDF handling
- Multi-modal prompting

**prompt_engineering/** - Prompting techniques
- System prompt patterns
- Few-shot examples
- Chain-of-thought techniques

**agents/** - Agentic patterns
- Agent architectures
- Multi-agent coordination
- Tool-using agents
</repository_structure>

<quick_start>
<workflow>
1. Identify what you're looking for (tool use, agents, skills, etc.)
2. Fetch the repository index to find relevant notebooks/examples
3. Fetch specific example files for detailed implementation
4. Adapt the patterns to your use case
</workflow>

<example title="Find tool use examples">
```
User: I need examples of how to define tools for Claude

Action: Fetch https://github.com/anthropics/claude-cookbooks/tree/main/tool_use
        to see available tool use examples, then fetch specific notebooks
```
</example>

<example title="Find skill examples">
```
User: Show me how to build a Claude Code skill

Action: Fetch https://github.com/anthropics/claude-cookbooks/tree/main/skills
        to find skill implementation patterns
```
</example>
</quick_start>

<lookup_urls>
<base_url>https://github.com/anthropics/claude-cookbooks/tree/main</base_url>

<category name="skills">
https://github.com/anthropics/claude-cookbooks/tree/main/skills
</category>

<category name="tool_use">
https://github.com/anthropics/claude-cookbooks/tree/main/tool_use
</category>

<category name="agents">
https://github.com/anthropics/claude-cookbooks/tree/main/agents
</category>

<category name="multimodal">
https://github.com/anthropics/claude-cookbooks/tree/main/multimodal
</category>

<category name="prompt_engineering">
https://github.com/anthropics/claude-cookbooks/tree/main/prompt_engineering
</category>

<category name="third_party">
https://github.com/anthropics/claude-cookbooks/tree/main/third_party
</category>

<category name="misc">
https://github.com/anthropics/claude-cookbooks/tree/main/misc
</category>

<raw_content_base>
For fetching actual file content, use raw GitHub URLs:
https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/{path}
</raw_content_base>
</lookup_urls>

<usage_patterns>
<pattern name="browse_category">
**When user wants to see what examples exist:**
1. Use WebFetch on the category URL
2. List available notebooks/files
3. Ask which specific example to explore
</pattern>

<pattern name="fetch_example">
**When user needs a specific example:**
1. Use WebFetch on the raw GitHub URL for the file
2. Extract relevant code patterns
3. Explain how to adapt for user's context
</pattern>

<pattern name="search_pattern">
**When user describes a problem:**
1. Identify likely category (tool_use, agents, skills, etc.)
2. Fetch category listing
3. Find most relevant example
4. Fetch and explain the implementation
</pattern>
</usage_patterns>

<common_lookups>
| Need | Category | Example File |
|------|----------|--------------|
| Define tools for Claude | tool_use | calculator_tool.ipynb |
| Build a skill | skills | various SKILL.md examples |
| Multi-agent patterns | agents | agent examples |
| Image/PDF processing | multimodal | vision examples |
| AWS Bedrock setup | third_party | bedrock examples |
| Prompting techniques | prompt_engineering | various notebooks |
</common_lookups>

<workflow_for_lookup>
<step n="1">
**Identify the domain**: What type of example does the user need?
- Tool calling → tool_use/
- Skills/commands → skills/
- Agent patterns → agents/
- Vision/docs → multimodal/
- Cloud providers → third_party/
- Prompting → prompt_engineering/
</step>

<step n="2">
**Fetch the category index**:
```
WebFetch: https://github.com/anthropics/claude-cookbooks/tree/main/{category}
Prompt: List all available examples and notebooks in this directory
```
</step>

<step n="3">
**Fetch specific example**:
```
WebFetch: https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/{category}/{filename}
Prompt: Extract the key implementation patterns and code examples
```
</step>

<step n="4">
**Apply to context**: Adapt the example patterns to the user's specific use case
</step>
</workflow_for_lookup>

<success_criteria>
- Found relevant example from cookbooks
- Fetched actual implementation code
- Explained how to adapt for user's needs
- Provided working code based on official patterns
</success_criteria>
