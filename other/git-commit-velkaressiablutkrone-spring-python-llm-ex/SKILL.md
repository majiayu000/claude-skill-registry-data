---
name: git-commit
description: >
  Conventional Commits 형식으로 안전한 Git 커밋을 생성하는 스킬.
  "/git-commit"을 입력하거나, "커밋해줘", "변경사항 저장해줘" 같은 요청에 트리거된다.
  변경 사항을 분석하고 적절한 커밋 메시지를 생성한 뒤 실행한다.
---

# Git Commit

Conventional Commits 형식으로 안전한 Git 커밋을 생성하는 스킬이다.

## 언제 사용하는가

- 코드 변경 후 커밋이 필요할 때
- "커밋해줘", "변경사항 저장해줘" 요청 시

## 동작 흐름

### Step 1: 변경 사항 분석

다음 명령을 **병렬로** 실행하여 현재 상태를 파악한다:

```bash
git status                    # 변경/추가/삭제된 파일 목록
git diff                      # 언스테이지 변경 내용
git diff --staged             # 스테이지 변경 내용
git log --oneline -5          # 최근 커밋 메시지 스타일 참고
```

### Step 2: 위험 파일 감지

다음 패턴의 파일이 포함되어 있으면 **경고**하고 커밋에서 제외할지 확인한다:

- `.env`, `.env.*`
- `credentials.json`, `secret.*`
- `*.pem`, `*.key`
- `application-prod.properties`

### Step 3: 커밋 타입 추천

변경 내용을 분석하여 Conventional Commits 타입을 추천한다:

| 타입 | 용도 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | 새 도메인, 새 API 엔드포인트 |
| `fix` | 버그 수정 | 오류 수정, 예외 처리 |
| `docs` | 문서 변경 | README, TROUBLESHOOTING, 주석 |
| `refactor` | 리팩토링 (기능 변경 없음) | 코드 정리, 구조 개선 |
| `test` | 테스트 추가/수정 | 단위 테스트, 통합 테스트 |
| `chore` | 빌드/설정 변경 | build.gradle, docker-compose |
| `style` | 코드 스타일 변경 | 포맷팅, 세미콜론, 공백 |

### Step 4: 스코프 결정

도메인 기반 스코프를 사용한다:

- `feat(board):` — board 도메인 관련
- `fix(user):` — user 도메인 관련
- `chore(core):` — _core 관련
- `docs(ai):` — AI 가이드/스킬 관련
- 여러 도메인에 걸치면 스코프 생략 가능

### Step 5: 커밋 메시지 생성

```
{type}({scope}): {subject}

{body}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**규칙:**
- subject: 50자 이내, 명령형, 마침표 없음
- body: 선택사항, "왜" 변경했는지 설명, 한국어 허용
- subject는 한국어도 허용: `feat(board): 게시글 CRUD 추가`
- **반드시** `Co-Authored-By` 라인을 포함한다

### Step 6: 스테이징 및 커밋

관련 파일만 선택적으로 스테이징하고, HEREDOC 형식으로 커밋한다:

```bash
# 관련 파일만 선택적으로 스테이징 (git add -A 지양)
git add src/main/java/com/sample/llm/board/Board.java
git add src/main/java/com/sample/llm/board/BoardService.java

# HEREDOC 형식으로 커밋 (줄바꿈과 특수문자를 안전하게 처리)
git commit -m "$(cat <<'EOF'
feat(board): 게시글 CRUD 추가

게시글 등록/수정/삭제 기능 구현
Board Entity, Service, Repository 생성

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## 커밋 메시지 예시

```
feat(user): 회원가입 기능 추가
fix(board): 게시글 수정 시 제목 누락 오류 수정
docs(ai): gen-entity 스킬 추가
refactor(reply): 댓글 조회 쿼리 최적화
chore: build.gradle 의존성 업데이트
test(user): 로그인 단위 테스트 추가
style(board): 코드 포맷팅 정리
```

## 주의사항

- 변경 사항이 없으면 빈 커밋을 만들지 않는다
- `git add -A`나 `git add .` 대신 파일을 개별 지정한다
- `--no-verify`, `--amend` 같은 위험 옵션은 사용자가 명시적으로 요청한 경우에만 사용한다
- 커밋 전 `git status`로 스테이징 상태를 한번 더 확인한다
- 하나의 커밋에는 하나의 논리적 변경만 포함한다 — 관련 없는 변경은 분리 커밋
