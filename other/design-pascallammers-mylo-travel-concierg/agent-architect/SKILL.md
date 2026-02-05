---
name: agent-architect
description: Design, optimize, and refactor AI agent systems based on Anthropic best practices and latest research. Guides you through architectural decisions with interactive questionnaire, loads current documentation, and launches specialized agent-architect for detailed analysis.
---

# AI Agent Architecture Design Assistant

I'll help you design optimal agent systems based on Anthropic's best practices and latest research (CoS, LIFT-COT).

## Quick Start (For Experienced Users)

If you already know what you need, just provide your requirements directly:

**Example:**
> "I have 7 validators that check content against different constraints. They run sequentially and it's slow. How should I restructure this?"

I'll fetch the latest docs and launch the agent-architect immediately.

---

## Guided Mode (For Detailed Analysis)

If you prefer a structured approach, answer these questions:

## Step 1: Understanding Your Needs

Let me ask you a few questions to understand your requirements:

**1. What problem are you trying to solve?**
   - Describe the task/workflow you want to automate or optimize

**2. Is this about:**
   - [ ] Designing a new agent system from scratch
   - [ ] Optimizing existing agent architecture
   - [ ] Deciding between agent vs. skill
   - [ ] Fixing agent communication/performance issues
   - [ ] Other (please specify)

**3. Key Requirements (if known):**
   - Expected inputs and outputs?
   - Performance constraints (time, tokens, etc.)?
   - Error tolerance (high/low)?
   - Number of steps/complexity?

**4. Current Setup (if optimizing existing system):**
   - Brief description of current agent structure
   - What's not working well?
   - Performance bottlenecks?

---

Please answer these questions, and I'll:
1. Fetch the latest Anthropic documentation on agent design
2. Launch the specialized agent-architect with your requirements
3. Get you research-backed architectural recommendations

**Note:** If you already have a clear description, you can skip the questionnaire and provide it directly. I'll proceed with fetching documentation and launching the agent.

---

## Common Scenarios

Here are typical use cases where agent-architect can help:

### 🔧 Optimization
- "Our agents are hitting token limits from passing too much context"
- "Sequential workflow is slow, can we parallelize?"
- "Agent responses don't follow constraints consistently"

### 🏗️ Design
- "Should this be an agent or a skill?"
- "How to structure multi-agent content generation pipeline?"
- "What's the best way to validate outputs against multiple rules?"

### 🐛 Debugging
- "Agents keep losing information in handoffs"
- "Context window fills up too fast"
- "System doesn't handle failures gracefully"

### 📚 Learning
- "What are Anthropic's best practices for agent communication?"
- "How to implement human-in-the-loop approval?"
- "What does research say about multi-constraint tasks?"

---

## Quick Decision Framework (Reference)

While you think about your answers, here's a quick reference:

**Use Agent when:**
- Multiple constraints (>1) need balancing
- Domain knowledge required
- Multi-step reasoning needed
- Iterative refinement beneficial
- Low error tolerance

**Use Skill when:**
- Simple, repetitive task
- Single clear constraint
- High error tolerance
- Minimal context needed (<1000 tokens)
- Algorithmic, well-defined steps

**Ready?** Provide your answers above (or describe your problem directly), and I'll launch the full architectural analysis!

---

## Instructions for Claude (Internal)

When the user responds (either with direct problem description OR questionnaire answers):

### Step 0: Detect Mode
- **Quick Mode:** User provided direct problem description → Skip to Step 1
- **Guided Mode:** User is answering questionnaire → Ask follow-up questions if needed
- **Silent:** User is still reading → Wait for their input

### Step 1: Acknowledge and Summarize
Briefly summarize the user's requirements to confirm understanding.

If information is incomplete, ask 1-2 clarifying questions maximum.

### Step 2: Fetch Anthropic Documentation
Use WebFetch to load the latest documentation on agent design patterns:

1. **Agent Best Practices:**
   - URL: `https://docs.anthropic.com/en/docs/build-with-claude/agent-patterns`
   - Focus: Agent design patterns, decomposition, communication

2. **Multi-Agent Systems:**
   - URL: `https://docs.anthropic.com/en/docs/build-with-claude/multi-agent-systems`
   - Focus: Orchestration, parallelization, context management

3. **Prompt Engineering:**
   - URL: `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering`
   - Focus: Constraint handling, iterative refinement

### Step 3: Launch Agent-Architect
Use the Task tool with `subagent_type: agent-architect` and provide:

```
User Requirements:
[Summarized user input from questionnaire]

Relevant Anthropic Documentation:
[Key excerpts from fetched docs]

Task:
[Based on user's problem type: design new system / optimize existing / agent vs skill decision / fix issues]

IMPORTANT: Write your complete analysis to a file and return only the file path.

File path format: workspace/agent-architect-reports/{timestamp}-{brief-description}.md

Include in your report:
1. Executive Summary (2-3 sentences)
2. Recommended architecture with diagrams
3. Research justification (cite CoS, LIFT-COT principles)
4. Implementation guidance (step-by-step)
5. Potential issues and mitigations
6. Next steps

Return format:
{
  "report_path": "workspace/agent-architect-reports/...",
  "summary": "Brief 1-sentence summary",
  "key_recommendations": ["rec1", "rec2", "rec3"]
}
```

### Step 4: Save Report and Present Summary
When agent-architect returns:

1. **Read the report file** using the Read tool
2. **Present a brief summary** to the user:
   - Executive summary (from report)
   - Top 3 key recommendations
   - Critical decisions requiring attention

3. **Show file path**: "Full report saved to: `{path}`"

### Step 5: Human-in-the-Loop Validation
**CRITICAL: Always request user feedback before concluding.**

Ask the user:
```
Would you like to:
1. ✅ Approve - Accept recommendations as-is
2. 🔄 Refine - Request changes or deeper analysis
3. 🔍 Explore - Deep dive into specific aspects
4. 💾 Implement - Get help implementing the architecture

Please respond with the number or describe what you need.
```

**Handle user response:**

- **If approved (1):**
  - Confirm completion
  - Offer next steps (implementation guidance, documentation, etc.)

- **If refinement requested (2):**
  - Ask what needs to change
  - Re-launch agent-architect with:
    - Original requirements
    - Previous report path (for context)
    - Specific refinement requests
  - Save new report with `-v2`, `-v3` suffix
  - Return to Step 4

- **If exploration requested (3):**
  - Ask which aspect to explore
  - Launch agent-architect in focused mode on that aspect
  - Append findings to original report or create supplement

- **If implementation help (4):**
  - Offer to create implementation plan
  - Generate code scaffolding if applicable
  - Create step-by-step implementation guide

### Step 6: Iterative Refinement Loop
If user requests changes (option 2 or 3):

1. **Collect specific feedback:**
   - What needs to change?
   - What's missing?
   - What needs deeper analysis?

2. **Re-launch agent with context:**
   ```
   Previous analysis: {previous_report_path}

   User feedback: [specific requests]

   Please refine your analysis addressing the feedback.
   Save updated report to: {original_path with -v2/-v3 suffix}
   ```

3. **Compare versions:**
   - Show what changed
   - Highlight new insights
   - Return to Step 5 for validation

4. **Limit iterations:** Maximum 3 rounds. After that, suggest live discussion or breaking into sub-tasks.

### Step 7: Archive and Cleanup
Once approved:

1. **Create final report** (if multiple versions exist):
   - Consolidate best insights
   - Mark as "APPROVED" in filename
   - Example: `workspace/agent-architect-reports/{timestamp}-{description}-APPROVED.md`

2. **Offer next steps:**
   - Implementation guidance
   - Documentation generation
   - Code scaffolding
   - Follow-up analysis

---

## Example Usage Flow

**User:** `/agent-architect`

**Skill expands:** [Questionnaire appears]

**User:** "I need to validate generated content against 7 different constraints..."

**Claude:**
1. Summarizes requirements
2. Fetches Anthropic documentation
3. Launches agent-architect
4. Reads generated report
5. Presents summary with top 3 recommendations
6. Shows report path: `workspace/agent-architect-reports/2025-11-10-143022-parallel-validation.md`
7. **Asks:** "Would you like to: 1) Approve, 2) Refine, 3) Explore, 4) Implement?"

**User:** "2 - I need more details on error handling"

**Claude:**
1. Collects specific feedback
2. Re-launches agent with refinement request
3. Reads updated report (`-v2` version)
4. Shows what changed
5. **Asks again:** "Would you like to: 1) Approve, 2) Refine, 3) Explore, 4) Implement?"

**User:** "1 - Approve"

**Claude:**
1. Creates final approved report
2. Offers implementation help
3. Provides next steps
