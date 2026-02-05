---
name: guided-ooda-loop
description: Universal pattern for structured LLM interaction managing finite context windows through phased progression (Observe-Orient-Decide-Act). Use when the user has a complex problem, wants to design/build/create something (software, strategy, document, process), or uses phrases like "I have an idea for...", "help me design...", "guide me through...", or mentions OODA, RPI, or PDD. Reduces hallucinations through structured interaction.
---

# Guided OODA Loop

## Overview

The Guided OODA Loop is a universal pattern for structured interaction with LLMs that addresses the fundamental constraint of finite context windows. By guiding users through four distinct phases—Observe, Orient, Decide, and Act—this skill enables effective problem-solving across any domain while optimizing for context convergence and minimizing hallucinations.

**Primary Value:**
- Manages context window limitations through phased progression
- Reduces confusion and hallucinations via structured interaction
- Creates durable artifacts that capture progress at each phase
- Applicable to ANY domain: software, strategy, writing, research, etc.

**The ACT phase produces execution-ready implementation plans** with detailed checklists and step-by-step actions based on the prior three phases (Observe-Orient-Decide).

## When to Use This Skill

Activate this skill when users express any of these patterns:

**Direct Triggers:**
- "I have an idea for..."
- "Help me design/build/create..."
- "I need to develop..."
- "Guide me through building..."
- "Walk through my thinking..."
- "Help me structure my approach to..."
- "Let's plan out how to..."
- Explicit mention of: OODA, RPI, PDD, Observe-Orient-Decide-Act, Research-Plan-Implement, Prompt-Driven Development

**Do NOT Trigger For:**
- Simple questions ("What is X?")
- Quick fixes ("Fix this bug")
- Pure information lookup
- Already-detailed specifications where planning is complete

## Core OODA Principles

The OODA Loop (Observe-Orient-Decide-Act) originated from military strategist John Boyd's framework for rapid, adaptive decision-making. When applied to LLM interaction, it becomes a powerful pattern for managing context and maintaining coherence.

### The Four Phases

**1. Observe (Research)**
- Gather raw data from the environment
- Understand relevant context, codebase, goals
- Collect information without judgment
- Document findings in structured format

**2. Orient (Analysis & Sense-Making)**
- Filter and analyze observations
- Make sense of collected data
- Identify patterns and relationships
- Refine understanding through Q&A

**3. Decide (Planning)**
- Select course of action based on analysis
- Create structured plan with small steps
- Design high-level approach
- Define checkpoints and deliverables

**4. Act (Execution-Ready Planning)**
- Create execution-ready implementation plan
- Generate detailed design specifications
- Build actionable checklists with clear steps
- Produce artifacts ready for immediate execution

### Context Window Convergence

The OODA pattern optimizes for **context convergence** by:

1. **Phased Loading:** Only load relevant information for current phase
2. **Artifact Creation:** Capture decisions in files, reducing need to hold in memory
3. **Checkpoint System:** `summary.md` tracks progress and status
4. **Structured Interaction:** Prevents wandering conversations that bloat context
5. **Progressive Refinement:** Each phase builds on previous, allowing focused context

### Context Monitoring

**Check context usage at each phase transition:**
- If context usage exceeds 60%, warn the user
- Recommend starting a new context window for optimal results
- Provide clear instructions for resuming with artifacts

**Warning Template:**
```
⚠️ CONTEXT USAGE WARNING: Current context at [X]% (>[threshold]%)

For optimal results, consider starting a new context window.

To resume in new window:
1. Read summary.md to understand current state
2. Load relevant artifacts for current phase
3. Continue from [current phase]
```

## Directory Structure

When the OODA loop activates, create this structure:

```
ooda-loop-{unique-name}-{DDMMMYY.HHMMSS}/
├── rough-idea.md              # Initial concept (extracted from context)
├── observe/
│   ├── research.md            # Domain-specific research findings
│   └── idea-honing.md         # Q&A requirements clarification (OO checkpoint)
├── decide/
│   ├── to-do.md               # Focused guide for OODA loop
│   └── high-level-design.md   # Thinking guide, drives virtuous cycle
├── act/                       # Planning artifacts (NOT execution)
│   ├── implementation-plan.md # Must include implementation checklist
│   └── detailed-design.md     # Complete design specification
└── summary.md                 # Succinct highlights with YAML frontmatter status
```

### Naming Convention

- `{unique-name}`: Descriptive identifier for the problem/project (e.g., "user-template-feature", "strategy-analysis", "content-workflow")
- `{DDMMMYY.HHMMSS}`: Timestamp (e.g., "03JAN26.150045")
- Example: `ooda-loop-user-auth-redesign-03JAN26.150045/`

### Key Files

**summary.md Format:**
```yaml
---
status: in-progress  # or 'complete'
phase: observe       # current phase: observe, orient, decide, act
domain: software     # software, strategy, writing, research, etc.
started: 2026-01-03T15:00:45Z
updated: 2026-01-03T16:30:12Z
---

# OODA Loop Summary: [Project Name]

## Current Status
[Brief description of where we are in the process]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Next Steps
- [Next action]
```

## Workflow: The Guided Process

### Phase 1: Observe (Research)

**Objective:** Gather comprehensive context and raw information.

**Process:**
1. **Check context usage** - If >60%, warn user and recommend new window
2. Extract or capture the rough idea
3. Save to `rough-idea.md`
4. Identify research areas based on domain
5. Propose research plan to user
6. Incorporate user guidance on resources
7. Document findings in `observe/research.md`
8. Include mermaid diagrams for system architectures
9. Cite sources and include links
10. **Before transition:** Check context usage again

**Outputs:**
- `rough-idea.md`
- `observe/research.md`
- Initial `summary.md` (status: in-progress, phase: observe)

### Phase 2: Orient (Clarification & Analysis)

**Objective:** Refine understanding through structured Q&A.

**Process:**
1. **Check context usage** - If >60%, warn user and recommend new window
2. Create `observe/idea-honing.md`
3. Ask ONE question at a time
4. Append question to idea-honing.md
5. Wait for complete user response
6. Append answer to idea-honing.md
7. Repeat until sufficient clarity achieved
8. Explicitly ask if clarification is complete
9. Update `summary.md` (phase: orient)
10. **Before transition:** Check context usage again

**Critical Constraints:**
- NEVER ask multiple questions at once
- NEVER pre-populate answers without user input
- MUST wait for complete response before next question
- MAY suggest options, but MUST wait for user's actual choice

**Outputs:**
- `observe/idea-honing.md` (complete Q&A record)
- Updated `summary.md`

### Phase 3: Decide (Planning)

**Objective:** Create structured plan with clear approach.

**Process:**
1. **Check context usage** - If >60%, warn user and recommend new window
2. Create `decide/to-do.md` with focused task list
3. Create `decide/high-level-design.md` with:
   - Architecture overview
   - Major components
   - Key decisions and rationales
   - Mermaid diagrams for visualization
4. Review with user
5. Iterate based on feedback
6. Update `summary.md` (phase: decide)
7. **Before transition:** Check context usage again

**Checkpoint:** Explicitly ask user if ready to proceed to Act phase.

**Outputs:**
- `decide/to-do.md`
- `decide/high-level-design.md`
- Updated `summary.md`

### Phase 4: Act (Execution-Ready Tasks and Actions)

**Objective:** Create detailed, actionable implementation plan.

**IMPORTANT:** This skill creates execution-ready artifacts only. It does NOT execute any tasks or actions.

**Process:**
1. **Check context usage** - If >60%, warn user and recommend new window
2. Create `act/detailed-design.md` with:
   - Complete specifications
   - Component details
   - Data models
   - Error handling
   - Testing strategy
   - Consolidated requirements
   - Research findings appendix
3. Create `act/implementation-plan.md` with:
   - Checklist at top
   - Numbered implementation steps
   - Each step must:
     - Have clear objective
     - Include implementation guidance
     - Specify test requirements
     - Show integration with previous work
     - Include explicit "Demo" section
   - Ensure each step produces working, demoable functionality
   - Sequence for core end-to-end functionality early
4. Update `summary.md` (phase: act, status: complete)
5. **Final check:** Report context usage to user

**Implementation Plan Requirements:**
- Steps are discrete and manageable
- Each builds incrementally on previous
- Test-driven development where appropriate
- Core functionality validated early
- No excessive detail (design doc has that)
- Assumes all context documents available during implementation

**Outputs:**
- `act/detailed-design.md`
- `act/implementation-plan.md`
- Final `summary.md` (status: complete)

## Iteration and Flexibility

The OODA loop is **iterative**:
- May move between Observe and Orient as research uncovers new questions
- May return to Orient after Decide if gaps identified
- Support multiple research-clarification cycles before proceeding

**Always:**
- Ask user for explicit direction before phase transitions
- Offer to return to previous phases if needed
- Check in during long research or clarification sessions
- Summarize current state before asking for next step

## Domain Adaptations

While the core OODA pattern is universal, the specifics adapt by domain:

- **Software Development:** See `references/domain-applications.md` Section 1
- **Strategy/Planning:** Business strategy, product planning, organizational design
- **Writing/Documentation:** Technical writing, content creation, documentation systems
- **Research/Analysis:** Academic research, market analysis, data investigation

For detailed domain-specific guidance, see:
- **`references/ooda-pattern.md`** - Deep dive on OODA theory and LLM application
- **`references/domain-applications.md`** - Specific guidance by domain

## Best Practices

### For Context Convergence

1. **Keep artifacts focused:** Each file serves a specific purpose
2. **Progressive detail:** Start high-level, add detail only when needed
3. **Checkpoint frequently:** Update summary.md at phase transitions
4. **Reference, don't duplicate:** Link to artifacts rather than copying content
5. **Structured Q&A:** One question at a time prevents context bloat

### For Reducing Hallucinations

1. **Explicit user confirmation:** Never assume answers
2. **Wait for complete responses:** Multi-turn dialogue is ok
3. **Document decisions:** Capture rationales in artifacts
4. **Cite sources:** Link to research sources and references
5. **Visual aids:** Use mermaid diagrams for complex relationships

### For User Experience

1. **Explain the process:** Help users understand OODA phases
2. **Offer options:** Suggest but don't prescribe
3. **Be adaptive:** Recognize when to iterate vs. proceed
4. **Check satisfaction:** Ask if phase is complete before moving on
5. **Summarize progress:** Regular status updates

## Troubleshooting

### Clarification Stalls
If the Orient phase (requirements clarification) stalls:
- Suggest moving to different aspect
- Provide examples or options
- Summarize what's established, identify gaps
- Suggest conducting research to inform decisions

### Research Limitations
If needed information isn't accessible:
- Document what's missing
- Suggest alternative approaches
- Ask user for additional context
- Continue with available information

### Complexity Overload
If design becomes too complex:
- Break down into smaller components
- Focus on core functionality first
- Suggest phased approach
- Return to clarification to prioritize features

## Future Enhancements

**Subagent Support (Planned):**
For complex OODA flows that exceed single context window:
- Large brownfield codebases
- Extensive file evaluation
- Multi-domain research
- Parallel workstream management

**Automation Scripts (Planned):**
- `scripts/code-analyzer.py` for software-specific codebase analysis
- Project structure initialization automation
- Domain-specific tooling

## Additional Resources

### Deep Dives
- **`references/ooda-pattern.md`** - OODA theory, history, LLM application principles
- **`references/domain-applications.md`** - Domain-specific implementations and examples

### Example Artifacts
Each reference file includes examples of artifacts created during OODA loops across different domains.

---

**Remember:** The goal is context convergence through structured interaction. Every step should move toward a clear, actionable plan while maintaining coherence within context window constraints.
