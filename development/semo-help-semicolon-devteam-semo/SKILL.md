---
name: semo-help
description: |
  SEMO 도움말 및 Semicolon 팀 컨텍스트 응답 (공통 Skill). Use when (1) /SEMO:help 커맨드,
  (2) "도움말", "SEMO란", "어떻게 해" 키워드, (3) SEMO 사용법 질문.
tools: [Read, Bash, WebFetch]
model: inherit
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: semo-help 호출 - {질문 카테고리}` 시스템 메시지를 첫 줄에 출력하세요.

# semo-help Skill

> SEMO 사용법 및 Semicolon 팀 컨텍스트 응답 (SEMO 공통 Skill)

## Purpose

모든 SEMO 패키지에서 공통으로 사용하는 도움말 Skill입니다.

### 지원 질문 카테고리

| 카테고리 | 예시 질문 | 참조 소스 |
|----------|-----------|-----------|
| **SEMO 기본** | "SEMO란?", "SEMO 어떻게 사용해?" | semo-core/PRINCIPLES.md |
| **패키지 정보** | "설치된 패키지 뭐야?", "버전 확인" | .claude/semo-*/VERSION |
| **명령어 안내** | "/SEMO:* 명령어 뭐있어?" | semo-core/commands/ |
| **팀 컨텍스트** | "Semicolon 팀 규칙", "docs 위키" | docs 레포, TEAM_RULES.md |

## Reference Chain

```text
semo-help
├── semo-core/PRINCIPLES.md (SEMO 핵심 원칙)
├── semo-core/MESSAGE_RULES.md (메시지 포맷 규칙)
├── semo-core/TEAM_RULES.md (Semicolon 팀 규칙)
├── .claude/semo-*/VERSION (설치된 패키지 버전)
├── .claude/semo-*/CLAUDE.md (패키지별 설명)
└── docs 레포 Wiki (팀 문서)
```

## Workflow

### Step 1: 질문 분류

사용자 질문을 카테고리로 분류합니다:

```text
질문 분석
├─ SEMO 사용법 → semo-core 문서 참조
├─ 패키지 정보 → .claude/ 디렉토리 스캔
├─ 명령어 안내 → commands/ 디렉토리 분석
└─ 팀 컨텍스트 → TEAM_RULES.md, docs 레포
```

### Step 2: 정보 수집

**SEMO 문서 조회**:

```bash
# SEMO 핵심 원칙
cat semo-core/PRINCIPLES.md

# 메시지 규칙
cat semo-core/MESSAGE_RULES.md

# 팀 규칙
cat semo-core/TEAM_RULES.md
```

**패키지 정보 조회**:

```bash
# 설치된 패키지 목록 및 버전
for dir in .claude/semo-*/; do
  name=$(basename "$dir")
  version=$(cat "$dir/VERSION" 2>/dev/null || echo "unknown")
  echo "$name: $version"
done
```

**docs 레포 Wiki 조회**:

```bash
# docs 레포 위키 접근
gh api repos/semicolon-devteam/docs/contents/wiki
```

### Step 3: 응답 제공

```markdown
[SEMO] Skill: semo-help 응답

## {질문 카테고리}

{관련 정보 및 안내}

---
📚 상세 정보: [관련 문서 링크]
```

## Quick Reference

### 공통 명령어 (/SEMO:*)

| 명령어 | 설명 | 호출 스킬 |
|--------|------|-----------|
| `/SEMO:help` | 도움말 (현재) | semo-help |
| `/SEMO:slack` | Slack 메시지 전송 | notify-slack |
| `/SEMO:update` | SEMO 업데이트 | version-updater |
| `/SEMO:feedback` | 피드백 제출 | feedback |

### 패키지별 특화 기능

| 패키지 | 설명 | 주요 Agent/Skill |
|--------|------|------------------|
| semo-core | 공통 컴포넌트 | compliance-checker, notify-slack |
| semo-meta | SEMO 개발/관리 | semo-architect, version-manager |
| semo-pm | PM 워크플로우 | pm-agent, assign-task |
| semo-po | PO 워크플로우 | issue-planner, complexity-scorer |
| semo-next | Next.js 개발 | next-guide, next-refactorer |
| semo-qa | QA 워크플로우 | qa-agent, test-creator |

## Expected Output

### SEMO 소개 질문

```markdown
[SEMO] Skill: semo-help 응답

## SEMO (Semicolon AI Transformation)

SEMO는 Semicolon 팀의 Claude Code 확장 프레임워크입니다.

### 핵심 기능
- **Agent**: 복잡한 워크플로우 자동화
- **Skill**: 재사용 가능한 기능 모듈
- **Command**: 빠른 실행을 위한 슬래시 명령어

### 공통 명령어
| 명령어 | 설명 |
|--------|------|
| `/SEMO:help` | 도움말 (현재) |
| `/SEMO:slack` | Slack 메시지 전송 |
| `/SEMO:update` | SEMO 업데이트 |
| `/SEMO:feedback` | 피드백 제출 |

---
📚 상세 정보: semo-core/PRINCIPLES.md
```

### 패키지 정보 질문

```markdown
[SEMO] Skill: semo-help 응답

## 설치된 SEMO 패키지

| 패키지 | 버전 | 설명 |
|--------|------|------|
| semo-core | 0.10.0 | 공통 컴포넌트 |
| semo-meta | 0.35.0 | SEMO 패키지 관리 |

### 사용 가능한 Agent/Skill
- Agents: orchestrator, semo-architect, ...
- Skills: notify-slack, version-updater, ...

---
📚 상세 정보: 각 패키지 CLAUDE.md 참조
```

### 팀 규칙 질문

```markdown
[SEMO] Skill: semo-help 응답

## Semicolon 팀 규칙

### 기본 설정
- **응답 언어**: 한글
- **기본 Organization**: semicolon-devteam
- **이슈 템플릿**: .github/ISSUE_TEMPLATE 기반

### 참고 문서
- docs 위키: https://github.com/semicolon-devteam/docs/wiki
- 팀 규칙: semo-core/TEAM_RULES.md

---
📚 상세 정보: TEAM_RULES.md
```

## SEMO Message Format

```markdown
[SEMO] Skill: semo-help 호출 - {질문 카테고리}

[SEMO] Skill: semo-help 응답
```

## References

- [docs-integration](references/docs-integration.md) - docs 레포 연동 가이드
- [package-info](references/package-info.md) - 패키지 정보 조회
- [team-context](references/team-context.md) - 팀 컨텍스트 설정
