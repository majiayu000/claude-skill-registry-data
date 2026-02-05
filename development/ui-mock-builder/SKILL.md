---
name: ui-mock-builder
description: SwiftUIを使ったiOSアプリのUI実装を支援するスキル。View + #Preview macroを生成し、既存の共通コンポーネントを活用しながら効率的にUIを構築する。以下のような場合にこのスキルを使用: (1)「〇〇画面を作って」のような画面作成リクエスト (2)「〇〇のUIをデザインして」のようなUIデザインリクエスト (3)「このコンポーネントを実装して」のようなコンポーネント実装リクエスト (4) SwiftUIのView作成全般
---

# iOS UI Builder

SwiftUIを使ったiOSアプリのUI実装を支援するスキル。

## [超重要]UIデザインに関する方針

- iOSの設定アプリのような、システム標準のパーツを多くつかって構成されたデザインは、退屈で面白みがないので避ける。例えば:
  - 背景色
  - tint color
  - フォント(タイポグラフィ)
  - corner radius
- トグルはシステム標準のコンポーネントを使う。似た見た目のものを再発明してはいけない。tint colorは調整して良い。
- 既存の画面があれば、そのトンマナを引き継ぐ。色やcornerRadius、paddingのようなパラメータは共通化されているものがあればそれを使う。適切に共通化する。
- 要件から想像できる理想の世界観をデザインする。ユーティリティ系のアプリであれば整然と、特定の分野や用途に寄ったものであれば、その世界観を反映した色やレイアウトを選択する。
- デザイン方針について、ユーザーに説明する。
- 背景色(グラデーション含む)、ScrollViewを使う場合は、コンテンツの横幅に注意する。多くの場合、 `.frame(maxWidth: .infinity)` をつけないと横幅いっぱいに表示されない。
- 情報を画面に並べる際は、その情報の性質から、1列で表示するべきか、2列で表示するべきか、単なるUIとしてではなく情報設計上のあるべき表現について検討する。
  - 特に、奇数と2列表示は相性が悪いということを留意する。
- ライトモード/ダークモードいずれも違和感のない色使いになるようにすること。

関連ドキュメント

- references/animation.md
- references/color.md
- references/grid-layout.md

## ワークフロー

### 1. 要件の明確化

ユーザーの説明から以下を把握する:
- 画面/コンポーネントの目的
- 必要なUI要素（ボタン、リスト、入力フィールド等）
- ユーザーインタラクション（タップ、スワイプ等）
- 表示するデータの種類

不明点があれば質問して明確にする。

### 2. 既存コンポーネントの確認（重要）

**実装前に必ず既存コードを確認する。**

プロジェクト内で以下を検索:
- 共通コンポーネント（`Components/`, `Views/Common/`, `Shared/`等）
- 類似の画面・コンポーネント
- デザインシステム関連ファイル（`Theme`, `Style`, `Color`等）

既存コンポーネントを見つけた場合:
- 可能な限り再利用する
- 拡張が必要なら既存を拡張
- 新規作成が必要な場合のみ新しく作成

### 3. デザイン設計

実装前にデザインの概要をユーザーに説明:
- レイアウト構造（VStack/HStack/ZStack等）
- 使用するコンポーネント
- 色やスペーシングの方針

### 4. View + #Preview実装

#### 基本構造

```swift
import SwiftUI

struct [ViewName]View: View {
    // MARK: - Properties

    // MARK: - Body
    var body: some View {
        // 実装
    }
}

// MARK: - Preview
#Preview {
    [ViewName]View()
}
```

#### Previewの充実（重要）

#Preview macroで複数のプレビューバリエーションを提供:

```swift
#Preview("Default") {
    [ViewName]View()
}

#Preview("With Data") {
    [ViewName]View(items: sampleItems)
}

#Preview("Empty State") {
    [ViewName]View(items: [])
}

#Preview("Dark Mode") {
    [ViewName]View()
        .preferredColorScheme(.dark)
}
```

状況に応じて以下も追加:
- 異なるデバイスサイズ
- Dynamic Type対応確認
- ローディング状態
- エラー状態

### 5. コンポーネント化の判断

以下の場合はコンポーネントとして分離:
- 他の画面でも使えそうな汎用的なUI
- 複雑で独立したロジックを持つ部分
- 繰り返し使われるパターン

コンポーネント化する場合:
- 適切なディレクトリに配置（`Components/`等）
- 汎用的なAPIを設計
- 単体での#Previewを提供

## SwiftUIベストプラクティス

### レイアウト
- `VStack`, `HStack`, `ZStack`を適切に使い分ける
- `Spacer()`でフレキシブルなスペーシング
- `padding()`で一貫したマージン
- `frame()`は必要最小限に

### 再利用性
- ViewModifierで共通スタイルを定義
- Extensionで便利なメソッドを追加
- @ViewBuilderで柔軟なコンポーネント

### パフォーマンス
- 大きなViewは小さなサブViewに分割
- 必要に応じて`@State`, `@Binding`を使用
- リストは`LazyVStack`/`LazyHStack`を検討

## チェックリスト

実装完了時に確認:
- [ ] 既存コンポーネントを確認したか
- [ ] #Previewが複数パターン用意されているか
- [ ] 色に関してガイドラインに沿っているか
- [ ] 再利用可能な部分をコンポーネント化したか
