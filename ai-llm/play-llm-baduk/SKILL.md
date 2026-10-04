---
name: play-llm-baduk
description: 설치된 `baduk` CLI로 사람 대 LLM 또는 CLI 대 CLI 바둑 대국을 진행한다. 사람 차례 대기, 패스, 무르기, 계가 합의, 재개와 종료를 처리할 때 사용한다.
---

# LLM 바둑 대국

사람은 브라우저 보드에서 수를 두고, 언어 모델은 설치된 `baduk` 명령으로 자신의 수를 전달합니다. CLI 대 CLI 모드에서는 서로 독립적인 AI 세션 두 개가 흑과 백을 각각 맡습니다. 매번 반환된 스냅샷을 현재 상태의 기준으로 사용합니다.

## 시작 또는 이어하기

1. `baduk --help`를 실행하고 표시된 명령 규약을 사용합니다.
2. `baduk status`로 현재 스냅샷을 확인합니다. `status`는 색상 지정 여부와 관계없이 읽기 전용입니다.
3. 명령이 없으면 LLM Baduk을 설치해야 한다고 알리고 멈춥니다.
4. 서버에 연결할 수 없으면 `baduk start`를 별도 프로세스로 실행하고, 대국 명령은 별도 셸에서 실행합니다.
5. 상태가 `setup`이면 브라우저에서 대국 모드·판 크기·참가자 이름을 설정하도록 안내합니다. 대국 생성 명령은 CLI에 없습니다.
6. 상태가 CLI 대 CLI이면 자신의 색상을 정해 모든 참가자 명령의 서브명령 앞에 `--color black` 또는 `--color white`를 붙입니다. 두 색상은 각각 별도 AI 세션에서 실행하며, 공유 세션 설정을 사용하지 않습니다.

## 턴 진행

- `status`가 `finished`, `resigned` 또는 `draw`이면 종료 상태입니다. `result`와 마지막 이벤트를 알리고 대국 루프를 끝냅니다.
- `game_reset` 이벤트가 반환되면 해당 종료 코드는 일시적인 대기 깨움 신호로 취급합니다. `baduk status`를 다시 실행해 새 상태에서 계속합니다.
- 사람의 차례이면 `baduk wait`를 실행합니다. 계가 중인 상태에서 사람의 다음 변경을 기다릴 때는 검토한 스냅샷의 revision을 `baduk wait --after-revision N`으로 전달합니다.
- 언어 모델 차례이면 현재 스냅샷의 `legal_moves`에서 수를 하나 골라 `baduk move MOVE`로 제출합니다. `pass`도 유효한 수입니다. 즉시 반환이 필요할 때만 `--no-wait`를 사용합니다.
- 대기 중인 사람의 무르기 요청이 반환되면 사용자 지시와 현재 대국 맥락으로 수락 또는 거부를 결정하고, `baduk takeback accept` 또는 `baduk takeback reject` 중 하나를 실행합니다. 요청이 처리될 때까지 새 수를 제출하지 않습니다.
- 언어 모델의 최근 수를 무르고 싶으면 `baduk takeback request`를 실행한 뒤 반환된 수락·거부 스냅샷을 처리합니다.

## CLI 대 CLI 턴 진행

- 흑 세션과 백 세션을 각각 독립적으로 실행합니다. 모든 `wait`, `move`, `takeback`, `resign`, `score` 명령에 해당 세션의 `--color`를 다시 지정합니다.
- 기본 `move`는 상대 응답을 기다리며 `--no-wait`도 사용할 수 있습니다. 한 세션에서 대기 명령을 하나만 실행합니다.
- `game_reset` 이벤트가 반환되면 종료 코드가 일시적인 대기 깨움 신호입니다. 해당 세션에서 `baduk --color COLOR status`를 다시 실행해 새 상태를 읽습니다.
- 무르기 요청은 상대 색상 세션이 `baduk --color COLOR takeback accept` 또는 `baduk --color COLOR takeback reject`로 처리합니다.
- `color_required`와 `player_not_cli`는 대국 상태에 따른 정상 오류입니다. 색상, 대국 모드, 참가자 제어 주체를 확인하고 명령을 고칩니다.
- CLI가 상대 AI를 자동으로 실행하지 않습니다. 두 세션의 진행과 대기 상태를 각각 관리합니다.

## 계가와 합의

1. 상태가 `scoring`이면 스냅샷의 `stones`, `dead`, `seki`, `territory`, `prisoners`, `totals`를 검토합니다.
2. 사람 대 LLM 모드에서 죽은 돌이나 세키를 표시하려면 `baduk score dead POINT` 또는 `baduk score seki POINT`를 실행합니다. 표시는 연결된 돌무리 전체에 적용됩니다. CLI 대 CLI 모드에서는 두 명령 모두 검토한 revision을 `--revision N`으로 명시합니다.
3. 검토를 끝낸 스냅샷의 revision을 사용해 합의합니다. 사람 대 LLM 모드는 `baduk score accept`를 실행하면 현재 revision을 자동 조회할 수 있고, CLI 대 CLI 모드는 반드시 `baduk --color COLOR score accept --revision N`을 실행합니다. 검토 후 상태가 바뀌었으면 새 스냅샷을 다시 검토하고 새 revision을 사용합니다.
4. revision 충돌이 나면 해당 색상 세션에서 `status`를 다시 읽고 새 스냅샷을 검토한 뒤 명령을 재실행합니다.
5. 양측 합의가 끝나면 반환된 종료 스냅샷의 결과를 알립니다. 계가 의견이 다르면 해당 색상으로 `baduk --color COLOR score resume`을 실행하고 새 상태를 확인해 턴 루프를 재개합니다.

## 운영 규칙

- 각 세션에서 한 번에 차단 대기 명령 하나만 실행합니다.
- 브라우저의 색상 선택과 사람 수 입력은 사람의 작업으로 둡니다.
- 서버가 반환한 법적 수와 현재 revision을 벗어나서 수나 계가 결과를 추측하지 않습니다.
- 서버 프로세스는 수, 무르기, 계가, 재개와 종료를 처리하는 동안 유지합니다.
