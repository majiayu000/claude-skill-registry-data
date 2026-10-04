---
name: release
description: npm 릴리스 운영. release 브랜치 선택 커밋 반영, 검증, publish, tag, GitHub Release, main 동기화 진행
---

# Release

## 원칙

- `develop`은 실질 메인 브랜치 기준
- `release`는 npm 배포 후보 커밋만 모으는 장기 브랜치 기준
- 자동 push 트리거 대신 명시 수동 배포
- npm publish 커밋과 `vX.Y.Z` git tag 일치 필수
- publish된 tag 커밋의 기준 브랜치 포함 필수
- `pnpm` 사용
- `npm` CLI는 인증 확인, registry 조회 같은 npm 계정/registry 작업에만 사용
- 버전 지정 배포 요청은 검증 통과 후 publish, tag, 원격 push, GitHub Release 생성, 기준 브랜치 동기화, 임시 release 브랜치 정리 승인으로 간주
- 사용자 명시 승인 없는 실제 `publish`, tag 생성, 원격 push, GitHub repo public 전환 금지
- GitHub repo public 전환은 별도 승인 필수
- 인증·2FA·OTP·recovery code는 채팅 요청 금지, 로컬 브라우저/터미널 프롬프트 직접 입력 기준

## 먼저 확인

작업 시작 시 다음 확인.

```bash
git status --short
git branch --show-current
git remote -v
git tag --list 'v*'
PATH=/opt/homebrew/bin:$PATH pnpm -v
PATH=/opt/homebrew/bin:$PATH npm whoami
PATH=/opt/homebrew/bin:$PATH gh auth status -h github.com
```

`git status --short`가 비어 있지 않으면 변경 파일 확인. 릴리스 작업과 무관한 변경은 제외. 브랜치 이동, cherry-pick, publish 전 dirty worktree 처리 방침 명확화.

## 인증 복구

`npm whoami`가 `E401`, `E403`, invalid token 등으로 실패하면 에이전트가 복구 명령 실행, 계정 확인·OTP 입력만 사용자 로컬 프롬프트 기준.

```bash
PATH=/opt/homebrew/bin:$PATH npm logout --registry=https://registry.npmjs.org/
PATH=/opt/homebrew/bin:$PATH npm login --registry=https://registry.npmjs.org/ --auth-type=web
PATH=/opt/homebrew/bin:$PATH npm whoami --registry=https://registry.npmjs.org/
```

- web login URL/브라우저 열기 프롬프트는 에이전트가 진행
- 계정 확인, 비밀번호, OTP, 2FA는 사용자 로컬 입력
- web login 실패 시 `--auth-type=legacy` 로컬 프롬프트 재시도
- 인증 성공 후 릴리스 흐름 자동 재개

`gh auth status` 실패 시 GitHub Release 생성 전 인증 복구.

```bash
PATH=/opt/homebrew/bin:$PATH gh auth login -h github.com -w
PATH=/opt/homebrew/bin:$PATH gh auth status -h github.com
```

## 릴리스 브랜치 구성

기준 브랜치 자동 판별. `develop` 존재 시 `develop`, 없으면 `main` 기준.

대상 브랜치 자동 판별. 장기 `release` 브랜치 존재 시 `release`, 없으면 `release/$PACKAGE_VERSION` 기준.

배포 커밋 미지정 시 기준 브랜치와 대상 브랜치 차이 제시 후 배포 커밋 후보 제안.

```bash
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
BASE_BRANCH=$(git show-ref --verify --quiet refs/heads/develop && echo develop || echo main)
RELEASE_BRANCH=$(git show-ref --verify --quiet refs/heads/release && echo release || echo "release/$PACKAGE_VERSION")
git fetch origin
git branch --list "$BASE_BRANCH" "$RELEASE_BRANCH"
if git show-ref --verify --quiet "refs/heads/$RELEASE_BRANCH"; then
  git log --oneline --decorate "$RELEASE_BRANCH..$BASE_BRANCH"
else
  git log --oneline --decorate "$BASE_BRANCH" --not --tags
fi
```

대상 브랜치가 없고 기준 브랜치 HEAD 전체를 배포하는 경우 기준 브랜치에서 생성.

```bash
git checkout -b "$RELEASE_BRANCH" "$BASE_BRANCH"
```

기존 대상 브랜치에 선택 커밋만 반영하는 경우 cherry-pick.

```bash
git checkout "$RELEASE_BRANCH"
git cherry-pick <commit-sha>
```

merge commit cherry-pick, 충돌 해결, version bump, release-only 수정은 높은 위험도. 필요한 이유와 결과 파일 설명 후 진행.

버전 지정 릴리스에서 `package.json` 버전 불일치 시 릴리스 브랜치에서 version bump 커밋 생성. 커밋 생성 시 `$commit` 기준 적용.

## 배포 전 메타데이터

첫 공개 배포 전 GitHub repo 공개 여부와 npm 페이지 메타데이터 확인.

- `package.json`의 `name`, `version`, `description`, `license`, `bin`, `files`
- 가능하면 `repository`, `bugs`, `homepage`
- README의 사용자 실행 예시가 `pnpm dlx codex-webtoon` 기준인지
- 공개 repo 전환을 먼저 할지, npm publish 후 공개할지

private repo에서도 npm publish 가능. 공개 패키지는 publish 전 repo public 전환과 메타데이터 입력 흐름 우선 제안.

## 검증

`release` 브랜치 HEAD에서 실행.

```bash
PATH=/opt/homebrew/bin:$PATH pnpm prepublishOnly
PATH=/opt/homebrew/bin:$PATH pnpm audit --prod
PATH=/opt/homebrew/bin:$PATH pnpm publish --dry-run --no-git-checks --access public
```

필요 시 tarball 설치 스모크까지 수행.

```bash
PACK_DIR=$(mktemp -d /tmp/codex-webtoon-pack.XXXXXX)
PATH=/opt/homebrew/bin:$PATH pnpm pack --pack-destination "$PACK_DIR"
```

tarball 설치 스모크에서는 임시 프로젝트와 임시 config/projects 경로 사용. 사용자 실제 설정이나 프로젝트 데이터 변경 금지.

## npm Registry 확인

버전 충돌 확인.

```bash
PACKAGE_NAME=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').name")
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
PATH=/opt/homebrew/bin:$PATH npm view "$PACKAGE_NAME" versions --json
git tag --list "v$PACKAGE_VERSION"
```

첫 publish 전 `npm view`의 `E404`는 공개 패키지 부재 1차 신호. 기존 패키지가 있으면 현재 `package.json` 버전의 registry 중복 여부 확인.

## 실제 Publish/Tag/Push

사용자의 버전 지정 배포 요청이 있고 검증이 모두 통과하면 재확인 질문 없이 연속 실행. publish 전 마지막 확인은 package/version, 현재 브랜치, HEAD, registry 중복, 기존 tag 기준.

```bash
CURRENT_BRANCH=$(git branch --show-current)
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
PATH=/opt/homebrew/bin:$PATH pnpm publish --access public
```

`pnpm publish`가 publish-branch 불일치 확인을 요구해도 현재 브랜치가 의도한 릴리스 브랜치이고 검증 통과 상태면 계속 진행.

2FA OTP 필요 시 사용자 로컬 직접 입력. 비밀번호, OTP, recovery code 채팅 요청 금지.

publish 성공 후 같은 커밋에 annotated tag 생성.

```bash
git tag -a "v$PACKAGE_VERSION" -m "Release v$PACKAGE_VERSION"
git push origin "$CURRENT_BRANCH" "v$PACKAGE_VERSION"
```

tag는 publish 성공 후 생성. publish 실패 시 tag 생성 금지.

## GitHub Release

tag push 후 GitHub Release 생성·갱신까지 기본 마무리. GitHub 웹 UI 수동 업데이트 지시 금지.

```bash
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
GH_REPO=$(PATH=/opt/homebrew/bin:$PATH gh repo view --json nameWithOwner -q .nameWithOwner)
PATH=/opt/homebrew/bin:$PATH gh release view "v$PACKAGE_VERSION" --repo "$GH_REPO"
```

GitHub Release가 없으면 `gh release create`, 있으면 필요한 경우 `gh release edit` 실행.

```bash
NOTES_FILE=$(mktemp /tmp/codex-webtoon-release-notes.XXXXXX.md)
PATH=/opt/homebrew/bin:$PATH gh release create "v$PACKAGE_VERSION" \
  --repo "$GH_REPO" \
  --title "codex-webtoon v$PACKAGE_VERSION" \
  --latest \
  --notes-file "$NOTES_FILE"
```

릴리즈 노트는 이전 tag와 현재 tag 사이 커밋 기준 자동 작성. 기존 Release의 Install/Notes 고지 형식 유지.

```bash
PREVIOUS_TAG=$(git tag --list 'v*' --sort=-version:refname | grep -v "v$PACKAGE_VERSION" | head -n 1)
git log --oneline --decorate "$PREVIOUS_TAG..v$PACKAGE_VERSION"
PATH=/opt/homebrew/bin:$PATH gh release list --repo "$GH_REPO" --limit 5
```

## 기준 브랜치 동기화

GitHub Release 생성 후 tag 커밋의 기준 브랜치 포함 여부 확인. publish된 tag 이동 금지.

```bash
BASE_BRANCH=$(git show-ref --verify --quiet refs/heads/develop && echo develop || echo main)
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
RELEASE_BRANCH=$(git branch --show-current)
git merge-base --is-ancestor "v$PACKAGE_VERSION" "$BASE_BRANCH"
```

tag 커밋이 기준 브랜치에 없으면 릴리스 브랜치를 기준 브랜치에 병합 후 push.

```bash
BASE_BRANCH=$(git show-ref --verify --quiet refs/heads/develop && echo develop || echo main)
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
RELEASE_BRANCH=$(git branch --show-current)
git status --short
git checkout "$BASE_BRANCH"
git pull --ff-only origin "$BASE_BRANCH"
git merge --no-ff "$RELEASE_BRANCH" -m "chore: $PACKAGE_VERSION 릴리스 브랜치 병합"
PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version"
git merge-base --is-ancestor "v$PACKAGE_VERSION" "$BASE_BRANCH"
git push origin "$BASE_BRANCH"
```

- 충돌 발생 시 중단 후 충돌 파일과 선택지 보고
- `package.json` version이 배포 버전과 다른 경우 중단
- `vX.Y.Z` tag 재생성·이동 금지

## 임시 release 브랜치 정리

`release/$PACKAGE_VERSION` 형태의 버전별 임시 브랜치는 기준 브랜치 동기화 후 삭제. 장기 `release` 브랜치는 삭제 금지.

```bash
PACKAGE_VERSION=$(PATH=/opt/homebrew/bin:$PATH node -p "require('./package.json').version")
TEMP_RELEASE_BRANCH="release/$PACKAGE_VERSION"
if git ls-remote --exit-code --heads origin "$TEMP_RELEASE_BRANCH" >/dev/null 2>&1; then
  git push origin --delete "$TEMP_RELEASE_BRANCH"
fi
if git show-ref --verify --quiet "refs/heads/$TEMP_RELEASE_BRANCH"; then
  git branch -d "$TEMP_RELEASE_BRANCH"
fi
```

GitHub의 `recent pushes` 배너는 PR 생성 유도 신호일 뿐 릴리스 누락 판단 기준 아님. 단, `release/$PACKAGE_VERSION` 배너가 남아 있으면 기준 브랜치 동기화와 임시 브랜치 정리 상태 확인.

## GitHub Actions 기준

수동 배포 워크플로우만 제안.

```yaml
on:
  workflow_dispatch:
```

`release` push만으로 자동 publish되는 설정 작성 금지.

```yaml
on:
  push:
    branches: [release]
```

위 형태는 사용자 명시적 자동 배포 요청 시에만 사용.

## 마무리 기록

릴리스 작업 종료 후 다음 요약.

- publish 여부와 배포 버전
- publish된 commit SHA와 tag
- GitHub Release URL과 Latest 여부
- 기준 브랜치 동기화 여부와 commit SHA
- 임시 release 브랜치 삭제 여부
- 실행한 검증 명령과 결과
- 남은 수동 작업

작업 청크 종료 시 진행 기록이 필요하면 `progress-log` 스킬로 `.progress/YYMMDD/<topic>.md` 기록.
