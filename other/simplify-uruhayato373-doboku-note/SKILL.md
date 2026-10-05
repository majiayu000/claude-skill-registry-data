---
name: simplify
description: >
  変更中のコード（git diff）を読んで、再利用可能な既存コードの見落とし・過剰設計・無関係な編集・非効率な実装を列挙し、ユーザ承認の上で最小差分で修正する。
  Use when user asks to [シンプル化, 簡素化, リファクタ, 冗長を削って, /simplify, simplify].
user-invocable: true
domain: ops
---

変更中のコード（git diff）を対象に、**再利用 / 品質 / 効率** の3観点で問題を洗い出し、**ユーザ承認後に最小差分で修正する** Evaluator + Generator。

## 用途

- LLM 生成直後のコードに典型的な問題（勝手な抽象化・車輪の再発明・無関係な整形）を最終段で潰す
- PR 作成前の最後のクリーンアップとして呼ぶ
- ハーネス設計原則「Generator と Evaluator を分離」「シンプルさ最優先」の実装レベルでの自動化

## 引数

```
/simplify [target ...]
```

- **`target` 省略時**: `git diff --name-only HEAD` の変更ファイルを対象
- **ファイルパス**: 単一ファイル
- **ディレクトリパス**: 配下の変更ファイル（git diff に含まれるもののみ）

## 実行手順

### Step 1: 対象 diff の収集

- `git diff HEAD --unified=10 -- {target...}` で変更を取得
- diff が空なら「変更なし」と報告して終了
- バイナリ・画像・`*.json` のロックファイルは除外

### Step 2: 3観点で問題点を列挙（修正はまだしない）

以下の観点でそれぞれ issue を抽出する。**重要度は HIGH / MEDIUM / LOW** で付ける。

#### 2-A. 再利用の見落とし（Reuse）
- プロジェクト内に既存のユーティリティがあるのに新規実装している
  - 例: `.claude/scripts/lib/mdx-io.mjs` の `readMdxFile` / `writeMdxFile` を使わず、直接 `readFileSync` / `writeFileSync` を呼んでいる → **HIGH**（CRLF 事故の再発リスク）
  - 例: `src/lib/docs.ts` の `preprocessMDX` と同等の正規表現を別ファイルで再実装
- グローバルな探索（Grep）で類似関数を確認してから指摘する

#### 2-B. 品質（Quality）
- **CLAUDE.md 違反**:
  - 装飾絵文字を本文に使用（❌✅💡等）→ **HIGH**
  - 4列以上の表・キーバリュー表 → **MEDIUM**
  - `border-gray-*` に `dark:border-*` が無い → **HIGH**
  - 生の `rounded-lg` / `shadow-md` 使用（デザイントークン無視）→ **MEDIUM**
- **勝手な仮定・過剰設計**:
  - 依頼されていない機能追加 → **MEDIUM**
  - 1 回しか使わないコードの抽象化 → **MEDIUM**
  - 起こり得ないエラーハンドリング → **LOW**

#### 2-C. 効率（Efficiency）
- 同じファイルを複数回読む・同じ正規表現を複数回 new する → **LOW**
- 並列化可能な独立ループを順次実行 → **LOW**
- 無関係な編集（依頼対象外のフォーマット変更・リネーム）→ **MEDIUM**

### Step 3: ユーザに提示して承認を得る

以下のフォーマットで出力し、**必ず確認を取ってから修正を開始する**:

```
=== /simplify: N files ===

<ファイルパス1>
  [HIGH] L42: readFileSync を直接呼んでいる
    → .claude/scripts/lib/mdx-io.mjs の writeMdxFile を使うべき
    （CRLF 保持が壊れて 100+ ファイル reject の事故歴あり）
  [MEDIUM] L58: 4列の比較表
    → 散文化 or 2軸比較に分割

<ファイルパス2>
  [HIGH] L12: border-gray-200 に dark:border 指定なし
    → `dark:border-gray-700` を追加

=== Summary ===
HIGH: 2 / MEDIUM: 1 / LOW: 0
修正を適用しますか？ (yes / no / HIGH のみ / 個別選択)
```

### Step 4: 承認後に最小差分で修正

- **ユーザが承認した issue のみ** 修正する
- 1 修正 = 1 Edit（まとめ差分にしない。レビューしやすさ優先）
- 無関係な整形・リネームはしない（Step 2-C で指摘したなら、その修正のみ）
- 修正後に `git diff --stat` を報告

### Step 5: 検証チェーン（pre-commit 相当）

Step 4 の修正後、自動で以下を実行して結果を報告する。**失敗したら次に進まない**。

1. **UI 変更があるなら `node scripts/lint-ui.mjs`** を走らせる（ステージ対象ではなく修正ファイルに対して）
2. **MDX 変更があるなら `node scripts/pre-commit-mdx.mjs`** を走らせる（staged ではなく修正ファイル対象の軽量検証）
3. **src/lib や .claude/scripts/lib の変更があるなら `npm test`** を走らせる
4. **type-check 変更影響が疑わしければ `npm run type-check`**（.tsx / .ts 変更があれば必ず走らせる）

全部 OK なら Step 6 へ。fail したら内容を報告してユーザに判断を委ねる（本スキルは修正まではしない）。

### Step 6: `/pr-create` 呼出確認

以下のプロンプトを出してユーザに選ばせる:

```
修正 + 検証 OK。次のアクションを選んでください:
  1. /pr-create           ── 現ブランチから PR を作成
  2. commit のみ           ── 変更をステージ済みまでに留める
  3. 何もしない            ── 終了

選択 (1/2/3):
```

選択 1: `/pr-create` を呼び出す（title / body の草案生成まで本スキルで行い、最終承認は `/pr-create` 内で）
選択 2: ユーザが手動で commit するよう案内して終了
選択 3: 「/simplify 完了」と報告して終了

**重要**: hook ではなくスキル内でチェーン化しているため、ユーザが `/simplify` を明示的に叩いた時のみ Step 5-6 が走る。自動発火はしない（CLAUDE.md §1「確認を挟むのは解釈の違いで成果物が大きく変わるときだけ」を守るため）。

## 出力フォーマット（省略版）

**検出は常に全件行う。絞るのは表示だけ**（検出段階で落とすと見逃しになる）。

10ファイル以上 or issue 20件超のとき:
- 会話にはファイル別の件数サマリ＋重大度上位のみを表示
- **全件は `.tmp/simplify-<対象>.md` に書き出してパスを明示する**（黙って省略しない）
- 詳細は「特定ファイルで `/simplify <path>` を再実行してください」と案内

## 例

### 例 1: scripts で直接 writeFileSync を使用

```
scripts/backfill-category.mjs
  [HIGH] L24: writeFileSync を直接呼んでいる
    → .claude/scripts/lib/mdx-io.mjs の transformMdxFile を使う
    （CLAUDE.md の MDX 書き込み規約、CRLF 保持）
```

### 例 2: 依頼以外の整形変更が混入

```
src/components/ui/Callout/Callout.tsx
  [MEDIUM] L1-5: import 順のみの変更（依頼範囲外）
    → 削除して diff を最小に
```

## アンチパターン

- **承認を得る前に修正を始めない** ── Step 3 のユーザ確認は必須
- **無関係な dead code を勝手に消さない** ── 指摘のみ、削除は別タスクで依頼
- **diff の外を触らない** ── 「ついでに」の周辺改善は禁止
- **重大度を過大評価しない** ── HIGH は「事故歴あり」「CLAUDE.md 明示違反」に限定
- **既存のユーティリティ有無を Grep で確認せずに「既存あり」と主張しない** ── 確認手順を省略するとハルシネーションになる

## 参照

- `CLAUDE.md` ── 「12 原則」（§1-§4 が実装の行動原則・§5 がハーネス設計原則）
- `.claude/knowledge/reference/content-authoring.md` ── MDX コンポーネント・frontmatter 規約
- `.claude/skills/dev/code-review/SKILL.md` ── コード品質レビュー（観点が重複するため、/simplify は「修正提案型」、/code-review は「批判型」と使い分け）
- `.claude/skills/dev/pr-create/SKILL.md` ── Step 6 で呼び出す PR 作成スキル
- `scripts/lint-ui.mjs` ── UI 静的 lint（Step 5-1 で呼ぶ）
- `scripts/pre-commit-mdx.mjs` ── MDX pre-commit 検証（Step 5-2 で呼ぶ）
