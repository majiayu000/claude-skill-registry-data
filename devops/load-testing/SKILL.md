---
name: load-testing
description: "K6 부하 테스트 — 테스트 유형, 기본·고급 시나리오, Kubernetes 실행, Grafana Cloud K6 분산 테스트, 안티패턴. Use when K6 스크립트로 스파이크·soak 등 부하를 만들고 실행할 때. 결과 분석은 load-testing-analysis."
---

# 부하 테스트 가이드

K6, nGrinder를 활용한 성능 테스트 및 결과 분석

## Quick Reference (결정 트리)

```
테스트 도구 선택?
    │
    ├─ 코드 기반 (DevOps 친화) ──> K6 (추천)
    ├─ GUI 기반 (비개발자) ─────> nGrinder
    ├─ 엔터프라이즈 ────────────> LoadRunner / Gatling
    └─ 간단한 HTTP ────────────> Apache Bench (ab)

테스트 유형?
    │
    ├─ Smoke Test ────────> 기본 동작 확인 (낮은 부하)
    ├─ Load Test ─────────> 예상 부하 검증
    ├─ Stress Test ───────> 한계점 확인
    ├─ Spike Test ────────> 급격한 부하 대응
    └─ Soak Test ─────────> 장시간 안정성
```

---

## CRITICAL: 테스트 유형

| 테스트 | 목적 | VU | 시간 |
|--------|------|-----|------|
| **Smoke** | 기본 동작 확인 | 1-5 | 1분 |
| **Load** | 예상 트래픽 검증 | 예상 VU | 10-30분 |
| **Stress** | 한계점 발견 | 점진적 증가 | 무제한 |
| **Spike** | 급격한 부하 대응 | 갑자기 증가 | 5-10분 |
| **Soak** | 장시간 안정성 | 예상 VU | 수 시간 |

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Test Patterns                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Smoke:    ▁▁▁▁▁▁▁▁▁▁                                       │
│                                                              │
│  Load:     ╱▔▔▔▔▔▔▔▔▔╲                                      │
│                                                              │
│  Stress:   ╱╱╱╱╱╱╱╱╱╱╱ (계속 증가)                          │
│                                                              │
│  Spike:    ▁▁▁█████▁▁▁                                      │
│                                                              │
│  Soak:     ╱▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔╲ (장시간)                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## K6 기본

### 설치

```bash
# macOS
brew install k6

# Docker
docker run --rm -i grafana/k6 run - <script.js

# Kubernetes Operator
helm repo add grafana https://grafana.github.io/helm-charts
helm install k6-operator grafana/k6-operator -n k6-operator-system --create-namespace
```

### 기본 스크립트

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // 단계별 부하
  stages: [
    { duration: '2m', target: 100 },  // 2분간 100 VU까지 증가
    { duration: '5m', target: 100 },  // 5분간 100 VU 유지
    { duration: '2m', target: 200 },  // 2분간 200 VU까지 증가
    { duration: '5m', target: 200 },  // 5분간 200 VU 유지
    { duration: '2m', target: 0 },    // 2분간 0으로 감소
  ],

  // 임계값 (SLO 기반)
  thresholds: {
    http_req_duration: ['p(95)<500'],  // p95 응답시간 500ms 이하
    http_req_failed: ['rate<0.01'],     // 에러율 1% 이하
    http_reqs: ['rate>100'],            // 초당 100 RPS 이상
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body contains users': (r) => r.body.includes('users'),
  });

  sleep(1);  // 1초 대기 (Think Time)
}
```

### 실행

```bash
# 기본 실행
k6 run load-test.js

# VU/시간 오버라이드
k6 run --vus 50 --duration 30s load-test.js

# 결과 출력
k6 run --out json=results.json load-test.js
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```

---

## K6 고급 시나리오

### 시나리오 기반 테스트

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    // 시나리오 1: 일반 사용자 브라우징
    browse: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 100 },
        { duration: '10m', target: 100 },
        { duration: '5m', target: 0 },
      ],
      exec: 'browseScenario',
    },

    // 시나리오 2: API 집중 호출
    api_heavy: {
      executor: 'constant-arrival-rate',
      rate: 50,           // 초당 50 요청
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 50,
      maxVUs: 100,
      exec: 'apiScenario',
    },

    // 시나리오 3: 스파이크 테스트
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      stages: [
        { duration: '2m', target: 10 },
        { duration: '1m', target: 200 },  // 스파이크!
        { duration: '2m', target: 10 },
      ],
      preAllocatedVUs: 200,
      exec: 'spikeScenario',
    },
  },

  thresholds: {
    'http_req_duration{scenario:browse}': ['p(95)<1000'],
    'http_req_duration{scenario:api_heavy}': ['p(95)<500'],
    'http_req_failed': ['rate<0.01'],
  },
};

export function browseScenario() {
  http.get('https://api.example.com/products');
  sleep(Math.random() * 3 + 1);  // 1-4초 랜덤
}

export function apiScenario() {
  const payload = JSON.stringify({ item: 'test', quantity: 1 });
  http.post('https://api.example.com/orders', payload, {
    headers: { 'Content-Type': 'application/json' },
  });
}

export function spikeScenario() {
  http.get('https://api.example.com/');
}
```

### 인증 처리

```javascript
import http from 'k6/http';
import { check } from 'k6';

// Setup: 테스트 시작 전 1회 실행
export function setup() {
  const loginRes = http.post('https://api.example.com/login', {
    username: 'testuser',
    password: 'testpass',
  });

  const token = loginRes.json('token');
  return { token };
}

export default function (data) {
  const params = {
    headers: {
      Authorization: `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
  };

  const res = http.get('https://api.example.com/protected', params);
  check(res, { 'status is 200': (r) => r.status === 200 });
}

// Teardown: 테스트 종료 후 1회 실행
export function teardown(data) {
  http.post('https://api.example.com/logout', null, {
    headers: { Authorization: `Bearer ${data.token}` },
  });
}
```

### 데이터 파일 사용

```javascript
import http from 'k6/http';
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

// CSV 데이터 로드 (모든 VU가 공유)
const users = new SharedArray('users', function () {
  return papaparse.parse(open('./users.csv'), { header: true }).data;
});

export default function () {
  // 랜덤 사용자 선택
  const user = users[Math.floor(Math.random() * users.length)];

  const payload = JSON.stringify({
    username: user.username,
    email: user.email,
  });

  http.post('https://api.example.com/users', payload, {
    headers: { 'Content-Type': 'application/json' },
  });
}
```

---

## K6 on Kubernetes

### K6 Operator TestRun

```yaml
apiVersion: k6.io/v1alpha1
kind: TestRun
metadata:
  name: load-test
spec:
  parallelism: 4  # 4개 Pod에서 분산 실행
  script:
    configMap:
      name: k6-test-script
      file: load-test.js
  arguments: --out influxdb=http://influxdb:8086/k6
  runner:
    image: grafana/k6:latest
    resources:
      limits:
        cpu: "1"
        memory: "1Gi"
      requests:
        cpu: "500m"
        memory: "512Mi"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: k6-test-script
data:
  load-test.js: |
    import http from 'k6/http';
    import { check } from 'k6';

    export const options = {
      vus: 50,
      duration: '5m',
    };

    export default function () {
      const res = http.get('http://my-service.default.svc.cluster.local/api');
      check(res, { 'status is 200': (r) => r.status === 200 });
    }
```

### CI/CD 통합

```yaml
# .github/workflows/load-test.yaml
name: Load Test

on:
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'  # 매일 새벽 2시

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install k6
        run: |
          curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz
          sudo mv k6-v0.47.0-linux-amd64/k6 /usr/local/bin/

      - name: Run Load Test
        run: k6 run --out json=results.json tests/load-test.js

      - name: Check Thresholds
        run: |
          if grep -q '"thresholds":{".*":{"ok":false' results.json; then
            echo "Threshold failed!"
            exit 1
          fi

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
```

---

## Grafana Cloud K6 (대규모 분산)

단일 injector 한계를 넘는 규모는 Cloud 실행으로 load zone 을 분산한다.

```bash
K6_CLOUD_PROJECT_ID=12345 \
K6_CLOUD_TOKEN=your-token \
k6 cloud run \
  --env BASE_URL=https://api.example.com \
  load-test.js
```

| 항목 | 값 |
|------|-----|
| 100만 VU 구성 | 300 load zones × 3,500 VUs |
| 과금 | 분당 과금 — 1회 테스트 ~$500-1000 |
| self-hosted 대안 | K6 Operator `parallelism` 상향 (아래 K6 on Kubernetes) |

> 비용이 분 단위로 누적되므로 **시나리오/threshold 를 self-hosted 소규모로 먼저 확정**한 뒤 Cloud 로 올린다.

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Think Time 없음 | 비현실적 부하 | sleep() 추가 |
| 단일 엔드포인트만 | 실제 시나리오 미반영 | 다양한 API 조합 |
| 로컬에서 대규모 테스트 | 네트워크 병목 | K6 Operator 분산 |
| Threshold 없이 실행 | Pass/Fail 기준 없음 | SLO 기반 threshold |

---

## 체크리스트

### 테스트 준비
- [ ] 테스트 환경 격리 (스테이징)
- [ ] 모니터링 설정 (Prometheus, Grafana)
- [ ] 기준선(Baseline) 측정
- [ ] 테스트 시나리오 정의

### K6 스크립트
- [ ] 현실적 시나리오 구성
- [ ] Think Time 추가
- [ ] SLO 기반 Threshold 설정
- [ ] 인증/데이터 처리

**관련 skill**: `/sre:sre-sli-slo`, `/k8s:k8s-autoscaling`, `/observability:monitoring-metrics`

---

## 참조 스킬

- `load-testing-analysis.md` - nGrinder, 결과 분석, SLO 기반 Threshold
- `/sre:sre-sli-slo` - SLI/SLO 정의 및 관리
- `/k8s:k8s-autoscaling` - 오토스케일링 연동
- `/observability:monitoring-metrics` - 모니터링 메트릭
