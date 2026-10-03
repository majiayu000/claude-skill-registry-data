---
name: antigravity-mnemo
description: Install, remove, or diagnose Mnemo long-term conversation memory for Google Antigravity CLI using its global Stop hook and GEMINI.md rules.
---

# Antigravity Mnemo

Installs the Antigravity-specific Mnemo adapter without changing project files.

## Commands

```bash
node "<module_root>/install.js"
node "<module_root>/install.js" --check
node "<module_root>/install.js" --uninstall
```

Resolve `module_root` as the directory containing this exact `SKILL.md`; do not assume the repository is the
current working directory.

`ANTIGRAVITY_HOME` may point to an isolated replacement for `~/.gemini` during testing.

## Managed assets

- `~/.gemini/config/hooks/olympus-save-turn.js`
- named entry `olympus-antigravity-mnemo` in `~/.gemini/config/hooks.json`
- marked rules block in `~/.gemini/GEMINI.md`

The installer also migrates Olympus-managed Gemini CLI Mnemo assets. Unmodified legacy files are removed; modified files are preserved under `~/.gemini/_olympus-preserved/`.

## Runtime contract

The Stop hook reads Antigravity's `transcriptPath`, stores the latest user and model turn in `conversations/YYYY-MM-DD-antigravity.md`, redacts `<private>` blocks, and always permits the Stop event.

## Rules and past-work lookup

The global policy source is [templates/gemini-md-rules.md](templates/gemini-md-rules.md): respond in the request's language, use code maps before broad code searches, and search `MEMORY.md` → relevant memory entries → conversation links/tags → conversation text. Preserve native Antigravity workflows and use Olympus only for their documented additional deliverables.

If these sources are insufficient, narrow the project and time range and confirm the actual source transcript path and format. `hooks/save-turn.js` exports `latestTurn(payload)` for read-only extraction of the latest user/model pair; it is not a full-history recovery command. Earlier turns require scoped, read-only parsing of user/model text. Never call `appendTurn` or replay the Stop hook for a read-only request, and never load an entire transcript into context or claim an unavailable recovery command succeeded.

Use `--check` after installation. A failed check means the adapter is not verified; do not report Mnemo as active.

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
