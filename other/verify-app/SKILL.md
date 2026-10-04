---
name: verify-app
description: 変更後の検証ループ — プロジェクトの lint・typecheck・test・build を実行し、失敗を修正して再実行する。実装完了の報告前、および commit・PR 作成前に必ず使用する。
---

# 🔁 verify-app — 変更後の検証ループ

実装を「書いただけ」で終わらせず、全チェック PASS まで 検出 → 修正 → 再実行 を
繰り返すための汎用検証ループです。

> 💡 このスキルは StartUpTools が配布する starter です。プロジェクト固有の
> チェック（毎回手で確認していること）を追記してカスタマイズしてください。
> 一度配布された後は上書きされないため、自由に編集できます。

## 🧭 Step 0: 検証コマンドの特定

1. `CLAUDE.md` に検証コマンドが明記されていれば**それを最優先で使う**
2. なければ manifest から推定する:
   - `package.json` の scripts（lint / typecheck / test / build）
   - `Makefile`、`pyproject.toml`、`go.mod` など言語標準の toolchain
3. 推定で実行した場合は、確定したコマンドを `CLAUDE.md` へ追記することを提案する
   （次回以降の推定コストと誤実行を防ぐ）

## ✅ Step 1-4: チェック実行（この順で）

| Step | チェック | 失敗時 |
|---|---|---|
| 1 | format / lint | 自動修正可能なものは修正して再実行 |
| 2 | typecheck | 型エラーの原因を修正して再実行 |
| 3 | test（変更範囲に比例した粒度） | 原因を特定し修正。テスト自体の誤りも疑う |
| 4 | build（production 相当） | 修正して再実行 |

## 🔁 ループ規則

1. 失敗したチェックは修正後、**該当チェックのみ**再実行する
2. 修正が広範囲に及んだ場合は Step 1 からやり直す
3. 同一チェックが 3 回の修正で解消しない場合は BLOCKED とし、原因分析と選択肢を報告して停止する
4. 環境・権限の問題で実行できないチェックは成功扱いにせず NOT RUN として理由を記載する
5. 既存の失敗（自分の変更と無関係と確認できたもの）は修正対象へ含めず、報告に明記する

## 📊 報告形式

```text
| チェック | 結果 | 備考 |
|---|---|---|
| lint | PASS | - |
| typecheck | PASS | - |
| test | FAIL→PASS | 境界値ケースを修正 |
| build | PASS | - |
```

## 🔗 チェーン連携（推奨運用）

- 実装系の作業が終わったら、完了報告の前にこのスキルを実行する（embedded）
- UI に影響する変更は続けて `/design-sync-check` を実行する（chained）
- PR マージ前の最終確認は `/safe-auto-merge` のゲート条件と組み合わせる

## 🛠️ プロジェクト固有チェックの追加方法

毎回手で確認していることがあれば、このファイルへ手順として追記する:

1. 今週最も頻繁に行った手動チェックを 1 つ選ぶ
2. 新しいチームメイトに渡すつもりで、手順を平易な文章で書き出す
3. このスキルの Step として追記する（例:「migration が column を drop する場合は backfill 手順を必須とする」）
4. 新しいタスクで発動させ、チェックが出力に含まれることを確認する
5. 安定したら独立スキル（`.claude/skills/<name>/SKILL.md`）へ分離し、チェーン化を検討する

参考: [Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)
