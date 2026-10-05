---
name: cso
description: Security audit skill — systematic OWASP + STRIDE review of a project. Covers attack surface, secrets archaeology, dependency supply chain, OWASP Top 10, threat modeling, and false-positive filtering. Outputs a prioritized findings report.
when_to_use: "security audit, OWASP, vulnerabilities, 安全审计, project-wide security review — NOT the CC built-in /security-review (which reviews a single diff/PR); /cso audits the whole project"
argument-hint: '[path or focus area — default: entire project] [--full]'
user_invocable: true
---
