---
name: validate-system
description: Validate Nexus-v3 system integrity and fix common issues automatically. Load when user mentions "validate system", "check system", or "fix problems". Runs comprehensive checks on folder structure, metadata files, and framework consistency with auto-repair capabilities.
---

# Validate System

Check system integrity, auto-fix issues, validate maps, and run optional Python validation hooks.

## Purpose

The `validate-system` skill performs comprehensive system health checks, validates structural integrity, checks navigation map accuracy, runs optional Python validation hooks, and attempts to auto-fix common issues. Use this skill when navigation seems stale, after manual file changes, or as periodic maintenance.

**Key Features:**
- **Comprehensive Checks**: Core files, structure, memory, navigation, projects, skills
- **Map Integrity Validation**: Ensures skill-map.md and project-map.md are accurate
- **Python Hooks**: Runs automated validators (optional, graceful skip if unavailable)
- **Auto-Fix**: Regenerates navigation, recreates templates, repairs structure
- **Detailed Reporting**: Clear report of checks, issues, and fixes

**Time Estimate**: <10 seconds for full validation

---


## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all validation steps:
```
- [ ] Check core files
- [ ] Check folder structure
- [ ] Check memory files
- [ ] Check navigation files
- [ ] Validate projects
- [ ] Validate skills
- [ ] Check map integrity
- [ ] Run Python hooks (if available)
- [ ] Auto-fix issues
- [ ] Generate report
- [ ] Display report
- [ ] Close session to save progress
```

**Mark tasks complete as you finish each step.**

### Step 2: Execute Validation Workflow

This skill performs comprehensive system validation with the following checks:

1. **Core Files** - Verify critical system files exist
2. **Folder Structure** - Check required directories
3. **Memory Files** - Validate Memory/ content
4. **Navigation Files** - Check framework-map.md and skill-map.md
5. **Projects** - Validate all projects in 02-Projects/
6. **Skills** - Validate all skills in 00-system/Skills/
7. **Map Integrity** - Ensure maps match actual files
8. **Python Hooks** - Run validation hooks (if available)
9. **Auto-Fix** - Repair common issues automatically
10. **Report** - Generate and display comprehensive report

**Detailed validation steps**: See [references/validation-checks.md](references/validation-checks.md)

**Report templates**: See [references/report-templates.md](references/report-templates.md)

**Time Estimate**: <10 seconds for full validation

### Final Step: Close Session

**Automatically trigger the close-session skill**:
```
Auto-triggering close-session to save progress...
```

This ensures all validation results and any auto-fixes are properly saved to memory.

---

## Error Handling

### Critical Files Missing
**Scenario**: framework-map.md, orchestrator.md, or claude.md missing

**Action**:
- Report as CRITICAL ERROR
- Cannot auto-fix (system corrupted)
- Suggest: "Your system appears corrupted. Please restore from backup or reinstall Nexus-v3."
- Do NOT proceed with auto-fixes (unsafe)

### Python Hook Crashes
**Scenario**: Python hook script crashes or returns invalid JSON

**Action**:
- Catch error gracefully
- Report: "Hook {name} crashed: {error}"
- Add to issues list
- Continue with other hooks (don't block validation)

### Cannot Write to Files
**Scenario**: Auto-fix fails due to file permission issues

**Action**:
- Report: "Cannot write to {file}: {error}"
- Add to manual fix list
- Provide manual instructions
- Continue with other auto-fixes

### Corrupted Memory Files
**Scenario**: Memory/ files exist but are not valid markdown

**Action**:
- Report: "{file} is corrupted (invalid markdown)"
- Offer: "Replace with empty template? This will lose current content."
- Wait for user confirmation
- IF confirmed → Replace with template
- IF declined → Add to manual fix list

### Empty Projects/ Folder
**Scenario**: Projects/ exists but is empty (only during first-time setup)

**Action**:
- Report: "Projects/ folder is empty (no projects yet)"
- Note: "This is normal for new users."
- Suggest: "Say 'create project' to start your first project!"
- Mark as INFO (not an error)

### Empty Skills/ Folder
**Scenario**: Skills/ exists but is empty

**Action**:
- Report: "No user skills found (Skills/ folder empty)"
- Note: "This is normal if you haven't created any skills yet."
- Suggest: "Run create-skill to add your first skill!"
- Mark as INFO (not an error)

---

## Notes

**When to Run validate-system:**
- After manual file edits
- When navigation seems stale or inaccurate
- After accidentally deleting files
- As periodic maintenance (weekly/monthly)
- When system behavior seems off

**Auto-Fix Safety:**
- Only fixes non-destructive issues
- Never deletes user content
- Creates templates, regenerates navigation
- Critical issues require manual intervention

**Python Hooks:**
- Completely optional (system works without them)
- Provide deeper automated validation
- Gracefully skip if Python not available
- Custom hooks can be added to 00-system/hooks/

**Hook JSON Format:**
```json
{
  "valid": true/false,
  "errors": [
    {"file": "path", "line": 42, "message": "error description", "severity": "error"}
  ],
  "warnings": [
    {"file": "path", "line": 15, "message": "warning description", "severity": "warning"}
  ]
}
```

**Map Integrity Importance:**
- skill-map.md MUST match Skills/ folder
- 02-projects/project-map.md MUST match Projects/ folder
- Dead links break navigation
- close-session maintains integrity automatically

**Validation Frequency:**
- Run when suspicious: anytime something feels off
- Run after manual changes: edited files outside skills
- Run periodically: weekly or monthly maintenance
- NOT needed after normal skill/project usage (close-session handles it)

**Integration with close-session:**
- close-session automatically maintains map integrity
- validate-system catches issues between sessions
- Both work together for system health

---

**Remember**: validate-system is your system health check. Run it when things seem off, and let it auto-fix what it can!
