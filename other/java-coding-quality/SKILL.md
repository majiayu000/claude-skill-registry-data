---
name: java-coding-quality
slug: java-coding-quality
displayName: Java 质量门禁
description: >-
  Java 代码质量与安全的工具化门禁助手。在完成任何 Java / Spring Boot 代码的编写、修改、
  重构后，或用户要求提交前检查、代码写完验证、代码审查 / code review、修复扫描告警、
  质量门禁、静态扫描、安全扫描（SQL 注入 / 弱加密 / 路径穿越 / XXE / SSRF / 硬编码密钥）时使用本技能——
  无论用户是否提到具体工具（PMD / SpotBugs / FindSecBugs / Java 规约 / lint / static analysis）。
  本技能用 JVM 插件链（PMD 7 + 自带规则集、SpotBugs + FindSecBugs）实跑扫描并按严重级修复，
  直到 Blocker/Critical 清零才算交付。
  完成任意 Java 代码任务后建议激活本技能做交付前门禁。
  不适用：非 JVM 语言、纯前端、无 Maven/Gradle 的项目、DDL / 架构设计。
version: "1.5.0"
last_verified: "2026-07-31"
agent_created: true
---

# Java 质量门禁

面向 Java 代码**交付前验证**的工具门禁助手。用 JVM 插件链（PMD 7 + 自带规则集、SpotBugs + FindSecBugs）实跑扫描并按严重级修复，直到 **Blocker/Critical 清零**才算交付。

## 三条铁律

1. **工具兜底，不再造规范**：约束靠实跑的静态扫描（PMD 7 + SpotBugs），不重复堆砌编码规则；发现的告警若属编码手法问题，用本技能 references 速查表修复。
2. **零侵入优先**：默认在项目根建 `.qualitygate/` 包装工程扫描，**项目自身 pom 零改动**；通过一次后才**询问一次**是否持久化进项目 pom，拒绝则不再问。
3. **安全告警不自行豁免**：误报抑制必须附注释理由并经用户确认；FindSecBugs 安全类告警 Agent 一律不得擅自 suppress。

## 工具链

| 层 | 工具 | 坐标（已实跑核实 2026-07） | 作用 |
|---|---|---|---|
| 规范层 | maven-pmd-plugin（PMD 7 内核） | `org.apache.maven.plugins:maven-pmd-plugin:3.27.0`（默认 PMD 7.14.0） | 源码级规范：空 catch、魔法值、命名、线程池、BigDecimal 等 |
| 规则集 | 技能自带 `assets/pmd7-ruleset.xml` | 随技能分发，无外部依赖 | 编码强制项（内置规则调参 + XPath 自定义） |
| bug/安全 | SpotBugs + FindSecBugs | `com.github.spotbugs:spotbugs-maven-plugin:4.9.6.0` + `com.h3xstream.findsecbugs:findsecbugs-plugin:1.14.0` | 字节码级 bug 模式 + 138 类安全漏洞 |

## 第 0 步：环境探测（激活时先执行）

读 `pom.xml` / `build.gradle` 一次性探测（读不到则一次问全，勿分多轮）：

1. **构建工具**：Maven（有 `pom.xml`）还是 Gradle；`mvn -v` / `gradle -v` 是否可用。
2. **目标 JDK**：`maven.compiler.release` / `<source>` / `sourceCompatibility`——决定 PMD 的 `targetJdk` 与编译参数（SpotBugs 需先编译）。
3. **项目是否已配质量插件**：pom/gradle 中是否已有 `maven-pmd-plugin` / `spotbugs-maven-plugin` / `checkstyle` / `sonar`——
   - **已配 → 直接复用项目自己的配置与规则集**，不引入技能默认规则集（尊重团队既有基线）；仅在项目无规则集时才用技能自带的。
   - **未配 → 走「接入方式」用技能自带规则集扫描**。
4. **无 Maven/Gradle 或不可用** → 告知无法实跑门禁，降级为「按 references 做人工对照检查」，并如实说明未做运行时验证。

## 接入方式（零侵入优先）

**默认（零侵入）**：在项目根建 `.qualitygate/` 目录，写入包装 pom + 从技能 `assets/` 拷入 `pmd7-ruleset.xml`；PMD 包装 pom 的 `sourceDirectory` 指向 `../src/main/java`；SpotBugs 包装 pom 用 `<classFilesDirectory>` 指向 `../target/classes`（被检项目须先 `mvn compile`）；把 `.qualitygate/` 追加进 `.gitignore`。**项目自身 pom 全程零改动**。完整模板见 `references/01-setup.md`。

**持久化（询问后）**：`.qualitygate/` 扫描通过一次后，**询问一次**是否把 PMD/SpotBugs 插件片段写入项目 pom（供团队 / CI 共享）；拒绝则保持零侵入、不再问。

## 门禁流程与退出条件

```
编译（SpotBugs 前置）→ PMD 扫描 + SpotBugs(FindSecBugs) 扫描 → 解析报告按严重级归并
→ 修复（Blocker→Critical→Major）→ 复扫 → Blocker/Critical 清零 → 交付
```

- **修复顺序**：Blocker → Critical → Major；**Minor 仅报告不强改**。
- **退出条件**：Blocker 与 Critical **必须清零**才算通过；Major 尽量修，无法修的登记说明。
- **死循环保护**：同一告警连续 2 轮修复仍无法消除 → 停下向用户说明原因并申请豁免，不无限重试。
- 严重级如何从 PMD priority / SpotBugs rank 映射到 Blocker/Critical/Major/Minor，见 `references/04-fix-workflow.md`。

## 误报 / 豁免规则

- 抑制手段（`@SuppressWarnings("PMD.RuleName")` / SpotBugs `@SuppressFBWarnings` / exclude filter）**必须附注释写明理由**且**须用户确认**后才可加。
- **Agent 不得自行豁免安全类告警**（FindSecBugs SECURITY 类别、PMD security 规则）；只能如实上报并给修复建议。
- 判定为误报的标准与各工具的抑制写法见 `references/04-fix-workflow.md`。

## 决策路由表（按需读对应 reference，勿全量加载）

| 需求场景 | 读取文件 | 关键内容 |
|---|---|---|
| 搭建 `.qualitygate/` 包装工程、包装 pom 模板、持久化片段、Gradle 等价配置、多模块适配、适用边界、报告路径 | `references/01-setup.md` | 零侵入包装 pom、`skipPmdError` 容错、报告 XML 解析、多模块/Gradle/测试代码边界 |
| 自带规则集设计说明、规则映射表（含日志/性能/空集合）、XPath 自定义规则清单、高频告警→修复速查、规则集增改维护 | `references/02-pmd-rules.md` | 41 条内置规则 + 2 条 XPath 明细、如何新增一条 XPath 规则 |
| SpotBugs 高频 bug pattern→修复、FindSecBugs 安全规则重点（SQL 注入/弱加密/路径穿越/XXE/SSRF/硬编码密钥/反序列化/XSS/CRLF）→修复 | `references/03-spotbugs-security.md` | NP_/EI_/DM_ 系列 + 安全类，已内联修复 |
| 严重级映射表、修复-复检循环操作、误报判定与抑制写法、批量告警分组修复策略 | `references/04-fix-workflow.md` | priority/rank→四级分级、豁免规范 |

## 使用流程

1. **第 0 步环境探测**：构建工具 + JDK + 是否已配质量插件；已配则复用，未配走技能自带规则集。
2. **接入**：默认建 `.qualitygate/` 零侵入包装工程（读 `references/01-setup.md`）。
3. **实跑扫描**：先编译，再跑 PMD 与 SpotBugs(FindSecBugs)，产出 XML 报告。
4. **按严重级修复**：Blocker→Critical→Major 顺序（读 `references/04-fix-workflow.md` 做分级），修复手法查 `02`/`03` 速查表。
5. **复扫收敛**：直到 Blocker/Critical 清零；同一告警 2 轮不消 → 说明并申请豁免。
6. **询问持久化**：通过后问一次是否把插件写进项目 pom，拒绝则保持零侵入。
