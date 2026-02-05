---
name: managing-subagents
description: Analyzes subagent usage patterns to determine when to delegate tasks, evaluates and improves existing subagent configurations, creates new custom subagents when needed, and identifies outdated subagent information. Use when deciding if a task should use a subagent, analyzing existing agents for effectiveness, recommending agent improvements, creating specialized agents for recurring patterns, or managing agent configurations. Optimizes Claude's subagent usage for performance, context preservation, and task specialization.
---

# Managing Subagents

Systematic approach for analyzing, evaluating, creating, and improving subagent configurations to maximize effectiveness.

## Core Concept

Subagents are specialized prompts with configuration (tools, model, permissions). When creating or optimizing subagent system prompts, consider using the **managing-prompts** skill for prompt engineering best practices, guardrails, and optimization techniques.

## When to Use This Skill

Use this skill when:
- **Deciding delegation**: Evaluating whether a task should use a subagent or direct tool calls
- **Evaluating agents**: Analyzing existing agent effectiveness and identifying improvements
- **Creating agents**: Building new agents for recurring task patterns or specialized workflows
- **Improving agents**: Optimizing agent configurations, descriptions, or system prompts
- **Explaining to users**: User asks how subagents work, when to use them, or requests examples
- **Managing configurations**: User requests agent creation, modification, or analysis via /agents command

If information about current Claude Code features or capabilities is unclear, ask the user to provide updated documentation or direct you where to look.

Load the appropriate workflow based on the task.

## Core Workflows

### Workflow 1: Analyzing Context for Subagent Delegation

When evaluating whether current context or logic should use a subagent:

#### Step 1: Load Decision Matrix
Use Read tool to load `decision-matrix.md` for detailed criteria.

#### Step 2: Apply Quick Assessment
Evaluate these factors:

**Delegation Score (0-10 points):**
- Context preservation need (+2): Main conversation context filling up with search results
- Task complexity (+2): Multi-step exploration requiring 5+ tool calls
- Parallel opportunity (+2): Multiple independent searches possible
- Focus requirement (+2): Task needs specialized system prompt or constraints
- Iteration depth (+2): Task requires retry loops or progressive refinement

**Score Interpretation:**
- 0-3: Use direct tool calls in main conversation
- 4-6: Consider subagent if user preference or specific constraints exist
- 7-10: Strong subagent candidate - use Task tool

#### Step 3: Select Agent Type
Match task to appropriate built-in agent:

- **Explore agent**: Codebase exploration, finding files by patterns, searching keywords, answering "how does X work" questions about code. Use thoroughness levels: "quick" (basic search), "medium" (moderate exploration), "very thorough" (comprehensive multi-location analysis).
- **Plan agent**: Automatic activation during plan mode for research. Not manually invoked.
- **general-purpose agent**: Complex multi-step tasks requiring autonomy, repeated searches with uncertain outcomes, tasks requiring multiple tool types.

#### Step 4: Determine Custom Agent Need
If built-in agents don't match requirements:
- Check user's `.claude/agents/` and project `.claude/agents/` directories using Glob tool with pattern `**/*.md`
- Use Grep tool to search agent descriptions for relevant keywords
- If no match found, recommend creating custom agent (proceed to Workflow 5)

#### Step 5: Formulate Task Prompt
Construct clear, autonomous task prompt:
- Specify exact information to return in final report
- Include all necessary context (agents cannot see future messages)
- State expected output format explicitly
- Clarify whether agent should write code or only research

### Workflow 2: Explaining Subagent Concepts to Users

When user asks how subagents work, what they are, when to use them, or requests general understanding:

#### Step 1: Determine Question Type

**"What are subagents?"** → Explain core concept:
- Pre-configured AI assistants with dedicated responsibilities
- Operate in separate context windows (prevents main conversation pollution)
- Custom system prompts enable specialized behavior
- Configurable tool access matched to domain
- Invoked via Task tool, return isolated results to main conversation

**"Why use subagents instead of direct tools?"** → Explain benefits:
- Context preservation: Main conversation not filled with search results
- Parallelization: Multiple subagents run simultaneously on independent tasks
- Specialization: Domain-specific prompts achieve higher success rates
- Reusability: Consistent workflows across projects, shareable with teams
- Permission boundaries: Tool restrictions enable security controls

**"When should I use subagents?"** → Reference decision framework:
- Load decision-matrix.md scoring criteria (0-10 points across 5 dimensions)
- Score 0-3: Use direct tool calls
- Score 4-6: Conditional (evaluate context factors)
- Score 7-10: Strong subagent candidate
- Provide concrete example: "Finding all API endpoints scores 8/10 (context+2, complexity+2, parallelization+2, focus+1, iteration+2) → use Explore agent with 'very thorough'"

**"How do I create a subagent?"** → Point to Workflow 6:
- File location: `.claude/agents/` (project) or `~/.claude/agents/` (user)
- Required fields: name, description
- Optional fields: tools, model
- System prompt follows YAML frontmatter
- Refer to Workflow 6 for complete creation process

**"What built-in agents exist?"** → List agent types:
- Explore agent: Codebase search, file pattern matching, "how does X work" questions (thoroughness levels: quick/medium/very thorough)
- Plan agent: Automatic in plan mode, not manually invoked
- general-purpose agent: Complex multi-step tasks, autonomous workflows

#### Step 2: Provide Concrete Example

Always include scored example from decision-matrix.md to demonstrate delegation decision process. Use examples from lines 244-277 based on complexity:
- Simple task example: "Read config.json" scores 0 → direct Read tool
- Complex task example: "Find all API endpoints" scores 8 → Explore agent

#### Step 3: Offer Further Assistance

Based on user response:
- If wants to evaluate specific task → Proceed to Workflow 1
- If wants to create custom agent → Proceed to Workflow 6
- If wants to analyze existing agent → Proceed to Workflow 3
- If wants specific documentation → Load appropriate supporting file (configuration-reference.md, example-subagents.md, agents-command-guide.md). If information unavailable, ask user to provide updated documentation.

### Workflow 3: Evaluating Existing Subagent Configurations

When analyzing whether an existing subagent is effective or needs improvement:

#### Step 1: Locate Agent File

**If user provided explicit path** (e.g., "analyze ~/.claude/agents/security-auditor.md"):
- Use Read tool directly on provided path
- Skip search steps

**If user provided agent name only** (e.g., "analyze the security-auditor agent"):
- Use Glob tool to search: `~/.claude/agents/**/{name}.md` and `.claude/agents/**/{name}.md`
- If multiple matches found, list all and ask user which one
- Use Read tool to load selected agent

**If user said "the agent" referencing previous context:**
- Resolve agent name/path from conversation history
- Use Read tool on resolved path

**For all cases:**
- Use Read tool to load complete agent configuration
- If file not found, report specific path attempted and suggest using Glob with pattern `**/*.md` to list available agents

#### Step 2: Load Analysis Framework
Use Read tool to load `analysis-framework.md` for systematic evaluation criteria.

#### Step 3: Parse Configuration
Extract and evaluate:
- `name`: Format validation (lowercase-with-hyphens, descriptive)
- `description`: Specificity, trigger keywords, clarity
- `tools`: Appropriateness of tool restrictions
- `model`: Model selection rationale
- System prompt: Instructions clarity, specificity, examples

#### Step 4: Assess Effectiveness Indicators
Evaluate against these patterns:

**Strong Agent Indicators:**
- Description contains 5+ specific trigger keywords
- System prompt includes concrete examples
- Tool restrictions match agent purpose
- Clear input/output specifications
- Single focused responsibility

**Weak Agent Indicators:**
- Vague description ("helps with various tasks")
- Generic system prompt without examples
- Unnecessary tool restrictions or overly broad tool access
- Multiple unrelated responsibilities
- Missing output format specifications

#### Step 5: Identify Issues
Categorize findings:
- **Critical**: Agent fails to activate when needed, incorrect tool access blocks functionality
- **Major**: Unclear description prevents discovery, system prompt lacks necessary context
- **Minor**: Could be more specific, missing helpful examples

#### Step 6: Generate Recommendations
Provide specific improvements with rationale focused on Claude's execution efficiency.

### Workflow 4: Identifying Outdated Agent Configurations

When analyzing whether an agent's configuration contains obsolete information:

#### Step 1: Load Agent Configuration
Use Read tool to load agent file.

#### Step 2: Extract Time-Sensitive Content
Identify references in agent's system prompt and configuration to:
- Claude Code features (tools, commands, behaviors)
- Tool names or parameters
- API structures or endpoints
- File paths or directory structures
- Model capabilities or behaviors
- Best practices or patterns

#### Step 3: Verify Current State
For each time-sensitive reference:
- Compare against supporting files in this skill (configuration-reference.md, example-subagents.md)
- Use Grep tool to search current codebase for API patterns or tool usage
- If information unavailable or unclear, ask user to provide updated documentation or direct where to look

#### Step 4: Document Discrepancies
List each outdated element:
- What agent configuration says: [current text]
- Current reality: [verified state]
- Impact: [how this affects agent effectiveness]
- Recommended update: [specific change]

#### Step 5: Prioritize Updates
Rank by impact on agent functionality:
1. **Critical**: Blocks agent execution (tool names changed, permissions invalid)
2. **Major**: Produces incorrect results (API structure changed, wrong tool usage)
3. **Minor**: Uses deprecated patterns (better approach exists but functional)
4. **Informational**: Suboptimal but functional (minor efficiency loss)

### Workflow 5: Recommending Subagent Improvements

When generating improvement recommendations for existing agents:

#### Step 1: Load Improvement Patterns
Use Read tool to load `improvement-patterns.md` for common optimization patterns.

#### Step 2: Apply Improvement Framework

**Description Optimization:**
- Add specific trigger keywords user would naturally use
- Include data types, file formats, task types
- Remove vague language ("various", "helps with", "handles")
- Ensure discoverability among 100+ potential agents

**System Prompt Enhancement:**
- Add concrete examples of expected inputs/outputs
- Specify exact information to include in final report
- Include error handling guidance
- Remove redundant information Claude already knows
- Add constraints or validation steps if needed

**Tool Configuration:**
- Restrict to minimum necessary tools (improves focus)
- Ensure MCP tools inherited if needed
- Verify no essential tools blocked

**Model Selection:**
- Use `haiku` for simple, fast tasks (cost/latency optimization)
- Use `sonnet` for complex reasoning or code generation
- Use `opus` only if maximum capability essential
- Use `inherit` for consistency with main conversation

#### Step 3: Structure Recommendations
For each improvement:
```
Category: [Description/SystemPrompt/Tools/Model]
Priority: [Critical/Major/Minor]
Current: [existing state]
Recommended: [specific change]
Rationale: [why this improves Claude's effectiveness]
Implementation: [exact steps to apply]
```

#### Step 4: Validate Improvements
Before finalizing recommendations:
- Ensure changes maintain backward compatibility
- Verify improved version more discoverable
- Confirm system prompt provides sufficient context
- Check tool restrictions don't block necessary operations

### Workflow 6: Deciding When to Create New Subagents

When evaluating whether to recommend new subagent creation:

#### Step 1: Apply Creation Criteria
Evaluate each criterion (need 4+ for strong recommendation):

- [ ] Task pattern repeats across multiple user conversations
- [ ] Task requires specialized system prompt or behavior modification
- [ ] Task benefits from isolated context (prevents main conversation pollution)
- [ ] Task enables useful parallelization (multiple instances simultaneously)
- [ ] Task requires specific tool access restrictions
- [ ] Task has clear completion criteria and expected output format
- [ ] Task domain-specific enough to benefit from focused instructions

**Decision Rule:**
- 0-3 criteria: Use direct tool calls or existing general-purpose agent
- 4-5 criteria: Consider custom agent, recommend if user has recurring need
- 6-7 criteria: Strong custom agent candidate, recommend creation

#### Step 2: Design Agent Specification
If custom agent recommended, specify:

**Required fields:**
```yaml
name: descriptive-action-name
description: Specific purpose with 5+ trigger keywords, data types, task types, clear activation contexts
```

**Optional fields:**
```yaml
tools: minimal-necessary-set  # Only if restrictions needed
model: haiku|sonnet|opus|inherit  # Default to inherit
```

**System prompt structure:**
```
[Purpose statement - what agent does]

[Activation contexts - when to use]

[Input specifications - what agent receives]

[Processing instructions - step-by-step workflow]

[Output specifications - exact format to return]

[Examples - concrete input/output pairs]

[Constraints - validation, error handling]
```

#### Step 3: Recommend Implementation
Provide complete agent file content with:
- Optimized description for discoverability
- Focused system prompt without redundancy
- Appropriate tool restrictions
- Model selection rationale
- Location recommendation (user vs project agent)

#### Step 4: Create Agent File

**Location selection:**
- User agents: `~/.claude/agents/` - Personal, experimental, individual workflows
- Project agents: `.claude/agents/` - Team-shared, committed to git, standardized workflows

**Implementation steps:**
1. Determine file path: `{location}/{name}.md` (where name from Step 2)
2. Use Write tool to create agent file with complete content:
   - YAML frontmatter with `---` delimiters
   - Required fields: name, description
   - Optional fields: tools (if restrictions needed), model (if non-default)
   - System prompt following YAML frontmatter
3. Use Read tool to verify file created successfully
4. Confirm YAML syntax valid (no tabs, proper delimiters, all fields present)

**Template structure:**
```
---
name: agent-name-here
description: Specific description with 5+ trigger keywords
tools: Tool1, Tool2  # Optional - omit to inherit all tools including MCP
model: haiku|sonnet|opus|inherit  # Optional - defaults to configured subagent model
---

[System prompt content following structure from Step 2]
```

**Verification checklist:**
- [ ] File created at correct location
- [ ] YAML delimiters present (---)
- [ ] Name and description fields populated
- [ ] No tabs in YAML (spaces only)
- [ ] System prompt follows frontmatter
- [ ] File readable via Read tool

### Workflow 7: Managing Subagents via /agents Command

When managing custom subagents interactively:

#### Step 1: Open /agents Interface
```
/agents
```

Interactive menu displays all available subagents:
- Built-in agents (Explore, Plan, general-purpose)
- Project custom agents (.claude/agents/)
- User custom agents (~/.claude/agents/)
- Plugin agents (from installed plugins - see **managing-plugins** skill for plugin system details)

**Plugin Agents**: When names conflict, priority is: project agents > plugin agents > user agents. Load plugin-agents.md for integration patterns.

#### Step 2: Available Operations

**View all agents**: See complete list with descriptions and tool access

**Create new agent**: Guided setup with:
- Name, description with trigger keywords
- Visual tool selector (check/uncheck from complete list)
- Model selection (haiku/sonnet/opus/inherit)
- System prompt entry
- Location selection (project vs user)

**Edit existing agent**: Modify custom agents' configuration
- Update description, tools, model, system prompt
- Changes take effect immediately

**Delete custom agent**: Remove agents (built-in agents read-only)

**Inspect agent**: View complete configuration for any agent

**Load agents-command-guide.md for detailed workflows and tool management.**

### Workflow 8: Understanding Configuration Fields

Complete reference for all YAML configuration options:

**Required**:
- `name`: lowercase-with-hyphens identifier, under 64 chars (e.g., "security-auditor", "api-explorer")
- `description`: 5+ trigger keywords, specify when to activate, data types/formats, under 1024 chars

**Optional**:
- `tools`: Comma-separated list of specific tools (omit to inherit all tools including MCP tools). Use to restrict tool access for security or focus. Example: `Read, Glob, Grep, Bash`
- `model`: haiku|sonnet|opus|inherit (default: system configured model, typically sonnet)
  - **'haiku'**: Simple/fast tasks, cost optimization
  - **'sonnet'**: Complex reasoning, code analysis (most common)
  - **'opus'**: Maximum capability (rare, expensive)
  - **'inherit'**: Use main conversation's model for consistency. Best when agent's purpose aligns with main task.
- `permissionMode`: default|acceptEdits|bypassPermissions|plan|ignore. Controls permission handling.
  - **'default'**: Agent asks for permission (safest, start here)
  - **'acceptEdits'**: Auto-accepts file edits (trusted refactoring agents)
  - **'bypassPermissions'**: Bypasses all permissions (only for fully trusted workflows)
  - **'plan'**: Operates in plan mode (returns plan without execution)
  - **'ignore'**: Ignores specific permission requests
- `skills`: Comma-separated skill names to pre-load when agent starts (reduces token usage, provides specialized domain knowledge). Example: `data-processor, statistical-analysis`

**CLI-Based Configuration**: For session-specific or testing scenarios, agents can be defined dynamically via `--agents` CLI flag in JSON format. Priority: CLI agents rank between project agents (highest) and user agents (lowest).

**Load configuration-reference.md for complete field documentation with detailed examples.**

**Load permission-modes.md for permission mode decision criteria and use cases.**

**Load cli-configuration.md for CLI flag usage, JSON format, and automation patterns.**

### Workflow 9: Using Resumable Subagents

When a task benefits from continuing previous subagent work across multiple invocations:

#### Step 1: Understand Resumable Capability

Subagents can be resumed to continue previous conversations with full context:
- Each subagent execution receives unique `agentId`
- Agent transcript stored in `agent-{agentId}.jsonl`
- Resume by passing `agentId` via `resume` parameter in Task tool
- Full context from previous conversation preserved
- Recording disabled during resume to avoid duplicating messages
- Both synchronous and asynchronous agents can be resumed

#### Step 2: Identify Resume Opportunities

**Use resumable agents when**:
- Long-running research needs to be split across multiple sessions
- Iterative refinement (continuing to improve previous analysis)
- Multi-step workflows on related tasks where context should carry over
- Previous agent work provides valuable foundation for next step

**Example scenarios**:
- "Start analyzing authentication module" → later → "Resume agent abc123 and analyze authorization"
- "Explore API endpoints" → later → "Resume agent abc123 and check error handling patterns"
- "Debug issue X" → later → "Resume agent abc123 and verify fix doesn't break Y"
- "Review security of auth system" → later → "Resume agent abc123 for session management review"

#### Step 3: Track Agent IDs During Invocation

When delegating to subagent, note the `agentId` returned in completion message:
```
User: "Use the code-analyzer agent to review authentication module"

Claude: [Invokes Task tool with subagent_type=code-analyzer]
[Agent completes work and returns]
[Agent ID visible in response: "abc123"]
```

Keep track of agent IDs for tasks that may need continuation later.

#### Step 4: Resume Agent with Full Context

To continue previous agent's work, use `resume` parameter:

**User invocation**:
```
User: "Resume agent abc123 and now analyze the authorization logic as well"
```

**Task tool usage**:
```json
{
  "description": "Continue security analysis",
  "prompt": "Now analyze authorization logic and session management patterns",
  "subagent_type": "code-analyzer",
  "resume": "abc123"
}
```

Agent receives full conversation history from previous execution and continues seamlessly.

#### Step 5: Best Practices for Resumable Agents

**When to resume**:
- Context from previous agent run is directly relevant
- Task is natural continuation of previous work
- Avoiding context duplication is valuable
- Iterative refinement benefits from accumulated knowledge

**When NOT to resume**:
- Completely independent task (fresh context better)
- Previous agent had errors or wrong approach (start clean)
- Context may confuse new task direction
- Agent ID lost or transcript unavailable

**Management tips**:
- Track agent IDs when suspending long-running analysis
- Agent transcripts stored in project directory
- Clean up old agent transcripts periodically
- Document agent ID in notes if work will span multiple sessions

## Progressive Disclosure References

For detailed guidance, load these files only when needed:

**Decision Making**:
- **decision-matrix.md**: Scoring rubric for when to use subagents (0-10 points) vs direct tool calls, with practical examples
- **analysis-framework.md**: Systematic evaluation of existing agents for effectiveness, identifying issues by severity

**Creating & Managing Agents**:
- **example-subagents.md**: Reference implementations - code-reviewer, debugger, data-scientist (complete YAML to adapt)
- **agents-command-guide.md**: Using /agents interface to create and manage agents interactively
- **configuration-reference.md**: Complete field documentation for creating agents (name, description, tools, model, permissionMode, skills)

**Optimization & Design**:
- **improvement-patterns.md**: 17 optimization patterns for descriptions, system prompts, tool configs, and model selection
- **permission-modes.md**: 5 permission modes with decision criteria (default, acceptEdits, bypassPermissions, plan, ignore)
- **multi-agent-patterns.md**: Parallel and sequential orchestration patterns

**Advanced Configuration**:
- **cli-configuration.md**: Dynamic agent definition via --agents CLI flag for session-specific or test agents
- **plugin-agents.md**: How plugin agents work, discovery, handling conflicts with custom agents

## Key Principles

1. **Context Preservation**: Subagents preserve main conversation context by isolating search results and exploration
2. **Parallelization**: Multiple subagents can run simultaneously for independent tasks
3. **Specialization**: Custom system prompts enable focused behavior not achievable with direct tool calls
4. **Autonomy**: Subagents operate independently - provide complete context in task prompt
5. **Efficiency**: Choose appropriate model (haiku/sonnet/opus) based on task complexity
6. **Discoverability**: Agent descriptions must enable activation among many potential agents

## Tool Usage Patterns

**When analyzing existing agents:**
1. Use Read tool to load agent configuration file
2. Use Glob tool with pattern `**/*.md` to find agent files in directories
3. Use Grep tool to search agent descriptions for keywords
4. Load analysis-framework.md from managing-agent-skills skill for systematic evaluation (if needed)

**When creating agents:**
1. Use Write tool to create agent file at appropriate location (.claude/agents/ or ~/.claude/agents/)
2. Use Read tool to verify file created successfully
3. Verify YAML frontmatter syntax (no tabs, proper delimiters, all required fields)
4. Load example-subagents.md for reference implementations

**When verifying agent configuration:**
1. Use Read tool to examine agent YAML frontmatter
2. Check required fields (name, description) present and properly formatted
3. Verify optional fields (tools, model, permissionMode, skills) correct if specified
4. Confirm agent file in correct location for intended scope (project vs user)

**When researching agent capabilities:**
1. Load appropriate supporting file first (configuration-reference.md, improvement-patterns.md, example-subagents.md)
2. Use decision-matrix.md for delegation scoring
3. Use analysis-framework.md for systematic evaluation
4. If information unclear or missing, ask user to provide updated documentation

## Best Practices for Creating & Improving Agents

**Use as reference**: When creating agents, load example-subagents.md for production-ready implementations (code-reviewer, debugger, data-scientist) to adapt.

**Apply improvement patterns**: When optimizing agents, use improvement-patterns.md for 17 common enhancements (descriptions, prompts, tools, models).

**Systematic evaluation**: Use analysis-framework.md to evaluate existing agents before recommending changes.

**Clear descriptions**: Agent descriptions need 5+ specific trigger keywords so I can identify when to use them. Include data types, formats, and concrete use cases.

**Single focused responsibility**: Each agent handles one domain - don't create multi-purpose agents that try to do everything.

**Appropriate tool access**: Restrict tools to what's necessary for security and focus. Omit tools field to inherit all + MCP tools when flexibility needed.

**Explicit output format**: Specify exact structure so agent returns usable results for further processing.

**Documentation**: When I create agents, include clear rationale for why the agent exists and when it should activate.

**Iteration cycle**: Create → Test → Analyze → Improve using the workflows in this skill.

## Anti-Patterns to Avoid

**When NOT to use subagents:**
- Single tool call suffices (use direct tool call)
- Task requires interactive back-and-forth (agents can't ask followup questions)
- Main conversation context not at risk of overflow
- Score 0-3 on decision matrix (direct calls better)

**Agent design anti-patterns:**
- Vague descriptions without specific triggers ("helps with various tasks")
- System prompts duplicating Claude's base knowledge
- Overly broad agents with multiple unrelated capabilities
- Unnecessary tool restrictions that block valid operations
- Missing output format specifications
- Generic names like "helper-agent" or "utility-agent"
- Not including concrete examples in system prompt
- permissionMode set to bypassPermissions for untrusted agents

## Quick Decision Framework

Use this for rapid subagent delegation decisions:

**Use Explore agent when:**
- Searching codebase for patterns or keywords
- Finding files by glob patterns
- Answering "how does X work" about code
- Context filling with search results

**Use general-purpose agent when:**
- Multi-step task requiring 5+ tool calls
- Uncertain number of search iterations needed
- Complex autonomous workflow
- Multiple tool types needed

**Use direct tool calls when:**
- 1-3 simple tool calls needed
- Interactive refinement required
- No context preservation benefit
- No specialized prompt needed

**Create custom agent when:**
- 4+ creation criteria met (Workflow 6)
- Recurring specialized task pattern
- Specific tool restrictions beneficial
- Domain-specific system prompt adds value

**Chain multiple agents when:**
- Task naturally splits into sequential steps
- One agent's output becomes next agent's input
- Example: "Use analyzer agent to find issues, then use fixer agent to resolve them"
- Load multi-agent-patterns.md for detailed sequential and parallel orchestration patterns

## Related Skills

- **managing-prompts**: Use for optimizing subagent system prompts, applying prompt engineering best practices, guardrails, and context management
- **managing-plugins**: Use when working with plugin-provided agents or bundling custom agents into plugins for distribution
- **managing-agent-skills**: Use for analyzing and improving this skill or understanding skill authoring patterns

## Output Format

When completing subagent analysis tasks:

1. **Assessment**: Delegation score or effectiveness evaluation
2. **Recommendation**: Specific action to take (use agent X, improve description, create new agent)
3. **Rationale**: Why recommendation optimizes Claude's effectiveness
4. **Implementation**: Exact steps or content if creating/modifying agents
5. **Trade-offs**: Performance, cost, or latency considerations
