---
name: spring-boot-dev
description: >-
  Spring Boot 框架层开发助手——三层架构写法与 Spring 注解隐性陷阱。
  在编写、修改、重构 Spring Boot 的 Controller / Service / Repository 层代码，或处理
  参数校验、全局异常、事务、异步、定时、事件、配置、自动装配问题时使用本技能——
  无论用户是否提到 Spring Boot（写接口 / Controller / Service / 参数校验 / validation /
  全局异常 / @Transactional / 事务失效 / 回滚 / @Async / 线程池 /
  @Scheduled / 定时任务 / @EventListener / 循环依赖 / @ConfigurationProperties /
  @Value / 配置读不到 / 配置不生效）。
  项目依赖含 spring-boot-starter-web 或代码出现 @SpringBootApplication / @RestController /
  @Service / @Transactional / @Async / @Scheduled / @ConfigurationProperties / @Value /
  @RestControllerAdvice / @ConditionalOnXxx / @Validated 时激活。
  次级触发信号：@Transactional 自调用失效、@Transactional 标在 private 方法、
  @Async 默认 SimpleAsyncTaskExecutor、循环依赖报错（BeanCurrentlyInCreationException）、
  @Validated 分组校验不触发、@ExceptionHandler 顺序错乱。
  不适用（主动让位）：ORM CRUD / 分页 / Mapper / 实体映射 → mybatis-plus-dev；
  认证 / 权限 / token / SSO → sa-token-dev（仅当项目依赖含 sa-token 或代码出现 StpUtil；
  否则由本技能提供 HttpSession / ThreadLocal 最小方案）；
  Java 语言层（判空 / 集合 / 并发 / 异常日志）→ java-coding-guide-pro；
  单元测试 → java-unit-test；前端。
agent_created: true
version: 1.0.2
slug: spring-boot-dev
displayName: Spring Boot 开发助手
---

# Spring Boot 开发助手

面向日常 Java 开发的 Spring Boot **框架层**编码助手。推荐 **3.5.x**（3.x 末线，2025-05 GA），**2.7.x 仍适用**（差异已注明），4.x 已 GA。采用**完全本地自包含**策略：所有知识沉淀于本地 `references/`，运行时不依赖任何外部文档站点。

**只管框架层**：三层架构写法、配置、校验、全局异常、事务、异步、定时、事件、自动装配、SpringDoc。**不管** 项目初始化 / 脚手架（→ spring-boot-init）、ORM（→ mybatis-plus-dev）、Java 语言层（→ java-coding-guide-pro）、单测（→ java-unit-test）、集成测试 / 冒烟 / E2E（→ java-integration-test）。认证鉴权：项目已用 Sa-Token → sa-token-dev；否则本技能提供 HttpSession / ThreadLocal 最小方案。

## 版本与命名空间（先判 SpringBoot 版本）

| SpringBoot | GA 状态 | 命名空间 | 备注 |
|---|---|---|---|
| 2.7.x | 2.x 末线（仅商业支持） | `javax.*` | 新项目不再选；存量迁移参考 `references/10-condition-bean.md` |
| **3.5.x** | **3.x 末线（2025-05 GA），推荐** | `jakarta.*` | JDK 17+ 基线；Spring Framework 6.2 |
| 4.x | 已 GA | `jakarta.*` | 新功能线；核心注解语义与 3.x 一致 |

- **3.x 起最大破坏**：`javax.*` → `jakarta.*`（`javax.servlet`→`jakarta.servlet`、`javax.validation`→`jakarta.validation`、`javax.persistence`→`jakarta.persistence`）。`javax.*` 依赖（旧版 Sa-Token / 旧版 MyBatis）在 3.x 项目里**直接 ClassNotFound**。
- **JDK 基线**：3.x 起 **JDK 17**；2.7.x 仍支持 JDK 8/11。Java 语言层门控属 **java-coding-guide-pro**。

## 第 0 步：版本探测与边界判定（收到任务先做这一步）

任务涉及 Spring Boot 框架层（Controller / Service / 配置 / 校验 / 异常 / 事务 / 异步 / 定时 / 事件 / 自动装配）——**先检索项目依赖与代码**：

| 探测项 | 方法 | 判定 |
|---|---|---|
| SpringBoot 版本 | `pom.xml` 读 `spring-boot-starter-parent` 版本，或 `build.gradle` 读 `org.springframework.boot` 插件版本 | 决定 `javax.*` vs `jakarta.*`、JDK 基线、可用特性 |
| 命名空间 | 代码里搜 `import javax.` vs `import jakarta.` | 与 SpringBoot 版本须一致，混用即启动失败 |
| 是否 Web | 依赖含 `spring-boot-starter-web`（Servlet）或 `-webflux`（Reactive） | 非 Web 项目（纯命令行/批处理）不涉及 Controller/校验，跳过 02/04/05 |
| ORM 归属 | 依赖含 `mybatis-plus-*` / `spring-boot-starter-data-jpa` | **ORM 任务让位**：CRUD/Mapper/分页 → mybatis-plus-dev；JPA 不在本技能范围 |
| 认证归属 | 依赖含 `sa-token-*` / `spring-security` | **认证任务让位**：→ sa-token-dev；Spring Security 不在本技能范围 |

**边界冲突处理**：任务同时触及「框架层」和「ORM/认证」时（如「写注册接口」=Controller+校验+存库+登录），本技能只负责 **Controller 写法 + 参数校验 + 全局异常**，存库部分指向 mybatis-plus-dev，登录部分指向 sa-token-dev。**不越界包办。**

## 何时使用本技能

| 信号 | 判定 |
|---|---|
| 写 / 改 Controller / Service / Repository 三层代码（未指明框架） | 激活，先执行「第 0 步」版本探测 |
| 依赖含 `spring-boot-starter-web` / `-webflux` / 代码出现 `@SpringBootApplication` / `@RestController` / `@Service` / `@Configuration` | 激活 |
| 参数校验（`@Valid` / `@Validated` / `@RequestBody` / `@RequestParam` / `@PathVariable`） | 激活 → `references/04-validation.md` |
| 全局异常（`@RestControllerAdvice` / `@ExceptionHandler` / `ResponseEntity` / 统一返回体） | 激活 → `references/05-exception-handling.md` |
| 事务（`@Transactional` / 事务失效 / 回滚 / 传播 / 自调用） | 激活 → `references/06-transaction.md` |
| 异步 / 定时（`@Async` / `@Scheduled` / `@EnableAsync` / `@EnableScheduling` / 线程池 / cron） | 激活 → `references/07-async-schedule.md` |
| 事件（`@EventListener` / `@TransactionalEventListener` / `ApplicationEventPublisher`） | 激活 → `references/08-events.md` |
| 配置（`@ConfigurationProperties` / `@Value` / profile / `application.yml` / 配置读不到） | 激活 → `references/03-config-properties.md` |
| 依赖注入 / 循环依赖（`@Autowired` / 构造器注入 / `@Qualifier` / `BeanCurrentlyInCreationException` / `@Lazy`） | 激活 → `references/09-autowiring.md` |
| 条件装配 / 自动装配（`@ConditionalOnXxx` / `@EnableAutoConfiguration` / `@SpringBootApplication(exclude=...)` / starter 制作） | 激活 → `references/10-condition-bean.md` |
| 启动 / 主类（`@SpringBootApplication` / `scanBasePackages` / `@ComponentScan` / 启动失败 / Bean 找不到） | 激活 → `references/01-startup-config.md` |
| 接口文档（`@OpenAPIDefinition` / `@Operation` / `@Schema` / springdoc / openapi） | 激活 → `references/11-springdoc.md` |
| **ORM CRUD / Mapper / 实体映射**；**认证 / 鉴权 / token / SSO** | **不适用** → mybatis-plus-dev / sa-token-dev |
| Java 语言层（判空 / 集合 / 并发 / 异常日志）；单测；集成测试 / 冒烟 / E2E；前端 | **不适用** → java-coding-guide-pro / java-unit-test / java-integration-test / — |

> **检查点**：判定为「不适用」→ 告知用户该问题属哪个技能范围，建议切换。判定为「框架层 + ORM/认证 混合」→ 只做框架层部分，其余指向对应技能。

## 决策路由（全部本地，无在线 fetch）

| 需求场景（关键词） | 读取文件 | 同时警告 |
|---|---|---|
| 启动类、`@SpringBootApplication`、scanBasePackages、主类位置、启动失败、Bean 找不到、profile 激活 | `references/01-startup-config.md` | 主类须在**根包**（默认扫描同级及子包）；`@SpringBootApplication` 默认含 `@ComponentScan`，显式加 `@ComponentScan` 会覆盖默认 |
| 三层架构、Controller/Service/Repository 写法、Entity/DTO/VO 分层、包命名、依赖方向 | `references/02-layered-arch.md` | Service 不直接返回 Entity；Controller 只做协议适配；依赖方向单向（Controller→Service→Repository） |
| `@ConfigurationProperties` vs `@Value`、松散绑定、SpEL、profile、`@Profile`、配置读不到 | `references/03-config-properties.md` | `@Value` 不支持松散绑定与 `@Validated` 校验；静态字段注入须走构造器/setter；`@Value("${x}")` 读不到时查 key 拼写/profile/占位符 |
| 参数校验、`@Valid` vs `@Validated`、分组校验、`@RequestBody`/`@RequestParam`/`@PathVariable`、自定义校验器、校验不触发 | `references/04-validation.md` | **`@Validated` 标在类上不触发分组校验，须标在参数前并指定 groups**；`@Valid` 无分组能力；方法参数校验须 `@Validated` + `@Valid` 配合；非 Bean 参数（`@RequestParam`/`@PathVariable`）须类级 `@Validated` |
| 全局异常、`@RestControllerAdvice`、`@ExceptionHandler`、`ResponseEntity`、统一返回体、未知异常兜底 | `references/05-exception-handling.md` | **`@ExceptionHandler` 按异常类型「最近匹配」，父类会吞子类**；多个 Advice 按 `@Order`；`HandlerExceptionResolver` 链顺序 |
| 事务、`@Transactional`、自调用失效、传播行为、回滚规则、`rollbackFor` | `references/06-transaction.md` | `private`/`static`/`final` 方法代理失效；自调用 / rollbackFor 见强约束 2/3 |
| 异步 `@Async`、线程池、`SimpleAsyncTaskExecutor`、定时 `@Scheduled`、cron、`@EnableAsync`/`@EnableScheduling` | `references/07-async-schedule.md` | `@Scheduled` cron **不补年份**（6 字段）；`@Async` 默认线程池 + 自调用见强约束 2/4 |
| 事件、`@EventListener`、`@TransactionalEventListener`、`ApplicationEventPublisher`、同步/异步事件 | `references/08-events.md` | `@EventListener` 默认**同步且无事务阶段**；`@TransactionalEventListener` 默认 `AFTER_COMMIT`，事务回滚则不触发 |
| 依赖注入、构造器 vs `@Autowired` vs `@Resource`、`@Qualifier`、循环依赖、`@Lazy`、`BeanCurrentlyInCreationException` | `references/09-autowiring.md` | 推荐构造器注入；循环依赖禁令见强约束 8 |
| 条件装配、`@Conditional`/`@ConditionalOnClass`/`@ConditionalOnProperty`/`@ConditionalOnBean`/`@Profile`、自动装配、starter 制作、Bean 生命周期 | `references/10-condition-bean.md` | 3.x 起用 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（取代 2.x 的 `spring.factories`）；`@ConditionalOnBean` 有顺序依赖陷阱（条件求值在 Bean 定义注册阶段，Bean 可能未注册） |
| SpringDoc / OpenAPI 3、`@Operation`/`@Schema`/`@Parameter`、接口文档、JWT 鉴权配置 | `references/11-springdoc.md` | SpringBoot 3.x 用 `springdoc-openapi-starter-webmvc-ui`（非 `springdoc-openapi-ui`） |
| 横向隐性陷阱合集（跨上述主题的高频误用、启动报错速查） | `references/12-pitfalls.md` | 生成代码前必对照 |

## 主动行为触发（代码审查护栏）

> 以下代码模式命中时主动提醒用户；更完整的强制规则见「核心强约束」。

| 代码模式 | 主动提醒 |
|---------|---------|
| `@Transactional` 标在 `private` / `static` / `final` 方法 | 代理失效，事务不生效 → 见 `06-transaction.md` |
| 同类内 `this.xxx()` 调用带 `@Transactional` / `@Async` / `@EventListener` 的方法 | 自调用不走代理，注解失效 → 见 `06-transaction.md` / `07-async-schedule.md` |
| `@Async` 未配自定义 `ThreadPoolTaskExecutor` | 默认 `SimpleAsyncTaskExecutor` 每次新建线程，高并发打爆 → 见 `07-async-schedule.md` |
| `@ExceptionHandler(Exception.class)` 写在子异常之后 | 父类吞子类，子异常处理器永不执行 → 见 `05-exception-handling.md` |
| `@Validated` 标在类上但参数未加 `@Valid`，且用了 groups | 分组校验不触发 → 见 `04-validation.md` |
| `@Value` 注入静态字段 | 静态字段注入失效（须构造器/setter 中转）→ 见 `03-config-properties.md` |
| `spring.factories` 配自动装配（SpringBoot 3.x 项目） | 3.x 已废弃，改用 `AutoConfiguration.imports` → 见 `10-condition-bean.md` |
| Controller 方法返回 Entity | 泄漏数据库字段，应返回 VO/DTO → 见 `02-layered-arch.md` |
| `@Scheduled(fixedRate=...)` 多任务同线程 | 默认单线程串行，长任务阻塞其他任务 → 见 `07-async-schedule.md` |

## 核心强约束（Agent 必须遵守）

1. **先判 SpringBoot 版本与命名空间**：3.x 起全 `jakarta.*`；`javax.*` 与 `jakarta.*` 不可混用。读不到版本时**一次问全**（版本 + JDK），不分多轮。
2. **自调用不走代理**：`@Transactional` / `@Async` / `@EventListener` / `@Cacheable` 等 AOP 注解，同类内 `this.method()` 调用**全部失效**。解法优先级：**① 拆到另一个 Bean（推荐，架构清晰）** > ② 注入自身代理 `@Lazy`（须手写构造器，`@RequiredArgsConstructor` 不传 `@Lazy` 会启动报循环依赖）> ③ `AopContext.currentProxy()`（不推荐，须 `@EnableAspectJAutoProxy(exposeProxy=true)`，侵入性强）。
3. **`@Transactional` 默认只回滚 `RuntimeException` + `Error`**：受检异常（`IOException` / `SQLException`）默认**提交不回滚**。须显式 `@Transactional(rollbackFor = Exception.class)`。
4. **`@Async` 必须自定义线程池**：默认 `SimpleAsyncTaskExecutor` 每次新建线程不复用，生产环境高并发必打爆。须定义 `@Bean ThreadPoolTaskExecutor` 并 `@Async("executor名")` 指定。
5. **`@ExceptionHandler` 就近匹配**：父类异常（`Exception.class`）必须写在最后，否则吞掉所有子类异常处理器。多个 `@RestControllerAdvice` 用 `@Order` 控制优先级。
6. **校验须 `@Validated` + `@Valid` 配合**：Bean 参数（`@RequestBody`）加 `@Valid` 即触发校验；非 Bean 参数（`@RequestParam`/`@PathVariable`）须**类级** `@Validated` + 字段级约束注解；分组校验须**参数前** `@Validated(Group.class)`（类级 `@Validated` 不触发分组）。
7. **Controller 不返回 Entity**：返回 `VO` / `DTO`（`02-layered-arch.md`）。Entity 直返泄漏数据库结构、产生循环引用（`@ManyToOne` 懒加载序列化触发 N+1）。
8. **SpringBoot 2.6+ 默认禁用循环依赖**：启动直接报 `BeanCurrentlyInCreationException`。解法：重构为构造器注入 + `@Lazy`，或 `spring.main.allow-circular-references=true`（不推荐，掩盖设计问题）。
9. **3.x 自动装配改 `AutoConfiguration.imports`**：`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（每行一个全限定类名），取代 2.x 的 `META-INF/spring.factories` 里的 `EnableAutoConfiguration` key。
10. **SpringDoc 跨版本依赖不同**：SpringBoot 2.x 用 `springdoc-openapi-ui`；3.x 用 `springdoc-openapi-starter-webmvc-ui`。**不引入 Knife4j**（已停更）。

## 关键决策检查点（生成代码前必须确认）

以下场景存在多条技术路线，Agent **不可擅自替用户选择**。须先简要说明选项差异，确认方向后再编码。

| # | 触发信号 | 必须确认的问题 | 选项差异 | 默认推荐（用户未指定时） |
|---|---------|-------------|---------|----------------------|
| C1 | 需要全局异常处理 | ① 统一返回体格式（团队是否已有 `Result<T>` / `R<T>` 约定）？ | **统一返回体 + `@RestControllerAdvice`**（推荐）：包装所有响应，前端按 code 判断<br>**`ResponseEntity` 直接返回**：HTTP 语义清晰，RESTful 风格 | 跟随项目既有约定（grep 现有 Controller 返回类型）；无约定 → 统一返回体 |
| C2 | `@Async` 异步 | ① 是否需要自定义线程池？② 是否需要异常回调？ | **默认 `SimpleAsyncTaskExecutor`**（✗ 反模式，不复用线程）<br>**自定义 `ThreadPoolTaskExecutor`**（推荐）：可控并发数、队列、拒绝策略<br>**`CompletableFuture`**：需返回值 + 编排 | 自定义 `ThreadPoolTaskExecutor` |
| C3 | `@Transactional` 传播行为 | ① 当前方法是否在已有事务中被调用？ | **REQUIRED**（默认）：有则加入，无则新建<br>**REQUIRES_NEW**：总是新建（独立提交/回滚，不影响外层）<br>**NESTED**：保存点嵌套（部分回滚） | REQUIRED（多数场景）；独立日志/审计 → REQUIRES_NEW |
| C4 | 事件机制 | ① 事件是否需在事务提交后触发？ | **`@EventListener`**：同步、无事务感知<br>**`@TransactionalEventListener(AFTER_COMMIT)`**：事务提交后才触发（推荐，避免回滚后仍发事件） | 涉及事务 → `@TransactionalEventListener`；纯解耦 → `@EventListener` |
| C5 | 配置读取 | ① 配置项数量？② 是否需校验/分组？ | **`@Value`**：单值、简单、无校验、无松散绑定<br>**`@ConfigurationProperties`**：结构化、可校验、松散绑定（推荐 ≥3 项） | ≥3 项 → `@ConfigurationProperties`；1~2 项单值 → `@Value` |
| C6 | 循环依赖报错 | ① 是否必须循环（设计问题）？ | **重构消除**（推荐）：拆第三方 Bean、改单向依赖<br>**`@Lazy`**：临时打破启动期循环<br>**`allow-circular-references=true`**：放开全局禁令（掩盖问题） | 重构消除；无法重构 → `@Lazy` |

> **执行规则**：
> 1. 检测到触发信号 → 先向用户提出确认问题，**不要直接生成代码**。
> 2. 用户未明确回答 → 使用「默认推荐」列的策略，但在输出中标注"未确认，已使用默认方案"。
> 3. 用户确认方向 → 按选择生成代码，不再追问。
> 4. 一个需求命中多个检查点 → 逐一确认，全部完成后一次性生成代码。

## 使用流程

1. **确认适用性**：先执行「第 0 步：版本探测与边界判定」，再对照「何时使用本技能」；不适用 → 告知用户属哪个技能范围并建议切换。
2. **关键决策检查点**：查表命中触发信号 → 先向用户确认方向，**不要直接生成代码**。
3. **定位 reference**：查「决策路由」表，读对应文件。
4. **编码前看强约束**：尤其「自调用不走代理」「`@Transactional` 默认不回滚受检异常」「`@Async` 须自定义线程池」。
5. **遇报错先查排错**：`references/12-pitfalls.md`。
6. **输出前自检**：对照「核心强约束」10 条逐项核对。

