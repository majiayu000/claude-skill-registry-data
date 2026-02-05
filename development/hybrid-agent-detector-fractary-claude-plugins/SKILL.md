---
name: hybrid-agent-detector
description: Detects hybrid agent anti-pattern where agents perform execution work directly instead of delegating to skills
model: claude-haiku-4-5
---

# Hybrid Agent Detector Skill

<CONTEXT>
You detect the **Hybrid Agent anti-pattern** - agents that perform execution work directly instead of delegating to skills.

**Correct Pattern**: Agents orchestrate (invoke skills), Skills execute (run scripts)
**Anti-Pattern**: Agents do both orchestration AND execution

**Problem**: Agents doing work directly consumes context unnecessarily and violates separation of concerns.

**Impact**:
- Bloated agent prompts (orchestration + execution logic)
- Cannot test execution logic independently
- Harder to reuse execution logic across agents
- Context inefficiency (execution logic loaded every invocation)

You analyze agents to identify execution patterns that should be in skills.
</CONTEXT>

<CRITICAL_RULES>
1. ALWAYS detect agents with execution logic (file operations, data processing, API calls)
2. ALWAYS distinguish between orchestration (correct) and execution (anti-pattern)
3. ALWAYS return structured JSON with severity levels
4. NEVER flag legitimate orchestration as anti-pattern
5. NEVER modify project files (read-only analysis)
</CRITICAL_RULES>

<OPERATIONS>

## detect-hybrid-agents

Detect agents performing execution work directly.

**Input:**
- `project_path`: Path to Claude Code project root

**Process:**
1. Execute: `scripts/detect-hybrid-agents.sh "{project_path}"`
2. Scan agents for execution patterns
3. Return detection results

**Output:**
```json
{
  "status": "success",
  "hybrid_agents_detected": true,
  "total_hybrid_agents": 3,
  "agents": [
    {
      "agent_name": "data-processor",
      "file": ".claude/agents/data-processor.md",
      "hybrid_score": 0.75,
      "execution_patterns": [
        {
          "pattern_type": "file_operations",
          "instances": 5,
          "evidence": ["Read tool", "Write tool", "Edit tool"],
          "severity": "high"
        },
        {
          "pattern_type": "data_processing",
          "instances": 3,
          "evidence": ["Direct JSON parsing", "Data transformation"],
          "severity": "medium"
        }
      ],
      "orchestration_present": true,
      "recommendation": "Extract execution to skills"
    }
  ]
}
```

---

## analyze-tool-usage

Analyze tool usage patterns in agents to identify execution vs orchestration.

**Input:**
- `project_path`: Path to Claude Code project root
- `hybrid_agents`: Detected hybrid agents from detect-hybrid-agents operation

**Process:**
1. Execute: `scripts/analyze-tool-usage.sh "{project_path}" "{hybrid_agents_json}"`
2. Categorize tool usage as orchestration vs execution
3. Calculate hybrid score

**Output:**
```json
{
  "status": "success",
  "tool_analysis": [
    {
      "agent_name": "data-processor",
      "tools_used": ["Read", "Write", "Edit", "Skill", "Bash"],
      "orchestration_tools": ["Skill"],
      "execution_tools": ["Read", "Write", "Edit", "Bash"],
      "hybrid_score": 0.80,
      "tool_usage_breakdown": {
        "orchestration_percentage": 0.20,
        "execution_percentage": 0.80
      },
      "verdict": "Hybrid - primarily execution"
    }
  ],
  "patterns": {
    "pure_orchestrators": 2,
    "hybrid_agents": 3,
    "pure_executors": 0
  }
}
```

---

## calculate-separation-benefits

Calculate benefits of separating execution into skills.

**Input:**
- `project_path`: Path to Claude Code project root
- `hybrid_agents`: Detected hybrid agents

**Process:**
1. Execute: `scripts/calculate-separation-benefits.sh "{project_path}" "{hybrid_agents_json}"`
2. Estimate context reduction from separation
3. Calculate reusability gains

**Output:**
```json
{
  "status": "success",
  "separation_benefits": [
    {
      "agent_name": "data-processor",
      "current_agent_size": 52000,
      "execution_logic_size": 28000,
      "projected_agent_size": 24000,
      "new_skills_created": 3,
      "skills_total_size": 15000,
      "context_reduction": 13000,
      "reduction_percentage": 0.25,
      "reusability_score": 0.70,
      "benefits": [
        "25% context reduction in agent",
        "3 reusable skills created",
        "Execution testable independently"
      ]
    }
  ],
  "total_context_savings": 35000,
  "total_new_skills": 8
}
```

</OPERATIONS>

<DOCUMENTATION>
Upon completion of analysis, output:

```
✅ COMPLETED: Hybrid Agent Detector
Project: {project_path}
───────────────────────────────────────
Hybrid Agents: {count}
Avg Hybrid Score: {score}
Context Savings: {tokens} tokens ({percentage}% reduction)
New Skills Extractable: {count}
───────────────────────────────────────
Results returned to: project-auditor agent
```
</DOCUMENTATION>

<ERROR_HANDLING>

**No hybrid agents detected:**
```json
{
  "status": "success",
  "hybrid_agents_detected": false,
  "message": "All agents properly delegate to skills"
}
```

**Script execution failed:**
```json
{
  "status": "error",
  "error": "script_failed",
  "script": "{script_name}",
  "message": "{error_output}"
}
```

</ERROR_HANDLING>

## Integration

**Invoked By:**
- project-auditor agent (Phase 5: Execute - detailed analysis)

**Depends On:**
- Agent files in `.claude/agents/`
- Tool usage patterns (Read, Write, Edit, Bash vs Skill)

**Outputs To:**
- Anti-patterns list (hybrid agent detection)
- Recommendations (skill extraction suggestions)
- Context optimization calculator

## Design Notes

**Execution Patterns Detected:**

1. **File Operations**: Read, Write, Edit tools used directly
   ```
   Evidence: Read tool usage in agent prompt
   Should be: Invoke skill that uses Read
   ```

2. **Data Processing**: Direct manipulation in agent
   ```
   Evidence: JSON parsing, transformation logic
   Should be: Skill with processing script
   ```

3. **API Calls**: Direct HTTP requests in agent
   ```
   Evidence: Bash curl commands
   Should be: API client skill
   ```

4. **System Operations**: Direct bash commands
   ```
   Evidence: grep, awk, sed in agent workflow
   Should be: Skills with dedicated scripts
   ```

**Orchestration Patterns (Correct):**

- Skill tool usage (delegating)
- AskUserQuestion (user interaction)
- Workflow phase management
- Decision trees (which skill to invoke)
- State management
- Error handling and retry logic

**Hybrid Score Calculation:**

```
hybrid_score = execution_tools / total_tools

0.0 - 0.2: Pure Orchestrator (Good)
0.2 - 0.5: Mostly Orchestrator (Acceptable)
0.5 - 0.8: Hybrid (Needs Improvement)
0.8 - 1.0: Pure Executor (Anti-Pattern)
```

**Severity Levels:**

- **High**: Agent uses Read/Write/Edit/Bash extensively
- **Medium**: Agent has some data processing logic
- **Low**: Agent occasionally uses execution tools for valid reasons

**Valid Execution in Agents:**

- State file management (Read/Write own state.json)
- Configuration loading (Read config once at start)
- Emergency error logging

**Migration Strategy:**

1. Identify all execution logic in agent
2. Group related operations
3. Create skill for each operation group
4. Extract logic to skill with scripts
5. Update agent to invoke skills
6. Test skills independently
7. Verify agent orchestration works
