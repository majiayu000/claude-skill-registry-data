---
name: dzero-tech-selection
description: UI・機能・コンポーネントの実装レイヤー（HTML/CSS/JavaScript）を決定する判断基準。実装・修正の着手前に必ず読む。アコーディオン、モーダル、ポップオーバー、開閉・切替などのインタラクション実装を依頼されたときに使う。
license: CC-BY-NC-SA-4.0
---

# 実装レイヤー選定

**UI や機能の実装に着手する前に、どのレイヤー（HTML / CSS / JavaScript）で実装するかを必ず決定する。** インタラクションは基本的に宣言的に記述し、JavaScript での実装は最小限に抑える（[HTML: インタラクション](https://guidelines.d-zero.co.jp/html/interactions.html)）。

## カスケード判断

上から順に検討し、上位レイヤーで実現できるなら下位レイヤーを使わない。

1. **HTML で実現できるか**
   - ネイティブ要素・属性で実現できるものは HTML で実装する
   - インタラクティブな呼び出しは原則 `button` 要素 + `command` 属性。規定アクション（`toggle-popover` / `show-popover` / `hide-popover` / `show-modal` / `close`）はそのまま活用する
2. **CSS で実現できるか**
   - スタイルは CSS、ロジックは JavaScript に分離する。状態変化によるスタイルは CSS 側で管理する
   - JavaScript から `style` 属性を直接書き換える実装は避ける（詳細は `dzero-js`）
3. **JavaScript が必要な場合**
   - 規定アクション中の処理・カスタムコマンドの実装、上記で実現できないロジックのみ JavaScript で行う
   - 頻発イベント（`scroll` / `resize` 等）はイベントではなく代替 API（IntersectionObserver / ResizeObserver / `matchMedia`）を利用する

## 代表パターン対応表

| 実装したいもの                                | 選定                                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------------ |
| アコーディオン・開閉                          | `details` / `summary`                                                                |
| モーダルダイアログ                            | `dialog` + `button command="show-modal"`                                             |
| ポップオーバー・ツールチップ類                | `popover` 属性 + `button command="toggle-popover"`                                   |
| 要素の状態（無効・展開など）                  | ネイティブ属性 → ARIA 属性 → `data-*` 属性 の優先順位（詳細は `dzero-html`）         |
| ビューポート進入の検知                        | IntersectionObserver（`scroll` イベント監視は不可）                                  |
| 要素サイズ変更の検知                          | ResizeObserver（`resize` イベント・`setTimeout` 監視は不可）                         |
| ウィンドウ幅・メディアクエリ状態              | `window.matchMedia`（`resize` イベント監視は不可）                                   |
| レスポンシブの画像出し分け                    | `picture` 要素（`sp-only` / `pc-only` クラスの `img` 二重配置は不可）                |
| HTML 標準に存在しないコンポーネント（タブ等） | WAI-ARIA + [APG](https://www.w3.org/WAI/ARIA/apg/) 準拠で実装（詳細は `dzero-a11y`） |

WAI-ARIA を使うのは「HTML 標準では再現できないコンポーネントを作成するときのみ」（[HTML: アクセシビリティ](https://guidelines.d-zero.co.jp/html/accessibility.html)）。

## 選定後

決定したレイヤーの軸スキル（`dzero-html` / `dzero-css` / `dzero-js`）を読んでから実装する。デザインデータ（Figma 等）を参照する実装の場合は `dzero-design-to-code` も読む。

実装後は必ずブラウザで表示・動作・インタラクションを確認する（コードを読むだけで完了としない。確認手段はプロジェクトの環境の指示に従う）。
