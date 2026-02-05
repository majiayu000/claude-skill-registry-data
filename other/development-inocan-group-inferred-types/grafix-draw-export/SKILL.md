---
name: grafix-draw-export
description: Grafix の `draw(t)` スケッチを生成・改良し、`python -m grafix export` で PNG を複数枚 headless 出力して比較するための手順。ユーザーが「Grafix の draw を作って」「PNG を書き出して」「候補を複数出して比較したい」「headless で export したい」などと言ったときに使う。
---

# Grafix Draw Export

## 目的

- `draw(t)` を作る/直す
- `python -m grafix export` で PNG を複数枚出す
- 人間の選別 → 改良のループを回す

## 前提

- PNG は内部的に SVG を生成して `resvg` でラスタライズする（`resvg` が必要）。
- このリポジトリから実行する場合は `PYTHONPATH=src` を付ける（pip インストール済みなら不要）。
- 作品制作にあたり、md ファイルでユーザーへの事前確認は不要。

## 最短の進め方（デフォルト運用）

- ユーザーは **モチーフ/雰囲気**だけ入力する（毎回ここだけは聞く）。
- それ以外（canvas/t/run-id 等）が未指定なら、まずは以下のデフォルトで候補を出す。
  - `canvas`: `800 800`
  - `t`: `0 0.25 0.5 0.75 1.0`
  - `run-id`: `v1`（改良のたびに `v2`, `v3`…）
- `resvg` は質問しない。まず export を試し、失敗したらエラーメッセージに応じて案内する。

## ワークフロー

### 1) 入力をもらう（最小）

- **必須**: どんな絵にしたい？（モチーフ/雰囲気、線の密度、対称/非対称、ノイズ有無など一言で OK）
- **任意**: 既存の `draw(t)` を export する？（するなら `--callable` 相当を指定してもらう: `sketch.generated.foo:draw`）

以降は、ユーザーの指定が無ければデフォルト値で進めて候補 PNG を出す。

### 2) `draw(t)` を作成/更新する

- 基本は `sketch/generated/<slug>.py` に作る。
- `draw` はモジュールトップレベル関数にする（import しやすくする）。

最小スケルトン:

```py
from grafix import E, G

def draw(t: float):
    ...
```

### 2.1) G（primitives）と E（effects）の使い方（組み込み）

- `G.<name>(...)` は **プリミティブの Geometry ノード**を作る（線/多角形/テキスト等）。
- `E.<name>(...)` は **effect のビルダ**を作る。`E.a().b().c()(g)` のようにチェーンして最後に `(g)` で適用する。

例:

```py
from grafix import E, G

def draw(t: float):
    g = G.polygon(n_sides=6, center=(400, 400, 0), scale=300)
    e = E.fill().displace()
    return e(g)
```

メモ:

- effect によっては複数入力を取るものがある。multi-input effect はチェーンの先頭にしか置けない。

### 2.2) ユーザー定義 primitive / effect の使い方

ユーザー定義は **デコレータで登録**する。登録は import 時に行われるため、`draw` と同じモジュールに書けば `python -m grafix export` で import された時点で有効になる。

primitive（`G.<name>(...)` で呼べる）:

```py
from grafix.api import primitive

@primitive
def my_prim(*, size: float = 1.0):
    ...
```

effect（`E.<name>(...)` で呼べる）:

```py
from grafix.api import effect

@effect
def my_eff(inputs, *, amount: float = 1.0):
    ...
```

Notes:

- 組み込み primitive/effect は `meta=...` 必須だが、ユーザー定義は `meta` 省略でよい（GUI に出したいなら `meta` を付ける）。
- `meta` を付ける場合、対象引数は **default 必須**で `None` は使えない。

### 3) PNG を export する（候補出し）

この repo から実行する例（`--out/--out-dir` を省略すると、config の `paths.output_dir`（既定 `data/output`）配下に、スケッチの相対パスをミラーして保存される）:

単発（デフォルト出力: `data/output/png/...`）:

```bash
PYTHONPATH=src python -m grafix export \
  --callable sketch.generated.foo:draw \
  --t 0 \
  --canvas 800 800 \
  --run-id v1
```

複数枚（連番で保存。比較 → 選別用。デフォルト出力）:

```bash
PYTHONPATH=src python -m grafix export \
  --callable sketch.generated.foo:draw \
  --t 0 0.25 0.5 0.75 1.0 \
  --canvas 800 800 \
  --run-id v1
```

保存先を明示的に変えたい場合だけ（単発）:

```bash
PYTHONPATH=src python -m grafix export \
  --callable sketch.generated.foo:draw \
  --t 0 \
  --canvas 800 800 \
  --out /tmp/foo.png
```

保存先を明示的に変えたい場合だけ（複数枚 / ディレクトリ指定）:

```bash
PYTHONPATH=src python -m grafix export \
  --callable sketch.generated.foo:draw \
  --t 0 0.25 0.5 \
  --canvas 800 800 \
  --out-dir /tmp/foo_v1
```

Notes:

- `--t` 複数指定時は `_f001` のように連番を付けて保存する。
- PNG と同名の `.svg` も生成される（PNG 生成の中間生成物）。

設定ファイル（`config.yaml`）を明示指定して PNG スケール等を変えたい場合:

```bash
PYTHONPATH=src python -m grafix export \
  --callable sketch.generated.foo:draw \
  --t 0 \
  --canvas 800 800 \
  --config ./.grafix/config.yaml
```

### 4) 選別 → 改良のループ

- ユーザーに「良かった画像」を決めてもらう（ファイル名 or `t` or インデックス）。
- 改良のたびに `--run-id` を進める（例: `v2`, `v3`）か、`--out-dir` を変えて上書き衝突を避ける。
- 画像を見ながら具体的な改善案が必要なら、ユーザーに PNG を添付してもらうか、残す画像のパスを指定してもらう。

## 組み込み（G/E）の一覧を調べる

最短:

- `$grafix-api-catalog` を併用し、`skills/grafix-api-catalog/references/api.md` を検索する。

CLI（一覧表示）:

```bash
PYTHONPATH=src python -m grafix list
PYTHONPATH=src python -m grafix list primitives
PYTHONPATH=src python -m grafix list effects
```

実装の場所（読む場所）:

- primitives 実体: `src/grafix/core/primitives/`
- effects 実体: `src/grafix/core/effects/`
- 公開ファサード（登録 import をしている）:
  - `src/grafix/api/primitives.py`
  - `src/grafix/api/effects.py`

## トラブルシュート

- `resvg` が無い: `resvg` をインストールして PATH を通す。
- `--callable` が import できない:
  - repo ルートで実行しているか確認する
  - `PYTHONPATH=src` が付いているか確認する
  - `module:attr` が正しいか確認する

