---
name: repo-about
description: README（英語版優先）から GitHub リポの About (description) と topics を生成し、gh repo edit で設定する。
---

# repo-about

README.en.md（なければ README.md）を読み、GitHub の About（description）と topics を生成して適用する。

**公開パイプラインの固定順**: `repo-standardize → guarantee-audit → repo-readme → readme-i18n → repo-publish → repo-about`。本 Skill は**第6**（README 完成・公開後の仕上げ）。この順は都度再判断しない。

## 手順

1. **README の確認**
   - `README.en.md` があれば優先して読み、なければ `README.md` を読む。

2. **内容の生成**
   - **Description**: リポが何をするものかを1文で言う英文（100〜120文字程度）を生成する。
   - **Topics**: 技術スタック、用途、主要機能からキーワードを 5〜10 個抽出する。

3. **確認と適用**
   - 提案する description と topics をユーザーに提示して確認を得る。
   - 確認後、既存の topics を一度すべて削除（クリーンリセット）してから、`gh repo edit` を用いて設定を適用する。
     - 削除は `gh repo view --json repositoryTopics` で既存の topic を取得し、各 topic を `--remove-topic` で除去する。
