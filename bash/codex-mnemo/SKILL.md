---
name: codex-mnemo
description: Codex CLI 과거 대화 검색과 장기기억 설정에 사용한다. notify 훅으로 대화 자동 저장, 키워드 태깅, 과거 검색을 제공한다. /mnemo, 므네모, 장기기억, 기억해, 이전에, handoff, 핸드오프, 세션 저장, codex 기억, codex memory 요청에 사용한다.
---

# Codex-Mnemo - Codex CLI 기억 시스템

> 기억의 여신 Mnemosyne에서 유래. Claude Code용 Mnemo를 Codex CLI에 이식.

Codex CLI 세션 간 컨텍스트 유지를 위한 장기기억 시스템입니다.

## 설치

```bash
node skills/codex-mnemo/install.js              # 설치
node skills/codex-mnemo/install.js --check      # 설치/notify 진단
node skills/codex-mnemo/install.js --uninstall  # 제거
```

---

## Claude Code Mnemo와의 차이

| | Claude Code (Mnemo) | Codex CLI (Codex-Mnemo) |
|---|---|---|
| 훅 | 2개 (UserPromptSubmit + Stop) | **1개** (notify: agent-turn-complete) |
| 데이터 전달 | stdin JSON + transcript JSONL 파싱 | **notify payload(JSON)** (argv/stdin/파일경로 모두 처리) |
| 설정 | settings.json (JSON) | **config.toml** (TOML) |
| 규칙 파일 | CLAUDE.md | **AGENTS.md** |
| 저장 경로 | `conversations/*-claude.md` | **`conversations/*-codex.md`** |
| 중복 방지 | 타임스탬프 기반 | **turn-id 기반** (더 정확) |

---

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **빠르게** | 기본은 훅에서 AI 호출 금지. 단, Chronos auto-continue는 예외 체인 |
| **단순하게** | 파일 기반, DB 없음 |
| **검색 가능하게** | 키워드 + 동의어 확장 |

전역 작업 규칙의 정본은 [templates/agents-md-rules.md](templates/agents-md-rules.md)이며,
설치기가 `<CODEX_HOME>/AGENTS.md`의 `CODEX-MNEMO` 관리 블록에 반영합니다.
요청 언어로 응답하고 코드맵을 우선 조회하며, 과거 검색은 메모리 → 대화 링크·태그 → 본문
→ 원본 세션 파싱·복구 순서입니다. 정확한 검색·기억·핸드오프 정책이 필요할 때 정본을 읽습니다.
읽기 전용 요청에서는 복구 파일을 쓰지 않습니다. `--dry-run`은 복구 후보의 집계를 확인하는
옵션이며 대화 본문을 출력하는 검색 기능으로 간주하지 않습니다.

---

## 포함 파일

```
codex-mnemo/
├── SKILL.md                     # 이 파일
├── install.js                   # 설치/제거 스크립트
├── hooks/
│   ├── save-turn.ps1            # Windows notify 오케스트레이터 (+ Chronos optional chain)
│   ├── append-user.ps1          # User 저장 전담
│   ├── append-assistant.ps1     # Assistant 저장 전담
│   ├── save-turn.sh             # Linux/Mac notify 오케스트레이터 (+ Chronos optional chain)
│   ├── append-user.sh           # User 저장 전담
│   └── append-assistant.sh      # Assistant 저장 전담
├── scripts/
│   └── reconcile_codex_conversations.py  # rollout JSONL → conversations/ 복구
└── templates/
    └── agents-md-rules.md       # AGENTS.md 주입 규칙
```

---

## Reconcile (누락 턴 복구)

Codex의 notify 훅이 한 번이라도 실패하거나 Codex CLI가 강제 종료되면 해당 턴의
`conversations/YYYY-MM-DD-codex.md` 미러링이 유실됩니다. 그러나 rollout JSONL
(`<CODEX_HOME>/sessions/YYYY/MM/DD/rollout-*.jsonl`)은 Codex가 직접 기록하는 source of truth
이므로, `reconcile_codex_conversations.py`가 이를 스캔해 누락된 turn을 자동 복구합니다.

여기서 `<CODEX_HOME>`은 `CODEX_HOME` 환경 변수 값이며, 미설정 시 `~/.codex`입니다.

**Dedup 키**: Codex rollout 라인에는 uuid가 없으므로 `sha1(timestamp + role + content[:200])`
조합을 키로 사용하며, `conversations/.mnemo-index.json`의 `codex` 네임스페이스에 저장됩니다.
Claude 인덱스(`claude` 네임스페이스)와 충돌하지 않습니다.

**자동 실행**: Claude Code의 `SessionStart` 훅(`reconcile-conversations.ps1/.sh`)이
오늘자 날짜에 대해 Claude + Codex 두 CLI를 모두 복구합니다.

**수동 실행**:
```bash
python skills/codex-mnemo/scripts/reconcile_codex_conversations.py              # 오늘자
python skills/codex-mnemo/scripts/reconcile_codex_conversations.py --all        # 전체 기간
python skills/codex-mnemo/scripts/reconcile_codex_conversations.py --dry-run    # 시뮬레이션
python skills/codex-mnemo/scripts/reconcile_codex_conversations.py --project-root D:/git/foo
```

---

## 동작 흐름

```
Codex CLI 대화
    ↓
[notify: agent-turn-complete]
    → JSON 페이로드 수신 (argv/stdin/파일경로)
    → save-turn(오케스트레이터)에서 역할 분리 호출
      → MEMORY.md + memory/*.md scaffold 자동 생성(없을 때만)
      → append-user: User 입력 저장
      → append-assistant: Assistant 응답 저장(전체)
    → conversations/YYYY-MM-DD-codex.md에 append
    → turn-id 기반 중복 방지
    → (optional) auto-continue-loop 설치 시 continue-loop 호출
      → loop-state.md 확인
      → 미완료면 background `codex exec resume --last`
```

---

## 저장 위치

| 파일 | 위치 |
|------|------|
| 대화 로그 | `conversations/YYYY-MM-DD-codex.md` |
| 의미기억 | `MEMORY.md` (프로젝트 루트) |
| 훅 | `<CODEX_HOME>/hooks/save-turn.ps1\|.sh` |
| 설정 | `<CODEX_HOME>/config.toml` |
| 규칙 | `<CODEX_HOME>/AGENTS.md` |
| 핸드오프 | 공통 프로젝트 경로 `docs/handoffs/YYYY-MM-DD-HHMMSS-slug.md` |

> 핸드오프는 CLI별 홈 디렉터리가 아니라 프로젝트 안의 공통 디렉터리 `docs/handoffs/`를 사용합니다.
> Claude, Codex, Antigravity가 같은 프로젝트 핸드오프를 이어받기 위한 의도된 동작입니다.
> 핸드오프 작성 시 Mnemo의 공통 품질 계약을 따른다: `Feature/Flow/Decision Snapshot`에 구현 기능 목록,
> 구성도, 기능 경계, 입력→처리→저장→표시 흐름, 주요 결정/대안/근거를 남긴다. CodeMap은 TermSnap 산출물이므로
> 핸드오프는 CodeMap을 대체하지 않고 현재 세션의 구현 근거와 구성도를 작성한다.

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
