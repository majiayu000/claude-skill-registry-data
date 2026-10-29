---
name: aws-vpc
description: Design and implement VPCs and networking. Configure subnets, route tables, and security groups. Use when setting up AWS network infrastructure. 
category: AI & Agents
source: antigravity
tags: [ai, agent, template, design, security, aws, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/aws-vpc
---


# AWS VPC

Design and manage Virtual Private Cloud networking for production AWS environments with proper subnet isolation, routing, and security.

## When to Use This Skill

- Building a new VPC for production, staging, or development
- Setting up public/private subnet architecture across multiple AZs
- Configuring NAT Gateways for private subnet internet access
- Creating security groups and NACLs for network segmentation
- Setting up VPC peering or Transit Gateway for multi-VPC connectivity
- Implementing VPC endpoints for private access to AWS services
- Troubleshooting connectivity issues between resources

## Prerequisites

- AWS CLI v2 installed and configured
- IAM permissions scoped to the needed VPC actions/resources and approved account/region
- CIDR range planning completed (avoid overlaps with on-premises or other VPCs)
- For VPC peering: access to both VPCs (same or different accounts)

## Network Architecture

Diagram address counts are total addresses; AWS reserves five per subnet, so a /24 normally has251 assignable addresses. Confirm account/region, AZ availability, nonoverlapping CIDRs, routing and approved cost before creation. CLI examples create twoAZs; the Terraform example creates three. Inspect existing resources and plan rollback rather than rerunning non-idempotent create commands. VPC/subnet tags do not enforce isolation: explicitly associate data subnets with local-only route tables and verify no inherited default route. New security groups allow all outbound by default; scope egress to actual dependencies.

```
VPC (10.0.0.0/16) - 65,536 IPs
├── Public Subnets (internet-facing via IGW)
│   ├── 10.0.1.0/24 (us-east-1a) - 256 IPs - ALBs, NAT GW, bastion
│   ├── 10.0.2.0/24 (us-east-1b) - 256 IPs
│   └── 10.0.3.0/24 (us-east-1c) - 256 IPs
├── Private Subnets (app tier, NAT GW for outbound)
│   ├── 10.0.11.0/24 (us-east-1a) - 256 IPs - ECS, EC2, Lambda
│   ├── 10.0.12.0/24 (us-east-1b) - 256 IPs
│   └── 10.0.13.0/24 (us-east-1c) - 256 IPs
├── Data Subnets (isolated, no internet)
│   ├── 10.0.21.0/24 (us-east-1a) - 256 IPs - RDS, ElastiCache
│   ├── 10.0.22.0/24 (us-east-1b) - 256 IPs
│   └── 10.0.23.0/24 (us-east-1c) - 256 IPs
├── Internet Gateway
├── NAT Gateways (one per AZ for HA)
├── Route Tables (public, private, data)
└── VPC Flow Logs → CloudWatch / S3
```

## Create a VPC with CLI

```bash
# Create the VPC
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=production-vpc},{Key=Environment,Value=production}]' \
  --query 'Vpc.VpcId' --output text)

# Enable DNS support and hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames '{"Value":true}'

# Create public subnets
PUB_SUB_A=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-a},{Key=Tier,Value=public}]' \
  --query 'Subnet.SubnetId' --output text)

PUB_SUB_B=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1b \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-b},{Key=Tier,Value=public}]' \
  --query 'Subnet.SubnetId' --output text)

# Enable auto-assign public IP on public subnets
aws ec2 modify-subnet-attribute --subnet-id $PUB_SUB_A --map-public-ip-on-launch
aws ec2 modify-subnet-attribute --subnet-id $PUB_SUB_B --map-public-ip-on-launch

# Create private subnets
PRIV_SUB_A=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.11.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-a},{Key=Tier,Value=private}]' \
  --query 'Subnet.SubnetId' --output text)

PRIV_SUB_B=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.12.0/24 \
  --availability-zone us-east-1b \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-b},{Key=Tier,Value=private}]' \
  --query 'Subnet.SubnetId' --output text)

# Create data subnets (isolated)
DATA_SUB_A=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.21.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=data-a},{Key=Tier,Value=data}]' \
  --query 'Subnet.SubnetId' --output text)

DATA_SUB_B=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.22.0/24 \
  --availability-zone us-east-1b \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=data-b},{Key=Tier,Value=data}]' \
  --query 'Subnet.SubnetId' --output text)
```

## Internet Gateway and NAT Gateway

```bash
# Create and attach Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=production-igw}]' \
  --query 'InternetGateway.InternetGatewayId' --output text
