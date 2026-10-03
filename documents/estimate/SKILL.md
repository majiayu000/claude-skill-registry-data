---
name: estimate
description: >
  개발 견적서 자동 생성. 젭마인 산출물(spec, sections, api-spec)에서 기능을 추출하고,
  비용 그룹별(개발비, 인건비, 클라우드, API, 잡비) 견적서를 엑셀로 출력.
  /estimate로 실행.
---

# Estimate — 개발 견적서

> 젭마인 산출물 또는 프로젝트 분석 결과를 기반으로
> **비용 그룹별 견적서**를 엑셀(.xlsx)로 생성하는 스킬.

## Quick Start

```
/estimate                           # 프로젝트 자동 분석 + 견적서 생성
/estimate docs/plan/my-feature      # 특정 젭마인 산출물 기준
/estimate --template only           # 빈 견적서 양식만 생성
```

**공식 호출명:** `/estimate` (별칭: `견적`, `견적서`, `공수 산정`)

## 파이프라인 위치

```
/zephermine → spec.md + sections/ + api-spec.md
                    ↓
              /estimate (견적서)
                    ↓
              estimate.xlsx
```

**독립 실행 가능** — 젭마인 산출물 없이도 프로젝트를 직접 분석하여 생성 가능.

---

## CRITICAL: First Actions

### 1. Print Intro

```
Estimate — 개발 견적서 생성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
순서: Analyze → Ask → Calculate → Excel
```

### 2. Resolve Inputs

입력 소스를 결정합니다:

**A. 젭마인 산출물이 있는 경우 (권장, archive/ 경로 제외):**
- `docs/plan/*/spec.md` — 기능 요구사항
- `docs/plan/*/sections/` — 섹션별 상세 스펙
- `docs/plan/*/api-spec.md` — API 엔드포인트
- `docs/plan/*/db-schema.md` — DB 구조

**B. 없는 경우:**
- 네이티브 위임이 가능하면 **읽기 전용 탐색 역할**에 기능, API, 데이터 모델, 외부 서비스 근거를 조사시킵니다.
  이 역할은 파일을 수정하지 않고 `file:line` 근거와 기능 목록만 반환하며, 특정 커스텀 에이전트 이름을 요구하지 않습니다.
- 위임 기능이 없거나 실패하면 메인 컨텍스트에서 코드맵(있는 경우) → `rg` → 핵심 파일 읽기 순으로 같은 조사를 순차 수행합니다.
- 공수 계산, 사용자 확인, 엑셀 작성과 검증은 항상 메인 스킬 하네스가 담당합니다.
- 사용자에게 기능 목록 직접 질문

---

## Phase 1: 기능 추출

### 젭마인 산출물에서 추출

```
spec.md → 기능 요구사항 목록 (FR-001, FR-002, ...)
sections/ → 섹션별 상세 기능 (프론트/백엔드 분리)
api-spec.md → API 엔드포인트 수
db-schema.md → 테이블/엔티티 수
```

### 기능별 복잡도 분류

각 기능을 복잡도로 분류합니다:

| 복잡도 | 기준 | 기본 공수 (MM) |
|--------|------|---------------|
| **단순** | CRUD, 목록/상세, 기본 폼 | 0.3 MM |
| **보통** | 검색/필터, 권한 분기, 파일 업로드 | 0.5 MM |
| **복잡** | 결제 연동, 실시간 처리, 복잡한 비즈니스 로직 | 1.0 MM |
| **고난도** | AI/ML 연동, 대용량 처리, 외부 시스템 통합 | 1.5~2.0 MM |

> **기본 공수는 참고값** — 사용자가 조정할 수 있습니다.

---

## Phase 2: 비용 기준 확인

현재 CLI의 질문 방식으로 사용자에게 단가를 확인합니다:

```
question: "견적서 기본 단가를 설정해주세요"
header: "비용 기준"
```

### 확인 항목

| 항목 | 질문 | 기본값 |
|------|------|--------|
| **1MM 단가** | "개발자 1인 1개월 인건비는?" | 800만원 |
| **프론트/백엔드 분리** | "프론트/백엔드 공수를 분리할까요?" | Yes |
| **PM 오버헤드** | "PM/기획 비용을 포함할까요? (개발비의 %)?" | 10% |
| **테스트 비용** | "QA/테스트 비용을 포함할까요? (개발비의 %)?" | 15% |
| **버퍼** | "예비비(버퍼)를 포함할까요? (총 비용의 %)?" | 10% |
| **부가세** | "부가세(VAT)를 포함할까요?" | Yes (10%) |
| **통화** | "통화 단위는?" | KRW (원) |

사용자가 "기본값 사용"을 선택하면 위 기본값으로 진행.

---

## Phase 3: 견적서 구조 생성

### 비용 그룹

```
1. 개발비
   ├── 1.1 프론트엔드 개발
   │   ├── 기능 A (보통) — 0.5MM
   │   ├── 기능 B (단순) — 0.3MM
   │   └── ...
   ├── 1.2 백엔드 개발
   │   ├── API 개발 — N개 엔드포인트
   │   ├── DB 설계/구현 — N개 테이블
   │   └── ...
   ├── 1.3 공통
   │   ├── 인증/권한 — 1.0MM
   │   ├── 초기 설정/환경 구성 — 0.3MM
   │   └── 배포 환경 구성 (Docker) — 0.3MM
   └── 소계

2. 인건비
   ├── 2.1 PM/기획 (개발비의 N%)
   ├── 2.2 디자인 (해당 시)
   ├── 2.3 QA/테스트 (개발비의 N%)
   └── 소계

3. 인프라 비용 (월간)
   ├── 3.1 클라우드 서버 (AWS/GCP/Azure 등)
   ├── 3.2 DB 서버/서비스
   ├── 3.3 스토리지 (S3 등)
   ├── 3.4 CDN
   └── 소계 (월)

4. 외부 서비스 비용 (월간)
   ├── 4.1 API 사용료 (PG결제, SMS, 이메일 등)
   ├── 4.2 SaaS 구독 (모니터링, 로깅 등)
   ├── 4.3 인증 서비스 (OAuth, SMS 인증 등)
   └── 소계 (월)

5. 기타 비용
   ├── 5.1 도메인 (연간)
   ├── 5.2 SSL 인증서 (연간, Let's Encrypt 무료 시 0)
   ├── 5.3 앱스토어 등록비 (해당 시)
   └── 소계

6. 요약
   ├── 개발비 합계 (1회)
   ├── 인건비 합계 (1회)
   ├── 월 운영비 합계 (3+4)
   ├── 기타 비용 합계
   ├── 예비비 (N%)
   ├── 부가세 (10%)
   └── 총 견적
```

---

## Phase 4: 엑셀 파일 생성

Python `openpyxl`을 사용하여 `.xlsx` 파일을 생성합니다.

### 엑셀 구조

**Sheet 1: 견적서 (Summary)**

| 구분 | 항목 | 단위 | 수량 | 단가 | 금액 | 비고 |
|------|------|------|------|------|------|------|
| 1. 개발비 | | | | | | |
| | 프론트엔드 - 기능A | MM | 0.5 | 8,000,000 | 4,000,000 | 보통 |
| | ... | | | | | |
| | **소계** | | | | **XX,XXX,XXX** | |
| 2. 인건비 | | | | | | |
| | PM/기획 | | | | | 개발비의 10% |
| | ... | | | | | |
| **총 합계** | | | | | **XX,XXX,XXX** | VAT 포함 |

**Sheet 2: 기능 상세 (Details)**

| # | 기능명 | 프론트(MM) | 백엔드(MM) | 복잡도 | 설명 |
|---|--------|-----------|-----------|--------|------|
| 1 | 회원가입/로그인 | 0.5 | 1.0 | 복잡 | JWT + OAuth |
| 2 | 대시보드 | 0.5 | 0.3 | 보통 | 통계 조회 |

**Sheet 3: 월 운영비 (Monthly)**

| 항목 | 서비스 | 월 비용 | 연 비용 | 비고 |
|------|--------|---------|---------|------|
| 클라우드 | AWS EC2 t3.medium | 50,000 | 600,000 | 예상 |

### 스타일링

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# 헤더: 진한 파란 배경 + 흰색 글자
header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True, size=11)

# 그룹 헤더: 연한 파란 배경
group_fill = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
group_font = Font(bold=True, size=11)

# 소계/합계: 노란 배경
subtotal_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
total_fill = PatternFill(start_color="FFD966", end_color="FFD966", fill_type="solid")

# 금액: 우측 정렬 + 천 단위 콤마
number_format = '#,##0'
```

### 파일 생성

```bash
# openpyxl 설치 확인
pip install openpyxl 2>/dev/null || pip3 install openpyxl 2>/dev/null

# Python 헬퍼로 생성 + 실행
python scripts/estimate_builder.py
```

**출력:** `docs/estimate/estimate-{project-name}-{YYYY-MM-DD}.xlsx`

---

## Phase 5: 완료 안내

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 견적서 생성 완료!

📁 산출물:
  docs/estimate/estimate-{project}-{date}.xlsx

📊 요약:
  개발비:     {금액}원 ({N}MM)
  인건비:     {금액}원
  월 운영비:  {금액}원/월
  기타:       {금액}원
  ─────────────────────
  총 견적:    {금액}원 (VAT 포함)

👉 다음 단계:
  엑셀 파일을 열어 단가/수량을 조정하세요.
  수식이 연결되어 있어 단가 변경 시 자동 재계산됩니다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--template` | 빈 견적서 양식만 생성 (기능 분석 없이) | false |
| `--no-ask` | 기본 단가로 즉시 생성 (질문 없이) | false |
| `--currency` | 통화 단위 변경 | KRW |
| `--output-dir` | 출력 디렉토리 | `docs/estimate/` |

---

## 예외사항

다음은 **문제가 아닙니다**:

1. **젭마인 산출물 없음** — 프로젝트를 직접 분석하거나 빈 양식 생성
2. **openpyxl 미설치** — 자동 설치 시도, 실패 시 CSV로 폴백
3. **프론트엔드 없는 프로젝트** — 백엔드만 견적 (프론트 섹션 비움)
4. **클라우드 비용 불확실** — "예상" 표시 + 비고에 가정 명시

---

## 엑셀 수식 연결

단가나 수량을 수정하면 자동 재계산되도록 엑셀 수식을 연결합니다:

```
금액 = 수량 × 단가                    (각 항목)
소계 = SUM(해당 그룹 금액)            (그룹별)
예비비 = (개발비 + 인건비) × 버퍼%     (자동)
부가세 = (합계) × 10%                 (자동)
총 견적 = 합계 + 예비비 + 부가세       (자동)
```

**사용자가 엑셀에서 단가만 바꾸면 총 견적이 자동으로 바뀝니다.**

---

## 연관 스킬

| 스킬 | 역할 | 연결 |
|------|------|------|
| zephermine | 기능 추출 원본 (spec, sections) | 입력 |
| closer | 최종 산출물 (PRD 등) | 병렬 |
| excel2md | 엑셀 ↔ 마크다운 변환 | 견적서 마크다운 버전 필요 시 |

## Helper Scripts

이 스킬에는 재사용 가능한 헬퍼 스크립트가 포함되어 있습니다.
Phase 4(엑셀 생성) 단계에서 반복되는 openpyxl 패턴을 함수로 제공합니다.

| 스크립트 | 용도 |
|---------|------|
| `scripts/estimate_builder.py` | openpyxl 기반 견적서 생성 헬퍼 (비용 그룹, 요약 시트, 수식 연결, 통화 형식) |

```bash
# 설치
pip install openpyxl

# 직접 실행 (샘플 견적서 생성)
python scripts/estimate_builder.py
```

주요 함수:

| 함수 | 역할 |
|------|------|
| `create_estimate_workbook(project_name)` | 헤더가 설정된 견적서 워크북 생성 |
| `add_cost_group(ws, group_name, items)` | 비용 그룹 + 항목 + 소계 행 추가, 소계 셀 주소 반환 |
| `add_summary_sheet(wb, subtotal_refs)` | 예비비/부가세/총 합계 수식이 연결된 요약 시트 생성 |
| `format_currency(value, currency)` | 숫자 → 통화 문자열 변환 (KRW/USD/JPY) |
| `calculate_totals(ws)` | Python 레벨 수량×단가 재계산 (수식 검증용) |

---

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/zephermine/SKILL.md` | 기능 추출 원본 |
| `skills/excel2md/SKILL.md` | 엑셀 변환 유틸리티 |
| `skills/estimate/scripts/estimate_builder.py` | 견적서 생성 헬퍼 스크립트 |
