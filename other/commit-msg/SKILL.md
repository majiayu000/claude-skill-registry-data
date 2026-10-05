---
name: commit-msg
description: >
  변경사항을 분석하고 프로젝트 스타일에 맞는 커밋 메시지를 추천한다.
  git commit, git add, git push는 실행하지 않는다.
  "커밋 만들어", "커밋해줘", "commit", "변경사항 커밋",
  "커밋 메시지 어떻게 쓰지", "커밋 메시지 추천", "뭐라고 커밋하지",
  "make a commit", "commit message", "what should I commit as"
  등에서 트리거.
---

# Commit Message

커밋 메시지를 추천하는 스킬. 메시지 후보를 제시하고 끝낸다.

## Mode

이 스킬 활성 중 git add, git commit, git push를 실행하지 않는다.
사용자가 "커밋해줘"라고 해도 메시지 추천까지만 수행한다.
실제 커밋은 사용자가 직접 하거나 `/commit` 커맨드를 사용한다.

## 워크플로우

1. 가드레일 체크
2. 변경사항 분석 (`git status`, `git diff`)
3. 스타일 분석 (`git log --oneline -10`)
4. 커밋 메시지 후보 1~2개 제시

## 가드레일

### 시크릿 파일

변경 목록에 다음 패턴이 있으면 경고한다:

- `.env`, `.env.*`
- `credentials.*`, `*secret*`, `*.pem`, `*.key`
- `*token*`, `*password*` (설정/시크릿 파일인 경우)

### main/master 브랜치

현재 브랜치가 main/master이면 브랜치 분리를 제안한다.

## 스타일 분석

```bash
git log --oneline -10
```

최근 커밋의 패턴(prefix, 언어, 길이, 형식)을 파악하고 일관성을 유지한다. 자기 스타일을 강요하지 않는다.

## 출력

아래 형식으로 출력한다:

(가드레일 경고가 있으면 여기에 먼저 표시)

**추천 커밋 메시지:**

1. `<메시지 후보 1>`
2. `<메시지 후보 2>` (선택지가 있을 때만)

## Gotchas

- `git add .`은 `.gitignore`에 없는 시크릿 파일을 포함시킨다. `.env.local`처럼 gitignore에 빠진 변형 파일이 특히 위험.
- Co-Authored-By를 무조건 붙이면 프로젝트 컨벤션과 충돌할 수 있다. 기존 커밋에 어트리뷰션 패턴이 있는지 먼저 확인.
- main에 직접 커밋 후 force-push하면 다른 사람의 작업을 덮어쓴다.
