---
name: efficiency-tracker
description: Track workflow timelines, blockers, verification results, and commits in flow-report.md. Use when recording execution flow or efficiency.
---

# Efficiency Tracker Skill

**역할**: 작업 흐름 상태를 기록하고 흐름 리포트(flow-report)를 생성합니다. (타임라인, 블로킹, 검증 결과, 커밋 링크)

## 입력
- 기능명: `{feature-name}`
- Phase/브랜치 정보(선택)
- 검증 명령 결과 로그(선택)

## 동작
1. 시작/종료 타임스탬프, 활성 Phase를 기록.
2. 블로킹 구간(예: 화면 정의서 확인 대기, API 스펙 대기)을 메모로 추가.
3. 실행한 검증 명령(typecheck/build/lint 등)과 결과를 기록.
4. 변경 파일/커밋 링크와 작성자 메모를 남김.
5. `.claude/docs/tasks/{feature-name}/flow-report.md`에 append 또는 생성.

## 출력
- flow-report.md 업데이트 로그
- 필요 시 session-log/day-...에 타임라인 항목 추가

## 실행 스니펫
```
작업 흐름 리포트를 업데이트해줘.
- 기능: {featureName}
- Phase: {phase}
- 블로킹 메모: {blockingNotes}
- 검증 결과: {verifyResults}
- 커밋/파일: {commitRefs}
출력: flow-report.md 업데이트
```
