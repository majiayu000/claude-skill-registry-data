---
name: list-bugs
description: |
  버그 이슈 조회 (Supabase DB 기반). Use when (1) "버그 이슈 목록",
  (2) "버그 확인", (3) "버그 조회", (4) 버그 이슈 필터링.
tools: [Supabase, Bash]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: list-bugs 호출` 시스템 메시지를 첫 줄에 출력하세요.

# list-bugs Skill

> Supabase DB 기반 버그 이슈 조회

## Purpose

SEMO Office Supabase의 `issues` 테이블에서 `issue_type = 'bug'` 이슈를 조회합니다.

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Issues | `gh issue list` CLI |
| **v2.0** | **Supabase** | `bug_list` 뷰 조회 |

### 기존 방식의 문제점 (GitHub CLI)

```bash
# 기존: 라벨 기반 (레포마다 naming이 다름)
gh issue list --label "bug" --state open
gh issue list --label "BugFix" --state open
```

- 레포마다 라벨 naming이 다름 (bug, BugFix, 🐛, fix 등)
- GitHub API 호출 비용
- 일관된 조회 불가

### 새 방식: Supabase `bug_list` 뷰

Supabase에 미리 정의된 `bug_list` 뷰를 사용합니다.

## Configuration

### Supabase 연결 정보

> **SEMO Office Supabase 프로젝트를 사용합니다.**

| 항목 | 값 |
|------|-----|
| Project | SEMO Office |
| Table | `issues` |
| View | `bug_list` |
| Filter | `type = 'bug'` AND `state = 'open'` |

### issues 테이블 스키마

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| office_id | UUID | 오피스 FK |
| number | SERIAL | 이슈 번호 |
| title | TEXT | 제목 |
| body | TEXT | 본문 |
| type | VARCHAR(20) | task, bug, feature, epic |
| state | VARCHAR(20) | open, closed |
| status | VARCHAR(30) | backlog, todo, in_progress, review, done |
| assignee_id | UUID | 담당자 FK |
| created_at | TIMESTAMPTZ | 생성일 |

## Workflow

### 1. Supabase로 버그 조회

```typescript
// Supabase 클라이언트를 사용한 버그 조회
const { data: bugs, error } = await supabase
  .from('bug_list')
  .select('*')
  .order('created_at', { ascending: false });
```

### 2. SQL 직접 조회 (MCP Server)

```sql
-- bug_list 뷰 조회
SELECT * FROM bug_list;

-- 또는 issues 테이블 직접 조회
SELECT
  i.number,
  i.title,
  i.status,
  ap.name as assignee_name,
  i.created_at
FROM issues i
LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
WHERE i.type = 'bug'
  AND i.state = 'open'
ORDER BY i.created_at DESC;
```

### 3. Office별 버그 조회

```sql
-- 특정 Office의 버그만 조회
SELECT * FROM bug_list
WHERE office_id = '{office_uuid}';
```

## Output Format

```markdown
## 🐛 버그 이슈 현황 (Supabase DB 기준)

| # | 제목 | 상태 | 담당자 | 생성일 |
|---|------|------|--------|--------|
| #123 | API 응답 지연 | in_progress | Developer | 2025-12-01 |
| #456 | 버튼 클릭 안됨 | todo | Frontend | 2025-12-05 |

---
**총 2개의 Open 버그 이슈**
```

## 전체 조회 쿼리

```sql
-- bug_list 뷰를 사용한 전체 버그 조회
SELECT
  number AS "#",
  title AS "제목",
  status AS "상태",
  assignee_name AS "담당자",
  TO_CHAR(created_at, 'YYYY-MM-DD') AS "생성일"
FROM bug_list
ORDER BY created_at DESC;
```

### 상태별 필터링

```sql
-- 진행 중인 버그만 조회
SELECT * FROM bug_list
WHERE status = 'in_progress';

-- 백로그에 있는 버그 조회
SELECT * FROM bug_list
WHERE status = 'backlog';
```

### 담당자별 조회

```sql
-- 특정 담당자의 버그 조회
SELECT * FROM bug_list
WHERE assignee_name = 'Developer';

-- 미할당 버그 조회
SELECT * FROM bug_list
WHERE assignee_id IS NULL;
```

## No Bugs Case

```markdown
## 🐛 버그 이슈 현황 (Supabase DB 기준)

✅ 현재 Open 상태의 버그 이슈가 없습니다.
```

## Error Handling

### Supabase 연결 오류

```markdown
⚠️ **Supabase 연결 오류**

Supabase 프로젝트에 연결할 수 없습니다.
- MCP 서버 설정을 확인해주세요.
- Supabase URL과 API 키를 확인해주세요.
```

### 권한 오류

```markdown
⚠️ **테이블 접근 오류**

issues 테이블에 접근할 수 없습니다.
- RLS 정책을 확인해주세요.
- 서비스 키 사용 여부를 확인해주세요.
```

## SEMO Message Format

```markdown
[SEMO] Skill: list-bugs 호출

[SEMO] Skill: list-bugs 완료 - {N}개 버그 이슈 발견
```

## GitHub CLI Fallback

Supabase 연결이 불가능한 경우 GitHub CLI로 폴백:

```bash
# Fallback: GitHub Issue Type 기반 조회
gh issue list --repo semicolon-devteam/semo --state open \
  --json number,title,issueType,createdAt,assignees \
  --jq '.[] | select(.issueType.name == "Bug")'
```

## Related

- [issues 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [check-feedback Skill](../check-feedback/SKILL.md) - 피드백 이슈 수집
- [project-status Skill](../project-status/SKILL.md) - 이슈 상태 변경
