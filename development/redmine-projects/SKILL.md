---
name: redmine-projects
description: 이 스킬은 사용자가 "프로젝트 목록", "프로젝트 정보", "버전 확인", "마일스톤", "프로젝트 검색", "project list", "show projects", "version info" 등을 언급할 때 사용됩니다. Redmine 프로젝트 관리 기능을 제공합니다.
version: 1.0.0
---

# Redmine 프로젝트 관리 스킬

Redmine 프로젝트 정보를 조회하고 관리합니다.

## 개요

이 스킬은 Redmine의 프로젝트 관리 기능을 자동으로 활성화합니다. 프로젝트 목록, 상세 정보, 버전/마일스톤 조회 등을 지원합니다.

## 트리거 조건

다음과 같은 요청에서 활성화됩니다:

### 프로젝트 조회
- "프로젝트 목록", "프로젝트 보여줘"
- "어떤 프로젝트 있어?", "프로젝트 검색"
- "list projects", "show all projects"

### 프로젝트 상세
- "프로젝트 정보", "프로젝트 상세"
- "프로젝트 설정", "트래커 확인"
- "project details", "project info"

### 버전/마일스톤
- "버전 목록", "마일스톤 확인"
- "릴리즈 일정", "스프린트 목록"
- "versions", "milestones", "releases"

## 사용 도구

### redmine_list_projects
모든 프로젝트 목록을 조회합니다.

**주요 파라미터:**
- `limit`: 최대 결과 수 (기본 25)
- `offset`: 페이징 오프셋

**예시:**
```
"프로젝트 목록 보여줘" → limit: 100
"처음 10개 프로젝트" → limit: 10
```

### redmine_get_project
특정 프로젝트의 상세 정보를 조회합니다.

**주요 파라미터:**
- `id`: 프로젝트 ID 또는 식별자 (필수)
- `include`: 추가 정보 배열
  - `trackers`: 사용 가능한 트래커
  - `issue_categories`: 이슈 카테고리
  - `enabled_modules`: 활성화된 모듈
  - `time_entry_activities`: 작업 시간 활동 유형

**예시:**
```
"sensor-agent 프로젝트 정보" → id: "sensor-agent"
"프로젝트 트래커 확인" → include: ["trackers"]
```

### redmine_get_project_versions
프로젝트의 버전/마일스톤 목록을 조회합니다.

**주요 파라미터:**
- `project_id`: 프로젝트 ID 또는 식별자 (필수)

**예시:**
```
"sensor-agent 버전 목록" → project_id: "sensor-agent"
"다음 릴리즈 일정" → project_id 확인 후 조회
```

## 워크플로우 가이드

### 프로젝트 찾기
1. `redmine_list_projects`로 전체 목록 조회
2. 이름이나 식별자로 원하는 프로젝트 확인
3. 필요시 `redmine_get_project`로 상세 정보 조회

### 이슈 생성 전 프로젝트 확인
1. 사용자가 프로젝트를 지정하지 않은 경우
2. `redmine_list_projects`로 목록 표시
3. 사용자에게 프로젝트 선택 요청

### 버전/마일스톤 확인
1. 프로젝트 ID 확인
2. `redmine_get_project_versions`로 버전 목록 조회
3. 상태별 (open, locked, closed) 버전 구분하여 표시
