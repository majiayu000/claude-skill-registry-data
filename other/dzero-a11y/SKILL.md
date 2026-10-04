---
name: dzero-a11y
description: D-ZERO のアクセシビリティ規約。マークアップやインタラクションの実装・変更・レビューで、WAI-ARIA、代替テキスト（alt）、ランドマーク、見出し、キーボード操作、フォーカスを扱うときに使う。
paths: ['**/*.html', '**/*.pug']
license: CC-BY-NC-SA-4.0
---

# アクセシビリティ規約

> マークアップの規範は `dzero-html` と併せて適用する。詳細は [HTML: アクセシビリティ](https://guidelines.d-zero.co.jp/html/accessibility.html) を参照。

## 実装規範

### 準拠基準

- 準拠基準は WCAG 2.2。WAI-ARIA は 1.2 を基本に、ブラウザ・支援技術の実装状況を鑑みて判断する

### WAI-ARIA の使いどころ

- **WAI-ARIA を使うのは HTML 標準では再現できないコンポーネントを作成するときのみ**。HTML 標準に要素がある場合や Popover などで済む場合は使わない
- 使う必要があるケース: `button` が `aria-pressed` / `aria-expanded` などの状態を持つ場合、タブやカルーセルなど HTML にないコンポーネントを扱う場合
- 使う場合は [APG](https://www.w3.org/WAI/ARIA/apg/) を参考に、インタラクション要件・キーボード操作・振る舞いを推奨実装に近づける（特別な理由がない限り APG に則る）。実装例は [APG Patterns Examples](https://masup9.github.io/apg-patterns-examples/) も参考にする
- 状態を表す属性の使い分けは `dzero-html` の状態管理に従う

### 代替テキスト

- `alt` は WCAG 達成基準 1.1.1「同等の目的」を基準に考える。コーディング段階ではなくデザイン段階で代替テキストが決まるように計画する（決まっていなければユーザーに確認する）
- **装飾ではない通常の `img` に `aria-hidden="true"` を付けない**。装飾画像は `alt=""`（空 alt）が正解
- `alt` が空の場合に `role="none"`（`role="presentation"`）を重ねて付けない（空 alt で同じ効果が得られる）

### ランドマーク

- 各コンポーネントの先祖となる要素にランドマークを設ける。もしくはコンポーネントルート自体をランドマークを持つ要素でマークアップする

### キーボード操作とフォーカス

- キーボード操作の要件は [APG](https://www.w3.org/WAI/ARIA/apg/) の該当パターンに則る（実装例の参考: [APG Patterns Examples](https://masup9.github.io/apg-patterns-examples/)）
- インタラクティブ要素には `:focus-visible` によるフォーカス表示を実装する。デザインカンプに描かれていなくても省略しない（`dzero-design-to-code` 参照）。フォーカス表示を消すだけのスタイル（`outline: none` 等）を書かない
