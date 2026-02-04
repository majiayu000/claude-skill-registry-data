---
name: why-verify-risk
description: 学習目的で、あらゆる提案変更に WHY / VERIFY / RISK とロールバックを必ず付ける（コード・コマンド・AWS手順）。WHYは「選択肢→特徴→結論（最適案）」で統一する。
---

# WHY / VERIFY / RISK（学習のための変更規律：選択肢→比較→結論）

## 使うタイミング（When to use）
次のいずれかの「変更を提案・実施」するときは、必ずこのスキルを適用する。
- コード修正（バグ修正、リファクタ、機能追加・変更）
- 設定変更（フレームワーク設定、CI、デプロイ設定）
- CLIコマンド（git、npm、aws、shell など）
- AWSコンソール操作（S3、CloudFront、IAM、Billing など）
- レビューコメントでの変更提案

## 非目標（Non-goals）
- 明示されない限り、大規模システムをゼロから作らない。
- 時間短縮のために、検証（VERIFY）や戻し方（RISK/rollback）を省略しない。

## 必須の出力構造（Required output structure / MUST）
あらゆる変更提案について、次の3セクションを「この順番で必ず」出す。
出力順：WHY → VERIFY → RISK（順序固定）

### 1) WHY（選択肢→特徴→結論）
WHY は「代替案」ではなく、常に次の型で書く。

1) Options（選択肢）
- 選択肢を 2〜3 個だけ列挙する（多すぎる選択肢は出さない）。
- 各選択肢は 1 行でラベル化する（例：Option A: OAC / Option B: Public S3）。

2) Characteristics（特徴）
- 各選択肢の特徴を短く書く（学習・安全・運用・コストの観点）。
- trade-off（交換条件）を必ず 1 つ以上書く。

3) Recommendation（結論＝最適案）
- 「今回はこれが最適」と 1 行で結論を書く。
- 結論の理由は 1〜2 行で（なぜ今回の目的に合うか）。

※ English tip: “Options → Comparison → Recommendation” を毎回同じ型で繰り返す。

### 2) VERIFY
すぐに実行できる「具体的な検証手順」を提示する。
- コマンドまたはUI確認（どこを見ればいいか）を明示する。
- 期待結果（成功したらどう見えるか）を書く。
- 前提があるなら明記する（Windows / PowerShell か bash か、リージョン、アカウントなど）。

### 3) RISK
リスクと副作用を箇条書きで列挙する（最低限、次を含む）。
- Security risk（公開範囲、過剰なIAM権限など）
- COST RISK（CloudFront invalidation、データ転送、ログなど）
- ダウンタイム／可用性のリスク
- データ損失／不可逆変更のリスク
- 設定ミス（misconfiguration）のリスク

さらに必ず含める：
- Rollback / Undo 手順（安全に戻す方法）
- COST RISK がある場合：より安全な代替（低コスト/無料枠に収まりやすい案）を 1 つ提示

## 変更のまとめ方ルール（Change packaging rules）

### コード変更の場合（For code changes）
- 最小の diff、または「ファイルパス＋該当箇所の正確な編集」を提示する。
- 変更は小さく、段階的（incremental）にする。
- diff の後に WHY / VERIFY / RISK を必ず付ける（WHYは選択肢→比較→結論）。

### コマンドの場合（For commands）
- 先にコマンドを提示する。
- その後に WHY / VERIFY / RISK を必ず付ける（WHYは選択肢→比較→結論）。
- 破壊的コマンドは、先に安全確認（list/describe/diff など）を要求する（可能なら dry-run を入れる）。

### AWSコンソール操作の場合（For AWS Console steps）
- 短い番号付き手順で提示する。
- 手順の後に WHY / VERIFY / RISK を必ず付ける（WHYは選択肢→比較→結論）。
- 原則：least privilege（最小権限）と private-by-default（まず非公開）。

## 不確実な場合のルール（One-question rule）
安全に進められない情報不足がある場合：
- 最後に「質問は1つだけ」する（targeted question）
- それでも「安全側のデフォルト手順」を提示し、仮定を明記する（Assumptions）。

## デフォルト優先順位（Default security & learning priorities）
- 最小権限（least privilege）を最優先する。
- S3はまず非公開（private by default）。
- Next.js の静的デプロイ学習は、S3（private）+ CloudFront（OAC）構成を優先する。
- 学習は実行中心：explain → verify → rollback を毎回回す。

## 例（Examples）

### 例A：コマンド（Command）
Command:
git reset --soft HEAD~1

WHY:
Options:
- Option A: git reset --soft HEAD~1（コミットだけ戻して変更は保持）
- Option B: git reset --mixed HEAD~1（変更は保持、ステージは外れる）
- Option C: git revert HEAD（履歴は残し、打ち消しコミットを作る）
Characteristics:
- A: まとめ直しに強い / trade-off: push済みだと履歴がズレる
- B: ステージ整理が必要 / trade-off: 追加の add が要る
- C: 安全（履歴維持）/ trade-off: コミットが増える
Recommendation:
- 今回は Option A が最適。直前コミットの内容をまとめ直したい目的に一致する。

VERIFY:
- `git status` で変更が残っていること、ステージ状態が想定通りか確認する。
- `git log --oneline -3` で直前コミットが履歴から消えていることを確認する。

RISK:
- 履歴改変リスク：push済みコミットには使わない（共同作業で衝突しやすい）。
- Rollback: `git reflog` でハッシュ特定 → `git reset --hard <hash>`（破壊的なので注意）。
- COST RISK: なし。

### 例B：AWSコンソール操作（AWS Console step）
Change:
CloudFront から S3 へ OAC でアクセスし、S3 を非公開のまま配信する。

WHY:
Options:
- Option A: S3 private + CloudFront OAC（CDN経由のみ許可）
- Option B: S3 website hosting を public で公開（S3直配信）
Characteristics:
- A: 境界が明確（S3直アクセス遮断）/ trade-off: 設定が少し複雑
- B: 設定は簡単 / trade-off: 公開範囲の管理が難しくなりやすい
Recommendation:
- 今回は Option A が最適。学習目的（アクセス制御の理解）と安全性（private-by-default）に一致する。

VERIFY:
- CloudFront のURLでサイトが表示されることを確認する。
- S3オブジェクトURL直アクセスが拒否（例：403）されることを確認する。

RISK:
- Security risk: バケットポリシー誤りで意図せず公開される可能性。
- Availability risk: origin/policy誤りで配信が壊れる可能性。
- COST RISK: CloudFront のリクエスト/転送が無料枠を超える可能性。
- Rollback: バケットポリシーを元に戻す／OAC関連付け解除／必要な場合のみ invalidation。
