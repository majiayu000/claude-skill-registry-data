---
name: redmine-issues
description: 이 스킬은 사용자가 "이슈 만들어", "버그 등록", "태스크 생성", "이슈 목록", "내 할일", "할당된 이슈", "이슈 수정", "이슈 상태 변경", "이슈 검색", "ticket", "issue", "bug report" 등을 언급할 때 사용됩니다. Redmine 이슈 관리 기능을 제공합니다.
version: 1.0.0
---

# Redmine 이슈 관리 스킬

Redmine 이슈 추적 시스템과 연동하여 이슈를 관리합니다.

## 개요

이 스킬은 Redmine의 이슈 관리 기능을 자동으로 활성화합니다. 사용자가 이슈 관련 작업을 요청하면 적절한 Redmine 도구를 사용합니다.

## 트리거 조건

다음과 같은 요청에서 활성화됩니다:

### 이슈 생성
- "이슈 만들어줘", "버그 등록해줘", "태스크 생성"
- "새 티켓 만들어", "feature request 등록"
- "create issue", "create bug", "new ticket"

### 이슈 조회
- "내 이슈 보여줘", "할당된 이슈 목록"
- "오픈된 이슈", "진행중인 태스크"
- "이슈 검색", "버그 찾아줘"
- "list my issues", "show open tickets"

### 이슈 수정
- "이슈 상태 변경", "이슈 업데이트"
- "이슈 완료 처리", "이슈 닫아줘"
- "담당자 변경", "우선순위 변경"
- "update issue", "close ticket"

## 사용 도구

### redmine_list_issues
이슈 목록을 조회합니다.

**주요 파라미터:**
- `project_id`: 프로젝트 ID 또는 식별자
- `assigned_to_id`: "me" 또는 사용자 ID
- `status_id`: "open", "closed", "*" 또는 상태 ID
- `tracker_id`: 트래커 ID (Bug, Feature, Task 등)
- `limit`: 최대 결과 수 (기본 25)

**예시:**
```
"내 이슈 보여줘" → assigned_to_id: "me", status_id: "open"
"완료된 이슈" → status_id: "closed"
"모든 버그" → tracker_id: 1 (Bug)
```

### redmine_get_issue
특정 이슈의 상세 정보를 조회합니다.

**주요 파라미터:**
- `id`: 이슈 ID (필수)
- `include`: 추가 정보 (journals, attachments, relations 등)

### redmine_create_issue
새 이슈를 생성합니다.

**주요 파라미터:**
- `project_id`: 프로젝트 ID (필수)
- `subject`: 이슈 제목 (필수)
- `description`: 이슈 설명
- `tracker_id`: 트래커 ID
- `priority_id`: 우선순위 ID
- `assigned_to_id`: 담당자 ID

### redmine_update_issue
기존 이슈를 수정합니다.

**주요 파라미터:**
- `id`: 이슈 ID (필수)
- `status_id`: 상태 ID
- `done_ratio`: 완료율 (0-100)
- `notes`: 코멘트 추가

## 워크플로우 가이드

### 이슈 생성 시
1. 프로젝트 ID가 없으면 `redmine_list_projects`로 먼저 확인
2. 트래커/우선순위 ID가 필요하면 `redmine_list_trackers`, `redmine_list_priorities` 사용
3. `redmine_create_issue`로 이슈 생성

### 이슈 검색 시
1. 조건에 맞는 필터 파라미터 설정
2. `redmine_list_issues`로 목록 조회
3. 필요시 `redmine_get_issue`로 상세 정보 확인

### 이슈 수정 시
1. 이슈 ID 확인 (목록에서 찾거나 사용자에게 확인)
2. 변경할 필드와 값 확인
3. `redmine_update_issue`로 업데이트
