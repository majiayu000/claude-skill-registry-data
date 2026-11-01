---
name: init
description: 현재 폴더에 keelkit 설정(CLAUDE.md 또는 AGENTS.md, .claude/ 또는 .agents/, docs/)을 설치한다. 기존 프로젝트에 같은 기능이 이미 있는지 먼저 확인해 겹치는 것은 기존을 유지하고, 겹치지 않는 것만 설치한 뒤 프로젝트 내용을 채운다. 새 프로젝트를 시작하거나 기존 프로젝트에 keelkit을 붙일 때 쓴다.
disable-model-invocation: true
---

# keelkit 설치

Claude Code와 Codex 플러그인이 이 파일을 함께 쓴다. 아래 `${CLAUDE_PLUGIN_ROOT}`는 플러그인 루트이고, Codex에서는 이 `SKILL.md`가 있는 폴더의 두 단계 위(`../..`, `scripts/`가 있는 폴더)로 읽는다. Claude 전용 명령(`claude plugin list`)은 Claude에서만 쓴다.

현재 폴더(프로젝트 루트)에 keelkit을 설치하고, 기존 것과 겹치는 기능을 정리하고, 프로젝트에 맞게 채운다. 기존 내용은 삭제하거나 요약하지 않는다.

원칙: 같은 기능은 한 곳에만 둔다. 겹치면 기존을 유지하고 keelkit 쪽을 설치하지 않는다. 사용자가 고른 것만 바꾼다. 설치한 뒤에 "겹쳤으니 고쳐 달라"는 말이 나오지 않게, 쓰기 전에 정한다.

## 1. 확인

현재 폴더가 프로젝트 루트인지 본다. 홈 폴더나 `~/.claude`이면 사용자에게 알리고 멈춘다.

Claude와 Codex가 같은 규칙과 docs를 쓰도록 항상 둘 다 설치한다. 도구를 고르는 질문은 하지 않는다.

## 2. 미리보기

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/install.py" --dry-run
```

`python`이 없으면 `python3`을 쓴다. 이 단계는 아무것도 쓰지 않는다. "직접 합쳐야 함"으로 나온 파일은 경로가 같은데 내용이 다른 것이다. 3번에서 같이 본다.

## 3. 겹치는 기능 찾기 (기능 단위)

파일 이름이 달라도 같은 일을 하는 규칙, skill, hook이 있으면 겹친 것이다. 아래 표의 기능마다 "기존에서 찾을 곳"을 직접 읽고 판정한다. 읽는 순서는 `CLAUDE.md`, `AGENTS.md` → `.claude/rules` → `.claude/skills`, `.agents/skills`, `.claude/agents` → `.claude/hooks`, `.claude/settings.json`, `.codex/` → `docs/`, `README`, `CONTRIBUTING.md` → `.husky`, `.git/hooks`, `.pre-commit-config.yaml`, `.github/` 순이다. 아래 표의 `CLAUDE.md`는 `AGENTS.md`도, skill은 `.agents/skills/`도, hook과 설정은 `.codex/`도 포함한다. `.husky` 이하는 근거로만 읽고 고치지 않는다.

| # | 기능 | keelkit 쪽 | 기존에서 찾을 곳 | 건너뛰는 방법 |
|---|---|---|---|---|
| 1 | 진행 방식 (계획 후 진행, 권한) | `docs/rules/workflow.md` 1절 첫 행, `settings.json`의 `allow` | `CLAUDE.md`, rules, `settings.json`의 `permissions` | 설치 뒤 `workflow.md` 행을 빼고, `settings.json`에 더해진 `allow` 항목을 백업 원본대로 되돌린다 |
| 2 | 삭제 확인 | `guard.py` 검사 `delete`, `workflow.md` 삭제 행 | hook, `settings.json`, `CLAUDE.md` | `guard.py`의 `DISABLED`에 `delete`, `workflow.md` 행 제거 |
| 3 | master / main 보호 | `guard.py` 검사 `protected`, `workflow.md` 행 | hook, `.husky/pre-push`, `.git/hooks`, `CLAUDE.md` | `DISABLED`에 `protected`, `workflow.md` 행 제거 |
| 4 | `.env` 보호 | `guard.py` 검사 `env`, `workflow.md` 환경변수 행 | hook, `.gitignore`, `CLAUDE.md` | `DISABLED`에 `env`, `workflow.md` 행 제거 |
| 5 | Co-Authored-By 금지 | `guard.py` 검사 `coauthor` | hook, `.husky/commit-msg`, `CLAUDE.md` | `DISABLED`에 `coauthor` |
| 6 | 브랜치 · 커밋 · PR · 병합 절차 | `skills/commit-pr` | skill, `CLAUDE.md`, `CONTRIBUTING.md`, `.husky/commit-msg`, commitlint, `.github/` PR 템플릿 | `--skip .claude/skills/commit-pr .agents/skills/commit-pr` (없는 쪽은 무시된다) |
| 7 | 구현 후 검증 | `skills/verify` | skill, `CLAUDE.md` | `--skip .claude/skills/verify .agents/skills/verify` (없는 쪽은 무시된다) |
| 8 | 긴 출력 실행 요약 | `agents/runner` | agent | `--skip .claude/agents/runner.md` |
| 9 | 큰 PR 검토 | `agents/reviewer` | agent, skill | `--skip .claude/agents/reviewer.md` |
| 10 | 코드 구조 · 같이 고칠 문서 | `docs/rules/code.md` | `.claude/rules`, `docs/rules`, `CLAUDE.md`, `AGENTS.md` | `--skip docs/rules/code.md` |
| 11 | 주석 규칙 | `docs/rules/style.md` | `.claude/rules`, `docs/rules`, `CLAUDE.md`, `AGENTS.md` | `--skip docs/rules/style.md` |
| 12 | 문서 구조 | `docs/rules/docs.md`, `docs/ROADMAP.md`, `ARCHITECTURE.md`, `SETUP.md` | `docs/`, `README`, rules | 파일마다 `--skip` (예: `--skip docs/SETUP.md`) |
| 13 | 압축(compact) 규칙 | `workflow.md` 3절 | `CLAUDE.md`, rules | 설치 뒤 3절 제거 |
| 14 | 파일 끝 빈 줄 제거 | `hooks/strip_eof.py` | hook, `.editorconfig` | `--skip .claude/hooks/strip_eof.py` (`settings.json`에서 그 hook도 빠진다) |
| 15 | 설정 채우기 · 변경 | `skills/harness` | skill | `--skip .claude/skills/harness .agents/skills/harness` (없는 쪽은 무시된다) |
| 16 | hook 우회 차단 (`--no-verify` 등) | `guard.py` 검사 `noverify`, `workflow.md` 공통 항목 | hook, `.husky`, `CLAUDE.md` | `DISABLED`에 `noverify` |

판정은 세 가지다.

| 판정 | 뜻 | 기본 처리 |
|---|---|---|
| 없음 | 기존에 같은 기능이 없다 | keelkit을 설치한다 |
| 겹침 · 내용 같음 | 같은 기능이고 규칙 내용이 같다 | 기존을 유지한다 |
| 겹침 · 내용 다름 | 같은 기능이지만 규칙이 다르다 (예: 커밋 형식이 `feat:` 대 `ADD`) | 기존을 유지한다. 사용자에게 묻는다 |

겹침인지 애매하면 "겹침 · 내용 다름"으로 두고 근거(파일과 줄)를 적는다. 추측으로 "없음"을 고르지 않는다.

## 4. 표로 보여주고 묻기 (설치 전)

설치하기 전에 모든 기능을 번호를 붙인 표 하나로 보여준다. 겹침도 없음도 모두 번호가 있다. 형식은 이렇다.

```
겹침 · 내용 다름 (기본값: 기존 유지)
1. 커밋 제목 형식: 기존 `feat:` (.husky/commit-msg:3) / keelkit `ADD`

겹침 · 내용 같음 (기본값: 기존 유지)
2. .env 보호: .claude/hooks/block_env.py
3. 삭제 확인: docs/rules/workflow.md

없음 (keelkit 설치)
4. master / main 보호
5. 구현 후 검증

바꿀 번호가 있으면 알려 주세요. 예: "1번, 3번 keelkit으로". 없으면 "그대로".
```

- 표 아래에 번호로 답하게 한다. 선택지 UI는 쓰지 않는다. 답은 한 번만 받는다.
- 기본값은 항상 기존 유지다. 사용자가 "그대로"라고 하면 기본값으로 진행한다.
- "N번 keelkit으로"는 그 기능을 keelkit 것으로 바꾼다는 뜻이다. 내용이 같아도 된다. "전부 keelkit으로"도 같다.
- 바꾸기 전에 사용자에게 지울 대상(파일이나 절)을 알리고 한 번 더 확인을 받는다. 백업은 `.keel-backup/`에 남는다.
- 겹침이 하나도 없으면 표 없이 "겹치는 기능 없음"으로 알리고 5번으로 간다.

## 5. 설치

기능마다 3번 표의 "건너뛰는 방법"을 따른다.

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/install.py" --skip <경로> <경로>
```

- 기존 유지로 정한 기능의 파일은 `--skip`에 넣는다. 건너뛴 파일은 만들지 않고 백업도 하지 않는다.
- 사용자가 "harness는 생략해", "harness 단계는 건너뛰어"라고 하면 7번 채우기 단계만 생략한다는 뜻이다. `harness` skill 파일(`.claude/skills/harness`, `.agents/skills/harness`)은 `--skip`에 넣지 않고 항상 설치한다. 기존 harness skill을 유지하겠다고 분명히 말했을 때만 `--skip`에 넣는다.
- `guard.py`는 파일을 합치지 않는다. 방금 만든 파일의 맨 위 `DISABLED = set()`에 끌 검사 ID를 넣는다 (예: `DISABLED = {"env", "delete"}`). 기존 hook 코드는 건드리지 않는다. 고친 뒤 `python -m py_compile .claude/hooks/guard.py`로 확인한다.
- `workflow.md`처럼 한 파일에 여러 기능이 들어 있으면, 기존 유지로 정한 기능의 행이나 절만 방금 만든 그 파일에서 뺀다.
- 사용자가 keelkit으로 바꾸기로 한 기능은 `.keel-backup/<시각>/original/`에 기존 것을 복사해 두었는지 확인한 뒤, 기존 쪽의 해당 규칙을 지우고 keelkit 것을 둔다.
- 스크립트가 `.gitignore`에 `.env`, `.keel-backup/`, `docs/`와 설정 경로(`CLAUDE.md`, `.claude/`, `AGENTS.md`, `.agents/`, `.codex/`)를 넣는다. 이미 git이 추적 중인 경로는 넣지 않고 출력에 알린다. 그 경로가 있으면 사용자에게 알린다.
- 설치 뒤에 `.gitignore`를 고치거나 다른 템플릿(스타터 등)의 `.gitignore`와 합칠 때도 `# keelkit` 아래 줄은 지우지 않고 그대로 둔다. 파일을 통째로 새로 쓰지 말고 필요한 줄만 더한다. 그 줄을 지우면 설치 경로가 커밋된다. 지우는 것은 사용자가 요청할 때만 한다.
- `guard.py`의 검사(표의 3, 4, 5, 16번)는 Claude의 `.claude/hooks`와 Codex의 `.codex/hooks`가 같은 규칙으로 막는다. Codex 어댑터(`.codex/hooks/guard.py`)는 `.claude/hooks/guard.py`를 불러 쓰므로 `DISABLED`도 같이 적용된다. 삭제 확인(2번)은 Codex hook이 지원하지 않고, 끝 빈 줄 제거(14번)는 Claude에서만 동작한다. 이 둘은 Codex에서 규칙 문장(`docs/rules/workflow.md`)으로만 지켜진다고 사용자에게 알린다.
- `.codex/hooks.json`이 이미 있으면 JSON으로 합쳐서 기존 hook을 유지한다.
- 스크립트는 `.claude/settings.json`을 JSON으로 더한다. 1번을 기존 유지로 정했다면, 더해진 `allow` 항목을 백업 원본(`original/.claude/settings.json`)과 비교해서 되돌린다.
- `AGENTS.md`의 `규칙과 절차` 표와 `Codex 설정` 표, `CLAUDE.md`의 `Claude 전용 설정` 표에서 건너뛴 기능의 행은 뺀다. 없는 파일을 가리키지 않게 한다. 기존 기능을 유지했다면 행을 빼지 말고 기존의 실제 위치(파일과 절)를 가리키게 고친다.

## 6. 남은 충돌 합치기

5번을 거친 뒤에도 "직접 합쳐야 함"으로 남은 파일이 있으면, 파일마다 `.keel-backup/<시각>/original/<경로>`(기존)와 `incoming/<경로>`(keelkit)를 읽고 프로젝트의 실제 파일에 합친다. 같은 내용은 기존 표현을 유지하고 keelkit 쪽을 넣지 않는다. 기존에 없는 것만 더한다.

| 대상 | 합치는 방법 |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | 기존 본문을 그대로 두고, 기존에 없는 keelkit의 0번 절, `규칙과 절차`, `Claude 전용 설정`, `문서` 표만 추가한다 |
| `docs/*.md` | 기존 내용을 유지하고, keelkit 뼈대에 있고 기존에 없는 절만 `미정`으로 추가한다 |
| `docs/rules/*.md`, `.claude/rules/*.md` | 4번에서 정한 대로 한다. 4번에 없던 어긋남이 새로 보이면 사용자에게 묻는다 |
| `.claude/hooks/*.py` | 기존 검사를 유지한다. 같은 검사를 두 번 넣지 않는다 |
| skill, agent | 4번에서 정한 대로 한다. 같은 이름이면 keelkit의 내용 중 없는 부분만 합친다 |

합칠 수 없는 항목은 그대로 두고 보고한다.

## 7. 채우기

프로젝트의 `.claude/skills/harness/SKILL.md`(Codex에서는 `.agents/skills/harness/SKILL.md`)를 읽고 1번 절차를 그대로 따른다. 기존 `README`, `AGENTS.md`, 문서, 의존성 파일에서 읽을 수 있는 것은 먼저 읽어서 `{{변수}}`와 `미정`을 채우고, 못 읽는 것만 사용자에게 한 번에 묻는다. 사용자가 채우기를 생략하라고 했으면 이 절은 생략하고 `{{`와 `미정`은 그대로 둔다고 알린다. 기존 harness skill을 유지해서 `harness`가 설치되지 않았으면 `{{`와 `미정`을 직접 채운다.

## 8. 마무리

- 기능별 결과를 한 표로 알린다: 기존 유지, 새로 설치, 교체, 직접 확인 필요.
- 남은 `{{`와 `미정` 위치를 목록으로 알린다.
- 백업 폴더 `.keel-backup/`은 합친 결과를 확인한 뒤 사용자가 지운다 (삭제는 확인을 받는다).
- hook과 권한은 새 Claude 세션부터 적용된다고 알린다. `init`을 돌리기 전에 폴더를 바꿨다면 새 세션을 열어야 hook 경로가 맞는다.
- Codex hook은 사용자가 신뢰하기 전에는 꺼져 있고, 꺼져 있어도 경고가 없다고 반드시 알린다. Codex에서 프로젝트 폴더를 신뢰한 뒤 `/hooks`에서 keelkit guard를 검토하고 신뢰해야 켜진다. hook 파일이 바뀌면(플러그인 업데이트 포함) 다시 신뢰해야 한다.
- `.claude/skills/`와 `.agents/skills/`는 같은 내용의 복사본이다. 한쪽을 고치면 다른 쪽도 같이 고친다고 알린다.
- keelkit이 설치한 경로는 `.gitignore`에 들어간다. 저장소에 올리려면 사용자가 그 줄을 지운다.
