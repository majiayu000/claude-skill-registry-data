---
name: task-progress
description: |
  개발자 업무 진행도 추적 및 자동화 (Supabase DB 기반).
  Use when (1) 할당된 이슈 진행 상황, (2) 현재 진행 상태 확인, (3) 워크플로우 단계 자동화.
tools: [Supabase, Bash, Read, Grep]
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: task-progress 호출 - #{이슈번호}` 시스템 메시지를 첫 줄에 출력하세요.

# task-progress Skill

> 개발자 업무 진행도를 체크리스트 형태로 표시하고 자동 진행 지원 (Supabase DB 기반)

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Projects | GraphQL API |
| **v2.0** | **Supabase** | `issues` + `issue_status_history` 조회 |

---

## 트리거

- `/SEMO:task-progress` 명령어
- "어디까지 했어", "현황", "체크리스트", "진행도" 키워드
- 이슈 번호 제공 시 orchestrator가 자동 호출

## 개발자 전체 프로세스

```text
1. 업무할당 (backlog → todo)
2. 상태 변경 (todo → in_progress)
3. dev 브랜치에서 Spec 작성 (spec.md, plan.md, tasks.md)
4. Spec 커밋 & 푸시 (원격에 Spec 공유)
5. Feature 브랜치 생성 (Spec 완료 후)
6. Draft PR 생성
7. 실제 코드 구현 (ADD Phase 4)
8. 테스트코드 작성 및 테스트 진행
9. 린트 및 빌드 통과
10. 푸시 및 리뷰 요청 (in_progress → review)
11. PR 승인 및 dev 머지 (review → testing)
12. STG 환경 QA 테스트 (testing → done)
```

### 상태 흐름

```text
backlog → todo → in_progress → review → testing → done
                      ↓           ↑
                  확인요청      수정요청
```

## Workflow

### Step 1: 이슈 현재 상태 조회

```sql
-- 이슈 상세 정보 조회
SELECT
  i.number,
  i.title,
  i.type,
  i.status,
  i.state,
  i.labels,
  i.estimation_point,
  ap.name AS assignee_name,
  TO_CHAR(i.created_at, 'YYYY-MM-DD') AS created_at,
  TO_CHAR(i.updated_at, 'YYYY-MM-DD') AS updated_at
FROM issues i
LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
WHERE i.number = 123
  AND i.office_id = '{office_uuid}';
```

### Step 2: 상태 변경 이력 조회

```sql
-- 상태 변경 히스토리 조회
SELECT
  ish.from_status,
  ish.to_status,
  TO_CHAR(ish.changed_at, 'YYYY-MM-DD HH24:MI') AS changed_at,
  ap.name AS changed_by
FROM issue_status_history ish
LEFT JOIN agent_personas ap ON ish.changed_by = ap.id
WHERE ish.issue_id = (
  SELECT id FROM issues WHERE number = 123
)
ORDER BY ish.changed_at DESC;
```

### Step 3: 진행도 체크리스트 생성

```typescript
// Supabase로 조회
const { data: issue, error } = await supabase
  .from('issues')
  .select(`
    number, title, status, body,
    assignee:agent_personas(name)
  `)
  .eq('number', 123)
  .eq('office_id', officeId)
  .single();

// 상태별 체크리스트 생성
const checklist = generateChecklist(issue.status);
```

## Quick Checks

| Step | Command |
|------|---------|
| 브랜치 | `git branch --show-current` |
| PR 확인 | `gh pr list --head {branch} --json number,isDraft` |
| 린트 | `npm run lint` |
| 타입체크 | `npx tsc --noEmit` |
| 미푸시 확인 | `git log origin/{branch}..HEAD --oneline` |

## Output Format

```markdown
[SEMO] Skill: task-progress 호출 - #123

## 📋 작업 진행 현황: #123

### 이슈 정보

| 항목 | 내용 |
|------|------|
| **제목** | 로그인 페이지 구현 |
| **유형** | feature |
| **상태** | in_progress |
| **담당자** | @reus |
| **작업량** | 4 points |

### 진행도 체크리스트

- [x] 1. 업무 할당
- [x] 2. 상태 변경 (todo → in_progress)
- [x] 3. Spec 작성
- [x] 4. Feature 브랜치 생성
- [x] 5. Draft PR 생성
- [ ] 6. 코드 구현
- [ ] 7. 테스트 작성
- [ ] 8. 린트/빌드 통과
- [ ] 9. 리뷰 요청
- [ ] 10. PR 머지

### 상태 변경 이력

| 시간 | 변경 | 변경자 |
|------|------|--------|
| 2025-01-10 14:30 | todo → in_progress | @reus |
| 2025-01-10 10:00 | backlog → todo | @pm |

### 다음 단계

🎯 **현재 단계**: 코드 구현
📌 **권장 액션**: `skill:write-code` 호출

[SEMO] Skill: task-progress 완료
```

## 자동 상태 변경

### 리뷰 요청 시 (Step 9)

PR Ready 상태가 되면 자동으로 상태를 "review"로 변경:

```sql
-- 상태를 review로 변경
SELECT * FROM update_issue_status(
  123,
  '{office_uuid}'::uuid,
  'review',
  '{actor_uuid}'::uuid
);
```

```markdown
[SEMO] Skill: task-progress → 상태 자동 변경

📋 **이슈**: #123
🔀 **PR**: #150 Ready for Review
🔄 **상태 변경**: in_progress → **review**

✅ 상태 변경 완료
```

## Error Handling

### 이슈 미발견

```markdown
❌ #123 이슈를 찾을 수 없습니다.

확인사항:
- 이슈 번호가 올바른가요?
- Office ID가 올바른가요?
```

### 상태 이력 없음

```markdown
⚠️ #123의 상태 변경 이력이 없습니다.

아직 상태가 변경된 적이 없는 새 이슈입니다.
현재 상태: backlog
```

## GitHub Projects Fallback

Supabase 연결이 불가능한 경우:

```bash
# Fallback: GitHub Projects GraphQL로 상태 조회
gh api graphql -f query='
  query {
    repository(owner: "semicolon-devteam", name: "semo") {
      issue(number: 123) {
        projectItems(first: 1) {
          nodes {
            fieldValueByName(name: "Status") {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
              }
            }
          }
        }
      }
    }
  }
'
```

## Related Skills

- [project-status](../project-status/SKILL.md) - 상태 변경
- [start-task](../start-task/SKILL.md) - 작업 시작
- [assign-task](../assign-task/SKILL.md) - 업무 할당

## References

- [issues 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [Verification Steps](references/verification-steps.md) - 12단계 검증 로직 상세
- [Automation](references/automation.md) - 자동화 명령, 출력 형식
