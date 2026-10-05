---
name: mapping-editor
description: "매핑 에디터. proposal_script.md와 generate_제안서.py 간의 매핑을 검증하고 수정합니다. 스크립트의 레이아웃 지시가 코드에 올바르게 반영되었는지 확인. 트리거: /mapping-editor, 매핑 검증, 스크립트-코드 매핑"
---

# 매핑 에디터

`proposal_script.md` ↔ `generate_제안서.py` 간의 매핑을 검증합니다.

## 사용법

```
/mapping-editor 테스트 XX
```

## 실행 절차

1. `output/테스트 XX/proposal_script.md` 읽기
2. `output/테스트 XX/generate_제안서.py` 읽기
3. 슬라이드별 매핑 검증:
   - 스크립트의 Action Title → 코드의 TB() 일치 여부
   - 스크립트의 레이아웃 → 코드의 함수 호출 일치 여부
   - 스크립트의 배경색 → 코드의 bg() 일치 여부
   - 스크립트의 시각 요소 → 코드 내 해당 함수 존재 여부
4. 불일치 리포트 출력
5. 사용자 요청 시 코드 수정

## 검증 항목

| 스크립트 필드 | 코드 매핑 | 불일치 시 |
|-------------|----------|---------|
| Action Title | `TB(s, "...", pg=N)` | WARNING: 제목 불일치 |
| 배경: dark | `bg(s, C["dark"])` | WARNING: 배경색 불일치 |
| 레이아웃: COLS 3열 | `COLS(s, [...])` | WARNING: 레이아웃 누락 |
| Win Theme: key1 | `WB(s, "key1", WIN)` | INFO: 뱃지 누락 |
| 시각 요소: STAT_ROW | `STAT_ROW(s, [...])` | WARNING: 시각 요소 누락 |

## 출력 포맷

```
═══ 스크립트↔코드 매핑 검증 ═══
✅ S01~S04: 매핑 정상
⚠️  S05: Action Title 불일치 — 스크립트: "3대 전략..." / 코드: "핵심 전략..."
⚠️  S12: 레이아웃 불일치 — 스크립트: COMPARE / 코드: COLS
✅ S13~S50: 매핑 정상
═══ 결과: 50장 중 48장 정상, 2장 불일치 ═══
```
