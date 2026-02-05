---
name: swiftui-components
description: SwiftUI UI component catalog. Use when implementing NavigationStack, Swift Charts, PhotosPicker, TipKit, ScrollView enhancements, animations, layouts, WebView, Liquid Glass and other UI components. Organized by feature category with OS version compatibility info. Reference for discovering available components and implementation patterns.
---

# SwiftUI UIコンポーネントカタログ

iOS 16以降で利用可能なSwiftUIコンポーネントを機能別に整理したリファレンス。

## ディレクトリ構成

```
swiftui-components/
├── SKILL.md (このファイル)
└── references/
    ├── navigation.md    # ナビゲーション
    ├── charts.md        # チャート・グラフ
    ├── scroll.md        # スクロール
    ├── media.md         # メディア・共有
    ├── animation.md     # アニメーション
    ├── layout.md        # レイアウト
    ├── tips.md          # TipKit
    ├── preview.md       # プレビュー
    ├── container.md     # コンテナ値
    ├── theming.md       # テーマ・デザイン
    └── webview.md       # WebView
```

## リファレンスファイル

### references/navigation.md
ナビゲーション関連コンポーネント：
- **NavigationStack** (iOS 16+): NavigationViewの後継、プログラマティックナビゲーション
- **NavigationSplitView** (iOS 16+): 2列/3列レイアウト対応
- **NavigationPath** (iOS 16+): 複数の型をサポートするナビゲーションパス
- **TabView刷新** (iOS 26+): 新デザイン・アニメーション

### references/charts.md
チャート・グラフ関連コンポーネント：
- **Swift Charts** (iOS 16+): LineMark, BarMark, AreaMark, PointMark等
- **Chart3D** (iOS 26+): 3Dチャートのネイティブサポート

### references/scroll.md
スクロール関連コンポーネント：
- **scrollPosition** (iOS 17+): スクロール位置の取得・設定
- **scrollTargetBehavior** (iOS 17+): スナップスクロール
- **containerRelativeFrame** (iOS 17+): 親コンテナに対する相対サイズ指定

### references/media.md
メディア・共有関連コンポーネント：
- **PhotosPicker** (iOS 16+): 写真ライブラリアクセス不要の写真選択
- **ShareLink** (iOS 16+): 標準シェア機能のSwiftUI対応
- **Transferable** (iOS 16+): データ転送プロトコル

### references/animation.md
アニメーション関連コンポーネント：
- **symbolEffect** (iOS 17+): SF Symbolsアニメーション
- **contentTransition** (iOS 17+): テキスト・コンテンツ変更アニメーション
- **phaseAnimator** (iOS 17+): 複数フェーズのアニメーション
- **keyframeAnimator** (iOS 17+): キーフレームベースのアニメーション
- **@Animatable** (iOS 26+): アニメーション対応マクロ

### references/layout.md
レイアウト関連コンポーネント：
- **Grid** (iOS 16+): 柔軟なグリッドレイアウト
- **ViewThatFits** (iOS 16+): スペースに応じた自動ビュー選択
- **AnyLayout** (iOS 16+): 動的レイアウト切り替え
- **Gauge** (iOS 16+): 進捗・レベル表示
- **Table** (iOS 16+): 表形式のデータ表示（macOS/iPadOS）
- **ToolbarSpacer** (iOS 26+): ツールバースペース制御
- **labelIconToTitleSpacing** (iOS 26+): Labelスペース調整

### references/tips.md
TipKitフレームワーク：
- **TipKit** (iOS 17+): 機能発見ヒント表示

### references/preview.md
プレビュー関連：
- **#Preview** (iOS 17+): プレビューマクロの簡略化
- **@Previewable** (iOS 18+ / Xcode 16+): プレビュー内で直接@State使用

### references/container.md
コンテナ値・トランザクション：
- **ContainerValues** (iOS 18+): 子→親への値伝達
- **Transaction** (iOS 18+): アニメーション制御

### references/theming.md
テーマ・デザイン：
- **Liquid Glass** (iOS 26+): iOS 7以来最大のUI刷新
- **.liquidGlass()** (iOS 26+): Liquid Glassエフェクト
- **.depthLayer()** (iOS 26+): 深度レイヤー設定

### references/webview.md
WebView関連：
- **WebView** (iOS 26+): SwiftUIネイティブWebView
- **Scene Bridging** (iOS 26+): UIKit/AppKitとSwiftUIシーンの統合

## バージョン対応表（概要）

| コンポーネント | iOS | 備考 |
|--------------|-----|------|
| NavigationStack | 16+ | NavigationViewの後継 |
| Swift Charts | 16+ | 宣言的チャート |
| PhotosPicker | 16+ | 権限不要の写真選択 |
| Grid | 16+ | 柔軟なグリッド |
| TipKit | 17+ | 機能発見ヒント |
| scrollPosition | 17+ | スクロール位置制御 |
| symbolEffect | 17+ | SFシンボルアニメ |
| #Preview | 17+ | 簡易プレビュー |
| ContainerValues | 18+ | 子→親値伝達 |
| @Previewable | 18+ | プレビュー内@State |
| Liquid Glass | 26+ | 新デザイン言語 |
| WebView | 26+ | ネイティブWebView |
| @Animatable | 26+ | アニメーションマクロ |
| Chart3D | 26+ | 3Dチャート |

## 使用方法

### 新しいUIを実装する際
1. 実装したい機能に対応するリファレンスファイルを参照
2. バージョン対応表でプロジェクトのデプロイメントターゲットとの互換性を確認
3. コード例を参考に実装

### 利用可能なコンポーネントを探す際
1. バージョン対応表でデプロイメントターゲット以下のコンポーネントを確認
2. 該当するリファレンスファイルで詳細を確認

## 関連スキル

- **swift-ios-migration**: 移行ガイド（@Observable、Swift 6等）
- **swiftui-coding-guidelines**: コーディングガイドライン
- **swiftui-ssot**: 状態管理の設計
