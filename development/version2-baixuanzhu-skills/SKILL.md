---
name: java-coding-guide-pro
slug: java-coding-guide-pro
displayName: Java 编码指南
description: >-
  Java 编码规范与避坑助手。在编写、修改、重构或审查任何 Java / Spring Boot 代码时使用本技能——
  无论用户是否提到编码规范或具体工具库（Java coding / code review / refactoring /
  best practices / code quality）。
  覆盖：判空与字符串、集合与 Stream、日期时间、文件 IO / HTTP 调用 / JSON 序列化、
  线程池与并发、Bean 拷贝、加密哈希、异常处理与日志、金额与浮点精确运算、
  现代 Java 语法（JDK 8~25，按特性最低版本门控）。
  次级触发信号——代码中出现：SimpleDateFormat、Executors.newFixedThreadPool /
  newCachedThreadPool / newSingleThreadExecutor、new Thread(...)、
  new BigDecimal(0.1) 小数构造、BeanUtils.copyProperties、catch (Throwable) /
  catch (InterruptedException) 空块、MessageDigest（手写 MD5/SHA）、
  log.error("x=" + x) 日志拼接、Optional.get()、subList(...)、
  finally 块内 return / throw、Math.random()、new Random()；
  用户任务词出现：生成订单号 / 流水号 / 唯一 ID、生成验证码 / token / 盐、
  密码加密 / 哈希存储、金额 / 价格计算、线程池 / 异步任务、日期格式化 / 时区。
  跟随项目既有技术栈（Spring / Hutool / commons-lang3 等），不强加任何库。
  不适用：业务架构设计、框架选型、DDL、纯算法、前端代码。
version: "3.5.0"
last_verified: "2026-08-23"
---

# Java 编码指南

面向日常 Java 开发的**编码约定助手**。每条规则「✗ 禁止 → ✓ 推荐」，覆盖 JDK 8~25+（LTS 锚定：8/11/17/21/25）。

## 三条铁律

1. **栈中立**：库的选择**跟随项目既有依赖**，本指南不强加任何库；Spring 项目优先 Spring 生态自带能力（Jackson / RestTemplate / WebClient / SLF4J）。
2. **一域一默认**：每个场景只给唯一推荐（以项目既有栈为准），不列举「或 A 或 B」制造决策疲劳。
3. **版本门控**：先确认目标 JDK，高版本特性按门控使用——JDK 8 项目严禁 `var`/`record`/`switch 表达式`/文本块/`sealed`/`虚拟线程`。

## 第 0 步：栈探测与适配（激活时先执行）

读 `pom.xml` / `build.gradle` 一次性探测（读不到则一次问全，勿分多轮）：

1. **目标 JDK**：`maven.compiler.release` / `<source>` / `sourceCompatibility`；读不到问用户「目标 JDK 版本是（8 / 11 / 17 / 21 / 25）？」。
2. **已有栈**：Spring 系（自带 Jackson/RestTemplate/WebClient/SLF4J）、Hutool、commons-lang3、Guava、Gson/Fastjson、OkHttp、Lombok、MapStruct。
3. **三条适配规则**：
   - 项目**已有**对应能力的库 → **跟随既有库**，不另引、不混用（一个项目一套字符串/集合工具）；仅当既有库缺该能力时补引，并在代码注释标注混用原因。
   - **高风险能力缺失**且任务确实需要（见「风险分级与构件选择」）→ 触发 C-CHECK 询问是否引入。
   - **低风险能力缺失**（判空/集合/随机数/日期等）→ 直接用 JDK 原生，**零打断、不询问**。

## JDK 版本策略

**判据：目标 JDK ≥ 特性最低版本 → 可用；低于 → 禁用，改低版本写法。** 非 LTS 目标同样按版本比较，不另设档位。

| 特性 | 最低 JDK |
|---|---|
| Lambda / 方法引用 / `Optional` / `Stream` / `java.time` / `CompletableFuture` | 8（下限） |
| `var`（仅局部变量） | 10 |
| JDK 内置 `HttpClient` | 11 |
| `switch` 表达式（箭头 / `yield`） | 14 |
| 文本块 `"""` | 15 |
| `record` / `Stream.toList()`（不可变）/ `instanceof` 模式匹配 | 16 |
| `sealed` | 17 |
| 虚拟线程 / `switch` 模式匹配 / `SequencedCollection` | 21 |
| 未命名变量 `_` / Stream Gatherers / Scoped Values（22–24 转正，完整清单见 09） | 25 |

> 22–24 转正特性统一按 25 门控；preview/incubator 不纳入。虚拟线程 + `synchronized` 在 21 会钉住载体线程（改 `ReentrantLock`），25 解除（JEP 491）。完整门控表（含推荐度）见 `references/09-modern-java.md`。

## 风险分级与构件选择

**构件选择顺序**：项目既有库 > JDK 原生 API > 引入新库（引入前触发 C-CHECK）。

- **高风险场景**（手写极易出 bug，**禁手写，必须用成熟构件**；具体推荐见「域 → 默认」表）：加密 / 哈希 / 密码、线程池 / 并发、JSON 解析、Bean 映射、HTTP 调用、金额运算。其中项目缺**加密**或 **Bean 映射**能力时触发 C-CHECK 询问；其余场景 JDK 原生 / Spring 自带即可覆盖，不询问。
- **低风险场景**（零打断）：判空、集合新建 / 分块、随机数、日期格式化——项目有 Hutool / commons-lang3 就用其工具方法，没有就 JDK 原生（`Objects`/`String.isBlank`(11+)/`List.of`(9+)/`ThreadLocalRandom`/`java.time`），不触发任何询问。

## 域 → 默认（项目无既有方案时；已有同类库按第 0 步跟随）

> 生成对应域代码前，**先读「详见」列的 reference 文件**：含该域完整的「✗ 禁止 → ✓ 推荐 → 为什么」规则、API 速查与 antipattern，本文规则表只是其摘要。

| 场景信号 | 无既有方案时的默认 | 详见 |
|---|---|---|
| 判 null / `Optional` 取值 / 相等防 NPE | JDK `Optional`/`Objects`；有 Hutool 用 `StrUtil`/`ObjectUtil` | `references/01-null-and-string.md` |
| 字符串判空/格式化/截取/命名转换 | JDK 原生；有 Hutool 用 `StrUtil` | `references/01-null-and-string.md` |
| 集合判空/新建/分块/交并差 | JDK 原生；有 Hutool 用 `CollUtil` | `references/02-collection-stream.md` |
| 集合分组/转 Map | JDK `Stream`/`Collectors` | `references/02-collection-stream.md` |
| 日期格式化/解析/加减/当前时间 | JDK `java.time`（`.now()` 显式传 ZoneId/Clock）；遗留 `Date` 用 Hutool `DateUtil` | `references/03-date-time.md` |
| 文件读写/流拷贝 | JDK NIO + try-with-resources；有 Hutool 用 `FileUtil`/`IoUtil` | `references/04-io-http-json.md` |
| HTTP 调用 | Spring 项目跟随 Spring；纯 Java 用 OkHttp3 | `references/04-io-http-json.md` |
| JSON 序列化 | Jackson `ObjectMapper`（复用单例） | `references/04-io-http-json.md` |
| 线程池/异步/虚拟线程 | JDK `ThreadPoolExecutor` + `CompletableFuture` | `references/05-concurrency.md` |
| Bean 拷贝/转 Map | MapStruct；无 processor 退 `BeanUtil` | `references/06-object-mapping.md` |
| MD5/SHA/AES/密码哈希 | `hutool-crypto`（`SecureUtil`/`BCrypt`） | `references/07-crypto.md` |
| 异常链/断言/日志 | SLF4J 门面 + 占位符；有 Hutool 用 `ExceptionUtil`/`Assert` | `references/08-exception-logging.md` |
| 随机数/随机字符串/安全凭证 | `ThreadLocalRandom`；有 Hutool 用 `RandomUtil`；凭证类用 `SecureRandom` | `references/08-exception-logging.md` |
| 现代 Java 语法（版本门控） | 按「JDK 版本策略」特性最低版本 | `references/09-modern-java.md` |
| 金额/精确小数 | JDK `BigDecimal` | `references/10-bigdecimal.md` |
| 命名/OOP 规约/格式 | 规约条目（无库选型） | `references/11-conventions.md` |
| 方法嵌套过深/分支膨胀/认知复杂度 | 卫语句 + 提炼语义方法 + 分支分发 | `references/12-complexity.md` |

## 规则表（S/A 分级）

**执行规则**：
- **S 级（bug/事故级）**：新代码禁止；审查/修改时发现**既有代码**命中 → 立即向用户提出改写。
- **A 级（风格约定）**：仅约束**新生成代码**；不主动改写用户既有代码、不发起任何询问；工具方法按第 0 步跟随既有栈。

| 级别 | ✗ 模式 | ✓ 改法 |
|---|---|---|
| S | `Executors.newCachedThreadPool`/`newFixedThreadPool`、`new Thread().start()` | `new ThreadPoolExecutor` + 有界队列 + 拒绝策略 |
| S | `SimpleDateFormat` 作共享/静态字段；`Calendar` 手算（月份从 0 起） | `java.time` / `DateUtil` |
| S | `double`/`float` 算钱、`new BigDecimal(double)`、`bd.equals(...)`、裸 `divide` | `BigDecimal(String)` + `compareTo` + scale/`RoundingMode` |
| S | 无盐 MD5/SHA 存密码 | `BCrypt.hashpw` |
| S | 手搓 `MessageDigest` 且 hex 无 `%02x` | `SecureUtil.md5`/`sha256`，或补 `%02x` |
| S | `catch (InterruptedException e) {}` 空吞 | 加 `Thread.currentThread().interrupt()` |
| S | `finally { throw/return }` | 移除 |
| S | `catch (Throwable/Error)`、空 catch 吞异常 | 缩窄到具体类型分别处理 |
| S | `Optional.get()` 前无 `isPresent`/`orXxx` | `orElse`/`orElseThrow` |
| S | `BeanUtils.copyProperties` 未确认源/目标顺序（Spring 与 Apache 参数顺序相反） | MapStruct / `BeanUtil`（顺序固定 source,target） |
| S | `subList` 结果当独立列表/分页 | `ListUtil.partition` 或拷贝 `new ArrayList<>(view)` |
| S | 手拼 JSON 字符串 | Jackson 等既有 JSON 库 |
| S | `Math.random()`/`Random` 生成"唯一"序号/单号/ID（如 `(int)(Math.random()*100000)` 当 seq） | DB 序列 / Redis `INCR` / 雪花 ID 等单调发号器 |
| S | `Random`/`ThreadLocalRandom`/`Math.random()` 生成 token/验证码/密码/盐等安全凭证 | JDK `SecureRandom`（原生即成熟） |
| S | 违反目标 JDK 版本门控（如 JDK 8 用 `var`/`record`） | 按版本门控降级写法 |
| A | `== null \|\| .trim().isEmpty()` 手写判空 | 工具方法（`StrUtil.isBlank` / `StringUtils` / JDK `isBlank`(11+)） |
| A | `a.equals(b)` 且 a 可能 null | `Objects.equals` / `ObjectUtil.equal` / 常量在前 |
| A | 仅初始化就 `new ArrayList<>()` 逐个 add；`subList` 手写分块 | `List.of` / `CollUtil.newArrayList`/`partition` |
| A | `log.error("x=" + e)` 字符串拼接 | 占位符 `log.error("x={}", x, e)`，异常作最后参数 |
| A | 裸 `LocalDateTime.now()`/`LocalDate.now()` 等 time-based `now()`（隐式 JVM 默认时区；Sonar java:S8688） | `now(zoneId)` / `now(clock)`（应用级统一 ZoneId 常量或注入 Clock） |
| A | `new Random().nextInt()` 手算范围、`(int)(Math.random()*n)` 强转 | `RandomUtil.randomInt(min, max)`（[min, max) 半开）/ `ThreadLocalRandom.current().nextInt(min, max)` |
| A | 手拼随机字符串（`Math.random()`+`String.format`/自建字符表循环） | `RandomUtil.randomString(len)` / `randomNumbers(len)` |
| A | POJO 布尔属性 `isXxx` 前缀 | 用 `deleted` 而非 `isDeleted` |
| A | 魔法值直出 | 抽 `static final` 常量或枚举 |
| A | 无用 import（未使用/重复/java.lang/同包；Sonar java:S1128）残留 | 移除；删掉某类最后一处使用时同步删 import |
| A | 单方法嵌套 ≥3 层、else-if ≥3 连、布尔混用 ≥3 项（Sonar java:S3776 认知复杂度阈值 15） | 卫语句早返回 / 提炼语义方法 / switch、策略 Map 分发（禁无语义拆块） |
| A | `get`/`find` 类方法返回 null | `Optional<T>` 或空集合 |

## C-CHECK 询问（仅高风险能力缺失时触发）

**触发条件**：任务确实需要**加密/哈希/密码**（项目无 crypto 能力）或 **Bean 映射**（无 MapStruct/Hutool），才向用户询问；低风险场景**永不询问**。

- **询问要点**（一次问全，可与第 0 步的 JDK 提问合并）：说明场景与推荐构件 → 给出坐标（下表）→ 两个选项：A) 引入并使用库；B) 不引入，手写实现。
- **用户拒绝 → 受控降级**：手写实现但按对应 reference（`references/07-crypto.md` / `references/06-object-mapping.md`）的 antipattern 保留守卫（如 hex 必须 `%02x` 补零；密码场景禁无盐并再次建议引入），并在代码注释标注这是受控降级。

| 依赖 | 坐标 | 说明 |
|---|---|---|
| BOM | `cn.hutool:hutool-bom:5.8.47`（dependencyManagement 中 `import`） | 版本单一来源，模块不带 version；禁 `hutool-all` |
| core | `cn.hutool:hutool-core` | StrUtil/CollUtil/DateUtil/BeanUtil/Base64 等 |
| crypto | `cn.hutool:hutool-crypto` | `SecureUtil`/`DigestUtil`/`BCrypt`/`AES` **全在 crypto**（仅 `Base64` 在 core） |

其他构件参考版本（项目无同类库且确需时才引入）：

| 构件 | 参考版本 | 门控 / 备注 |
|---|---|---|
| MapStruct | 1.5.5.Final | 需 annotation processor（编译期生成） |
| Jackson | 2.17.1 | Spring 项目跟随 Boot 自带版本 |
| OkHttp3 | 4.12.0 | 纯 Java 项目 HTTP |
| Lombok | 1.18.34 | JDK 8+ |
| SLF4J + Logback | 2.0.13 + 1.5.x | 需 JDK 11+；JDK 8 用 SLF4J 1.7.36 + Logback 1.2.x，两套禁混用（见 `references/08-exception-logging.md`） |

## 使用流程

1. **第 0 步栈探测**：目标 JDK + 已有栈，确定本次的工具选型基线。
2. **定位并阅读 reference**：查「域 → 默认」路由表，**生成对应域代码前先读「详见」列文件**（含该域完整规则与 antipattern，本文规则表仅是摘要）。
3. **生成代码遵循规则表**：S 级禁止项不出现；A 级约定用于新代码；审查/修改时 S 级命中既有代码 → 提出改写。
4. **高风险能力缺失** → 触发 C-CHECK 询问，拒绝则受控降级。
5. **输出前对 S 级规则逐项自检**（尤其线程池、日期、金额、加密、随机数当序号、异常处理）。

## 版本与范围

- Hutool 5.8.x（最新稳定 5.8.47，API 对照官方 javadoc 核实）；JDK 8 为下限，门控见 `references/09-modern-java.md`。
- **去重原则**：一个项目一套字符串/集合工具，不混用。已有 commons-lang3 → 用其 `StringUtils`/`ObjectUtils`，仅当缺该能力（如 BCrypt、DateUtil）才补对应 Hutool 模块并注释混用原因；已有 Hutool → 不再加 commons-lang3。
