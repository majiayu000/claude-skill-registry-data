---
name: repo-knowledge-lookup
description: |
  knowledgeca がプロジェクト内一次情報と外部公式ドキュメントに当たって回答する手順。
---

# 目的
「推測」ではなく「根拠」に基づく回答を短く返し、作業の手戻りを減らす。

# プロジェクト内の当たり方（順序）
1. `docs/<work_item>/implementedplan.md` / `tasks.md` / `review.md` / `notes.md`
2. README / docs/index / docs/architecture / ADR（存在する場合）
3. 該当コード（呼び出し元→定義の順で追う）

# 外部の当たり方（MCPが利用可能な場合）
- Microsoft系: Microsoft Learn MCP を優先
- ライブラリAPI: Context7
- 公開リポ構造: DeepWiki

# 回答フォーマット（必須）
1. 結論（1行）
2. 根拠（プロジェクト内ファイル/外部公式）
3. 注意点（不確実なら不確実）
4. oca判断が必要か（Yes/No）
