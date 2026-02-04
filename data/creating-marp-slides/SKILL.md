---
name: creating-marp-slides
description: このプロジェクトでの Marp スライド作成ルール。スライド作成、画像配置、ビルド、プレビュー時に使用。画像は slides/images/ に配置、bun run preview/build を使用。
---

# Marp スライド作成スキル

本プロジェクトにおける Marp スライド作成の固有ルールと設定。

## 画像配置（重要）

スライドで使用する画像は **必ず `slides/images/` に配置**。

```markdown
![](./images/diagram.png)
![bg right:40%](./images/photo.jpg)
```

**理由**: Marp CLI サーバーモードはルート以下のみ配信。他の場所では CLI プレビューで表示されない。
参考: [GitHub Issue #163](https://github.com/marp-team/marp-cli/issues/163)

## ファイル配置

| 種類 | パス |
|------|------|
| スライド | `slides/*.md` |
| 画像 | `slides/images/` |
| カスタムテーマ | `themes/*.css` |
| 出力 | `dist/` |

## 開発コマンド

```bash
# プレビュー（ルートから実行）
bun run preview
# → http://localhost:8080/slides/[ファイル名].md

# ビルド
bun run build        # HTML + PDF
bun run build:html   # HTML のみ
bun run build:pdf    # PDF のみ
bun run build:pptx   # PPTX のみ
```

## 設定（.marprc.yml）

```yaml
allowLocalFiles: true  # ローカル画像読み込み許可
themeSet: ./themes     # カスタムテーマディレクトリ
html: true             # HTML タグ許可
```

その他のオプション（`inputDir`, `output` 等）については [Marp CLI 公式ドキュメント](https://github.com/marp-team/marp-cli#configuration-file) を参照。

## Front Matter 必須設定

```yaml
---
marp: true
theme: default  # または gaia, uncover
paginate: true  # 推奨
---
```

## テーマ選択

- `default`: ビジネス向け、シンプル
- `gaia`: カラフル、視覚的
- `uncover`: ミニマル、テキスト中心

**注意**: `invert` クラスは `default` テーマで最も安定。`gaia` では期待通りに動作しない場合あり。

## 詳細リファレンス

- [トラブルシューティング](./references/troubleshooting.md)
- [コンテンツ最適化](./references/content-optimization.md)
