---
name: bicep-what-if-analysis
description: Bicep/azd デプロイ前の what-if 分析。「差分確認」「変更影響」「破壊的変更」「デプロイしたら何が変わる」「Bicep と実リソースの比較」を求める場合に使用。
---

# Bicep What-If 分析

## 分析フロー（必須）

以下の手順に従う。スキップ不可。

### Step 1: サマリー実行

```bash
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh --summary
```

### Step 2: 結果確認（すべて報告、優先順位なし）

**重要**: 以下のすべての項目を同等に扱う。特定の項目を優先的に確認しない。

| 確認項目 | 0件でも報告 | 詳細確認が必要 |
|---------|-------------|---------------|
| `resourceDeletions` | Yes | リソース削除がある場合 |
| `destructiveChanges` | Yes | リソース再作成がある場合 |
| `changesWithDeletions` | Yes | **必ず詳細確認**（プロパティ削除） |
| `resourceCreations` | Yes | リソース作成がある場合 |
| `modifiedResources` | No（件数のみ） | - |
| `unsupported` | Yes（必ず詳細説明） | 説明が必要 |

**changesWithDeletions の重要性**:
- Bicep定義と実リソースの乖離を示す
- リソース再作成なしでも影響大の可能性
- 1件でもあれば、**必ず全プロパティを詳細確認**

**サポート外リソースの報告ルール**:
- サマリーに件数を含める場合、必ず詳細説明を追加する
- 「サポート外 (分析対象外・問題なし)」のように安心材料を併記する
- 対象リソースと理由を具体的に説明する
- 「デプロイは正常に実行される」ことを明記する

### Step 3: 詳細確認（プロセスベース）

`changesWithDeletions` が 1 件以上の場合、**必須**：

```bash
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh
```

**プロセスベースアプローチ（重要）**:

すべてのプロパティ削除に対して、以下のプロセスを**一律に**適用：

```
1. 削除されるプロパティを特定
   - トップレベル: properties.xxx
   - ネスト: properties.config.xxx
   - 配列要素: properties.subnets[1].xxx

2. Bicep定義を確認（grep/viewツール）
   - 定義あり → 次へ
   - 定義なし → 🔴 乖離

3. ARMリファレンスで readOnly を確認
   - readOnly: true → ✅ ノイズ
   - readOnly: false → ⚠️ 実削除
   - 不明 → ❓ 要調査
```

**禁止事項**:
- 特定のリソースタイプやプロパティだけを確認して終わらない
- 「重要そう」「起きやすそう」という事前判断をしない
- `potentiallyDestructive: false` のリソースをスキップしない
- 大量の変更があっても流し読みしない
- 「たぶんノイズだろう」と推測しない

**必須事項**:
- `changesWithDeletions` に含まれる**全リソースの全プロパティ**を列挙する
- 各プロパティに上記プロセスを適用する
- 判定根拠を明示する（Bicep定義の有無、readOnlyの値）
- 判定に自信がない場合は「要確認」と報告する（ノイズと推測しない）

### Step 4: 報告

1. サマリー表（変更タイプ別件数）
2. 注意が必要な変更の詳細
3. 各変更の評価（ノイズ / 実際の変更 / 要確認）
4. サポート外リソースの説明（件数が1件以上の場合）
5. 推奨アクション

**報告時の必須要素**:
- サポート外リソースがある場合、「問題ではない」ことを明示
- 単に「サポート外: N件」だけを記載しない
- 不安を与えずに、正確な情報を伝える

## スクリプトオプション

| オプション | 用途 |
|-----------|------|
| `--summary` | サマリー（最初に実行） |
| (なし) | フィルタ済み全出力 |
| `--raw` | Azure CLI 生出力 |
| `--template`, `--parameters` | カスタム指定 |

## 重要な概念

### プロパティ削除の意味

`changesWithDeletions` は **実リソースに存在する設定が Bicep に未定義** であることを示す。

- Bicep定義にないプロパティ → デプロイで削除される（**乖離**）
- Bicep定義にあるが読み取り専用 → デプロイしても適用されない（**ノイズ**）

リソース再作成を伴わなくても、セキュリティや可用性に影響する可能性がある。

### プロセスベースアプローチ

**チェックリストではなくプロセス**で評価する：

- 特定のリソースタイプ（VNet, NSG等）のリストに依存しない
- 特定のプロパティ（tags, networkSecurityGroup等）の優先順位付けをしない
- すべてのプロパティ削除に同じプロセスを一律適用
- 未知のリソースや新しいAzureサービスにも対応可能

評価プロセス:
1. Bicep定義を確認（定義の有無）
2. ARM リファレンスで readOnly を確認
3. 結果を報告（乖離 / ノイズ / 要調査）

### ノイズ判定

スクリプトは**明らかな読み取り専用プロパティ**（`provisioningState`, `etag` 等）のみを自動フィルタする。
それ以外のプロパティは、上記のプロセスで評価する。

判定基準の詳細は [references/noise.md](references/noise.md) を参照。

## 前提条件

- `azd env` 初期化済み
- Azure CLI ログイン済み
- azd プロジェクトルートで実行

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| "AZURE_LOCATION is not set" | `azd env refresh` |
| 大量の変更 | `--raw` で生出力確認 |
| 特定リソース確認 | `jq '.changes[] \| select(.resourceType == "xxx")'` |

## Dependencies

az, azd, jq, python3
