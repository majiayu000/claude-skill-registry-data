---
name: foreign-matter-car
description: This skill should be used when the user asks to "이물 분석해줘", "이물 대책서 만들어줘", "이물 원인 파악", "혼입 사고 보고서", "SEM-EDX 분석 결과 있어", "이물 DB 대조해줘", "foreign matter report", "corrective action report", "재발방지 대책서", or provides foreign matter incident files for analysis. Make sure to use this skill whenever the user mentions 이물, 혼입, SEM-EDX, or corrective action in the context of manufacturing quality incidents.
arguments:
  - name: input
    description: 초기보고서 또는 SEM-EDX 분석 결과 파일 경로
    default: ""
tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - Agent
  - Skill
---

# 이물 혼입 재발방지 대책서 자동 생성

> 이물 초기보고 → SEM-EDX 해석 → DB 대조 → 작업지시서 교차검증 → 대책서(md/docx/pptx) 일괄 생성

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

이물 관련 파일이 제공되면 즉시 Phase 1부터 실행한다. 파일 없이 구두 요청만 있으면 필요한 파일을 질문한다.

---

## Workflow

### Phase 1: 자료 수집 및 파싱

**Type**: prompt

1. 사용자가 제공한 파일 확인 (초기보고서, SEM-EDX 결과)
2. 필수 정보 추출:
   - **초기보고서**: 발생 일시, 라인, 제품, LOT, 검출 방식, 이물 육안 소견(크기, 색상, 질감, 냄새)
   - **SEM-EDX**: 원소별 wt% 수치, 분석 조건, 샘플 ID
3. 누락 정보가 있으면 사용자에게 한 번에 질문 (최소화)

**초기보고서와 SEM-EDX 파싱은 독립적 — 병렬 실행 가능.**

---

### Phase 2: 이물 DB 대조

**Type**: prompt + script

1. 이물 DB 파일 탐색:
   ```
   Glob: **/sem_edx_database.csv
   ```
   기본 경로: `references/sem_edx_database.csv` 또는 `data/sem_edx_database.csv`

2. **2단계 매칭 알고리즘 실행:**

   **Step A — Hard Filter (시그니처 패턴):**
   - 검체의 주요 원소 존재/부재로 카테고리 축소
   - 예: Zn+S 동시 검출 + N 부재 → 가황 천연고무 계열
   - 예: Fe+Cr+Ni → 스테인리스 계열
   - 예: Cl 고농도 → PVC 계열

   **Step B — Soft Score (wt% 유사도):**
   - 후보군 내에서 원소별 오차 비교
   - 허용 오차: 주요 원소(>5%) ±5wt%, 미량 원소(<5%) ±2wt%
   - 각 후보별 일치 원소 수 / 전체 원소 수로 매칭 점수 산출

3. **결과 제시 규칙:**
   - 유일 매칭 (점수 > 0.8, 2위와 격차 > 0.15) → 후보 1건 + 비교표 제시
   - 복수 매칭 → 상위 3건 비교표 제시 + "다음 정보로 구분 가능" 안내
   - **매칭 없음 → `UNMATCHED` 플래그. 추측하지 않는다.** "DB에 등록되지 않은 이물입니다. 전문가 확인이 필요합니다." 출력

4. **사용자에게 매칭 결과 보고 후 확인 요청** (이물 정체 확정은 반드시 사용자 승인)

---

### Phase 3: 작업지시서 교차 검증

**Type**: prompt + rag

1. 작업지시서 파일 탐색:
   ```
   Glob: **/작업지시서* OR **/work-instruction*
   ```
2. 이물 정체 확정 결과를 기반으로 관련 조항 검색:
   - Grep으로 키워드 탐색 (예: "장갑", "보호구", "위생", 해당 공정명)
3. **규정 vs 현장 실태 불일치 테이블 작성:**
   | 항목 | 작업지시서 규정 | 현장 실태 | 위반 여부 |
4. **규정 미비 사항 식별** (교체 주기, 점검 절차, 변경 승인 등)
5. 사용자에게 추가 정보 확인 (작업자 확인 결과, 장갑 재고 상황 등)

**작업지시서가 없으면:** "작업지시서 미확인 — 수동 첨부 필요" 크로스체크 포인트로 분리. 나머지 분석은 계속 진행.

---

### Phase 4: 원인 경로 종합

**Type**: prompt

Phase 1~3 결과를 종합하여 원인 경로 정리:

```
근본 원인 → 관리 원인 → 직접 원인 → 혼입 경로 → 검출
```

**반드시 사용자에게 원인 경로를 제시하고 승인받는다.** 승인 없이 대책서를 생성하지 않는다.

---

### Phase 5: 재발방지 대책서 생성

**Type**: generate

사용자 승인된 원인 분석을 기반으로 대책서 생성.

#### 대책서 구조 (7섹션):
1. **사고 개요** — 발생 일시/라인/LOT/이물 정체
2. **이물 동정 결과** — SEM-EDX 수치 + DB 대조 비교표
3. **원인 분석** — 원인 경로(근본→직접) + 규정 불일치 + 규정 미비
4. **영향 범위** — Hold 현황 + 납기 영향
5. **재발방지 대책** — 즉시/단기/중장기 계층화, 담당+기한 명시
6. **유효성 검증 계획** — 대책별 검증 방법/시기/판정 기준
7. **첨부 자료** + 결재란

#### 대책 설계 원칙:
- 즉시 조치: 원상 복귀 + 긴급 점검 (1~3일)
- 단기 대책: 규정 보완 + 절차 추가 (1~2주)
- 중장기 대책: 소재/설비 전환 검토 + 제도화 (1개월)
- 각 대책에 No./담당/기한 필수 명시

#### 출력:
1. `reports/YYYY-MM-DD_이물대책서.md` — Write로 생성
2. 사용자에게 "워드/PPT도 생성할까요?" 확인

---

### Phase 6: 문서 변환 (선택)

**Type**: generate

사용자 요청 시 docx/pptx 생성.

- **docx**: `docx` 스킬 호출 (`Skill: docx`)
- **pptx**: `pptx` 스킬 호출 (`Skill: pptx`)

docx/pptx 모두 Phase 5의 마크다운을 단일 소스로 사용 → 숫자 불일치 방지.

---

## Edge Cases

| 상황 | 처리 |
|------|------|
| DB 매칭 없음 | `UNMATCHED` 플래그, 추측 금지, 전문가 확인 권고 |
| 복수 매칭 | 상위 3건 비교표 + 구분 가능한 추가 확인 항목 안내 |
| 작업지시서 없음 | 크로스체크 포인트로 분리, 나머지 진행 |
| 초기보고서 필수 필드 누락 | 누락 항목 명시 후 사용자에게 질문 |
| SEM-EDX에 N 미포함 | "검출 한계 이하"와 "미측정"을 구분하여 처리 |
| DB CSV 컬럼 불일치 | 컬럼명 기반 파싱, 인덱스 기반 금지 |

## 절대 자동화 금지 항목

- 이물 원인 최종 확정 (사용자 승인 필수)
- 출하 중단/재개 판단
- 고객사/기관 제출 결정
- 보고서 결재

---

## Integration Points

- `docx` 스킬: 워드 문서 생성
- `pptx` 스킬: 보고용 PPT 생성
- `cross-check` 스킬: 생성된 보고서 검증 시 활용 가능
- `data-analyst` 스킬: DB 데이터 심층 분석 필요 시
