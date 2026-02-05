---
name: project-kickoff
description: Interactive project creation from cm-template. Use when (1) user requests new service creation, (2) creating new cm-* project, (3) need guided wizard for project configuration, (4) generating ready-to-copy project in implement-dist/.
tools: [Bash, Read, Write, Edit]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: project-kickoff 호출 - {프로젝트명}` 시스템 메시지를 첫 줄에 출력하세요.

# Project Kickoff Skill

**Purpose**: Interactive wizard for creating new Semicolon community services from cm-template

## Activation Triggers

This skill is invoked when users say:

- `cm-{name} 프로젝트 만들어줘`
- `새 커뮤니티 서비스 만들어줘`
- `{name} 서비스 생성해줘`
- `프로젝트 킥오프 해줘`

## Quick Start

### 1. Gather Configuration (Interactive)

Collect required information sequentially:

| Step | Input | Format |
|------|-------|--------|
| 1️⃣ Project Name | `my-school-community` | kebab-case |
| 2️⃣ Supabase ID | `wloqfachtbxceqikzosi` | alphanumeric |
| 3️⃣ ANON_KEY | `eyJ...` | JWT token |
| 4️⃣ SERVICE_ROLE (optional) | `eyJ...` or `skip` | JWT token |
| 5️⃣ Description (optional) | text or `skip` | string |

### 2. Confirm & Generate

```bash
# Run generation script
./scripts/create-service.sh {project_name} {supabase_project_id} implement-dist/{project_name}

# Update .env.local with actual keys
sed -i '' "s/your-anon-key-here/{anon_key}/" implement-dist/{project_name}/.env.local
```

### 3. Output Location

```text
implement-dist/{project_name}/
├── src/              # 소스 코드
├── .claude/          # Claude 에이전트/스킬
├── CLAUDE.md         # AI 가이드 (커스터마이즈됨)
├── .env.local        # 환경 변수 (키 설정됨)
└── package.json      # 의존성 (이름 변경됨)
```

## Next Steps After Generation

```bash
# 1. Copy to workspace
cp -r implement-dist/{project_name} ~/your-workspace/{project_name}

# 2. Install dependencies
cd ~/your-workspace/{project_name} && npm install

# 3. Start dev server
npm run dev

# 4. Connect GitHub
git remote add origin https://github.com/semicolon-devteam/{project_name}.git
```

## Validation Rules

| Field | Validation |
|-------|------------|
| Project Name | kebab-case, 3+ chars, no `--` |
| Supabase ID | alphanumeric, 15-25 chars |
| ANON_KEY | starts with `eyJ`, 100+ chars |

## Dependencies

- `scripts/create-service.sh` - Core generation script
- `templates/CLAUDE.template.md` - CLAUDE.md template
- `templates/README.template.md` - README.md template

## Related Skills

- `scaffold-domain` - Creates domain structure within a project
- `fetch-team-context` - Provides team standards context

## References

For detailed documentation, see:

- [Interactive Wizard](references/interactive-wizard.md) - Full wizard flow, example interaction
- [Generation Process](references/generation-process.md) - Script execution, output structure
- [Validation & Errors](references/validation-errors.md) - Schema, validation rules, error messages
