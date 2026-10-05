---
name: repo-publish
description: Private リポを Public 化する。全履歴のシークレットスキャン → 公開 → 公開時にしかできない設定（ruleset・auto-merge）までを一括で行う。公開したいとき、gh repo edit --visibility を打ちたくなったときに必ず使用する。
disable-model-invocation: true
---

# repo-publish

Private → Public は**公開後に取り消せない唯一の不可逆点**（履歴は fork・クロール・アーカイブに残りうる）。gh 一発で公開せず、必ず本手順を踏む。

**公開パイプラインの固定順**: `repo-standardize → guarantee-audit → repo-readme → readme-i18n → repo-publish → repo-about`。本 Skill は**第5**。この順は都度再判断しない。

## 前提

- `repo-standardize` 済み（LICENSE・README コアメッセージ・CI・dependabot）。未実施ならそちらが先。
- README 肉付け（`repo-readme`）・英語版（`readme-i18n`）は公開前に済んでいるのが既定。user が明示的に急ぐ場合のみ省略可。

## 1. 全履歴シークレットスキャン（公開前・必須）

ワーキングツリーだけでなく **git 履歴全体** を見る。

```bash
# 汎用スキャン（gitleaks）
nix run nixpkgs#gitleaks -- detect --source . --log-opts="--all"
```

```bash
# フリート固有値スキャン: secrets-agents 辞書の実値が履歴に無いか
# ~/dotfiles/secrets-agents/*.md の「実値」列（ドメイン・Tailscale IP・Tunnel UUID・
# OAuth Secret・SSH ユーザ等）を対象に、履歴全体を grep する
git grep -I "{実値}" $(git rev-list --all) | head
```

辞書の実値は多いので、そのリポに関係しうるもの（デプロイ先・使用サービス）に絞ってよい。ただし `<BASE_DOMAIN>`・Tailscale IP・OAuth/tskey 系は必ず全履歴を確認する。

**検出された場合**: 公開を中止して user に報告する。履歴書き換え（`git filter-repo`）は影響が大きいため相談者が勝手にやらない。

## 2. 直前チェック

```
[ ] スキャン結果クリーン（gitleaks + 辞書 grep）
[ ] LICENSE の年・owner が正しい
[ ] README の画像・GIF がリポ内パス参照（外部 URL や private 依存が無い）
[ ] .env が追跡されていない（git ls-files | grep -c '\.env$' が 0）
[ ] GitHub Secrets に登録済みの値がワークフロー YAML に直書きされていない
[ ] docs/guarantees.md が存在する、または skip 理由（テストなし等）がチャットで明示されている
```

## 3. 公開

スキャン結果を user に提示し、公開してよいか**この時点で一度確認する**（不可逆のため。事前に「公開まで一括でやって」と明示されている場合は省略可）。

```bash
gh repo edit {owner}/{repo} --visibility public --accept-visibility-change-consequences
```

## 4. 公開直後の設定（private/Free では設定できなかったもの）

```bash
# auto-merge 有効化（dependabot-auto-merge workflow の前提）
gh repo edit {owner}/{repo} --enable-auto-merge

# main の ruleset: required status check に CI のジョブ名、bypass に Repository admin
gh api repos/{owner}/{repo}/rulesets -X POST --input - <<'EOF'
{
  "name": "main-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "required_status_checks",
      "parameters": { "strict_required_status_checks_policy": false,
        "required_status_checks": [ { "context": "test" } ] } }
  ],
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always" }
  ]
}
EOF
```

`"context": "test"` は CI のジョブ名に合わせる（`ci.yml` の `jobs.{name}`）。`actor_id: 5` は Repository admin。

## 5. 公開後の確認

```
[ ] リポページが匿名で見える（gh api repos/{owner}/{repo} --jq .private が false）
[ ] README の CI バッジ・GIF が描画される
[ ] ruleset が active（gh api repos/{owner}/{repo}/rulesets --jq '.[].name'）
[ ] allow_auto_merge が true
```

## 6. ローカルの配置換え（~/github-private → ~/github-public）

ローカルの規約は「visibility とディレクトリを一致させる」。公開が確認できたら作業コピーを**確認を取らずにそのまま移す**（user への確認は §3 の公開判断で済んでいる。mv は可逆であり、ここで止まると配置換えが漏れる。本スキルの完了条件に含む）。

```bash
mv ~/github-private/{repo} ~/github-public/{repo}
```

git 自体は無風（リポは自己完結・リモート URL はパス非依存）。整合を取るのは**旧パスを絶対参照している周辺**で、以下を確認する。

```bash
# 他リポ・設定からの絶対パス参照（PYTHONPATH・スクリプト・launchd・cron 等）
grep -rn "github-private/{repo}" ~/dotfiles ~/github-private ~/github-public 2>/dev/null
```

- venv（`pip install -e` 済み含む）は旧パスを記録しているため、移動後に作り直す
- 開いているエディタ・実行中の Claude セッションは旧パスを見ているので、user に移動した旨を伝える

About（description / topics）が未設定なら `repo-about` スキルを続けて実行する。
