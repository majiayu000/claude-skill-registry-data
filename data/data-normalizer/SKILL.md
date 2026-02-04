---
name: data-normalizer
description: 발굴조사 자료(논문/보고서/주변유적) 수집 및 메타데이터 정규화
tags: [archaeology, data-extraction, normalization, pipeline-step-1]
---

# Data Normalizer - 자료 수집 및 정규화

## 목적
논문/, 발굴조사보고서/, 주변유적/ 폴더의 모든 문서(PDF, HWP, DOCX, TXT)에서 텍스트와 메타데이터를 추출하여 통합 인덱스를 생성합니다.

## 입력
- `논문/` 폴더: 학술 논문 파일들
- `발굴조사보고서/` 폴더: 발굴조사 보고서 파일들
- `주변유적/` 폴더: 주변 유적 관련 자료들

## 처리 프로세스

### 1단계: 폴더 스캔 및 파일 목록 생성
```python
# 지원 파일 형식: .pdf, .hwp, .docx, .doc, .txt
# 재귀적으로 모든 하위 폴더 탐색
```

### 2단계: 파일별 메타데이터 추출
각 파일에서 다음 정보를 추출:
- **식별자**: UUID 또는 파일경로 기반 해시
- **경로**: 상대 경로
- **제목**: 문서 제목 (메타데이터 또는 첫 페이지에서 추출)
- **저자/기관**: 작성자 또는 발간 기관
- **연도**: 발간/작성 연도
- **지명**: 조사지역, 유적명 (키워드 추출)
- **좌표**: 위도/경도 (있는 경우)
- **시대**: 청동기, 삼국시대, 통일신라 등
- **유구/유물 유형**: 주거지, 수혈, 토기, 기와 등
- **초록/요약**: 문서 요약 (있는 경우)
- **본문 텍스트 해시**: 내용 변경 감지용

### 3단계: 텍스트 추출 및 구조화
- 페이지 단위 텍스트 추출
- 섹션 경계 보존 (목차, 장/절 제목 인식)
- 표와 그림 캡션 별도 필드화
- 참고문헌 섹션 식별 및 파싱

### 4단계: 출력 파일 생성
**output/normalized/documents.jsonl** (JSONL 형식)
```json
{
  "id": "doc_001",
  "path": "논문/김철수_2020_청동기취락연구.pdf",
  "title": "○○지역 청동기시대 취락 연구",
  "author": "김철수",
  "year": 2020,
  "location": "○○시 △△동",
  "coordinates": {"lat": 37.5665, "lon": 126.9780},
  "period": ["청동기시대"],
  "types": ["주거지", "수혈유구", "무문토기"],
  "abstract": "본 연구는...",
  "text_sections": [
    {"section": "서론", "page": 1, "text": "..."},
    {"section": "조사내용", "page": 5, "text": "..."}
  ],
  "tables": [
    {"caption": "유구 일람표", "page": 15, "content": "..."}
  ],
  "references": ["이영희(2018)...", "박민수(2019)..."]
}
```

**output/normalized/metadata.csv** (스프레드시트용)
```csv
id,path,title,author,year,location,lat,lon,period,types,abstract_preview
doc_001,논문/...,○○지역 청동기...,김철수,2020,○○시,37.5665,126.9780,청동기시대,"주거지;수혈유구",본 연구는...
```

**output/normalized/extraction_log.txt** (처리 로그)
```
[2025-11-12 10:00:00] 처리 시작
[2025-11-12 10:00:01] 논문/ 폴더 스캔: 15개 파일 발견
[2025-11-12 10:00:05] doc_001 처리 완료: 논문/김철수_2020.pdf
[2025-11-12 10:00:10] 오류: doc_005 읽기 실패 (암호화된 PDF)
...
[2025-11-12 10:05:00] 처리 완료: 총 42개 파일, 성공 40개, 실패 2개
```

## 오류 처리
- 읽기 불가 파일 (암호화, 손상): 로그에 기록 후 건너뜀
- 메타데이터 부족: 추정값 사용 또는 "미상"으로 표기
- 좌표 없음: 지명 기반 지오코딩 시도 (선택)

## 품질 검증
- [ ] 추출된 파일 수와 실제 파일 수 일치 확인
- [ ] 필수 필드(제목, 연도, 지명) 누락률 < 10%
- [ ] 텍스트 추출 완전성: 페이지 수 vs 추출 섹션 수 비교

## 완료 후 다음 단계
```
다음 스킬 호출: similarity-matcher
전달 데이터: output/normalized/metadata.csv, output/normalized/documents.jsonl
```

## 기술 구현 가이드

### PDF 텍스트 추출
```python
import PyPDF2
import pdfplumber  # 표 추출에 유용

def extract_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text_sections = []
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            tables = page.extract_tables()
            text_sections.append({
                "page": page_num,
                "text": text,
                "tables": tables
            })
    return text_sections
```

### HWP 파일 처리
```python
import olefile  # HWP 파일은 OLE 구조
# 또는 hwp5tools 사용

def extract_hwp_text(file_path):
    # HWP는 복잡하므로 hwp5txt 명령줄 도구 활용 권장
    import subprocess
    result = subprocess.run(['hwp5txt', file_path],
                          capture_output=True, text=True)
    return result.stdout
```

### 메타데이터 추출 (정규식 활용)
```python
import re

def extract_metadata(text):
    # 연도 추출 (19XX, 20XX)
    year_match = re.search(r'(19|20)\d{2}', text)
    year = int(year_match.group()) if year_match else None

    # 좌표 추출 (N37°34'12" E126°58'30" 형식)
    coord_pattern = r'N(\d+)°(\d+)\'(\d+)"\s*E(\d+)°(\d+)\'(\d+)"'
    coord_match = re.search(coord_pattern, text)

    # 시대 키워드
    periods = []
    period_keywords = ['청동기', '초기철기', '원삼국', '삼국시대',
                      '통일신라', '고려', '조선']
    for keyword in period_keywords:
        if keyword in text:
            periods.append(keyword)

    return {
        'year': year,
        'coordinates': parse_coordinates(coord_match) if coord_match else None,
        'periods': periods
    }
```

### JSONL 저장
```python
import json

def save_jsonl(data_list, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
```

## 실행 명령
Claude에게 다음과 같이 요청하세요:
```
data-normalizer 스킬을 사용하여 논문/, 발굴조사보고서/, 주변유적/ 폴더의
모든 자료를 수집하고 메타데이터를 추출해주세요.
```

## 주의사항
- 대용량 파일(>100MB) 처리 시 메모리 관리 필요
- 한글 인코딩 문제: UTF-8, CP949, EUC-KR 모두 시도
- 스캔 PDF는 OCR 필요 (Tesseract 활용)
- 저작권 준수: 내부 분석용으로만 사용
