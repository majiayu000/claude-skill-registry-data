---
name: excel-to-report
description: This skill should be used when the user asks to "엑셀 분석 보고서 만들어줘", "데이터 종합 분석해줘", "파일들 연결해서 분석해줘", "원인 분석 PPT 만들어줘", "이번 달 실적 분석해줘", "불량 원인 찾아줘", "경영진 보고용 PPT", "데이터 분석 보고서", "excel analysis report", "multi-file analysis". Make sure to use this skill whenever the user provides multiple Excel files and wants cross-file analysis, root cause analysis, or a presentation report. This skill combines audit, cleaning, cross-analysis, visualization, and PPT generation into one workflow.
arguments:
  - name: path
    description: 분석 대상 엑셀 파일이 있는 폴더 경로 또는 개별 파일 경로
    default: ""
tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Agent
---

# Excel-to-Report

> 여러 엑셀 파일을 입력받아 오딧 → 클리닝 → 크로스파일 분석 → 문제점 탐지 → 근본원인 분석 → 차트 시각화 → PPT 보고서까지 자동 생성합니다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

이 스킬이 트리거되면 Phase 1부터 순서대로 실행한다. 사용자가 폴더/파일 경로를 이미 제공했으면 바로 시작, 아니면 경로를 물어본다.

---

## Preflight: Dependency Check

```bash
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install --break-system-packages openpyxl
python3 -c "import matplotlib" 2>/dev/null || python3 -m pip install --break-system-packages matplotlib
python3 -c "import pptx" 2>/dev/null || python3 -m pip install --break-system-packages python-pptx
python3 -c "import pandas" 2>/dev/null || python3 -m pip install --break-system-packages pandas
```

---

## Phase 1: INGEST & AUDIT (수집 · 오딧 · 클리닝)

**Type**: script + prompt

### Step 1-1: 파일 탐색 및 확인

1. 지정된 경로에서 `.xlsx`, `.xls`, `.csv` 파일을 Glob으로 탐색
2. 파일 목록을 사용자에게 제시:
   ```
   분석 대상 파일 N개를 확인했습니다:
   1. 파일명.xlsx (시트 N개, 행 N개)
   2. ...
   이 파일들로 진행할까요?
   ```

**GATE 1**: 사용자 승인 없이 다음 단계 진행 금지.

### Step 1-2: 오딧

Python 스크립트(Bash)로 각 파일에 대해 자동 실행:

| 검사 항목 | 방법 |
|----------|------|
| 수식 에러 | `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!` 탐지 |
| 합계 검증 | 소계/합계 행의 값 ≠ 상세 행의 합산 |
| 비율 검증 | 퍼센트 값 ≠ 분자/분모 계산값 |
| 크로스시트 | 같은 워크북 내 시트 간 동일 항목 수치 불일치 |
| 크로스파일 | 파일 간 동일 항목(매출, 생산량 등) 수치 불일치 |
| 구조 이슈 | 병합셀 수, 숨겨진 행/열, 수식 유무, 혼합 타입 열 |

결과를 심각도별(Critical/Warning/Info) 테이블로 보고.

### Step 1-3: 클리닝

오딧 결과를 기반으로 AI 가독성 클리닝 실행:

- 병합셀 해제 → 빈 셀에 원래 값 채우기
- 퍼센트 문자열("30.9%") → 숫자(0.309) 변환
- datetime 객체 → "YYYY-MM-DD" 문자열 정규화
- 소계/합계 행 구분을 위한 `row_type` 컬럼 추가 (data/subtotal/total)
- 클린 파일은 `_clean.xlsx` 접미사로 **원본 보존 + 별도 저장**

**원본 파일은 절대 수정하지 않는다.**

---

## Phase 2: CONNECT & DETECT (연결 · 탐지 · 원인분석)

**Type**: script + prompt

### Step 2-1: 크로스파일 연결 분석

클린 데이터를 기반으로 Python으로 크로스파일 집계:

- 일별/주별/월별 집계 (생산, 불량, 재고, 판매, 손익 등)
- 라인별/제품별/거래처별 분해
- 파일 간 동일 지표 비교 (매출: 경영현황 vs 판매현황 등)

### Step 2-2: 문제 시점 탐지

통계적 이상치 및 패턴 이탈 탐지:

- 달성률/불량률/이익률 등 핵심 지표의 시계열 이상치
- 주별 비교에서 분기 평균 대비 ±1.5σ 초과 구간
- 전월 대비 급변(±20% 이상) 시점

탐지 결과를 "문제 시점 목록"으로 정리.

### Step 2-3: 근본원인 구조 분석

**LLM이 담당** — 데이터 패턴에서 인과관계 가설을 생성:

- Level 0 (외부 환경) → Level 1 (1차 대응) → Level 2 (생산 충격) → Level 3 (실적 영향) → Level 4 (경영 결과)
- 모든 인사이트에 **출처 파일명 + 근거 수치** 필수
- 데이터 근거 없는 추정은 **"데이터 미확인 가설"**로 명시
- `references/기준값.md`가 있으면 판단 기준으로 참조

**GATE 2**: 근본원인 가설을 사용자에게 제시하고 승인/수정 요청.
```
근본원인 분석 가설입니다:
1. [외부] ...
2. [1차 영향] ...
3. [경영 결과] ...
수정하거나 추가할 내용이 있으신가요?
```

---

## Phase 3: VISUALIZE (시각화)

**Type**: script

확정된 분석 결과를 기반으로 matplotlib 차트 자동 생성.

### 기본 차트 세트 (6종)

| # | 차트 | 용도 |
|---|------|------|
| 1 | KPI 대시보드 | 핵심 지표 월별 비교 (카드 + 막대) |
| 2 | 위기 타임라인 | 듀얼축 라인 + 이벤트 마커 (인과 시각화) |
| 3 | 비용 구조 | 100% 누적 막대 (비용 비중 변화) |
| 4 | 라인/부문 비교 | 그룹 막대 (피해 vs 정상 비교) |
| 5 | 폭포(Waterfall) | 이익 변동 요인 분해 |
| 6 | 회복 추적 | 불릿/게이지 (기준선 대비 현재 위치) |

### 차트 생성 규칙

- 한글 폰트 자동 감지 (우선순위):
  1. Windows/WSL: `/mnt/c/Windows/Fonts/malgun.ttf` (맑은 고딕)
  2. macOS: `Apple SD Gothic Neo` (system font)
  3. Linux: `Nanum Gothic` (apt install fonts-nanum)
  4. 최종 fallback: `DejaVu Sans` (한글 깨질 수 있음, 경고 출력)

  Python helper 권장:
  ```python
  import os, matplotlib.font_manager as fm

  def get_korean_font():
      candidates = [
          "/mnt/c/Windows/Fonts/malgun.ttf",  # WSL
          "C:/Windows/Fonts/malgun.ttf",      # Windows native
      ]
      for path in candidates:
          if os.path.exists(path):
              return fm.FontProperties(fname=path).get_name()

      for name in ["Apple SD Gothic Neo", "AppleGothic",  # macOS
                   "NanumGothic", "Nanum Gothic",          # Linux
                   "Malgun Gothic"]:                       # Windows installed
          try:
              fm.findfont(name, fallback_to_default=False)
              return name
          except Exception:
              continue
      return "DejaVu Sans"  # last resort

  plt.rcParams["font.family"] = get_korean_font()
  plt.rcParams["axes.unicode_minus"] = False
  ```
- DPI: 150 (보고서용 고해상도)
- 색상: 문제 시점은 빨강, 정상은 파랑, 목표선은 점선
- 차트 제목 = 인사이트 (예: "2월 영업이익 79% 감소")
- `charts/` 폴더에 PNG로 저장

분석 내용에 따라 차트 종류와 수를 LLM이 판단하여 조정.

---

## Phase 4: REPORT (PPT 보고서)

**Type**: script + prompt

### Step 4-1: 슬라이드 구성 확인

**GATE 3**: PPT 생성 전 슬라이드 구성을 사용자에게 제시.
```
보고서 슬라이드 구성:
1. 표지
2. Executive Summary (3카드 요약)
3. KPI 대시보드
4. 위기 타임라인
5. 부문별 비교
6. 비용 구조 분석
7. 이익 변동 분석
8. 회복 추적
9. 시사점 및 조치 사항
추가/수정할 내용이 있으신가요?
```

### Step 4-2: PPT 생성

python-pptx로 슬라이드 조립:

- 와이드스크린 16:9 (13.333" x 7.5")
- 표지: 제목 + 소속 + 기준일 (`CLAUDE.md` 담당자 정보 참조)
- 차트 슬라이드: 이미지 삽입 + 하단 인사이트 박스
- 시사점 슬라이드: 단기/중기/확인필요 3분할 레이아웃
- 모든 수치에 출처 명시
- 크로스체크 포인트가 있으면 별도 표시

### Step 4-3: 저장 및 보고

```
reports/YYYY-MM-DD_{주제}_분석보고서.pptx
```

최종 산출물 목록을 사용자에게 보고:
- PPT 보고서 (핵심)
- 클린 엑셀 파일 (_clean.xlsx)
- 차트 이미지 (charts/)
- 크로스체크 포인트 목록

---

## Edge Cases

| 상황 | 대응 |
|------|------|
| 파일이 1개뿐 | 크로스파일 분석 건너뛰고, 단일 파일 심층 분석으로 전환 |
| 파일이 10개 초과 | "파일이 많습니다. 핵심 파일 5~7개를 선택해주세요" 안내 |
| 컬럼명이 파일마다 다름 | 오딧 단계에서 스키마 비교표 제시 후 사용자에게 매핑 확인 |
| 기간이 파일마다 다름 | 날짜 범위 불일치 경고 + 공통 기간만 분석할지 사용자 선택 |
| 데이터가 비어있음 | 해당 파일 제외하고 진행할지 사용자 확인 |
| 차트 생성 실패 (폰트 등) | 기본 폰트로 fallback, 경고만 표시하고 계속 진행 |

---

## 금지 사항

- 원본 파일 수정 금지 (항상 _clean.xlsx로 별도 저장)
- 데이터에 없는 수치를 생성(할루시네이션)하지 않는다
- 상관관계를 인과관계로 단정하지 않는다 (가설로 제시)
- 예측/예보 수치를 제시하지 않는다 (과거 데이터 분석만)
- 사용자 승인 없이 PPT를 저장하지 않는다

---

## Integration Points

- `references/기준값.md`: 정상/주의/경고 판단 기준으로 참조
- `references/보고서양식.md`: PPT 양식이 있으면 해당 양식 준수
- `CLAUDE.md` 담당자 정보: 표지 소속/이름에 반영
- `audit-xls` 스킬: Phase 1 오딧 로직의 기반
- `clean-data-xls` 스킬: Phase 1 클리닝 로직의 기반
- `data-analyst` 스킬: 단일 파일 분석은 data-analyst로 라우팅
- `cross-check` 스킬: 크로스체크 포인트 검증에 활용 가능
