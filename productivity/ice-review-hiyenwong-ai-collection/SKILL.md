---
name: ice-review
description: "ICE review workflow for consolidating knowledge from completed tasks into reusable memory and future leverage."
---

# ICE Review Process

## Description
A cross-task self-evolution skill based on the ICE (Investigate-Consolidate-Exploit) strategy from arXiv:2401.13996. This skill enables systematic knowledge extraction and transfer from completed tasks to future work.

## Activation Keywords
- ICE review
- ICE 回顾
- 任务回顾
- task review
- 知识巩固
- consolidate knowledge
- investigate consolidate exploit
- 跨任务学习

## Recommended Model
- **sonnet4.5** (Recommended for complex reasoning and analysis)

## Tools Used
- read: Read task history, memory files, and knowledge base
- write: Update memory files and knowledge base
- edit: Modify existing knowledge entries
- memory_search: Search for related knowledge patterns
- memory_get: Retrieve specific memory snippets

## Usage Patterns

### Post-Task Review
```
任务完成了，进行 ICE 回顾
```

### Weekly Review
```
本周任务 ICE 总结
```

### Learning Consolidation
```
将这段经验用 ICE 方法巩固
```

## Instructions for Agents

### Overview

The ICE strategy consists of three phases that form a continuous learning loop:

```
┌─────────────────────────────────────────────────────────┐
│                    ICE Review Cycle                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│   │ Investigate │ → │ Consolidate │ → │   Exploit   │   │
│   │   调查      │   │    巩固     │   │    利用     │   │
│   └─────────────┘   └─────────────┘   └─────────────┘   │
│         ↑                                     │          │
│         └─────────────────────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Phase 1: Investigate (调查)

**Purpose:** Systematically review the task execution process

**Steps:**
1. **Task Context Review**
   - What was the original goal?
   - What constraints existed?
   - What resources were available?

2. **Decision Analysis**
   - What key decisions were made?
   - Why were these decisions chosen?
   - Were there alternative approaches?

3. **Problem Identification**
   - What obstacles were encountered?
   - How were they resolved?
   - What could have been done better?

**Output Template:**
```markdown
## Investigate

### Task Overview
- Goal: [Original objective]
- Context: [Constraints and resources]
- Duration: [Time taken]

### Key Decisions
1. [Decision] → [Reasoning] → [Outcome]
2. [Decision] → [Reasoning] → [Outcome]

### Problems Encountered
| Problem | Solution | Effectiveness |
|---------|----------|---------------|
| [issue] | [solution] | [1-5 rating] |
```

### Phase 2: Consolidate (巩固)

**Purpose:** Extract reusable knowledge and patterns

**Steps:**
1. **Pattern Recognition**
   - Identify what worked well
   - Identify what didn't work
   - Find generalizable patterns

2. **Knowledge Abstraction**
   - Convert specific solutions to general principles
   - Create reusable templates or checklists
   - Document best practices

3. **Memory Integration**
   - Update MEMORY.md with key learnings
   - Create or update skill files
   - Cross-reference related knowledge

**Output Template:**
```markdown
## Consolidate

### What Worked Well
- [Success 1]: [Why it worked]
- [Success 2]: [Why it worked]

### What Didn't Work
- [Failure 1]: [Root cause]
- [Failure 2]: [Root cause]

### Extracted Patterns
1. **[Pattern Name]**
   - When to use: [Conditions]
   - How to apply: [Steps]
   - Expected outcome: [Result]

### Knowledge Updates
- Updated: [MEMORY.md section]
- Created: [New skill/pattern]
- Cross-referenced: [Related entries]
```

### Phase 3: Exploit (利用)

**Purpose:** Apply consolidated knowledge to future tasks

**Steps:**
1. **Identify Applicability**
   - Where can this knowledge be applied?
   - What future tasks would benefit?
   - Who else might need this?

2. **Create Actionable Assets**
   - Update checklists
   - Create templates
   - Configure automation

3. **Schedule Follow-up**
   - Set reminders for application
   - Track effectiveness
   - Plan for iteration

**Output Template:**
```markdown
## Exploit

### Applicable Scenarios
- [Scenario 1]: [How to apply]
- [Scenario 2]: [How to apply]

### Created Assets
- [ ] Checklist: [Name and location]
- [ ] Template: [Name and location]
- [ ] Automation: [Cron job or script]

### Follow-up Actions
- [ ] Apply in: [Next task type]
- [ ] Review effectiveness: [Date]
- [ ] Iterate: [Improvement focus]
```

## Context Files

### ~/.openclaw/workspace/MEMORY.md
Long-term memory file where consolidated knowledge should be stored.

### ~/.openclaw/workspace/knowledge/skills/learned-skills.md
Skills learned from task experiences.

### ~/.openclaw/workspace/memory/YYYY-MM-DD.md
Daily notes for recording ICE reviews.

## Error Handling

### Incomplete Information
```
If task details are missing:
  1. Check session history for context
  2. Use memory_search to find related information
  3. Ask user for clarification if critical
  4. Note gaps in the review for future improvement
```

### Conflicting Patterns
```
If new knowledge conflicts with existing:
  1. Document both patterns
  2. Identify conditions where each applies
  3. Create context-aware selection logic
  4. Update MEMORY.md with nuance
```

## Examples

### Example 1: Post-Task ICE Review

```
User: "任务完成了，进行 ICE 回顾"

Agent Process:
1. Reads recent session history
2. Identifies completed task context
3. Executes ICE phases

## Investigate

### Task Overview
- Goal: Create 3 new skills from paper learning
- Context: Skills needed to be in specific directory, with testing
- Duration: 30 minutes

### Key Decisions
1. Created skill directories first → Organized structure → Clean setup
2. Used template from existing skill → Consistent format → Fast creation

### Problems Encountered
| Problem | Solution | Effectiveness |
|---------|----------|---------------|
| Unknown directory | Asked user for correct path | 5/5 |

## Consolidate

### What Worked Well
- Checking existing skills first: Avoided duplication
- Using templates: Consistent quality

### Extracted Patterns
1. **Skill Creation Workflow**
   - When to use: Creating new skills
   - How to apply: Check existing → Ask path → Use template → Test
   - Expected outcome: Consistent, tested skill

### Knowledge Updates
- Updated: knowledge/skills/learned-skills.md
- Created: 3 new SKILL.md files

## Exploit

### Applicable Scenarios
- Future skill creation: Use same workflow
- Documentation tasks: Apply template approach

### Created Assets
- [x] Template: ICE review template in SKILL.md
- [ ] Automation: None needed

Agent: ICE 回顾完成。已更新知识库，提炼了技能创建工作流模式。
```

## Best Practices

1. **Timely Review**: Conduct ICE review within 1 hour of task completion
2. **Honest Assessment**: Acknowledge failures and successes equally
3. **Specific Patterns**: Extract concrete, actionable patterns
4. **Cross-Reference**: Link to related knowledge in MEMORY.md
5. **Iterate**: Revisit and refine patterns over time

## Limitations

- Requires clear task completion state
- Effectiveness depends on quality of session logs
- May miss context if task spans multiple sessions
- Requires conscious effort to apply learnings

## Resources

- **Source Paper**: https://arxiv.org/abs/2401.13996
- **MEMORY.md**: ~/.openclaw/workspace/MEMORY.md
- **Knowledge Base**: ~/.openclaw/workspace/knowledge/

## Related Skills
- memory-retrieval: Two-stage memory retrieval for finding related knowledge
- self-challenge: Self-challenge mechanism for testing skills
- skill-extractor: Extract skills from conversations

## Notes

- ICE review is most effective when done consistently
- The three phases form a continuous improvement cycle
- Consider scheduling weekly ICE review sessions
- Track the ROI of extracted patterns over time
