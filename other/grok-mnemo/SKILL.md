---
name: grok-mnemo
description: Grok Build(xAI CLI) 과거 대화 검색과 장기기억 설정에 사용한다. UserPromptSubmit+Stop 훅으로 대화 자동 저장, 키워드 태깅, 과거 검색을 제공한다. /mnemo, 므네모, 장기기억, 기억해, 이전에, handoff, 핸드오프, grok 기억, grok memory 요청에 사용한다.
---

# Grok-Mnemo - Grok Build 기억 시스템

> 기억의 여신 Mnemosyne에서 유래. Claude Code용 Mnemo를 Grok Build(xAI CLI)에 이식.

Grok Build 세션 간 컨텍스트 유지를 위한 장기기억 시스템입니다.

## 설치

```bash
node "<module_root>/install.js"              # 설치 (Grok 미설치 시 자동 skip)
node "<module_root>/install.js" --uninstall  # 제거
node "<module_root>/install.js" --check      # 설치 상태 점검
```

---

## 4종 Mnemo 비교

| | Claude Code (Mnemo) | Codex CLI | Antigravity CLI | Grok Build (Grok-Mnemo) |
|---|---|---|---|---|
| 훅 | 2개 (Submit + Stop) | 1개 (notify) | 1개 (Stop) | **1스크립트 2이벤트** (UserPromptSubmit + Stop) |
| 데이터 전달 | stdin + transcript JSONL | argv JSON | stdin JSON | **stdin JSON (camelCase)** |
| 페이로드 | prompt / transcript 파싱 | input/last-assistant-message | transcriptPath / user·model 파싱 | **prompt(`<user_query>` 래핑) / lastAssistantMessage** |
| 설정 형식 | settings.json | config.toml | config/hooks.json | **hooks/*.json 자동 스캔** |
| 규칙 파일 | CLAUDE.md | AGENTS.md | GEMINI.md | **~/.grok/rules/*.md (델타만)** |
| 저장 경로 | `conversations/*-claude.md` | `conversations/*-codex.md` | `conversations/*-antigravity.md` | **`conversations/*-grok.md`** |
| 중복 방지 | 타임스탬프 | turn-id | 타임스탬프 | **이벤트 식별자 또는 세션 입력·응답 상태 + reason 필터** |

**Grok만의 특이점** (실측 근거, Grok Build 0.2.111):

1. **Claude 자산 직접 읽기**: 스킬/에이전트/MCP/규칙은 `[compat.claude]` 기본값으로 `~/.claude/`를 직접 읽음 → **mnemo 훅만 어댑터 필요** (memory/learned/018 참조)
2. **camelCase envelope**: Claude의 `transcript_path`(snake_case)와 달리 `transcriptPath`/`sessionId`/`lastAssistantMessage` — Claude 훅 스크립트가 그대로 동작하지 않는 이유
3. **`<user_query>` 래핑**: UserPromptSubmit의 `prompt`는 `<user_query>...</user_query>`로 감싸져 옴 → 훅에서 스트립
4. **Stop 이중 발화**: 세션 종료 시 observe-only Stop이 한 번 더 발화 (`reason: channel_closed|shutdown`) → `reason == "end_turn"`만 저장
5. **Stop stdout 파싱**: Stop 훅의 stdout JSON은 stop 결정으로 해석됨 → 훅은 stdout에 아무것도 쓰지 않음 (안내는 stderr)
6. **이중 저장 방지 가드**: Grok은 `~/.claude/settings.json`의 Claude 훅도 로드하므로, Claude용 mnemo 훅들은 첫 줄에서 `GROK_HOOK_EVENT` 환경변수를 감지하면 exit 0 (grok-mnemo가 전담)

---

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **빠르게** | 훅에서 AI 호출 금지 |
| **단순하게** | 파일 기반, DB 없음 |
| **검색 가능하게** | 키워드 + 동의어 확장 |

---

## 포함 파일

```
grok-mnemo/
├── SKILL.md                     # 이 파일
├── install.js                   # 설치/제거 스크립트
├── hooks/
│   ├── save-turn.ps1            # Windows 훅 스크립트 (2이벤트 분기)
│   ├── save-turn.sh             # Linux/Mac 훅 스크립트 (2이벤트 분기)
│   └── append-event.js          # Node.js 공통 저장·중복 방지
└── templates/
    └── grok-rules.md            # ~/.grok/rules/ 주입 규칙 (Grok 전용 델타)
```

---

## 동작 흐름

```
Grok Build 대화
    ├─ [UserPromptSubmit 이벤트]
    │      → stdin JSON (camelCase) 수신
    │      → prompt에서 <user_query> 래퍼 제거 → User 저장
    └─ [Stop 이벤트]
           → reason == "end_turn" 확인 (세션 종료 재발화 제외)
           → lastAssistantMessage → Assistant 저장 (transcript 파싱 불필요)
           → observations.jsonl 관찰 기록 (gotchas/learned)
           → MEMORY.md + memory/*.md scaffold 자동 생성(없을 때만)
    공통: <private> 스크럽 → conversations/YYYY-MM-DD-grok.md append
```

---

## 저장 위치

| 파일 | 위치 |
|------|------|
| 대화 로그 | `conversations/YYYY-MM-DD-grok.md` |
| 이벤트 인덱스 | `conversations/.grok-events.json` (식별자·내용의 해시와 세션 진행 상태) |
| 의미기억 | `MEMORY.md` (프로젝트 루트) |
| 훅 스크립트 | `~/.grok/hooks/grok-mnemo-save-turn.ps1\|.sh` |
| 공통 저장기 | `~/.grok/hooks/grok-mnemo-append-event.js` |
| 훅 등록 | `~/.grok/hooks/grok-mnemo.json` |
| 규칙 | `~/.grok/rules/grok-mnemo.md` |
| 핸드오프 | 공통 프로젝트 경로 `docs/handoffs/YYYY-MM-DD-HHMMSS-slug.md` |

> 핸드오프는 CLI별 홈 디렉터리가 아니라 프로젝트 안의 공통 디렉터리 `docs/handoffs/`를 사용합니다.
> Claude, Codex, Antigravity, Grok이 같은 프로젝트 핸드오프를 이어받기 위한 의도된 동작입니다.

## 저장 식별과 한계

두 셸 어댑터 모두 Node.js 저장기를 실행한다. `sessionId`와 함께 `eventId`, `messageId`, `promptId`, `turnId` 중 제공된 식별자를 사용해 지연 재전달을 걸러낸다. 이 식별자들은 선택 입력이다. [Grok 공식 훅 문서](https://docs.x.ai/build/features/hooks)가 모든 페이로드에서 이를 제공한다고 보장하지 않는다.

식별자가 없으면 직전 역할·내용과 입력 순번으로 연속 중복을 제거한다. 응답 후 같은 문장을 새로 입력하면 별도 턴으로 보존한다. 이 경우 과거 입력·응답 쌍 전체의 재전달과 동일한 새 대화는 구분할 수 없다. 세션 정보까지 없으면 다른 대화를 잘못 버리지 않도록 중복 제거를 하지 않는다.

파일 잠금으로 동시 저장을 직렬화하고 종료된 프로세스의 잠금은 회수한다. 인덱스 손상이나 잠금 시간 초과는 기존 오류 로그·`MNEMO_STRICT` 규칙을 따른다. 인덱스를 지우면 과거 이벤트의 중복 판정 근거가 사라지므로 일반 청소 대상으로 취급하지 않는다.

## 검색 규칙 (Grok 세션에서)

- 공통 규칙은 글로벌 `~/.claude/CLAUDE.md`, Grok 전용 차이는 [templates/grok-rules.md](templates/grok-rules.md)가 정본입니다. `grok inspect`에서 Claude rules·skills 호환과 실제 로드 경로를 확인합니다.
- `MEMORY.md` → 관련 기억 항목 → 연결 대화·`#tags:` → 대화 본문 순으로 검색합니다. 모든 CLI의 `conversations/*.md`를 함께 검색하고 태그가 없어도 본문을 확인합니다.
- 그래도 부족하면 프로젝트·시기를 좁혀 `~/.grok/sessions/**/updates.jsonl` 등 실제 원본 경로·형식을 확인하고 필요한 사용자·응답 텍스트만 읽기 전용으로 파싱합니다. 원본 전체와 비밀값은 출력하지 않습니다.
- 현재 이 모듈에는 세션 일괄 복구 CLI가 없습니다. Claude·Codex의 reconcile 도구를 Grok 원본에 적용하거나 Stop 훅을 복구 도구로 재실행하지 않습니다. 파싱할 수 없으면 확인 범위와 제한을 알립니다.
- `module_root`는 이번에 읽은 정확한 `SKILL.md`의 디렉터리입니다. 참조·스크립트는 이 경로를 기준으로 실행합니다.

## 프로젝트 저장 경계

기억·대화·핸드오프는 확정된 프로젝트 루트에 저장한다. 공통 규약은 소스의
`skills/mnemo/references/project-storage.md`, 설치 스킬의
`<module_root>/references/project-storage.md`에서 읽는다.

모든 어댑터와 핸드오프·복구 도구는 공통 `mnemo-project-root.js`를 사용한다.
Git 환경변수·하위 cwd로 저장 위치를 바꾸지 않으며, Git도 `.mnemo-root`도 없는
일반 cwd에는 자동 저장하지 않는다. 비-Git 프로젝트는 명시한 workspace에서
초기화한다. 설치 패키지에는 공통 핸드오프 `scripts/`도 포함된다. 소스 checkout의
핸드오프 도구 정본은 `skills/mnemo/scripts/`이다. 실행에는 Python 3와 Node.js가 필요하다.
Python 명령은 `python`·`py`·`python3` 중 `--version`이 되는 첫 것을 쓴다 — `python`만 실패했다고
Python 없음으로 판정하지 않는다(Windows 스토어 별칭, `references/handoff-memory.md` 3항).

## 프로젝트 스킬 자기개선

핸드오프 정제 또는 명시적 개선 작업에서는 [자기개선 계약](references/self-improvement.md)을 읽는다.
동봉된 내부 모듈을 직접 읽으며 별도 slash 등록이나 Jev API는 필요하지 않다.
핸드오프에서는 후보만 남기고, 승인된 개선 작업에서 실제 비교 검증을 수행한다.
