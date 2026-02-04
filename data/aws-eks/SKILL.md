---
name: aws-eks
description: Amazon Elastic Kubernetes Service (EKS) for running Kubernetes on AWS. Use for container orchestration, deploying applications, managing clusters, and Kubernetes workloads on AWS.
---

# AWS EKS (Amazon Elastic Kubernetes Service) Skill

Comprehensive assistance with Amazon EKS development, cluster management, and Kubernetes workloads on AWS.

## When to Use This Skill

Trigger this skill when working with:

### Cluster Operations
- Creating, configuring, or managing EKS clusters
- Setting up EKS Auto Mode clusters for simplified compute management
- Configuring cluster networking (IPv4/IPv6, VPC, subnets)
- Managing cluster access controls and IAM roles
- Enabling cluster features (logging, encryption, zonal shift)

### Add-ons & Extensions
- Installing or managing Amazon EKS add-ons (VPC CNI, CoreDNS, kube-proxy, CSI drivers)
- Working with community add-ons (Metrics Server, Prometheus, Cert Manager)
- Configuring add-on permissions and service accounts
- Running critical add-ons on dedicated system nodes

### Application Deployment
- Deploying containerized applications to EKS
- Creating Kubernetes deployments, services, and ingresses
- Configuring Horizontal Pod Autoscaler for scaling
- Managing workload namespaces and resource allocation

### Networking & Storage
- Configuring VPC CNI and pod networking
- Setting up IPv6 addressing for pods and services
- Integrating storage (EBS, EFS, FSx) with CSI drivers
- Managing Application Load Balancers with AWS Load Balancer Controller

### Monitoring & Observability
- Setting up Prometheus or CloudWatch monitoring
- Using the EKS observability dashboard
- Configuring control plane logs and metrics
- Troubleshooting cluster health issues

## Key Concepts

### EKS Cluster Types
- **Standard EKS**: Traditional cluster where you manage nodes and compute
- **EKS Auto Mode**: Simplified management where AWS handles compute provisioning, lifecycle, and optimization
- **EKS with Fargate**: Serverless compute for pods without managing nodes

### Node Pools (EKS Auto Mode)
- **General-purpose**: For standard application workloads
- **System**: Dedicated nodes for critical add-ons with `CriticalAddonsOnly` taint

### Add-on Types
- **AWS Add-ons**: Built and supported by AWS (VPC CNI, CoreDNS, kube-proxy, CSI drivers)
- **Community Add-ons**: Validated for compatibility but community-supported (Metrics Server, Prometheus)

### IAM Integration
- **Cluster IAM Role**: Permissions for EKS control plane to manage AWS resources
- **Node IAM Role**: Permissions for worker nodes (EC2 instances)
- **IRSA (IAM Roles for Service Accounts)**: Pod-level IAM permissions via OIDC

## Quick Reference

### Example 1: Create Basic EKS Cluster with eksctl

```bash
# Simple cluster creation with default settings
eksctl create cluster --name my-cluster --region us-west-2

# With specific node configuration
eksctl create cluster \
  --name my-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4
```

**Use when**: Starting a new EKS cluster quickly with standard configuration.

---

### Example 2: Create EKS Auto Mode Cluster

```bash
# Command-line approach
eksctl create cluster --name auto-cluster --enable-auto-mode

# YAML configuration approach
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: my-auto-cluster
  region: us-west-2

autoModeConfig:
  enabled: true
  # Leave nodePools empty for defaults (general-purpose, system)
  nodePools: []
```

**Use when**: You want AWS to manage compute resources automatically without configuring node groups.

---

### Example 3: Deploy Sample Application

```bash
# Create namespace
kubectl create namespace eks-sample-app

# Deploy application
kubectl apply -n eks-sample-app -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eks-sample-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: eks-sample
  template:
    metadata:
      labels:
        app: eks-sample
    spec:
      containers:
      - name: nginx
        image: public.ecr.aws/nginx/nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: eks-sample-service
spec:
  selector:
    app: eks-sample
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
EOF
```

**Use when**: Deploying a simple application with load balancer exposure.

---

### Example 4: Install Community Add-on (Metrics Server)

```bash
# Check add-on type
aws eks describe-addon-versions --addon-name metrics-server

# Install via AWS API
aws eks create-addon \
  --cluster-name my-cluster \
  --addon-name metrics-server \
  --addon-version v1.0.0-eksbuild.1

# Verify installation
kubectl get deployment metrics-server -n kube-system
```

**Use when**: Adding the Kubernetes Metrics Server for resource monitoring and HPA.

---

### Example 5: Configure Horizontal Pod Autoscaler

```bash
# Deploy sample application
kubectl apply -f https://k8s.io/examples/application/php-apache.yaml

# Create autoscaler (scale between 1-10 pods at 50% CPU)
kubectl autoscale deployment php-apache \
  --cpu-percent=50 \
  --min=1 \
  --max=10

# Check autoscaler status
kubectl get hpa

# Generate load to test scaling
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

**Use when**: Implementing automatic scaling based on CPU utilization.

---

### Example 6: Deploy Critical Add-on to System Node Pool (Auto Mode)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-addon
  namespace: kube-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: critical-addon
  template:
    metadata:
      labels:
        app: critical-addon
    spec:
      # Select system node pool
      nodeSelector:
        eks.amazonaws.com/compute-type: auto
        karpenter.sh/nodepool: system
      # Tolerate system node taint
      tolerations:
      - key: CriticalAddonsOnly
        operator: Exists
        effect: NoSchedule
      containers:
      - name: app
        image: critical-app:latest
```

**Use when**: Running critical infrastructure components on dedicated system nodes in EKS Auto Mode.

---

### Example 7: Create Cluster IAM Role

```bash
# Create trust policy
cat > eks-cluster-role-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create IAM role
aws iam create-role \
  --role-name myEKSClusterRole \
  --assume-role-policy-document file://eks-cluster-role-trust-policy.json

# Attach required policy
aws iam attach-role-policy \
  --role-name myEKSClusterRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
```

**Use when**: Setting up IAM permissions for EKS cluster control plane.

---

### Example 8: Deploy Prometheus for Monitoring

```bash
# Create namespace
kubectl create namespace prometheus

# Add Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/prometheus \
  --namespace prometheus \
  --set alertmanager.persistentVolume.storageClass="gp2" \
  --set server.persistentVolume.storageClass="gp2"

# Port forward to access dashboard
kubectl port-forward -n prometheus deploy/prometheus-server 9090
```

**Use when**: Setting up comprehensive monitoring for your EKS cluster.

---

### Example 9: Configure IPv6 for Cluster

```bash
# Create cluster with IPv6
aws eks create-cluster \
  --name my-ipv6-cluster \
  --kubernetes-network-config ipFamily=ipv6 \
  --vpc-config subnetIds=subnet-xxx,subnet-yyy,securityGroupIds=sg-xxx \
  --role-arn arn:aws:iam::account-id:role/myEKSClusterRole

# Get IPv6 service CIDR
aws eks describe-cluster \
  --name my-ipv6-cluster \
  --query cluster.kubernetesNetworkConfig.serviceIpv6Cidr \
  --output text
```

**Use when**: Building IPv6-native clusters to avoid IPv4 address exhaustion.

---

### Example 10: Deploy Application Load Balancer with Ingress

```bash
# Create namespace
kubectl create namespace game-2048 --save-config

# Deploy application with ingress
kubectl apply -n game-2048 -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.0/docs/examples/2048/2048_full.yaml

# Get ingress address
kubectl get ingress -n game-2048

# Output will show ALB address:
# NAME            CLASS   HOSTS   ADDRESS                                                                  PORTS   AGE
# ingress-2048    alb     *       k8s-game2048-ingress2-xxx.region.elb.amazonaws.com                      80      30s
```

**Use when**: Exposing applications via AWS Application Load Balancer with Kubernetes Ingress.

## Reference Files

This skill includes comprehensive documentation in `references/`:

### addons.md (4 pages)
- **Community add-ons**: Metrics Server, kube-state-metrics, Prometheus Node Exporter, Cert Manager, External DNS
- **Amazon EKS add-ons**: Managing official AWS add-ons, customization, namespace configuration
- **Critical workloads**: Running add-ons on dedicated system nodes with EKS Auto Mode
- **Add-on permissions**: Custom namespaces, RBAC configuration

**When to read**: Installing or managing cluster add-ons, configuring system node pools.

### cluster_management.md (121 pages)
- **Cluster creation**: Step-by-step guides with eksctl, AWS Console, and API
- **EKS Auto Mode**: Creating and managing Auto Mode clusters
- **Observability**: Dashboard usage, control plane monitoring, cluster health
- **Networking**: IPv6 configuration, VPC setup, subnet requirements
- **Access control**: IAM roles, OIDC providers, cluster endpoint access

**When to read**: Creating new clusters, troubleshooting cluster issues, configuring monitoring.

### deployment.md (10 pages)
- **Application deployment**: Sample applications, deployments, services
- **Prometheus setup**: Helm-based installation and configuration
- **Horizontal Pod Autoscaler**: Configuring automatic scaling based on metrics
- **Kubernetes workloads**: Deployments, ReplicaSets, StatefulSets

**When to read**: Deploying applications, setting up monitoring, configuring autoscaling.

### getting_started.md
- **Prerequisites**: AWS account setup, CLI tools, IAM permissions
- **First cluster**: Quickstart guides for different scenarios
- **kubectl setup**: Connecting to clusters, kubeconfig configuration
- **Initial workloads**: Deploying first applications

**When to read**: First-time EKS setup, onboarding new team members.

### networking.md
- **VPC CNI plugin**: Pod networking, ENI management
- **IPv4 and IPv6**: Address family selection and configuration
- **Load balancing**: ALB, NLB, and ingress controllers
- **Network policies**: Security groups, network isolation

**When to read**: Configuring cluster networking, troubleshooting connectivity, setting up load balancers.

### nodes.md
- **Node groups**: Managed node groups, self-managed nodes
- **EKS Auto Mode**: Automatic compute provisioning
- **Fargate profiles**: Serverless pod execution
- **Node IAM roles**: Permissions and IRSA setup

**When to read**: Managing compute resources, configuring node groups, setting up Fargate.

### security.md
- **IAM integration**: Cluster roles, node roles, IRSA (IAM Roles for Service Accounts)
- **Certificate management**: Kubernetes certificate API, custom signers
- **Encryption**: Control plane encryption, secrets encryption
- **Security groups**: Cluster security group, pod security groups

**When to read**: Implementing security best practices, configuring IAM permissions, certificate management.

### other.md
- **API reference**: Detailed API operation documentation
- **Advanced features**: EKS extensions, hybrid nodes, Outposts
- **Migration guides**: Upgrading clusters, migrating workloads
- **Troubleshooting**: Common issues and solutions

**When to read**: API integration, advanced use cases, troubleshooting complex issues.

## Working with This Skill

### For Beginners
1. **Start here**: Read `getting_started.md` for fundamental concepts and your first cluster
2. **Simple deployment**: Follow Example 3 to deploy a basic application
3. **Learn networking**: Understand how pods communicate via `networking.md`
4. **Add monitoring**: Set up Metrics Server (Example 4) and Prometheus (Example 8)
5. **Practice scaling**: Experiment with Horizontal Pod Autoscaler (Example 5)

### For Intermediate Users
1. **EKS Auto Mode**: Explore simplified cluster management with Examples 2 and 6
2. **Add-on management**: Learn community vs AWS add-ons in `addons.md`
3. **IAM integration**: Master IRSA and pod-level permissions in `security.md`
4. **Storage integration**: Configure EBS/EFS CSI drivers for persistent storage
5. **Load balancing**: Implement ingress controllers (Example 10)
6. **IPv6 networking**: Transition to IPv6 for future-proof addressing (Example 9)

### For Advanced Users
1. **Custom networking**: Deep dive into VPC CNI customization in `networking.md`
2. **Hybrid deployments**: Explore EKS Hybrid Nodes in `other.md`
3. **Security hardening**: Implement certificate signing, encryption at rest, pod security
4. **Observability**: Full-stack monitoring with Prometheus, Grafana, CloudWatch Container Insights
5. **Multi-cluster strategies**: Federation, service mesh, cross-cluster communication
6. **Cost optimization**: Right-sizing, Spot instances, Auto Mode for better resource utilization

### Navigation Tips
- **By category**: Each reference file covers a specific domain (networking, security, etc.)
- **By task**: Use Quick Reference examples as starting points for common tasks
- **By component**: Find specific add-ons or features using file descriptions above
- **Search within files**: Use `view` command to read specific sections of large reference files

## Common Workflows

### Creating Your First Cluster
```
getting_started.md → Example 1 (cluster creation) → Example 3 (deploy app) → Example 4 (add monitoring)
```

### Production Cluster Setup
```
cluster_management.md → security.md (IAM) → networking.md (VPC/IPv6) → addons.md (install essentials) → deployment.md (deploy workloads)
```

### Troubleshooting Issues
```
cluster_management.md (observability dashboard) → nodes.md (node health) → networking.md (connectivity) → other.md (common issues)
```

### Migrating to EKS Auto Mode
```
Example 2 (create Auto Mode cluster) → nodes.md (understand node pools) → Example 6 (critical add-ons) → deployment.md (migrate workloads)
```

## Best Practices

### Cluster Configuration
- Use **EKS Auto Mode** for simplified operations unless you need specific instance types
- Enable **control plane logging** to CloudWatch for troubleshooting
- Use **multiple availability zones** for high availability
- Configure **cluster endpoint access** appropriately (public, private, or both)

### Networking
- Use **IPv6** for new clusters to avoid address exhaustion
- Implement **Network Policies** for pod-to-pod security
- Use **AWS Load Balancer Controller** instead of legacy in-tree controllers
- Plan **CIDR ranges** carefully to avoid conflicts with peered VPCs

### Security
- Use **IRSA** (IAM Roles for Service Accounts) instead of node-level IAM roles
- Enable **secrets encryption** with AWS KMS
- Implement **Pod Security Standards** to enforce security policies
- Regularly update **add-ons** for security patches

### Monitoring
- Deploy **Metrics Server** for basic resource metrics
- Use **Prometheus + Grafana** or **CloudWatch Container Insights** for production monitoring
- Enable **control plane metrics** for API server health
- Set up **alerts** for cluster health issues

### Scaling
- Use **Horizontal Pod Autoscaler** for application scaling
- Use **Cluster Autoscaler** or **Karpenter** for node scaling (EKS Auto Mode handles this automatically)
- Configure **resource requests and limits** for predictable behavior
- Test **autoscaling** under load before production

## Resources

### Official Documentation
- [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Amazon EKS API Reference](https://docs.aws.amazon.com/eks/latest/APIReference/)
- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)

### Tools
- **eksctl**: Simplified cluster management CLI
- **kubectl**: Kubernetes command-line tool
- **AWS CLI**: AWS service management
- **Helm**: Kubernetes package manager

### Community
- [AWS Containers Roadmap](https://github.com/aws/containers-roadmap)
- [EKS Workshop](https://www.eksworkshop.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

## Notes

- This skill was automatically generated from official AWS EKS documentation
- Examples are extracted from real-world usage patterns and AWS documentation
- Code examples include language detection for proper syntax highlighting
- Always check AWS documentation for latest API versions and features
- EKS Auto Mode is recommended for new users and simplified operations

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information from AWS docs
3. Review changes in cluster versions, API updates, and new features
