---
name: fedramp
description: "CR26（FedRAMP 2026 年合并规则）下 FedRAMP 认证与合规的专家指引。当用户询问 FedRAMP 授权、ATO（运营授权）、联邦政府云安全、NIST SP 800-53 控制、CSP 合规，或任何核心 FedRAMP 文档类型：SSP、SAP、SAR、POA&M、CIS/CRM 工作簿时，使用本技能。以下问题同样触发：FedRAMP 认证类别（A、B、C、D——新基线标签：A = 试点/过渡，B = LI-SaaS/Low，C = Moderate，D = High，依据 NTC-0004）、FedRAMP 20x（现为主要授权路径）、OSCAL 强制要求（2026 年 9 月）、3PAO 评估、持续监控（ConMon）、差距评估、系统边界界定或联邦云架构审查。FedRAMP Ready 于 2026 年 7 月 28 日退役。不确定时使用本技能——它涵盖从就绪度到持续监控的完整 FedRAMP 生命周期。"
---

# FedRAMP 认证技能

> **最后核实：** 2026-07-03

一份帮助用户驾驭 FedRAMP 授权——从初始就绪度到 ATO 和持续监控——的全面指南。

## 快速参考：用户需要什么？

识别用户的目标并跳转到相应章节：

| 用户目标 | 前往 |
|---|---|
| "Are we ready for FedRAMP?" / 差距评估 | → [就绪度与差距评估](#1-readiness--gap-assessment) |
| 撰写 SSP、POA&M、SAR、SAP 或其他文档 | → [ATO 文档](#2-ato-documentation) |
| "哪些控制适用于我们？" / 控制映射 | → [NIST 800-53 控制映射](#3-nist-800-53-control-mapping) |
| 云架构 / AWS/Azure/GCP 配置 | → [架构指引](#4-architecture-guidance) |
| 已授权，持续合规 | → [持续监控](#5-continuous-monitoring) |

---

## 当前 FedRAMP 状态（截至 2026 年 7 月——CR26）

> ⚠️ **CR26（FedRAMP 2026 年合并规则）**：FedRAMP 已重构其授权框架。基于 FIPS 199 的基线标签（Low/Moderate/High/LI-SaaS）被**认证类别 A–D** 取代（依据通知 NTC-0004；CR26 规则有效期至 2028 年 12 月 31 日）。类别标签改变了基线的*名称*，而非其要求。已在旧标签下获得授权的 CSP 通过新旧标签关联的过渡期保留其授权。

- **基线**：NIST SP 800-53 **Rev 5**（全面生效）
- **控制数量**（Rev 5）：Low ≈ 156、Moderate = 323、High = 421（传统引用；CR26 基于类别的数量由 PMO 发布）
- **CR26 认证类别**（官方映射，NTC-0004）：**A** = 新的试点/过渡基线（通过项目认证经外部框架如 SOC 2 Type II 进入；持证者有两年来获得 B/C/D 的窗口期），**B** = 现行 **LI-SaaS + Low** 基线，**C** = 现行 **Moderate** 基线（大多数联邦部署，含 CUI），**D** = 现行 **High** 基线。
- **FedRAMP 20x**：现为**主要授权路径**——持续授权、模块化 API 驱动提交、自动化证据收集。传统 SSP/SAP/SAR 模板保留用于传统路径。
- **FedRAMP Ready** 指定：**2026 年 7 月 28 日退役**。当前处于 FedRAMP Ready 状态的 CSP 必须过渡到 FedRAMP 20x 或启动完整授权包。不再颁发新的 FedRAMP Ready 指定。
- **JAB P-ATO**：完全暂停；FedRAMP PMO 是唯一授权机构。
- **OSCAL 强制要求**：RFC-0024 要求所有 CSP 在 **2026 年 9 月 30 日**前提交机器可读的 OSCAL 包。
- **Security Inbox**：所有已授权 CSP 必须维护专用的 Security Inbox（无验证码或障碍）以接收紧急漏洞指令——自 2026 年 1 月 5 日起生效。
- **关键模板已更新**：SSP、SAR、SAP、POA&M、CIS/CRM、IIW、ISCP——全部更新为与 Rev 5 一致（2024 年 12 月发布版）。

---

## 1. 就绪度与差距评估

### 方法
1. **澄清范围** —— 询问用户：CSO（云服务产品）是什么？IaaS/PaaS/SaaS？CR26 下的目标认证类别？
2. **识别授权路径** —— FedRAMP 20x（主要、首选）对比传统机构授权包（复杂系统在 CR26 过渡期间仍可用）
3. **走完就绪度清单** —— 见 `references/readiness-checklist.md`
4. **呈现差距** —— 将当前状态映射到所需控制；标记缺失文档、未实施控制和架构缺陷
5. **排序** —— 按以下分组： (a) 就绪度审查的障碍、(b) 3PAO 评估前可解决的事项、(c) POA&M 候选

> **FedRAMP Ready 将于 2026 年 7 月 28 日退役。** 如果 CSP 当前正在追求 FedRAMP Ready，建议立即转向 FedRAMP 20x 或开始完整授权包。

### 要询问用户的关键就绪度问题
- 您的目标是 FedRAMP 20x（首选）还是传统授权包？
- 使用什么云平台（AWS GovCloud、Azure Government、GCP、本地混合）？
- 您是否利用任何现有的 FedRAMP 授权 IaaS/PaaS（例如 AWS GovCloud FedRAMP High）？
- 您是否已部署经 FIPS 140-2/3 验证的加密？
- 您的授权边界是否已定义并记录？
- 您是否有漏洞扫描项目（操作系统、数据库、Web 应用、容器）？
- 安全政策和程序是否已记录？
- 您是否有经测试的事件响应计划（IRP）和应急计划（CP）？
- 您的授权包工件是否采用 OSCAL 格式（2026 年 9 月 30 日前强制）？

### 输出格式
- 产出**差距表**：控制族 | 当前状态 | 差距 | 优先级 | 责任人
- 以散文概括前 5-10 项高优先级差距
- 注明目标认证类别以及 FedRAMP 20x 是否可行

---

## 2. ATO 文档

核心 FedRAMP 授权包由以下组成：

```
Authorization Package
├── System Security Plan (SSP) + Appendices A–Q
├── Security Assessment Plan (SAP) + Appendices A–D  [3PAO-prepared]
├── Security Assessment Report (SAR) + Appendices A–F  [3PAO-prepared]
└── Plan of Action & Milestones (POA&M)  [SSP Appendix O]
```

> **重要**：CSP 必须使用官方 FedRAMP PMO 模板。OSCAL 格式提交在 2026 年 9 月 30 日前为强制。
> 模板：https://www.fedramp.gov/documents-templates/

### 文档指引

对每种文档类型的详细指引，阅读相应的参考文件：

- **SSP** → `references/ssp-guide.md`
- **POA&M** → `references/poam-guide.md`
- **SAP / SAR** → `references/sap-sar-guide.md`
- **支持性附录** → `references/appendices-guide.md`

### 所有 ATO 文档的通用写作原则
1. **只描述已实施的内容** —— 不要记录计划中的或理想的控制；这些会触发发现，且应放入 POA&M
2. **具体** —— 引用确切的工具、文件名、章节号、策略名称；含糊语言会导致发现
3. **注意动词** —— 每项控制要求使用特定动词（跟踪、记录、执行、测试）。显式处理每个动词
4. **共担责任** —— 对任何客户可配置或共担的控制，创建清晰的"客户责任"章节
5. **保持一致** —— 架构图、数据流、清单和控制陈述必须全部内部一致

---

## 3. NIST 800-53 控制映射

### 控制族（Rev 5）

| ID | 族 | 备注 |
|---|---|---|
| AC | 访问控制 | IAM、RBAC、最小权限、远程访问 |
| AT | 意识与培训 | 安全 + **隐私**培训（Rev 5 新增） |
| AU | 审计与问责 | 日志保留、SIEM、审计审查 |
| CA | 评估、授权与监控 | ConMon、3PAO、ATO |
| CM | 配置管理 | 基线、变更控制、CMDB |
| CP | 应急计划 | BCP/DR、每年测试 |
| IA | 识别与认证 | MFA、PIV、FIPS 140-2/3 加密 |
| IR | 事件响应 | IRP、每年测试、报告 SLA |
| MA | 维护 | 远程维护控制 |
| MP | 介质保护 | 静态数据、介质清除 |
| PE | 物理与环境 | 数据中心；通常从 IaaS 继承 |
| PL | 规划 | SSP、行为规则 |
| PM | 项目管理 | 企业级安全项目 |
| PS | 人员安全 | 审查、离职程序 |
| PT | PII 处理与透明度 | **Rev 5 新增族** —— 隐私控制 |
| RA | 风险评估 | 漏洞扫描、MITRE ATT&CK 评分 |
| SA | 系统与服务获取 | SDLC、供应链 |
| SC | 系统与通信保护 | 传输加密、网络分段 |
| SI | 系统与信息完整性 | 补丁、恶意软件、完整性监控 |
| SR | 供应链风险管理 | **Rev 5 新增族** —— SCRM |

### CR26 认证类别映射

在 CR26 下，FedRAMP PMO 正在将控制基线对齐到认证类别。当用户描述其系统时，映射到某类别：

- **类别 A**（试点/过渡）：20x 下引入的新基线——通过外部框架（最初为 SOC 2 Type II）经项目认证进入联邦市场；类别 A 持证者有**两年的窗口期**通过全面评估获得 B、C 或 D 类认证
- **类别 B**（取代 LI-SaaS + Low）：处理非敏感联邦信息的系统，违规只会造成有限损害
- **类别 C**（取代 Moderate）：最常见——大多数联邦云部署，包括处理 CUI 的系统
- **类别 D**（取代 High）：泄露会产生严重或灾难性影响的联邦信息（例如执法、金融、健康数据）

> **传统引用**：许多现有 FedRAMP 文档仍引用 Low/Moderate/High/LI-SaaS。它们映射为 **LI-SaaS/Low → 类别 B、Moderate → 类别 C、High → 类别 D**（类别 A 是新的——没有传统对应物）。在 CR26 过渡期间，新旧标签关联。建议 CSP 查看 fedramp.gov 获取最新信息。

### 映射工作流
1. 询问：系统将处理/存储/传输哪些类型的联邦数据？
2. 确定 CR26 下的目标认证类别（A、B、C 或 D）
3. 使用类别映射选择 NIST 800-53 Rev 5 基线（B ↔ Low、C ↔ Moderate、D ↔ High）
4. 交叉引用 FedRAMP 参数要求（FedRAMP 通常设定比基础 NIST 更严格的参数）
5. 对继承的控制，识别哪些从利用的 FedRAMP IaaS/PaaS 完全/部分继承，并在 CIS/CRM 工作簿中记录

### 需强调的 Rev 4 → Rev 5 关键变更
- **新控制族**：PT（隐私）、SR（供应链）
- **密码控制修订**：不再有强制轮换时间表；要求泄露密码清单和密码强度计（NIST 800-63b 对齐）
- **隐私整合**：AT-3 现在强制隐私培训；许多族有隐私特定增强
- **基于威胁的方法论**：MITRE ATT&CK 框架为控制优先级提供依据

---

## 4. 架构指引

### 授权边界
边界定义了 FedRAMP 范围内包含什么。这是最常见的发现和延误来源之一。

关键原则：
- **所有处理、存储或传输联邦数据的组件**必须在边界内
- 连接到范围内系统的外部服务必须经 FedRAMP 授权**或**以补偿控制记录
- 边界必须在清晰的**网络/数据流图**中描绘（SSP 必需）

### 云平台考虑

**AWS GovCloud (US)**
- AWS GovCloud 已获 FedRAMP High 授权——大多数 PE 和部分 SC 控制完全继承
- 使用 AWS Config、CloudTrail、GuardDuty、Security Hub 满足 AU、RA、SI 控制
- 确保使用 GovCloud 区域端点（而非标准商业端点）以保持在边界内
- IA 控制有 FIPS 端点可用

**Azure Government**
- Azure Government 已获 FedRAMP High 授权
- Azure Policy + Defender for Cloud 与 CM、RA、SI 映射良好
- 使用对齐 FedRAMP Moderate/High 的 Azure Blueprints / Policy Initiatives

**Google Cloud（FedRAMP 授权区域）**
- Assured Workloads 用于 FedRAMP 合规
- Chronicle SIEM 用于 AU 控制

### 支持 FedRAMP 的架构模式
- **零信任** —— 与 AC、IA、SC 控制族直接对齐
- **不可变基础设施** —— 简化 CM（配置漂移是常见发现）
- **集中式日志记录** —— SIEM/日志聚合全面处理 AU 族
- **自动化漏洞扫描** —— 必需；必须覆盖操作系统、数据库、Web 应用和容器（如使用）
- **OSCAL 原生工具** —— 现在投资；OSCAL 提交在 2026 年 9 月 30 日强制

### 常见架构发现
- 未记录的离开边界的外部连接
- 传输或静态数据中的不合规 FIPS 加密算法
- 过宽的 IAM 角色 / 缺乏最小权限
- 特权账户缺少 MFA
- 漏洞扫描未覆盖所有边界组件
- 日志缺口（并非所有组件都向集中式 SIEM 发送日志）
- 授权包在 2026 年 9 月强制要求前未采用 OSCAL 格式

---

## 5. 持续监控

授权后，CSP 必须通过 ConMon 活动维持合规：

### 月度要求
- 漏洞扫描结果提交给机构 AO
- POA&M 更新（未结发现、整改进展）
- 清单更新（新增/移除资产）
- ConMon 月度执行摘要（模板于 2024 年 11 月更新）

### 年度要求
- 使用年度评估控制选择工作表由 3PAO 进行完整安全评估
- 更新的 SSP 和附录
- 经测试的 IRP 和 CP
- SAR 和更新的 POA&M

### POA&M 管理
- 所有未结发现必须包含：风险等级、责任人、里程碑日期、整改计划
- 供应商依赖（VD）：发现依赖第三方修复时——记录并跟踪
- 偏差请求（DR）：误报和风险调整需要 AO 批准
- 整改 SLA（FedRAMP ConMon 绩效管理指南）：自识别起 **High = 30 天**、**Moderate = 90 天**、**Low = 180 天**。在 Critical 与 High 区分之处（例如扫描器评级），将其视为 High 或更严格（≤30 天，立即优先处理）

---

## 输出格式指南

将输出格式与请求类型匹配：

| 请求类型 | 首选格式 |
|---|---|
| 差距评估 | 表格 + 散文摘要 |
| SSP 控制叙述 | 散文段落（每项控制/增强一段） |
| POA&M 条目 | 含所有必需字段的结构化表格行 |
| 架构审查 | 要点发现 + 建议整改 |
| 控制映射问题 | 表格：控制 ID \| 要求 \| 如何实施 |
| 就绪度概览 | 执行摘要散文 + 优先行动清单 |

生成文档内容时，始终注明：*"Use official FedRAMP templates from fedramp.gov — this content should be inserted into the appropriate template section."*

---

## 参考文件

需要更多深度时加载这些文件：

- `references/readiness-checklist.md` —— 完整就绪度清单（75+ 项）
- `references/ssp-guide.md` —— SSP 逐节写作指南
- `references/poam-guide.md` —— POA&M 结构、字段定义、SLA 表
- `references/sap-sar-guide.md` —— SAP/SAR 概览和 CSP 审查技巧
- `references/appendices-guide.md` —— 所有 SSP 附录（A–Q）指南
- `references/control-families.md` —— 20 个控制族中每一个的深入介绍

---

> *本技能提供一般合规信息，不构成法律意见。对照官方来源核实现行要求；对决策咨询合格律师或经认可的评估员。*
