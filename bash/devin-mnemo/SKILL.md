---
name: devin-mnemo
description: Devin CLI의 프로젝트별 Mnemo 대화 저장, 검색, 설치 상태를 설정하거나 진단할 때 사용한다. Devin 훅과 로컬 세션 DB를 공통 MEMORY.md·conversations/ 저장소에 연결한다.
---

# Devin-Mnemo

Devin CLI 3000.11.3에서 확인한 로컬 어댑터다. Devin이 읽는 프로젝트 `AGENTS.md`와 Claude 호환 Mnemo 규칙은 재사용한다. 이 모듈은 Devin 전용 훅과 대화 저장만 추가한다.

```bash
node "<module_root>/install.js"             # 설치
node "<module_root>/install.js" --check     # 설정·파일 진단
node "<module_root>/install.js" --uninstall # 이 어댑터가 추가한 항목 제거
```

Devin의 `UserPromptSubmit`은 사용자 입력을 제공하지만 [공식 Stop 페이로드](https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks)에 응답 본문은 명시되지 않는다. Windows 실측 경로 `%APPDATA%/devin/cli/sessions.db`의 `message_nodes`에서 현재 세션·턴 이후의 assistant 본문만 읽는다. Python 3와 Node.js가 필요하다. 로컬 DB가 없거나 형식이 달라지면 사용자 입력만 남을 수 있으므로 실제 Devin 턴으로 확인한다. 저장 실패는 Devin 턴을 차단하지 않는다.

- 저장: `conversations/YYYY-MM-DD-devin.md`, `MEMORY.md`, `memory/`. `<private>...</private>` 본문은 `[PRIVATE]`로 바꾼다. `MNEMO_DISABLE=1`이면 저장하지 않는다.
- 프로젝트 루트: 공통 `mnemo-project-root.js`를 사용한다. Git 루트나 Devin이 명시한 workspace만 기록한다. CLI 설정 홈은 기록 대상이 아니다.
- 검색: 공통 Mnemo 규칙에 따라 `MEMORY.md` → 관련 기억 → `conversations/*-devin.md`와 다른 CLI 로그 → 필요한 원본 세션 순서로 확인한다. 원본 DB는 읽기 전용으로 필요한 세션만 조회한다.
- 설치 위치: [Devin 공식 훅 설정](https://docs.devin.ai/cli/extensibility/hooks/overview)에 따라 Windows는 `%APPDATA%/devin/config.json`, macOS·Linux는 `~/.config/devin/config.json`의 `hooks`를 사용한다. 글로벌 `AGENTS.md`에는 Devin 전용 차이만 관리 블록으로 넣는다.
- 검증: `--check`는 설정 정적 검사다. Devin `/hooks`에서 로드 여부를 보고, 한 테스트 턴 후 `conversations/*-devin.md`의 User·Assistant 한 쌍을 확인해야 런타임 저장을 PASS로 판단한다.
