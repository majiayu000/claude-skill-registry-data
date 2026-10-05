---
name: epic-5-dividend
description: 执行 Epic 5 —— 分红计算引擎（按持股比例分配、定时/手动触发、分红记录）。依赖 Epic 4 已完成。
---

# Epic 5 — 分红计算引擎

## 前置条件
- Epic 4 已完成（PlatformRevenue.Approved 事件可用）
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`DividendRecord` 实体** (`src/Domain/Entities/DividendRecord.cs`)
```csharp
public class DividendRecord : Entity<Guid>
{
    public Guid ProjectId { get; private set; }
    public Guid SlotId { get; private set; }
    public Guid InvestorUserId { get; private set; }
    public Guid PlatformRevenueId { get; private set; }
    public decimal RevenueAmount { get; private set; }     // 参与分配的收益额
    public int SharePermille { get; private set; }         // 持股千分比（快照）
    public decimal DividendAmount { get; private set; }    // = RevenueAmount * SharePermille / 1000
    public string Currency { get; private set; } = string.Empty;
    public DividendStatus Status { get; private set; }     // Calculated / Confirmed / Distributed
    public DateTime CalculatedAt { get; private set; }

    public static DividendRecord Calculate(
        Guid projectId, Guid slotId, Guid investorId,
        Guid revenueId, decimal revenue, int permille, string currency)
    {
        return new DividendRecord
        {
            Id = Guid.NewGuid(),
            ProjectId = projectId,
            SlotId = slotId,
            InvestorUserId = investorId,
            PlatformRevenueId = revenueId,
            RevenueAmount = revenue,
            SharePermille = permille,
            DividendAmount = Math.Round(revenue * permille / 1000m, 2),
            Currency = currency,
            Status = DividendStatus.Calculated,
            CalculatedAt = DateTime.UtcNow
        };
    }

    public void Confirm() { Status = DividendStatus.Confirmed; SetUpdatedAt(); }
    public void MarkDistributed() {
        Status = DividendStatus.Distributed;
        AddDomainEvent(new DividendDistributedEvent(Id, InvestorUserId, DividendAmount, Currency));
    }
}

public enum DividendStatus { Calculated, Confirmed, Distributed }
```

**`DividendDistributedEvent`** → 钱包到账（Epic 6 监听）

**Repository** `IDividendRepository`
```csharp
Task<IReadOnlyList<DividendRecord>> GetByRevenueIdAsync(Guid revenueId);
Task<PagedResult<DividendRecord>> GetByInvestorAsync(Guid investorId, DiviQueryRequest q);
Task<DividendSummary> GetProjectSummaryAsync(Guid projectId);
Task AddRangeAsync(IEnumerable<DividendRecord> records);
Task UpdateAsync(DividendRecord record);
```

#### Application 层

**IDividendCalculationService**
```csharp
public interface IDividendCalculationService
{
    /// <summary>
    /// 对某条已审核收益，按所有 Occupied Slots 的 SharePermille 分别计算分红
    /// 一般由 RevenueApprovedEvent Handler 触发
    /// </summary>
    Task CalculateForRevenueAsync(Guid revenueId);

    Task ConfirmBatchAsync(IEnumerable<Guid> dividendIds, Guid operatorId);
    Task DistributeBatchAsync(IEnumerable<Guid> dividendIds, Guid operatorId);
}
```

**Event Handler** (`RevenueApprovedEventHandler`)
```csharp
public class RevenueApprovedEventHandler(IDividendCalculationService calcService)
    : INotificationHandler<RevenueApprovedEvent>
{
    public async Task Handle(RevenueApprovedEvent evt, CancellationToken _)
        => await calcService.CalculateForRevenueAsync(evt.RevenueId);
}
```

**分红计算逻辑** (in `DividendCalculationService`):
1. 查 `PlatformRevenue` → 获得 `ProjectId, Amount, Currency`
2. 查 `ProjectSlot` where `ProjectId = X AND Status = Occupied` → 获得所有投资人和 SharePermille
3. 按公式：`DividendAmount = Amount * SharePermille / 1000`，批量创建 `DividendRecord`
4. 保存 DB

**定时任务** (Quartz.NET `DividendCalculationJob`)
- Cron: 每天 02:00 UTC
- 补算前一天所有 Approved 但未计算分红的收益

#### API Controller

`GET  /v1/admin/dividends`               `[Permission("dividend.read")]`
`GET  /v1/admin/dividends/summary`       项目汇总视图
`POST /v1/admin/dividends/confirm`       批量确认 `[Permission("dividend.write")]`
`POST /v1/admin/dividends/distribute`    批量分发（触发钱包到账）

客户端（Epic 7 补充）：
`GET  /v1/client/dividends`             `[Authorize(Roles="Client")]`

### 前端

#### `views/admin/dividends/`
- `DividendListView.vue` — NDataTable，按项目/状态/日期筛选
- `DividendSummaryCard.vue` — 项目累计分红汇总卡片
- 批量确认 / 批量分发操作按钮

## 完成标准
- [ ] Revenue Approved 后 DividendRecord 自动生成（数量 = Occupied Slots 数量）
- [ ] `DividendAmount = Revenue * SharePermille / 1000`，精度 decimal(15,2)
- [ ] 批量分发后触发 `DividendDistributedEvent`（Epic 6 可消费）
- [ ] Quartz 定时任务已注册
