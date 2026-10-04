---
name: start-orchestration-session
description: 요구사항 하나를 Orca orchestration + git worktree로 분석·설계·계획·TDD 구현·리뷰까지 다수 에이전트에 나눠 수행하는 파이프라인 진입점. 사용자가 "/start-orchestration-session", "오케스트레이션 시작", "이 요구사항 파이프라인으로 돌려줘", "에이전트 나눠서 구현해줘"라고 할 때 사용. 코디네이터는 feature/xxxxx-master worktree에서 사람과 소통하고 나머지 단계는 워커에게 위임한다.
---

# start-orchestration-session — 요구사항 오케스트레이션 파이프라인

요구사항 하나를 받아 분석 → 설계 → 스펙 리뷰 → 계획 → 계획 리뷰 → TDD 구현(모듈 병렬)
→ 통합 → 코드 리뷰 → 최종 반환까지 자동으로 돈다.

설계 정본은 [`parfait/android/specs/2026-08-05-orchestration-session-pipeline.md`](../../../parfait/android/specs/2026-08-05-orchestration-session-pipeline.md).
이 문서와 스펙이 어긋나면 스펙이 정답이다.

## 이 스킬을 쓰지 않는 경우

- 단순 온보딩만 필요하다 → `start-default-session`
- 위키(`wiki/`·`raw/`) 작업 → `ingest`·`query`·`lint`
- 파일 한두 개 고치는 수준의 변경 → 파이프라인 비용이 이득보다 크다. 그냥 한다.

## 용어

| 표기 | 뜻 |
|---|---|
| 코디네이터 | `feature/xxxxx-master` worktree에서 도는 이 세션. 사람과 소통하는 유일한 지점 |
| W1 analyst | 요구분석 + 설계. `parfait/android/specs/`에 스펙 작성 |
| W2 spec-reviewer | 스펙 독립 검수 |
| W3 planner | 파일 선택 + 모듈 분할 + 테스트 명세. `parfait/android/plans/`에 계획 작성 |
| W4 plan-reviewer | 계획 독립 검수 |
| wt-domain / wt-data / wt-feature | Gradle 모듈별 구현 자식 worktree |
| wt-integrate | 병합·전체 테스트·코드 리뷰 자식 worktree |
| G1 / G2 / G3 | 사람 확인 지점 — 스펙 승인 / 계획 승인 / 최종 보고. 셋 다 코디네이터가 사용자에게 **대화로 직접 묻는다**(Orca gate 객체를 만들지 않는다) |
| 프로필 | 모델 배치 3종 — `균형`(기본) / `품질` / `비용` |

## 0. 전제 확인

아래를 먼저 실행하고, 하나라도 실패하면 파이프라인을 시작하지 않고 사용자에게 보고한다.

```bash
orca status --json
orca repo list --json
orca worktree list --json
```

확인 항목:

| 항목 | 판정 |
|---|---|
| 런타임 | `result.runtime.state == "ready"` |
| orchestration | `result.runtime.capabilities`에 `orchestration.contract.v1` 포함 |
| TEAMYG-Android 등록 | `repo list`에 `TEAMYG-Android` 존재 |
| master worktree | `worktree list`에 `feature/…-master` 브랜치의 TEAMYG-Android worktree 존재 |
| 시작 정책 | TEAMYG-Android `hookSettings.setupAgentStartupPolicy` 값을 기록해 둔다 |

로컬 절대경로는 `wiki/personal-private/project-paths.md`에서 읽는다.
이 문서에 직접 적지 않는다(public repo).

`feature/…-master` worktree가 없으면 만들고 시작한다.

```bash
orca worktree create --name <xxxxx>-master --repo name:TEAMYG-Android --base-branch develop --json
```

**`--name`과 브랜치 이름의 관계** — `--name`에 준 `<xxxxx>-master`는 Orca worktree의 표시
이름이고, Orca가 그 worktree에 만드는 git 브랜치는 `feature/<xxxxx>-master`다. 이 문서에서
`<xxxxx>-master`(worktree 이름)와 `feature/xxxxx-master`(브랜치 이름)는 **같은 대상의 두 이름**이다.
worktree selector에는 `name:<xxxxx>-master`를, `git diff`·`--base-branch`에는
`feature/<xxxxx>-master`를 쓴다.

**이름은 추측하지 말고 응답에서 읽는다.** `worktree create --json` 응답(또는
`orca worktree list --json`)에서 브랜치 이름을 읽어 기록해 둔다. 이후 만드는 모든 자식
worktree(§4·§5)도 마찬가지다 — 브랜치 이름은 integrator의 merge 대상과 `git diff` 기준이
되므로 코디네이터가 표로 들고 있어야 한다.

| 기록할 것 | 어디서 | 어디에 쓰는가 |
|---|---|---|
| worktree 이름 | `--name`에 준 값 | `--worktree name:<...>` selector |
| 브랜치 이름 | `worktree create --json` 응답 / `worktree list --json` | integrator의 merge 목록, `git diff <base>...HEAD` |
| 터미널 handle | `terminal create --json` 응답 | 워커 기동, **`worker_done` 이후 재-디스패치(§3 반려 루프)** |
| task id / dispatch id | `task-create --json` / `worker-start --json` | 계보 추적, 살아 있는 워커에게 보내는 mail |

**터미널 handle은 `worker_done`을 받은 뒤에도 버리지 않는다.** 반려·재작업은 그 handle로
같은 터미널을 다시 깨우는 방식이라(§3), handle을 잃으면 워커의 컨텍스트를 잃는다.

시작 정책이 `wait-for-setup`이면 모델 지정 2단계 경로(§4)를 쓸 수 없다.
그때는 모든 워커를 `--agent claude`(기본 모델)로 띄우고, 그 사실을 사용자에게 알린다.
`start-immediately`(2026-08-05 기준 현재 값)면 그대로 진행한다.

### cross-repo 쓰기 권한 확인

문서 워커(W1~W4)는 TEAMYG-Android worktree에서 돌면서 산출물은 team-yg repo의 `parfait/`
아래에 쓴다. cwd 밖 절대경로 쓰기가 권한 프롬프트에 걸리면 워커는 사람이 없는 자리에서
멈춰 버린다. 파이프라인을 시작하기 전에 한 번 확인한다.

```bash
# 두 경로는 wiki/personal-private/project-paths.md에서 읽어 채운다(public repo라 직접 적지 않는다)
TJYG="<TEAMYG-Android 절대경로 — wiki/personal-private/project-paths.md 참조. 코디네이터가 §0에서 이 문서를 읽어 실제 경로로 채워 넣은 뒤 워커에게 전달한다>"
TEAMYG="<team-yg-pesonal-agent 절대경로 — 같은 문서 참조>"

cd "$TJYG" && printf 'probe\n' > "$TEAMYG/.orch-write-probe" \
  && test -f "$TEAMYG/.orch-write-probe" && echo "OK: cross-repo write allowed"
rm -f "$TEAMYG/.orch-write-probe"
```

`OK`가 나오면 §3의 배치를 그대로 쓴다. 막히면 **문서 워커만 team-yg worktree에서 띄운다** —
§3 표의 "실행 위치"를 team-yg repo의 worktree selector로 바꾸고, 그 경우 워커가
TEAMYG-Android 코드를 읽을 때는 절대경로로 읽는다는 문장을 task spec에 함께 넣는다.
구현 워커(§4)는 TEAMYG-Android 안에서만 쓰므로 영향이 없다.

## 1. 요구사항 수집

사용자에게 요구사항을 받고, 아래 세 가지를 확정한다. 답이 없으면 기본값을 쓰고 그 사실을 알린다.

| 항목 | 기본값 | 의미 |
|---|---|---|
| 프로필 | `균형` | 모델 배치. 아래 표 |
| 진행 방식 | 게이트 유지 | `자동진행`이면 G1·G2를 건너뛰고 G3만 받는다 |
| master 브랜치 | 현재 worktree의 브랜치 | 결과를 돌려줄 대상 |

### 프로필

| 워커 | 균형(기본) | 품질 | 비용 |
|---|---|---|---|
| W1 analyst | Opus 5 | Opus 5 | Opus 5 |
| W2 spec-reviewer | Opus 5 | Opus 5 | Opus 5 |
| W3 planner | Opus 5 | Opus 5 | Sonnet 5 |
| W4 plan-reviewer | Opus 5 | Opus 5 | Sonnet 5 |
| 모듈 구현 워커 | 계획서의 `model:` | Opus 5 | Sonnet 5 |
| integrator | Sonnet 5 | Opus 5 | Sonnet 5 |
| code-reviewer | Opus 5 | Opus 5 | Opus 5 |

모델 표기는 스펙과 맞춰 `Opus 5` / `Sonnet 5`로 통일한다. CLI에 넘길 때는
`--model opus` / `--model sonnet`이다.

`품질`은 아키텍처를 건드리는 큰 변경, `비용`은 화면 하나 추가 수준의 정형 작업에 쓴다.
어느 프로필이든 **리뷰어는 작성자와 같은 티어 이상**이라는 규칙이 깨지지 않는다.

**재시도 티어 예외** — 실패 재시도는 "한 티어 올린 모델"이 원칙이지만, `품질` 프로필은
전부 Opus 5라 올릴 티어가 없다. 이미 최상위 티어면 모델을 바꾸는 대신
**프롬프트를 좁혀서** 재시도한다 — 실패한 지점만 남기고 범위를 줄이거나, 실패 로그를
task spec에 그대로 넣어 재시도한다. 같은 프롬프트 그대로의 재시도는 하지 않는다.

모델 배치의 근거 세 가지(스펙 §모델 분배):

1. 실패 비용은 상류일수록 크다 — 스펙이 틀리면 하류 전부가 폐기된다.
2. 판단 자유도가 낮으면 티어를 낮춘다 — RED/GREEN 게이트가 기계적으로 검증하는 자리는 안전하다.
3. 리뷰어는 작성자와 같은 티어 이상 — 아래 티어가 위 티어 산출물을 반려하기 어렵다.
   **기준 2와 충돌하면 기준 3이 이긴다.** 검증 장치가 다른 에이전트일 때 그 티어를 낮추면
   검증 자체가 약해진다. `비용` 프로필에서 W3·W4가 함께 Sonnet 5인 것은 규칙 위반이 아니다.

요구사항 원문은 **그대로 보존**한다. 요약해서 워커에 넘기지 않는다.
W1과 W2가 같은 원문을 보고 각자 판단해야 리뷰가 의미를 갖는다.

## 2. Run 생성

```bash
orca orchestration run-create --objective "<요구사항 한 줄 요약>" --json
```

Run은 이 요구사항 하나에 대응하는 네임스페이스이자 코디네이터 우편함이다.
Run이 워커를 스케줄하지는 않는다 — 배치와 동시성은 코디네이터가 정한다.

Run을 만든 뒤 Orca 워크스페이스 카드에 시작을 남긴다.

```bash
orca worktree set --worktree current \
  --comment "오케스트레이션 시작: <요약> (프로필=<균형|품질|비용>)" \
  --workspace-status in-progress --json
```

이후 각 단계 전환마다 `--comment`를 갱신하고, 코드 리뷰 단계에서 `--workspace-status in-review`,
최종 보고에서 `completed`로 옮긴다. 이것은 **장식층**이다 —
진행의 정본은 `orca orchestration task-list --json`과 각 워커의 `worker_done`이다.

## 3. 문서 단계 (W1 → W2 → G1 → W3 → W4 → G2)

문서 단계는 TEAMYG-Android 코드를 건드리지 않는다. 산출물은 team-yg repo의 `parfait/` 아래에
절대경로로 쓴다. 그래서 worktree를 새로 파지 않고 터미널만 띄운다.

| 워커 | 실행 위치 | 모델(균형 프로필) | 산출물 |
|---|---|---|---|
| W1 analyst | `terminal create --worktree current` → 그 handle | Opus 5 | `parfait/android/specs/YYYY-MM-DD-<topic>.md` |
| W2 spec-reviewer | `terminal create --worktree current` → 그 handle | Opus 5 | findings(파일 없음) |
| W3 planner | `terminal create --worktree current` → 그 handle | Opus 5 | `parfait/android/plans/YYYY-MM-DD-<topic>.md` |
| W4 plan-reviewer | `terminal create --worktree current` → 그 handle | Opus 5 | findings(파일 없음) |

네 워커는 순차 실행한다. 병렬 이득이 없고, 뒤 워커가 앞 산출물을 입력으로 받는다.

### 문서 워커 기동 (공통)

`worker-start --agent claude`는 **모델을 지정하지 못한다**(§4 워커 기동). 프로필 표가 워커별
티어를 지정하므로 문서 워커도 모듈 워커와 **같은 2단계 경로**를 쓴다. worktree는 새로 파지
않고 현재 worktree에 터미널만 추가한다.

```bash
# 1) 모델을 지정해 에이전트 터미널 생성 (worktree는 현재 것 그대로)
orca terminal create --worktree current --command "claude --model <opus|sonnet>" --json

# 2) 그 터미널에 task를 붙인다
orca orchestration worker-start --task <task_id> --terminal <handle> --json
```

⚠️ `terminal create --json`의 handle 필드 경로도 **확인되지 않았다**. 첫 실행에서 `--json`
출력 전체를 눈으로 보고 handle 필드 경로를 특정한다. Orca 가이드는 `worktree create --agent`
응답에 대해 `agentTerminalHandle`(구버전은 `startupTerminal.handle`)을 읽으라고 안내하는데,
**`terminal create`에 같은 경로가 쓰이는지는 미검증**이다. 첫 출발점으로만 쓰고, 확인되면
그 경로로 고정한다. 못 찾으면 `orca terminal list --worktree current --json`으로 재해석한다.

§0 정책이 `wait-for-setup`이면 이 2단계 경로를 쓸 수 없다. 그때만
`orca orchestration worker-start --task <task_id> --worktree current --agent claude --json`
한 줄로 가고, 프로필 표의 모델 지정이 적용되지 않는다는 사실을 사용자에게 알린다.

### 반려·재작업은 mail이 아니라 재-디스패치다 (필수)

워커는 `worker_done`을 보낸 뒤 **턴을 끝내고 프롬프트에서 대기하며 더 이상 `check`를 돌리지
않는다.** 그리고 그 `worker_done`이 task와 dispatch를 자동으로 `completed`로 만든다.
따라서 완료된 워커에게 `send --to dispatch:<id>`로 보낸 반려 지시는 **아무도 읽지 않는다.**
코디네이터는 오지 않을 `worker_done`을 기다리며 영원히 대기한다.

반려 라운드마다 **새 task를 만들어 같은 터미널을 다시 깨운다.** 터미널이 같으므로 워커의
컨텍스트(자기가 뭘 썼는지)는 그대로 살아 있다.

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 직전 산출물 재작업. 아래 findings를 반영한다.

[원 산출물] <스펙 또는 계획 절대경로>
[findings]
<리뷰어 body 원문 그대로>

[해라]
findings 각 건에 대해 고치거나, 고치지 않는다면 그 근거를 반박으로 적는다.
파일을 다시 쓴 뒤 worker_done을 보낸다.

[보고]
worker_done --outcome succeeded --files-modified "<수정 파일>"
body에 findings 건별 처리 결과(수정 / 반박 + 근거).
SPEC
)" --json

orca terminal wait --terminal <원 워커의 terminal handle> --for tui-idle --timeout-ms 60000 --json
orca orchestration dispatch --task <new_task_id> --to <원 워커의 terminal handle> --inject --json
```

`dispatch --inject` 앞에 `terminal wait --for tui-idle`을 먼저 둔다 — 터미널이 idle 상태가
되기 전에 주입하면 프롬프트가 유실될 수 있다.

`--inject`는 새 프리앰블 + TASK 블록을 터미널 입력으로 넣는다. 가이드가 말하는
"코디네이터가 idle 워커를 다시 깨우는" 바로 그 경로다.

- **완료된 task를 `task-update`로 되살리지 않는다.** 라운드마다 새 task를 만들면 반려
  이력이 task 목록에 그대로 감사 흔적으로 남는다.
- `send --to dispatch:<id>`는 **아직 돌고 있는(worker_done 전) 워커에게 주는 중간 안내**
  에만 쓴다. 그 mail은 워커의 *다음* `orchestration check`에서 읽힌다.
  완료된 워커에게는 쓰지 않는다 — 이 구분을 지우면 파이프라인이 교착한다.
- 재-디스패치 후에는 평소대로 `check --wait --types worker_done,escalation,question`으로 기다린다.

### W1 analyst

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 요구사항 분석 + 설계. 산출물은 설계 스펙 문서 하나다.

[읽어라]
- 코드 대상: <TEAMYG-Android 절대경로 — wiki/personal-private/project-paths.md 참조. 코디네이터가
  §0에서 이 문서를 읽어 실제 경로로 채워 넣은 뒤 워커에게 전달한다>
- 규약: <team-yg>/CLAUDE.md, <team-yg>/parfait/index.md, <team-yg>/parfait/android/specs/README.md
- 형식: <team-yg>/parfait/android/specs/template.md
- 기존 결정: <team-yg>/parfait/android/adr/, <team-yg>/parfait/android/architecture/
- 정책 SoT: <team-yg>/wiki/index.md에서 관련 페이지만

[해라]
1. superpowers:brainstorming 스킬을 로드한다.
2. 주제와 관련된 벤더 스킬을 먼저 찾는다:
   python3 <team-yg>/parfait/script/search.py "<주제>"
   상위 후보 중 관련 스킬을 네이티브 Skill로 로드한 뒤 설계를 확정한다.
3. 설계 스펙을 <team-yg>/parfait/android/specs/YYYY-MM-DD-<kebab-topic>.md에 쓴다.
   형식은 template.md, frontmatter 필수. 라인번호·hex·변동수치는 적지 않는다.
4. parfait/android/specs/README.md 인덱스에 한 줄 등록한다.

[금지]
- TEAMYG-Android 코드 수정. 이 단계는 읽기만 한다.
- placeholder("TBD", "추후 결정", 빈 섹션). 결정할 수 없으면 열린 질문 절에 근거와 함께 적는다.
- wiki/ 파일 수정.

[요구사항 원문]
<사용자 원문 그대로>

[보고]
worker_done --outcome succeeded --files-modified "<스펙 경로>,<README 경로>"
body에 스펙 절대경로와 핵심 설계 결정 3~5줄 요약.
SPEC
)" --json
```

기동(위 "문서 워커 기동 (공통)"의 2단계 경로):

```bash
orca terminal create --worktree current --command "claude --model opus" --json
orca orchestration worker-start --task <task_id> --terminal <handle> --json
```

W1의 handle을 기록해 둔다. 반려 루프에서 이 터미널을 다시 깨운다.

### W2 spec-reviewer

리뷰어에게는 **요구사항 원문과 스펙 파일만** 준다. W1의 대화 컨텍스트는 주지 않는다.
그래야 "문서만 읽고 이해되는가"가 실제로 검증된다.

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 설계 스펙 독립 검수. 너는 이 스펙을 쓰지 않았고, 작성 과정도 모른다.

[입력]
- 요구사항 원문: 아래
- 검수 대상: <스펙 절대경로>
- 대조 대상: <team-yg>/parfait/android/adr/, <team-yg>/parfait/android/architecture/, <team-yg>/wiki/

[반려 사유 — 하나라도 해당하면 반려]
1. 요구사항 원문의 항목 중 스펙에 담기지 않은 것
2. placeholder·TBD·"추후 결정"
3. 내부 모순 (아키텍처 서술 vs 기능 서술)
4. 두 가지로 읽히는 요구사항
5. parfait/android/adr/ 또는 parfait/android/architecture/의 기존 결정과 상충

[에스컬레이션 — 반려하지 말고 escalation]
- wiki/ 정책과 스펙이 상충. 기획 자체의 미결일 수 있어 에이전트가 판정하지 않는다.

[금지]
- 파일 수정. 너는 findings만 반환한다.
- 스타일 지적(문장 다듬기, 표 정렬). 위 5개 사유에만 집중한다.

[요구사항 원문]
<사용자 원문 그대로>

[보고]
통과: worker_done --outcome succeeded, body 첫 줄에 "PASS"
반려: worker_done --outcome succeeded, body 첫 줄에 "REJECT", 이어서 사유별로
      "사유번호 / 스펙의 어느 절 / 무엇이 빠졌거나 어긋나는지"를 한 건씩.
SPEC
)" --json
```

기동은 W1과 같다 — `terminal create --worktree current --command "claude --model opus"` →
`worker-start --terminal <handle>`.
W2의 handle을 기록해 둔다. W1이 재작업을 마치면 재검수를 위해 이 터미널을 다시 깨운다.

**반려 루프**: `REJECT`를 받으면 findings를 **W1의 터미널에 새 task로 재-디스패치**한다.
W2의 `worker_done`으로 W1의 task는 이미 완료 상태이므로 mail로는 W1이 깨어나지 않는다
(위 "반려·재작업은 mail이 아니라 재-디스패치다" 참조).

```bash
# 재작업 task spec 템플릿은 위 "반려·재작업은 mail이 아니라 재-디스패치다" 절의 히어독을 쓴다
orca orchestration task-create --spec "<재작업 spec: findings + 무엇을 고칠지 + 원 산출물 경로>" --json
orca terminal wait --terminal <W1_terminal_handle> --for tui-idle --timeout-ms 60000 --json
orca orchestration dispatch --task <rework_task_id> --to <W1_terminal_handle> --inject --json
```

여기서도 `dispatch --inject` 전에 idle을 확인한다 — 프롬프트 유실 방지.

W1이 수정해 `worker_done`을 다시 보내면 W2도 같은 방식으로(새 task → `terminal wait --for tui-idle` →
`dispatch --inject`) W2 터미널을 다시 깨워 재검수시킨다.
**상한 2회.** 3회째 반려면 escalation으로 사람을 부른다 —
리뷰어와 작성자가 합의하지 못하는 상태이고 자동으로 풀리지 않는다.

### G1 — 스펙 승인

**코디네이터가 사용자에게 직접 묻는다.** Orca gate 객체를 만들지 않는다 — 코디네이터가
바로 사람과 대화 중인 세션이므로 중간에 게이트 객체를 둘 이유가 없고, `gate-create`는
코디네이터가 관리하는 task DAG 결정용이다.

`자동진행` 모드면 건너뛴다. 아니면 사용자에게 다음을 제시하고 답을 기다린다.

- 산출물 경로: `<스펙 절대경로>`
- W2 검수 결과 요약(PASS / 반려 이력)
- 선택지: **진행 / 수정 요청 / 중단**

받은 답에 따라:

- `진행` → W3
- `수정 요청` → 사용자 지적을 findings로 삼아 W1 터미널에 재-디스패치하고, 다시 W2 검수부터
- `중단` → Run을 남긴 채 종료하고, 재개 방법(§8)을 사용자에게 알린다

사용자가 바로 답하지 않아도 실패가 아니다. 워커를 죽이지 않고, 답이 올 때까지 이 지점에 머문다.

### W3 planner

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 구현 계획 작성. 파일 선택 + 모듈 분할 + 테스트 명세 + 모델 지정.

[읽어라]
- 확정 스펙: <스펙 절대경로>
- 코드 대상: <TEAMYG-Android 절대경로 — wiki/personal-private/project-paths.md 참조. 코디네이터가
  §0에서 이 문서를 읽어 실제 경로로 채워 넣은 뒤 워커에게 전달한다>
- 형식: <team-yg>/parfait/android/plans/template.md, 규약: parfait/android/plans/README.md

[해라]
1. superpowers:writing-plans 스킬을 로드한다.
2. 주제 관련 벤더 스킬을 먼저 찾는다:
   python3 <team-yg>/parfait/script/search.py "<주제>"
3. 변경이 필요한 파일을 전부 나열하고 **Gradle 모듈 경계로 묶는다.**
   모듈 간 파일 집합이 겹치면 안 된다. 겹치면 분할을 다시 한다.
4. 모듈별로 아래를 확정한다:
   - 담당 파일 화이트리스트(절대경로)
   - 테스트 명세: 무엇을 검증하고 기대값이 무엇인지. 실행 가능한 형태로.
   - Gradle 테스트 태스크(예: :domain:test)
   - model: opus | sonnet — 근거 한 줄과 함께
     · opus — Compose UI·recomposition, 코루틴 동시성, 기존 코드 대수술, 파일 6개 이상
     · sonnet — 시그니처까지 특정된 신규 파일, DTO·매퍼·Repository 같은 정형 작업
   - 의존 관계(기본형: domain → data, domain → feature)
5. 계획을 <team-yg>/parfait/android/plans/YYYY-MM-DD-<kebab-topic>.md에 쓰고
   parfait/android/plans/README.md 인덱스에 한 줄 등록한다.

[판단]
- 파일이 한 모듈 안에서 많이 겹쳐 병렬 이득이 없으면 **단일 워커로 결정**해도 된다.
  그 판단과 근거를 계획서에 적는다.

[금지]
- TEAMYG-Android 코드 수정.
- placeholder. "적절히 처리", "테스트 추가" 같은 서술.

[보고]
worker_done --outcome succeeded --files-modified "<계획 경로>,<README 경로>"
body에 모듈 분할 결과(모듈 / 파일 수 / model / 의존)를 표로.
SPEC
)" --json
```

기동은 W1과 같은 2단계 경로를 쓰되, 모델은 선택한 프로필의 W3 값을 넣는다(`비용` 프로필은
Sonnet 5) — `terminal create --worktree current --command "claude --model <opus|sonnet>"` →
`worker-start --terminal <handle>`.
W3의 handle을 기록해 둔다. W4 반려 시 이 터미널을 다시 깨운다.

### W4 plan-reviewer

W2와 같은 구조다. 리뷰어에게는 **스펙 파일과 계획 파일만** 준다. W3의 대화 컨텍스트는 주지 않는다.

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 구현 계획 독립 검수. 너는 이 계획을 쓰지 않았고, 작성 과정도 모른다.

[입력]
- 확정 스펙: <스펙 절대경로>
- 검수 대상: <계획 절대경로>
- 대조 대상: TEAMYG-Android의 실제 Gradle 모듈 구조(settings.gradle.kts, 각 모듈 build.gradle.kts)

[반려 사유 — 하나라도 해당하면 반려]
1. 스펙 항목 중 계획에 잡히지 않은 것
2. 모듈 간 파일 집합 겹침 — merge 충돌 예고이므로 반려
3. 테스트 명세가 실행 가능한 형태가 아님(검증 대상·기대값 미특정)
4. 의존 순서가 실제 Gradle 모듈 의존과 어긋남
5. task 하나의 크기가 과도함
6. model: 필드 누락 또는 근거 없음

[에스컬레이션 — 반려하지 말고 escalation]
- 계획이 스펙 자체의 결함을 드러낸 경우(스펙이 정한 것으로는 구현 분할이 성립하지 않는다).
  계획을 고쳐서 될 문제가 아니므로 에이전트가 판정하지 않는다.

[금지]
- 파일 수정. 너는 findings만 반환한다.
- 스타일 지적(문장 다듬기, 표 정렬). 위 6개 사유에만 집중한다.
- TEAMYG-Android 코드 수정. 이 단계는 읽기만 한다.

[보고]
통과: worker_done --outcome succeeded, body 첫 줄에 "PASS"
반려: worker_done --outcome succeeded, body 첫 줄에 "REJECT", 이어서 사유별로
      "사유번호 / 계획의 어느 task·절 / 무엇이 빠졌거나 어긋나는지"를 한 건씩.
SPEC
)" --json
```

기동은 W2와 같은 2단계 경로를 쓰되, 모델은 선택한 프로필의 W4 값을 넣는다(`비용` 프로필은
Sonnet 5) — `terminal create --worktree current --command "claude --model <opus|sonnet>"` →
`worker-start --terminal <handle>`.
W4의 handle을 기록해 둔다. W3이 재작업을 마치면 재검수를 위해 이 터미널을 다시 깨운다.

균형 프로필에서 모델은 Opus 5다. 검사 항목이 명시적 체크리스트라 낮출 만해 보이지만,
작성자 W3가 Opus 5라 "리뷰어는 작성자와 같은 티어 이상" 규칙이 이긴다.
반려 루프(새 task → `terminal wait --for tui-idle` → `dispatch --inject`로 W3 터미널 재-디스패치)와 상한 2회는 W2와 동일하다.

### G2 — 계획 승인

G1과 같은 방식 — **코디네이터가 사용자에게 직접 묻는다.** gate 객체를 만들지 않는다.
제시할 것: 계획 절대경로, 모듈 분할 결과(모듈 / 파일 수 / model / 의존), W4 검수 결과,
선택지 **진행 / 수정 요청 / 중단**. `자동진행`이면 건너뛴다.

## 4. 구현 단계

계획서가 나눈 모듈마다 자식 worktree를 하나씩 만들고 워커를 붙인다.

의존 관계는 `task-create --deps`로 표현한다. 기본형은 domain → (data, feature)다.
인터페이스가 domain에 있으므로 domain이 끝나야 나머지 둘이 병렬로 시작한다.
계획서가 domain 변경 없음이라고 판단했으면 세 모듈이 모두 동시에 출발한다.

⚠️ **`task-create --json`의 응답 스키마는 Orca 가이드에 문서화돼 있지 않다.** id 필드 경로를
가정한 채 `jq`로 자동화하면, 경로가 틀렸을 때 변수가 빈 문자열이 되고 `--deps '[""]'`가
들어가 **의존이 조용히 깨진다**(에러 없이 순서만 무너진다).

**먼저 눈으로 확인한다.** domain task는 **한 번만** 만든다 — 응답 전체를 파일에 캡처해 두고
그 값을 눈으로 본 뒤, 같은 파일에서 id를 뽑는다. `task-create`를 두 번 실행하면 domain
task가 두 개 생겨 하나가 `pending`으로 남고, 그 orphan이 §8이 복구 근거로 쓰는
`task-list --json`을 오염시킨다.

```bash
orca orchestration task-create --spec "<domain task spec>" --json | tee <scratchpad>/domain-task.json
orca orchestration task-list --brief --json                          # id 필드 위치 확인
```

응답을 변수가 아니라 **파일**(`<scratchpad>/domain-task.json`, §6의 `final.patch`와 같은
placeholder 관례)에 남기는 이유는 두 블록 사이에 그 파일을 직접 열어 눈으로 확인할 수 있고,
아래 블록을 몇 번이든 다시 돌려도 domain task가 다시 생기지 않기 때문이다.

**그다음에야 자동화한다.** 아래 `jq` 경로는 위 확인으로 실제 경로를 특정한 뒤 그 값으로
바꿔 쓴다. `domain-task.json`은 이미 캡처했으므로 `task-create`를 다시 실행하지 않는다.
id 추출이 실패해도 **셸을 닫는 `exit`는 쓰지 않는다** — 대화형으로 붙여넣었을 때 사용자의
셸까지 끊기고, 실패 분기는 그냥 아래 두 `task-create`를 실행하지 않는 것으로 충분하다.

```bash
DOMAIN_TASK=$(jq -r '<확인한 id 경로>' <scratchpad>/domain-task.json)
if [ -z "$DOMAIN_TASK" ]; then
  echo "id 추출 실패 — jq 경로를 고쳐 이 블록만 다시 실행한다."
  echo "domain task는 이미 만들어져 있으므로 task-create를 다시 실행하지 않는다."
else
  orca orchestration task-create --spec "<data task spec>"    --deps "[\"$DOMAIN_TASK\"]" --json
  orca orchestration task-create --spec "<feature task spec>" --deps "[\"$DOMAIN_TASK\"]" --json
fi
```

### 워커 기동

`worker-start --agent claude`는 **모델을 지정하지 못한다.** 계획서가 정한 모델을 쓰려면
worktree와 터미널을 먼저 만들고 그 터미널에 task를 붙인다.

```bash
# 1) 자식 worktree 생성
orca worktree create --name wt-<module> --repo name:TEAMYG-Android \
  --base-branch <feature/xxxxx-master> --json

# 2) 모델을 지정해 에이전트 터미널 생성
orca terminal create --worktree name:wt-<module> \
  --command "claude --model <opus|sonnet>" --json

# 3) 그 터미널에 task를 붙인다 (orchestration 계보 유지)
orca orchestration worker-start --task <task_id> --terminal <handle> --json
```

⚠️ `terminal create --json`의 handle 필드 경로는 **미검증**이다. 첫 실행에서 `--json` 출력
전체를 확인해 handle 필드 경로를 특정한다. 가이드가 `worktree create --agent` 응답에 대해
안내하는 `agentTerminalHandle`(구버전 `startupTerminal.handle`)을 첫 추측으로 삼되,
`terminal create`에도 같은 경로가 쓰이는지는 확인 전까지 가정하지 않는다.
못 찾으면 `orca terminal list --worktree name:wt-<module> --json`으로 재해석한다.

1)의 응답(또는 `orca worktree list --json`)에서 **브랜치 이름**을, 2)의 응답에서
**터미널 handle**을 읽어 §0의 기록 표에 적어 둔다. 브랜치 이름은 §5 integrator의 merge
대상이 되고, handle은 반려 시 이 워커를 다시 깨우는 유일한 주소다.
`worker_done`을 받은 뒤에도 handle을 버리지 않는다.

`--terminal`로 붙여도 task·dispatch 계보, `worker_done` 권한, 주입 프리앰블은 그대로다.

이 경로는 repo의 `wait-for-setup` 정책을 강제하지 못한다. §0에서 기록해 둔 값이
`start-immediately`면 잃는 것이 없다. `wait-for-setup`이면 모델 지정을 포기하고
아래 한 줄로 간다.

```bash
orca orchestration worker-start --task <task_id> --worktree new-child --name wt-<module> \
  --repo name:TEAMYG-Android --base-branch <feature/xxxxx-master> --agent claude --setup run --json
```

`--repo`와 `--base-branch`를 빼면 안 된다. 빼면 자식 worktree가 repo 기본 base(`develop`)에서
갈라져 나오고, §6의 `git diff <feature/xxxxx-master>...HEAD`가 엉뚱한 패치를 만든다.
(`worker-start --help`가 `new-child`에 대해 `--repo`·`--base-branch`를 받는다.
`current`·기존 worktree에는 이 생성 플래그들이 거부되므로 붙이지 않는다.)

세 모듈이 동시에 돌면 Gradle 데몬이 최대 3개, `build/`가 3벌이 된다. `~/.gradle`은 공유라
동시 쓰기 잠금 경합이 생길 수 있다. 락 대기나 비정상적인 지연이 보이면 그때 모듈 워커를
줄인다. 미리 튜닝하지 않는다.

### 구현 워커 task spec

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] <module> 모듈 TDD 구현.

[입력]
- 계획 문서: <계획 절대경로>
- 담당 모듈: <module>
- 담당 파일 화이트리스트:
    <파일 절대경로 목록>
- 테스트 명세:
    <검증 대상과 기대값>
- 테스트 태스크: ./gradlew :<module>:test

[순서 — 이 순서를 지켜야 한다]
1. 테스트를 먼저 쓴다.
2. ./gradlew :<module>:test 를 실행한다. RED여야 한다. 실패 출력을 그대로 보관한다.
   여기서 GREEN이면 테스트가 잘못된 것이다. 다시 쓴다.
3. 구현한다.
4. ./gradlew :<module>:test 를 다시 실행한다. GREEN이어야 한다. 출력을 그대로 보관한다.
5. 커밋한다. repo 관례를 따라 test: 와 feat: 를 나눈다.

[금지]
- 담당 파일 화이트리스트 밖 수정. 필요하면 escalation을 보낸다.
- 구현을 먼저 하고 테스트를 나중에 붙이는 것.
- RED 확인 없이 3단계로 건너뛰는 것.

[보고]
worker_done --outcome succeeded --files-modified "<수정 파일 목록>"
body에 다음 둘을 **모두** 넣는다:
  - RED 로그: 2단계 실행 출력 중 실패를 보여주는 부분
  - GREEN 로그: 4단계 실행 출력 중 통과를 보여주는 부분
실패했으면 --outcome failed 를 쓴다. 산문으로만 실패를 적지 않는다.
SPEC
)" --json
```

### 증거 검사

`worker_done`을 받으면 코디네이터가 body를 확인한다.

| 확인 | 통과 조건 | 위반 시 |
|---|---|---|
| RED 로그 | 2단계 실행 결과에 실패가 보인다 | 반려(재-디스패치) |
| GREEN 로그 | 4단계 실행 결과에 통과가 보인다 | 반려(재-디스패치) |
| 파일 범위 | `--files-modified`가 화이트리스트를 벗어나지 않는다 | **escalation** — 반려하지 않는다 |

**화이트리스트를 벗어난 변경은 반려가 아니라 escalation이다.** 워커가 계획서에 없던 파일을
건드렸다는 것은 계획의 모듈 분할이 틀렸다는 신호이고, 워커에게 되돌리라고 시키면 그 신호가
사라진 채 같은 문제가 통합 단계에서 merge 충돌로 다시 나온다. 사람을 부르고, 필요하면 계획
단계로 되돌아간다.

RED·GREEN 로그가 하나라도 없으면 **반려**한다. 반려는 mail이 아니라 **새 task +
`dispatch --inject`로 그 워커의 터미널을 다시 깨우는 것**이다(§3 "반려·재작업은 mail이 아니라
재-디스패치다"). 워커는 `worker_done` 이후 idle 상태이고 task·dispatch는 이미 완료라
`send --to dispatch:<id>`는 읽히지 않는다.

```bash
orca orchestration task-create --spec "증거 누락 재작업. RED 로그와 GREEN 로그를 모두 첨부해 다시 보고하라. 이미 작성한 테스트·구현은 그대로 두고, ./gradlew :<module>:test 실행 출력을 붙여 worker_done을 다시 보낸다. 로그가 없으면 이 task는 완료로 인정하지 않는다." --json
orca terminal wait --terminal <해당 워커의 terminal handle> --for tui-idle --timeout-ms 60000 --json
orca orchestration dispatch --task <rework_task_id> --to <해당 워커의 terminal handle> --inject --json
```

여기서도 `dispatch --inject` 전에 idle을 확인한다 — 프롬프트 유실 방지.

이 검사를 강제하는 이유는, 로그 두 개가 TDD를 지켰다는 **유일하게 검증 가능한 흔적**이기
때문이다. 없으면 구현을 먼저 하고 통과하는 테스트를 나중에 붙인 것과 구분할 수 없다.

GREEN에 도달하지 못했으면 같은 방식으로 1회 재시도시킨다. 재시도는 **한 티어 올린 모델**로
한다 — 같은 모델에 같은 프롬프트를 다시 넣으면 같은 결과가 나온다. 모델을 바꾸려면
`terminal create --worktree name:wt-<module> --command "claude --model opus"`로 그 모듈의
worktree 안에 터미널을 새로 만들고 그 handle에
`worker-start --task <retry_task_id> --terminal <new_handle> --retry-of <원 dispatch_id>`로 붙인다.
**`--worktree`를 빼면 기본값인 코디네이터의 현재 worktree(`feature/xxxxx-master`)에서 도는
터미널이 되어 master 트리를 직접 건드리게 된다** — §6의 "master는 커밋하지 않는다"를 깨고,
모듈 브랜치에는 재시도의 수정이 반영되지 않아 §5 병합 대상에서 빠진다.
이미 최상위 티어(Opus 5)면 §1의 예외대로 프롬프트를 좁혀 같은 터미널에 재-디스패치한다.
그래도 실패하면 escalation.

### 대기

```bash
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 540000 --json
orca orchestration check --ack <delivery_id> --wait --types worker_done,escalation,question --timeout-ms 540000 --json
```

orca `--wait` 타임아웃은 하네스 Bash 도구 타임아웃(최대 600000ms)보다 짧아야 한다.
길게 주면 orca가 아니라 하네스가 먼저 명령을 끊어 대기가 중간에 잘린다.

Delivery 안의 메시지를 **전부 처리한 뒤** ack한다.
타임아웃이나 `{count:0}`은 실패가 아니라 체크포인트다. 구현 task는 보통 오래 걸린다.
워커를 죽이거나 재시작하지 않는다. 하트비트와 터미널 활동은 살아 있다는 뜻이지 끝났다는
뜻이 아니다. 창이 비어서 돌아오면 같은 명령으로 다시 기다린다(rolling wait).

## 5. 통합과 코드 리뷰

모듈 워커가 전부 `worker_done`을 보내고 증거 검사를 통과하면 통합 worktree를 만든다.

```bash
orca worktree create --name wt-integrate --repo name:TEAMYG-Android \
  --base-branch <feature/xxxxx-master> --json
orca terminal create --worktree name:wt-integrate --command "claude --model <opus|sonnet>" --json
orca orchestration worker-start --task <integrate_task_id> --terminal <handle> --json
```

모델은 선택한 프로필의 integrator 값을 넣는다(`품질` 프로필은 Opus 5).

integrator task spec의 `<wt-domain 브랜치>` 자리는 §0·§4에서 기록해 둔 **모듈 worktree의
브랜치 이름**으로 채운다. 기억에 의존하지 말고 `orca worktree list --json`으로 다시 확인한다.
integrator 터미널 handle도 기록한다 — 코드 리뷰 findings 재작업이 이 handle로 간다.

### integrator task spec

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 모듈 브랜치 병합 + 전체 테스트.

[해라]
1. 아래 브랜치를 순서대로 merge 한다: <wt-domain 브랜치>, <wt-data 브랜치>, <wt-feature 브랜치>
2. 충돌이 나면 **직접 해결하지 말고 escalation을 보낸다.**
   모듈 경계로 나눴는데 충돌했다는 것은 분할이 잘못됐다는 신호이고,
   여기서 임의로 봉합하면 그 신호가 사라진다.
3. ./gradlew test 로 전체 테스트를 돌린다. GREEN이어야 한다.
4. 커밋한다.

[보고]
worker_done --outcome succeeded --files-modified "<병합 결과 변경 파일>"
body에 전체 테스트 출력의 결과 부분과 병합한 브랜치 목록.
SPEC
)" --json
```

### code-reviewer

같은 worktree에 **별도 터미널**로 띄운다. 리뷰어는 파일을 고치지 않는다.

```bash
orca terminal create --worktree name:wt-integrate --command "claude --model opus" --json
orca orchestration worker-start --task <review_task_id> --terminal <handle> --json
```

code-reviewer의 handle을 기록해 둔다. integrator가 재작업을 마치면 재리뷰를 위해 이
터미널을 다시 깨운다.

```bash
orca orchestration task-create --spec "$(cat <<'SPEC'
[역할] 통합 diff 코드 리뷰. 너는 이 코드를 쓰지 않았다.

[입력]
- 스펙: <스펙 절대경로>
- 계획: <계획 절대경로>
- 대상: git diff <feature/xxxxx-master>...HEAD

[보는 것]
- 스펙 요구 중 구현되지 않은 것
- 모듈 간 인터페이스 불일치 (모듈별 리뷰로는 안 보이는 것 — 여기가 핵심)
- 테스트가 실제로 명세한 동작을 검증하는가 (통과만 하는 빈 테스트가 아닌가)
- 계획의 담당 파일 화이트리스트를 벗어난 변경
- repo 관례 이탈 (parfait/android/architecture/ 참조)

[금지]
- 파일 수정. findings만 반환한다.
- 스타일 지적. ktlint가 잡는 것은 적지 않는다.

[보고]
worker_done --outcome succeeded
body 첫 줄에 "PASS" 또는 "FINDINGS", FINDINGS면 건별로
"심각도(Critical|Important|Minor) / 파일#심볼 / 무엇이 문제인지 / 어떻게 고칠지".
SPEC
)" --json
```

`FINDINGS`를 받으면 integrator를 **재-디스패치**해 수정시킨다. integrator는 이미
`worker_done`을 보내고 idle 상태이므로 `send --to dispatch:<id>`로는 깨어나지 않는다
(§3 "반려·재작업은 mail이 아니라 재-디스패치다").

```bash
orca orchestration task-create --spec "코드 리뷰 findings 반영. <findings 원문>. 대상: wt-integrate의 현재 HEAD. 각 건을 고치거나, 고치지 않는다면 근거를 반박으로 적고 다시 ./gradlew test로 GREEN을 확인한 뒤 커밋하고 worker_done을 보낸다." --json
orca terminal wait --terminal <integrator_terminal_handle> --for tui-idle --timeout-ms 60000 --json
orca orchestration dispatch --task <rework_task_id> --to <integrator_terminal_handle> --inject --json
```

여기서도 `dispatch --inject` 전에 idle을 확인한다 — 프롬프트 유실 방지.

수정 후 code-reviewer도 같은 방식으로(새 task → `terminal wait --for tui-idle` →
`dispatch --inject`) 그 터미널을 다시 깨워 재리뷰시킨다. **상한 2회.** 3회째면 escalation.

## 6. 최종 산출

통합 worktree에서 diff를 뽑아 master 작업 트리에 적용한다. **커밋하지 않는다.**

```bash
# wt-integrate에서
git diff <feature/xxxxx-master>...HEAD > <scratchpad>/final.patch

# master worktree에서
git apply <scratchpad>/final.patch
git status --short
```

`git apply`가 실패하면 master 브랜치가 그 사이 앞으로 나갔다는 뜻이다.
덮어쓰지 말고 사용자에게 보고한다.

### G3 — 최종 보고

G1·G2와 같이 **코디네이터가 사용자에게 직접 보고하고 답을 기다린다.** gate 객체를 만들지
않는다. 차이는 하나뿐이다 — `자동진행` 모드에서도 **G3는 건너뛰지 않는다.** 보고 항목:

- 변경 파일 목록 (`git status --short` 출력)
- 전체 테스트 결과
- 코드 리뷰 findings와 처리 내역 (해소 / 이월 / 반박)
- 스펙·계획 문서 경로
- 자식 브랜치 이름들

`push`와 PR 생성은 사용자 승인 후에만 한다.

이 방식으로 만들어지는 PR 히스토리는 사람이 만든 커밋 하나다.
자식 worktree의 커밋들은 PR에 올라가지 않고 로컬 브랜치에만 남는다.

### 정리

**자식 worktree는 보고 후에도 유지한다.** 사용자가 중간 산출물과 커밋 히스토리를 볼 수
있어야 하고, 재수정 요청이 오면 거기서 이어간다.
사용자가 명시적으로 정리를 요청할 때만 archive한다.

### 커밋 정책

기본 규칙은 "TEAMYG-Android는 구현이 끝나도 커밋하지 않는다"이다.
이 파이프라인에 한해 **자식 worktree 브랜치의 커밋은 병합 수단으로 허용**한다.
master 브랜치는 커밋하지 않고, push와 PR은 사용자 승인을 받는다.

## 7. 에스컬레이션

| 상황 | 동작 |
|---|---|
| `worker-start` 실패 | receipt의 `stage`·`effects`·`residualResources`를 읽고 판단. `--retry-of <dispatch_id>`로 1회만 재시도. 자동 무한 재시도 금지 |
| RED 또는 GREEN 로그 누락 | 반려 — 새 task → `terminal wait --for tui-idle` → `dispatch --inject`로 그 워커의 터미널 재-디스패치 |
| 담당 파일 화이트리스트 초과 변경 | **사람 호출.** 반려하지 않는다 — 계획의 모듈 분할이 틀렸다는 신호이므로 워커에게 되돌리게 하면 신호가 사라진다 |
| GREEN 미달성 | 한 티어 올린 모델로 1회 재시도(이미 최상위면 프롬프트를 좁혀 재시도) → 실패 시 사람 호출 |
| 문서 리뷰 반려 3회째 | 사람 호출 |
| 코드 리뷰 findings 3회째 | 사람 호출 |
| merge 충돌 | 즉시 사람 호출. 분할이 잘못됐다는 신호이므로 계획 단계로 되돌아간다 |
| 같은 task 3연속 실패 | Orca가 circuit-break하여 task failed. 사람에게 보고하고 중단 |
| `wiki/` 정책과 스펙 상충 | 사람 호출. 기획 미결일 수 있어 에이전트가 판정하지 않는다 |
| `git apply` 실패 | 사람 호출. 덮어쓰지 않는다 |

## 8. 중단과 재개

한 번 도는 데 워커가 8개쯤 붙고, Orca 가이드도 코딩 task가 보통 15~60분 걸린다고 말한다.
**코디네이터 세션이 중간에 죽는 것은 예외가 아니라 정상 경로다.** Run·Task·Dispatch는
Orca에 남아 있으므로 새 세션에서 다시 붙으면 된다.

```bash
# 1) 이 터미널이 어떤 Run에 묶여 있는지 확인 (비어 있으면 바인딩이 끊긴 것)
orca orchestration run-current --json

# 2) Run 목록에서 objective로 해당 Run을 찾는다
orca orchestration run-list --limit 20 --json

# 3) 이 코디네이터 터미널을 그 Run에 다시 묶는다
orca orchestration run-use --id <run_id> --json

# 4) 어디까지 갔는지 복원한다
orca orchestration task-list --brief --json     # 각 task의 status: pending|ready|dispatched|completed|failed|blocked
orca orchestration dispatch-show --task <task_id> --json
orca orchestration worker-show --dispatch <dispatch_id> --json
orca terminal list --json                        # 살아 있는 워커 터미널 handle 회수
orca worktree list --json                        # 자식 worktree와 브랜치 이름 회수
```

복원 판정:

| task status | 뜻 | 다음 |
|---|---|---|
| `completed` | 그 단계는 끝났다 | 다음 단계로 |
| `dispatched` | 워커가 아직 돌고 있다 | 죽이지 말고 `check --wait`로 다시 기다린다 |
| `failed` | 3연속 실패로 circuit-break 됐거나 워커가 실패 보고 | 사람에게 보고 |
| `pending` / `ready` / `blocked` | 아직 안 붙었거나 의존 대기 | 해당 단계부터 다시 기동 |

§0의 기록 표(worktree 이름 / 브랜치 이름 / 터미널 handle / task·dispatch id)를
`terminal list`·`worktree list`·`task-list` 출력으로 다시 채운 뒤 이어간다. **재개할 때
자식 worktree를 새로 만들지 않는다** — 기존 브랜치의 커밋이 곧 지금까지의 산출물이다.

Run을 못 찾겠으면 `orca orchestration inbox --limit 50 --json`으로 최근 메시지에서
task·dispatch id를 역추적한다.

## 9. 진행 상황 확인

```bash
orca orchestration task-list --brief --json
orca orchestration dispatch-show --task <task_id> --json
orca orchestration worker-read --dispatch <dispatch_id> --limit 50 --json
```
