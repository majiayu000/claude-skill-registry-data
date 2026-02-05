---
name: meta-agent
description: Generates new Claude Code subagent configuration files from user descriptions. Use proactively when the user asks to create a new subagent or agent. Keywords include create subagent, new agent, build agent, agent architecture.
---

# Meta Agent

Creates complete, ready-to-use Claude Code subagent configuration files. This skill acts as an expert agent architect that analyzes requirements and generates properly structured subagent definitions with appropriate tools, prompts, and workflows.

## Instructions

### Prerequisites

- Understanding of the task or domain the subagent should handle
- Access to Claude Code documentation for latest features
- `.claude/agents/` directory for project-level agents (recommended)

### Workflow

1. **Get latest documentation**:
   - Fetch updated subagent documentation:
     ```
     https://docs.claude.com/en/docs/claude-code/sub-agents
     ```
   - Fetch available tools reference:
     ```
     https://docs.claude.com/en/docs/claude-code/settings
     ```
   - Use Firecrawl Scrap (if available) or WebFetch to ensure you have current information

2. **Analyze the user's requirements**:
   - Understand the subagent's purpose and primary tasks
   - Identify the domain or specialization
   - Determine what tools will be needed
   - Consider when this agent should be invoked

3. **Generate the subagent name**:
   - Use kebab-case format (e.g., `code-reviewer`, `api-tester`)
   - Make it descriptive but concise
   - Ensure it clearly indicates the agent's purpose
   - Must use only lowercase letters and hyphens

4. **Select appropriate color**:
   - Choose from: red, blue, green, yellow, purple, orange, pink, cyan
   - Use color to indicate agent type or domain:
     - cyan/blue: technical/code tasks
     - green: testing/validation
     - yellow: documentation/analysis
     - red: debugging/critical tasks
     - purple: data/research tasks

5. **Write the delegation description**:
   - This is CRITICAL for automatic delegation
   - State clearly WHEN to use the agent
   - Use action-oriented language
   - Include trigger phrases
   - Examples:
     - "Expert code reviewer. Use proactively after code changes to check quality, security, and maintainability."
     - "Debugging specialist. Use when errors occur or tests fail to analyze and fix issues."
   - Keep under 200 characters but be specific

6. **Determine minimal tool set**:
   - **IMPORTANT**: If tools aren't specifically mentioned by the user, OMIT the tools field entirely
   - Omitting tools allows the agent to inherit ALL tools from the parent thread
   - Only restrict tools if the user explicitly wants to limit capabilities
   - Available tools (if restricting):
     - **Read**: Read file contents
     - **Write**: Create new files
     - **Edit**: Modify existing files
     - **Bash**: Execute shell commands
     - **Glob**: Find files by pattern
     - **Grep**: Search file contents
     - **WebFetch**: Fetch web content
     - **WebSearch**: Search the web
     - **TodoWrite**: Manage task lists
     - **Task**: Invoke other subagents
     - **NotebookRead**: Read Jupyter notebooks
     - **NotebookEdit**: Edit Jupyter notebooks
   - Common restricted tool combinations (only use if specified):
     - Code reviewer: `Read, Grep, Glob`
     - Debugger: `Read, Edit, Bash, Grep, Glob`
     - File creator: `Write, Read, Glob`
     - Data analyst: `Bash, Read, Write`

7. **Select the model**:
   - **Default to `sonnet`** if not specified by the user
   - **sonnet**: Balanced performance (recommended default)
   - **opus**: Maximum capability for complex tasks
   - **haiku**: Fast, lightweight for simple tasks

8. **Construct the system prompt**:
   - Read the template: [templates/subagent-template.md](templates/subagent-template.md)
   - Fill in placeholders:
     - `{{AGENT_NAME}}`: kebab-case name
     - `{{DESCRIPTION}}`: Delegation description
     - `{{TOOLS}}`: Comma-separated tool list OR omit the entire `tools:` line if inheriting all tools
     - `{{COLOR}}`: Selected color
     - `{{MODEL}}`: Selected model (default: `sonnet`)
     - `{{AGENT_TITLE}}`: Title case name for display
     - `{{PURPOSE_DEFINITION}}`: Role definition (e.g., "a senior code reviewer focused on quality and security")
     - `{{INSTRUCTIONS}}`: Bullet-point list of additional guidance, constraints, or best practices
     - `{{WORKFLOW_STEPS}}`: Numbered step-by-step instructions
     - `{{REPORT_FORMAT}}`: Structure for the agent's output

9. **Write instructions section**:
   - Include arbitrary bullet points that add useful context
   - Examples of what to include:
     - Important constraints or limitations
     - Best practices specific to this agent's domain
     - Edge cases to watch for
     - Preferred approaches or patterns
     - Things to avoid
   - Format as bullet points:
     ```markdown
     - Focus on security-critical issues first
     - Use industry-standard naming conventions
     - Avoid making assumptions about user intent
     - When in doubt, ask for clarification
     ```

10. **Write detailed workflow steps**:
   - Provide clear, numbered instructions
   - Be specific about what to do at each step
   - Include examples where helpful
   - Consider edge cases and error handling
   - Format as a numbered list:
     ```markdown
     1. **First action**: Description of what to do
        - Additional context
        - Sub-steps if needed

     2. **Second action**: Next step
        ```bash
        command to run
        ```

     3. **Final action**: Conclusion
     ```

11. **Define the report structure**:
    - Specify how the agent should communicate results back
    - Include sections like:
      - Summary
      - Findings/Results
      - Recommendations
      - Next steps
    - Use markdown formatting
    - Make it easy for the main agent to parse

12. **Write the file**:
    - Save to `.claude/agents/<agent-name>.md`
    - Use the generated kebab-case name for the filename
    - Verify the file was created successfully

13. **Confirm creation**:
    - Inform the user the subagent was created
    - Show the file path
    - Explain how to use it (automatic or explicit invocation)
    - Suggest testing with a sample task

### Available Tools Reference

**File Operations:**
- `Read` - Read file contents
- `Write` - Create new files
- `Edit` - Modify existing files
- `Glob` - Find files by pattern
- `Grep` - Search file contents

**Execution:**
- `Bash` - Run shell commands

**Web:**
- `WebFetch` - Fetch URL content
- `WebSearch` - Search the web

**Specialized:**
- `NotebookRead` - Read Jupyter notebooks
- `NotebookEdit` - Edit Jupyter notebooks
- `TodoWrite` - Manage task lists
- `Task` - Invoke subagents
- `SlashCommand` - Execute slash commands
- `Skill` - Use other skills

**Best Practice:** By default, OMIT the tools field to inherit all parent tools. Only restrict tools if the user explicitly requests limitations for security or focus.

### Color Guide

- **cyan**: Technical, code-focused agents
- **blue**: Architecture, design, planning
- **green**: Testing, validation, verification
- **yellow**: Documentation, analysis, research
- **red**: Debugging, critical fixes, urgent tasks
- **purple**: Data science, research, investigation
- **orange**: Build, deployment, DevOps
- **pink**: UI/UX, design, creative tasks

## Examples

See [examples.md](examples.md) for comprehensive examples covering:

**Engineering Use Cases:**
- Code reviewer (inherit all tools)
- Debugging specialist (inherit all tools)
- Read-only code analyzer (restricted tools)
- SQL data analyst (custom model)

**Content & Creative Use Cases:**
- Transcription specialist (audio/video to text)
- YouTube script writer (hooks, structure, CTAs)
- Social media strategist (multi-platform content)
- Technical documentation writer (clear, comprehensive docs)

**Research & Analysis:**
- Research synthesizer (gather and synthesize information)

Each example includes detailed step-by-step walkthroughs showing how to analyze requirements, select appropriate settings, fill the template, and create the agent file.

## Tips

- **Single responsibility**: Each agent should do one thing well
- **Default to inheriting tools**: Omit the tools field unless user explicitly requests restrictions
- **Default to sonnet**: Use sonnet model unless user specifies haiku (fast) or opus (complex)
- **Clear delegation**: Write descriptions that clearly indicate when to use the agent
- **Detailed workflows**: More specific instructions lead to better results
- **Test immediately**: Create and test with a sample task to verify behavior
- **Version control**: Commit project agents to git for team sharing
- **Iterate**: Refine based on actual usage and feedback

## Best Practices from Documentation

1. **Start with Claude-generated configs**: Let this skill create the initial structure, then customize
2. **Use project agents for teams**: Store in `.claude/agents/` and commit to git
3. **Write detailed prompts**: Include specific instructions, examples, and constraints
4. **Default to full tool access**: Omit tools field to inherit all tools; only restrict when explicitly needed
5. **Consider model choice**: Use haiku for speed, opus for complexity, sonnet as default
6. **Test delegation**: Ensure the description triggers automatic invocation correctly
