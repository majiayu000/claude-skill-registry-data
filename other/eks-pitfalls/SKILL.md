---
name: eks-pitfalls
description: "EKS 운영 함정 — VPC CNI prefix delegation·max-pods, 서브넷 CIDR, WARM_IP_TARGET, Kyverno webhook, IAM 누락, IMDS. Use when EKS 에서 IP 고갈이나 노드·네트워크 장애가 나거나 운영 전 점검할 때."
---

# EKS 운영 Pitfalls

EKS 운영 중 발생하는 실전 함정 카탈로그. 매니지드 노드그룹/IAM/networking/스케일링.
2026-04-01 연쇄 장애(SG 삭제 + IP 고갈 + Kyverno 차단 + Prometheus OOM) 경험 기반.

---

## 1. VPC CNI Prefix Delegation + max-pods

### 문제
Bottlerocket AMI에서 `ENABLE_PREFIX_DELEGATION=true` 설정했으나 max-pods가 35로 고정 → ENI secondary IP 미할당 → 실질적 Pod 배치 불가.

### 원인
Bottlerocket kubelet은 기본적으로 secondary IP 모드의 max-pods(35)를 사용. Prefix delegation 활성화 시 별도 오버라이드 필요.

### 해결
```toml
# Bottlerocket user_data (TOML 형식)
[settings.kubernetes]
max-pods = 110
```

### max-pods 계산 공식
```
Max Pods = (ENIs × ((IPs_per_ENI - 1) × 16)) + 2

예: m5.large (3 ENIs, 10 IPs_per_ENI)
= (3 × ((10 - 1) × 16)) + 2
= (3 × 144) + 2
= 434 → cap at 250 (EKS 권장 상한)
→ 실무: 110 설정 (K8s 스케일링 안정성)
```

AWS 공식 계산기: `max-pods-calculator.sh --instance-type <type> --cni-prefix-delegation-enabled`

---

## 2. VPC 서브넷 CIDR 계획

### 문제
`/24` 서브넷(256 IPs)에서 prefix delegation 활성화 → 18+ 노드 시 IP 고갈 → 신규 Pod 미스케줄링, 노드 조인 실패.

### IP 소모 계산
```
Prefix delegation 시 노드당 IP 소모:
= ENIs_per_node × /28 prefixes × 16 IPs
= 3(m5.large) × 3 × 16 = 144 IPs

18 노드 × 144 = 2,592 IPs → /24(256 IPs) 절대 부족
```

### 권장 서브넷 크기

| 노드 수 | 최소 서브넷 | 권장 서브넷 |
|---------|-----------|-----------|
| ~10 | /22 (1,024) | /20 (4,096) |
| ~50 | /20 (4,096) | /18 (16,384) |
| ~100+ | /18 (16,384) | /16 (65,536) |

### 긴급 대응 (IP 고갈 시)
1. `WARM_PREFIX_TARGET` 제거
2. `WARM_IP_TARGET=2` 설정 (최소 IP 예약)
3. 서브넷 CIDR 확장 후 `WARM_PREFIX_TARGET=1` 복원

---

## 3. WARM_IP_TARGET vs WARM_PREFIX_TARGET

### 선택 가이드

| 설정 | 동작 | 적합한 환경 |
|------|------|-----------|
| `WARM_PREFIX_TARGET=1` (권장) | 노드당 1개 추가 /28 prefix 예약 | 정상 운영, 빠른 Pod 시작 |
| `WARM_IP_TARGET=2` | 노드당 2개 IP만 예약 | IP 절약 필요 시 (긴급) |
| `MINIMUM_IP_TARGET=N` | 최소 N개 IP 유지 | 특수 워크로드 |

### 주의
- `WARM_IP_TARGET` 설정 시 `WARM_PREFIX_TARGET` **자동 무시됨** (IP-level이 우선)
- 두 설정 동시 사용 금지 — 의도치 않은 동작 발생

---

## 4. Kyverno Webhook + EKS Managed Node Group

### 문제
모든 워커 노드 다운 → Kyverno pod 미실행 → validating webhook 응답 불가 (`failurePolicy: Fail`) → 새 노드 Ready 불가 → deadlock.

### 근거
kyverno/kyverno#11122 (2026-04 기준 미해결).

### 대응 방안

| 방법 | 장점 | 단점 |
|------|------|------|
| `failurePolicy: Ignore` | Deadlock 방지 | 검증 우회 가능 |
| Webhook 수동 삭제 | 즉각 복구 | 운영자 개입 필요 |
| kube-system 제외 | 시스템 Pod 영향 없음 | 적용 범위 축소 |
| port 9443 SG 규칙 확인 | 네트워크 문제 해결 | 원인이 다를 수 있음 |

### 복구 명령 (deadlock 시)
```bash
kubectl delete validatingwebhookconfiguration kyverno-resource-validating-webhook-cfg
kubectl delete mutatingwebhookconfiguration kyverno-resource-mutating-webhook-cfg
# 노드 정상화 후 Kyverno pod 재시작 → webhook 자동 재생성
```

---

## 5. EKS IAM Policy 누락

### 문제
클러스터 IAM Role에 `AmazonEKSClusterPolicy` 누락 → 노드 조인 시 401 Unauthorized.

### 필수 IAM 정책 체크리스트

**클러스터 Role:**
- `AmazonEKSClusterPolicy`
- `AmazonEKSVPCResourceController`

**노드 Role:**
- `AmazonEKSWorkerNodePolicy`
- `AmazonEKS_CNI_Policy`
- `AmazonEC2ContainerRegistryReadOnly`

**추가 (IRSA 사용 시):**
- OIDC provider 설정 확인
- ServiceAccount annotation 확인

### 디버깅
```bash
# 클러스터 Role 정책 확인
aws iam list-attached-role-policies --role-name <cluster-role-name>

# access entry 확인 (EKS API mode)
aws eks list-access-entries --cluster-name <cluster>
```

---

## 6. IMDS 보안 (권장)

### IMDS v2 강제 + hop limit
```hcl
# Terraform launch template
metadata_options {
  http_endpoint               = "enabled"
  http_tokens                 = "required"    # IMDSv2 강제
  http_put_response_hop_limit = 1             # 컨테이너에서 IMDS 접근 차단
}
```

- `hop_limit = 1`: 호스트에서만 접근 가능, 컨테이너(+1 hop)에서는 접근 불가
- NetworkPolicy IMDS 차단과 병행 권장 (defense in depth)
