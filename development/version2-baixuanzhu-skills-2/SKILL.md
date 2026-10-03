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
  现代 Java 语法（JDK 8~25，按 LTS 版本门控）。
  次级触发信号：new SimpleDateFormat、Executors.newXxx、new Thread()、double/float 算钱、
  new BigDecimal(double)、BeanUtils.copyProperties、catch(Throwable)、手搓 MessageDigest、
  log.error("x"+e) 拼接、Optional.get() 不判空、subList 分页、finally 中 return/throw、
  Math.random() 强转生成序号/ID、Random 生成 token/验证码。
  跟随项目既有技术栈（Spring / Hutool / commons-lang3 等），不强加任何库。
  不适用：业务架构设计、框架选型、DDL、纯算法、前端代码。
version: "3.4.0"
last_verified: "2026-08-04"
---

# Java 编码指南

面向日常 Java 开发的**编码约定助手**。每条规则含「✗ 禁止 → ✓ 推荐 → 为什么」，覆盖 JDK 8~25+（LTS 锚定：8/11/17/21/25）。

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
   - **高风险能力缺失**且任务确实需要（见「高风险场景」表）→ 触发 C-CHECK 询问是否引入。
   - **低风险能力缺失**（判空/集合/随机数/日期等）→ 直接用 JDK 原生，**零打断、不询问**。

## JDK 版本策略（五档 LTS 语义）

- **JDK 8（下限）**：可用 `Optional`/`Stream`/`java.time`/`CompletableFuture`/Lambda。**禁** `var`/`record`/`switch 表达式`/文本块/`sealed`/`虚拟线程`/`Stream.toList()`。
- **JDK 11**：+ `var`(10)、JDK `HttpClient`(11)。
- **JDK 17**：+ `switch` 表达式(14)、文本块(15)、`record`(16)、`sealed`(17)、`Stream.toList()`(16)、`instanceof` 模式匹配(16)。
- **JDK 21**：+ 虚拟线程、`switch` 模式匹配、`SequencedCollection`、record 模式。
- **JDK 25**：+ 22–24 转正特性（未命名变量 `_`、Stream Gatherers、Scoped Values 等）；虚拟线程不再被 synchronized 钉住（JEP 491）。

> LTS 锚定：门控只标 LTS；22–24 转正特性统一归入 25；preview/incubator 不纳入。详细门控见 `references/09-modern-java.md`。

## 高风险场景优先成熟构件（本指南的核心立场）

以下场景手写极易出 bug，**优先用成熟构件**（顺序：项目既有库 > JDK 原生成熟 API > 推荐引入）：

| 风险场景 | 为什么手写危险 | 项目无既有方案时的推荐 |
|---|---|---|
| 加密 / 哈希 / 密码 | hex 前导零丢失致碰撞；无盐哈希被彩虹表反查 | `hutool-crypto`（`SecureUtil`/`BCrypt`），触发 C-CHECK |
| 线程池 / 并发 | `Executors.newXxx` 无界队列 OOM；中断状态丢失 | JDK `ThreadPoolExecutor` + `CompletableFuture`（原生即成熟） |
| JSON 解析 | 手拼转义遗漏 / 注入 | Jackson `ObjectMapper` 复用单例（Spring 项目已自带） |
| Bean 映射 | Spring/Apache `BeanUtils` 源目标顺序相反，静默拷空 | MapStruct（编译期安全）；无 processor 退 `BeanUtil`，触发 C-CHECK |
| HTTP 调用 | 连接泄漏、超时缺省 | 跟随 Spring（RestTemplate/WebClient）；纯 Java 项目才 OkHttp3 |
| 金额运算 | 二进制浮点无法精确表示十进制 | JDK `BigDecimal`（原生即成熟） |

**低风险场景**（判空、集合新建/分块、随机数、日期格式化）：项目有 Hutool / commons-lang3 就用其工具方法，没有就 JDK 原生（`Objects`/`String.isBlank`(11+)/`List.of`(9+)/`ThreadLocalRandom`/`java.time`），**不触发任何询问**。

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
| 现代 Java 语法（版本门控） | 按目标 JDK 五档 | `references/09-modern-java.md` |
| 金额/精确小数 | JDK `BigDecimal` | `references/10-bigdecimal.md` |
| 命名/OOP 规约/格式 | 阿里 Java 开发手册规约 | `references/11-conventions.md` |
| 方法嵌套过深/分支膨胀/认知复杂度 | 卫语句 + 提炼语义方法 + 分支分发 | `references/12-complexity.md` |

## 规则表（S/A 分级）

**执行规则**：
- **S 级（bug/事故级）**：新代码禁止；审查/修改时发现**既有代码**命中 → 立即向用户提出改写。
- **A 级（风格约定）**：仅约束**新生成代码**；不主动改写用户既有代码、不发起任何询问；工具方法按第 0 步跟随既有栈。

| 级别 | ✗ 模式 | ✓ 改法 | 为什么 |
|---|---|---|---|
| S | `Executors.newCachedThreadPool`/`newFixedThreadPool`、`new Thread().start()` | `new ThreadPoolExecutor` + 有界队列 + 拒绝策略 | 无界队列任务堆积 OOM |
| S | `SimpleDateFormat` 作共享/静态字段；`Calendar` 手算 | `java.time` / `DateUtil` | 线程不安全；月从 0 |
| S | `double`/`float` 算钱、`new BigDecimal(double)`、`bd.equals(...)`、裸 `divide` | `BigDecimal(String)` + `compareTo` + scale/`RoundingMode` | 浮点精度陷阱；equals 连 scale 一起比 |
| S | 无盐 MD5/SHA 存密码 | `BCrypt.hashpw` | 彩虹表反查 |
| S | 手搓 `MessageDigest` 且 hex 无 `%02x` | `SecureUtil.md5`/`sha256`，或补 `%02x` | 前导零丢失致哈希碰撞 |
| S | `catch (InterruptedException e) {}` 空吞 | 加 `Thread.currentThread().interrupt()` | 中断丢失，线程池无法关停 |
| S | `finally { throw/return }` | 移除 | — |
| S | `catch (Throwable/Error)`、空 catch 吞异常 | 缩窄到具体类型分别处理 | — |
| S | `Optional.get()` 前无 `isPresent`/`orXxx` | `orElse`/`orElseThrow` | — |
| S | `BeanUtils.copyProperties` 未确认源/目标顺序 | MapStruct / `BeanUtil`（顺序固定 source,target） | Spring 与 Apache 参数顺序相反，记错静默拷空 |
| S | `subList` 结果当独立列表/分页 | `ListUtil.partition` 或拷贝 `new ArrayList<>(view)` | — |
| S | 手拼 JSON 字符串 | Jackson 等既有 JSON 库 | — |
| S | `Math.random()`/`Random` 生成"唯一"序号/单号/ID（如 `(int)(Math.random()*100000)` 当 seq） | DB 序列 / Redis `INCR` / 雪花 ID 等单调发号器 | 随机≠唯一：10 万空间约 400 次即 50% 碰撞（生日悖论），单号重复是事故 |
| S | `Random`/`ThreadLocalRandom`/`Math.random()` 生成 token/验证码/密码/盐等安全凭证 | JDK `SecureRandom`（原生即成熟） | 线性同余可由少量输出反推种子，凭证可预测 |
| S | 违反目标 JDK 版本门控（如 JDK 8 用 `var`/`record`） | 按五档门控降级写法 | — |
| A | `== null \|\| .trim().isEmpty()` 手写判空 | 工具方法（`StrUtil.isBlank` / `StringUtils` / JDK `isBlank`(11+)） | — |
| A | `a.equals(b)` 且 a 可能 null | `Objects.equals` / `ObjectUtil.equal` / 常量在前 | — |
| A | 仅初始化就 `new ArrayList<>()` 逐个 add；`subList` 手写分块 | `List.of` / `CollUtil.newArrayList`/`partition` | — |
| A | `log.error("x=" + e)` 字符串拼接 | 占位符 `log.error("x={}", x, e)`，异常作最后参数 | 拼接在日志关闭时也执行 |
| A | 裸 `LocalDateTime.now()`/`LocalDate.now()` 等 time-based `now()` | `now(zoneId)` / `now(clock)`（应用级统一 ZoneId 常量或注入 Clock） | 隐式依赖 JVM 默认时区，容器多为 UTC，日切/对账跨天错 8 小时；Sonar java:S8688 |
| A | `new Random().nextInt()` 手算范围、`(int)(Math.random()*n)` 强转 | `RandomUtil.randomInt(min,max)` / `ThreadLocalRandom.current().nextInt(min,max)` | 手算边界易错（半开区间）；`Math.random()` 全局共享实例有锁竞争 |
| A | 手拼随机字符串（`Math.random()`+`String.format`/自建字符表循环） | `RandomUtil.randomString(len)` / `randomNumbers(len)` | — |
| A | POJO 布尔属性 `isXxx` 前缀 | 用 `deleted` 而非 `isDeleted` | — |
| A | 魔法值直出 | 抽 `static final` 常量或枚举 | — |
| A | 无用 import（未使用/重复/java.lang/同包）残留 | 移除；删掉某类最后一处使用时同步删 import | 虚假依赖信号、污染 diff；Sonar java:S1128 |
| A | 单方法嵌套 ≥3 层、else-if ≥3 连、布尔混用 ≥3 项（预示认知复杂度超标） | 卫语句早返回 / 提炼语义方法 / switch、策略 Map 分发（禁无语义拆块） | 嵌套惩罚是计分大头，难读难测；Sonar java:S3776（阈值 15） |
| A | `get`/`find` 类方法返回 null | `Optional<T>` 或空集合 | — |

## C-CHECK 询问（仅高风险能力缺失时触发）

**触发条件**：任务确实需要**加密/哈希/密码**（项目无 crypto 能力）或 **Bean 映射**（无 MapStruct/Hutool），才向用户询问；低风险场景**永不询问**。

- **询问要点**（一次问全，可与第 0 步的 JDK 提问合并）：说明场景与推荐构件 → 给出坐标（下表）→ 两个选项：A) 引入并使用库；B) 不引入，手写实现。
- **用户拒绝 → 受控降级**：手写实现但按对应 reference（`references/07-crypto.md` / `references/06-object-mapping.md`）的 antipattern 保留守卫（如 hex 必须 `%02x` 补零；密码场景禁无盐并再次建议引入），并在代码注释标注这是受控降级。

| 依赖 | 坐标 | 说明 |
|---|---|---|
| BOM | `cn.hutool:hutool-bom:5.8.47`（dependencyManagement 中 `import`） | 版本单一来源，模块不带 version；禁 `hutool-all` |
| core | `cn.hutool:hutool-core` | StrUtil/CollUtil/DateUtil/BeanUtil/Base64 等 |
| crypto | `cn.hutool:hutool-crypto` | `SecureUtil`/`DigestUtil`/`BCrypt`/`AES` **全在 crypto**（仅 `Base64` 在 core） |

> 其他构件参考版本（JDK 8~25 兼容，仅在项目无同类库且确需时引入）：MapStruct 1.5.5.Final（需 annotation processor）、Jackson 2.17.1、OkHttp3 4.12.0、Lombok 1.18.34、SLF4J 2.0.13（JDK 8 用 1.7.36）+ Logback。
>
> **Sonar S3252 与 Hutool 门面**（`StrUtil.isBlank` 等会命中）：默认保留 `StrUtil` 等门面写法，不主动改写；仅当项目门禁启用该规则且阻断时，才全局换 `CharSequenceUtil` 或配置规则例外，禁混用、禁逐处 NOSONAR，详见 `references/01-null-and-string.md`。

## 使用流程

1. **第 0 步栈探测**：目标 JDK + 已有栈，确定本次的工具选型基线。
2. **定位并阅读 reference**：查「域 → 默认」路由表，**生成对应域代码前先读「详见」列文件**（含该域完整规则与 antipattern，本文规则表仅是摘要）。
3. **生成代码遵循规则表**：S 级禁止项不出现；A 级约定用于新代码；审查/修改时 S 级命中既有代码 → 提出改写。
4. **高风险能力缺失** → 触发 C-CHECK 询问，拒绝则受控降级。
5. **输出前对 S 级规则逐项自检**（尤其线程池、日期、金额、加密、随机数当序号、异常处理）。

## 版本与范围

- Hutool 5.8.x（最新稳定 5.8.47，API 对照官方 javadoc 核实）；JDK 8 为下限，门控见 `references/09-modern-java.md`。
- **去重原则**：一个项目一套字符串/集合工具，不混用。已有 commons-lang3 → 用其 `StringUtils`/`ObjectUtils`，仅当缺该能力（如 BCrypt、DateUtil）才补对应 Hutool 模块并注释混用原因；已有 Hutool → 不再加 commons-lang3。
