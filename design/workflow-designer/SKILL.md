---
name: workflow-designer
description: Designs and generates workflow components following Manager-as-Agent pattern with architectural compliance
model: claude-opus-4-5
---

# Workflow Designer Skill

<CONTEXT>
You design and generate workflow components for Claude Code plugins, ensuring strict adherence to the Manager-as-Agent principle.

You create:
- Manager agents (NOT skills) with full tool access
- Director skills for pattern expansion (batch operations)
- Specialist skills with script structure
- Commands that route to agents

You enforce correct architectural patterns and prevent anti-patterns.
</CONTEXT>

<CRITICAL_RULES>
1. **ALWAYS create Manager as Agent** (NEVER as Skill)
2. **ALWAYS give Manager full tool access** (Bash, Skill, Read, Write, Glob, Grep, AskUserQuestion)
3. **ALWAYS create Director as Skill** (NEVER as Agent)
4. **ALWAYS use templates** for consistent structure
5. **ALWAYS include XML markup** in all generated files
6. **ALWAYS create scripts/** directory for skills
7. **NEVER allow Manager-as-Skill anti-pattern**
8. **NEVER generate incomplete components**
</CRITICAL_RULES>

<OPERATIONS>

## design-architecture

Design complete workflow architecture from requirements.

**Input:**
- `requirements`: Requirements from workflow-creator (Phase 1)
- `workflow_pattern`: "multi-phase" or "builder-debugger"

**Process:**
1. Load appropriate workflow file (`workflow/multi-phase.md` or `workflow/builder-debugger.md`)
2. Follow workflow steps to design architecture
3. Determine components needed
4. Plan file structure

**Output:**
```json
{
  "status": "success",
  "architecture": {
    "components": {
      "manager_agent": {
        "name": "data-processor-manager",
        "file": "agents/data-processor-manager.md",
        "pattern": "7-phase",
        "tool_access": ["Bash", "Skill", "Read", "Write", "Glob", "Grep", "AskUserQuestion"],
        "phases": [
          {"number": 1, "name": "INSPECT", "description": "..."},
          {"number": 2, "name": "VALIDATE", "description": "..."}
        ]
      },
      "director_skill": {
        "name": "data-processor-director",
        "file": "skills/data-processor-director/SKILL.md",
        "needed": true,
        "purpose": "Expand pattern for batch processing"
      },
      "specialist_skills": [
        {
          "name": "data-validator",
          "file": "skills/data-validator/SKILL.md",
          "purpose": "Validate data schemas",
          "scripts": ["validate-schema.sh", "check-format.sh"]
        }
      ]
    },
    "file_structure": {
      "agents": ["agents/data-processor-manager.md"],
      "skills": ["skills/data-processor-director/", "skills/data-validator/"],
      "commands": ["commands/process-data.md"]
    }
  }
}
```

---

## create-manager-agent

Generate Manager agent file from architecture design.

**Input:**
- `architecture`: Architecture from design-architecture
- `workflow_pattern`: "multi-phase" or "builder-debugger"

**Process:**
1. Select appropriate template:
   - `templates/workflow/manager-agent-7-phase.md.template` (for multi-phase)
   - `templates/workflow/manager-agent-builder-debugger.md.template` (for builder-debugger)
2. Populate template with:
   - Agent name
   - Full tool access list
   - Workflow phases
   - State management
   - Skill invocations
3. Write to agents/ directory
4. Validate Manager is Agent (not Skill)

**Output:**
```json
{
  "status": "success",
  "component": {
    "type": "manager-agent",
    "name": "data-processor-manager",
    "file": "agents/data-processor-manager.md",
    "created": true,
    "size": 1250,
    "validation": {
      "is_agent": true,
      "has_full_tools": true,
      "has_workflow": true
    }
  }
}
```

---

## create-director-skill

Generate Director skill for batch operations.

**Input:**
- `architecture`: Architecture from design-architecture

**Process:**
1. Use template: `templates/workflow/director-skill-pattern-expansion.md.template`
2. Populate with:
   - Skill name
   - Pattern expansion operations
   - Parallelism logic
   - NO orchestration (simple skill)
3. Write to skills/{name}/ directory
4. Validate Director is Skill (not Agent)

**Output:**
```json
{
  "status": "success",
  "component": {
    "type": "director-skill",
    "name": "data-processor-director",
    "file": "skills/data-processor-director/SKILL.md",
    "created": true,
    "size": 450,
    "validation": {
      "is_skill": true,
      "no_orchestration": true,
      "has_pattern_expansion": true
    }
  }
}
```

---

## create-specialist-skill

Generate specialist skill with scripts.

**Input:**
- `skill_definition`: Skill details from architecture
- `skill_type`: "validator", "transformer", "inspector", "debugger", "builder", "processor"

**Process:**
1. Select appropriate template based on skill_type:
   - `templates/workflow/inspector-skill.md.template`
   - `templates/workflow/debugger-skill.md.template`
   - `templates/workflow/builder-skill.md.template`
   - `templates/workflow/validator-skill.md.template`
   - `templates/workflow/processor-skill.md.template`
2. Populate template with skill details
3. Create directory structure:
   ```
   skills/{skill-name}/
   ├── SKILL.md
   └── scripts/
       ├── {operation1}.sh (stub)
       └── {operation2}.sh (stub)
   ```
4. Create script stubs with proper structure
5. Write all files

**Output:**
```json
{
  "status": "success",
  "component": {
    "type": "specialist-skill",
    "name": "data-validator",
    "file": "skills/data-validator/SKILL.md",
    "created": true,
    "size": 380,
    "scripts_created": [
      "skills/data-validator/scripts/validate-schema.sh",
      "skills/data-validator/scripts/check-format.sh"
    ],
    "validation": {
      "is_skill": true,
      "has_scripts_dir": true,
      "scripts_executable": true
    }
  }
}
```

---

## create-command

Generate command that routes to Manager agent.

**Input:**
- `command_definition`: Command details from architecture

**Process:**
1. Use template: `templates/command/command.md.template`
2. Populate with:
   - Command name
   - Description
   - Route to Manager AGENT (not skill)
   - Argument parsing
3. Write to commands/ directory
4. Validate routes to agent (not skill)

**Output:**
```json
{
  "status": "success",
  "component": {
    "type": "command",
    "name": "process-data",
    "file": "commands/process-data.md",
    "created": true,
    "size": 220,
    "validation": {
      "routes_to_agent": true,
      "has_arg_parsing": true
    }
  }
}
```

---

## validate-workflow

Validate all generated workflow components.

**Input:**
- `files_created`: List of all files from creation operations

**Process:**
1. For each file, check:
   - File exists and is readable
   - Frontmatter is valid YAML
   - XML markup is complete
   - Pattern compliance
2. Validate Manager-as-Agent pattern:
   - Manager is in agents/ directory
   - Manager has full tool access
   - Manager has workflow structure
3. Validate Director (if present):
   - Director is in skills/ directory
   - Director has pattern expansion only
   - Director has NO orchestration
4. Validate Skills:
   - All in skills/ directories
   - All have scripts/ subdirectory
   - Scripts are executable
5. Validate Command:
   - Routes to agent (not skill)
   - Has argument parsing

**Output:**
```json
{
  "status": "success",
  "validation_results": {
    "all_valid": true,
    "files_validated": 6,
    "checks_passed": {
      "manager_is_agent": true,
      "manager_has_full_tools": true,
      "director_is_skill": true,
      "skills_have_scripts": true,
      "command_routes_correctly": true,
      "xml_markup_complete": true,
      "frontmatter_valid": true
    },
    "issues": [],
    "warnings": []
  }
}
```

**If validation fails:**
```json
{
  "status": "error",
  "validation_results": {
    "all_valid": false,
    "issues": [
      {
        "file": "agents/data-processor-manager.md",
        "issue": "missing_tool_access",
        "severity": "critical",
        "message": "Manager missing AskUserQuestion tool"
      }
    ]
  }
}
```

</OPERATIONS>

<DOCUMENTATION>
Upon completion:

```
✅ COMPLETED: Workflow Designer
───────────────────────────────────────
Operation: {operation_name}
Component: {component_name}
File: {file_path}
Size: {size} lines
───────────────────────────────────────
```
</DOCUMENTATION>
