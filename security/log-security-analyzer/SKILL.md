---
name: log-security-analyzer
description: Analyze logs for security events and threats
activation_keywords: [security, log, attack, intrusion, brute force, failed login, threat, audit]
execution_mode: server
---

# Log Security Analyzer

Analyzes logs for security threats:
- Failed login attempts detection
- Brute force attack detection
- Unusual access patterns
- Suspicious IP addresses
- Malware detection
- Privilege escalation attempts
- Data exfiltration attempts
- DDoS patterns

Use `builtin_log_security_analyzer` tool with fields:
- `log_text`: the log content to analyze (required)
- `log_type`: (optional) log type (apache, nginx, ssh, systemd, etc.)
- `threat_level`: (optional) sensitivity level (low, medium, high)

Returns detected security events with severity and recommendations.
