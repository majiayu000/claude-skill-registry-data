---
name: gemini-multimodal-evidence
description: Gemini Files API의 강력한 멀티모달 기능을 활용한 증거 분석 스킬. 이미지, PDF, 문서 OCR, 비디오 등 다양한 형식의 증거를 AI로 분석하고 법적 판단을 지원합니다.
---

# Gemini 멀티모달 증거 분석 스킬

## 목적

Gemini Files API의 **멀티모달 AI 기능**을 최대한 활용하여:
- 이미지 증거 분석 (OCR, 객체 인식, 상황 분석)
- PDF 문서 분석 (판례, 계약서, 진술서)
- 복합 증거 종합 분석
- 법적 판단 지원 (참고용)

## 사용 시점

다음과 같은 작업을 할 때 자동 활성화됩니다:
- 증거 파일 업로드 및 분석 (이미지, PDF, 문서)
- OCR 텍스트 추출 및 해석
- 복합 증거 종합 평가
- 법적 판단 사전 검토
- 변호사 상담 준비 자료 작성
- 소송 전략 수립 지원

---

## 주요 기능

### 1. 멀티모달 파일 지원

**지원 형식**:
```
✅ 이미지: PNG, JPEG, WEBP, HEIC, HEIF
✅ 문서: PDF (최대 1,000 페이지)
✅ 스캔 문서: 자동 OCR
✅ 복합 문서: 텍스트 + 이미지 + 표 + 차트
```

**자동 처리**:
- OCR (광학 문자 인식)
- 객체 인식
- 장면 이해
- 텍스트 분석
- 구조 파싱

### 2. 증거 분석 유형

#### A. 문서 증거 분석
- 신용카드 명세서
- 통장 거래 내역
- 카카오톡 대화 캡처
- 문자 메시지 스크린샷
- 이메일 출력물

#### B. 이미지 증거 분석 (⚠️ 합법적 수집만)
- SNS 공개 게시물 스크린샷
- 공개된 장소 촬영 사진
- 목격자 제공 사진

#### C. 판례 문서 분석
- 법원 판결문 PDF
- 법률 문서 스캔본
- 판례집

#### D. 복합 증거 종합 분석
- 여러 증거 간 연관성 분석
- 시간순 정리
- 모순점 발견
- 입증력 평가

### 3. 법적 판단 지원

**제공 분석**:
- 민법 제840조 적용 가능성
- 유책 배우자 판단 근거
- 증거 강도 평가 (상/중/하)
- 추가 필요 증거 제안
- 예상 반박 및 대응 전략
- 유사 판례 비교

**제공하지 않는 것**:
- 법적 효력 있는 판단
- 소송 결과 보장
- 변호사 업무 대체

---

## Gemini Files API 멀티모달 기능

### 1. 자동 OCR

```python
from google import genai

client = genai.Client(api_key=api_key)

# 이미지/PDF 업로드 (자동 OCR)
file = client.files.upload(path="card_statement.jpg")

# 텍스트 자동 추출 + 분석
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        file,
        "이 신용카드 명세서를 분석하여 의심스러운 거래 패턴을 찾아주세요."
    ]
)

print(response.text)
# → 자동으로 텍스트 추출 + 패턴 분석
```

### 2. 복합 문서 분석

```python
# 여러 파일 동시 분석
files = [
    client.files.upload(path="evidence1.pdf"),
    client.files.upload(path="evidence2.jpg"),
    client.files.upload(path="evidence3.png")
]

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=files + [
        """
        이 3개 증거를 종합 분석하여:
        1. 시간순 정리
        2. 상호 연관성
        3. 입증 강도
        4. 모순점
        를 평가하세요.
        """
    ]
)
```

### 3. 구조화된 출력

```python
# JSON 형식 출력
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[file, "분석 결과를 JSON으로 출력하세요"],
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "strength_score": {"type": "integer"},
                "legal_issues": {"type": "array"},
                "recommendations": {"type": "array"}
            }
        }
    }
)

result = json.loads(response.text)
```

---

## 사용 예시

### 예시 1: 신용카드 명세서 OCR 분석

```python
from divorce_evidence_tool import DivorceEvidenceAnalyzer

analyzer = DivorceEvidenceAnalyzer()

# 이미지 업로드 및 분석
result = analyzer.analyze_single_evidence(
    file_path="card_statement.jpg",
    evidence_type="신용카드 명세서",
    analysis_focus=[
        "호텔 이용 패턴",
        "고액 결제 내역",
        "반복적 거래",
        "의심스러운 항목"
    ]
)

print(result)
```

**출력 예시**:
```json
{
  "ocr_text": "2024-11-15 | 강남 XX호텔 | 350,000원\n...",
  "pattern_analysis": {
    "suspicious_transactions": 4,
    "hotel_frequency": "매주 금요일",
    "total_amount": "1,590,000원"
  },
  "legal_assessment": {
    "article_840_1": "중간 (60%)",
    "evidence_strength": "중",
    "additional_evidence_needed": [
      "호텔 투숙 기록",
      "동반자 확인",
      "위치 정보"
    ]
  },
  "recommendations": [
    "법원에 호텔 CCTV 제출 명령 신청 검토",
    "목격자 진술 확보",
    "변호사 상담 필수"
  ]
}
```

### 예시 2: 복합 증거 종합 분석

```python
# 여러 증거 한 번에 분석
result = analyzer.analyze_multiple_evidence(
    files=[
        {
            "path": "card_statement.pdf",
            "type": "신용카드 명세서",
            "collection_date": "2024-12-01"
        },
        {
            "path": "kakao_chat.jpg",
            "type": "카카오톡 대화",
            "collection_date": "2024-12-02"
        },
        {
            "path": "witness_statement.pdf",
            "type": "목격자 진술서",
            "collection_date": "2024-12-03"
        }
    ],
    case_description="배우자 부정행위 의심 케이스"
)
```

**출력 예시**:
```json
{
  "case_summary": "6개월간 반복적 호텔 이용, 친밀한 대화, 목격자 증언이 있는 케이스",
  "evidence_timeline": [
    {
      "date": "2024-06-01~",
      "evidence": "신용카드 호텔 결제",
      "strength": "중"
    },
    {
      "date": "2024-09-15",
      "evidence": "카카오톡 애정 표현",
      "strength": "강"
    },
    {
      "date": "2024-11-20",
      "evidence": "목격자 증언",
      "strength": "중강"
    }
  ],
  "correlation_analysis": {
    "consistency": "높음 (85%)",
    "contradictions": "없음",
    "reinforcing_pattern": "호텔 날짜와 대화 시점 일치"
  },
  "legal_evaluation": {
    "article_840_1_probability": "75-85%",
    "overall_strength": "중상",
    "win_probability": "75-80%"
  },
  "strategy_recommendations": [
    "조정 시도 (유리한 조건 협상)",
    "법원에 통신 기록 제출 명령 신청",
    "사설 탐정 고용 검토",
    "재산 목록 확보"
  ]
}
```

### 예시 3: 판례 문서 비교 분석

```python
# 내 증거와 유사한 판례 비교
result = analyzer.compare_with_precedent(
    my_evidence_files=["my_evidence1.jpg", "my_evidence2.pdf"],
    precedent_file="similar_case_237553.pdf",
    comparison_focus=[
        "증거 유형 유사성",
        "법원 판단 기준",
        "승소/패소 요인",
        "참고할 점"
    ]
)
```

---

## API 사용법

### Python SDK

```python
from divorce_evidence_tool import DivorceEvidenceAnalyzer

# 초기화
analyzer = DivorceEvidenceAnalyzer(
    api_key="your-gemini-api-key"
)

# 단일 파일 분석
result = analyzer.analyze_single_evidence(
    file_path="evidence.jpg",
    evidence_type="신용카드 명세서"
)

# 복합 분석
result = analyzer.analyze_multiple_evidence(
    files=["file1.pdf", "file2.jpg"],
    case_description="케이스 설명"
)

# 적법성 검토
legality = analyzer.check_evidence_legality(
    evidence_description="배우자 신용카드 명세서"
)

# 판례 비교
comparison = analyzer.compare_with_precedents(
    evidence_summary="호텔 반복 이용 + 대화 내용",
    top_k=5
)
```

### REST API (웹 인터페이스)

```bash
# 파일 업로드 및 분석
curl -X POST http://localhost:8000/api/divorce-evidence/analyze \
  -F "file=@evidence.jpg" \
  -F "evidence_type=신용카드 명세서" \
  -F "analysis_focus=패턴 분석,법적 판단"

# 복합 증거 분석
curl -X POST http://localhost:8000/api/divorce-evidence/analyze-multiple \
  -F "files=@evidence1.pdf" \
  -F "files=@evidence2.jpg" \
  -F "case_description=부정행위 의심 케이스"

# 적법성 사전 검토
curl -X POST http://localhost:8000/api/divorce-evidence/check-legality \
  -H "Content-Type: application/json" \
  -d '{"evidence_description": "배우자 카카오톡 대화 캡처"}'
```

---

## 웹 인터페이스

### 화면 구성

```
┌─────────────────────────────────────────────────┐
│  이혼 증거 AI 분석 시스템                          │
└─────────────────────────────────────────────────┘

📁 증거 파일 업로드
[파일 선택] [이미지/PDF 드래그 앤 드롭]

증거 유형:
○ 신용카드 명세서  ○ 통장 거래내역
○ 카카오톡 대화    ○ 문자 메시지
○ SNS 스크린샷     ○ 목격자 진술서
○ 기타 (직접 입력)

케이스 설명:
[텍스트 입력 영역]

분석 옵션:
☑ OCR 텍스트 추출
☑ 패턴 분석
☑ 법적 판단
☑ 유사 판례 검색
☑ 추가 증거 제안

[분석 시작]

───────────────────────────────────────────────

📊 분석 결과

1. 증거 요약
   - 파일명: card_statement.jpg
   - 유형: 신용카드 명세서
   - OCR 정확도: 98%

2. 추출된 정보
   [OCR 텍스트 표시]

3. 패턴 분석
   - 의심스러운 거래: 4건
   - 반복 패턴: 매주 금요일
   - 총 금액: 1,590,000원

4. 법적 평가
   - 민법 840조 1호: 60% (중간)
   - 증거 강도: 중
   - 추가 증거 필요

5. 유사 판례
   [판례 카드 3개 표시]

6. 추천 사항
   ✓ 법원 CCTV 신청
   ✓ 목격자 확보
   ✓ 변호사 상담

⚠️ 면책 조항: 이 분석은 법적 효력이 없으며 참고용입니다.

[PDF 다운로드] [이메일 전송] [변호사 상담 예약]
```

---

## 안전 지침

### ✅ 합법적 증거만 사용

**허용되는 증거**:
- 본인이 당사자인 대화/문서
- 배우자의 신용카드 명세서 (공동 계좌)
- 공개된 SNS 게시물
- 본인이 촬영한 사진 (적법한 장소)
- 목격자가 제공한 자료 (동의 하에)

**금지되는 증거**:
- 타인 몰래 촬영한 사진
- 불법 녹음/도청
- 해킹으로 취득한 자료
- GPS 불법 추적 정보
- 동의 없는 제3자 정보

### 🔒 개인정보 보호

```python
# 자동 개인정보 마스킹
analyzer = DivorceEvidenceAnalyzer(
    auto_mask_personal_info=True  # 기본값
)

# 마스킹 대상:
# - 주민등록번호
# - 계좌번호
# - 전화번호
# - 주소
# - 얼굴 (선택적)
```

### ⚖️ 법적 책임

**AI 분석의 한계**:
1. 법적 효력 없음
2. 변호사 업무 대체 불가
3. 최종 판단은 법원
4. 참고 자료로만 사용

**사용자 책임**:
1. 증거의 적법성 확인
2. 개인정보 보호법 준수
3. 변호사 상담 필수
4. AI 분석 맹신 금지

---

## 비용

### Gemini Files API

```
파일 저장:
- $0.001/GB/day
- 48시간 자동 삭제
- 100MB 증거 → $0.002 (2일)

API 호출:
- Gemini 2.0 Flash: 무료 (일일 한도 내)
- 또는 Gemini 2.5 Flash: $0.00001875/1K 입력 토큰
```

### 예상 비용 (케이스당)

```
증거 파일 5개 (총 50MB):
- 저장: $0.001
- OCR + 분석: $0.01-0.05
- 판례 검색: $0.005
- 총: ~$0.02-0.06 (₩25-80)

변호사 상담 대비:
- 변호사 상담: ₩200,000-500,000
- AI 사전 검토: ₩25-80
- 절감: 99.98%
```

---

## 실전 활용 시나리오

### 시나리오 1: 초기 증거 수집 단계

**상황**: 막 증거를 모으기 시작함

**활용법**:
1. 수집한 증거 AI 업로드
2. 적법성 사전 검토
3. 부족한 증거 파악
4. 추가 수집 계획 수립

**효과**: 불법 증거 수집 방지, 효율적 증거 확보

### 시나리오 2: 변호사 상담 준비

**상황**: 변호사 상담 예정

**활용법**:
1. 모든 증거 종합 분석
2. AI 분석 리포트 생성
3. 질문 사항 정리
4. 예상 질문/답변 준비

**효과**: 상담 시간 단축, 비용 절감, 명확한 전달

### 시나리오 3: 소송 전략 수립

**상황**: 소송 진행 여부 결정

**활용법**:
1. 승소 가능성 평가
2. 예상 위자료 산정
3. 소송 비용/기간 추정
4. 조정 vs 소송 비교

**효과**: 합리적 의사결정, 리스크 최소화

---

## 고급 기능

### 1. 자동 판례 매칭 (Image-to-Precedent Search) ✨
- **이미지 증거 기반 판례 검색**: 사용자가 업로드한 사진(메모, 카톡)을 분석하여 유사한 판례를 찾습니다.
- **프로세스**:
  1. **Vision Analysis**: Gemini Vision으로 이미지에서 텍스트 및 상황 설명 추출
  2. **Query Expansion**: 추출된 설명을 법률 검색 쿼리로 변환 (예: "남편의 메모" → "배우자 자필 메모 부정행위 증거")
  3. **Dual Index RAG**: 시맨틱 인덱스에서 유사 판례 검색
  4. **Matching**: 내 증거와 판례의 유사점 매칭

```python
# 이미지에서 바로 판례 검색
matches = analyzer.auto_match_precedents_from_image(
    image_path="husband_memo.jpg",
    top_k=5
)

for match in matches:
    print(f"유사 판례: {match['case_no']}")
    print(f"판례 상황: {match['fact_summary']}")
    print(f"내 증거와 유사점: {match['similarity_reason']}")
```

### 2. 시간순 타임라인 자동 생성

```python
# 증거를 시간순으로 자동 정렬 및 시각화
timeline = analyzer.generate_timeline(
    evidence_files=[...],
    output_format="html"  # 또는 "json", "pdf"
)

# timeline.html 생성
# 대화형 타임라인 차트
```

### 3. 모순점 자동 탐지

```python
# 여러 증거 간 모순 자동 발견
contradictions = analyzer.detect_contradictions(
    evidence_files=[...]
)

for c in contradictions:
    print(f"모순: {c['description']}")
    print(f"증거1: {c['evidence_1']}")
    print(f"증거2: {c['evidence_2']}")
    print(f"설명: {c['explanation']}")
```

---

## 제약 사항

### 기술적 제약

```
파일 크기: 최대 2GB
페이지 수: PDF 최대 1,000 페이지
동시 업로드: 최대 20개 파일
저장 기간: 48시간 (이후 자동 삭제)
처리 시간: 파일당 5-30초
```

### 법적 제약

```
⚠️ AI 분석은 법적 자문이 아닙니다
⚠️ 변호사 업무를 대체할 수 없습니다
⚠️ 최종 판단은 법원이 합니다
⚠️ 불법 수집 증거는 분석 거부됩니다
```

---

## 다음 단계

### Phase 1: 기본 구현 (1주)
- [ ] Gemini Files API 통합
- [ ] 기본 OCR 및 분석 기능
- [ ] 웹 UI 구축
- [ ] 단일 파일 분석

### Phase 2: 고급 기능 (2주)
- [ ] 복합 증거 분석
- [ ] 판례 RAG 연동
- [ ] 자동 마스킹
- [ ] 타임라인 생성

### Phase 3: 프로덕션 (3주)
- [ ] 사용자 인증
- [ ] 데이터 암호화
- [ ] 결제 시스템
- [ ] 변호사 연결 기능

---

## 참고 자료

### 공식 문서
- [Gemini Files API](https://ai.google.dev/gemini-api/docs/files)
- [Document Processing](https://ai.google.dev/gemini-api/docs/document-processing)
- [Multimodal Capabilities](https://ai.google.dev/gemini-api/docs/vision)

### 법률 자료
- 민법 제840조 (이혼 원인)
- 개인정보보호법
- 증거법 기본 원칙

---

**버전**: 1.0.0
**작성일**: 2025-12-04
**작성자**: Claude (SuperClaude Framework)
**법적 고지**: 이 스킬은 법적 자문을 제공하지 않으며, 참고 자료로만 사용되어야 합니다.
