---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: コードベースの規模に応じた目標値計算、倍増エスカレーション、領域追跡、最終検証を備えた体系的なバグスウィープ。/bugsweep 実行時や体系的なバグ調査が要求された場合に使用します。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="bugsweep banner">

> **日本語** — `bugsweep` の公式日本語版。


# /bugsweep — 体系的なバグスウィープワークフロー (日本語)

収束停止条件を備えた反復的なバグハンティング。コードベースの規模に応じてスケールし、検索が表面的と判断された場合にエスカレートし、領域追跡によって重複を防ぎます。

## 1. 基準レート (base_rate) の計算

```
LOC = productive source lines (src/, lib/ — excluding tests, configs, docs, generated)
x = max(1, ceil(LOC / 1500))
base_rate = x * 3
```

| LOC | x | 基準レート (Base rate) |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

ユーザーへの報告: "コードベース: {LOC} LOC → 基準レート = {base_rate} 回のクリーンな検索パス。"

## 2. 検索ループ

```
counter = 0
target = base_rate
any_bug_found = False
checked = []  # (area_name, type: code|task)

LOOP:
  area = pick_new_area()  # see area rules
  checked.append(area)

  Perform a thorough bug search

  IF bug found:
    any_bug_found = True
    Fix following bugfix-protocol (phases 4+5)
    Review: see model rule (newer model classes: no external review needed)
    Commit + push
    counter = 0  # RESET
  ELSE:
    counter += 1
    Report: "✓ Clean: {area} — {counter}/{target}"

  IF counter >= target:
    IF NOT any_bug_found:
      # Doubling escalation: not a single bug → search too shallow?
      target = base_rate * 2
      any_bug_found = True  # escalate only ONCE
      Report: "⚠ No bug in {base_rate} passes → target doubled to {target}."
      CONTINUE LOOP
    ELSE:
      GOTO final verification
```

### 検索ループに関する実践的なメモ (実際のスイープからの学び)

- **non-git リポジトリ:** `git` が存在しない環境 (例: クラウド同期されたプロジェクトフォルダ) では、"commit + push" の代わりに**バージョン管理されたバックアップ**を使用します。最初の修正前に `file_<ts>.bak` を作成します。**注意 — 修正前のバックアップは作業成果のバックアップではありません:** 最後の修正後、新たな `_FINAL_` バックアップを取得してください。そうしないと、同期の不具合により修正セッション全体が消失する可能性があります。
- **事前に多数のバグが判明している場合:** 開始時点ですでに N 個のバグが判明している場合 (例: 前回の実行から)、"バグごと: 修正 → レビュー → コミット → リセット" は非効率的です。判明しているバグを 1 つの修正ブロックとして処理し (最後にまとめてレビュー)、**新しく発見された**最初のバグから基準レート / 検索ループのカウントを開始します。リセット論理はスイープ中に新しく見つかったバグに引き続き適用されます。
- **複数の場所に存在する同じバグ:** 発見された欠陥 (例: 誤った正規表現、壊れたフォーマットの前提) は、他の場所にもコピーされていることがよくあります。各修正後、他の場所で同じパターンを検索してください — これは独立した「領域」として価値があります。

## 3. 領域ルール (手抜き防止)

「領域」とは、**コードのフォーカス**または**タスク** (コードの目的) のいずれかです。

### コードのフォーカス
- パス間で**拡張** (ファイルを追加) または**移動** (別の部分) することができます
- 過去のパスと完全に同じ選択であってはなりません
- OK: パス 1 = `maintenance.py`、パス 5 = `maintenance.py + orchestrator.py` (拡張)
- NG: パス 1 = `maintenance.py`、パス 5 = `maintenance.py` (同一)

### タスク (目的)
- **より詳細** (サブ関数の確認) にする、または**より広範** (関連機能をまとめる) にすることができます
- 過去と完全に同じタスクであってはなりません
- OK: パス 1 = "ウォッチドッグ内のスレッドセーフ"、パス 5 = "トレイ全体におけるスレッドセーフ" (広範)
- OK: パス 1 = "プロセス検出"、パス 5 = "プロセス検出内のストアマーカーマッチング" (より詳細)
- NG: パス 1 = "ウォッチドッグ内のスレッドセーフ"、パス 5 = "ウォッチドッグ内のスレッドセーフ" (同一)

### 命名
- 領域は検索**前**に命名されなければなりません (後付け指定は不可)
- フォーマット: `"{name}" ({type}: code|task)`

## 4. 最終検証

counter >= target かつ any_bug_found の場合:

**ステップ A — bugfix-protocol フェーズ 5:**
- [ ] フルテストスイートがパス (`pytest`)
- [ ] **変更された実行パスを実際に少なくとも1回実行する** — 単にテストを通すだけでなく。変更箇所を一度も呼び出さないコードでのユニットテスト成功は偽りの安全です。実際に変更されたパスを実行し (ドライラン、スモークラン、CLI 呼び出し)、トレースバック、シグネチャ、命名エラーがないか確認します。`py_compile` や単なる import は構文をチェックするだけで、パスが正常に実行されるかは確認できません。
- [ ] **すべての修正に、それを実行するテストが少なくとも1つ存在する** — 変更されたブランチを実際にトリガーするテストがない修正は未検証とみなされます (オーケストレーション/ネットワークパスの場合、必要に応じてモック + ドライランを組み合わせます)。
- [ ] 型チェック (設定されている場合)
- [ ] リンター (設定されている場合)
- [ ] セッション中の修正の境界値ケースの確認

**ステップ B — レビュー (モデルルール):**
- **より新しいモデルクラス (例: Claude 5 / Fable クラス):** 外部アドバイザーや第2モデルによるレビューは不要です。ステップ A (テスト + 実際のスモークラン) が検証となります。真に不確実な場合は、オプションとして新しいレビューサブエージェントを使用できますが、バグとしてカウントする前に empirical (未変更のコードに対してテスト) にその指摘を検証してください。背景 (2026-06-11 のスイープ経験): 第2レビュアーが利用不可で、代替サブエージェントが 1 つの指摘 (確信度 85) を提示しましたが、テストによりバグではないことが証明されました — 外部レビューは結果に影響を与えませんでした。
- **古いモデル:** アドバイザーとの最終議論 (フォールバック: レビュアーとしての第2モデル); アドバイザーが確認または抜け漏れを指摘します。

**検証中にバグが見つかった場合:**
→ 修正 + テスト + コミット
→ リセット: counter = 0, target = base_rate (フレッシュな基準レート、倍増なし)
→ 検索ループに戻る (チェック済みリスト checked は維持、any_bug_found = True)

**検証がクリーンな場合:**
→ 完了。Commit + push。プロトコルを出力します。

## 5. プロトコル (終了時)

```markdown
## Bug Sweep Result

- **Codebase:** {LOC} LOC
- **Base rate:** {base_rate} (escalated: {target})
- **Areas checked:** {len(checked)}
- **Bugs found:** {count}
- **Resets:** {reset_count}
- **Doubling triggered:** yes/no
- **Fixes:**
  - {title} — {commit_hash}
  - ...
- **Final test suite:** {passed}/{total} green
- **Review verdict:** self-verification (newer model class) / advisor confirmed / gaps named
```

## このワークフローを使用するタイミング

- 機能開発後 (品質保証)
- リリース前 (受入スイープ)
- 定期的な衛生チェックとして
- ユーザーが `/bugsweep` と入力したとき

## 他のスキルとの連携

- **bugfix-protocol:** 発見された各バグの修正手順 (フェーズ 4+5)
- **systematic-debugging:** スイープ内での再現困難なバグ用
- **code-review:** タスク領域として使用可能

---

## 変更履歴

### 1.1.0 (2026-06-13)
- ステップ B のモデルルールをバックポート (ローカルスキルインストール、2026-06-11 時点より): より新しいモデルクラスはテスト + 実際のスモークランによりセルフ検証を行い、外部レビューは不要。これに伴いプロトコル項目 "Review verdict" を拡張

### 1.0.0 (2026-06-13)
- スキルライブラリへの最初の公開 (ローカルスキルインストール、2026-06-01 時点より採用)
