---
name: boundary-observation
description: "境界条件・エッジケースの観測。null/空/0/最大値/最小値/オーバーフロー/タイムゾーン等を網羅的にテスト。Use when: テスト設計、バリデーション実装、パーサー実装、日付/金額処理、例は通るが端で壊れる疑い、バグ修正後の再発防止。"
---

# Boundary Observation（境界条件観測）

## 目的

生成コードは「平均的なケースに強く、端に弱い」傾向がある。
このスキルは、入力空間の端での欠陥を発見し、**自己欺瞞を崩す**。

## 観測の恩恵

- "未知の未知"を減らす（狙っていない入力で壊す）
- 境界条件が「仕様に昇格」し、次回生成の精度が上がる
- バグが潜伏しやすい箇所（パーサ、日付、金額、状態遷移）が早く炙り出せる

## Procedure

### Step 1: 外部境界の特定

対象コードの「外部境界」を列挙する。

**外部境界の例**：
- API入力（リクエストパラメータ）
- DB境界（クエリ結果、NULL可能性）
- ファイル境界（サイズ、エンコーディング）
- 時間境界（タイムゾーン、DST、うるう年）
- 数値境界（0、負数、最大値、オーバーフロー）

### Step 2: 境界値テストの設計

各外部境界に対して、以下のテストケースを設計する：

| カテゴリ | テストケース |
|----------|-------------|
| 最小値 | 下限値、下限-1 |
| 最大値 | 上限値、上限+1 |
| 空/null | null、空文字、空配列 |
| 異常値 | 不正な型、不正なフォーマット |

### Step 3: プロパティベーステスト（性質テスト）

重要なロジックに対して、**期待値に依存しない**性質テストを1本以上設計する。

**検証すべき性質の例**：
- **単調性**: f(a) ≤ f(b) if a ≤ b
- **可逆性**: decode(encode(x)) == x
- **冪等性**: f(f(x)) == f(x)
- **保存則**: sum(before) == sum(after)
- **交換律**: f(a, b) == f(b, a)

### Step 4: ファズテスト（必要に応じて）

以下のコンポーネントには特にファズテストが効く：
- パーサー
- デコーダー
- 正規化処理
- 文字コード変換

### Step 5: 入力分布の観測（運用時）

実際にどんな値が来ているかを観測し、テストケースを補強する。

## 最小セット

- **(B1)** 境界値テスト：外部境界ごとに「最小・最大・空・異常」
- **(B2)** 重要ロジックに1つだけでも"性質テスト"を入れる

## 境界値カタログ

詳細は `references/boundary-catalog.md` を参照。

## Outputs

- 境界値テストコード
- プロパティテストコード（QuickCheck / Hypothesis / fast-check 等）
- ファズテスト設定（必要に応じて）

## Examples

### 日付処理の境界値テスト

```python
# 境界値テスト
@pytest.mark.parametrize("date_str,expected", [
    ("2024-01-01", date(2024, 1, 1)),      # 通常
    ("2024-02-29", date(2024, 2, 29)),     # うるう年
    ("2023-02-29", ValueError),            # 非うるう年 → 異常
    ("", ValueError),                      # 空文字
    (None, TypeError),                     # null
    ("9999-12-31", date(9999, 12, 31)),   # 最大年
])
def test_parse_date_boundaries(date_str, expected):
    ...
```

### 金額計算のプロパティテスト

```python
# 性質テスト: 金額の加算は交換律を満たす
from hypothesis import given, strategies as st

@given(st.integers(min_value=0), st.integers(min_value=0))
def test_add_money_commutative(a, b):
    assert add_money(a, b) == add_money(b, a)

# 性質テスト: 割引後の金額は元の金額以下
@given(st.integers(min_value=0, max_value=1000000), st.floats(min_value=0, max_value=1))
def test_discount_reduces_price(price, discount_rate):
    result = apply_discount(price, discount_rate)
    assert result <= price
```
