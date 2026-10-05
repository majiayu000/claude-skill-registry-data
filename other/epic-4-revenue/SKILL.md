---
name: epic-4-revenue
description: 执行 Epic 4 —— 平台收益录入（CSV 导入、AI 截图识别、人工录入、多级审核）。依赖 Epic 2 已完成。
---

# Epic 4 — 平台收益录入与审核

## 前置条件
- Epic 2 已完成（项目可用）
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`PlatformRevenue` 实体** (`src/Domain/Entities/PlatformRevenue.cs`)
```csharp
public class PlatformRevenue : Entity<Guid>
{
    public Guid ProjectId { get; private set; }
    public string PlatformName { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }           // 原始平台货币金额
    public string Currency { get; private set; } = string.Empty;  // USD / CNY
    public DateTime RevenueDate { get; private set; }    // 收益所属日期
    public RevenueImportSource ImportSource { get; private set; }  // Manual / Csv / AiScreenshot
    public RevenueStatus Status { get; private set; }    // Pending / NeedsVerification / Approved / Rejected
    public string? ScreenshotStoragePath { get; private set; }   // AI 识别时的截图路径
    public string? AiRawResult { get; private set; }      // AI 原始返回 JSON
    public decimal AiConfidence { get; private set; }     // 0-1
    public Guid? VerifiedByUserId { get; private set; }
    public DateTime? VerifiedAt { get; private set; }
    public string? RejectReason { get; private set; }

    public void Approve(Guid verifierId) {
        Status = RevenueStatus.Approved;
        VerifiedByUserId = verifierId;
        VerifiedAt = DateTime.UtcNow;
        AddDomainEvent(new RevenueApprovedEvent(Id, ProjectId, Amount, Currency, RevenueDate));
    }
    public void Reject(Guid verifierId, string reason) { ... }
    public void FlagForVerification() { Status = RevenueStatus.NeedsVerification; }
}

public enum RevenueImportSource { Manual, Csv, AiScreenshot }
public enum RevenueStatus { Pending, NeedsVerification, Approved, Rejected }
```

**`RevenueApprovedEvent`** → Epic 5 (分红计算) 监听

#### Application 层 — 策略工厂

**`IPlatformRevenueHandlerFactory`** (`src/Application/Overseas/Revenue/Interfaces/`)
```csharp
public interface IPlatformRevenueHandlerFactory
{
    IPlatformRevenueHandler GetHandler(string platformName);
}

public interface IPlatformRevenueHandler
{
    RevenueImportSource SupportedSource { get; }
    Task<IReadOnlyList<ParsedRevenueItem>> ParseAsync(RevenueParseRequest request);
}

// 实现类:
// - TikTokCsvHandler
// - YouTubeCsvHandler
// - TikTokAiScreenshotHandler
// - YouTubeAiScreenshotHandler
// - ManualEntryHandler

// Factory 注册（Autofac）:
// builder.RegisterType<TikTokCsvHandler>().Keyed<IPlatformRevenueHandler>("tiktok.csv");
// 查找: IIndex<string, IPlatformRevenueHandler>["tiktok.csv"]
```

#### AI 截图识别

**`IAiRevenueSkillAgent`** (`src/Application/Overseas/Revenue/Interfaces/IAiRevenueSkillAgent.cs`)
```csharp
public interface IAiRevenueSkillAgent
{
    Task<AiRevenueExtractResult> ExtractAsync(string imageBase64, string mimeType, string platform);
}

public record AiRevenueExtractResult
{
    public decimal Amount { get; init; }
    public string Currency { get; init; } = string.Empty;
    public DateTime Date { get; init; }
    public decimal Confidence { get; init; }  // 0-1
    public string RawJson { get; init; } = string.Empty;
}
```

**`ClaudeAiRevenueAgent`** (`src/Infrastructure/Services/ClaudeAiRevenueAgent.cs`)
```csharp
public class ClaudeAiRevenueAgent(IHttpClientFactory clientFactory,
                                   IPromptStrategyFactory promptFactory,
                                   IRegionContext regionContext) : IAiRevenueSkillAgent
{
    public async Task<AiRevenueExtractResult> ExtractAsync(string imageBase64, string mimeType, string platform)
    {
        var prompt = promptFactory.GetStrategy(platform).BuildPrompt();
        // POST https://api.anthropic.com/v1/messages
        // Headers: x-api-key, anthropic-version: 2023-06-01
        // Body: model=claude-opus-4-5, messages[{role:user,content:[{type:image,...},{type:text,prompt}]}]
        // 解析返回 JSON → AiRevenueExtractResult
        // Confidence < 0.7 → FlagForVerification
    }
}

public interface IPromptStrategyFactory
{
    IPromptStrategy GetStrategy(string platform);
}

public interface IPromptStrategy
{
    string BuildPrompt();
}

// 各平台实现: TikTokPromptStrategy, YouTubePromptStrategy, ...
```

**IRevenueService**
```csharp
public interface IRevenueService
{
    Task<Guid> AddManualAsync(AddManualRevenueRequest req, Guid operatorId);
    Task<BatchImportResult> ImportCsvAsync(Guid projectId, string platform, Stream csvStream);
    Task<AiImportPreviewDto> PreviewScreenshotAsync(Guid projectId, string platform, IFormFile screenshot);
    Task ConfirmAiImportAsync(Guid revenueId, decimal? overrideAmount);
    Task ApproveAsync(Guid revenueId, Guid verifierId);
    Task RejectAsync(Guid revenueId, Guid verifierId, string reason);
    Task<PagedResult<RevenueDto>> GetListAsync(RevenueQueryRequest query);
}
```

#### API Controller

`GET    /v1/admin/revenues`                   `[Permission("revenue.write")]`
`POST   /v1/admin/revenues/manual`            手工录入
`POST   /v1/admin/revenues/csv`               CSV批量上传 (`IFormFile`)
`POST   /v1/admin/revenues/screenshot-preview` AI预识别
`POST   /v1/admin/revenues/{id}/confirm-ai`   确认AI结果
`POST   /v1/admin/revenues/{id}/approve`      `[Permission("revenue.verify")]`
`POST   /v1/admin/revenues/{id}/reject`

### 前端

#### `views/admin/revenues/`
- `RevenueListView.vue` — 表格 + Status 筛选 + Import 按钮组
- `CsvImporterDrawer.vue` — 上传 CSV, 预览解析结果, 确认提交
- `AiScreenshotUploader.vue` — 拖拽上传截图 → AI识别结果展示 → 允许修改金额

**`AiScreenshotUploader.vue` 关键逻辑：**
```typescript
// 上传截图 → POST /screenshot-preview
// 显示: 识别金额、日期、置信度
// 置信度 < 70%: 显示黄色警告 "请人工核实"
// 允许手动修改金额后确认
```

## 完成标准
- [ ] CSV 批量导入 TikTok/YouTube 格式解析正确
- [ ] AI 截图识别调用 Claude API，返回金额+日期
- [ ] 置信度 < 0.7 自动标记 NeedsVerification
- [ ] `revenue.verify` 权限才能审核
- [ ] `RevenueApprovedEvent` 发布成功（Epic 5 可消费）
