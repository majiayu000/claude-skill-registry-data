---
name: ghostty-translate-docs
description: ghosttyドキュメントの日本語訳を作成
---

# 環境変数

このスキルの呼び出し時に提供される `Base directory for this skill:` の値を `SKILL_DIR` として使用する。
すべてのスクリプトと指示書は `${SKILL_DIR}/...` で参照すること。

# 指示内容

`${SKILL_DIR}/instructions/orchestrator.md` を読んで、その手順に従って処理を実行する。

docs_dir の指定があればそれを使用し、なければデフォルト（prepare-translation.sh のデフォルト）を使用する。

# 結果

- 成功/失敗件数とカテゴリ別内訳の要約
- ユーザーが詳細を求めたら生成されたファイルを読んで説明

# スキルディレクトリ内のファイルを編集する際の必須事項

**`${SKILL_DIR}/` 配下のファイルを編集・追加・削除する場合は、必ず `${SKILL_DIR}/DESIGN.md` を読むこと。**

- 設計思想、ディレクトリ構成、処理フロー、コミット前チェックリストが記載されている
- スキルを単に実行するだけなら読む必要はない
