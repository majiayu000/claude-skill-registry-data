---
name: agent-native-audit
description: >
  대상 프로젝트가 "agent-native"한 정도를 7개 축(Action Parity, Tool Primitives,
  Doc Coverage, Hook Coverage, Log Access, Workflow Coverage, Knowledge Capture)으로
  점수화하고 개선 추천을 P1/P2/P3로 정리한다.
  "이 프로젝트 agent-native 점검", "agent 친화 감사", "agent-native audit",
  "claude code 적합성 점검", "AGENTS.md 점검", "이 레포 agent에 최적화돼 있어?",
  "claude 친화 진단", "에이전트 적합성", "이 프로젝트 onboarding 점검",
  "audit this repo for agents", "agent readiness" 등에서 트리거.
  대상 경로 미지정 시 현재 디렉토리를 점검한다.
---

# Agent-Native Audit

대상 프로젝트가 자율 에이전트(Claude Code/Codex 등)에 얼마나 친화적인지 7개 축으로 점수화하고, 개선 우선순위를 결정 가능한 형태로 보고한다.

`setup-hooks`, `statusline` 같은 단편 인프라 스킬과 달리 *전체 점검*을 수행한다. 새 프로젝트 onboarding이나 기존 레포의 agent-readiness 확인에 사용.

## 점검 대상

- 인자로 경로가 주어지면 그 경로.
- 없으면 현재 작업 디렉토리.
- 단, git 레포 루트가 아니면 가장 가까운 `.git` 상위 디렉토리로 자동 보정.

## 점검 7축

각 축 0–3점. 합계 21점.

| 점수 | 의미 |
|------|------|
| 0 | 부재 또는 의도와 반대 작동 |
| 1 | 부분적 / 일관성 없음 |
| 2 | 작동하지만 사각지대 있음 |
| 3 | 완성도 높음, 사각지대 거의 없음 |

### 1. Action Parity

사람이 UI/manual로 하는 일을 agent가 CLI/script로 동등하게 할 수 있는가.

확인 신호:
- `package.json` scripts, `Makefile`, `bin/`, `scripts/` 디렉토리
- 배포·migration·rollback·seed 같은 운영 작업의 자동화 진입점
- README/AGENTS.md에 "이런 작업은 어떻게 한다" 절차가 명시됐는가
- 점수 감점: "GUI에서만 가능", "회사 인트라넷에서만", "이 사람한테 물어봐야" 류

### 2. Tool Primitives

스크립트·CLI가 *조합 가능한 작은 단위*로 쪼개졌는가, 거대한 monolithic 스크립트인가.

확인 신호:
- 각 script가 단일 책임, stdout/stderr/exit code가 합리적
- 옵션·인자가 명시적 (flag 없이 동작이 분기되지 않음)
- 점수 감점: 한 스크립트가 빌드·테스트·배포를 동시에 수행, 인자 없이 호출 시 prompt로 물어보는 등 비대화형 환경 적대적

### 3. Doc Coverage

에이전트가 *처음 진입*해서 일을 시작하기에 충분한가.

확인 신호:
- `CLAUDE.md` 또는 `AGENTS.md` 존재
- README에 빌드·테스트·실행 명령
- 도메인 용어/약어 정의가 명시됐는가
- 비명시적 규약(언어 선택, 커밋 컨벤션, 브랜치 전략)이 문서화됐는가
- 점수 감점: 문서는 있지만 코드와 drift, 1년 이상 갱신 없음, 외부 위키 링크만

### 4. Hook Coverage

위험 명령에 대한 가드레일이 설치됐는가.

점수는 먼저 repo-local evidence로 산정한다. home-directory hook은 현재 operator 환경의 보정 근거로만 쓰고, repo가 공유한 readiness 점수를 올리는 단독 근거로 사용하지 않는다.

확인 신호:
- Repo-local: `.claude/settings.json`, `.codex/hooks.json`, `.githooks/` 등 공유 hook 설정
- Operator-local: `~/.claude/settings.json`, `~/.codex/hooks.json` hook (auto-stash, force-push deny, Codex deny-only guard 등)
- pre-commit / pre-push hook
- `.gitignore`가 secret/build artifact를 충분히 가리는가
- 점수 감점: repo-local 가드 없음, 또는 hook은 있지만 우회가 너무 쉬움

### 5. Log / Runtime Access

agent가 *실행 중 상태*에 도달 가능한가.

확인 신호:
- dev 서버 로그가 파일·stdout·tmux 등에 접근 가능 (브라우저 콘솔만이면 감점)
- 테스트 출력이 텍스트로 캡처됨
- CI 상태를 `gh run list` 등으로 확인 가능
- DB / queue / cache 상태를 CLI로 조회 가능
- 점수 감점: 로그가 외부 dashboard에만, 테스트가 GUI runner 필수 등

### 6. Workflow Coverage

compound engineering 4-phase(`plan` / `work` / `review` / `compound`) 중 비어 있는 단계가 얼마인가.

확인 신호:
- `docs/plans/` 또는 plan 자산화 위치 존재
- worktree / 격리 워크플로우 가이드 존재
- 코드 리뷰 절차 명시 (PR template, review checklist)
- `docs/solutions/` 같은 자산화 위치 존재
- 점수 감점: 4단계 중 2개 이상 비어 있음

### 7. Knowledge Capture

해결된 문제·결정이 *재사용 가능한 위치*에 누적되는가.

확인 신호:
- `docs/solutions/`, `docs/decisions/`(ADR), `docs/history/` 등
- frontmatter 또는 일관된 메타데이터로 grep 가능
- 최근 6개월 누적 빈도
- 점수 감점: 위치는 있지만 비어 있음, 또는 1회성 노트만 쌓여 검색 불가

## 점검 절차

### 1. 컨텍스트 수집

```bash
ls -la                                          # 루트 구조
find . -maxdepth 2 -name 'CLAUDE.md' -o -name 'AGENTS.md' -o -name 'README.md'
cat package.json 2>/dev/null | head -30         # scripts 영역
find scripts bin -maxdepth 2 -type f 2>/dev/null
ls .claude 2>/dev/null; ls .codex 2>/dev/null
ls docs 2>/dev/null
git log --oneline -20
```

대형 모노레포면 root + 대표 패키지 1–2개 한정.

### 2. 축별 evidence 수집

각 축에 대해 evidence 파일·명령·실측 결과를 한두 줄로 메모한다. 추측 금지 — 실측 안 된 축은 `unresolved: <reason>`으로 표기하고 점수 미부여.

### 3. 점수 + 사각지대 식별

각 축 0–3점 부여. *왜 그 점수인지* 한 줄 근거.

### 4. 개선 추천 P1/P2/P3

- **P1**: 0–1점 축 중에서 *작업 차단*이 되는 것. 예: hook 부재로 agent가 위험 명령 차단 못함.
- **P2**: 1–2점 축의 사각지대.
- **P3**: 2–3점 축의 polish.

추천은 *이 레포에 추가할 구체적 산출물* 형태로. "문서 보강해라" 대신 "`docs/solutions/` 디렉토리 생성 + `compound` 스킬 도입" 같이.

## 출력 템플릿

```markdown
## Agent-Native Audit — <레포명>

대상: <절대경로>
실행 일자: <YYYY-MM-DD>

### Scorecard (합계 N/21)

| 축 | 점수 | 한 줄 근거 |
|----|------|-----------|
| Action Parity | n/3 | … |
| Tool Primitives | n/3 | … |
| Doc Coverage | n/3 | … |
| Hook Coverage | n/3 | … |
| Log / Runtime Access | n/3 | … |
| Workflow Coverage | n/3 | … |
| Knowledge Capture | n/3 | … |

### 사각지대

- <축 이름>: <증거 → 위험>
- ...

### 추천 (우선순위)

**P1 — 즉시**
- <구체 산출물> — <기대 효과>

**P2 — 단기**
- ...

**P3 — 장기 polish**
- ...

### Unresolved
- <축>: <왜 점검 못했는지>
```

## Gotchas

- **읽기 전용 스킬이다.** 점검 결과로 직접 hook을 설치하거나 문서를 만들지 말 것. 추천만 반환하고, 실행은 사용자가 별도 스킬(`setup-hooks`, `compound`, `skill-guide`)로 진행.
- **모노레포 함정**: 루트 점수가 좋아 보여도 패키지별로 격차가 크다. 큰 모노레포면 루트 + 대표 패키지 한 개를 각각 채점하고, 결과에 그 사실을 명시.
- **점수 인플레이션**: "있긴 있다"로 2점을 주면 평가가 무의미해진다. 사각지대를 한 줄로 적을 수 있으면 그 축은 2점 이상이 어렵다.
- **체크리스트 강박**: 모든 프로젝트가 7축 모두 3점일 필요는 없다. 1인 도구 레포에 CI 점검은 과잉. 사용 맥락을 보고 "이 프로젝트에 의미 있는 축"을 가중치로 표시해도 된다.
- **추천 P1 과다**: P1이 5개 이상이면 사용자가 모두 무시한다. P1은 2–3개로 제한하고, 나머지는 P2로 강등.
- **`unresolved`를 회피 카드로 쓰지 말 것**: 명령 한 번이면 확인되는 항목을 `unresolved`로 두면 audit 가치가 떨어진다. 글로벌 inspection rule(`CLAUDE.md`)대로 inspect로 닫을 수 있으면 닫는다.

## 범위 외

- hook 실제 설치 — `setup-hooks`.
- 발견된 문제 자산화 — `compound`.
- 새 스킬 설계 — `skill-guide`.
- 코드베이스 건강 진단(churn, bug cluster) — `git-diagnosis`. 본 스킬과 보완적이며, 함께 돌리면 *agent 친화도*와 *코드 부채*를 양축으로 볼 수 있다.
