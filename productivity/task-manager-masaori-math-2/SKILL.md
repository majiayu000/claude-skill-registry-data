---
name: task-manager
description: 指定されたtaskの完了状況を調査し、現在実行可能なタスクを特定、エージェントのアサインメントを行う。
---

# タスクマネージャー

## 着手前に読むもの（厳守・省略不可）

| 文書 | 何の正本か |
|---|---|
| [CLAUDE.md](../../../CLAUDE.md) / [AGENTS.md](../../../AGENTS.md) | リポジトリ最優先の規約。検証コマンドと**完了の定義**（`origin/main` への包含を fetch と ancestry で確認するまで完了ではない）・**「文書・定理を番号や記号で管理しない」** |
| [task-rules スキル](../task-rules/SKILL.md) | タスクファイルの共通フォーマット |
| [math-prover スキル](../math-prover/SKILL.md) | 証明の記述ルール（完了判定の基準） |
| 作業対象プロジェクトの `README.md` と `MEMORY.md` | プロジェクト固有のゴールと引き継ぎ状況 |

**アサインするエージェントへの指示には、CLAUDE.md と対象プロジェクトの README を
読ませることを必ず含める。**

**タスクは名前で呼ぶ。** 番号で指さない（CLAUDE.md「文書・定理を番号や記号で管理しない」）。

---

## 完了状態の調査

- `<project>/docs/tasks/<scope-name>/task-dependency-graph.md` を読み、タスク一覧と依存関係を把握する
  （**実行順序はこのファイルが正本**。ファイル名の並びではない）
- 各タスクの完了状態を以下の方法で判断する:
  - 対象ブロック（**ラベル**で特定する）の証明が構造化テキスト側で完成しているか
    （`proof` が存在し、TODO ノードが残っていないか）
  - 次の検証が通るか

    ```sh
    (cd <project>/structured-latex && npm run check)
    node <project>/structured-latex/tools/validate-content.ts
    node <project>/structured-latex/tools/verify-no-lost-proofs.ts
    node <project>/sagemath/tools/verify-check-linkage.ts
    ```

  - **検証がどこまで済んでいるか**を確認する（記述のみ／`sagemath/check/` に数値検証があるか／
    `lean/` に具体版・必要十分版があるか）。記述だけ済んだものを「完了」と呼ばない
  - PR がマージされているか（GitHub MCP ツールで確認）
  - 見つからない場合は、過去のコミットを辿る
- **ブロック数や参照解決だけを見て「完了」と判断しない。** 証明の中身が原本から運ばれているかを
  突き合わせる（`verify-no-lost-proofs.ts` が機械検証する）

## エージェントのアサインメント

- 現在並列で実行可能なタスク全てに対して、エージェントを起動するために以下のコマンドを出力する:

```
claude --worktree <scope-name>_<task-name> --model claude-opus-4-6 "CLAUDE.md と対象プロジェクトの README を読んだうえで、docs/tasks/<scope-name>/proof/<task-name>.md のタスクを実行してください。証明は構造化テキスト（structured-latex）で書くこと（Typst では書かない）。完了したら PR を作成してください。"
```

- 必ず上記のフォーマットで `--worktree` 名を指定すること（例: `fermion-bilinear_a-theta-gamma`）
- 何も指定がなければ `--model claude-opus-4-6` を指定すること
- 依存関係が満たされていないタスクはアサインしない

## 完了報告

- 成果が `origin/main` の祖先に含まれることを `git fetch origin` と
  `git merge-base --is-ancestor` で確認するまで、完了報告を出さない（[CLAUDE.md](../../../CLAUDE.md)）
- push 前に該当プロジェクトの `MEMORY.md` を更新する
