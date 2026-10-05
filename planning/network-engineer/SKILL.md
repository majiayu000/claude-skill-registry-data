---
name: network-engineer
description: Network engineering expertise for designing and troubleshooting modern network architectures. Use when configuring VPCs, subnets, and routing tables.
---

# Network Engineer

Specialized expertise in network architecture and operations across cloud and hybrid environments, providing guidance on VPC design, DNS architecture, load balancing, network security, troubleshooting methodology, service mesh networking, and CDN/edge networking.

## When to Use This Skill

Use this skill for:

- Designing VPC layouts with proper CIDR planning and subnet tiers
- Configuring DNS resolution, failover routing, and service discovery
- Selecting and configuring load balancers (ALB, NLB, GLB)
- Implementing network security with security groups, NACLs, WAF, and DDoS protection
- Troubleshooting connectivity issues using TCP/IP layer analysis
- Designing service mesh networking with Envoy, mTLS, and traffic management
- Configuring CDN and edge networking for global content delivery

**Trigger phrases**: "VPC design", "subnet layout", "CIDR planning", "DNS routing", "load balancer", "security group", "NACL", "WAF", "traceroute", "packet capture", "service mesh", "CDN", "CloudFront", "network troubleshooting", "VPN", "Direct Connect", "transit gateway"

## What This Skill Does

Provides production-ready network patterns including:

- **VPC Design**: Multi-AZ subnet tiers, CIDR allocation, peering, transit gateway
- **DNS Architecture**: Route 53 patterns, failover, latency-based routing, DNSSEC
- **Load Balancing**: ALB/NLB/GLB selection, health checks, weighted routing
- **Network Security**: Defense in depth with SGs, NACLs, WAF, Shield, zero-trust
- **Troubleshooting**: Systematic layer-by-layer diagnosis with practical CLI tools
- **Service Mesh**: Envoy, mTLS, traffic splitting, fault injection, observability
- **CDN/Edge**: Cache strategies, origin shield, edge functions, HTTP/3

## Instructions

### Step 1: Design VPC and Subnet Architecture

**CIDR Planning Principles**:

Plan your IP address space before creating any resources. Use RFC 1918 private ranges and leave room for growth. A common mistake is allocating overlapping CIDRs across VPCs, which prevents peering and transit gateway connectivity later.

| Range | Total IPs | Typical Use |
|-------|-----------|-------------|
| `10.0.0.0/8` | 16.7M | Enterprise backbone (subdivide into /16 per VPC) |
| `172.16.0.0/12` | 1M | Secondary environments, staging |
| `192.168.0.0/16` | 65K | Small VPCs, development |

**Three-Tier Subnet Layout (Multi-AZ)**:

```
                    ┌──────────────────────────────────────────────────────────┐
                    │                  VPC: 10.0.0.0/16                        │
                    │                                                          │
                    │   AZ-a              AZ-b              AZ-c              │
                    │  ┌──────────┐     ┌──────────┐     ┌──────────┐        │
                    │  │ Public   │     │ Public   │     │ Public   │        │
                    │  │10.0.1/24│     │10.0.2/24│     │10.0.3/24│        │
                    │  │ NAT GW  │     │ NAT GW  │     │ NAT GW  │        │
                    │  │ ALB     │     │ ALB     │     │ ALB     │        │
                    │  └────┬─────┘     └────┬─────┘     └────┬─────┘        │
                    │       │                │                │               │
                    │  ┌────▼─────┐     ┌────▼─────┐     ┌────▼─────┐        │
                    │  │ Private  │     │ Private  │     │ Private  │        │
                    │  │10.0.11/24│    │10.0.12/24│    │10.0.13/24│       │
                    │  │ App Tier │     │ App Tier │     │ App Tier │        │
                    │  │ ECS/EKS │     │ ECS/EKS │     │ ECS/EKS │        │
                    │  └────┬─────┘     └────┬─────┘     └────┬─────┘        │
                    │       │                │                │               │
                    │  ┌────▼─────┐     ┌────▼─────┐     ┌────▼─────┐        │
                    │  │ Isolated │     │ Isolated │     │ Isolated │        │
                    │  │10.0.21/24│    │10.0.22/24│    │10.0.23/24│       │
                    │  │ RDS     │     │ RDS     │     │ RDS     │        │
                    │  │ No IGW  │     │ No IGW  │     │ No IGW  │        │
                    │  └──────────┘     └──────────┘     └──────────┘        │
                    └──────────────────────────────────────────────────────────┘
```

- **Public subnets**: Internet Gateway attached, NAT Gateways, ALB nodes, bastion hosts
- **Private subnets**: Application workloads with outbound internet via NAT Gateway
- **Isolated subnets**: Databases, caches with no route to the internet (only VPC endpoints)

**VPC Terraform Configuration**:

```hcl
# VPC with DNS support and IPv6
resource "aws_vpc" "main" {
  cidr_block                       = "10.0.0.0/16"
  enable_dns_hostnames             = true
  enable_dns_support               = true
  assign_generated_ipv6_cidr_block = true

  tags = { Name = "production-vpc" }
}

# Public subnets across three AZs
resource "aws_subnet" "public" {
  count                           = 3
  vpc_id                          = aws_vpc.main.id
  cidr_block                      = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 1)
  ipv6_cidr_block                 = cidrsubnet(aws_vpc.main.ipv6_cidr_block, 8, count.index + 1)
  availability_zone               = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch         = true
  assign_ipv6_address_on_creation = true

  tags = { Name = "public-${count.index + 1}", Tier = "public" }
}

# Private subnets (application tier)
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 11)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "private-${count.index + 1}", Tier = "private" }
}

# Isolated subnets (database tier, no NAT route)
resource "aws_subnet" "isolated" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 21)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "isolated-${count.index + 1}", Tier = "isolated" }
}

# NAT Gateway per AZ for high availability
resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = { Name = "nat-${count.index + 1}" }
}
```

**Transit Gateway for Multi-VPC Connectivity**:

```
                         ┌─────────────────────┐
                         │   Transit Gateway    │
                         │   (Hub)              │
                         └──┬──────┬──────┬────┘
                            │      │      │
               ┌────────────┘      │      └────────────┐
               │                   │                    │
        ┌──────▼──────┐    ┌──────▼──────┐     ┌───────▼─────┐
        │ Production  │    │  Staging    │     │  Shared     │
        │ VPC         │    │  VPC        │     │  Services   │
        │ 10.1.0.0/16 │    │ 10.2.0.0/16│     │  10.0.0.0/16│
        └─────────────┘    └─────────────┘     └─────────────┘
```

Use Transit Gateway instead of VPC peering when you have more than two or three VPCs. Transit Gateway supports transitive routing, centralized route management, and inter-region peering. VPC peering is simpler but creates a full mesh that becomes unmanageable at scale.

**IPv6 Dual-Stack Considerations**:

- Enable `assign_generated_ipv6_cidr_block` on the VPC for automatic /56 allocation
- Add IPv6 CIDR blocks to each subnet (/64 per subnet)
- Use egress-only internet gateways for IPv6 outbound from private subnets (replaces NAT for IPv6)
- Update security groups and NACLs to include IPv6 rules
- Not all AWS services support IPv6; verify compatibility before enabling dual-stack on application subnets

### Step 2: Architect DNS Solutions

**Route 53 Routing Policies**:

| Policy | Use Case | How It Works |
|--------|----------|--------------|
| **Simple** | Single resource | Returns one or more values at random |
| **Weighted** | A/B testing, blue-green | Distributes traffic by weight percentage |
| **Latency** | Global users | Routes to the lowest-latency region |
| **Failover** | Active-passive DR | Health-checked primary with standby secondary |
| **Geolocation** | Compliance, localization | Routes by user continent/country |
| **Multi-value** | Simple load distribution | Returns up to 8 healthy records |

**Split-Horizon DNS Configuration**:

Split-horizon DNS returns different answers depending on whether the query originates from inside or outside your network. This is critical for hybrid environments where internal services should resolve to private IPs internally and public IPs externally.

```hcl
# Private hosted zone (resolves inside VPC)
resource "aws_route53_zone" "private" {
  name = "app.example.com"

  vpc {
    vpc_id = aws_vpc.main.id
  }
}

resource "aws_route53_record" "api_private" {
  zone_id = aws_route53_zone.private.zone_id
  name    = "api.app.example.com"
  type    = "A"
  ttl     = 60
  records = ["10.0.11.50"]  # Private IP
}

# Public hosted zone (resolves from internet)
resource "aws_route53_zone" "public" {
  name = "app.example.com"
}

resource "aws_route53_record" "api_public" {
  zone_id = aws_route53_zone.public.zone_id
  name    = "api.app.example.com"
  type    = "A"

  alias {
    name                   = aws_lb.api.dns_name
    zone_id                = aws_lb.api.zone_id
    evaluate_target_health = true
  }
}
```

**Failover Routing with Health Checks**:

```hcl
resource "aws_route53_health_check" "primary" {
  fqdn              = "api-primary.example.com"
  port               = 443
  type               = "HTTPS"
  resource_path      = "/health"
  failure_threshold  = 3
  request_interval   = 10

  tags = { Name = "primary-health-check" }
}

resource "aws_route53_record" "api_primary" {
  zone_id = aws_route53_zone.public.zone_id
  name    = "api.example.com"
  type    = "A"

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier  = "primary"
  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "api_secondary" {
  zone_id = aws_route53_zone.public.zone_id
  name    = "api.example.com"
  type    = "A"

  alias {
    name                   = aws_lb.secondary.dns_name
    zone_id                = aws_lb.secondary.zone_id
    evaluate_target_health = true
  }

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "secondary"
}
```

**Service Discovery with Cloud Map**:

```hcl
resource "aws_service_discovery_private_dns_namespace" "main" {
  name        = "internal.local"
  description = "Service discovery namespace"
  vpc         = aws_vpc.main.id
}

resource "aws_service_discovery_service" "api" {
  name = "api"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}
```

ECS and Kubernetes services register automatically with Cloud Map, enabling DNS-based service discovery at `api.internal.local` without external service registries.

**DNSSEC**: Enable DNSSEC signing on Route 53 public hosted zones to protect against DNS spoofing. Create a KMS key with the `SIGN_VERIFY` usage and `ECC_NIST_P256` spec, then enable DNSSEC signing on the zone. Establish a chain of trust by adding a DS record to the parent zone (your domain registrar).

### Step 3: Configure Load Balancing

**Load Balancer Selection Guide**:

| Feature | ALB (Layer 7) | NLB (Layer 4) | GLB (Layer 3) |
|---------|---------------|----------------|----------------|
| **Protocol** | HTTP, HTTPS, gRPC, WebSocket | TCP, UDP, TLS | IP (GENEVE encapsulation) |
| **Latency** | ~400ms added | ~100us added | ~100us added |
| **Static IP** | No (use Global Accelerator) | Yes, Elastic IP per AZ | Yes |
| **Use case** | Web apps, APIs, microservices | High throughput, gaming, IoT | Firewalls, IDS/IPS, DPI |
| **TLS termination** | Yes (with ACM certs) | Yes (passthrough or terminate) | No |
| **Target types** | Instance, IP, Lambda | Instance, IP, ALB | Instance, IP |

**ALB with Path-Based Routing and gRPC**:

```hcl
resource "aws_lb" "main" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_cross_zone_load_balancing = true
  enable_deletion_protection       = true
  drop_invalid_header_fields       = true

  access_logs {
    bucket  = aws_s3_bucket.alb_logs.id
    prefix  = "alb"
    enabled = true
  }
}

# HTTPS listener with default action
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# Path-based routing: /api/* to API service
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern { values = ["/api/*"] }
  }
}

# gRPC target group
resource "aws_lb_target_group" "grpc" {
  name             = "grpc-targets"
  port             = 50051
  protocol         = "HTTP"
  protocol_version = "GRPC"
  vpc_id           = aws_vpc.main.id
  target_type      = "ip"

  health_check {
    enabled             = true
    path                = "/grpc.health.v1.Health/Check"
    protocol            = "HTTP"
    matcher             = "0"  # gRPC status OK
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}
```

**Health Check Best Practices**:

- Use a dedicated `/health` endpoint that checks downstream dependencies (database, cache, external APIs)
- Set `healthy_threshold` to 2 and `unhealthy_threshold` to 3 for a balance between speed and stability
- Use `interval` of 10-15 seconds; shorter intervals increase cost and load
- For gRPC services, implement the gRPC Health Checking Protocol and set matcher to "0" (OK status)
- Enable cross-zone load balancing to distribute traffic evenly when AZ capacity is asymmetric

**Weighted Target Groups for Canary Deployments**:

```hcl
resource "aws_lb_listener_rule" "canary" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 50

  action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.stable.arn
        weight = 90
      }
      target_group {
        arn    = aws_lb_target_group.canary.arn
        weight = 10
      }

      stickiness {
        enabled  = true
        duration = 3600
      }
    }
  }

  condition {
    path_pattern { values = ["/*"] }
  }
}
```

### Step 4: Implement Network Security

**Defense in Depth Model**:

```
Internet
    │
    ▼
┌──────────────┐
│  AWS Shield  │  ← DDoS protection (L3/L4)
│  (Advanced)  │
└──────┬───────┘
       │
┌──────▼───────┐
│     WAF      │  ← L7 filtering (SQL injection, XSS, rate limiting)
└──────┬───────┘
       │
┌──────▼───────┐
│    NACLs     │  ← Stateless subnet-level rules (L3/L4)
└──────┬───────┘
       │
┌──────▼───────┐
│  Security    │  ← Stateful instance-level rules (L3/L4)
│  Groups      │
└──────┬───────┘
       │
┌──────▼───────┐
│  Application │  ← App-level auth, TLS, input validation
└──────────────┘
```

**Security Groups vs NACLs**:

| Aspect | Security Groups | NACLs |
|--------|----------------|-------|
| **Level** | Instance/ENI | Subnet |
| **State** | Stateful (return traffic auto-allowed) | Stateless (must allow both directions) |
| **Rules** | Allow only | Allow and Deny |
| **Evaluation** | All rules evaluated | Rules evaluated in order by number |
| **Default** | Deny all inbound, allow all outbound | Allow all inbound and outbound |

```hcl
# Security group: application tier
resource "aws_security_group" "app" {
  name_prefix = "app-"
  vpc_id      = aws_vpc.main.id
  description = "Application tier - accepts traffic from ALB only"

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "HTTP from ALB"
  }

  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.db.id]
    description     = "PostgreSQL to database tier"
  }

  egress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    prefix_list_ids = [aws_vpc_endpoint.s3.prefix_list_id]
    description     = "HTTPS to S3 via VPC endpoint"
  }
}

# NACL: isolated subnet (database tier)
resource "aws_network_acl" "isolated" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.isolated[*].id

  # Allow inbound PostgreSQL from private subnets only
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.11.0/24"
    from_port  = 5432
    to_port    = 5432
  }

  ingress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.12.0/24"
    from_port  = 5432
    to_port    = 5432
  }

  ingress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.13.0/24"
    from_port  = 5432
    to_port    = 5432
  }

  # Allow ephemeral return traffic
  ingress {
    rule_no    = 200
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.0.0/16"
    from_port  = 1024
    to_port    = 65535
  }

  # Deny all other inbound
  ingress {
    rule_no    = 999
    protocol   = "-1"
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  # Allow outbound ephemeral ports to private subnets
  egress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.0.0/16"
    from_port  = 1024
    to_port    = 65535
  }

  egress {
    rule_no    = 999
    protocol   = "-1"
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }
}
```

**WAF Rules for Common Attacks**:

```hcl
resource "aws_wafv2_web_acl" "main" {
  name        = "app-waf"
  scope       = "REGIONAL"
  description = "WAF for application ALB"

  default_action { allow {} }

  # AWS Managed Rules: Common Rule Set
  rule {
    name     = "aws-managed-common"
    priority = 1
    override_action { none {} }

    statement {
      managed_rule_group_statement {
        vendor_name = "AWS"
        name        = "AWSManagedRulesCommonRuleSet"
      }
    }

    visibility_config {
      sampled_requests_enabled   = true
      cloudwatch_metrics_enabled = true
      metric_name                = "aws-common-rules"
    }
  }

  # Rate limiting
  rule {
    name     = "rate-limit"
    priority = 2
    action { block {} }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      sampled_requests_enabled   = true
      cloudwatch_metrics_enabled = true
      metric_name                = "rate-limit"
    }
  }

  visibility_config {
    sampled_requests_enabled   = true
    cloudwatch_metrics_enabled = true
    metric_name                = "app-waf"
  }
}
```

**VPN and Direct Connect**:

- **Site-to-Site VPN**: Encrypted tunnel over the internet. Use for quick connectivity with up to 1.25 Gbps per tunnel. Deploy two tunnels per connection for redundancy. Combine with Transit Gateway for hub-and-spoke topology.
- **Direct Connect**: Dedicated physical connection (1 Gbps or 10 Gbps). Use when you need consistent latency, high throughput, or reduced data transfer costs. Always pair with a VPN backup for failover.
- **Zero-Trust Network Architecture**: Replace perimeter-based security with identity-verified, least-privilege access at every hop. Use AWS Verified Access or Google BeyondCorp for application-level access without VPN. Combine with mTLS between services and short-lived certificates from a private CA.

### Step 5: Apply Troubleshooting Methodology

**TCP/IP Layer Diagnosis Model**:

When troubleshooting connectivity issues, work from the bottom of the stack upward. Most network problems are at Layer 3 (routing) or Layer 4 (firewall/security group rules).

| Layer | What to Check | Tools |
|-------|--------------|-------|
| **L1 Physical** | Cable, NIC, ENI status | `ethtool`, AWS console (ENI status) |
| **L2 Data Link** | ARP, MAC table, VLAN | `arp -a`, `ip link show` |
| **L3 Network** | IP addressing, routing | `ip route`, `traceroute`, `mtr` |
| **L4 Transport** | Ports, firewalls, SGs | `ss -tlnp`, `telnet`, `nmap`, VPC Flow Logs |
| **L7 Application** | HTTP status, TLS, DNS | `curl -v`, `dig`, `openssl s_client` |

**Essential CLI Commands**:

```bash
# DNS resolution check
dig +short api.example.com
dig @8.8.8.8 api.example.com    # bypass local resolver
dig +trace api.example.com       # full delegation chain

# Path analysis with MTR (combines ping and traceroute)
mtr --report --report-cycles=10 api.example.com

# TCP connectivity test
nc -zv api.example.com 443       # quick port check
curl -v --connect-timeout 5 https://api.example.com/health

# Packet capture for deep analysis
tcpdump -i eth0 -nn host 10.0.11.50 and port 5432 -w capture.pcap
tcpdump -i any -nn 'tcp[tcpflags] & (tcp-syn|tcp-rst) != 0'  # SYN and RST only

# TLS certificate inspection
openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject

# Network socket analysis
ss -tlnp          # listening TCP sockets with process info
ss -s             # socket summary statistics

# MTU path discovery (detect MTU black holes)
ping -M do -s 1472 api.example.com   # 1472 + 28 byte header = 1500
tracepath api.example.com             # discovers MTU along the path
```

**VPC Flow Logs Analysis**:

Enable VPC Flow Logs on all production VPCs. Use the following query in CloudWatch Logs Insights to find rejected traffic (the most common indicator of security group or NACL misconfiguration):

```
fields @timestamp, srcAddr, dstAddr, srcPort, dstPort, protocol, action
| filter action = "REJECT"
| sort @timestamp desc
| limit 50
```

To find traffic patterns for a specific destination:

```
fields @timestamp, srcAddr, dstPort, packets, bytes, action
| filter dstAddr = "10.0.11.50"
| stats sum(bytes) as totalBytes, count(*) as flowCount by srcAddr, dstPort, action
| sort totalBytes desc
```

**Common Failure Patterns**:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Connection timeout | Security group missing inbound rule | Add inbound rule for the source SG or CIDR |
| Connection refused | Service not listening on port | Check service status, verify port binding |
| Intermittent drops | Asymmetric routing or NAT table exhaustion | Check route tables, scale NAT Gateways |
| TLS handshake failure | Certificate mismatch or expired cert | Verify SNI, check ACM certificate status |
| DNS resolution failure | Wrong VPC DHCP options, missing private zone | Verify DHCP option set, check zone VPC association |
| Path MTU black hole | Jumbo frames across VPN or internet | Set `DF` bit and reduce MSS; use `tracepath` to find the bottleneck |

### Step 6: Design Service Mesh Networking

**Service Mesh Architecture**:

```
                    ┌──────────────────────────────────────────────┐
                    │              Control Plane                    │
                    │   ┌─────────┐  ┌──────────┐  ┌──────────┐  │
                    │   │  Istiod │  │  Cert    │  │  Config  │  │
                    │   │ (Pilot) │  │  Manager │  │  Store   │  │
                    │   └────┬────┘  └─────┬────┘  └────┬─────┘  │
                    └────────┼─────────────┼────────────┼─────────┘
                             │  xDS API    │  mTLS      │
                    ┌────────┼─────────────┼────────────┼─────────┐
                    │        │  Data Plane  │            │         │
                    │  ┌─────▼───────────────────────────▼──────┐  │
                    │  │  Pod A                                 │  │
                    │  │  ┌─────────┐    ┌──────────────────┐   │  │
                    │  │  │  App    │◄──►│  Envoy Sidecar   │   │  │
                    │  │  │Container│    │  (L7 Proxy)      │   │  │
                    │  │  └─────────┘    └────────┬─────────┘   │  │
                    │  └──────────────────────────┼─────────────┘  │
                    │                             │ mTLS           │
                    │  ┌──────────────────────────▼─────────────┐  │
                    │  │  Pod B                                 │  │
                    │  │  ┌─────────┐    ┌──────────────────┐   │  │
                    │  │  │  App    │◄──►│  Envoy Sidecar   │   │  │
                    │  │  │Container│    │  (L7 Proxy)      │   │  │
                    │  │  └─────────┘    └──────────────────┘   │  │
                    │  └────────────────────────────────────────┘  │
                    └──────────────────────────────────────────────┘
```

**Sidecar vs Ambient Mesh**:

| Aspect | Sidecar (Traditional) | Ambient Mesh (Istio 1.18+) |
|--------|----------------------|---------------------------|
| **Proxy** | One Envoy per pod | Shared ztunnel (L4) + optional waypoint (L7) |
| **Resource cost** | High (memory per sidecar) | Lower (shared infrastructure) |
| **mTLS** | Per-pod termination | ztunnel handles L4 mTLS |
| **L7 features** | Always available | Only when waypoint proxy deployed |
| **Adoption** | Requires pod restart for injection | No restart needed |

**Traffic Splitting for Canary Releases**:

```yaml
# Istio VirtualService: 90/10 traffic split
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-service
spec:
  hosts:
    - api.internal.local
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: api-service
            subset: canary
    - route:
        - destination:
            host: api-service
            subset: stable
          weight: 90
        - destination:
            host: api-service
            subset: canary
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx,reset,connect-failure
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-service
spec:
  host: api-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        maxRequestsPerConnection: 1000
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

**Fault Injection for Resilience Testing**:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment.internal.local
  http:
    - fault:
        delay:
          percentage:
            value: 10
          fixedDelay: 3s
        abort:
          percentage:
            value: 5
          httpStatus: 503
      route:
        - destination:
            host: payment-service
```

This injects a 3-second delay into 10% of requests and returns HTTP 503 for 5% of requests, allowing you to verify that upstream services handle degraded dependencies gracefully with timeouts, retries, and circuit breakers.

**Observability with Distributed Tracing**: Deploy Jaeger or Zipkin alongside the service mesh. Envoy automatically generates trace spans for each request hop. Ensure your application code propagates trace headers (`x-request-id`, `x-b3-traceid`, `x-b3-spanid`, `traceparent`) so that spans are stitched into complete traces across services.

### Step 7: Configure CDN and Edge Networking

**CloudFront Distribution Architecture**:

```
Users (Global)
    │
    ▼
┌──────────────────┐
│  Edge Locations  │  ← 400+ PoPs worldwide
│  (Cache + TLS)   │
└────────┬─────────┘
         │ Cache miss
┌────────▼─────────┐
│  Regional Edge   │  ← Mid-tier cache (13 locations)
│  Cache           │
└────────┬─────────┘
         │ Cache miss
┌────────▼─────────┐
│  Origin Shield   │  ← Single cache layer before origin (optional)
│  (1 location)    │
└────────┬─────────┘
         │ Cache miss
┌────────▼─────────┐
│  Origin Server   │  ← ALB, S3, or custom origin
└──────────────────┘
```

**CloudFront Terraform Configuration**:

```hcl
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http3"
  price_class         = "PriceClass_100"  # US, Canada, Europe only
  aliases             = ["cdn.example.com"]
  default_root_object = "index.html"

  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "alb-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
      origin_read_timeout    = 30
    }

    origin_shield {
      enabled              = true
      origin_shield_region = "us-east-1"
    }
  }

  # Static assets: aggressive caching
  ordered_cache_behavior {
    path_pattern     = "/static/*"
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "alb-origin"
    compress         = true

    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 86400
    default_ttl            = 604800    # 7 days
    max_ttl                = 31536000  # 1 year
  }

  # API: no caching, pass all headers
  ordered_cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "alb-origin"
    compress         = true

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Origin", "Accept"]
      cookies { forward = "all" }
    }

    viewer_protocol_policy = "https-only"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
  }

  # Default behavior
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "alb-origin"
    compress         = true

    forwarded_values {
      query_string = true
      cookies { forward = "none" }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.cdn.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }
}
```

**Cache Invalidation Strategies**:

| Strategy | When to Use | How |
|----------|------------|-----|
| **Versioned URLs** | Static assets (JS, CSS, images) | Include content hash in filename: `app.a1b2c3.js` |
| **Path invalidation** | Emergency content updates | `aws cloudfront create-invalidation --paths "/page/*"` |
| **TTL tuning** | API responses, dynamic content | Set `Cache-Control: max-age=60, s-maxage=300` |
| **Stale-while-revalidate** | Balance freshness and performance | `Cache-Control: max-age=60, stale-while-revalidate=300` |

Versioned URLs are always preferred over path invalidation. Invalidation requests cost money (first 1,000/month free, then $0.005 each) and take time to propagate. Versioned URLs give instant cache busting with zero cost.

**Edge Functions (CloudFront Functions vs Lambda@Edge)**:

| Feature | CloudFront Functions | Lambda@Edge |
|---------|---------------------|-------------|
| **Runtime** | JavaScript (ES 5.1) | Node.js, Python |
| **Execution time** | < 1ms | Up to 30s (origin events) |
| **Memory** | 2 MB | 128-10240 MB |
| **Network access** | No | Yes |
| **Use cases** | URL rewrites, header manipulation, simple auth | A/B testing, image optimization, SSR |
| **Cost** | $0.10/million | $0.60/million + duration |

```javascript
// CloudFront Function: Add security headers
function handler(event) {
    var response = event.response;
    var headers = response.headers;

    headers['strict-transport-security'] = { value: 'max-age=63072000; includeSubDomains; preload' };
    headers['x-content-type-options']    = { value: 'nosniff' };
    headers['x-frame-options']           = { value: 'DENY' };
    headers['x-xss-protection']          = { value: '1; mode=block' };
    headers['referrer-policy']           = { value: 'strict-origin-when-cross-origin' };

    return response;
}
```

**WebSocket Support**: ALB natively supports WebSocket connections (upgrade from HTTP). CloudFront supports WebSocket via the `wss://` protocol when the origin supports it. Set the origin protocol policy to `https-only` and ensure the cache behavior forwards the `Upgrade`, `Sec-WebSocket-Key`, `Sec-WebSocket-Version`, and `Sec-WebSocket-Protocol` headers.

**HTTP/3 and QUIC**: Enable HTTP/3 on CloudFront distributions with `http_version = "http3"`. QUIC reduces connection establishment latency (0-RTT), handles packet loss better than TCP, and supports connection migration (seamless handoff when a mobile user switches from Wi-Fi to cellular). HTTP/3 is backward-compatible; clients that do not support QUIC fall back to HTTP/2 automatically.

## Best Practices

- **Plan CIDR allocation upfront**: Overlapping address spaces prevent peering and transit gateway connectivity. Document all allocations in a central IPAM tool.
- **Use three AZs minimum**: Two AZs is not enough for production. A single AZ failure with two-AZ deployment leaves you at 50% capacity, while three-AZ deployment retains 66%.
- **Automate DNS with IaC**: Manual DNS changes are the leading cause of outages. Manage all records through Terraform or CloudFormation.
- **Layer your defenses**: Never rely on a single security control. Combine WAF, security groups, NACLs, and application-level validation.
- **Enable flow logs everywhere**: They cost very little and are invaluable during incident response. Send them to S3 for long-term retention and CloudWatch for real-time queries.
- **Monitor certificate expiry**: Use ACM for automatic renewal where possible. For non-ACM certificates, set CloudWatch alarms at 30 and 7 days before expiry.
- **Test failover regularly**: DNS failover, AZ failover, and region failover should be tested quarterly. Untested failover is not failover.
- **Use origin shield**: For high-traffic distributions, origin shield reduces origin load by 50-90% by adding a centralized cache tier.
- **Prefer versioned URLs over invalidation**: Content-hash filenames give instant, free cache busting with no propagation delay.
- **Document network topology**: Maintain up-to-date architecture diagrams. Network issues are nearly impossible to diagnose without understanding the topology.

## Common Patterns

### Pattern 1: Hub-and-Spoke with Transit Gateway

```
On-Premises ──VPN──► Transit GW ──► Production VPC
                          │──► Staging VPC
                          │──► Shared Services VPC (DNS, logging, CI/CD)
```

### Pattern 2: Global Application with Latency Routing

```
Route 53 (Latency) ──► US: CloudFront ──► ALB us-east-1
                   ──► EU: CloudFront ──► ALB eu-west-1
                   ──► AP: CloudFront ──► ALB ap-southeast-1
```

### Pattern 3: Zero-Trust Service Connectivity

```
Client ──► Verified Access (identity check) ──► Private ALB ──► App (mTLS mesh)
```

## Quality Checklist

- [ ] CIDR ranges documented and non-overlapping across all VPCs
- [ ] Three-AZ deployment for all production workloads
- [ ] NAT Gateway per AZ (not shared) for high availability
- [ ] Security groups follow least-privilege (no 0.0.0.0/0 ingress)
- [ ] NACLs on isolated subnets deny all except required ports
- [ ] VPC Flow Logs enabled and shipping to S3 and CloudWatch
- [ ] DNS failover health checks configured with appropriate thresholds
- [ ] Load balancer health checks test downstream dependencies
- [ ] WAF rules deployed with AWS Managed Rule Sets at minimum
- [ ] TLS 1.2+ enforced on all listeners and origins
- [ ] CDN configured with origin shield and versioned static assets
- [ ] Network architecture diagram current and accessible

## Related Skills

- `cloud-architect` - Cloud infrastructure design and Well-Architected Framework
- `terraform-specialist` - Infrastructure as Code provisioning
- `kubernetes-expert` - Container orchestration and cluster networking
- `security-review` - Security assessment and compliance

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: AWS networking best practices, cloud-architect skill patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
