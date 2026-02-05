---
name: grafix-api-catalog
description: Grafix の組み込み primitive/effect を「薄いカード」形式で参照するためのカタログ。作品制作中に「何がある？」「この表現に合う op は？」を素早く探索する用途。`references/api.md` は `scripts/build_catalog.py` の自動生成を正とする。
---

# Grafix API Catalog

## 目的

- primitive / effect の「一覧・要点・主要パラメータ」を **検索しやすい形**で持つ
- 作品制作中に「使える op を思い出す」「似た op を比較する」を速くする

## 前提

- `references/api.md` は **自動生成**（手編集しない）。
- このリポジトリから実行する場合は `PYTHONPATH=src` を付ける（pip インストール済みなら不要）。

## 使い方（エージェント向け）

- ユーザーが「使える primitive/effect を見たい」「○○っぽい effect を探したい」と言ったら、まず `references/api.md` を検索して候補を 3 つ以内に絞る。
- その後は `$grafix-compose` / `$grafix-draw-export` と組み合わせて実装・出力まで進める。

## カタログの再生成（開発者向け）

```bash
PYTHONPATH=src python skills/grafix-api-catalog/scripts/build_catalog.py
```

出力:

- `skills/grafix-api-catalog/references/api.md`

