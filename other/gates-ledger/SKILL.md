---
name: gates-ledger
description: Create, check, and report task gate ledgers with the issueops gates CLI. Turns acceptance criteria into G-numbered CHECK and EXPECT gates in .issueops/issues/<n>/gates.md or .issueops/gates/<scope>.md, fills EVIDENCE by running the checks through the command policy, and abandons gates honestly. Use when issueops-plan, issueops-implement, issueops-slop-clean, issueops-verify, or verified-execution needs a gate ledger, or when the user says "게이트 원장", "gates 만들어줘", "수용 기준 체크".
---

# Gates Ledger

이 스킬의 일은 **수용 기준을 실행 가능한 게이트 원장으로 만들고 그 원장을 CLI로
채우는 것**이다. 원장은 "무엇이 됐다고 말할 수 있는가"를 명령과 기대 출력으로
고정한다. 사람이 읽고 판단하는 체크리스트가 아니라 다시 실행할 수 있는 기록이다.

- 계획이 게이트를 만든다: [`issueops-plan`](../issueops-plan/SKILL.md)
- 구현이 EVIDENCE를 채운다: [`issueops-implement`](../issueops-implement/SKILL.md)
- 정리 뒤 재실행: [`issueops-slop-clean`](../issueops-slop-clean/SKILL.md)
- 검증이 유효한 증거를 읽고 필요할 때 재실행한다: [`issueops-verify`](../issueops-verify/SKILL.md)

## 경로 규칙

- provider 이슈 번호가 있으면 `<worktree>/.issueops/issues/<n>/gates.md`다.
- 번호가 없으면 `.issueops/gates/<scope>.md`다.
- 원장은 워크트리 **안**에 둔다. 밖에 두면 변경 집합에 들어가지 않아 커밋되지 않고,
  다음 세션이 그 원장을 찾지 못한다.
- 같은 폴더의 `plan.md`, `intent.md`, `spec.md`, `plan-review.md`는 구현 자료의 추적
  사본이다. 경로를 제한하는 게이트를 쓸 때 `.issueops/issues/<n>/` 전체를 허용 경로에
  넣는다. 봉인 원본이 있는 `artifact/` 하위는 계속 무시된다.
- root `GATES.md`와 `gates/*.md`는 더 이상 찾지 않는다. `gates abandon`은 `--file`을
  반드시 받는다.

## 만들기

수용 기준 하나가 게이트 하나다. 결과는 관찰 가능한 동작으로 쓰고, 그것을 관찰하는
읽기 전용 명령과 그 출력에 들어 있어야 할 문자열을 함께 적는다.

```bash
issueops gates init --file "$WORKTREE/.issueops/issues/$ISSUE/gates.md" --scope "$ISSUE" \
  --gate "G1: <관찰 가능한 결과> | CHECK: <read-only 명령> | EXPECT: <출력 줄 전체·줄 머리 또는 /정규식/>" \
  --gate "G2: <결과> | CHECK: <명령> | EXPECT: <문자열>" --json
```

- 결과 문장은 "테스트를 추가한다"가 아니라 "미머지 아티팩트는 닫히고 머지된 것은
  거부된다"처럼 동작으로 쓴다.
- CHECK는 command policy를 지나므로 셸 확장과 파이프 우회를 넣지 않는다.
  `$(...)`, 백틱, `&&`로 이어 붙인 우회는 정책이 거부한다. 한 게이트에 명령 하나다.
- 통과 조건은 EXPECT 일치와 종료 코드 0 **둘 다**이다. 한쪽만으로는 통과하지
  않는다.
- EXPECT는 부분 문자열이 아니다. 세 형식 중 하나여야 통과한다(`internal/domain/gates/evaluate.go`
  `ExpectMatches`): 출력의 어느 한 **줄 전체**가 EXPECT와 같거나, 어느 한 줄이 EXPECT로
  **시작하고 바로 뒤가 공백·탭**이거나(`EXPECT: ok`가 `ok  	issueops/...` 줄에 맞는 이유),
  `/정규식/` 형식(`/Skill is valid/`, `/^ok\s/m`처럼 `i`·`m`·`s` 플래그 가능)이 출력에
  매치돼야 한다. `grep -n`처럼 줄 앞에 번호가 붙는 출력은 정규식 형식으로 쓴다.
- 출력에 자격 증명처럼 보이는 값이 하나라도 있으면 EVIDENCE 전체가 `<redacted>`로
  바뀌어 어떤 EXPECT도 매치되지 않는다. `go test ./...`처럼 긴 출력은
  `python3 -c`로 감싸 출력을 캡처하고 종료 코드만 `ALL_PASS` 같은 한 줄로 바꿔 내보낸다.
- 자동으로 관찰할 수 없는 결과는 게이트로 쓰지 않는다. 그런 것은 수동 확인 기록으로
  남기고 EVIDENCE에 관측 시각과 관측값을 적는다.

원장을 만들기 전에, 그리고 계획에 게이트를 적거나 고칠 때마다 실행 없이 검사한다.

```bash
issueops gates lint --plan "$PLAN" --cwd "$WORKTREE" --json   # 또는 --gate SPEC..., --file "$LEDGER"
```

`problems`가 있는 게이트는 구현과 상관없이 met이 될 수 없다. 정책 거부, `|`로 잘리는 정규식,
셸 연산자, 컴파일되지 않는 정규식이 여기 해당한다. 고친 뒤 다시 lint한다. 큰따옴표 안의
`\`는 토크나이저가 먹는다는 경고(`argv`에 실제 값이 나온다)와 읽지 못한 `CHECK:` 줄 경고도 확인한다.

원장에서 `CHECK`·`EXPECT`·`EVIDENCE`는 게이트 줄 아래 목록 기호 없이 들여쓴 줄에서만 읽힌다. spec 형식(`| CHECK:`)을
체크박스 줄에 그대로 두거나 `- EVIDENCE:`처럼 목록 항목으로 적으면 그 값은 무시된다. `gates lint --file`,
`gates status`, `gates check`는 이런 게이트를 `warnings`에 이름과 함께 적는다.

## 검사

```bash
issueops gates check --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --write --json
```

- `--write`가 각 게이트의 EVIDENCE를 실제 출력으로 채운다. 이것이 원장을 채우는
  유일한 방법이다.
- 네트워크가 필요한 CHECK는 `--network`를 붙인다. 붙이지 않으면 정책이 막는다.
- 오래 걸리는 CHECK는 `--timeout-seconds N`으로 한도를 올린다.
- 종료 코드 1은 미충족 게이트가 남았다는 뜻이다. 실패가 아니라 아직 아니라는 뜻이므로
  원장을 고치지 말고 구현을 고친다.

## 상태와 보고

```bash
issueops gates status --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --json
issueops gates report --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE"
```

`--file`·`--cwd`·`--workspace-root`는 세 명령에서 같은 값을 쓴다. 다르면 다른 원장을
보게 되고, 통과했다고 보고한 원장과 게이트가 읽는 원장이 달라진다.

## 포기

실행할 수 없다고 판정한 게이트는 정직하게 닫는다.

```bash
issueops gates abandon --gate G3 --reason "<왜 이 게이트를 실행할 수 없는가>" --file "$LEDGER" --json
```

EXPECT를 느슨하게 고쳐 통과시키지 않는다. 그렇게 하면 원장은 통과하고 결과는
검증되지 않은 채 남는다. 포기 사유는 다음 사람이 같은 판단을 다시 할 수 있게 쓴다.

## IssueOps와의 관계

- strict pr-readiness는 자기 이슈 번호의 원장과 익명 원장만 판정하고, 다른 번호의
  원장은 warning으로 건너뛴다.
- 미충족 게이트가 남으면 `gates_incomplete:<file>`로 pr 진입이 막힌다. 원장이 아예
  없으면 이 요구는 추가되지 않는다.
- 단계별 소유: 3단계 계획이 원장을 만들고, 4단계 구현이 `--write`로 EVIDENCE를 채우며,
  5단계 정리 뒤 다시 `--write`로 재실행한다. 7단계는 `issueops-verify`의 증거 재사용
  조건을 확인해 `status`로 읽거나 `check`로 재실행한다.
- 원장 파일은 변경 집합에 포함되므로 `ai-slop-clean record` 이후에 원장을 고치면
  fingerprint가 바뀌어 `ai_slop_clean_stale`이 된다. 원장 갱신은 봉인 전에 끝낸다.

## 나쁜 예

- EVIDENCE를 손으로 적는다. 명령을 실행하지 않고 채운 증거는 증거가 아니다.
- 실패한 CHECK를 EXPECT 완화로 통과시킨다.
- 원장을 source checkout이나 워크트리 밖에 만든다. 커밋되지 않고 다음 세션이 못 찾는다.
- 같은 이슈 번호로 canonical과 legacy 원장을 둘 다 남긴다. pr 진입이 막힌다.
- CHECK에 `$(...)`나 파이프 체인을 넣는다. 정책이 거부하고, 통과해도 무엇을 관찰했는지
  다음 사람이 재현할 수 없다.
- 게이트를 "구현한다"처럼 작업으로 쓴다. 작업은 끝났는지 관찰할 수 없다.

## 검증

- `issueops gates status --file "$LEDGER" --cwd "$WORKTREE" --workspace-root "$WORKTREE" --json`으로
  미충족 게이트가 0인지 확인한다.
- `issueops pr-readiness --id "$ISSUEOPS_ID" --strict --json`의 `missing`에
  `gates_incomplete:`로 시작하는 키가 없는지 확인한다.
- 원장 파일이 `git -C "$WORKTREE" status --porcelain`에 커밋 대상으로 보이는지 확인한다.
