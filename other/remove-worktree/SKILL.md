---
name: remove-worktree
description: |-
  現在のセッションが使用しているworktree環境（worktreeディレクトリ＋devcontainer＋関連リソース）を自動特定して破棄するスキル。INSTANCE_IDの判定、未コミット変更の確認、`./scripts/remove-worktree.sh`の実行までを安全に行う。「worktree破棄」「worktree削除」「worktreeを片付けて」「remove worktree」「devcontainerを停止」「環境を片付け」など、開発環境のクリーンアップ依頼があった際に使用する。
allowed-tools: Bash, Read
---

# Worktree破棄スキル

現在のセッションで使用しているworktree環境を自動特定して破棄する。

## 1. 現在のworktree番号を自動判定

以下のコマンドで現在のworking directoryを確認する:

```bash
pwd
```

- `worktree-N` の形式が含まれていれば、N がINSTANCE_ID
- そうでない場合（プロジェクトの main worktree 等）は、Environment情報の "Additional working directories" を確認し、`worktree-N` にマッチするものからINSTANCE_IDを特定する
- 複数ある場合はユーザーに確認する

## 2. 稼働中のworktreeと関連コンテナを確認

```bash
for i in 1 2 3 4; do
  dir="../worktree-${i}"
  if [ -d "$dir" ]; then
    branch=$(git -C "$dir" branch --show-current 2>/dev/null || echo "不明")
    container=$(docker ps -a --filter "label=devcontainer.local_folder=$(cd "$dir" && pwd)" --format "{{.Names}} ({{.Status}})" 2>/dev/null || echo "なし")
    echo "  worktree-${i}: ブランチ=${branch}, コンテナ=${container:-なし}"
  fi
done
```

## 3. 未コミット・未プッシュの変更を確認

特定したINSTANCE_IDを使って確認する:

```bash
git -C "../worktree-<INSTANCE_ID>" status
git -C "../worktree-<INSTANCE_ID>" log <primary_branch>..HEAD --oneline 2>/dev/null  # <primary_branch> = .stdd.config.yml の project.primary_branch
```

## 4. 破棄を実行

```bash
./scripts/remove-worktree.sh -i <INSTANCE_ID>
```

デフォルトではDockerイメージを保持して次回の起動を高速化する。
`--clean` を付けるとイメージも含めて完全削除する。

## 5. 破棄後の確認

```bash
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "REPOSITORY|vsc-<project_name>"
docker volume ls --format "table {{.Name}}" | grep -E "NAME|<project_name>|dind"
```

## 注意事項

- 未コミットの変更がないか事前に確認すること
- コミット済みだがpush未完了のブランチがないか確認すること
- デフォルトではDockerイメージは保持される（次回起動の高速化のため）
