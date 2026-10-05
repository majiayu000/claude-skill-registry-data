---
name: script-editor
description: "제안서 스크립트 에디터 v2.0. proposal_script.md를 3가지 뷰(Overview/Strategy/Slide List)로 분석하고 편집합니다. 전체 구성·목차·흐름을 한눈에 파악하고, 전략 품질을 진단합니다. 트리거: /script-editor, 스크립트 수정, 스크립트 편집, 스크립트 분석, 구조 확인, 전략 분석"
---

# 제안서 스크립트 에디터 v2.0

`output/$ARGUMENTS/proposal_script.md`를 **3가지 뷰 모드**로 분석하고 편집합니다.

---

## 사용법

```
/script-editor 테스트 XX
```

실행 시 **Overview → Strategy → Slide List** 순서로 3가지 뷰를 모두 출력한 뒤, 사용자 피드백을 대기합니다.

---

## 뷰 모드 1: Overview (전체 조망)

스크립트의 구조를 한눈에 파악할 수 있는 요약 테이블.

### 출력 형식

```
═══════════════════════════════════════════════════
  제안서 구조 Overview
═══════════════════════════════════════════════════
프로젝트: [프로젝트명]
발주처:   [발주처]
유형:     marketing_pr
예산:     X억
기간:     YYYY.MM ~ YYYY.MM
컨셉:     "[한 줄 컨셉]"
총 슬라이드: 55장
═══════════════════════════════════════════════════

Part | 제목              | 장수 | 비중  | 목표  | 판정 | 감정    | 분위기 리듬
-----|-------------------|------|-------|-------|------|---------|------------------
1    | SPARK             | 5    | 9%    | 8%    | ✅   | 호기심  | D-W-W-W-L
2    | PROBLEM→OPP       | 8    | 15%   | 15%   | ✅   | 공감    | W-W-D-W-W-L-W-W
3    | SOLUTION          | 9    | 16%   | 15%   | ✅   | 확신    | D-W-D-W-W-W-L-W-D
4    | EXECUTION         | 22   | 40%   | 35%   | ⚠️   | 납득    | W-W-D-W-W-L-...
5    | PROOF             | 7    | 13%   | 17%   | ⚠️   | 신뢰    | W-D-W-W-L-W-W
6    | RETURN            | 4    | 7%    | 10%   | ⚠️   | 행동    | D-W-W-D

판정 기준: 목표 비중 ±5% 이내 = ✅, 초과 = ⚠️
```

### 분석 항목
1. **메타데이터**: 프로젝트명, 발주처, 유형, 예산, 기간, 컨셉
2. **Part별 통계**: 장수, 비중(%), 목표 비중과 비교
3. **분위기 리듬**: D(dark), W(white), L(light), G(gradient), B(branded) 약어로 표시
4. **비중 판정**: 프로젝트 유형별 가중치 기준 ±5% 이내면 ✅, 벗어나면 ⚠️

### 프로젝트 유형별 목표 비중 (참조)

| Part | Marketing/PR | Event | IT/System | Public | Consulting |
|------|-------------|-------|-----------|--------|------------|
| 1 SPARK | 8% | 6% | 5% | 5% | 6% |
| 2 PROBLEM→OPP | 15% | 10% | 15% | 18% | 18% |
| 3 SOLUTION | 15% | 12% | 15% | 12% | 18% |
| 4 EXECUTION | 35% | 45% | 35% | 30% | 25% |
| 5 PROOF | 17% | 17% | 20% | 22% | 20% |
| 6 RETURN | 10% | 10% | 10% | 13% | 13% |

---

## 뷰 모드 2: Strategy (전략 분석)

제안서의 전략적 품질을 진단합니다.

### 출력 형식

```
═══════════════════════════════════════════════════
  전략 분석
═══════════════════════════════════════════════════

▶ Win Theme 관통도
  W1 "데이터 기반" ─── 12회 (S02,S07,S12,S18,S24,S30,S35,...) ✅ 충분
  W2 "시민 참여"   ─── 8회  (S05,S10,S15,S22,S26,...) ✅ 충분
  W3 "통합 시너지" ─── 3회  (S08,S30,S42) ⚠️ 약함 (최소 5회 권장)

▶ S-E-P 설득 구조 품질
  콘텐츠 슬라이드: 45장
  Story 있음:    45/45 (100%) ✅
  Evidence 있음: 43/45 (96%)  ✅
  Promise 있음:  44/45 (98%)  ✅
  Evidence 출처 있음: 40/43 (93%) ✅
  출처 누락:     S14, S28, S33 ⚠️

▶ Action Title 품질
  Action Title 적용: 42/45 (93%) ✅
  Topic Title 의심:  S19 "채널 전략", S37 "리스크 관리" ⚠️
    → 인사이트+데이터 기반으로 수정 필요

▶ 패턴 다양성
  사용 패턴: 14종 / 20종 ✅
  사용:   hero_stat(3), card_grid(8), bento_grid(2), comparison(3), ...
  미사용: funnel, waterfall, radar_profile, sankey, heatmap, bubble
  ⚠️ card_grid 8회 → 과다 사용 (5회 이하 권장)

▶ 분위기 리듬 분석
  dark: 12장 (22%)
  white: 30장 (55%)
  light: 8장 (15%)
  gradient: 3장 (5%)
  branded: 2장 (4%)
  ⚠️ white 5장 연속: S20-S24 → dark/gradient 삽입 권장

▶ Bridge 점검
  Part 1→2: ✅ "이러한 시장 환경 속에서..."
  Part 2→3: ✅ "이 기회를 잡기 위한 전략은..."
  Part 3→4: ✅ "구체적으로 어떻게 실행할 것인가..."
  Part 4→5: ✅ "이 모든 것을 해낼 수 있는 팀은..."
  Part 5→6: ✅ "투자 대비 기대 효과는..."

▶ KPI 산출근거
  KPI 수: 5개
  산출근거 있음: 5/5 ✅
  출처 있음:    4/5 ⚠️ (KPI3: 출처 누락)

═══════════════════════════════════════════════════
  전략 종합 점수: 87/100 (양호)
  CRITICAL: 0건 | WARNING: 5건 | INFO: 3건
═══════════════════════════════════════════════════
```

### 진단 항목

| # | 진단 항목 | CRITICAL 기준 | WARNING 기준 |
|---|----------|--------------|-------------|
| 1 | Win Theme 관통도 | Win Theme 0회 출현 | 5회 미만 출현 |
| 2 | S-E-P 구조 | Evidence 50% 미만 | Evidence 출처 90% 미만 |
| 3 | Action Title | Action Title 70% 미만 | Topic Title 존재 |
| 4 | 패턴 다양성 | 5종 미만 | 10종 미만 또는 특정 패턴 6회 이상 |
| 5 | 분위기 리듬 | — | white 5장 연속 |
| 6 | Bridge | Bridge 누락 | — |
| 7 | KPI 산출근거 | 산출근거 없음 | 출처 누락 |
| 8 | Part 3 필수 장표 | Concept Reveal 없음 | Strategy Framework 없음 |

### 점수 산정
- 100점 기준, CRITICAL 1건당 -15점, WARNING 1건당 -3점
- 90+ 우수 / 80+ 양호 / 70+ 보통 / 70 미만 개선 필요

---

## 뷰 모드 3: Slide List (슬라이드 목록)

모든 슬라이드를 1줄씩 나열하여 흐름을 파악합니다.

### 출력 형식

```
═══════════════════════════════════════════════════
  슬라이드 목록 (총 55장)
═══════════════════════════════════════════════════

── Part 1: SPARK (5장) ──────────────────────────
S01 [cover]    표지                                         dark     —       —
S02 [content]  "MZ세대 55분, SNS가 브랜드 접점 73%"          dark     W1      hero_stat
S03 [toc]      목차                                         white    —       —
S04 [content]  "3대 Win Theme으로 관통하는 제안 전략"          white    all     card_grid
S05 [content]  "관광 산업 디지털 전환, 지금이 기회"            light    W2      split_visual
               → Bridge: "이러한 시장 환경 속에서..."

── Part 2: PROBLEM→OPPORTUNITY (8장) ────────────
S06 [divider]  Part 2 구분자                                dark     all     —
S07 [content]  "국내 관광 시장 52조, 그러나 지역 편중 심화"    white    W1      hero_stat
...

── Part 3: SOLUTION (9장) ──────────────────────
S14 [divider]  Part 3 구분자                                dark     all     —
S15 [content]  컨셉 공개 — "[컨셉 키워드]"                    dark     all     concept_reveal
S16 [content]  전략 프레임워크                                dark     all     process_flow
...
```

### 표시 정보
- **슬라이드 ID**: S01~
- **유형**: cover, content, section_divider, toc
- **Action Title**: 인용부호로 표시 (cover/toc/divider는 설명)
- **분위기**: dark, white, light, gradient, branded
- **Win Theme**: W1, W2, W3, all, —
- **패턴 힌트**: hero_stat, card_grid 등
- **Bridge**: Part 마지막 슬라이드에 표시

---

## 편집 기능

뷰 출력 후 사용자 피드백에 따라 스크립트를 수정합니다.

### 피드백 처리

| 사용자 입력 | 처리 |
|------------|------|
| "S12 Action Title 수정: [새 제목]" | S12의 Action Title 교체 |
| "S12 Evidence 출처 추가" | S12 Evidence에 출처 보완 |
| "Part 4에 채널 전략 슬라이드 추가" | Part 4에 새 블록 삽입, 번호 재배정 |
| "S23~S25 삭제" | 해당 블록 제거, 번호 재배정 |
| "S15 패턴 card_grid → bento_grid" | 패턴 힌트 변경 |
| "S20~S24 분위기 단조로움 해소" | 중간에 dark/gradient 삽입 |
| "Win Theme W3 강화" | W3 관련 슬라이드에 Win Theme 태그 추가 |
| "Bridge 추가" | 누락된 Bridge 문장 보완 |
| "overview" / "strategy" / "list" | 해당 뷰 재출력 |

### 수정 후 자동 처리
1. 슬라이드 번호 재배정 (S01, S02, ...)
2. Part별 장수/비중 재계산
3. 분위기 리듬 재확인
4. 변경 요약 출력

---

## 시각 자료 필드 표시

슬라이드에 시각 자료(이미지/차트/출처)가 포함된 경우 Slide List에 표시:

```
S15 [content]  "벤치마킹 사례 3선"                          white    W2      gallery
               📷 이미지 2개 | 📊 차트 1개 | 📝 출처 3개
```

---

## 절대 하지 말 것

- ❌ 사용자 확인 없이 스크립트 내용을 임의 수정
- ❌ 슬라이드 번호를 건너뛰거나 중복 배정
- ❌ Bridge를 임의로 삭제
- ❌ Win Theme 테이블을 수정하면서 관련 슬라이드 태그를 업데이트하지 않는 것
