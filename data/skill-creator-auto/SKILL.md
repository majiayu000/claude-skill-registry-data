---
name: skill-creator-auto
description: >
  Automatically designs, initializes, implements, validates, and packages new skills
  from a single high-level request. Use when the user gives a short, possibly vague
  description like "社内Redshift向けのSQLヘルパースキル作って" and wants a complete,
  production-ready .skill file generated with minimal manual intervention.
license: Complete terms in LICENSE.txt
---

# Skill AUTL Creator

このスキルは、**1行レベルの「やりたいこと」から、フルオートでスキルを作り切る**ためのメタスキルです。

通常の `skill-creator` は「人間とClaudeが協力してスキルを作る」前提ですが、この `skill-auto-creator` は:

- 目的の聞き出し
- ユースケースの洗い出し
- スキル構成の設計
- ディレクトリの生成 (`init_skill.py`)
- `scripts/` / `references/` / `assets/` の実装
- SKILL.md の執筆
- 検証 (`quick_validate.py`)
- パッケージング (`package_skill.py`)
- 必要なら改善ループ

までを、**Claude/エージェント主導で再帰的に回し、ほぼ自動で完結させる**ことを目的とします。

---

## 想定する利用シナリオ

- ユーザ:
  「**1行の要望**」を投げる。

  **【新規作成の例】**:
  - `社内Redshiftのメトリクスを分析するスキルを作って`
  - `PDFを分割・結合・回転できるpdf-toolsスキルをフルセットで作って`
  - `NotionのAPIを叩いてDBを同期するスキルを作って`

  **【更新の例】**:
  - `commit-prep-helperを最新の共通ライブラリ方式に更新して`
  - `既存のgithub-issue-improverスキルを移植可能にアップデートして`
  - `すべてのスキルスクリプトを動的.env読み込み方式に更新して`

- エージェント（Claudeなど）:
  1. このSKILL_AUTL.mdに従い、目的・制約・環境を**対話で最小限ヒアリング**
  2. **新規作成の場合**: 設計 → 実装 → 検証 → パッケージ を**自動でループ**
  3. **更新の場合**: 解析 → 差分適用 → 検証 → レポート を**自動でループ**
  4. `.skill` ファイルと、必要なら簡単な README 相当の説明を返す

---

## 基本原則

### コード・指示の一元化（最重要）

**【絶対遵守】**: このスキルは、機能や指示が重複することを断固として拒否する。

- **コード重複の禁止**: 同じ機能を持つコードが複数存在しないようにする
- **指示の一本化**: 同じ内容の指示が複数箇所に存在しないようにする
- **破壊的変更の恐れを克服**: 新しい方式が確立したら、古い方式は即座に完全削除する
- **フォールバックは最小限**: 互換性のためのコード重複は、最小限で安全な代替処理のみにする

#### 実践ルール

1. **新機能追加時**:
   - 既存の類似機能をまず検索
   - 存在する場合は機能拡張を検討
   - 重複が許容されない場合は、既存機能を削除して統合

2. **更新時**:
   - 古い実装は完全に削除
   - 新しい実装に一本化
   - 過渡期のコード共存を許容しない

3. **文書化時**:
   - 同じ説明が複数箇所に存在しないようにする
   - 参照によって一元化する
   - 重複説明は削除統合

この原則を守ることで、メンテナンス性と一貫性を最大化する。

---

## 全体アーキテクチャ

### 使用するローカルスクリプト

- `scripts/init_skill.py`
  新しいスキルのテンプレートディレクトリを生成する。

- `scripts/quick_validate.py`
  スキルフォルダのフォーマットと内容を素早く検証する。

- `scripts/package_skill.py`
  スキルフォルダを `.skill` ファイルとして検証＆パッケージングする。

Claude/エージェントは「ローカル環境に対してコマンド実行できる」か「ツール呼び出し経由でこれらのスクリプトを叩ける」前提とする。

### 既存スキルの更新機能

**重要**: このスキルは新規作成だけでなく、既存スキルの**差分更新**もサポートします。

#### 更新モードの開始条件
- ユーザーが「既存のスキル名を更新して」という指示をした場合
- 例: 「commit-prep-helperを更新して」「既存の〇〇スキルを最新の方式にアップデートして」

#### 更新フロー
1. **既存スキルの解析**:
   - 既存のSKILL.md、scripts/、references/の構造を分析
   - 現在の実装と最新の共通ライブラリ方式との差分を特定
   - 更新が必要な箇所をリストアップ

2. **差分の適用**:
   - 共通ライブラリ使用パターンの更新（絶対パス→動的探索）
   - .env読み込み方式の更新
   - 最新のバリデーションルールへの準拠
   - ドキュメントの修正（必要な場合）

3. **検証とテスト**:
   - `quick_validate.py`で更新後の構造を検証
   - スクリプトが正しく動作することを確認
   - 既存機能が維持されていることをテスト

4. **差分レポート**:
   - 何を変更したかの明確なリスト
   - 変更理由（セキュリティ、移植性、保守性向上など）
   - 影響範囲と互換性情報

#### 更新時の注意点
- **破壊的変更を避ける**: 既存の主要機能は維持
- **段階的適用**: 可能な限り後方互換性を確保
- **明確な記録**: すべての変更をドキュメント化
- **テスト重視**: 更新後の動作確認を必ず実行

### プロジェクト共通ライブラリ

**重要**: すべての生成スキルはMiyabi共通ライブラリを使用する必要があります。

#### 共通ライブラリの存在場所
- パス: `.claude/lib/python/` (プロジェクトルートから見た相対パス)
- 主要モジュール: `env_utils.py`

#### env_utils.py の機能
```python
# 利用可能な関数:
- load_env_files(start_path=None, project_root=None, additional_paths=None)
  - 複数階層の.envファイルを自動検索・読み込み
  - スクリプト位置→プロジェクトルートまで遡って.envを探索
  - 優先順位: スクリプトディレクトリ > カレント > プロジェクトルート > 親階層

- setup_python_path(project_root=None)
  - プロジェクトルートと共通ディレクトリをPythonパスに追加
  - lib/, src/, scripts/ ディレクトリを自動追加

- find_project_root(start_path=None, max_depth=6)
  - .git, package.json, requirements.txt等の指標からプロジェクトルートを自動検出
```

#### スクリプトでの必須使用パターン
```python
import sys
from pathlib import Path

# 共通ライブラリパスを追加（.claudeディレクトリを動的に探す）
def find_claude_lib():
    current = Path(__file__).resolve()
    for _ in range(8):  # 最大8階層まで遡る
        claude_lib = current / '.claude' / 'lib'
        if claude_lib.exists():
            return str(claude_lib)
        current = current.parent
        if current == current.parent:  # ファイルシステムルートに到達
            break
    return None  # 見つからない場合

claude_lib_path = find_claude_lib()
if claude_lib_path:
    sys.path.insert(0, claude_lib_path)
    from env_utils import setup_python_path, load_env_files

    # 初期化（必須）
    setup_python_path()
    load_env_files()
else:
    import warnings
    warnings.warn("Miyabi共通ライブラリが見つかりませんでした")
```

#### 探索対象の.envファイル階層
生成スキルのscripts/から以下の順で.envを探索:
1. `scripts/.env` (スキル固有)
2. カレントディレクトリ/.env
3. プロジェクトルート/.env (自動検出)
4. `.claude`ディレクトリが見つかった階層の.env (.claudeの親ディレクトリ)
5. 親階層を6階層まで遡って.envを探索

これにより、どのリポジトリに埋め込まれてもプロジェクトルートの.envを確実に読み込めます。

---

## フルオートスキル生成の再帰ループ構造

### 高レベルフロー

#### 【新規作成の場合】
1. **目的の理解・補完**
2. **スキル設計（リソース設計）**
3. **スキルの初期化（`init_skill.py`）**
4. **リソース実装（scripts/references/assets の埋め込み）**
5. **SKILL.md 実装**
6. **検証＆パッケージング（`quick_validate.py`, `package_skill.py`）**
7. **エラー・不足分の解析と再帰的改善**
8. **完成報告とハンドオフ**

#### 【更新の場合】
1. **既存スキルの解析**
   - 現在の構造と実装を調査
   - 最新方式との差分を特定
2. **差分の特定と優先順位付け**
   - 共通ライブラリ使用方式の更新
   - .env読み込み方式の改善
   - バリデーションルールへの準拠
3. **段階的な適用**
   - 破壊的変更を避ける段階的更新
   - 各ステップで動作確認
4. **検証とテスト**
   - `quick_validate.py`での構造検証
   - 既存機能の維持確認
5. **差分レポート作成**
   - 変更内容の明確な記録
   - 互換性情報の提供
6. **更新完了報告**

各ステップは「満足度チェック」と「再帰的な自己修正」を含む。
エージェントは**自分自身の出力を批評しながら次のステップを決める**。

---

## ステップ 0: モード判定（新規作成 vs 更新）

### モード判定フロー

ユーザーの入力を分析して、新規作成モードか更新モードかを判定する。

#### 新規作成モードの条件
- 「〜を作って」「〜スキルを作成」「新しい〜」などの表現
- 具体的な機能や要件の説明
- 既存のスキル名が指定されていない

#### 更新モードの条件
- 既存のスキル名が明示的に指定されている
  - 例: 「commit-prep-helperを更新して」「github-issue-improverスキルを修正して」
- 「更新」「アップデート」「修正」「改善」といったキーワード
- 「最新の方式に」「移植可能に」など既存技術の改善を示す表現

#### 判定が曖昧な場合
- ユーザーに明確化を求める：
  - 「新規にスキルを作成しますか？それとも既存のスキルを更新しますか？」
  - 「対象となる既存スキル名を教えてください」

---

## ステップ 1: 目的の理解・補完（再帰的質問ループ）

### 新規作成モードの場合

### 目標

- ユーザの1行要望を、スキル設計に使えるレベルまで**具体化**する。
- 不必要に質問し過ぎない。**最小限の質問**で決めきる。

### 更新モードの場合

### 目標

- 更新の**目的と範囲**を明確化する。
- 破壊的変更を避け、**差分のみ**を適用する。
- 既存機能の維持を確認する。

### 手順

1. **対象スキルの特定**:
   - スキル名の正確な特定
   - スキルの場所と現在の状態を確認

2. **更新目的の明確化**:
   - なぜ更新が必要か？（セキュリティ、移植性、機能追加など）
   - どの部分を更新したいか？
   - 期待される改善点は何か？

3. **制約の確認**:
   - 破壊的変更を許容するか？
   - 後方互換性は必須か？
   - 既存のAPIやインターフェースは維持するか？

### 更新パターンの例

- **共通ライブラリ対応**: 「最新の動的.env読み込み方式に対応させたい」
- **移植性向上**: 「どのリポジトリでも動くようにしたい」
- **セキュリティ強化**: 「最新のセキュリティ基準に合わせたい」
- **機能改善**: 「新しい機能を追加したい」

---

## ステップ 2: スキル設計（リソース設計の再帰）

### 目標

- 「このスキルフォルダには何を入れるか？」を決める。
- `scripts/`, `references/`, `assets/` 内の具体的な構造を設計する。

### 手順

1. 各ユースケースごとに以下を考える:
   - この処理を**毎回ゼロから書くとしたら**、どんなコードになるか？
   - その中で、**共通化したい部分**はどこか？
   - ドキュメント化すべき知識は何か？
   - 出力テンプレートやスタブファイルは必要か？

2. その結果から、以下を列挙する:
   - `scripts/` に入れるべきスクリプト
     - 名前
     - 役割
     - 想定する引数・I/O
   - `references/` に入れるべきドキュメント
     - 例: `schema.md`, `api_docs.md`, `workflows.md`, `output-patterns.md`
   - `assets/` に入れるべきテンプレ/静的ファイル
     - 例: HTMLテンプレ, PPTXテンプレ, サンプルコード一式

3. 設計を内省:
   - 不要に細かく分割しすぎていないか？
   - 逆に1ファイルに詰め込みすぎていないか？
   - ユーザの典型フローを1〜2本想定して、それをトレースしやすい構造になっているか？

4. 必要であれば、再度ユーザに確認・調整質問を行う。

---

## ステップ 3: スキルの初期化 (`init_skill.py` の自動利用)

### 目標

- 設計したスキルの骨組みを、`init_skill.py` を使って自動生成する。

### 操作（ローカルコマンド）

```bash
python skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

### エージェントの挙動

1. スキル名を正規化:
   - 小文字・ハイフン区切りで一意な名前を決める（例: `redshift-analytics-helper`）
2. 出力ディレクトリが既にあるかを確認し、競合があれば対処方針を決める:
   - 例: `<output-directory>/<skill-name>` が既にあれば、別名を案内するか、上書き可否を聞く。
3. コマンド実行結果を解析し、生成されたフォルダ構造をキャプチャする。

---

## ステップ 4: リソース実装（scripts / references / assets）

### 目標

- ステップ2の設計に従って、`scripts/`, `references/`, `assets/` を埋める。
- ここも再帰ループで、徐々に精度と網羅性を上げる。

### 一般方針

1. **最初はミニマル実装**から始める:
   - 各ユースケースを代表する1〜2本のスクリプト
   - 必須の schema / API docs / workflows のみ
   - 必須テンプレートのみ

2. その後、
   - quick_validate / package_skill のエラー
   - 内省（「このままだと使いづらい」など）
   に基づいてファイルを増やす。

### `scripts/` 実装ガイド

- 各スクリプトは「外部からも単体で動く」ように書く：
  - `if __name__ == "__main__":` を用いた CLI エントリ
  - 引数パースの簡易ラッパ（`argparse` 等）
- Claude が後からパッチしやすいように：
  - 単一ファイル内でロジックを整理
  - 関数レベルで責務を分離する（取得・変換・出力など）

- **【必須】共通ライブラリの使用**:
  ```python
  import sys
  from pathlib import Path

  # 共通ライブラリパスを追加（.claudeディレクトリを動的に探す）
  def find_claude_lib():
      current = Path(__file__).resolve()
      for _ in range(8):  # 最大8階層まで遡る
          claude_lib = current / '.claude' / 'lib'
          if claude_lib.exists():
              return str(claude_lib)
          current = current.parent
          if current == current.parent:  # ファイルシステムルートに到達
              break
      return None  # 見つからない場合

  claude_lib_path = find_claude_lib()
  if claude_lib_path:
      sys.path.insert(0, claude_lib_path)
      from env_utils import setup_python_path, load_env_files

      def main():
          # 環境初期化（必須）
          setup_python_path()
          load_env_files()

          # ここからスクリプト本体の処理
  else:
      import warnings
      warnings.warn("Miyabi共通ライブラリが見つかりませんでした")
  ```

- **.envファイルアクセスについて**:
  - 共通ライブラリにより自動的にプロジェクトルートの.envが読み込まれる
  - 追加の環境変数が必要な場合は `os.getenv()` でアクセス
  - スキル固有の設定は `スキルディレクトリ/.env` に配置可能
  - `.claude`ディレクトリがある階層が自動的に検出され、その親ディレクトリの.envも読み込まれる

### `references/` 実装ガイド

- できるだけ「構造化された Doc」として書く：
  - セクション見出し
  - テーブル形式（スキーマ／パラメータ一覧等）
  - 例／アンチパターン
- SKILL.md からのリンクを一段階に収める：
  - `SKILL.md` → `references/*.md`
    それ以上深くネストしない。

- **【推奨】共通ライブラリのドキュメント**:
  - `references/common_libraries.md` にMiyabi共通ライブラリの使用例を記載
  - 特に `env_utils.py` の具体的な使用方法をドキュメント化
  - スキル固有の環境設定パターンを明記

### `assets/` 実装ガイド

- 必要最小限のテンプレやサンプルのみ含める。
- 大きなバイナリや不要なサンプルは避ける。
- ファイル名は機能がわかるものにする（例: `report_template.pptx`, `hello-world-react/`）。

---

## ステップ 5: SKILL.md 実装（この AUTL スキル自身の応用）

### 目標

- 生成したスキルフォルダ用の `SKILL.md` を、
  - トリガ情報（frontmatter）
  - 使い方のワークフロー
  - `scripts/` / `references/` / `assets/` のナビゲーション
を備えた状態にする。

### ガイドライン（`skill-creator` の原則に加えた AUTL 視点）

1. **frontmatter の description は「いつ使うか」を必ず含める**
   - 例:

     ```yaml
     description: >
       社内Redshiftのイベントログとメトリクステーブルを分析して、
       日次/週次のKPIレポートを生成するためのスキル。
       「Redshiftのログから日次アクティブユーザを出して」などの集計・分析依頼に使う。
     ```

2. Body には以下を含める:
   - Quick start（最も典型的な1本のフロー）
   - 主要ユースケースごとのセクション
   - `scripts/` の使い方（どのスクリプトをいつ叩くか）
   - `references/` のリンクと参照タイミング
   - `assets/` の使い方（どのテンプレートをどのように適用するか）

3. **「これは人間用ではなく、エージェント用のマニュアルだ」という前提**で書く：
   - 命令形で書く（「〜せよ」「〜を行う」）
   - 迷う余地のあるところには選択ルールを書く（AならX, BならY）

---

## ステップ 6: 検証＆パッケージング（`quick_validate.py` / `package_skill.py`）

### quick_validate の利用

```bash
python skill-creator/scripts/quick_validate.py <path/to/skill-folder>
```

- 目的：
  - SKILL.md の frontmatter / 構造の検証
  - ディレクトリ構成・ファイル配置の確認
- エージェントはエラーメッセージを:
  - 分類（構文エラー / 命名規約違反 / 参照切れなど）
  - 優先度付け
  - 自動修正

### package_skill の利用

```bash
python skill-creator/scripts/package_skill.py <path/to/skill-folder> <optional-output-dir>
```

- 目的：
  - バリデーションを通過したスキルを `.skill` にパッケージング
  - `<skill-name>.skill` を生成してユーザに渡せる状態にする

---

## ステップ 7: 再帰的改善ループ

### トリガ

- quick_validate / package_skill のエラー
- 自己内省での違和感（例: 「このSKILL.mdだとトリガ条件が曖昧」）
- ユーザからのフィードバック（例: 「このスキルだと○○ができない」）

### 改善サイクル

1. 問題点の特定
   - どの層の問題か？
     - frontmatter / SKILL.md body / scripts / references / assets / 構造
2. 改善候補の列挙
   - 最小変更から順に3案程度
3. 影響範囲を評価
   - 既存ユースケースへの影響
   - 将来の拡張性
4. 一つの案を選び、変更を適用
5. 再度 quick_validate / package_skill を実行
6. 終了条件:
   - バリデーションが通り、主要ユースケースをカバーできている
   - description と実際の機能が整合している

---

## ステップ 8: 完成報告とハンドオフ

### エージェントがユーザに返すべき情報

- 生成された `.skill` ファイルのパス
- スキル名と簡単な説明
- 代表的な使い方（1〜3個）
- もしあれば、制約事項や今後の拡張候補

### 例（応答テンプレート）

> 次のスキルを自動生成し、`./dist/redshift-analytics-helper.skill` としてパッケージしました。
>
> - スキル名: `redshift-analytics-helper`
> - 機能概要: 社内Redshiftのイベントログ/メトリクステーブルから、日次・週次のKPIを集計し、Markdownレポートを生成します。
> - 主なユースケース:
>   - 日次アクティブユーザ / 週次アクティブユーザの算出
>   - 任意の期間のイベント回数・ユニークユーザ数の集計
>   - フラグメント化したクエリのテンプレを使った分析
>
> 詳細なワークフローやスキーマは SKILL 内の `SKILL.md` と `references/schema.md` に記載しています。

---

## この SKILL_AUTL.md 自体の利用方法（メタ）

- ユーザが「1行の要望」を投げたとき、
  - Claude / エージェントはまずこの SKILL_AUTL をトリガし、
  - ここに書かれた手順に沿って**自己誘導しながら**スキル生成プロセスを進める。
- 必要に応じて、
  - この SKILL_AUTL.md 自体を別のスキルとしてパッケージングし、
  - 「スキル自動生成スキル」として組織内で再利用することもできる。

---
