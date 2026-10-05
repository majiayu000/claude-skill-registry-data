---
name: epic-7-client-portal
description: 执行 Epic 7 —— 持股客户门户（Dashboard、项目收益、分红记录、钉包、合同下载）。依赖 Epic 3/5/6 已完成。
---

# Epic 7 — 持股客户门户

## 前置条件
- Epic 3 (合同+账号初始化)、Epic 5 (分红)、Epic 6 (钱包) 已完成
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端（客户端专属 API）

所有路由前缀 `/v1/client/`，`[Authorize(Roles="Client")]`

**`IClientDashboardService`**
```csharp
public interface IClientDashboardService
{
    Task<ClientDashboardDto> GetDashboardAsync(Guid clientUserId);
}

public record ClientDashboardDto
{
    public decimal TotalSharePct { get; init; }
    public decimal TotalDividendReceived { get; init; }
    public decimal WalletBalance { get; init; }
    public string Currency { get; init; } = string.Empty;
    public IReadOnlyList<ClientProjectSummaryDto> Projects { get; init; } = [];
    public IReadOnlyList<RecentDividendDto> RecentDividends { get; init; } = [];
}

public record ClientProjectSummaryDto
{
    public string ProjectTitle { get; init; } = string.Empty;
    public string PlatformName { get; init; } = string.Empty;
    public decimal SharePct { get; init; }
    public decimal TotalDividend { get; init; }
    public string ContractStatus { get; init; } = string.Empty;
}
```

**`IClientRevenueService`**
```csharp
Task<PagedResult<ClientRevenueDto>> GetProjectRevenuesAsync(
    Guid clientUserId, Guid projectId, PagedRequest paged);
// 只返回 Approved 状态收益，只展示含该客户 Slot 的项目
```

**API Controller** (`ClientController.cs`)
```
GET  /v1/client/dashboard
GET  /v1/client/projects               客户参与的项目列表
GET  /v1/client/projects/{id}/revenues 指定项目收益明细
GET  /v1/client/dividends              全部分红记录（分页）
GET  /v1/client/wallet                 钱包余额
GET  /v1/client/wallet/transactions    流水明细
POST /v1/client/wallet/withdrawals     申请提现
GET  /v1/client/contracts              我的合同列表
GET  /v1/client/contracts/{id}/pdf     下载 PDF（通过存储签名 URL）
```

**注意：数据隔离安全规则**
- 所有查询必须附加 `WHERE ClientUserId = currentUserId`
- Controller 中从 JWT Claims 提取 userId，通过 `ICurrentUserService` 注入

**`ICurrentUserService`** (`src/Application/Common/Interfaces/ICurrentUserService.cs`)
```csharp
public interface ICurrentUserService
{
    Guid UserId { get; }
    string Role { get; }
    IReadOnlyList<string> Permissions { get; }
}
// 实现: HttpContextCurrentUserService（从 IHttpContextAccessor 读取 Claims）
```

### 前端

#### 路由配置
```typescript
// src/router/index.ts
{
  path: '/client',
  component: ClientLayout,
  meta: { requiresAuth: true, roles: ['Client'] },
  children: [
    { path: 'dashboard', component: ClientDashboardView },
    { path: 'projects', component: ClientProjectsView },
    { path: 'projects/:id/revenues', component: ClientRevenuesView },
    { path: 'dividends', component: ClientDividendsView },
    { path: 'wallet', component: ClientWalletView },
    { path: 'contracts', component: ClientContractsView },
  ]
}
```

#### `layouts/ClientLayout.vue`
- 侧栏导航：Dashboard / 我的持股 / 分红记录 / 鑉包 / 合同
- 头部：用户名 + 语言切换 + 退出
- 响应式（移动端折叠）

#### `views/client/`

**`ClientDashboardView.vue`**
```html
<!-- 数据卡片行：持股比例 / 已收分红 / 鑉包余额 -->
<!-- 参与项目列表（ProjectSummaryCard 组件） -->
<!-- 最近分红记录（最近5条） -->
```

**`ClientProjectsView.vue`** — 卡片式展示参投项目

**`ClientDividendsView.vue`** — NDataTable，按项目/日期筛选，导出 CSV

**`ClientWalletView.vue`**
- 余额大字显示 + "申请提现"按钮
- 流水列表（NTimeline 或 NDataTable）

**`ClientContractsView.vue`**
- 合同列表 + 状态标签
- "下载 PDF"按钮（GET /contracts/{id}/pdf → 返回签名 URL → window.open）

#### 国际化注意
- 客户端门户需同时支持 zh-CN / en-US（`vue-i18n`）
- `useRegion()` 决定货币符号、数字格式

## 完成标准
- [ ] Dashboard 3 个汇总卡片数据正确
- [ ] 客户只能看到自己的数据（数据隔离验证）
- [ ] PDF 下载链接有效（30min 签名 URL）
- [ ] 申请提现后钱包余额冻结
- [ ] 路由守卫：非 Client 角色无法访问 /client/* 路由
