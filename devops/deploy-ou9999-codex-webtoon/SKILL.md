---
description: "배포 스킬 - release 브랜치에 main을 merge 후 빌드 검증, 성공 시 push하여 Vercel 자동 배포 트리거"
allowed-tools: ["Bash", "Read", "AskUserQuestion"]
---

# 배포 Skill

`release` 브랜치에 `main` 반영, 빌드 검증 통과 후 push, Vercel 자동 배포 트리거.

## 배포 플로우 개요

1. 사전 상태 점검
2. `release` 브랜치 체크아웃 및 `main` 반영
3. 빌드 검증 (`pnpm build`)
4. push (Vercel 자동 배포 트리거)
5. 원래 브랜치로 복귀

## 실행 순서

### 1. 사전 상태 점검

아래 명령으로 현재 상태 확인:

```bash
git status --porcelain
git rev-parse --abbrev-ref HEAD
```

**중단 조건:**

- working tree dirty 상태면 중단, 사용자에게 커밋/스태시 요청
- 현재 브랜치 변수 저장 (작업 후 복귀용)

`origin/main`과 `origin/release` 최신화:

```bash
git fetch origin main release --prune
```

### 2. release 브랜치 체크아웃 및 main 반영

```bash
git checkout release
git pull --ff-only origin release
git merge origin/main --no-edit
```

**주의:**

- `--ff-only` 실패 시 원격 release와 로컬 divergence → 사용자 확인 필수
- merge conflict 발생 시 **즉시 중단** 및 사용자 알림
  (자동으로 `git merge --abort` 실행 후 원래 브랜치로 복귀)

### 3. 빌드 검증

`pnpm build`로 프로덕션 빌드 검증.
(빌드는 장시간 실행 가능 작업이므로 `run_in_background` 사용을 고려)

```bash
pnpm build
```

**실패 시:**

- push하지 않음
- merge 커밋을 되돌릴지 사용자에게 확인
  (되돌림: `git reset --hard origin/release`)
- 원래 브랜치로 복귀 후 종료

### 4. push (Vercel 자동 배포)

빌드 성공 시에만 push:

```bash
git push origin release
```

push 성공 후 Vercel 자동 배포 시작.

### 5. 원래 브랜치로 복귀

1단계에서 기억해둔 원래 브랜치로 복귀:

```bash
git checkout <원래 브랜치>
```

## 금지 사항

- `--no-verify`, `--force`, `--force-with-lease` 사용 금지
- 빌드 실패 시 push 절대 금지
- merge conflict 자동 해결 금지 → 반드시 사용자에게 위임
- `release` 브랜치에 직접 커밋 추가 금지 (main merge만 허용)

## 확장 포인트 (추후 추가)

CI/CD 인프라 확장 시 스킬 내부 통합 후보.

- 배포 전 lint/type-check 통합 (`pnpm lint`)
- 버전 태그 자동 생성 (`git tag v0.x.y`)
- 배포 후 smoke test (대상 URL heartbeat 체크)
- Slack/Discord 배포 알림 hook
- 체인지로그 생성 및 GitHub Release 연동
