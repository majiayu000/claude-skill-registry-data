---
name: project-guide
description: claude-plugin 프로젝트 개발 가이드라인, 레퍼런스 패턴, 프로젝트 구조 조회. Use when Claude needs to (1) Look up development principles (P1-P4, DRY, KISS, YAGNI, SOLID), (2) Find reference patterns for Hooks/Agents/Commands creation, (3) Understand project structure and file locations, (4) Learn how to create Skills/Hooks/Agents/Commands, or (5) Delegate to claude-code-guide for official Claude Code documentation
---

# Project Guide: claude-plugin 프로젝트 개발 도우미

## 핵심 지침

### 1. 프로젝트 문서 우선 원칙

**항상 다음 순서로 조회:**

```
1. /docs/guidelines/        # 개발 원칙 (development.md, tool-creation.md, documentation.md)
2. /docs/references/        # 레퍼런스 패턴 (hooks, agents, commands, plugins)₩
3. CLAUDE.md, README.md     # 프로젝트 개요 및 구조
4. claude-code-guide        # 공식 Claude Code 문서 (위임)
```

### 2. 주요 문서 경로

- **Guidelines**: `docs/guidelines/*.md`
- **References**: `docs/references/{hooks,agents,commands,plugins}/*.md`
- **Templates**: `templates/`

### 3. claude-code-guide 위임 기준

**다음 경우 반드시 위임:**

1. **Claude Code 작동 원리** 질문
   - "Skill은 어떻게 자동 활성화되나요?"
   - "Hook 이벤트는 언제 발생하나요?"

2. **공식 API/Tool 문서** 질문
   - "WebSearch 도구 사용법은?"
   - "Task 도구 파라미터는?"

3. **Agent SDK** 관련 질문
   - "Claude Agent SDK 구조는?"
   - "서브에이전트 생성 방법은?"

**위임 방법:**

```
Task tool 사용:
- subagent_type: claude-code-guide
- description: "Claude Code 공식 문서 조회"
- prompt: "{사용자 질문 원문}"
```

### 4. 답변 형식

**핵심 요약 + 파일:줄번호 참조**

예시:
```
DRY 원칙(P3): 3번 반복 시 중복 제거
상세: docs/guidelines/development.md:69-84
```

---

## 제약 조건

- **허용 도구**: Read, Grep, Glob, Task (claude-code-guide 위임용)
- **금지 도구**: Write, Edit
- **답변 형식**: 핵심 요약 + 파일 경로 제공 (전체 문서 복사 금지)

---

## 프로젝트 문서 위치

**개발 가이드라인:**
- Development principles: `/docs/guidelines/development.md`
- Tool creation guide: `/docs/guidelines/tool-creation.md`
- Documentation guide: `/docs/guidelines/documentation.md`

**레퍼런스:**
- Quick reference table: `/docs/references/README.md`
- Hooks patterns: `/docs/references/hooks/`
- Agents patterns: `/docs/references/agents/`
- Commands patterns: `/docs/references/commands/`

**템플릿:**
- Skills, Hooks, Agents, Commands: `/docs/templates/`
