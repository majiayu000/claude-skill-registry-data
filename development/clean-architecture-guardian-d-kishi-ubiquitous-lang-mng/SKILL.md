---
name: clean-architecture-guardian
description: Clean Architecture準拠性を自動チェック（循環依存・namespace階層・レイヤー間参照制約）。新規実装時・リファクタリング時・Step完了時に使用。Phase B1で97点品質を達成した知見を適用。
allowed-tools: Read, Grep
---

# Clean Architecture Guardian Skill

## 概要

このSkillは、F# + C# Clean Architecture実装の準拠性を自動的にチェックします。Phase B1で確立した97点品質基準を自動維持します。

## 使用タイミング

Claudeは以下の状況でこのSkillを自律的に使用すべきです：

1. **新規実装時**
   - 新規クラス・モジュール作成時
   - 新規Bounded Context追加時
   - レイヤー間の新規依存関係作成時

2. **リファクタリング時**
   - コード移動時
   - namespace変更時
   - プロジェクト参照変更時

3. **Step/Phase完了時**
   - Step完了チェック時
   - Phase完了検証時
   - 統合ビルド前

4. **問題発生時**
   - 循環依存エラー発生時
   - namespace衝突発生時
   - ビルドエラー発生時

## チェック項目

### 1. レイヤー分離原則

**詳細**: [`rules/layer-separation.md`](./rules/layer-separation.md)

**チェックポイント**:
- ✅ C# → F#依存は許可（Application層・UI層からDomain層呼び出し）
- ❌ F# → C#依存は禁止（Clean Architecture依存関係ルール準拠）
- ✅ 各層の責務分離（Domain/Application/Infrastructure/Web）
- ✅ 循環依存ゼロ

**典型的な問題**: `Error: Circular dependency detected between projects`

### 2. namespace階層化ルール

**詳細**: [`rules/namespace-design.md`](./rules/namespace-design.md)

**チェックポイント**:
- ✅ Bounded Context別サブnamespace使用
- ✅ 基本テンプレート準拠: `<ProjectName>.<Layer>.<BoundedContext>[.<Feature>]`
- ✅ 階層制限遵守（3階層推奨、4階層許容）
- ✅ F# Compilation Order制約対応

**典型的な問題**: `Error: The type or namespace name 'ProjectManagement' does not exist`

### 3. Bounded Context境界

**チェックポイント**:
- ✅ Common境界: 全境界文脈共通定義のみ
- ✅ Authentication境界: ユーザー・認証・権限管理
- ✅ ProjectManagement境界: プロジェクト管理
- ✅ UbiquitousLanguageManagement境界: ユビキタス言語管理
- ✅ DomainManagement境界: ドメイン管理（Phase C予定）

**典型的な問題**: 境界を越えた不適切な依存関係

### 4. F# Compilation Order

**チェックポイント**:
- ✅ Common → Authentication → ProjectManagement → UbiquitousLanguageManagement
- ✅ ValueObjects → Errors → Entities → DomainServices
- ✅ 前方参照なし（F#制約）

**典型的な問題**: `Error: The type 'ProjectId' is used before it is defined`

## 品質基準（Phase B1確立）

### Clean Architecture スコア: 97点

| 観点 | 目標 | Phase B1達成 |
|------|------|--------------|
| **依存関係の正しさ** | 100% | ✅ 100% |
| **循環依存** | 0件 | ✅ 0件 |
| **レイヤー責務分離** | 100% | ✅ 100% |
| **namespace階層化** | 100% | ✅ 100% |
| **Bounded Context分離** | 95%+ | ✅ 97% |

### ビルド品質基準

- ✅ **0 Warning**: 警告ゼロ維持
- ✅ **0 Error**: エラーゼロ維持
- ✅ **テスト100%成功**: 全テスト成功維持

## 自動チェック手順

### 1. 依存関係チェック

```
# プロジェクト参照を確認
Grep "ProjectReference" *.csproj *.fsproj

# 不正な依存（Domain → Infrastructure等）を検出
```

### 2. namespace階層チェック

```
# namespace宣言を確認
Grep "namespace UbiquitousLanguageManager" *.cs *.fs

# 基本テンプレート準拠を検証
# 期待: <ProjectName>.<Layer>.<BoundedContext>[.<Feature>]
```

### 3. Bounded Context境界チェック

```
# using/open文を確認
Grep "using UbiquitousLanguageManager" *.cs
Grep "open UbiquitousLanguageManager" *.fs

# 境界を越える不適切な参照を検出
```

### 4. F# Compilation Orderチェック

```
# .fsprojファイルのCompile順序を確認
Read src/UbiquitousLanguageManager.Domain/UbiquitousLanguageManager.Domain.fsproj

# Common → Authentication → ProjectManagement順序を検証
```

## よくある違反パターンと修正方法

### 違反1: F# → C#依存

```
❌ 誤り: Domain層からInfrastructure層への参照
<ProjectReference Include="..\UbiquitousLanguageManager.Infrastructure\..." />
```

**修正**: 依存関係逆転の原則（DIP）適用
```
✅ 正しい: Domain層でInterface定義、Infrastructure層で実装
// Domain層
type IProjectRepository = ...

// Infrastructure層（C#）
public class ProjectRepository : IProjectRepository { ... }
```

### 違反2: フラットnamespace

```
❌ 誤り: Bounded Contextなしのフラットnamespace
namespace UbiquitousLanguageManager.Domain

type Project = ...
type User = ...  // 異なる境界文脈が混在
```

**修正**: Bounded Context別サブnamespace
```
✅ 正しい: 境界文脈別に分離
namespace UbiquitousLanguageManager.Domain.ProjectManagement
type Project = ...

namespace UbiquitousLanguageManager.Domain.Authentication
type User = ...
```

### 違反3: 循環依存

```
❌ 誤り: Application ⇄ Infrastructure 循環参照
```

**修正**: Clean Architecture依存方向遵守
```
✅ 正しい: Infrastructure → Application → Domain（一方向のみ）
```

### 違反4: F# Compilation Order違反

```
❌ 誤り: ProjectManagementがCommonより前
<Compile Include="ProjectManagement\ProjectEntities.fs" />
<Compile Include="Common\CommonTypes.fs" />
```

**修正**: 依存順序に並べ替え
```
✅ 正しい: Commonを最初に配置
<Compile Include="Common\CommonTypes.fs" />
<Compile Include="ProjectManagement\ProjectEntities.fs" />
```

## Phase B1での実証結果

### 実装影響（Phase B1 Step5）

- **修正ファイル数**: 42ファイル
- **修正時間**: 3.5-4.5時間
- **エラー種別**: namespace階層化・型衝突解決
- **最終品質**: 0 Warning/0 Error・全32テスト成功

### 確立した知見

1. **事前検証の重要性**: Step開始前にnamespace構造レビュー実施
2. **段階的移行**: プロジェクト単位での段階的移行
3. **ロールバック準備**: Step単位でのgit commit

## 関連Agents

- **design-review**: システム設計・Clean Architecture準拠確認
- **dependency-analysis**: 依存関係特定・実装順序決定
- **code-review**: コード品質・Clean Architecture準拠レビュー

## 注意事項

1. **Phase開始前に必ずチェック**: Phase B1 Step5の教訓
2. **検証プロセス実行**: Step開始時・Phase完了時の検証必須
3. **97点品質維持**: Phase B1で確立した品質基準を下回らない
4. **Bounded Context追加時**: ADR_019再確認必須

## 参考資料

- Phase B1 Step5実装記録: `Doc/08_Organization/Completed/Phase_B1/Step05_namespace階層化.md`
- Phase B1完了報告: `Doc/08_Organization/Completed/Phase_B1/Phase_Summary.md`
- GitHub Issue #42: namespace階層化対応Issue
