---
name: 'Network+ Learning Assistant'
description: 'Interactive CompTIA Network+ N10-009 certification study assistant with OSI model training, subnetting practice, protocol analysis, and exam preparation. Use when studying networking concepts, practicing subnetting, reviewing OSI layers, or preparing for Network+ certification exam.'
---

# Network+ Learning Assistant

## Overview

Comprehensive learning assistant for CompTIA Network+ N10-009 certification covering all exam objectives with interactive exercises, visual aids, and exam-style questions.

## Prerequisites

- Basic computer literacy
- Interest in networking concepts
- Access to the learn_comptia_network+ application

## What This Skill Does

1. **OSI Model Training**: Layer-by-layer breakdown with real-world examples
2. **Subnetting Practice**: IPv4/IPv6 subnet calculations with step-by-step solutions
3. **Protocol Analysis**: Deep dive into TCP/IP, DNS, DHCP, and common protocols
4. **Exam Preparation**: Practice questions mapped to exam objectives
5. **Network Troubleshooting**: Systematic methodology using OSI model

---

## Quick Start

### Study Session

```bash
# Start a focused study session on any topic
"Help me understand [topic]"

# Topics available:
# - OSI Model layers and protocols
# - TCP/IP fundamentals
# - Subnetting and CIDR notation
# - Network topologies
# - Wireless networking (802.11)
# - Network security concepts
# - Cloud networking
# - Network appliances and devices
```

### Practice Mode

```bash
# Generate practice questions
"Give me 5 practice questions about [topic]"

# Subnetting practice
"Create a subnetting exercise for a /24 network"

# Troubleshooting scenarios
"Give me a network troubleshooting scenario"
```

---

## Exam Objectives Coverage

### Domain 1: Networking Concepts (23%)

- OSI and TCP/IP models
- Network topologies
- Cloud concepts and connectivity
- Common ports and protocols

### Domain 2: Network Implementation (19%)

- Routing technologies
- Switching features
- Wireless standards
- WAN technologies

### Domain 3: Network Operations (16%)

- Documentation and diagrams
- Monitoring and metrics
- Remote access methods
- Policies and best practices

### Domain 4: Network Security (19%)

- Security concepts
- Attack types
- Hardening techniques
- Remote access security

### Domain 5: Network Troubleshooting (23%)

- Troubleshooting methodology
- Cable connectivity issues
- Network service issues
- Performance issues

---

## Learning Modules

### OSI Model Deep Dive

```
Layer 7 - Application    : HTTP, HTTPS, FTP, SMTP, DNS, DHCP
Layer 6 - Presentation   : SSL/TLS, JPEG, GIF, encryption
Layer 5 - Session        : NetBIOS, RPC, session management
Layer 4 - Transport      : TCP, UDP, port numbers
Layer 3 - Network        : IP, ICMP, routers, routing
Layer 2 - Data Link      : Ethernet, MAC addresses, switches
Layer 1 - Physical       : Cables, hubs, physical media
```

### Common Ports Reference

```
Port 20/21  - FTP (data/control)
Port 22     - SSH/SFTP
Port 23     - Telnet
Port 25     - SMTP
Port 53     - DNS
Port 67/68  - DHCP
Port 80     - HTTP
Port 110    - POP3
Port 143    - IMAP
Port 443    - HTTPS
Port 3389   - RDP
```

### Subnetting Quick Reference

```
/8   = 255.0.0.0       = 16,777,214 hosts
/16  = 255.255.0.0     = 65,534 hosts
/24  = 255.255.255.0   = 254 hosts
/25  = 255.255.255.128 = 126 hosts
/26  = 255.255.255.192 = 62 hosts
/27  = 255.255.255.224 = 30 hosts
/28  = 255.255.255.240 = 14 hosts
/29  = 255.255.255.248 = 6 hosts
/30  = 255.255.255.252 = 2 hosts
```

---

## Study Strategies

### Effective Learning Techniques

1. **Active Recall**: Test yourself frequently
2. **Spaced Repetition**: Review material at increasing intervals
3. **Hands-On Practice**: Use simulators and labs
4. **Teach Others**: Explain concepts to solidify understanding
5. **Practice Tests**: Take full-length practice exams

### Exam Day Tips

- Get adequate sleep the night before
- Arrive early to the testing center
- Read each question carefully
- Flag difficult questions and return to them
- Manage your time (90 minutes for ~90 questions)

---

## Troubleshooting Methodology

### 7-Step Process

1. **Identify the problem**: Gather information
2. **Establish theory**: Consider probable causes
3. **Test the theory**: Confirm or eliminate causes
4. **Establish action plan**: Plan resolution steps
5. **Implement solution**: Execute the plan
6. **Verify functionality**: Confirm resolution
7. **Document**: Record findings and actions

### Layer-by-Layer Troubleshooting

```
Start at Physical (Layer 1):
├── Check cables and connections
├── Verify link lights
└── Test with known-good equipment

Move to Data Link (Layer 2):
├── Check MAC address table
├── Verify VLAN configuration
└── Test switch port settings

Continue up the stack...
```

---

## Interactive Features

### Terminal Simulator Commands

```bash
# Available in the learning platform
ping <host>           # Test connectivity
traceroute <host>     # Trace packet path
nslookup <domain>     # DNS lookup
ipconfig / ifconfig   # View IP configuration
netstat               # Network statistics
arp -a                # ARP table
```

### Practice Scenarios

The platform includes:

- Network design challenges
- Troubleshooting simulations
- Configuration exercises
- Real-world case studies

---

## Resources

### Application Components

- `/src/components/osi/` - OSI model visualizations
- `/src/components/ipv4/` - IPv4 subnetting tools
- `/src/components/protocols/` - Protocol deep dives
- `/src/components/assessment/` - Practice tests
- `/src/components/topologies/` - Network diagrams

### Related Documentation

- See `docs/` directory for architecture details
- Review `README.md` for application overview

---

**Exam Version**: N10-009 (Current)
**Passing Score**: 720 (on 100-900 scale)
**Questions**: Up to 90
**Time Limit**: 90 minutes
**Question Types**: Multiple choice, drag-and-drop, performance-based
