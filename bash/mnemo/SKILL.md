---
name: mnemo
description: >
  과거 대화 검색, 장기기억 설정, 세션 핸드오프할 때 사용. 대화 자동 저장, 키워드 태깅,
  MEMORY.md 관리, 세션 전환. 관리 대상은 프로젝트 루트의 3계층(MEMORY.md + memory/ + conversations/)이며,
  프로젝트 이동 후에도 기록을 함께 사용할 수 있도록 저장 경계를 검증한다.
  /mnemo, 므네모, 장기기억, memory, 기억해, 이전에, handoff, 핸드오프, 핸즈오프, 세션 저장 요청에 사용한다.
---

# Mnemo - 기억 시스템

> 기억의 여신 Mnemosyne에서 유래

세션 간 컨텍스트 유지를 위한 통합 메모리 시스템입니다.

## 설치

```bash
node skills/mnemo/install.js              # 설치
node skills/mnemo/install.js --uninstall  # 제거
```

---

## 실행 요건

| 기능 | 런타임 | Python이 없으면 |
|------|--------|-----------------|
| 대화 자동 저장 · 도구 관찰 로그 · MEMORY.md 규칙 | PowerShell / bash | **정상 동작** |
| 누락 턴 복구 (SessionStart) | 셸 → Python | **조용히 건너뜀** (`exit 0`) |
| 핸드오프 생성·검증·목록·staleness | Python 3 | 실행 불가 → 아래 대안 |
| 변경 계보 수확 · 기억 앵커 검사 | Python 3 + Node | 실행 불가 |

**Python이 없어도 기억은 계속 쌓입니다.** 저장 훅은 전부 셸 스크립트이고, Python은
쌓인 것을 읽고 분석하는 도구에만 필요합니다. `install.js --check`의 `[4/4]`가 현재
상태를 알려주며, **Python 없음은 설치 실패로 치지 않습니다.** 명령은 `python`·`py`·`python3` 중
`--version`이 되는 첫 것을 씁니다 — Windows 스토어 별칭 때문에 `python`만 실패하고 `py`는 되는 PC가 있습니다
([판정 규칙](references/handoff-memory.md)).

> **Python 없이 핸드오프 쓰기**: `references/handoff-template.md`를 읽고
> `docs/handoffs/YYYY-MM-DD-HHMMSS-{slug}.md`에 직접 작성합니다. 스캐폴드와 검증만
> 없을 뿐 핸드오프 계약은 동일합니다. 컨텍스트가 차오르는 순간에 스크립트가 없다고
> 핸드오프를 포기하지 마세요 — 그게 가장 큰 손실입니다.

---

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **빠르게** | 훅에서 AI 호출 금지 |
| **단순하게** | 파일 기반, DB 없음 |
| **검색 가능하게** | 키워드 + 동의어 확장 |
| **점진적 공개** | 필요한 깊이까지만 읽기 (Progressive Disclosure) |
| **프라이버시** | `<private>` 태그로 민감 정보 제외, `MNEMO_DISABLE=1`로 저장 전체 opt-out |

---

## 포함 파일

```
mnemo/
├── SKILL.md                    # 이 파일
├── install.js                  # 설치 스크립트
├── hooks/                      # 대화 저장 훅 (root hooks/에 위치)
│   ├── save-conversation.ps1/.sh       # User 입력 저장
│   ├── save-tool-use.ps1/.sh           # 도구 호출 관찰 로그 + 앵커 조회 주입 (Claude·Grok 공용)
│   ├── save-response.ps1/.sh           # Assistant 응답 저장 (Stop)
│   └── reconcile-conversations.ps1/.sh # 누락 턴 복구 (SessionStart)
├── templates/                  # CLAUDE.md 규칙
│   └── claude-md-rules.md
├── scripts/                    # Python 3 (+ 루트 판정에 Node)
│   │   # ── 핸드오프 (세션 경계) ──
│   ├── create_handoff.py       # 스캐폴드 (Origin=현재 CLI가 확인한 요구·출처, Files=관찰, 대체 후보 제시)
│   ├── validate_handoff.py     # 게이트 (feature-bearing: Origin+Diagram 필수)
│   ├── list_handoffs.py        # 목록
│   ├── check_staleness.py      # 핸드오프가 현재 코드 대비 얼마나 낡았나 (git 기준)
│   │   # ── 기억 위생 (진단 전부 · 수정 최소) ──
│   ├── mnemo_doctor.py         # 진입점: 17개 점검, --fix는 기계적인 셋만
│   ├── build_anchor_index.py   # 착수 전 조회: 이 파일에 기대는 결정 (기억 파생)
│   ├── harvest_lineage.py      # 착수 전 조회: 파일별 "언제·왜·어떻게" (핸드오프 파생)
│   ├── check_memory_anchors.py  # 기억이 가리키는 파일이 실재하는가 (CodeMap 이동 힌트)
│   ├── split_memory_file.py    # 복구: 비대한 memory/X.md → X/NNN-*.md + index.md
│   ├── reclassify_observations.py  # 복구: 옛 훅이 오분류한 관찰을 learned로
│   │   # ── 공통 ──
│   ├── reconcile_conversations.py  # JSONL → conversations/ 누락 턴 복구
│   └── mnemo_project_root.py   # 프로젝트 루트 판정 (훅과 같은 경계)
├── references/                 # 핸드오프 템플릿
│   ├── handoff-template.md
│   └── resume-checklist.md
├── docs/                       # 상세 문서
│   ├── memory-system.md        # 인지 모델 설명
│   └── memory-hygiene.md       # 기능 4 도구별 상세 (SKILL.md 경량화로 분리)
└── evals/                      # 평가
```

---

## 기능 1: 대화 자동 저장

```
[SessionStart 훅] reconcile-conversations
    → 지난 세션에서 놓친 assistant 턴을 JSONL 기준으로 backfill (멱등)
    ↓
사용자 입력
    ↓
[UserPromptSubmit 훅] save-conversation
    → 대화 파일에 User 입력 append (<private> 블록 제거)
    ↓
Claude 도구 호출
    ↓
[PostToolUse 훅] save-tool-use
    → 도구명 + 파일경로를 toollog에 한 줄 append
    ↓
Claude 응답 (끝에 #tags 포함)
    ↓
[Stop 훅] save-response
    → transcript에서 응답 추출 → <private> 블록 제거 → 대화 파일 append
```

**원본 세션** (마지막 단계에서 필요한 대화만 파싱·복구): `~/.claude/projects/<encoded>/*.jsonl`
**검색 대상** (사람이 읽고 Claude가 grep): `conversations/YYYY-MM-DD-claude.md`
**멱등 인덱스**: `conversations/.mnemo-index.json` (JSONL 줄 uuid 기반)

> 검색 순서는 `MEMORY.md` → 관련 기억 항목 → 연결 대화·`#tags:` → 대화 본문 → 범위를 좁힌 원본 세션입니다. 태그가 없어도 본문을 확인합니다. [전역 규칙 정본](templates/claude-md-rules.md)의 읽기 전용·카탈로그·핸드오프 기준을 함께 따릅니다. 설치기는 `autoMemoryEnabled=false`로 설정해 새 의미기억을 프로젝트 Mnemo에 모읍니다. 기존 네이티브 기억과 원본 세션은 삭제하지 않습니다.

Stop 훅이 한 번이라도 실패하거나 Claude Code가 강제 종료되면 해당 턴의
미러링이 누락됩니다. 다음 세션 시작 시 `reconcile-conversations`가 자동으로
JSONL을 스캔하여 놓친 턴을 복구합니다. 수동 실행도 가능합니다:

```bash
python "<module_root>/scripts/reconcile_conversations.py" --project-root "<project>" --date YYYY-MM-DD
python "<module_root>/scripts/reconcile_conversations.py" --project-root "<project>" --days 30
python "<module_root>/scripts/reconcile_conversations.py" --project-root "<project>" --date YYYY-MM-DD --dry-run
```

---

`module_root`는 이번에 읽은 정확한 `SKILL.md`의 디렉터리입니다. 날짜 옵션을 생략하면 최근 7일이며,
질문의 실제 시기에 맞춰 `--date` 또는 `--days`를 지정합니다. `--all`은 전체 기간이 필요할 때만 사용합니다.
`--dry-run`은 쓰기 예정 요약이며 대화 전체 추출이 아닙니다. 원본 전체를 컨텍스트에 읽지 말고,
읽기 전용 요청에서는 복구 쓰기를 하지 않습니다. 추가 근거는 실제 파서의 사용자·응답 텍스트만 제한해 추출하고,
그 경로가 없으면 도구의 한계를 알립니다.
현재 reconcile 파서는 assistant 텍스트를 복구합니다. 사용자 질문이 필요하면 해당 세션의 사용자 레코드를
별도로 제한해 파싱하며, assistant 복구 성공을 전체 대화 복구로 보고하지 않습니다.

## 기능 2: MEMORY.md 관리

CLAUDE.md 규칙으로 자동 동작:
- 첫 저장 턴에서 `MEMORY.md` + `memory/*.md` 기본 scaffold 자동 생성
- 중요 결정 → MEMORY.md 자동 업데이트
- 과거 질문 → 동의어 확장 검색

**3계층 메모리 구조:**

| 계층 | 파일 | 용도 |
|------|------|------|
| **인덱스** | MEMORY.md | 키워드 인덱스 + 프로젝트 목표 (항상 로드) |
| **의미기억** | memory/*.md | 카테고리별 상세 항목 (필요 시 Read) |
| **일화기억** | conversations/*.md | 상세 대화 원본 (검색 시에만) |

### 줄기와 증거 — 항목이 태어날 때 들고 오는 것

**기억은 주장이고 대화는 증거인데, 둘을 잇는 링크가 없었습니다.** 항목만 읽은 다음 세션은
"그렇게 정했구나"까지는 가도 의심이 들 때 내려갈 곳이 없어서, 같은 논쟁을 처음부터 다시 합니다.
그래서 **결정이 굳는 순간에** 항목이 다음을 들고 태어납니다. 나중에 붙이지 않습니다 —
옛 것과 새 것을 동시에 아는 순간은 그때뿐이고, 세션 끝에는 이미 절반을 잊습니다.

| 줄 | 담는 것 | 없으면 생기는 일 |
|----|---------|------------------|
| `evidence:` | 대화 파일 + 턴 시각, 핸드오프 경로 | 의심이 들 때 15만 줄에서 다시 찾아야 한다 |
| `alternatives:` | 탈락 대안 · 그 대안의 가장 강한 논거 · 왜 졌나 · 복귀 조건 | 나중에 그 논거를 들고 오는 사람과 논쟁을 0에서 다시 한다 |
| `depends-on:` | 기대는 항목 `[[NNN-slug]]` | 기댄 결정이 뒤집혀도 이 항목은 CURRENT인 채 조용히 낡는다 |
| `sources:` | 원천 문서·URL·설계 산출물 | 외부 사실이 바뀌어도 다시 볼 줄 모른다 |
| `files:` | 근거 코드 경로 (루트 기준 상대) | 파일에서 결정으로 되짚는 문이 닫힌다 |
| `reopen-when:` | **무엇이 바뀌면 다시 보는지** (없으면 `none — <이유>`) | 아무도 반박하지 않는 한 영원히 현재 — 결정이 관습이 된다 |
| `last_verified:` | 외부 사실을 실측으로 확인한 날 | 저쪽이 바뀌어도 모른다. 013은 틀린 줄을 달고 165일을 CURRENT로 있었다 |

**기록의 목적은 논쟁을 끝내는 것이 아니라 0이 아닌 지점에서 다시 시작하게 하는 것입니다.** `CURRENT`는 "아직 맞다"가 아니라 "아직 대체되지 않았다"는 뜻이고, 되돌릴 조건이 없는 결정은 반박할 수 없으므로 영원히 현재로 남습니다. 그래서 이유는 **조건 형태**로 적습니다. "MCP는 별로였다"가 아니라 "이 세 결함 때문에"라고 적어야
그 결함이 고쳐졌을 때 항목이 스스로 재검토 대상임을 압니다. 고뇌 과정과 버린 논의 **자체**는
대화에 남기고 항목은 `evidence:`로 가리킵니다 — 항목은 서사가 아닙니다.

### 파일에서 결정으로 — 앵커 역색인

기억은 제목·태그·`MEMORY.md`로, 즉 **의미로** 색인되어 있습니다. 그것은 "지난번에 이런 거
했던 것 같은데"에 답합니다. 훨씬 흔한 시작인 **"이 기능 오류났어, 고치자"에는 답하지 못합니다** —
그 요청에는 검색할 단어가 없고 대상만 있기 때문입니다. 그래서 조회 키를 파일로 뒤집습니다.

```bash
python scripts/build_anchor_index.py --file hooks/save-turn.sh   # 이 파일에 기대는 결정
python scripts/build_anchor_index.py --out                        # memory/.mnemo-anchor-index.md
```

`--file` 조회는 저장된 색인을 읽지 않고 기억에서 매번 다시 만들므로 **낡을 수가 없습니다**.
`files:` 줄이 있으면 그것이 정본이고 없으면 본문의 코드 경로를 읽으므로, 계약 적용 전 항목도
지금 당장 걸립니다. 파생 색인이라 점 접두 이름을 쓰고(기억 항목으로 오인되면 진단 수치가 오염된다),
원본을 고치지 않고 매번 처음부터 다시 만듭니다. 색인 재생성은 핸드오프가 소유합니다 —
도구 단위 훅이 없는 CLI에서도 네 CLI가 모두 지나는 자리이기 때문입니다.

**훅이 이 조회를 대신 불러 줍니다.** 파일을 고친 직후, 그 파일에 기대는 결정이 모델의 컨텍스트로
들어옵니다. 세션당 파일당 한 번입니다. 어느 줄기 위에 있는지가 **판단이 아니라 읽기**가 됩니다.

| CLI | 수단 | 비고 |
|-----|------|------|
| Claude | `PostToolUse` → `additionalContext` | `PreToolUse`는 `deny`로만 말할 수 있어 조회에 못 쓴다 |
| Grok | 같은 Claude 훅·같은 스키마 | `GROK_HOOK_EVENT` 가드를 `post_tool_use`만 통과하도록 좁혔다. 저장은 계속 `grok-mnemo` 전담 |
| Antigravity | `PreToolUse` 기록 → `PostInvocation` `injectSteps` | `PostToolUse` 출력이 빈 객체라 한 훅으로 안 된다 |
| Codex | 없음 (`notify` 하나) | 규칙과 핸드오프 스캐폴드로 대신한다 |

parity 우선순위는 **포착 > 연결 > 주입**입니다. 네 CLI가 같은 프로젝트의 같은 `conversations/`에
쓰므로, Codex 세션이 남긴 대화를 나중에 다른 CLI가 읽고 줄기에 붙일 수 있습니다. Codex에 없는
것은 주입뿐이고 **지연이 생길 뿐 유실은 없습니다**. 근거·실측·되돌릴 조건은
`memory/architecture/057-hook-budget-llm-never-process-rarely-constant-time-per-tool.md`에 있습니다.

---

## 기능 3: 세션 핸드오프

컨텍스트가 차거나 작업을 중단할 때 핸드오프 문서를 생성합니다.

**핸드오프는 기억의 입력구입니다.** 아키텍처 결정이 `memory/`에 들어온 경로를 추적하면
전부 핸드오프 세션이고(실측 69회/69회), 계보 수확·역사 복원도 핸드오프를 원천으로 씁니다.
설계 파이프라인(`specs/`·`adr/`)은 설계할 때만 생기지만 핸드오프는 즉흥 작업에도 남기
때문입니다. 그래서 핸드오프의 `Origin`·`Files Modified`·`Decisions Made` 세 표가 채워져
있어야 나중에 "왜 시작했고, 어디를, 왜 고쳤나"를 되살릴 수 있습니다.

핸드오프는 구현한 기능 목록과 구성도/흐름도를 작성하는 산출물입니다.
항상 **Feature/Flow/Decision Snapshot**에 구현 기능, 기능 경계, 구성도, 입력→처리→저장→표시 흐름,
주요 결정/대안/근거를 남깁니다. CodeMap은 TermSnap이 만드는 별도 산출물이므로,
핸드오프는 CodeMap을 대체하지 않고 현재 세션의 구현 근거와 구성도를 작성합니다.

### 핸드오프 생성

먼저 [핸드오프 기억 점검](references/handoff-memory.md)을 읽습니다. 생성 도구는 두 경우에
닥터를 자동으로 한 번 실행합니다(진단만, 방문을 차트에 기록) — **아키텍처 기억이 없을 때**와
**마지막 닥터 방문이 30일을 넘었을 때**입니다. 후자가 없으면 기억이 있는 프로젝트에서는
조건부 진단이 영원히 건너뛰어, 점검이 사람의 기억에만 의존하게 됩니다.
에이전트가 근거 기반 보완과 재검색을 마쳐야 합니다.
TermSnap 부품 지도(`codemap/component-map.json`)가 있는 프로젝트에서는 `owners.json`으로 이번 세션
파일의 미배정·재생성 필요를 `Component map:` 한 줄로 알립니다(지도가 없으면 줄 없음, 닥터와 별개).
컨텍스트 압축/한계 시 자동 핸드오프는 전역 규칙이며 고정 20턴 타이머가 아닙니다.

```bash
python "<module_root>/scripts/create_handoff.py" [task-slug]
python "<module_root>/scripts/create_handoff.py" "auth-part-2" --continues-from previous.md
```

### 핸드오프 검증

검증기는 **이번 세션 범위**만 봅니다 — 결정 표의 `대체 대상`이 실재하는지(없으면 게이트),
결정을 적었는데 그날 기억 항목이 하나도 갱신되지 않았는지(경고), `Component map:` 줄이 보고한
미배정·재생성 필요·지도 오류에 `→ 배정함:`/`→ 보류:` 표식이 없는지(경고). 프로젝트 전체 백로그
(미부착 날·죽은 링크·이유 없는 교체)는 닥터의 몫이고, 인계 순간에 펼치면 읽히지 않습니다.

```bash
python scripts/validate_handoff.py <handoff-file>
```

**기능을 구현·변경한 세션(feature-bearing)만** `Composition Diagram`과 `Origin`을
필수로 요구합니다. 탐색·문서·설정만 한 세션은 면제됩니다 — typo 수정에 구성도를
강요하는 것은 신호가 아니라 의례이고, 같은 판단을 Origin에도 적용합니다.

`Origin`은 **"왜 이 작업이 시작됐나"**를 남기는 자리입니다. 세션이 끝나면 "무엇을
했나"는 `Files Modified`에 남지만 최초 요구는 사라집니다. 이어받는 세션은
`--continues-from`을 쓰면 출처가 선행 핸드오프 링크로 자동 채워지므로, 최초 요구는
체인당 한 번만 적으면 됩니다.

> 규칙 도입 이전 핸드오프에는 `Origin`이 없습니다. 검증기는 새로 작성한 핸드오프를
> 검사하는 게이트이므로 과거 문서를 소급 수정할 필요는 없습니다.

### 핸드오프 목록

```bash
python scripts/list_handoffs.py
```

### Staleness 체크

```bash
python scripts/check_staleness.py <handoff-file>
```

**Staleness 레벨:**
- FRESH: 바로 재개 가능
- SLIGHTLY_STALE: 변경사항 확인 후 재개
- STALE: 컨텍스트 검증 필요
- VERY_STALE: 새 핸드오프 권장

---

## 기능 4: 기억 위생

기억은 쓰는 쪽(훅·핸드오프)만 있으면 조용히 썩습니다. `memory/`·`docs/`·`codemap/`는
관례상 git 추적 밖이라 **diff로는 썩음을 볼 수 없고**, 인덱스에만 예산이 있어 상세 파일은
무제한으로 자라며, 항목이 가리키는 파일은 이름이 바뀌어도 아무도 모릅니다. 기능 4는 그
썩음을 **드러나는 문제로 바꾸는** 도구 묶음입니다.

| 시점 | 도구 | 하는 일 |
|------|------|---------|
| **파일에 손대기 전** | `build_anchor_index.py --file X` | **그 파일에 기대는 결정**. 어느 줄기인가는 판단이 아니라 읽기다 |
| 구현 착수 전 | `harvest_lineage.py --file X` | 그 파일이 언제·왜·어떻게 바뀌어왔나 (없음 확인도 결과) |
| 주기적 / 이상할 때 | `mnemo_doctor.py` | 17개 점검 한 번에. FAIL·WARN과 근거 |
| 방문 기록을 남길 때 | `mnemo_doctor.py --chart` | 이번 판단을 차트에 남긴다. 다음 방문은 차이만 말한다 |
| 닥터가 가리킬 때 | `mnemo_doctor.py --promote-structure` | 산문 앵커·암묵적 수명을 `files:`·`status:` 줄로 (기억 본문 수정, 백업) |
| 닥터가 가리킬 때 | `check_memory_anchors.py` | 사라진 파일을 가리키는 기억 목록 + 이동 후보 |
| 닥터가 가리킬 때 | `split_memory_file.py` | 비대한 상세 파일을 항목별로 (백업·링크 갱신) |
| 닥터가 가리킬 때 | `reclassify_observations.py` | 옛 훅의 오분류 관찰 복구 (백업·delta 보존) |

원칙 넷 — **진단은 전부, 수정은 기계적인 것만**(닥터 `--fix`는 정제 기준값, 정확히 하나에 맞는 `#slug` 링크의 `[[NNN-slug]]` 번호화, 기록 안의 루트 내부 절대경로 상대화 셋. 기억 본문을 고치는 `--promote-structure`와 차트를 쓰는 `--chart`는 별도 플래그이고, **진단만 할 때는 아무 파일도 쓰지 않는다**) /
**판정 로직은 한 곳**(닥터는 형제 스크립트를 호출, 과거 재분류는 명시적 성공 근거가 있을 때만) /
**"없음 확인"도 결과**(입력 부재는 exit 0 + 이유 + 대안, 실패 2는 루트 판정 불가뿐) /
**되돌릴 수 있게**(dry-run 기본, `--apply`에 백업 강제).

도구별 상세 — 닥터의 17개 점검 표, 앵커 판정 규칙(문맥 분류·이동 후보), 재분류 절차,
분할 규칙, 계보 이유 폴백과 각 종료 코드 — 는 **[`docs/memory-hygiene.md`](docs/memory-hygiene.md)**에
있습니다. 위 시점 표와 원칙 넷이 계약이고, 상세는 해당 도구를 쓸 때 읽습니다.

---

## 사용법 요약

| 시점 | 상황 | 방법 |
|------|------|------|
| 항상 (자동) | 대화·응답 저장 | 훅 (Python 불필요) |
| 항상 (자동) | 도구 관찰 기록 | PostToolUse 훅 → toollog + `gotchas/learned observations.jsonl` (에러 형태만 실패) |
| 항상 (자동) | 키워드 태깅 | Claude가 응답 끝에 `#tags:` 추가 |
| 항상 (자동) | 지식 축적 | 중요 결정 시 `memory/`·`MEMORY.md` 갱신 |
| 항상 | 민감 정보 제외 | `<private>API키</private>` → `[PRIVATE]` |
| 항상 | 저장 전체 끄기 | `MNEMO_DISABLE=1` — 모든 훅 즉시 종료, 기존 저장분 유지 |
| 착수 전 | 과거 검색 | "이전에 ~했었지?" — `MEMORY.md` 코드(`g:072`, `a:147`)가 항목을 직접 지정 |
| 착수 전 | 이 파일 왜 이렇게 됐나 | `python scripts/harvest_lineage.py --file <파일>` |
| 세션 끝 | 세션 전환 | `python scripts/create_handoff.py` → `validate_handoff.py` |
| 세션 시작 | 세션 재개 | 최신 핸드오프 읽기, 낡았으면 `check_staleness.py` |
| 주기적 | 기억 건강 진단 | `python scripts/mnemo_doctor.py` (`--fix`는 기계적인 셋만) |
| 닥터가 가리킬 때 | 앵커 · 분할 · 재분류 | `check_memory_anchors.py` · `split_memory_file.py` · `reclassify_observations.py` |

---

## 저장 위치

| 파일 | 위치 |
|------|------|
| 대화 로그 | `conversations/YYYY-MM-DD-claude.md` |
| 도구 사용 로그 | `conversations/YYYY-MM-DD-toollog.md` |
| 핸드오프 | `docs/handoffs/YYYY-MM-DD-HHMMSS-slug.md` |
| 인덱스 | `MEMORY.md` (프로젝트 루트, 100줄·5KB, 코드 `a:N g:N l:N h:`로 항목 직접 지정) |
| 의미기억 | `memory/<카테고리>/NNN-slug.md` + `index.md` (항목별 분할). 작은 카테고리는 `memory/X.md` 단일 |
| 관찰 로그 | `memory/{gotchas,learned}/observations.jsonl` (10MB에서 `archive/`로 회전), 정제 기준값 `memory/.mnemo-distill-offset` |

## 프로젝트 저장 경계

기억·대화·핸드오프는 확정된 프로젝트 루트에 저장한다. 공통 규약은 소스의
`skills/mnemo/references/project-storage.md`, 설치 스킬의
`<module_root>/references/project-storage.md`에서 읽는다.

모든 어댑터와 핸드오프·복구 도구는 공통 `mnemo-project-root.js`를 사용한다.
Git 환경변수·하위 cwd로 저장 위치를 바꾸지 않으며, Git도 `.mnemo-root`도 없는
일반 cwd에는 자동 저장하지 않는다. 비-Git 프로젝트는 명시한 workspace에서
초기화한다. 설치 패키지에는 공통 핸드오프 `scripts/`도 포함된다. 소스 checkout의
핸드오프 도구 정본은 `skills/mnemo/scripts/`이다. 실행에는 Python 3와 Node.js가 필요하다.

## 프로젝트 스킬 자기개선

핸드오프 정제 또는 명시적 개선 작업에서는 [자기개선 계약](references/self-improvement.md)을 읽는다.
동봉된 내부 모듈을 직접 읽으며 별도 slash 등록이나 Jev API는 필요하지 않다.
핸드오프에서는 후보만 남기고, 승인된 개선 작업에서 실제 비교 검증을 수행한다.
