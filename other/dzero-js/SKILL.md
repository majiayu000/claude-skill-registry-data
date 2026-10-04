---
name: dzero-js
description: D-ZERO の JavaScript/TypeScript コーディング規約。JS/TS を書く・編集する・レビューするときに使う。イベント処理、DOM 操作、状態変更、ライブラリ追加、スクリプト読み込みに適用する。
paths: ['**/*.js', '**/*.ts']
license: CC-BY-NC-SA-4.0
---

# JavaScript コーディング規約

> 実装レイヤー選定（`dzero-tech-selection`）を経ていない場合は先にそちらを読むこと。**HTML だけで実現できるものは JavaScript で実装しない。** 詳細は [JavaScript ガイドライン](https://guidelines.d-zero.co.jp/js/) を参照。

## 実装規範

### モジュール設計

- 目的や機能ごとにファイルを分割する
- 実行タイミングをコントロールできるよう、ひとつの関数にまとめて export する（定数の export は可）
- `import` した時点でブラウザや DOM に影響する処理が走る実装（import 副作用）を避ける。import 後に任意に実行できる状態にする
- `type="module"` 環境のためファイル参照に拡張子は必須。TypeScript ファイルの参照は `.ts` を `.js` に変えて書く。`__assets/_libs` はエイリアス `@` で参照する

### DOM・スタイル操作

- `style` 属性のプロパティを直接書き換えない。状態の変更は、その状態を表す `data-*` 属性の変更で行い、スタイルは CSS 側で管理する（JS はロジックと管理に徹する）
- 動的な値を反映する場合はカスタムプロパティを使う（`el.style.setProperty('--block-size', ...)`）
- インタラクションの呼び出しは `command` 属性を基本とし、規定にないアクションやフックは `command` イベント（`e.command` / `e.source`）で実装する。`[commandfor]` の要素に直接イベントリスナを張るような、意図と振る舞いの関連が不明確な実装は避ける

### パフォーマンス

- 頻発するイベント・タイマー（`scroll` / `resize` / `mousemove` / `touchmove` / `wheel` / `setTimeout` / `setInterval`）での監視は避け、代替 API を使う:
  - ビューポート進入の検知 → IntersectionObserver
  - 要素サイズ変更の検知 → ResizeObserver
  - ウィンドウ幅・メディアクエリ状態 → `window.matchMedia`
- イベントリスナには Passive Event Listener（`{ passive: true }`）を利用する
- 同一フレーム内で複数回走りうる処理は `requestAnimationFrame`（+ `cancelAnimationFrame`）で間引く
- 同じ戻り値を期待できる処理（セレクタクエリ等）は変数化して繰り返さない

### ライブラリ

- 許可リスト: core-js、@oddbird/popover-polyfill、invokers-polyfill、what-input、jQuery、Splide。**リスト外のライブラリは必ず相談する**
- 信頼性（継続的な保守運用が可能か）を十分に検証する
- yarn で NPM からインストールして `import` で利用するのが基本。`package.json` と `yarn.lock` の変更はコミットする
- CDN から直接参照しない。外部ファイルとして読み込む必要がある場合はダウンロードして同じサーバーにセルフホストする

### 読み込み

- `script` 要素には `type="module"` が必要。基本は `import` を利用し、`script` 要素での直接読み込みは例外（依存順に注意）
- インライン JavaScript が許されるのは、タグマネージャー・トラッキング・SNS 埋め込み・そのページ限定と保証されたコードのみ。書く場合は `<script type="module">`（タグマネージャー等は加工せずそのまま貼る）

### lint

- リントエラー（ESLint / Prettier）は例外なく必ず修正する。`eslint-disable` で逃げず、ルールが現状にそぐわない場合は Config ファイルの変更を提案する
