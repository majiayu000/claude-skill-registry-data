---
name: java-unit-test
slug: java-unit-test
displayName: Java 单元测试
description: >-
  Java 单元测试**规范对齐**助手。在编写、评审、补全单元测试时使用本技能——
  无论用户是否提到具体框架（unit test / JUnit / Mockito / 测试用例 / 怎么测 /
  测哪些 / 写多少测试）。
  核心：统一团队的测试规范——用同一套设计方法（等价类/边界值/决策表/状态迁移）、
  同一套默认（JUnit 5 原生断言、四维度必检）、同一套"写多少"的停止标准，
  让不同人/不同对话产出的测试质量一致、可溯源、可审计，而非每次碰运气。
  覆盖：一个方法必测的四维度（正向/反向/边界/异常）、最小充分集、
  覆盖率反向校验、测试命名与组织、Mock 边界、"写多少"的成本收益判定。
  次级触发信号：只写 happy path、补测试不知道写几个、手写一堆重复 @Test、
  多条件分支只测一两种、有状态对象只测正常流转、@MockBean 用于纯单测、
  不确定测试该写到什么程度。
  工具默认：断言默认用 JUnit 5 原生 Assertions，仅在集合内容断言/字段分组断言（同一逻辑组）时升级到 AssertJ；
  Spring Boot 项目走 spring-boot-starter-test（自带 JUnit5+Mockito）。
  不适用：集成测试/E2E（@SpringBootTest 全量上下文）、性能测试、前端测试。
version: "1.4.0"
last_verified: "2026-08-03"
---

# Java 单元测试

面向团队的**单元测试规范对齐助手**：统一"测什么、测多少、怎么设计、用什么默认"。规范分两部分——**A. 设计方法**（等价类/边界值/决策表/状态迁移）保证测得全；**B. 工程默认值与纪律**（断言库/Mock 边界/停止标准）保证每次一样。每条规则含「✗ 错误设计 → ✓ 正确设计」。

## 三条铁律

1. **设计优先于编码**：先确定"测哪些用例"（等价类/边界值/决策表/状态），再落成 `@Test`。禁止上来就写代码、想到哪测到哪——那是"覆盖率的幻觉"，不是测试设计。
2. **最小充分集**：用等价类合并代表"无穷输入"，用边界值钉住 off-by-one 高发区；**穷尽测试不可能**，目标是"用最少的用例覆盖最有代表性的输入"。一个方法的有效用例通常在 3~8 个之间，不是越多越好。
3. **栈中立**：测试框架**跟随项目既有**——JUnit 4 还是 5、Spring Boot 还是非 Spring，按项目现状走，不强加、不主动迁移。断言库默认见下方"断言库策略"。

## 断言库策略

**默认用 JUnit 原生 `Assertions`（`assertEquals`/`assertThrows`/`assertTrue` 等）。仅当满足以下任一条件时，升级到 AssertJ：**

- **集合内容断言**（断言 list 元素构成/顺序/提取字段）—— AssertJ 的 `containsExactlyInAnyOrder` / `extracting(...)`。
- **字段分组断言**（同一逻辑组的多个字段作为一个整体校验，如坐标 x/y/z、时间窗 start/end）—— AssertJ 的 `extracting(...).containsExactly(...)`。

**其余场景（简单值、抛异常、各列语义独立的逐列断言如表格型 VO）一律 JUnit 原生，不切换。升级标准可机械执行：是否集合？是否同一逻辑组？两条都不是 → 留在原生逐列断言（失败定位准、加列只改一处）。**

- Spring 项目 `spring-boot-starter-test` 已传递 AssertJ，触发条件时直接用；非 Spring 项目首次触发时按 `references/06` §1 引入 `assertj-core`。
- 既有代码已用 AssertJ 的不主动改写；新测试默认 JUnit 原生，触发条件时该测试用 AssertJ，同文件内可混用。

## 快速入门（第一次用，按这条线走）

| 你想做的 | 看这份 | 读多少 |
|---|---|---|
| 不知道测什么 / 测多少 | `references/01` 四维度 + 「DoD 锚点」三停止信号 | 各前 30 行 |
| 写纯计算/校验方法测试 | `references/02` | 通读（有完整范例） |
| 写多条件组合 / 状态机测试 | `references/03` / `references/04` | 通读 |
| 设计好的用例怎么落代码 / Mock 怎么写 | `references/06` | 按需查 |

> `01` 根文件（设计前必读）；`05` 回答"测到什么程度算够"（含遗留代码补测、覆盖率反向校验）；`06` 工具落地。

## 第 0 步：探测被测对象（激活时先执行）

读被测方法/类，一次性判断（读不到则问用户，勿分多轮）：

1. **工具栈**：是否 Spring Boot（决定 `spring-boot-starter-test` 一行 vs 逐库坐标）；JUnit 4 还是 5（决定 `@Before`/`@BeforeEach`、`Assert`/`Assertions` 写法）；Mockito 版本（决定 `mockStatic` 能否用、是否需 `mockito-inline`，见 06）。三条都用 `grep` 探 `pom.xml`：`grep -E "spring-boot-starter-test|spring-boot-starter-parent"` / `grep -E "junit-jupiter|<artifactId>junit</artifactId>"`（前者命中=JUnit5，后者=JUnit4）/ `grep mockito`。
2. **被测对象类型**（决定用哪种设计方法，详见路由表）：
   - 纯计算/校验方法（输入→输出） → 等价类 + 边界值
   - 多条件组合逻辑（if/else 或规则） → 决策表
   - 有状态对象（订单/审批/支付状态机） → 状态迁移
   - 有外部依赖（DB/RPC/时间） → 需 Mock，界定 Mock 边界

## 设计方法 → 场景路由

> 设计用例前，**先读「详见」列文件**：含该方法的完整设计步骤、用例计数规则与 antipattern，本文仅摘要。

| 被测对象特征 | 用什么方法 | 典型用例数 | 详见 |
|---|---|---|---|
| 任何方法（先读它） | 四维度 + 黑盒优先 | — | `references/01-test-design-foundations.md` |
| 纯计算/校验（输入→输出） | 等价类划分 + 边界值 | 3~6 | `references/02-equivalence-and-boundary.md` |
| 多条件组合（促销/费率/权限） | 决策表（列数=用例数） | 决策表列数 | `references/03-decision-table.md` |
| 有状态对象（状态机） | 状态迁移 | 迁移数 + 非法迁移数 | `references/04-state-transition.md` |
| **"写到什么程度算够"** | 覆盖率反向校验 + 成本收益 + DoD 锚点 | 覆盖率/成本见 05，判定 checklist 见「DoD 锚点」 | `references/05-coverage-and-quantity.md` |
| 设计好的用例怎么落代码 | JUnit5/Mockito/Parameterized 映射 | — | `references/06-tools-lean.md` |

> **每次设计完用例后都应回看下方「测试完成判定（DoD 锚点）」的三个勾选项**（回答"测到什么程度算够"）。

## 每个方法的四维度（必检清单）

任何被测方法，至少回答这四组"有没有测到"——**缺一个维度就是设计漏洞**：

| 维度 | 测什么 | 设计方法 |
|---|---|---|
| **正向** | 合法、正常输入的预期输出 | 等价类有效代表 |
| **反向** | 非法、异常输入的拒绝行为 | 等价类无效代表 → `assertThrows` |
| **边界** | 区间端点、空/null、极值 | 边界值分析（off-by-one 高发区） |
| **异常** | 抛出的业务异常/受检异常路径 | 异常等价类 |

## S/A 规则表（设计层）

- **S 级（设计缺陷级）**：导致"测试存在但测不出 bug"——新测试禁止；审查既有测试命中 → 立即指出补全。
- **A 级（约定）**：约束新生成测试。

| 级别 | ✗ 错误设计 | ✓ 正确设计 |
|---|---|---|
| S | 只写 happy path，缺反向/边界/异常 | 四维度各至少一个代表用例 |
| S | "想到几个写几个"，无等价类/边界分析 | 先划等价类再取代表，边界必取端点 |
| S | 多条件逻辑只测一两种组合 | 画决策表，**列数=用例数**，不漏不重 |
| S | 有状态对象只测正常流转，不测非法/不可达转移 | 状态迁移：每条合法迁移+每个非法转移的拒绝 |
| S | 被测类内部 `new` 的依赖被 mock 掉 | 重构为构造器注入，再 mock 注入的依赖 |
| S | `@MockBean` 用于纯单元测试 | 纯单测默认 `@Mock`+`@InjectMocks`；**项目既定的 mock 装配模式（如 TestConfig 手写 `@Bean` mock 轻量容器）优先于本默认**——跟随项目，不强加 `@InjectMocks`。`@MockBean` 的红线是"用于纯单测起全量 Spring Context"（会重建 Context），切片测试才用它 |
| S | `mockStatic` 未包 try-with-resources | `try (MockedStatic<x> m = mockStatic(X.class)) {...}`（不释放会污染同线程其他测试） |
| S | 直接采信 AI 一次性生成的"四维度齐全"测试 | 必须人工复核三维度的**真代表性**：代表值换一个同区间值期望行为不变（变了说明选错了类）；且至少触发一条与相邻等价类不同的分支。异常维度断言**被测契约指定的具体异常类**（如 `IllegalArgumentException`），勿断言 `RuntimeException`/`Exception` 根父类 |
| A | 测试方法间共享可变状态 | 每个 `@Test` 自包含、可乱序执行 |
| A | 测试名 `test1`/`testMethod` | `should_<期望>_when_<条件>` 或 Given-When-Then |
| A | 一个 `@Test` 塞多个无关断言 | 一个测试一个行为（可多断言但同一关注点） |
| A | 手写一堆重复 `@Test` 仅输入不同 | `@ParameterizedTest`+`@MethodSource` |
| A | JUnit4 `@Before` 与 JUnit5 混用 | 按探测到的 JUnit 版本统一 |
| A | 无断言测试（调一下方法即算"覆盖"） | 每个测试必须有行为断言 |
| A | 反射测私有方法 | 通过公有方法间接测；私有方法复杂到要单测→提取为独立类 |
| A | 测框架胶水（`@Autowired` 能否注入、getter/setter） | 胶水交给集成测试；POJO 用 Lombok 不测 |
| A | 一个测试 mock 了 5+ 依赖仍硬测 | 提示被测类违反 SRP，建议拆分而非硬测 |

## Mock 边界

- **只 Mock 外部依赖**（DB / RPC / 时间 / 第三方），**不 Mock 被测对象自身**及其内部协作对象。
- 其余 Mock 纪律（内部 `new` 的依赖、5+ 依赖、`mockStatic` try-with-resources）见 S/A 表 + `references/06` §3。

## 架构守护询问（仅架构守护缺失时触发）

**触发条件**：用户要求"防止架构腐化/禁止跨层调用/禁止循环依赖"，且项目**无 ArchUnit**；或被测类处于**分层包**（`..web..`/`..service..`/`..repo..`）、且本次单测会**触达跨层依赖**（如 Controller 调 Repository、Service 互相依赖）、项目无 ArchUnit 时——作为次级信号提一次询问。纯计算/校验方法（即便住在分层包里但不碰跨层依赖）**不询问**。

> 判定"项目无 ArchUnit"：第 0 步探测依赖时一并 `grep archunit pom.xml`；有则跳过本节。

- 询问要点（一次问全）：说明 ArchUnit 的价值（编译期/测试期守护分层契约）→ 给坐标 `com.tngtech.archunit:archunit-junit5:1.3.0` → 两个选项：A) 引入并加架构测试；B) 不引入，靠人工 review 守护。
- 选 A 时给两条**可直接复制**的规则（实测一行即可抓 Controller 直连 Repository 等真实高频违规）：

```java
@AnalyzeClasses(packages = "com.xxx")
class ArchitectureTest {
    // web 不得依赖 repo（应通过 service）—— 抓 Controller 直连 Repository
    @ArchTest static final ArchRule webNoRepo =
        noClasses().that().resideInAPackage("..web..")
                   .should().dependOnClassesThat().resideInAPackage("..repo..");
    // 分层不得有环：web → service → repo 单向
    @ArchTest static final ArchRule noCycles =
        slices().matching("com.xxx.(*)..").should().beFreeOfCycles();
}
```

- 用户拒绝 → 不再追问，按普通单测设计继续。

## 使用流程

1. **第 0 步探测**：工具栈 + 被测对象类型，确定本次设计方法与工具基线。
2. **读对应 reference**：查路由表，**设计用例前先读「详见」列**（含完整设计步骤）。
3. **设计用例**：四维度逐项检视 → 应用对应设计方法（等价类/边界值/决策表/状态）→ 得出最小充分用例集。
4. **落成代码**：按 `references/06-tools-lean.md` 把每个用例映射为 `@Test`/`@ParameterizedTest`/`assertThrows`；需 Mock 按上文边界界定。
5. **输出前自检 S 级**：尤其"四维度是否齐全""多条件是否画了决策表""有状态对象是否测了非法转移""`new` 的依赖是否被误 mock"。

## 测试完成判定（DoD 锚点）

本节供外部 PR/DoD checklist **直接引用**——回答"这个方法的测试做完了没有"。三条**同时**满足才算最小充分（不是穷尽）。判定陷阱（"无遗漏"不可绝对证明）见 `references/05-coverage-and-quantity.md`「三个停止信号」。

- [ ] **四维度齐全**：正向 / 反向 / 边界 / 异常各至少一个代表用例（对照上方「每个方法的四维度」表逐项打勾）。
- [ ] **分支覆盖无盲区**：所有 `if/switch` 的每个分支都被至少一个用例走到——`mvn test` 后看 JaCoCo 报告的 Branch 列，红色（`BRANCH_MISSED > 0`）行逐一对照"漏了哪个等价类"再补，或判为死代码。**项目无 JaCoCo 时**：人工核对分支表，或按"成本收益"决定是否接入（接入见 05）。
- [ ] **等价类清单已显式走完**：按 `references/02` 四步法列出有效/无效等价类清单，逐类打勾（`null`/空串/越界这些无效类最易漏）。

> ✗ DoD 写"覆盖率 ≥ 80%" → ✓ DoD 写"四维度齐全 + 分支覆盖无盲区 + 等价类清单已走完"。前者把覆盖率当目标，催生凑数测试；后者才是测试设计完整性的判定。

## 版本与范围

- JUnit 5（Jupiter）为主，JDK 8+；JUnit 4 项目的写法差异见 `references/06-tools-lean.md` §4。
- Spring Boot 项目测试依赖一行 `spring-boot-starter-test`（自带 JUnit5+Mockito）；非 Spring 项目逐库坐标见 `references/06-tools-lean.md` §1。断言默认 JUnit 原生，升级条件见上文"断言库策略"。
- **与 `java-coding-guide-pro` 的关系**：正交互补。guide-pro 的编码高风险域（金额/日期/并发/加密）天然是测试设计的重点——其边界值正是 off-by-one 高发区，设计测试时优先覆盖这些域的边界。（注：guide-pro 用「S 级」标注编码高风险，与本文 S/A 表的「S 级＝测试设计缺陷」是两套体系，勿混。）
