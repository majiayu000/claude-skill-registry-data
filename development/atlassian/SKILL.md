---
name: atlassian
description: >
  Jira 이슈 조회, 생성, 편집, 상태 변경, 댓글 관리 등 Atlassian CLI를 활용한 Jira 작업 수행.
  사용자가 Jira, 이슈, 티켓, SF-, PROJ- 같은 이슈 키, JQL, 스프린트, 보드를 언급할 때 사용.
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Atlassian CLI Integration

공식 Atlassian CLI (ACLI)를 사용하여 Jira를 관리합니다.

**⚠️ 주의**: ACLI v1.3.5는 **Jira만 지원**합니다. Confluence는 지원되지 않습니다.

## 빠른 시작

### 인증 확인
```bash
acli jira auth status
```

인증이 필요한 경우:
```bash
acli jira auth login --web
```

상세한 인증 방법은 `authentication.md` 참고

## 핵심 명령어

### 이슈 조회
```bash
# 이슈 상세 보기 (모든 필드)
acli jira workitem view SF-946 --fields "*all"

# 특정 필드만 조회
acli jira workitem view SF-946 --fields "summary,status,assignee,description"

# 웹 브라우저에서 열기
acli jira workitem view SF-946 --web
```

### 이슈 검색 (JQL)
```bash
# 프로젝트의 모든 이슈
acli jira workitem search --jql "project = SF"

# 현재 사용자에게 할당된 미완료 이슈
acli jira workitem search --jql "assignee = currentUser() AND status != Done"

# JSON 출력
acli jira workitem search --jql "project = SF" --json
```

### 이슈 생성
```bash
# 기본 생성
acli jira workitem create \
  --project "SF" \
  --type "Task" \
  --summary "새로운 작업"

# 상세 정보 포함
acli jira workitem create \
  --project "SF" \
  --type "Bug" \
  --summary "버그 제목" \
  --description "상세 설명" \
  --assignee "@me"
```

### 이슈 편집
```bash
# 요약 변경
acli jira workitem edit --key "SF-946" --summary "새로운 요약"

# 담당자 변경
acli jira workitem edit --key "SF-946" --assignee "@me"

# 여러 이슈 일괄 편집
acli jira workitem edit --key "SF-1,SF-2,SF-3" --assignee "@me"
```

### 상태 변경
```bash
# 단일 이슈
acli jira workitem transition --key "SF-946" --status "In Progress"

# 여러 이슈
acli jira workitem transition --key "SF-1,SF-2" --status "Done"
```

### 댓글 관리
```bash
# 댓글 조회
acli jira workitem comment list --key "SF-946"

# 댓글 추가
acli jira workitem comment create --key "SF-946" --body "댓글 내용"

# 여러 이슈에 댓글 추가
acli jira workitem comment create --jql "project = SF" --body "공통 댓글"
```

## 자주 사용하는 패턴

### 내 작업 조회
```bash
acli jira workitem search --jql "assignee = currentUser() AND status != Done"
```

### 할당되지 않은 이슈 조회
```bash
acli jira workitem search --jql "project = SF AND assignee is EMPTY"
```

### CSV로 내보내기
```bash
acli jira workitem search --jql "project = SF" --csv > issues.csv
```

## 유용한 옵션

```bash
--json          # JSON 출력
--csv           # CSV 출력 (search만)
--yes           # 확인 없이 실행
--web           # 웹 브라우저에서 열기
```

## 추가 문서

- **reference.md** - 전체 명령어 레퍼런스 (프로젝트, 보드, 스프린트, 필드, 관리자 등)
- **examples.md** - JQL 예제, 배치 작업, 실전 사례
- **authentication.md** - 설치 및 인증 가이드

## 문제 해결

인증 문제:
```bash
acli jira auth status
acli jira auth login --web
```

연결 테스트:
```bash
acli jira project list --limit 1
```

도움말:
```bash
acli jira workitem --help
```

## 참고 링크

- 공식 문서: https://developer.atlassian.com/cloud/acli/
- API 토큰: https://id.atlassian.com/manage-profile/security/api-tokens
- JQL 가이드: https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-search-in-jira-cloud/
