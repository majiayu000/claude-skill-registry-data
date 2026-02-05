---
name: ios-design-direction
description: |
  iOSアプリのデザイン哲学とクリエイティブディレクション。Apple Human Interface Guidelinesに基づく
  Clarity/Deference/Depthの原則、SwiftUIによる実装パターン、アクセシビリティ設計を包括的にガイド。
  使用タイミング: (1) 新規アプリのUI/UX設計時、(2) デザインシステム構築時、(3) SwiftUIコンポーネント設計時、
  (4) 「iOSらしいデザインにしたい」「HIGに準拠したい」、(5) アクセシビリティ対応時、
  (6) アニメーション・インタラクション設計時、(7) 複数プラットフォーム（iOS/iPadOS/watchOS/visionOS）対応時
---

# iOS Design Philosophy & Creative Direction

Apple Human Interface Guidelinesに基づくiOSアプリデザインの哲学と実装ガイド。

## ワークフロー

デザイン作業を開始する前に、以下の情報を確認する。

### Step 1: 要件確認（必須）

以下をユーザーに確認：

1. **ターゲットプラットフォーム**
   - iOS / iPadOS / watchOS / visionOS のどれか（複数可）
   - 最小対応OSバージョン（例: iOS 15+, iOS 17+）

2. **プロジェクトの性質**
   - 新規アプリ / 既存アプリの改修 / デザインシステム構築
   - アプリのカテゴリ（生産性、エンターテイメント、ヘルスケア等）

3. **既存資産の有無**
   - ブランドガイドライン（カラー、タイポグラフィ、ロゴ）
   - 既存のデザインシステム / コンポーネントライブラリ
   - Figma/Sketch等のデザインファイル

### Step 2: 制約と優先事項の確認

1. **アクセシビリティ要件**
   - 標準対応（WCAG AA）/ 高度な対応（WCAG AAA）
   - 特定の要件（VoiceOver必須、高齢者向け等）

2. **パフォーマンス制約**
   - ターゲットデバイス（最新機種のみ / 旧機種サポート）
   - アニメーション許容度（リッチ / 軽量）

3. **デザインの方向性**
   - システム標準に準拠 / カスタムブランド表現を重視
   - ミニマル / リッチ・表現的

### Step 3: 成果物の確認

何を作成するか確認：
- [ ] コンポーネント設計・実装
- [ ] 画面レイアウト設計
- [ ] デザイントークン定義
- [ ] アニメーション・トランジション設計
- [ ] アクセシビリティ対応の実装
- [ ] デザインレビュー・改善提案

---

確認完了後、以下のガイドラインを適用して作業を進める。

## Core Design Philosophy (HIG)

### 三原則

| 原則 | 意味 | 実践 |
|------|------|------|
| **Clarity** | テキスト・アイコン・装飾の明瞭性 | 読みやすいフォント、意味のあるアイコン、機能的な装飾 |
| **Deference** | コンテンツを主役に | UIは控えめに、コンテンツを邪魔しない、流動的な動き |
| **Depth** | 視覚的階層で理解を促進 | レイヤー、リアルな動き、発見の喜び |

## Creative Direction Framework

### Visual Hierarchy
```
Primary   → ユーザーの注目を集める要素（CTA、重要情報）
Secondary → 補助的情報（サブテキスト、メタデータ）
Tertiary  → 背景・コンテナ要素
```

### Emotional Design
- **Delight**: 予期せぬ楽しい瞬間を演出
- **Trust**: 一貫性と予測可能性で信頼構築
- **Flow**: 摩擦のない体験でタスク完了を支援

## Key Visual Elements

### Typography
| フォント | 用途 |
|----------|------|
| SF Pro | iOS/macOSのシステムフォント |
| SF Compact | watchOS、小さいスペース |
| SF Mono | コード、等幅テキスト |
| New York | セリフ体、読み物コンテンツ |

```swift
// Dynamic Type対応
Text("Title")
    .font(.largeTitle)  // 自動的にDynamic Type対応

// カスタムフォントでもDynamic Type
@ScaledMetric var fontSize: CGFloat = 17
Text("Body").font(.system(size: fontSize))
```

### Color
- **Semantic Colors**: `.primary`, `.secondary`, `.accent` を使用
- **Adaptive Colors**: ライト/ダークモード自動対応
- **High Contrast**: アクセシビリティ設定に対応

```swift
// ✅ Semantic Color（推奨）
Text("Label").foregroundStyle(.primary)
Rectangle().fill(.background)

// ✅ Asset Catalogでダークモード対応
Color("BrandColor")
```

### SF Symbols
```swift
// 基本
Image(systemName: "heart.fill")

// 可変シンボル
Image(systemName: "speaker.wave.3.fill")
    .symbolVariableValue(0.7)

// レンダリングモード
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.multicolor)
```

詳細は [references/visual-elements.md](references/visual-elements.md) を参照。

## Interaction Patterns

### Gestures
| ジェスチャー | 標準的な用途 |
|-------------|-------------|
| Tap | 選択・アクティベート |
| Long Press | コンテキストメニュー |
| Swipe | ナビゲーション・アクション |
| Pinch | ズーム |
| Rotate | 回転 |

### Feedback
```swift
// Haptic Feedback
let generator = UIImpactFeedbackGenerator(style: .medium)
generator.impactOccurred()

// SwiftUIでのsensoryFeedback
Button("Tap") { }
    .sensoryFeedback(.impact(weight: .medium), trigger: tapCount)
```

### Navigation
- **Tab Bar**: メインナビゲーション（5項目以下）
- **Navigation Stack**: 階層的ドリルダウン
- **Modal/Sheet**: 一時的なタスク・詳細

## Animation Philosophy

### 原則
1. **Purpose-driven**: 意味のあるアニメーションのみ
2. **Physics-based**: 自然な物理法則に従う
3. **Contextual timing**: 操作に応じた適切な長さ

### 推奨タイミング
| 操作 | Duration |
|------|----------|
| 軽い切り替え | 0.2-0.3秒 |
| 画面遷移 | 0.3-0.5秒 |
| 複雑なアニメーション | 0.5-0.8秒 |

```swift
// Spring Animation（推奨）
withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
    isExpanded.toggle()
}

// 明示的なタイミング
.animation(.easeInOut(duration: 0.25), value: selection)
```

詳細は [references/swiftui-patterns.md](references/swiftui-patterns.md) を参照。

## Platform Considerations

| Platform | 特徴 |
|----------|------|
| **iOS** | タッチ中心、片手操作考慮、Safe Area |
| **iPadOS** | マルチタスク、ポインタ対応、サイズクラス |
| **watchOS** | グランス可能、Digital Crown、小画面 |
| **visionOS** | 空間UI、視線+ジェスチャー、奥行き |

詳細は [references/platform-considerations.md](references/platform-considerations.md) を参照。

## SwiftUI Implementation

### Layout Patterns
```swift
// Adaptive Layout
ViewThatFits {
    HStack { content }  // 横に収まれば
    VStack { content }  // 縦にフォールバック
}

// Size Class対応
@Environment(\.horizontalSizeClass) var sizeClass

var body: some View {
    if sizeClass == .compact {
        CompactLayout()
    } else {
        RegularLayout()
    }
}
```

### Component Structure
```swift
struct FeatureCard: View {
    let feature: Feature
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Icon
            Image(systemName: feature.icon)
                .font(.title)
                .foregroundStyle(.accent)
            
            // Title
            Text(feature.title)
                .font(.headline)
            
            // Description
            Text(feature.description)
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}
```

## Accessibility (必須)

### 基本対応
```swift
// VoiceOver
Button(action: save) {
    Image(systemName: "square.and.arrow.down")
}
.accessibilityLabel("保存")
.accessibilityHint("現在の編集内容を保存します")

// Dynamic Type
Text("Body")
    .dynamicTypeSize(...DynamicTypeSize.accessibility3)

// Color Contrast
// 4.5:1以上のコントラスト比を確保
```

### チェックリスト
- [ ] すべてのインタラクティブ要素にaccessibilityLabelを設定
- [ ] Dynamic Typeで最大サイズでもレイアウトが崩れない
- [ ] 色のみに依存しない情報伝達
- [ ] タップターゲット44pt以上
- [ ] Reduce Motionへの対応

詳細は [references/accessibility-guide.md](references/accessibility-guide.md) を参照。

## Performance in Design

### 60fps維持
- 複雑なシェイプは`drawingGroup()`で最適化
- 大量の要素は`LazyVStack`/`LazyHGrid`を使用
- 重いビューは`task`で非同期初期化

### Asset最適化
- 画像は適切なスケール（@2x, @3x）で用意
- SVGよりPDFベクターを優先（小さいアセット）
- 大きな画像は圧縮・リサイズ

### Progressive Loading
```swift
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image.resizable().aspectRatio(contentMode: .fit)
    case .failure:
        Image(systemName: "photo")
    @unknown default:
        EmptyView()
    }
}
```

## Design Tokens Example

```swift
enum DesignTokens {
    enum Spacing {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 16
        static let lg: CGFloat = 24
        static let xl: CGFloat = 32
    }
    
    enum CornerRadius {
        static let small: CGFloat = 8
        static let medium: CGFloat = 12
        static let large: CGFloat = 16
        static let extraLarge: CGFloat = 24
    }
    
    enum Shadow {
        static let subtle = ShadowStyle(color: .black.opacity(0.1), radius: 4, y: 2)
        static let medium = ShadowStyle(color: .black.opacity(0.15), radius: 8, y: 4)
    }
}
```

## Critical Success Factors

1. **User-centered**: ユーザーの課題解決を最優先
2. **Consistency**: システム全体で一貫したパターン
3. **Iteration**: テスト→フィードバック→改善のサイクル
4. **Accessibility**: すべてのユーザーが使えるデザイン
5. **Platform Authenticity**: 各プラットフォームの慣習に従う
