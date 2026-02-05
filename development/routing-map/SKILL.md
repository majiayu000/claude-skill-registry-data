---
name: routing-map
description: |
  SEMO 라우팅 구조 시각화. Use when (1) /SEMO:routing-map 커맨드,
  (2) "라우팅 구조", "SEMO 구조", "설치된 패키지" 키워드,
  (3) Agent/Skill 전체 목록 확인 요청.
tools: [Bash, Read, Glob, Grep]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: routing-map 호출` 시스템 메시지를 첫 줄에 출력하세요.

# routing-map Skill

> SEMO 설치 현황 및 라우팅 구조 시각화

## Purpose

현재 프로젝트에 설치된 SEMO 구성 요소(Core, Packages)와 전체 라우팅 경로를 시각적으로 표시합니다.

## Workflow

### Phase 1: 버전 정보 수집

```bash
# 1. semo-system 존재 여부 (Meta 설치 여부)
if [ -d "semo-system" ] && [ ! -L "semo-system" ]; then
  echo "META_INSTALLED=true"
else
  echo "META_INSTALLED=false"
fi

# 2. 버전 파일 스캔
find . -path "./node_modules" -prune -o -name "VERSION" -print 2>/dev/null | \
  grep -E "(semo-core|semo-skills|packages)" | \
  while read f; do
    pkg=$(echo "$f" | sed 's|^\./||' | sed 's|/VERSION||')
    ver=$(cat "$f" 2>/dev/null)
    echo "$pkg|$ver"
  done
```

### Phase 2: Orchestrator 분석

```bash
# Orchestrator 파일 목록
find . -path "./node_modules" -prune -o \
  -name "orchestrator.md" -print 2>/dev/null | \
  grep -v node_modules
```

### Phase 3: Agent/Skill 수집

```bash
# Agent 목록 (.md 파일 기준)
find .claude/agents -name "*.md" 2>/dev/null | \
  xargs -I {} basename {} .md

# Skill 목록
find .claude/skills -name "SKILL.md" 2>/dev/null | \
  xargs -I {} dirname {} | xargs -I {} basename {}
```

### Phase 4: 라우팅 테이블 추출

각 Orchestrator의 Quick Routing Table 섹션에서 라우팅 정보 추출:

```bash
# Routing Table 추출 (각 orchestrator.md에서)
grep -A 50 "Quick Routing Table" {orchestrator_path} | \
  grep "^\|" | head -20
```

## Output Format

### 1. 버전 정보 섹션

```markdown
[SEMO] Skill: routing-map 호출

## SEMO 설치 현황

**환경**: Meta 설치됨 | 패키지만 설치됨
**스캔 일시**: {timestamp}

### Core Components

| 구성 요소 | 버전 | 상태 |
|----------|------|------|
| semo-core | 1.2.0 | ✅ |
| semo-skills | 1.3.0 | ✅ |

### Installed Packages

| 패키지 | 버전 | 설명 |
|--------|------|------|
| packages/core | 0.32.0 | Core Skills |
| packages/eng/nextjs | 1.1.0 | Next.js 개발 |
| packages/biz/discovery | 1.0.0 | 기획/발견 |
| packages/ops/qa | 0.x.x | QA 워크플로우 |

> ⚠️ 버전 정보가 없는 패키지는 `VERSION` 파일 추가를 권장합니다.
```

### 2. 라우팅 구조 섹션

```markdown
## Routing Structure

\`\`\`
CLAUDE.md (Entry Point)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator                           │
│  semo-core/agents/orchestrator/orchestrator.md             │
└─────────────────────────────────────────────────────────────┘
    │
    ├── [코드 작성] ──────────► skill:coder
    ├── [테스트] ────────────► skill:tester
    ├── [계획/설계] ─────────► skill:planner
    ├── [배포] ──────────────► skill:deployer
    ├── [슬랙 알림] ─────────► skill:notify-slack
    ├── [피드백] ────────────► skill:feedback
    ├── [버전 확인] ─────────► skill:version-updater
    ├── [도움말] ────────────► skill:semo-help
    ├── [메모리] ────────────► skill:memory
    ├── [버그 목록] ─────────► skill:list-bugs
    ├── [아키텍처] ──────────► skill:semo-architecture-checker
    └── [오류 반복] ─────────► skill:circuit-breaker (자동)
\`\`\`
```

### 3. 패키지별 확장 Orchestrator

```markdown
## Package-Specific Orchestrators

### eng/nextjs (Next.js 개발)

\`\`\`
packages/eng/nextjs/agents/orchestrator
    │
    ├── [이슈 작업] ─────────► advisor
    ├── [이슈 상태] ─────────► skill:project-board
    ├── [Git 커밋/푸시] ─────► skill:git-workflow
    ├── [기능 명세] ─────────► spec-master
    ├── [코드 구현] ─────────► implementation-master
    ├── [UI 디자인] ─────────► skill:frontend-design
    ├── [태스크 리뷰] ───────► skill:review-task
    ├── [테스트 요청] ───────► skill:change-to-testing
    └── [빠른 수정] ─────────► skill:fast-track
\`\`\`

### ops/qa (QA 워크플로우)

\`\`\`
packages/ops/qa/agents/orchestrator
    │
    ├── [테스트중 변경] ─────► skill:change-to-testing
    ├── [테스트 대기열] ─────► skill:test-queue
    ├── [테스트 실행] ───────► qa-master
    ├── [테스트 통과/실패] ──► skill:report-test-result
    └── [프로덕션 가능] ─────► skill:production-gate
\`\`\`
```

### 4. 전체 Agent/Skill 목록

```markdown
## Available Components

### Agents ({count}개)

| Agent | 패키지 | 설명 |
|-------|--------|------|
| orchestrator | core | Primary Router |
| advisor | eng/nextjs | 전략적 조언 |
| teacher | eng/nextjs | 기술 교육 |
| spec-master | eng/nextjs | SDD 명세 |
| implementation-master | eng/nextjs | 코드 구현 |
| quality-master | eng/nextjs | 품질 검증 |
| semicolon-reviewer | eng/nextjs | 코드 리뷰 |
| qa-master | ops/qa | QA 통합 관리 |

### Skills ({count}개)

| Skill | 패키지 | Trigger Keywords |
|-------|--------|-----------------|
| coder | core | 코드 작성, 구현 |
| tester | core | 테스트, 커버리지 |
| planner | core | 계획, 설계 |
| deployer | core | 배포, deploy |
| notify-slack | core | 슬랙, 알림 |
| feedback | core | 피드백, 이슈 |
| memory | core | 기억, 저장 |
| version-updater | core | 버전, 업데이트 |
| semo-help | core | 도움말, 사용법 |
| routing-map | core | 라우팅 구조 |
| git-workflow | eng/nextjs | 커밋, 푸시, PR |
| project-board | eng/nextjs | 상태 변경 |
| review-task | eng/nextjs | 리뷰해줘 |
| change-to-testing | ops/qa | 테스트 요청 |

### Commands ({count}개)

| 명령어 | 설명 |
|--------|------|
| `/SEMO:help` | 도움말 |
| `/SEMO:feedback` | 피드백 제출 |
| `/SEMO:update` | SEMO 업데이트 |
| `/SEMO:onboarding` | 온보딩 가이드 |
| `/SEMO:dry-run` | 라우팅 시뮬레이션 |
| `/SEMO:routing-map` | 라우팅 구조 (현재) |
```

## Error Handling

### 버전 파일 없음

```markdown
⚠️ **버전 정보 누락**

다음 패키지에 VERSION 파일이 없습니다:
- packages/xxx

`semo version-updater`로 버전 파일을 생성하세요.
```

### Meta 미설치 환경

```markdown
ℹ️ **패키지 전용 환경**

semo-system이 심볼릭 링크로 연결되어 있습니다.
SEMO 소스 수정은 Meta 환경에서만 가능합니다.
```

## SEMO Message Format

```markdown
[SEMO] Skill: routing-map 호출

[SEMO] Skill: routing-map 완료 - {agent_count}개 Agent, {skill_count}개 Skill 발견
```

## References

- [Package Scanner](references/package-scanner.md) - 패키지 스캔 로직
- [Routing Extractor](references/routing-extractor.md) - 라우팅 테이블 추출
