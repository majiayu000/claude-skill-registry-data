---
name: java-unit-test
slug: java-unit-test
displayName: Java 开发期测试
description: >-
  Java 开发期测试（纯单元测试）助手——@Mock + @InjectMocks，毫秒级，不起
  Spring Context、不起容器、零测试基础设施。在编写、评审、补全、重构单元
  测试时使用本技能，无论用户是否提到具体框架（unit test / JUnit / Mockito /
  测试用例 / 怎么测 / 测哪些 / 写多少）。
  次级触发信号——代码或 pom 中出现：spring-boot-starter-test、junit-jupiter、
  @Test / @BeforeEach / @ParameterizedTest / @MethodSource、
  assertEquals / assertThrows / assertThat / extracting（AssertJ）、
  @Mock / @InjectMocks / MockitoAnnotations.openMocks、mockStatic /
  MockedStatic、mockito-core；
  用户任务词或痛点出现：只写 happy path、补测试不知道写几个、手写一堆重复
  @Test、多条件分支只测一两种、有状态对象只测正常流转、@MockBean 用于纯单测、
  测够了没 / 写到什么程度算够、等价类 / 边界值 / 决策表 / 状态迁移用例设计。
  核心默认：一个方法四维度必检（正向/反向/边界/异常）、JUnit 5 原生断言为
  默认、栈中立跟随项目既有（JUnit 4/5 均支持）。接口级验证（接口通不通）
  不写测试、不属本技能范围；需要真实依赖断言 / 可重复回归的重型测试
  （Testcontainers / E2E）→ java-integration-test（明示或确认后激活）。
  不适用：切片 / 集成 / 冒烟 / E2E 测试（@SpringBootTest 全量上下文 /
  @WebMvcTest / Testcontainers / REST Assured / WireMock）→
  java-integration-test；性能测试、前端测试。
version: "2.0.0"
last_verified: "2026-08-03"
---

# Java 开发期测试

开发期测试 = **纯单元测试**：`@Mock`+`@InjectMocks`，毫秒级，`mvn test` 秒级跑完——不起 Spring Context、不引 Testcontainers / H2，零测试基础设施。规范分两部分——**A. 设计方法**（等价类/边界值/决策表/状态迁移）保证测得全；**B. 工程默认值与纪律**（断言库/Mock 边界/停止标准）保证每次一样。每条规则含「✗ 错误设计 → ✓ 正确设计」。

> 接口级验证（"接口通不通"）不写测试、不属本技能范围；需要真实依赖断言 / 可重复回归的重型测试 → java-integration-test，明示或确认后激活。

## 三条铁律

1. **设计优先于编码**：先确定"测哪些用例"（等价类/边界值/决策表/状态），再落成 `@Test`。禁止上来就写代码、想到哪测到哪——那是"覆盖率的幻觉"，不是测试设计。
2. **最小充分集**：用等价类合并代表"无穷输入"，用边界值钉住 off-by-one 高发区；穷尽测试不可能，目标是"用最少的用例覆盖最有代表性的输入"。一个方法的有效用例通常在 3~8 个之间。
3. **零基础设施**：纯单测不起 Spring、不引 Testcontainers / H2 / 内嵌库。需要真实依赖才能断言的行为（SQL 实际执行 / 迁移 / 缓存语义）不属单测——→ java-integration-test（激活后）。

## 断言库策略

**默认用 JUnit 原生 `Assertions`（`assertEquals`/`assertThrows`/`assertTrue` 等）。仅当满足以下任一条件时，升级到 AssertJ：**

- **集合内容断言**（断言 list 元素构成/顺序/提取字段）—— AssertJ 的 `containsExactlyInAnyOrder` / `extracting(...)`。
- **字段分组断言**（同一逻辑组的多个字段作为一个整体校验，如坐标 x/y/z、时间窗 start/end）—— AssertJ 的 `extracting(...).containsExactly(...)`。

**其余场景（简单值、抛异常、各列语义独立的逐列断言如表格型 VO）一律 JUnit 原生，不切换。升级标准可机械执行：是否集合？是否同一逻辑组？两条都不是 → 留在原生逐列断言（失败定位准、加列只改一处）。**

- Spring 项目 `spring-boot-starter-test` 已传递 AssertJ，触发条件时直接用；非 Spring 项目首次触发时按 `references/03` §1 引入 `assertj-core`。
- 既有代码已用 AssertJ 的不主动改写；新测试默认 JUnit 原生，触发条件时该测试用 AssertJ，同文件内可混用。

## 快速入门（第一次用，按这条线走）

| 你想做的 | 看这份 | 读多少 |
|---|---|---|
| 不知道测什么 / 测多少 / 测到什么程度算够 | `references/01` 四维度 + 覆盖率立场 + DoD 锚点 | 各前 40 行 |
| 写纯计算/校验 / 多条件组合 / 状态机测试 | `references/02` 设计方法速查 | 按需查 |
| 设计好的用例怎么落代码 / Mock 怎么写 / 栈版本 | `references/03` | 按需查 |

## 第 0 步：探测被测对象（激活时先执行）

读被测方法/类，一次性判断（读不到则问用户，勿分多轮）：

1. **工具栈**：是否 Spring Boot（决定 `spring-boot-starter-test` 一行 vs 逐库坐标）；JUnit 4 还是 5；Mockito 版本（决定 `mockStatic` 能否用）。决策表见 `references/03` §1。
2. **被测对象类型**（决定用哪种设计方法，详见路由表）：纯计算/校验 → 等价类+边界值；多条件组合 → 决策表；有状态对象 → 状态迁移；有外部依赖 → Mock，界定边界。

## 设计方法 → 场景路由

| 被测对象特征 | 用什么方法 | 典型用例数 | 详见 |
|---|---|---|---|
| 任何方法（先读它） | 四维度 + 黑盒优先 | — | `references/01` |
| 纯计算/校验（输入→输出） | 等价类划分 + 边界值 | 3~8 | `references/02` |
| 多条件组合（促销/费率/权限） | 决策表（列数=用例数） | 化简后列数 | `references/02` |
| 有状态对象（状态机） | 状态迁移 | 合法迁移数 + 非法迁移数 | `references/02` |
| **"写到什么程度算够"** | 覆盖率反向校验 + 成本收益 | — | `references/01` |
| 设计好的用例怎么落代码 | JUnit5/Mockito/Parameterized 映射 | — | `references/03` |

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
| S | `@MockBean` 用于纯单元测试 | 纯单测默认 `@Mock`+`@InjectMocks`；**项目既定的 mock 装配模式（如 TestConfig 手写 `@Bean` mock 轻量容器）优先于本默认**——跟随项目，不强加。`@MockBean` 的红线是"用于纯单测起全量 Spring Context" |
| S | `mockStatic` 未包 try-with-resources | `try (MockedStatic<x> m = mockStatic(X.class)) {...}`（不释放会污染同线程其他测试） |
| S | 为跑单测引入 Testcontainers / H2 / 内嵌库 | 纯单测零基础设施；需要真实依赖才能断言的行为 → java-integration-test（激活后） |
| S | 直接采信 AI 一次性生成的"四维度齐全"测试 | 必须人工复核三维度的**真代表性**；异常维度断言**被测契约指定的具体异常类**，勿断言 `RuntimeException`/`Exception` 根父类 |
| A | 测试方法间共享可变状态 | 每个 `@Test` 自包含、可乱序执行 |
| A | 测试名 `test1`/`testMethod` | `should_<期望>_when_<条件>` 或 Given-When-Then |
| A | 一个 `@Test` 塞多个无关断言 | 一个测试一个行为（可多断言但同一关注点） |
| A | 手写一堆重复 `@Test` 仅输入不同 | `@ParameterizedTest`+`@MethodSource` |
| A | JUnit4 `@Before` 与 JUnit5 混用 | 按探测到的 JUnit 版本统一 |
| A | 无断言测试（调一下方法即算"覆盖"） | 每个测试必须有行为断言 |
| A | 反射测私有方法 | 通过公有方法间接测；私有方法复杂到要单测→提取为独立类 |
| A | 测框架胶水（`@Autowired` 能否注入、getter/setter） | 胶水不测；POJO 用 Lombok 不测 |
| A | 一个测试 mock 了 5+ 依赖仍硬测 | 提示被测类违反 SRP，建议拆分而非硬测 |

## Mock 边界

- **只 Mock 外部依赖**（DB / RPC / 时间 / 第三方），**不 Mock 被测对象自身**及其内部协作对象。
- 其余 Mock 纪律（内部 `new` 的依赖、5+ 依赖、`mockStatic` try-with-resources、spy/doReturn）见 S/A 表 + `references/03` §3。

## 使用流程

1. **第 0 步探测**：工具栈 + 被测对象类型。
2. **读对应 reference**：查路由表，设计用例前先读「详见」列。
3. **设计用例**：四维度逐项检视 → 应用对应设计方法 → 最小充分用例集。
4. **落成代码**：按 `references/03` 映射表。
5. **输出前自检 S 级**：尤其"四维度是否齐全""多条件是否画了决策表""有状态对象是否测了非法转移""`new` 的依赖是否被误 mock"。

## 测试完成判定（DoD 锚点）

本节供外部 PR/DoD checklist **直接引用**——回答"这个方法的测试做完了没有"。三条**同时**满足才算最小充分（不是穷尽）。判定陷阱见 `references/01`「三个停止信号」。

- [ ] **四维度齐全**：正向 / 反向 / 边界 / 异常各至少一个代表用例。
- [ ] **分支盲区清零**：被测方法的每个 `if/switch` 分支至少被一个用例走到（JaCoCo 口径下即 Branch 列 Missed = 0，无 JaCoCo 时人工分支清单全勾）。
- [ ] **等价类清单已显式走完**：列出有效/无效等价类清单，逐类打勾（`null`/空串/越界这些无效类最易漏）。

> 三条全勾即判"完成"——开发期不以"还没写集成 / 接口测试"为由继续加测试；重型层（Testcontainers / E2E）由 java-integration-test 在明示或确认后补齐。

> ✗ DoD 写"覆盖率 ≥ 80%" → ✓ DoD 写"四维度齐全 + 分支盲区清零 + 等价类清单已显式走完"。前者把覆盖率当目标，催生凑数测试；后者才是测试设计完整性的判定。

## 版本与范围

- JUnit 5（Jupiter）为主，JDK 8+；JUnit 4 项目的写法差异见 `references/03` §1 栈基线决策表。
- Spring Boot 项目测试依赖一行 `spring-boot-starter-test`；非 Spring 项目逐库坐标见 `references/03` §1。断言默认 JUnit 原生，升级条件见上文"断言库策略"。
- **与 `java-integration-test` 的边界**：本技能 = 纯单测（`@Mock`+`@InjectMocks`，毫秒级，零基础设施，全周期默认）；测试自管真实依赖（Testcontainers、迁移、真实事务传播、E2E、WireMock、契约切片 `@WebMvcTest`/`@JsonTest`）——→ java-integration-test，明示或确认后激活。注解分界：纯单测 `@Mock`（本技能），Spring 测试内 `@MockitoBean`（→ java-integration-test）。
- **不适用**：性能测试、前端测试。
