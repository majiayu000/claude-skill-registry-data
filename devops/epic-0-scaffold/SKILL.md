---
name: epic-0-scaffold
description: 执行 Epic 0 —— ShareFlow 项目脚手架与基础设施搭建。包含后端 .NET 解决方案初始化、前端 Vue 项目初始化、Docker 双实例配置。执行前请先加载 shareflow-context Skill。
---

# Epic 0 — 项目脚手架与基础设施

## 前置条件
- 已读取 `shareflow-context/SKILL.md`
- 工作目录：项目根目录 `e:\duanshipinfenkong\`

## 执行顺序

### STEP 1：后端 .NET 解决方案

```bash
mkdir back-end && cd back-end

# 创建解决方案
dotnet new sln -n ShareFlow

# 创建各层项目
dotnet new webapi -n ShareFlow.Api --no-openapi -o src/Api
dotnet new classlib -n ShareFlow.Application -o src/Application
dotnet new classlib -n ShareFlow.Domain -o src/Domain
dotnet new classlib -n ShareFlow.Infrastructure -o src/Infrastructure
dotnet new classlib -n ShareFlow.Migrator -o src/Migrator
dotnet new xunit -n ShareFlow.Tests -o tests/UnitTests

# 添加到解决方案
dotnet sln add src/Api src/Application src/Domain src/Infrastructure src/Migrator tests/UnitTests

# 设置项目引用（Clean Architecture 方向）
dotnet add src/Api reference src/Application
dotnet add src/Application reference src/Domain
dotnet add src/Infrastructure reference src/Application
dotnet add src/Infrastructure reference src/Domain
dotnet add src/Migrator reference src/Infrastructure
dotnet add tests/UnitTests reference src/Application src/Domain
```

### STEP 2：安装 NuGet 包

**Api 项目：**
```bash
cd src/Api
dotnet add package Autofac.Extensions.DependencyInjection
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File
dotnet add package Swashbuckle.AspNetCore
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package FluentValidation.AspNetCore
```

**Application 项目：**
```bash
cd src/Application
dotnet add package Mapster
dotnet add package Mapster.DependencyInjection
dotnet add package FluentValidation
dotnet add package MediatR
dotnet add package BCrypt.Net-Next
```

**Infrastructure 项目：**
```bash
cd src/Infrastructure
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add package StackExchange.Redis
dotnet add package Autofac
dotnet add package Quartz
dotnet add package Quartz.AspNetCore
dotnet add package QuestPDF
dotnet add package CsvHelper
```

**Migrator 项目：**
```bash
cd src/Migrator
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
```

### STEP 3：生成核心文件

创建以下文件（按顺序）：

#### `src/Domain/Common/Entity.cs`
```csharp
namespace ShareFlow.Domain.Common;

public abstract class Entity<TId>
{
    public TId Id { get; protected set; } = default!;
    public DateTime CreatedAt { get; protected set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; protected set; } = DateTime.UtcNow;

    protected void SetUpdatedAt() => UpdatedAt = DateTime.UtcNow;
}
```

#### `src/Domain/Common/BusinessException.cs`
```csharp
namespace ShareFlow.Domain.Common;

public class BusinessException : Exception
{
    public int Code { get; }
    public BusinessException(string message, int code = 400) : base(message)
    {
        Code = code;
    }
}
```

#### `src/Domain/Interfaces/IRegionContext.cs`
```csharp
namespace ShareFlow.Domain.Interfaces;

public enum RegionMode { Overseas, Domestic }

public interface IRegionContext
{
    RegionMode Mode { get; }
    string DefaultCurrency { get; }
    string DefaultLocale { get; }
    IReadOnlyList<string> EnabledPlatforms { get; }
    bool IsYouTubeOAuthEnabled { get; }
}
```

#### `src/Application/Common/ApiResponse.cs`
```csharp
namespace ShareFlow.Application.Common;

public class ApiResponse<T>
{
    public int Code { get; set; }
    public string Message { get; set; } = string.Empty;
    public T? Data { get; set; }
    public string TraceId { get; set; } = string.Empty;

    public static ApiResponse<T> Success(T data, string message = "Success") =>
        new() { Code = 200, Message = message, Data = data };

    public static ApiResponse<T> Fail(string message, int code = 400) =>
        new() { Code = code, Message = message };
}

public class PagedResult<T>
{
    public IReadOnlyList<T> Items { get; set; } = [];
    public int Total { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
}
```

#### `src/Infrastructure/RegionContext.cs`
```csharp
using ShareFlow.Domain.Interfaces;

namespace ShareFlow.Infrastructure;

public class RegionContext : IRegionContext
{
    public RegionMode Mode { get; }
    public string DefaultCurrency { get; }
    public string DefaultLocale { get; }
    public IReadOnlyList<string> EnabledPlatforms { get; }
    public bool IsYouTubeOAuthEnabled { get; }

    public RegionContext(IConfiguration config)
    {
        var regionStr = config["REGION"] ?? "overseas";
        Mode = regionStr == "domestic" ? RegionMode.Domestic : RegionMode.Overseas;
        DefaultCurrency = config["DEFAULT_CURRENCY"] ?? "USD";
        DefaultLocale = config["CLIENT_LOCALE"] ?? "en-US";
        var platforms = config["ENABLED_PLATFORMS"] ?? "YouTube,TikTok,Instagram,BrandDeal";
        EnabledPlatforms = platforms.Split(',', StringSplitOptions.RemoveEmptyEntries);
        IsYouTubeOAuthEnabled = bool.TryParse(config["YOUTUBE_OAUTH_ENABLED"], out var v) && v;
    }
}
```

#### `src/Api/Middleware/GlobalExceptionMiddleware.cs`
```csharp
using ShareFlow.Application.Common;
using ShareFlow.Domain.Common;
using System.Net;
using System.Text.Json;

namespace ShareFlow.Api.Middleware;

public class GlobalExceptionMiddleware(RequestDelegate next, ILogger<GlobalExceptionMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        try { await next(context); }
        catch (BusinessException ex)
        {
            logger.LogWarning(ex, "Business exception: {Message}", ex.Message);
            await WriteResponse(context, ex.Code, ex.Message);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Unhandled exception");
            await WriteResponse(context, 500, "Internal server error");
        }
    }

    private static async Task WriteResponse(HttpContext context, int code, string message)
    {
        context.Response.StatusCode = code >= 500 ? (int)HttpStatusCode.InternalServerError : (int)HttpStatusCode.BadRequest;
        context.Response.ContentType = "application/json";
        var response = ApiResponse<object>.Fail(message, code);
        await context.Response.WriteAsync(JsonSerializer.Serialize(response));
    }
}
```

#### `src/Infrastructure/InfrastructureModule.cs`
```csharp
using Autofac;
using ShareFlow.Domain.Interfaces;

namespace ShareFlow.Infrastructure;

public class InfrastructureModule : Module
{
    protected override void Load(ContainerBuilder builder)
    {
        builder.RegisterType<RegionContext>()
            .As<IRegionContext>()
            .SingleInstance();

        // Repositories 自动注册（后续 Epic 持续补充）
        builder.RegisterAssemblyTypes(ThisAssembly)
            .Where(t => t.Name.EndsWith("Repository"))
            .AsImplementedInterfaces()
            .InstancePerLifetimeScope();
    }
}
```

#### `src/Application/ApplicationModule.cs`
```csharp
using Autofac;

namespace ShareFlow.Application;

public class ApplicationModule : Module
{
    protected override void Load(ContainerBuilder builder)
    {
        // Services 自动注册（后续 Epic 持续补充）
        builder.RegisterAssemblyTypes(ThisAssembly)
            .Where(t => t.Name.EndsWith("Service"))
            .AsImplementedInterfaces()
            .InstancePerLifetimeScope();
    }
}
```

#### `src/Api/Program.cs`
```csharp
using Autofac;
using Autofac.Extensions.DependencyInjection;
using FluentValidation;
using FluentValidation.AspNetCore;
using Mapster;
using MapsterMapper;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Serilog;
using ShareFlow.Api.Middleware;
using ShareFlow.Application;
using ShareFlow.Infrastructure;
using ShareFlow.Infrastructure.Persistence;
using System.Reflection;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// Serilog
builder.Host.UseSerilog((ctx, cfg) => cfg
    .ReadFrom.Configuration(ctx.Configuration)
    .WriteTo.Console()
    .WriteTo.File("Logs/log-.txt", rollingInterval: RollingInterval.Day));

// Autofac
builder.Host.UseServiceProviderFactory(new AutofacServiceProviderFactory());
builder.Host.ConfigureContainer<ContainerBuilder>(cb =>
{
    cb.RegisterModule<ApplicationModule>();
    cb.RegisterModule<InfrastructureModule>();
});

// EF Core
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseNpgsql(builder.Configuration.GetConnectionString("Default")));

// JWT
var jwtKey = builder.Configuration["Jwt:SecretKey"]!;
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(opt =>
    {
        opt.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey)),
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Jwt:Audience"],
            ClockSkew = TimeSpan.Zero
        };
    });

// Mapster
var config = TypeAdapterConfig.GlobalSettings;
config.Scan(Assembly.GetExecutingAssembly(),
    typeof(ApplicationModule).Assembly);
builder.Services.AddSingleton(config);
builder.Services.AddScoped<IMapper, ServiceMapper>();

// FluentValidation
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddValidatorsFromAssembly(typeof(ApplicationModule).Assembly);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseMiddleware<GlobalExceptionMiddleware>();
app.UseSerilogRequestLogging();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.MapGet("/health", () => Results.Ok(new { status = "healthy", region = app.Configuration["REGION"] }));

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.Run();
```

### STEP 4：前端项目初始化

```bash
cd front-end

# 安装依赖
pnpm install
pnpm add naive-ui
pnpm add pinia @pinia/persist
pnpm add axios
pnpm add vue-i18n
pnpm add echarts vue-echarts
pnpm add vee-validate zod @vee-validate/zod
pnpm add -D @types/node
```

创建以下文件：

#### `src/api/http.ts`
```typescript
import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { useAuthStore } from '@/stores/auth'

export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
  traceId: string
}

const http: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/v1',
  timeout: 15000,
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

http.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    if (response.data.code !== 200) {
      return Promise.reject(new Error(response.data.message))
    }
    return response
  },
  async (error) => {
    if (error.response?.status === 401) {
      const auth = useAuthStore()
      try {
        await auth.refreshToken()
        return http(error.config)
      } catch {
        auth.logout()
        window.location.href = '/auth/login'
      }
    }
    return Promise.reject(error)
  }
)

export default http
```

#### `src/composables/useRegion.ts`
```typescript
import { computed } from 'vue'

const region = import.meta.env.VITE_REGION as 'overseas' | 'domestic'
const currency = import.meta.env.VITE_DEFAULT_CURRENCY as string
const defaultLocale = import.meta.env.VITE_DEFAULT_LOCALE as string
const enabledPlatforms = (import.meta.env.VITE_ENABLED_PLATFORMS as string ?? '').split(',')

export function useRegion() {
  return {
    region,
    isOverseas: computed(() => region === 'overseas'),
    isDomestic: computed(() => region === 'domestic'),
    currency,
    currencySymbol: computed(() => currency === 'USD' ? '$' : '¥'),
    defaultLocale,
    enabledPlatforms,
  }
}
```

#### `src/composables/usePagedList.ts`
```typescript
import { ref, reactive } from 'vue'

export function usePagedList<T>(
  fetcher: (page: number, pageSize: number, filters?: Record<string, unknown>) => Promise<{ items: T[]; total: number }>
) {
  const list = ref<T[]>([])
  const loading = ref(false)
  const pagination = reactive({ page: 1, pageSize: 20, total: 0 })

  async function fetchData(filters?: Record<string, unknown>) {
    loading.value = true
    try {
      const result = await fetcher(pagination.page, pagination.pageSize, filters)
      list.value = result.items as T[]
      pagination.total = result.total
    } finally {
      loading.value = false
    }
  }

  function reset() {
    pagination.page = 1
    fetchData()
  }

  return { list, loading, pagination, fetchData, reset }
}
```

#### `src/directives/permission.ts`
```typescript
import type { DirectiveBinding } from 'vue'
import { useAuthStore } from '@/stores/auth'

export const vPermission = {
  mounted(el: HTMLElement, binding: DirectiveBinding<string>) {
    const auth = useAuthStore()
    if (!auth.hasPermission(binding.value)) {
      el.style.display = 'none'
    }
  },
}
```

### STEP 5：Docker 配置

创建 `docker-compose.base.yml`、`docker-compose.overseas.yml`、`docker-compose.domestic.yml`，以及后端/前端 Dockerfile 和 nginx.conf。

### STEP 6：验证

```bash
# 后端编译检查
cd back-end && dotnet build

# 前端编译检查
cd front-end && pnpm build

# Docker 启动测试
docker-compose -f docker-compose.overseas.yml up -d
curl http://localhost:5000/health
```

## 完成标准
- [ ] `dotnet build` 零错误
- [ ] `pnpm build` 零错误
- [ ] `GET /health` 返回 `{ status: "healthy", region: "overseas" }`
- [ ] `.claude/skills/` 目录结构完整
- [ ] 双环境 docker-compose 可独立启动
