---
name: padlet-orchestrator
description: "교육용 Padlet 클론 프로젝트의 전체 3단계(Notion→SQLite→Supabase) 개발 워크플로우를 조율하는 오케스트레이터. '패들렛 만들어줘', 'Padlet 클론 시작', '교육용 보드 앱 개발', '단계별 진행' 등을 요청하면 반드시 이 스킬을 사용할 것."
---

# Edu-Padlet Orchestrator

교육용 Padlet 클론 프로젝트를 단계별로 개발하고, 각 단계마다 **동작하는 코드 + 교육 자료**를 생성하는 통합 워크플로우.

## ⚠️ 핵심 원칙: 학생에게는 하네스가 없다

이 하네스는 **교사/개발자용 생성 도구**이다. 학생에게는 하네스 시스템(에이전트, 스킬)이 없으므로:

1. **하네스가 자동 실행하는 모든 과정**(git init, npm install, 서버 실행, 배포 등)은 **반드시 교안의 실습 지침서에 학생이 따라할 수 있는 형태로 포함**해야 한다.
2. 하네스가 자동으로 해결한 문제(에러, 설정 등)는 **트러블슈팅 교안에 반영**한다.
3. 하네스의 역할은 "수업 자동화"가 아니라 **"교안 + 코드 생성 및 검증"**이다.
4. **교안만으로 학생이 처음부터 끝까지 완성할 수 있어야** 한다. 교안에 없으면 학생은 할 수 없다.

이 원칙은 모든 에이전트(code-builder, curriculum-writer, qa-validator)에 적용된다.

## 실행 모드: 에이전트 팀 (단계별 팀 재구성)

## 에이전트 구성

| 팀원 | 타입 | 역할 | 출력 |
|------|------|------|------|
| code-builder | 커스텀 | 동작하는 코드 생성 | `code/step{N}/` |
| curriculum-writer | 커스텀 | 교안 + 지침서 작성 | `교안/step{N}/` |
| qa-validator | 커스텀 | 코드 + 교안 검증 | `_workspace/qa_step{N}_report.md` |

## 3단계 로드맵

| 단계 | DB | 학습 목표 | 핵심 개념 |
|------|-----|---------|---------|
| Step 1 | Notion DB | CRUD, API, 서버의 역할 | HTTP, JSON, API 키 |
| Step 2 | SQLite | DB = 파일, SQL 입문 | SELECT/INSERT/DELETE |
| Step 3 | Supabase | 실서비스 DB, 배포 개념 | 클라우드, 인증, 환경변수 |

---

## 워크플로우

### Phase 0: 프로젝트 준비

1. 사용자에게 현재 진행할 단계 확인 (1, 2, 3 또는 전체)
2. 작업 디렉토리 구조 생성:
   ```
   edu-padlet/
   ├── code/
   │   ├── step1-notion/
   │   ├── step2-sqlite/
   │   └── step3-supabase/
   ├── 교안/
   │   ├── step1-notion/
   │   ├── step2-sqlite/
   │   └── step3-supabase/
   └── _workspace/
   ```
3. `_workspace/00_project_spec.md`에 프로젝트 스펙 저장

### Phase 1: Step 1 — Notion DB

#### 팀 구성
```
TeamCreate(
  team_name: "step1-team",
  members: [
    { name: "code-builder", agent_type: "code-builder", model: "opus",
      prompt: "Step 1 Notion DB 연동 코드 생성. notion-step 스킬 참조. 완성 후 qa-validator에게 알림." },
    { name: "curriculum-writer", agent_type: "curriculum-writer", model: "opus",
      prompt: "Step 1 Notion 교안 + API 키 가이드 작성. curriculum-write 스킬 참조. 완성 후 qa-validator에게 알림." },
    { name: "qa-validator", agent_type: "qa-validator", model: "opus",
      prompt: "Step 1 코드 + 교안 검증. 문제 발견 시 해당 팀원에게 수정 요청." }
  ]
)
```

#### 작업 등록
```
TaskCreate(tasks: [
  { title: "Step1 서버 코드 작성", assignee: "code-builder",
    description: "Express + Notion API 프록시 서버. db.js 표준 인터페이스 준수." },
  { title: "Step1 프론트엔드 작성", assignee: "code-builder",
    description: "Vanilla HTML/CSS/JS 보드 UI. 카드 CRUD 기능." },
  { title: "Step1 개념 교안 작성", assignee: "curriculum-writer",
    description: "00_개념교안 ~ 05_트러블슈팅 6개 파일. 중등~고등 수준." },
  { title: "Step1 QA 검증", assignee: "qa-validator",
    description: "코드 + 교안 검증. 체크리스트 기준으로 검토.",
    depends_on: ["Step1 서버 코드 작성", "Step1 프론트엔드 작성", "Step1 개념 교안 작성"] }
])
```

#### 팀원 간 통신 규칙
- code-builder → curriculum-writer: API 엔드포인트 목록 SendMessage
- code-builder, curriculum-writer → qa-validator: 완성 알림 SendMessage
- qa-validator → 오케스트레이터: "Step 1 QA 완료" 알림

#### 완료 조건
- `code/step1-notion/` 디렉토리에 실행 가능한 코드 존재
- `교안/step1-notion/` 디렉토리에 6개 파일 존재
- `_workspace/qa_step1_report.md`에 주요 항목 통과 기록

### Phase 2: Step 1 완료 확인 및 사용자 리뷰

1. 팀 정리 (TeamDelete)
2. 사용자에게 Step 1 결과 요약 보고:
   - 코드 위치: `code/step1-notion/`
   - 실행 방법: `cd code/step1-notion && npm install && node server.js`
   - 교안 위치: `교안/step1-notion/`
3. **Step 2 진행 여부 사용자 확인** → 확인 후 진행

### Phase 3: Step 2 — SQLite (사용자 확인 후)

#### 팀 재구성
```
TeamCreate(
  team_name: "step2-team",
  members: [
    { name: "architect", agent_type: "architect", model: "opus",
      prompt: "Step1→Step2 전환 계획 수립. db.js 교체 범위 분석 후 code-builder에게 전달." },
    { name: "code-builder", agent_type: "code-builder", model: "opus",
      prompt: "Step 2 SQLite db.js 작성. Step1 server.js는 수정하지 않음. sqlite-step 스킬 참조." },
    { name: "curriculum-writer", agent_type: "curriculum-writer", model: "opus",
      prompt: "Step 2 SQLite 교안 작성. Step1과의 차이 강조. curriculum-write 스킬 참조." },
    { name: "qa-validator", agent_type: "qa-validator", model: "opus",
      prompt: "Step 2 코드 + 교안 검증. db.js 인터페이스 일관성 중점 확인." }
  ]
)
```

작업 등록 및 통신 규칙은 Phase 1과 동일 패턴 적용.

### Phase 4: Step 3 — Supabase (사용자 확인 후)

Phase 3와 동일 패턴, `supabase-step` 스킬 참조.

---

## 데이터 흐름

```
오케스트레이터
    ├── TeamCreate → [code-builder] ──SendMessage──→ [curriculum-writer]
    │                    │                                  │
    │               code/step{N}/                    교안/step{N}/
    │                    │                                  │
    │                    └──────────SendMessage────────────→[qa-validator]
    │                                                        │
    │                                              _workspace/qa_report.md
    │                                                        │
    └── ←──────────────── "단계 완료" SendMessage ───────────┘
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| code-builder 실패 | 재시도 1회 → 재실패 시 오케스트레이터가 직접 기본 템플릿 생성 |
| curriculum-writer 지연 | qa-validator가 코드만 먼저 검증 → 교안 완성 후 재검증 |
| QA 2회 이상 실패 | 오케스트레이터가 문제 항목 사용자에게 보고 후 진행 여부 확인 |
| 이전 단계 코드 없이 Step 2 요청 | Step 1부터 자동 시작 알림 |

## 테스트 시나리오

### 정상 흐름
1. 사용자: "Step 1 시작해줘"
2. Phase 0: 디렉토리 생성
3. Phase 1: 팀 구성 → 병렬 작업 (코드 + 교안) → QA
4. Phase 2: 사용자에게 결과 보고 + Step 2 진행 여부 확인
5. 예상 결과: `code/step1-notion/` + `교안/step1-notion/` 생성

### 에러 흐름
1. qa-validator가 "package.json 누락" 발견
2. code-builder에게 수정 요청 SendMessage
3. code-builder가 package.json 추가
4. qa-validator 재검증 → 통과
5. 오케스트레이터에게 완료 보고
