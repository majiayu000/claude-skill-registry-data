---
name: deploy-service
description: |
  **Docker/SSH 기반** 마이크로서비스 직접 배포.
  로컬 빌드 → SSH 전송 → PM2 재시작.
  Use when:
  (1) ms-* 서비스 배포 (ms-notifier, ms-scheduler 등),
  (2) Docker 빌드/이미지 생성,
  (3) PM2 재시작/롤백,
  (4) SSH 접근 필요한 직접 배포.
  ⚠️ GitHub Actions/Milestone 기반 배포는 deployer 사용.
tools: [Bash, Read]
model: inherit
triggers:
  - ms-* 배포
  - Docker 빌드
  - PM2 재시작
  - 롤백
  - SSH 배포
---

> **호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: deploy-service 호출 - {service_name} ({env})` 시스템 메시지를 첫 줄에 출력하세요.

# Deploy Service Skill

> **Docker/SSH 기반** 마이크로서비스 직접 배포 자동화
>
> ⚠️ **deployer와 혼동 주의**: GitHub Actions/Milestone 기반 배포는 `deployer` 사용

## 🔴 deploy-service vs deployer 선택 기준

| 조건 | 선택 스킬 | 이유 |
|------|----------|------|
| ms-* 마이크로서비스 배포 | `deploy-service` | Docker + PM2 방식 |
| "Docker 빌드", "PM2" 언급 | `deploy-service` | SSH 직접 제어 |
| SSH 접근 필요한 직접 배포 | `deploy-service` | 원격 서버 직접 접근 |
| 프로젝트 별칭 사용 (랜드, 오피스 등) | `deployer` | projects.md에 별칭 등록 |
| "Milestone", "릴리즈" 언급 | `deployer` | GitHub 릴리즈 워크플로우 |
| GitHub Actions 기반 배포 | `deployer` | CI/CD 자동 트리거 |

## 배포 환경

| 환경 | 대상 | 배포 방식 |
|------|------|----------|
| **development** | 로컬 | Docker Compose |
| **staging** | AWS Lightsail | Docker + PM2 |
| **production** | AWS Lightsail | Docker + PM2 (Blue-Green) |

## 서비스별 배포 정보

| 서비스 | 포트 | 배포 서버 | PM2 이름 |
|--------|------|----------|---------|
| ms-notifier | 3000 | lightsail-ms-1 | notifier |
| ms-scheduler | 3003 | lightsail-ms-1 | scheduler |
| ms-ledger | 3000 | lightsail-ms-2 | ledger |
| ms-media-processor | 3001 | lightsail-ms-1 | media |
| ms-collector | 3002 | lightsail-ms-1 | collector |
| ms-allocator | 3004 | lightsail-ms-2 | allocator |
| ms-gamer | 8080 | lightsail-game | gamer |

## 워크플로우

### Phase 0: 배포 전 검증 (NON-NEGOTIABLE)

```bash
# 1. 현재 브랜치 확인
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "dev" ]; then
  echo "⚠️ 경고: main/dev 브랜치가 아닙니다 ($BRANCH)"
fi

# 2. 미커밋 변경사항 확인
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ 미커밋 변경사항이 있습니다"
  exit 1
fi

# 3. 테스트 실행
npm test || go test ./...

# 4. 빌드 검증
npm run build || go build ./...
```

---

### Phase 1: Docker 이미지 빌드

```bash
# 서비스명과 버전 설정
SERVICE_NAME="ms-{service}"
VERSION=$(git describe --tags --always)

# Docker 이미지 빌드
docker build -t $SERVICE_NAME:$VERSION -t $SERVICE_NAME:latest .

# 이미지 크기 확인
docker images $SERVICE_NAME:latest --format "{{.Size}}"
```

### 멀티 스테이지 빌드 예시 (Node.js)

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["npm", "start"]
```

---

### Phase 2: 로컬 테스트 (Docker Compose)

```bash
# Docker Compose로 로컬 실행
docker compose up -d $SERVICE_NAME

# 헬스체크
sleep 5
curl -s http://localhost:{port}/api/health | jq

# 로그 확인
docker compose logs -f $SERVICE_NAME
```

---

### Phase 3: 원격 서버 배포

#### 방법 A: Docker 이미지 푸시 (권장)

```bash
# Docker Hub 또는 ECR에 푸시
docker tag $SERVICE_NAME:$VERSION registry.example.com/$SERVICE_NAME:$VERSION
docker push registry.example.com/$SERVICE_NAME:$VERSION

# 원격 서버에서 풀 및 실행
ssh user@server << 'EOF'
  docker pull registry.example.com/$SERVICE_NAME:$VERSION
  docker stop $SERVICE_NAME || true
  docker rm $SERVICE_NAME || true
  docker run -d --name $SERVICE_NAME -p {port}:{port} registry.example.com/$SERVICE_NAME:$VERSION
EOF
```

#### 방법 B: 소스 배포 + PM2

```bash
# 원격 서버에 배포
ssh user@server << 'EOF'
  cd /app/$SERVICE_NAME
  git pull origin main
  npm ci --production
  npm run build
  pm2 restart $PM2_NAME
EOF
```

---

### Phase 4: 헬스체크 및 검증

```bash
# 배포 후 헬스체크 (최대 30초 대기)
MAX_RETRIES=6
RETRY_INTERVAL=5

for i in $(seq 1 $MAX_RETRIES); do
  HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://server:{port}/api/health)
  if [ "$HEALTH" = "200" ]; then
    echo "✅ 헬스체크 성공"
    break
  fi
  echo "⏳ 헬스체크 대기 중... ($i/$MAX_RETRIES)"
  sleep $RETRY_INTERVAL
done

if [ "$HEALTH" != "200" ]; then
  echo "❌ 헬스체크 실패 - 롤백 필요"
fi
```

---

### Phase 5: 롤백 (필요 시)

```bash
# 이전 버전으로 롤백
PREVIOUS_VERSION=$(docker images $SERVICE_NAME --format "{{.Tag}}" | grep -v latest | head -2 | tail -1)

ssh user@server << EOF
  docker stop $SERVICE_NAME
  docker rm $SERVICE_NAME
  docker run -d --name $SERVICE_NAME -p {port}:{port} $SERVICE_NAME:$PREVIOUS_VERSION
EOF

echo "🔄 롤백 완료: $PREVIOUS_VERSION"
```

## 출력 포맷

### 배포 성공

```markdown
[SEMO] Skill: deploy-service 호출 - ms-{service} (staging)

=== 배포 결과 ===

## 배포 정보
| 항목 | 값 |
|------|-----|
| 서비스 | ms-{service} |
| 환경 | staging |
| 버전 | v1.2.3 (abc1234) |
| 서버 | lightsail-ms-1 |

## 실행 단계
| 단계 | 상태 | 소요시간 |
|------|------|----------|
| 사전 검증 | ✅ | 5s |
| Docker 빌드 | ✅ | 45s |
| 이미지 푸시 | ✅ | 30s |
| 서버 배포 | ✅ | 15s |
| 헬스체크 | ✅ | 10s |

## 결과
✅ **배포 성공**

- 배포 시간: 2025-01-22 14:30:00 KST
- 총 소요시간: 1m 45s
- 헬스체크: HTTP 200

## 확인 명령어
```bash
# 로그 확인
ssh user@server "pm2 logs {service} --lines 50"

# 상태 확인
curl https://api.example.com/health
```
```

### 배포 실패

```markdown
[SEMO] Skill: deploy-service 호출 - ms-{service} (staging)

=== 배포 실패 ===

## 오류 발생 단계
**Phase 4: 헬스체크**

## 오류 내용
```
❌ 헬스체크 실패
HTTP 503 - Service Unavailable
```

## 자동 롤백
| 항목 | 상태 |
|------|------|
| 이전 버전 | v1.2.2 |
| 롤백 실행 | ✅ 완료 |
| 헬스체크 | ✅ 정상 |

## 원인 분석 필요
1. 로그 확인: `ssh user@server "docker logs ms-{service}"`
2. 환경변수 확인: `.env` 파일 검토
3. DB 연결 확인: `debug-service` 스킬 실행

## 다음 단계
- `debug-service` 스킬로 원인 분석
- 수정 후 재배포
```

## 환경별 체크리스트

### Staging 배포

- [ ] dev 브랜치 최신화
- [ ] 테스트 통과
- [ ] 빌드 성공
- [ ] Docker 이미지 생성
- [ ] 헬스체크 통과

### Production 배포

- [ ] main 브랜치 최신화
- [ ] 스테이징 테스트 완료
- [ ] 팀 승인 (Slack 알림)
- [ ] 백업 확인
- [ ] 트래픽 분산 준비 (Blue-Green)
- [ ] 롤백 계획 수립
- [ ] 배포 후 모니터링

## Related Skills

- [debug-service](../debug-service/SKILL.md) - 배포 후 문제 진단
- [health-check](../health-check/SKILL.md) - 환경 검증
- [review](../review/SKILL.md) - 배포 전 코드 리뷰

## References

- [Microservices Context](/.claude/memory/microservices.md) - 서비스 배포 정보
