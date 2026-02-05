---
name: redmine-timetrack
description: 이 스킬은 사용자가 "작업 시간 기록", "시간 등록", "타임 로그", "작업 시간 조회", "몇 시간 일했어", "time entry", "log hours", "time tracking", "work hours" 등을 언급할 때 사용됩니다. Redmine 작업 시간 관리 기능을 제공합니다.
version: 1.0.0
---

# Redmine 작업 시간 관리 스킬

Redmine의 작업 시간(Time Entry) 기능을 관리합니다.

## 개요

이 스킬은 Redmine의 작업 시간 추적 기능을 자동으로 활성화합니다. 작업 시간 기록, 조회, 수정 등을 지원합니다.

## 트리거 조건

다음과 같은 요청에서 활성화됩니다:

### 시간 기록
- "작업 시간 기록", "시간 등록해줘"
- "2시간 일했어", "오늘 작업 시간 로그"
- "log time", "record hours", "time entry"

### 시간 조회
- "내 작업 시간", "이번 주 작업 시간"
- "프로젝트 시간 조회", "이슈별 시간"
- "my time entries", "show work hours"

### 시간 수정/삭제
- "시간 수정", "작업 시간 변경"
- "시간 기록 삭제"
- "update time entry", "delete time log"

## 사용 도구

### redmine_list_time_entries
작업 시간 목록을 조회합니다.

**주요 파라미터:**
- `user_id`: "me" 또는 사용자 ID
- `project_id`: 프로젝트 ID
- `issue_id`: 이슈 ID
- `from`: 시작일 (YYYY-MM-DD)
- `to`: 종료일 (YYYY-MM-DD)
- `spent_on`: 특정 날짜 (YYYY-MM-DD)
- `limit`: 최대 결과 수

**예시:**
```
"내 작업 시간" → user_id: "me"
"이번 주 시간" → from: "2024-01-15", to: "2024-01-21"
"오늘 작업 시간" → spent_on: "2024-01-18"
```

### redmine_create_time_entry
새 작업 시간을 기록합니다.

**주요 파라미터:**
- `hours`: 작업 시간 (필수)
- `activity_id`: 활동 유형 ID (필수)
- `issue_id`: 이슈 ID (issue_id 또는 project_id 중 하나 필수)
- `project_id`: 프로젝트 ID
- `spent_on`: 작업 날짜 (기본: 오늘)
- `comments`: 작업 내용 설명

**예시:**
```
"이슈 #123에 2시간 기록" → issue_id: 123, hours: 2
"개발 작업 3시간" → hours: 3, activity_id: (개발)
```

### redmine_get_time_entry
특정 작업 시간 상세 정보를 조회합니다.

**주요 파라미터:**
- `id`: 작업 시간 ID (필수)

### redmine_update_time_entry
작업 시간을 수정합니다.

**주요 파라미터:**
- `id`: 작업 시간 ID (필수)
- `hours`: 수정할 시간
- `comments`: 수정할 설명
- `activity_id`: 수정할 활동 유형

### redmine_delete_time_entry
작업 시간을 삭제합니다.

**주요 파라미터:**
- `id`: 작업 시간 ID (필수)

### redmine_list_time_entry_activities
사용 가능한 활동 유형 목록을 조회합니다.

**용도:**
- 시간 기록 전 activity_id 확인
- 일반적인 활동: 개발, 설계, 테스트, 회의 등

## 워크플로우 가이드

### 시간 기록 시
1. 활동 유형이 필요하면 `redmine_list_time_entry_activities`로 확인
2. 이슈 ID 또는 프로젝트 ID 확인
3. `redmine_create_time_entry`로 시간 기록

### 시간 조회 시
1. 기간 또는 조건 파악
2. `redmine_list_time_entries`로 목록 조회
3. 합계나 통계가 필요하면 결과를 집계하여 표시

### 시간 수정/삭제 시
1. `redmine_list_time_entries`로 해당 기록 찾기
2. 시간 기록 ID 확인
3. `redmine_update_time_entry` 또는 `redmine_delete_time_entry` 실행
