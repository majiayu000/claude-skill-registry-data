---
name: generate-db-schema
description: >
  VDM-SL仕様の型・不変条件・状態定義からデータベーススキーマ（DDL）を導出する。
  「仕様からDBスキーマを生成して」「テーブル設計をして」「DDLを作って」
  「不変条件をDB制約に変換して」「データモデルを設計して」「ER図のもとになる
  スキーマを作って」といったリクエストに使用する。
  English triggers: "generate a database schema from the spec", "derive tables from
  the VDM spec", "turn invariants into DB constraints", "design the data model".
  record型→テーブル、map→キー付きテーブル、不変条件→CHECK/UNIQUE/FK/トリガーの
  規則的な写像を適用し、DDLで表現しきれない乖離は DEVIATIONS.md（retrenchment表）に、
  各不変条件の担保箇所は TRACEABILITY.md に記録する。
metadata:
  version: "2.1.0"
  author: Formal Agent Contracts
  tags: [vdm-sl, database, schema-generation, ddl, retrenchment, traceability]
---

# DBスキーマ導出スキル (v2.1.0)

確定した VDM-SL 仕様（型定義・不変条件・状態定義・操作）から、データベーススキーマ（DDL）を**規則的に導出**するスキルです。設計判断を LLM の自由作文に任せるのではなく、番号付きの写像規則（R1〜R18、`references/vdm-to-sql-mapping.md`）を適用し、規則で写せない箇所は**乖離（deviation）として明示的に記録**します。

## 設計原理

このスキルは形式手法の**データ具体化（data reification）**の考え方に基づきます：

1. **導出できるものは機械的に導出する** — 抽象型→具体表現の対応は規則で決まる。LLM が「それらしいスキーマを推測」してはならない
2. **写せないものは隠さず記録する** — `nat`（無限）→ `BIGINT`（有限）のような忠実でない写像は retrenchment（譲歩）として DEVIATIONS.md に残し、その箇所にランタイム契約チェックとテストを集中させる
3. **すべての不変条件に担保箇所を与える** — 各 `inv` は「DB制約 / アプリ層チェック / 契約テスト」のいずれかで守られ、その対応を TRACEABILITY.md が示す。担保箇所のない不変条件が残ったら導出は未完成

## 成果物

| ファイル | 内容 |
|---|---|
| `db/schema.sql` | DDL（テーブル、型、CHECK/UNIQUE/FK 制約、トリガー、コメント） |
| `db/DEVIATIONS.md` | retrenchment 表：仕様と DB 表現の乖離と、その補償手段 |
| `db/TRACEABILITY.md` | 不変条件・契約 → 担保箇所（DB制約名 / アプリ層 / テスト）の対照表 |

## ステップ1：入力の解析

**目的**：VDM-SL 仕様から永続化対象を特定する

ユーザーに確認する情報：

- **仕様ファイル**：対象の `.vdmsl` ファイル（複数可）
- **永続化スコープ**：state 定義の全コンポーネントを永続化するか、一部か
  （例：`board : TaskBoard` は永続化、セッション的な一時状態は対象外）
- **既存スキーマ**：ゼロから作るか、既存 DB への追加か（追加ならマイグレーション形式で出力）

仕様から抽出する要素：

```
✓ 型定義: record型、quote型（列挙）、基本型の別名、合成型（map/set/seq/optional）
✓ 型不変条件: inv 節（値域、長さ、形式）
✓ state 定義: コンポーネント、状態不変条件、init
✓ 操作: atomic ブロック（トランザクション境界の候補）、事前・事後条件
```

## ステップ2：対象 DB と規約の確認

**目的**：方言と命名規約を固定する

- **DBMS**：PostgreSQL（デフォルト・最も表現力が高い）/ MySQL / SQLite。
  方言差は `references/vdm-to-sql-mapping.md` の各規則に併記
- **命名規約**：デフォルトは snake_case、テーブル名は複数形（`Task` → `tasks`）。
  VDM 名との対応は schema.sql のコメントに必ず残す
- **予約語回避**：`desc` → `description` 等。変換は TRACEABILITY.md に記録

## ステップ3：写像規則の適用

**目的**：`references/vdm-to-sql-mapping.md` の規則 R1〜R18 を順に適用する

主要規則の概要（詳細・方言差は参照文書）：

| 規則 | VDM-SL | DB 表現 |
|---|---|---|
| R1 | record 型 | テーブル（1フィールド=1カラム） |
| R2 | state の `map K to V` | V のテーブルに K を主キーとして埋め込む |
| R3 | quote 型の合併 `<A>\|<B>` | ENUM 型（PostgreSQL）/ VARCHAR + CHECK IN |
| R4 | `nat` / `nat1` / `int` / `bool` | BIGINT + CHECK / BOOLEAN ※整数は乖離 D-NUM |
| R5 | `seq of char` / `seq1 of char` | TEXT / TEXT + CHECK (length > 0)。inv に長さ上限があれば VARCHAR(n) |
| R6 | optional `[T]` | NULL 許容カラム |
| R7 | 単一値の型不変条件 | CHECK 制約 |
| R8 | map のキー一意性 | 主キー（構造として自動的に成立） |
| R9 | `inv board(id).id = id` 型（キー=フィールド） | 構造的に成立（フィールドを主キーに昇格）※記録のみ |
| R10 | エンティティ間参照の不変条件 | FOREIGN KEY |
| R11 | `forall` の一意性主張 | UNIQUE 制約 / 部分インデックス |
| R12 | **状態遷移規則**（`ValidTransition` 等） | UPDATE トリガー（OLD/NEW 比較）またはアプリ層 ※乖離 D-TRANS |
| R13 | 複数コンポーネントにまたがる状態不変条件 | トリガー / 遅延制約 / アプリ層 ※乖離 D-CROSS |
| R14 | `set of T` / `seq of T`（char 以外） | 結合テーブル（順序が要る seq は position カラム付き） |
| R15 | `atomic` ブロック・複数代入の操作 | トランザクション境界（BEGIN/COMMIT）としてコメントに明記 |
| R16 | `real` | DOUBLE PRECISION ※乖離 D-FLOAT。金額なら NUMERIC を対話で確認 |
| R17 | state の単一値コンポーネント（`nextId` 等） | シングルトン状態テーブル、または連番なら SEQUENCE/IDENTITY への置換を対話で確認 ※乖離 D-SEQ |
| R18 | `token` / 合成キー | サロゲートキー + UNIQUE、対話で確認 |

**適用の作法**：

- 各 DDL 要素には、**由来する VDM 要素を SQL コメントで記す**（例：`-- inv Task: len title <= 100 (R5/R7)`）
- 規則で写せない構文に出会ったら、推測せず**乖離として記録して先へ進む**
- 不明瞭な設計判断（NUMERIC か FLOAT か、SEQUENCE 置換の可否など）は**ユーザーに質問する**。規則にない独自判断をしない

## ステップ4：DEVIATIONS.md（retrenchment 表）の生成

**目的**：仕様と DB 表現の乖離をすべて列挙し、補償手段を割り当てる

形式：

```markdown
| ID | 仕様上の表現 | DB 表現 | 乖離の内容 | 補償手段 |
|----|------------|---------|-----------|---------|
| D-NUM-1 | TaskId = nat1（無限） | BIGINT（〜2^63-1） | 上限が有限 | 実用上到達不能。生成コードの契約チェックが nat1 を検査 |
| D-TRANS-1 | ValidTransition（Done から戻れない） | UPDATE トリガー | DDL の CHECK では表現不可 | トリガー + 契約テスト（遷移全パターン） |
```

**乖離の典型パターン**は `references/deviation-patterns.md` を参照。乖離には必ず ID を付け、
補償手段は「DB トリガー / アプリ層ランタイムチェック（generate-code の checkPre/checkInv） /
契約テスト（generate-tests）」のいずれかを具体的に指す。**「注意する」は補償手段ではない**。

## ステップ5：TRACEABILITY.md の生成

**目的**：すべての不変条件・契約に担保箇所を与える

```markdown
| 仕様要素 | 内容 | 担保箇所 | 種別 |
|---------|------|---------|------|
| inv Task (title) | len title <= 100 | tasks.title VARCHAR(100) + tasks_title_nonempty | DB制約 |
| inv TaskManagerState | forall id in dom board & id < nextId | trg_tasks_id_lt_next + trg_state_next_id_gt_tasks（両側） | DBトリガー |
| pre ChangeStatus | ValidTransition(from, to) | trg_tasks_status_transition + 契約テスト | DBトリガー+テスト |
| post CreateTask | RESULT = nextId~ | アプリ層 checkPost | アプリ層 |
```

**完成条件**：仕様中のすべての `inv`・操作契約が表に現れ、担保箇所が「なし」の行が存在しないこと。
担保できないものが残った場合は、ユーザーにその旨を明示して判断を仰ぐ（黙って省略しない）。

## ステップ6：検証

**目的**：生成したスキーマの実行可能性と仕様との整合を確認する

1. **DDL の実行検証**：
   - SQLite 方言を生成した場合：`sqlite3 :memory: < schema.sql` で即座に検証可能
   - PostgreSQL：利用可能なら `psql -f schema.sql` / Docker（`postgres` イメージ）で検証。
     不可能な環境では、その旨を報告して構文レビューに留める（検証したと偽らない）
2. **網羅性チェック**：ステップ1で抽出した型・state コンポーネントがすべて
   schema.sql / DEVIATIONS.md のどちらかに現れることを確認
3. **CHECK 制約と inv の整合（任意・smt-verify 連携）**：
   CHECK 制約の論理式が対応する inv を含意するか、乖離があるか（例：VARCHAR(100) は
   バイト長か文字長か）を smt-verify スキルで SMT-LIB に変換して Z3 で確認できる。
   自動での完全証明は保証しない — 確認できた範囲を正直に報告する

## ステップ7：次のステップ提案

```
提案：
1. generate-code — このスキーマに対応するデータアクセス層を生成
   （DEVIATIONS の補償手段「アプリ層」の checkPre/checkInv を実装）
2. generate-tests — DEVIATIONS の補償手段「契約テスト」を生成
   （DB制約のテスト：制約違反INSERTが拒否されることの確認を含む）
3. 将来の design-system スキル — このスキーマを含む全体アーキテクチャの設計
```

## 使用例（同梱サンプル）

`examples/task-manager/db/` に、`TaskManager.vdmsl` から本スキルの規則で導出した
実例一式（schema.sql / schema.sqlite.sql / DEVIATIONS.md / TRACEABILITY.md）があります。
SQLite 版は実行検証済みです。

## トラブルシューティング

### Q: 仕様に state 定義がなく、関数だけの仕様から何を永続化すべきか分からない
**A**: 永続化対象は原則 state 定義です。state がない仕様は永続データを持たない
（純粋な変換エージェント）可能性が高いので、本当に DB が必要かをユーザーに確認してください。

### Q: 不変条件が複雑すぎて CHECK にもトリガーにも写せない
**A**: 無理に写さず、乖離（補償手段=アプリ層+契約テスト）として記録してください。
DB で守る制約は「壊れたデータが永続化されない最後の砦」に絞り、
複雑な業務ルールはアプリ層の契約チェックに委ねるのが正しい分担です。

### Q: 既存 DB があり、スキーマを変えられない
**A**: 逆方向です — extract-spec で既存スキーマから暫定仕様を起こし、refine-spec で
磨いてから、本スキルの出力と既存スキーマの差分を DEVIATIONS として整理してください。

### Q: NoSQL（ドキュメントDB）に写したい
**A**: 本スキルの規則は関係モデル前提です。ドキュメント DB の場合、record の入れ子は
自然に写りますが、**不変条件の大半が DB 制約として表現できず**、ほぼすべてが
アプリ層補償になります。その trade-off を DEVIATIONS に明記した上で進めてください。

## 参考資料

- 写像規則の完全版：`references/vdm-to-sql-mapping.md`
- 乖離の典型パターン集：`references/deviation-patterns.md`
- 理論的背景：VDM のデータ具体化（reification）、retrenchment（Banach & Poppleton）、
  Event-B からの DB 導出（UB2DB）— `../formal-methods-guide/SKILL.md` も参照
- 仕様定義スキル：`../define-contract/SKILL.md`
- コード生成スキル：`../generate-code/SKILL.md`
- テスト生成スキル：`../generate-tests/SKILL.md`

---

**最終更新**: 2026-07-02  
**バージョン**: 2.1.0  
**メンテナ**: Formal Agent Contracts チーム
