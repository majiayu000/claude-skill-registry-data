---
name: sa-token-dev
description: >-
  Sa-Token（cn.dev33）Java 权限认证框架开发助手。
  在 Java / Spring Boot 项目中开发任何登录、注册、登出、认证、鉴权、权限、角色、token、
  会话管理、接口保护、路由拦截、SSO 单点登录、OAuth2.0、JWT、踢人下线、账号封禁、记住我、
  二级认证、多账号体系、微服务网关鉴权相关功能时使用本技能——无论用户是否提到 Sa-Token
  （login / logout / authentication / authorization / permission / role / session / JWT /
  SSO / access control）。
  项目依赖已含 sa-token（sa-token-spring-boot*-starter 系列，覆盖 SpringBoot 2/3/4 与
  WebFlux 响应式变体）或代码出现 StpUtil / StpInterface / @SaCheckLogin / @SaCheckPermission /
  @SaCheckRole / SaInterceptor / SaRouter / SaSession 时必须使用本技能；
  项目尚无任何认证框架时，先主动询问用户是否引入 Sa-Token 再开发。
  不适用于：已使用 Spring Security / Shiro 的项目（不建议迁移）、纯 JWT 自实现方案、非 Java 语言。
agent_created: true
version: 2.3.0
slug: sa-token-dev
displayName: Sa-Token 开发助手
---

# Sa-Token 开发助手

面向日常 Java 开发的 Sa-Token 编码助手。推荐 **1.46.0+**（最新稳定版），**1.40.x 及以上全线适用**。版本基准以本声明为准，references 不再重复标注；功能级版本差异已在文中以 `v1.xx.0+` 标注。
采用**完全本地自包含**策略：所有知识沉淀于本地 `references/`，运行时不依赖任何外部文档站点。

## 版本与依赖

| SpringBoot | starter 坐标 | 环境 |
|---|---|---|
| 2.x | `sa-token-spring-boot-starter` | Servlet (SpringMVC) |
| 3.x | `sa-token-spring-boot3-starter` | Servlet (SpringMVC) |
| 4.x | `sa-token-spring-boot4-starter` | Servlet (SpringMVC) |
| 2.x (响应式) | `sa-token-reactor-spring-boot-starter` | WebFlux / Gateway |
| 3.x (响应式) | `sa-token-reactor-spring-boot3-starter` | WebFlux / Gateway |
| 4.x (响应式) | `sa-token-reactor-spring-boot4-starter` | WebFlux / Gateway |

- **切勿**同时引入 `sa-token-spring-boot-starter` 和 `sa-token-reactor-spring-boot-starter`，项目无法启动。
- **Redis 集成**：引 `sa-token-redis-template` + `commons-pool2`，分布式场景必须。
- **SpringBoot 3.x**：Redis 前缀从 `spring.redis` 改为 `spring.data.redis`。
- 微服务网关用 Reactor 依赖，子服务用 Servlet 依赖，**不要在父 pom 统一引入**。

## 第 0 步：依赖探测与激活分支

任务涉及登录、注册、认证、鉴权、权限、token、会话、SSO、OAuth2 等编码——**即使用户没提 Sa-Token**——先检索项目依赖（在 `pom.xml` / `build.gradle` 中搜 `sa-token`、`spring-security`、`shiro`）：

| 探测结果 | 动作 |
|---|---|
| 依赖含 `sa-token-*` | 直接激活本技能，走下方流程 |
| 无 sa-token，也无 Spring Security / Shiro | **主动询问**用户是否引入 Sa-Token（轻量、零配置可启动，登录/权限/SSO/OAuth2 一站式）；同意 → 按「版本与依赖」表 + `references/01-setup.md` 引入后继续；拒绝 → 退出本技能，不再打扰 |
| 已使用 Spring Security / Shiro | 告知不适用并退出，**不建议迁移** |

## 何时使用本技能

| 信号 | 判定 |
|------|------|
| Java/SpringBoot 项目中的登录/注册/认证/鉴权/权限/token/会话/SSO 任务（未指明框架） | 激活，先执行「第 0 步」依赖探测 |
| 依赖含 `sa-token-*` / 代码用 `StpUtil` / `SaInterceptor` / `SaRouter` | 激活 |
| 提到 `@SaCheckLogin` / `@SaCheckPermission` / `@SaCheckRole` / `@SaIgnore` / "Sa-Token" / "sa-token" | 激活 |
| SSO 单点登录 / OAuth2.0 / 微服务网关鉴权 / JWT / API-Key / API 签名 | 激活 |
| 已使用 Spring Security / Shiro 的项目 | 不适用（不建议迁移） |
| 非 Java 语言（Go / Python / Node.js） | 不适用 |
| 纯 JWT 自实现（无 Sa-Token 依赖） | 不适用 |

> **检查点**：判定为「不适用」→ 告知用户当前问题不在 Sa-Token 范围，建议退出本技能。

## 关键决策检查点

以下 6 个场景存在多条技术路线，Agent **不可擅自替用户选择**。

**执行规则（机械判据，逐条执行）：**

1. 拿到任务后、写任何代码前，先扫描用户消息与上下文是否命中下表「触发信号」列的关键词（逐字匹配）。
2. 命中任一检查点 → **本轮回复只做一件事：输出确认问题**。禁止输出业务代码块、依赖坐标、配置片段。
3. 确认问题必须是**选择题**：列出候选方案（A/B/C）+ 标注推荐项 + 一句话理由。禁止开放式提问（如"你想怎么做认证？"）。
4. 用户未明确回答 → 使用「默认推荐」列策略，并在输出开头标注「未确认，已使用默认方案」。
5. 用户确认方向 → 按选择生成代码，不再重复追问。
6. 一个需求命中多个检查点 → 一次性列出全部确认问题，全部完成后才生成代码。

| # | 触发信号（逐字关键词） | 必须确认的问题 | 方案差异（一句话） | 默认推荐（用户未指定时） |
|---|---------|-------------|---------|----------------------|
| C1 | "JWT" / "无状态" / "不要 Redis" / "水平扩展" / "token 风格" / "自包含 token" | ① 是否要无状态（不依赖 Redis）？② 是否要 JWT 风格 token（自包含/可读）？ | 有状态默认 **simple-uuid**（不引 JWT，功能完整）；有状态 + JWT = Simple；无状态 = Stateless JWT（不支持踢人/Session/active-timeout）；Mixin = JWT+Redis 内嵌。详见 `references/14-plugin.md` | **有状态 + simple-uuid**；用户显式声明"无状态/不要 Redis" 视为已确认，直接 Stateless |
| C2 | "SSO" / "单点登录" | ① 各子系统前端是否同域？② 各子系统后端是否共享同一 Redis？ | 模式一：同域+同 Redis（共享 Cookie）；模式二：跨域+同 Redis（URL 重定向 + Ticket）；模式三：跨域+异 Redis（HTTP 请求校验）。详见 `references/12-sso-oauth2.md` | 按条件自动判定（同域同 Redis → 模式一） |
| C3 | "登录" / "认证"（未明确前后端分离） | ① 前端是浏览器渲染页面，还是 App/小程序/SPA？② 是否前后端分离？ | **Cookie 模式**：浏览器自动管理，login() 后自动注入；**Header 模式**：前后端分离，后端返回 tokenValue，前端塞 header | Cookie（浏览器）；Header（前后端分离/App/小程序） |
| C4 | "鉴权" / "权限" / "保护接口" | ① 需要粗粒度（路径级）还是细粒度（接口/方法级）？② 是否有全局白名单？ | **路由拦截**：SaInterceptor + SaRouter，粗粒度；**注解**：@SaCheck*，细粒度；可混用 | **混用**（路由全局白名单 + 注解细粒度） |
| C5 | "微服务" / "网关" | ① 是否需要无状态（不依赖 Redis）？② 是否需要踢人/active-timeout？ | **Redis 方案**：有状态，功能完整（推荐）；**JWT Stateless**：无 Redis，但不支持踢人/active-timeout | **Redis 方案** |
| C6 | "多账号" / "多体系" / "多端" | ① 需要几套独立登录体系？② 各体系是否需要不同 timeout/配置？ | **StpKit 门面**：每体系独立 StpLogic，可独立配置；**单账号 + device**：同一体系区分设备类型 | 按体系数量决定（≥2 套 → StpKit） |

## 决策路由

| 需求场景（关键词） | 读取文件 |
|---|---|
| 依赖、starter 选择、yml 配置、生产配置清单 | `references/01-setup.md` |
| 登录、登出、会话查询、Token 查询、timeout vs active-timeout、登录流程 | `references/02-login-auth.md` |
| 权限认证、角色认证、StpInterface、通配符、RBAC 权限模型 | `references/03-permission.md` |
| 注解鉴权（@SaCheck*、SaMode、orRole、@SaIgnore、@SaCheckOr）、注解 vs 路由选型 | `references/04-annotation.md` |
| 路由拦截鉴权（SaInterceptor / SaRouter / match / free / stop / back）、全局白名单 | `references/05-interceptor-route.md` |
| Session 会话（Account/Token/Custom）、三大作用域 | `references/06-session.md` |
| 集成 Redis、前后端分离 token 传递、Redis 部署模式 | `references/07-redis-frontsep.md` |
| StpUtil 常用 API（登录/踢人/封禁/二级认证/身份切换/多账号） | `references/08-api-stputil.md` |
| 排错：NotLoginException 场景值、异常码、注解不生效、跨域、反代 uri、过滤器异常 | `references/09-pitfalls.md` |
| Agent 常见错误与最佳实践（28 条 antipattern） | `references/10-antipattern.md` |
| 高级特性：记住我、同端互斥、账号封禁、二级认证、身份切换、多账号、密码加密、Token 风格/前缀、全局侦听器/过滤器、Http Basic/Digest | `references/11-advanced.md` |
| SSO 单点登录（三种模式）、OAuth2.0（四种授权模式）、SSO vs OAuth2 选型 | `references/12-sso-oauth2.md` |
| 微服务：分布式 Session、网关统一鉴权、内部服务隔离（Same-Token）、依赖引入 | `references/13-micro-service.md` |
| 插件：JWT、API-Key、API 签名、AOP 注解、临时 Token、Alone Redis、SpEL 表达式 | `references/14-plugin.md` |

## 核心强约束

1. **先注册拦截器再用注解**：`@SaCheck*` 注解依赖 `SaInterceptor`，默认关闭。必须先 `registry.addInterceptor(new SaInterceptor()).addPathPatterns("/**")` 注册，注解才生效。高版本 SpringBoot（≥2.6.x）可能需额外加 `@EnableWebMvc`。
2. **SaSession ≠ HttpSession**：`StpUtil.getSession()` 返回的 `SaSession` 与 `HttpSession` 无任何关系，互不通。用 Sa-Token 时统一使用 `SaSession`，不要混用。
3. **权限校验后端必须做**：前端按钮级权限只是辅助显示，后端接口必须用 `StpUtil.checkPermission()` 或 `@SaCheckPermission` 再次校验。
4. **实现 StpInterface 才能鉴权**：权限/角色校验依赖 `StpInterface` 实现类（`@Component`），返回权限码和角色集合。不实现则所有权限/角色校验通过。
5. **timeout vs active-timeout 独立**：`timeout` 是长久有效期（默认 30 天），`active-timeout` 是最低活跃频率（超时冻结）。两者独立，任一过期 token 不可用。`-1` 代表永久/不限制。
6. **踢人 vs 注销 vs 顶人不同**：`logout`=正常退出；`kickout`=被动踢下线（场景值 -5）；`replaced`=被顶下线（场景值 -4）。`is-share` 和 `is-concurrent` 配置影响行为。
7. **封禁需先踢下线**：`StpUtil.disable(id, time)` 不会自动让已登录用户下线。需先 `StpUtil.kickout(id)` 再 `disable`。v1.31.0+ `login()` 不再自动校验封禁，需显式 `checkDisable`。
8. **Starter 不可混用**：`sa-token-spring-boot-starter`（Servlet）和 `sa-token-reactor-spring-boot-starter`（Reactor）不可同时引入同一项目。
9. **前后端分离需手动传 token**：Cookie 模式自动注入；前后端分离（App/小程序）需后端返回 `SaTokenInfo`，前端塞 header（参数名即 `tokenName`，默认 `satoken`）。
10. **过滤器异常不进 @ExceptionHandler**：`SaServletFilter` / `SaReactorFilter` 中抛出的异常不进入 Spring 全局异常处理器，必须通过 `.setError()` 处理。
11. **Redis 前缀注意版本**：SpringBoot 2.x 用 `spring.redis.*`，SpringBoot 3.x 用 `spring.data.redis.*`。配错导致连接失败。
12. **JWT 是可选 token 风格，与有状态/无状态正交**：有状态场景默认用 Sa-Token 原生 `simple-uuid` token 风格 + Redis 即可，**无需引入 JWT**；仅当用户要 JWT 自包含/可读格式时引入 `sa-token-jwt`（Simple 模式，JWT + Redis）。无状态场景必须 JWT（`StpLogicJwtForStateless`，不要 Redis，不支持踢人/active-timeout）。Mixin 才同时需要 JWT + Redis（登录数据内嵌 Token）。**不要默认假设用 JWT。**

## 使用流程

1. **确认适用性**：先执行「第 0 步：依赖探测与激活分支」，再对照「何时使用本技能」；依赖缺失时主动询问是否引入 Sa-Token，不适用 → 告知用户并建议退出。
2. **关键决策检查点**：逐字扫描 C1–C6 触发信号；命中 → 本轮只输出确认选择题，禁止生成代码。
3. **定位 reference**：查「决策路由」表，读对应文件。
4. **编码前看 antipattern**：对照 `10-antipattern.md` 常见错误。
5. **编码遵循强约束**：先读 12 条核心强约束，再给代码。
6. **遇异常先查排错**：`references/09-pitfalls.md`。
7. **输出前自检（二值核对，任一为「否」即违规，必须返工）**：
   - C1–C6 已逐项扫描：命中的检查点均已确认，或已按执行规则 4 标注默认方案？
   - starter 对应 SpringBoot 版本，Servlet / Reactor 未混用？
   - `@SaCheck*` 使用处已注册 `SaInterceptor`？
   - 前后端分离场景已返回 tokenValue？
   - SaSession 未与 HttpSession 混用？
   - Redis 前缀对应 SpringBoot 版本？
   - 封禁流程已先 kickout 再 disable，登录前已 checkDisable？
   - 过滤器已配 `.setError()`？
   - JWT 仅在用户要 JWT 格式或无状态时引入（默认 simple-uuid）？

## 版本注意

- **前向兼容**：新版本 API 签名变更以官方 `StpUtil` 源码为准，本 skill 未覆盖的新增功能参考 `sa-token.com` 官方文档。
- **1.46.0 升级必查**：`StpInterface.isDisabled` 改 3 参（`11-advanced.md` §3.5）；`allowLoginIdColon` 默认禁 loginId 冒号（`09-pitfalls.md` §10）；JWT `extraData` 禁保留字段（`14-plugin.md`）。
- `sa-token-jwt` 显式依赖 `hutool-jwt`，hutool 5.8.13/5.8.14 存在类型转换问题，建议避开。
