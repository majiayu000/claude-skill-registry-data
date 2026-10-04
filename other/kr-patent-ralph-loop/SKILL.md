---
name: kr-patent-ralph-loop
description: 한국 특허 명세서 반복 정제 루프 — 결함이 0이 될 때까지 consistency-check → 결함 분류 → 해당 Stage 스킬 재호출 또는 inline 수정 → 재 consistency-check 사이클을 자동 반복하여 수렴시키는 메타 오케스트레이터. 매 iteration 시작 시 청구범위 백업·종료 시 diff=0 검증으로 신규사항 추가 금지 원칙을 강제. 종료 조건은 기본 0 Priority A (또는 엄격 모드 시 0 Priority A+B). 최대 5회 반복 안전 캡(사용자 조정 가능). 결함 → 수정 전략은 J섹션 Stage 라우팅을 활용하여 (Stage 2 결함 → symbol-design/drawing-mapping, Stage 3 결함 → spec-drafting 해당 단계, Stage 4 결함 → definition-insertion/embodiment-addition) 자동 분기. 각 iteration의 결함 수·적용 수정·청구범위 무결성·종료 여부를 로그 표로 산출하며 수렴 실패 시 잔존 결함 + 사용자 결정 요청. "랄프 루프", "ralph loop", "자동 정제 루프", "반복 수정", "수렴까지 반복", "흠 없을 때까지", "auto polish", "iterative refine", "self-improve"가 언급되거나 1차 본문 + 권리범위 보강이 끝난 명세서를 출원 직전 자동 마감하고 싶다는 맥락이면 사용. consistency-check만으로는 미흡한 자동화 단계를 1단계 위로 끌어올리는 출원 전 마지막 자동 게이트.
---

# 한국 특허 명세서 랄프 루프 — 반복 정제 자동 수렴

## [역할]

당신은 한국 특허 명세서를 **결함이 0이 될 때까지 반복 정제**하는 메타 오케스트레이터다. `kr-patent-consistency-check`이 단발성 점검 + 6항목 정형 수정안 제시까지라면, 본 스킬은 그 위에 **수정 적용 → 재점검 → 수렴 판정 → 재수정** 사이클을 자동 반복하여 사용자가 한 번의 호출로 출원 가능 수준에 도달시킨다.

**입력**: 1차 본문 + 권리범위 보강(Stage 3, 4)이 끝난 명세서 docx/텍스트, 청구항 원문, 도면 파일들
**출력**: 0결함 명세서 + iteration 로그 + 청구범위 무결성 증명 + 잔존 결함(수렴 실패 시)

---

## 종료 조건 (수렴 판정)

| 모드 | 조건 |
|---|---|
| **기본** (default) | Priority A 결함 0개 |
| **엄격** (strict) | Priority A 결함 0개 **AND** Priority B 결함 0개 |
| **완전** (perfect) | Priority A + B + C 모두 0개 (실무적으로 도달 어려움 — 비추천) |

호출 시 사용자가 모드 미지정이면 **기본 모드**로 진행하고, 1차 iteration 완료 후 사용자에게 "엄격 모드로 계속할까요?" 묻는다.

### 안전 캡

- **최대 반복**: 5회 (사용자가 명시적으로 늘리지 않는 한)
- **반복 간 결함 감소 정체 시 조기 종료**: 직전 iter와 현재 iter의 결함 수가 동일하면 "수정이 결함을 해결하지 못함" 경고 + 사용자 결정 요청
- **청구범위 변경 감지 시 즉시 중단**: 어느 iter에서든 청구범위 섹션이 입력 청구항과 1글자라도 달라지면 즉시 사이클 중단하고 사용자에게 alert (신규사항 추가 금지 원칙)

---

## 청구범위 read-only 보호 (★★★ 최우선 안전장치)

매 iteration의 **시작·종료 시점**에 청구범위 무결성을 강제 검증한다.

```
[Iteration N 시작]
  ① 입력 명세서에서 【청구범위】 섹션 텍스트 추출 → CLAIMS_N_BEFORE
  ② CLAIMS_N_BEFORE ↔ CLAIMS_0 (최초 입력 청구항) diff
     - diff ≠ 0 이면 즉시 중단, 사용자 alert
[수정 적용]
[Iteration N 종료]
  ③ 수정 후 명세서에서 【청구범위】 섹션 텍스트 추출 → CLAIMS_N_AFTER
  ④ CLAIMS_N_AFTER ↔ CLAIMS_0 diff
     - diff ≠ 0 이면 즉시 청구범위 원상복구 + 사용자 alert
     - 어떤 수정이 청구범위를 건드렸는지 역추적 보고
```

**위반 시 동작**:
- 자동 원상복구: 【청구범위】 섹션만 CLAIMS_0으로 덮어쓰기 (본문은 보존)
- 어느 수정 단계가 청구범위를 건드렸는지 로그 (보통 embodiment-addition 오작동)
- 해당 수정은 무효화하고 다음 iter로 진행

---

## 결함 → 수정 라우팅 표

consistency-check이 산출하는 J섹션(Stage 역추적) 결과 + Priority 분류를 보고 어느 도구로 어떻게 수정할지 자동 결정한다.

### Stage 2 결함 (부호 설계)

| 결함 패턴 | 수정 방법 | 호출 스킬 |
|---|---|---|
| 계층 넘버링 미준수 (100→210 비계층) | 부호 체계 재설계 | kr-patent-symbol-design |
| 동일 부호 두 객체 지칭 (Priority A) | 한 부호에 새 번호 할당 + 본문 일괄 치환 | kr-patent-symbol-design + inline replace |
| 도면 박스 부호 1:1 매핑 누락 | 도면 이미지 OCR + 박스별 부호 부여 | kr-patent-drawing-mapping |
| 부재번호 흐름 정합성 결함 | 처리 결과 객체에 새 부호 분리 | kr-patent-symbol-design |

### Stage 3 결함 (1차 본문)

| 결함 패턴 | 수정 방법 | 호출 스킬 |
|---|---|---|
| S4 청구항 전수 매핑 빈칸 (Priority A ★★★) | 누락된 청구항을 4종 도입 정형으로 풀어쓰기 추가 | kr-patent-spec-drafting S4 부분 재호출 |
| S13 "청구항 X" / "단계 SXXX" 직접 언급 | 해당 표현을 추상화된 본문 서술로 치환 | inline edit |
| S13 내부 작성 로직 노출 | 메모성 표현 삭제 | inline edit |
| S2 마지막 문단 정형 누락 | 정형 문구 삽입 | inline edit |
| S5 효과 3단 인과 부재 | 각 효과를 구조→메커니즘→이점으로 재구성 | kr-patent-spec-drafting S5 부분 재호출 |
| 금지 표현 ("종래", "구성되는", 슬래시) | 대체 표현으로 일괄 치환 | inline edit |
| 띄어쓰기 변형 ("지식그래프"/"지식 그래프") | 한 형태로 통일 | inline edit |
| "상기" 본문 남용 | 도면부호 활용 표현으로 치환 (예외 적용) | inline edit |
| 의미 비약·전문용어 풀이 누락 | 정형 풀이 단락 삽입 | inline edit |
| 수식 정의 정형 누락 | "여기에서, ~은(는) ~을 의미한다" 단락 삽입 | inline edit |
| 브릿지 문장 정형 미준수 | 정형 문구로 치환 | inline edit |
| 문장 4줄 초과 | 절 단위 분리 | inline edit |

### Stage 4 결함 (권리범위 보강)

| 결함 패턴 | 수정 방법 | 호출 스킬 |
|---|---|---|
| **청구범위 read-only 위반 (Priority A ★★★)** | 즉시 청구범위 섹션 CLAIMS_0으로 원상복구 | 자동 (스킬 호출 없음) |
| 자체 사전 정의 단락 부족 | 청구항 한정 용어에 자체 정의 인라인 삽입 | kr-patent-definition-insertion |
| 정의 4원칙 부분 누락 | 동의어 방어망·비제한적 예시 보강 | kr-patent-definition-insertion |
| 변형 실시예 도입어 변주 부족 | "한편/또 다른 실시예/나아가" 도입어 다양화 | kr-patent-embodiment-addition |
| 16카테고리 변형 6개 미만 | 추가 카테고리 변형 실시예 부가 | kr-patent-embodiment-addition |

### 라우팅 우선순위

한 iteration에서 여러 결함이 동시 발견되면 다음 순서로 처리:

1. **청구범위 read-only 위반** (즉시 원상복구 + 그 iter 종료)
2. **Priority A 모두**
3. **Priority B 모두** (엄격 모드 시)
4. **Priority C** (완전 모드 시)

같은 Priority 안에서는 **Stage 2 → Stage 3 → Stage 4** 순서(상류 먼저 고정). 부호가 안정되어야 본문 정합이 의미 있고, 본문이 안정되어야 권리범위 보강이 의미 있다.

---

## 작업 순서

### Step 1. 초기화 (Iteration 0)

- 입력 명세서 텍스트 추출
- 【청구범위】 섹션 추출 → `CLAIMS_0` 변수에 저장 (불변 기준)
- 도면 파일·청구항 원문 확인
- 사용자에게 모드 선택 받기 (기본 / 엄격 / 완전) — 응답 없으면 기본
- 사용자에게 최대 반복 횟수 확인 — 응답 없으면 5

### Step 2. Iteration N 진입 — 청구범위 무결성 사전 검증

```python
CLAIMS_N_BEFORE = extract_claims_section(current_spec)
if diff(CLAIMS_N_BEFORE, CLAIMS_0) != 0:
    halt("청구범위가 입력과 달라짐 — 이전 iter에서 손상됨, 즉시 alert")
```

### Step 3. consistency-check #N 호출

`kr-patent-consistency-check` 스킬을 호출하여 보고서 산출:
- Stage 역추적 표 (J섹션)
- Priority A/B/C 결함 리스트 + 6항목 정형
- 종합 점수

### Step 4. 수렴 판정

```
if mode == 기본 and Priority_A_count == 0:
    → 수렴 → Step 8 종료 단계로
if mode == 엄격 and Priority_A_count == 0 and Priority_B_count == 0:
    → 수렴 → Step 8 종료 단계로
if mode == 완전 and all_count == 0:
    → 수렴 → Step 8 종료 단계로
if N == max_iterations:
    → 수렴 실패 → Step 9 잔존 결함 보고로
if defect_count_N == defect_count_(N-1):
    → 정체 감지 → 사용자에게 "수정이 결함을 해결하지 못함, 계속할까요?" 묻기
else:
    → Step 5로
```

### Step 5. 결함 라우팅

위 "결함 → 수정 라우팅 표"에 따라 각 결함을 분류하고 적용 순서(청구범위 보호 → Priority A → Stage 2 → 3 → 4) 결정.

### Step 6. 수정 적용

라우팅된 도구를 순차 호출:
- **inline edit**: 직접 텍스트 치환 (정형 위반·금지어·"상기"·슬래시·띄어쓰기 등)
- **상류 스킬 재호출**: 해당 Stage의 부분 재실행 (symbol-design / spec-drafting / definition-insertion / embodiment-addition)

각 수정 적용 후 차이를 diff로 보존 (이터레이션 로그용).

### Step 7. Iteration N 종료 — 청구범위 무결성 사후 검증

```python
CLAIMS_N_AFTER = extract_claims_section(modified_spec)
if diff(CLAIMS_N_AFTER, CLAIMS_0) != 0:
    # 청구범위가 손상됨
    rollback_claims_section(modified_spec, CLAIMS_0)
    log("Iteration N에서 청구범위 손상 발견 — 본문은 유지하고 청구범위만 원상복구")
    log("손상 원인: <어느 수정 단계가 청구범위를 건드렸는지>")
```

→ Step 2로 돌아가 Iteration N+1 진입.

### Step 8. 수렴 종료 — 최종 산출물

- 최종 명세서 텍스트
- Iteration 로그 표 (아래 형식)
- 청구범위 무결성 증명: `diff(CLAIMS_final, CLAIMS_0) == 0` ✅
- Stage 역추적 최종 결과: 모든 Stage ✅
- 다음 단계 권장: kr-patent-docx-builder (최종 docx 출력)

### Step 9. 수렴 실패 종료 — 잔존 결함 보고

최대 반복 도달 또는 정체 감지로 수렴 실패 시:
- 잔존 결함 리스트 (Priority A/B/C 분류)
- 각 결함에 대해 자동 수정이 실패한 이유 분석
- 사용자에게 결정 요청:
  1. 잔존 결함 수동 수정 후 재호출
  2. 최대 반복 늘리고 계속
  3. 현재 상태로 종료 (잔존 결함 감수)

---

## Iteration 로그 형식

매 iteration 종료 시 다음 표를 누적 업데이트:

```markdown
## 🔁 Ralph Loop Iteration 로그

| Iter | 진입 시각 | Priority A | Priority B | Priority C | 적용 수정 (요약) | 청구범위 무결성 | 종료 여부 |
|---|---|---|---|---|---|---|---|
| 0 | 00:00:00 | 7 | 12 | 18 | (초기 점검) | ✅ | 진행 |
| 1 | 00:02:14 | 3 | 10 | 18 | S4 매핑 추가, 금지어 치환 | ✅ | 진행 |
| 2 | 00:04:01 | 1 | 8 | 17 | S13 직접 언급 제거, 정의 보강 | ✅ | 진행 |
| 3 | 00:05:48 | 0 | 6 | 16 | 부재번호 흐름 정합 | ✅ | **수렴 (기본)** |

## 종합 결과
- 최종 결함: A 0 / B 6 / C 16
- 청구범위 무결성: ✅ diff = 0
- 다음 단계 권장: kr-patent-docx-builder
- 엄격 모드 시 추가 처리 필요: B 6건 (사용자 결정)
```

---

## 호출 형식 (사용 예시)

```
사용자: "이 명세서 랄프 루프 돌려줘" / "흠 없을 때까지 자동 수정해줘" / "ralph loop strict"

랄프 루프:
1. 모드 확인 (응답 없으면 기본)
2. 최대 반복 확인 (응답 없으면 5)
3. Iteration 0 실행 → 점검 보고서 + 로그 표 시작
4. 수렴까지 반복 또는 사용자 결정 지점에서 일시 정지
5. 최종 산출물 + 로그 표 + 다음 단계 권장
```

---

## 안전·비용 고려사항

| 항목 | 정책 |
|---|---|
| **청구범위 손상** | 매 iter 무결성 검증 + 자동 원상복구. 절대 신규사항 추가 안 됨 |
| **무한 루프 방지** | 최대 5회 + 정체 감지 (2회 연속 결함 수 동일 시 사용자 결정) |
| **비용** | Opus 4.7 기준 1 iter ≈ $0.5~1 (consistency-check + 수정 적용). 5회 풀로 돌리면 $3~5. 사용자에게 사전 고지 |
| **사용자 개입 지점** | (1) 모드 선택, (2) 정체 감지 시, (3) 청구범위 손상 감지 시, (4) 수렴 실패 종료 시 |
| **부분 수정 모드** | 사용자가 "Priority A만 자동, B/C는 수동" 식으로 범위 제한 가능 |
| **dry-run 모드** | 실제 수정 적용 없이 어떤 수정이 일어날지만 시뮬레이션 (옵션) |

---

## kr-patent-full-workflow와의 관계

- **full-workflow**: 처음부터 끝까지 단방향 — IDS → 명세서 → docx 출력. 각 단계 1회 실행.
- **ralph-loop**: 완성된 명세서에 대한 **출원 직전 자동 마감** — 폐쇄 루프로 결함 0까지 수렴.

호출 시점:
- full-workflow Stage 5 (consistency-check) 자리에 **선택적으로 ralph-loop 삽입 가능**
- 또는 외부 변리사 명세서를 받아 출원 전 자동 정제할 때 단독 호출

---

## 트러블슈팅

| 증상 | 원인 | 대응 |
|---|---|---|
| 청구범위가 매 iter 손상됨 | embodiment-addition이 청구범위를 잘못 인식 | embodiment-addition 호출 자체를 비활성화 + inline edit만으로 진행 |
| Priority A가 줄지 않음 | S4 청구항 매핑 누락이 spec-drafting 재호출로도 보강 안 됨 | 청구항 원문 자체에 모호성 — 사용자에게 청구항 검토 요청 |
| 결함이 늘어남 (역행) | 수정이 새 결함 유발 | 직전 iter 상태로 롤백 + 해당 수정 비활성화 |
| 5회 모두 소진 | 결함 패턴이 자동 수정으로 풀리지 않음 | 잔존 결함을 사용자에게 6항목 정형으로 보고하고 수동 수정 안내 |

---

## 누적 학습 항목 (컴파운딩 루프)

- (2026-05-27 신설) 사용자 요청으로 신규 스킬 도입. consistency-check이 단발성 게이트라면 ralph-loop은 자동 수렴 게이트. 매 iter 청구범위 무결성 검증을 ★★★ 최우선 안전장치로 설계 — 한국 특허 신규사항 추가 금지 원칙(메모리 [[feedback_kr_patent_claims_readonly]])이 이 스킬의 근본 제약.
- 결함 → 수정 라우팅은 consistency-check의 J섹션(Stage 역추적) 결과를 그대로 활용. J섹션이 만들어진 직후 본 스킬이 자연스럽게 가능해졌음 — 두 스킬은 강한 짝(pair).
- (2026-05-27, 사건 A 첫 사용) 검증 정규식의 한국어 조사 매칭 누락이 false negative의 주된 원인. 검증식 작성 시 `[은는이가을를]` 등 명시. 또한 점검 영역에서 【부호의 설명】·【청구범위】·【요약서】는 본문 룰 적용 대상에서 자동 제외해야 false positive를 막을 수 있음.
