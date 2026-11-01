---
name: harness
description: 프로젝트의 AI 도구 설정(AGENTS.md, CLAUDE.md, docs, rules, skills, hooks, agents)을 채우거나 바꿀 때 쓴다. `미정`이 남은 첫 세션, 또는 사용자가 규칙 · 절차 · 금지 사항 · 자동화를 추가 · 변경 · 삭제하라고 할 때.
---

# 프로젝트 설정 채우기 · 바꾸기

이 템플릿에는 뼈대만 있고 답은 없다. 프로젝트의 답은 코드와 사용자 설명에서만 가져온다. 다른 프로젝트의 관습이나 아래 표의 예시를 기본값으로 채우지 않는다.

## 1. 처음 채우기 (`미정`이 남았을 때)

1. 코드를 읽는다. README, 의존성 파일(`package.json`, `requirements.txt` 등), 폴더 트리, `git remote`, 기존 코드의 스타일. 읽어서 알 수 있는 것은 묻지 않고 채운다.
2. 못 읽은 것만 사용자에게 한 번에 묻는다. 답을 못 정한 항목은 `미정`으로 남긴다.

   | 항상 묻는 것 | 담을 곳 |
   |---|---|
   | 무엇을 만드나, 누가 쓰나 | `AGENTS.md` 소개, `docs/ROADMAP.md` 1번 |
   | 핵심 흐름 (입력 → 처리 → 결과) | `docs/ROADMAP.md` 2번 (Mermaid) |
   | 진행 방식은 `docs/rules/workflow.md` 1번의 기본값(변경 전 계획과 승인, 변경 뒤 검수와 한 줄 보고, 삭제는 확인, master / main 제외)을 알려주고, 바꿀 것만 묻는다 | `docs/rules/workflow.md` 1번 |

3. 해당하는 주제만 추가로 묻는다. 프로젝트에 없는 주제는 묻지 않는다.

   | 주제 | 묻는 것 | 담을 곳 |
   |---|---|---|
   | 구조 | 폴더를 나누는 기준, 계층 | `docs/rules/code.md`, `docs/ARCHITECTURE.md` 1번 |
   | 스타일 | 쓰는 언어 (`docs/rules/style.md` 1번 표에서 그 언어의 줄만 남긴다), 번호 박스 헤더를 켤지 (기본은 쓰지 않음. 켜면 `style.md` 2번의 "켠 언어"에 적는다), 이름 규칙 | `docs/rules/style.md` |
   | 설정값 | 어디에 두나, 비밀값은 | `docs/rules/config.md` |
   | 예외 · 로깅 | 실패를 어떻게 다루고 무엇을 남기나 | `docs/rules/errors.md` |
   | 보안 | 인증 방식, 외부 입력, 비밀값 | `docs/rules/security.md` |
   | 데이터 | 저장소, 스키마를 바꾸는 방법 | `docs/rules/data.md` |
   | 화면 | 폴더 기준, 상태 관리 | `docs/rules/ui.md` |
   | 테스트 · 배포 | 방법과 순서 | `skills/verify`, `skills/deploy` |

4. 채운다.
   - 프로젝트 전체에서 `{{`와 `미정`을 검색해서 나온 곳을 모두 채운다 (`AGENTS.md` 또는 `CLAUDE.md`, `docs/`(rules 포함)). skill 파일에는 프로젝트 값이 없으므로 고치지 않는다 (Codex 샌드박스는 `.agents/`를 보호 경로로 다룬다).
   - 사용자가 답한 주제는 3번 표의 위치에 파일로 만든다. 사용자가 한 답만 규칙으로 쓴다.
   - `AGENTS.md`의 규칙 표에 그 규칙을 읽는 때(어떤 파일을 만질 때인지)를 적는다.
   - `.gitignore`는 파일을 새로 쓰지 않고 필요한 줄만 더한다. `# keelkit` 아래 줄은 지우지 않는다.
   - `.gitignore`에 `.env`가 없으면 추가한다. `.env`는 하나만 쓰므로 `.env.*`는 추가하지 않는다. 이미 추적 중인 `.env*` 파일이나 `.env.example` 같은 파일이 있으면 사용자에게 알린다 (합치거나 추적 해제하는 것은 삭제이므로 확인을 받는다).
   - `docs/SETUP.md` 3번에는 `.env`의 키 이름만 적는다. `.env`는 열어서 읽지 않고 `grep -oE '^[A-Za-z_][A-Za-z0-9_]*' .env`로 키 이름만 뽑는다 (값이 출력에 섞이지 않게).
5. 마무리한다. `미정`이 남은 곳을 검색해서 사용자에게 알리고, `AGENTS.md` 0번 절을 지운다. 무엇을 어디에 채웠는지 표로 보고한다. `gh --version`과 `gh auth status`로 `gh` 준비를 확인하고, 없으면 설치(`winget install GitHub.cli`)와 `gh auth login`을 사용자가 직접 하도록 안내한다. 보고 끝에 GitHub 저장소 설정(Settings → General → Automatically delete head branches)을 켜 두면 병합 즉시 원격 feature 브랜치가 자동 삭제된다고 안내한다. 같은 화면 Pull Requests 섹션에서 merge commit과 squash의 Default commit message를 Pull request title and description으로 바꿔 두면, 사용자가 `dev` → `main` PR을 병합할 때 병합 창에 PR 제목과 본문이 채워진다고 안내한다 (설정하지 않으면 `Merge pull request #N from ...`만 나온다). 설정은 사용자가 직접 바꾼다.

## 2. 나중에 바꾸기 (규칙 · 절차 · 금지 · 자동화 요청)

사용자가 말한 내용을 아래 표로 분류해서 알맞은 칸에 넣는다.

| 사용자가 말한 것 | 넣을 곳 |
|---|---|
| 매번 알아야 하는 사실 (소개, 자주 쓰는 명령) | `AGENTS.md` |
| 특정 주제 / 경로에서만 지킬 규칙 | `docs/rules/<주제>.md` + `AGENTS.md` 표에 읽는 때 추가 |
| 여러 단계로 된 절차 (배포, 릴리스) | `.claude/skills/<이름>/SKILL.md`와 `.agents/skills/<이름>/SKILL.md` (같은 내용으로 둔다) |
| 절대 어기면 안 되는 것 | `.claude/hooks/` + `settings.json` 연결 (부탁이 아니라 동작 차단. Claude 전용이고 Codex는 아직 지원하지 않는다) |
| 출력이 긴 작업 (테스트, 빌드) | `.claude/agents/<이름>.md` |
| 권한 (허용 / 금지 명령) | `.claude/settings.json` |

넣기 전에 확인한다.

- 같은 내용이 이미 있으면 새로 만들지 않고 그 파일을 고친다. 같은 내용은 원본 한 곳에만.
- 기존 규칙과 충돌하면 어느 쪽이 맞는지 사용자에게 묻는다.
- 규칙 파일은 주제 하나당 하나. 이름은 스택이 아니라 주제로 짓는다.
- hook은 사용자가 "반드시", "절대"라고 말한 것에만 제안한다. 만든 뒤 실제로 막히는지 확인한다.
- 사용자 설명이 모호하면 추측하지 않고 묻는다.

바꾼 뒤에 한다.

- `AGENTS.md`의 규칙 표에 파일과 읽는 때를 반영한다. 200줄 안을 지킨다.
- 방향이나 구조가 바뀌면 `docs/ROADMAP.md` 4번(결정 기록)에 "무엇을, 왜"를 한 줄 적고, `docs/ARCHITECTURE.md`도 고친다.
- 무엇을 어디에 넣었는지 한 줄씩 보고한다.