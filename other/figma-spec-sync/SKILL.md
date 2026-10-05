---
name: figma-spec-sync
description: >
  Figma 기획 파일을 기계 추출 스냅샷(md + 선택 PNG)으로 받아 이전 판본과의 구조 delta(섹션·화면·기획 설명)를 뽑고,
  그 변경을 구현 실물과 대조해 기존 정합 plan(대조표)의 작업 항목으로 라우팅하는 워크플로 skill.
  Figma REST API를 직접 부르므로 MCP 없이 반복 pull이 되고, 파일 version 게이트로 "plan이 아직 반영하지 않은 pull"을 판정한다.
  "figma 동기화", "figma 스냅샷 받아", "figma 뭐 바뀌었나", "figma diff", "기획 변경 확인", "figma 변경으로 계획 세워줘",
  "figma 정합 plan", "디자인 대조표 만들어", "figma sync", "figma spec snapshot", "figma delta", "what changed in figma",
  "align implementation with figma", "figma-spec-sync" 등에서 트리거. 디자인→코드 생성이나 Figma 파일 편집은 다루지 않는다.
---

# figma-spec-sync

Figma 기획 변경 → 작업 계획. 목적은 diff를 **보여주는** 게 아니라 변경을 **행선지가 있는 작업 항목으로 바꾸는** 것이다.

기본은 읽기 전용이다. plan에 쓰는 것은 사용자가 항목을 승인한 뒤이고, 유일한 예외는 §Sync 상태 표 갱신이다(판단이 아니라 기록).

## 전제

- Node 18+, git, Figma 토큰. 토큰은 env `FIGMA_TOKEN` 또는 `~/.config/figma/token`(scope `file_content:read`) — 발급은 `references/config.md`.
- 대상 repo의 설정 파일 `figma-spec-sync.json` — 스키마는 `references/config.md`. 첫 사용이면 §1에서 만든다.
- 정합 plan(대조표) — 없으면 `references/alignment-plan-template.md`로 만든다. §Sync 상태 표의 `Figma file version` 행이 게이트의 기준이다.
- `SKILL_DIR`은 이 SKILL.md가 있는 디렉토리다 — 스킬을 로드한 절대 경로에서 `SKILL_DIR="$(dirname <SKILL.md 절대 경로>)"`로 잡는다. 셸 상태는 호출 간에 유지되지 않으므로 명령마다 인라인으로 앞에 붙이거나 스크립트 절대 경로를 직접 쓴다.

## 실행 순서

### 1. Setup

설정 탐색 순서는 `--config` → `./figma-spec-sync.json` → `./docs/figma-spec-sync.json`. 없으면 사용자에게 Figma URL(file key·node-id)과 스냅샷 md·plan 경로를 물어 설정을 만들고, plan이 없으면 템플릿으로 뼈대를 만든다. 토큰이 없으면 스크립트가 발급 절차를 출력하고 멈춘다.

설정이 있으면 두 가지만 본다: `plan`이 가리키는 파일이 실재하는가, 그리고 `git status --short <out> <plan>`. `out`이 dirty면 이전 pull이 아직 triage되지 않은 채 working tree에 있는 것이고, `plan`이 dirty면 triage가 진행 중이다 — §3 게이트(base 판본 plan vs working tree md)를 읽을 때 이 상태를 알아야 한다.

### 2. Pull

```bash
node "${SKILL_DIR}/scripts/figma-sync.mjs" --config figma-spec-sync.json
```

version 게이트라 무변경이면 API 왕복 한 번(수 초)으로 끝난다. 기준은 이미지 캐시 state가 있으면 그것, 없으면 기존 md 서두의 version 줄 — clone만 한 머신에서도 같은 판정이다. 둘 다 없으면(첫 실행·구 포맷 md) 항상 받는다. 스냅샷 md는 손으로 고치지 않는다.

**"변경 없음"은 Figma↔md 판정이고 plan 반영 여부는 §3 게이트가 판정한다 — 항상 §3까지 돈다.** md가 최신인데 plan이 뒤처진 상태("변경 없음" + 게이트 미반영 + delta 큼)가 이 skill이 제일 자주 만나는 시작점이다.

### 3. 구조 delta

raw `git diff`는 섹션 개명을 거대한 삭제+추가로 보여 읽을 수 없다. 헬퍼가 섹션·화면·기획 설명 단위로 접는다.

```bash
node "${SKILL_DIR}/scripts/snapshot-delta.mjs" --config figma-spec-sync.json
```

기본은 `--base <deltaBase> --head :worktree`. 출력 서두의 두 블록을 먼저 읽는다:

- `[게이트]` — plan(base 판본) §Sync 상태의 version과 md(head)의 version을 대조한다. **다르면 plan이 아직 반영하지 않은 pull이 있고, 이 skill의 나머지 단계가 그 작업이다.** 같으면 아래 delta가 비어 있어야 정상이고, 비어 있지 않으면 §6의 표 갱신을 빠뜨린 것이다.
- `[검증]` — md 서두의 "추출 결과: 섹션 N개, 기획 설명 M건"과 파싱 결과를 대조한다. `⚠`가 뜨면 렌더 포맷이 바뀌어 파서가 낡은 것이다. delta를 믿지 말고 `snapshot-delta.mjs`의 `parse`를 먼저 고친다.

읽는 법:

- `~ A → B (화면 겹침 N%)` — 개명·재편. 100%면 이름만 바뀐 것이라 작업 항목이 아니다. 단 `✅` 류 접두사가 붙은 개명은 디자이너의 확정 신호라 버리지 않고 Gotchas대로 사용자 확인 대상에 올린다.
- `- 사라짐` + `+ 신규`가 같이 뜨면 개명이 아니라 **실제 재편**이다. 헬퍼는 화면 이름 겹침 30% 미만을 짝지어주지 않으므로 화면 단위로 사람이 이어붙이지 말고 신규 섹션으로 읽는다. 중첩 섹션(depth 2)이 depth 1로 승격되면 이렇게 보이고, 실제로도 재편이 맞다. 이건 화면 lineage 얘기이고 **도메인 소속은 §6에서 따로 판정한다** — 사라진 섹션과 같은 도메인의 plan이 있으면 신규 섹션은 그 plan으로 간다.
- `+ 신규: X (화면 N, 설명 M)` 아래에 화면 이름이 나열되고, 신규 섹션의 기획 설명은 `[기획 설명]`에 **전문**이 출력된다. 여기가 작업 항목의 원재료다.
- `+ 신규: X (화면 0, 설명 0)` — 빈 섹션은 기획이 없는 게 아니라 추출 한계(작은 프레임·짧은 메모·낱개 목업)로 비어 보이는 것이다. §Figma 직접 보기로 실물을 확인하고 §6의 "담지 않는 축"으로 라우팅한다.

이미 publish된 구간을 다시 보려면 `--base <이전 commit> --head <rev>`. 옵션은 `--help`.

### 4. 기존 결정과 충돌하는지 확인하고 최신 원본으로 재판정

**최신 Figma가 기준이다.** 기획은 계속 바뀌므로 이전 결정이 있어도 원본이 바뀌면 최신본으로 다시 판단한다. 이 단계의 목적은 결정을 지키는 게 아니라 **무엇이 되돌아가는지 드러내는 것**이다 — 신규 내용을 spec으로 취급하기 전에 그 영역에 이미 내려진 판단이 있는지 plan의 결정 로그·확인 필요·해당 화면 절에서 찾고, 충돌하면 사용자에게 유효성을 되묻지 않고 재판정한 뒤 되돌린 결정을 결정 로그와 보고에 명시한다. 재판정은 자동 채택이 아니다 — Figma가 준 것과 사용자가 직접 말한 것을 구분해 적는다.

### 5. 구현 실물과 대조

기획 설명은 가설이고 현재 동작은 source가 권위다. 각 delta마다 실제로 뭐가 있는지 확인하고 `file:line`으로 근거를 남긴다. 근거 출처는 스킬이 아니라 **대상 repo에서 도출한다** — AGENTS.md·README·디렉토리 구조에서 라우트 정의, 기능 게이팅(feature flag·registry), DB schema, API 계약(OpenAPI·controller)의 위치를 찾아 표로 정리하고 그 표를 이번 세션의 기준으로 쓴다.

### 6. 라우팅 — 새 plan을 만들지 않는다

행선지가 이미 있다. 없을 때만 새로 만든다.

| delta 성격 | 행선지 |
|---|---|
| **매 pull의 규모·version** | plan §Sync 상태 표 + "pull에서 반영된 변화" 문단. **delta가 비어도 갱신한다** — 이 표의 version이 §3 게이트의 기준이라 빠뜨리면 다음에 이미 본 delta가 다시 미반영으로 판정된다 |
| 기존 화면 절의 기획 변경 | plan의 해당 화면 절 |
| 소유 plan이 있는 신규 도메인의 기획 도착 | 그 도메인 plan. 대기 그룹에서 진행 그룹으로 올릴지는 사용자 판단 |
| 소유 plan이 없는 신규 영역 | plan에 새 절 + 대상 repo의 roadmap 문서(있으면) |
| 기획 내부 불일치·해석 불가 | plan §확인 필요 |
| 추출 한계로 안 보이는 것 | plan §Sync 상태의 "담지 않는 축" 목록 |

새 plan이 필요하면 대상 repo의 plan 규약(위치·untracked 인큐베이션 여부)을 따른다.

### 7. 출력

작업 항목은 **제안**으로 내고 승인 전에 plan에 쓰지 않는다. 항목마다: 무엇이 바뀌었나(Figma 근거) · 현재 구현은 어떤가(`file:line`) · 무엇을 해야 하나 · 행선지. §Sync 상태 표만 바로 갱신한다.

스냅샷 md와 plan 갱신은 **같은 브랜치·같은 PR**에 묶는다. 갈라놓으면 main이 md는 받고 plan version은 옛것인 상태가 생겨, 게이트는 "미반영"이라 하고 delta는 "변화 없음"이라 하는 모순이 난다. commit·PR·merge 절차는 대상 repo 규약을 따른다.

## Figma 직접 보기

스냅샷이 답하지 못하는 지점(빈 신규 섹션·짧은 메모·낱개 목업·작은 프레임)에서 "Figma를 연다"는 에이전트에게는 Figma MCP(`mcp.figma.com`) 호출이다. 스냅샷 md의 모든 화면·섹션·기획 설명 링크에 `node-id`가 있으므로 그 id로 바로 본다. 대량·반복 조회는 여기가 아니라 REST 스냅샷이다 — MCP는 **특정 node 하나를 들여다보는 저빈도 조회**에만 쓴다.

- `get_screenshot` — 노드 하나를 PNG로. 1000×600 미만 프레임(템플릿·컴포넌트 크기)과 낱개 목업의 실물 확인.
- `use_figma` 읽기 전용 스크립트 — 특정 섹션 아래를 `findAll`로 훑어 60자 미만 TEXT·프레임 밖 노드를 즉석 조회. 호출 전에 `figma-use` 스킬을 먼저 로드한다(호출마다 페이지 컨텍스트가 리셋되고, 쓰기 규칙이 같은 도구에 걸려 있다).

진입 조건: 첫 호출 전 `whoami`로 seat를 본다 — Starter 플랜과 유료 플랜의 View/Collab seat는 **월 6콜**이라 triage 도구로 못 쓴다. MCP가 없거나 제한이면 사용자에게 node-id 링크를 주고 브라우저 확인을 요청한다. 코멘트는 MCP에 도구가 없어 이 경로로도 못 본다.

## Gotchas

- **version은 내용이 아니다.** Figma `version`은 본문이 한 글자도 안 바뀌어도 올라간다(실측: version 상이, md 본문 바이트 동일). 게이트 "미반영" + delta "변화 없음"은 정상이고 할 일은 §Sync 상태 version 갱신 하나다. 이걸 "delta 헬퍼가 놓쳤다"로 진단하지 않는다.
- **확정 디자인이 아니다.** 화면마다 다른 버전이 섞여 있고 메뉴 구성은 계속 바뀐다. 정합 대상은 기획 **의미**이지 그런 표면이 아니다. `✅` 같은 접두사는 디자이너의 확정 표시로 읽되 근거로 삼기 전에 사용자에게 확인한다.
- **화면 수가 세 종류다.** md 표는 *이름 있는* 프레임을 세되 `Body`·`App`처럼 이름만 있는 컨테이너도 섞여 있다. PNG와 pull 로그의 "화면 N개"는 크기 기준(`FRAME` 1000×600 이상)이라 이름 없는 안쪽 컨테이너까지 잡는다. 세 숫자를 같은 것으로 보고 "누락"을 진단하지 않는다.
- **스냅샷이 구조적으로 담지 않는 축** — 여기 없다고 기획에 없는 것이 아니다. 판단이 걸리면 §Figma 직접 보기. (1) 코멘트: 미결 논의가 코멘트에만 있는데 스크립트는 노드 트리만 받고 MCP에도 코멘트 도구가 없다 — REST `/comments` 수집을 스크립트에 추가하는 것이 유일한 경로다. (2) 60자 미만 메모: `SPEC_MIN_LENGTH`가 짧은 전이 지시·조각 메모를 떨어뜨린다. (3) 캔버스 낱개 목업: 프레임으로 묶이지 않은 노드는 표에도 PNG에도 없다. (4) 1000×600 미만 프레임: 템플릿·컴포넌트 크기는 렌더 대상이 아니다. (5) 중첩 섹션 라벨: depth 2 `SECTION`은 이름이 사라지고 화면만 평평하게 나열된다.
- **같은 `images`(=state)를 가리키는 실행은 한 곳에서만.** 다른 checkout에서 같은 images로 돌리면 state만 앞서 나가고 원래 checkout의 md는 낡은 채 "변경 없음"으로 끝나 영구히 안 고쳐진다. 정기 실행(cron·launchd)을 두면 그 래퍼가 유일한 images 소유자다.
- **스냅샷을 승인 전에 commit하는 lane**이면 `deltaBase`를 publish 지점(`main` 등)으로 준다. commit은 "확인했다"의 표시가 아니고, plan이 기록한 version만 triage 완료의 마커다.
- **파서는 렌더 포맷에 결합돼 있다.** 두 스크립트는 한 디렉토리에서 같이 움직인다. `[검증] ⚠`가 뜨면 delta보다 파서를 먼저 본다.

## 관련

- 문서 repo ↔ 구현 repo 동기화의 evidence 규칙·쓰기 방향은 `repo-prd-sync` skill. 이 skill은 소스가 문서가 아니라 디자인 툴 API인 경우를 다룬다.
- 화면 PNG는 `images` 디렉토리의 `index.html`을 브라우저로 열어 훑는다. repo 밖이고 git 추적 대상이 아니다.
