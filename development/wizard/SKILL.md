---
name: wizard
description: Smart routing wizard for creating skills, agents, commands with complexity-based skill loading
allowed-tools: ["Read", "Write", "Bash", "Grep", "Glob", "Task", "Skill", "AskUserQuestion"]
---

# Wizard Skill

Smart routing for plugin development with complexity-based skill loading.

## Self-Enforcement (W028 Compliance)

All MUST/CRITICAL keywords are hookified via `hooks/hooks.json`:
- `PreToolUse/PostToolUse → validate_all.py`
- `PostToolUse:Task → solution-synthesis-gate.py`

---

## Complexity Detection

| Level | Keywords | Skills to Load |
|-------|----------|----------------|
| **Simple** | simple, basic, 단순, 기본 | skill-design |
| **Standard** | standard, normal, 일반 | + orchestration-patterns, hook-templates |
| **Advanced** | advanced, complex, serena, mcp, 고급 | ALL pattern skills |

If no keyword detected, ask:
```yaml
AskUserQuestion:
  question: "프로젝트 복잡도를 선택하세요"
  header: "Complexity"
  options:
    - label: "Simple"
    - label: "Standard (Recommended)"
    - label: "Advanced"
```

---

## Routing

| Pattern | Route | Details |
|---------|-------|---------|
| `init\|new.*project\|새.*프로젝트` | PROJECT_INIT | `Read("references/route-project-init.md")` |
| `skill.*create\|스킬.*만들` | SKILL | `Read("references/route-skill.md")` |
| `convert\|from.*code\|변환` | SKILL_FROM_CODE | `Read("references/route-skill.md")` |
| `agent\|에이전트\|subagent` | AGENT | `Read("references/route-agent-command.md")` |
| `command\|workflow\|명령어` | COMMAND | `Read("references/route-agent-command.md")` |
| `analyze\|분석\|리뷰\|review` | ANALYZE | `Read("references/route-analyze.md")` |
| `validate\|check\|검증` | VALIDATE | `Read("references/route-validate.md")` |
| `publish\|deploy\|배포` | PUBLISH | `Read("references/route-publish.md")` |
| `register\|local\|등록` | LOCAL_REGISTER | `Read("references/route-publish.md")` |
| `llm\|sdk\|직접.*호출\|background.*agent` | LLM_INTEGRATION | `Read("references/route-llm-integration.md")` + `Skill("skillmaker:llm-sdk-guide")` |
| `hook.*design\|훅.*설계\|적절한.*hook` | HOOK_DESIGN | `Read("references/route-hook-design.md")` |
| no match | MENU | Show menu below |

---

## MENU

```yaml
AskUserQuestion:
  question: "What would you like to do?"
  header: "Action"
  options:
    - label: "New Project"
      description: "Initialize new plugin/marketplace"
    - label: "Skill"
      description: "Create new skill"
    - label: "Agent"
      description: "Create subagent with skills"
    - label: "Command"
      description: "Create workflow command"
    - label: "Hook Design"
      description: "Design hook with proper skill selection"
    - label: "LLM Integration"
      description: "Direct LLM calls from hooks/agents"
    - label: "Analyze"
      description: "Validation + design principles"
    - label: "Validate"
      description: "Quick schema/path check"
    - label: "Publish"
      description: "Deploy to marketplace"
```

Route selection to corresponding reference file.

---

## Common Post-Action Steps

After any creation (SKILL, AGENT, COMMAND):

### Validation (MANDATORY)
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_all.py --json
```

- **status="fail"**: Show errors, ask for auto-fix
- **status="warn"**: Show warnings, allow proceed
- **status="pass"**: Continue to next steps

### Next Steps Template
```markdown
1. **로컬 등록**: `/wizard register`
2. **테스트**: Claude Code 재시작 → 기능 테스트
3. **배포**: `/wizard publish`
```

---

## References

Each route has detailed instructions:

| Route | Reference |
|-------|-----------|
| PROJECT_INIT | [route-project-init.md](references/route-project-init.md) |
| SKILL, SKILL_FROM_CODE | [route-skill.md](references/route-skill.md) |
| AGENT, COMMAND | [route-agent-command.md](references/route-agent-command.md) |
| ANALYZE | [route-analyze.md](references/route-analyze.md) |
| VALIDATE | [route-validate.md](references/route-validate.md) |
| PUBLISH, LOCAL_REGISTER | [route-publish.md](references/route-publish.md) |
| LLM_INTEGRATION | [route-llm-integration.md](references/route-llm-integration.md) |
| HOOK_DESIGN | [route-hook-design.md](references/route-hook-design.md) |
