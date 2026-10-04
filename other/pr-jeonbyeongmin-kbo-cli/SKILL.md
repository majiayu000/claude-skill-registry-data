---
name: pr
description: kbo-cli 의 작업 브랜치에서 develop 으로 향하는 새 PR 을 만든다. 단순 push+gh pr create 가 아니라, /code-review 로 diff 검토 → biome check (format+lint) → tsc typecheck → bun build → bun test 5단계 검증을 통과시킨 뒤에 PR 을 올린다. PR 제목·본문은 모두 한국어 Angular 컨벤션 (CLAUDE.md 참조). 사용자가 "PR 올려줘", "pull request 만들어줘", "PR 생성해줘", "이거 PR 로 정리해줘", "리뷰 받게 올려줘" 같은 PR 생성 의도를 보이거나, 기능 작업이 끝나서 머지 흐름을 시작하려는 맥락이면 반드시 이 스킬을 쓴다. push 만 하고 끝나는 단순 push 요청과 다르다 — push 직전에 검증을 강제하는 게 핵심이다.
---

# /pr

작업 브랜치 → `develop` PR 을 올린다. 단순 push + gh pr create 래퍼가 아니다. PR 직전에 코드 검증을 강제해서, 머지 후 develop 이 깨지는 일을 막는다. 검증 도중 실패가 나오면 PR 생성까지 가지 않고 중단한다.

## 브랜치 정책

- 베이스는 항상 `develop` (CLAUDE.md 의 브랜치 정책). main 으로 직접 PR 하지 않는다.
- HEAD 는 `main` / `develop` 이외의 작업 브랜치여야 한다.
- 커밋 메시지·PR 제목·PR 본문은 모두 한국어, Angular 컨벤션 (`<type>(<scope>): <한국어 제목>`).

## 실행 절차

각 단계는 실패 시 **중단**하고 사용자에게 원인을 보고한다. `--force`, `--no-verify` 같은 강제 옵션은 절대 쓰지 않는다 — 검증 실패는 우회 대상이 아니라 수정 대상이다.

### 1. Pre-flight 검증

다음을 모두 확인한다. 하나라도 어긋나면 중단.

- 현재 브랜치: `git rev-parse --abbrev-ref HEAD` 결과가 `develop` 또는 `main` 이면 중단 (작업 브랜치를 만들고 다시 시도하라고 안내).
- HEAD 가 develop 보다 앞서 있어야 함: `git fetch origin develop` 후 `git rev-list --count origin/develop..HEAD` 가 1 이상.
- gh CLI 인증: `gh auth status` 가 통과해야 함. 실패하면 `gh auth login` 안내 후 중단.
- 워킹 트리 상태:
  - 깨끗하면 그대로 진행.
  - dirty 면 `git status -s` 와 `git diff` 를 보여주고, "현재 변경분도 PR 에 포함하시겠어요?" 한 번 묻는다.
    - 동의 → 변경 성격을 보고 Angular 타입을 추론해 한 줄 한국어 메시지로 커밋 (예: `feat(watch): 진행중 경기 좌우 전환`). scope 모호하면 생략.
    - 거부 → 중단.

### 2. /code-review --fix 호출

Skill 도구로 `code-review` 스킬을 `--fix` 로 호출해, `develop..HEAD` diff 를 correctness 버그 관점에서 검토하고 findings 를 워킹 트리에 바로 반영한다 (effort 는 low/medium — 고신뢰 findings 위주). /code-review 가 실제로 파일을 수정했다면:

```bash
git diff --stat
git add -u
git commit -m "fix: /code-review 결과 반영"
```

scope 가 명확하면 `fix(<scope>): /code-review 결과 반영` 형태로. 수정이 없으면 커밋 없이 다음 단계로. 어떤 findings 가 반영됐는지는 §8 보고에 요약한다.

> 사용자가 "리뷰 없이 그대로 올려줘" 라고 미리 요청했다면 이 단계를 건너뛴다. 이후 단계(검증)는 그래도 모두 실행한다.

### 3. 코드 검증

순서대로 실행. **중간 결과를 절대 무시하지 않는다.** 한 단계라도 실패하면 멈추고 보고.

```bash
bun run check        # biome check --write . (format + 안전한 lint 자동 수정)
```

- `check` 가 파일을 변경했으면:
  ```bash
  git add -u
  git commit -m "style: biome check 자동 수정"
  ```
- `check` 가 0 이 아닌 코드로 종료했으면 자동으로 못 고치는 lint 위반이 남은 것이다. 출력을 그대로 보여주고 중단 — 코드 수정은 사용자가 결정한다 (스킬이 임의로 lint 룰을 비활성화하거나 우회하지 않는다).

이어서:

```bash
bun run typecheck    # tsc --noEmit
bun run build        # bun run scripts/build.ts → dist/kbo.js
bun test             # bun 내장 테스트 러너 (테스트 0개여도 0 종료)
```

- typecheck/build/test 실패는 자동 수정하지 않는다. 첫 실패 시점에 멈추고 사용자에게 위임한다.
- `dist/` 는 `.gitignore` 에 들어 있어 build 산출물이 워킹 트리에 남아도 PR 에 안 섞인다.
- `bun test` 가 테스트 파일 0 개일 때 stderr 로 `error: 0 test files matching ...` 를 찍고 **exit 0** 으로 끝낸다. 이건 정상 — 실패로 다루지 말고 통과로 처리한다 (실제로 bun 의 종료 코드만 본다). 사용자에게 이 경고는 굳이 노출하지 않는다.

### 4. Push

upstream 이 없으면 `-u` 로 등록, 있으면 그대로 push.

```bash
BR=$(git rev-parse --abbrev-ref HEAD)
if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git push
else
  git push -u origin "$BR"
fi
```

push 가 비-ff 로 거부되면 (원격에 다른 커밋이 있으면) 중단하고 보고 — `--force` / `--force-with-lease` 자동 사용 금지. 사용자에게 rebase/merge 결정을 위임한다.

### 5. 기존 PR 확인

같은 브랜치에 이미 열린 PR 이 있는지:

```bash
gh pr view --json number,url,state 2>/dev/null
```

- 열린 PR (`state=OPEN`) 이 이미 있으면 새로 만들지 않는다 — 위 push 만으로 갱신됨. URL 만 보고하고 종료.
- 없으면 다음 단계.

### 6. PR 메타데이터 작성

**title** — `git log origin/develop..HEAD --pretty=format:"%s"` 으로 본 커밋 제목들에서 한국어 Angular 컨벤션 한 줄 제목을 만든다:

- 의미 있는 커밋이 1 개면 그 메시지를 그대로 사용 (chore/style 만 모인 경우는 제외하고 가장 의미 있는 type 우선).
- 여러 개면 type 다수결 + 핵심을 종합한 한국어 제목. 50자 이내, 마침표 없음.
- 예: `feat(watch): 진행중 경기 좌우 전환 추가`, `fix(api): 응답 success=false 시 에러 처리`.

**body** — 다음 한국어 템플릿:

```markdown
## 요약
- <변경 핵심 1~3 bullet, 한국어>

## 테스트
- [x] `bun run check` (biome format + lint)
- [x] `bun run typecheck`
- [x] `bun run build`
- [x] `bun test`
- [ ] CLI 동작 확인 (`bun run dev today`, `bun run dev watch --game <id>`)
- [ ] fixture 화면 검증 (`bun run render:fixture` — 라이브 없을 때 STARTED/RESULT/BEFORE 한 프레임씩)

## 관련
- (이슈 / 문서 / 외부 컨텍스트 링크가 있으면, 없으면 섹션 통째로 생략)
```

세부 규칙:

- UI/렌더(`src/render.ts`, `src/watch.ts`) 또는 CLI 동작(`src/index.ts`)이 바뀌지 않았다면 "CLI 동작 확인" 과 "fixture 화면 검증" 두 체크박스를 제외.
- UI/렌더가 바뀐 PR 이고 라이브 경기가 없는 시간대라면, "CLI 동작 확인" 체크박스는 제외하고 "fixture 화면 검증" 만 남긴다 — 라이브 없이도 모드별 렌더를 그려볼 수 있도록 `scripts/snapshot.ts` / `scripts/render-fixture.ts` 가 준비돼 있다 (CLAUDE.md 자주 쓰는 명령 참조).
- `src/api.ts`, `src/types.ts` 가 수정된 PR 이라면 "테스트" 섹션 끝에 `--debug 로 raw 응답 확인` 항목을 추가한다 — Naver 비공식 API 응답 구조 변경 위험이 있어서 (CLAUDE.md 데이터 소스 항목).
- 본문은 한국어. 머릿글 `## 요약`, `## 테스트` 는 그대로 유지 — 리뷰어가 빠르게 스캔할 수 있게 형식이 일관되어야 한다.

### 7. PR 생성

```bash
gh pr create \
  --base develop \
  --head "$BR" \
  --title "$TITLE" \
  --body "$(cat <<'EOF'
$BODY
EOF
)"
```

`HEREDOC` 으로 본문을 전달해 따옴표·백틱이 깨지지 않게 한다.

### 8. 사용자에게 보고

다음을 한 번에 정리:

- 거친 검증 단계와 각각의 결과 (✓ code-review, ✓ check, ✓ typecheck, ✓ build, ✓ test)
- /code-review 가 --fix 로 반영한 findings 요약 (있었으면)
- 스킬이 만든 추가 커밋 목록 (`fix: /code-review 결과 반영`, `style: biome check 자동 수정` 등)
- push 한 브랜치 이름과 upstream
- 생성된 PR URL (또는 이미 열려있던 PR URL)

## 주의사항

- **/code-review --fix 와 biome check 가 만드는 자동 수정 커밋은 PR diff 를 어지럽힐 수 있다.** 사용자가 "자동 수정 커밋 없이 가고 싶다" 고 미리 말했으면 §2 와 §3 의 자동 수정 단계를 건너뛴다 — 단, typecheck/build/test 는 반드시 통과해야 PR 을 만든다 (검증 자체를 건너뛰지는 않는다).
- biome 이 처음 적용되는 PR 은 포매팅 변경이 광범위할 수 있다. 첫 PR 에서는 검증 커밋이 큰 게 정상 — 사용자에게 미리 알린다.
- 작업 브랜치가 origin 에 없을 수 있다. 첫 push 는 `-u origin <branch>` 로 upstream 을 만들어 둔다.
- PR 본문에 본인이 만든 커밋 SHA 를 나열하지 않는다 — gh 가 자동으로 commits 탭에 보여주고, 본문 중복은 노이즈다.
- 코드 식별자(함수명, 옵션명) 는 영문 그대로. 한국어 번역하지 않는다.
- 이 스킬은 `git push` 와 `gh pr create` 를 실행한다 — 둘 다 사용자 외 영향 (원격 갱신, 리뷰어 알림). pre-flight 검증을 다 통과한 뒤에야 push 하므로, 사전 동의는 "PR 올려줘" 발화 자체로 보고 별도 확인은 묻지 않는다. 단 dirty 워킹 트리를 PR 에 포함할지(§1)는 명시적으로 한 번 묻는다.
