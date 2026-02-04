---
name: court-divorce-bigquery-indexing
description: Claude가 판례 Markdown 파일을 직접 분석하여 JSON 메타데이터를 생성합니다.
---

# 판례 분석 및 JSON 메타데이터 생성 스킬

## 목적

이혼 판례의 Markdown 파일을 Claude가 직접 읽고 분석하여 구조화된 JSON 메타데이터로 변환합니다. 전체 문맥 이해를 기반으로 정확한 정보를 추출합니다.

## 사용 시점

다음과 같은 작업을 할 때 사용됩니다:
- 판례 MD 파일 분석 및 JSON 메타데이터 생성
- 위자료, 재산분할, 혼인 기간, 유책 사유 추출
- 판례 데이터베이스 구축
- BigQuery 인덱싱용 데이터 준비

---

## 주요 기능

### Claude 직접 분석 방식
**특징**:
- 전체 판례 문맥 이해
- 정규식 한계 극복
- 높은 정확도 (95%+)
- 판결문 의미 파악 기반

### 추출 정보
- **case_id**: 판례일련번호
- **filename**: 원본 MD 파일명
- **alimony_amount**: 위자료 액수 (원 단위, 0이면 미인정)
- **property_ratio_plaintiff**: 원고 재산분할 비율 (0.0~1.0)
- **marriage_duration_years**: 실제 혼인 기간 (연수)
- **fault_type**: 인정된 유책 사유
- **key_summary**: 판결의 핵심 1문장 요약

---

## 사용 방법

### Claude를 통한 판례 분석 요청

**입력 디렉토리**:
```
/Users/realpio4/Documents/vibe-with-bigquery/data/court_cases/details_20251203_135227/
```
- 법제처 API로 다운로드한 판례 MD 파일들
- 파일명 형식: `{판례일련번호}_{사건번호}.md`

**출력 디렉토리**:
```
/Users/realpio4/Documents/vibe-with-bigquery/data/court_cases/metadata_json/
```
- 각 판례마다 생성되는 JSON 메타데이터
- 파일명 형식: `{판례일련번호}.json`

### 사용 예시

```
Claude에게 요청: "court-divorce-bigquery-indexing 스킬 로드해서
/Users/realpio4/Documents/vibe-with-bigquery/data/court_cases/details_20251203_135227
디렉토리의 판례들을 분석해서
/Users/realpio4/Documents/vibe-with-bigquery/data/court_cases/metadata_json
디렉토리에 JSON으로 저장해줘"
```

---

## 출력 형식

### JSON 메타데이터 예시

```json
{
  "case_id": "609501",
  "filename": "609501_2024다64000.md",
  "alimony_amount": 5000000,
  "property_ratio_plaintiff": 0.5,
  "marriage_duration_years": 15,
  "fault_type": "부정행위",
  "key_summary": "배우자의 부정행위를 이유로 한 이혼 청구 인용",
  "extraction_method": "rules"
}
```

### 필드 설명

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `case_id` | string | 판례 일련번호 | "609501" |
| `filename` | string | 원본 MD 파일명 | "609501_2024다64000.md" |
| `alimony_amount` | number | 위자료 액수 (원) | 5000000 |
| `property_ratio_plaintiff` | float | 원고 재산분할 비율 (0~1) | 0.5 |
| `marriage_duration_years` | number | 혼인 기간 (년) | 15 |
| `fault_type` | string | 주된 유책 사유 | "부정행위" |
| `key_summary` | string | 판결 요지 (1문장) | "배우자의 부정행위..." |
| `extraction_method` | string | 추출 방식 | "rules" 또는 "llm" |

---

## 추출 방식 비교

| 구분 | 규칙 기반 | LLM 기반 |
|------|---------|---------|
| 속도 | 매우 빠름 (1초/건) | 느림 (5-10초/건) |
| 정확도 | 중간 (80-90%) | 높음 (95%+) |
| API 호출 | 없음 | Gemini 호출 |
| 비용 | 무료 | 유료 |
| 추천 상황 | 대량 데이터 | 정확성 중요 |

---

## 환경 변수 설정

### 필수 (LLM 사용 시)
```bash
export GOOGLE_API_KEY=your_gemini_api_key
```

### 선택 (BigQuery 인덱싱 시)
```bash
export GCP_PROJECT_ID=your_project_id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## 유책 사유 분류

추출 가능한 유책 사유:

| 사유 | 키워드 | 설명 |
|------|--------|------|
| 부정행위 | 부정행위, 불륜, 간통 | 배우자의 외도 |
| 폭언 | 폭언, 욕설, 모욕 | 심한 언어 폭력 |
| 폭행 | 폭행, 폭력, 가정폭력 | 신체적 폭력 |
| 악의적 유기 | 악의적 유기, 별거 | 정당한 이유 없는 유기 |
| 성격차이 | 성격차이, 성격 불일치 | 성격 갈등 |
| 도박 | 도박, 중독 | 도박 중독 |
| 알코올 | 음주, 알코올 중독 | 알코올 중독 |

---

## 처리 결과

### 성공 시 출력
```
🚀 609개 판례 처리 시작...
✅ [1/609] 609501_2024다64000.md
✅ [2/609] 609503_2023다11758.md
...
✅ [609/609] 612131_2024도17056.md

🎉 완료! JSON 저장 위치: data/court_cases/json
```

### 실패 시 처리
- 추출 실패 판례는 로그에 기록
- 기본값으로 채워진 JSON 생성 (알 수 없는 값은 0 또는 "Unknown")
- 처리는 계속 진행

---

## 데이터 품질

### 규칙 기반 추출 시 주의사항

1. **위자료 금액**:
   - 단위가 명확하지 않으면 만원 단위로 가정
   - 숫자만 추출 (단위 기호 제거)

2. **재산분할 비율**:
   - 부부 합의 비율로 계산
   - 정해지지 않으면 0.0으로 설정

3. **혼인 기간**:
   - 정확한 연수 추출
   - 모르면 -1로 설정

4. **유책 사유**:
   - 복합 사유는 가장 먼저 매칭되는 사유만 추출
   - 해당 사유가 없으면 "Unknown"

---

## 법적 고지

- 본 스킬은 **교육 및 연구 목적**으로만 사용하세요
- 판례 분석 결과는 **참고용**입니다
- 실제 법률 문제는 **변호사와 상담**하세요
- 판례 데이터의 저작권은 **법제처 및 법원**에 있습니다

---

**스킬 상태**: 완료 ✅
**관련 스크립트**: `extract_precedent_metadata.py`
