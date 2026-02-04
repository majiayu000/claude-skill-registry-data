---
name: skills-mcp-playbook
description: Skill/MCPの使い分けと組み合わせ設計を支援するガイド。外部ツール接続はMCP、手順・品質基準はSkillという分離原則、衝突回避、実例（財務バリュエーション/ミーティング準備）を参照し、どちらを使うか判断・設計したいときに使う。
---

# Skills-MCP Playbook

## 使いどころ
- 「Skillで書くか、MCPで実装するか」が曖昧なとき
- 複数MCPを束ねてワークフロー化し、一貫した出力基準を持たせたいとき
- MCPのI/O指示とSkill側のフォーマット指示が衝突しないようガードレールを敷きたいとき

## 判断クイックチャート（高レベル）
- 何かにアクセス/操作する必要がある → MCP（接続とI/O契約）
- どう進めるか、どの順で何を見てどう出力するかを共有したい → Skill（シーケンスと品質基準）
- 両方必要 → MCPで取れるデータ/アクションを洗い出し、Skillで手順と合格基準を記述

## 設計ガイド（要点）
- 分離原則: MCPは接続とフォーマット契約、Skillはワークフロー手順・優先順位・出力様式。
- 衝突回避: 出力フォーマット指示はどちらか一方に寄せる。MCPがJSON返却要求ならSkillでMarkdown表を要求しない。Skillで整形するならMCPは「生データで返す」と明記。
- 複数MCP束ね: Skill内で順序とフォールバックを決める（例: Notion→CRM→Web検索）。失敗時の代替手順も書く。
- 品質基準: Skillに「完了条件」を書く（必須セクション、検証チェック）。
- Progressive Disclosure: この記事の実例や使い分け表は references/ に分離、必要時のみ読む。

## 手順テンプレ（流用可）
1) インテント整理: 目的と成果物の型（例: pre-read, agenda, valuationシート）
2) MCP列挙: 必要な接続と取得/操作内容を箇条書き
3) Skill記述: 取得順序、加工・検証手順、出力フォーマット、例外ハンドリング
4) 衝突チェック: MCP側の返却形式とSkill側の期待形式を揃える
5) 簡易テスト: ダミー入力で一連の流れと出力形を確認

## 参照
- `references/quick-diff-table.md`: SkillとMCPの役割の対比表
- `references/examples/financial-valuation.md`: 財務バリュエーションの組み合わせ例
- `references/examples/meeting-prep.md`: Notionミーティング準備の組み合わせ例
