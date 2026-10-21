---
name: io-model
description: "Use when the user wants to see or change which model and effort IssueOps uses per role (implement, child-implement, plan-review, diff-review, review-escalate, research, reader-check) for Claude Code or Codex, globally or for one repository. Triggers include io model, issueops model, 역할별 모델 설정, 리뷰 모델 바꿔줘, 서브에이전트 모델, global·local 모델 설정."
---

# IO Model

IssueOps가 역할별로 띄우는 세션과 서브에이전트의 model·effort를 `issueops model`로
조회하고 바꾼다. 값의 원본은 설정 파일과 CLI이며, 이 스킬은 대화 요청을 정확한
명령으로 옮기고 결과를 다시 읽어 보여 준다. 모델 이름 표를 이 본문에 옮겨 적지 않는다.
현재 값은 항상 `issueops model show --json`으로 읽는다.

## 개념

| 항목 | 의미 |
|---|---|
| host | `claude`, `codex`, `omo`, `omp`, `opencode`. omo·omp·opencode 모델 ID는 `chatgpt-subscription/gpt-6.1-sol`, `anthropic/claude-sonnet-5-5`, `opencode/deepseek-v4.1-flash-free`처럼 `<provider>/<model>` 형식으로 적는다 |
| role | `implement`, `child-implement`, `plan-review`, `diff-review`, `review-escalate`, `research`, `reader-check` |
| scope | `global`(사용자 전체), `local`(이 저장소의 메인 워크트리 하나) |
| 우선순위 | 필드(model, effort)마다 명시 플래그 > local > global > 내장 기본값 |

- `local`은 메인 워크트리의 `.issueops/agent-models.local.json` 하나다. 연결 워크트리에서
  실행해도 같은 파일을 쓴다. 처음 만들 때 `.git/info/exclude`에 등록되어 커밋되지 않는다.
- `global`은 `$XDG_CONFIG_HOME/issueops/agent-models.json`, 변수가 없으면
  `~/.config/issueops/agent-models.json`이다.
- `child-implement`를 비워 두면 `implement`를 따른다. `review-escalate`를 비워 두면
  리뷰 3~5라운드에 원래 리뷰 모델을 effort 한 단계 올려 쓴다.
- docs-only 변경의 리뷰 effort 하향은 내장 기본값에만 적용된다. 사용자가 적은 effort는
  그대로 쓴다.
- opencode effort는 모델이 정의한 variant 이름(`none`·`minimal`·`low`·`medium`·`high`·`xhigh`·`max`)이다.
  docs-only 하향과 3라운드 상향을 적용하지 않고 적은 값을 그대로 쓴다.
- 이미 실행 중인 세션의 모델은 설정을 바꿔도 바뀌지 않는다. 새로 여는 세션부터 적용된다.

## 요청별 명령

| 요청 | 명령 |
|---|---|
| 지금 설정 보기 | `issueops model show --json` (특정 host만 `--host codex`) |
| 값 바꾸기 | `issueops model set --scope global\|local --host H --role R [--model M] [--effort E] --json` |
| 값 지우기 | `issueops model unset --scope global\|local --host H --role R [--field model\|effort] --json` |
| 특정 역할의 최종 값 | `issueops model resolve --host H --role R [--tier T] [--round N] --json` |

- scope를 말하지 않았으면 대화 맥락으로 정한다. "이 프로젝트에서만", "이 레포"는 `local`,
  "기본으로", "항상", "전역"은 `global`이다. 둘 다 근거가 없을 때만 한 번 묻는다.
- model과 effort 중 말한 것만 넘긴다. 말하지 않은 필드는 아래 층에서 이어받는다.
- 모델 별칭과 전체 ID는 사용자가 말한 그대로 넘긴다. 이름을 추측해 바꾸지 않는다.

## 절차

1. `issueops model show --json`으로 현재 값과 `local_path`, `global_path`를 읽는다.
2. 요청을 위 표의 명령 하나로 옮겨 실행한다. 여러 역할이면 역할마다 한 번씩 실행한다.
3. 결과를 확인한다.
   - 종료 코드 2는 입력 오류다. 에러에 나온 허용 값(host, role, effort)으로 고쳐 다시 실행한다.
   - 종료 코드 1은 설정 파일이나 git 오류다. 에러에 나온 파일 경로를 사용자에게 보여 주고,
     파일을 임의로 지우거나 덮어쓰지 않는다.
   - `warnings`는 저장은 됐지만 host가 모를 수 있는 모델이라는 뜻이다. 그대로 전달한다.
     Codex 경고는 로컬 모델 캐시 기준이므로 계정이 쓸 수 있는지는 실제 실행으로만 확인된다.
   - local 쓰기의 `excluded: true`는 이번에 exclude 줄을 추가했다는 뜻이다.
4. `issueops model show --json`을 다시 실행해 바뀐 행의 값과 출처(`model_source`,
   `effort_source`)를 사용자에게 보여 준다.

## 하지 않는 것

- `~/.claude/agents/`, `~/.codex/agents/`, `~/.codex/config.toml`을 만들거나 고치지 않는다.
  역할 에이전트는 IssueOps가 세션을 띄울 때 실행 인자로 주입한다.
- claude나 codex를 실행해 모델을 시험하지 않는다. 사용자가 실측을 따로 요청했을 때만
  `issueops model resolve --json`의 `argv`로 빈 컨텍스트 세션을 띄운다.
- Fable은 사용자가 이름으로 지정할 때만 설정한다. 기본값이나 대안으로 제안하지 않는다.
- 설정 파일을 손으로 편집하지 않는다. 형식이 깨지면 IssueOps가 그 파일을 읽는 모든 명령이
  실패하거나 리뷰 모델을 비운다.
