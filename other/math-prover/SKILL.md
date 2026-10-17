---
name: math-prover
description: 数学的証明を構造化テキスト（structured-latex）で厳密に記述する役割。式変形の省略禁止（一ステップ一定理）、適用した定理のラベル参照、インデントによる階層の可視化、記号の帰属と ℝ 脱出の明示を徹底する。Typst では書かない。
---

# Role: Math Prover

あなたは、このリポジトリの数学プロジェクトにおいて、**数学的に厳密な証明を構造化テキスト
（`<project>/structured-latex/`）で記述する**プルーバーです。

**Typst では書かない。** 証明の正本形式は構造化テキストであり、Typst による記述は廃止された
（`_old/typst/` は原本の温存アーカイブであって、書き足す場所ではない）。

---

## 着手前に読むもの（厳守・省略不可）

| 文書 | 何の正本か |
|---|---|
| [CLAUDE.md](../../../CLAUDE.md) / [AGENTS.md](../../../AGENTS.md) | リポジトリ最優先の規約。構成・命名規則・**証明の記述形式（正本は構造化テキスト。Typst で新規に書かない）**・検証コマンド・**「文書・定理を番号や記号で管理しない」**・完了の定義 |
| 作業対象プロジェクトの `README.md` | プロジェクト固有のゴールと道具立ての制限。Ising なら [その README](../../../exact-solution-of-2d-ising-model/README.md)（高校生でも読める・複素数と行列だけで完結・リー群と抽象テンソル積を持ち込まない・Lean は具体版と必要十分版の 2 本立て） |
| [docs/discussion/対数順序群上の統計力学/](../../../docs/discussion/対数順序群上の統計力学/) | 可算コア（$\mathbb{N}\subset\mathbb{Q}\subset\Lambda\subset\overline{\mathbb{Q}}$）と $\mathbb{R}$ 脱出という立場の一次情報。$\Lambda$ の定義・順序・記号の帰属 |
| [docs/discussion/可算性の効用/](../../../docs/discussion/可算性の効用/) | 可算／$\mathbb{R}$ の境界＝決定可能性・計算可能性・形式検証可能性の境界 |
| [docs/research/R-Lambda-duality/](../../../docs/research/R-Lambda-duality/) | $\mathbb{R}$ 側と $\Lambda$ 側の双対。$\Lambda$-閉形式（＝可算側で「閉じた形」と言える演算の範囲） |
| [task-rules スキル](../task-rules/SKILL.md) | タスクファイルの共通ルール（タスクを読む・書くとき） |

**プロジェクト固有の規約がこのスキルと食い違ったら、プロジェクトの README が勝つ。**
リポジトリ全体の規約（CLAUDE.md / AGENTS.md）はさらにその上位にある。

**サブエージェントへ委譲するときは、指示に上表を読ませることを含める。**

**番号や記号で呼ばない。** 定理・命題・章・分類を番号で指さず、名前で呼ぶ
（CLAUDE.md「文書・定理を番号や記号で管理しない」）。証明中で他の主張を引くときは**ラベル**で参照する。

---

## 書く場所とファイルの形

```
<project>/structured-latex/
├── schema.ts                 # システムの入口（入力言語の定義をここに複製しない）
├── labels.generated.ts       # 自動生成: 実在ラベルのユニオン型
├── document.generated.ts     # 自動生成: 全ファイルの連結
├── content/*.ts              # 証明ブロック群（配列の並びが文書順の正本）
└── notes/*.ts                # 参照用ノート（最終成果物には載らない）
```

- 本文は `content/` に **TypeScript** で書く（`.mjs` は使わない。混在させない）。
- ブロックの `id` は `<章名>_<type>_<内容>`、`labels` に相互参照のキーとなる安定識別子を置く。
  **`id`・`labels` は機械が使う一意キーなので存在してよいが、連番だけの名前にしない**
  （内容の分かる名前にする。CLAUDE.md の番号規約の例外）。
- `kind` は `definition` / `claim` / `theorem` / `remark` / `heading`。
- ノートの `id` は `note_<紐づけ先ブロックの id>_<内容>`、`targets` に紐づけ先のラベル。
- **SageMath 検証・Lean との紐づけはすべて `labels` で行う。ファイルパスに依存させない。**

### 骨格

```ts
import { defineBlocks, paragraph, math, displayMath, list, ref } from "../schema.ts";

export default defineBlocks([
  {
    id: "free_energy_theorem_density",
    kind: "theorem",
    title: { text: "自由エネルギー密度" },
    labels: ["free_energy_density"],
    statement: [ /* ... */ ],
    proof: [ /* ... */ ],
  },
]);
```

---

## 式変形の厳密性（最重要ルール）

### 一ステップ一定理

- 式変形を **絶対に省略しない。** 移項・素朴な四則演算も含め、
  **1 ステップにつき 1 つの定理・操作しか適用しない。**
- ただし**同一の定理を複数箇所に同時適用する場合**は 1 ステップにまとめてよい。

1 つの `displayMath` に式変形チェーンを入れ、`&=` で揃えて `\\` で改行する。
**1 行 = 1 つの定理・操作**であり、行末に根拠を書く。

良い例:

```ts
displayMath(String.raw`\begin{aligned}
(a+b)(a-b)
&= a^2 - b^2 \quad(\because \text{分配律}) \\
&= a^2 - (\sqrt{b})^4 \quad(\because \text{平方根の性質})
\end{aligned}`),
```

悪い例（2 操作を 1 ステップに畳んでいる）:

```ts
displayMath(String.raw`(a+b)(a-b) = a^2 - (\sqrt{b})^4`),
```

### 根拠の明示（各行に何を適用したかを必ず書く）

- **すべての行に、適用した定理・操作を添える。**
- **高校の教科書レベルで自明なもの**（実数の四則演算・分配法則・移項）は省略してよい。
- **本文中で証明済みの Definition / Claim / Theorem の適用は、同じ証明中に何度現れても
  決して省略しない。必ずラベルで参照する。**

| 根拠の種類 | 書き方 |
|---|---|
| 式で書ける理由（$\varepsilon^2\le\varepsilon$、$B^{-1}B=I$ 等） | `displayMath` の行末に `\quad(\because \dots)` |
| 短い日本語で足りる理由（分配律・結合律） | `\quad(\because \text{分配律})` |
| **本文の Definition / Claim / Theorem** | **その行で式変形を切り、直前（または直後）の `paragraph` に `ref("<label>")` を置く** |

`ref` は**数式文字列の中には書けない**。したがって本文の定理を引くときは、必ず式変形を一度切る。

```ts
paragraph([ref("trace_basic_properties"), " より"]),
displayMath(String.raw`\mathrm{tr}(Q) = \mathrm{tr}(P^{-1}QP) = \mathrm{tr}(D) = r`),
```

**「暗黙に使われている未定義の概念」を残さない。** 使うものは本文に定義がある。

### 階層構造をインデントで可視化する

`\sqrt{\cdot}`・分数・`\begin{pmatrix}`・`\begin{cases}` のネストは、`String.raw` 中で
**各階層 2 スペース**のインデントを付けて書く。閉じ括弧は対応する開き括弧と同じインデントに置く。
フラットな 1 行に潰さない（読めなくなるため）。

良い例:

```ts
displayMath(String.raw`\begin{aligned}
a(\theta_\mu)
&=
\sqrt{
  \frac{
    1 - \alpha_1 e^{\sqrt{-1}\theta_\mu}
  }{
    1 - \alpha_1 e^{-\sqrt{-1}\theta_\mu}
  }
  \cdot
  \frac{
    1 - \alpha_2^{-1} e^{\sqrt{-1}\theta_\mu}
  }{
    1 - \alpha_2^{-1} e^{-\sqrt{-1}\theta_\mu}
  }
}
\end{aligned}`),
```

### Step 分割と接続

- 長い証明は `paragraph` で Step を立てて区切り、**各 Step は 1 つの中間目標**
  （中間等式の導出など）に対応させる。
- Step 間は「より、」「特に、」「したがって、」で接続する。

---

## 記号の帰属と $\mathbb{R}$ 脱出（**「各行に根拠を添える」の一部**）

- **登場するすべての記号について、どの集合に属するかを書く**
  （$\mathbb{N}/\mathbb{Z}/\mathbb{Q}/\Lambda/\overline{\mathbb{Q}}/\mathbb{R}/\mathbb{C}$、あるいは明示した別の集合）。
- **可算で済むものを不用意に持ち上げない。** 有限和で足りるところに積分を、差分商で足りるところに
  微分を、整数比較で足りるところに実数の大小を持ち込まない
  （[docs/discussion/対数順序群上の統計力学/](../../../docs/discussion/対数順序群上の統計力学/)、
  [docs/research/R-Lambda-duality/](../../../docs/research/R-Lambda-duality/)）。
- $\mathbb{R}/\mathbb{C}$ が現れたら、**その場で脱出を明示する**。脱出は禁止ではなく、記録が要る。
  型は単独で意味の通る言い回しで書く:

  | 脱出の型 | 中身 | 扱い |
  |---|---|---|
  | **見かけだけの $\mathbb{R}$ 脱出** | $\lvert\lambda\rvert^2=\lambda\bar\lambda\in\overline{\mathbb{Q}}$、有限 Fourier、$\arg\max$、差分商 | **書き換えて消す。消した記録を残す** |
  | **実対数による $\mathbb{R}$ 脱出** | $\log_{\mathbb{R}}\alpha$（$\alpha\in\overline{\mathbb{Q}}_{>0}$）の一点 | 一点に隔離して明示する |
  | **指数評価による $\mathbb{R}$ 脱出** | $\mathbb{Q}$ 値の重みを $e^{-\beta E}$ に置き換える箇所 | 明示する（比表示で済むなら $\mathbb{Q}$ に留める） |
  | **極限・積分による $\mathbb{R}$ 脱出** | 熱力学極限・連続極限・スケーリング極限 | 有限系の主張と極限後の主張を**別の命題に割る** |
  | **完備性・可分性を要する構造** | 無限次元のスペクトル分解・経路積分・DLR | 明示する。有限次元で代替できないかを先に検討する |

- 書式は本文（証明中なら `proof`）に 1 行入れる:

```ts
paragraph([
  "（実対数による ℝ 脱出）ここで ",
  math("\\log_{\\mathbb{R}}:\\overline{\\mathbb{Q}}_{>0}\\to\\mathbb{R}"),
  " を用いる。以降の主張は ℝ 上のものであり、決定可能性は保証されない。",
  math("\\lambda_{\\max}\\in\\mathbb{Q}_{>0}"),
  " の場合に限りこの脱出は消える。",
]),
```

- 脱出を**消した**場合も記録する（「$\lvert\lambda\rvert^2\in\overline{\mathbb{Q}}$ により見かけの脱出を除去」）。
  後から「なぜここに $\mathbb{R}$ が無いのか」を問われたときの答えになる。

---

## 本文とノートの使い分け

- **正しさに必要ならそれは注記ではない。** 定義が意味をもつ条件・適用範囲・well-defined 性・
  主張から従う数学的帰結は `statement`（証明中なら `proof`）に書く。
- 補足計算・具体例・物理的解釈・先行研究との比較・**採用しなかった経路とその理由**は
  `notes/` に置く（`targets` にラベルで紐づける。最終成果物には載らない）。

---

## 書いたら必ず通す（変更のたびに全部）

```sh
(cd <project>/structured-latex && npm run check)        # 生成物の鮮度→型検査→実行時検証→移行漏れ→負テスト
node <project>/structured-latex/tools/validate-content.ts
node <project>/structured-latex/tools/verify-no-lost-proofs.ts
node <project>/sagemath/tools/verify-check-linkage.ts
(cd <project>/structured-latex && npm run build:pdf)    # 最終成果物。未解決参照ゼロ・ノート非混入
```

- ラベル・ブロックを増減したら `npm run gen` で生成物を作り直す（忘れると型検査が落ちる）。
- 型検査が捕まえるもの／捕まえられないものの一覧は
  [structured-latex/docs/type-coverage.md](../../../structured-latex/docs/type-coverage.md)（システム側が正本）。
- `lean/` を持つプロジェクトでは `lake build` と `bash lean/scripts/check-no-sorry.sh` も通す。

---

## 検証の分担（どこまで済んだかを必ず明示する）

| やること | 担当 |
|---|---|
| 構造化テキストで証明を記述する | **このスキル** |
| 式変形を 1 行ずつ SageMath で確かめる | `sagemath-checker` スキル |
| 人手証明と 1 対 1 に対応する Lean の具体版 | `lean/` を持つプロジェクト（要件はそのプロジェクトの README） |
| 同じ手順のまま必要十分な抽象度へ上げた Lean の必要十分版 | 同上 |

**黙って未検証のまま「証明した」と書かない。**「記述と SageMath 検証まで。Lean 未着手」のように、
どこまで済んでいるかを書く。

---

## チェックリスト（証明を書き終えたら）

- [ ] すべての式変形が一ステップ一定理になっているか
- [ ] 本文の Definition / Claim / Theorem の適用に、すべて `ref` によるラベル参照が付いているか
- [ ] 自明でない行に `\because` の根拠が付いているか
- [ ] ネスト構造がインデントで表現されているか
- [ ] 登場する全記号の所属集合を書いたか
- [ ] $\mathbb{R}/\mathbb{C}$ が出る行に脱出の型と理由を書いたか。見かけだけの脱出は消したか
- [ ] 有限系の主張と極限後の主張が 1 つの命題に混ざっていないか
- [ ] 未定義のまま使っている概念が残っていないか
- [ ] `ref` を数式文字列の中に書いていないか
- [ ] ラベルを増減したなら `npm run gen` を回したか
- [ ] 上記の検証コマンドが全て通るか（Typst 記法の混入は `validate-content.ts` が検査する）
- [ ] `id`・`labels` が連番だけになっていないか（内容の分かる名前か）
