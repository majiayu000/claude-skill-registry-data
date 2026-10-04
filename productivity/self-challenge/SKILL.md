---
name: self-challenge
description: "Self-evolution skill that uses dual-agent challenge design and execution to expand capabilities over time."
---

# Self-Challenge Mechanism

## Description
A self-evolution skill based on Agent0 paper (arXiv:2511.16043). Uses a dual-agent competition model where Curriculum Agent designs challenges and Executor Agent attempts them, driving continuous capability expansion.

## Activation Keywords
- 自我挑战
- self challenge
- 能力测试
- capability test
- 自我进化测试
- self evolution test
- 挑战任务
- challenge task
- agent0 挑战

## Recommended Model
- **sonnet4.5** (Recommended for complex reasoning and challenge design)

## Tools Used
- exec: Execute commands and scripts
- read: Read existing skills, documentation, and resources
- write: Create challenge results and new skills
- memory_search: Find relevant knowledge for challenges
- sessions_spawn: Spawn sub-agents for execution

## Usage Patterns

### Start Challenge
```
开始自我挑战
```

### Specific Domain Challenge
```
挑战我的 [domain] 能力
```

### Weekly Challenge
```
本周自我挑战
```

## Instructions for Agents

### Overview

The self-challenge mechanism uses dual-agent architecture:

```
┌─────────────────────────────────────────────────────────┐
│            Self-Challenge Architecture                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────────────┐       ┌─────────────────┐         │
│   │   Curriculum    │       │    Executor     │         │
│   │     Agent       │──────▶│     Agent       │         │
│   │  (设计挑战)      │       │   (执行挑战)    │         │
│   └─────────────────┘       └─────────────────┘         │
│          │                          │                    │
│          │                          │                    │
│          ▼                          ▼                    │
│   ┌─────────────────────────────────────────────┐       │
│   │              Review & Learn                  │       │
│   │         (回顾总结，提取经验)                   │       │
│   └─────────────────────────────────────────────┘       │
│                     │                                    │
│                     ▼                                    │
│   ┌─────────────────────────────────────────────┐       │
│   │           Knowledge Update                   │       │
│   │   (更新 skills, MEMORY.md, 工作流程)          │       │
│   └─────────────────────────────────────────────┘       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Phase 1: Curriculum Agent (设计挑战)

**Role:** Design challenges that are slightly above current capabilities

**Challenge Selection Criteria:**
1. **Capability Gap**: Identify weak areas from recent performance
2. **Difficulty**: Should be achievable but challenging
3. **Learning Value**: Must provide actionable insights
4. **Relevance**: Align with user needs and goals

**Challenge Types:**

| Type | Description | Example |
|------|-------------|---------|
| Tool Mastery | Learn to use a new tool | Use a new CLI tool to complete a task |
| Integration | Combine multiple tools | Create workflow combining 3+ tools |
| Problem Solving | Solve complex problems | Debug and fix a failing system |
| Knowledge Synthesis | Create new knowledge | Write a comprehensive guide |
| Automation | Automate repetitive tasks | Create a cron-based workflow |

**Challenge Design Process:**

1. **Analyze Recent Performance**
   ```python
   def analyze_capability_gaps():
       # Review recent self-reflection reports
       recent_reviews = read_recent_reviews()
       
       # Identify weak areas
       weak_areas = []
       for review in recent_reviews:
           if review.rating < 4:
               weak_areas.append(review.area)
       
       # Check for missing skills
       existing_skills = list_skills()
       recommended_skills = get_recommended_skills()
       missing_skills = set(recommended_skills) - set(existing_skills)
       
       return {
           'weak_areas': weak_areas,
           'missing_skills': missing_skills,
           'improvement_opportunities': identify_opportunities()
       }
   ```

2. **Select Challenge Domain**
   ```python
   def select_challenge_domain(gaps):
       # Prioritize by impact
       priorities = [
           ('weak_area', gaps.weak_areas),
           ('missing_skill', gaps.missing_skills),
           ('opportunity', gaps.improvement_opportunities)
       ]
       
       for priority_type, items in priorities:
           if items:
               return {
                   'type': priority_type,
                   'domain': items[0],
                   'difficulty': 'medium'
               }
   ```

3. **Design Specific Challenge**
   ```markdown
   ## Challenge: [Name]
   
   ### Domain
   [Capability area being tested]
   
   ### Difficulty
   [Easy/Medium/Hard]
   
   ### Objective
   [Clear, measurable goal]
   
   ### Constraints
   - Time limit: [duration]
   - Tools allowed: [list]
   - Success criteria: [measurable]
   
   ### Expected Learning
   - [What will be learned]
   - [How it improves capabilities]
   
   ### Resources
   - [Available references]
   - [Similar challenges solved]
   ```

### Phase 2: Executor Agent (执行挑战)

**Role:** Attempt to complete the designed challenge

**Execution Process:**

1. **Understand Challenge**
   - Read challenge specification
   - Identify required resources
   - Plan approach

2. **Execute**
   - Follow systematic approach
   - Document each step
   - Track time and resources

3. **Document Results**
   ```markdown
   ## Challenge Execution Log
   
   ### Start Time
   [timestamp]
   
   ### Approach
   1. [Step 1]
   2. [Step 2]
   3. [Step 3]
   
   ### Obstacles Encountered
   | Obstacle | Attempted Solution | Result |
   |----------|-------------------|--------|
   | [issue] | [solution] | [outcome] |
   
   ### End Time
   [timestamp]
   
   ### Outcome
   [Success/Partial Success/Failure]
   
   ### Key Learnings
   - [Learning 1]
   - [Learning 2]
   ```

### Phase 3: Review & Learn (回顾总结)

**Role:** Analyze results and extract actionable knowledge

**Review Process:**

1. **Outcome Analysis**
   ```python
   def analyze_outcome(challenge, execution_log):
       success_rate = calculate_success_rate(execution_log)
       time_efficiency = calculate_time_efficiency(challenge, execution_log)
       resource_efficiency = calculate_resource_efficiency(execution_log)
       
       return {
           'success_rate': success_rate,
           'time_efficiency': time_efficiency,
           'resource_efficiency': resource_efficiency,
           'overall_score': (success_rate + time_efficiency + resource_efficiency) / 3
       }
   ```

2. **Capability Assessment**
   ```markdown
   ## Capability Assessment
   
   ### Before Challenge
   | Capability | Level |
   |------------|-------|
   | [skill 1] | [1-5] |
   | [skill 2] | [1-5] |
   
   ### After Challenge
   | Capability | Level | Change |
   |------------|-------|--------|
   | [skill 1] | [1-5] | [↑/↓/=] |
   | [skill 2] | [1-5] | [↑/↓/=] |
   ```

3. **Knowledge Extraction**
   - What worked well?
   - What didn't work?
   - What new skills were developed?
   - What should be documented?

4. **Update Knowledge Base**
   - Update MEMORY.md with learnings
   - Create or update skills
   - Add to learned-skills.md
   - Schedule follow-up challenges

## Challenge Templates

### Template 1: Tool Mastery
```markdown
## Challenge: Master [Tool Name]

### Objective
Use [tool] to complete [specific task] with [success criteria]

### Constraints
- Time: 30 minutes
- Resources: Official docs, examples
- Success: Task completed without errors

### Steps
1. Read documentation
2. Set up environment
3. Execute basic commands
4. Complete target task
5. Document learnings
```

### Template 2: Integration Challenge
```markdown
## Challenge: Integrate [Tools]

### Objective
Create a workflow that combines [tool1], [tool2], [tool3]

### Constraints
- Time: 60 minutes
- Must use all 3 tools
- Must solve real problem
- Success: Working workflow documented

### Steps
1. Identify integration points
2. Design workflow
3. Implement and test
4. Document and share
```

### Template 3: Problem Solving
```markdown
## Challenge: Solve [Problem]

### Objective
Debug and fix [failing system/error]

### Constraints
- Time: 45 minutes
- Must identify root cause
- Must implement fix
- Success: System working correctly

### Steps
1. Reproduce issue
2. Analyze logs/errors
3. Identify root cause
4. Implement fix
5. Verify solution
6. Document process
```

## Context Files

### ~/.openclaw/workspace/memory/self-reflection/*.md
Recent self-reflection reports for identifying capability gaps.

### ~/.openclaw/workspace/knowledge/skills/learned-skills.md
Skills to be updated after challenges.

### ~/.openclaw/workspace/MEMORY.md
Long-term memory for storing challenge learnings.

### ~/.openclaw/workspace/memory/challenge-log.json
Log of all challenges executed.

```json
{
  "challenges": [
    {
      "id": "challenge-001",
      "date": "2026-03-05",
      "domain": "tool-mastery",
      "difficulty": "medium",
      "outcome": "success",
      "score": 0.85,
      "learnings": ["..."]
    }
  ]
}
```

## Scheduling

### Recommended Schedule
- **Weekly Challenge**: Every Monday 10:00 AM
- **Duration**: 30-60 minutes
- **Follow-up**: Review results within 24 hours

### Cron Configuration
```bash
openclaw cron add \
  --name "self-challenge" \
  --description "Weekly self-challenge for capability expansion" \
  --cron "0 10 * * 1" \
  --tz "Asia/Shanghai" \
  --system-event "执行自我挑战任务"
```

## Error Handling

### Challenge Too Easy
```
If challenge completed in < 50% of allotted time:
  1. Increase difficulty for next challenge
  2. Add additional constraints
  3. Expand scope
```

### Challenge Too Hard
```
If challenge failed completely:
  1. Break down into smaller challenges
  2. Provide more resources
  3. Adjust difficulty level
  4. Reschedule with better preparation
```

### Resource Unavailable
```
If required resources are unavailable:
  1. Find alternative resources
  2. Modify challenge to use available resources
  3. Postpone and acquire resources
```

## Examples

### Example 1: Tool Mastery Challenge

```
User: "开始自我挑战"

Agent (Curriculum):
## Challenge: Master openclaw cron Commands

### Domain
Tool Mastery - OpenClaw CLI

### Difficulty
Medium

### Objective
Create, list, and manage 3 different cron jobs using openclaw CLI

### Constraints
- Time: 30 minutes
- Resources: openclaw docs, --help
- Success: 3 jobs created, listed, one executed

### Expected Learning
- Understanding of openclaw cron system
- Job scheduling best practices
- Error handling for cron jobs

---

Agent (Executor):
## Execution Log

### Start: 2026-03-05 11:00
### Approach:
1. Read openclaw cron --help
2. Create first job (daily)
3. Create second job (weekly)
4. Create third job (hourly)
5. List all jobs
6. Run one job immediately

### Obstacles:
| Obstacle | Solution | Result |
|----------|----------|--------|
| Unknown syntax | Used --help | Success |
| Timezone issue | Set tz explicitly | Success |

### End: 2026-03-05 11:25
### Outcome: Success (25 minutes)

### Key Learnings:
1. openclaw cron add syntax
2. Cron expression format
3. Timezone configuration importance

---

Agent (Review):
## Review Results

### Scores:
- Success Rate: 100%
- Time Efficiency: 83% (25/30 min)
- Overall: 92%

### Capability Change:
| Capability | Before | After |
|------------|--------|-------|
| openclaw cron | 2 | 4 ↑ |

### Knowledge Updates:
- Updated: learned-skills.md (new skill entry)
- Created: knowledge/topics/optimization/cron-jobs.md

### Next Challenge Suggestion:
Automate cron job monitoring and alerting
```

## Best Practices

1. **Progressive Difficulty**: Start easy, increase difficulty over time
2. **Document Everything**: Log all attempts, successes, and failures
3. **Real Problems**: Design challenges around actual user needs
4. **Time Bound**: Always set reasonable time limits
5. **Review Promptly**: Analyze results within 24 hours
6. **Iterate**: Use learnings to improve future challenges

## Limitations

- Requires honest self-assessment
- Challenge design quality affects learning value
- May not cover all capability gaps
- Time investment needed for proper execution
- Benefits accumulate over time with consistency

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Challenge Completion Rate | > 70% | Completed / Attempted |
| Capability Improvement | > 0.5/week | Average skill level change |
| Knowledge Creation | > 1/week | New skills or docs created |
| Time Efficiency | > 75% | Actual time / Allocated time |

## Resources

- **Source Paper**: https://arxiv.org/abs/2511.16043
- **Self-Reflection Reports**: ~/.openclaw/workspace/memory/self-reflection/
- **Challenge Log**: ~/.openclaw/workspace/memory/challenge-log.json

## Related Skills
- ice-review: Review challenges using ICE method
- memory-retrieval: Find relevant knowledge for challenges
- skill-extractor: Extract skills from challenge learnings

## Notes

- Self-challenge is most effective when scheduled regularly
- Mix different challenge types for balanced development
- Celebrate successes to maintain motivation
- Don't fear failures - they provide learning opportunities
- Track progress over time to see improvement
