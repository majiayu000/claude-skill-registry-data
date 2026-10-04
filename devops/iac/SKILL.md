---
name: iac
description: Infrastructure as Code practices
license: MIT
compatibility: opencode
metadata:
  audience: developer, devops-engineer
  category: devops
---

## What I do

- Write and maintain Infrastructure as Code
- Use tools like Terraform, CloudFormation, Pulumi
- Implement GitOps workflows for infrastructure
- Create reusable modules and components
- Manage state and secrets in IaC
- Implement policy-as-code

## When to use me

- When provisioning cloud infrastructure
- When managing multi-environment deployments
- When implementing GitOps practices
- When auditing infrastructure changes
- When automating infrastructure lifecycle
- When managing complex dependencies

## Key Concepts

### Terraform Example

```hcl
# Module structure
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.0.0"
  
  name = "main-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.0.0"
  
  cluster_name    = "my-cluster"
  cluster_version = "1.27"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    primary = {
      min_size       = 2
      max_size       = 10
      desired_size   = 2
      
      instance_types = ["t3.medium"]
    }
  }
}
```

### Pulumi Program

```python
import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
)

# Create subnets
subnet = aws.ec2.Subnet(
    "my-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
)

# Create security group
sg = aws.ec2.SecurityGroup(
    "web-sg",
    description="Security group for web servers",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
)

# Export VPC ID
pulumi.export("vpc_id", vpc.id)
```

### CloudFormation Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'EKS Cluster'

Parameters:
  ClusterName:
    Type: String
    Default: my-cluster
    
Resources:
  EKSCluster:
    Type: AWS::EKS::Cluster
    Properties:
      Name: !Ref ClusterName
      Version: '1.27'
      RoleArn: !GetAtt EKSRole.Arn
      ResourcesVpcConfig:
        SubnetIds:
          - !Ref Subnet1
          - !Ref Subnet2

  EKSRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole

Outputs:
  ClusterEndpoint:
    Value: !GetAtt EKSCluster.Endpoint
```

### State Management

```hcl
# Remote state with locking
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Testing IaC

```python
# Terratest example
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/gruntwork-io/terratest/modules/terraform"
)

func TestEC2Instance(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/ec2",
        Vars: map[string]interface{}{
            "instance_type": "t3.micro",
        },
    }
    
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)
    
    instanceID := terraform.Output(t, terraformOptions, "instance_id")
    assert.NotEmpty(t, instanceID)
}
```

### Key Practices

- **Version Control**: Store all IaC in Git
- **Modules**: Create reusable components
- **Workspaces**: Manage environments
- **State Management**: Use remote state with locking
- **Secrets**: Never commit secrets, use vaults
- **Testing**: Validate before applying
- **Drift Detection**: Monitor for changes outside IaC
