---
name: git-pr
description: >
  Git Flow 브랜치 전략에 따라 구조화된 템플릿으로 GitHub PR을 생성하는 스킬.
  "/git-pr"을 입력하거나, "PR 만들어줘", "풀리퀘스트 생성해줘" 같은 요청에 트리거된다.
  변경 사항을 분석하고 적절한 base 브랜치와 PR 본문을 자동 생성한다.
---

# Git PR

Git Flow 브랜치 전략에 따라 구조화된 GitHub PR을 생성하는 스킬이다.

## 언제 사용하는가

- 기능 개발 완료 후 PR을 만들 때
- "PR 만들어줘", "풀리퀘스트 생성해줘" 요청 시

## 동작 흐름

### Step 1: base 브랜치 동적 감지

먼저 프로젝트의 실제 브랜치 구조를 파악한다:

```bash
git branch --show-current                    # 현재 브랜치
git branch -a                                # 로컬+원격 브랜치 목록
git status                                   # 커밋되지 않은 변경 확인
```

**base 브랜치 결정 로직:**

1. `develop` 브랜치가 존재하는지 확인한다 (`git branch -a`로 로컬+원격 모두 확인)
2. 존재 여부에 따라 다음 규칙을 적용한다:

**`develop` 브랜치가 있는 경우 (Git Flow):**

| 현재 브랜치 | base 브랜치 | 설명 |
|-------------|-------------|------|
| `feature/*`, `feat/*` | `develop` | 기능 개발 완료 → develop에 머지 |
| `release/*` | `main`/`master` | 릴리스 준비 완료 → main에 머지 |
| `hotfix/*` | `main`/`master` | 긴급 수정 → main에 머지 |
| `develop` | `main`/`master` | 개발 통합 → main에 머지 |

**`develop` 브랜치가 없는 경우 (GitHub Flow):**

| 현재 브랜치 | base 브랜치 | 설명 |
|-------------|-------------|------|
| `feature/*`, `feat/*` | `main`/`master` | 기능 개발 완료 → main에 머지 |
| `hotfix/*` | `main`/`master` | 긴급 수정 → main에 머지 |
| 기타 | `main`/`master` | 기본적으로 main에 머지 |

3. `main`과 `master` 중 실제 존재하는 브랜치를 사용한다
4. 자동 판별이 불확실하면 사용자에게 확인한다

### Step 2: 현재 상태 분석

감지된 base 브랜치 기준으로 **병렬** 실행한다:

```bash
git log --oneline {base}..HEAD               # base 대비 커밋 목록
git diff {base}...HEAD --stat                # 변경 파일 요약
git ls-remote --heads origin {현재브랜치}     # 원격 브랜치 존재 여부
```

### Step 3: 커밋되지 않은 변경 처리

커밋되지 않은 변경이 있으면 먼저 커밋할지 확인한다:

```
커밋되지 않은 변경 사항이 있습니다:
  수정됨: docker-compose.yml
  수정됨: src/main/resources/application.yml

먼저 커밋할까요, 커밋 없이 PR을 생성할까요?
```

### Step 4: PR 제목 생성

커밋 히스토리를 분석하여 PR 제목을 생성한다:

**규칙:**
- 70자 이내
- Conventional Commits 타입 포함
- 한국어 허용

**예시:**
```
feat(board): 게시글 CRUD 기능 추가
fix(user): 로그인 시 세션 저장 오류 수정
refactor(reply): 댓글 조회 쿼리 최적화
```

### Step 5: push 확인

원격에 현재 브랜치가 없거나 최신이 아니면 **PR 생성 전에** push를 먼저 진행한다:

```bash
# push 필요 시
git push -u origin {브랜치명}
```

### Step 6: PR 생성

HEREDOC 형식으로 본문을 자동 생성하여 PR을 만든다:

```bash
gh pr create --base {base브랜치} --title "{PR 제목}" --body "$(cat <<'EOF'
## 변경 요약
- [커밋 히스토리 기반 주요 변경 사항 요약]
- [2~5개 bullet point]

## 변경 유형
- [ ] feat: 새로운 기능
- [ ] fix: 버그 수정
- [ ] refactor: 리팩토링
- [ ] docs: 문서 변경
- [ ] test: 테스트 추가/수정
- [ ] chore: 빌드/설정 변경

## 주요 변경 파일
| 파일 | 변경 내용 |
|------|-----------|
| `Board.java` | 게시글 Entity 생성 |
| `BoardService.java` | CRUD 비즈니스 로직 |

## 테스트 방법
1. [검증 절차 기술]
2. [예상 결과 기술]

## 체크리스트
- [ ] common-rule.md 컨벤션을 준수했는가
- [ ] Entity에 EAGER fetch가 없는가
- [ ] REST API 응답에 Resp 래퍼를 사용했는가
- [ ] SSR/REST Controller가 분리되어 있는가
- [ ] 민감 정보(.env 등)가 포함되지 않았는가
EOF
)"
```

### Step 7: 결과 안내

```
PR이 생성되었습니다!
URL: https://github.com/{owner}/{repo}/pull/{번호}

base: master ← feat/board-crud
커밋 수: 3
변경 파일: 7개
```

## PR 본문 커스텀

사용자가 추가 정보를 제공하면 템플릿에 반영한다:

- "스크린샷 추가해줘" → `## 스크린샷` 섹션 추가
- "관련 이슈 #5" → `## 관련 이슈` 섹션에 `Closes #5` 추가
- "리뷰어 지정해줘" → `--reviewer {사용자}` 옵션 추가

## 주의사항

- 커밋되지 않은 변경이 있으면 먼저 커밋할지 확인한다
- `main`/`master`에서 직접 PR을 만들지 않는다
- `gh` CLI가 설치되어 있고 인증이 완료되어 있어야 한다 — 없으면 안내
- PR 생성 후 URL을 반드시 사용자에게 보여준다
- 체크리스트는 프로젝트의 common-rule.md 기반으로 구성한다
