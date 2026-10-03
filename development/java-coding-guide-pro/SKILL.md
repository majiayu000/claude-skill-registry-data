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
  静默失效排查（注解自调用 / 包装类型比较 / 不可变集合）、
  分层职责与代码组织（封装 / 复用 / 常量与配置归属 / 资源托管）、
  现代 Java 语法（JDK 8~25，按特性最低版本门控）。
  次级触发信号——代码中出现：SimpleDateFormat、Executors.newFixedThreadPool /
  newCachedThreadPool / newSingleThreadExecutor、new Thread(...)、
  new BigDecimal(0.1) 小数构造、BeanUtils.copyProperties、BeanUtil.copyProperties、BeanUtil.toBean、BeanUtil.beanToMap、catch (Throwable) /
  catch (InterruptedException) 空块、MessageDigest（手写 MD5/SHA）、
  log.error("x=" + x) 日志拼接、Optional.get()、subList(...)、
  finally 块内 return / throw、Math.random()、new Random()、
  @Transactional / @Async / @Cacheable 自调用或打在 private 方法上、@Autowired 字段注入、
  @Value 注 static 字段、包装类型（Integer/Long）== 比较、List.of/Map.of 结果被 add、
  并发 Map 先查后写、Lombok @Data 打在实体上、getXxx() 直接返回内部集合、
  业务类内堆 static final 常量 / 硬编码 URL 与超时；
  用户任务词出现：生成订单号 / 流水号 / 唯一 ID、生成验证码 / token / 盐、
  密码加密 / 哈希存储、金额 / 价格计算、线程池 / 异步任务、日期格式化 / 时区、
  分层 / 职责划分、常量放哪 / 配置外置、代码结构组织 / 复用抽取。
  跟随项目既有技术栈（Spring / Hutool / commons-lang3 等），不强加任何库。
  不适用：业务架构设计（微服务拆分 / 领域建模）、框架选型、DDL、纯算法、前端代码。
version: "3.8.0"
last_verified: "2026-09-18"
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

> 22–24 转正特性统一按 25 门控；preview/incubator 不纳入。虚拟线程 + `synchronized` 在 21 会钉住载体线程（改 `ReentrantLock`），25 解除（JEP 491）。完整门控表见 `references/09-modern-java.md`。

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
| Bean 拷贝/转 Map | MapStruct；无 processor 用显式 setter/构造器；禁止反射拷贝（BeanUtil/BeanUtils.copyProperties、toBean、beanToMap、cloneByStream） | `references/06-object-mapping.md` |
| MD5/SHA/AES/密码哈希 | `hutool-crypto`（`SecureUtil`/`BCrypt`） | `references/07-crypto.md` |
| 异常链/断言/日志 | SLF4J 门面 + 占位符；有 Hutool 用 `ExceptionUtil`/`Assert` | `references/08-exception-logging.md` |
| 随机数/随机字符串/安全凭证 | `ThreadLocalRandom`；有 Hutool 用 `RandomUtil`；凭证类用 `SecureRandom` | `references/08-exception-logging.md` |
| 现代 Java 语法（版本门控） | 按「JDK 版本策略」特性最低版本 | `references/09-modern-java.md` |
| 金额/精确小数 | JDK `BigDecimal` | `references/10-bigdecimal.md` |
| 命名/OOP 规约/格式/常量与字面量 | 规约条目（无库选型） | `references/11-conventions.md` |
| 方法嵌套过深/分支膨胀/认知复杂度 | 卫语句 + 提炼语义方法 + 分支分发 | `references/12-complexity.md` |
| 编译过、单测过但运行不生效（注解自调用、包装类型 `==`、拆箱 NPE、不可变集合被改、`@Data` 打实体） | 按静默失效清单逐条消除 | `references/13-silent-failure.md` |
| 分层职责/封装/复用/类职责判定（上帝类）/常量与配置归属/资源托管 | 规约条目（无库选型） | `references/14-engineering-structure.md` |

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
| S | 反射式 Bean 拷贝/映射（`BeanUtils.copyProperties` / `BeanUtil.copyProperties` / `BeanUtil.toBean` / `BeanUtil.beanToMap` / `mapToBean`）—— 运行时反射，字段名/类型错误运行期才暴露，AI 生成尤危 | MapStruct（编译期生成）/ 显式 setter 或构造器 |
| S | 序列化式深拷贝（`ObjectUtil.cloneByStream`）—— 依赖 Serializable，类型/字段不符运行期才暴露，单测易漏 | 显式拷贝构造器 / MapStruct |
| S | `subList` 结果当独立列表/分页 | `ListUtil.partition` 或拷贝 `new ArrayList<>(view)` |
| S | 手拼 JSON 字符串 | Jackson 等既有 JSON 库 |
| S | `Math.random()`/`Random` 生成"唯一"序号/单号/ID（如 `(int)(Math.random()*100000)` 当 seq） | DB 序列 / Redis `INCR` / 雪花 ID 等单调发号器 |
| S | `Random`/`ThreadLocalRandom`/`Math.random()` 生成 token/验证码/密码/盐等安全凭证 | JDK `SecureRandom`（原生即成熟） |
| S | 违反目标 JDK 版本门控（如 JDK 8 用 `var`/`record`） | 按版本门控降级写法 |
| S | `@Transactional`/`@Async`/`@Cacheable` 自调用（同类 `this.xxx()`），或注解打在 `private`/`final`/`static` 方法上 —— 不走代理，注解静默失效 | 拆到另一个 Bean / `TransactionTemplate`；注解方法必须 public 且非 final/static |
| S | 事务方法内 `catch` 吞异常 —— 事务静默不回滚（默认只回滚 `RuntimeException`） | 继续抛出；必须吞则 `setRollbackOnly()`；受检异常配 `rollbackFor` |
| S | `@Value`/`@Autowired` 注 `static` 字段 —— 恒为 null | 实例字段 + 构造器注入 |
| S | 包装类型 `==`（`Integer`/`Long` 超 -128~127 缓存即 false）、`map.get(k)` 直赋 `int`（拆箱 NPE） | `Objects.equals` / `intValue()` / `getOrDefault` |
| S | 并发 Map 两段式（`containsKey`+`put`、`get` 判空再 `put`）—— 非原子，并发丢更新 | `computeIfAbsent` / `putIfAbsent` / `merge` |
| S | `List.of`/`Map.of`/`Arrays.asList` 结果做 `add`/`put` —— 运行期 `UnsupportedOperationException` | 需可变则 `new ArrayList<>(...)`；返回前确认可变性 |
| S | `split(",")` 不传 limit —— 尾随空串被丢弃，字段数变少、下标错位 | 需全字段（CSV / 定长协议）传 `split(",", -1)` |
| S | Lombok `@Data` 打在实体 / 领域对象上 —— 全字段 setter 破封装、双向关联 `toString`/`hashCode` 递归 `StackOverflowError`、判等覆盖可变字段 | 实体用 `@Getter` + 显式构造；关联字段 `@ToString.Exclude` / `@EqualsAndHashCode.Exclude` |
| S | `getXxx()` 直接返回内部集合引用 —— 调用方 `clear()`/`add()` 即改内部状态 | `List.copyOf(...)`（`Collections.unmodifiableList` 只是视图） |
| S | `equals` 签名写成 `equals(User)` —— 静默降级为**重载**，`contains`/`get`/`Set` 去重全按引用比较 | 参数必须 `Object`，与 `hashCode` 成对重写 |
| S | 业务方法内 `new` 线程池 / HTTP 客户端 / `ObjectMapper` 等重资源对象（不关闭、不复用） | 应用级单例 Bean + `destroyMethod="shutdown"` |
| A | `== null \|\| .trim().isEmpty()` 手写判空 | 工具方法（`StrUtil.isBlank` / `StringUtils` / JDK `isBlank`(11+)） |
| A | `a.equals(b)` 且 a 可能 null | `Objects.equals` / `ObjectUtil.equal` / 常量在前 |
| A | 仅初始化就 `new ArrayList<>()` 逐个 add；`subList` 手写分块 | `List.of` / `CollUtil.newArrayList`/`partition` |
| A | `log.error("x=" + e)` 字符串拼接 | 占位符 `log.error("x={}", x, e)`，异常作最后参数 |
| A | 裸 `LocalDateTime.now()`/`LocalDate.now()` 等 time-based `now()`（隐式 JVM 默认时区） | `now(zoneId)` / `now(clock)`（应用级统一 ZoneId 常量或注入 Clock） |
| A | `new Random().nextInt()` 手算范围、`(int)(Math.random()*n)` 强转 | `RandomUtil.randomInt(min, max)`（[min, max) 半开）/ `ThreadLocalRandom.current().nextInt(min, max)` |
| A | 手拼随机字符串（`Math.random()`+`String.format`/自建字符表循环） | `RandomUtil.randomString(len)` / `randomNumbers(len)` |
| A | POJO 布尔属性 `isXxx` 前缀 | 用 `deleted` 而非 `isDeleted` |
| A | 魔法值直出 | 抽 `static final` 常量或枚举 |
| A | 字面量 ≥2 处未提取；常量堆在实现类中不共享 | 状态/类型码 → 枚举；阈值/配置 → 按域拆分的常量类 |
| A | 无用 import（未使用/重复/java.lang/同包）残留 | 移除；删掉某类最后一处使用时同步删 import |
| A | 单方法嵌套 ≥3 层、else-if ≥3 连、布尔混用 ≥3 项（认知复杂度阈值 15） | 卫语句早返回 / 提炼语义方法 / switch、策略 Map 分发（禁无语义拆块） |
| A | `get`/`find` 类方法返回 null | `Optional<T>` 或空集合 |
| A | `@Autowired` 字段注入 | 构造器注入 + `final` |
| A | Controller 写业务规则 / 直连 DAO；Service 直接返回 Entity | 各层只做自己的事；Entity → DTO/VO（见 `06`） |
| A | 环境相关值（回调 URL / 超时 / 开关 / 阈值）硬编码在业务类 | `@ConfigurationProperties` 按域外置，`@Value` 不撒满业务类 |
| A | 上帝类：一个类混杂多个互不相关的业务概念（类名/javadoc 需用「以及」概括、变更原因来自多个业务方） | 按**业务概念**拆类；**注入依赖数 / 行数 / 方法数不作为判据**（见 `14`） |
| A | 同一逻辑 ≥2 处各写一遍；或反向抽带 flag 的"通用"方法 | 提到领域对象（内聚最高）；概念相同才合并 |

## C-CHECK 询问（仅高风险能力缺失时触发）

**触发条件**：任务确实需要**加密/哈希/密码**（项目无 crypto 能力）或 **Bean 映射**（无 MapStruct/Hutool），才向用户询问；低风险场景**永不询问**。

- **询问要点**（一次问全，可与第 0 步的 JDK 提问合并）：说明场景与推荐构件 → 给出坐标（下表）→ 两个选项：A) 引入并使用库；B) 不引入，手写实现。
- **用户拒绝 → 受控降级**：手写实现但按对应 reference（`references/07-crypto.md` / `references/06-object-mapping.md`）的 antipattern 保留守卫（如 hex 必须 `%02x` 补零；密码场景禁无盐并再次建议引入），并在代码注释标注这是受控降级。

| 依赖 | 坐标 | 说明 |
|---|---|---|
| BOM | `cn.hutool:hutool-bom:5.8.47`（dependencyManagement 中 `import`） | 版本单一来源，模块不带 version；禁 `hutool-all` |
| core | `cn.hutool:hutool-core` | StrUtil/CollUtil/DateUtil/Base64 等 |
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
5. **输出前对 S 级规则逐项自检**（尤其线程池、日期、金额、加密、随机数当序号、异常处理、反射拷贝、注解自调用与代理边界、包装类型比较、重资源归属）。
6. **结构自检（新代码）**：分层是否越界（Controller / Service / DAO）、Entity 是否外泄、依赖是否构造器注入、常量与配置是否放对位置、类职责是否单一——逐项对照 `references/14-engineering-structure.md`。

## 版本与范围

- Hutool 5.8.x（最新稳定 5.8.47，API 对照官方 javadoc 核实）；JDK 8 为下限，门控见 `references/09-modern-java.md`。
- **去重原则**：一个项目一套字符串/集合工具，不混用。已有 commons-lang3 → 用其 `StringUtils`/`ObjectUtils`，仅当缺该能力（如 BCrypt、DateUtil）才补对应 Hutool 模块并注释混用原因；已有 Hutool → 不再加 commons-lang3。
