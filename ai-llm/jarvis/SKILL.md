---
name: jarvis
description: git 변경량을 self-paced로 폴링하다 직전 리뷰 이후 새 변경이 쌓이거나·위험 경로가 바뀌거나·새 커밋이 생기면 jarvis-once 단발 리뷰를 자동 실행하는 워치 루프. 반복은 /loop의 self-paced 모드 위에서 도므로 반드시 /loop /jarvis로 띄운다. 고정 라인/파일 임계값은 없다. args(key=value)로 강도 프리셋(strength)·폴링 간격·경로·위험 경로를 설정한다. args 없이 부르면 최초 1회 강도를 물어본다(이전 설정은 .jarvis/args에서 자동 복원). 첫 로드 직후엔 잠깐 빠르게 폴링한다(warmup). "jarvis", "변경 감지 리뷰 루프", "jarvis 워치" 요청 시 사용.
---

# jarvis

사람이 직접 코드를 짜는 동안 곁에서 git 변경량을 싸게 폴링하다가, 직전 리뷰 이후 **새 변경이 쌓이면**(분량 임계 없음) `jarvis-once`(단발 navigator) 스킬을 자동으로 한 번 돌려주는 self-paced 워치 루프다.

- **폴링은 토큰을 거의 쓰지 않는다** (`git diff --shortstat` 한 번). 비싼 `jarvis-once` 풀 리뷰는 직전 리뷰 이후 새 변경이 쌓였거나·위험 경로가 바뀌었거나·새 커밋이 생겼을 때만 실행한다.
- **이벤트 기반이 아니다.** 사람 손 편집을 실시간으로 깨우는 OS 이벤트는 없으므로 주기적 wake로 확인한다. 대신 확인 자체를 극도로 싸게 유지한다.
- **`jarvis-once`는 코드를 직접 고치지 않는다** (리뷰/제안/다음 스텝만). 사람이 "이거 고쳐줘"라고 하면 그 턴은 일반 개발 모드로 전환한다.

> **이름 정리:** `jarvis`(이 스킬) = *지속 워치 루프*(진입점). `jarvis-once` = 트리거 시 *1회만 실행되는 단발 navigator*. 워치가 깨우면 `jarvis-once`를 호출한다.

## 실행 — `/loop`로 자기 반복

이 스킬은 반드시 **`/loop /jarvis [args]`** 로 띄운다. 반복의 엔진은 `/loop`의 **self-paced(dynamic) 모드**이고, 그 위에서 절차 4의 `ScheduleWakeup`이 다음 tick 간격을 스스로 정한다.

> ⚠️ **`ScheduleWakeup`은 `/loop` dynamic 모드 안에서만 동작한다.** 맨 `/jarvis`(=`/loop` 없이 호출)에서 부르면 호출은 성공한 것처럼 리턴하지만 **아무것도 예약되지 않고 조용히 무시된다.** 그래서 `/loop` 없이 띄우면 첫 tick 뒤 루프가 그대로 죽는다. 진입점은 항상 `/loop /jarvis`다.

> ⚠️ **`/loop`에 간격을 직접 주지 말 것.** `/loop /jarvis`처럼 **간격 없이** 띄워야 dynamic 모드가 되어 절차 4의 `ScheduleWakeup`(=`active`/`idle`/`debounce`)이 주기를 몬다. `/loop 5m /jarvis`처럼 `/loop`에 고정 간격을 주면 그 고정 스케줄이 이겨서 jarvis의 `active`/`idle`이 **무시된다.** 주기 조절은 항상 jarvis args로 한다 — 예: `/loop /jarvis active=3m idle=20m` 또는 `/loop /jarvis strength=high`. (Bedrock/Vertex/Foundry 환경은 간격 없는 `/loop`도 고정 스케줄로 돌아 self-pace가 적용되지 않는다.)

- **시작**: 사용자가 `/loop /jarvis [args]`를 한 번 호출한다. → 이번 tick을 수행하고, 마지막에 반드시 `ScheduleWakeup`으로 다음 실행을 예약한다(prompt에 현재 args echo). `/loop`이 이 예약을 받아 다음 tick을 발화시킨다.
- **지속**: 예약된 wake가 발화하면 `/jarvis [args]`가 다시 실행되고, 또 다음 wake를 예약한다. 이렇게 사용자가 추가 입력 없이도 루프가 유지된다.
- **불변 규칙**: 종료 의사(아래 "중지")가 없는 한, **모든 tick은 끝에서 반드시 `ScheduleWakeup`을 호출한다.** 이 호출을 빠뜨리면 다음 wake가 예약되지 않아 루프가 죽는다.
- **맨 `/jarvis`(=`/loop` 없이)로 띄운 경우**: 스킬은 자신이 `/loop` 안인지 밖인지 런타임에 구분할 수 없다. 그래서 이번 1회 tick은 정상 수행하되, 최초 부팅 tick 출력 끝에 **"`/loop` 없이 띄웠다면 이 tick 뒤 멈춘다 — 지속 감시는 `/loop /jarvis`로 다시 띄워라"** 안내를 남긴다(절차 0.7). `/loop` 위였다면 그대로 반복되고, 아니었다면 안내대로 여기서 멈춘다.

## 인자 (args, key=value)

| key | 의미 | 기본값 |
|-----|------|--------|
| `strength` | **강도 프리셋.** 폴링 간격 노브들을 한 번에 묶어 세팅한다(`low`/`medium`/`high`). 개별 노브를 같이 주면 그 항목만 덮어쓴다. 아래 "강도 프리셋" 참조. | `medium` |
| `active` | 직전 wake에서 `jarvis-once`를 실행했거나 워킹트리에 변경이 있을 때의 다음 wake 간격 | `4m` |
| `idle` | 변경이 없어 잠잠할 때(워킹트리 깨끗)의 다음 wake 간격 | `25m` |
| `debounce` | **대화가 멎었다고 볼 정지 시간.** 리뷰할 조건이 됐어도 사람이 대화 중이면 실행을 미루고 이 간격으로 짧게 재예약한다. 사람이 한 마디 할 때마다 타이머가 리셋된다. | `90s` |
| `warmup` | **첫 로드 빠른 폴링 tick 수.** 부팅 직후 이 횟수만큼은 변경이 없어도 `idle` 대신 `active` 간격으로 재확인한다(처음 켰을 때 반응을 빠르게). `0`이면 끔. | `3` |
| `paths` | 감시 대상 경로 한정 (생략 시 전체) | (전체) |
| `risk` | **위험 경로** glob — 여기에 매칭되는 파일은 분량과 무관하게(단 한 줄이라도 새로 바뀌면) `jarvis-once`를 깨운다. 쉼표로 여러 개. | (없음/off) |
| `focus` | **집중 영역 디렉토리.** 여기 모인 `.md`를 리뷰 시 우선 렌즈로 본다(아래 "컨벤션 문서 수집" 4번). | `.claude/jarvis/focus/` |
| `mirror` | **거울(gray zone 가시화).** 누적 변경의 상당 부분이 이 세션에서 *생성된* 코드면 "직접 파악했는지" 한 줄 메모로 짚는다(비강제). `off`로 끔. 아래 절차 3.5 참조. | `on` |
| `plan` | **계획 모드.** 첫 부팅에서 이 작업의 계획+체크리스트를 만들지 물어본다(절차 0.55). `off`면 질문을 건너뛴다(지금과 완전히 동일 동작). 소스(`plan=PROJ-123`, URL, 파일 경로)를 주면 옵트인 *과 동시에* 소스를 지정해 두 질문을 모두 건너뛴다. 계획이 생기면(`.jarvis/checklist.md` 존재) 워치가 게이트가 걸리는 tick마다 그것을 기준으로 리뷰한다. | (첫 부팅에 질문) |

> **커밋 경계 트리거는 args와 무관하게 항상 켜져 있다.** 새 커밋이 감지되면 변경 누적과 무관하게 그 커밋 변경에 대해 `jarvis-once`를 1회 실행한다. 착오가 코드로 봉인되기 직전/직후가 경고의 골든타임이기 때문이다. (manifesto: "사람의 착오에는 AI가 적극적으로 경고")

예시:

```
/loop /jarvis                                         # args 없음 → 최초 1회 강도를 물어봄 (이후 medium 기본)
/loop /jarvis strength=high                            # 강하게 — 촘촘히 폴링 (새 변경을 빨리 잡음)
/loop /jarvis strength=low                             # 약하게 — 드물게 폴링
/loop /jarvis strength=high idle=30m                   # 강 프리셋 + idle만 30m으로 덮어쓰기
/loop /jarvis paths=src/billing active=3m              # 특정 경로만, 더 촘촘히
/loop /jarvis risk=**/*payment*,**/*auth*              # 결제·인증은 한 줄만 바뀌어도 즉시 경고
```

> 진입은 항상 `/loop /jarvis`다(`/loop` 없이는 반복 안 됨, 위 "실행" 참조). ScheduleWakeup의 echo prompt에는 `/loop` 접두어 없이 `/jarvis [args]`만 넣는다 — 다음 tick은 `/loop`이 그 prompt로 발화시킨다(절차 4).

인자 파싱 규칙:
- `key=value` 형태만 인식한다. 인식 못 한 토큰은 무시하고 기본값을 쓴다.
- `strength`를 먼저 해석해 프리셋 노브 묶음을 깐 뒤, 나머지 개별 key=value를 그 위에 덮어쓴다(개별 노브 우선). `strength` 미지정 시 `medium`과 동일.
- `strength` 값은 별칭을 허용한다(아래 "강도 프리셋" 표). 인식 못 한 값이면 `medium`으로 폴백한다.
- 시간 간격은 `s`/`m`/`h` 접미사를 허용한다(`90s`, `4m`, `1h`). 숫자만 오면 분으로 간주한다.
- `active`/`idle`은 런타임에서 [60s, 3600s]로 클램프된다.
- `paths`/`risk`는 쉼표(`,`)로 여러 값을 구분한다. glob 패턴을 허용한다.

## 강도 프리셋 (strength)

`strength` 하나로 "얼마나 촘촘히 폴링할지"를 묶어 조절한다. 각 프리셋은 아래 노브 묶음으로 전개되며, 같은 호출에 개별 노브(`active=` 등)가 있으면 **그 항목만** 프리셋 값을 덮어쓴다. (라인/파일 임계값은 없으므로 프리셋은 *분량 민감도*가 아니라 *폴링 빈도*만 바꾼다.)

| `strength` | 별칭 | `active` | `idle` | `debounce` | 성격 |
|-----------|------|----------|--------|------------|------|
| `low` | `약`, `약하게`, `느슨`, `relaxed`, `1` | `8m` | `40m` | `120s` | 드물게 폴링. 소음 최소·비용 최소 |
| `medium` | `중`, `보통`, `normal`, `2` | `4m` | `25m` | `90s` | 기본. 균형 |
| `high` | `강`, `강하게`, `촘촘`, `aggressive`, `3` | `3m` | `12m` | `60s` | 촘촘히 폴링. 새 변경·커밋을 가장 빨리 잡음 |

규칙:
- 프리셋은 위 3개 노브(`active`/`idle`/`debounce`)만 건드린다. `paths`/`risk`는 프리셋과 무관하게 별도로 지정한다.
- `strength=high`라도 `jarvis-once` 자체의 severity 문턱은 그대로다 — 강도는 *폴링 빈도*(=새 변경을 잡는 속도)를 높일 뿐 잔소리를 늘리지 않는다(비용 가이드 참조). 즉 안심하고 올려도 된다.
- 다음 wake 예약 시 echo하는 args에는 **전개된 개별 노브가 아니라 `strength=<값>`(+ 개별 덮어쓰기)을 그대로** 직렬화한다. 그래야 프리셋 의미가 보존된다.

## 마커 파일

직전 리뷰 시점의 기준선을 `.jarvis/baseline`에 저장한다. 워킹 트리에 있으므로 `.gitignore`에 `.jarvis/`를 등록해 커밋되지 않게 하고(클론마다 독립적인 로컬 상태로 동작), 디렉토리가 없으면 쓰기 전에 `mkdir -p .jarvis`로 생성한다.

> **`.git/`을 쓰지 않는 이유:** `.git/` 내부는 민감 경로라 쓰기마다 권한 승인을 받아야 해서 무인 루프에 부적합하다. `.jarvis/`는 일반 워킹 트리 경로라 권한 마찰이 없고, `.gitignore`로 비추적을 보장하면 "커밋 안 됨 + 로컬 전용"이라는 원래 이점을 그대로 유지한다.

형식(한 줄): `lines=<정수> risk=<정수> head=<커밋 SHA> deferred=<0|1> boot=<정수> mirrored=<0|1>`
파일이 없으면 `lines=0 risk=0 head= deferred=0 boot=0 mirrored=0`으로 간주한다. (구버전 파일에 `boot`·`mirrored`가 없으면 0으로 보고, `files` 필드가 남아 있으면 무시한다.)
- `lines`: 직전 리뷰 시점의 working tree 변경 라인 수. "직전 리뷰 이후 새 변경이 쌓였나"를 판정하는 기준선이다.
- `risk`: 직전 리뷰 시점의 위험 경로(`risk` glob) 변경 라인 수 (risk 미설정 시 0)
- `head`: **직전 tick에서 관측한** `git rev-parse HEAD` 값. 커밋 경계 감지에 쓴다.
- `deferred`: 리뷰할 조건이 됐지만 대화 중이라 **미뤄둔 리뷰가 있는지**(debounce 대기). 1이면 대화가 멎는 순간 flush한다.
- `boot`: 남은 **웜업 tick 수.** 부팅 시 `warmup`으로 초기화되고 매 tick 1씩 줄어든다. `>0`이면 변경이 없는 tick도 `idle` 대신 `active` 간격으로 폴링한다(첫 로드 직후 빠른 반응).
- `mirrored`: **거울 쿨다운 플래그.** 거울(절차 3.5)을 띄운 뒤 1로 둬 매 tick 반복 발화를 막는다. 사람이 직접 타이핑한 변경이 다시 주를 이루거나 리뷰를 flush하면 0으로 풀린다.

### 제어 상태 파일 (`.jarvis/` 하위)

워치의 진행 상태는 아래 2개 파일로 제어된다. 둘 다 `.jarvis/` 하위라 `.gitignore`로 비추적·로컬 전용이고, **각각 한 줄짜리 고정 크기 상태 파일이라 매 tick 덮어쓰기만 된다(누적 캐시가 아니다).**

| 파일 | 역할 | 생성/삭제 주체 |
|------|------|----------------|
| `.jarvis/baseline` | 위 형식의 워치 기준선. 루프 진행 상태의 핵심. 디스크에 남아 있으면 다음 `/loop /jarvis`가 그 지점에서 이어서 감시한다(=재개). | 매 tick 기록 / `/jarvis-reset`이 삭제 |
| `.jarvis/args` | 직전 tick의 유효 args 문자열(예: `strength=medium`). 매 tick 갱신. 다음 시작이 **args 없이** 호출되면 jarvis가 이 값을 읽어 같은 설정으로 자동 재개한다(절차 0.4). 없으면 기본값(medium). | 매 tick 기록 / `/jarvis-reset`이 삭제 |
| `.jarvis/status` | **생존 신호용 상태 한 줄**(아래 "생존 가시화"). 매 tick 끝에서 다음 wake 시각(`next_wake` epoch)·간격·강도를 기록한다. statusline 스크립트가 이 파일을 읽어 tick **사이에도** "감시 중 / 멈춤?"을 연속 표시한다. | 매 tick 기록 / `/jarvis-reset`이 삭제 |
| `.jarvis/stopped` | **이벤트 기반 "멈춤" 플래그**(아래 "생존 가시화 (B)"). Stop 훅(`assets/loop-watch-hook.sh`)이 턴 종료 시 `/jarvis` wake가 사라진 걸 감지하면 남긴다. 있으면 statusline이 시간 추론 없이 **즉시** "멈춤"을 표시. wake가 살아있으면 훅이 지운다. | Stop 훅이 기록/삭제 / `/jarvis-reset`이 삭제 |
| `.jarvis/plan.md` | **승인된 계획 문서**(목표/스코프/접근/열린 질문). 사람이 승인한 뒤 `jarvis-plan`이 1회 기록. 이 파일 + `checklist.md`가 있으면 **계획 모드 활성.** 지속 파일(매 tick 한 줄짜리가 아님). | 옵트인 시 `jarvis-plan`이 기록 / `/jarvis-reset`이 삭제(확인 후) |
| `.jarvis/checklist.md` | **작업 체크리스트** — 마크다운 `- [ ]`/`- [x]` 항목. **체크마크는 사람이 소유**하고, 워치는 게이트 리뷰마다 이 파일을 읽어 공식적으로 뭐가 됐는지 알고 나머지를 재평가한다. 진행률 = 체크됨/전체. 이 파일의 존재가 워치의 "계획 모드 활성" 판정 키다. | `jarvis-plan`이 생성, 사람이 체크 / `/jarvis-reset`이 삭제(확인 후) |

> **생애주기(`/loop` 위):** 시작·재개는 `/loop /jarvis` — baseline/args가 남아 있으면 그 상태에서 이어진다. 멈춤·일시정지는 `/loop` 자체를 인터럽트(Esc) — 다음 wake가 예약되지 않아 루프가 끝나고, baseline/args는 디스크에 그대로 남아 재개를 기다린다. 완전 초기화는 **`/jarvis-reset`**(독립 스킬: baseline/args 삭제 → 다음 시작은 최초 부팅). 루프 종료엔 teardown 훅이 없으므로 상태 정리는 시작 시점(자가보정)과 `/jarvis-reset`에서만 일어난다. (구버전 `.jarvis/paused` 플래그·`/jarvis-pause`·`/jarvis-resume`·`/jarvis-stop`은 더 이상 쓰지 않는다.)

## 컨벤션 문서 수집 (`jarvis-once` 호출 직전에만 수행)

`jarvis-once`를 실제로 부르기로 결정한 순간(절차 2a 또는 3 충족)에만 수행한다. 리뷰하지 않는 tick에서는 토큰 낭비이므로 **하지 않는다.**

목적: `jarvis-once`가 "이 패키지·이 디렉토리 규칙"까지 알고 리뷰하게 한다. `CLAUDE.md`와 `.claude/rules/**`는 하네스가 자동 주입하므로 **중복 수집하지 않는다.** on-demand 문서만 모은다.

변경된 파일 목록을 먼저 얻는다:

```bash
git diff --name-only HEAD [-- paths]      # 게이트로 깨운 경우 (working tree)
git diff --name-only <base_head>..<cur_head>   # 커밋 경계로 깨운 경우
```

그 경로들을 기준으로 다음을 수집한다(존재하는 것만, **이미 컨텍스트에 있으면 재읽기 금지**):

0. **작업 계획 & 체크리스트 (계획 모드 활성 — `.jarvis/checklist.md` 존재 시에만)** — `.jarvis/plan.md`·`.jarvis/checklist.md`를 읽어 `jarvis-once`에 **"작업 스펙(최우선)"**으로 넘긴다. 이건 변경이 *무엇을 이루려 하는가*이므로 집중 영역보다도 우선한다: jarvis-once가 변경을 체크리스트에 대고 리뷰한다(어느 항목을 전진시키나, 완료로 보이나, 항목별로 뭐가 빠졌거나 위험한가). 절차 3.6 참조.
1. **가장 가까운 `AGENTS.md`** — 각 변경 파일의 디렉토리에서 위로 올라가며 처음 만나는 `AGENTS.md`. (예: `packages/billing/**` 변경 → `packages/billing/AGENTS.md`)
2. **디렉토리 `README.md`** — 변경 파일이 위치한 디렉토리에 `README.md`가 있으면 그 파일.
3. **변경 파일에 해당하는 `.claude/rules/**` 규칙 문서** — 변경 파일의 종류·경로에 맞는 규칙만 추려서(전부 말고) 참조한다. 프로젝트가 `.claude/rules/`를 어떤 축으로 조직했든(언어별·레이어별·기능별·디렉토리별) 변경된 파일과 가장 관련된 1~3개만 고른다. 규칙 파일명·디렉토리명이 곧 적용 힌트다(예: UI 파일을 바꿨으면 `ui`·`view` 류, 테스트를 바꿨으면 `test` 류, 결제를 바꿨으면 `payment`·`billing` 류). 하드코딩된 언어별 매핑에 기대지 말고 **그 프로젝트가 실제로 가진 규칙 파일에서 발견**한다. 이미 자동 주입된 규칙은 생략한다.
4. **집중 영역 문서 (`focus` 디렉토리, 기본 `.claude/jarvis/focus/**`)** — 사용자가 "이 프로젝트에서 특히 주의 깊게 리뷰받고 싶은 것"을 모아둔 곳. 존재하면 그 안의 `.md`(README 제외)를 모아 `jarvis-once`에 **"집중 영역"** 맥락으로 넘긴다. 위 1~3의 일반 컨벤션과 달리 이건 **우선순위 렌즈**다 — jarvis-once가 일반 감지 카탈로그보다 먼저 본다. `focus=<경로>` 인자로 위치를 바꿀 수 있다. (이 디렉토리는 변경 파일과 무관하게, 리뷰를 실제로 하기로 한 tick에서 항상 수집한다.)

중복·과수집을 피한다: 같은 `AGENTS.md`를 여러 변경 파일이 공유하면 한 번만 읽는다. 수집량이 과하면 변경 파일이 가장 많은 상위 디렉토리 1~2곳으로 한정한다.

수집한 내용을 `jarvis-once` 호출 시 함께 전달한다 — 0은 **"작업 스펙(최우선)"**, 1~3은 **"참고 컨벤션"**, 4는 **"집중 영역(우선)"** 으로 구분해 넘긴다. (페르소나(`persona.md`)는 `jarvis-once`가 자기 디렉토리에서 직접 읽으므로 워치가 수집하지 않는다.)

## Jarvis 출력 마커 (필수)

`jarvis-once` 리뷰 결과를 사용자에게 전달할 때는, 그 내용이 **Jarvis가 자동 생성한 것**임을 보이도록 반드시 시작/끝에 아래 마커로 감싼다. 워치가 자동으로 내놓은 출력과 일반 대화를 구분하기 위함이다.

**시작 마커:**

```
╭─🤖 JARVIS ─────────────── (jarvis 자동 관찰)
```

**끝 마커:**

```
╰─🤖 JARVIS ─────────────── 키보드는 당신이 잡습니다 · 판단은 당신 몫
```

규칙:
- `jarvis-once`가 실제로 무언가 말할 때만(리뷰 내용이 있을 때) 감싼다. "특별히 걸리는 건 없어" 수준의 침묵·"새 변경 없음" 한 줄 알림에는 마커를 붙이지 않는다.
- 마커 사이 본문은 `jarvis-once`가 생성한 내용 그대로 둔다. 워치(`jarvis`) 자신의 운영 메시지(예약·debounce 안내 등)는 마커 **밖**에 둔다.
- 끝 마커의 꼬리 문구는 저자성이 사람에게 있음을 상기시키는 고정 문구다.

## 시작 배너 (최초 tick 전용)

`/jarvis`가 **처음 가동되는 tick**에서만 `JARVIS` 아스키 로고 배너를 **1회** 출력한다. 판정 기준: `.jarvis/baseline` 파일이 **아직 없으면** 최초 부팅 tick이다(이후 tick엔 baseline이 생기므로 자동으로 재출력 안 됨). 예약 wake·이후 tick에서는 출력하지 않는다 — 반복은 노이즈다.

**항상 보이게 — 반드시 "어시스턴트 응답 본문"에 코드펜스로 직접 출력한다.**
`cat`으로만 내보내면 Claude Code UI가 긴 tool 출력을 접어버려(Ctrl+O 필요) 배너가 바로 안 보인다. 따라서:
1. `assets/jarvis-banner.txt`(이미 컨텍스트에 있으면 재읽기 불필요)를 읽어 내용을 확보하고,
2. 그 내용을 **응답 메시지 안의 삼중 백틱(```) 코드블록에 그대로 붙여** 출력한다. (tool 출력이 아니라 본문이라 항상 펼쳐져 보인다)

- 색: 본문 마크다운은 ANSI 색을 못 살리므로 **모노크롬**으로 나간다. 이 로고는 블록 글자(`█`)와 박스 모서리(`╗╝╚╔║═`)로 `JARVIS` 형태가 또렷이 드러난다. (굳이 컬러가 필요하면 `assets/jarvis-banner.ansi`를 **raw 터미널**에서 `cat` — 단 Claude Code UI에선 접힘.)
- 원본 아트: `assets/jarvis-banner.txt`. (`colorize.sh` → `.ansi`는 raw 터미널용 컬러 fallback으로만 유지)
- 배너는 워치 운영 메시지이므로 "Jarvis 출력 마커"(╭─🤖) **밖**에 둔다. 배너 아래 캡션 한 줄을 덧붙인다:
  `J · A · R · V · I · S  —  watch online · 키보드는 당신이 잡습니다`

## 매 실행(wake) 절차

> 이 스킬은 매 wake마다 아래를 처음부터 끝까지 수행한다.

### 0. 사람 우선 + 대화 활성도 판정 (debounce)
**`active_chat` 판정:** 직전 tick(직전 `ScheduleWakeup` 발화) 이후 사람이 보낸 메시지가 있는가? transcript 끝부분으로 판정한다.
- 사람의 의논/구현 메시지가 있었으면 → `active_chat = true` (대화 중)
- 이번 tick이 순수 예약 발화뿐이면 → `active_chat = false` (조용)

`active_chat == true`이고 사람이 무언가 요청 중이면, **그 요청(질문 답변·코드 작성·명령 실행)에 먼저 집중한다.** 워치 출력으로 대화를 끊지 않는다. 리뷰는 미루고, 절차 3·2a의 debounce 분기가 처리한다(절차 4에서 `debounce` 간격으로 재예약).

이 `active_chat` 값은 절차 2a·3의 "말해도 되는가" 판단에 쓰인다.

### 0.4. 저장된 설정 자동 복원 (재개 시)
이번 호출에 **인식된 args가 하나도 없고** `.jarvis/args` 파일이 존재하면, 그 한 줄을 읽어 이번 tick의 유효 args로 삼는다(이전 설정으로 자동 재개). 이로써 루프를 인터럽트(Esc)로 멈춘 뒤 `/loop /jarvis`(인자 없이)로 다시 띄워도 직전 `strength` 등이 그대로 복원된다 — 별도 resume 명령이 필요 없다.

```bash
cat .jarvis/args 2>/dev/null || true
```

- 명시적으로 준 args가 하나라도 있으면 그쪽이 우선이고 `.jarvis/args`는 읽지 않는다(**명시 > 저장 > 기본 medium**).
- 예약 wake(자동 발화) tick은 args가 항상 echo되므로 이 분기에 들어오지 않는다.
- `.jarvis/args`도 없으면 기본값(medium)으로 둔다. (복원했든 안 했든, 이렇게 정해진 유효 args는 이후 0.6·절차 4가 그대로 쓴다.)

### 0.5. 시작 배너 (최초 부팅 1회)
`.jarvis/baseline` 파일이 **없으면** 이번이 최초 가동 tick이다 → "시작 배너" 섹션 규칙대로 `JARVIS` 아스키 로고를 **응답 본문 코드펜스에** 1회 출력한다(마커 밖, 캡션 포함, 항상 보임). 파일이 이미 있으면 건너뛴다. 배너 출력 후에도 절차 1~4는 정상 진행한다.

### 0.55. 계획 옵트인 (최초 부팅 + 인터랙티브일 때만 1회)
**조건:** 이번이 최초 가동 tick(`0.5`에서 baseline 없음 판정)이고 **인터랙티브 시작(예약 자동 wake가 아님)일 때만** 수행한다. 강도(0.6)와 같은 가드: **예약 자동 발화 tick에서는 절대 묻지 않는다** — 자리를 비운 사이 질문이 루프를 막는다.

- **`plan=off`** → 계획을 완전히 건너뛴다. 루프는 **이 기능이 없을 때와 완전히 동일하게**(as-is) 동작한다. plan/checklist 파일도, plan-review도 없다.
- **`plan=<소스>`**(Jira 키·URL·파일 경로) → 소스까지 지정된 옵트인으로 본다. 곧장 `jarvis-plan`에 넘긴다(예/아니오 질문 건너뜀).
- **그 외엔 1회 묻는다** — `AskUserQuestion`: *"이 작업의 계획+체크리스트를 만들까요?"* — 선택지 **"예, 계획 만들기"** / **"아니오, 그냥 감시."**
  - **아니오** → 계획 없이 as-is로 진행. 여기서 더 할 일 없음.
  - **예** → `Skill('jarvis-plan')`을 호출한다. 소스 선택(Jira / Confluence / Notion / 문서 / 직접 작성) → 읽기 → `plan.md`·`checklist.md` **초안** → 사람 **승인** → `.jarvis/`에 기록까지 처리한다. 돌아오면 0.6으로 이어간다.
- **순서:** 이건 강도(0.6) **앞**이다 — *무엇을 하는지*를 정하고 *얼마나 촘촘히 볼지*를 정한다.
- **첫 부팅 한정.** 재개(baseline 존재) 시 다시 묻지 않는다. `.jarvis/checklist.md`가 있으면 계획 모드가 그냥 활성이고 워치가 그걸 기준으로 리뷰한다. 나중에 (다시) 계획하려면: `/jarvis-reset` 후 재시작, 또는 `/loop /jarvis plan=<소스>`.

### 0.6. 강도 선택 (최초 부팅 + args 없을 때만 1회)
**조건:** 이번이 최초 가동 tick(`0.5`에서 baseline 없음 판정)이고 **인식된 args가 하나도 없을 때만** 수행한다.
- `AskUserQuestion`으로 강도를 1회 묻는다. 선택지는 `강하게(high)` / `보통(medium)` / `약하게(low)` 3개 + 각 프리셋의 노브 요약을 description에 적는다. (사용자는 "Other"로 직접 값을 줄 수도 있다.)
- 사용자가 고른 값을 이번 tick의 `strength`로 확정하고, 절차 4의 wake 예약 prompt에 `strength=<선택값>`을 echo한다. 이후 wake부터는 args가 비어있지 않으므로 다시 묻지 않는다.
- **예약 wake(자동 발화) tick에서는 절대 묻지 않는다** — args(`strength=` 포함)가 항상 echo되므로 이 분기에 들어오지 않는다. 사용자가 자리를 비운 사이 질문으로 루프가 막히는 일을 방지한다.
- args가 하나라도 있으면(예: `/loop /jarvis strength=high`, `/loop /jarvis idle=30m`) 질문 없이 그 값을 그대로 쓴다.

> 이 질문은 "처음 켤 때 한 번"만이다. 강도를 나중에 바꾸려면 `/loop /jarvis strength=<값>`으로 다시 부르면 된다(진행 중인 예약을 덮어쓴다).

### 0.7. `/loop` 안내 (최초 부팅 1회 — 맨 호출 대비)
**조건:** 이번이 최초 가동 tick(`0.5`에서 baseline 없음 판정)일 때만 수행한다. (예약 wake·이후 tick에서는 출력하지 않는다.)
- 스킬은 자신이 `/loop` 안에서 도는지 맨 `/jarvis`로 띄워졌는지 런타임에 구분할 수 없다. 그래서 최초 부팅 tick에서는 항상 마커 **밖**에 안내 한 줄을 남긴다:

  ```
  ↻ 지속 감시는 /loop /jarvis 로 띄워야 반복됩니다. /loop 없이 띄웠다면 이 1회 tick 뒤 멈춥니다.
  ```

- 이 안내는 정보용이다. `/loop` 위에서 돌고 있었다면 절차 4의 `ScheduleWakeup`이 정상 동작해 그대로 반복되고(안내는 무해), 맨 호출이었다면 `ScheduleWakeup`이 조용히 무시돼 안내대로 이번 tick 뒤 멈춘다.
- 절차 1~4는 평소대로 진행한다(이번 1회 tick은 정상 수행).

### 1. 측정 (저비용)
`paths`가 있으면 `-- <paths>`를 붙여서 working tree 변경량을 잰다. **추적 파일 변경**과 **미추적(새로 생성된) 파일**을 둘 다 센다:

```bash
git diff --shortstat HEAD -- [paths]                 # ① 추적 파일 변경
git ls-files --others --exclude-standard -- [paths]  # ② 미추적(새) 파일 목록
```

- ①에서 `insertions(+)`, `deletions(-)`를 파싱한다.
- ②의 각 파일 라인 수(`wc -l`)를 더한다.
- `cur_lines = (① insertions + deletions) + (② 새 파일들의 총 라인 수)`
- 비어 있으면 0.

> ⚠️ **왜 ②가 필수인가:** `git diff HEAD`는 **미추적 파일을 포함하지 않는다.** 이게 빠지면 사람이 **새 파일을 손으로 짤 때**(이 프로젝트의 핵심 사용 사례) jarvis가 stage/commit 전까지 0으로 보고 침묵한다. `git add -N`(intent-to-add)로 인덱스에 끌어들이는 방법도 있으나, **인덱스를 변조해 무인 루프에 부작용**을 주므로 쓰지 않는다 — 읽기 전용 `ls-files`로 따로 세어 더한다.

`risk`가 설정돼 있으면 위험 경로만 따로(추적+미추적 동일 방식으로) 잰다:

```bash
git diff --shortstat HEAD -- <risk globs>
git ls-files --others --exclude-standard -- <risk globs>
```
→ `risk_lines = (추적 ins+del) + (미추적 새 파일 라인 수)` (위험 경로 기준). risk 미설정 시 0.

현재 커밋도 확인한다:

```bash
git rev-parse HEAD
```
→ `cur_head`.

> 측정은 staged·unstaged·**미추적**을 모두 포함하는 working tree 기준(`HEAD` 대비)이다.

### 2. 경계 판단 (커밋·되돌림 자동 보정)
`.jarvis/baseline`에서 `base_lines`, `base_risk`, `base_head`를 읽는다.

**(0) stale baseline 자가보정 (재개 위생 — 가벼운 1회 체크):**
루프를 인터럽트(Esc)로 멈춘 뒤 밖에서 rebase·reset·브랜치 삭제 등을 하면, `base_head`가 **레포에 더는 존재하지 않는 SHA**가 될 수 있다. `base_head`가 비어있지 않을 때 그 존재 여부를 1회 확인한다:

```bash
git cat-file -e <base_head>^{commit} 2>/dev/null   # 존재하면 exit 0
```

→ **존재하지 않으면**(exit 0 아님) 직전 기준선이 의미를 잃은 것이다. 이번 tick을 최초 부팅처럼 다루지 말고(배너 재출력 X), 조용히 baseline을 **현재 측정값으로 리셋**한다(`lines=cur_lines risk=risk_lines head=cur_head deferred=0`, `boot`/`mirrored`는 보존). `jarvis-once`는 실행하지 않고 절차 4로 간다. (커밋 경계·되돌림 보정은 head가 유효할 때만 의미가 있으므로, 무효 head로 (a)·(b)를 돌리지 않기 위해 먼저 친다.) `base_head`가 비어있으면 이 체크는 건너뛴다.

**(a) 커밋 경계 — 강제 관찰 (항상 켜짐):**
`base_head`가 비어있지 않고 `cur_head != base_head`이면, 직전 tick 이후 **새 커밋이 생겼다**(commit/merge). 분량과 무관하게 `jarvis-once`로 1회 점검한다.
- **단, `active_chat`이면(대화 중) 이 커밋 점검도 미룬다:** `deferred = 1`로 두고 **`base_head`를 갱신하지 않은 채** 절차 4에서 `debounce` 간격으로 재예약한다. 조용해지면 다음 tick에서 이 분기로 다시 들어와 실행한다. (커밋 점검이 유실되지 않도록 head를 일부러 안 옮긴다)
- 조용하면(`active_chat == false`) 바로 실행:
  - 보여줄 diff: `base_head`가 `cur_head`의 조상이면 `git diff <base_head>..<cur_head>`, 아니면(rebase/checkout/force 등) `git show <cur_head>`
  - 먼저 "컨벤션 문서 수집"을 수행해 함께 넘긴다.
  - `jarvis-once`에 "막 커밋된 변경이다. 봉인 직전 마지막 점검 관점으로 착오·누락을 봐달라"는 맥락을 전달한다.
  - 리뷰 결과를 **"Jarvis 출력 마커"로 감싸** 전달한다.
  - 실행 후 절차 3(게이트)은 **건너뛴다.** 기준선을 현재값으로 갱신하고 `deferred=0`으로 절차 4로 간다.
- 단, 사용자가 종료를 요청한 상태면 실행하지 않는다.

**(b) 되돌림(discard) 감지:**
`cur_head == base_head`인데 `cur_lines < base_lines`이면, 사용자가 변경을 되돌린 것이다. 기준선을 현재값으로 리셋하고 `jarvis-once`는 실행하지 않는다. (절차 4로)

**(c) 그 외 — 증가분 계산:**
- `delta_lines = cur_lines - base_lines` (직전 리뷰 이후 새로 쌓인 라인 수; 양수면 새 변경 있음)
- `delta_risk  = risk_lines - base_risk` (risk 미설정 시 0)

### 3. 게이트 + debounce 판단

**게이트 충족 여부** — 다음 중 하나라도 충족하면 `gate_met = true`:
- `delta_lines >= 1` — 직전 리뷰 이후 **새 변경이 쌓였으면** 리뷰한다(고정 분량 임계 없음). 이미 리뷰한 변경은 절차 끝에서 `base_lines`로 흡수되므로 같은 변경을 다시 발동하지 않는다.
- `risk` 설정 시 `delta_risk >= 1` — 위험 경로는 분량 무관. 단 한 줄이라도 새로 바뀌면 경고. (tenet 7: 위험에 반응)

**리뷰 필요 여부**: `should_review = gate_met OR (base_deferred == 1)`
→ 이전에 미뤄둔 리뷰가 있으면 게이트가 다시 충족되지 않아도 리뷰 대상이다(미뤄둔 변경은 사라지지 않는다).

**말해도 되는가**: `may_speak_now = (active_chat == false)` — 대화가 멎은 상태.

분기:

- **should_review && may_speak_now → 실행 (flush):**
  1. "컨벤션 문서 수집"을 수행한다.
  2. `Skill('jarvis-once')`를 호출해 현재 변경분(working tree diff)을 리뷰받는다. 수집한 참고 컨벤션 + "직전 리뷰 이후 새로 쌓인 변경 위주로 봐달라" 맥락을 함께 전달한다. 위험 경로/미뤄둔 리뷰 때문이면 그 사실을 명시한다.
  3. 리뷰 결과를 **"Jarvis 출력 마커"로 감싸** 사용자에게 간결히 전달한다.
  4. `deferred = 0`으로 클리어.

- **should_review && !may_speak_now → 미룸 (debounce):**
  - `jarvis-once`를 실행하지 않는다. `deferred = 1`로 표시.
  - 워치 운영 메시지를 마커 **밖**에 한 줄로 남긴다(예: "변경 감지 — 대화 중이라 보류, 멎으면 리뷰할게").
  - 절차 4에서 `debounce` 간격으로 짧게 재예약한다.

- **그 외 (should_review == false):** 새로 쌓인 변경이 없는 경우다. 침묵하지 말고 **하트비트 한 줄**(아래 "생존 가시화 (A)")을 마커 밖에 남긴다 — 단 대화 중(`active_chat == true`)이면 생략한다(statusline이 메운다).

**기준선 기록 규칙 (절차 끝에서 항상 적용):**
- `head`: 매 tick 끝에 `cur_head`로 기록한다. **단, 커밋 경계(2a)를 debounce로 미룬 경우는 예외** — 다음 조용한 tick에서 다시 감지되도록 `head`를 갱신하지 않는다.
- `lines` / `risk`: **`jarvis-once`를 실행(flush)했거나 되돌림 리셋(2b)한 경우에만** 현재값(`cur_lines`/`risk_lines`)으로 갱신한다. 갱신하면 그 변경이 base로 흡수돼 다음 tick부터는 "새 변경"으로 잡히지 않는다(같은 변경 반복 리뷰 방지). 미룸·미충족 tick에서는 기존 값을 유지해 변경이 계속 누적되게 둔다.
- `deferred`: 위 분기 결과(0/1)를 기록한다.
- `boot`: `boot_now`에서 1 줄여 기록한다(최소 0). 즉 부팅 후 `warmup` tick 동안만 웜업 폴링이 유지되고, 그 뒤 자동으로 `idle`로 내려간다. `warmup=0`이면 처음부터 웜업 없음.
- `mirrored`: 절차 3.5 결과(0/1)를 기록한다. 거울을 띄웠으면 1, 풀림 조건(사람 직접 타이핑이 주를 이룸 · 리뷰 flush · 되돌림 리셋)이면 0.

### 3.5. 거울 — gray zone 가시화 (비강제)
저자성 보존을 위한 보조 장치다. **코드를 막지도 고치지도 않는다** — 사람이 자기도 모르게 조종석에서 일어나려 할 때 거울만 비춘다. `mirror=off`면 이 절차 전체를 건너뛴다(`mirrored`는 0으로 유지).

**신호 (싸게 — transcript+diff만, `jarvis-once` 호출 없음):** 직전 tick 이후 쌓인 변경이 *어떻게* 만들어졌는지 본다.
- 이 세션 transcript에서 어시스턴트의 `Edit`/`Write`/`NotebookEdit` 호출이 변경 파일을 직접 만들었으면 → **AI 생성분.**
- 그런 도구 호출 없이 diff에만 나타난 변경 → **사람이 직접 타이핑.**
- severity 게이트와 **독립**이다 — 생성 코드가 깔끔해 `jarvis-once`가 침묵해도 저자성 신호는 따로 뜬다.

**발화 조건 (모두 충족):** ① 누적 변경의 상당 부분이 AI 생성(대략 과반) · ② 절대량이 사소하지 않음(한두 줄 수정 수준이 아님) · ③ `base_mirrored == 0`(아직 안 띄움). 충족 시 마커 **밖**에 건조한 메모 한 줄을 남기고 `mirrored=1`로 기록한다:

```
🪞 이번 변경의 상당 부분이 이 세션에서 생성된 코드로 보여 — 네 이름으로 커밋될 텐데 직접 파악했는지 확인 필요.
```

**풀림(쿨다운 해제):** 이후 tick에서 **사람이 직접 타이핑한 변경이 다시 주를 이루거나**, 리뷰를 flush했거나, 되돌림 리셋(2b)이면 `mirrored=0`으로 되돌려 다음 생성 버스트에 다시 뜰 수 있게 한다.

**register · 한계:**
- 설교·비난·강요가 아니다. **짚고 비킨다** — `jarvis-once`의 "떠먹이지도 떠보지도 않는다"와 같은 건조한 메모 register.
- **보이는 범위에서만.** 이 세션 transcript만 본다 — 다른 터미널/세션 생성이나 외부 붙여넣기는 못 본다. 그래서 단정("~다")하지 않고 "~로 보여"로 짚고, 추궁하지 않는다.
- 끄려면 `mirror=off`. 사람이 거울을 원치 않으면 그 선택도 존중한다 — 거울조차 비강제다. (리트머스 ①: 강요는 울트론, 거울은 자비스)

### 3.6. 계획 리뷰 & 완료 (계획 모드 활성일 때만)
`.jarvis/checklist.md`가 없으면 이 절차 전체를 건너뛴다. 있으면 체크리스트가 워치가 기준으로 navigate 하는 스펙이다.

**리뷰당 체크리스트 평가 (게이트에 얹힘 — 추가 비용 없음):** 이건 리뷰를 실제로 flush한 tick(절차 3의 실행 분기, 또는 커밋 경계 리뷰 2a)에서만 돈다 — 매 tick이 아니라 같은 비싼 순간들. `jarvis-once` 호출 시 계획/체크리스트는 이미 "작업 스펙"(수집 항목 0)으로 넘어가 있다. 일반 리뷰와 함께 체크리스트에 대고 보고하게 한다:
- 이 변경이 어느 항목(들)을 전진시키나, 그리고 어느 항목이 이제 **완료로 보이나**;
- 항목별로 **뭐가 빠졌거나 위험한가**(해피 패스는 됐지만 에러/빈 입력 경로는 안 된 항목);
- **완료 오판정** — 사람이 이미 체크한 항목(`- [x]`)인데 코드가 뒷받침하지 않으면 짚는다(설익은 "완료"를 반박하는 게 내비게이터의 일이지, 도장 찍어주는 게 아니다).
- 이 평가는 Jarvis 마커 **안**에 리뷰 본문의 일부로 넣는다.

**체크마크는 사람이 소유한다.** 워치는 `- [ ]` → `- [x]`를 **스스로 체크하지 않는다** — 그 판단(그리고 거기 실리는 책임)은 사람의 몫으로 남는다. 워치는 자기 평가를 *보고*만 하고, 사람이 동의하면 `.jarvis/checklist.md`에서 항목을 체크한다. (매 리뷰에 파일을 읽어 공식적으로 뭐가 됐고 뭐가 열려 있는지 안다.)

**무엇부터 할지는 사람의 몫.** 물으면 다음 항목 하나와 왜인지 한 줄을 추천하고 — 비킨다. 작업 순서를 대신 짜지 않는다.

**완료 → 최종 리뷰, 그다음 종료 추천(확정은 사람):** **모든 체크리스트 항목이 완료로 보이면**(전부 체크됨, 또는 열린 공백 없이 전부 완료로 평가됨) 그 tick에서 `jarvis-once`에 **계획 전체에 대고 종합 최종 리뷰**를 시킨다 — "전부 봉인되기 직전"의 골든타임을 가장 큰 스케일로. 마커로 감싸 전달한 뒤, 마커 **밖**에 한 줄 추천을 남긴다:

```
✅ 체크리스트 전 항목 완료로 보임 — 위 최종 리뷰 참고. 루프를 닫을까요? (Esc로 멈춤 · 또는 "done" / 계속)
```

- 이 tick에서 스스로 루프를 끝내지 **않는다** — 사람이 정하는 동안 워치가 살아있도록 **다음 wake는 그대로 예약한다**(절차 4). 루프 종료는 사람의 행위다: 사람이 확정("done")하거나 그냥 인터럽트(Esc)하면 그때 다음 wake가 예약되지 않는다. ("모든 방아쇠는 사람이 당긴다"와 일관)
- 완료 신호 후에도 사람이 계속 편집하면, 루프는 그냥 계속 리뷰한다 — 특별히 할 일 없음.

### 4. 다음 wake 예약 (루프 유지의 핵심)
`ScheduleWakeup`을 호출해 다음 실행을 예약한다.

- **웜업 판정:** `boot_now`를 정한다 — 최초 부팅 tick(0.5에서 baseline 없음으로 판정)이면 `warmup` 값, 아니면 baseline의 `boot` 값(없으면 0).
- 간격 결정:
  - 이번 tick에서 리뷰를 **미뤘으면**(`deferred`를 1로 세팅) → `debounce` (짧게, 곧 다시 확인)
  - 이번 tick에서 `jarvis-once`를 **실행(flush)했으면** → `active`
  - **웜업 중**(`boot_now > 0`) → `active` (첫 로드 직후엔 idle 대신 빠르게 재확인)
  - **워킹트리에 변경이 있으면**(`cur_lines > 0`) → `active` (작업이 진행 중이니 촘촘히 폴링해 새 변경·커밋을 빨리 잡는다)
  - 그 외(워킹트리 깨끗 · 웜업 종료) → `idle`
- **prompt에는 이번에 받은 args를 그대로 echo 한다.** 그래야 다음 wake에서도 설정이 유지된다. `strength`를 쓴 경우 **전개된 개별 노브가 아니라 `strength=<값>`(+ 개별 덮어쓰기)** 형태로 직렬화한다(강도 의미 보존). 예:

  ```
  /jarvis strength=high paths=src/billing risk=**/*payment*
  /jarvis strength=high idle=30m                          # 프리셋 + 개별 덮어쓰기도 그대로 echo
  /jarvis active=4m idle=25m debounce=90s                 # strength 미사용 시는 개별 노브로 echo
  ```

  ⚠️ 이 echo를 빠뜨리면 두 번째 wake부터 모든 설정이 기본값으로 돌아간다. 반드시 현재 유효 args 전체(`strength` 또는 개별 노브 + `paths`·`risk`)를 직렬화해 넘긴다.
- **재개용 args 저장:** wake 예약과 함께, prompt에 echo한 것과 **동일한 args 문자열**을 `.jarvis/args`에 1줄로 기록한다(`/jarvis ` 접두어 없이 args만). 루프를 인터럽트(Esc)로 멈춘 뒤 `/loop /jarvis`(인자 없이)로 다시 띄우면 절차 0.4가 이 값을 읽어 같은 설정으로 자동 재개한다.
- `reason`에는 무엇을 기다리는지 구체적으로 적는다(예: "변경 누적 폴링, 다음 4분 뒤 확인").
- **생존 상태 기록(`.jarvis/status`):** `ScheduleWakeup` 직후, 다음 wake 시각을 epoch로 환산해 `.jarvis/status`에 한 줄로 덮어쓴다. `<delay_s>`는 이번에 예약한 간격(초), `<interval>`은 그 간격 라벨(`active`/`idle`/`debounce`), `<strength>`는 유효 강도(개별 노브만 쓴 경우 생략 가능):

  ```bash
  mkdir -p .jarvis
  now=$(date +%s)
  plan=""   # 계획 모드: 체크리스트 진행률을 붙여 statusline이 표시하게 함
  if [ -f .jarvis/checklist.md ]; then
    done=$(grep -cE '^[[:space:]]*-[[:space:]]*\[[xX]\]' .jarvis/checklist.md); total=$(grep -cE '^[[:space:]]*-[[:space:]]*\[[ xX]\]' .jarvis/checklist.md)
    plan=" plan=${done}/${total}"
  fi
  echo "state=watching next_wake=$((now + <delay_s>)) interval=<interval> strength=<strength>${plan} tick=$now" > .jarvis/status
  rm -f .jarvis/stopped   # tick이 돈다 = 루프 살아있음 → 이벤트 멈춤 플래그 해제(있다면)
  ```

  이 한 줄이 statusline의 연속 표시(감시 중 / 멈춤?)와 stall 추론의 근거다(아래 "생존 가시화"). 기록을 빠뜨리면 statusline이 옛 `next_wake`만 보고 곧 "멈춤?"으로 뜬다. `plan=<완료>/<전체>` 필드는 선택 — 계획 모드에서만 있고, statusline이 `· plan 3/7` 구획으로 그린다.

## 생존 가시화 (하트비트 + statusline)

"지금 루핑 중인지" 사용자가 늘 알 수 있게 두 겹으로 신호를 낸다. `/loop` dynamic 모드는 상주 프로세스가 없어 tick과 tick **사이엔 아무것도 안 돈다** — 그래서 (A) tick마다 본문에 한 줄, (B) tick 사이에도 보이는 statusline, 둘을 함께 쓴다.

### (A) tick 하트비트 — 본문 한 줄
조용한 tick(새 변경 없음)이라도 **마커 밖**에 alive 신호 한 줄을 남긴다. 이 한 줄이 "루프가 살아있고 다음 확인은 언제"임을 매 tick 보여준다.

```
⏱ jarvis · alive · 다음 확인 ~4m 뒤 (active) · strength=medium
```

- 표기는 절대 시각이 아니라 **상대(~Nm 뒤)** 로 한다(절차 4에서 정한 간격을 그대로 쓰면 되고 `date` 계산이 필요 없다).
- 간격 라벨(`active`/`idle`/`debounce`)과 유효 강도를 함께 적는다.
- **대화 중(`active_chat == true`) tick에서는 하트비트를 찍지 않는다** — 사람이 곁에 있어 루프 생존이 자명하고, 대화를 끊지 않기 위함이다(절차 0). 이때의 연속 신호는 (B) statusline이 메운다. 단 미룸(debounce) 분기의 운영 메시지는 평소대로 남긴다.
- 리뷰를 flush한 tick은 마커로 감싼 리뷰 본문 **뒤에** 이 하트비트 한 줄을 덧붙인다(다음 확인 ETA 제공).

> 절차 3의 "그 외(새 변경 없음)" 분기는 이제 침묵 대신 이 하트비트 한 줄을 낸다(대화 중이면 생략).

### (B) statusline — tick 사이에도 연속 표시
`.jarvis/status`(절차 4에서 매 tick 기록)를 읽어 Claude Code 하단 상태줄에 워치 상태를 **렌더마다** 그린다. tick이 안 도는 사이에도 보이고, `next_wake`가 한참 지났는데 갱신이 없으면 **"멈춤?"**까지 추론한다(=루프가 죽었거나 Esc로 멈춤).

```
🤖 jarvis · 감시 중 · 다음 ~3m (active)            (정상 — 살아 있음)
🤖 jarvis · 확인 중…                                (예약 시각 도달, 곧 tick)
🤖 jarvis · ⚠ 멈춤? 11m 동안 tick 없음 — /loop /jarvis 로 재개   (죽었을 가능성)
```

스크립트는 이 스킬에 동봉돼 있다: **`assets/statusline.sh`**. `.jarvis/status`가 없으면(=워치 미가동) 아무것도 출력하지 않아, 항상 켜둬도 무해하다. 활성화는 비파괴적으로 **사용자가 직접** settings.json에 등록한다(설치 시 자동으로 건드리지 않는다):

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/skills/jarvis/assets/statusline.sh"
  }
}
```

- 프로젝트 단위 설치면 경로를 `.claude/skills/jarvis/assets/statusline.sh`로 바꾼다.
- 이미 다른 `statusLine`을 쓰고 있으면 Claude Code는 statusLine을 하나만 허용하므로, 기존 스크립트 안에서 `bash .../statusline.sh`를 호출해 그 출력을 한 구획으로 합쳐 쓴다.

### (C) Stop 훅 — 멈춤을 시간 추론 없이 즉시 확정 (선택)
(B)의 statusline은 `next_wake`가 지나야 죽음을 추론하므로 최대 `interval + grace`만큼 지연된다. 이를 **이벤트 기반**으로 끌어올리는 보조 장치가 Stop 훅이다.

`assets/loop-watch-hook.sh`를 **Stop**·**StopFailure** 훅으로 걸면, 매 턴 종료 시 payload의 `session_crons`(현재 예약된 wake 목록)를 검사한다. 거기에 `/jarvis` wake가 없으면 = 루프가 더는 예약돼 있지 않다(ScheduleWakeup 누락·에러, 또는 Esc로 죽은 뒤 사용자가 무언가 입력한 턴) → `.jarvis/stopped`를 남겨 statusline이 **즉시** "멈춤"을 표시하게 한다. wake가 살아있으면 플래그를 지운다.

```json
{
  "hooks": {
    "Stop":        [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/skills/jarvis/assets/loop-watch-hook.sh" } ] } ],
    "StopFailure": [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/skills/jarvis/assets/loop-watch-hook.sh" } ] } ]
  }
}
```

- **타이밍:** Esc *그 순간*엔 못 잡는다 — Claude Code엔 인터럽트 훅이 없다(Stop은 정상 턴 종료에만 발화). 대신 **Esc 후 다음 턴(=사용자의 다음 입력)이 끝나는 순간** 확정된다. 보통 곧바로 손대므로 체감상 거의 즉시이고, "Esc 후 아무 입력 없이 방치"한 경우만 (B)의 시간 추론이 받는다.
- **오탐 방지:** `last_assistant_message` 등에 "/jarvis" 텍스트가 있어도 무시하고 **오직 `session_crons` 안의 wake prompt만** 본다.
- 훅이 없으면 (B)만으로도 동작한다(시간 추론). 훅은 *감지 속도*를 높이는 선택적 보강이다.

## 멈춤 / 재개 / 초기화

`/loop`을 엔진으로 쓰므로 생애주기는 `/loop`의 수명주기에 얹힌다. 별도 pause/resume 명령은 없다.

| 동작 | 방법 | 상태(`.jarvis/`) |
|------|------|------------------|
| **시작 · 재개** | `/loop /jarvis [args]` | baseline/args가 남아 있으면 그 지점에서 이어감. args 없이 띄우면 `.jarvis/args` 자동 복원(절차 0.4) |
| **멈춤 · 일시정지** | `/loop` 인터럽트(Esc) | 손대지 않음 — baseline/args 보존돼 재개 대기 |
| **완전 초기화** | **`/jarvis-reset`** (독립 스킬) | `.jarvis/baseline`·`.jarvis/args` 삭제(그리고 확인 후 `plan.md`·`checklist.md`) → 다음 시작은 최초 부팅(배너 · 계획 옵트인 · 강도 질문) |

작동 원리:
- **가벼운 양보(암묵)**: 사용자가 그냥 다른 메시지를 보내면 그 턴은 절차 0에 따라 의논/구현에 양보한다(워치 자체는 살아 있음). 명령 없이 일어나는 암묵적 양보다.
- **멈춤/일시정지 = 루프 인터럽트(Esc)**: `/loop` dynamic 모드에서 다음 tick은 `ScheduleWakeup`을 부를 때만 생긴다. 루프를 인터럽트하면 다음 wake가 예약되지 않아 루프가 끝난다. baseline·args는 디스크에 그대로 남으므로 손실 없이 재개를 기다린다. (루프 종료엔 teardown 훅이 없어 종료 시점에 정리 코드를 돌릴 수 없다 — 그래서 별도 pause 플래그를 두지 않는다.)
- **재개 = `/loop /jarvis`**: 다시 띄우면 baseline이 있어 배너·강도 질문을 건너뛰고(절차 0.5·0.6), args 없이 띄웠으면 절차 0.4가 `.jarvis/args`를 복원해 같은 설정으로 이어간다. 밖에서 rebase/reset 했더라도 절차 2(0) stale 자가보정이 무효 head를 현재값으로 조용히 맞춘다.
- **`/jarvis-reset`**: `.jarvis/baseline`·`.jarvis/args`를 지우는 **독립 명령**이다. 돌고 있는 루프를 멈추진 않는다(그건 Esc) — 멈춘 뒤 "처음부터 새로"를 원할 때 상태를 비운다. ("jarvis 초기화", "처음부터 다시"도 동일하게 처리. "그냥 멈춰"는 Esc 안내.)

## 비용 가이드 (사용자 안내용)

- wake 간격이 5분 미만이면 prompt 캐시(TTL 5분)가 살아 폴링 턴이 거의 공짜다. 그래서 `active` 기본값은 4분이다.
- 잠잠할 때는 `idle`을 길게(기본 25분) 두어 캐시 미스 누적 비용을 줄인다.
- 실제 토큰의 대부분은 "`jarvis-once`가 도는 순간"(새 변경 누적·위험 경로·커밋 경계)에 쓰인다. 새 변경이 쌓일 때마다 리뷰하므로, 폴링이 촘촘할수록(강도 `high`) 리뷰가 잦아져 비용이 는다. `idle`을 길게 잡거나 강도를 낮추면 준다.
- 폴링을 **촘촘히** 해도 소음은 늘지 않는다. `jarvis-once`는 자체 severity 문턱 아래선 스스로 조용히 있기 때문이다. 폴링을 높이면 *호출 비용*만 늘릴 뿐 잔소리를 늘리지 않는다 — 반응 속도를 높이고 싶으면 안심하고 올려도 된다.
- 커밋 경계 트리거는 커밋당 1회뿐이라 비용이 예측 가능하고, "착오 봉인 직전" 단 한 번의 점검이라 비용 대비 가치가 가장 높은 실행이다.

## 의존성 주의

이 스킬은 `jarvis-once`(단발 navigator) 스킬을, 계획 옵트인 시엔 `jarvis-plan`(계획 navigator) 스킬을 호출한다. 팀에 공유하려면 둘 다 함께 접근 가능해야 한다(레포 `.claude/skills/jarvis-once/`·`jarvis-plan/` 또는 공통 레포). 개인 글로벌(`~/.claude/skills/…`)에만 있으면 다른 팀원 환경에서는 호출이 실패할 수 있다.
