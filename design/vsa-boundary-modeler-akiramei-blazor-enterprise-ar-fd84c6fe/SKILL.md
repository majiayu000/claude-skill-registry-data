---
name: vsa-boundary-modeler
description: >
  Blazor VSA における Boundary パターンのモデリング支援。UI を持つ機能で
  Entity.CanXxx() メソッドの設計、Intent 定義、BoundaryService の責務分離を
  支援する。AI の学習バイアス（古典 DDD は UI を対象外とする）により
  忘却されやすい Boundary モデリングを自動的に想起させ、操作可否判定の
  業務ロジックを Entity に正しく配置する設計を促す。
allowed-tools:
  - Read
  - Glob
  - Grep
---

# VSA Boundary Modeler

このスキルは、UI がある機能における Boundary モデリングの自動想起を目的とする。

**重要**: AI の学習データには「Boundary をモデリングする」という発想がほとんど含まれていない。
このスキルにより、UI 機能の設計・実装時に Boundary パターンを自動的に想起させる。

---

## 適用場面

- UI を持つ機能の設計・実装
- フォーム、一覧画面、詳細画面の作成
- 操作可否判定（ボタン活性/非活性）
- ユーザーの意図（Intent）に基づく操作

---

## Boundary パターンの核心

**業務ロジックは Entity が持つ。BoundaryService は委譲のみ。**

```
UI → BoundaryService → Entity.CanXxx()
       ↓                    ↓
    データ取得のみ      業務ルール判定
```

---

## 開発フロー（推奨順序）

### Step 1: Intent 定義

ユーザーができる操作（意図）を列挙する。

```csharp
// 例: 注文画面の Intent
public enum OrderIntent
{
    Pay,      // 支払い
    Cancel,   // キャンセル
    View      // 詳細表示
}
```

### Step 2: Entity.CanXxx() 設計

各 Intent に対応する CanXxx() メソッドを Entity に実装する。

```csharp
public class Order : AggregateRoot<OrderId>
{
    public BoundaryDecision CanPay()
    {
        return Status switch
        {
            OrderStatus.Pending => BoundaryDecision.Allow(),
            OrderStatus.Paid => BoundaryDecision.Deny("既に支払い済みです"),
            OrderStatus.Cancelled => BoundaryDecision.Deny("キャンセル済みの注文です"),
            _ => BoundaryDecision.Deny("この状態では支払いできません")
        };
    }

    public BoundaryDecision CanCancel()
    {
        if (Status == OrderStatus.Paid)
            return BoundaryDecision.Deny("支払い済みの注文はキャンセルできません");

        if (Status == OrderStatus.Cancelled)
            return BoundaryDecision.Deny("既にキャンセル済みです");

        return BoundaryDecision.Allow();
    }
}
```

### Step 3: BoundaryService 実装

データ取得と Entity への委譲のみを行う。

```csharp
public class OrderBoundaryService : IOrderBoundary
{
    private readonly IOrderRepository _repository;

    public async Task<BoundaryDecision> ValidatePayAsync(OrderId id, CancellationToken ct)
    {
        var order = await _repository.GetByIdAsync(id, ct);

        // 存在チェックのみ許可
        if (order == null)
            return BoundaryDecision.Deny("注文が見つかりません");

        // ★ 業務ロジックは Entity に委譲
        return order.CanPay();
    }
}
```

---

## BoundaryDecision クラス

```csharp
public sealed class BoundaryDecision
{
    public bool IsAllowed { get; }
    public string? Reason { get; }

    private BoundaryDecision(bool isAllowed, string? reason = null)
    {
        IsAllowed = isAllowed;
        Reason = reason;
    }

    public static BoundaryDecision Allow() => new(true);
    public static BoundaryDecision Deny(string reason) => new(false, reason);
}
```

---

## 禁止事項

### BoundaryService に業務ロジックを書かない

```csharp
// ❌ 禁止: BoundaryService に業務ロジック
public async Task<BoundaryDecision> ValidatePayAsync(OrderId id, CancellationToken ct)
{
    var order = await _repository.GetByIdAsync(id, ct);

    // ↓ これは業務ロジック！Entity.CanPay() に移動すべき
    if (order.Status == OrderStatus.Paid)
        return BoundaryDecision.Deny("既に支払い済みです");

    return BoundaryDecision.Allow();
}
```

---

## 優先権のある操作（FR-021 対策）

Ready 状態の予約者がいる場合など、優先権を考慮する必要がある場合：

```csharp
// Entity.CanBorrow に優先権エンティティを渡す
public BoundaryDecision CanBorrow(MemberId memberId, MemberId? readyReserverId)
{
    if (Status != BookCopyStatus.Available && Status != BookCopyStatus.Reserved)
        return BoundaryDecision.Deny("このコピーは貸出可能状態ではありません");

    // ★ Ready状態の予約者がいる場合、その人以外は Deny
    if (readyReserverId.HasValue && readyReserverId.Value != memberId)
    {
        return BoundaryDecision.Deny(
            "予約者に優先権があります。予約者の貸出処理をお待ちください。");
    }

    return BoundaryDecision.Allow();
}
```

---

## チェックリスト

UI がある機能を設計・実装する際は、以下を確認：

```
□ Intent（ユーザーの意図）を列挙したか？
□ 各 Intent に対応する Entity.CanXxx() を設計したか？
□ CanXxx() は BoundaryDecision を返すか？
□ BoundaryService に業務ロジック（if 文）がないか？
□ 優先権のある操作は CanXxx() に優先権エンティティを渡しているか？
```

---

## 計画が不完全とみなされる条件

| 条件 | 判定 |
|-----|------|
| UI があるのに Boundary セクションがない | ❌ 不完全 |
| Intent が定義されていない | ❌ 不完全 |
| Entity.CanXxx() の設計がない | ❌ 不完全 |
| 「後から Boundary を追加する」という計画 | ❌ 不完全 |

---

## 参照

詳細は `catalog/patterns/boundary-pattern.yaml` を参照。
