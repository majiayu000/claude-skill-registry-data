---
name: repo-prd-sync
description: >
  구현 repo와 PRD/design repo 사이의 수동 동기화를 가드하는 스킬.
  PRD/design 문서를 truth가 아니라 decision snapshot으로 보고, pull-in,
  back-sync, doc drift 점검에서 evidence 확인, working tree 확인, 단방향 쓰기,
  경로 하드코딩 제거를 강제한다. "PRD 반영", "디자인 문서랑 구현 동기화",
  "문서 기준으로 구현 계획 세워줘", "구현 내용을 PRD에 반영해줘",
  "PRD가 구현이랑 맞는지 확인", "design doc stale", "repo prd sync",
  "sync PRD with repo", "update PRD from implementation", "back-sync",
  "pull-in" 등의 요청에서 트리거.
---

# Repo PRD Sync

구현 repo와 PRD/design repo 사이의 수동 동기화를 안전하게 수행한다.
자동 복사나 양방향 merge가 아니라, 사실 확인과 쓰기 방향 통제를 위한 스킬이다.

## 왜 이 스킬이 존재하는가

Claude는 PRD/design 문서를 현재 truth로 과신하거나, 구현 repo와 문서 repo를 한 번에 고치거나, 이전 프로젝트 경로를 새 작업에 끌고 오는 실수를 하기 쉽다.
이 스킬은 그 세 가지 실패를 막기 위해 evidence, 쓰기 방향, repo 역할을 먼저 고정한다.

## 모드 선언

- `implementation repo`: 실제 구현, 런타임 동작, 테스트, API, schema가 있는 repo.
- `PRD/design repo`: 요구사항, 설계 의도, 의사결정 snapshot이 있는 repo.
- PRD/design 문서는 truth가 아니라 decision snapshot이다. 현재 구현이나 runtime data와 다르면 먼저 어느 쪽이 맞는지 확인한다.
- 한 번의 흐름에서는 쓰기 방향을 하나로 고정한다.
- 방향을 바꿔야 하면 현재 결과를 보고하고 사용자 확인을 받은 뒤 새 흐름으로 전환한다.
- review/검토/확인/분석 요청은 읽기 전용이다. `수정해줘`, `고쳐줘`, `해결해줘`, `반영해줘`, `구현해줘`, `커밋해줘` 같은 명시적 실행 요청이 있어야 쓰기 작업을 한다.

## 시작 게이트

1. 요청에서 방향을 판정한다.
   - `pull-in`: PRD/design repo를 읽고 implementation repo에 계획, 기준, 구현 변경을 만든다.
   - `back-sync`: implementation repo를 읽고 PRD/design repo 문서를 정정한다.
2. 두 repo의 역할과 경로를 확인한다.
   - 사용자 발화에 명시된 경로를 우선한다.
   - 현재 `cwd`, git remote, 주변 문서로 식별 가능하면 그 근거를 말한다.
   - 둘 중 하나라도 불명확하면 추측하지 말고 필요한 경로만 질문한다.
3. 양쪽 repo에서 `git status --short`를 확인한다.
   - 관련 없는 사용자 변경은 그대로 둔다.
   - 쓰기 대상 repo에 충돌 가능성이 있는 변경이 있으면 먼저 보고한다.
4. 각 repo의 `AGENTS.md`, `README.md`, 관련 docs index를 확인한다.
   - 프로젝트별 문서 구조, index 갱신, archive 규칙은 고정 규칙이 아니라 해당 repo 컨벤션으로 확인한다.

## Evidence 규칙

문서와 구현이 다르면 아래 순서로 확인한다. 상위 evidence가 없으면 그 사실을 결과에 남긴다.

1. runtime data, API response, database value, logs
2. source code, schema, config, tests
3. git history, commits, linked issues
4. PRD/design 문서

PRD/design 문서만 근거로 구현 상태를 단정하지 않는다.

## Pull-In 흐름

PRD/design repo의 decision snapshot을 implementation repo 작업 기준으로 가져오는 흐름이다.

1. PRD/design repo에서 대상 문서와 관련 문서를 읽는다.
2. 문서의 요구, 결정, 미정 항목을 분리한다.
3. implementation repo에서 현재 구현, schema, API, config, runtime data 중 필요한 증거를 확인한다.
4. 문서와 구현이 다르면 `discrepancy`로 기록한다.
   - 문서가 stale인지, 구현이 요구를 충족하지 못하는지, 둘 다 불명확한지 구분한다.
5. 쓰기는 implementation repo에만 한다.
   - review/검토 요청이면 읽기 전용으로 끝낸다.
   - 구현/수정/반영 요청이면 implementation repo 안의 plan, docs, code만 변경한다.

## Back-Sync 흐름

implementation repo에서 확인한 실제 상태를 PRD/design repo 문서에 반영하는 흐름이다.
사용자가 명시적으로 PRD/design repo 반영을 요청했을 때만 실행한다.

1. implementation repo에서 실제 동작과 source of evidence를 확인한다.
2. PRD/design repo에서 수정 대상 문서와 문서 컨벤션을 확인한다.
3. 반영 항목을 세 가지로 분리한다.
   - confirmed: 구현과 runtime evidence로 확인된 사실
   - inferred: 코드 구조나 변경 이력에서 추론한 내용
   - open: 사용자 결정이나 추가 검증이 필요한 내용
4. 쓰기는 PRD/design repo 문서에만 한다.
   - implementation repo의 코드를 동시에 수정하지 않는다.
   - PRD/design repo의 index나 navigation 파일은 해당 repo 컨벤션에서 필요성이 확인된 경우만 수정한다.

## 출력 규칙

작업 전에는 아래 항목을 짧게 선언한다.

- mode: `pull-in` 또는 `back-sync`
- repos: implementation repo path, PRD/design repo path
- write boundary: 읽기 전용 또는 쓰기 대상 repo

결과 보고에는 아래 항목을 포함한다.

- evidence checked: 확인한 문서, source, runtime evidence
- discrepancies: 문서와 구현이 어긋난 항목, 없으면 `없음`
- changes: 수정한 파일, 없으면 `없음`
- open items: 사용자 결정 또는 추가 검증이 필요한 항목, 없으면 `없음`

수정 후에는 변경 파일과 검증 명령을 함께 보고한다.

## Gotchas

- 같은 세션에서 pull-in과 back-sync를 섞으면 양쪽 repo 변경이 얽힌다. 방향 전환은 사용자 확인 뒤 별도 흐름으로 처리한다.
- PRD/design 문서의 구체 경로, index 파일, archive 규칙은 repo마다 다르다. 새 스킬 본문에 특정 구조를 고정하지 말고 현재 repo에서 확인한다.
- "문서와 맞지 않는다"는 곧바로 구현 버그가 아니다. 문서가 오래됐을 수 있으므로 source, tests, runtime data를 먼저 비교한다.
- back-sync는 구현을 미화하는 작업이 아니다. 확인된 사실만 반영하고, 추론이나 미정 사항은 그렇게 표시한다.
- 쓰기 대상 repo에 unrelated changes가 있으면 덮어쓰지 않는다. 변경 범위를 좁히거나 사용자에게 충돌 위험을 보고한다.
- 두 repo가 같은 workspace 아래에 있으면 상대 경로가 헷갈리기 쉽다. 결과 보고에는 항상 역할명과 경로를 함께 적는다.
- `git status`를 현재 `cwd`에서만 보면 다른 repo의 변경을 놓친다. 두 repo 각각에서 확인한다.
- "index도 같이 갱신해야 할 것 같다"는 추측으로 navigation 파일을 고치지 않는다. 해당 repo의 문서 컨벤션에서 필요성이 확인될 때만 갱신한다.
- runtime evidence 없이 source만 본 경우에는 `confirmed`가 아니라 source-based finding으로 보고한다.
