---
name: java-springboot-standards-skill
description: >-
  Java Spring Boot 2.7+/3.x 单体与微服务后端的新建、实现、重构和审查规范。适用于 Controller/Service/Mapper 分层、DTO/VO、参数校验、统一异常、MyBatis/MyBatis-Plus、联表查询、N+1 治理、分页、安全脱敏、事务并发、状态机和 Spring Cloud 中间件；Spring AI 仅在项目已有依赖或用户明确提出 AI/智能体/RAG/工具调用需求时适用。不适用于非 Spring Java 工具、前端页面、纯运维部署和数据库 DBA 专项问题。
---

# /java-springboot-standards-skill — Spring Boot 单体、微服务、Spring AI 与安全合规开发规范

本 Skill 是面向企业级 **Java Spring Boot 单体架构（Monolith & Modular Monolith）**、**微服务架构（Spring Cloud Alibaba）**、**Spring AI 智能体体系** 与 **Spring Security 安全合规防护** 的全栈开发与审查规范，提供从工程脚手架、软件包分层、六端接口隔离、数据流转、统一上下文、安全防御体系、AI 智能体与微服务联动到 Javadoc/步骤化业务注释的闭环标准。

---

## 1. 按需适配与反过度设计铁律 (Zero Over-Engineering)

**【核心纪律】严禁凭空给不需要的项目堆砌无关技术栈！**

Agent 在为工程生成代码或包结构时，必须严格基于**当前项目的 `pom.xml` 依赖与用户的实际需求**进行按需匹配：
1. **普通单体项目 (无 AI)**：
   * 只生成/遵循经典的 MVC / DDD 规范包结构（`controller`, `service`, `mapper`, `model.{domain,dto,vo}`）。
   * **绝对禁止**创建 `agent/`, `advisor/`, `tools/`, `memory/` 等 AI 目录；**绝对禁止**引入 Spring AI 依赖或编写智能体/大模型相关代码。
2. **普通微服务项目 (无 AI)**：
   * 只生成/遵循微服务标准治理（Feign, Nacos, Seata, Redisson, RabbitMQ, XXL-Job）。
   * **绝对禁止**无端引入 AI 模块。
3. **AI 赋能项目 (明确包含 Spring AI / LLM 需求)**：
   * 仅在存在 `spring-ai` 相关依赖或用户明确要求 AI / 智能体 / RAG / 工具调用场景时，方可按需启用 `agent/`, `tools/`, `advisor/` 及流式 SSE 规范。

---

## 2. 触发场景 (Trigger)

当用户或 Agent 在处理以下任何场景时必须激活本 Skill：
* **Spring Boot 架构与分层接口开发**：创建或重构单体模块、Maven 多模块工程、通用 Starter、Feign 契约层，以及编写 Controller、Service、Mapper、Domain/DTO/VO、参数校验、统一响应与异常、六端路由划分。
* **数据建模与数据流转**：设计实体字段、审计字段、Entity/DTO/VO 契约、分页查询、MyBatis/MyBatis-Plus 映射、联表查询、多表装配、N+1 查询治理、状态数据、用户归属和订单快照等数据规范。
* **安全防护与合规审查**：配置 Spring Security、JWT 身份认证、`@PreAuthorize` 方法级鉴权、SQL 注入与 XSS 防御、PII 数据脱敏、接口限流、上线前安全审查。
* **事务、并发与中间件治理**：处理本地/分布式事务、Redis + Lua 原子扣减、Redisson 分布式锁、状态机、Canal + ElasticSearch 同步、RabbitMQ、XXL-Job 等 Spring Cloud 组件。
* **Spring AI 与智能体开发**：仅在项目已有 Spring AI 依赖或用户明确提出 AI/智能体/RAG/工具调用需求时，构建 Multi-Agent、`@Tool` 微服务工具链、SSE 流式响应、RedisChatMemory 与 Token 优化 Advisor。
* **代码审查与注释规范**：为 Java 代码补充/审查 Javadoc、消除注释噪音、添加序号化分步业务注释（`// 1. 数据校验` ... `// 2. 状态机流转`）。

---

## 3. 架构选型与形态决策 (Architecture Decision)

在开展代码编写前，首先依据项目规模与部署形态确定技术选型模式：

```text
                                  [ 项目架构决策 ]
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
         【 单体 / 模块化单体 】                         【 微服务集群体系 】
   (小型/中型系统，单一进程部署)                   (大型分布式系统，多独立微服务部署)
  ─────────────────────────────────               ─────────────────────────────────
  • 模块通信: Spring Bean 直接注入                • 模块通信: OpenFeign + Nacos 服务发现
  • 异步解耦: Spring Event 事件总线               • 异步解耦: RabbitMQ 延迟/死信队列
  • 事务一致: 本地 @Transactional                 • 事务一致: Seata @GlobalTransactional
  • 缓存与锁: Caffeine / Redis / JVM锁            • 缓存与锁: Redis 多级缓存 + Redisson @Lock
  • 认证授权: Filter + SecurityContext            • 认证授权: Gateway 网关统一鉴权 + Header 透传
  • 安全防御: 严格参数化绑定 + XSS 清洗           • 安全防御: /inner/** 网关隔离 + SQL/XSS 全链路防御
  • AI 智能体: 仅在有AI需求时按需注入             • AI 智能体: 仅在有AI需求时以独立服务接入
  • 定时任务: Spring Task @Scheduled              • 定时任务: XXL-Job 分布式分片调度
  • 契约分层: 内部 service 接口共享              • 契约分层: 独立 api 模块暴露 Feign 契约
```

详细对比与选型细节参见 ➔ [references/architecture_modes.md](references/architecture_modes.md)。

---

## 4. 核心分层与包结构原则 (Layering Principles)

无论单体还是微服务，代码包结构均必须遵循严格的职责边界（AI 相关目录仅在 AI 项目中按需出现）：

```text
com.<company>.<project/service>
├── advisor/          # [仅AI项目按需] Spring AI 拦截器 (Token优化/上下文记录)
├── agent/            # [仅AI项目按需] 智能体体系 (RouteAgent, AbstractAgent, 领域智能体)
├── client/           # 外部 HTTP/RPC/第三方 API 客户端封装
├── config/           # Spring 核心配置、Security 过滤器与 Bean 注入
├── constants/        # 业务常量与缓存 Key (RedisConstants, ErrorInfo)
├── controller/       # 控制器层 (严格按端隔离，禁止多端混写)
│   ├── agency/       # 机构端 / B端商户端接口 (/agency/**)
│   ├── consumer/     # C端用户 / 小程序端 / APP端接口 (/consumer/**)
│   ├── inner/        # 内部/服务间 Feign 专用接口 (/inner/**，网关拦截对外暴露)
│   ├── open/         # 开放免认证接口 (/open/**，如登录、短信验证码、公开配置)
│   ├── operation/    # 运营端 / 平台管理后台接口 (/operation/**)
│   └── worker/       # 服务人员端 / 师傅履约端接口 (/worker/**)
├── enums/            # 业务枚举类 (状态机事件、业务状态、业务类型)
├── handler/          # 任务处理器 (XXL-Job Handler、Canal 数据同步处理器)
├── listener/         # 监听器 (RabbitMQ 消息监听、Spring Event 监听)
├── mapper/           # MyBatis-Plus BaseMapper 接口及 XML 映射文件
├── memory/           # [仅AI项目按需] 分布式会话记忆 (RedisChatMemory)
├── model/            # 领域模型 (分层对象严禁混用)
│   ├── domain/       # 数据库持久化实体 Entity (@TableName)
│   ├── dto/          # 数据传输对象 (request/*ReqDTO, response/*ResDTO, *QueryDTO)
│   └── vo/           # 视图展示对象 (*VO, ChatEventVO)
├── properties/       # 配置属性映射类 (@ConfigurationProperties)
├── service/          # 业务逻辑接口 (I*Service)
│   └── impl/         # 业务逻辑实现类 (*ServiceImpl)
├── strategy/         # 策略与规则实现 (派单规则链、计费策略、取消策略等)
└── tools/            # [仅AI项目按需] Spring AI @Tool 工具链与结构化出参 (tools/result)
```

详细包结构与对象生命周期流转规范参见 ➔ [references/layering_and_packages.md](references/layering_and_packages.md)。

---

## 5. 黄金编码纪律 (Golden Rules)

1. **用户上下文绝对隔离**：已登录接口**严禁在请求体/URL中显式传递 `userId`**，必须统一通过 `UserContext.currentUserId()` / `UserContext.currentUser()` 从线程上下文中获取。
2. **控制器响应自包装与 `@NoWrapper` 穿透**：Controller 方法直接返回具体 DTO/VO，框架统一自动包装为 `Result<T>`；对于 **SSE 流式响应（`Flux<ChatEventVO>`）或文件下载，必须添加 `@NoWrapper` 注解**跳过统一包装。
3. **实体绝不外露**：`model.domain.Entity` 严禁直接作为 Controller 返回值，严禁作为 Feign API 参数暴露，出入参必须转换至 `DTO/VO`。
4. **统一异常与 600+ 错误码**：
   * 参数不合法：`throw new BadRequestException("错误原因");`
   * 操作受限/禁止：`throw new ForbiddenOperationException("禁止原因");`
   * 自定义业务异常：`throw new CommonException(ErrorInfo.Code.XXX, ErrorInfo.Msg.YYY);`
5. **复杂业务序号化步骤注释**：核心方法内部必须按执行逻辑进行序号化分步注释（如 `// 1. 数据校验`、`// 2. 状态机流转`、`// 3. 业务持久化`、`// 4. 发送异步通知`），对非显然约束明确解释 **Why（为什么这样做）**。
6. **SQL 注入与参数安全铁律**：MyBatis XML 与代码中必须使用 `#{}` 参数绑定，绝对禁止 `${}` 拼接 SQL；动态排序必须经过白名单校验；查询优先使用 `lambdaQuery()`。
7. **敏感信息脱敏与密钥隔离**：禁止在代码和配置文件中提交明文密码/私钥；日志中禁止打印明文密码与完整 Token；手机号、身份证等 PII 信息强制脱敏输出。
8. **AI 工具与微服务联动规范 (仅限AI场景)**：Spring AI 的 `@Tool` 工具类应直接注入微服务 Feign Client，利用 `ToolContext` 接收上下文，并通过 `ToolResultHolder` 将结构化业务卡片以 `PARAM` 事件透传给前端渲染。
9. **状态变更受控**：关键状态（如订单、支付、认证状态）必须通过状态机或受保护方法更新，禁止业务代码任意 `update` 状态字段。
10. **高并发防御**：涉及库存、抢单、抢券等临界资源，必须使用 Redis + Lua 保证原子性或通过 Redisson `@Lock` 控制并发。

编码规范、命名规则与 Javadoc 详见 ➔ [references/coding_and_comment_standards.md](references/coding_and_comment_standards.md)。  
数据建模、数据流转、分页、MyBatis 映射、状态与敏感数据规范详见 ➔ [references/data_standards.md](references/data_standards.md)。  
安全防护、认证授权与合规审查详见 ➔ [references/security_and_compliance.md](references/security_and_compliance.md)。  
高级中间件、Spring AI 模式与实战代码范式详见 ➔ [references/patterns_and_middleware.md](references/patterns_and_middleware.md)。

---

## 6. 质量审查清单 (Review Checklist)

交付或审查代码前必须进行以下自检：

- [ ] **按需裁剪**：如果是普通单体/微服务（无 AI 需求），是否严格杜绝了 AI 相关的无用包和多余依赖？
- [ ] **分层定位**：Controller 是否放入正确的端目录（`agency/consumer/inner/open/operation/worker`）？
- [ ] **模型防漏**：是否杜绝了 `domain.Entity` 暴露给前端或跨服务 Feign 接口？
- [ ] **数据规范**：字段类型、审计填充、分页上限、SQL 参数绑定、状态受控变更、用户归属条件、敏感数据脱敏是否满足 [references/data_standards.md](references/data_standards.md)？
- [ ] **联表与 N+1**：是否杜绝循环逐条查询 Mapper/RPC/Redis？JOIN fan-out、分页口径、批量 `IN` 上限、索引和 `EXPLAIN` 执行计划是否已审查？
- [ ] **上下文安全**：是否存在请求参数接收 `userId` 的漏洞？是否使用 `UserContext` 获取当前用户？
- [ ] **安全与防注入**：是否杜绝了 SQL 字符串拼接（`${}`）？敏感端点是否具备 `@PreAuthorize` 守卫？
- [ ] **数据脱敏**：出参与日志中是否对手机号、身份证、密码等敏感信息进行了脱敏？
- [ ] **SSE 流式响应**：返回 `Flux<T>` 的接口是否标注了 `@NoWrapper` 与 `MediaType.TEXT_EVENT_STREAM_VALUE`？
- [ ] **异常与响应**：Controller 是否直接返回 DTO/PageResult？异常是否使用规范的异常类并携带错误码？
- [ ] **事务边界**：单体/单库事务是否标注 `@Transactional(rollbackFor = Exception.class)`？跨服务写操作是否标注 `@GlobalTransactional`？
- [ ] **并发安全**：修改共享资源是否加了分布式锁（`@Lock`）或原子 Lua 脚本？
- [ ] **注释质量**：类级 Javadoc、方法级 Javadoc 是否完整？复杂逻辑是否具备序号化分步注释与 Why 解释？
