---
name: compound
description: >
  방금 해결한 문제를 `docs/solutions/`에 YAML frontmatter가 붙은 검색 가능한
  단위로 자산화한다. 다음 세션에서 grep/rg로 즉시 재사용 가능한 형태로 압축.
  "이 문제 자산화해줘", "solution 저장", "이번 디버깅 정리해서 저장",
  "지금 알아낸 거 저장", "compound 이거", "compound this",
  "save this lesson", "capture this solution", "이걸 solutions에 저장",
  "lesson 저장", "knowledge capture", "이 패턴 자산화" 등에서 트리거.
  session-history와 달리 대화 전체가 아니라 problem → root cause → fix → 재사용 패턴
  네 축에 한정한다.
---

# Compound

방금 해결한 문제 하나를 `docs/solutions/`에 검색 가능한 단위로 압축한다.
다음에 같은 패턴이 다시 등장할 때 grep 한 번으로 끝나도록.

이름은 복리(compound interest)에서 왔다. 같은 문제를 두 번 풀지 않기 위함.

## session-history와의 차이

| 구분 | session-history | compound |
|------|-----------------|----------|
| 단위 | 세션 한 건의 의사결정 흐름 | 문제 한 건의 해법 패턴 |
| 출력 | 시간순 narrative | problem/root-cause/fix/applies-to 4축 |
| 검색 키 | 날짜·세션명 | tags, applies-to, 증상 키워드 |
| 재사용 방식 | 후속 세션 핸드오프 | 다음 occurrence에서 grep |

세션 마무리에서 의사결정 기록이 필요하면 `session-history`.
방금 해결한 *문제 하나*가 재발 가능한 패턴이면 `compound`.
둘 다 해당하면 두 스킬 모두 실행해도 된다.

## 저장 경로

`docs/solutions/YYYY-MM-DD-<slug>.md`

- `<slug>`는 문제의 증상 또는 도메인 키워드 (kebab-case).
- 같은 날짜·slug 파일이 있으면 덮어쓰기 전 사용자 확인.
- `docs/solutions/` 디렉토리가 없으면 생성.

## Frontmatter 스키마

```yaml
---
problem: 한 줄로 증상 또는 트리거. grep으로 발견되는 첫 단서.
root-cause: 한두 줄. 진짜 원인. "왜 그렇게 되는가"까지 들어가야 함.
fix: 한두 줄. 무엇을 바꿨는지. 코드가 아니라 변경의 의도.
applies-to: # 재발 가능한 환경/스택. 비어 있으면 생략.
  - <stack/lib/framework 식별자>
tags: # grep 보조용 키워드. 동의어·증상·에러 메시지 핵심어.
  - <keyword>
related: # 관련 solutions/plans 경로. 없으면 생략.
  - docs/solutions/<other-file>.md
---
```

`<` 또는 `>` 문자는 frontmatter 파싱을 깬다. 본문에서도 꺾쇠 대신 backtick 사용.

## 수집 절차

### 1. 트리거 확인

다음 신호 중 하나가 있을 때 자산화 가치가 있다. 없으면 사용자에게 "정말 저장할 가치가 있는지" 한 번 묻는다.

- 해결까지 30분+ 들었거나 막힌 경험이 있었다
- 비명시적 의존성·문서화되지 않은 동작·timing 이슈가 원인이었다
- 같은 스택에서 재발 가능성이 있다
- 다른 사람/세션이 grep으로 빨리 발견하면 시간이 절약된다

5분 안에 풀린 단순 문제·자기설명적 fix는 자산화 비대상.

### 2. 4축 추출

현재 세션 컨텍스트와 다음 소스에서 추출한다:

- 최근 commit message + diff (`git log --oneline -10`, `git diff HEAD~1`)
- 사용자가 명시한 problem 요약
- 디버깅 중 발견한 *비명시적* 사실 (timing, version, hidden state)

추출 우선순위:
- **root-cause는 fix보다 중요하다.** fix는 diff를 보면 알지만 root-cause는 휘발된다.
- "왜 안 됐는가" 한 단계로 끝나면 부족. "왜 그게 안 되도록 설계됐는가"까지.
- applies-to는 *최대한 좁게* — 너무 넓으면 다음 검색에서 false positive.

### 3. 작성 후 한 번 더 묻기

저장 전에 사용자에게 다음을 확인:

- slug가 검색하기 좋은가 (동의어 빠지지 않았나)
- tags에 사용자가 검색 시 떠올릴 단어가 들어 있는가
- root-cause 한 문장이 *이 문서를 보는 미래의 자신*에게 충분한가

확인 없이 바로 저장하면 다음에 못 찾는다.

## 출력 템플릿

```markdown
---
problem: <한 줄 증상>
root-cause: <한두 줄, 진짜 원인>
fix: <한두 줄, 변경 의도>
applies-to:
  - <stack/lib>
tags:
  - <keyword>
related:
  - <path>
---

# <제목>

## Problem

증상이 어떻게 나타났는지. 재현 조건. 처음 본 사람이 "이 상황 맞다"고 판단할 수 있게.

## Root Cause

진짜 원인. 비명시적 가정, 숨겨진 의존성, timing 등. 코드를 보면 알 수 있는 표면 원인은 fix에 둔다.

## Fix

무엇을 어떻게 바꿨는가. 코드 블록은 1개까지, 핵심만. 변경의 *의도*에 집중.

## Patterns to Reuse

- 다음에 같은 증상이 보이면 우선 확인할 곳
- 같은 root cause가 가능한 다른 표면

## Related

- 관련 plan, 다른 solution, 외부 링크
```

`Patterns to Reuse` 섹션이 자산화의 핵심. 이게 비어 있으면 단순 회고록이지 compound 자산이 아니다.

## 검색·재사용

다음 세션에서 같은 패턴을 만났을 때:

```bash
rg -l 'tag-or-keyword' docs/solutions/
rg -n 'applies-to:' docs/solutions/ | rg <stack>
```

`Patterns to Reuse` 섹션이 grep으로 찾기 좋도록 키워드를 의도적으로 포함시킨다.

## Gotchas

- **fix만 적고 root-cause를 빠뜨리는 게 가장 흔한 실패.** diff를 보면 fix는 알 수 있다. 자산화 가치는 root-cause + Patterns to Reuse에 있다.
- **slug를 도메인 용어로만 쓰면 다음에 못 찾는다.** 증상 키워드를 1개는 포함시킨다. 예: `2026-05-22-rn-metro-log-missing.md` (도메인 `rn-metro` + 증상 `log-missing`).
- **applies-to 과대 일반화 금지.** "JavaScript"는 거의 무의미. "React Native 0.77+", "Next.js 14 app router" 수준의 좁은 범위가 검색에 유용.
- **세션 종료 전 묻지 않으면 컨텍스트가 날아간다.** 큰 문제를 풀었으면 끝나기 전에 이 스킬을 트리거할지 사용자에게 한 번 묻는다.
- **session-history와 중복 호출.** 둘 다 필요한 경우 compound 먼저 (좁은 단위) → session-history (전체 narrative). 순서 반대면 compound 단계에서 세션 종료 상태라 컨텍스트 손실.
- **5분짜리 사소한 fix를 저장하는 함정.** 재발 가능성이 낮거나 diff로 자명한 변경은 자산이 아닌 노이즈. 트리거 단계에서 한 번 거른다.

## 범위 외

- 세션 전체 의사결정 기록 — `session-history`.
- plan 작성 — `plan`.
- 메모리 정리·승격 — `clean-memory`.
- 변경 의도 추적(이미 commit된 변경에 대해 *왜* 바꿨는지) — `trace-change-why`.
