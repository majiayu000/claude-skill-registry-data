---
name: aws-vpc-design
description: Design and implement production-grade VPC architectures
sasmp_version: "1.3.0"
bonded_agent: 04-aws-networking
bond_type: PRIMARY_BOND
---

# AWS VPC Design Skill

Create secure, scalable VPC architectures with proper segmentation.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | VPC |
| Complexity | Medium-High |
| Est. Time | 15-30 min |
| Prerequisites | CIDR planning |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| vpc_cidr | string | VPC CIDR block | Valid CIDR /16-/28 |
| availability_zones | int | Number of AZs | 1-6 |
| region | string | AWS region | Valid region |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enable_nat | bool | true | NAT Gateway for private subnets |
| enable_vpn | bool | false | VPN Gateway |
| enable_flow_logs | bool | true | VPC Flow Logs |
| subnet_strategy | string | tiered | tiered, flat, or custom |

## VPC Architecture Pattern

```
VPC: 10.0.0.0/16
│
├── Public Subnets (Internet-facing)
│   ├── 10.0.1.0/24 (AZ-a) - ALB, NAT Gateway
│   ├── 10.0.2.0/24 (AZ-b) - ALB, NAT Gateway
│   └── 10.0.3.0/24 (AZ-c) - ALB, NAT Gateway
│
├── Private Subnets (Application tier)
│   ├── 10.0.11.0/24 (AZ-a) - EC2, ECS, Lambda
│   ├── 10.0.12.0/24 (AZ-b) - EC2, ECS, Lambda
│   └── 10.0.13.0/24 (AZ-c) - EC2, ECS, Lambda
│
└── Database Subnets (Data tier)
    ├── 10.0.21.0/24 (AZ-a) - RDS, ElastiCache
    ├── 10.0.22.0/24 (AZ-b) - RDS, ElastiCache
    └── 10.0.23.0/24 (AZ-c) - RDS, ElastiCache
```

## Implementation

### Create VPC
```bash
# Create VPC
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=prod-vpc}]' \
  --query 'Vpc.VpcId' --output text)

# Enable DNS
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-support
```

### Create Subnets
```bash
# Public subnet
aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-1a}]'

# Private subnet
aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.11.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-1a}]'
```

### Internet & NAT Gateway
```bash
# Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID

# NAT Gateway (in public subnet)
EIP_ID=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
NAT_ID=$(aws ec2 create-nat-gateway \
  --subnet-id $PUBLIC_SUBNET_ID \
  --allocation-id $EIP_ID \
  --query 'NatGateway.NatGatewayId' --output text)
```

## Route Tables

### Public Route Table
```bash
# Route to Internet Gateway
aws ec2 create-route \
  --route-table-id $PUBLIC_RT_ID \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id $IGW_ID
```

### Private Route Table
```bash
# Route to NAT Gateway
aws ec2 create-route \
  --route-table-id $PRIVATE_RT_ID \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id $NAT_ID
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| No internet (public) | Missing IGW route | Add 0.0.0.0/0 → IGW |
| No internet (private) | Missing NAT route | Add 0.0.0.0/0 → NAT |
| Cross-VPC failure | Peering route missing | Add peer CIDR route |
| DNS not resolving | DNS disabled | Enable DNS hostnames |

### Debug Checklist
- [ ] VPC has IGW attached?
- [ ] Public subnets route to IGW?
- [ ] NAT Gateway in public subnet?
- [ ] Private subnets route to NAT?
- [ ] Security groups allow traffic?
- [ ] NACLs not blocking?
- [ ] DNS resolution enabled?

### Connectivity Test
```bash
# From EC2 in private subnet
curl -I https://aws.amazon.com  # Tests NAT/internet
nslookup amazonaws.com           # Tests DNS
telnet rds-endpoint 3306         # Tests internal
```

## Security Best Practices

1. **Subnet Isolation**: Separate public/private/data tiers
2. **Least Privilege NACLs**: Explicit allow rules only
3. **VPC Flow Logs**: Enable for security analysis
4. **No Public IPs**: Private subnets by default
5. **VPC Endpoints**: Use for AWS services

## Test Template

```python
def test_vpc_creation():
    # Arrange
    cidr = "10.99.0.0/16"

    # Act
    vpc = ec2.create_vpc(CidrBlock=cidr)
    vpc_id = vpc['Vpc']['VpcId']

    # Assert
    assert vpc['Vpc']['CidrBlock'] == cidr
    assert vpc['Vpc']['State'] == 'available'

    # Cleanup
    ec2.delete_vpc(VpcId=vpc_id)
```

## Assets

- `assets/vpc-diagram.yaml` - VPC architecture diagram

## References

- [VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [VPC Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
