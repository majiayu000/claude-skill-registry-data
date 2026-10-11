---
name: java-integration-test
slug: java-integration-test
displayName: Java 重型测试
description: >-
  Java/Spring Boot 重型测试助手——测试自管真实依赖：Testcontainers 起真实
  PostgreSQL / MySQL / Redis / Kafka、Flyway/Liquibase 迁移可重放、事务传播
  真实效果、冒烟测试、API 级 E2E、WireMock 隔离外部调用、契约切片层
  （@WebMvcTest / @JsonTest / @RestClientTest）。仅当需求明确需要重型 /
  真实环境测试时使用本技能：用户明示（"补集成测试 / 需求冻结 / 准备发版"）
  → 直接开始；仅能推断出需要 → 先询问"是否开始写重型测试"，确认后动手；
  无信号 → 不写，新功能测试 → java-unit-test（纯单测）。核心：消灭仿真测试——可断言、可重复、可版本控制，替代
  curl 调接口 + 肉眼判断；断言真实行为的测试默认 Testcontainers 真实容器
  （不用 H2 替代）。分级：契约切片层（无真实依赖）与真实依赖层（容器）；
  业务分支矩阵永远铺纯单测（→ java-unit-test），容器用例每特性 1~3 条；
  集成测试类名 *IT（mvn verify），不混进 mvn test。
  次级触发信号：功能已稳定要补集成层、用 curl 或手动启动应用调接口"测试"、
  @SpringBootTest 全量上下文测单层 Controller、业务分支矩阵铺进容器测试、
  测试间数据互相污染、@Transactional 回滚失效、测试基础设施待搭建（生产
  PostgreSQL / MySQL / Redis）、测试用 H2 替代生产数据库、外部 API 真调、
  "返回 200 就是通过了"、跑测试太慢（反复全量 / 全文读输出）。
  边界：纯单测（开发期默认层，零基础设施）→
  java-unit-test；前端 E2E（Selenium / Playwright）/ 性能 / 安全 → 不适用。
version: "2.0.0"
last_verified: "2026-08-21"
---

# Java 重型测试（集成 / 冒烟 / E2E）

本技能管理**测试自管依赖**的重型测试——Testcontainers、迁移可重放、真实事务传播、冒烟、E2E、外部依赖 WireMock 隔离，以及功能稳定后补齐的契约切片层。与开发期测试的分界沿**依赖轴**：开发期测试连"内存或本地已运行环境"（→ java-unit-test）；本技能的测试自己拉起并管理真实依赖，CI 无预置环境也可重复跑。核心仍是消灭 curl 仿真测试（无断言 / 不可重复 / 不进版本控制，详见铁律 1 + `references/01`）。每条规则含「✗ 错误做法 → ✓ 正确做法」。

## 激活协议（最优先——未激活不写一个字的重型测试）

| 信号 | 判定 | 动作 |
|---|---|---|
| **明示**：用户说"补集成测试 / 需求冻结 / 特性验收了 / 准备发版 / 要 Testcontainers" | 需求明确要重型 / 真实环境测试 | 直接开始（不再追问） |
| **推断**：特性已稳定 + SQL 密集 + 集成覆盖为零等信号同时出现，但用户没说 | 可能需要，未确认 | **先询问**："是否开始为 X 补重型集成测试？"——确认后动手，拒绝则回到 java-unit-test |
| **无信号**：开发期常规写码 / 新功能开发 | 不需要 | **不写重型测试**；新功能测试 → java-unit-test（纯单测）；存量重型测试照跑照修，不删不新增 |

> 重型测试是十秒级/条的重资产，写在还在变动的行为上 = 需求每变一次连带重写——"测试久过开发"的根源。默认永远从轻（开发期测试），重的东西等人开口。

## 分级

| 层 | 测什么 | 工具 | 详见 |
|---|---|---|---|
| **契约切片层**（无真实依赖） | 单层协议行为：参数校验 / 路由 / 异常处理 / JSON / HTTP 客户端逻辑 / 权限逻辑 | `@WebMvcTest` / `@JsonTest` / `@RestClientTest` | `03` |
| **真实依赖层**（测试自管容器） | 离开真实依赖就不成立的行为：SQL / 方言 / 迁移 / 事务传播 / 缓存语义 / 消息协议；冒烟；E2E | Testcontainers + `@DataJpaTest` / `@SpringBootTest` | `02`+`04`+`07` |

**容器准入判据**（机械化自问——每条容器用例写前过一遍）：**这条断言离开真实 DB / Redis / Kafka 就不成立吗？**
- 成立（→ 容器）：SQL 实际语句与方言特性（`jsonb`/`ARRAY`/`ENUM`）、Flyway / Liquibase 迁移脚本、事务传播实际效果、缓存过期 / 序列化语义、消息协议。
- 不成立（→ 开发期测试 / 切片）：业务规则、多条件分支矩阵、DTO 映射、参数校验、权限逻辑。

**数量锚点**：容器用例每特性 1~3 条锚定真实行为；分支矩阵铺纯单测（→ java-unit-test），不铺切片 / 容器；E2E 全套件 3~10 条（见 `07`）。

**命名分离**（机械保障，`mvn test` 保持轻量）：集成测试类名 **`*IT`**（failsafe，`mvn verify` 跑）；开发期测试 `*Test`（surefire，`mvn test` 跑）。存量集成测试叫 `*Test` 混在 `mvn test` 里 → 建议改名迁移，不强制一次性完成。

## 四条铁律

1. **curl 结果不是测试**：测试必须有结构化断言（HTTP status + response body + jsonPath），而非"看起来返回正常"——curl 调接口 + 肉眼判断不构成测试。
2. **激活才写**：未过激活协议不新增重型测试（存量照跑照修不删）；默认新功能测试 → java-unit-test。
3. **分级准入**：容器层只收「离开真实依赖就不成立」的行为；契约切片层封顶的功能（参数校验 / JSON / 权限逻辑 / HTTP 客户端逻辑）永远不进容器；分支矩阵永远铺纯单测。
4. **隔离优先**：测试间数据不污染。`@Transactional` 回滚（注意失效场景）、Testcontainers 重置、`@Sql` 清理——一个测试的副作用不能影响另一个。

## 快速入门

| 你想做的 | 看这份 | 读多少 |
|---|---|---|
| 确认该不该写重型测试 / 用哪层 | `references/01` 激活协议 + 分级 + curl 反模式 | 各前 40 行 |
| 写 @SpringBootTest / MockMvc / WebTestClient | `references/02` | 通读 |
| 契约切片测试（@WebMvcTest / @JsonTest） | `references/03` | 通读 |
| 用 Testcontainers 起真实依赖 | `references/04` | 通读 |
| 写 API 断言（REST Assured） | `references/05` | 通读 |
| 测试隔离 / @Transactional 失效 / WireMock | `references/06` | 通读 |
| 冒烟测试 / 多接口串联 E2E | `references/07` | 通读 |
| 跑测试烧 token / 反复全量 / 输出太多 / 调度 | `references/08` | 通读 |

## 第 0 步：探测项目与场景（激活时先执行）

读项目 `pom.xml` / `build.gradle` 和测试代码，一次性判断：

1. **激活判定**（最优先）：按「激活协议」表判定——无信号则本技能仅处理存量测试的评审 / 修复，不新增。
2. **工具栈**：
   - Spring Boot 版本（`pom.xml` 读 `spring-boot-starter-parent`）→ 决定 `@ServiceConnection` 可用性（3.1+）、命名空间（`javax.*` vs `jakarta.*`）、HTTP 测试客户端选型（≤3.x：TestRestTemplate 可用；4.x：废弃，用 RestTestClient——见 `references/02`）。
   - 是否已有 `testcontainers` / `rest-assured` / `wiremock` 依赖 → 决定是否需引导引入。
3. **测试场景**（激活后；每条容器用例先过准入判据，再按路由选行）。
4. **curl 检测**：正在用 curl 或手动启动应用调接口"测试"→ **拦截**，落成可断言测试。
5. **真实依赖需求判定**（准入判据通过后）：**默认 Testcontainers**——不取决于项目当前是否已引 H2（没用 H2、测试未搭，同样引入；H2 只是反例，不是触发前提，详见 `04`）。依赖选择（探测生产 → 询问用户）见「使用流程」第 2 步。

## 测试路由（激活后）

| 场景 | 层 | 工具 | 详见 |
|---|---|---|---|
| 单类业务逻辑（含 Service 分支矩阵，调 Repository） | 开发期 | `@Mock`+`@InjectMocks` | → **java-unit-test** |
| Controller 参数校验 / 路由 / 异常处理 / 权限逻辑 | 契约切片 | `@WebMvcTest` + MockMvc | `03` |
| JSON 序列化 / HTTP 客户端调用逻辑 | 契约切片 | `@JsonTest` / `@RestClientTest` | `03` |
| Repository SQL / 查询 / 分页 | 真实依赖 | `@DataJpaTest` + Testcontainers | `03`+`04` |
| 跨层真实协作 / 事务传播验证 | 真实依赖 | `@SpringBootTest(MOCK)` + Testcontainers + `@Transactional` | `02`+`04`+`06` |
| 完整 HTTP API（含过滤器 / 拦截器 / 序列化管道） | 真实依赖 | `@SpringBootTest(RANDOM_PORT)` + REST Assured | `02`+`05` |
| "服务能不能启动"冒烟 | 真实依赖 | `@SpringBootTest` + Actuator health | `07` |
| 多接口串联业务流程（E2E） | 真实依赖 | `@SpringBootTest(RANDOM_PORT)` + REST Assured 多步 | `05`+`07` |
| 外部 HTTP 依赖隔离 | — | WireMock stub | `06` |

> "跨层协作"指验证协作本身（SQL 实际执行 / 事务传播 / 序列化管道）——不是"Service 调了 Repository"（那属纯单测，mock Repository 铺分支矩阵）。

## S 级反模式表（致命——测试存在但测不出问题，或测试拖垮迭代）

> S 级：导致"测试存在但测不出问题"或"测试拖垮迭代"——新测试禁止；审查既有测试命中 → 立即指出补全。

| ✗ 错误做法 | ✓ 正确做法 |
|---|---|
| 业务分支矩阵 / 参数校验写进容器测试 | 分支矩阵铺纯单测（mock Repository，毫秒级，→ java-unit-test）；容器每特性 1~3 条锚定真实行为（准入判据） |
| 用 `curl` 调接口 + 肉眼判断输出 | 用 MockMvc / REST Assured / WebTestClient 写可断言测试（statusCode + body + jsonPath） |
| 手动启动应用再 curl "测试" | `@SpringBootTest(webEnvironment=RANDOM_PORT)` 进程内启动 + 自动断言 |
| 全量 `@SpringBootTest` 测单层 Controller | `@WebMvcTest` 切片——只加载 Web 层，秒级启动 |
| `@Transactional` 回滚用于 `RANDOM_PORT` 场景 | `RANDOM_PORT` 下 HTTP 请求走独立线程，回滚**失效**→ 用 `@Sql` 清理 or Testcontainers 重置（见 `06`） |
| 断言真实行为的测试用 H2 替代生产数据库（无论当前是否已引 H2） | 容器测试**默认** Testcontainers 真实容器——消除方言差异（`jsonb`/`ARRAY`/`SERIAL` 等 H2 不支持）；H2 仅限 CI 无 Docker 降级（见 `04`） |
| 外部 API 真调（第三方支付 / 短信） | WireMock stub——可控、可重复、不产生费用 |
| 无断言测试（调一下接口即算"覆盖"） | 每个测试必须有结构化断言：HTTP status + 响应体字段值 |
| `@DirtiesContext` 每个测试都加 | 只在 Context 状态确实被污染时用——它会重建整个 Spring Context（十秒级），优先 `@Sql` / `@Transactional` |
| 启动日志有 WARN/ERROR 但测试绿 | 日志报错 = 测试失败信号，必须排查——Bean 创建失败、Flyway 迁移失败常被 Mock 遮掩 |

## A 级规则表（约定——约束新生成测试）

| ✗ 错误做法 | ✓ 正确做法 |
|---|---|
| 测试间共享数据，互相污染 | 每个 `@Test` 自包含；`@AfterEach` / `@Sql` 清理 |
| 测试依赖执行顺序 | 可乱序执行（JUnit 5 默认）；不依赖 `@Order` |
| `@MockitoBean` 替换大量 Bean | 每组不同 `@MockitoBean` 组合重建 Context → 测试极慢；统一 mock 配置，或用 `@Import` + `@TestConfiguration` |
| `@DataJpaTest` 默认用 H2 但生产是 PostgreSQL | `@AutoConfigureTestDatabase(replace = NONE)` + Testcontainers（见 `04`） |
| `@WebMvcTest` 不 mock Service 导致启动失败 | `@WebMvcTest` 只加载 Web 层——Service 需 `@MockitoBean` 或 `@Import` |
| REST Assured `RestAssuredMockMvc` 当真实 HTTP 用 | `RestAssuredMockMvc` 走 MockMvc（进程内，无真实 HTTP）；要真实 HTTP 用 `RestAssured` + `RANDOM_PORT`（见 `05`） |
| Testcontainers 容器每个测试方法启停 | `@Container` + `static` → 容器全类共享；或 `testcontainers.reuse.enable=true` 跨类复用 |
| WireMock 固定端口，并行测试端口冲突 | WireMock 随机端口（`options().dynamicPort()`）+ `@DynamicPropertySource` 注入 |
| 集成测试类名用 `*Test` 混进 `mvn test` | 类名 `*IT`（failsafe，`mvn verify` 跑）——`mvn test` 保持开发期轻量套件 |

## 核心强约束（Agent 必须遵守）

1. **激活协议**：未激活不新增重型测试（存量照跑照修，不删）；推断出需要时先询问，确认后动手。激活后按「分级」补齐：容器锚（迁移可跑 + 启动冒烟 + 核心 SQL 1~3 条）→ 契约切片层 → 特性级容器用例 1~3 条。
2. **容器分级准入**：每条容器用例写前自问"断言离开真实依赖就不成立吗"——不成立回开发期测试 / 契约切片。切片封顶清单（参数校验 / JSON / 权限逻辑 / HTTP 客户端逻辑）永远不进容器；容器每特性 1~3 条，分支矩阵不铺容器层。
3. **禁止 curl 测试**：生成测试不得用 `curl` / `httpie` / 手动 HTTP 客户端；必须用 MockMvc / WebTestClient / REST Assured / RestTestClient（Boot 4+）编写含结构化断言的测试。
4. **`@Transactional` 回滚仅限 `MOCK` 模式**：MOCK 有效、`RANDOM_PORT` 失效（根因见 S 级表 + `references/06`），改用 `@Sql(execution=AFTER_TEST_METHOD)` 或 Testcontainers 重置。
5. **真实依赖默认 Testcontainers**：准入判据通过的测试 → **默认**用 Testcontainers 起同款容器——**不取决于项目当前是否已引 H2**。H2 仅限 CI 无 Docker 时的显式降级（见 `references/04` checklist）；方言差异是"测试绿生产炸"头号来源。
6. **外部依赖必须 stub**：调用外部 HTTP API（支付 / 短信 / 第三方认证）必须用 WireMock stub，不得真调。
7. **`@DirtiesContext` 是最后手段**：重建整个 Context（十秒级），仅在 Bean 内部状态被污染且无法用 `@Sql` / `@Transactional` / Testcontainers 重置时才用。
8. **Context 缓存友好**：`@MockitoBean` / `@MockitoSpyBean` / `@SpringBootTest` 属性的组合变化会导致 Context 缓存失效并重建。统一测试的 mock 配置。
9. **执行降噪 + 调度 + 命名分离**：`-B -ntp` + `-q` / logger 级别 + `logging.level.root` 分层降噪，**不全文回传 stdout**；失败读 `target/surefire-reports/*.txt`、`-Dtest` 单测重跑，不反复全量、不每次 `clean`。集成测试 `*IT` + failsafe（`mvn verify`），`mvn test` 只跑开发期套件（调度表见 `references/08` §3）。

## 使用流程

1. **第 0 步探测**：激活判定（最优先）→ 工具栈 → 测试场景 → curl 检测 → 真实依赖需求判定。
2. **依赖选择询问**：涉及真实依赖时——探测生产依赖（驱动 / datasource / docker-compose）→ 给候选版本询问用户（对齐生产优先，推荐值见 `04` §依赖选择）→ 落定后写代码。**不静默选镜像 tag。**
3. **读 `references/01`**：确认激活状态与分层（切片 / 容器）。
4. **定位工具 reference**：按路由表读 `02`-`05` 对应文件。
5. **隔离策略**：读 `references/06`，确定数据清理方案（`@Transactional` / `@Sql` / Testcontainers 重置 / WireMock）。
6. **执行效率**：读 `references/08`——分层调度、降噪输出、`-Dtest` 单测迭代。
7. **输出前自检**：逐项核对下方清单——任一项未过，不得交付。

## 输出前自检清单（交付测试代码前逐项核对，任一未过不得交付）

- [ ] 已过激活协议（用户明示或确认）——未激活时未新增重型用例
- [ ] 每条容器用例过准入判据（断言离开真实依赖就不成立）；每特性 ≤3 条；分支矩阵未铺在容器层
- [ ] 类名 `*IT`（failsafe）——未混进 `mvn test` 开发期套件
- [ ] 无 `curl` / `httpie` / 手动启动应用调接口——测试用 MockMvc / WebTestClient / REST Assured / RestTestClient（Boot 4+）编写
- [ ] 每个测试有结构化断言：HTTP status + 响应体字段值（jsonPath / expectBody）
- [ ] `@Transactional` 回滚仅用于 `MOCK` 模式——`RANDOM_PORT` / `DEFINED_PORT` 场景已改 `@Sql` / Testcontainers 重置
- [ ] 容器测试用 Testcontainers 真实容器——未静默用 H2 替代；镜像版本已探测生产 + 询问用户确认
- [ ] 外部 HTTP 依赖（支付 / 短信 / 三方认证）全部 WireMock stub，无真调
- [ ] 单层协议行为用切片（`@WebMvcTest` / `@JsonTest`），未用全量 `@SpringBootTest` 测单层
- [ ] `@DirtiesContext` 仅在状态无法用 `@Sql` / `@Transactional` / Testcontainers 重置时使用
- [ ] 启动日志无未排查的 WARN / ERROR
- [ ] 依赖坐标与 Boot 版本匹配：Boot 4 → RestTestClient（非 TestRestTemplate）、`@MockitoBean`（非 `@MockBean`，已移除）、`@AutoConfigureMockMvc` 显式标注、Testcontainers 2.x 新模块名（`testcontainers-*`）、rest-assured 手写 6.x；Boot ≤3.x → 旧坐标、BOM 已管的不写 `<version>`（`references/02` / `04` / `05`）

## 版本与范围

- Spring Boot 2.7.x / 3.x / 4.x 均适用；3.1+ 新增 `@ServiceConnection`（Testcontainers 自动连接），3.0 及以下用 `@DynamicPropertySource`。
- **Boot 4 测试工具链变化**：① `TestRestTemplate` 废弃——拆到独立模块 `org.springframework.boot:spring-boot-resttestclient`（test scope），升级 Boot 4 后原注入直接失败；新测试用 `RestTestClient` + `@AutoConfigureRestTestClient`（迁移对照见 `references/02`）。② Testcontainers 跳到 2.x——模块加 `testcontainers-` 前缀（旧名 2.x 下 404）、容器类移独立包且无泛型（对照表见 `references/04`）。③ `@MockBean` / `@SpyBean` **已移除**（编译错误）→ 换 `@MockitoBean` / `@MockitoSpyBean`（Boot 3.4+ 可用；不能声明在 `@Configuration` 类里，见 `references/02`）。④ `@SpringBootTest` 不再自动配置 MockMvc——必须显式 `@AutoConfigureMockMvc`。
- JUnit 版本不手选——由 `spring-boot-starter-test` 传递：Boot ≤3.x = JUnit 5，Boot 4 = JUnit 6。JUnit 4 遗留项目：用 `@RunWith(SpringRunner.class)`，断言用 `org.junit.Assert`，生命周期注解为 `@Before`/`@After`；其余写法与本技能示例一致。
- **与 `java-unit-test` 的边界（依赖轴）**：开发期测试 = 纯单测（`@Mock`+`@InjectMocks`，毫秒级，零基础设施）→ java-unit-test；测试**自管**真实依赖（Testcontainers、迁移、真实事务传播、E2E、WireMock 隔离、契约切片 `@WebMvcTest`/`@JsonTest`）→ 本技能，明示或确认后激活。Context 内替换 Bean 的注解分界：纯单测 `@Mock`，Spring 测试内 `@MockitoBean`（→ 本技能）。
- **不适用**：前端 E2E（Selenium / Playwright / Cypress）、性能测试（JMeter / Gatling）、安全测试。
