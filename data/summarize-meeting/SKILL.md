---
name: summarize-meeting
description: |
  회의 녹취록을 분석하여 Supabase discussions 테이블에 회의록/의사결정 로그 생성.
  Use when (1) 회의 녹취록 요약 요청, (2) /summarize-meeting 커맨드,
  (3) 의사결정 사항 정리 요청, (4) Action Items 추출 요청.
tools: [Supabase, Bash, Read, Write]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: summarize-meeting 호출 - {회의명}` 시스템 메시지를 첫 줄에 출력하세요.

# summarize-meeting Skill

> 회의 녹취록 → Supabase discussions 테이블 (회의록/의사결정 로그) 자동 생성

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Discussions | GraphQL API |
| **v2.0** | **Supabase** | `discussions` 테이블 INSERT |

---

## Purpose

회의 녹취록 텍스트를 분석하여 구조화된 회의록과 의사결정 로그를 **Supabase discussions 테이블**에 저장합니다.

## 🔴 NON-NEGOTIABLE RULES

### 출력 위치

| 유형 | discussions.category | 설명 |
|------|----------------------|------|
| 회의록 | `meeting-minutes` | 회의 전체 내용 정리 |
| 의사결정 로그 | `decision-log` | 결정사항 별도 문서화 |

**로컬 파일 생성 금지** - 반드시 Supabase discussions 테이블에 저장

### 필수 생성물 (Dual Output)

> **모든 회의에 대해 반드시 회의록과 의사결정 로그를 모두 생성해야 합니다.**

| 생성물 | 필수 여부 | 설명 |
|--------|----------|------|
| 회의록 | **필수** | 회의 전체 내용 정리 |
| 의사결정 로그 | **필수** | 결정사항 별도 문서화 (결정이 없어도 "결정사항 없음" 명시) |

## Execution Flow

```text
1. 녹취록 파일 읽기 또는 텍스트 입력 받기
   ↓
2. 회의 내용 분석
   - 참석자 식별
   - 안건별 논의 내용 정리
   - 의사결정 사항 추출
   - Action Items 추출
   ↓
3. Supabase discussions 테이블에 INSERT
   - category: 'meeting-minutes' → 회의록
   - category: 'decision-log' → 주요 의사결정
   ↓
4. Slack 알림 전송 (#개발사업팀)
```

## Supabase 저장

### 회의록 저장

```sql
-- 회의록 생성
INSERT INTO discussions (office_id, category, title, body, created_by)
VALUES (
  '{office_uuid}',
  'meeting-minutes',
  '[{날짜}] 정기 회고 & 회의',
  E'# 정기 회의록\n\n> **일시**: {날짜} {시간}\n> **참석자**: {참석자}\n\n---\n\n## 📋 안건\n\n### 1. {안건1}\n\n**논의 내용**:\n- ...\n\n---\n\n## ✅ Action Items\n\n| 담당자 | 할 일 | 기한 |\n|--------|-------|------|\n| @담당자 | 할 일 | 기한 |',
  '{creator_uuid}'
)
RETURNING id, title;
```

```typescript
// Supabase 클라이언트
const { data: meetingMinutes, error } = await supabase
  .from('discussions')
  .insert({
    office_id: officeId,
    category: 'meeting-minutes',
    title: `[${date}] 정기 회고 & 회의`,
    body: meetingBody,
    created_by: creatorId
  })
  .select()
  .single();
```

### 의사결정 로그 저장

```sql
-- 의사결정 로그 생성
INSERT INTO discussions (office_id, category, title, body, created_by)
VALUES (
  '{office_uuid}',
  'decision-log',
  '[{날짜}] {의사결정 제목}',
  E'# {의사결정 제목}\n\n> **결정일**: {날짜}\n> **결정자**: {참여자}\n\n---\n\n## 📋 배경\n\n{배경}\n\n## 🎯 결정 사항\n\n{결정 내용}',
  '{creator_uuid}'
)
RETURNING id, title;
```

```typescript
// Supabase 클라이언트
const { data: decisionLog, error } = await supabase
  .from('discussions')
  .insert({
    office_id: officeId,
    category: 'decision-log',
    title: `[${date}] ${decisionTitle}`,
    body: decisionBody,
    created_by: creatorId
  })
  .select()
  .single();
```

## 템플릿

### 회의록 템플릿

```markdown
# {회의명} 회의록

> **일시**: {날짜} {시간}
> **참석자**: {참석자 목록}
> **장소/방식**: {장소 또는 온라인}

---

## 📋 안건

### 1. {안건1 제목}

**논의 내용**:
- {논의 사항 1}
- {논의 사항 2}

**결론**: {결론 또는 다음 단계}

---

## ✅ Action Items

| 담당자 | 할 일 | 기한 |
|--------|-------|------|
| @{담당자1} | {할 일 내용} | {기한} |

---

## 🔗 관련 의사결정

- {의사결정 제목}
```

### 의사결정 로그 템플릿

```markdown
# {의사결정 제목}

> **결정일**: {날짜}
> **결정자**: {결정 참여자}

---

## 📋 배경

{의사결정이 필요했던 배경 설명}

## 🎯 결정 사항

{최종 결정 내용}

## 📊 검토된 대안

| 대안 | 장점 | 단점 | 선택 |
|------|------|------|------|
| {대안1} | {장점} | {단점} | ❌ |
| {대안2} | {장점} | {단점} | ✅ |
```

## Slack 알림

### 대상 채널

| 채널 | 용도 |
|------|------|
| #개발사업팀 | 회의록/의사결정 알림 |

### 알림 형식

```markdown
📝 회의록 생성 완료

**회의**: {회의명}
**일시**: {날짜}

**생성된 문서**:
- 회의록: #{meeting_id}
- 의사결정: #{decision_id} (있는 경우)

**Action Items**: {N}개
```

## Output

```markdown
[SEMO] Skill: summarize-meeting 완료

✅ 회의록 생성 완료

**회의**: {회의명}
**Supabase discussions**:
- 회의록: #{meeting_id} (category: meeting-minutes)
- 의사결정: #{decision_id} (category: decision-log)

**Slack 알림**: #개발사업팀 전송 완료
```

## GitHub Discussion Fallback

Supabase 연결이 불가능한 경우 GitHub Discussion으로 폴백:

```bash
# Fallback: GitHub Discussion API
gh api graphql -f query='
mutation($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {
    repositoryId: $repoId
    categoryId: $categoryId
    title: $title
    body: $body
  }) {
    discussion {
      number
      url
    }
  }
}' \
  -f repoId="R_kgDOOdzh9w" \
  -f categoryId="DIC_kwDOOdzh984Cw9Lp" \
  -f title="[회의록] {날짜} - {회의명}" \
  -f body="$MEETING_BODY"
```

## References

- [discussions 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [Meeting Template](references/meeting-template.md)
- [Decision Template](references/decision-template.md)

## Related

- `notify-slack` - Slack 알림 전송
- `create-meeting-minutes` - 정기 회의록 생성
- `create-decision-log` - 의사결정 로그 생성
