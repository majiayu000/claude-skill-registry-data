---
name: autoresearch
description: >
  Karpathy의 autoresearch 패턴을 스킬 프롬프트 최적화에 적용.
  체크리스트(3~6개 예/아니오 기준) 기반 hill-climbing 루프로
  SKILL.md를 자동 개선합니다. 한 번에 하나만 바꾸고, 채점하고,
  유지하거나 되돌립니다. 95%+ × 3회 연속 달성 시 종료.
  최종 합격은 라운드에 쓰지 않은 holdout 입력으로 독립 채점합니다.
  기본 설치에서는 카탈로그의 source-only 원본을 직접 읽고, 전체 활성화 설치에서는 /autoresearch로 실행.
---

# Autoresearch

> **Karpathy의 autoresearch** — 한 번에 하나만 바꾸고, 채점하고, 유지하거나 되돌린다.
> 레시피를 고쳐서 앞으로 만드는 요리를 전부 좋게 만드는 것.

---

## 핵심 원리

```
점수를 매길 수 있으면, autoresearch할 수 있다.
— Ole (@unclejobs)
```

| 원본 (Karpathy ML) | 이 스킬 (프롬프트 최적화) |
|--------------------|-----------------------|
| `train.py` 수정 | `SKILL.md` 수정 |
| `program.md` 지침 | 이 SKILL.md = 루프 지침 |
| `val_bpb` 메트릭 | 체크리스트 점수 (pass/total × 100) |
| 학습 데이터 ≠ 검증 데이터 | 최적화 입력 ≠ holdout 입력 (holdout은 라운드에 쓰지 않고 최종 판정에만) |
| `results.tsv` | `autoresearch-log.md` 변경 로그 |
| `git commit/reset` | 유지/되돌림 |

---

## 사용법

기본 설치에서는 카탈로그에서 이 `SKILL.md`를 직접 읽고 아래 인자 의도를 적용합니다. 다음 표기는
명령 실행이 아니라 route intent입니다. `--include-source-only-skills`로 전체 활성화한 설치에서만
같은 앞에 `/`를 붙인 `/autoresearch` compatibility alias를 사용할 수 있습니다.

```text
# 기본 — 단일 스킬 최적화
autoresearch humanizer

# 옵션 지정
autoresearch humanizer --input sample.md --rounds 20

# 체크리스트 파일 직접 지정
autoresearch humanizer --checklist my-checklist.md

# 스캔 모드 — 전체 스킬 품질 진단
autoresearch --scan

# 스캔 후 바로 최적화
autoresearch --scan --auto
```

### 인자

| 인자 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `<skill-name>` | — | — | 개선할 대상 스킬 이름 (scan 모드 시 생략) |
| `--scan` | — | — | 전체 스킬 품질 스캔 모드 |
| `--auto` | — | — | scan 후 최하위 스킬부터 자동 최적화 시작 |
| `--input` | — | 자동 생성 | 테스트용 샘플 입력. 파일 경로 또는 인라인 텍스트 |
| `--holdout` | — | 자동 생성 1~2개 | 라운드에는 쓰지 않고 최종 독립 채점에만 쓰는 입력의 파일 경로. 개선 행위자는 내용을 읽지 않음 |
| `--checklist` | — | 대화로 수집 | 체크리스트 파일 경로 (.md) |
| `--rounds` | — | 20 | 최대 라운드 수 |
| `--target` | — | 95 | 목표 점수 (%) |
| `--streak` | — | 3 | 연속 달성 횟수 |

---

## Scan 모드 (`--scan`)

> **어떤 스킬을 돌려야 하는지 모르면** scan부터.
> 96개 스킬을 빠르게 훑어서 우선순위 리스트를 뽑아준다.

### 사용법

```text
# 전체 스캔
autoresearch --scan

# 스캔 + 최하위부터 자동 최적화
autoresearch --scan --auto
```

### Scan 워크플로우

```
1. 스킬 목록 수집
   └─ skills/*/SKILL.md를 Glob으로 전부 수집

2. 각 스킬에 Quick Health Check (6개 항목, 예/아니오)
   └─ skill-judge의 D1~D8 차원을 빠른 이진 질문으로 압축:

   ┌─────────────────────────────────────────────────────────────┐
   │ Q1 [Knowledge Delta]                                        │
   │    SKILL.md에 기본 모델이 모르는 전문 지식이 있는가?         │
   │    (결정 트리, 비직관적 트레이드오프, 경험 기반 엣지 케이스)  │
   │                                                             │
   │ Q2 [Anti-Patterns]                                          │
   │    구체적인 NEVER 리스트(하지 말 것 + 이유)가 있는가?        │
   │                                                             │
   │ Q3 [Examples]                                                │
   │    좋은 예시 또는 나쁜 예시가 스킬 안에 포함돼 있는가?       │
   │                                                             │
   │ Q4 [Description Quality]                                    │
   │    frontmatter description이 WHAT + WHEN + KEYWORDS를       │
   │    모두 포함하는가?                                          │
   │                                                             │
   │ Q5 [Progressive Disclosure]                                 │
   │    SKILL.md가 500줄 이하이고, 무거운 콘텐츠가               │
   │    references/로 분리돼 있는가?                              │
   │                                                             │
   │ Q6 [Actionable Instructions]                                │
   │    지시가 구체적인가? ("좋은 코드를 작성하라" ❌ vs          │
   │    "함수는 20줄 이내, 단일 책임" ✅)                         │
   └─────────────────────────────────────────────────────────────┘

3. 점수 산출
   └─ 각 항목 PASS=1, FAIL=0
   └─ 점수 = (PASS / 6) × 100

4. 등급 분류 + 정렬

   | 점수 | 등급 | 의미 |
   |------|------|------|
   | 0~33% | 🔴 낮음 | 즉시 autoresearch 필요 |
   | 34~66% | 🟡 보통 | 개선 여지 있음 |
   | 67~100% | 🟢 양호 | 유지 |
```

### Scan 출력 형식

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Autoresearch Skill Scan — 96 skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 낮음 (즉시 개선 필요)
  17%  domain-name-brainstormer  — 예시 없음, 지시 모호, NEVER 리스트 없음
  17%  meme-factory              — 전문 지식 없음, 예시 없음
  33%  web-to-markdown           — description 불완전, 예시 없음

🟡 보통 (개선 여지)
  50%  marp-slide               — NEVER 리스트 없음, 지시 일부 모호
  50%  commit-work              — 예시 없음, 엣지 케이스 미비
  67%  naming-analyzer          — 예시 풍부하나 NEVER 리스트 없음

🟢 양호
  83%  humanizer                — 예시 필요
  83%  zephermine               — description 보강 여지
 100%  skill-judge              — 모든 항목 통과

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 3개 | 🟡 3개 | 🟢 3개
  추천: domain-name-brainstormer부터 autoresearch route 실행
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Scan + skill-judge 연동

scan의 Quick Health Check는 **skill-judge의 경량 버전**입니다.

| skill-judge 차원 | Scan 질문 | 매핑 |
|-----------------|-----------|------|
| D1: Knowledge Delta (20pt) | Q1: 전문 지식 존재? | 핵심 차원 → 직접 매핑 |
| D3: Anti-Pattern Quality (15pt) | Q2: NEVER 리스트? | 구체적 안티패턴 유무 |
| D8: Practical Usability (15pt) | Q3: 예시 포함? | 예시 = 실용성 핵심 |
| D4: Spec Compliance (15pt) | Q4: Description 품질? | WHAT+WHEN+KEYWORDS |
| D5: Progressive Disclosure (15pt) | Q5: 500줄 이하? | 토큰 효율 |
| D6: Freedom Calibration (15pt) | Q6: 지시 구체성? | 모호 vs 구체 |

**심층 평가가 필요하면**: 전역 `SKILLS-CATALOG.md`에서 첫 셀이 정확히 `skill-judge`인 단 하나의
source-only 행과 `읽을 경로`를 해석해 그 `SKILL.md` 전체를 직접 읽고 `<skill-name>`을 평가합니다.
해석할 수 없으면 정밀 평가는 `NOT RUN`이며 Quick Health Check를 정밀 평가로 가장하지 않습니다.

### `--scan --auto` 모드

scan 후 자동으로 최하위 스킬부터 순서대로 autoresearch를 실행합니다.

```
1. --scan 실행 → 우선순위 리스트 생성
2. 🔴 등급 스킬 중 최하위 선택
3. 해당 스킬에 대해:
   └─ scan에서 FAIL된 항목을 체크리스트로 자동 생성
   └─ 스킬 유형에 맞는 테스트 입력 자동 생성 + holdout 입력 위임 생성 (Phase 0 3b)
   └─ Hill-Climbing 루프 실행 → 독립 채점 게이트(holdout)
4. 완료 후 다음 🔴 스킬로 이동
5. 🔴 전부 처리 후 → 사용자에게 "🟡 스킬도 진행할까요?" 질문
```

**자동 체크리스트 생성 규칙**:
scan에서 FAIL된 Q1~Q6 항목을 해당 스킬의 체크리스트로 변환합니다.

```
FAIL된 항목 → 체크리스트 변환 예시:
Q1 FAIL → "스킬 출력에 기본 모델이 모르는 전문적 판단이 반영됐는가?"
Q2 FAIL → "구체적인 '하지 마라' 사례가 출력에 포함됐는가?"
Q3 FAIL → "좋은 예시/나쁜 예시가 출력 품질을 좌우하는가?"
Q6 FAIL → "지시가 모호하지 않고 측정 가능한 기준을 제시하는가?"
```

FAIL 항목이 3개 미만이면 해당 스킬 유형에 맞는 범용 체크리스트를 보충합니다.

---

## 워크플로우 (단일 스킬 최적화)

### Phase 0: 준비

```
1. 대상 스킬 확인
   └─ skills/<skill-name>/SKILL.md 존재 확인
   └─ 없으면 에러 → 종료

2. 체크리스트 확보 (--checklist 없으면 현재 CLI의 질문 방식으로 사용자에게 질문)
   └─ 질문: "이 스킬의 '잘 됐는지' 기준을 알려주세요. 예/아니오로 답할 수 있는 질문 3~6개."
   └─ 6개 초과 시 경고: "6개 넘으면 게이밍이 시작됩니다. 가장 중요한 6개만 골라주세요."

3. 테스트 입력 확보 (--input 없으면)
   └─ 스킬 유형에 맞는 샘플 자동 생성
   └─ 글쓰기 스킬: 의도적으로 AI스러운 샘플 텍스트
   └─ 코드 스킬: 대표적인 코드 스니펫
   └─ 설계 스킬: 간단한 기능 요구사항

3b. holdout 입력 확보 — 최적화 입력과 같은 유형, 다른 내용 1~2개
   └─ 생성·보관·실행은 격리된 쓰기 가능 작업자(holdout 담당 — Claude general-purpose /
      Codex worker / Antigravity generalist / Grok general-purpose)에게 위임. holdout 담당은 채점하지 않음
   └─ 위치: 입력 holdout/inputs/, 출력 holdout/outputs/baseline/, holdout/outputs/gate-<N>/
      (모두 .autoresearch/<skill-name>/ 아래, 출력 파일명은 입력과 같게)
   └─ holdout 담당이 읽는 것: 최적화 입력(유형을 맞추기 위해서만), 대상 SKILL.md, holdout 입력.
      체크리스트는 읽지 않음 — 보면 출력이 채점 기준 쪽으로 기울어 판정이 무의미해짐
   └─ 실행 계약은 Phase 1의 1번과 같음: SKILL.md 본문 + 입력만 따르고, 입력당 1회 실행
   └─ 반환은 "쓴 파일 경로 + done"만. 모호점 보고·작업 요약·완료 메시지에도 입력·출력의
      내용이나 주제를 적지 않음 (런타임이 자동으로 붙이는 완료 요약도 이 규칙을 따르게 지시)
   └─ --holdout이 주어지면 그 경로를 holdout 담당에게 넘기기만 함
   └─ 개선 행위자(메인)는 holdout 입력·출력을 읽지 않음 — 읽으면 최적화 입력이 됨.
      메인은 holdout 담당이 준 경로를 채점 역할에게 그대로 전달만 함
   └─ holdout 내용이 메인에 노출되면(반환·요약에 섞여 들어온 경우 포함) 그 holdout은 오염된 것:
      로그에 holdout: leaked를 남기고 다음 게이트 전에 새 holdout 입력으로 교체
   └─ 위임이 없으면 메인이 만들되 로그에 holdout: self-generated (약한 격리)로 기록

4. 백업 생성
   └─ SKILL.md 원본을 .autoresearch/backup/<skill-name>-original.md로 복사
   └─ git stash 또는 별도 백업 (되돌림 안전장치)

5. 로그 파일 초기화
   └─ .autoresearch/<skill-name>/autoresearch-log.md 생성
```

### Phase 1: 기준점 측정 (Baseline)

```
1. 대상 스킬의 SKILL.md를 프롬프트로 사용하여 테스트 입력 처리
   └─ 네이티브 범용 작업 역할로 실행 (격리된 컨텍스트)
   └─ 역할 계약: 대상 SKILL.md와 로그는 읽기 전용, 테스트 출력 또는 지정 임시 산출물만 반환.
      체크리스트는 실행 역할에 주지 않음 (보면 출력이 채점 기준에 맞춰져 점수가 부풀음)
   └─ 특정 커스텀 에이전트명이나 vendor별 spawn 형식을 요구하지 않음
   └─ 위임이 없으면 메인 컨텍스트에서 순차 실행하고 로그에 isolation: main-context 기록

2. 출력물을 체크리스트로 채점
   └─ 각 항목: PASS (1) 또는 FAIL (0)
   └─ 점수 = (PASS 수 / 전체 항목 수) × 100
   └─ ⚠️ Eval 격리: 출력물만 보고 채점. 프롬프트를 보면 관대해짐.

3. 기준점 기록
   └─ 로그에 "Baseline: 56% (3/5 pass)" 기록

4. holdout 기준점 — holdout 담당이 원본 SKILL.md(.autoresearch/backup/<skill-name>-original.md)로
   holdout 입력을 실행해 holdout/outputs/baseline/에 쓰고, 독립 채점 역할(아래 게이트와 같은 역할)이 그 출력을 채점
   └─ 기준점과 게이트는 같은 holdout 담당·같은 채점 역할이 맡아야 비교가 성립 (실행 방식·채점자 차이로
      되돌림이 일어나지 않게). 세션 중 역할을 잃으면 같은 지시문으로 다시 만들고 로그에 기록
   └─ 채점 역할은 체크리스트·holdout 입력·출력만 읽음 (SKILL.md·최적화 입력·로그는 읽지 않음)
   └─ 메인에 돌아오는 것은 고정 형식의 점수와 체크리스트 항목별 PASS/FAIL뿐. 채점 역할의
      완료 요약에도 입력·출력의 인용·요약을 넣지 않게 지시 (넣으면 위 leaked 규칙 적용)
   └─ 로그에 "Holdout baseline: 50% (2 inputs)" 기록
```

### Phase 2: Hill-Climbing 루프

```
LOOP (라운드 1 ~ --rounds):

  ┌─ ① 약점 분석
  │  └─ 가장 최근 FAIL 항목 중 하나 선택
  │  └─ 왜 실패했는지 분석 (출력물 vs 체크리스트 항목)
  │
  ├─ ② Mutation 전략 선택 (하나만)
  │  └─ add_counterexample: 실패 케이스를 스킬에 "이렇게 하지 마라" 예시로 삽입
  │  └─ tighten_language: 모호한 지시를 구체적으로 강화
  │  └─ add_constraint: 형식/길이/구조 제약 추가
  │  └─ add_negative_example: "나쁜 예시 vs 좋은 예시" 쌍 삽입
  │  └─ add_good_example: 이상적인 출력 예시 직접 삽입
  │  └─ remove_bloat: 불필요한 지시 제거 (토큰 절약)
  │
  ├─ ③ SKILL.md 수정 (딱 하나만 변경)
  │  └─ 현재 런타임의 직접 편집 기능으로 최소 변경
  │  └─ 변경 내용을 로그에 기록
  │
  ├─ ④ 재실행 + 채점
  │  └─ 동일한 테스트 입력으로 스킬 재실행
  │  └─ 체크리스트로 재채점
  │
  ├─ ⑤ 판정
  │  ├─ 점수 상승 → ✅ 유지 (Keep)
  │  │  └─ 로그: "R3: ✅ Keep — add_constraint '20단어 제한' (75% → 83%)"
  │  │
  │  ├─ 점수 동일 → ✅ 유지 (중립 변경은 유지 — 로컬 옵티마 탈출)
  │  │  └─ 로그: "R4: ✅ Keep (neutral) — tighten_language (83% → 83%)"
  │  │
  │  └─ 점수 하락 → ❌ 되돌림 (Revert)
  │     └─ SKILL.md를 이전 상태로 복원
  │     └─ 로그: "R5: ❌ Revert — remove_bloat → CTA 약화 (83% → 67%)"
  │
  └─ ⑥ 종료 조건 확인
     └─ 목표 점수(--target) 이상이 --streak회 연속? → Phase 3로 (success)
     └─ 최대 라운드 초과? → Phase 3로 (exhausted — 목표 미달 종료, success 아님)
        └─ 최종 점수 < baseline이면 SKILL.md를 원본으로 전량 되돌림 (개악 방지)
     └─ 원본으로 되돌리지 않았다면 success든 exhausted든 Phase 3 전에 아래 독립 채점 게이트(holdout)를 거침
     └─ 아니면 → 다음 라운드
```

### Phase 3: 완료 + 산출물

```
1. 최종 SKILL.md 저장 (이미 수정된 상태)

2. 변경 로그 완성 — .autoresearch/<skill-name>/autoresearch-log.md:
   ┌──────────────────────────────────────────────┐
   │ # Autoresearch Log: humanizer                │
   │ Target: 95% × 3 streak                       │
   │ Baseline: 56% (3/5)                          │
   │ Final: 92% (4.6/5 avg over 3 runs)           │
   │ Holdout: 50% → 83% (independent, 2 inputs)   │
   │ Rounds: 7 (4 kept, 1 neutral, 2 reverted)    │
   │                                              │
   │ ## Checklist                                  │
   │ 1. AI 유행어가 없는가? ................. ✅   │
   │ 2. 문장이 20단어 이내인가? ............ ✅   │
   │ 3. 능동태를 사용했는가? ............... ✅   │
   │ 4. em dash 2개 이하인가? .............. ✅   │
   │ 5. 개성이 느껴지는가? ................. ⚠️   │
   │                                              │
   │ ## Rounds                                     │
   │ R1: ✅ Keep — add_negative_example 유행어     │
   │     (56% → 75%)                               │
   │ R2: ✅ Keep — tighten_language 능동태          │
   │     (75% → 75%, neutral)                      │
   │ R3: ❌ Revert — add_constraint 15단어 제한    │
   │     (75% → 50%, CTA 약화)                     │
   │ R4: ✅ Keep — add_good_example 문장 분리      │
   │     (75% → 92%)                               │
   │ R5-7: 92%, 92%, 92% → 3 streak 달성 🏁       │
   │                                              │
   │ ## Mutation Stats                             │
   │ add_negative_example: 1/1 (100%)              │
   │ tighten_language:     1/1 (100%, neutral)     │
   │ add_constraint:       0/1 (0%)                │
   │ add_good_example:     1/1 (100%)              │
   │                                              │
   │ ## Diff Summary                               │
   │ +3 lines: 유행어 금지 목록                     │
   │ +2 lines: 능동태 변환 규칙                     │
   │ +4 lines: 좋은 예시 삽입                       │
   │ -0 lines: (되돌림으로 제거됨)                  │
   └──────────────────────────────────────────────┘

3. 사용자에게 결과 요약 출력
```

---

## 독립 채점 게이트 (034 — 자기채점 오버피팅 방지)

Hill-climbing은 생성·채점을 같은 행위자가 수행하므로, 최종 버전이 자기 체크리스트에만 과적합했을 수 있다.
streak 달성으로 완료를 선언하기 전, 가능하면 **다른 모델 패밀리의 읽기 전용 독립 채점 역할**에
최종 SKILL.md로 holdout 입력을 실행한 출력물을 동일 체크리스트로 1회 채점시킨다. 현재 CLI가 제공하는 네이티브 reviewer/explorer나
별도 CLI 리뷰를 사용할 수 있지만, 채점 역할은 대상 SKILL.md와 로그를 수정하지 않는다.

- 최적화에 쓴 점수(라운드 신호)와 합격 판정(독립 채점)을 **분리**한다 — 같은 점수로 고치고 같은 점수로 승인하지 않는다.
- **판정은 holdout 입력으로 한다.** 최적화 입력은 라운드마다 고친 대상이라, 같은 입력으로 다시 채점하면 채점자가 바뀌어도 "그 입력에 맞춘 스킬"을 걸러내지 못한다(특히 `add_good_example`). holdout 담당이 최종 SKILL.md로 holdout 입력을 실행해 `holdout/outputs/gate-<N>/`에 쓰고, 독립 채점 역할이 그 출력을 채점한다. 메인에는 점수와 항목별 PASS/FAIL만 돌아온다.
- holdout 점수가 목표 미달이면 streak는 무효다. 최적화 점수보다 20%p 이상 낮으면 과적합으로 보고 낮은 쪽 점수를 채택한 뒤 라운드를 더 돈다. 다음 라운드는 holdout에서 FAIL한 **항목 이름**만 보고 고친다 — holdout 출력 본문을 보고 고치면 holdout이 최적화 입력이 된다.
- holdout 점수가 holdout 기준점보다 낮으면 개악이다. 1회 재실행해 같은 결과면 SKILL.md를 원본으로 되돌리고 `status: overfit`으로 기록한다 (최적화 점수가 올랐어도 일반화에 실패한 것).
- 네이티브 위임이 없으면 메인 컨텍스트에서 반대 관점 채점을 순차 실행하고 `validator: sequential-main`으로 기록한다. 이때 holdout도 메인이 실행하므로 `holdout: self-run (약한 격리)`을 함께 기록한다.
- 다른 모델 패밀리가 없으면 single-model 결과로 라벨하고 "독립 검증 안 됨"을 로그에 명시한다 (거짓 합격 금지).

---

## 체크리스트 작성 가이드

### 규칙

| 규칙 | 이유 |
|------|------|
| **3~6개** | 3개 미만 → 허점 발생. 6개 초과 → 게이밍 시작 |
| **예/아니오만** | 1~7점 척도 쓰면 "기술적으로 5점"인 쓰레기가 나옴 |
| **구체적으로** | "좋은 글인가?" ❌ → "유행어가 없는가?" ✅ |
| **독립적으로** | 항목 간 상충하지 않아야 함 |

### 좋은 체크리스트 예시

**글쓰기 스킬용:**
```
1. "혁신적", "획기적", "탁월한" 같은 AI 유행어가 없는가?
2. 모든 문장이 20단어 이내인가?
3. 수동태 대신 능동태를 사용했는가?
4. em dash(—)를 2개 이하로 사용했는가?
5. 첫 문장이 구체적인 고충이나 상황을 짚는가?
```

**설계 스킬용:**
```
1. API 명세에 에러 응답 코드(4xx, 5xx)가 정의됐는가?
2. 비기능 요구사항(성능, 보안)이 포함됐는가?
3. 컴포넌트 간 의존성 방향이 명시됐는가?
4. 데이터 스키마가 정규화(3NF 이상)됐는가?
```

**코드 생성 스킬용:**
```
1. 타입이 any 없이 구체적으로 지정됐는가?
2. 에러 처리가 try-catch로 감싸졌는가?
3. 함수가 단일 책임을 지키는가? (20줄 이내)
4. import 경로가 절대 경로인가?
```

---

## 제약 사항

### 반드시 지킬 것

| # | 규칙 |
|---|------|
| 1 | **한 번에 하나만 변경.** 두 가지를 동시에 바꾸면 뭐가 효과 있었는지 모름 |
| 2 | **Eval 격리.** 채점 시 SKILL.md(프롬프트)를 보지 말 것. 출력물만 보고 판단 |
| 3 | **되돌림은 즉시.** 점수가 떨어지면 고민하지 말고 바로 되돌림 |
| 4 | **같은 테스트 입력 사용.** 입력이 바뀌면 공정한 비교 불가 (라운드는 최적화 입력만 사용) |
| 5 | **로그는 매 라운드 기록.** 건너뛰면 변경 로그의 가치가 사라짐 |
| 6 | **holdout은 보지 않는다.** 개선 행위자는 holdout 입력·출력을 읽지 않고 점수와 항목별 PASS/FAIL만 받는다 |

### 하지 말 것

| # | 금지 사항 | 이유 |
|---|----------|------|
| 1 | 체크리스트 7개 이상 | 게이밍 시작 — 시험 답만 외우는 학생 |
| 2 | 1~7점 슬라이딩 척도 | "기술적 5점" 쓰레기 양산 |
| 3 | 한 번에 여러 변경 | 어떤 변경이 효과인지 구분 불가 |
| 4 | 프롬프트 전체 재작성 | Hill climbing이 아니라 random restart |
| 5 | 테스트 입력 중간 변경 | 점수 비교의 기준이 무너짐 |
| 6 | holdout 출력을 보고 수정 | 미공개 입력이 최적화 입력이 되어 일반화 검증이 사라짐 |
| 7 | 최적화 입력 문장을 그대로 `add_good_example`에 복사 | 그 입력에만 맞는 스킬이 됨 — 예시는 일반화해서 넣음 |

---

## Mutation 전략 상세

| 전략 | 설명 | 성공률* | 언제 사용 |
|------|------|---------|----------|
| `add_counterexample` | 실패 케이스를 "이렇게 하지 마라" 예시로 삽입 | 높음 | 특정 안티패턴이 반복될 때 |
| `tighten_language` | "좋은 글을 써라" → "능동태, 20단어 이내, 구체적 숫자 포함" | 높음 | 지시가 모호할 때 |
| `add_constraint` | 형식/길이/구조 제약 추가 | 중간 | 출력이 산만할 때 |
| `add_negative_example` | "나쁜 예시 → 좋은 예시" 쌍 삽입 | 중간 | 경계가 불분명할 때 |
| `add_good_example` | 이상적인 출력 예시 삽입 | 중간 | 기대 수준이 명확할 때 |
| `remove_bloat` | 불필요한 지시 삭제 | 낮음 | 토큰 과다, 지시 충돌 시 |

*성공률은 Balu Kosuri의 14-cycle 실험 기준 참고치

### 전략 선택 우선순위

```
1. 실패 항목 분석 → 원인이 "안티패턴 반복"이면 → add_counterexample
2. 원인이 "지시가 모호"이면 → tighten_language
3. 원인이 "형식 이탈"이면 → add_constraint
4. 원인이 "경계 불명확"이면 → add_negative_example
5. 위 전략이 이미 시도됐으면 → add_good_example
6. 점수가 정체(5 라운드 이상 변화 없음)이면 → remove_bloat (정체 탈출)
```

---

## 산출물 파일 구조

```
.autoresearch/
├── scan-report.md                  # --scan 결과 (전체 스킬 품질 리포트)
├── backup/
│   └── <skill-name>-original.md    # 원본 백업
└── <skill-name>/
    ├── autoresearch-log.md         # 변경 로그 + 점수 히스토리
    └── holdout/                    # holdout 담당·채점 역할만 읽음, 개선 행위자는 읽지 않음
        ├── inputs/                 # holdout 입력
        └── outputs/
            ├── baseline/           # 원본 SKILL.md 실행 결과
            └── gate-<N>/           # N번째 게이트의 최종 SKILL.md 실행 결과
```

---

## 관련 스킬

| 스킬 | 관계 |
|------|------|
| `skill-judge` | 스킬 품질 평가 (1회성) — autoresearch는 평가 + 수정 + 반복 |
| `humanizer` | 대표적인 최적화 대상 (글쓰기 스킬) |
| `auto-continue-loop` | 자율 루프 인프라 — autoresearch는 자체 루프 보유 |
| `manage-skills` | 스킬 관리 — autoresearch는 스킬 개선 |

---

## 레퍼런스

- [karpathy/autoresearch (GitHub)](https://github.com/karpathy/autoresearch)
- [Autoresearch 101 Builder's Playbook](https://sidsaladi.substack.com/p/autoresearch-101-builders-playbook)
- [Universal Skill (Balu Kosuri)](https://medium.com/@k.balu124/i-turned-andrej-karpathys-autoresearch-into-a-universal-skill-1cb3d44fc669)
- [autoexp Gist](https://gist.github.com/adhishthite/16d8fd9076e85c033b75e187e8a6b94e)
