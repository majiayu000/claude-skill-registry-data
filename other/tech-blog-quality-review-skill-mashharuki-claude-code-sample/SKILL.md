---
name: tech-blog-quality-review-skill
description: Review and upgrade existing technical blog drafts to publish-ready quality for Zenn, Qiita, company tech blogs, and personal dev blogs. Use when asked to critique an article, improve readability/completion rate, refine structure and titles, tighten technical accuracy, or produce a concrete rewrite plan and revised draft.
---

# Tech Blog Quality Review Skill

技術ブログの「下書き→公開品質」への引き上げに特化したレビュー手順。

## Core Workflow

1. レビュー対象を確認する。
- 入力: 記事本文、想定読者、公開媒体（Zenn/Qiita/企業ブログなど）、目的（採用/ナレッジ共有/検索流入）。
- 不足がある場合は、合理的な仮定を置いて先にレビューを進める。

2. まず診断サマリーを作る。
- `references/review-rubric.md` の6軸で 1-5 点評価。
- 重大な欠陥（誤情報、再現不能、結論不明、対象読者不一致）を最優先で特定する。

3. 改善方針を設計する。
- `references/improvement-playbook.md` から該当パターンを選び、改善順序を決める。
- 原則は「構成→論理→技術検証→可読性→SEO/タイトル→仕上げ」。

4. 実際の改稿案を提示する。
- 抽象論ではなく、見出し再設計・導入文・結論・コード説明・削除候補まで具体化する。
- 可能なら「Before/After の差分」形式で示す。

5. 最終出力をテンプレート化して返す。
- `references/output-templates.md` のフォーマットで、再利用可能なレビュー結果を出す。

## Review Policy

- 文章テクニックより先に、技術的正確性と再現性を担保する。
- 「読者が次に何を実行できるか」を常に判定基準にする。
- 冗長さを削るが、背景や制約の説明が欠けて誤解を生む削り方はしない。
- 主張には根拠（公式ドキュメント、一次情報、検証結果）を付ける。
- 媒体文化に合わせる。
  - Zenn: 学習価値と読みやすさ重視。
  - Qiita: 実装知見・再現手順・ハマりどころ重視。
  - 企業Tech Blog: 信頼性、運用実例、組織文脈の明確化を重視。

## Resource Map

- 評価基準: `references/review-rubric.md`
- 改善方針: `references/improvement-playbook.md`
- 出力形式: `references/output-templates.md`
- 参考サイトの要点: `references/source-notes.md`

必要なファイルのみ読み込む。通常は `review-rubric.md` と `output-templates.md` を先に使い、詳細改善時のみ `improvement-playbook.md` を読む。
