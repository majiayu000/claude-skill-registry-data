---
name: release
description: kbo-cli 새 버전을 릴리즈한다. develop 에서 package.json 버전을 올리고 커밋·태그를 만든 뒤, main 을 develop 으로 fast-forward 동기화해 origin 으로 push 하면, GitHub Actions 가 npm 배포와 GitHub Release 생성을 처리한다. 인자 형식 — `/release` (patch), `/release minor`, `/release major`, `/release 1.2.3` (명시 버전).
---

# /release

이 프로젝트의 태그 기반 자동 릴리즈 흐름을 실행한다. 로컬에서는 버전 bump · 빌드 검증 · 커밋 · 태그 · main 동기화 · push 까지만 한다. 실제 npm publish 와 GitHub Release 작성은 `.github/workflows/release.yml` 이 `v*` 태그를 받아 수행한다.

## 브랜치 정책

- **default 브랜치는 `develop`** — 모든 작업과 릴리즈 커밋·태그 생성은 develop 에서.
- **`main` 은 develop 의 거울** — 항상 develop 의 fast-forward 가능한 상태로 동기화. main 에만 있는 커밋이 생기면 안 된다 (생기면 정책 위반으로 중단).
- 태그는 develop 에서 만들고, main 을 develop 으로 fast-forward 시키면 동일 SHA 가 두 브랜치에 노출된다.

## 인자 해석

`$ARGUMENTS` 가 비어 있으면 `patch`. 다음 중 하나로 해석한다.

- `patch` | `minor` | `major` — semver bump
- `X.Y.Z` 형태의 명시 버전 — 그대로 사용 (현재 버전보다 커야 함)
- 그 외 — 사용자에게 원하는 형식을 되묻고 중단

## 실행 절차

각 단계는 실패 시 **중단하고** 사용자에게 원인을 보고한다. 임의로 우회하거나 강제 옵션 (`--force`, `--no-verify` 등) 을 쓰지 않는다.

### 1. Pre-flight 검증

다음을 모두 확인한다. 하나라도 어긋나면 무엇이 문제인지 보고하고 중단.

- 현재 브랜치가 `develop` — `git rev-parse --abbrev-ref HEAD`
- 워킹 트리가 깨끗함 — `git status --porcelain` 이 빈 문자열
- `git fetch origin` 1회 실행 후 아래 항목 확인:
  - origin/develop 과 동기화됨 — `git rev-list --left-right --count HEAD...origin/develop` 이 `0\t0`
  - 로컬 main 이 origin/main 과 동기화됨 — `git rev-list --left-right --count main...origin/main` 이 `0\t0`
  - main 이 develop 의 ancestor (= main 에 develop 에 없는 커밋이 없음) — `git rev-list --count develop..main` 이 `0`. **0 이 아니면 정책 위반**으로 중단하고 사용자에게 main 에만 있는 커밋을 보고한다.

### 2. 새 버전 결정

- 현재 버전: `package.json` 의 `version` 필드를 Read 로 읽는다.
- bump 모드면 semver 규칙대로 계산.
- 명시 버전이면 현재 버전보다 큰지 확인 (큰지 비교는 `src/update.ts` 의 `compareVersion` 과 동일한 의미여야 함 — 단순 dot-split 정수 비교).
- 동일 버전 태그(`vX.Y.Z`)가 이미 존재하면 중단: `git tag -l vX.Y.Z`.
- 결정된 새 버전을 사용자에게 한 줄로 알리고 다음 단계로 (별도 확인 묻지 않음 — 인자로 이미 의도가 표현됨).

### 3. 빌드 검증 (순차 실행)

- `bun run typecheck`
- `bun run build`

둘 중 하나라도 실패하면 중단. 코드 수정은 하지 않는다 — 사용자가 먼저 고쳐야 한다.

### 4. 릴리즈 노트 초안 작성

태그 push 후 GitHub Actions 가 `generate_release_notes: true` 로 자동 노트를 만들지만, 한국어 + Angular 타입별 그룹핑된 노트로 §10 에서 덮어쓴다. 여기서는 그 초안을 만든다.

이전 태그부터 develop HEAD 까지의 커밋을 모은다 (이전 태그가 없으면 전체 히스토리):

```bash
PREV=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
RANGE=${PREV:+${PREV}..HEAD}
git log --no-merges --pretty=format:"%H%x09%s" ${RANGE}
```

각 커밋 제목을 Angular 타입(`feat`, `fix`, `perf`, `refactor`, `docs`, `build`, `ci`, `chore`, `test`, `style`, `revert`)으로 분류한다. 타입 prefix 가 없는 커밋은 `기타` 섹션으로 모으고, 사용자에게 그 사실을 함께 알린다.

다음 형식의 마크다운 초안을 만들고 셸 변수 `RELEASE_NOTES` 에 담아 둔다 (HEREDOC 으로 안전하게):

```markdown
## ✨ 새 기능
- watch 진행중 경기 좌우 전환 추가 (61b2e57)

## 🐛 버그 수정
- api 응답 success=false 시 에러 처리 (45b3913)

## 🛠 기타
- 0.2.0 (3f37ff7)

**전체 변경 이력**: https://github.com/jeonbyeongmin/kbo-cli/compare/vPREV...vNEW
```

규칙:
- 타입별 섹션 제목과 이모지: `✨ 새 기능` (feat), `🐛 버그 수정` (fix), `⚡ 성능` (perf), `♻ 리팩터링` (refactor), `📝 문서` (docs), `🏗 빌드` (build), `🤖 CI` (ci), `🧹 잡무` (chore), `✅ 테스트` (test), `💄 스타일` (style), `⏪ 되돌림` (revert), `🛠 기타` (분류 불가).
- 비어있는 섹션은 생략.
- 각 항목은 커밋 제목의 한국어 본문만 사용 (`feat(scope): ` prefix 는 제거). scope 가 있으면 본문 앞에 그대로 두어 맥락을 살린다 (예: `watch 진행중 경기 좌우 전환 추가`).
- 끝에 short SHA(7자) 를 괄호로.
- 마지막 줄의 비교 링크는 이전 태그가 없으면 생략.

초안을 사용자에게 한 번 보여주고 수정 의견이 있으면 반영한다. 별다른 요청이 없으면 그대로 진행 (별도 확인 묻지 않음).

### 5. README 최신화

코드는 바뀌었는데 README 가 따라오지 않으면 사용자에게 거짓을 보여주게 된다. 이 단계는 README 와 코드의 *사실 어긋남* 만 좁게 좇는다 — 전체 재작성·문체 다듬기·스크린샷 교체는 스코프 밖.

§4 에서 모은 커밋 중에서 README 에 영향을 줄 수 있는 type 만 추린다:

- `feat`: 거의 모두 후보. 새 서브커맨드/옵션/키바인딩/환경변수일 가능성.
- `fix`: 동작이 바뀐 경우만 (예: 기본값 변경, 행동 변화). 단순 버그 수정은 무시.
- `refactor`: CLI 인터페이스가 노출되는 변경만 후보 (예: 옵션 이름 변경). 내부 리팩터는 무시.
- `chore`/`style`/`docs`/`test`/`ci`/`build`: 무시.

추린 항목을 README.md 의 다음 영역과 1:1 대조:

| README 섹션          | 대조 대상                                                  |
| -------------------- | ---------------------------------------------------------- |
| `## 사용`            | `kbo <subcommand>`, `--flag`, 옵션 인자                    |
| `## 라이브 중 키`    | watch 모드 키바인딩 (q/r/← →/Ctrl+C 등)                    |
| `## 데이터 소스`     | 호출 엔드포인트 path                                       |
| `## 구조`            | `src/` 파일 추가·역할 변경                                 |
| 환경 변수 안내       | 새 `KBO_*` ENV 추가                                        |
| 요구사항 (Node ≥ X)  | `package.json` 의 `engines.node` 변경                      |

대조 결과:

- **어긋남 있음** → README.md 의 해당 섹션을 `Edit` 로 *국지적으로* 패치한다 (전체 재작성 금지). diff 를 사용자에게 보여주고, 별도 의견 없으면 다음 단계로.
- **어긋남 없음** → "README 변경 없음" 한 줄 보고하고 다음 단계로.

README 가 변경됐으면 별도 커밋:

```bash
git add README.md
git commit -m "docs(readme): vX.Y.Z 변경사항 반영"
```

> 면책 조항·라이선스·설치 일반 안내·스크린샷·문체 다듬기는 이 단계에서 건드리지 않는다. 그건 별도 PR 의 책임이다. 여기서는 *코드 변화로 발생한 사실 어긋남* 만 좁게 좇는다.

### 6. package.json 업데이트

`Edit` 도구로 `version` 필드만 정확히 교체한다. `npm version` 같은 명령은 쓰지 않는다 (의도치 않게 태그/커밋이 함께 만들어져 흐름이 꼬인다).

### 7. 커밋

이 레포의 릴리즈 커밋 컨벤션은 메시지가 그냥 `X.Y.Z` 한 줄이다 (`git log` 참고: `0.2.0`).

```bash
git add package.json
git commit -m "X.Y.Z"
```

`-A` 나 `.` 으로 stage 하지 말 것. `package.json` 만 명시적으로 add (§5 에서 README 가 변경됐어도 그 커밋은 이미 따로 만들어졌으므로 여기에 섞이지 않는다).

### 8. 태그 생성 (develop 에서)

§7 의 버전 bump 커밋이 HEAD 다 (§5 README 커밋이 있다면 그 위에 bump 커밋이 쌓인 형태). 그 HEAD 위에 annotated 태그를 만든다 (`-a`). 태그 이름은 `v` 접두사 포함.

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
```

### 9. main 을 develop 으로 fast-forward

main 동기화는 **fast-forward 만** 허용한다. §1 에서 ancestor 검증을 통과했다면 항상 ff 가능. 만약 여기서 비-ff 로 실패하면 정책 위반이므로 중단하고 보고한다 (절대 `--force` 나 강제 rebase 로 우회하지 않는다).

```bash
# 워킹 트리/HEAD 를 건드리지 않고 로컬 main ref 만 develop 으로 fast-forward
git fetch . develop:main
```

### 10. Push (순서 중요)

`tag push` 가 npm publish 트리거이므로 **마지막**에 둔다. 앞 단계가 실패해도 npm 까지 나가지 않아 롤백 비용이 낮다.

```bash
git push origin develop      # 1) 버전 bump 커밋 (+ §5 README 커밋이 있으면 같이)
git push origin main         # 2) 동기화된 main (ff push)
git push origin vX.Y.Z       # 3) 태그 — 이 시점에 npm publish + GitHub Release 트리거
```

`--force` / `--force-with-lease` 류는 절대 쓰지 않는다. main push 가 비-ff 로 거부되면 중단하고 보고한다.

### 11. GitHub Release 본문 업데이트

태그 push 직후 `softprops/action-gh-release` 가 자동 생성한 영문 노트를 §4 의 한국어 초안으로 덮어쓴다.

Release 가 생성될 때까지 짧게 폴링한다 (워크플로 build/typecheck 시간 때문에 보통 30~90초 소요):

```bash
for i in $(seq 1 30); do
  if gh release view vX.Y.Z >/dev/null 2>&1; then break; fi
  sleep 5
done
```

30회(≈2.5분) 안에 안 보이면 워크플로 실패 가능성이 있으니 폴링을 멈추고 사용자에게 actions URL 과 함께 보고하고 종료한다 (수동 보강은 사용자에게 위임).

생성이 확인되면 `gh release edit` 로 본문을 교체한다:

```bash
gh release edit vX.Y.Z --notes "$RELEASE_NOTES"
```

이 단계는 멱등 — 실패 시 재실행해도 안전하다. 단, 사용자가 GitHub UI 에서 이미 노트를 수정했을 가능성이 있으면 덮어쓰기 전에 확인한다 (`gh release view vX.Y.Z --json body` 결과가 비어있거나 자동 생성 영문 패턴이면 그대로 덮어쓰기, 한국어가 섞여 있으면 사용자에게 물어본다).

### 12. 사용자에게 보고

- 새 버전 번호
- 푸시된 태그 이름
- §5 의 README 갱신 여부 (변경 없음 / 어떤 섹션을 패치했는지)
- develop / main 이 동일 SHA 로 동기화됐다는 안내
- GitHub Actions 가 npm publish + GitHub Release 생성을 처리했고, 한국어 릴리즈 노트로 본문을 교체했다는 안내 (§11 폴링이 시간초과로 끝났으면 그 사실을 알리고 사용자에게 수동 보강 위임)
- workflow run URL: `https://github.com/jeonbyeongmin/kbo-cli/actions`
- Release URL: `https://github.com/jeonbyeongmin/kbo-cli/releases/tag/vX.Y.Z`

## 주의사항

- **태그를 push 하기 전까지** 어떤 단계에서든 중단하면 사용자가 수동 복구 가능하다 (`git reset --soft HEAD~1` — README 커밋이 있었다면 `~2`, `git tag -d vX.Y.Z`, `git update-ref refs/heads/main <원래 SHA>`). 태그 push 이후의 롤백은 npm unpublish 제약 등으로 비싸므로, 그 직전까지 검증을 충분히 한다.
- main 은 항상 fast-forward 로만 갱신한다. develop..main 이 0 이 아니면 (main 에만 있는 커밋이 있으면) 자동으로 처리하지 않고 사용자에게 위임한다 — hotfix 브랜치 머지 정책 등 컨텍스트 필요한 결정은 스킬 범위 밖.
- 현재 working dir 외부 파일은 건드리지 않는다.
- npm publish 자격 증명(`NPM_TOKEN`) 은 워크플로 환경에서만 다룬다. 로컬에서 직접 publish 하지 않는다.
- 태그/릴리즈 권한이 owner 한정인지(또는 특정 actor 가드가 워크플로에 걸려 있는지) 확인이 필요하면 `.github/workflows/release.yml` 의 `if: github.actor == ...` 라인을 본다.
