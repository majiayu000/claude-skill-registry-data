---
name: fetch-team-context
description: Fetch Semicolon team standards from docs wiki. Use when (1) providing workflow or process advice, (2) recommending DevOps strategies, (3) referencing team conventions for decision-making, (4) checking team standards compliance.
tools: [Bash, Read, GitHub CLI]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: fetch-team-context 호출 - {토픽}` 시스템 메시지를 첫 줄에 출력하세요.

# Fetch Team Context Skill

**Purpose**: Retrieve Semicolon team standards, processes, and conventions from docs wiki for informed decision-making

## When to Use

Agents should invoke this skill when:

- Providing workflow or process advice
- Recommending DevOps strategies
- Checking team conventions before suggesting changes
- Validating recommendations against team standards

## Quick Start

### 1. Identify Required Context

| Topic | Wiki Page |
|-------|-----------|
| Git & Commits | Team Codex |
| Workflow | Collaboration Process |
| Architecture | Development Philosophy |
| Estimation | Estimation Guide |

### 2. Fetch via GitHub API

```bash
# List all wiki pages
gh api repos/semicolon-devteam/docs/contents | jq '.[].name'

# Web fetch fallback
web_fetch({ url: "https://github.com/semicolon-devteam/docs/wiki/Team-Codex" });
```

### 3. Extract Key Information

Parse fetched content for:
- **Rules**: MUST, SHOULD, MUST NOT patterns
- **Conventions**: Naming, formatting, structure
- **Processes**: Step-by-step workflows
- **Examples**: Code snippets, command examples

## Usage

```javascript
// Fetch specific context
skill: fetchTeamContext({ topic: "git-commits" });

// Fetch multiple contexts
skill: fetchTeamContext({ topics: ["workflow", "code-quality"] });
```

## Critical Rules

1. **docs wiki is Source of Truth**: Always prefer wiki over cached data
2. **Explicit Over Implicit**: If wiki doesn't specify, don't assume
3. **Version Awareness**: Note if wiki content seems outdated
4. **Fallback Gracefully**: Use quick reference if wiki unavailable
5. **Attribution**: Always cite source URL in responses
6. **문서 유효성 검증 필수**: 404 응답이면 반드시 사용자에게 알림

## Dependencies

- `gh api` - GitHub API access
- `web_fetch` - Web content retrieval (fallback)
- docs wiki - Source of truth

## Related Skills

- `check-team-codex` - Uses this for code quality rules
- `create-issues` - Uses this for issue conventions
- `implement` - Uses this for development workflow

## References

For detailed documentation, see:

- [Wiki Pages](references/wiki-pages.md) - Topic mapping, fetch methods, validation
- [Quick Reference](references/quick-reference.md) - Git conventions, workflow, quality gates
