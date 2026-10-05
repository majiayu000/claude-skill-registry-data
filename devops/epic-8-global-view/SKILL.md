---
name: epic-8-global-view
description: 执行 Epic 8 —— 跨实例全局看板（境外实例 SuperAdmin 聚合境内只读汇总数据，双货币分列展示）。依赖 Epic 7 已完成。
---

# Epic 8 — 跨实例全局看板

## 前置条件
- Epic 7 已完成（本实例数据完整）
- 双实例（overseas + domestic）均已部署
- 已读取 `shareflow-context/SKILL.md`

## 架构说明

> 境外实例作为"主控"实例，通过调用境内实例的 `/internal/summary` API（IP白名单 + 内部Token保护）拉取境内汇总数据，在 SuperAdmin 看板中 USD / CNY 分列展示，不进行货币合并。

## 任务清单

### 境内实例后端（Internal API）

**`InternalSummaryController.cs`** (`src/Api/Controllers/Internal/`)

路由：`GET /internal/summary`

认证方式：
```csharp
// Middleware: InternalApiAuthMiddleware
// 校验 Header: X-Internal-Token == appsettings["InternalApi:Token"]
// 仅允许来自白名单 IP（appsettings["InternalApi:AllowedIps"]）
public record DomesticSummaryDto
{
    public int ActiveProjects { get; init; }
    public int ActiveInvestors { get; init; }
    public decimal TotalInvestedCny { get; init; }
    public decimal TotalRevenueThisMonthCny { get; init; }
    public decimal TotalDividendDistributedCny { get; init; }
    public decimal PendingWithdrawalCny { get; init; }
    public DateTime GeneratedAt { get; init; }
}
```

配置（`appsettings.json` domestic）：
```json
{
  "InternalApi": {
    "Token": "${INTERNAL_API_TOKEN}",
    "AllowedIps": ["${OVERSEAS_API_IP}"]
  }
}
```

### 境外实例后端（Global Dashboard Service）

**`IDomesticSummaryClient`** (`src/Application/Reports/Interfaces/`)
```csharp
public interface IDomesticSummaryClient
{
    Task<DomesticSummaryDto?> GetSummaryAsync();
}

// Infrastructure 实现: HttpDomesticSummaryClient
// - 读取 InternalApi:DomesticBaseUrl, InternalApi:Token from config
// - HttpClient GET {baseUrl}/internal/summary
// - Header: X-Internal-Token
// - 失败 → 返回 null（境外实例独立运行不受影响）
```

**`IGlobalDashboardService`** (`src/Application/Reports/Interfaces/`)
```csharp
public interface IGlobalDashboardService
{
    Task<GlobalDashboardDto> GetDashboardAsync();
}

public record GlobalDashboardDto
{
    // 境外数据（USD）
    public OverseasSummaryDto Overseas { get; init; } = new();
    // 境内数据（CNY）—— 可能为 null（境内实例不可达时）
    public DomesticSummaryDto? Domestic { get; init; }
    public DateTime GeneratedAt { get; init; }
}

public record OverseasSummaryDto
{
    public int ActiveProjects { get; init; }
    public int ActiveInvestors { get; init; }
    public decimal TotalInvestedUsd { get; init; }
    public decimal TotalRevenueThisMonthUsd { get; init; }
    public decimal TotalDividendDistributedUsd { get; init; }
    public decimal PendingWithdrawalUsd { get; init; }
}
```

**缓存**：Redis `global:dashboard` TTL 5分钟（避免频繁跨实例调用）

**API Controller**：`GET /v1/admin/global-dashboard` `[Authorize(Roles="SuperAdmin")]`

### 前端

#### `views/admin/GlobalDashboardView.vue`
```html
<!-- 顶部标题 + 刷新按钮 -->
<!-- 两列布局: 境外(USD左列) + 境内(CNY右列) -->

<n-grid cols="2" x-gap="16">
  <n-grid-item>
    <n-card title="Overseas 境外 (USD)">
      <MetricCard label="活跃项目" :value="data.overseas.activeProjects" />
      <MetricCard label="总投入" :value="data.overseas.totalInvestedUsd" currency="USD" />
      <MetricCard label="本月收益" :value="data.overseas.totalRevenueThisMonthUsd" currency="USD" />
      <MetricCard label="待提现" :value="data.overseas.pendingWithdrawalUsd" currency="USD" />
    </n-card>
  </n-grid-item>
  <n-grid-item>
    <n-card title="国内 (CNY)" :class="{ 'offline': !data.domestic }">
      <n-alert v-if="!data.domestic" type="warning">境内实例暂时不可达</n-alert>
      <template v-else>
        <MetricCard label="活跃项目" :value="data.domestic.activeProjects" />
        <MetricCard label="总投入" :value="data.domestic.totalInvestedCny" currency="CNY" />
        ...
      </template>
    </n-card>
  </n-grid-item>
</n-grid>
```

**`MetricCard.vue`** (`components/dashboard/MetricCard.vue`)
```typescript
defineProps<{
  label: string
  value: number
  currency?: 'USD' | 'CNY'
  trend?: number  // 环比增减百分比
}>()
// 货币格式化: useRegion().formatCurrency(value, currency)
```

#### 路由
```typescript
{ path: '/admin/global-dashboard', component: GlobalDashboardView,
  meta: { requiresRole: 'SuperAdmin' } }
```

### Docker 配置
`docker-compose.overseas.yml` 中增加环境变量：
```yaml
environment:
  - InternalApi__DomesticBaseUrl=http://domestic-api:8080
  - InternalApi__Token=${INTERNAL_API_TOKEN}
  - InternalApi__AllowedIps__0=172.20.0.0/16
```

## 完成标准
- [ ] 境外实例 SuperAdmin 能看到双列数据看板
- [ ] 境内实例不可达时，境外看板仍正常显示（境内列显示警告）
- [ ] Redis 缓存 5min，避免每次请求都跨实例调用
- [ ] 非 SuperAdmin 访问返回 403
- [ ] `/internal/summary` Token 错误返回 401
