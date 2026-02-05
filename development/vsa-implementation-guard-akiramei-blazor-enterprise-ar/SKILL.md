---
name: vsa-implementation-guard
description: >
  Blazor VSA アーキテクチャの実装ミス防止ガード。Handler、Validator、
  BoundaryService、Entity などの C# コードを生成・修正する際に自動的に
  適用される知識。SaveChangesAsync の禁止、BoundaryService での業務ロジック
  禁止、Result<T> パターンの強制、Value Object 比較ルールなど、
  カタログ駆動開発で頻発する実装ミスを防止する。
allowed-tools:
  - Read
  - Glob
  - Grep
---

# VSA Implementation Guard

このスキルは Blazor VSA 実装時の自動ミス防止を目的とする。

C# コードを生成・修正する際に、このスキルの知識が自動的に適用される。

---

## 適用場面

- C# コードの生成・修正
- MediatR Handler の実装
- FluentValidation Validator の実装
- BoundaryService の実装
- Entity の CanXxx() メソッド実装

---

## 禁止事項（NEVER DO）

### 1. Handler 内で SaveChangesAsync() を呼ばない

```csharp
// ❌ 禁止
public async Task<Result<Guid>> Handle(CreateProductCommand request, CancellationToken ct)
{
    var entity = new Product(...);
    await _repository.AddAsync(entity, ct);
    await _dbContext.SaveChangesAsync(ct);  // ← これを書かない！
    return Result.Success(entity.Id);
}

// ✅ 正しい
public async Task<Result<Guid>> Handle(CreateProductCommand request, CancellationToken ct)
{
    var entity = new Product(...);
    await _repository.AddAsync(entity, ct);
    return Result.Success(entity.Id);  // TransactionBehavior が SaveChanges を実行
}
```

**理由**: `TransactionBehavior` が Handler 実行後に自動で `SaveChangesAsync` を呼び出す。

---

### 2. BoundaryService に業務ロジック（if文）を書かない

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

// ✅ 正しい: Entity に委譲
public async Task<BoundaryDecision> ValidatePayAsync(OrderId id, CancellationToken ct)
{
    var order = await _repository.GetByIdAsync(id, ct);
    if (order == null)
        return BoundaryDecision.Deny("注文が見つかりません");  // 存在チェックのみ許可

    return order.CanPay();  // ★ 業務ロジックは Entity に委譲
}
```

**理由**: 業務ロジックは Entity が持つ。BoundaryService は委譲のみ。

---

### 3. 例外を throw してエラーを伝播しない

```csharp
// ❌ 禁止
if (product == null)
    throw new NotFoundException("Product not found");

// ✅ 正しい
if (product == null)
    return Result.Fail<Product>("Product not found");
```

**理由**: 例外は本当に予期しないエラーのみ。ビジネスロジック上のエラーは `Result<T>` で伝播。

---

### 4. Value Object の比較で .Value プロパティにアクセスしない

```csharp
// ❌ LINQ変換エラー
var board = await _dbContext.Boards
    .Where(b => b.Id.Value == guid)  // EF Core が変換できない
    .FirstOrDefaultAsync();

// ✅ 正しい: インスタンス同士で比較
var boardId = BoardId.From(guid);
var board = await _dbContext.Boards
    .Where(b => b.Id == boardId)
    .FirstOrDefaultAsync();
```

**理由**: EF Core は `.Value` プロパティへのアクセスを SQL に変換できない。

---

### 5. Validator で DB アクセスしない

```csharp
// ❌ 禁止: Validator 内で DB アクセス
public class CreateBookingValidator : AbstractValidator<CreateBookingCommand>
{
    public CreateBookingValidator(IBookingRepository repo)
    {
        RuleFor(x => x.RoomId)
            .MustAsync(async (roomId, ct) => await repo.ExistsAsync(roomId, ct))
            .WithMessage("会議室が存在しません");
    }
}

// ✅ 正しい: 形式検証のみ
public class CreateBookingValidator : AbstractValidator<CreateBookingCommand>
{
    public CreateBookingValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(100);
        RuleFor(x => x.StartTime).LessThan(x => x.EndTime);
    }
}
```

**理由**: ValidationBehavior は形式検証のみ。存在確認は Handler 内で行う。

---

### 6. Handler のメソッド名を HandleAsync にしない

```csharp
// ❌ 禁止
public async Task<Result<Guid>> HandleAsync(...)

// ✅ 正しい
public async Task<Result<Guid>> Handle(...)
```

**理由**: MediatR は `Handle` という名前のメソッドを探す。`HandleAsync` は規約外。

---

### 7. Singleton で DbContext を注入しない

```csharp
// ❌ 禁止: Captive Dependency 問題
services.AddSingleton<IMyService, MyService>();

// ✅ 正しい: すべて Scoped
services.AddScoped<IMyService, MyService>();
```

**理由**: MediatR は Scoped で動作。Singleton が Scoped の依存関係を持つと問題発生。

---

## 必須パターン

| 項目 | ルール |
|-----|-------|
| Command 戻り値 | `Result<T>` |
| サービス登録 | Scoped |
| Command インターフェース | `ICommand<Result<T>>`（`IRequest<T>` 直接使用禁止） |
| Handler メソッド名 | `Handle`（`HandleAsync` 禁止） |

---

## 実装前チェックリスト

```
□ Handler 内で SaveChangesAsync を呼んでいないか？
□ BoundaryService に業務ロジック（if文）がないか？
□ Entity に CanXxx() メソッドがあるか？
□ Result<T> でエラーを返しているか？
□ Value Object はインスタンス同士で比較しているか？
□ Validator は形式検証のみか？
□ サービスは Scoped で登録しているか？
```

---

## 参照

詳細は `catalog/COMMON_MISTAKES.md` を参照。
