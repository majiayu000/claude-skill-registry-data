---
name: epic-10-sales
description: 执行 Epic 10 —— 销售端工作台（销售线索、项目推介、合同发起、业绩统计）。依赖 Epic 3 已完成。
---

# Epic 10 — 销售端工作台

## 前置条件
- Epic 3 (合同签约) 已完成
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`Lead` 实体** (`src/Domain/Entities/Lead.cs`)
```csharp
public class Lead : Entity<Guid>
{
    public string Name { get; private set; } = string.Empty;
    public string ContactInfo { get; private set; } = string.Empty;  // 手机/WhatsApp/微信
    public string? Email { get; private set; }
    public LeadStatus Status { get; private set; }  // New / Contacted / Interested / Converted / Lost
    public Guid SalesOwnerId { get; private set; }
    public Guid? ConvertedInvestorId { get; private set; }
    public string? Notes { get; private set; }

    public void Convert(Guid investorUserId) {
        Status = LeadStatus.Converted;
        ConvertedInvestorId = investorUserId;
        SetUpdatedAt();
    }
    public void UpdateStatus(LeadStatus status, string? notes = null) { ... }
}

public enum LeadStatus { New, Contacted, Interested, Converted, Lost }
```

**`SalesPerformance`** — 视图/聚合查询，不作实体

#### Application 层

**ISalesService**
```csharp
public interface ISalesService
{
    // Leads
    Task<PagedResult<LeadDto>> GetLeadsAsync(Guid salesId, LeadQueryRequest query);
    Task<Guid> CreateLeadAsync(CreateLeadRequest request, Guid salesId);
    Task UpdateLeadAsync(Guid id, UpdateLeadRequest request, Guid salesId);
    Task ConvertLeadAsync(Guid leadId, Guid investorUserId, Guid salesId);

    // Sales portal: 可见的项目（Fundraising 状态）
    Task<IReadOnlyList<SalesProjectDto>> GetAvailableProjectsAsync();

    // 合同发起（调用 IESignService）
    Task<string> InitiateContractAsync(InitiateContractRequest request, Guid salesId);
    // → 返回签约短链接

    // 业绩统计
    Task<SalesPerformanceDto> GetPerformanceAsync(Guid salesId, DateRange range);
}
```

**DTO**
```csharp
public record SalesPerformanceDto
{
    public int TotalLeads { get; init; }
    public int ConvertedLeads { get; init; }
    public decimal ConversionRate { get; init; }
    public int ContractsSent { get; init; }
    public int ContractsSigned { get; init; }
    public decimal TotalAmountClosed { get; init; }
}
```

#### API Controller (`SalesController.cs`)

路由 `/v1/sales/`，`[Authorize(Roles="Sales")]`

```
GET    /v1/sales/leads
POST   /v1/sales/leads
PUT    /v1/sales/leads/{id}
POST   /v1/sales/leads/{id}/convert

GET    /v1/sales/projects               可募资项目列表
POST   /v1/sales/contracts              发起合同 → 返回签约链接

GET    /v1/sales/performance            自己的业绩汇总
```

管理端（查看所有销售业绩）：
```
GET /v1/admin/sales/performance         `[Permission("report.read")]`
```

### 前端

#### 路由配置
```typescript
{
  path: '/sales',
  component: SalesLayout,
  meta: { requiresAuth: true, roles: ['Sales'] },
  children: [
    { path: 'dashboard', component: SalesDashboardView },
    { path: 'leads', component: LeadsView },
    { path: 'projects', component: SalesProjectsView },
    { path: 'contracts', component: SalesContractsView },
  ]
}
```

#### `views/sales/`

**`SalesDashboardView.vue`**
- 漏斗图（线索 → 跟进 → 意向 → 成交）
- 本月业绩卡片：已签约数 / 成交金额 / 转化率

**`LeadsView.vue`**
- NDataTable + 状态筛选
- 看板视图快速切换（Kanban/列表）
- 操作：新增线索 / 更新状态 / 转化为投资人

**`SalesContractsView.vue`**
- 发起合同弹窗：选择投资人 + 项目 + 槽位 → 提交
- 返回签约链接 → 显示"复制链接"按钮（附提示：请自行通过 WhatsApp/微信等发送）

## 完成标准
- [ ] Sales 角色只能看到自己的线索（数据隔离）
- [ ] 发起合同后页面显示可复制的签约链接
- [ ] 线索转化后自动关联投资人账号
- [ ] 业绩漏斗数据与 DB 一致
