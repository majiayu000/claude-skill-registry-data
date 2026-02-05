---
name: create-sprint
description: |
  Sprint(Iteration) 목표 설정 및 시작. Use when (1) 새 Sprint 시작,
  (2) Sprint 계획 수립, (3) /SEMO:sprint create 커맨드.
tools: [Bash, Read, Write]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: create-sprint 호출` 메시지를 첫 줄에 출력하세요.

# create-sprint Skill

> Sprint 목표 설정 및 Iteration 활성화

## Purpose

기존 GitHub Projects Iteration을 Sprint로 활용하여 목표를 설정하고 Sprint를 시작합니다.

> **Note**: Iteration은 GitHub Projects에서 자동 생성됩니다. 이 Skill은 해당 Iteration을 Sprint로 "선언"하고 목표를 설정합니다.

## Workflow

```
Sprint 시작 요청
    ↓
1. 현재/다음 Iteration 조회
2. Sprint Issue 생성 (docs 레포)
3. Sprint 목표 설정
4. 알림 전송 (선택)
    ↓
완료
```

## Input

```yaml
iteration_title: "12월 1/4"           # 필수 (GitHub Projects Iteration 이름)
goals:                                # 선택
  - "댓글 기능 완성"
  - "알림 연동 시작"
notify_slack: true                    # 선택
```

## Output

```markdown
[SEMO] Skill: create-sprint 완료

✅ Sprint "12월 1/4" 시작

**기간**: 2025-12-01 ~ 2025-12-07 (1주)
**Sprint Issue**: [#123](issue_url)
```

## API 호출

### Iteration 조회 (GraphQL)

```bash
gh api graphql -f query='
{
  organization(login: "semicolon-devteam") {
    projectV2(number: 1) {
      field(name: "이터레이션") {
        ... on ProjectV2IterationField {
          configuration {
            iterations {
              id
              title
              startDate
              duration
            }
          }
        }
      }
    }
  }
}'
```

### Sprint Issue 생성

```bash
gh issue create \
  --repo semicolon-devteam/docs \
  --title "🏃 Sprint: 12월 1/4" \
  --label "sprint,sprint-current" \
  --body "$(cat <<'EOF'
# 🏃 Sprint: 12월 1/4

**Iteration**: 12월 1/4
**기간**: 2025-12-01 ~ 2025-12-07

## 🎯 Sprint 목표
- 댓글 기능 완성
- 알림 연동 시작

## 📋 포함된 Task
> GitHub Projects "이슈관리" → 이터레이션 "12월 1/4" 필터로 확인

[📊 Projects 보기](https://github.com/orgs/semicolon-devteam/projects/1/views/1?filterQuery=iteration:"12월 1/4")

## 📈 진행 현황
| 상태 | 개수 |
|------|------|
| 작업중 | 0 |
| 완료 | 0 |
| 대기 | 0 |
EOF
)"
```

### 이전 Sprint Issue 정리

```bash
# 이전 sprint-current 라벨 제거
gh issue list \
  --repo semicolon-devteam/docs \
  --label "sprint-current" \
  --json number \
  | jq -r '.[].number' \
  | xargs -I {} gh issue edit {} --remove-label "sprint-current" --add-label "sprint-closed"
```

## Sprint Issue 템플릿

```markdown
# 🏃 Sprint: {iteration_title}

**Iteration**: {iteration_title}
**기간**: {start_date} ~ {end_date}

## 🎯 Sprint 목표
{goals_list}

## 📋 포함된 Task
> GitHub Projects "이슈관리" → 이터레이션 "{iteration_title}" 필터로 확인

[📊 Projects 보기](https://github.com/orgs/semicolon-devteam/projects/1/views/1?filterQuery=iteration:"{iteration_title}")

## 📈 진행 현황
| 상태 | 개수 | Point |
|------|------|-------|
| 작업중 | {in_progress} | {ip_points}pt |
| 완료 | {done} | {done_points}pt |
| 대기 | {todo} | {todo_points}pt |

## 📊 용량
- **총 할당**: {total_points}pt
- **팀 용량**: {capacity}pt
```

## 완료 메시지

```markdown
[SEMO] Skill: create-sprint 완료

✅ **Sprint "{iteration_title}"** 시작

| 항목 | 값 |
|------|-----|
| Iteration | {iteration_title} |
| 기간 | {start_date} ~ {end_date} |
| Sprint Issue | [#{issue_number}]({issue_url}) |

다음 단계: `/SEMO:sprint add` 명령어로 Task를 Sprint에 할당하세요.
```
