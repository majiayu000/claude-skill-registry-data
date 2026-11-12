---
name: ec2-cd-pipeline
description: "EC2 배포 파이프라인 — GitHub Actions + SSM, ALB 헬스체크, CloudFront behavior 라우팅, 배포 완료 대기. Use when EC2 서버에 SSM 으로 배포하는 CD 를 만들거나 검증할 때."
---

# EC2 기반 CD 파이프라인 패턴

GitHub Actions + SSM + ALB + CloudFront 기반 EC2 배포 실무 패턴.

## Quick Reference

```
배포 흐름 (GitHub Actions CD)
    │
    ├─ GitHub Actions Trigger (push to main/develop)
    │
    ├─ SSM SendCommand → EC2에서 deploy.sh 실행
    │     │
    │     ├─ docker compose pull
    │     ├─ docker compose up -d
    │     └─ healthcheck 대기
    │
    ├─ Polling으로 SSM 명령 완료 대기
    │
    └─ 결과 확인 (Success/Failed/TimedOut)

트래픽 경로
    │
    ├─ Route53 → CloudFront
    │     │
    │     ├─ /api/*         → ALB → EC2:8080 (app-server)
    │     ├─ /swagger-ui/*  → ALB → EC2:8080
    │     ├─ /v3/*          → ALB → EC2:8080
    │     ├─ /monitoring/*  → ALB → EC2:3000 (Grafana)
    │     └─ /* (default)   → S3 (프론트엔드)
    │
    └─ ALB → Target Group → EC2 Docker containers
```

---

## SSM 배포 완료 대기 패턴

### ❌ Anti-pattern: `aws ssm wait`

```bash
# 기본 대기: 5초 × 20회 = 100초 고정. 커스텀 불가.
aws ssm wait command-executed \
  --command-id "$COMMAND_ID" \
  --instance-id "$INSTANCE_ID"
# → deploy.sh가 100초 초과 시 무조건 실패 판정
```

**문제**: `aws ssm wait command-executed`는 polling interval(5초), max attempts(20회)가 고정.
Docker pull + 컨테이너 기동 + healthcheck가 100초를 초과하면 명령이 아직 `InProgress`인데 waiter가 포기.

### ✅ Shell polling 루프

```bash
MAX_WAIT=300    # 서버: 300초, 모니터링: 600초
INTERVAL=10     # 서버: 10초, 모니터링: 15초
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  STATUS=$(aws ssm get-command-invocation \
    --command-id "$COMMAND_ID" \
    --instance-id "$INSTANCE_ID" \
    --query "Status" --output text 2>/dev/null)

  case "$STATUS" in
    "Success")
      echo "배포 성공"
      exit 0
      ;;
    "Failed"|"TimedOut"|"Cancelled"|"Cancelling")
      echo "배포 실패 (Status: $STATUS)"
      # stdout + stderr 출력
      aws ssm get-command-invocation \
        --command-id "$COMMAND_ID" \
        --instance-id "$INSTANCE_ID" \
        --query "[StandardOutputContent, StandardErrorContent]" \
        --output text
      exit 1
      ;;
    *)
      echo "대기 중... (${ELAPSED}s / ${MAX_WAIT}s, Status: $STATUS)"
      sleep $INTERVAL
      ELAPSED=$((ELAPSED + INTERVAL))
      ;;
  esac
done

echo "타임아웃 (${MAX_WAIT}s 초과)"
exit 1
```

### 대기 시간 설정 기준

| 서비스 | MAX_WAIT | INTERVAL | 근거 |
|--------|----------|----------|------|
| Server (단일 컨테이너) | 300초 | 10초 | Docker pull + 기동 + healthcheck 20회 |
| Monitoring (6+ 컨테이너) | 600초 | 15초 | 6개 이미지 pull + 서비스 기동 |

**원칙**: `MAX_WAIT` ≥ SSM `send-command --timeout-seconds` 값

---

## CloudFront Behavior 라우팅

### CRITICAL: 새 서버 경로 노출 시 behavior 추가 필수

CloudFront default behavior(`/*`)는 S3로 라우팅됨.
서버 경로를 추가할 때 behavior를 빠뜨리면 S3에서 403 AccessDenied 반환.

```
CloudFront Behaviors (우선순위 순):
  /api/*          → ALB Origin
  /swagger-ui/*   → ALB Origin    ← 누락 시 S3에서 403
  /v3/*           → ALB Origin    ← Swagger가 내부 호출하는 경로
  /monitoring/*   → ALB Origin
  /* (default)    → S3 Origin
```

### Path Pattern 주의사항

```
/v3/api-docs/*   → /v3/api-docs (trailing slash 없음) 매칭 실패
/v3/*            → /v3/api-docs, /v3/api-docs/swagger 모두 매칭 ✅
```

- `/*`는 **하위 경로만** 매칭, 정확 경로 자체는 별도 패턴 필요
- 가능하면 넓은 prefix(`/v3/*`)로 잡아서 누락 방지

### 체크리스트

새 API 경로 추가 시:
- [ ] CloudFront behavior 추가 필요 여부 확인
- [ ] ALB 리스너 룰에 해당 경로 → 타겟 그룹 매핑 확인
- [ ] CORS 설정 필요 여부 확인

---

## ALB Healthcheck 설정

### CRITICAL: 인증 불필요한 엔드포인트 사용

```hcl
# ❌ Spring Security가 인증 요구 → 401 → unhealthy
health_check {
  path = "/"
  matcher = "200"
}

# ✅ actuator는 기본적으로 인증 불필요
health_check {
  path     = "/actuator/health"
  matcher  = "200"
  interval = 30
  timeout  = 5
}
```

### 서비스별 healthcheck 경로

| 서비스 | 경로 | 비고 |
|--------|------|------|
| Spring Boot | `/actuator/health` | Spring Security 인증 예외 |
| Grafana | `/api/health` | 인증 불필요 |
| Prometheus | `/-/healthy` | |
| Loki | `/ready` | |
| Tempo | `/ready` | |

### ALB Target 상태 검증

```bash
# 배포 후 반드시 확인
aws elbv2 describe-target-health \
  --target-group-arn "$TG_ARN" \
  --query "TargetHealthDescriptions[*].{Target:Target.Id,Status:TargetHealth.State}" \
  --output table
```

---

## CD 파이프라인 검증 체크리스트

### 배포 전
- [ ] SSM SendCommand `--timeout-seconds` ≤ polling `MAX_WAIT`
- [ ] deploy.sh에 healthcheck 대기 로직 포함
- [ ] 필수 환경변수 `.env` 또는 SSM Parameter Store에 설정

### 배포 후
- [ ] ALB 타겟 그룹 healthy 상태 확인
- [ ] 서비스 엔드포인트 응답 확인 (`curl -s -o /dev/null -w "%{http_code}"`)
- [ ] CloudFront 캐시 무효화 필요 여부 확인 (프론트엔드 변경 시)

### 장애 대응
- [ ] SSM 명령 stdout/stderr 확인: `aws ssm get-command-invocation`
- [ ] Docker 로그 확인: `docker logs <container>`
- [ ] ALB unhealthy 시: 포트 바인딩(`127.0.0.1` 아닌지) + healthcheck 경로 확인

---

## Anti-Patterns

| 실수 | 올바른 방법 | 근거 |
|------|------------|------|
| `aws ssm wait` 사용 | Shell polling 루프 | 100초 고정, 커스텀 불가 |
| CloudFront 새 경로 behavior 누락 | 서버 경로 추가 시 behavior 동시 추가 | S3 폴백 → 403 |
| ALB healthcheck 경로 `/` | `/actuator/health` 등 인증 불필요 경로 | Spring Security 401 → unhealthy |
| SSM timeout < deploy 소요 시간 | timeout ≥ 예상 소요 시간 + 여유 | InProgress 중 타임아웃 |
| CloudFront path `/{exact}/*` | 넓은 prefix `/{prefix}/*` | trailing slash 없는 경로 매칭 실패 |

**관련 skill**: `/infra:docker`, `/infra:terraform-security`
