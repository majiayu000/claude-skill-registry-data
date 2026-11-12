---
name: cicd-devsecops
description: "CI/CD 보안 파이프라인 — GitHub Actions, Trivy 취약점 스캔, SonarQube, secret 관리. Use when GitHub Actions 에 보안 스캔 단계를 넣어 파이프라인을 구성할 때."
---

# CI/CD & DevSecOps 가이드

GitHub Actions, 보안 스캔(Trivy, SonarQube), 통합 파이프라인

## Quick Reference (결정 트리)

```
CI/CD 도구 선택?
    │
    ├─ GitHub 사용 ────────> GitHub Actions (추천)
    ├─ GitLab 사용 ────────> GitLab CI
    ├─ 멀티 클라우드/복잡 ──> Jenkins / Tekton
    └─ K8s 네이티브 ───────> ArgoCD + Tekton

보안 스캔 단계?
    │
    ├─ 코드 작성 ──> SonarQube (SAST, 코드 품질)
    ├─ 빌드 ──────> Trivy (이미지 취약점)
    ├─ 배포 ──────> Kyverno (정책 검증)
    └─ 런타임 ───> Falco (런타임 보안)
```

---

## CRITICAL: DevSecOps 파이프라인

```
┌─────────────────────────────────────────────────────────────────┐
│                    DevSecOps Pipeline                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Code ──> Build ──> Test ──> Scan ──> Deploy ──> Monitor       │
│    │        │        │        │         │          │           │
│   SAST    Image    Unit    Trivy    Kyverno     Falco         │
│  Sonar   Build    Test    DAST     Policy     Runtime         │
│  Lint             E2E     SBOM     Admission   Alert          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Shift Left**: 보안을 개발 초기 단계로 이동

---

## GitHub Actions 파이프라인

### 기본 CI/CD 워크플로우

```yaml
# .github/workflows/ci.yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 1. 코드 품질 검사
  code-quality:
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

      - name: Quality Gate
        uses: SonarSource/sonarqube-quality-gate-action@v1
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  # 2. 테스트
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Tests
        run: go test -v -race -coverprofile=coverage.out ./...

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.out

  # 3. 빌드 & 스캔
  build-scan:
    needs: [code-quality, test]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  # 4. 배포
  deploy:
    needs: build-scan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to K8s
        run: |
          argocd app sync ${{ env.APP_NAME }} --revision ${{ github.sha }}
```

### PR 검증 워크플로우

```yaml
# .github/workflows/pr-check.yaml
name: PR Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Kubernetes 매니페스트 검증
      - name: Validate K8s manifests
        uses: instrumenta/kubeval-action@master
        with:
          files: ./k8s

      # Helm 차트 검증
      - name: Helm Lint
        run: helm lint ./charts/*

      # Kyverno 정책 테스트
      - name: Kyverno CLI Test
        run: kyverno apply ./policies/ --resource ./k8s/

      # 보안 정책 검증
      - name: Checkov Scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./k8s
          framework: kubernetes
```

---

## Trivy (취약점 스캔)

### 스캔 유형

| 유형 | 대상 | 명령어 |
|------|------|--------|
| Image | 컨테이너 이미지 | `trivy image` |
| Filesystem | 로컬 파일 | `trivy fs` |
| Repository | Git 저장소 | `trivy repo` |
| K8s | 클러스터 | `trivy k8s` |
| SBOM | 소프트웨어 목록 | `trivy sbom` |

### 이미지 스캔

```bash
# 기본 스캔
trivy image myapp:latest

# CRITICAL/HIGH만 검출
trivy image --severity CRITICAL,HIGH myapp:latest

# 빌드 실패 조건
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# SBOM 생성
trivy image --format spdx-json -o sbom.json myapp:latest
```

### CI 통합 설정

```yaml
# trivy.yaml - 설정 파일
severity:
  - CRITICAL
  - HIGH

vulnerability:
  type:
    - os
    - library

scan:
  skip-dirs:
    - /tmp
    - /var/cache

ignore-unfixed: true
```

---

## SonarQube (코드 품질)

### 분석 유형

| 유형 | 설명 |
|------|------|
| **SAST** | 정적 보안 분석 (SQL Injection, XSS 등) |
| **Code Smells** | 유지보수성 문제 |
| **Bugs** | 잠재적 버그 |
| **Coverage** | 테스트 커버리지 |
| **Duplications** | 중복 코드 |

### 프로젝트 설정

```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project

# 소스 코드 경로
sonar.sources=src/main
sonar.tests=src/test

# 언어별 설정
sonar.java.binaries=target/classes
sonar.go.coverage.reportPaths=coverage.out

# 제외 패턴
sonar.exclusions=**/vendor/**,**/*_test.go

# Quality Gate 설정
sonar.qualitygate.wait=true
```

### Quality Gate 조건

```yaml
# 권장 Quality Gate 조건
conditions:
  - metric: new_reliability_rating    # 새 코드 버그
    op: GT
    value: 1                          # A 등급 이상

  - metric: new_security_rating       # 새 코드 취약점
    op: GT
    value: 1                          # A 등급 이상

  - metric: new_coverage              # 새 코드 커버리지
    op: LT
    value: 80                         # 80% 이상

  - metric: new_duplicated_lines_density  # 중복
    op: GT
    value: 3                          # 3% 이하
```

---

## Secret 관리

### GitHub Secrets 사용

```yaml
# 민감 정보는 항상 secrets 사용
env:
  SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  REGISTRY_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}

# secrets를 파일로 사용
- name: Create kubeconfig
  run: |
    echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig.yaml
```

### External Secrets Operator

```yaml
# K8s에서 외부 시크릿 동기화
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: db-password
      remoteRef:
        key: prod/myapp/db
        property: password
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 하드코딩된 시크릿 | 노출 위험 | GitHub Secrets / Vault |
| 스캔 결과 무시 | 취약점 방치 | Quality Gate 실패 설정 |
| latest 태그 사용 | 재현 불가 | SHA/버전 태그 사용 |
| root 권한 컨테이너 | 권한 상승 공격 | Kyverno로 강제 |
| SBOM 미생성 | 공급망 추적 불가 | Trivy SBOM 생성 |
| 수동 배포 | 휴먼 에러 | GitOps (ArgoCD) |

---

## 체크리스트

### CI/CD
- [ ] GitHub Actions 워크플로우 설정
- [ ] 이미지 빌드 및 푸시 자동화
- [ ] 캐시 설정 (빌드 속도)

### 보안 스캔
- [ ] Trivy 이미지 스캔
- [ ] SonarQube SAST
- [ ] SBOM 생성
- [ ] Quality Gate 설정

### 시크릿 관리
- [ ] GitHub Secrets 사용
- [ ] External Secrets Operator (선택)

**관련 skill**: `/cicd:cicd-policy` (Kyverno 정책), `/cicd:gitops-argocd`, `/k8s:k8s-security`, `/infra:docker`
