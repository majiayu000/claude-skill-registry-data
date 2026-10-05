---
name: epic-3-contract
description: 执行 Epic 3 —— 合同管理与电子签约（状态机、模板工厂、Canvas 签名、短链接发送）。依赖 Epic 2 已完成。
---

# Epic 3 — 合同管理与电子签约

## 前置条件
- Epic 2 已完成（项目/槽位可用）
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`Contract` 实体** (`src/Domain/Entities/Contract.cs`)
```csharp
public class Contract : Entity<Guid>
{
    public Guid ProjectId { get; private set; }
    public Guid SlotId { get; private set; }
    public Guid InvestorUserId { get; private set; }
    public ContractStatus Status { get; private set; }
    public string TemplateType { get; private set; } = string.Empty;  // 按 IRegionContext 决定
    public string? SignToken { get; private set; }          // 短链接 Token（UUID）
    public DateTime? SignTokenExpiresAt { get; private set; }
    public string? SignatureDataUrl { get; private set; }   // Canvas base64
    public DateTime? SignedAt { get; private set; }
    public string? PdfStoragePath { get; private set; }     // 对象存储路径
    public DateTime? RenewRequestedAt { get; private set; }

    // 状态机方法
    public string GenerateSignLink() {
        SignToken = Guid.NewGuid().ToString("N");
        SignTokenExpiresAt = DateTime.UtcNow.AddDays(7);
        Status = ContractStatus.Sent;
        return SignToken;
    }
    public void Sign(string signatureDataUrl) {
        if (SignTokenExpiresAt < DateTime.UtcNow) throw new BusinessException("contract.tokenExpired");
        SignatureDataUrl = signatureDataUrl;
        SignedAt = DateTime.UtcNow;
        Status = ContractStatus.Signed;
        AddDomainEvent(new ContractSignedEvent(Id, InvestorUserId, ProjectId, SlotId));
    }
    public void PdfGenerated(string storagePath) { PdfStoragePath = storagePath; Status = ContractStatus.Executed; }
    public void RequestRenew() { /* Pending Renew */ }
    public void Renew() { /* 新合同替换，旧合同 Status = Superseded */ }
}

public enum ContractStatus
{
    Draft, Sent, Signed, Executed, Expired, Renewing, PendingRenew, Superseded
}
```

**`ContractSignedEvent`** (`src/Domain/Events/ContractSignedEvent.cs`)
```csharp
public record ContractSignedEvent(Guid ContractId, Guid InvestorUserId, Guid ProjectId, Guid SlotId)
    : INotification;
```

**Repository 接口** (`IContractRepository`)
```csharp
Task<Contract?> GetByIdAsync(Guid id);
Task<Contract?> GetBySignTokenAsync(string token);
Task<PagedResult<ContractDto>> GetListAsync(ContractQueryRequest query);
Task AddAsync(Contract contract);
Task UpdateAsync(Contract contract);
```

#### Application 层

**IContractTemplateFactory** (`src/Application/Contracts/Interfaces/IContractTemplateFactory.cs`)
```csharp
public interface IContractTemplateFactory
{
    /// <summary>根据 IRegionContext 返回对应语言/法律版本模板</summary>
    IContractTemplate GetTemplate(string templateType);
}

public interface IContractTemplate
{
    string Render(ContractTemplateData data);  // 返回 HTML 字符串
}
// 实现: OverseasEnglishTemplate, DomesticChineseTemplate
```

**IESignService** (`src/Application/Contracts/Interfaces/IESignService.cs`)
```csharp
public interface IESignService
{
    /// <summary>生成签约短链接（仅返回后端 Token，不负责发送）</summary>
    Task<string> GenerateSignLinkAsync(Guid contractId);

    /// <summary>验证 Token 有效性，返回合同预览数据</summary>
    Task<ContractPreviewDto> GetPreviewAsync(string token);

    /// <summary>投资人提交 Canvas 签名</summary>
    Task SignAsync(string token, string signatureDataUrl);
}
```

**Event Handler** (`src/Application/EventHandlers/ContractSignedEventHandler.cs`)
```csharp
public class ContractSignedEventHandler(
    IAccountProvisioningService accountProvisioning,
    IESignService eSignService,
    IPdfGeneratorService pdfGenerator) : INotificationHandler<ContractSignedEvent>
{
    public async Task Handle(ContractSignedEvent evt, CancellationToken _)
    {
        // 1. 生成 PDF → 上传存储
        // 2. 更新 Contract.PdfStoragePath
        // 3. 触发账号初始化（如账号未存在）
        // 4. （可选）推 WhatsApp/短信通知（Epic 11）
    }
}
```

**IPdfGeneratorService** → QuestPDF 实现
```csharp
public interface IPdfGeneratorService
{
    Task<byte[]> GenerateContractPdfAsync(Guid contractId);
}
```

#### API Controller

后台管理：
`GET    /v1/admin/contracts`              `[Permission("contract.read")]`
`POST   /v1/admin/contracts`             创建草稿合同
`POST   /v1/admin/contracts/{id}/send`   生成签约短链接 → 返回 `{ signUrl: "https://app/esign/{token}" }`
`POST   /v1/admin/contracts/{id}/renew`  `[Permission("contract.renew")]`

**公开端点（无需 JWT）：**
`GET  /v1/public/esign/{token}`   → 返回合同预览数据（投资人姓名、项目、金额、份额）
`POST /v1/public/esign/{token}`   → 提交 base64 签名

### 前端

#### 签约页（Public，无需登录）`views/public/ESignView.vue`
```
路由: /esign/:token    meta: { requiresAuth: false }

流程:
1. mounted → GET /v1/public/esign/:token → 显示合同摘要
2. 若 token 已过期 → 显示"链接已失效，请联系销售"
3. Canvas 签名区 (SignaturePad.vue 组件)
4. 点击"确认签署" → POST /v1/public/esign/:token → 成功页
```

**`SignaturePad.vue`** (`components/esign/SignaturePad.vue`)
```typescript
// 使用 HTMLCanvasElement API 实现手绘签名
// Emits: update:modelValue (base64 png dataUrl)
// 方法: clear()

const canvas = ref<HTMLCanvasElement>()
// pointer/touch 事件绘制路径
// toDataURL('image/png') 导出
```

#### 后台合同管理 `views/admin/contracts/`
- `ContractListView.vue` — 表格 + 状态筛选
- `ContractDetailView.vue` — 状态时间线 + PDF 预览链接 + "生成签约链接"按钮
- 点击"生成签约链接" → 显示链接 + "复制"按钮（销售员自行发送）

## 完成标准
- [ ] `POST /send` 返回签约 URL，管理员可复制
- [ ] 투资人通过短链接打开页面，能看到合同摘要
- [ ] Canvas 签名提交后 DB 状态变 `Signed`
- [ ] Event Handler 触发 PDF 生成 + 账号初始化
- [ ] 无效/过期 Token 返回 400 with `contract.tokenExpired`
