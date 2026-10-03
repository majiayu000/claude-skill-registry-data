---
name: excel2md
description: >
  .xlsx 엑셀 파일 읽기/변환 전문 스킬. JSON/마크다운 변환, 임베디드 이미지 자동 추출,
  시트별 파일 생성.
  ".xlsx", "엑셀", "excel", "스프레드시트" 요청에 실행.
license: MIT
metadata:
  version: "2.0.0"
---

# Excel to JSON/Markdown

엑셀 파일을 구조화된 JSON 또는 마크다운으로 변환합니다.
임베디드 이미지도 자동 추출하여 해당 행에 매핑합니다.

## Quick Start

```
/excel2md report.xlsx                        # JSON (기본)
/excel2md report.xlsx --format md            # 마크다운
/excel2md data.xlsx --sheet "매출현황"        # 특정 시트
/excel2md data.xlsx --output ./docs          # 출력 디렉토리
/excel2md data.xlsx --no-images              # 이미지 제외
```

---

## Step 0: 구조 분석 (First Actions)

변환 전 엑셀 파일의 구조를 먼저 파악합니다.

```python
import openpyxl

wb = openpyxl.load_workbook('data.xlsx', data_only=True)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    print(f"\n=== {sheet_name} ===")
    print(f"  크기: {ws.max_row}행 × {ws.max_column}열")
    print(f"  병합 셀: {len(ws.merged_cells.ranges)}개")
    
    # 헤더 자동 감지 (문자열 비율 기반)
    for row_idx in range(1, min(6, ws.max_row + 1)):
        row = [ws.cell(row_idx, c).value for c in range(1, ws.max_column + 1)]
        str_ratio = sum(1 for v in row if isinstance(v, str)) / max(len(row), 1)
        marker = " ← 헤더 후보" if str_ratio > 0.7 else ""
        print(f"  행 {row_idx}: {row[:5]}...{marker}")
```

### 구조 분석 출력 예시

```
=== Sheet1 ===
  크기: 150행 × 8열
  병합 셀: 3개
  행 1: ['번호', '이름', '부서', '직급', '입사일']... ← 헤더 후보
  행 2: [1, '김철수', '개발팀', '대리', datetime(2020,3,1)]...

=== 매출현황 ===
  크기: 50행 × 12열
  병합 셀: 12개 (그룹 헤더)
  행 1: ['', '', '2025년', None, None, '2026년']... ← 그룹 헤더
  행 2: ['지역', '담당자', '1Q', '2Q', '3Q', '1Q']... ← 실제 헤더
```

---

## Step 1: 데이터 타입 감지 + 변환

### 타입별 처리 규칙

| 엑셀 타입 | JSON 출력 | MD 출력 |
|-----------|-----------|---------|
| 문자열 | `"text"` | text (파이프·줄바꿈 이스케이프) |
| 정수 | `123` | 천 단위 콤마 `1,234` |
| 소수 | `3.14` | `1,234.56` (정수값이면 콤마 정수) |
| 날짜/일시 | `"2020-03-01 00:00:00"` (datetime을 `str()`로 — ISO 변환 안 함) | 동일 문자열 |
| 불리언 | `true`/`false` | Yes/No |
| 수식 | 계산 결과값 (`data_only=True`) | 계산 결과값 |
| 빈 셀 | `null` | (공백) |

> JSON 셀 직렬화는 `None`/`bool`/`int`/`float`만 원형 유지하고 **나머지(날짜·하이퍼링크 등)는 모두 `str()`로 변환**합니다. 하이퍼링크/통화/퍼센트를 구조화 객체(`{value, format}`)로 분리하는 기능은 **없습니다** — 셀의 텍스트/숫자 값만 출력됩니다.

> **병합 셀·멀티 헤더(그룹 헤더)는 자동 처리하지 않습니다.** 현재 CLI는 `iter_rows(values_only=True)`로 첫 행을 단일 헤더로 사용합니다 — 병합 값 전파나 그룹 헤더 평탄화는 미지원입니다. 그런 시트는 위 [Step 0](#step-0-구조-분석-first-actions)로 구조를 먼저 확인하고 수동 보정하세요.

---

## Step 2: 이미지 추출

xlsx는 ZIP 아카이브이며, 내부 XML을 파싱하여 이미지를 추출합니다:

1. `xl/worksheets/_rels/sheet*.xml.rels` → 시트→드로잉 매핑
2. `xl/drawings/_rels/drawing*.xml.rels` → rId→미디어 파일 매핑
3. `xl/drawings/drawing*.xml` → 앵커에서 row/col + rId 추출
4. `xl/media/*` → 이미지 바이너리 추출

**Fallback**: 드로잉 매핑 실패 시 media 폴더 전체 추출 (위치 없음 → "기타" 섹션 배치).

---

## Step 3: 출력

### JSON 구조

```json
{
  "source": "report.xlsx",
  "sheet": "Sheet1",
  "row_count": 150,
  "headers": ["번호", "이름", "부서", "직급", "입사일"],
  "rows": [
    {"번호": 1, "이름": "김철수", "부서": "개발팀", "직급": "대리", "입사일": "2020-03-01 00:00:00"}
  ],
  "images": [
    {"filename": "image1.png", "row": 1, "col": 0}
  ]
}
```

### Markdown 구조

```markdown
# Sheet1

> Source: report.xlsx | Sheet: Sheet1 | Rows: 150 | Images: 5

| 번호 | 이름 | 부서 | 직급 | 입사일 |
|------|------|------|------|--------|
| 1 | 김철수 | 개발팀 | 대리 | 2020-03-01 00:00:00 |

## 첨부 이미지

### 행 1
![image1.png](image1.png)
```

---

## 특수 케이스 처리

| 케이스 | 처리 |
|--------|------|
| 파이프(`\|`) 포함 셀 | MD에서만 이스케이프 |
| 시트명 특수문자 | 안전한 파일명으로 변환 (`/` → `_`) |
| 이미지 없는 xlsx | 텍스트만 변환 |
| twoCellAnchor + oneCellAnchor | 두 앵커 타입 모두 지원 |
| 빈 시트 | `_(빈 시트)_` 표기 |

---

## 요구사항

```bash
pip install openpyxl
```

## 옵션

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--format` | | `json`(기본) 또는 `md` |
| `--sheet` | `-s` | 특정 시트만 |
| `--output` | `-o` | 출력 디렉토리 |
| `--overwrite` | `-f` | 덮어쓰기 |
| `--no-images` | | 이미지 제외 |

## Helper Scripts

| 스크립트 | 용도 |
|---------|------|
| `excel2md.py` | 메인 CLI |
| `scripts/excel_parser.py` | openpyxl 파싱 헬퍼 |

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/pdf/SKILL.md` | PDF 변환 |
| `skills/docx/SKILL.md` | Word 문서 변환 |
| `skills/web-to-markdown/SKILL.md` | 웹페이지 변환 |
