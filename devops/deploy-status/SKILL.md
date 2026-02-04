---
name: deploy-status
description: 배포 상태 실시간 모니터링 및 Health Check. GitHub Actions 워크플로우 진행 상황, K8s Pod 상태, Health Check 결과 확인. "배포 상태", "배포 확인", "정상 동작" 요청 시 사용.
---

# 배포 상태 모니터링 Skill

배포 후 또는 배포 중 시스템 상태를 실시간으로 모니터링하고 Health Check를 수행합니다.

## 사용 시점

다음과 같은 요청을 받았을 때 이 Skill을 사용하세요:
- "배포 상태 확인", "배포 잘 됐어?"
- "서비스 정상 동작해?", "Health Check"
- "지금 배포 어떻게 되고 있어?"
- 배포 완료 후 자동 검증 시
- 롤백 후 상태 확인 시

## 실행 단계

### 1단계: 환경 확인

모니터링할 환경을 결정하세요:
- 사용자가 명시한 환경 사용 (preview/production)
- 명시되지 않은 경우 현재 브랜치로 판단:
  - wonuk 브랜치 → preview
  - donghee 브랜치 → production

```bash
CURRENT_BRANCH=$(git branch --show-current)
echo "현재 브랜치: $CURRENT_BRANCH"
```

### 2단계: GitHub Actions 워크플로우 상태 확인

#### gh CLI 사용 가능한 경우
```bash
bash /home/donghee/bodam/.claude/skills/deploy-status/scripts/check-github-actions.sh
```

**확인 사항**:
- 최근 워크플로우 실행 상태
- Backend CI/CD 진행 상황
- Frontend CI/CD 진행 상황
- 실패한 작업 여부

#### gh CLI 없는 경우
사용자에게 GitHub Actions 페이지 링크 제공:
```
GitHub Actions 워크플로우 상태 확인:
https://github.com/{owner}/{repo}/actions

최근 실행 목록에서:
- ✅ 녹색 체크: 성공
- ❌ 빨간 X: 실패
- 🟡 노란 점: 진행 중
```

### 3단계: Backend 상태 확인 (K8s)

```bash
bash /home/donghee/bodam/.claude/skills/deploy-status/scripts/check-backend-status.sh {preview|production}
```

**확인 항목**:

#### Deployment 상태
- Desired vs Available Replicas
- 업데이트 전략 상태
- 현재 이미지 태그

#### Pod 상태
- Running/Pending/Failed Pod 개수
- 재시작 횟수
- 리소스 사용량 (CPU, Memory)

#### Service 상태
- ClusterIP 할당 여부
- 엔드포인트 연결 상태
- 외부 접근 가능 여부

#### 최근 이벤트
- 배포 관련 이벤트
- 에러 또는 경고 이벤트
- Pod 스케줄링 이벤트

### 4단계: Frontend 상태 확인 (Vercel)

```bash
bash /home/donghee/bodam/.claude/skills/deploy-status/scripts/check-frontend-status.sh {preview|production}
```

**확인 항목**:

#### 배포 상태
- 현재 활성 배포 버전
- 배포 URL
- 배포 시간

#### 빌드 상태
- 빌드 성공/실패 여부
- 빌드 로그 (오류 시)

#### 도메인 상태
- 커스텀 도메인 연결 상태
- SSL 인증서 상태

### 5단계: Health Check 실행

```bash
bash /home/donghee/bodam/.claude/skills/deploy-status/scripts/health-check.sh {preview|production}
```

**검증 항목**:

#### Backend API Health Check
```bash
# Preview
curl -f -s https://preview-api.bodam.com/health

# Production
curl -f -s https://api.bodam.com/health
```

**기대 응답**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-10T14:00:00Z"
}
```

#### Frontend Health Check
```bash
# Preview
curl -f -s -o /dev/null -w "%{http_code}" https://preview.bodam.com

# Production
curl -f -s -o /dev/null -w "%{http_code}" https://bodam.com
```

**기대 응답**: HTTP 200

#### 주요 API 엔드포인트 테스트
```bash
# API 버전 확인
curl -s https://api.bodam.com/api/v1/health

# 인증 엔드포인트 (접근만 확인, 401 정상)
curl -s -o /dev/null -w "%{http_code}" https://api.bodam.com/api/v1/auth/me
```

### 6단계: 데이터베이스 연결 상태

```bash
bash /home/donghee/bodam/.claude/skills/deploy-status/scripts/check-db-status.sh {preview|production}
```

**확인 방법**:
- Backend Pod에서 DB 연결 테스트
- Connection Pool 상태 확인
- 최근 쿼리 에러 로그

### 7단계: 모니터링 대시보드 상태

사용자에게 Grafana/Prometheus 대시보드 안내:

```
📊 모니터링 대시보드:

Grafana (메트릭 대시보드):
- URL: http://localhost:3001 (로컬) 또는 {production-grafana-url}
- 확인 항목:
  - API 응답 시간
  - 요청 처리율 (RPS)
  - 에러율
  - CPU/Memory 사용량
  - DB Connection Pool 상태

Prometheus (메트릭 수집):
- URL: http://localhost:9091
- 쿼리 예시:
  - http_requests_total
  - http_request_duration_seconds
  - db_connections_active
```

### 8단계: 상태 리포트 생성

모든 확인 완료 후 종합 리포트를 사용자에게 제공:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 배포 상태 리포트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

환경: {preview/production}
확인 시간: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 GitHub Actions 워크플로우
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend CI/CD:
  ✅ 완료 (8분 32초 소요)
  커밋: abc123 - "feat: 새 기능 추가"

Frontend CI/CD:
  ✅ 완료 (6분 15초 소요)
  배포 URL: https://preview.bodam.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☸️  Backend (Kubernetes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Deployment: bodam-backend
  ✅ 3/3 Pods Ready
  이미지: registry.digitalocean.com/bodam/backend:production-abc123

Pod 상태:
  ✅ bodam-backend-7d9f8c6b5d-x4k2p  Running  (재시작: 0회)
  ✅ bodam-backend-7d9f8c6b5d-y5m3q  Running  (재시작: 0회)
  ✅ bodam-backend-7d9f8c6b5d-z6n4r  Running  (재시작: 0회)

리소스 사용량:
  CPU: 45% / 100% (요청/제한)
  Memory: 512MB / 1GB (요청/제한)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Frontend (Vercel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

배포 상태: ✅ 활성
배포 URL: https://preview.bodam.com
버전: v1.2.3
빌드 시간: 3분 42초

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💚 Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend API:
  ✅ /health → HTTP 200 (응답 시간: 45ms)
  ✅ /api/v1/health → HTTP 200 (응답 시간: 52ms)

Frontend:
  ✅ 홈페이지 → HTTP 200 (응답 시간: 320ms)
  ✅ 렌더링 정상 ("보담" 텍스트 확인)

데이터베이스:
  ✅ PostgreSQL 연결 정상
  ✅ Connection Pool: 5/10 활성

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 종합 상태: ✅ 정상
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

모든 시스템이 정상 동작 중입니다.

다음 단계:
- 주요 기능 테스트 권장
- 모니터링 대시보드 확인
- 에러 로그 모니터링

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 상태별 대응 가이드

### ✅ 정상 상태
- 모든 검증 통과
- 추가 조치 불필요
- 정기적 모니터링 권장

### ⚠️ 경고 상태
**예시 경고**:
- Pod 재시작 횟수 높음 (5회 이상)
- 응답 시간 느림 (500ms 이상)
- CPU/Memory 사용량 높음 (80% 이상)

**대응**:
- 모니터링 강화
- 로그 확인
- 필요시 스케일링

### ❌ 오류 상태
**예시 오류**:
- Health Check 실패
- Pod CrashLoopBackOff
- 배포 실패

**대응**:
1. 즉시 롤백 검토 (`rollback` Skill)
2. 에러 로그 수집 및 분석
3. 근본 원인 파악
4. Hotfix 또는 재배포

## 실시간 모니터링 (연속 모드)

사용자가 실시간 모니터링을 원하는 경우:

```bash
# Pod 로그 실시간 스트리밍
kubectl logs -f deployment/bodam-backend -n bodam-{env}

# Pod 상태 실시간 감시
watch -n 5 kubectl get pods -n bodam-{env} -l app=bodam-backend

# GitHub Actions 실시간 모니터링 (gh CLI)
gh run watch
```

## 알림 설정 (Slack)

배포 상태를 Slack으로 알림 받는 방법 안내:

```
Slack 알림은 GitHub Actions 워크플로우에서 자동 전송됩니다.

설정 확인:
1. GitHub Secrets > SLACK_WEBHOOK_URL 설정 확인
2. Slack 채널에서 알림 수신 확인

알림 내용:
- 배포 시작/완료/실패
- Health Check 결과
- 배포 환경 및 브랜치 정보
```

## 트러블슈팅

### Pod가 Pending 상태
- **원인**: 리소스 부족 (CPU/Memory)
- **확인**: `kubectl describe pod {pod-name} -n {namespace}`
- **해결**: 노드 스케일링 또는 리소스 요청 조정

### Pod가 CrashLoopBackOff
- **원인**: 애플리케이션 시작 실패
- **확인**: `kubectl logs {pod-name} -n {namespace}`
- **해결**: 로그에서 에러 확인 후 수정

### Health Check 실패
- **원인**: 서비스 미시작 또는 오류
- **확인**: Pod 로그 및 애플리케이션 로그
- **해결**: 롤백 또는 Hotfix

### 배포 타임아웃
- **원인**: 이미지 pull 실패, 리소스 부족
- **확인**: Pod 이벤트 및 노드 상태
- **해결**: 이미지 확인, 리소스 증설

## 참고 스크립트

- GitHub Actions 확인: `scripts/check-github-actions.sh`
- Backend 상태 확인: `scripts/check-backend-status.sh`
- Frontend 상태 확인: `scripts/check-frontend-status.sh`
- Health Check: `scripts/health-check.sh`
- DB 연결 확인: `scripts/check-db-status.sh`

## 관련 Skills

- `deploy`: 배포 실행
- `rollback`: 오류 발생 시 롤백
- `predeploy`: 배포 전 검증

## 주요 메트릭

모니터링 시 확인할 주요 메트릭:

**애플리케이션**:
- 요청 처리율 (RPS)
- 평균 응답 시간
- 에러율 (4xx, 5xx)
- 활성 연결 수

**인프라**:
- CPU 사용률
- Memory 사용률
- Network I/O
- Disk I/O

**데이터베이스**:
- Connection Pool 사용량
- 쿼리 응답 시간
- 활성 트랜잭션 수
- Dead Lock 발생 횟수
