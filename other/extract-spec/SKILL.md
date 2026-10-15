---
name: extract-spec
description: >
  Extract a provisional VDM-SL specification from existing source code.
  This is NOT the true spec — it is a scaffold for dialogue to uncover the user's real intent.
  Triggered by: "extract spec from code", "reverse engineer the specification",
  "extract-spec", "code to spec", "formalize the existing code".
  Japanese: 「既存のコードから仕様を抽出して」「コードの仕様を形式化して」
  「コードベースを分析して」「コードをリバースエンジニアリングして」
metadata:
  version: "1.1.0"
---

# Extracting Provisional VDM-SL Specifications from Source Code

Extract structural and behavioral information from existing code and generate a PROVISIONAL
VDM-SL specification as a starting point for dialogue with the user.

**Critical principle:** The spec extracted from code is NOT the true spec. It is a provisional
scaffold for dialogue. The true spec exists in the user's head. Every extracted item must be
tagged `[PROVISIONAL]` and framed as a question, not a statement.

<!-- 日本語 -->

既存のコードから構造情報と動作情報を抽出し、ユーザーとの対話の出発点となる
暫定的なVDM-SL仕様を生成する。

**重要な原則:** コードから抽出した仕様は「真の仕様」ではない。それはあくまで対話のための
暫定的な足がかりである。真の仕様はユーザーの頭の中に存在する。抽出した全ての項目には
`[PROVISIONAL]`というタグをつけ、陳述ではなく質問として表現する。

## Dialogue Flow

### Step 1: Scope Identification

Ask the user which files or directories to analyze.

Questions to guide the scope:
1. Which files or directories should I analyze?
2. Are there entry points (main functions, API endpoints)?
3. Are there any main modules or key classes I should focus on?
4. Are there tests, documentation, or comments that explain the behavior?

<!-- 日本語 -->

ユーザーに、どのファイルまたはディレクトリを分析するかを質問する。

スコープを確定するための質問:
1. どのファイルまたはディレクトリを分析すべきか？
2. エントリーポイント（メイン関数、APIエンドポイント）はあるか？
3. 注目すべきメインモジュールやキークラスはあるか？
4. 動作を説明するテスト、ドキュメント、またはコメントはあるか？

### Step 2: Structural Analysis

Read the code and extract candidates for:

**Data Types**
- Classes, interfaces, structs, dataclasses → VDM-SL record type candidates
- Enums → quote union candidates
- Optional/nullable types → optional type `[T]` candidates
- Union types → VDM-SL union type candidates
- Collections (arrays, lists, sets, maps) → sequence/set/map type candidates

**Functions and Operations**
- Function/method signatures → VDM-SL function/operation candidates
- Parameters and return types → type mappings
- State mutations (if any) → operation vs. function classification

**Constraints and Validation Logic**
- If-guards, assertions, validation functions → pre-condition candidates
- Return value patterns and state postconditions → post-condition candidates
- Invariants, decorators, schema validators → invariant candidates
- Test assertions → implicit specification evidence

<!-- 日本語 -->

コードを読み込み、以下の候補を抽出する：

**データ型**
- クラス、インターフェース、構造体、データクラス → VDM-SLレコード型の候補
- 列挙型 → クォート合併型の候補
- オプション型/nullable型 → オプション型 `[T]` の候補
- 合併型 → VDM-SL合併型の候補
- コレクション（配列、リスト、集合、辞書） → sequence/set/map型の候補

**関数と操作**
- 関数/メソッドのシグネチャ → VDM-SL関数/操作の候補
- パラメータと戻り値の型 → 型マッピング
- 状態変更（ある場合） → 操作 vs. 関数の分類

**制約と検証ロジック**
- if-ガード、assertions、検証関数 → 事前条件の候補
- 戻り値パターンと状態の事後条件 → 事後条件の候補
- 不変条件、デコレータ、スキーマバリデーター → 不変条件の候補
- テストのassertions → 暗黙的な仕様の証拠

### Step 3: Provisional VDM-SL Generation

Convert extracted information to VDM-SL using the mapping rules in
`references/code-to-vdmsl-mapping.md`.

**Tagging Requirements:**
Every extracted line MUST be tagged with one of:
- `[PROVISIONAL]` — mechanically extracted from code, unconfirmed by user
- `[QUESTION]` — code behavior is questionable or ambiguous, user must confirm
- `[IMPLICIT]` — inferred from tests/comments/patterns, not explicitly in code
- `[MISSING]` — no corresponding code found, may need to be defined by user

**Output format:**
- File extension: `.provisional.vdmsl`
- Include source code reference for each extracted item (line numbers, function names)
- Comment each extraction with its provenance

Example:
```vdmsl
-- [PROVISIONAL] Extracted from classes/user.ts lines 5-20
-- QUESTION: Is the email validation rule exactly as shown in the code?
types
  Email = seq1 of char
  inv email == email_valid(email)
```

<!-- 日本語 -->

`references/code-to-vdmsl-mapping.md` の変換ルールを使用して、抽出した情報を
VDM-SLに変換する。

**タグ付けの要件:**
抽出した全ての行には、以下のいずれかをタグとして付ける必要がある：
- `[PROVISIONAL]` — コードから機械的に抽出、ユーザーにより未確認
- `[QUESTION]` — コードの動作が疑わしい、またはあいまい。ユーザーが確認する必要がある
- `[IMPLICIT]` — テスト/コメント/パターンから推論されたもの。コードに明示的にはない
- `[MISSING]` — 対応するコードが見つからない。ユーザーが定義する必要があるかもしれない

**出力形式:**
- ファイル拡張子: `.provisional.vdmsl`
- 抽出した各項目のコード参照（行番号、関数名）を含める
- 各抽出に出典コメントを付ける

例:
```vdmsl
-- [PROVISIONAL] classes/user.ts lines 5-20から抽出
-- QUESTION: メール検証ルールはコードに示されているとおりですか？
types
  Email = seq1 of char
  inv email == email_valid(email)
```

### Step 4: Uncertainty Identification

List all ambiguous or unclear points as "Questions for User".

**Categorization:**
- `[UNCLEAR]` — Code intent is unclear or ambiguous
- `[AMBIGUOUS]` — Multiple interpretations are possible
- `[IMPLICIT]` — Specification exists in tests or comments, not code
- `[MISSING]` — Feature appears in tests but not in implementation

Each question should present:
1. What the code appears to do
2. Why it's unclear or ambiguous
3. What the options are (if any)

Example:
```
[UNCLEAR] Type of `status` field in User class
Code:
  class User { status: string }
Question:
  - Is `status` constrained to specific values (e.g., "active", "inactive")?
  - Should we define an enumeration?
  - Or is any string value allowed?
Options:
  - Quote union: Status = <ACTIVE> | <INACTIVE> | <PENDING>
  - String with invariant: inv s == s in ["active", "inactive", "pending"]
  - Unconstrained: seq1 of char
```

<!-- 日本語 -->

あいまいまたは不明瞭なポイントを全て「ユーザーへの質問」としてリストアップする。

**分類:**
- `[UNCLEAR]` — コードの意図が不明瞭またはあいまい
- `[AMBIGUOUS]` — 複数の解釈が可能
- `[IMPLICIT]` — テストまたはコメントに仕様が存在。コードにはない
- `[MISSING]` — テストに表れているが実装されていない機能

各質問には以下を含める:
1. コードが何をしているように見えるか
2. なぜそれが不明瞭またはあいまいなのか
3. 何か選択肢があれば、その選択肢は何か

例:
```
[UNCLEAR] Userクラスの `status` フィールドの型
コード:
  class User { status: string }
質問:
  - `status` は特定の値（例："active"、"inactive"）に制限されているか？
  - 列挙型を定義すべきか？
  - それとも、任意の文字列値が許容されるのか？
オプション:
  - クォート合併型: Status = <ACTIVE> | <INACTIVE> | <PENDING>
  - 不変条件を持つ文字列: inv s == s in ["active", "inactive", "pending"]
  - 制約なし: seq1 of char
```

### Step 5: Extraction Report

Produce a summary report covering:

1. **What was extracted**
   - Types found, operations found, pre/post/invariant candidates
   - Count of each category

2. **What wasn't extracted**
   - Missing constraints, unclear behavior, implicit specifications

3. **Confidence levels**
   - High: Clearly stated in code
   - Medium: Inferred from patterns, tests, or comments
   - Low: Ambiguous or conflicting evidence

4. **Next steps**
   - Explicit statement: "This is a provisional spec. Proceed to refine-spec for dialogue."
   - Recommend addressing unclear items first

<!-- 日本語 -->

以下を含む概要レポートを生成する:

1. **抽出したもの**
   - 見つかった型、操作、事前/事後条件/不変条件の候補
   - 各カテゴリの数

2. **抽出されなかったもの**
   - 欠落した制約、不明瞭な動作、暗黙的な仕様

3. **信頼水準**
   - 高: コードに明確に記述されている
   - 中: パターン、テスト、またはコメントから推論された
   - 低: あいまいまたは矛盾する証拠

4. **次のステップ**
   - 明示的な声明: 「これは暫定的な仕様です。refine-specに進んで対話してください。」
   - 不明瞭な項目を最初に扱うことを推奨

## Important Notes

### Framing as Questions, Not Statements

Never present extracted specifications as confirmed facts. Always frame them as questions.

WRONG: "The User type has a required email field of type string."
RIGHT: "[PROVISIONAL] Does the User type require an email field of type string?"

WRONG: "The updateUser operation takes a user ID and returns a boolean indicating success."
RIGHT: "[QUESTION] Does the updateUser operation take a user ID and return a boolean (true=success, false=fail)?"

<!-- 日本語 -->

### 質問として表現する、陳述ではなく

抽出した仕様を確認された事実として提示してはいけない。常に質問として表現する。

悪い例: 「Userタイプには、型stringの必須メールフィールドがある。」
良い例: 「[PROVISIONAL] Userタイプに、型stringのメールフィールドが必須か？」

悪い例: 「updateUser操作は、ユーザーIDを受け取り、成功を示すブール値を返す。」
良い例: 「[QUESTION] updateUser操作は、ユーザーIDを受け取り、ブール値（true=成功、false=失敗）を返すか？」

### Bugs in Code Become Bugs in the Provisional Spec

If the code contains a logic bug, the extracted spec will reflect that bug. Inform the user:

"Note: The provisional spec reflects what the code currently does, not necessarily what
it *should* do. If you notice discrepancies between the spec and intended behavior,
those may indicate bugs in the code that should be fixed."

<!-- 日本語 -->

### コードのバグは暫定仕様のバグになる

コードにロジックバグが含まれている場合、抽出した仕様もそのバグを反映する。
ユーザーに以下を伝える:

「注意: 暫定仕様は、コードが現在やっていることを反映しており、
それが*すべきこと*とは限りません。仕様と意図された動作の間に
矛盾に気づいた場合、それはコードの中のバグを示している可能性があり、
修正すべきです。」

### Always Proceed to Refine-Spec

After extraction is complete, strongly recommend proceeding to the refine-spec skill
for dialogue with the user. The refine-spec skill is designed to:
- Clarify ambiguities by asking targeted questions
- Confirm implicit specifications
- Identify missing constraints
- Build consensus on the true specification

<!-- 日本語 -->

### 常にrefine-specに進む

抽出が完了したら、ユーザーとの対話のためにrefine-specスキルに進むことを
強く推奨する。refine-specスキルは以下のように設計されている:
- ターゲットとした質問をすることであいまいさを明確にする
- 暗黙的な仕様を確認する
- 欠落した制約を識別する
- 真の仕様に関するコンセンサスを構築する

### Reference Documentation

For detailed code-to-VDM-SL mapping rules, see `references/code-to-vdmsl-mapping.md`.

For VDM-SL syntax and formal methods concepts, refer to the formal-methods-guide skill.

<!-- 日本語 -->

### 参照ドキュメント

詳細なコードからVDM-SLへのマッピングルールについては、
`references/code-to-vdmsl-mapping.md` を参照してください。

VDM-SLの文法と形式手法の概念については、formal-methods-guideスキルを
参照してください。
