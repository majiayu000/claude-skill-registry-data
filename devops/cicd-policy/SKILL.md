---
name: cicd-policy
description: "CI/CD 정책 자동화 — Kyverno 정책과 CLI 검증, 보안 점수 대시보드, 통합 DevSecOps 파이프라인. Use when 배포 전에 정책 위반을 Kyverno 로 CI 단계에서 막고 싶을 때."
---

# CI/CD Policy as Code 가이드

Kyverno 정책, 보안 점수 대시보드, 통합 DevSecOps 파이프라인

## Quick Reference

```
Policy as Code 도구?
    │
    ├─ Kyverno ────────> K8s 네이티브, YAML 기반
    │       │
    │       └─ Validation + Mutation + Generation
    │
    ├─ OPA/Gatekeeper ──> Rego 언어, 범용
    │
    └─ Checkov ────────> IaC 스캔 (Terraform, K8s)
```

---

## Kyverno (Policy as Code)

### 핵심 정책: 이미지 레지스트리 제한

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: validate-registries
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "이미지는 허용된 레지스트리에서만 가져올 수 있습니다"
        pattern:
          spec:
            containers:
              - image: "ghcr.io/* | gcr.io/* | *.dkr.ecr.*.amazonaws.com/*"
```

### 리소스 제한 필수

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-limits
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "CPU/메모리 limits 설정이 필요합니다"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
```

### 권한 상승 금지

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privilege-escalation
spec:
  validationFailureAction: Enforce
  rules:
    - name: deny-privilege-escalation
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "권한 상승이 금지되어 있습니다"
        pattern:
          spec:
            containers:
              - securityContext:
                  allowPrivilegeEscalation: false
```

### 필수 라벨 정책

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-team-label
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
      validate:
        message: "team, app 라벨이 필요합니다"
        pattern:
          metadata:
            labels:
              team: "?*"
              app: "?*"
```

### Mutation 정책 (기본값 자동 주입)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-securitycontext
spec:
  rules:
    - name: add-security-context
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        patchStrategicMerge:
          spec:
            securityContext:
              runAsNonRoot: true
              seccompProfile:
                type: RuntimeDefault
            containers:
              - (name): "*"
                securityContext:
                  allowPrivilegeEscalation: false
                  readOnlyRootFilesystem: true
                  capabilities:
                    drop:
                      - ALL
```

---

## Kyverno CLI (CI 검증)

### 기본 사용법

```bash
# 정책 테스트
kyverno apply ./policies/ --resource ./k8s/deployment.yaml

# 정책 테스트 (테스트 케이스)
kyverno test ./policies/tests/

# 결과 출력
kyverno apply ./policies/ -r ./k8s/ -o json
```

### 테스트 케이스 작성

```yaml
# policies/tests/require-labels-test.yaml
apiVersion: cli.kyverno.io/v1alpha1
kind: Test
metadata:
  name: require-labels-test
policies:
  - ../require-labels.yaml
resources:
  - resources.yaml
results:
  - policy: require-labels
    rule: require-team-label
    resource: good-deployment
    kind: Deployment
    result: pass
  - policy: require-labels
    rule: require-team-label
    resource: bad-deployment
    kind: Deployment
    result: fail
```

---

## 통합 DevSecOps 파이프라인

### Complete Pipeline

```yaml
# .github/workflows/devsecops.yaml
name: DevSecOps Pipeline

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # Stage 1: Static Analysis
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v2
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

      - name: Semgrep SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: p/default

  # Stage 2: Dependency Check
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Trivy FS Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  # Stage 3: Build & Image Scan
  build:
    needs: [sast, dependency-check]
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Build Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Trivy Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          exit-code: '1'
          severity: 'CRITICAL'

      - name: Generate SBOM
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: 'spdx-json'
          output: 'sbom.json'

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json

  # Stage 4: Policy Validation
  policy-check:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Kyverno CLI
        run: |
          curl -LO https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_amd64.tar.gz
          tar -xvf kyverno-cli_linux_amd64.tar.gz
          sudo mv kyverno /usr/local/bin/

      - name: Validate Policies
        run: kyverno apply ./policies/ --resource ./k8s/

      - name: Checkov IaC Scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./k8s
          framework: kubernetes
          soft_fail: false

  # Stage 5: Deploy
  deploy:
    needs: [build, policy-check]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy via ArgoCD
        run: |
          argocd app sync myapp --revision ${{ github.sha }}
          argocd app wait myapp --timeout 300
```

---

## 보안 점수 대시보드

### Prometheus Metrics 수집

```yaml
# prometheus-rules.yaml
groups:
  - name: devsecops
    rules:
      - record: security:vulnerabilities:critical
        expr: sum(trivy_vulnerability_total{severity="CRITICAL"})

      - record: security:vulnerabilities:high
        expr: sum(trivy_vulnerability_total{severity="HIGH"})

      - record: security:policy_violations
        expr: sum(kyverno_policy_results_total{result="fail"})

      - record: security:sonar_issues
        expr: sum(sonarqube_issues_total{severity="BLOCKER"})
```

### Grafana 대시보드 쿼리

```promql
# 취약점 트렌드
sum(trivy_vulnerability_total) by (severity)

# 정책 위반율
sum(kyverno_policy_results_total{result="fail"})
/
sum(kyverno_policy_results_total)

# 코드 품질 점수
sonarqube_quality_gate_status{project="myapp"}
```

---

## 체크리스트

### Kyverno
- [ ] Kyverno 설치
- [ ] 필수 정책 적용 (이미지, 리소스, 권한)
- [ ] CI에서 정책 검증
- [ ] Mutation 정책 (기본값 주입)

### 통합 파이프라인
- [ ] SAST 스캔 (SonarQube)
- [ ] 의존성 스캔 (Trivy FS)
- [ ] 이미지 스캔 (Trivy Image)
- [ ] SBOM 생성
- [ ] 정책 검증 (Kyverno CLI)

### 모니터링
- [ ] 보안 메트릭 수집
- [ ] 대시보드 구축
- [ ] 알림 설정

**관련 skill**: `/cicd:cicd-devsecops` (파이프라인), `/k8s:k8s-security`, `/observability:monitoring-metrics`
