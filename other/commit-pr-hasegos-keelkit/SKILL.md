---
name: commit-pr
description: 기능 구현을 마친 뒤 dev 기준으로 브랜치를 만들고 커밋, PR 작성, dev 병합, 병합 뒤 브랜치 삭제까지 하는 절차. PR은 gh CLI로 만든다. 브랜치 이름, 커밋 메시지, PR 본문 틀, squash 병합 포함.
---

# 커밋 · PR 절차

저장소는 `git remote get-url origin`으로 확인한다. 기준 브랜치는 항상 `dev`. 계획이 승인된 작업은 기능 구현과 검증(`verify`)이 끝나면 묻지 않고 커밋 · push · PR · dev 병합까지 한다 (`docs/rules/workflow.md` 1번). 작성자는 git 설정 그대로, AI 도구 표시 줄(`Co-Authored-By` 등)은 넣지 않는다. `.env` 계열 파일은 커밋하지 않는다 (hook이 막는다).

## 0. gh 준비

PR 작성과 병합은 `gh` CLI로 한다. 시작 전에 `gh auth status`로 확인한다.

- `gh`가 없거나 로그인이 안 돼 있으면 멈추고 사용자에게 알린다. 설치는 `winget install GitHub.cli`, 로그인은 사용자가 터미널에서 `gh auth login`을 직접 실행한다. 로그인은 AI 도구가 대신하지 않는다.
- 준비가 끝날 때까지 PR 단계는 보류하고, 브라우저로 우회하지 않는다. 커밋과 push까지는 진행한다.

## 1. 브랜치

1. `git remote get-url origin`으로 원격이 있는지 보고, 없으면 사용자에게 저장소 URL을 묻는다. 있으면 `git ls-remote --heads origin`으로 브랜치가 있는지 확인한다.
2. 원격이 비어 있으면(브랜치가 하나도 없으면) `dev` 앞에 기본 브랜치부터 만든다. 작업 파일은 그대로 두고 빈 커밋만 올린다. 이 경우에만 `master` push가 허용된다 (`workflow.md`, hook도 원격이 비어 있을 때만 통과시킨다).

   ```bash
   git init -b master                                # 이미 저장소이면 건너뛴다
   git commit --allow-empty -m "ADD 저장소 초기화"
   git push -u origin master
   git switch -c dev
   git push -u origin dev
   ```

   `dev`만 만들고 `master`를 건너뛰지 않는다. 첫 push한 `master`가 GitHub 기본 브랜치가 된다. 이미 커밋이 있는 로컬 저장소이면 빈 커밋은 만들지 않고 그 브랜치를 그대로 push한다.
3. 원격에 `dev`가 없고 기본 브랜치(`main` 또는 `master`)만 있으면 거기서 만들어 올린다: `git switch -c dev origin/<기본 브랜치>` → `git push -u origin dev`.
4. `git switch dev` → `git pull --ff-only` → `git switch -c feature/<기능>`. 기능 이름은 kebab-case (예: `feature/login`). 처음 올리는 작업도 `dev`에 바로 커밋하지 않고 기능 브랜치에서 PR로 올린다.
5. 브랜치는 기능 하나당 하나. 브랜치를 겹쳐 쌓지 않는다. squash 병합 뒤에는 앞 브랜치 커밋이 `dev` 이력에 없어서 뒤 브랜치 PR에 다시 나타난다.
6. 커밋 직전 `git branch --show-current`로 기능 브랜치인지 확인한다.

## 2. 커밋

- 파일 · 단위별로 작게 나눈다. 제목은 `ADD <대상> 추가` / `FIX <대상> 수정` / `DELETE <대상> 삭제` 한 줄.
- 처음 올리는 작업도 똑같이 나눈다. 예: 앱 코드, 테스트, 설정 파일을 각각 다른 커밋으로. `git add -A`와 `git add .`는 쓰지 않고 파일이나 폴더를 이름으로 지정해서 add한다. 한 커밋에 서로 다른 단위를 섞지 않는다.
- 단위 기준: 스타터 · 스캐폴드를 복사한 파일, 직접 만든 앱 코드, DB 스키마와 마이그레이션, 빌드 · 배포 설정, 문서는 서로 다른 단위다. 커밋 직전 `git diff --cached --stat`로 확인해서 파일이 30개를 넘거나 서로 다른 단위가 둘 이상 섞이면 `git reset`으로 되돌리고 나눠서 add한다.
- Codex 샌드박스가 `.git` 쓰기에 권한 승인을 요구해도 커밋을 한 번에 합치지 않는다. 단위마다 승인을 받고 나눠서 커밋한다.
- 본문은 빈 줄 뒤에 한두 줄로 "무엇을 왜".
- 여러 줄 메시지는 `git commit -F -` + heredoc.

## 3. PR

PR 작성 전에 `dev` 대비 diff를 읽고 검수한다 (`docs/rules/workflow.md` 1번 변경 절차 4번). 변경이 아주 크면 `reviewer` agent(Claude에만 있다. 없으면 직접 읽어서)로 한다. 기준은 `git diff --shortstat dev...HEAD`에서 변경 파일 20개 이상 또는 변경 줄(추가 + 삭제) 500줄 이상이다. 작은 변경은 agent를 부르지 않고 직접 읽는다. 높음 · 중간 지적 사항은 고친 뒤 진행한다.

브랜치를 push한 뒤 만든다. 본문은 실제 diff와 맞는지 확인한다.

```bash
gh pr create --base dev --head feature/<이름> --title "<제목>" --body-file - <<'EOF'
<본문>
EOF
```

- 제목: 무엇을 했는지 한 문장, 명사형 (`~ 추가`, `~ 정리`).
- 본문 틀 (확인 방법 절은 두지 않는다):

      ## 개요

      <무엇을, 왜. 두 문단 안>

      ## 주요변경사항

      1. <묶음 제목>
          + <계층 (파일 · 클래스)>
              + <변경 내용. "~했습니다." 체>

- `dev` → `main` PR은 사용자가 요청할 때 `--base main --head dev`로 만든다. 병합은 하지 않고, 사용자에게 Create a merge commit으로 병합하라고 안내한다. squash로 병합하면 `main`이 `dev`의 커밋과 연결되지 않아 다음 PR에서 같은 파일이 충돌한다 (squash는 feature → `dev`에서만 쓴다).
- `dev` → `main` PR 본문은 PR을 만들기 직전에 `main`에 아직 없는 `dev` 커밋을 뽑아서 쓴다. `dev` 커밋 제목이 `<PR 제목> (#N)`이라 이 목록이 병합된 PR 목록이다. `main`이 없으면 `master`로 바꾼다.

```bash
git fetch
git log --first-parent --format='- %s' origin/main..origin/dev
```

      ## 변경 사항

      <위 명령 출력을 그대로>

  제목은 변경이 한 건이면 그 PR 제목을 쓰고, 여러 건이면 `ADD <묶음 요약> 반영`처럼 한 문장으로 쓴다.
- PR 만든 뒤 사용자에게 병합 창 주의를 안내한다. `dev` 커밋이 1개이면 GitHub가 PR 제목과 본문 대신 그 커밋의 제목 · 본문을 병합 창에 넣고 제목 끝에 `(#N)`을 또 붙여서 `(#9) (#10)`처럼 번호가 겹칠 수 있다. 이때는 제목 끝 번호를 PR 번호 하나만 남기고, 설명 칸은 PR 본문으로 바꾸라고 안내한다.

## 4. 병합

`dev`를 체크아웃한 상태에서 실행한다 (현재 브랜치가 병합 대상 브랜치이면 gh가 기본 브랜치로 바꿔 놓을 수 있다).

- 대상이 `dev`이면 squash 병합한다. 병합 메시지는 PR 제목 + ` (#<번호>)` + PR 본문으로 한다. 커밋에서 PR로 바로 찾아갈 수 있다. 결과는 `dev`에 부모 1개짜리 커밋 하나.

```bash
gh pr merge <번호> --squash --delete-branch --subject "<PR 제목> (#<번호>)" --body-file - <<'EOF'
<PR 본문>
EOF
```

- 병합 뒤 `git fetch` 후 `git log --format='%h %p | %s' origin/dev`로 부모가 1개인지 확인한다.
- 대상이 `main` / `master`이면 병합하지 않는다. Claude에서는 hook이 `gh pr merge`를 막고, 브라우저에서 병합 버튼을 누르는 것도 하지 않는다 (hook이 못 막으므로 규칙으로 지킨다).

## 5. 병합 뒤 브랜치 정리

`dev`에 병합이 끝난 기능 브랜치는 확인 없이 로컬과 원격 모두 삭제한다. 병합이 성공한 것을 확인한 뒤에만 한다.

1. 원격: `--delete-branch`가 지운다. 저장소 설정 "Automatically delete head branches"가 켜져 있어도 된다. 남아 있으면 `git push origin --delete feature/<이름>`.
2. 로컬: `git switch dev` → `git pull --ff-only` → 남아 있으면 `git branch -D feature/<이름>` → `git fetch --prune`. squash 병합은 git이 병합된 브랜치로 인식하지 못해서 `-d`가 아니라 `-D`를 쓴다.
3. `feature/`로 시작하지 않는 브랜치(`dev`, `main` 등)는 삭제하지 않는다. 삭제가 필요하면 확인을 받는다 (Claude에서는 hook이 확인을 요청한다).