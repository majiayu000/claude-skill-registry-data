---
name: issueops-review
description: Use when issueops-plan or issueops-verify needs an independent review of a cycle architecture document, plan, or implementation diff, or when the user asks for "아키텍처 검토", "계획 검토", "구현 리뷰", "architecture-review", or "devil's advocate" within an IssueOps cycle.
---

# IssueOps Architecture, Plan, and Implementation Review

이 스킬의 일은 **적대 리뷰 한 번을 실제로 실행하고 그 판정을 원장에 기록하는
것**이다. 계획 단계(아키텍처 문서와 계획)와 검증 단계(구현 diff)가 같은 규칙을 쓰도록 두 곳에서 이 스킬을
호출한다. 대상 파일을 고치는 것은 호출한 단계의 일이다.

- 계획 단계: [`issueops-plan`](../issueops-plan/SKILL.md)
- 검증 단계: [`issueops-verify`](../issueops-verify/SKILL.md)
- 리뷰 렌즈 원문: [`architecture-review`](../architecture-review/SKILL.md)
- 원격 반영 프로토콜: [`issueops-remote-write`](../issueops-remote-write/SKILL.md)

## 입력

`--target architecture`, `--target plan`, `--target diff` 세 가지다. 대상을 정하고 리뷰어에게 줄 자료를
모은다.

| target | 리뷰 대상 | 함께 주는 자료 |
|---|---|---|
| `architecture` | staged `architecture` artifact 전문(`artifact stage --name architecture`로 올린 것) | 이슈 본문, intent contract의 성공 기준, 관련 문서 발췌 |
| `plan` | `status --json`의 `plan_path` 파일 전체(링크 전이면 staged plan artifact) | 이슈 본문, intent contract의 성공 기준, 승인된 아키텍처 문서 전문 |
| `diff` | `git -C "$WORKTREE" diff "$BASE_SHA"` 전체 | plan 파일 전체, 봉인 intent 문서(`<artifact_dir>/intent.md`, 없으면 `status --json`의 `.intent`), 검증 명령과 결과, 변경한 프로젝트 문서 |

리뷰가 "무시된 결정"을 잡으려면 계획이 인용한 항목만으로는 부족하다. plan과 diff 모두 리뷰를
띄우기 전에 `.issueops/ADR.md`, `.issueops/CAUTIONS.md`, `.issueops/ARCHITECTURE.md` 세 색인을 직접 열어
변경 모듈과 관련된 항목을 고르고, 그 항목이 가리키는 모듈·기록 파일을 연다. `project_docs_route`에
대상 요약을 넣어 나온 dated `cautions/`·`adr/` 기록은 여기에 **더한다**. route 결과가 세 색인을
대신하지 않는다. diff 리뷰에는 `.issueops/CONVENTIONS.md`와 `.issueops/TESTING.md`를 더하고, 두 색인의
모듈 표가 변경 영역(예: 변경 언어의 기본 검증, CLI·JSON 출력 계약)을 넘기는 모듈 파일도 연다.
grep으로 색인의 한 줄만 본 것은 연 것이 아니다.

모든 변경에 걸리는 원칙(`.issueops/CONSTITUTION.md`)도 연다. 대상이 원칙에 걸리는 동작(반복·재시도·감시
루프, secret이 지나는 경로, 권한·실행 경계, 결함·회귀 수정)을 담으면, 그 원칙 문장을 리뷰어 프롬프트의
문서 발췌에 넣는다. 결함·회귀 수정이면 문제 해결 원칙의 근본 원인 두 문장
(`.issueops/CONSTITUTION.md:69-70`)을 넣는다.

리뷰를 실행하기 직전에 exact lifecycle ID로 다음 명령을 읽는다. 준비 자료의
reviewer 메타데이터는 준비 당시 기본값이며 현재 리뷰 설정을 대신하지 않는다.

```bash
issueops next --id "$ISSUEOPS_ID" --json
# .review.model, .review.effort, .review.tier, .review.lenses
```

이 값은 리뷰 역할(implement 전은 `plan-review`, 이후는 `diff-review`)을 `issueops model`
설정(local > global > 내장 기본값)으로 해석한 model·effort와 현재 변경 집합 티어다. 스킬 본문에
모델 이름 표를 복사하지 않는다. 조회에 실패하거나 review의 model/effort/tier/lenses가 누락되면
진행하지 않고 조회 실패나 누락 필드를 보고한다. `review.model`이 비어 있고 `warnings`에
`agent model settings are invalid`가 있으면 그 파일 경로를 보고하고 멈춘다. 경고 없이 비어
있으면 이 호스트의 기본값이 없으므로 어떤 모델로 리뷰할지 사용자에게 묻는다.
사용자가 reviewer 모델이나 effort를 명시했다면 해당 값에만 그 지시를 우선하고,
지정하지 않은 값은 현재 출력을 따른다. owner-model/owner-effort override는 구현자
선택이며 reviewer 지정으로 해석하지 않는다.

`--target diff`는 정리와 문서 반영이 끝나 봉인된 diff에 실행한다. 검증과 리뷰의
동시 실행은 `issueops-verify`를 따르며, 모든 필수 결과를 확인한 뒤 판정을 기록한다.
판정이 fingerprint에 묶이므로, 리뷰 뒤 파일을 고치면 그 판정은 무효가 된다.

## 실행

현재 호스트의 delegation 도구로 architecture-review를 **빈 컨텍스트의 새 세션**에 띄운다.
띄우기는 이 세션이 지금 하는 도구 호출이다. 리뷰어 프롬프트를 파일로 써 두고 끝내지 않는다.
기록할 판정과 finding은 서브에이전트가 돌려준 출력에서 옮긴다. 서브에이전트를 백그라운드로 띄웠으면 결과가
도착할 때까지 기다린다. 시작됐다는 응답(실행 ID, launch 안내)은 판정이 아니다. 저자 세션이 먼저 읽고 내린
판단은 판정이 아니므로 기록하지 않는다. 서브에이전트를 띄우지 못했으면 판정 없이 그 사실과
이유를 보고한다. `--reviewer-context subagent`는 서브에이전트가 실제로 돌려준 판정에만 쓴다.
필수 수정의 기준은 [`architecture-review`의 Blocking threshold](../architecture-review/SKILL.md#blocking-threshold)를
따른다. `architecture`는 아키텍처 문서의 결정과 계약을, `plan`은 계획을, `diff`는 구현 동작과 영향받은 계약을 확인한다.
리뷰가 지적을 냈다는 이유만으로 수정하지 않고, 발생 조건·위반한 요구사항·근거가
맞는지 확인한 뒤 필요한 수정만 한다. 반증된 지적은 그 증거를 재리뷰에 전달한다.

저자 세션이 architecture-review의 게이트를 직접 밟아 보는 것은 리뷰가 아니다. 문서나 계획을 쓴
에이전트는 매몰 비용을 지고 있고 자기 합리화를 기억하며 자기 설계를 무의식적으로
변호한다. 독립성이 기제 전부다. 계획에 아무 투자도 하지 않은 새 컨텍스트만이 저자가
못 보는 결함을 본다.

프롬프트에 다음을 전부 넣는다. 서브에이전트는 빈 컨텍스트에서 시작하므로 여기 없는
것은 리뷰어에게 존재하지 않는다.

1. 대상 전문(위 표의 리뷰 대상과 함께 주는 자료).
2. 성공 기준과 범위 경계. `diff` 대상이면 intent 문서의 성공 기준·비목표 대비 diff가 무엇을 덮고 무엇을
   벗어나는지도 판정하게 한다.
3. `## 입력`에서 고른 문서 항목의 경로, 제목, 관련 본문 발췌. 리뷰어는 지적마다 위반한
   문서 경로와 항목을 근거로 적고, 대조했지만 관련 없는 문서는 그 목록을 남긴다.
4. 출력 계약: 판정(`pass|revise|stop`), 필수 결함별 위치·발생 조건·위반한 계약·근거와
   최소 수정 또는 확인 방법. 발견한 필수 결함은 한 번에 전달한다. 결함이 없으면
   없다고 쓰고 확인한 계약과 근거를 남긴다. 선택적 개선 목록과 대안 설계는 요구하지 않는다.
   필수 결함의 위반한 계약 칸에는 문서 규칙 원문(경로:줄)이나, 대상이 약속한 동작이 실제로
   깨지는 입력·경로를 적는다. 이 칸을 채우지 못한 지적(테스트·게이트를 더 두면 좋겠다는 선호
   포함)은 비차단 메모로 적는다. 지금 동작이 맞는 작은 중복(있는 상수·함수 대신 같은 값을 다시 적은 것)도
   비차단 메모다. 중복 때문에 실제로 어긋날 때(값이 이미 다르다, 대상 안에 한쪽만 바뀌는 경로가 있다)만 그
   근거와 함께 필수 결함으로 올린다.
   대상이 만들지 않았고 성공 기준과도 무관한 결함(`diff`면 base에 이미 있던 코드·문서, `plan`이면 계획이
   건드리지 않는 기존 동작)은 기존 결함으로 표시해 비차단 메모에 둔다. 다만 이슈·intent의 성공 기준이
   고치라고 한 결함, 결함 수정 사이클에서 그 결함의 근본 원인, 대상이 성공 기준을 지키려고 기대는 기존
   동작은 기존 결함으로 내리지 않는다. 대상이 기존 결함을 새 경로로 노출하거나 악화시켰으면 그렇게 만든
   대상의 줄을 근거로 필수 결함에 남긴다.
   판정을 돌려주기 전에 필수 결함마다 위반한 계약 칸을 한 번 더 확인한다. 인용한 문서 줄을 실제로 다시 열어
   그 문장이 이 결함을 금지하는지 보고, 깨지는 입력을 적었다면 대상이 그 입력에 대해 무엇을 약속했는지 대상
   본문에서 찾는다. 문서 문장이 다른 것을 말하거나 대상이 그 입력에 대해 약속한 것이 없으면 그 결함은 비차단
   메모로 옮기고, 남은 필수 결함으로 판정을 다시 정한다.
   최소 수정을 처방할 때는 그 수정이 기대는 사실(명령·플래그, 설치된 라이브러리 버전의 동작,
   게이트 형식)을 결함과 같은 수준으로 확인하고, 수정이 함께 다뤄야 할 입력·경로(빈 값, 진행 중
   상태, 다른 호출 경로)를 같은 결함 안에 적는다. 확인하지 못한 처방은 "확인 안 한 처방"으로
   표시한다. 다음 라운드가 처방의 결함을 찾느라 한 바퀴를 더 돌지 않게 하려는 것이다.
   필수 결함마다 같은 유형의 다른 발생 위치를 대상 전체에서 찾아 같은 결함 안에 나열한다. delta
   라운드에서도 대상 파일을 직접 열어 검색한다. 찾은 방법(검색한 패턴과 범위)을 함께 적고, 다른 위치가
   없으면 "다른 위치 없음"과 그 근거를 적는다. 한 위치만 고친 수정이 다음 라운드에서 같은 결함으로 다시
   걸리지 않게 하려는 것이다.
   명령으로 판별할 수 있는 지적에는
   `CHECK: <read-only 명령> | EXPECT: <출력에 있어야 할 문자열>`을 함께 요구한다.
   한 줄 명령으로 표현할 수 없으면 확인할 가정·절차·통과 조건을 적는다. 필수 계약의
   증거가 빠졌으면 **필수 검증 공백**으로 남기고 `revise` 또는 `stop`으로 판정한다.
   필수 검증 공백은 대상이 지켜야 할 계약(대상이나 인용 문서에 적힌 것)을 확인할 수단이
   대상에 없을 때다. 리뷰어가 코드를 읽지 않아 남은 추측("다른 경로와 공유될 수 있다",
   "나중에 어긋날 수 있다")은 공백이 아니다. 열 수 있는 파일이면 먼저 열어 발생 조건을
   확인한 뒤 지적한다. 열 수 없으면 그 가정과 최소 확인을 **확인 질문**으로 따로 적고
   판정을 바꾸지 않는다.
   호출자가 확인한 결과를 다음 라운드에 전달하며, CHECK 형식의 유무로 차단 여부를
   바꾸지 않는다([`architecture-review`의 Blocking threshold](../architecture-review/SKILL.md#blocking-threshold)).
5. 대상에 맞는 렌즈. `architecture`에는 architecture-review의 아키텍처 문서 렌즈를 적용한다.
   `plan`에는 architecture-review의 계획 렌즈와 아래 코드베이스 존중
   렌즈를 적용한다. 구현 전 `next.review.tier`는 변경 경로를 조회하지 않은 `default`이므로
   계획의 위험 분류로 해석하지 않는다. 계획에 명시한 인증·스키마 등 필수 계약을 확인한다.
   `diff`에는 `next.review.tier`와 `lenses`를 전달하고 선택된 렌즈만 적용한다.
   `docs-only`의 코드베이스 존중 렌즈는 `side-effect` 하나다. frontend 추가 렌즈는
   호출한 검증 단계의 규칙을 따른다.
   intent가 결함·회귀 수정이면 `diff`에 근본 원인 렌즈를 더한다. 이 렌즈는 `tier`와 `lenses` 목록과
   상관없이 더한다. diff가 원인을 제거하는지, 증상만 덮는지(출력 문구 보정, 테스트 기대값 완화, 문서만
   변경, 우회 분기) 판정한다. 증상만 덮었는데 대상·계획에 근본 원인이 이미 제거됐거나 현재 범위에서
   물리적으로 제거할 수 없다는 근거가 없으면 필수 결함이고, 위반한 계약 칸에는
   `.issueops/CONSTITUTION.md:70` 원문을 쓴다.

이름·스타일·선택적 리팩터링·가상 규모를 이유로 수정이나 추가 테스트를 요구하지 않는다.
영향받은 필수 동작의 증거가 부족하면 그 가정을 판별하는 최소 확인을 요청한다.
재현된 실패가 없다는 이유로 확인되지 않은 필수 동작을 통과시키지는 않는다.

코드베이스 존중 렌즈는 다음을 묻는다.

- **재사용**: 이미 있는 구현으로 됐을 일을 새로 만들지 않았는가. 같은 판정을 두 곳이
  소유하게 되지 않았는가.
- **성능**: 이 변경이 자주 불리는 경로에 관측·조회·할당을 늘리지 않는가. 같은 관측을
  두 번 하지 않는가. 변경이 제한 시간 안에 끝나야 하는 경로(hook, 요청 처리, CI job)에서
  기다리거나 재시도하면, 그 경로의 실제 설정 파일을 열어 제한 시간·재시도 값을 찾고 대상이 쓰는
  대기·재시도 시간과 비교한다.
- **하위 호환**: 계약 표면(포트 인터페이스, CLI 플래그, JSON 필드, 온디스크 형식)이
  기존 호출자를 깨지 않는가. 기본값이 종전 동작을 유지하는가.
- **side effect**: 파일·원격·durable state에 남는 변화가 문서화된 것과 일치하는가.
  실패했을 때 남는 상태가 사람이 이어받을 수 있는 모양인가.

렌즈에 걸린 항목도 [Blocking threshold](../architecture-review/SKILL.md#blocking-threshold)를 넘어야
필수 결함이다. 작은 중복의 기준은 위 4번 출력 계약을 따른다.

## 지적을 실행한다

리뷰어가 낸 CHECK는 호출자가 실행한다. 실행 결과는 다음 라운드의 **입력**이지
판정이 아니다.

```bash
issueops verify-work --json -- <CHECK>
```

- `--target architecture`, `--target plan`, `--target diff` 모두 이 경로로 실행한다. 계획 단계에는 아직 게이트
  원장 파일이 없다(원장은 4단계 진입의 `gates init`이 만든다). 그러니 여기서 `gates`
  명령을 부르지 않는다.
- plan 리뷰에서 살아남은 CHECK/EXPECT는 4단계 진입의 그 단일 `gates init` spec에
  `G(n+1)..`로 얹어 원장의 일부가 되게 한다.
- diff 리뷰의 CHECK는 원장에 넣지 않는다. 검증 단계에서 파일을 고치면 봉인이 바뀐다.
- 각 CHECK의 명령·종료 코드·EXPECT 일치 여부를 그 결함 옆에 적어 다음 라운드에 넘긴다.

## 기록

리뷰가 **끝난 뒤에만** 호출자가 기록한다. 기록이 리뷰를 대신하지 않는다.
`diff` 리뷰를 검증 배터리·스키마 확인·QA와 병렬로 수행했다면 모든 필수 결과를 모으고
현재 fingerprint가 시작 때와 같은지 확인한 뒤 기록한다. 검증 실패나 미확인 필수 계약이
있으면 먼저 도착한 `pass`를 기록하지 않는다. 실패 증거는 호출한 단계에 전달한다.

```bash
# --target architecture (pass일 때만 --approved)
issueops architecture review --id "$ISSUEOPS_ID" \
  --problem-summary "<문제>" --proposed-architecture "<아키텍처 결정>" --refactor-plan "<리팩터 계획>" \
  --alternative "<기각한 대안>" --risk "<위험>" --verification "아키텍처 검토로 대안과 위험을 확인했다" \
  --reviewer-context subagent --approved $RECORD_ACTOR_FLAGS --json

# --target plan
issueops devils-advocate review --id "$ISSUEOPS_ID" \
  --verdict pass --reviewer-context subagent \
  --finding "<무엇을 공격했고 왜 살아남았는가>" $RECORD_ACTOR_FLAGS --json

# --target diff
issueops implementation-review record --id "$ISSUEOPS_ID" \
  --verdict pass --finding "<finding>" --evidence "<evidence>" \
  --reviewer-host "$HOST" --reviewer-model "$REVIEWER_MODEL" --reviewer-effort "$REVIEWER_EFFORT" \
  $RECORD_ACTOR_FLAGS --json
```

`--reviewer-model`과 `--reviewer-effort`에는 실제 리뷰 실행에 넘긴 값을 shell-quote해
넣는다. 생성 owner command의 `<REVIEWER_MODEL>`·`<REVIEWER_EFFORT>`도 같은 값으로
채운다. 기본 티어 선택과 아래 3라운드부터의 상승은 구분하고, 상승 이유는 finding에 남긴다.
준비 자료의 고정값이나 상승 전 값을 감사 필드에 기록하지 않는다.

finding은 이슈의 `## 계획 검토` 구간과 `.issueops/issues/<n>/plan-review.md`로 팀에 보인다.
독자가 읽는 한국어 완성 문장으로 쓴다: 무엇을 공격했고 결과가 어땠는지. 해시, 커밋 SHA
전문, 로컬 절대 경로는 쓰지 않는다(렌더러가 가리지만 문장이 깨진다). 리뷰가 이슈
본문의 사실이 틀렸다고 판정하면 호출 단계가 `feedback add --classification
contract_change`로 기록한다([`issueops-plan`](../issueops-plan/SKILL.md)의 검토 루프).

`architecture review`의 승인은 스테이징한 아키텍처 문서의 sha256에 묶인다. 리뷰 뒤 문서를 고치면
`architecture_review_stale`이므로 다시 스테이징하고 새 리뷰를 받는다. `revise`면 문서를 고쳐 다시
리뷰하고(같은 5라운드 상한), `stop`이면 승인을 기록하지 않고 이슈 본문의 사실 변경을
`feedback add --classification contract_change`로 남긴 뒤 이슈를 동기화한다.

`reviewer_context`와 `reviewer_*`는 감사 필드이지 게이트 조건이 아니다. 하네스는
모델의 자기신고를 검증할 수 없으므로 verdict와 finding·evidence의 실질만 게이트한다.
그래서 이 필드를 사실대로 적는 것은 도구가 아니라 실행자의 책임이다.

## 루프 규칙

- 첫 라운드는 대상 전체를 검토한다. 수정 뒤의 라운드는 **delta 리뷰**다. 대상 전체를
  다시 읽히지 않고 직전 지적, 각 CHECK의 실행 결과, 대상의 delta, 영향받은 계약만
  새 컨텍스트 서브에이전트에 넘긴다. 판정과 기록할 finding은 그 서브에이전트가 정하고
  호출자는 받은 verdict를 그대로 기록한다. CHECK가 전부 통과했다는 사실은 delta 리뷰의
  입력이지 호출자가 `pass`를 정할 근거가 아니다.
  호출자는 다음 규칙을 delta 리뷰 프롬프트에 넣는다. delta 리뷰어는 직전 지적마다 해결됨 또는 남음만
  판정하고, 남음이면 남은 위치와 이유를 적는다. 반증 자료로 철회된 지적은 해결됨으로 적고 반증 근거를
  붙인다. 새 필수 결함은 delta와 영향받은 계약에서만 찾는다. 직전 라운드에 나온 지적을 다른 말로 다시
  내지 않는다.
- delta 리뷰를 띄우기 **전에** 호출자가 수정한 대상을 직접 점검한다. 실제 사이클에서 3~5라운드까지
  간 필수 결함의 절반 가까이가 이 점검으로 잡히는 종류였다(수정이 남긴 옛 표현, 게이트 형식, 틀린 처방).
  1. 수정이 바꾼 값(경로, 명령, 이름, 숫자, 상태, 규칙 문장)마다 옛 값을 대상 전체에서 검색해 남은
     곳을 모두 고친다. 바뀐 항목을 참조하는 절(단계 순서, 게이트, 하위 호환, 수용 기준)을 다시 읽어
     서로 맞는지 본다.
  2. 수정이 새로 단언하는 사실(명령·플래그 존재, 설치된 버전의 동작, `파일:줄`)을 명령으로 확인한다.
     리뷰어가 처방한 수정도 확인 전에는 가설이다. 처방이 틀렸으면 근거와 함께 다른 수정을 쓴다.
  3. 게이트를 고쳤으면 `issueops gates lint --plan <대상> --cwd <워크트리> --json`이 problems 없이
     끝나야 한다.

  세 점검의 결과(고친 곳, 확인한 명령과 출력, lint 결과)를 delta 리뷰 입력에 함께 넣는다.
- 구조나 범위가 바뀌면 전체 리뷰를 다시 띄운다. 필수 검증 공백은 그 확인 결과와
  영향받은 계약을 delta 리뷰에 포함한다. CHECK 형식이 없다는 이유만으로 전체를 반복하지 않는다.
- 같은 대상의 수정·재리뷰는 최대 5라운드다. 3라운드부터 5라운드까지는 상향된 리뷰 모델로
  띄운다. model과 effort는 다음 명령의 결과를 그대로 쓴다. `review-escalate` 설정이 있으면 그
  값이, 없으면 원래 리뷰 모델에 effort 한 단계 상향이 나온다. architecture와 plan 대상이면 `--role plan-review`다.

  ```bash
  issueops model resolve --host "$HOST" --role diff-review --tier "$TIER" --round "$ROUND" --json
  # .model, .effort, .argv
  ```

  사용자가 reviewer 모델을 이름으로 지정했으면 그 값을 `--model`로 함께 넘긴다. 실제로 넘긴 두
  값을 `--reviewer-model`·`--reviewer-effort`(diff) 또는 finding 첫 줄(plan)에 적는다. 그 안에
  통과하지 못하면 남은 결함과 시도한 수정을 보고한다.
  - 서브에이전트 도구는 effort를 받지 않는다. 그러므로 `.argv`로 빈 컨텍스트 세션을 띄운다.
    Claude는 `.argv`에 `--allowedTools
    "Bash Read Grep Glob Skill"`을 붙이고 프롬프트를 표준 입력으로 넘긴다. 출력 파일은 ignored 영역
    `.issueops/issues/<n>/review/`나 워크트리 밖에 둔다. 워크트리 안 미추적 파일은
    fingerprint에 들어가 봉인을 깬다.
  - Fable 5는 명시적 수동 지정 전용이다(`.issueops/adr/2026-09-24-claude-role-models-opus-5-plans-and-reviews-sonnet-5-impleme.md`).
    해석기는 Fable을 기본값이나 상향 결과로 내지 않으므로 3~5라운드용으로 고르지 않는다.
- 같은 plan phase의 비-waived `revise`는 다섯 번까지다. 여섯 번째는 CLI가
  `revise round cap reached`로 거부한다. stop 판정 뒤의 `regress` 재계획도 사이클당 다섯 번까지다. 그때의 탈출은 `stop`을 기록하고
  `issueops remote reflect-devils-advocate --confirm`으로 반영한 뒤 `regress`로
  재계획하거나, 근거를 적은 `--waive --waiver-rationale`로 넘어가는 것이다. `revise`
  상태에서 `regress`를 직접 부르면 거부된다.
- `revise`면 호출한 단계가 근거를 확인해 필요한 결함을 고치고 이 스킬을 다시 실행한다.
  반증된 지적만 남았으면 대상을 불필요하게 바꾸지 않고 반증 자료로 새 판정을 받는다.
- `stop`이면 `--target plan`은 호출자가 `issueops regress --id
  "$ISSUEOPS_ID" --reason "<TEXT>"`로 grill까지 되돌려 재조사·재계획한다.
  `--target diff`는 publication을 멈춘다. 승인 범위 안에서 해소할 수 있는 결함은
  구현 단계로 돌아가 수정하고 다시 리뷰한다. 범위·권한·요구사항 결정이 필요할 때만
  사용자에게 묻는다. stop 판정을 pass로 바꾸거나 우회하지 않는다.
- 현재 digest·fingerprint에 유효한 `pass`가 있고 새 결함 증거나 계약 변경이 없으면
  재사용한다. 불안감이나 선택적 개선은 추가 리뷰 사유가 아니다.
- `pass`는 finding이 하나 이상 있어야 기록된다. 이 finding은 확인한 계약과 안전한 이유를
  적는 증거이며, 결함을 하나 이상 만들어 내라는 뜻이 아니다.
- `--waive`는 override이며 `--waiver-rationale`이 필수다. "지적을 반영했다"는 뜻으로
  쓰지 않는다. 반영했으면 다시 리뷰해서 새 판정을 받는다.
- 판정은 plan sha256(`reviewed_plan_digest`) 또는 change fingerprint
  (`reviewed_fingerprint`)에 묶인다. 판정 뒤 대상을 고치면
  `devils_advocate_review_stale`·`implementation_review_stale`이 되어 implement 진입과
  publication이 막히므로 다시 실행해 새 판정을 기록한다.

## 이슈 반영

계획 판정을 팀이 보게 하려면 [`issueops-remote-write`](../issueops-remote-write/SKILL.md)의
절차로 다음을 실행한다.

```bash
issueops remote reflect-devils-advocate --id "$ISSUEOPS_ID" --confirm --json
```

이슈에는 라운드 흐름 한 줄("1차 수정 요청(지적 3건) → 계획 수정 → 2차 통과")이
보이고, `stop` 판정일 때만 중단 이유가 목록으로 붙는다. 지적 원문은 record와
`plan-review.md`에 있다. `stop` 판정은 반영이 특히 중요하다. 사이클이 뒤로 돌아간
이유가 이슈에 남지 않으면 팀이 보는 진행 상태와 실제가 어긋난다.

## 나쁜 예

- 저자 세션이 인라인으로 게이트를 밟고 `--reviewer-context subagent`로 기록한다.
  기록은 통과하지만 리뷰는 없었다.
- 리뷰를 실행하지 않고 `--verdict pass`를 기록한다. 게이트 연극이다.
- CHECK가 전부 통과했다는 이유로 호출자가 `pass`를 기록한다. 판정 없는 기록이다.
- `revise` 판정을 고치는 대신 `--waive`로 닫는다.
- 판정 뒤 계획이나 코드를 고치고 재검토를 생략한다. stale 판정으로 다음 단계에서
  막히고, 막히지 않았다면 검토되지 않은 변경이 게시된 것이다.
- `reviewer_model`이 기록됐으니 planner급 모델이 돌았다고 믿는다. 그 필드는 감사
  기록이지 증명이 아니다.
- `--target diff` 리뷰에 plan을 주지 않는다. 무엇을 하기로 했는지 모르는 리뷰어는
  구현이 계획에서 벗어났는지 판정할 수 없다.
- 3~5라운드에서 '다른 모델'로 Fable 5를 고른다. Fable 5는 사용자가 이름으로 지정할 때만 쓴다.

## 검증

- `issueops status --id "$ISSUEOPS_ID" --json`의 `devils_advocate_review`
  또는 `implementation_review`에 이번 판정이 있고 digest·fingerprint가 현재 대상과
  같은지 확인한다.
- `issueops next --id "$ISSUEOPS_ID" --json`의 `missing`에
  `devils_advocate_review*`·`implementation_review*`가 남아 있지 않은지 확인한다.
- 남아 있으면 그 키가 곧 다음 명령이다. 추측하지 말고 `next_command`를 실행한다.
