---
name: deployment-verifier
description: Enforce comprehensive deployment verification after deploying code, scripts, or configurations. Use after any deployment, build, or installation operation. Prevents deployment verification failures (FP-9).
---

# Deployment Verifier

**Version**: 1.0.0
**対策対象**: FP-9 (デプロイ検証不足)
**優先度**: 高
**出典**: vibration-diagnosis-prototype失敗事例、WORK_PROCESS_PROTOCOLS

## The Iron Law

> Every deployment MUST be verified before declaring completion

**定義**: デプロイ = コード、スクリプト、設定ファイル、パッケージ等を本番環境・テスト環境・ローカル環境に配置すること

---

## 4-Stage Verification Process

### Stage 1: Pre-Deployment (配備前確認)

**目的**: デプロイの安全性を事前確認

**Checklist**:
```
□ デプロイ対象ファイルを明確化
□ バックアップ取得（必要に応じて）
□ 依存関係を確認（パッケージ、ライブラリ等）
□ デプロイ先環境を確認（dev/staging/prod）
□ ロールバック手順を準備
```

**実行コマンド例**:
```bash
# Gitステータス確認
git status

# 変更内容確認
git diff

# 依存関係確認
npm list  # Node.js
pip list  # Python
```

**禁止事項**:
- ❌ 確認なしでデプロイコマンド実行
- ❌ バックアップなしで本番環境変更
- ❌ 依存関係の未確認

---

### Stage 2: During Deployment (配備中監視)

**目的**: デプロイプロセスのエラー検出

**Checklist**:
```
□ デプロイコマンドの出力を監視
□ エラーメッセージがないか確認
□ 警告メッセージを記録
□ 実行時間が異常でないか確認
```

**実行例**:
```bash
# デプロイコマンド（出力を監視）
npm install 2>&1 | tee deploy.log

# ビルドコマンド（出力を監視）
npm run build 2>&1 | tee build.log
```

**確認ポイント**:
- Exit code が 0 か？
- "ERROR", "FAIL", "FATAL" 等のキーワードがないか？
- "WARN" がある場合、内容を確認
- ファイルが正しい場所に配置されたか？

---

### Stage 3: Post-Deployment (配備後検証)

**目的**: デプロイが成功したことを確認

**3.1 存在確認**:
```bash
# ファイル存在確認
ls -la /path/to/deployed/files

# パッケージインストール確認
npm list <package>  # Node.js
pip show <package>  # Python
```

**3.2 動作確認**:
```bash
# スクリプト実行テスト
node script.js
python script.py

# ビルド成果物確認
ls -la dist/
ls -la build/
```

**3.3 統合テスト**:
```bash
# テスト実行
npm test
pytest

# エンドツーエンドテスト
npm run e2e
```

**Checklist**:
```
□ ファイルが存在するか？
□ 実行権限が正しいか？
□ 依存関係が解決されたか？
□ スクリプトが実行できるか？
□ テストがパスするか？
```

---

### Stage 4: Definition of Done (完了基準)

**必須条件** (すべて満たすこと):

```yaml
✅ Pre-Deployment: 事前確認完了
✅ During-Deployment: エラーなし
✅ Post-Deployment: 動作確認完了
✅ Tests: 全テストパス
✅ Documentation: デプロイ記録完了
→ 完了
```

**未完了の例**:
- ❌ "デプロイしました" だけで完了宣言
- ❌ エラーログを確認せずに完了
- ❌ テストを実行せずに完了
- ❌ "多分動いている" 状態

---

## Deployment Scenarios (シナリオ別検証)

### Scenario 1: npm install / pip install

**Pre-Deployment**:
```bash
# package.json / requirements.txt 確認
cat package.json
cat requirements.txt

# 既存パッケージリスト保存
npm list > before.txt
pip freeze > before.txt
```

**During-Deployment**:
```bash
# インストール実行（ログ保存）
npm install 2>&1 | tee npm-install.log
pip install -r requirements.txt 2>&1 | tee pip-install.log
```

**Post-Deployment**:
```bash
# インストール成功確認
npm list <new-package>
pip show <new-package>

# バージョン確認
npm list | grep <package>
pip freeze | grep <package>

# 動作確認
node -e "require('<package>')"
python -c "import <package>"
```

**Definition of Done**:
```
✅ パッケージがインストールされた
✅ バージョンが正しい
✅ import/require が成功する
✅ 依存関係が解決された
```

---

### Scenario 2: git clone / git pull

**Pre-Deployment**:
```bash
# 現在のブランチ・コミット確認
git branch
git log -1

# 未コミット変更確認
git status
```

**During-Deployment**:
```bash
# クローン or プル
git clone <repo> 2>&1 | tee git-clone.log
git pull origin main 2>&1 | tee git-pull.log
```

**Post-Deployment**:
```bash
# リポジトリ確認
ls -la
cat README.md

# ブランチ確認
git branch -a

# コミット履歴確認
git log -5

# ファイル数確認
find . -type f | wc -l
```

**Definition of Done**:
```
✅ リポジトリがクローンされた
✅ ブランチが正しい
✅ 必要なファイルが存在する
✅ .git ディレクトリが存在する
```

---

### Scenario 3: ビルド成果物のデプロイ

**Pre-Deployment**:
```bash
# ビルド設定確認
cat webpack.config.js
cat tsconfig.json

# デプロイ先ディレクトリ確認
ls -la dist/
ls -la build/
```

**During-Deployment**:
```bash
# ビルド実行
npm run build 2>&1 | tee build.log

# デプロイ実行
cp -r dist/* /path/to/deploy/ 2>&1 | tee deploy.log
```

**Post-Deployment**:
```bash
# ファイル存在確認
ls -la /path/to/deploy/

# ファイルサイズ確認（0バイトでないか）
find /path/to/deploy/ -type f -size 0

# 実行権限確認
ls -la /path/to/deploy/*.sh

# 動作確認
/path/to/deploy/app --version
```

**Definition of Done**:
```
✅ ビルドが成功した
✅ ファイルがデプロイされた
✅ ファイルサイズが正常
✅ 実行権限が正しい
✅ アプリケーションが起動する
```

---

### Scenario 4: 設定ファイルの配備

**Pre-Deployment**:
```bash
# 既存設定のバックアップ
cp config.json config.json.backup
cp .env .env.backup

# 変更内容確認
diff config.json.backup config.json
```

**During-Deployment**:
```bash
# 設定ファイル配備
cp new-config.json config.json

# 権限設定
chmod 600 config.json  # 機密情報がある場合
```

**Post-Deployment**:
```bash
# ファイル存在確認
cat config.json

# JSON妥当性確認
cat config.json | jq .  # JSON
yamllint config.yaml    # YAML

# アプリケーション読み込み確認
app --validate-config
```

**Definition of Done**:
```
✅ 設定ファイルが配備された
✅ 形式が正しい（JSON/YAML妥当性）
✅ 権限が正しい
✅ アプリケーションが読み込める
```

---

## Prohibited Patterns (アンチパターン)

### Anti-Pattern 1: "デプロイしました" 完了宣言

**症状**:
```
User: "このパッケージをインストールしてください"
❌ Bad: "npm install を実行しました。完了です。"
```

**正しい対応**:
```
User: "このパッケージをインストールしてください"
✅ Good:
"1. Pre-Deployment: package.json を確認しました
2. During-Deployment: npm install を実行しました
   - 出力: [ログ内容]
   - Exit code: 0
3. Post-Deployment: パッケージを確認しました
   - npm list: パッケージが存在
   - import テスト: 成功
4. Tests: テストを実行しました
   - 結果: 全テストパス

完了です。"
```

---

### Anti-Pattern 2: エラーログ未確認

**症状** (vibration-diagnosis-prototype):
```bash
$ npm install
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /package.json
npm ERR! errno -2
...

❌ Bad: "インストールしました。完了です。"
```

**正しい対応**:
```bash
$ npm install
npm ERR! code ENOENT
...

✅ Good:
"エラーが発生しました:
- エラーコード: ENOENT
- 原因: package.json が見つかりません
- 対処: カレントディレクトリを確認し、正しいディレクトリで実行します

修正後、再度実行します。"
```

---

### Anti-Pattern 3: テスト未実行

**症状**:
```
❌ Bad: "コードをデプロイしました。完了です。"
（テストを実行していない）
```

**正しい対応**:
```
✅ Good:
"1. コードをデプロイしました
2. テストを実行します:
   $ npm test
   [テスト結果]
   - 全テストパス: ✅
3. 動作確認:
   $ node app.js --version
   - v1.2.3

完了です。"
```

---

## Verification Examples (検証例)

### Example 1: Python パッケージインストール

```bash
# Stage 1: Pre-Deployment
$ cat requirements.txt
requests==2.28.0

$ pip freeze | grep requests
# （既存バージョン確認）

# Stage 2: During-Deployment
$ pip install -r requirements.txt
Collecting requests==2.28.0
  Downloading requests-2.28.0-py3-none-any.whl (62 kB)
Installing collected packages: requests
Successfully installed requests-2.28.0

# Stage 3: Post-Deployment
$ pip show requests
Name: requests
Version: 2.28.0
✅ 正しいバージョンがインストールされた

$ python -c "import requests; print(requests.__version__)"
2.28.0
✅ import が成功した

# Stage 4: Definition of Done
✅ Pre-Deployment完了
✅ During-Deployment エラーなし
✅ Post-Deployment 動作確認完了
→ 完了
```

---

### Example 2: Node.js ビルドとデプロイ

```bash
# Stage 1: Pre-Deployment
$ ls -la dist/
ls: cannot access 'dist/': No such file or directory
✅ デプロイ先が空であることを確認

# Stage 2: During-Deployment
$ npm run build
> build
> webpack --mode production

asset main.js 1.2 KiB [compared for emit] [minimized] (name: main)
webpack 5.75.0 compiled successfully in 234 ms
✅ ビルド成功

# Stage 3: Post-Deployment
$ ls -la dist/
total 12
-rw-r--r-- 1 user user 1234 Dec 27 10:00 main.js
-rw-r--r-- 1 user user 567  Dec 27 10:00 index.html
✅ ファイルが生成された

$ find dist/ -type f -size 0
✅ 0バイトファイルなし

$ node dist/main.js
Hello World
✅ 動作確認完了

# Stage 4: Definition of Done
✅ All checks passed
→ 完了
```

---

## Error Handling Protocols

### Protocol 1: Exit Code 確認

**必須**:
```bash
# コマンド実行後、必ずexit codeを確認
echo $?  # Linux/Mac
echo %ERRORLEVEL%  # Windows

# 0以外の場合はエラー
```

### Protocol 2: ログ保存

**推奨**:
```bash
# 重要なデプロイは必ずログ保存
npm install 2>&1 | tee npm-install-$(date +%Y%m%d-%H%M%S).log
```

### Protocol 3: エラー時の対応

**手順**:
```
1. エラーメッセージを全文読む
2. エラーコードを特定
3. 原因を診断（推測禁止、ファイル確認）
4. 修正を実施
5. 再実行
6. 検証
```

---

## Multi-layer Defense (3層防御)

**Layer 1: Rules** (弱)
- `docs/rules/deployment.md` - デプロイ検証ルール
- LLMが無視する可能性あり

**Layer 2: Skills** (中) ← **このSkill**
- **deployment-verifier**: デプロイ検証強制
- タスク開始時に自動適用

**Layer 3: Hooks** (強)
- `post_deploy_verification.sh`: デプロイ後自動検証
- 最も強力な防御

---

## Invocation Examples

### Example 1: パッケージインストール

**User**: "requests パッケージをインストールしてください"

**Skill Response**:
```
Deployment Verifier が起動しました。

Stage 1: Pre-Deployment
□ requirements.txt を確認
□ 既存バージョン確認: pip freeze | grep requests

Stage 2: During-Deployment
□ pip install requests 実行
□ 出力を監視

Stage 3: Post-Deployment
□ pip show requests で確認
□ import テスト実行

Stage 4: Definition of Done
全ステージ完了後に完了宣言します。
```

---

### Example 2: ビルド実行

**User**: "アプリをビルドしてください"

**Skill Response**:
```
Deployment Verifier が起動しました。

Stage 1: Pre-Deployment
□ ビルド設定確認（webpack.config.js等）
□ デプロイ先ディレクトリ確認

Stage 2: During-Deployment
□ npm run build 実行
□ エラー・警告を監視

Stage 3: Post-Deployment
□ ビルド成果物確認（dist/）
□ ファイルサイズ確認
□ 動作確認

Stage 4: Definition of Done
全ステージ完了後に完了宣言します。
```

---

## Best Practices

### 1. Documentation (記録)

**デプロイ記録**:
```markdown
# Deployment Log - 2025-12-27

## Objective
Install requests package v2.28.0

## Pre-Deployment
- Checked requirements.txt: ✅
- Backup created: ✅

## During-Deployment
- Command: pip install requests==2.28.0
- Exit code: 0
- Warnings: None

## Post-Deployment
- Package installed: ✅ (pip show requests)
- Import test: ✅ (python -c "import requests")
- Version: 2.28.0

## Definition of Done
All checks passed: ✅

Status: COMPLETED
```

### 2. Rollback Preparation (ロールバック準備)

**必須** (本番環境):
```bash
# バックアップ取得
cp -r /app /app.backup.$(date +%Y%m%d-%H%M%S)

# デプロイ実施
cp new-app /app

# 問題発生時のロールバック
cp -r /app.backup.20251227-100000 /app
```

### 3. Staged Deployment (段階的デプロイ)

**推奨**:
```
1. Local環境でテスト
2. Development環境でテスト
3. Staging環境でテスト
4. Production環境にデプロイ
```

---

## Related Resources

### Internal
- `docs/rules/deployment.md` - デプロイ検証ルール詳細
- `test-process-requirements.md` - テストプロセス要件

### External
- WORK_PROCESS_PROTOCOLS - 検証プロトコル

### Phase 3成果物
- `step3.5-failure-case-analysis.md` - FP-9詳細分析
- `CRITICAL_FAILURE_REPORT_20251226.md` - vibration-diagnosis-prototype失敗事例

---

## Completion Criteria

```yaml
✅ Pre-Deployment: 事前確認完了
✅ During-Deployment: エラーなし
✅ Post-Deployment: 動作確認完了
✅ Tests: 全テストパス（該当する場合）
✅ Documentation: デプロイ記録完了
```

**不完全な状態での完了宣言は禁止**

---

**注意**: このSkillは自動的に起動されます。無効化したい場合は `.claude/settings.local.json` から削除してください。
