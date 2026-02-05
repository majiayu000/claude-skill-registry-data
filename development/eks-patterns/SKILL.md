---
name: eks-patterns
description: EKS cluster patterns and best practices for Terraform. Provides cluster, node group, add-on, and IRSA scaffolds. Use when developing EKS infrastructure.
---

# EKS Patterns

Terraform patterns for Amazon EKS infrastructure development.

## Before Generating Code

ALWAYS use doc-researcher or Terraform MCP to verify:
- Current terraform-aws-eks module version
- EKS add-on versions
- Kubernetes version compatibility

## Primary Module Reference

Use `terraform-aws-modules/eks/aws` (v20+):
- Registry: https://registry.terraform.io/modules/terraform-aws-modules/eks/aws
- GitHub: https://github.com/terraform-aws-modules/terraform-aws-eks

## Naming Convention

Use `{project}-{environment}-eks` pattern:
```hcl
locals {
  cluster_name = "${var.project}-${var.environment}-eks"
}
```

## Complete EKS Cluster

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = local.cluster_name
  cluster_version = "1.31"

  # Networking
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Access
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true
  enable_cluster_creator_admin_permissions = true

  # Logging
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  # Encryption
  cluster_encryption_config = {
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }

  # Managed Node Groups
  eks_managed_node_groups = {
    general = {
      name           = "${local.cluster_name}-general"
      instance_types = ["m6i.large", "m5.large"]
      capacity_type  = "ON_DEMAND"

      min_size     = 2
      max_size     = 10
      desired_size = 3

      disk_size = 100
      disk_type = "gp3"

      labels = {
        role = "general"
        "node.kubernetes.io/capacity-type" = "on-demand"
      }

      update_config = {
        max_unavailable_percentage = 33
      }
    }
  }

  # Add-ons
  cluster_addons = {
    coredns = {
      most_recent = true
      configuration_values = jsonencode({
        replicaCount = 2
      })
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent              = true
      before_compute           = true
      service_account_role_arn = module.vpc_cni_irsa.iam_role_arn
      configuration_values = jsonencode({
        env = {
          ENABLE_PREFIX_DELEGATION = "true"
          WARM_PREFIX_TARGET       = "1"
        }
      })
    }
    aws-ebs-csi-driver = {
      most_recent              = true
      service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
    }
  }

  tags = var.tags
}
```

## Node Group Patterns

### On-Demand with Multiple Instance Types
```hcl
eks_managed_node_groups = {
  on_demand = {
    name           = "${local.cluster_name}-on-demand"
    instance_types = ["m6i.large", "m5.large", "m5a.large"]
    capacity_type  = "ON_DEMAND"

    min_size     = 2
    max_size     = 10
    desired_size = 3

    disk_size = 100
    disk_type = "gp3"

    labels = {
      role = "general"
      "node.kubernetes.io/capacity-type" = "on-demand"
    }

    update_config = {
      max_unavailable_percentage = 33
    }
  }
}
```

### Spot Instances
```hcl
eks_managed_node_groups = {
  spot = {
    name           = "${local.cluster_name}-spot"
    instance_types = ["m6i.large", "m5.large", "m5a.large", "m5n.large"]
    capacity_type  = "SPOT"

    min_size     = 0
    max_size     = 20
    desired_size = 3

    labels = {
      role = "spot"
      "node.kubernetes.io/capacity-type" = "spot"
    }

    taints = [{
      key    = "spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }]
  }
}
```

### GPU Node Group
```hcl
eks_managed_node_groups = {
  gpu = {
    name           = "${local.cluster_name}-gpu"
    instance_types = ["g4dn.xlarge", "g4dn.2xlarge"]
    capacity_type  = "ON_DEMAND"

    min_size     = 0
    max_size     = 5
    desired_size = 0

    ami_type  = "AL2_x86_64_GPU"
    disk_size = 200

    labels = {
      "nvidia.com/gpu"                   = "true"
      "node.kubernetes.io/capacity-type" = "on-demand"
    }

    taints = [{
      key    = "nvidia.com/gpu"
      value  = "true"
      effect = "NO_SCHEDULE"
    }]
  }
}
```

### ARM/Graviton Instances
```hcl
eks_managed_node_groups = {
  graviton = {
    name           = "${local.cluster_name}-graviton"
    instance_types = ["m6g.large", "m6g.xlarge"]
    capacity_type  = "ON_DEMAND"

    min_size     = 2
    max_size     = 10
    desired_size = 3

    ami_type = "AL2_ARM_64"

    labels = {
      "kubernetes.io/arch"               = "arm64"
      "node.kubernetes.io/capacity-type" = "on-demand"
    }
  }
}
```

## Fargate Profile Pattern

```hcl
fargate_profiles = {
  kube_system = {
    name = "${local.cluster_name}-kube-system"
    selectors = [
      {
        namespace = "kube-system"
        labels = {
          k8s-app = "kube-dns"
        }
      }
    ]
  }

  serverless = {
    name = "${local.cluster_name}-serverless"
    selectors = [
      { namespace = "serverless" },
      {
        namespace = "batch"
        labels    = { compute = "fargate" }
      }
    ]
  }
}
```

## IRSA Patterns

### VPC CNI IRSA
```hcl
module "vpc_cni_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name             = "${local.cluster_name}-vpc-cni"
  attach_vpc_cni_policy = true
  vpc_cni_enable_ipv4   = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-node"]
    }
  }

  tags = var.tags
}
```

### EBS CSI IRSA
```hcl
module "ebs_csi_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name             = "${local.cluster_name}-ebs-csi"
  attach_ebs_csi_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:ebs-csi-controller-sa"]
    }
  }

  tags = var.tags
}
```

### Custom Application IRSA
```hcl
module "app_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "${local.cluster_name}-app"

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["app-namespace:app-service-account"]
    }
  }

  role_policy_arns = {
    s3_read  = aws_iam_policy.s3_read.arn
    sqs_send = aws_iam_policy.sqs_send.arn
  }

  tags = var.tags
}
```

## Karpenter Pattern

```hcl
module "karpenter" {
  source  = "terraform-aws-modules/eks/aws//modules/karpenter"
  version = "~> 20.0"

  cluster_name = module.eks.cluster_name

  enable_v1_permissions           = true
  create_pod_identity_association = true

  node_iam_role_use_name_prefix = false
  node_iam_role_name            = "${local.cluster_name}-karpenter-node"

  node_iam_role_additional_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }

  tags = var.tags
}

# Karpenter Helm release (optional - can be done via GitOps)
resource "helm_release" "karpenter" {
  namespace        = "karpenter"
  create_namespace = true
  name             = "karpenter"
  repository       = "oci://public.ecr.aws/karpenter"
  chart            = "karpenter"
  version          = "1.0.0"

  values = [
    yamlencode({
      settings = {
        clusterName       = module.eks.cluster_name
        clusterEndpoint   = module.eks.cluster_endpoint
        interruptionQueue = module.karpenter.queue_name
      }
    })
  ]
}
```

## Access Entry Pattern (API Mode)

```hcl
access_entries = {
  admin_role = {
    principal_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/AdminRole"

    policy_associations = {
      admin = {
        policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
        access_scope = {
          type = "cluster"
        }
      }
    }
  }

  developer_role = {
    principal_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/DeveloperRole"

    policy_associations = {
      edit = {
        policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy"
        access_scope = {
          type       = "namespace"
          namespaces = ["dev", "staging"]
        }
      }
    }
  }

  readonly_role = {
    principal_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/ReadOnlyRole"

    policy_associations = {
      view = {
        policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy"
        access_scope = {
          type = "cluster"
        }
      }
    }
  }
}
```

## EKS KMS Key

```hcl
resource "aws_kms_key" "eks" {
  description             = "KMS key for EKS cluster ${local.cluster_name}"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow EKS Service"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = merge(var.tags, { Name = "${local.cluster_name}-eks" })
}

resource "aws_kms_alias" "eks" {
  name          = "alias/${local.cluster_name}-eks"
  target_key_id = aws_kms_key.eks.key_id
}
```

## Common Outputs

```hcl
output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded cluster CA certificate"
  value       = module.eks.cluster_certificate_authority_data
}

output "oidc_provider_arn" {
  description = "OIDC provider ARN for IRSA"
  value       = module.eks.oidc_provider_arn
}

output "cluster_security_group_id" {
  description = "Cluster security group ID"
  value       = module.eks.cluster_security_group_id
}

output "node_security_group_id" {
  description = "Node security group ID"
  value       = module.eks.node_security_group_id
}
```

## kubectl Configuration

```bash
# Update kubeconfig
aws eks update-kubeconfig --name ${local.cluster_name} --region ${data.aws_region.current.name}

# Verify connection
kubectl get nodes
kubectl get pods -A
```
