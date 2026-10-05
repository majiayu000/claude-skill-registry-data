---




name: aws-vpc
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Configures Virtual Private Clouds with subnets, route tables, NAT gateways"
  security groups, and network ACLs for secure, isolated network infrastructure on
  AWS.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-cloudformation, aws-ec2, aws-eks, aws-elb
  role: reference
  scope: infrastructure
  triggers: vpc, virtual private cloud, subnet, route table, security group, nat gateway,
    network acl, vpn
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




# VPC (Virtual Private Cloud)

Design and configure isolated cloud networks with subnets, route tables, security groups, and advanced networking features for secure, scalable infrastructure.

## TL;DR Checklist

- [ ] Use multiple availability zones for high availability
- [ ] Separate public and private subnets by function
- [ ] Use NAT gateways for private subnet egress (not NAT instances)
- [ ] Configure security groups as stateful firewalls
- [ ] Use network ACLs for stateless, subnet-level filtering
- [ ] Enable VPC Flow Logs for network traffic analysis
- [ ] Configure route tables with specific routes (no overly broad routes)
- [ ] Use VPC endpoints for private AWS service access
- [ ] Enable DNS hostnames and DNS resolution
- [ ] Plan IP address space with non-overlapping CIDRs

---

## When to Use

Use VPC when:

- Isolating resources within a custom network
- Building production infrastructure requiring network control
- Implementing network segmentation and security boundaries
- Creating hybrid architectures with on-premises networks
- Building multi-tier applications with different security zones

---

## When NOT to Use

Avoid VPC complexity when:

- Building simple proof-of-concepts
- Requiring no network customization (default VPC acceptable)
- Running fully serverless architectures (less relevant for Lambda)

---

## Purpose and Use Cases

**Primary Purpose:** Provide isolated, customizable network environments with granular control over IP addressing, routing, and access control.

**Common Use Cases:**

1. **Production Application Tiers** — Web, app, database layers in separate subnets
2. **Hybrid Cloud** — VPN/Direct Connect to on-premises networks
3. **Multi-Tenancy** — Isolated VPCs per tenant with VPC peering
4. **Disaster Recovery** — Secondary VPC in different region with failover
5. **Development/Testing** — Separate non-production VPCs with minimal cost

---

## Architecture Design Patterns

### Pattern 1: Three-Tier Production VPC with High Availability

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # VPC
  ProductionVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: production-vpc

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: prod-igw

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref ProductionVPC
      InternetGatewayId: !Ref InternetGateway

  # Public Subnets (for ALB and NAT)
  PublicSubnetAZ1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: us-east-1a
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: public-subnet-az1

  PublicSubnetAZ2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: us-east-1b
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: public-subnet-az2

  PublicSubnetAZ3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.3.0/24
      AvailabilityZone: us-east-1c
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: public-subnet-az3

  # Private Subnets (for application servers)
  PrivateSubnetAZ1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.11.0/24
      AvailabilityZone: us-east-1a
      Tags:
        - Key: Name
          Value: private-subnet-az1
        - Key: Type
          Value: Application

  PrivateSubnetAZ2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.12.0/24
      AvailabilityZone: us-east-1b
      Tags:
        - Key: Name
          Value: private-subnet-az2
        - Key: Type
          Value: Application

  PrivateSubnetAZ3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.13.0/24
      AvailabilityZone: us-east-1c
      Tags:
        - Key: Name
          Value: private-subnet-az3
        - Key: Type
          Value: Application

  # Database Subnets (for RDS)
  DBSubnetAZ1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.21.0/24
      AvailabilityZone: us-east-1a
      Tags:
        - Key: Name
          Value: db-subnet-az1
        - Key: Type
          Value: Database

  DBSubnetAZ2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ProductionVPC
      CidrBlock: 10.0.22.0/24
      AvailabilityZone: us-east-1b
      Tags:
        - Key: Name
          Value: db-subnet-az2
        - Key: Type
          Value: Database

  # NAT Gateway (High Availability - one per AZ)
  NATGatewayEIP1:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: nat-eip-az1

  NATGateway1:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGatewayEIP1.AllocationId
      SubnetId: !Ref PublicSubnetAZ1
      Tags:
        - Key: Name
          Value: nat-gateway-az1

  NATGatewayEIP2:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: nat-eip-az2

  NATGateway2:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGatewayEIP2.AllocationId
      SubnetId: !Ref PublicSubnetAZ2
      Tags:
        - Key: Name
          Value: nat-gateway-az2

  NATGatewayEIP3:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: nat-eip-az3

  NATGateway3:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGatewayEIP3.AllocationId
      SubnetId: !Ref PublicSubnetAZ3
      Tags:
        - Key: Name
          Value: nat-gateway-az3

  # Route Tables
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ProductionVPC
      Tags:
        - Key: Name
          Value: public-rt

  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  # Associate public subnets with public route table
  AssocPublicSubnetAZ1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetAZ1
      RouteTableId: !Ref PublicRouteTable

  AssocPublicSubnetAZ2:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetAZ2
      RouteTableId: !Ref PublicRouteTable

  AssocPublicSubnetAZ3:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetAZ3
      RouteTableId: !Ref PublicRouteTable

  # Private Route Tables (one per AZ for NAT)
  PrivateRouteTableAZ1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ProductionVPC
      Tags:
        - Key: Name
          Value: private-rt-az1

  PrivateRouteAZ1:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTableAZ1
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NATGateway1

  AssocPrivateSubnetAZ1:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnetAZ1
      RouteTableId: !Ref PrivateRouteTableAZ1

  # Similar for AZ2 and AZ3...

  # VPC Flow Logs
  VPCFlowLogRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: vpc-flow-logs.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: CloudWatchLogPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:DescribeLogGroups
                  - logs:DescribeLogStreams
                Resource: '*'

  VPCFlowLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/vpc/flowlogs
      RetentionInDays: 30

  VPCFlowLog:
    Type: AWS::EC2::FlowLog
    Properties:
      ResourceType: VPC
      ResourceId: !Ref ProductionVPC
      TrafficType: ALL
      LogDestinationType: cloud-watch-logs
      LogGroupName: !Ref VPCFlowLogGroup
      DeliverLogsPermissionIAM: !GetAtt VPCFlowLogRole.Arn
      Tags:
        - Key: Name
          Value: prod-vpc-flowlog
```

**Key Elements:**
- Multi-AZ subnets for high availability
- Public subnets for ALB and NAT gateways
- Private subnets for application servers
- Database subnets for RDS
- NAT gateway per AZ for egress (not single point of failure)
- Public/private route tables with appropriate routes
- VPC Flow Logs for network traffic analysis

### Pattern 2: Security Groups and Network ACLs

```yaml
Resources:
  # Security Group for ALB
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: alb-sg
      GroupDescription: Security group for Application Load Balancer
      VpcId: !Ref ProductionVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP from internet
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS from internet
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
          Description: Allow all outbound
      Tags:
        - Key: Name
          Value: alb-sg

  # Security Group for Application Tier
  AppSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: app-sg
      GroupDescription: Security group for application servers
      VpcId: !Ref ProductionVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref ALBSecurityGroup
          Description: App traffic from ALB
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          SourceSecurityGroupId: !Ref BastionSecurityGroup
          Description: SSH from bastion
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
          Description: Allow all outbound
      Tags:
        - Key: Name
          Value: app-sg

  # Security Group for Database
  DBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: db-sg
      GroupDescription: Security group for database servers
      VpcId: !Ref ProductionVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref AppSecurityGroup
          Description: PostgreSQL from app tier
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
          Description: Allow all outbound
      Tags:
        - Key: Name
          Value: db-sg

  # Network ACL for Database Subnets
  DBNetworkAcl:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref ProductionVPC
      Tags:
        - Key: Name
          Value: db-nacl

  # Inbound Rule: PostgreSQL from App Tier
  DBIngressPostgreSQL:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref DBNetworkAcl
      RuleNumber: 100
      Protocol: 6  # TCP
      RuleAction: allow
      CidrBlock: 10.0.11.0/24  # App subnet AZ1
      PortRange:
        FromPort: 5432
        ToPort: 5432

  # Inbound Rule: Ephemeral ports for return traffic
  DBIngressEphemeral:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref DBNetworkAcl
      RuleNumber: 120
      Protocol: 6  # TCP
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        FromPort: 1024
        ToPort: 65535

  # Outbound Rule: Allow all
  DBEgress:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref DBNetworkAcl
      RuleNumber: 100
      Protocol: -1  # All
      Egress: true
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
```

**Key Elements:**
- Security groups as stateful firewalls
- Reference-based ingress rules (security group ID, not CIDR)
- Network ACLs for stateless filtering
- Principle of least privilege for all rules
- Clear descriptions for auditing

### Pattern 3: VPC Endpoints for Private AWS Service Access

```yaml
Resources:
  # S3 Gateway Endpoint (free)
  S3Endpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref ProductionVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.s3'
      RouteTableIds:
        - !Ref PrivateRouteTableAZ1
        - !Ref PrivateRouteTableAZ2
        - !Ref PrivateRouteTableAZ3
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal: '*'
            Action:
              - s3:GetObject
              - s3:PutObject
            Resource: arn:aws:s3:::app-bucket/*

  # DynamoDB Gateway Endpoint
  DynamoDBEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref ProductionVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.dynamodb'
      RouteTableIds:
        - !Ref PrivateRouteTableAZ1
        - !Ref PrivateRouteTableAZ2
        - !Ref PrivateRouteTableAZ3

  # Secrets Manager Interface Endpoint
  SecretsManagerEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref ProductionVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.secretsmanager'
      VpcEndpointType: Interface
      SubnetIds:
        - !Ref PrivateSubnetAZ1
        - !Ref PrivateSubnetAZ2
        - !Ref PrivateSubnetAZ3
      SecurityGroupIds:
        - !Ref EndpointSecurityGroup
      PrivateDnsEnabled: true

  # Security Group for Interface Endpoints
  EndpointSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for VPC endpoints
      VpcId: !Ref ProductionVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 10.0.0.0/16  # VPC CIDR
          Description: HTTPS from VPC
```

**Key Elements:**
- S3/DynamoDB gateway endpoints (no charges)
- Interface endpoints for other services
- Private DNS enabled for seamless access
- Subnet and security group configuration

---

## Integration Approaches

### 1. Integration with Route 53

VPC + Route 53 provides:
- Private hosted zones for internal DNS
- DNS resolution for VPC resources
- Health checks for failover

### 2. Integration with Direct Connect

VPC + Direct Connect enables:
- Dedicated network connection to on-premises
- Low-latency, high-bandwidth hybrid connectivity
- Consistent network performance

### 3. Integration with VPN

VPC + VPN provides:
- Encrypted site-to-site connectivity
- Remote access VPN for employees
- Cost-effective alternative to Direct Connect

### 4. Integration with VPC Peering

Multi-VPC connectivity:
- Non-transitive peering between VPCs
- Cross-account and cross-region peering
- Private connectivity between VPCs

---

## Common Pitfalls

### ❌ Pitfall 1: Overlapping CIDR Blocks

**Problem:** Overlapping subnets prevent routing between VPCs or on-premises networks.

**Solution:**
- Plan IP address space upfront
- Use tools like ipcalc to prevent overlap
- Document CIDR allocation per VPC
- Use VPC CIDR 10.x.0.0/8 range for planning space

### ❌ Pitfall 2: Single NAT Gateway

**Problem:** NAT gateway in single AZ becomes bottleneck; AZ failure affects all private subnets.

**Solution:**
- Deploy NAT gateway per AZ
- Route each private subnet to local AZ NAT
- Distributes bandwidth; no single point of failure

### ❌ Pitfall 3: Overly Permissive Security Groups

**Problem:** Allow all traffic violates least-privilege; increases blast radius.

**Solution:**
- Restrict ingress to required ports/sources
- Use security group references instead of CIDR blocks
- Regularly audit rules
- Deny by default

### ❌ Pitfall 4: No VPC Flow Logs

**Problem:** Network issues hard to troubleshoot; no traffic visibility.

**Solution:**
- Enable VPC Flow Logs to CloudWatch
- Analyze traffic patterns and anomalies
- Integrate with CloudWatch Insights for queries
- Monitor rejected connections

### ❌ Pitfall 5: Bastion Host Too Permissive

**Problem:** SSH to EC2 instances allowed from anywhere.

**Solution:**
- Require bastion host for SSH access
- Restrict bastion ingress to known IPs
- Use Systems Manager Session Manager (no SSH needed)
- Log all bastion access

### ❌ Pitfall 6: Not Using VPC Endpoints

**Problem:** Private subnets route all traffic through NAT gateway; adds cost and latency.

**Solution:**
- Use S3/DynamoDB gateway endpoints (no charge)
- Interface endpoints for Secrets Manager, KMS, etc.
- Reduces NAT gateway traffic and costs

---

## Best Practices Summary

| Category | Best Practice |
|---|---|
| **Architecture** | Multi-AZ subnets; separate public/private/database layers |
| **NAT** | One NAT gateway per AZ; no single point of failure |
| **Security** | Least-privilege security groups; use reference-based rules |
| **Monitoring** | Enable VPC Flow Logs; analyze traffic patterns |
| **Endpoints** | Use gateway endpoints for S3/DynamoDB; interface for others |
| **DNS** | Use private hosted zones for internal DNS |

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-aws-ec2` | Deploy instances within VPC subnets |
| `cncf-aws-rds` | Database subnets and security groups |
| `cncf-aws-elb` | Load balancers integrated with VPC |
| `cncf-aws-iam` | Network-level access controls |
| `cncf-aws-cloudformation` | Infrastructure as code for VPC |
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

---

## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Primary Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnets.html)
- [Configuration Guide](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
- [Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Network_Acls.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Security_Groups.html)

