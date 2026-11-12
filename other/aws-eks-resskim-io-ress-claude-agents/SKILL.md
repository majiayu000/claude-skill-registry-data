---
name: aws-eks
description: "AWS EKS 기본 — 클러스터 구성, VPC 설계, IRSA, Add-ons 관리. Use when EKS 클러스터를 새로 설계·생성하거나 IRSA 와 add-on 을 설정할 때."
---

# AWS EKS 가이드

EKS 클러스터 구성, VPC 설계, IRSA, Add-ons 관리

## Quick Reference (결정 트리)

```
EKS 운영 모드?
    │
    ├─ 완전 관리형 ────────> EKS Auto Mode (신규)
    ├─ 유연한 관리 ────────> EKS + Karpenter
    └─ 전통적 방식 ────────> EKS + Managed Node Group

노드 스케일링?
    │
    ├─ 비용 최적화 + 빠른 프로비저닝 ──> Karpenter
    ├─ 간단한 운영 ────────────────────> Cluster Autoscaler
    └─ AWS 완전 관리 ──────────────────> EKS Auto Mode

Pod 권한 관리?
    │
    ├─ AWS 서비스 접근 ──> IRSA (IAM Roles for Service Accounts)
    └─ 신규 방식 ────────> EKS Pod Identity
```

---

## CRITICAL: EKS 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    EKS Architecture                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐      ┌─────────────────────────────┐   │
│  │  Control Plane  │      │         Data Plane          │   │
│  │   (AWS 관리)    │      │        (고객 관리)          │   │
│  │                 │      │                             │   │
│  │ ┌─────────────┐ │      │  ┌───────┐  ┌───────┐      │   │
│  │ │ API Server  │ │      │  │Node 1 │  │Node 2 │ ...  │   │
│  │ │   etcd      │◄├──────┤► │       │  │       │      │   │
│  │ │ Controller  │ │      │  │ Pods  │  │ Pods  │      │   │
│  │ │ Scheduler   │ │      │  └───────┘  └───────┘      │   │
│  │ └─────────────┘ │      │         Private Subnets     │   │
│  └─────────────────┘      └─────────────────────────────┘   │
│           │                            │                     │
│           └────────── VPC ─────────────┘                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## VPC 설계

### CRITICAL: 서브넷 요구사항

| 서브넷 유형 | 용도 | 태그 |
|------------|------|------|
| **Public** | NAT Gateway, ALB | `kubernetes.io/role/elb=1` |
| **Private** | Worker Nodes, Pods | `kubernetes.io/role/internal-elb=1` |
| **최소 AZ** | 2개 (권장 3개) | - |

### Terraform VPC 모듈

```hcl
# vpc.tf
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "eks-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = false  # 프로덕션: AZ별 NAT
  enable_dns_hostnames   = true
  enable_dns_support     = true

  # EKS 서브넷 태그
  public_subnet_tags = {
    "kubernetes.io/role/elb"                      = 1
    "kubernetes.io/cluster/${var.cluster_name}"   = "owned"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb"             = 1
    "kubernetes.io/cluster/${var.cluster_name}"   = "owned"
    "karpenter.sh/discovery"                      = var.cluster_name
  }
}
```

### IP 주소 계획

```
VPC CIDR: 10.0.0.0/16 (65,536 IPs)
├── Private Subnets (Nodes + Pods)
│   ├── 10.0.0.0/18   (16,384 IPs) - AZ-a
│   ├── 10.0.64.0/18  (16,384 IPs) - AZ-b
│   └── 10.0.128.0/18 (16,384 IPs) - AZ-c
└── Public Subnets (NAT, ALB)
    ├── 10.0.192.0/20 (4,096 IPs) - AZ-a
    ├── 10.0.208.0/20 (4,096 IPs) - AZ-b
    └── 10.0.224.0/20 (4,096 IPs) - AZ-c

권장: Pod에 VPC IP 직접 할당 시 충분한 CIDR 확보
```

---

## EKS 클러스터 생성

### Terraform EKS

```hcl
# eks.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # 클러스터 엔드포인트 설정
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # 클러스터 로깅
  cluster_enabled_log_types = [
    "api", "audit", "authenticator", "controllerManager", "scheduler"
  ]

  # Add-ons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent              = true
      service_account_role_arn = module.vpc_cni_irsa.iam_role_arn
      configuration_values = jsonencode({
        enableNetworkPolicy = "true"
        env = {
          ENABLE_PREFIX_DELEGATION = "true"
          WARM_PREFIX_TARGET       = "1"
        }
      })
    }
    eks-pod-identity-agent = {
      most_recent = true
    }
  }

  # Managed Node Group
  eks_managed_node_groups = {
    default = {
      name           = "default"
      instance_types = ["m6i.large"]
      min_size       = 2
      max_size       = 10
      desired_size   = 3

      labels = {
        role = "general"
      }

      tags = {
        "k8s.io/cluster-autoscaler/enabled"         = "true"
        "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned"
      }
    }

    # Spot Node Group
    spot = {
      name           = "spot"
      instance_types = ["m6i.large", "m5.large", "m5a.large"]
      capacity_type  = "SPOT"
      min_size       = 0
      max_size       = 20
      desired_size   = 0

      labels = {
        role          = "spot"
        "node.kubernetes.io/lifecycle" = "spot"
      }

      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  tags = var.tags
}
```

### eksctl 생성

```yaml
# cluster.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: my-cluster
  region: ap-northeast-2
  version: "1.29"

vpc:
  id: "vpc-xxx"
  subnets:
    private:
      ap-northeast-2a: { id: "subnet-xxx" }
      ap-northeast-2b: { id: "subnet-xxx" }
      ap-northeast-2c: { id: "subnet-xxx" }

iam:
  withOIDC: true  # IRSA 활성화

managedNodeGroups:
  - name: default
    instanceType: m6i.large
    desiredCapacity: 3
    minSize: 2
    maxSize: 10
    privateNetworking: true
    iam:
      withAddonPolicies:
        imageBuilder: true
        autoScaler: true
        cloudWatch: true

addons:
  - name: vpc-cni
    version: latest
  - name: coredns
    version: latest
  - name: kube-proxy
    version: latest
  - name: eks-pod-identity-agent
    version: latest
```

```bash
eksctl create cluster -f cluster.yaml
```

---

## IRSA (IAM Roles for Service Accounts)

### CRITICAL: IRSA 설정

```hcl
# irsa.tf
module "s3_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "${var.cluster_name}-s3-access"

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["production:my-app"]
    }
  }

  role_policy_arns = {
    s3_read = aws_iam_policy.s3_read.arn
  }
}

resource "aws_iam_policy" "s3_read" {
  name = "${var.cluster_name}-s3-read"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::my-bucket",
          "arn:aws:s3:::my-bucket/*"
        ]
      }
    ]
  })
}
```

### ServiceAccount 설정

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/my-cluster-s3-access
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: my-app  # IRSA ServiceAccount 사용
      containers:
        - name: app
          image: my-app:latest
          # AWS SDK가 자동으로 IRSA 자격증명 사용
```

### IRSA Best Practices

| 원칙 | 설명 |
|------|------|
| **최소 권한** | 필요한 권한만 부여 |
| **SA당 1 Role** | 서비스별 분리된 Role |
| **Node Role 사용 금지** | IRSA로 대체 |
| **Namespace 제한** | 특정 NS의 SA만 허용 |

---

## EKS Add-ons

### 핵심 Add-ons

| Add-on | 역할 | 필수 여부 |
|--------|------|----------|
| **vpc-cni** | Pod 네트워킹 | 필수 |
| **coredns** | DNS 서비스 | 필수 |
| **kube-proxy** | 서비스 프록시 | 필수 |
| **eks-pod-identity-agent** | Pod Identity | 권장 |
| **aws-ebs-csi-driver** | EBS 볼륨 | 스토리지 시 |
| **aws-efs-csi-driver** | EFS 볼륨 | 공유 스토리지 시 |

### VPC CNI 설정

```yaml
# VPC CNI ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: amazon-vpc-cni
  namespace: kube-system
data:
  # Prefix Delegation 활성화 (IP 절약)
  enable-prefix-delegation: "true"
  warm-prefix-target: "1"

  # Network Policy 활성화
  enable-network-policy-controller: "true"

  # POD_SECURITY_GROUP_ENFORCING_MODE
  POD_SECURITY_GROUP_ENFORCING_MODE: "standard"
```

### EBS CSI Driver IRSA

```hcl
module "ebs_csi_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name             = "${var.cluster_name}-ebs-csi"
  attach_ebs_csi_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:ebs-csi-controller-sa"]
    }
  }
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Node Role에 모든 권한 | 보안 취약 | IRSA 사용 |
| 작은 VPC CIDR | IP 고갈 | /16 이상 할당 |
| Public Endpoint만 | 보안 노출 | Private + VPN |
| Add-on 수동 관리 | 버전 불일치 | EKS 관리형 사용 |
| 단일 AZ | 가용성 저하 | 3 AZ 분산 |

---

## 체크리스트

- [ ] 충분한 CIDR 할당 (/16 이상), 3 AZ 분산
- [ ] 서브넷 태그 설정 (ELB, internal-elb)
- [ ] Private Endpoint 활성화
- [ ] OIDC Provider 활성화 (IRSA)
- [ ] 로깅 활성화 (api, audit, authenticator)
- [ ] 관리형 Add-ons 사용
- [ ] IRSA로 Pod 권한 관리
- [ ] Managed Node Group 또는 Karpenter 설정

---

## 참조 스킬

- `/infra:aws-eks-advanced` - Karpenter, 보안 강화, 운영 최적화
- `/k8s:k8s-security` - Kubernetes 보안
- `/k8s:k8s-autoscaling` - Autoscaling (HPA, VPA, KEDA)
- `/infra:terraform-security` - Terraform 보안 설정
