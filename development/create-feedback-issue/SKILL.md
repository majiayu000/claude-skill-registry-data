---
name: create-feedback-issue
description: |
  SEMO 패키지 피드백 수집 및 이슈 생성 (Supabase DB 기반).
  Use when (1) /SEMO:feedback 명령어 호출, (2) 사용자가 SEMO 동작 오류 지적, (3) 개선 제안 요청.
tools: [Supabase, Bash, Read]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: create-feedback-issue 호출 - {피드백 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# create-feedback-issue Skill

> SEMO 패키지에 대한 사용자 피드백을 Supabase issues 테이블에 저장 (SEMO 공통 Skill)

## Purpose

모든 SEMO 패키지에서 공통으로 사용하는 피드백 수집 Skill입니다.

---

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Issues | `gh issue create` CLI |
| **v2.0** | **Supabase** | `issues` 테이블 INSERT |

---

## 🔴 NON-NEGOTIABLE RULES

### 로컬 수정 금지

> **feedback 스킬은 절대로 로컬 스킬 파일을 직접 수정하지 않습니다.**

| 동작 | 허용 여부 | 설명 |
|------|----------|------|
| Supabase issues 테이블에 INSERT | ✅ 허용 | DB에 피드백 등록 |
| 로컬 스킬 파일 수정 | ❌ 금지 | semo-system/ 내 파일 수정 불가 |
| 로컬 CLAUDE.md 수정 | ❌ 금지 | .claude/ 내 파일 수정 불가 |

### 이유

- 로컬 수정은 npm 패키지 업데이트 시 덮어씌워짐
- SEMO 팀에 피드백이 전달되지 않음
- 다른 사용자에게 개선사항이 공유되지 않음

### Meta 환경 예외

Meta 환경(semo 레포 직접 작업)에서만 직접 수정 허용:

```bash
# Meta 환경 확인 방법
git remote -v | grep "semicolon-devteam/semo"
# 또는
[ -d "semo-system/meta" ] && echo "Meta 환경"
```

| 환경 | 동작 |
|------|------|
| 일반 환경 (semo init 설치) | 이슈 생성만 허용 |
| Meta 환경 (semo 레포) | 직접 수정 허용 (process-feedback 스킬 사용) |

---

## Feedback Types

| 유형 | 설명 | issues.type |
|------|------|-------------|
| **bug** | 의도한 대로 동작하지 않음 | `bug` |
| **feature** | 개선 아이디어, 새 기능 요청 | `feature` |

> **Note**: labels 컬럼에 `feedback` 값이 필수로 포함됩니다.

## Workflow

```text
1. 피드백 유형 확인 (버그 or 제안)
   ↓
2. 정보 수집 (질문/결과/기대사항)
   ↓
3. Supabase issues 테이블에 INSERT
   ↓
4. 완료 메시지 (이슈 번호 안내)
```

## Execution

### Step 1: 피드백 정보 수집

사용자에게 다음 정보를 수집:
- 피드백 유형 (bug / feature)
- 제목
- 상세 내용 (재현 단계, 기대 결과 등)

### Step 2: Supabase로 이슈 생성

```typescript
// Supabase 클라이언트를 사용한 이슈 생성
const { data, error } = await supabase
  .from('issues')
  .insert({
    office_id: officeId,  // 현재 Office ID
    title: `[Feedback] ${title}`,
    body: body,
    type: feedbackType,  // 'bug' or 'feature'
    state: 'open',
    status: 'backlog',
    labels: ['feedback', packageName]
  })
  .select('number')
  .single();
```

### Step 2-1: SQL 직접 사용 (MCP Server)

```sql
-- 버그 피드백 생성
INSERT INTO issues (office_id, title, body, type, state, status, labels)
VALUES (
  '{office_uuid}',
  '[Feedback] {제목}',
  '{본문}',
  'bug',
  'open',
  'backlog',
  ARRAY['feedback', 'semo-skills']
)
RETURNING number;

-- 개선 제안 생성
INSERT INTO issues (office_id, title, body, type, state, status, labels)
VALUES (
  '{office_uuid}',
  '[Enhancement] {제목}',
  '{본문}',
  'feature',
  'open',
  'backlog',
  ARRAY['feedback', 'semo-skills']
)
RETURNING number;
```

### Step 3: create_feedback_issue 함수 사용 (권장)

마이그레이션에 포함된 헬퍼 함수를 사용:

```sql
-- 피드백 이슈 생성 함수 호출
SELECT * FROM create_feedback_issue(
  '{office_uuid}'::uuid,
  '[Feedback] 스킬 동작 오류',
  '## 문제 상황\n\nwrite-code 스킬이 제대로 동작하지 않습니다...',
  'bug',
  ARRAY['feedback', 'semo-skills']
);
```

## Output

```markdown
[SEMO] Feedback: 이슈 생성 완료

✅ 피드백이 등록되었습니다!

**이슈**: #{이슈번호}
**제목**: {이슈 제목}
**유형**: {버그/기능요청}
**상태**: backlog
```

## GitHub CLI Fallback

Supabase 연결이 불가능한 경우 GitHub CLI로 폴백:

```bash
# 버그 이슈 (Fallback)
gh issue create \
  --repo semicolon-devteam/semo \
  --title "[Feedback] {제목}" \
  --body-file /tmp/issue-body.md \
  --label "feedback" \
  --label "bug"
```

## Error Handling

### Supabase 연결 오류

```markdown
⚠️ **Supabase 연결 오류**

이슈를 생성할 수 없습니다.
- MCP 서버 설정을 확인해주세요.
- GitHub CLI 폴백을 시도합니다...
```

### 필수 필드 누락

```markdown
⚠️ **입력 오류**

다음 필드가 필요합니다:
- 피드백 유형 (bug / feature)
- 제목
- 상세 내용
```

## References

- [issues 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [Issue Templates](references/issue-templates.md)
- [Trigger Detection](references/trigger-detection.md)
