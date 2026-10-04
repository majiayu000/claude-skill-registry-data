---
name: surfacing-work-in-cmux
description: Use when work in this repo produces something the user would want to look at — a new spec or plan file under parfait/, a plan phase finishing, a test or gradle run, a screenshot or build artifact — and you are deciding where that output should appear. Covers cmux helper panes, sidebar status/progress, and the fallback when the terminal is not cmux.
---

# Surfacing Work in cmux

## Overview

superpowers가 **순서와 게이트**를 정한다. cmux는 그 진행을 **보이게** 할 뿐이다.

**핵심 원칙: cmux는 가산적 장식층이다.** cmux가 있든 없든 산출물의 경로·내용·커밋은
동일해야 한다. cmux 없이 이 repo를 쓰는 터미널에서 결과가 달라지면 이 스킬이 틀린 것이다.

## 게이트 (먼저 실행 — 필수)

```bash
[ -n "${CMUX_WORKSPACE_ID:-}" ] && command -v cmux >/dev/null 2>&1 && echo cmux || echo plain
```

- `plain` → **이 스킬은 여기서 끝난다.** 아무 것도 하지 않고 평소 superpowers 흐름 그대로 진행.
  "cmux가 없어서 X를 못 한다"고 보고하지 않는다. 없어도 잃는 게 없어야 정상이다.
- `cmux` → 아래 매핑 적용.

## 매핑 (superpowers 단계 → cmux)

| 단계 | 행동 |
|---|---|
| `brainstorming` 스펙 확정 | 파일 저장 후 `cmux open parfait/android/specs/<f>.md --workspace "$CMUX_WORKSPACE_ID" --pane pane:<helper> --no-focus` |
| `writing-plans` 계획 확정 | 같음(`parfait/android/plans/`) + `cmux set-status plan "0/<N>" --workspace "$CMUX_WORKSPACE_ID"` |
| `executing-plans` phase 전환 | `cmux set-progress <done/total> --label "Phase <n>: <제목>"` + `cmux log --level info -- "<phase> done"` |
| `test-driven-development` 루프 | 테스트를 helper surface에 `cmux send`, 결과는 `cmux read-screen`. 실패 출력이 사용자 화면에 남는다 |
| `verification-before-completion` | 이미 만든 아티팩트를 `cmux open ... --no-focus`. 아티팩트 **경로는 cmux와 무관하게 정한다** |
| `requesting-code-review` | `cmux diff`로 리뷰 대상 표시 |

helper pane 해소·surface 생성 규칙은 `cmux-workspace` 스킬을 따른다(여기 복제하지 않는다).

## 이 repo 전용 override

- **`/cmux-assets/<branch>/` 쓰지 않는다.** `cmux-workspace` 스킬의 기본값이지만 이 repo에선
  무효다. 산출물은 `parfait/` 또는 세션 scratchpad에 두고, cmux는 **열기만** 한다.
  cmux 전용 경로에 산출물을 두면 non-cmux 터미널에서 그 파일이 사라진다.
- **cmux 관련 파일을 커밋하지 않는다.** helper pane 배치, workspace 이름, surface ref는
  세션 상태지 repo 상태가 아니다.
- **`parfait/` 문서 본문에 cmux 명령·pane ref·workspace ID를 쓰지 않는다.** 문서는 어느
  터미널에서 읽어도 실행 가능해야 한다.
- git 3작업(commit/push/PR)은 여전히 사용자 확인 필수. cmux 자동화로 우회하지 않는다.

## 실패 처리

cmux 호출 실패는 **작업 실패가 아니다.** 한 번 실패하면 그 단계의 cmux 표시를 포기하고
본 작업을 계속한다. 재시도 루프·대체 경로 탐색 금지.

helper terminal을 만든 직후에는 `cmux surface-health` 또는 `read-screen`으로 실제로
붙었는지 확인한 뒤에만 "저기서 돌고 있다"고 말한다. 안 붙었으면 `nohup`·`tmux` 같은
숨김 fallback을 쓰지 말고 그대로 보고한다.

## 포커스

`select-workspace`·`focus-pane`·`focus-panel`·포커스성 `tab-action`은 사용자가 명시적으로
요청할 때만. 생성·이동 계열은 전부 `--focus false` / `--no-focus`. 사용자가 다른
workspace나 다른 앱을 보고 있을 수 있다.

## 흔한 실수

| 실수 | 결과 |
|---|---|
| cmux 없는 터미널에서 "표시 못 함" 보고 | 게이트가 `plain`이면 조용히 넘어가야 함 |
| 아티팩트를 `/cmux-assets`에 저장 | non-cmux 사용자에게 파일 없음 |
| 사이드바 진행률을 진행상황 정본으로 취급 | 정본은 `parfait/android/plans/*.md` 체크박스. 사이드바는 투영 |
| `cmux send`로 테스트 돌리고 결과 확인 없이 통과 선언 | `read-screen`으로 실제 출력 확인 후 판단 |
| cmux 호출 실패 → 작업 중단 | best-effort. 계속 진행 |

## Red Flags — 멈추고 재검토

- "cmux에서만 되는 방식으로 하면 편한데" → 이식성 위반
- "이 경로는 cmux가 열어주니까 괜찮다" → non-cmux에서 깨진다
- "포커스 한 번만 옮기면 사용자가 볼 텐데" → 명시 요청 없으면 금지
- "진행률 다 찼으니 승인된 걸로" → 게이트는 사람이다

## 연관

- `cmux-workspace` — helper pane·surface·사이드바 명령 상세
- `cmux-cli` — CLI 문법 확인(`cmux <command> --help` 먼저)
- `superpowers:executing-plans`·`superpowers:test-driven-development` — 순서와 게이트의 정본
