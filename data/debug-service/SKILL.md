---
name: debug-service
description: |
  마이크로서비스 디버깅 및 로그 분석. Use when:
  (1) 서비스 에러 분석, (2) 로그 확인, (3) 헬스체크 실패 원인 파악,
  (4) DB 연결 상태 확인, (5) 환경변수 검증.
tools: [Bash, Read, Grep]
model: inherit
triggers:
  - 서비스 디버깅
  - 로그 확인
  - 에러 분석
  - 헬스체크 실패
  - DB 연결 확인
---

> **호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: debug-service 호출 - {service_name}` 시스템 메시지를 첫 줄에 출력하세요.

# Debug Service Skill

> 마이크로서비스 디버깅 및 문제 진단

## Quick Start

```bash
# 서비스 상태 확인
curl -s http://localhost:{port}/api/health | jq

# Docker 로그 확인 (최근 100줄)
docker logs --tail 100 ms-{service}

# PM2 로그 확인
pm2 logs {service} --lines 100
```

## 진단 워크플로우

### Phase 1: 서비스 상태 확인

```bash
# 헬스체크 엔드포인트 테스트
SERVICE_PORT={port}
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:$SERVICE_PORT/api/health)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ 헬스체크 정상"
  echo "$BODY" | jq
else
  echo "❌ 헬스체크 실패 (HTTP $HTTP_CODE)"
fi
```

**확인 항목**:
- [ ] HTTP 응답 코드 (200 정상)
- [ ] 응답 시간 (1초 이내 권장)
- [ ] 응답 본문 (status: healthy)

### Phase 2: 로그 수집

#### Docker 환경

```bash
# 최근 로그 확인
docker logs --tail 200 ms-{service} 2>&1

# 에러 로그만 필터링
docker logs ms-{service} 2>&1 | grep -i "error\|exception\|fail"

# 실시간 로그 스트림
docker logs -f ms-{service}
```

#### PM2 환경

```bash
# PM2 프로세스 상태
pm2 status

# 특정 서비스 로그
pm2 logs {service} --lines 200

# 에러 로그만
pm2 logs {service} --err --lines 100
```

#### 시스템 로그

```bash
# journalctl (systemd 서비스)
journalctl -u ms-{service} -n 200 --no-pager
```

### Phase 3: 데이터베이스 연결 확인

#### PostgreSQL

```bash
# 연결 테스트
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1"

# 연결 수 확인
psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname = '$DB_NAME'"

# 락 확인
psql -c "SELECT * FROM pg_locks WHERE NOT granted"
```

#### Prisma 상태

```bash
# Prisma 연결 테스트
npx prisma db pull --print 2>&1 | head -5

# 마이그레이션 상태
npx prisma migrate status
```

#### Redis (해당 시)

```bash
# Redis 연결 테스트
redis-cli -h $REDIS_HOST ping

# 키 개수 확인
redis-cli -h $REDIS_HOST dbsize
```

### Phase 4: 환경변수 검증

```bash
# 필수 환경변수 확인
REQUIRED_VARS=("DATABASE_URL" "NODE_ENV" "PORT")
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ 누락: $var"
  else
    echo "✅ 설정됨: $var"
  fi
done

# .env.example과 비교
if [ -f ".env.example" ]; then
  echo "=== .env.example에 정의된 변수 ==="
  grep -v "^#" .env.example | grep "=" | cut -d= -f1
fi
```

### Phase 5: 리소스 사용량 확인

```bash
# Docker 컨테이너 리소스
docker stats ms-{service} --no-stream

# PM2 프로세스 리소스
pm2 monit

# 시스템 리소스
free -h
df -h
```

## 출력 포맷

### 진단 결과

```markdown
[SEMO] Skill: debug-service 호출 - ms-{service}

=== 서비스 진단 보고서 ===

## 1. 서비스 상태
| 항목 | 상태 | 상세 |
|------|------|------|
| 헬스체크 | ✅ 정상 | HTTP 200, 응답시간 45ms |
| 프로세스 | ✅ 실행 중 | PID 12345 |
| 포트 | ✅ 리스닝 | :3000 |

## 2. 데이터베이스
| 항목 | 상태 | 상세 |
|------|------|------|
| PostgreSQL | ✅ 연결됨 | 활성 연결 5개 |
| Prisma | ✅ 동기화됨 | 마이그레이션 최신 |

## 3. 최근 에러 로그
```
[2025-01-01 10:00:00] ERROR: Connection timeout
[2025-01-01 10:00:05] ERROR: Retry failed
```

## 4. 리소스 사용량
- CPU: 15%
- Memory: 256MB / 512MB
- Disk: 45% 사용

## 5. 권장 조치
- ⚠️ DB 연결 타임아웃 발생 → 연결 풀 크기 확인
- ⚠️ 메모리 50% 이상 사용 → 모니터링 필요
```

### 문제 발견 시

```markdown
## 진단 결과: ❌ 문제 발견

### Critical Issues
1. **DB 연결 실패**
   - 원인: DATABASE_URL 환경변수 미설정
   - 해결: `.env` 파일에 DATABASE_URL 추가

2. **헬스체크 타임아웃**
   - 원인: 서비스 응답 없음
   - 해결: 서비스 재시작 필요 (`pm2 restart {service}`)

### 권장 명령어
```bash
# 서비스 재시작
pm2 restart {service}

# 로그 실시간 확인
pm2 logs {service} -f
```
```

## 서비스별 포트 참조

| 서비스 | 포트 | 헬스체크 경로 |
|--------|------|--------------|
| ms-notifier | 3000 | /api/health |
| ms-scheduler | 3003 | /api/health |
| ms-ledger | 3000 | /api/health |
| ms-media-processor | 3001 | /api/health |
| ms-crawler | 3333 | /api/health |
| ms-collector | 3002 | /api/health |
| ms-allocator | 3004 | /api/health |
| ms-gamer | 8080 | /health |

## Related Skills

- [health-check](../health-check/SKILL.md) - 개발 환경 검증
- [review](../review/SKILL.md) - 코드 리뷰

## References

- [Microservices Context](/.claude/memory/microservices.md) - 서비스 목록 및 컨텍스트
