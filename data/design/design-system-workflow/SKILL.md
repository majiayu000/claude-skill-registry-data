---
name: design-system-workflow
description: Swift Design Systemを使用したiOS UI実装スキル。デザイントークン（カラー、タイポグラフィ、スペーシング、角丸、モーション、エレベーション）、UIコンポーネント（Button、Card、Chip、FAB、Snackbar、Picker）、レイアウトパターン（AspectGrid、SectionCard）のベストプラクティスを提供。「デザイン」「UI」「テーマ」「カラー」「色」「タイポグラフィ」「フォント」「スペーシング」「余白」「角丸」「アニメーション」「ボタン」「カード」「チップ」「グリッド」「レイアウト」「FAB」「Snackbar」「Picker」「SwiftUI」「DesignSystem」などのキーワードで自動適用。
---

# Swift Design System スキル

no problem製iOSアプリのUI実装に必須のデザインシステム。一貫性のあるUIを効率的に構築するためのトークン・コンポーネント・パターンを提供。

---

## 必須依存関係

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/no-problem-dev/swift-design-system.git", from: "X.X.X")
]

// ターゲット
.target(
    name: "YourApp",
    dependencies: [
        .product(name: "DesignSystem", package: "swift-design-system")
    ]
)
```

> **Note**: `X.X.X` には最新バージョンを指定してください。
> 最新バージョンは [GitHub Releases](https://github.com/no-problem-dev/swift-design-system/releases) で確認できます。

---

## 設計原則

### 3層トークンシステム

```
Primitive Tokens (基本値) - 直接使用禁止
    ↓ 参照
Semantic Tokens (意味的トークン) - 推奨
    ↓ 参照
Component Tokens (コンポーネント固有) - 自動適用
```

**重要**: Primitiveトークンは直接使用せず、必ずSemantic/Componentトークンを使用すること。

### Environment経由のアクセス

```swift
@Environment(\.colorPalette) var colors
@Environment(\.spacingScale) var spacing
@Environment(\.radiusScale) var radius
@Environment(\.motion) var motion
```

### 型安全性

プロトコルベースの設計により、カスタムテーマ・トークンの拡張が可能。

### アクセシビリティ

- WCAG AAA準拠のコントラスト
- reduce motion設定の自動尊重
- Dynamic Type対応

---

## テーマ設定（必須）

アプリ起動時に必ずThemeProviderを設定:

```swift
import DesignSystem

@main
struct MyApp: App {
    @State private var themeProvider = ThemeProvider()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .theme(themeProvider)  // 必須
        }
    }
}
```

詳細は → **references/patterns/THEME.md**

---

## Good / Bad パターン（代表例）

### カラー

```swift
// ✅ Good: セマンティックカラーを使用
Text("エラー").foregroundColor(colors.error)

// ❌ Bad: ハードコードされた色
Text("エラー").foregroundColor(.red)
```

### タイポグラフィ

```swift
// ✅ Good: typographyモディファイアを使用
Text("見出し").typography(.headlineLarge)

// ❌ Bad: 直接フォント指定
Text("見出し").font(.system(size: 32, weight: .semibold))
```

### スペーシング

```swift
// ✅ Good: スペーシングトークンを使用
VStack(spacing: spacing.lg) { ... }

// ❌ Bad: マジックナンバー
VStack(spacing: 16) { ... }
```

### コンポーネント

```swift
// ✅ Good: デザインシステムのコンポーネントを使用
Card(elevation: .level2) { content }

// ❌ Bad: 独自実装
RoundedRectangle(cornerRadius: 8)
    .fill(Color.white)
    .shadow(radius: 4)
```

---

## リファレンス索引

デザイン実装時は、該当するリファレンスを参照してください。

### デザイントークン

**すべてのUI実装で必須の知識**

→ **references/TOKENS.md**
- Color（カラーパレット）
- Typography（タイポグラフィ）
- Spacing（スペーシング）
- Radius（角丸）
- Motion（アニメーション）
- Elevation（エレベーション）
- GridSpacing（グリッド間隔）

---

### コンポーネント

| コンポーネント | 用途 | リファレンス |
|--------------|------|-------------|
| **Button** | アクションボタン | → references/components/BUTTON.md |
| **Card** | コンテンツコンテナ | → references/components/CARD.md |
| **Chip** | タグ、フィルター | → references/components/CHIP.md |
| **FAB** | 浮遊アクションボタン | → references/components/FAB.md |
| **Snackbar** | 一時的通知 | → references/components/SNACKBAR.md |
| **IconPicker** | SF Symbols選択 | → references/components/ICON_PICKER.md |
| **EmojiPicker** | 絵文字選択 | → references/components/EMOJI_PICKER.md |
| **ColorPicker** | カラー選択 | → references/components/COLOR_PICKER.md |
| **ImagePicker** | 画像選択 | → references/components/IMAGE_PICKER.md |

---

### レイアウトパターン

| パターン | 用途 | リファレンス |
|---------|------|-------------|
| **Theme** | テーマ設定・切り替え | → references/patterns/THEME.md |
| **AspectGrid** | アスペクト比統一グリッド | → references/patterns/ASPECT_GRID.md |
| **SectionCard** | タイトル付きカードセクション | → references/patterns/SECTION_CARD.md |

---

## 関連スキル

- **ios-clean-architecture**: アーキテクチャ設計（View層で本スキルを活用）
- **ios-build-workflow**: ビルド・テスト実行
