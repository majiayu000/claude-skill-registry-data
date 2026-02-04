---
name: delegation-advisor
description: Recommend who should do a task (Claude Code, Gemini, ChatGPT, Human, Taskmaster, MCPs) and generate handoff prompts.
triggers:
  - who should do this
  - delegate
  - assign tasks
  - what can AI do
  - מי יכול לעשות את זה
---

# Delegation Advisor Skill

Analyze tasks and recommend optimal delegation - whether to human, AI agent, or external tool. Generate appropriate prompts for AI delegation.

## Purpose

This skill helps determine the best assignee for each task based on the task's requirements and each agent's strengths. It also generates handoff prompts tailored to the selected agent.

## Agent Profiles

### 1. Claude Code

**Strengths:**
- Building software/tools
- Coding and debugging
- System architecture
- Deployment and DevOps
- File system operations
- MCP integrations

**Best For:** Implementation tasks, technical building, automation

**Prompt Style:** Detailed specs, clear acceptance criteria, technical requirements

**Example Tasks:**
- Build a Python script
- Create a web application
- Debug code issues
- Set up CI/CD pipeline

---

### 2. Gemini

**Strengths:**
- Deep research
- Multi-document analysis
- Long context processing
- Comparative analysis
- PDF and document understanding

**Best For:** Research tasks, document analysis, literature review

**Prompt Style:** Clear research questions, source guidance, expected output format

**Example Tasks:**
- Research existing frameworks
- Analyze competitor approaches
- Summarize multiple papers
- Compare policy documents

---

### 3. ChatGPT

**Strengths:**
- Creative writing
- Drafting and editing
- Brainstorming
- Conversational interfaces
- Content generation

**Best For:** Content creation, ideation, copywriting

**Prompt Style:** Creative briefs, tone guidance, audience context

**Example Tasks:**
- Draft marketing copy
- Write blog posts
- Brainstorm feature ideas
- Edit and refine text

---

### 4. Human (Omer)

**Strengths:**
- Strategic decisions
- Stakeholder communication
- Quality judgment
- Domain expertise application
- Final approvals

**Best For:** Decisions, reviews, external communication, sign-offs

**Requires:** Clear options and recommendations, decision criteria

**Example Tasks:**
- Approve project direction
- Review deliverables
- Communicate with stakeholders
- Make strategic choices

---

### 5. Taskmaster (MCP)

**Strengths:**
- Task tracking
- Dependency management
- Progress monitoring
- Status updates

**Best For:** Task CRUD operations, status updates, project tracking

**Integration:** Direct MCP calls

**Example Tasks:**
- Update task status
- Expand task into subtasks
- Get next task to work on
- Track project progress

---

### 6. Other MCPs

| MCP | Best For | Example Use |
|-----|----------|-------------|
| **Monday** | Project boards, team collaboration | Sync tasks to team board |
| **Google Drive** | Document storage, sharing | Save deliverables, share with stakeholders |
| **Gmail** | Email communication | Send updates, schedule meetings |
| **Calendar** | Scheduling | Book meetings, set reminders |

## Workflow

### Step 1: Analyze Task Requirements

Assess the task across these factors:

| Factor | Questions |
|--------|-----------|
| Technical complexity | Does it require coding? System design? |
| Creative requirements | Does it need writing? Ideation? |
| Decision authority | Does it need human judgment? |
| External communication | Does it involve stakeholders? |
| Time sensitivity | Is there urgency? |
| Context requirements | How much background is needed? |

### Step 2: Match to Best Agent

Apply matching logic:

```
IF technical_building OR coding:
    → Claude Code (confidence: high)
    
ELIF deep_research OR multi_doc_analysis:
    → Gemini (confidence: high)
    
ELIF creative_writing OR brainstorming:
    → ChatGPT (confidence: medium)
    
ELIF strategic_decision OR stakeholder_communication:
    → Human (Omer) (confidence: high)
    
ELIF task_tracking OR status_update:
    → Taskmaster MCP (confidence: high)
    
ELSE:
    → Present options to human (confidence: low)
```

**Output:**
- `assignee`: Selected agent name
- `confidence`: high | medium | low
- `reasoning`: Why this agent is best suited

### Step 3: Generate Handoff Prompt

For AI agents, generate a structured handoff prompt:

```markdown
## Task Handoff: {task_name}

### Context
{project_context_summary}

### Objective
{clear_task_description}

### Requirements
- {requirement_1}
- {requirement_2}

### Acceptance Criteria
- {criterion_1}
- {criterion_2}

### Constraints
- {constraint_1}

### Output Format
{expected_deliverable_format}
```

### Step 4: Checkpoint

**CHECKPOINT:** Present recommendation to user

Ask:
- "Approve this delegation?"
- "Want to modify the assignee?"
- "Any changes to the handoff prompt?"

### Step 5: Update

- Update task assignee in `{project}_tasks.md`
- Provide handoff prompt if AI agent selected

## Example Interaction

**User Request:**
> "מי יכול לעשות את המחקר על frameworks קיימים?"

**Analysis:**
- Task type: Research
- Requirements: Multi-document analysis, comparative study
- No coding required
- No stakeholder communication

**Recommendation:**
> **Recommended Assignee:** Gemini
> **Confidence:** High
> **Reasoning:** This is a research task requiring analysis of multiple documents and comparison. Gemini excels at deep research and long-context processing.

**Generated Prompt for Gemini:**
```markdown
## Task Handoff: Research Existing AI Frameworks

### Context
Working on an AI Strategy project for the Law Faculty. Need to understand the landscape of existing frameworks before proposing our approach.

### Objective
Research and analyze existing AI governance/strategy frameworks used in academic institutions, particularly law schools.

### Requirements
- Find at least 5 relevant frameworks
- Focus on academic/educational contexts
- Include both governance and implementation aspects

### Acceptance Criteria
- Summary of each framework (1-2 paragraphs)
- Comparison table with key features
- Recommendations on which elements to adopt

### Output Format
Markdown document with sections for each framework, comparison table, and recommendations
```

## Cross-Interface Notes

- **Claude AI**: Presents recommendations, user copies prompt manually
- **Claude Code**: Can directly invoke other agents with prompt
- Both use same agent profiles and matching logic

