---
name: create-decision-log
description: |
  의사결정 로그 Supabase discussions 테이블에 생성.
  회의/Slack/PR 등에서 결정된 사항을 기록.
  Use when (1) 의사결정 기록 요청, (2) 회의 결정사항 문서화, (3) summarize-meeting 스킬에서 호출.
tools: [Supabase, Bash, Read, AskUserQuestion]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: create-decision-log 호출` 메시지를 첫 줄에 출력하세요.

# create-decision-log Skill

> 팀의 중요한 의사결정을 Supabase discussions 테이블에 문서화

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Discussions | GraphQL API |
| **v2.0** | **Supabase** | `discussions` 테이블 INSERT |

---

## Purpose

회의, Slack, GitHub 등 모든 채널에서 발생한 의사결정을 **Supabase discussions 테이블 (category: 'decision-log')**에 투명하게 기록합니다.

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
3. Supabase discussions 테이블에 INSERT
    ↓
4. 생성된 Discussion ID 반환
```

## Execution

### Supabase로 저장

```sql
-- 의사결정 로그 생성
INSERT INTO discussions (office_id, category, title, body, created_by)
VALUES (
  '{office_uuid}',
  'decision-log',
  '[2025-01-15] API 버전 관리 전략 결정',
  E'## 🏷️ 의사결정 분류\n기술/아키텍처\n\n## 📍 결정 출처\n정기 회의\n\n## 👥 참여자\n@reus-jeon, @garden92, @kyago\n\n## 🔍 의사결정 배경\n{배경}\n\n## ✅ 의사결정 내용\n{결정 내용}\n\n## 📎 추가 메모\n{메모}',
  '{creator_uuid}'
)
RETURNING id, title;
```

```typescript
// Supabase 클라이언트
const { data, error } = await supabase
  .from('discussions')
  .insert({
    office_id: officeId,
    category: 'decision-log',
    title: `[${date}] ${title}`,
    body: decisionBody,
    created_by: creatorId
  })
  .select('id, title')
  .single();
```

### 본문 템플릿

```markdown
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
| Supabase ID | {discussion_uuid} |
```

### 실패

```markdown
[SEMO] Skill: create-decision-log 실패

❌ Discussion 생성 실패

**원인**: {error_message}
**해결**: Supabase 연결 및 권한 확인
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

## GitHub Discussion Fallback

Supabase 연결이 불가능한 경우:

```bash
# Fallback: GitHub Discussion API
gh discussion create \
  --repo semicolon-devteam/command-center \
  --category "Decision-Log" \
  --title "[$(date +%Y-%m-%d)] {title}" \
  --body-file /tmp/decision-log-body.md
```

## References

- [discussions 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)

## Related

- [summarize-meeting](../summarize-meeting/SKILL.md) - 회의록 정리 (이 스킬 호출)
- [create-meeting-minutes](../create-meeting-minutes/SKILL.md) - 정기 회의록 생성
- [notify-slack](../notify-slack/SKILL.md) - Slack 알림
