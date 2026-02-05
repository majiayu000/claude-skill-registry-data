---
name: create-decision-log
description: |
  의사결정 로그 Discussion 생성. 회의/Slack/PR 등에서 결정된 사항을 command-center에 기록.
  Use when (1) 의사결정 기록 요청, (2) 회의 결정사항 문서화, (3) summarize-meeting 스킬에서 호출.
tools: [Bash, Read, AskUserQuestion]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: create-decision-log 호출` 메시지를 첫 줄에 출력하세요.

# create-decision-log Skill

> 팀의 중요한 의사결정을 GitHub Discussion으로 문서화

## Purpose

회의, Slack, GitHub 등 모든 채널에서 발생한 의사결정을 `command-center` 레포지토리의 Discussion으로 투명하게 기록합니다.

## Input

### 필수 파라미터

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `title` | string | 결정 내용 요약 (날짜 자동 추가됨) |
| `category` | enum | 의사결정 분류 (아래 참조) |
| `source` | enum | 결정 출처 (아래 참조) |
| `context` | string | 의사결정 배경 |
| `decision` | string | 의사결정 내용 |
| `participants` | string[] | 참여자 목록 |

### 선택 파라미터

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `notes` | string | 추가 메모 |
| `related_issue` | string | 관련 이슈/PR 번호 |

### Enum 값

**category**:
- `기술/아키텍처`
- `제품/기획`
- `운영/프로세스`
- `인사/조직`
- `비즈니스/전략`

**source**:
- `정기 회의`
- `긴급 회의`
- `Slack 논의`
- `GitHub Discussion`
- `GitHub Issue/PR`
- `1:1 논의`

## Workflow

```text
의사결정 정보 수신
    ↓
1. 필수 정보 검증
    ↓
2. Discussion 본문 생성 (템플릿 기반)
    ↓
3. gh discussion create 실행
    ↓
4. 생성된 Discussion URL 반환
```

## Execution

### Step 1: Discussion 생성

```bash
# 본문 파일 생성
cat > /tmp/decision-log-body.md << 'EOF'
## 🏷️ 의사결정 분류
{category}

## 📍 결정 출처
{source}

## 👥 참여자
{participants}

## 🔍 의사결정 배경
{context}

## ✅ 의사결정 내용
{decision}

## 📎 추가 메모
{notes}
EOF

# Discussion 생성
gh discussion create \
  --repo semicolon-devteam/command-center \
  --category "Decision-Log" \
  --title "[$(date +%Y-%m-%d)] {title}" \
  --body-file /tmp/decision-log-body.md
```

## Output

### 성공

```markdown
[SEMO] Skill: create-decision-log 완료

✅ 의사결정 로그 생성 완료

| 항목 | 내용 |
|------|------|
| 제목 | [2025-01-15] API 버전 관리 전략 결정 |
| 분류 | 기술/아키텍처 |
| 출처 | 정기 회의 |
| Discussion | https://github.com/semicolon-devteam/command-center/discussions/XXX |
```

### 실패

```markdown
[SEMO] Skill: create-decision-log 실패

❌ Discussion 생성 실패

**원인**: {error_message}
**해결**: Discussion 카테고리 'Decision-Log' 존재 여부 확인
```

## Quick Start

### 단일 의사결정

```yaml
title: "GraphQL 도입 결정"
category: "기술/아키텍처"
source: "정기 회의"
participants: ["@reus-jeon", "@garden92", "@kyago"]
context: |
  - 문제: REST API N+1 쿼리 문제
  - 필요성: 클라이언트 유연성 향상
decision: |
  - GraphQL을 새로운 API 표준으로 채택
  - Apollo Server 사용
  - 기존 REST API는 3개월 내 점진적 마이그레이션
```

## Related

- [summarize-meeting](../summarize-meeting/SKILL.md) - 회의록 정리 (이 스킬 호출)
- [notify-slack](../../../../semo-skills/notify-slack/SKILL.md) - Slack 알림
