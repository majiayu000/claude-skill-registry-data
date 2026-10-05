---
name: epic-9-reports
description: 执行 Epic 9 —— 报表与数据导出（收益报表、分红报表、客户汇总、ECharts 图表、Excel/CSV 导出）。依赖 Epic 5/6 已完成。
---

# Epic 9 — 报表与数据导出

## 前置条件
- Epic 5 (分红) + Epic 6 (钱包) 已完成
- 已读取 `shareflow-context/SKILL.md`

## NuGet 包
```
ClosedXML (Excel 导出)
```

## 任务清单

### 后端

#### Application 层

**`IReportService`**
```csharp
public interface IReportService
{
    // 管理端报表
    Task<RevenueReportDto> GetRevenueReportAsync(RevenueReportQuery query);
    Task<DividendReportDto> GetDividendReportAsync(DividendReportQuery query);
    Task<InvestorSummaryReportDto> GetInvestorSummaryAsync(InvestorSummaryQuery query);
    Task<ProjectPerformanceDto> GetProjectPerformanceAsync(Guid projectId, DateRange range);

    // 导出
    Task<byte[]> ExportRevenueToExcelAsync(RevenueReportQuery query);
    Task<byte[]> ExportDividendToExcelAsync(DividendReportQuery query);
    Task<byte[]> ExportInvestorSummaryToExcelAsync(InvestorSummaryQuery query);
}
```

**DTO 示例**
```csharp
public record RevenueReportDto
{
    public IReadOnlyList<RevenueByMonthItem> ByMonth { get; init; } = [];
    public IReadOnlyList<RevenueByPlatformItem> ByPlatform { get; init; } = [];
    public decimal TotalRevenue { get; init; }
    public string Currency { get; init; } = string.Empty;
}

public record RevenueByMonthItem { public string Month { get; init; } = ""; public decimal Amount { get; init; } }
public record RevenueByPlatformItem { public string Platform { get; init; } = ""; public decimal Amount { get; init; } }
```

**Excel 导出实现** (`ExcelExportService.cs` in Infrastructure)
```csharp
public class ExcelExportService : IExcelExportService
{
    public byte[] ExportToExcel<T>(IEnumerable<T> data, string sheetName)
    {
        using var wb = new XLWorkbook();
        var ws = wb.AddWorksheet(sheetName);
        // 通过反射或手动列映射写入表头和数据行
        using var stream = new MemoryStream();
        wb.SaveAs(stream);
        return stream.ToArray();
    }
}
```

#### API Controller `[Permission("report.read")]`

```
GET /v1/admin/reports/revenue             Revenue 统计 (ByMonth + ByPlatform)
GET /v1/admin/reports/dividend            Dividend 统计
GET /v1/admin/reports/clients             客户汇总
GET /v1/admin/reports/projects/{id}       单项目绩效
GET /v1/admin/reports/revenue/export      → application/vnd.openxmlformats (Excel)
GET /v1/admin/reports/dividend/export
GET /v1/admin/reports/clients/export
```

### 前端

#### `views/admin/reports/`

**`RevenueReportView.vue`**
```typescript
// ECharts 折线图：月度收益趋势
// ECharts 饼图：各平台占比
// 右上角"导出 Excel"按钮 → 调用 export API → triggerDownload(blob, 'revenue.xlsx')
```

**`DividendReportView.vue`**
- 柱状图：各项目分红金额对比
- 表格：分客户分红汇总

**`ClientSummaryView.vue`**
- 表格列：客户名称、持股比例、已收分红、鑉包余额
- 导出按钮

#### `composables/useExportDownload.ts`
```typescript
export function useExportDownload() {
  async function download(url: string, filename: string, params?: Record<string, unknown>) {
    const res = await http.get(url, { params, responseType: 'blob' })
    const blob = new Blob([res.data])
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = filename
    a.click()
    URL.revokeObjectURL(a.href)
  }
  return { download }
}
```

#### ECharts 封装 `components/charts/`
- `LineChart.vue` — Props: `series`, `xAxis`, `title`
- `PieChart.vue` — Props: `data` (name+value), `title`
- `BarChart.vue` — Props: `series`, `categories`, `title`
- 统一通过 `useECharts(canvasRef)` composable 初始化

## 完成标准
- [ ] Revenue ByMonth 图表数据正确（与数据库聚合一致）
- [ ] Excel 导出文件可在 Excel 中正常打开
- [ ] `report.read` 权限控制正常
- [ ] ECharts 图表响应式（窗口 resize 自动调整）
