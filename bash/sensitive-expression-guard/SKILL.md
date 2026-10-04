---
name: sensitive-expression-guard
version: 1.0.0
description: 章の執筆・改訂完了時・原稿ビルド前に、センシティブ表現（絶対量詞・欠陥モデル語彙・著者誤認リスクの共起・アブストラクト語彙ポリシー・非診断宣言の存在）を check_sensitive_expression.py で機械検査し、あわせて LLM による「浅く読む敵対的読者」シミュレーションで意味レベルの短絡リスクを発見し、判断を sensitive-expressions.yml に蓄積するスキル。自己言及ケースを含む DSR 論文で特に重要
---

# センシティブ表現ガードスキル (Sensitive Expression Guard)

## 目的
DSR 論文、とりわけ**著者自身の実践を分析対象とする自己言及ケース**では、症状隣接の語彙（診断・スペクトラム・過集中等）が著者の医学的状態の誤認を招きやすく、修辞的な絶対表現（無尽蔵等）が宣言済みの主張強度（Modality）を超過しやすい。読者の一部は逆接の前節を読み飛ばし、キーワードだけで短絡する。本スキルは次の**三層**でこのリスクに対処する。

1. **機械層（再発防止）**: `scripts/check_sensitive_expression.py` が登録ルールを検査する。`banned_terms`（著者確定の禁止表現）の再出現のみ FAIL、それ以外は WARN
2. **LLM 層（意味的発見）**: 機械は登録語と文レベルの共起しか見ない。エージェントが「浅く読む敵対的読者（careless reader）」をシミュレートし、比喩レベルの誇張・逆接の読み飛ばし・SNS での切り出し耐性を意味的に点検する
3. **蓄積層（学習）**: 著者の判断（修正・allowlist・banned 登録）を `design/sot/sensitive-expressions.yml` に理由付きで蓄積し、機械層に還元する

## 発動タイミング
- 章ファイルの執筆・改訂を完了した時（機械層は必須）
- `assemble_manuscript.py` が FAIL でビルドを中断した時
- 投稿前ゲートで `sensitive-expression` が WARN/FAIL を返した時
- 著者が表現のリスク（誤認・大げさ・欠陥モデル語彙）を指摘した時（LLM 層レビュー＋蓄積）

## 原則
- **FAIL（banned 再出現）は常にブロック**: 著者が一度較正した表現の回帰であり、「対応不要」には分類しない
- **WARN は意図確認**: 否定文・言及（「」内）・引用文はスクリプトが免除済み。残った WARN は著者がトリアージする
- **共起ルールの解釈**: `misidentify` は「医学化語彙 × 著者自己言及 が同段落」で発火する。同段落に非診断宣言パターンがあれば免除される。ペア定義が別章にあるだけでは免除されないことに注意（浅い読者は章を単独で読みうる）
- **アブストラクトは別レジスタ**: `abstract_flagged` の語は本文ではペア定義付きで許容されても、アブストラクト（`paper-outline.md` の `## 1.` 節）では WARN。要約では医学的連想を持つ語を絞る方針を制度化したもの
- **存在チェック**: 医学化語彙を1語でも使う論文には、非診断カテゴリ宣言（「診断の有無を問わない」等）の一文が必須。悪い語の不在だけでは不十分

## 処理手順

```text
[Step 1: 機械スキャン] ➔ [Step 2: 既知パターン照合・トリアージ] ➔ [Step 3: LLM 敵対的読者レビュー] ➔ [Step 4: 著者判定 ➔ yml 蓄積]
```

### Step 1: 機械スキャン

```bash
# 全章（アブストラクト節は paper-outline.md から自動抽出され別レジスタで検査）
python3 scripts/check_sensitive_expression.py docs/<paper-id>/chapters
# 単一章
python3 scripts/check_sensitive_expression.py docs/<paper-id>/chapters/<file>.md
```

### Step 2: 検出項目の既知パターン照合

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| `FAIL/banned`（禁止表現の再出現） | 要修正 | 著者確定の較正済み表現への回帰。例外は認めない |
| `WARN/absolute`（絶対・無限量詞） | 要確認 | 検証可能な範囲の表現へ較正。否定文・言及は免除済み |
| `WARN/quantifier`（定性量詞・引用なし） | 要確認 | 引用を添えるか存在主語化。「少なくない→存在する」型 |
| `WARN/modality`（強度超過動詞） | 要確認 | 論文が宣言した主張強度の天井（探究・示唆・存在例）と整合させる |
| `WARN/deficit`（欠陥モデル語彙） | 要確認 | 神経多様性の立場と整合するか。「障壁」等の確立語彙へ |
| `WARN/misidentify`（誤認共起） | 要確認 | 段落内に非診断宣言を足すか、語彙を分離。定義済みなら対応不要も可（根拠を記録） |
| `WARN/abstract`（要約レジスタ違反） | 要修正寄り | アブストラクトの語彙を絞る方針に従い置換（本文は維持可） |
| `WARN/disclaimer`（非診断宣言の欠如） | 要修正 | 医学化語彙を使う以上、宣言文は必須 |

### Step 3: LLM 敵対的読者レビュー（機械では拾えない短絡）

1. **逆接読み飛ばし**: 「〜ではなく」「〜に限定せず」の前節・後節が単独でどう読めるかを点検する
2. **比喩の誇張**: 登録語にない修辞（「無尽蔵」型）を意味的に発見する
3. **切り出し耐性**: 一文が SNS 等で文脈から切り出されて単独引用された場合の読まれ方を点検する
4. **著者属性の推測耐性**: 自己言及ケースの記述全体から「著者=診断済み」と推測される経路が残っていないかを点検する

### Step 4: 著者判定と sensitive-expressions.yml への蓄積

1. 著者の判断を `docs/<paper-id>/design/sot/sensitive-expressions.yml` に理由コメント付きで反映する

```yaml
banned_terms:
  - 無尽蔵 # 2026-08-18：無限の絶対表現・検証不能のため較正済み
allowlist:
  - 障害|二項対立 # 欠陥モデルのメタ議論（批判対象としての言及）
```

2. 本文修正後はスクリプトを再実行して FAIL=0・WARN の残件妥当性を確認する
3. 判断サマリを `docs/<paper-id>/design/logs/friction-log.md` に追記する（日付・検出・分類・根拠・アクション）

## 関連
- 検出スクリプト: `scripts/check_sensitive_expression.py`
- 強制発動: `assemble_manuscript.py`（FAIL 時はビルド中断、`--force` で回避）、投稿前ゲート `check_pre_submission.py` 第7チェック
- 用語の表記揺れ: `terminology-consistency` スキル（主張強度の天井など §2.5 系と連携）
- WARN/FAIL 全般のトリアージ: `pre-submission-triage` スキル

## 成果物
- センシティブ表現トリアージ判断サマリ（チャット提示）
- `docs/<paper-id>/design/sot/sensitive-expressions.yml`（ルールと判断の蓄積・正本）
- `docs/<paper-id>/design/logs/friction-log.md`（判断の監査証跡）
