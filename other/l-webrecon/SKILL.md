---
name: l-webrecon
description: "Web/API 的范围确定、低影响探测、权限与数据边界检查"
---

# l-webrecon Local Entry

Scope: authorized pentesting / web security testing / injection / privilege escalation / cloud and domain security (with a URL/target). This skill is a local routing entry; the detailed capabilities live in local modules.

## Selection Rules (avoid mis-picking)
1. First read the "Module List" below.
2. Scan the "Module List" below **top to bottom**; use the first one that matches the current task.
   When multiple capabilities are needed, stack at most 3, with entries higher up taking priority.
3. Read the selected local module from `../<MODULE_ID>/SKILL.md`, then apply its task guidance.
4. When none matches exactly, fall through to the "Fallback" at the bottom of this page.

## Module List (ordered by priority)

- `pentest-tools` — Pentest tools quick reference: common tools and command cheat sheet.
- `pentest-tools__src-hunter` — Source/sensitive-info hunting: gather source code and credential leads in the target.
- `attack-chain` — Attack-chain orchestration: multi-stage planning of recon → initial access → privilege escalation → lateral movement.
- `api-security` — API security testing: assessment of interface auth, broken access control, rate limiting, CI/CD, etc.
- `network-analysis` — Network analysis: packet capture, protocols, traffic forensics.
- `database-security` — Database security: injection, permissions, and configuration-hardening assessment.
- `windows-ad` — Windows domain security: Kerberos, AD CS, domain privilege-escalation research.
- `identity-federation` — Identity federation: analysis of identity systems such as SSO/OAuth/SAML.
- `cloud-k8s` — Cloud and K8s security: assessment of containers, clusters, and cloud credentials.
- `supply-chain-security` — Supply-chain security: assessment of SBOM, dependencies, and build integrity.
- `email-security` — Email security: phishing, SPF/DKIM, and mail-gateway assessment.
- `wifi-wireless` — Wireless security: Wi-Fi capture, handshake analysis, lab deauth.
- `ot-ics` — OT/ICS security: assessment of PLC, SCADA, and industrial protocols.
- `llm-security` — LLM security: assessment of prompt injection, jailbreak, and data leakage.
- `threat-hunting` — Threat hunting: detection rules, SIEM, alert validation (blue team).
- `code-audit` — Code audit: source-level security vulnerability review.
- `api-design` — API design: design guidance for REST/GraphQL interface structure, versioning, and error conventions.
- `deploy-infra` — Deployment and infrastructure: environment setup and ops deployment.
- `jailbreak-engineering` — Jailbreak engineering: prompt-bypass and safety-boundary research (controlled experiments).

## Fallback
When no listed method matches, return to the installed edition's local directory and choose a relevant available module.

## 本版可用模块

| 模块 | 用途 | 正文 |
| --- | --- | --- |
| `pentest-tools` | 为已确定范围的系统选择探测、验证和回归工具 | [读取](../pentest-tools/SKILL.md) |
| `pentest-tools__src-hunter` | 从接口、路由、日志与仓库定位安全问题相关源码 | [读取](../pentest-tools__src-hunter/SKILL.md) |
| `attack-chain` | 将多个已确认问题关联成有证据的影响路径 | [读取](../attack-chain/SKILL.md) |
| `api-security` | 审查接口认证、对象权限、租户隔离和输入处理 | [读取](../api-security/SKILL.md) |
| `network-analysis` | 分析 PCAP、协议会话、异常请求或连接故障 | [读取](../network-analysis/SKILL.md) |
| `database-security` | 检查数据库账户、权限、查询与备份的数据边界 | [读取](../database-security/SKILL.md) |
| `windows-ad` | 审查 AD、Kerberos、NTLM、证书服务与域内权限关系 | [读取](../windows-ad/SKILL.md) |
| `identity-federation` | 审查 SAML/OIDC 的验证、租户绑定和会话边界 | [读取](../identity-federation/SKILL.md) |
| `cloud-k8s` | 检查集群身份、工作负载权限、网络与供应链配置 | [读取](../cloud-k8s/SKILL.md) |
| `supply-chain-security` | 分析依赖来源、构建输入、SBOM 与制品完整性 | [读取](../supply-chain-security/SKILL.md) |
| `email-security` | 分析邮件头、认证配置、样本附件和异常投递 | [读取](../email-security/SKILL.md) |
| `wifi-wireless` | 分析自有无线网络的配置、认证、流量和覆盖问题 | [读取](../wifi-wireless/SKILL.md) |
| `ot-ics` | 审查 ICS、SCADA、PLC 的配置、协议和资产边界 | [读取](../ot-ics/SKILL.md) |
| `llm-security` | 审查提示词注入、工具授权、数据隔离与代理执行边界 | [读取](../llm-security/SKILL.md) |
| `threat-hunting` | 将行为假设转为日志查询、检测规则和可验证线索 | [读取](../threat-hunting/SKILL.md) |
| `code-audit` | 对指定代码路径检查正确性、权限、数据处理与实际缺陷 | [读取](../code-audit/SKILL.md) |
| `api-design` | api-design | [读取](../api-design/SKILL.md) |
| `deploy-infra` | 规划可回滚的部署、配置变更与基础设施迁移 | [读取](../deploy-infra/SKILL.md) |
| `jailbreak-engineering` | jailbreak-engineering | [读取](../jailbreak-engineering/SKILL.md) |
