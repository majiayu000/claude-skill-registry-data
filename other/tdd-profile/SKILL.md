---
name: tdd-profile
description: TDD 세션이 끝난 뒤 "어디서 시간·토큰이 많이 들었나"를 단계(Skill)·에이전트별로 집계하고 병목과 model/effort 조정안을 보고한다. 세션 transcript를 읽는 사후 분석이며 코드를 바꾸지 않는다. "이번 TDD 세션 병목 분석", "토큰 어디에 썼어", "어느 단계가 느렸어", "모델 조정 제안", "/tdd-profile" 요청 시 사용.
argument-hint: "[session.jsonl | transcript-dir]  (없으면 현재 프로젝트의 최근 TDD 세션)"
allowed-tools: Bash(python3:*), Read
---

# TDD Profile Skill

`bin/tdd-profile.py`를 실행하고 그 출력을 **해석해서** 병목 3개 이내와 model/effort
조정안을 보고한다. 숫자는 스크립트가 산출하고, 판단은 이 스킬이 한다.

## GOAL

- 성공 = 사용자가 "다음 세션에서 무엇을 바꿀지" 3개 이내로 안다
- 입력: 세션 JSONL 경로, transcript 디렉터리, 또는 인자 없음(현재 cwd)
- 출력: 아래 OUTPUT FORMAT의 보고 1개 (터미널 30줄 이내)

## CONSTRAINTS

- 스크립트 출력에 없는 수치를 지어내지 않는다. 해석은 출력의 숫자를 인용해서 한다
- `in(total)`은 "턴 수 × 컨텍스트 크기"의 합이다. 이 값이 크다고 "많이 읽었다"고 말하지
  않는다 — 새로 읽은 양은 `cache+`, 긴 이유는 `turns`
- 메인 wall-clock은 에이전트 실행 대기를 포함하지 않는다(에이전트 행이 따로 있다).
  둘을 더해서 단계 시간으로 말한다
- 모델 제안은 스크립트의 휴리스틱(`out/turn`, `tools/turn`, edits)을 근거로 하되,
  코드 편집 에이전트(tdd-red/green/blue)를 haiku로 변경하자고 하지 않는다 — 편집 품질
  하락 위험이 절감분보다 크다
- hunk-reviewer가 에이전트 목록에 보이면 hook 차단 이전 세션인지 확인하고 보고한다
  (`hooks/block-hunk-reviewer.sh`, v1.17.0 이후는 차단됨)

## 절차

1. 실행 — 인자를 그대로 넘긴다:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/bin/tdd-profile.py" [인자]
   ```
   transcript 디렉터리가 없다는 오류면 사용자에게 세션 JSONL 경로를 요청한다
   (`~/.claude/projects/<cwd를 '-'로 치환한 slug>/`)
2. 출력의 네 절을 읽는다: 단계 표 → Agents → Heaviest turns → Recommendation
3. 병목 판정 순서:
   1. **에이전트 합산 시간 1위 타입** (Agents by type) — 호출 빈도를 줄일 수 있는가
   2. **단계별 wall + 에이전트 wall 합 1위** — 그 단계의 `turns`가 큰가(왕복 과다),
      `cache+`가 큰가(반복 읽기·캐시 만료)
   3. **Heaviest turns**의 `cache+` 300k 이상이 같은 단계에 집중되어 있는가 → 1h 캐시
      TTL 만료 또는 컨텍스트 압축 후 재적재 신호
4. model/effort: Recommendation 절의 단계별 제안과 "실제 사용" 절을 대조해 **다른
   곳만** 말한다 (이미 일치하면 "유지")

## OUTPUT FORMAT

```
## TDD 세션 프로파일 — <session-id 앞 8자리>
메인 <wall> / <turns>턴 / 에이전트 <n>개 <agent wall>

병목
1. <단계 또는 에이전트> — <숫자 인용> → <조치 한 줄>
2. ...
3. ...

model / effort
| 단계 | 실제 | 제안 | 근거 |
(다른 곳만, 최대 5행)

다음 세션에서 바꿀 것 (1~3개)
```

## FAILURE CONDITIONS

- 스크립트를 실행하지 않고 추정으로 보고
- 병목이 4개 이상이거나 조치 없는 병목
- `in(total)`을 "읽은 양"으로 해석
- 코드 편집 에이전트에 haiku 제안
