---
name: session-logger
description: Log work sessions with timestamps, decisions, agent handoffs, issues, and outcomes. Use when a session log needs to be created or updated.
---

# Session Logger Skill

> **목적**: 개발 작업 세션을 실시간으로 기록하여 의사결정 과정과 시행착오를 추적
> **사용 시점**: 작업 시작, 에이전트 전환, 의사결정, 이슈 발생, 작업 완료
> **출력**: `.claude/docs/tasks/{feature-name}/session-logs/day-YYYY-MM-DD.md`

---

## 🎯 목표

### 문제점
- **2025-12-19 세션 분석 결과**: 의사결정 과정이 기록되지 않아 재작업 원인 파악 불가
- 컨텍스트 전환 시 작업 내용 재구성 필요 (시간 낭비)
- 실시간 작업 흐름 추적 부재

### 해결 방안
- 작업 중 자동 세션 로깅
- 타임라인 기반 작업 추적
- 의사결정/이슈 구조화 기록

---

## 📝 기록 시점 (자동 트리거)

### 1. 작업 시작 시
```markdown
## [09:00] 작업 시작

### 요청
- 사용자 메시지: "배치 관리 기능 구현해줘"
- 브랜치: feature/batch-management
- 기존 context.md: 없음

### 초기 분석
- 작업 타입: feature (신규 기능)
- 복잡도: complex (예상 8개 파일)
- Phase: planning (계획 필요)
```

### 2. 에이전트 전환 시
```markdown
## [09:15] Requirements Analyzer → Context Builder

### 산출물
- 사전 합의서 생성 완료
- 주요 변경사항: 날짜 단일 입력, 배치실행일시 제거
- 불확실한 부분: 없음 (모두 명확화)

### 다음 단계
- Context Builder Agent 호출
- 구현 계획 작성 예상 시간: 10분
```

### 3. 의사결정 시
```markdown
## [09:20] 의사결정: API 프록시 패턴 사용

### 결정 내용
- 클라이언트 → Next.js API Routes → 백엔드
- 직접 호출 금지 (CLAUDE.md 규칙)

### 이유
- 인증 토큰 서버 사이드 처리 필수
- 활동 로그 헤더 자동 추가
- 보안 강화

### 대안 (고려했으나 채택 안 함)
- 클라이언트 직접 호출: 보안 취약
- 브라우저 쿠키 사용: CORS 이슈
```

### 4. 이슈 발생 시
```markdown
## [10:15] 이슈: 타입 에러 발생

### 문제
- `ExecuteBatchApiResponse`에서 snake_case 필드 인식 불가
- TypeScript 에러: Property 'job_execution_id' does not exist

### 원인
- 백엔드 응답 타입 정의 누락
- camelCase 변환 로직 없음

### 해결
- `_requests/types.ts`에 API 응답 원본 타입 추가
- `mapResponse` 함수로 변환 로직 분리
- 소요 시간: 10분

### 재발 방지
- API 응답 타입 정의 우선 작성
- snake_case → camelCase 변환 표준화
```

### 5. 작업 완료 시
```markdown
## [11:30] 작업 완료

### 산출물
- 커밋 2개: 7b0072e (Mock), c07d9b6 (API)
- 신규 파일: 8개
- 문서: context.md, session-log.md

### 검증 결과
- ✅ typecheck 통과
- ✅ build 성공
- ✅ lint 통과

### 남은 작업
- [ ] 수동 테스트
- [ ] 에러 케이스 처리
```

---

## 📋 세션 로그 구조

### 기본 템플릿

```markdown
# {YYYY-MM-DD} {기능명} 구현 세션

## 세션 메타데이터
- 시작 시간: {HH:MM}
- 종료 시간: {HH:MM} (진행 중이면 미기재)
- 주요 작업: {작업 요약}
- 브랜치: {git branch}
- 작업자: {사용자명}

## 타임라인

### [HH:MM] 이벤트명
- 내용...

### [HH:MM] 이벤트명
- 내용...

## 의사결정 로그

| 시간 | 결정 사항 | 이유 | 대안 |
|------|-----------|------|------|
| 09:20 | API 프록시 사용 | 보안 강화 | 직접 호출 (채택 안 함) |

## 이슈 로그

### 이슈 #1: {제목}
- **발견 시각**: HH:MM
- **문제**: ...
- **원인**: ...
- **해결**: ...
- **소요 시간**: N분
- **재발 방지**: ...

## 블로킹/대기 기록

| 시작 시간 | 종료 시간 | 사유 | 영향 |
|----------|----------|------|------|
| 09:20 | 09:25 | API 스펙 확인 대기 | 5분 대기 |

## 회고 메모

### 잘한 점
- 사전 합의서 작성으로 재작업 0

### 개선할 점
- API 스펙 초안을 더 일찍 요청할 것

### 배운 점
- snake_case → camelCase 변환 표준화 필요
```

---

## 🔧 사용 방법

### 수동 트리거 (사용자가 직접 호출)

```
session-logger 시작: 배치 관리 기능 구현
```

→ `.claude/docs/tasks/batch-management/session-logs/day-2025-12-20.md` 생성

### 자동 트리거 (시스템이 자동 호출)

1. **작업 시작 시**: 사용자 메시지 수신 → 세션 로그 생성
2. **에이전트 전환 시**: Agent 호출 → 타임라인 추가
3. **의사결정 시**: 중요한 선택 → 의사결정 로그 추가
4. **이슈 발생 시**: 에러/문제 → 이슈 로그 추가
5. **작업 완료 시**: 최종 산출물 → 완료 기록

---

## 📊 출력 예시

### 실제 세션 로그 (2025-12-20)

```markdown
# 2025-12-20 배치 관리 기능 구현 세션

## 세션 메타데이터
- 시작 시간: 09:00
- 종료 시간: 11:30
- 주요 작업: 배치 관리 기능 구현
- 브랜치: feature/batch-management
- 작업자: 문석기

## 타임라인

### [09:00] 작업 시작
- 사용자 요청: "배치 관리 기능 구현해줘"
- PM Agent 분석: feature, complex, planning phase
- 불확실한 부분: 화면 정의서 버전, API 스펙 초안

### [09:05] 사용자 응답 (요구사항 명확화)
- 화면 정의서: v3 (2025-12-18 확정)
- API 스펙: POST /api/admin/shelf/product/batch-executions
- 날짜 입력: 단일 일자 (yyyy-mm-dd)

### [09:10] Requirements Analyzer 완료
- 사전 합의서 생성: .claude/docs/agreements/batch-management.md
- 주요 변경사항: 날짜 단일 입력, 배치실행일시 제거
- 다음 단계: Context Builder

### [09:20] Context Builder 완료
- context.md 생성: .claude/docs/tasks/batch-management-context.md
- 변경 대상 파일: 8개 신규, 2개 수정
- 예상 작업 시간: 2.5시간

### [09:45] Implementation Phase 1 완료 (Mock)
- 타입 정의, Mock 데이터, UI 컴포넌트 구현
- commit 7b0072e: 배치 관리 1차 커밋
- 검증: typecheck ✅, build ✅

### [10:30] Implementation Phase 2 완료 (API)
- API 라우트, Fetch 함수, 데이터 변환 로직
- commit c07d9b6: 배치 관리 API 적용
- 검증: API 호출 성공 ✅

### [11:00] Verification 완료
- typecheck ✅, build ✅, lint ✅
- 활동 로그 헤더 확인 ✅

### [11:30] Documentation 완료
- context.md 최종 업데이트
- session-log.md 생성
- 작업 흐름 리포트 생성

## 의사결정 로그

| 시간 | 결정 사항 | 이유 | 대안 |
|------|-----------|------|------|
| 09:10 | 날짜 단일 입력 | 화면 정의서 v3 명시 | 시작일~종료일 (v2, 채택 안 함) |
| 09:20 | API 프록시 사용 | CLAUDE.md 규칙 준수 | 직접 호출 (금지) |
| 10:00 | Mock 먼저 구현 | API 스펙 확정 대기 | API 대기 후 일괄 구현 |

## 이슈 로그

### 이슈 #1: 타입 에러 (snake_case 미변환)
- **발견 시각**: 10:15
- **문제**: ExecuteBatchApiResponse에서 job_execution_id 인식 불가
- **원인**: snake_case → camelCase 변환 로직 누락
- **해결**: mapResponse 함수 추가, 타입 분리
- **소요 시간**: 10분
- **재발 방지**: API 응답 타입 정의 우선 작성

## 블로킹/대기 기록

| 시작 시간 | 종료 시간 | 사유 | 영향 |
|----------|----------|------|------|
| 09:20 | 09:25 | API 스펙 확인 (사용자 응답 대기) | 5분 |

## 회고 메모

### 잘한 점
- 사전 합의서 작성으로 재작업 0
- 단계별 검증으로 조기 에러 발견
- 명확한 타임라인으로 작업 추적 용이

### 개선할 점
- API 스펙 초안을 더 일찍 요청
- snake_case 변환 표준화 미리 정의

### 배운 점
- 요구사항 명확화 30분 투자 → 4시간 절약 (ROI 800%)
- 실시간 세션 로깅으로 의사결정 근거 보존
```

---

## 🎨 활용 사례

### 사례 1: 며칠에 걸친 작업

**Day 1 (Mock 구현)**
```markdown
# 2025-12-20 배치 관리 기능 구현 세션 (Day 1)

## [16:00] 작업 중단 (API 대기)
- Phase 1 완료: Mock 기반 UI
- Phase 2 대기: API 스펙 확정 필요
- 다음 작업: API 연동 (내일 진행)
```

**Day 2 (API 연동)**
```markdown
# 2025-12-21 배치 관리 기능 구현 세션 (Day 2)

## [09:00] 작업 재개
- Day 1 상태: Mock 구현 완료 (commit 7b0072e)
- 오늘 작업: API 연동
- pending-questions.md 확인: 없음 (API 스펙 확정)

## [09:30] API 연동 시작
- API 라우트 구현...
```

### 사례 2: 이슈 추적

```markdown
## 이슈 로그

### 이슈 #1: 날짜 포맷 불일치
- **발견 시각**: 10:20
- **문제**: 백엔드는 yyyyMMdd, 화면은 yyyy-mm-dd
- **원인**: 날짜 포맷 변환 누락
- **해결**: toApiDate, formatApiDate 함수 추가
- **소요 시간**: 15분
- **재발 방지**: 날짜 포맷 변환 유틸 표준화

### 이슈 #2: 활동 로그 헤더 누락
- **발견 시각**: 11:00
- **문제**: fetchCount에 활동 로그 헤더 포함됨
- **원인**: CLAUDE.md 규칙 미숙지 (카운트는 헤더 제외)
- **해결**: 헤더 제거
- **소요 시간**: 5분
- **재발 방지**: CLAUDE.md 활동 로그 섹션 재확인
```

---

## 🔗 연계 에이전트/스킬

### 입력 (사용하는 정보)
- PM Agent: 작업 타입, 복잡도, Phase 판단 결과
- Requirements Analyzer: 사전 합의서, 질문 목록
- Context Builder: 구현 계획, 체크포인트
- Implementation Agent: 커밋 메시지, 변경 파일 목록
- Verification Agent: 검증 결과

### 출력 (제공하는 정보)
- Documentation Agent: 세션 로그 → 작업 흐름 리포트
- Efficiency Tracker: 타임라인 → 시간 분배 분석
- 사용자: 실시간 작업 진행 상황

---

## 📦 파일 구조

```
.claude/docs/tasks/
└── {feature-name}/
    └── session-logs/
        ├── day-2025-12-20.md  # Day 1
        ├── day-2025-12-21.md  # Day 2
        └── day-2025-12-22.md  # Day 3
```

---

## 💡 사용 팁

### 1. 작업 시작 시 자동 생성
- 첫 사용자 메시지 → 세션 로그 자동 생성
- 기능명 자동 추출 (예: "배치 관리 기능" → `batch-management`)

### 2. 실시간 업데이트
- 에이전트 전환마다 타임라인 자동 추가
- 의사결정/이슈는 구조화된 형태로 자동 기록

### 3. 하루 마감 시 검토
- 회고 메모 작성
- pending-questions.md 업데이트
- WIP 커밋 (예: `chore: wip mock ready for api`)

### 4. 다음 날 재진입
- 이전 세션 로그 확인
- 마지막 타임라인부터 재개
- pending-questions 우선 처리

---

## 🎯 기대 효과

### 정성적 효과
1. **의사결정 근거 보존**: 왜 그렇게 결정했는지 기록
2. **시행착오 추적**: 같은 실수 반복 방지
3. **작업 흐름 가시화**: 실시간 진행 상황 파악
4. **컨텍스트 전환 용이**: 작업 재구성 시간 단축

### 정량적 효과
- **컨텍스트 전환 시간**: 30분 → 5분 (83% 단축)
- **이슈 재발 방지**: 동일 이슈 재발 0%
- **회고 품질 향상**: 구조화된 데이터 기반 분석

---

**이 스킬을 활성화하면 모든 작업이 자동으로 기록됩니다!**
