---
name: shareflow-context
description: ShareFlow 项目全局上下文。执行任何 ShareFlow 开发任务前必须加载此 Skill，包含完整的架构规范、目录结构、编码约定和技术决策。
---

# ShareFlow 项目全局上下文

## 项目概述

ShareFlow 是短视频持股分红平台，采用**同一套代码库、双实例部署**策略：
- **境外实例（Overseas）**：TikTok / YouTube / Instagram / Kwai / 小红书海外版，USD 结算，客户端英文界面
- **境内实例（Domestic）**：抖音 / 快手 / 小红书，CNY 结算，客户端中文界面
- **管理后台（Admin）和销售端（Sales）无论境内外实例，统一使用中文界面**

通过环境变量 `REGION=overseas|domestic` 区分实例行为，数据库完全独立。

## 技术栈

### 后端
- **.NET 8** + ASP.NET Core Web API
- **EF Core 8** + PostgreSQL 16（Code First，迁移放 Migrator 项目）
- **Redis 7**（Token 黑名单、权限缓存、分布式锁）
- **Autofac**（IoC 容器，模块化注册）
- **Quartz.NET**（定时任务）
- **Serilog**（结构化日志）
- **FluentValidation**（请求校验）
- **Mapster**（DTO 映射，使用 IRegister 配置类 + IMapper 注入，禁止手动映射）
- **MediatR**（领域事件）
- **QuestPDF**（PDF 生成）

### 前端
- **Vue 3.5** + TypeScript 5 + Vite 6
- **Naive UI**（组件库）
- **Pinia**（状态管理，auth store 持久化）
- **Axios**（HTTP 请求，统一封装）
- **vue-i18n**（zh-CN / en-US）
- **ECharts 5**（图表）
- **Vee-Validate + Zod**（表单校验）

### 部署
- Docker + docker-compose（双套：overseas / domestic）
- Nginx（反向代理 + SPA fallback）

## 项目目录结构

### 后端（Clean Architecture）
```
back-end/
├── ShareFlow.sln
├── Dockerfile
└── src/
    ├── Api/
    │   ├── Program.cs
    │   ├── Controllers/
    │   │   ├── Admin/
    │   │   ├── Sales/
    │   │   ├── Client/
    │   │   └── ESign/
    │   ├── Filters/          ← PermissionFilter, AuditLogFilter
    │   ├── Middleware/        ← GlobalExceptionMiddleware, RequestLoggingMiddleware
    │   └── appsettings.json
    ├── Application/
    │   ├── ApplicationModule.cs
    │   ├── Common/            ← ApiResponse<T>, PagedResult<T>, BusinessException
    │   ├── Auth/
    │   ├── Admin/
    │   ├── Sales/
    │   ├── Client/
    │   ├── ESign/
    │   └── Internal/         ← 集团总览内部 API Service
    ├── Domain/
    │   ├── Entities/
    │   ├── Enums/
    │   ├── Interfaces/        ← IRegionContext, Repository 接口
    │   ├── Events/
    │   └── Exceptions/
    ├── Infrastructure/
    │   ├── InfrastructureModule.cs
    │   ├── Persistence/
    │   │   ├── AppDbContext.cs
    │   │   ├── Configurations/
    │   │   └── Repositories/
    │   ├── Services/          ← JwtService, RedisService, FileStorageService
    │   ├── AiSkills/          ← Claude Agent Skill 文件目录
    │   ├── ESign/             ← ESignService, ContractTemplateFactory
    │   └── Jobs/              ← Quartz 定时任务
    └── Migrator/
        ├── Migrations/
        └── DesignTimeDbContextFactory.cs
```

### 前端
```
front-end/
├── src/
│   ├── api/
│   │   ├── http.ts            ← Axios 封装（拦截器、401刷新、统一错误）
│   │   ├── auth.ts
│   │   ├── admin/
│   │   ├── sales/
│   │   └── client/
│   ├── components/
│   │   ├── base/              ← Naive UI 二次封装（AppTable, AppModal, AppForm...）
│   │   └── business/          ← 业务组件（SlotProgressBar, PlatformTag, SignaturePad...）
│   ├── composables/
│   │   ├── useRegion.ts
│   │   ├── usePagedList.ts
│   │   └── useForm.ts
│   ├── directives/
│   │   └── permission.ts      ← v-permission 指令
│   ├── i18n/
│   │   ├── zh-CN/
│   │   └── en-US/
│   ├── layouts/
│   │   ├── AdminLayout.vue
│   │   ├── SalesLayout.vue
│   │   ├── ClientLayout.vue
│   │   └── PublicLayout.vue
│   ├── router/
│   │   ├── index.ts
│   │   └── guards.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   ├── admin/
│   │   ├── sales/
│   │   └── client/
│   ├── types/
│   └── views/
│       ├── admin/
│       ├── sales/
│       ├── client/
│       ├── esign/             ← 公开签约页
│       └── auth/
├── .env.overseas
└── .env.domestic
```

## 编码规范

### 后端
- 所有金额 `decimal`，禁止 `float/double`
- 持股比例 `decimal(8,4)`，金额 `decimal(15,2)`
- 数据库列名 `snake_case`，C# 代码 `PascalCase`
- 禁止 Controller 直接使用 DbContext，必须通过 Repository
- 读查询一律 `AsNoTracking()`
- DTO 映射使用 Mapster `IRegister` 配置类 + `IMapper` 注入，**禁止手动 new DTO 赋值**
- 测试命名：`MethodName_StateUnderTest_ExpectedBehavior`
- 异常统一 `throw new BusinessException(errorCode, message)`
- 功能开关通过 `IRegionContext` 读取，**禁止硬编码 if(region == "overseas")**

### 前端
- 组件文件 `PascalCase.vue`，其他文件 `kebab-case`
- 所有 UI 文案使用 `$t('key')` 国际化
- 所有 Props 使用 TypeScript interface 定义
- 不直接使用 Naive UI 原始组件，统一使用 `components/base/` 封装版
- 权限控制使用 `v-permission="'permission.key'"` 指令

## API 规范
- 路径：`/v1/{module}/{resource}`，RESTful
- 响应：`ApiResponse<T> { code, message, data, traceId }`
- 分页：`PagedResult<T> { items, total, page, pageSize }`
- 认证：JWT Bearer（Access 2h + Refresh 7d）

## 关键架构接口

### IRegionContext
```csharp
public interface IRegionContext
{
    RegionMode Mode { get; }                        // Overseas | Domestic
    string DefaultCurrency { get; }                 // USD | CNY
    string DefaultLocale { get; }                   // en-US | zh-CN
    IReadOnlyList<string> EnabledPlatforms { get; }
    bool IsYouTubeOAuthEnabled { get; }
}
```

### ApiResponse<T>
```csharp
public class ApiResponse<T>
{
    public int Code { get; set; }
    public string Message { get; set; }
    public T? Data { get; set; }
    public string TraceId { get; set; }
    public static ApiResponse<T> Success(T data) { ... }
    public static ApiResponse<T> Fail(string message, int code = 400) { ... }
}
```

## 双实例环境变量

> **界面语言规则**：Admin 后台与 Sales 端无论哪个实例，**固定使用中文（zh-CN）**；仅 Client 客户端跟随 `CLIENT_LOCALE` 变量区分中英文。

| 变量 | 境外值 | 境内值 |
|------|--------|--------|
| REGION | overseas | domestic |
| DEFAULT_CURRENCY | USD | CNY |
| CLIENT_LOCALE | en-US（仅影响客户端） | zh-CN（仅影响客户端） |
| ENABLED_PLATFORMS | YouTube,TikTok,Instagram,Kwai,Xiaohongshu,BrandDeal | Douyin,Kuaishou,Xiaohongshu,BrandDeal |
| YOUTUBE_OAUTH_ENABLED | true | false |
| DOMESTIC_API_URL | https://domestic-api.example.com | — |
