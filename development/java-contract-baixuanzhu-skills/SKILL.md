---
name: java-contract
slug: java-contract
displayName: Java 编码契约
description: >-
  为项目建立并执行 Java 编码契约：把需求没说明的边界决策（无结果 / null 参数 / 集合里的 null /
  重复 key / 结果顺序与可变性 / 非法参数 / 静态还是实例 / 重复到达）落成 .claude/rules/java-contract.md，
  动手前先读、写完编译验证；审存量代码时按失效模式七组追问。
  在编写、修改、审查 Java 代码时使用；也用于决定某个方法该返回 null 还是空集合、
  空集合聚合该返回 0 还是 Optional、为项目定下统一的边界处理规则。
  触发信号：要为新方法定返回契约、项目里还没有 .claude/rules/java-contract.md、
  put 与 putIfAbsent 混用、写操作可能被重复投递或重试、
  cannot find symbol 且 symbol 是 var 或 JDK 9+ 方法名。
  不适用：第三方库 API 用法与选型、Spring 分层与工程组织、测试框架、静态检查规则集、前端代码。
version: "2.7.1"
last_verified: "2026-10-23"
---

# Java 编码契约

模型对 JDK 写法的判断已经够准（实测语法陷阱 3/3、7/7 全部避开），API 字典类内容不必再写。真正的分歧在
**需求文档不写、几个实现会给几种答案**的地方。本技能只做三件事：把这些决策定下来、动手前读一遍、写完验证。

## 两条原则

1. **契约先落盘，用前先读。** 第一次在项目里写 Java 时，把八项边界决策写进 `.claude/rules/java-contract.md`；
   之后每次动 `.java` 前先读它。它**不会自动进上下文**——实测里一个被要求不浏览其他文件的 agent
   虽然有这份契约，仍按自己的判断把该保留的记录丢了。不落盘的决策等于没定，落了盘没人读同样等于没定。
   **读不到它时**（文件不存在、只能看片段、子代理拿不到仓库），按本技能默认值写，并在回复里点明
   「按 java-contract 默认，未读到项目契约」。分歧摆在明面上，比静默按自己的判断做要好。
2. **写完即编译。** 目标版本从 `pom.xml` 的 `maven.compiler.release` / `<source>` / `sourceCompatibility` /
   `java.toolchain` 读，四者都读不到才问一次。一个类写完就 `mvn -q compile`（Gradle：`./gradlew compileJava`）。
   版本不匹配在这一步暴露，比背着规则表写 200 行再让 CI 拦下来便宜。

## 第一步：读项目

三件事都在仓库里，做完再动笔：

| 读什么 | 得到什么 |
|---|---|
| `pom.xml` / `build.gradle` | 目标 JDK；`<modules>` 说明是否多模块 |
| `.claude/rules/java-contract.md` | 已有契约。**读到才生效**，读到就遵守、不重新提议 |
| 同包下 2~3 个同类方法 | 既有惯例：返回 `Optional` 还是裸值、抛异常还是错误码 |

**项目惯例与下表默认冲突时，惯例优先。** 契约的作用是消除分歧，不是推行新风格。

## 契约八项

需求没说明时按下表取；项目已有不同做法就记进契约文件，不在代码里另搞一套。

| 分歧点 | 默认 |
|---|---|
| 无结果 | 单条 → `Optional`；列表 → 空集合；聚合值看 0 是否有业务含义（求和 → 0，平均 / 最大 → `Optional`）。不返回 null |
| null 参数 | 必填标量 → `Objects.requireNonNull`，不编默认值；**集合参数一律按空处理**，不用 `requireNonNull`，业务要求非空用 `isEmpty()` 校验 |
| 集合中的 null 元素 | `null` 元素跳过；字段无值看用途——累加 / 平均跳过整条记录，拼接跳过该值，排序 / 分页保留并排末尾；**先剔除再切页** |
| 重复 key | `putIfAbsent` 保留首条；要覆盖用 `put` 并在注释写明原因 |
| 返回集合的形态 | 顺序：对外返回的 `Map` 保插入顺序（`groupingBy` 传 `LinkedHashMap::new`），字典序用 `TreeMap`。可变性：默认不可变；`Map.copyOf` 不保序，保序 Map 用 `unmodifiableMap(new LinkedHashMap<>(x))`；8 用 `unmodifiableList(new ArrayList<>(x))` |
| 非法参数 | 展示层容错（`pageNo < 1` 纠正为 1），领域层 fail fast（状态码不认识就抛）。抛哪种异常见 `references/01-contract.md` 第五节 |
| 静态还是实例 | 纯函数 `static`；依赖注入用实例；同一个类不混用 |
| 重复到达 | 重复请求 → 返回上次结果、不重复执行、**不抛异常**（抛了会重投）；已终态（CLOSED / REFUNDED）又收到成功通知 → 默认不复活、不加权益，但**落一条可查询的待处理记录**（只打日志不算），返回成功 |

**怎么定位到哪一项**：对每个新增的 public 方法问六句，答「是」的才受契约约束——

1. 入参为空时，结果是「没有」还是「就是 0」？→ 第一节（无结果）
2. 哪个参数为 `null` 时方法无意义？→ 第二节（null 参数）
3. 入参或中间结果里有集合吗？→ 第三节（集合里的 null 元素）
4. 有没有从外部数据构造 `Map`、或按 key 分组汇总？→ 第四节（重复 key）、第七节（顺序与可变性）
5. 有分页、条数、状态码这类外部数值或枚举参数吗？→ 第五节（非法参数）
6. 这是写操作吗？同一个请求可能到达两次（外部重试、用户连点、回调重投）？→ 第八节（重复到达）

六句都不成立（纯计算、无集合入参、不写数据）就不必套模板。静态还是实例这一项不看单个方法，建类时定一次、
类内统一。每项的识别判据、两项冲突时听谁，见 `references/01-contract.md`。

**落盘**：模板 `assets/contract-template.md` → `.claude/rules/java-contract.md`，`paths` 固定
`"**/*.java"`，首行标记 `<!-- seeded: java-contract@⟨版本⟩ -->`，`⟨版本⟩` 填本文件 frontmatter 的 `version`。
文件已存在且无该标记，说明是用户自己写的——只补缺失事实，不改原文。

**加一道保险**：把最通用的四五条同步写进类的 javadoc（集合参数 `null` 与空等价、集合里 `null` 元素跳过、
无列表结果返回空集合、返回集合不可变）。实测这四项写在 javadoc 里就能让没读到契约文件的实现者做对；
细粒度规则（字段无值按用途三分、先剔除再切页）留契约文件——那部分写在 javadoc 里会喧宾夺主，
而它恰恰是必须读到契约才做得对的一条。

## 写完即验证

1. 编译：`mvn -q compile`。版本问题在这一步暴露，别留到 CI。
2. 契约相关分支至少跑一次：空入参、无结果、重复 key 三类各一个调用或用例。没有测试的，说明原因。

**编译报错时**：`cannot find symbol` 且 `symbol` 是 `class var`、或方法名属于 JDK 9+ API（`List.of`、
`isBlank`、`Stream.toList`）时，先怀疑版本，不要顺着报错去补 import 或改名——那会把版本问题改成一堆
无用代码。`record` / 文本块 / `switch` 表达式会直接提示 `are not supported in -source N`，按提示换写法。
一律改代码，不改 `maven.compiler.release`，那只会让产物在目标运行时 `UnsupportedClassVersionError`。

## 审查（存量代码，独立动作）

靶子是**已有的、别人写的代码**。刚生成的新代码不必逐条对照——这些坑生成时基本不犯，对照只是消耗上下文。
审存量时读 `references/02-review.md`，按它的七组顺序**逐组用一句问题去追代码路径**：数据是否在两处各算一遍、
状态是否还有第二份副本、信任边界是否被绕过、什么会随运行时间累积。
不要按 API 分类扫（数值一组、字符串一组）——那会把范围收窄到分组枚举过的写法，最贵的问题往往落在组外。
审查与生成分开做：写完立刻自审会顺着自己的思路看，最容易漏的是「返回契约与调用方期望不一致」。
可交给子代理执行，rubric 用项目里的契约文件。

## 库边界

读 `pom.xml` 一次，只在下表能力缺失且任务确实需要时推荐一次：

| 能力 | 缺失时推荐 |
|---|---|
| 判空 / 集合 / 字符串 / 日期 | 国内栈 `cn.hutool:hutool-bom`；Spring 国际栈 `commons-lang3` |
| Bean 映射 | `org.mapstruct:mapstruct`（编译期生成） |
| 加密 / 哈希 | `cn.hutool:hutool-crypto` |
| JSON / HTTP | 跟随项目既有栈；都没有则 Jackson / OkHttp |

只给坐标加一句理由，不给 API 示例。用户拒绝就用 JDK 原生，不追问第二次。

## 使用流程

1. 读项目：pom 确认目标 JDK；`.claude/rules/java-contract.md` 有就先读（它决定契约）；同包 2~3 个同类方法看惯例。
2. 无契约文件时按「契约八项」提议落盘，等用户确认。
3. 用六问定位本次方法落在哪几项，定下返回契约，再动手。
4. 写代码；编译报错先按「编译报错时」判版本，再改语法。
5. 写完编译，契约分支跑一次。
6. 要审存量代码时按 `references/02-review.md` 独立执行。
