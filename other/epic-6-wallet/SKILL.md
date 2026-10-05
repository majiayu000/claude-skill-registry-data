---
name: epic-6-wallet
description: 执行 Epic 6 —— 持股客户鑉包（余额账本、充値（管理员）、提现申请（线下审核）、流水明细）。依赖 Epic 5 已完成。
---

# Epic 6 — 投资人钱包与提现

## 前置条件
- Epic 5 已完成（DividendDistributedEvent 可用）
- 已读取 `shareflow-context/SKILL.md`

## 任务清单

### 后端

#### Domain 层

**`Wallet` 实体** (`src/Domain/Entities/Wallet.cs`)
```csharp
public class Wallet : Entity<Guid>
{
    public Guid InvestorUserId { get; private set; }
    public decimal Balance { get; private set; }        // 当前可用余额
    public decimal FrozenAmount { get; private set; }   // 提现申请中的冻结额
    public string Currency { get; private set; } = string.Empty;

    public void Credit(decimal amount, string remark) {
        if (amount <= 0) throw new BusinessException("wallet.invalidAmount");
        Balance += amount;
        AddDomainEvent(new WalletCreditedEvent(Id, InvestorUserId, amount, Currency, remark));
    }

    public void Freeze(decimal amount) {
        if (amount > Balance) throw new BusinessException("wallet.insufficientBalance");
        Balance -= amount;
        FrozenAmount += amount;
    }

    public void Unfreeze(decimal amount) {
        FrozenAmount -= amount;
        Balance += amount;
    }

    public void DeductFrozen(decimal amount) {
        FrozenAmount -= amount;
    }
}
```

**`WalletTransaction` 实体** (`src/Domain/Entities/WalletTransaction.cs`)
```csharp
public class WalletTransaction : Entity<long>  // long for high-freq log
{
    public Guid WalletId { get; private set; }
    public Guid InvestorUserId { get; private set; }
    public TransactionType Type { get; private set; }  // Dividend / AdminCredit / Withdrawal
    public TransactionDirection Direction { get; private set; }  // In / Out
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = string.Empty;
    public decimal BalanceBefore { get; private set; }
    public decimal BalanceAfter { get; private set; }
    public string Remark { get; private set; } = string.Empty;
    public Guid? ReferenceId { get; private set; }     // DividendRecordId / WithdrawalRequestId
}

public enum TransactionType { Dividend, AdminCredit, Withdrawal }
public enum TransactionDirection { In, Out }
```

**`WithdrawalRequest` 实体** (`src/Domain/Entities/WithdrawalRequest.cs`)
```csharp
public class WithdrawalRequest : Entity<Guid>
{
    public Guid InvestorUserId { get; private set; }
    public Guid WalletId { get; private set; }
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = string.Empty;
    public WithdrawalStatus Status { get; private set; }  // Pending / Approved / Rejected / Completed
    public string? PaymentMethod { get; private set; }   // 线下付款方式备注
    public string? RejectReason { get; private set; }
    public Guid? ApprovedByUserId { get; private set; }
    public DateTime? ProcessedAt { get; private set; }

    public void Approve(Guid adminId) { ... }          // Wallet.Freeze()
    public void Complete(Guid adminId) { ... }         // Wallet.DeductFrozen()
    public void Reject(Guid adminId, string reason) { ... }  // Wallet.Unfreeze()
}

public enum WithdrawalStatus { Pending, Approved, Rejected, Completed }
```

**Repository** `IWalletRepository`, `IWithdrawalRequestRepository`, `IWalletTransactionRepository`

#### Application 层

**Event Handler** (`DividendDistributedEventHandler`)
- 监听 `DividendDistributedEvent`
- 找到 investor 的 Wallet → `wallet.Credit(amount, "Dividend")`
- 记录 `WalletTransaction`

**IWalletService**
```csharp
public interface IWalletService
{
    Task<WalletDto> GetByInvestorIdAsync(Guid investorId);
    Task AdminCreditAsync(Guid investorId, decimal amount, string remark, Guid adminId);
    Task<Guid> RequestWithdrawalAsync(Guid investorId, decimal amount, string? paymentMethod);
    Task ApproveWithdrawalAsync(Guid requestId, Guid adminId);
    Task CompleteWithdrawalAsync(Guid requestId, Guid adminId);
    Task RejectWithdrawalAsync(Guid requestId, Guid adminId, string reason);
    Task<PagedResult<WalletTransactionDto>> GetTransactionsAsync(Guid investorId, PagedRequest paged);
}
```

**Mapster 配置**
```csharp
config.NewConfig<WalletTransaction, WalletTransactionDto>()
    .Map(dest => dest.TypeLabel, src => src.Type.ToString())
    .Map(dest => dest.DirectionLabel, src => src.Direction == TransactionDirection.In ? "+" : "-");
```

#### API Controller

管理端（后台）：
`GET    /v1/admin/wallets`                          所有投资人钱包列表
`POST   /v1/admin/wallets/{investorId}/credit`      管理员充值 `[Permission("dividend.write")]`
`GET    /v1/admin/withdrawals`                      提现申请列表
`POST   /v1/admin/withdrawals/{id}/approve`         `[Permission("withdrawal.approve")]`
`POST   /v1/admin/withdrawals/{id}/complete`
`POST   /v1/admin/withdrawals/{id}/reject`

客户端（自服务）：
`GET    /v1/client/wallet`            查看余额
`GET    /v1/client/wallet/transactions`
`POST   /v1/client/wallet/withdrawals`  申请提现

### 前端

#### 管理端 `views/admin/wallet/`
- `WalletListView.vue` — 投资人余额汇总列表
- `WithdrawalRequestListView.vue` — 提现申请列表 + 审批操作
- 提现流程：Pending → Approve（冻结）→ Complete（打款后标记完成）

#### 客户端 `views/client/wallet/`
- `WalletView.vue` — 余额 + 流水 Timeline
- `WithdrawalFormModal.vue` — 申请提现表单

## 完成标准
- [ ] 分红分发后钱包余额自动更新
- [ ] 每次余额变化均有 `WalletTransaction` 记录（含 before/after）
- [ ] 提现状态机：Pending → Approved → Completed 正确流转
- [ ] `withdrawal.approve` 权限校验
- [ ] 提现金额超过余额时返回 `wallet.insufficientBalance` 错误
