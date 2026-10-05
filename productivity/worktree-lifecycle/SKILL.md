---
name: worktree-lifecycle
description: >
  git worktree 기반 task workflow의 lifecycle 단계를 식별하고 단계별 inspect 항목,
  결정 트리, 체크리스트를 안내하는 스킬. 자동 실행은 하지 않는다.
  "worktree 만들까", "여기서 바로 할까", "fast-path", "slug 뭐로 할까",
  "이거 분량이 작아서 main에서 해도 될까", "plan scaffold commit", "worktree 정리",
  "main 머지 준비", "squash merge", "branch 삭제해도 돼", "worktree remove",
  "logical DB drop", "followups 정리", "plan archive" 같은 요청에서 트리거.
  작업 시작 전 fast-path 판단과 squash & cleanup이 주 시점이고, 그 사이 Working,
  Squash 직전 정리도 보조로 다룬다. 특정 경로, 스크립트 이름, DB 이름 규칙, branch 이름은 고정하지 않는다.
---

# Worktree Lifecycle

git worktree 기반 task workflow를 시작과 종료 시점에서 안전하게 닫기 위한 스킬.
실제 명령 실행은 사용자 또는 다른 스킬이 한다. 이 스킬은 단계 식별, inspect, 결정 트리, 체크리스트만 다룬다.

## 용어: 통합 branch

이 문서는 feature 작업이 합쳐지는 대상을 **통합 branch**라고 부른다. 실제 이름은 repo가 정한다 — `main`인 repo도 있고, `main`을 release pointer로 두고 `develop`을 통합 branch로 쓰는 repo도 있다. **기본값을 가정하지 않는다.** 대상 repo의 `AGENTS.md`에서 작업 시점에 확인한다. 통합 branch를 잘못 잡으면 squash가 엉뚱한 곳에 얹히고 cleanup의 반영 확인이 통과해도 실제로는 유실이다.

## 이 스킬이 막는 실패

worktree workflow에서 가장 자주 발생하는 실수는 lifecycle 단계를 잘못 잡는 데서 온다.

- fast-path로 끝났어야 할 좁은 변경에 worktree 만들어서 시간 낭비.
- 반대로 dependency 추가나 schema 변경을 통합 branch에서 시작했다가 commit이 둘로 갈라지고 unrelated diff가 섞임.
- squash 직전 정리(followups, archive)를 worktree branch에 commit하지 않아 통합 branch 히스토리에 사후 별도 commit으로 분리됨.
- squash가 통합 branch에 반영되지 않은 상태에서 worktree remove 또는 `git branch -D`로 작업 유실.
- worktree DB 분기를 빠뜨려 root DB가 오염되거나, 반대로 root DB를 worktree에서 mutate.
- 다른 worktree의 파일에 `reset`, `clean`, `checkout .`, `restore .` 같은 destructive 명령을 적용.

## 모드 선언

이 스킬은 한 시점에 한 단계만 다룬다. 활성되면 먼저 현재 단계를 명시한 뒤 그 단계의 체크리스트만 본다.

- `setup`: 새 작업 시작 직전. fast-path 또는 worktree 결정.
- `working`: 이미 worktree 안에서 작업 중. dirty 보존, 다른 worktree 격리, plan scaffold commit.
- `prep`: working 단계 commit 종료 후 squash 직전. followups, plan archive 정리.
- `cleanup`: squash가 통합 branch에 반영된 뒤 worktree, branch, logical DB 정리.

단계가 불분명하면 사용자에게 묻기 전에 git state로 추정한다.

| 관찰 | 추정 단계 |
| --- | --- |
| root checkout, working tree clean | `setup` |
| feature branch, dirty, plan 문서 아직 archive 전 | `working` |
| feature branch, 본 작업 commit 종료 + plan 문서 archive 전 + 사용자가 squash 준비 신호 | `prep` |
| 통합 branch에 squash commit 반영됨 + worktree 잔존 | `cleanup` |

추정이 어긋났을 때만 사용자에게 단계를 확인한다.

## 작업 시점에 먼저 inspect

대상 repo의 worktree 컨벤션은 repo마다 다르다. 단계 진입 전에 다음을 직접 읽는다. 사용자에게 묻지 않는다.

1. `git status --short --branch`
2. `git worktree list --porcelain`
3. 대상 repo의 worktree 정책 문서: `AGENTS.md`, scoped `AGENTS.md`, `README.md`. 통합 branch 이름을 여기서 확정한다.
4. init/remove 스크립트 존재 여부: 보통 `scripts/worktree-*.sh` 또는 동등한 자동화. 있으면 단계별로 무엇을 자동 처리하는지 본다 (branch 생성, DB 분기, env 파일, install, migrate).
5. logical DB 분기 정책: 단일 postgres 컨테이너를 공유하면서 DB 이름만 분기하는지, 또는 컨테이너 자체를 분기하는지.
6. plan/followups/archive 문서 위치와 범위 밖 항목의 라우팅 규칙.

이 정보가 없으면 단계별 결정을 내릴 수 없다. 읽고 단계로 들어간다.

## Setup: fast-path vs worktree

분량으로만 판단하지 않는다. 변경 종류가 우선이다. 아래를 **모두** 만족하면 fast-path. 하나라도 깨지면 worktree.

1. 시작 시 working tree가 clean이다. 단, 대상 repo가 plan/brainstorm untracked buffer를 허용하면 그 경로만 예외다.
2. 예상 변경이 단일 logical commit 1개로 닫힌다. 예: doc 오타, 좁은 fix, lint/format, 작은 config 수정.
3. DB schema/migration 변경, dependency 추가·변경, cross-package refactor가 **없다**.
4. plan 문서가 필요 없을 만큼 작다.

도중에 조건이 하나라도 깨지면 그 자리에서 멈추고 worktree로 옮긴다. 부분 작업을 통합 branch에 commit해 두고 worktree에서 마저 진행하는 식으로 분리하지 않는다. 분리하면 followups/archive 라이프가 끊긴다.

fast-path를 선택하면 working/prep/cleanup은 적용되지 않는다. 단일 commit으로 닫고 이 스킬에서 빠진다.

fast-path의 작업 위치도 통합 branch 규칙을 따른다. repo가 특정 branch의 직접 작업을 금지하면(release pointer 보호 등) 그 금지가 fast-path에도 그대로 적용된다.

### Worktree 셋업 항목

대상 repo에 init 스크립트가 있으면 손으로 분해하지 않는다. 스크립트가 branch, DB, env, install, migrate를 묶어 처리하도록 위임한다. 다음만 결정해 준다.

- slug: kebab-case, 변경 범위가 그대로 드러나는 이름. squash commit 제목과 worktree branch가 같은 어휘를 쓰도록 맞춘다.
- base branch: 대상 repo의 통합 branch. 다른 branch가 base이면 그 근거를 plan에 남긴다.
- worktree 경로: 대상 repo 컨벤션 우선. 자체 경로를 발명하지 않는다.
- logical DB 분기 필요성: schema/migration/seed 변경이 작업 범위면 필요. 그렇지 않으면 root와 격리만으로 충분한지 정책 문서로 확인한다.
- root checkout에 있는 untracked plan/design 파일: worktree로 같이 옮길지 결정. init 스크립트가 옵션을 제공하면 그쪽을 쓴다.
- 첫 commit이 plan scaffold가 되도록 준비한다. 구체 규칙은 Working 단계에서 다룬다.

## Working

- feature branch 첫 commit은 plan scaffold다. 본 작업 commit이 plan보다 앞서면 plan lifecycle이 한 squash commit에 닫히지 않는다.
- 다른 worktree의 파일을 delete/reset/restore/clean/move하지 않는다. 다른 worktree의 변경은 그 worktree 안에서만 다룬다.
- dirty 상태를 한 번이라도 본 뒤에는 state-changing 작업 전에 commit/stash로 보존한다. 사용자 확인 없이 destructive 명령을 쓰지 않는다.
- dependency 변경은 `package.json`과 lockfile 기준으로 판단한다. `node_modules` 존재 여부만 보고 결론짓지 않는다.
- DB migration 생성 명령의 실행 위치와 draft migration의 commit 여부는 대상 repo 정책이 정한다. **repo마다 정반대라 기본값을 가정하지 않는다** — worktree에서 생성해 schema와 함께 commit하는 repo가 있고, root checkout에서만 생성하고 worktree migration은 commit하지 않는 repo가 있다. 작업 전 해당 repo의 db package 문서를 읽는다.

## Prep: squash 직전 정리

이 정리를 worktree branch commit에 포함시키지 못하면 squash 이후 통합 branch에 사후 별도 commit으로 분리된다. 그러면 한 squash commit 안에 plan lifecycle이 닫히지 않는다.

1. plan 범위 밖에서 발견한 항목은 대상 repo의 라우팅 규칙에 따라 행선지를 정한다. 규칙이 없으면 followups 문서 상단에 새 entry로 추가한다. 다른 문서 본문 산문에 끼워넣지 않는다 — entry로 두어야 다음 사이클에서 식별 가능하다.
2. 완료된 plan 문서는 archive 경로로 이동한다. 사후 별도 commit으로 미루지 않는다.
3. 위 두 정리를 worktree branch에 commit한 뒤 확인 없이 squash로 넘어간다. 정리 commit과 working commit을 한 commit으로 묶을 필요는 없다. squash가 합쳐 준다. push는 사용자가 요청할 때만 한다.

## Cleanup

순서를 지킨다. 거꾸로 하면 작업이 유실된다.

1. squash가 통합 branch에 반영됐는지 먼저 확인한다. 예: `git log <integration> --oneline -1`, `git merge-base --is-ancestor <squash> <integration>`. branch를 통합 branch 끝에 rebase한 뒤 squash했다면 `git diff --quiet <branch> <integration>`으로 tree가 같은지도 본다. 머지된 commit을 직접 본 뒤에만 다음 단계로 간다.
2. worktree 제거. 대상 repo에 remove 스크립트가 있으면 사용한다. 없으면 `git worktree remove <path>`.
3. logical DB drop. remove 스크립트가 처리하지 않으면 별도로 drop한다. drop 전 다른 worktree나 root가 같은 DB를 참조하지 않는지 확인한다.
4. merged feature branch 삭제. squash 반영 확인 후에만 `git branch -d` (필요시 `-D`).
5. root checkout에서 `git status`와 `git worktree list`로 정리 결과를 확인한다.

squash가 통합 branch에 반영되지 않은 상태에서 worktree remove 또는 `branch -D`를 실행하지 않는다. 사용자가 명시적으로 폐기를 지시한 경우에만 예외.

## Anti-pattern

- fast-path 조건이 깨졌는데 통합 branch에서 계속 진행. 결과적으로 분리된 commit이 쌓이거나 unrelated 변경이 섞인다.
- 통합 branch 이름을 확인하지 않고 `main`으로 가정. release pointer를 `main`으로 두고 `develop`에 통합하는 repo에서 squash가 보호된 branch로 향한다.
- worktree는 만들었지만 logical DB 분기를 빠뜨림. schema/seed 변경이 root DB를 오염시킨다.
- plan archive 이동을 squash 후 통합 branch에서 별도 commit으로 처리. 히스토리에 plan lifecycle이 둘로 나뉜다.
- followups를 별도 문서가 아닌 다른 plan 문서 본문 산문에 끼워넣음. 다음 사이클에서 entry로 식별이 안 되어 누락된다.
- squash 미반영 상태에서 cleanup 진행. worktree와 branch가 같이 사라지면 작업이 유실된다.
- 다른 worktree branch에 영향 주는 destructive 명령(`git clean`, `git reset --hard`, `git checkout .`, `git restore .`)을 사용자 확인 없이 실행. 사용 중인 작업 트리를 덮어쓸 수 있다.

## Gotchas

- worktree 컨벤션은 repo마다 다르다. 이 스킬은 단계 구조만 고정한다. 통합 branch 이름, 경로 패턴, 스크립트 이름, DB 명명 규칙, plan 디렉토리 위치, 라우팅 규칙은 대상 repo의 `AGENTS.md`와 `scripts/`에서 작업 시점에 확인한다.
- "이 작업이 worktree까지 필요할까"는 분량 직관보다 변경 종류로 결정된다. dependency·schema·cross-package가 끼면 분량이 작아 보여도 worktree가 안전하다.
- plan 문서를 root checkout에서 untracked로 incubate하는 컨벤션은 dirty가 아니다. 의도된 buffer이므로 setup에서 worktree로 강제 이동시키지 않는다. 단, init 스크립트가 함께 옮기는 옵션을 제공하면 그쪽이 권장 흐름이다.
- DB 컨테이너 자체는 보통 root checkout이 띄운 단일 인스턴스를 공유한다. logical DB만 worktree별로 분기. 이걸 헷갈리면 worktree마다 docker compose를 띄우려다 port 충돌이 난다.
- 사용자가 순서를 명시하면 그대로 따른다. 정리를 squash 전에 끼워넣어 사용자 흐름을 깨지 않는다. 단, followups/archive는 squash가 합쳐주려면 worktree branch commit 시점에 포함되어 있어야 한다는 점을 사전에 알린다.
- root checkout과 feature worktree가 같은 단일 컨테이너를 공유하는 환경에서는 `DATABASE_URL` 같은 env 값을 worktree별 local config에서 분기한다. 코드나 tracked config에 hardcode하지 않는다.
- cleanup에서 squash 확인을 commit message grep으로만 끝내면 동명 commit을 잘못 매칭할 수 있다. commit hash 기반 ancestor 검사를 쓴다.
