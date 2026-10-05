---
name: epic-12-quality
description: 执行 Epic 12 —— 质量保障（单元测试补全、集成测试、E2E 烟雾测试、监控、性能基准、安全加固）。依赖全部 Epic 已完成。
---

# Epic 12 — 质量保障与生产加固

## 前置条件
- Epic 0–11 全部完成
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端单元测试（xUnit + Moq + FluentAssertions）

#### 覆盖目标目录
- `tests/UnitTests/Domain/` — 所有 Entity 方法、状态机转换
- `tests/UnitTests/Application/` — Service 层核心逻辑
- `tests/UnitTests/Infrastructure/` — AI 客户端、Excel 导出

#### 关键测试用例示例

**合同状态机**
```csharp
[Fact]
public void Sign_WhenTokenExpired_ThrowsBusinessException()
{
    var contract = CreateContractWithExpiredToken();
    var act = () => contract.Sign("base64signature");
    act.Should().Throw<BusinessException>()
       .WithMessage("*contract.tokenExpired*");
}

[Fact]
public void Sign_WhenValid_SetsStatusToSignedAndRaisesEvent()
{
    var contract = CreateValidContract();
    contract.Sign("base64signature");
    contract.Status.Should().Be(ContractStatus.Signed);
    contract.DomainEvents.Should().ContainSingle(e => e is ContractSignedEvent);
}
```

**分红计算**
```csharp
[Theory]
[InlineData(1000, 100, 100)]   // 10% → 100
[InlineData(1000, 50, 50)]     // 5%  → 50
[InlineData(333.33, 333, 110.99)] // 精度测试
public void Calculate_ShouldComputeCorrectDividendAmount(
    decimal revenue, int permille, decimal expectedDividend)
{
    var record = DividendRecord.Calculate(
        Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(),
        Guid.NewGuid(), revenue, permille, "USD");
    record.DividendAmount.Should().Be(expectedDividend);
}
```

**钱包余额**
```csharp
[Fact]
public void Freeze_WhenAmountExceedsBalance_ThrowsBusinessException()
{
    var wallet = CreateWalletWithBalance(100m);
    var act = () => wallet.Freeze(150m);
    act.Should().Throw<BusinessException>()
       .WithMessage("*wallet.insufficientBalance*");
}
```

#### 覆盖率目标
```xml
<!-- tests/UnitTests/UnitTests.csproj coverlet 配置 -->
<PackageReference Include="coverlet.collector" />
<!-- 目标: Domain ≥ 90%, Application ≥ 80% -->
```

### 集成测试（WebApplicationFactory）

`tests/IntegrationTests/` 目录（新建项目）

```csharp
// 使用 Testcontainers.PostgreSql 进行真实 DB 集成测试
public class AuthIntegrationTests : IClassFixture<TestWebApplicationFactory>
{
    [Fact]
    public async Task Login_WithValidCredentials_ReturnsTokenPair() { ... }

    [Fact]
    public async Task Login_WithWrongPassword_Returns401() { ... }
}
```

关键集成测试覆盖：
- 认证流程（Login/Refresh/Logout）
- 合同签约完整流程（Create → Send → Sign → PDF Generated）
- 分红计算链（Revenue Approved → Dividend Created → Wallet Credited）

### 监控与观测

**Serilog 结构化日志**（已在 Epic 0 中配置）
- 确认生产环境 MinimumLevel = Information
- 错误日志写入 `Logs/errors-.json`
- 按天滚动文件

**健康检查端点**（`/health`）
```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddNpgsql(connectionString, name: "postgresql")
    .AddRedis(redisConnection, name: "redis");

// 确认: GET /health 返回 200 + JSON 状态
```

**性能 AOP 拦截器**（已在 ApplicationModule 中注册）
- `PerformanceInterceptor`：超过 500ms 记录 Warning 日志
- 验证: 查询接口在合理数据量下响应 ≤ 200ms

### 安全加固清单

- [ ] `appsettings.Production.json` 不含明文密码（全用环境变量）
- [ ] JWT Secret 至少 256 位随机值
- [ ] `/internal/summary` IP 白名单严格配置
- [ ] CORS 只允许已知前端域名（生产）
- [ ] EF 参数化查询（无原始 SQL 字符串拼接）
- [ ] `IFormFile` 上传限制大小（截图 ≤ 5MB）
- [ ] Rate Limiting（登录端点：每 IP 每分钟 ≤ 20 次）

```csharp
// Program.cs 中添加
builder.Services.AddRateLimiter(opt => {
    opt.AddSlidingWindowLimiter("login", o => {
        o.Window = TimeSpan.FromMinutes(1);
        o.SegmentsPerWindow = 6;
        o.PermitLimit = 20;
    });
});
// LoginController: [EnableRateLimiting("login")]
```

### 前端测试（Vitest）

**覆盖目标**：
- `composables/` — usePagedList, useForm, useRegion
- `stores/` — auth, notification
- `utils/` — 格式化函数

```typescript
// tests/unit/stores/auth.test.ts
describe('useAuthStore', () => {
  it('hasPermission should return true for SuperAdmin regardless of permission', () => {
    ...
  })
  it('hasPermission should check permissions array for non-SuperAdmin', () => {
    ...
  })
})
```

### Docker 生产配置验证

- [ ] `docker-compose.overseas.yml` + `docker-compose.domestic.yml` 各自独立启动成功
- [ ] Nginx 配置：gzip, 静态资源缓存, proxy_pass 正确
- [ ] 数据库迁移在容器启动时自动执行（Migrator 容器）
- [ ] Redis 持久化配置（AOF 或 RDB）

## 完成标准
- [ ] Domain 层测试覆盖率 ≥ 90%
- [ ] Application 层覆盖率 ≥ 80%
- [ ] 所有集成测试绿色通过
- [ ] `/health` 返回所有组件健康
- [ ] Rate Limiting 生效（测试：连续 21 次登录第 21 次返回 429）
- [ ] 两套 Docker Compose 均可一键启动
