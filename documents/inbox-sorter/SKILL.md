---
name: inbox-sorter
description: This skill should be used when the user asks to "inbox 정리해줘", "파일 분류해줘", "파일 정리", "inbox 비워줘", "쌓인 파일 분류", "받은 파일 정리", "인박스 정리", "/inbox-sorter", "file sort", "organize inbox".
tools:
  - Bash
  - Read
  - Write
  - Glob
  - Agent
---

# Inbox Sorter

> 00-inbox/ 폴더의 파일과 폴더를 분석하고, 적절한 목적지로 분류합니다.
> 모든 항목의 내용을 먼저 읽고 한 번에 분류 결과를 제시합니다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

`00-inbox/` 폴더를 스캔하고 Step 1부터 시작합니다.

---

## Workflow

### Step 1: 프리플라이트 [script]

```bash
# inbox 존재 확인
ls ./00-inbox/ 2>/dev/null || echo "INBOX_NOT_FOUND"

# 도구 확인
command -v pandoc >/dev/null 2>&1 && echo "PANDOC=yes" || echo "PANDOC=no"
python3 -c "import openpyxl" 2>/dev/null && echo "OPENPYXL=yes" || echo "OPENPYXL=no"
```

**inbox가 없으면**: "00-inbox/ 폴더를 찾을 수 없습니다. 먼저 폴더를 만들고 파일을 넣어주세요." → 종료

**항목 목록 수집**:
```bash
# 숨김파일, 임시파일 제외. 파일과 폴더 모두 포함.
ls -1 ./00-inbox/ | grep -v '^\.' | grep -v '^~\$' | grep -v '.tmp$'
```

**항목이 없으면**: "00-inbox/가 비어있습니다. 정리할 파일을 넣어주세요." → 종료

**지원 형식**: pdf, docx, xlsx, pptx, csv, md, txt, hwp, jpg, png + 폴더 + 기타

---

### Step 2: 내용 읽기 + 분류 [script + prompt]

**모든 항목을 처음부터 내용까지 읽고 한 번에 분류한다.** 중간 단계 없음.

#### 항목 유형별 내용 읽기 방법

| 유형 | 방법 | 범위 |
|------|------|------|
| **폴더** | `ls -1 ./00-inbox/폴더명/` | 내부 파일 목록으로 성격 판단 |
| `.pptx` | `pandoc -t plain "파일" \| head -30` | 첫 슬라이드 텍스트 |
| `.docx` | `pandoc -t plain "파일" \| head -50` | 첫 50줄 |
| `.xlsx` | `python3 -c "import openpyxl; ..."` (헤더+4행) | 첫 시트 상단 |
| `.pdf` | `Read(pages: "1")` | 첫 1페이지 |
| `.csv` | `head -5 "파일"` | 헤더+4행 |
| `.md`, `.txt` | `Read(limit: 30)` | 첫 30줄 |
| `.hwp` | 파일명 기반 분류 (내용 추출 불가) | — |
| 이미지 | 파일명 기반 분류 | — |

**pandoc/openpyxl 미설치 시**: 해당 형식은 파일명 기반 분류 + `신뢰도: 낮음`.
**대용량 파일 (50MB+)**: 내용 추출 생략. 파일명 기반 분류 + `신뢰도: 낮음`.
**읽기 실패 시**: 에러 무시. 파일명 기반 fallback. 절대 중단하지 않는다.

**병렬 실행**: 항목이 5개 이상이면 Bash 호출을 최대한 병렬로 실행하여 속도를 높인다.

#### xlsx 읽기 스크립트

```python
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('파일경로')
ws = wb.active
for row in ws.iter_rows(max_row=5, values_only=True):
    print(row)
"
```

#### 분류 목적지

| 폴더 | 자연어 표시 | 이런 항목이 갈 수 있음 |
|------|-----------|---------------------|
| `data/` | 분석용 데이터 | CSV, 원시 데이터, 측정값, 로그 |
| `references/` | 참고 자료 | 용어집, 가이드, 매뉴얼, 기준 문서, SOP |
| `reports/` | 보고서/결과물 | 보고서, 분석 결과, 발표 자료, 대책서 |
| `10-projects/` | 프로젝트 문서 | 기획서, 제안서, 프로젝트 산출물, 검토 자료 |
| `20-operations/` | 운영/업무 자료 | 회의록, SOP, 양식, 프로세스 문서 |
| `30-knowledge/` | 학습/지식 자료 | 아티클, 학습 자료, 리서치, 인사이트 |
| `50-resources/` | 외부 참고 자료 | 외부 벤치마크, 샘플, 레퍼런스, teardown |
| `90-archive/` | 보관 | 오래된 문서, 완료된 프로젝트 자료 |

**분류 판단 순서:**
1. 파일명 키워드 + 내용을 **함께** 고려하여 최적 목적지를 판단
2. 내용이 확인되면 파일명보다 내용 기반 판단을 우선
3. 모든 항목에 대해 확정된 목적지를 결정 — "uncertain"으로 남기지 않는다
4. 내용을 읽었지만 여전히 애매하면 가장 가까운 목적지 + `신뢰도: 낮음`

---

### Step 3: 분류표 제안 + 승인 게이트 [review]

**중복 체크 먼저:**
각 항목의 목적지에 같은 이름이 있는지 확인:
```bash
test -e "./목적지/항목명" && echo "CONFLICT"
```

**최종 분류표 출력 (한 번만):**

```
■ 인박스 분류 결과

| # | 항목명 | → 목적지 | 판단 근거 | 신뢰도 |
|---|--------|---------|---------|--------|
| 1 | 월간보고서_3월.xlsx | 보고서/결과물 (reports/) | 내용: 실적 집계 | 높음 |
| 2 | meeting_0405.docx | 운영/업무 (20-operations/) | 내용: 회의 안건 | 높음 |
| 3 | 설계리뷰/ | 프로젝트 문서 (10-projects/) | 내부 파일: 도면, 검토서 | 중간 |

이대로 이동할까요? 수정할 항목이 있으면 번호로 알려주세요.
```

**주의: 중간 과정(1차 분류, uncertain 목록 등)을 사용자에게 보여주지 않는다. 최종 결과만 한 번 깔끔하게 제시한다.**

**사용자 응답 처리:**
- "이대로" / "확인" / "ㅇㅇ" → Step 4 실행
- 번호 지정 → 해당 항목 목적지 변경 후 다시 표시
- "취소" → 종료 (항목 그대로)

---

### Step 4: 실행 + 결과 보고 [script]

**이동 실행:**
```bash
mv "./00-inbox/항목명" "./목적지/항목명"
```

**이동 규칙:**
- 모든 경로는 쌍따옴표로 감싼다 (한글, 공백 대응)
- 폴더도 mv로 동일하게 이동 (재귀 이동됨)
- 충돌 항목은 사용자 선택에 따라 처리 (덮어쓰기 / `항목명_2.확장자` / 건너뛰기)
- 이동 실패한 항목은 건너뛰고 계속 진행 (부분 실패 허용)
- 삭제는 절대 하지 않는다

**결과 보고:**

```
인박스 정리 완료

이동 완료: N개
- 보고서/결과물 (reports/): 3개
- 분석용 데이터 (data/): 2개

건너뜀: M개 (있을 경우만)
이동 실패: K개 (있을 경우만)
00-inbox/ 남은 항목: X개
```

**메모리 기록:**
분류 결과를 `memory/MEMORY.md`의 `## Unsorted`에 한 줄 기록:
`- YYYY-MM-DD: inbox-sorter 실행, N개 항목 분류 (reports/ 3, data/ 2, ...)`

**ONBOARDING_MODE 추가 저장:**

onboarding 스킬이 `ONBOARDING_MODE`로 호출하면 (인수 또는 컨텍스트 플래그), 분류 결과를 JSON으로 별도 저장:

```bash
cat > ./memory/state/onboarding-inbox-snapshot.json << 'EOF'
{
  "run_at": "2026-04-09T14:23:11Z",
  "items": [
    {"name": "월간보고_4월.xlsx", "dest": "reports/", "reason": "실적 집계", "confidence": "높음"},
    {"name": "defect_2603.csv", "dest": "data/", "reason": "원시 데이터", "confidence": "높음"}
  ],
  "dest_counts": {"reports/": 3, "data/": 2, "references/": 1}
}
EOF
```

그리고 결과 메시지 끝에 한 줄 추가:
```
→ 온보딩 Phase 4로 돌아갑니다. 이 분류 결과를 기반으로 직무 해석을 제안할게요.
```

onboarding 스킬은 이 JSON을 Read하여 Phase 4 재해석의 근거로 활용합니다.

---

## Edge Cases

**사용자가 새 목적지를 원하면**: "다른 폴더에 넣고 싶으면 경로를 알려주세요" → 분류표에서 수정.

**항목이 매우 많으면 (내부 처리)**: 15개 이상이면, Agent 도구로 5개씩 배치 병렬 처리. 각 Agent에게 항목 목록을 명시적으로 파티셔닝하여 중복 처리 방지. 사용자에게는 투명하게 — 결과만 보여줌.

**목적지 폴더가 없으면**: mkdir -p로 생성 후 이동.

---

## Integration Points

- **council**: 분류 판단이 애매한 항목에 대해 다관점 분석 요청 가능
- **data-analyst**: 분류 후 data/ 폴더의 CSV를 바로 분석
- **content-draft**: 분류 후 references/의 문서를 참조하여 보고서 초안
- **cross-check**: 분류 결과의 신뢰도를 교차 검증
