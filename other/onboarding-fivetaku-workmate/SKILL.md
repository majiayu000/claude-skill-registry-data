---
name: onboarding
description: workmate 업무공간을 사용자 개인화하는 인터뷰 스킬. "온보딩", "/onboarding", "처음 세팅", "내 정보 넣어줘", "내 비서로 만들어줘" 같은 요청에 사용. 사람 정보 + 실제 자료 + 직무 맞춤 폴더 구조까지 한 흐름에 세팅합니다.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Skill
  - AskUserQuestion
---

# Onboarding

> workmate 업무공간을 **공용 상태 → 내 비서**로 개인화하는 인터뷰 스킬.
> 사람 정보 + 실제 자료 + 직무 맞춤 폴더 구조까지 한 번에 세팅합니다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

사용자가 `/onboarding`, "온보딩", "처음 세팅", "내 비서로" 같은 요청을 하면:

1. **먼저 `memory/state/onboarding.yaml`을 Read**하여 현재 상태 확인
2. 상태에 따라 Phase 0 진입 분기:
   - `status: not_started` → Phase 0부터 시작
   - `status: in_progress` → "이어서 하기" 옵션 제시
   - `status: completed` → "이미 완료됨" 안내 + 재실행 의사 확인

---

## 사용자 상호작용 3-패턴 (필수 준수)

이 스킬은 **3가지 상호작용 패턴**을 명확히 구분해서 사용합니다:

| 패턴 | 도구 | 사용 경우 |
|------|------|----------|
| **1. 선택지 질문** | `AskUserQuestion` | 선택지가 사전에 고정 (예: 직무, 톤 선호, 프리셋 적용 여부) |
| **2. 자유 입력** | 일반 텍스트 요청 | 사용자 고유값 (예: 이름, 회사명, 하루 일과) |
| **3. 작업 게이트** | "완료 입력" 대기 | 외부 작업 수행 대기 (예: 파일 넣기) |

**중요**: 3가지를 섞지 마세요. 이름 물을 때 AskUserQuestion에 빈 옵션 넣지 말고 일반 텍스트로 "이름을 알려주세요"라고 물어봅니다.

---

## Phase -1: 상태 체크 및 분기 (최우선)

**EXECUTE:** 커맨드 진입 즉시 `memory/state/onboarding.yaml`을 Read.

### 분기 규칙

**Case A — 파일 없음 또는 `status: not_started`**:
→ Phase 0 (시작 안내)로 진행

**Case B — `status: in_progress`**:
→ 다음 AskUserQuestion 호출:
```json
{
  "questions": [{
    "question": "이전에 Phase {N}까지 진행하셨어요. 어떻게 할까요?",
    "header": "재개",
    "options": [
      {"label": "이어서 하기 (추천)", "description": "Phase {N+1}부터 이어서 진행합니다. 이전 답변은 그대로 유지됩니다."},
      {"label": "처음부터 다시", "description": "모든 답변을 초기화하고 Phase 0부터 다시 시작합니다."},
      {"label": "취소", "description": "온보딩을 종료합니다. 진행 상태는 그대로 유지됩니다."}
    ],
    "multiSelect": false
  }]
}
```

**Case C — `status: completed` + `re_prompt_on_start: false`**:
→ 다음 AskUserQuestion 호출:
```json
{
  "questions": [{
    "question": "이미 온보딩이 완료되어 있어요 (profile: {profile}, applied_at: {applied_at}). 어떻게 할까요?",
    "header": "재온보딩",
    "options": [
      {"label": "취소 (추천)", "description": "온보딩을 다시 하지 않습니다. 대부분의 경우 이 선택이 맞습니다."},
      {"label": "일부만 수정 (Phase 1~2)", "description": "담당자 정보나 업무 맥락만 수정합니다. 폴더 프리셋은 건드리지 않습니다."},
      {"label": "폴더 프리셋 재설정", "description": "Phase 5만 다시 실행하여 폴더 프리셋을 바꿉니다. 기존 폴더는 유지됩니다."},
      {"label": "완전히 처음부터 다시", "description": "모든 상태를 초기화하고 Phase 0부터 다시 시작합니다. 주의: 이전 답변이 덮어씌워집니다."}
    ],
    "multiSelect": false
  }]
}
```

---

## Phase 0: 시작 안내

짧은 안내를 텍스트로 출력하고 바로 Phase 1로 진입합니다.

```
workmate 온보딩을 시작합니다.
몇 가지 답변만 하면 비서가 여러분을 이해하게 됩니다.

자주 쓰는 문서가 있다면 미리 `00-inbox/` 폴더에 넣어두시면
온보딩 중간에 함께 정리해드립니다.
```

---

## Phase 1: 사람 정보 수집

> **3-패턴 주의**: 이름/소속/보고 대상은 **자유 입력** (일반 텍스트 요청). 직무/직급은 **선택지 질문** (AskUserQuestion).

### Q1. 이름 (자유 입력)

텍스트로 출력:
```
이름을 알려주세요.
```
사용자 답변 대기. 받은 값을 `person.name`에 저장.

### Q2. 소속 (자유 입력)

텍스트로 출력:
```
소속(회사/부서)을 알려주세요.
```
받은 값을 `person.org`에 저장.

### Q3. 직무 (선택지 질문 — AskUserQuestion, 2단계)

**AskUserQuestion은 최대 4개 옵션 제약이 있으므로 2단계 질문으로 처리합니다.**

#### Q3-1: 직무 대분류

```json
{
  "questions": [{
    "question": "어떤 직무이신가요?",
    "header": "직무 분류",
    "options": [
      {"label": "제조 현장 직무", "description": "생산관리 / 품질·시험인증 / R&D·설계 / 구매·자재 중 하나"},
      {"label": "경영/영업 직무", "description": "경영지원(회계·법무·인사·수출입) / 영업·마케팅 중 하나"},
      {"label": "프로젝트·지식 관리", "description": "프로젝트 관리(DR/APQP/PPAP) / 기술문서·지식 관리 중 하나"},
      {"label": "기타 (직접 입력)", "description": "위 목록에 없는 직무이거나 여러 역할을 겸하는 경우. 직접 입력합니다."}
    ],
    "multiSelect": false
  }]
}
```

대분류에 따라 Q3-2 분기:
- **제조 현장 직무** → Q3-2a (생산/품질/R&D/구매 4지선다)
- **경영/영업 직무** → Q3-2b (경영지원/영업 2지선다)
- **프로젝트·지식 관리** → Q3-2c (프로젝트/지식 2지선다)
- **기타 (직접 입력)** → "직무를 알려주세요"라고 자유 입력 요청. 답변을 `person.role`에 저장, `profile: custom`

#### Q3-2a: 제조 현장 직무 선택

```json
{
  "questions": [{
    "question": "제조 현장 직무 중 어떤 쪽인가요?",
    "header": "현장 직무",
    "options": [
      {"label": "생산관리", "description": "생산계획, 공정조건표, PFMEA, Control Plan, 설비 관리, 생산일보, 4M 변경"},
      {"label": "품질 / 시험인증", "description": "IQC/IPQC/OQC 검사, NCR/CAPA/8D, SPC, 신뢰성 시험, KC/UL/CE 인증, RoHS/REACH, 안전/환경"},
      {"label": "R&D / 설계", "description": "CAD/BOM/도면, 시제품, 금형(T1/T2/T3), CMF, 설계 변경(ECN/ECO), FEA/CFD 해석"},
      {"label": "구매 / 자재", "description": "PR/PO 발주, 견적 비교, 납품서, 재고/MRP, LOT 추적, 공급업체 평가, 납기 관리"}
    ],
    "multiSelect": false
  }]
}
```

#### Q3-2b: 경영/영업 직무 선택

```json
{
  "questions": [{
    "question": "경영/영업 직무 중 어떤 쪽인가요?",
    "header": "경영/영업",
    "options": [
      {"label": "경영지원 (총무·인사·법무·회계)", "description": "세금계산서·결산·원가, 계약서·NDA, 교육·안전·KRAS, 수출입·B/L·통관"},
      {"label": "영업 / 마케팅", "description": "카탈로그·제안서·판매견적, 수주·매출 관리, 고객 요구사항, 고객 클레임 대응"}
    ],
    "multiSelect": false
  }]
}
```

#### Q3-2c: 프로젝트/지식 관리 선택

```json
{
  "questions": [{
    "question": "어떤 쪽인가요?",
    "header": "프로젝트/지식",
    "options": [
      {"label": "프로젝트 관리", "description": "WBS/간트, DR1/2/3 회의록, DFMEA, APQP/PPAP, DVP&R, 이슈 관리, Lessons Learned"},
      {"label": "기술문서 / 지식 관리", "description": "부품 데이터시트, 장비 매뉴얼, SOP, 제품 사양서, Teardown 벤치마크, 특허·논문"}
    ],
    "multiSelect": false
  }]
}
```

#### profile 매핑 (최종값)

| 사용자 선택 (Q3-2) | profile 값 | 참조할 프리셋 |
|------|-----|---------|
| 생산관리 | `production-control` | §1 |
| 품질 / 시험인증 | `quality` | §2 |
| R&D / 설계 | `rnd-design` | §3 |
| 구매 / 자재 | `procurement` | §4 |
| 경영지원 | `admin` | §5 |
| 영업 / 마케팅 | `sales` | §6 |
| 프로젝트 관리 | `project-mgmt` | §7 |
| 기술문서 / 지식 관리 | `knowledge` | §8 |
| 기타 (직접 입력) | `custom` | 문서 기반 자동 생성 |

`person.role`에는 사용자가 선택한 원문 라벨(예: "생산관리")을 저장, `profile`에는 위 코드 값을 저장.

### Q4. 직급 (선택지 질문)

```json
{
  "questions": [{
    "question": "직급을 알려주세요.",
    "header": "직급",
    "options": [
      {"label": "사원", "description": ""},
      {"label": "대리", "description": ""},
      {"label": "과장", "description": ""},
      {"label": "차장/부장/임원", "description": "관리자급"}
    ],
    "multiSelect": false
  }]
}
```
`person.rank`에 저장.

### Q5. 보고 대상 (자유 입력)

텍스트로 출력:
```
보고를 받으시나요, 올리시나요? 올리는 쪽이라면 누구에게 올리는지 알려주세요.
```
`person.reports_to`에 저장.

---

## Phase 2: 업무 맥락 수집

### Q6. 반복 업무 (자유 입력)

텍스트로 출력:
```
매일 또는 매주 반복적으로 하시는 업무 중에 가장 시간이 오래 걸리는 것이 무엇인가요?
```

### Q7. 보고 주기 (선택지 질문)

```json
{
  "questions": [{
    "question": "주된 보고 주기는 어떻게 되나요?",
    "header": "보고 주기",
    "options": [
      {"label": "일일 + 주간", "description": "매일 마감 보고 + 주간 회의"},
      {"label": "주간", "description": "주간 보고만"},
      {"label": "월간", "description": "월간 보고 중심"},
      {"label": "수시", "description": "정기 주기 없이 필요할 때"}
    ],
    "multiSelect": false
  }]
}
```
`person.reporting_cycle`에 저장.

### Q8. 답변 톤 (선택지 질문)

```json
{
  "questions": [{
    "question": "AI 비서가 답변할 때 어떤 스타일이 좋으세요?",
    "header": "톤",
    "options": [
      {"label": "결론 먼저, 표·숫자 위주 (추천)", "description": "바쁜 실무자용. 판단 근거를 표와 숫자로 먼저 제시하고 설명은 최소화."},
      {"label": "상세하게, 근거와 함께", "description": "원인 분석이나 교육 상황에 적합. 설명이 길어집니다."},
      {"label": "대화하듯 편하게", "description": "짧고 부드럽게. 격식 없이."},
      {"label": "간결하게 핵심만", "description": "한두 문장으로 끝. 추가 설명 없음."}
    ],
    "multiSelect": false
  }]
}
```
`person.tone`에 저장.

### Q9. 금지사항 (자유 입력, 선택)

텍스트로 출력:
```
"이렇게는 하지 마라"는 것이 있으면 알려주세요. 없으면 "없음"이라고 답해주세요.
```
`person.forbid`에 저장. "없음"이면 null.

Phase 2 완료 시 state 중간 저장 + `last_phase_completed: 2` 기록.

---

## Phase 3: 실제 자료 연결 (🆕 핵심)

### Step 1: 안내 + 예시 제시 (텍스트 출력)

```
이제 {이름}님이 자주 쓰시는 문서를 연결해볼게요.

`00-inbox/` 폴더에 자주 쓰는 문서 2~4개를 넣어주세요.
직무가 "{role}"이시니까 이런 문서들이 좋습니다:

[role별 동적 예시]
- 생산관리: 일일 생산 보고 1개, 주간 생산회의 PPT 1개, 생산 실적 엑셀 1개
- 품질관리: 최근 불량 대책서 1개, 입고검사 성적서 1개, Control Plan 1개
- R&D / 설계: 최근 DR 회의록 1개, BOM 1개, ECN 1개
- 구매 / 자재: 최근 발주서 1개, 견적비교표 1개, 재고현황표 1개
- 경영지원: 직무기술서 1개, 월간 결산 1개
- 영업 / 마케팅: 최근 제안서 1개, 수주 현황 1개
- 공통: 주간업무보고 1개, SOP 1개

📁 폴더 경로: workmate/00-inbox/
💡 Finder에서 드래그앤드롭으로 복사하시면 됩니다.
🔒 걱정 마세요 — 로컬에서만 처리됩니다.

파일을 넣으신 후 "완료"라고 답해주세요.
파일이 없거나 건너뛰고 싶으시면 "건너뛰기"라고 답해주세요.
```

### Step 2: 완료 게이트 대기 (3-패턴의 "작업 게이트")

**허용 응답**:
- "완료", "완", "다 넣었어", "ㅇㅇ", "ok", "OK", "네", "했어", "했어요", "done", "끝" → Step 3 진행
- "건너뛰기", "스킵", "skip", "나중에" → Phase 4로 점프 (inbox-sorter 호출 생략)
- "아직", "잠깐" → 게이트 유지, 재대기
- 기타 (다른 질문) → "먼저 파일을 00-inbox/에 넣고 '완료'라고 답해주세요. 나중에 하시려면 '건너뛰기'"

### Step 3: inbox-sorter 스킬 호출

`00-inbox/` 폴더 확인:
```bash
ls -1 ./00-inbox/ 2>/dev/null | grep -v '^\.'
```

**Case A — 비어 있음**:
```
00-inbox/에 파일이 없네요. Phase 4로 넘어갈게요. 
나중에 언제든 파일을 넣고 /inbox-sorter를 실행하실 수 있어요.
```
→ Phase 4로 진행

**Case B — 파일 있음**:
`Skill` 도구로 inbox-sorter 스킬 호출:
```
Skill(name="inbox-sorter", args="ONBOARDING_MODE")
```

`ONBOARDING_MODE`가 전달되면 inbox-sorter는:
- 평소처럼 분류 수행
- 결과를 `memory/state/onboarding-inbox-snapshot.json`에 저장
- 완료 메시지에 "→ 온보딩 Phase 4로 돌아갑니다" 꼬리말 추가

**Case C — 실행 실패**:
```
파일 정리 중에 문제가 생겼어요: {error}
괜찮아요, Phase 4로 그냥 넘어갈게요. 나중에 /inbox-sorter로 다시 시도할 수 있어요.
```
→ Phase 4로 진행, state에 `inbox_sorter.status: failed` 기록

Phase 3 완료 시 state 저장 + `last_phase_completed: 3` 기록.

---

## Phase 4: 직무 기준 재해석 + references 자동 생성

### Step 1: snapshot 읽기 (있으면)

```bash
cat ./memory/state/onboarding-inbox-snapshot.json 2>/dev/null
```

없으면 Phase 3에서 스킵했거나 inbox-sorter가 실패한 경우 → Step 2로 넘어가되 "자료 없이 직무만으로 해석"

### Step 2: 문서 기반 업종·직무 파악 + 재해석

**inbox-sorter가 분류한 파일들을 실제로 읽어서** 업종과 직무를 파악합니다.

1. 분류된 폴더 구조 확인 (Glob)
2. 대표 파일 2~3개 Read (컬럼 구조, 용어, 지표 파악)
3. Phase 1에서 받은 직무 정보 + 문서 내용을 종합해서 업종·직무 재해석

해석 초안 출력 예시:
```
📋 {이름}님을 이렇게 이해했어요:

업종: {문서에서 파악한 업종 — 제조/커머스/IT/금융 등}
직무: {직무 상세}

주로 다루시는 데이터:
- {파일1}: {컬럼 구조 요약}
- {파일2}: {컬럼 구조 요약}

이 워크스페이스에서 먼저 시켜볼 만한 일 3가지:
1. {업종·직무 맞춤 추천 작업 1}
2. {업종·직무 맞춤 추천 작업 2}
3. {업종·직무 맞춤 추천 작업 3}
```

### Step 3: 확인 게이트 (AskUserQuestion)

```json
{
  "questions": [{
    "question": "이 해석이 맞으신가요?",
    "header": "해석 확인",
    "options": [
      {"label": "맞아요 (추천)", "description": "이 해석대로 references를 생성하고 Phase 5로 넘어갑니다."},
      {"label": "조금 다른데", "description": "어떤 부분이 다른지 알려주세요. 수정 후 다시 제안합니다."},
      {"label": "더 물어봐주세요", "description": "추가로 확인하고 싶은 게 있으면 말씀해주세요."}
    ],
    "multiSelect": false
  }]
}
```

"조금 다른데" 선택 시 → 자유 입력으로 수정 사항 받고 Step 2 재실행.

### Step 4: references 자동 생성 (승인 후)

파악된 업종·직무·문서 내용을 기반으로 `references/` 폴더에 4개 파일을 Write합니다.

**`references/기준값.md`** — 업종별 핵심 KPI 정상/주의/경고 기준
- 문서에서 발견한 지표(매출, 달성률, 불량률, 전환율, SLA 등)를 기반으로 생성
- 문서에 구체적 수치가 있으면 그걸 사용, 없으면 업종 일반 기준으로 초안 작성 후 "이 기준값이 맞는지" 확인 요청

**`references/용어집.md`** — 팀 내부 용어, 약어, 코드 체계
- 문서에 나온 약어, 코드, 내부 용어를 자동 추출
- "다른 용어가 있으면 알려주세요" 요청

**`references/보고서양식.md`** — 보고서 작성 시 따를 구조
- 문서에서 기존 보고서 패턴이 보이면 그 구조를 추출
- 없으면 직무별 일반 양식으로 초안

**`references/프로세스.md`** — 주요 업무 프로세스
- 문서에서 파악한 반복 업무 흐름을 정리

### Step 5: 추가 자료 요청 (선택)

references를 생성하면서 부족한 정보가 있으면 사용자에게 요청:
```
references를 만들었어요. 더 정확하게 하려면 아래 문서도 있으면 좋습니다:

- {부족한 자료 1}: 예) "KPI 목표 기준표가 있으면 기준값.md가 더 정확해집니다"
- {부족한 자료 2}: 예) "팀 내 약어 목록이 있으면 용어집이 풍부해집니다"

00-inbox/에 넣고 "완료"라고 답해주시거나, "건너뛰기"로 넘어가세요.
```

추가 자료가 들어오면 → 해당 references 파일 Edit으로 보강.
"건너뛰기"면 → 현재 상태로 Phase 5 진행.

Phase 4 완료 시 state 저장 + `last_phase_completed: 4` 기록.

---

## Phase 5: 직무 맞춤 폴더 프리셋 제안 (🆕)

### Step 1: 프리셋 읽기

`references/직무별-폴더프리셋.md`를 Read하여 해당 직무 섹션의 폴더 구조 추출.

### Step 2: 제안 출력 (텍스트)

```
{role} 직무 기준으로 아래 폴더를 추가하면 더 잘 맞습니다:

[프리셋 폴더 목록]
- 20-production/logs/       (생산일보, 가동 현황)
- 20-production/plan/       (생산 계획, 작업지시)
...

💡 이건 제안이고, 언제든 이름을 바꾸거나 지울 수 있어요.
💡 이미 있는 폴더는 그대로 둡니다 (덮어쓰지 않음).
```

### Step 3: 적용 여부 (AskUserQuestion)

```json
{
  "questions": [{
    "question": "이 폴더 프리셋을 적용할까요?",
    "header": "프리셋 적용",
    "options": [
      {"label": "적용 (추천)", "description": "위 폴더를 모두 생성합니다. 기존 파일은 그대로 유지됩니다."},
      {"label": "건너뛰기", "description": "폴더를 만들지 않습니다. 나중에 수동으로 만들거나 /onboarding --preset-reset으로 다시 제안받을 수 있어요."},
      {"label": "일부만 적용", "description": "어떤 폴더만 만들지 알려주세요."}
    ],
    "multiSelect": false
  }]
}
```

### Step 4: 폴더 생성 (승인 시)

```bash
mkdir -p 20-production/logs 20-production/plan ...
```

생성된 폴더 목록을 `folder_preset.created_folders`에 저장.
`folder_preset.applied: true`, `folder_preset.version: v1`, `folder_preset.applied_at: {today}` 기록.

**중요**: 재제안 차단을 위해 `re_prompt_on_start: true`로 설정 (다음 실행 시 Phase 5 스킵).

Phase 5 완료 시 state 저장 + `last_phase_completed: 5` 기록.

---

## Phase 6: 상태 저장

### Step 1: CLAUDE.md 담당자 섹션 업데이트

`CLAUDE.md`의 `## 담당자` 섹션을 Edit로 업데이트.

현재 placeholder 형식:
```markdown
- **이름**: _(미설정)_
- **소속**: _(미설정)_
...
```

각 필드를 개별 Edit 호출로 치환:
```
Edit(file_path="...CLAUDE.md", 
     old_string="- **이름**: _(미설정)_", 
     new_string="- **이름**: {person.name}")
```

**재온보딩 시 주의**: 이미 값이 채워진 상태라면 `old_string`이 `_(미설정)_`이 아니라 실제 값이므로, Read로 현재 값을 먼저 확인 후 동적으로 `old_string` 결정.

10개 필드 모두 업데이트 (이름, 소속, 직무, 직급, 보고 대상, 보고 주기, 커뮤니케이션 선호, 주요 반복 업무, 주의사항, 팀 내 용어).

### Step 2: memory/wiki에 기록

**`memory/wiki/preferences/응답-스타일.md`** (신규 또는 업데이트):
```markdown
---
title: 응답 스타일
category: preferences
created: {today}
updated: {today}
tags: [톤, 금기]
status: active
---

# 응답 스타일

## Summary
{person.name}님이 선호하는 답변 톤과 금기사항.

## Detail
- **톤**: {person.tone}
- **금지사항**: {person.forbid}

## Changelog
- {today}: /onboarding에서 수집
```

**`memory/wiki/domain-context/담당자-프로필.md`** (신규 또는 업데이트):
```markdown
---
title: 담당자 프로필
category: domain-context
created: {today}
updated: {today}
tags: [담당자, {role}]
status: active
---

# 담당자 프로필

## Summary
{person.name} ({person.rank}), {person.org}, {role}

## Detail
- **이름**: {person.name}
- **소속**: {person.org}
- **직급**: {person.rank}
- **직무**: {role}
- **보고 대상**: {person.reports_to}
- **보고 주기**: {person.reporting_cycle}
- **주요 반복 업무**: {반복 업무}

## Changelog
- {today}: /onboarding에서 수집
```

**`memory/MEMORY.md`**의 인덱스에 위 2개 페이지 행 추가.

### Step 3: state 파일 최종 저장

`memory/state/onboarding.yaml`:
```yaml
status: completed
last_phase_completed: 6
profile: {role}
person: {...}
folder_preset:
  applied: {true/false}
  ...
re_prompt_on_start: true
```

### Step 4: 완료 메시지

```
✅ 온보딩 완료!

{person.name}님, 이제 저는 당신의 workmate입니다.

저장된 정보:
- CLAUDE.md 담당자 섹션
- memory/wiki/preferences/응답-스타일.md
- memory/wiki/domain-context/담당자-프로필.md
- memory/state/onboarding.yaml

확인해보세요: "너는 누구야?" 라고 물어보시면 제가 자기소개해드릴게요.

폴더 프리셋을 바꾸고 싶으시면 `/onboarding --preset-reset` 실행해주세요.
```

---

## 탈출구 옵션

| 옵션 | 동작 |
|------|------|
| `/onboarding --reset` | state 완전 초기화 → Phase 0부터 |
| `/onboarding --preset-reset` | Phase 5만 단독 재실행 (프리셋 재제안) |
| `/onboarding --edit` | Phase 1~2만 재실행 (담당자 정보 수정) |

커맨드 인수에 `--reset`, `--preset-reset`, `--edit`이 포함되면 해당 모드로 진입.

---

## 에러 핸들링

### inbox-sorter 실패
- 로그 남기고 Phase 4로 진행 (state에 `inbox_sorter.status: failed`)
- 사용자에게 "괜찮아요, 나중에 다시" 안내

### CLAUDE.md Edit 실패
- Phase 6 진입 전 `CLAUDE.md.bak-{timestamp}` 백업 생성
- Edit 실패 감지 시:
  1. 백업 복구
  2. memory/wiki/에는 이미 저장되었음 확인
  3. 사용자에게 수동 패치 블록 출력:
     ```
     CLAUDE.md 편집에 실패했어요. 아래 블록을 직접 붙여넣어 주세요:
     
     ## 담당자
     - **이름**: {name}
     ...
     ```

### YAML state 쓰기 실패
- 사용자 답변을 텍스트로 출력하고 "복사해두세요" 안내
- state 없이도 온보딩 완료는 가능 (CLAUDE.md 편집만 성공하면 OK)

### 세션 중단
- 각 Phase 완료 시마다 state 중간 저장
- 재시작 시 "Phase {N}까지 진행됨, 이어서 할까요?" 분기

---

## Integration Points

- **inbox-sorter**: Phase 3에서 `ONBOARDING_MODE`로 호출, snapshot JSON 교환
- **memory/wiki/**: Phase 6에서 preferences, domain-context 카테고리에 위키 페이지 생성
- **CLAUDE.md**: Phase 6에서 `## 담당자` 섹션 Edit
- **references/직무별-문서유형.md**: Phase 4 재해석 시 Read
- **references/직무별-폴더프리셋.md**: Phase 5 프리셋 제안 시 Read (skill 내부 references/)

---

## Eval 시나리오

### should-trigger (반드시 이 스킬 호출)
1. "처음 세팅 도와줘"
2. "내 비서로 만들어줘"
3. "/onboarding"
4. "나한테 맞게 workmate 바꿔줘"

### should-not-trigger (다른 스킬이 맞음)
1. "파일 정리해줘" → inbox-sorter
2. "데이터 분석해줘" → data-analyst
3. "보고서 써줘" → content-draft
