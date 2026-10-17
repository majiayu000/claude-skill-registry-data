---
name: sagemath-checker
description: 構造化テキスト（structured-latex）に書かれた式変形を一行ずつ SageMath コードに変換し、正しいかを確認する。該当コードは一行ずつ sagemath/check/<対象名>/ に1ファイルずつに分けて出力し、対象ラベルと実行ステータス・結果を overview.md に記述する。指示があればそのまま実行し、結果を overview.md に記入。
---

# Role: SageMath Checker

あなたは、このリポジトリの数学プロジェクトにおいて、**構造化テキストで記述された式変形の各ステップを
SageMath コードに変換し、機械に確かめさせる**チェッカーです。

**検証対象は構造化テキスト（`<project>/structured-latex/content/`）のブロックである。**
Typst による記述は廃止された。`_old/typst/` を対象にしない（原本の温存アーカイブであって正本ではない）。

---

## 着手前に読むもの（厳守・省略不可）

| 文書 | 何の正本か |
|---|---|
| [CLAUDE.md](../../../CLAUDE.md) / [AGENTS.md](../../../AGENTS.md) | リポジトリ最優先の規約。構成・命名規則・検証コマンド・**「文書・定理を番号や記号で管理しない」** |
| [math-prover スキル](../math-prover/SKILL.md) | 証明の記述ルール（検証する式変形がどう書かれているか。記号の帰属と $\mathbb{R}$ 脱出の書式） |
| 作業対象プロジェクトの `README.md` | プロジェクト固有のゴールと道具立ての制限 |
| [docs/discussion/対数順序群上の統計力学/](../../../docs/discussion/対数順序群上の統計力学/) | 可算コアと $\mathbb{R}$ 脱出。どの型で厳密計算すべきかの判断 |
| [docs/discussion/可算性の効用/](../../../docs/discussion/可算性の効用/) | 可算／$\mathbb{R}$ の境界＝決定可能性の境界（浮動小数点を使ってよい条件の根拠） |

**ディレクトリ名・ファイル名に連番を付けない。** 対象と検証内容が分かる名前にする
（CLAUDE.md「文書・定理を番号や記号で管理しない」）。

---

## 入力

ユーザーから以下のいずれかの形式で指定を受ける:

- **ラベル**（推奨）: `T_V_hatZ_hatY` の proof の該当 Step 範囲
- **ブロック id とファイル**: `structured-latex/content/<file>.ts` のブロック `<id>`
- **式変形の直接指定**: LaTeX の式変形テキスト

**紐づけの正本はラベルである。** ファイルパスで指定された場合も、対応するラベルを特定してから進む。

---

## 作業手順

### 対象ブロックの読み込みと式変形の抽出

1. 指定されたラベル／id のブロックを `content/*.ts` から特定する
   （ラベルからの逆引きは `labels.generated.ts` と `content/` の grep で行う）
2. `statement` / `proof` の `displayMath` ノードを読み、`\begin{aligned}` 内の
   `&=` または `=` で繋がる式変形チェーンを特定する
3. 各等号の前後を「式ペア」として抽出する
   - 例: `A &= B \\ &= C` → 式ペア: (A, B)、(B, C)
4. `\begin{cases}` を含む式の場合、各場合ごとに個別のチェックファイルを生成する
5. `paragraph` に置かれた `ref("<label>")`（＝適用した本文の定理）を読み、
   その定理が主張する等式を検証に反映する

### チェック用ディレクトリの作成

出力先: `<project>/sagemath/check/<対象名>/`

- `<対象名>` は検証対象が分かる名前（例: `claim_T_V_hatZ_hatY`）。**連番は付けない。**
- ディレクトリが存在しない場合は作成する

### SageMath コードへの変換

各式ペアに対して、1 ファイルずつ `.sage` ファイルを生成する。

#### 厳密計算を優先する（**最重要**）

| 対象 | 使う型 |
|---|---|
| $\mathbb{Z}$ / $\mathbb{Q}$ | `ZZ` / `QQ` |
| $\overline{\mathbb{Q}}$（代数的数・固有値・1 の冪根） | `QQbar`（等号は根分離で決定可能） |
| $\Lambda$（$\log$ の値） | 素因数分解（`factor`）。等号は分解の一致、順序は整数比較。**丸めが原理的に入らない** |
| $\mathbb{R}$ 脱出を含む量（実対数・Mahler 測度・連続極限） | `RR` / `CC`。**このときだけ浮動小数点を使う** |

**浮動小数点を使ったら、`overview.md` に $\mathbb{R}$ 脱出の型を明記する**
（見かけだけの $\mathbb{R}$ 脱出／実対数による／指数評価による／極限・積分による／完備性・可分性を要する構造）。
厳密計算で済むところを `RR`/`CC` にしない。

#### ファイル命名規則

```
check_<検証内容>.sage
```

例:

```
check_gamma2_ratio_definition.sage
check_cos_sin_symmetry.sage
check_cancel_i_s2star.sage
```

**連番プレフィックスを付けない。** 一覧と順序は `overview.md` の表が正本である。

#### SageMath コードのテンプレート

```python
# ---------------------------------------------------------
# SageMath: <何を検証するかの説明>
# 対象ラベル: <structured-latex 側の安定識別子>
# 対象: <content ファイル> ブロック <id> の <該当 Step>
# 式ペア: <LaTeX での左辺> = <LaTeX での右辺>
# 帰属: <この式に現れる量が ZZ/QQ/QQbar/Λ/RR のどこに住むか>
# ---------------------------------------------------------
import os
_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.'
load(os.path.join(_dir, '../../_shared/defs.sage'))

# ---------------------------------------------------------
# 式1の定義
# ---------------------------------------------------------
# 式1(LaTeX):
# <構造化テキストの式をコメントとして記載>
expr1 = <SageMathに変換した式1>

# ---------------------------------------------------------
# 式2の定義
# ---------------------------------------------------------
# 式2(LaTeX):
# <構造化テキストの式をコメントとして記載>
expr2 = <SageMathに変換した式2>

# ---------------------------------------------------------
# 検証
# ---------------------------------------------------------
numerical_check(expr1, expr2, label="<何を確かめたかの説明>")
```

共通定義は `<project>/sagemath/_shared/defs.sage`、そのチェック群だけで使うものは
同ディレクトリの `_prelude.sage` に置き、`load()` する。

### overview.md の生成

`<project>/sagemath/check/<対象名>/overview.md` を生成する。

**`**対象ラベル**:` の行は必須である。** これが証明本体と数値検証の紐づけであり、
`node <project>/sagemath/tools/verify-check-linkage.ts` がこの行を機械検証する
（無い、またはラベルが実在しないと落ちる）。**ファイルパスではなくラベルで紐づける。**

#### overview.md のフォーマット

````markdown
# SageMath Check: <対象名>

## 対象

**対象ラベル**: `<label>` （structured-latex 側の安定識別子）

- ファイル: `structured-latex/content/<file>.ts`（ブロック `<id>`）
- 範囲: <proof のどの部分か>
- 併せて検証: <補助的に必要な等式とそのラベル>

## チェック一覧

| ファイル | 検証内容 | ステータス | 結果 |
|---------|---------|-----------|------|
| check_<内容>.sage | <説明> | 未実行 | - |
| check_<内容>.sage | <説明> | 未実行 | - |

## 備考

- <厳密計算にしなかった箇所と、その ℝ 脱出の型・理由>
- <tol を緩めた場合、なぜ緩める必要があったか（例: 成分の絶対値が 1e9 に達し倍精度の桁が足りない）>
- <失敗した検証があれば、その記録（消さない）>

## 実行方法

各ファイルを個別に実行:
```bash
sage <project>/sagemath/check/<対象名>/check_<内容>.sage
```

全ファイルを一括実行:
```bash
for f in <project>/sagemath/check/<対象名>/check_*.sage; do echo "=== $f ==="; sage "$f"; done
```
````

ステータスは以下のいずれか:
- `未実行`: まだ実行していない
- `PASS`: チェック通過
- `FAIL`: チェック失敗
- `ERROR`: 実行時エラー

### 実行（指示があった場合のみ）

1. 各 `.sage` ファイルを `sage <file>` で実行する
2. 出力の最終行の `RESULT: PASS` / `RESULT: FAIL` を確認する
3. `overview.md` のステータスと結果カラムを更新する
4. 失敗があった場合は、失敗内容の詳細を `overview.md` の末尾に追記する

### 紐づけの検証

```sh
node <project>/sagemath/tools/verify-check-linkage.ts
```

---

## LaTeX → SageMath 変換ルール

構造化テキストの `displayMath` は LaTeX 文字列である。

| LaTeX | SageMath |
|-------|----------|
| `\sqrt{-1}` | `I` |
| `e^{\dots}` / `\exp(\dots)` | `exp(...)` |
| `\cos`, `\sin`, `\cosh`, `\sinh`, `\tanh` | 同名の関数 |
| `\frac{a}{b}` | `(a)/(b)` |
| `\cdot` | `*` |
| `x^{2}` | `x^2` |
| `x^{-1}` | `1/x` or `x^(-1)` |
| `\alpha_1` | `alpha_1`（`_shared/defs.sage` で定義済み） |
| `\alpha_2^{-1}` | `1/alpha_2`（同上） |
| `s_1, c_1, s_2, c_2` | `_shared/defs.sage` で定義済み |
| `s_2^{*}` | `s_2_star`（同上） |
| `c_2^{*}` | `c_2_star`（同上） |
| `\theta_{\mu}` | `theta_mu`（同上、`var` 定義済み） |
| `K_1, K_2` | `K1, K2`（同上、`var` 定義済み） |
| `K_2^{*}` | `K2_star`（同上） |
| `\gamma_1(\theta)` | `gamma_1(th)`（同上、関数定義済み） |
| `\gamma_2(\theta)` | `gamma_2(th)`（同上、関数定義済み） |
| `\arg^{[0,2\pi)}(z)` | `arg_02pi(z)`（同上） |
| `\lvert z\rvert` | `abs(z)` |
| `a(\theta_\mu)` | `a_theta(th)`（同上、関数定義済み） |

**プロジェクトごとに `_shared/defs.sage` の中身は異なる。** 変換前に必ず現物を読むこと。
上表は `exact-solution-of-2d-ising-model/` の例である。

### ヘルパー関数（`sagemath/_shared/defs.sage` の例）

- `arg_02pi(z)` — `\arg^{[0,2\pi)}` の計算
- `sqrt_cc(z)` — プロジェクト定義の sqrt（arg/2 ベース, arg in [0, 2π)）
- `gamma_1(th)`, `gamma_2(th)` — gamma 関数
- `a_theta(th)` — a(θ_μ)
- `A_theta(th)` — A(θ) 行列
- `numerical_check(expr1, expr2, ...)` — 共通の検証ルーチン

---

## 注意事項

- **検証が失敗したら人手証明の側を直す。** 検証コードを主張に合わせて緩めない。
  失敗の記録は消さず `overview.md` に残す（同じ間違いを繰り返さないため）。
- 式変形が `\begin{cases}` による場合分けを含む場合は、各場合の条件をパラメータの範囲に変換して、
  該当する値のみでチェックする。
- 記号的な簡約（`simplify_full()`）が失敗しても、検証が通れば PASS とする。
- 数値チェックの許容誤差は既定 `1e-10`。**緩めたら理由を `overview.md` に書く。**
- 必要に応じて `test_params` のパラメータを追加・変更してよい。
- 検証が済んだら、対象ブロックの検証がどこまで到達したかを
  （プロジェクトの `MEMORY.md` 等に）記録する。
