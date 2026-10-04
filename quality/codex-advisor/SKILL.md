---
name: codex-advisor
description: Advisory consultation skill for architectural reviews, design decisions, code analysis, and technology evaluation. Codex provides recommendations without making code changes. Invoked by phrases like "consult Codex", "get Codex's opinion", "ask Codex about", "have Codex review", "Codex analysis", "validate this approach", "brainstorm with Codex", or "Codex consensus".
allowed-tools: Read, Grep, Glob, mcp__codex__codex, mcp__codex__codex-reply
---

# Codex Advisor

Use this skill to consult Codex as a senior engineering advisor through two specialized collaboration modes: **Chat**
for peer brainstorming and **Consensus** for structured evaluation. Invoke Codex strictly for advisory consultation—it
provides analysis and recommendations while Claude handles all code implementation.

## Collaboration Modes

**Chat Mode** — Peer brainstorming for exploring solutions, trade-offs, and validation. Use for iterative
problem-solving and technical discussions. See `references/chat-pattern.md` for detailed guidance.

**Consensus Mode** — Structured evaluation for major decisions. Provides 7-dimension assessment with verdict and
confidence scoring. Use for high-stakes architectural or technology decisions. See `references/consensus-pattern.md` for
detailed guidance.

## When to Use This Skill

Invoke Codex for advisory consultation on architecture, design decisions, code review, technology selection, and
strategic planning. Codex provides analysis and recommendations only—all code implementation uses Claude's tools
directly.

**Do not use for:** Simple questions, actual code writing, or file modifications.

## Collaboration Workflow

### Step 1: Load Project Context (Always Do This First)

Before consulting Codex, gather project-specific context to ensure recommendations align with established constraints:

**Required:**

1. Read `~/.claude/CLAUDE.md` for global project principles and constraints
2. Extract key information:
    - Core principles (e.g., "INVESTIGATE BEFORE CHANGING", "MINIMAL SURGICAL CHANGES")
    - Forbidden patterns or practices
    - Architecture constraints
    - Code style requirements
    - Security/quality standards

**Optional:**

- If project-specific `./AGENTS.md` exists in current directory, read it for additional context

**Usage:**

- Include extracted constraints in your prompt to Codex, OR
- Add them as context in the `developer-instructions` parameter

**Example context to include:**

```
Project constraints from CLAUDE.md:
- INVESTIGATE BEFORE CHANGING: debug systematically first
- MINIMAL SURGICAL CHANGES: change only what's requested
- FOLLOW EXISTING PATTERNS: match codebase conventions
- No placeholders or fallback implementations
```

**If CLAUDE.md is missing or unreadable:**

- Note this limitation to the user
- Proceed with consultation but warn recommendations may not align with project standards
- Ask user if they want to provide key constraints manually

### Step 2: Choose Mode and Load System Prompt

Determine which collaboration mode fits the user's request:

- **Chat Mode:** Brainstorming, trade-offs, validation, iterative discussion
- **Consensus Mode:** Formal evaluation, structured assessment, high-stakes decisions

#### For Chat Mode (Brainstorming):

**2a. Load system prompt:**

- Read the file `prompts/chat-mode-system-prompt.md`
- Use the complete contents as `developer-instructions` parameter

**2b. Invoke Codex:**
Use `mcp__codex__codex` tool with these parameters:

- `prompt`: Your question/problem (include context from Step 1 here)
- `developer-instructions`: Contents from step 2a
- `sandbox`: "read-only" (REQUIRED - prevents file modifications)
- `approval-policy`: "never" (safe for read-only consultations)
- `cwd`: Current project directory path (optional)

**Note:** Chat mode uses optimized GPT-5 prompt (~158 tokens). See `references/chat-pattern.md` for detailed usage
patterns.

#### For Consensus Mode (Evaluation):

**2a. Load system prompt template:**

- Read the file `prompts/consensus-mode-system-prompt.md`
- This file contains a `{stance_prompt}` placeholder that must be replaced

**2b. Select and apply stance:**

1. Choose stance based on evaluation needs (default: neutral):
    - **neutral**: Balanced, objective analysis
    - **skeptical**: Risk-focused scrutiny
    - **supportive**: Opportunity-focused
    - **security-focused**: Security-first lens
    - **performance-focused**: Performance-first lens
    - **pragmatic**: Resource-constrained practicality

2. Get stance text from `references/consensus-pattern.md` section "Stance Options"

3. Replace `{stance_prompt}` placeholder with chosen stance text

**2c. Invoke Codex:**
Use `mcp__codex__codex` tool with these parameters:

- `prompt`: Your proposal with context (include constraints from Step 1)
- `developer-instructions`: Modified template from step 2b
- `sandbox`: "read-only" (REQUIRED)
- `approval-policy`: "never"
- `cwd`: Current project directory path (optional)
- `model`: "gpt-5.2" (recommended for architecture/code evaluation)

**Note:** Consensus mode uses optimized GPT-5 prompt (~420 tokens). See `references/consensus-pattern.md` for detailed
evaluation framework.

### Step 3: Continue Collaboration (Optional)

For multi-turn consultation, use `mcp__codex__codex-reply`:

**3a. Store conversation ID:**

- Save the `conversationId` returned from initial `mcp__codex__codex` call

**3b. Invoke follow-up:**
Use `mcp__codex__codex-reply` tool with these parameters:

- `conversationId`: ID from step 3a
- `prompt`: Your follow-up question or clarification request

**Note:** No need to re-specify `developer-instructions`, `sandbox`, or other settings - they carry over from initial
call.

**When to follow up:**

- User asks for deeper exploration of Codex's recommendation
- You need clarification on specific points
- Alternative approaches should be discussed
- Implementation details need elaboration

### Step 4: Synthesize and Present

After receiving Codex's input:

1. Summarize key findings and recommendations
2. Present trade-offs and alternatives to user
3. Let user decide which approach to pursue
4. Implement the chosen solution using Claude's own tools

## Verification Checklist

Before presenting Codex's response to the user, verify you completed these steps correctly:

### Pre-Consultation Checks

- ✅ Read `~/.claude/CLAUDE.md` for project constraints
- ✅ Extracted key principles and included them in consultation context
- ✅ Loaded correct system prompt file for chosen mode
- ✅ For Consensus: selected stance and replaced `{stance_prompt}` placeholder

### Safety Checks

- ✅ Set `sandbox: "read-only"` (Codex must never modify files)
- ✅ Set `approval-policy: "never"` (safe for read-only advisory mode)
- ✅ Codex's role is ADVISORY ONLY - no file modifications requested

### Quality Checks

- ✅ Prompt includes sufficient context (scale, tech stack, constraints, timeline)
- ✅ Prompt is specific and focused (not vague like "should we use microservices?")
- ✅ For Consensus: proposal format with context and evaluation dimensions

**If any check fails:**

1. Identify which step was missed
2. Re-do the consultation with corrections
3. Do not present incomplete or incorrectly configured results

## Error Handling

### If CLAUDE.md is Missing or Unreadable

1. Note limitation to user: "CLAUDE.md not found - proceeding without project-specific constraints"
2. Ask user: "Would you like to provide key project constraints manually?"
3. Continue consultation with available context

### If System Prompt File Not Found

1. Report error to user: "System prompt file missing at [path]"
2. Suggest checking skill installation
3. Do not proceed with consultation

### If Codex Returns Error

1. Show full error message to user
2. Check if parameters were correct (especially stance replacement)
3. Suggest simpler prompt or different mode
4. Offer to retry with corrections

### If Stance Replacement Fails (Consensus Mode)

1. Fall back to neutral stance
2. Notify user: "Using neutral stance (default)"
3. Continue with consultation

## Quick Reference Examples

### Chat Mode — Architecture Brainstorming

**User request:** "Brainstorm with Codex about our caching strategy"

**Invocation:**

```
mcp__codex__codex(
  prompt: "We're experiencing slow dashboard load times (2-3 seconds) with 50K daily users. Current stack: Node.js + Express + PostgreSQL. Considering Redis for caching. What are the key trade-offs and potential pitfalls? What caching patterns work best for dashboards with user-specific data?",
  developer-instructions: "[Load from prompts/chat-mode-system-prompt.md]",
  sandbox: "read-only",
  approval-policy: "never"
)
```

### Consensus Mode — Technology Decision

**User request:** "Have Codex evaluate our GraphQL vs REST decision"

**Invocation:**

```
mcp__codex__codex(
  prompt: "Proposal: Migrate our REST API to GraphQL for the new mobile app.

Context:
- 10-person team, mostly backend experience with Node.js/Express
- 100K users, mobile and web clients
- Current API has 50+ REST endpoints
- Mobile team wants flexible data fetching
- Timeline: 6 months

Evaluate this proposal across technical feasibility, implementation complexity, and long-term implications.",
  developer-instructions: "[Load from prompts/consensus-mode-system-prompt.md, replace {stance_prompt} with neutral stance]",
  sandbox: "read-only",
  approval-policy: "never",
  model: "gpt-5.2"
)
```

**For comprehensive examples** covering refactoring discussions, security audits, performance optimization, network
research, multi-turn conversations, and various stances, see:

- **Chat Mode:** `references/chat-pattern.md` — Complete invocation examples with follow-up patterns
- **Consensus Mode:** `references/consensus-pattern.md` — Examples with different stances and evaluation scenarios

## Presenting Codex Collaboration to User

### Chat Mode Results

Structure as conversational synthesis:

```markdown
## Codex Discussion: [Topic]

**Key Insights:**

- [Insight with supporting reasoning]
- [Trade-off identified]
- [Pitfall or edge case surfaced]

**Recommendations:**
[Codex's suggested approach with rationale]

**Alternatives Discussed:**

- Option A: [Brief description with trade-offs]
- Option B: [Brief description with trade-offs]

**Next Steps:**
[2-3 actionable options for the user]

Would you like to explore any of these further, or shall I implement the recommended approach?
```

### Consensus Mode Results

Structure as formal evaluation:

```markdown
## Codex Consensus Evaluation: [Proposal]

**Verdict:**
[Single-sentence summary from consensus]

**Analysis Highlights:**

- **Technical Feasibility:** [Key finding]
- **Implementation Complexity:** [Key finding]
- **Long-term Implications:** [Key finding]

**Confidence:** [Score/10 with justification]

**Critical Takeaways:**

1. [Most important insight]
2. [Significant risk or consideration]
3. [Actionable recommendation]

**Recommendation:**
[Claude's synthesis of whether to proceed, modify, or reconsider]

What would you like to do?
```

### Common Anti-Patterns to Avoid

**Wrong mode choice** — Using Consensus for quick questions or Chat for formal reviews wastes effort. Match mode to
decision stakes.

**Vague requests without context** — Provide specific focus areas, constraints, and expected deliverable formats.
Include scale, tech stack, timeline, and team expertise.

**Implementation requests to Codex** — Request strategy and recommendations only. Codex advises in read-only mode;
Claude implements using its own tools.

**Missing project constraints** — Always read CLAUDE.md first and include extracted principles in consultation context
to ensure alignment.

**Simple questions** — Reserve Codex consultation for complex analysis requiring specialized expertise, not
straightforward lookups.

## Resources

### references/chat-pattern.md

Complete chat mode system prompt and usage guidelines for peer brainstorming:

- Interactive collaboration principles
- Practical problem-solving focus
- Edge case and trade-off exploration
- Example prompts for various scenarios

### references/consensus-pattern.md

Complete consensus mode system prompt and evaluation framework:

- 7-dimension assessment structure
- Verdict and confidence scoring format
- Stance configuration options
- Example proposals and evaluations

### references/mcp-parameters.md

Complete reference for Codex MCP tool parameters:

- Required vs optional parameters
- Advisory mode configuration (sandbox, approval-policy)
- Developer instructions formatting
- Model selection guidance

## Philosophy

**Two Modes, One Purpose: Advisory Excellence**

Chat and Consensus modes provide complementary collaboration styles while maintaining strict advisory boundaries:

- **Safety:** Read-only mode prevents unintended modifications in both modes
- **Control:** User reviews recommendations before implementation
- **Efficiency:** Claude uses optimal tools for code editing
- **Expertise:** Codex provides deep technical analysis through appropriate collaboration style
- **Flexibility:** Choose interaction mode based on decision complexity and stakes
