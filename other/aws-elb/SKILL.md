---




name: aws-elb
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Configures Elastic Load Balancing (ALB, NLB, Classic) for distributing"
  traffic across instances with health checks, SSL termination, and cross-AZ failover.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-cloudwatch, aws-ec2, aws-route53, aws-vpc
  role: reference
  scope: infrastructure
  triggers: elb, load balancer, alb, nlb, application load balancer, health check,
    ssl termination, traffic distribution
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




# Elastic Load Balancing (ELB)

Distribute traffic across EC2 instances with health checks, SSL/TLS termination, and automatic failover for high availability and scalability.

## TL;DR Checklist

- [ ] Use Application Load Balancer (ALB) for HTTP/HTTPS (most common)
- [ ] Use Network Load Balancer (NLB) for extreme performance (millions of RPS)
- [ ] Distribute targets across multiple AZs for high availability
- [ ] Configure health checks with appropriate thresholds
- [ ] Use sticky sessions only for stateful applications
- [ ] Terminate SSL/TLS at load balancer (not instances)
- [ ] Enable connection draining for graceful shutdown
- [ ] Monitor target health and latency metrics
- [ ] Use security groups to restrict ingress to LB only
- [ ] Configure appropriate idle timeout

---

## When to Use

Use ELB when:

- Distributing traffic across EC2 instances
- Requiring SSL/TLS termination
- Building highly available applications
- Needing automatic failover
- Distributing traffic based on hostname or path
- Requiring extreme throughput (NLB)

---

## When NOT to Use

Avoid ELB when:

- Running containers (use service mesh instead)
- No traffic distribution needed
- Very low traffic (cost not justified)

---

## Purpose and Use Cases

**Primary Purpose:** Distribute incoming application traffic across multiple targets with SSL termination, health checks, and automatic failover.

**Common Use Cases:**

1. **Web Application LB** — Distribute HTTP/HTTPS across web servers
2. **API Gateway** — Load balance API servers across instances
3. **High Performance LB** — Extreme throughput with NLB
4. **Multi-tier Application** — Separate LBs for web and app tiers
5. **Global Load Distribution** — AWS Global Accelerator with regional ALBs

---

## Architecture Design Patterns

### Pattern 1: Application Load Balancer for Web Applications

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: web-alb
      Type: application
      Scheme: internet-facing
      IpAddressType: ipv4
      Subnets:
        - subnet-0123456789abcdef0  # Public subnet AZ1
        - subnet-0123456789abcdef1  # Public subnet AZ2
        - subnet-0123456789abcdef2  # Public subnet AZ3
      SecurityGroups:
        - sg-0123456789abcdef0  # ALB security group
      Tags:
        - Key: Name
          Value: web-alb

  # Target Group
  WebTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: web-tg
      Port: 8080
      Protocol: HTTP
      VpcId: vpc-0123456789abcdef0
      HealthCheckEnabled: true
      HealthCheckProtocol: HTTP
      HealthCheckPath: /health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      Matcher:
        HttpCode: 200-299
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: 30
        - Key: stickiness.enabled
          Value: 'false'
        - Key: load_balancing.algorithm.type
          Value: least_outstanding_requests
      Tags:
        - Key: Name
          Value: web-tg

  # HTTP Listener (redirect to HTTPS)
  HTTPListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: redirect
          RedirectConfig:
            Protocol: HTTPS
            Port: '443'
            StatusCode: HTTP_301
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP

  # HTTPS Listener
  HTTPSListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      Certificates:
        - CertificateArn: arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref WebTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      SslPolicy: ELBSecurityPolicy-TLS-1-2-2017-01

  # Host-Based Routing
  HostBasedListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Actions:
        - Type: forward
          TargetGroupArn: !Ref WebTargetGroup
      Conditions:
        - Field: host-header
          Values:
            - example.com
            - www.example.com
      ListenerArn: !Ref HTTPSListener
      Priority: 1

  # Path-Based Routing
  PathBasedListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Actions:
        - Type: forward
          TargetGroupArn: !Ref APITargetGroup
      Conditions:
        - Field: path-pattern
          Values:
            - /api/*
      ListenerArn: !Ref HTTPSListener
      Priority: 2

  # API Target Group
  APITargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: api-tg
      Port: 8000
      Protocol: HTTP
      VpcId: vpc-0123456789abcdef0
      HealthCheckPath: /api/health
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: 60
        - Key: load_balancing.algorithm.type
          Value: least_outstanding_requests

  # Register EC2 Instances (Alternative: Auto Scaling Group)
  # Typically done via Auto Scaling Group with TargetGroupArNs property

  # CloudWatch Alarms
  ALBUnHealthyHostsAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: ALB-Unhealthy-Hosts
      MetricName: UnHealthyHostCount
      Namespace: AWS/ApplicationELB
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      Dimensions:
        - Name: TargetGroup
          Value: !GetAtt WebTargetGroup.TargetGroupFullName
        - Name: LoadBalancer
          Value: !GetAtt ApplicationLoadBalancer.LoadBalancerFullName

  ALBHighLatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: ALB-High-Latency
      MetricName: TargetResponseTime
      Namespace: AWS/ApplicationELB
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 1.0  # 1 second
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: LoadBalancer
          Value: !GetAtt ApplicationLoadBalancer.LoadBalancerFullName

  ALBHTTPErrorsAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: ALB-HTTP-5xx-Errors
      MetricName: HTTPCode_Target_5XX_Count
      Namespace: AWS/ApplicationELB
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: LoadBalancer
          Value: !GetAtt ApplicationLoadBalancer.LoadBalancerFullName

Outputs:
  LoadBalancerDNS:
    Value: !GetAtt ApplicationLoadBalancer.DNSName
    Description: ALB DNS name
  LoadBalancerArn:
    Value: !Ref ApplicationLoadBalancer
    Description: ALB ARN
  TargetGroupArn:
    Value: !Ref WebTargetGroup
    Description: Target group ARN (for ASG)
```

**Key Elements:**
- Application Load Balancer for Layer 7 (application) routing
- HTTP to HTTPS redirect
- SSL/TLS termination at ALB
- Health checks with thresholds
- Host and path-based routing rules
- Deregistration delay for graceful shutdown
- Least outstanding requests algorithm
- CloudWatch alarms for health and performance

### Pattern 2: Network Load Balancer for High Performance

```yaml
Resources:
  # Network Load Balancer
  HighPerformanceLB:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: high-perf-nlb
      Type: network
      Scheme: internet-facing
      IpAddressType: ipv4
      Subnets:
        - subnet-0123456789abcdef0
        - subnet-0123456789abcdef1
        - subnet-0123456789abcdef2
      LoadBalancerAttributes:
        - Key: load_balancing.cross_zone.enabled
          Value: 'true'
      Tags:
        - Key: Name
          Value: high-perf-nlb

  # TCP Target Group
  TCPTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: tcp-tg
      Port: 9000
      Protocol: TCP
      VpcId: vpc-0123456789abcdef0
      HealthCheckEnabled: true
      HealthCheckProtocol: TCP
      HealthCheckIntervalSeconds: 10
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 2
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: 30
        - Key: preserve_client_ip.enabled
          Value: 'true'

  # TCP Listener
  TCPListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref TCPTargetGroup
      LoadBalancerArn: !Ref HighPerformanceLB
      Port: 9000
      Protocol: TCP
```

**Key Elements:**
- Network Load Balancer for extreme performance
- TCP/UDP for low-latency protocols
- Ultra-high throughput (millions of RPS)
- Ultra-low latency (< 100 microseconds)
- Cross-zone load balancing

### Pattern 3: Load Balancer with Security Group Integration

```yaml
Resources:
  # Security group for ALB
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: alb-sg
      GroupDescription: Security group for ALB
      VpcId: vpc-0123456789abcdef0
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP from anywhere
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS from anywhere
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0

  # Security group for targets (restrict to ALB)
  TargetSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: target-sg
      GroupDescription: Security group for ALB targets
      VpcId: vpc-0123456789abcdef0
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref ALBSecurityGroup
          Description: App traffic from ALB
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
```

**Key Elements:**
- ALB in public subnets with public SG
- Target instances in private subnets
- Target SG restricts ingress to ALB only
- Egress allows outbound for database, external APIs

---

## Integration Approaches

### 1. Integration with Auto Scaling Groups

ASG + ALB enables:
- Dynamic registration of targets
- Automatic scaling based on metrics
- Health check integration

### 2. Integration with CloudWatch

ALB + CloudWatch provides:
- Request count and latency metrics
- Target health metrics
- HTTP error rate tracking

### 3. Integration with WAF

WAF + ALB provides:
- Web application firewall rules
- DDoS protection
- SQL injection and XSS prevention

### 4. Integration with Route 53

Route 53 + ALB enables:
- DNS failover to secondary ALB
- Weighted routing policies
- Geolocation routing

---

## Common Pitfalls

### ❌ Pitfall 1: Unhealthy Targets Not Deregistered

**Problem:** Failed instances still receive traffic; user-facing errors.

**Solution:**
- Set appropriate health check thresholds (2 failures = unhealthy)
- Monitor target health in CloudWatch
- Set UnhealthyThresholdCount appropriately

### ❌ Pitfall 2: No Connection Draining

**Problem:** In-flight requests dropped during instance termination.

**Solution:**
- Enable deregistration delay (connection draining)
- Set timeout appropriate for longest request (30-300s)
- Allows graceful shutdown

### ❌ Pitfall 3: Sticky Sessions Overused

**Problem:** Session stickiness can cause uneven load; if target fails, session lost.

**Solution:**
- Enable only for stateful applications
- Prefer stateless design
- Use session store (ElastiCache, RDS)

### ❌ Pitfall 4: Single AZ Deployment

**Problem:** AZ failure causes complete outage; no automatic failover.

**Solution:**
- Always register targets in multiple AZs (minimum 2)
- ALB automatically fails over to healthy targets
- Cross-zone load balancing distributes traffic

### ❌ Pitfall 5: SSL Policy Too Permissive

**Problem:** Weak SSL ciphers expose traffic to interception.

**Solution:**
- Use ELBSecurityPolicy-TLS-1-2-2017-01 or newer
- Disable older protocols (TLS 1.0, 1.1)
- Regular updates to AWS-managed policies

### ❌ Pitfall 6: Not Monitoring Target Health

**Problem:** Silent failures; no alerts when targets become unhealthy.

**Solution:**
- Enable CloudWatch alarms for unhealthy host count
- Monitor HTTP 5xx error rate
- Test health check endpoint regularly

---

## Best Practices Summary

| Category | Best Practice |
|---|---|
| **Type** | ALB for HTTP/HTTPS; NLB for extreme performance |
| **Availability** | Targets in 2+ AZs; health checks enabled |
| **Security** | SSL termination at LB; restrict target SGs to LB |
| **Graceful Shutdown** | Enable connection draining (deregistration delay) |
| **Monitoring** | CloudWatch alarms for health, latency, errors |
| **Sessions** | Use stateless design; session store for state |

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-aws-ec2` | Target instances for load balancing |
| `cncf-aws-auto-scaling` | Dynamic target registration via ASG |
| `cncf-aws-vpc` | Load balancer and target networking |
| `cncf-aws-cloudwatch` | Health and performance monitoring |
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

- [Primary Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/introduction-distributed-load-balancing.html)
- [Configuration Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/elb-security-policy-definitions.html)
- [Best Practices](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/monitoring-elb-load-balancers.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/health-check-overview.html)

