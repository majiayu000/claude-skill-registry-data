---
name: setup-global-config
description: >
  팀 공용 글로벌 에이전트 설정(CLAUDE.md / AGENTS.md)을 Claude Code와 Codex에 설치, 검증, 제거하는 스킬.
  두 대상에 byte-identical한 tool-agnostic 원칙을 적용하고 기존 사용자 설정은 backup으로 보호한다.
  "글로벌 설정 설치", "global config 설치", "공용 CLAUDE.md 설치", "팀 글로벌 규칙 적용",
  "global CLAUDE.md AGENTS.md 설치", "에이전트 공통 규칙 설치", "글로벌 설정 제거",
  "install global config", "setup global config", "uninstall global config" 등에서 트리거.
---

# setup-global-config

번들된 공통 원칙을 Claude Code와 Codex의 글로벌 지침 파일에 byte-identical하게 설치하거나 제거한다. 기존 사용자 설정을 먼저 비교하고 backup한 뒤 변경한다.

## 대상 파일

| 에이전트 | 설치 위치 | 비고 |
|----------|-----------|------|
| Claude Code | `~/.claude/CLAUDE.md` | 세션 시작 시 로드되는 글로벌 지침 |
| Codex | `~/.codex/AGENTS.md` | Codex가 읽는 글로벌 지침 |

사용자가 특정 에이전트만 지정하면 그 대상만 처리한다. 지정이 없으면 둘 다 처리한다. 설치된 모든 대상은 canonical과 byte-identical해야 한다.

## Canonical 소스

이 `SKILL.md`를 기준으로 `references/global-config.md`를 resolve한다. 설치된 대상 파일이나 다른 agent의 글로벌 파일을 source로 삼지 않는다.

Claude plugin runtime에서 같은 파일은 다음 경로다.

```text
${CLAUDE_PLUGIN_ROOT}/skills/setup-global-config/references/global-config.md
```

Canonical은 두 agent가 공통으로 해석할 tool-agnostic 원칙만 소유한다. Agent별 tool 호출, model alias, hook 동작, browser CLI command catalog는 넣지 않는다.

## 설치 절차

각 대상에 다음 절차를 적용한다.

1. Canonical 파일을 끝까지 읽고 source path를 고정한다.
2. 대상이 없으면 parent directory를 만든 뒤 canonical bytes를 그대로 복사한다.
3. 대상이 있으면 `cmp -s "$canonical" "$target"`으로 비교한다.
   - Exit `0`: 이미 설치됨. 변경하지 않는다.
   - Exit `1`: 차이를 요약하고 덮어쓰기 전에 사용자 승인을 받는다.
   - Exit `2`: path·permission 오류를 해결하거나 blocker로 보고한다.
4. 덮어쓰기가 승인되면 먼저 기존 파일을 `<target>.bak.<timestamp>`로 `cp -p` backup한다. Timestamp는 `date +%Y%m%dT%H%M%S`처럼 파일명에 안전한 형식을 쓴다.
5. Markdown을 재생성하지 말고 canonical 파일 자체를 복사한다.
6. 모든 대상에 `cmp -s "$canonical" "$target"`을 다시 실행한다. 하나라도 다르면 설치 성공을 보고하지 않는다.
7. Backup 경로와 검증 결과를 보고하고, 새 세션부터 적용된다고 안내한다.

## 역할 경계

Canonical 설치와 함께 다른 도구를 자동 설치하거나 설정하지 않는다.

- Git hook 설치·제거와 hook별 동작은 `setup-hooks` skill이 소유한다.
- Browser automation 절차는 설치된 browser skill과 현재 CLI의 live help가 소유한다.
- Model 선택, subagent runtime option, 질문 UI와 tool schema는 현재 agent platform의 설정과 tool instructions가 소유한다.
- Repo별 commit, test, deploy, worktree 절차는 가장 가까운 repo 지침이 소유한다.

## 제거 절차

1. 대상과 canonical을 `cmp -s`로 비교한다.
2. 대상이 canonical과 같으면 설치 전 backup 후보를 확인한다.
   - 복원할 backup이 명확하면 사용자에게 경로를 보여주고 복원한다.
   - 복원할 backup이 없으면 제거 요청 범위에서 대상 파일을 삭제한다.
3. 대상이 canonical과 다르면 설치 후 사용자 수정일 수 있으므로 삭제하거나 덮어쓰지 않는다. 차이와 `unresolved` 사유를 보고한다.
4. 복원 또는 삭제 결과를 filesystem inspection으로 검증한다.

## 검증

```bash
cmp -s "$canonical" "$target"
```

- 설치: 각 대상의 exit status가 `0`인지 확인한다.
- 제거: 대상이 사라졌거나 선택한 backup과 byte-identical한지 확인한다.
- Repo에서 이 skill을 수정할 때는 frontmatter, relative path, canonical의 machine-local absolute path 부재, README·marketplace 등록을 함께 확인한다.

## Gotchas

- `diff`가 비어 보이는 것과 byte identity는 다르다. Newline·encoding 차이를 포함해 `cmp`로 최종 판정한다.
- 기존 대상이 다를 때 install 요청만으로 overwrite 승인을 추론하지 않는다. 사용자 작성 글로벌 규칙을 잃을 수 있으므로 backup 전 차이를 보여준다.
- Backup 없이 overwrite하거나, 수정된 대상 파일을 uninstall 과정에서 삭제하지 않는다.
- `~/.claude/CLAUDE.md`와 `~/.codex/AGENTS.md`는 현재 세션에 소급 적용되지 않는다. 새 세션에서 확인한다.
- Tracked 문서에 실제 machine-local absolute path를 기록하지 않는다.
