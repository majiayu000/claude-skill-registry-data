---




name: aws-eks
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Deploys managed Kubernetes clusters with EKS for container orchestration"
  auto-scaling, networking, and integrations with AWS services for production Kubernetes
  workloads.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-cloudwatch, aws-ecr, aws-iam, aws-vpc
  role: reference
  scope: infrastructure
  triggers: eks, container orchestration, k8s, cluster, pods, namespaces, ingress,
    kubernetes namespace
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




# EKS (Elastic Kubernetes Service)

Deploy and manage production-grade Kubernetes clusters with automatic control plane updates, high availability, and deep AWS service integration.

## TL;DR Checklist

- [ ] Use managed node groups for automatic scaling
- [ ] Enable multiple AZs for high availability
- [ ] Configure RBAC with IAM Roles for Service Accounts (IRSA)
- [ ] Use AWS Load Balancer Controller for ingress
- [ ] Enable cluster logging to CloudWatch
- [ ] Configure network policies for security
- [ ] Use Fargate for serverless pods
- [ ] Enable Pod Security Policy or Pod Security Standards
- [ ] Monitor cluster metrics with CloudWatch
- [ ] Regular cluster and node updates

---

## When to Use

Use EKS when:

- Running containerized microservices
- Needing Kubernetes orchestration
- Requiring managed Kubernetes (no control plane management)
- Building scalable container applications
- Integrating with AWS services from containers

---

## When NOT to Use

Avoid EKS when:

- Simple workloads better served by Fargate only
- Self-managed K8s preferred (use EC2 + kubeadm)
- Minimal operational overhead needed (use App Runner)

---

## Purpose and Use Cases

**Primary Purpose:** Provide fully managed Kubernetes control plane with integration to AWS services, eliminating control plane management overhead.

**Common Use Cases:**

1. **Microservices** — Deploy service mesh (Istio/Linkerd)
2. **Data Processing** — Run Apache Spark, Hadoop jobs
3. **CI/CD Pipelines** — Build runners, artifact processing
4. **API Services** — High-scale REST/gRPC APIs
5. **Batch Jobs** — Scheduled batch processing

---

## Architecture Design Patterns

### Pattern 1: EKS Cluster with Managed Node Groups

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # EKS Cluster IAM Role
  EKSServiceRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSServiceRolePolicy

  # EKS Cluster
  EKSCluster:
    Type: AWS::EKS::Cluster
    Properties:
      Name: production-cluster
      Version: 1.27
      RoleArn: !GetAtt EKSServiceRole.Arn
      ResourcesVpcConfig:
        SubnetIds:
          - subnet-0123456789abcdef0
          - subnet-0123456789abcdef1
          - subnet-0123456789abcdef2
        SecurityGroupIds:
          - sg-0123456789abcdef0
        EndpointPrivateAccess: true
        EndpointPublicAccess: true
      Logging:
        ClusterLogging:
          - LogTypes:
              - api
              - audit
              - authenticator
              - controllerManager
              - scheduler
            Enabled: true
      Tags:
        Environment: production

  # Node Group IAM Role
  NodeGroupRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser

  # Managed Node Group
  NodeGroup:
    Type: AWS::EKS::NodeGroup
    Properties:
      ClusterName: !Ref EKSCluster
      NodeRole: !GetAtt NodeGroupRole.Arn
      Subnets:
        - subnet-0123456789abcdef0
        - subnet-0123456789abcdef1
        - subnet-0123456789abcdef2
      ScalingConfig:
        MinSize: 2
        MaxSize: 10
        DesiredSize: 3
      InstanceTypes:
        - t3.medium
        - t3.large
      DiskSize: 100
      Tags:
        Name: production-nodes
```

**Key Elements:**
- EKS cluster with managed control plane
- Multi-AZ for high availability
- Managed node group with auto-scaling
- CloudWatch logging enabled
- IAM roles for service and nodes

### Pattern 2: IRSA (IAM Roles for Service Accounts)

```yaml
Resources:
  # OIDC Provider for IRSA
  EKSOIDCProvider:
    Type: AWS::IAM::OIDCProvider
    Properties:
      Url: !Sub 'https://oidc.eks.${AWS::Region}.amazonaws.com/id/${EKSClusterOID}'
      ClientIdList:
        - sts.amazonaws.com

  # Service Account Role
  ServiceAccountRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Federated: !Sub 'arn:aws:iam::${AWS::AccountId}:oidc-provider/oidc.eks.${AWS::Region}.amazonaws.com/id/${EKSClusterOID}'
            Action: sts:AssumeRoleWithWebIdentity
            Condition:
              StringEquals:
                'oidc.eks.${AWS::Region}.amazonaws.com/id/${EKSClusterOID}:sub': 'system:serviceaccount:default:app-sa'

  # Application Policy
  AppPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: app-s3-access
      Roles:
        - !Ref ServiceAccountRole
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - s3:GetObject
              - s3:PutObject
            Resource: arn:aws:s3:::app-bucket/*
```

**Key Elements:**
- OIDC provider for service account federation
- Pod can assume IAM role without credentials
- Fine-grained permissions per service account

---

## Integration Approaches

### 1. Integration with ECR

EKS + ECR provides:
- Container image registry
- Pod pulls images directly from ECR
- No Docker Hub dependency

### 2. Integration with AWS Load Balancer Controller

ALB/NLB integration enables:
- Kubernetes Ingress resources map to ALBs
- Service type LoadBalancer creates NLBs
- Native AWS load balancing

### 3. Integration with CloudWatch

CloudWatch + EKS provides:
- Cluster metrics and logs
- Application performance insights
- Operational dashboards

### 4. Integration with VPC

VPC integration provides:
- Pod networking in VPC subnets
- Security groups for pod-level control
- Network policies for microsegmentation

---

## Common Pitfalls

### ❌ Pitfall 1: Single AZ Cluster

**Problem:** AZ failure causes complete outage.

**Solution:**
- Deploy node groups across 3+ AZs
- Use managed node groups for auto-scaling

### ❌ Pitfall 2: No RBAC

**Problem:** Cluster access uncontrolled; security risk.

**Solution:**
- Enable RBAC (default)
- Use IRSA for pod permissions
- Restrict cluster access via security groups

### ❌ Pitfall 3: Pod Security Uncontrolled

**Problem:** Containers run as root; privileged pods.

**Solution:**
- Enable Pod Security Standards
- Enforce restricted policy
- Regular security audits

### ❌ Pitfall 4: No Log Aggregation

**Problem:** Cluster issues hard to troubleshoot.

**Solution:**
- Enable control plane logging
- Stream to CloudWatch
- Archive to S3 for long-term

---

## Best Practices Summary

| Category | Best Practice |
|---|---|
| **Availability** | Multi-AZ node groups; managed updates |
| **Security** | RBAC; IRSA; network policies; PSS |
| **Scaling** | Cluster Autoscaler; HPA for pods |
| **Monitoring** | CloudWatch logs; Prometheus/Grafana |
| **Updates** | Regular cluster and node updates |

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-aws-ecr` | Container image storage |
| `cncf-aws-vpc` | Networking for pod communication |
| `cncf-aws-iam` | IRSA and role management |
| `cncf-aws-cloudwatch` | Cluster monitoring |
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests
