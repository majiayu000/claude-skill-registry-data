---
name: root-cause-analyzer
description: Enforce evidence-based thinking and root cause analysis before making code changes. Use when debugging, investigating issues, or diagnosing problems. Prevents guessing-based implementation (FP-8).
---

# Root Cause Analyzer

**Version**: 1.0.0
**対策対象**: FP-8 (推測による実装)
**優先度**: 最高
**出典**: WORK_PROCESS_PROTOCOLS, vibration-diagnosis-prototype失敗事例

## The Iron Law

> Read First, Code Later
> Trust, but Verify
> No Guessing, Only Evidence

**出典**: WORK_PROCESS_PROTOCOLS Protocol 1

---

## 3-Step Approach

### Step 1: Read (読む)

**目的**: 事実を収集し、推測を排除

**実行内容**:
```
□ 関連ファイルをすべて読む
□ エラーメッセージを全文読む
□ ログファイルを確認する
□ ドキュメントを確認する
□ テストコードを確認する
```

**禁止事項**:
- ❌ ファイル名だけで判断する
- ❌ "多分こうだろう" と推測する
- ❌ エラーメッセージを途中まで読んで判断
- ❌ ログを確認せずに進める

---

### Step 2: Verify (確認する)

**目的**: 仮説を検証し、証拠を確保

**実行内容**:
```
□ 仮説を立てる
□ 実際に動かして確認する
□ ログ出力を追加して確認する
□ デバッガで変数を確認する
□ テストを書いて確認する
```

**確認方法**:
- **ファイル存在確認**: `ls`, `stat`, `test -f`
- **関数定義確認**: `grep -r "def function_name"`
- **変数確認**: `console.log`, `print`, デバッガ
- **動作確認**: 実際に実行してログ確認

**禁止事項**:
- ❌ 確認せずに "あるはず" と仮定
- ❌ "動くはず" と思い込む
- ❌ ドキュメントを信じて確認しない

---

### Step 3: Implement (実装する)

**目的**: 証拠に基づいて正しく実装

**実行内容**:
```
□ Step 1, 2で得た証拠を元に実装
□ 実装後、再度確認
□ テストを実行
□ 動作確認
```

**完了基準**:
```
✅ 証拠に基づいて実装した
✅ 推測による実装が0件
✅ すべて確認済み
✅ テストがパス
→ 完了
```

---

## Root Cause Analysis Workflow

### Phase 1: Problem Definition (問題定義)

**明確化すべき項目**:
```markdown
## Problem Definition

### Symptom（症状）
何が起きているか？（具体的な現象）

### Expected Behavior（期待動作）
何が起きるべきか？（本来の動作）

### Actual Behavior（実際の動作）
実際に何が起きているか？（観測された動作）

### Impact（影響）
誰・何に影響するか？（影響範囲）

### Frequency（頻度）
どのくらいの頻度で発生するか？（再現性）
```

**例**:
```markdown
## Problem Definition

### Symptom
ユーザーログインが失敗する

### Expected Behavior
正しいパスワードでログイン成功

### Actual Behavior
正しいパスワードでも "Invalid password" エラー

### Impact
全ユーザー（1000人）がログインできない

### Frequency
100%再現（常に発生）
```

---

### Phase 2: Evidence Collection (証拠収集)

**収集すべき証拠**:

#### 1. Log Files（ログファイル）
```bash
# アプリケーションログ確認
tail -100 app.log
grep "ERROR" app.log
grep "password" app.log

# システムログ確認
journalctl -xe
```

#### 2. Error Messages（エラーメッセージ）
```
□ エラーメッセージ全文を記録
□ スタックトレースを記録
□ エラーコードを記録
□ 発生時刻を記録
```

#### 3. Code Review（コード確認）
```bash
# 関連コードを読む
cat src/auth/password.js

# 関数定義を探す
grep -r "validatePassword"

# 変更履歴を確認
git log --oneline src/auth/
git diff HEAD~5 src/auth/password.js
```

#### 4. Configuration（設定確認）
```bash
# 設定ファイル確認
cat config.json
cat .env

# 環境変数確認
printenv | grep PASSWORD
```

#### 5. Database/State（データベース・状態確認）
```bash
# データベース確認（該当する場合）
SELECT * FROM users WHERE username='test';

# ファイルシステム確認
ls -la /path/to/data
```

**証拠記録テンプレート**:
```markdown
## Evidence Collection

### Logs
\```
[ログ内容をコピペ]
\```

### Error Messages
\```
[エラーメッセージ全文]
\```

### Code Review
\```
[関連コード]
\```

### Configuration
\```
[設定内容]
\```

### Observed Facts
- Fact 1: [確認した事実]
- Fact 2: [確認した事実]
```

---

### Phase 3: Hypothesis Formation (仮説構築)

**5 Whys Technique（5回のなぜ）**:

```markdown
## 5 Whys Analysis

1. Why did the problem occur?
   → [仮説1]

2. Why [仮説1]?
   → [仮説2]

3. Why [仮説2]?
   → [仮説3]

4. Why [仮説3]?
   → [仮説4]

5. Why [仮説4]?
   → [Root Cause - 根本原因]
```

**例**:
```markdown
## 5 Whys Analysis

1. Why does login fail?
   → Password validation fails

2. Why does password validation fail?
   → Hash comparison returns false

3. Why does hash comparison return false?
   → Hash algorithm mismatch

4. Why is there a hash algorithm mismatch?
   → Code was updated from bcrypt to argon2

5. Why wasn't the database migrated?
   → Migration script was not executed
   → **Root Cause**: Database still contains bcrypt hashes
```

---

### Phase 4: Hypothesis Verification (仮説検証)

**検証方法**:

#### Method 1: Logging（ログ追加）
```python
# ログを追加して変数を確認
def validate_password(input_password, stored_hash):
    print(f"DEBUG: input_password={input_password}")
    print(f"DEBUG: stored_hash={stored_hash}")
    print(f"DEBUG: hash_algorithm={detect_algorithm(stored_hash)}")

    result = compare_hash(input_password, stored_hash)
    print(f"DEBUG: result={result}")
    return result
```

#### Method 2: Unit Test（単体テスト）
```python
# テストを書いて仮説を検証
def test_password_validation_with_bcrypt_hash():
    # Given: bcrypt hash
    stored_hash = "$2b$12$..."

    # When: validate with correct password
    result = validate_password("correct_password", stored_hash)

    # Then: should succeed
    assert result == True  # 失敗 → 仮説が正しい
```

#### Method 3: Debugger（デバッガ）
```bash
# Python debugger
python -m pdb app.py

# Node.js debugger
node inspect app.js

# ブレークポイント設定して変数確認
```

#### Method 4: Minimal Reproduction（最小再現）
```python
# 最小限のコードで再現
import bcrypt
import argon2

bcrypt_hash = bcrypt.hashpw(b"password", bcrypt.gensalt())
print(f"bcrypt_hash: {bcrypt_hash}")

# argon2で検証を試みる
try:
    argon2.verify(bcrypt_hash, b"password")
except Exception as e:
    print(f"Error: {e}")  # 仮説検証: エラーが発生
```

**検証結果記録**:
```markdown
## Hypothesis Verification

### Hypothesis（仮説）
bcrypt hashをargon2で検証しようとしている

### Verification Method（検証方法）
最小再現コードで確認

### Result（結果）
✅ Error: Hash type mismatch
→ 仮説が正しいことを確認

### Root Cause Confirmed（根本原因確定）
Database migration未実施により、
bcrypt hashをargon2で検証しようとしてエラー
```

---

### Phase 5: Solution Implementation (解決策実装)

**実装前チェック**:
```
□ Root Causeを特定した
□ 解決策を設計した
□ 影響範囲を確認した
□ テスト計画を立てた
□ ロールバック手順を準備した
```

**実装手順**:
```markdown
## Solution Implementation

### Root Cause（根本原因）
[確定した根本原因]

### Solution（解決策）
[実装する解決策]

### Implementation Steps（実装手順）
1. [ステップ1]
2. [ステップ2]
3. [ステップ3]

### Verification（検証）
- [ ] 単体テスト
- [ ] 統合テスト
- [ ] 手動テスト
- [ ] 本番環境確認（該当する場合）

### Rollback Plan（ロールバック手順）
[問題発生時の戻し方]
```

---

## Prohibited Patterns (アンチパターン)

### Anti-Pattern 1: Guessing-Based Implementation（推測による実装）

**症状** (vibration-diagnosis-prototype):
```
User: "エラーが出ています"
❌ Bad: "多分パスの問題です。修正します"
（ログを確認していない、推測で実装）
```

**正しい対応**:
```
User: "エラーが出ています"
✅ Good:
"Root Cause Analyzer を起動しました。

Step 1: Evidence Collection
□ エラーメッセージ全文を確認
□ ログファイルを確認
□ 関連コードを確認

[ログ確認後]
証拠: エラーは `FileNotFoundError: file.txt`
仮説: file.txt が存在しない

Step 2: Verification
$ ls -la file.txt
ls: file.txt: No such file or directory
✅ 仮説確認: file.txt が存在しない

Step 3: Root Cause Analysis
5 Whys:
1. Why missing? → ファイルが作成されていない
2. Why not created? → 作成処理がスキップされた
3. Why skipped? → 条件分岐でelseブロックに入った
4. Why else? → 環境変数が設定されていない
5. Root Cause: .env ファイルが配備されていない

Solution: .env ファイルを配備します"
```

---

### Anti-Pattern 2: Assumption-Based Debugging（仮定ベースのデバッグ）

**症状**:
```python
# ❌ Bad: 確認せずに仮定
def get_user(user_id):
    # "データベースに存在するはず" と仮定
    user = db.query(User).filter_by(id=user_id).first()
    return user.name  # user が None の可能性を考慮せず
```

**正しい対応**:
```python
# ✅ Good: 確認してから処理
def get_user(user_id):
    user = db.query(User).filter_by(id=user_id).first()

    # 証拠: userの存在を確認
    if user is None:
        logger.error(f"User not found: {user_id}")
        raise ValueError(f"User {user_id} does not exist")

    return user.name
```

---

### Anti-Pattern 3: Documentation-Only Verification（ドキュメントだけ信じる）

**症状**:
```
ドキュメント: "function_name() は value を返します"
❌ Bad: "ドキュメント通りのはず" と信じて実装
（実際の動作を確認していない）
```

**正しい対応**:
```
ドキュメント: "function_name() は value を返します"
✅ Good:
"Trust, but Verify - 確認します"

$ python -c "result = function_name(); print(type(result), result)"
<class 'NoneType'> None

証拠: 実際には None を返している
→ ドキュメントが古いまたは誤り
→ 実際の動作に合わせて実装
```

---

## Evidence Collection Checklist

### File System（ファイルシステム）
```bash
# ファイル存在確認
ls -la /path/to/file
test -f /path/to/file && echo "exists" || echo "not found"

# ディレクトリ構造確認
tree /path/to/directory
find /path/to/directory -type f

# ファイル内容確認
cat /path/to/file
head -20 /path/to/file
```

### Code（コード）
```bash
# 関数定義を探す
grep -rn "def function_name" .
grep -rn "function function_name" .

# クラス定義を探す
grep -rn "class ClassName" .

# import文を探す
grep -rn "import module_name" .
grep -rn "from module_name" .
```

### Git History（Git履歴）
```bash
# 変更履歴確認
git log --oneline --graph --all

# 特定ファイルの変更履歴
git log --follow /path/to/file

# 最近の変更差分
git diff HEAD~5..HEAD

# 誰が変更したか
git blame /path/to/file
```

### Runtime State（実行時状態）
```bash
# プロセス確認
ps aux | grep app_name

# ポート確認
netstat -an | grep PORT
lsof -i :PORT

# 環境変数確認
printenv
echo $VARIABLE_NAME
```

---

## Multi-layer Defense (3層防御)

**Layer 1: Rules** (弱)
- `docs/rules/evidence-based-thinking.md` - 証拠ベース思考
- LLMが無視する可能性あり

**Layer 2: Skills** (中) ← **このSkill**
- **root-cause-analyzer**: 証拠収集強制
- タスク開始時に自動適用

**Layer 3: Hooks** (強)
- （該当なし - Skillで十分強力）

---

## Invocation Examples

### Example 1: エラー調査

**User**: "エラーが出ています。修正してください"

**Skill Response**:
```
Root Cause Analyzer が起動しました。

Step 1: Evidence Collection
まず、エラーの詳細を確認します。

1. エラーメッセージ全文を提供してください
2. ログファイルを確認します
3. 関連コードを確認します

推測ではなく、証拠に基づいて根本原因を特定します。
```

---

### Example 2: バグ修正

**User**: "この機能が動きません"

**Skill Response**:
```
Root Cause Analyzer が起動しました。

Step 1: Problem Definition
何が起きているか明確化します:

1. Expected Behavior: 何が起きるべきですか？
2. Actual Behavior: 実際に何が起きていますか？
3. Reproduction Steps: どうすれば再現しますか？

Step 2: Evidence Collection
事実を収集します:
- ログ確認
- コード確認
- 動作確認

Step 3: Root Cause Analysis
5 Whysで根本原因を特定します。

証拠に基づいて修正を実施します。
```

---

## Best Practices

### 1. Always Read the Code（常にコードを読む）

**Good**:
```
1. 関連ファイルをすべて読む
2. 理解してから実装
3. 推測を排除
```

**Bad**:
```
1. ファイル名だけ見る
2. "多分こうだろう" と推測
3. すぐにコードを書く
```

---

### 2. Trust, but Verify（信頼するが検証する）

**Good**:
```
ドキュメント: "function() は string を返す"
→ 実際に実行して確認: print(type(function()))
→ 証拠: <class 'str'>
→ ドキュメント通り ✅
```

**Bad**:
```
ドキュメント: "function() は string を返す"
→ "そのはず" と信じて実装
→ 実行時エラー（実際は None を返す）❌
```

---

### 3. Evidence-Based Decisions（証拠ベースの意思決定）

**Good**:
```
仮説: "パフォーマンスボトルネックは DB クエリ"
検証: プロファイラで測定
証拠: DB クエリは 5ms, JSON parse が 500ms
結論: JSON parse が原因（仮説は誤り）
→ JSON parse を最適化
```

**Bad**:
```
仮説: "パフォーマンスボトルネックは DB クエリ"
検証: なし
→ DB クエリを最適化（効果なし）
→ 時間の無駄
```

---

## Related Resources

### Internal
- `docs/rules/evidence-based-thinking.md` - 証拠ベース思考詳細
- `docs/rules/implementation.md` - 実装品質ルール

### External
- WORK_PROCESS_PROTOCOLS - Protocol 1: Read First, Code Later
- 5 Whys Technique - Toyota Production System

### Phase 3成果物
- `step3.5-failure-case-analysis.md` - FP-8詳細分析
- `CRITICAL_FAILURE_REPORT_20251226.md` - vibration-diagnosis-prototype失敗事例

---

## Completion Criteria

```yaml
✅ Evidence Collection完了
✅ Root Cause特定完了
✅ Hypothesis Verification完了
✅ 推測による実装0件
✅ 全て確認済み
```

**推測ベースの実装は禁止**

---

**注意**: このSkillは自動的に起動されます。無効化したい場合は `.claude/settings.local.json` から削除してください。
