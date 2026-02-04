---
name: material3-expressive
description: Material 3 Expressiveガイドラインに沿ったUI実装を提供するスキル。Jetpack Composeで画面やコンポーネントを作成する際に使用。MotionScheme、新しいExpressiveコンポーネント、テーマ設定のパターンを提供。
---

# Material 3 Expressive UI作成ガイド

Jetpack ComposeでUI作成時は **Material 3 Expressive** のガイドラインに従う。

## 必須要件

| 要件 | 値 |
|------|-----|
| minSdk | 23以上 |
| Material3 | 1.5.0-alpha以上（Expressiveコンポーネント含む） |
| OptIn | `@OptIn(ExperimentalMaterial3ExpressiveApi::class)` |

## クイックリファレンス

### テーマ設定
```kotlin
MaterialTheme(
    colorScheme = colorScheme,
    typography = typography,
    shapes = shapes,
    motionScheme = MotionScheme.expressive()
) { content() }
```

### 推奨コンポーネント

| 用途 | コンポーネント | 備考 |
|------|----------------|------|
| 読み込み表示 | `LoadingIndicator` | 5秒未満の待機時間用 |
| 読み込み表示（コンテナ付き） | `ContainedLoadingIndicator` | - |
| ボトムツールバー | `DockedToolbar` | BottomAppBarの代替 |
| フローティングツールバー | `FloatingToolbar` | 水平・垂直対応 |
| 可変ボトムバー | `FlexibleBottomAppBar` | スクロール連動 |

### 非推奨 → 代替

| 非推奨 | 代替 |
|--------|------|
| `BottomAppBar` | `DockedToolbar` |
| `CircularProgressIndicator`（短時間） | `LoadingIndicator` |

## ベストプラクティス

1. `MotionScheme.expressive()` で流れるようなアニメーション
2. 形状のモーフィングを活用
3. カラーロールを遵守（アクセシビリティ自動対応）
4. Android 12+でダイナミックカラーをサポート
5. Elevationはトーナルカラーオーバーレイで表現

## 詳細

- コンポーネント詳細・テーマ設定: `REFERENCE.md`
- 実装例: `EXAMPLES.md`