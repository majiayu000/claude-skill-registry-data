---
name: rollback-service
description: 서비스를 이전 버전으로 롤백. Use when (1) 롤백 요청, (2) 이전 버전 복원, (3) /SEMO:rollback 커맨드.
tools: [Bash, Read, Write]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: rollback-service 호출 - {환경}/{서비스}/{태그}` 시스템 메시지를 첫 줄에 출력하세요.

# rollback-service

> 서비스 롤백 Skill

## 개요

서비스를 이전 버전으로 롤백합니다.

## 트리거

- "롤백해줘"
- "이전 버전으로 되돌려"
- `/SEMO:rollback`

## 입력 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|----------|------|------|------|
| environment | ✅ | 환경 | `dev`, `stg` |
| service | ✅ | 롤백할 서비스 | `cm-land` |
| target_tag | ❌ | 롤백 대상 태그 | `v1.2.2`, `stg-abc1234-20240115` |

## 실행 절차

### 1. 현재 태그 확인

```bash
# 환경 파일에서 현재 태그 확인
grep "{SERVICE}_TAG" .env.{env}
```

### 2. 이전 태그 조회

```bash
# Docker Hub에서 이미지 태그 목록
docker images semicolonmanager/{service} --format "{{.Tag}}"
```

### 3. 환경변수 수정

```bash
# 태그 변경
sed -i 's/{SERVICE}_TAG=.*/{SERVICE}_TAG={target_tag}/' .env.{env}
```

### 4. 서비스 재시작

```bash
docker-compose --env-file .env.{env} pull {service}
docker-compose --env-file .env.{env} up -d --no-deps {service}
```

### 5. 상태 확인

```bash
docker-compose --env-file .env.{env} ps {service}
curl -f http://localhost:{port}/health
```

## 출력

### 성공

```markdown
[SEMO] rollback-service: 롤백 완료 ✅

**롤백 결과**

환경: `{environment}`
서비스: `{service}`

| 항목 | 값 |
|------|-----|
| 이전 태그 | `{old_tag}` |
| 롤백 태그 | `{target_tag}` |
| 상태 | running |
| 헬스 | healthy |

롤백 시간: {timestamp}
```

### 실패

```markdown
[SEMO] rollback-service: 롤백 실패 ❌

**롤백 결과**

환경: `{environment}`
서비스: `{service}`

### 오류
```
{error_message}
```

### 수동 복구
1. 이미지 확인: `docker images semicolonmanager/{service}`
2. 수동 태그 변경
3. 서비스 재시작
```

## 롤백 전략

### 이미지 태그 롤백

```bash
# 1. 태그 변경
sed -i 's/CM_LAND_TAG=.*/CM_LAND_TAG=v1.2.2/' .env.stg

# 2. Pull & Restart
docker-compose --env-file .env.stg pull cm-land
docker-compose --env-file .env.stg up -d --no-deps cm-land
```

### Git 기반 롤백

```bash
# 1. 이전 커밋의 환경 파일
git checkout HEAD~1 -- .env.stg

# 2. 전체 재배포
docker-compose --env-file .env.stg pull
docker-compose --env-file .env.stg up -d
```

### 전체 스택 롤백

```bash
# 1. 이전 커밋 체크아웃
git checkout HEAD~1

# 2. 전체 재배포
docker-compose --env-file .env.stg pull
docker-compose --env-file .env.stg up -d
```

## 이전 태그 찾기

### Docker Hub에서 조회

```bash
# 로컬 이미지 태그 목록
docker images semicolonmanager/{service} --format "{{.Tag}}" | head -10

# 또는 Git 로그에서 태그 변경 이력
git log --oneline -p -- .env.stg | grep "_TAG=" | head -10
```

### 추천 이전 태그

최근 성공적으로 배포된 태그 기준:
1. 현재 -1 버전
2. 가장 최근 `v*.*.*` 태그
3. Git 이력 기반 이전 태그

## 참조

- [deploy-master agent](../../agents/deploy-master/deploy-master.md)
- [zero-downtime-deploy.md](../../agents/deploy-master/references/zero-downtime-deploy.md)
