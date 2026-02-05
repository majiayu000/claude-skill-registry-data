---
name: enhancing-progressively
description: >
  CSS-first approach - use CSS before JavaScript. Triggers: レイアウト, スタイル,
  位置, アニメーション, 表示/非表示, トグル, レスポンシブ, CSS Grid, Flexbox,
  transforms, transitions, CSSのみ, JavaScript不要, シンプル
allowed-tools: [Read, Grep, Glob]
user-invocable: false
---

# プログレッシブエンハンスメント

## 優先順位

| 優先度 | アプローチ | 例                                 |
| ------ | ---------- | ---------------------------------- |
| 1      | HTML       | セマンティック要素、ネイティブ入力 |
| 2      | CSS        | Grid, Flexbox, :has(), transitions |
| 3      | JS         | 本当に必要な場合のみ               |

## 検出

| JSパターン                   | CSS代替                            |
| ---------------------------- | ---------------------------------- |
| `element.style.display`      | CSS `:has()`, `[open]`, `<dialog>` |
| `addEventListener('resize')` | CSS `@media`, `clamp()`, `min()`   |
| `getBoundingClientRect`      | CSS Grid, Flexbox, `gap`           |
| `setInterval` アニメーション | CSS `transition`, `@keyframes`     |
| `classList.toggle`           | CSS `:checked`, `:target`          |
| `scrollTo`, `scrollIntoView` | CSS `scroll-behavior: smooth`      |
| `matchMedia`                 | CSS `@media`, `@container`         |
