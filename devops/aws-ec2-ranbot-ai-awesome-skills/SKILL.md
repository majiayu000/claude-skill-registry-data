---
name: aws-ec2
description: Manage EC2 instances, AMIs, and auto-scaling groups. Configure security groups, key pairs, and instance types. Use when deploying compute resources on AWS. 
category: AI & Agents
source: antigravity
tags: [ai, agent, template, image, security, aws, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/aws-ec2
---


# AWS EC2

Deploy and manage Amazon EC2 compute instances for production, staging, and development workloads.

## When to Use This Skill

- Launching new compute instances for application hosting
- Building golden AMIs for consistent deployments
- Setting up auto-scaling groups behind load balancers
- Migrating workloads to Spot instances for cost savings
- Troubleshooting instance connectivity, performance, or launch failures
- Creating launch templates for repeatable infrastructure

## Prerequisites

- AWS CLI v2 installed and configured (`aws configure`)
- Least-privilege IAM actions for selected compute, scaling and load-balancer resources; restrict iam:PassRole to the intended instance role
- An existing VPC with subnets (see aws-vpc (`aws-vpc`))
- SSH key pair created (`umask 077` before creating a key file in a private directory; prefer approved session access where appropriate)

## Instance Type Selection Guide

| Category | Types | Use Case |
|---|---|---|
| General Purpose | t3, t3a, m6i, m7g | Web servers, small databases, dev/test |
| Compute Optimized | c6i, c7g | Batch processing, media encoding, ML inference |
| Memory Optimized | r6i, r7g, x2idn | In-memory caches, large databases |
| Storage Optimized | i3, i4i, d3 | Data warehousing, distributed file systems |
| Accelerated | p4d, g5, inf2 | ML training, GPU rendering, inference |
| Burstable | t3.micro-t3.2xlarge | Low-steady-state with occasional bursts |

## Launch an Instance

```bash
# Launch a production web server
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --iam-instance-profile Name=EC2AppProfile \
  --metadata-options "HttpTokens=required,HttpEndpoint=enabled" \
  --block-device-mappings '[{
    "DeviceName": "/dev/xvda",
    "Ebs": {
      "VolumeSize": 30,
      "VolumeType": "gp3",
      "Iops": 3000,
      "Throughput": 125,
      "Encrypted": true
    }
  }]' \
  --tag-specifications 'ResourceType=instance,Tags=[
    {Key=Name,Value=web-server-01},
    {Key=Environment,Value=production},
    {Key=Team,Value=platform}
  ]' \
  --user-data file://userdata.sh

# Launch with IMDSv2 required (security best practice)
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --metadata-options "HttpTokens=required,HttpPutResponseHopLimit=1,HttpEndpoint=enabled" \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=secure-instance}]'
```

## User Data Scripts

```bash
#!/bin/bash
# userdata.sh - Bootstrap a web server on Amazon Linux 2023
set -euo pipefail # avoid tracing secrets in user-data logs

# System updates
dnf update -y

# Install and start web server
dnf install -y nginx
systemctl enable nginx
systemctl start nginx

# Install CloudWatch agent
dnf install -y amazon-cloudwatch-agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 \
  -s -c ssm:AmazonCloudWatch-linux

# Install CodeDeploy agent
dnf install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
# Verify a reviewed pinned installer and integrity before execution; do not run latest blindly.

# Signal CloudFormation (if launched via CFN)
# /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource ASG --region ${AWS::Region}
```

## Launch Templates

```bash
# Create a launch template with full configuration
aws ec2 create-launch-template \
  --launch-template-name web-server-template \
  --version-description "v1 - AL2023 with nginx" \
  --launch-template-data '{
    "ImageId": "ami-0abcdef1234567890",
    "InstanceType": "t3.medium",
    "KeyName": "my-key",
    "SecurityGroupIds": ["sg-12345678"],
    "IamInstanceProfile": {"Name": "EC2AppProfile"},
    "MetadataOptions": {
      "HttpTokens": "required",
      "HttpEndpoint": "enabled"
    },
    "BlockDeviceMappings": [{
      "DeviceName": "/dev/xvda",
      "Ebs": {
        "VolumeSize": 30,
        "VolumeType": "gp3",
        "Encrypted": true
      }
    }],
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Environment", "Value": "production"},
        {"Key": "ManagedBy", "Value": "launch-template"}
      ]
    }],
    "Monitoring": {"Enabled": true},
    "UserData": "'"$(base64 -w0 userdata.sh)"'"
  }'

# Create a new version of the launch template
aws ec2 create-launch-template-version \
  --launch-template-name web-server-template \
  --source-version 1 \
  --version-description "v2 - updated AMI" \
  --launch-template-data '{"ImageId": "ami-0newami1234567890"}'

# Set the default version
aws ec2 modify-launch-template \
  --launch-template-name web-server-template \
  --default-version 2
```

## Auto Scaling Group

```bash
# Create ASG with mixed instances (on-demand + spot)
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --m
