---
name: thorlabs-blender-optical-path-ja
description: 測定要件、2D 光路図、出所を記録した CAD から新しい測定光路を設計し、Blender 光学システムを再構築・監査・改訂します。高精細 optics-only モデル、Thorlabs 互換光機部品、光路 topology、全系検証、証拠範囲を明示した出版用レンダーに使用します。
---

# Thorlabs Blender Optical Path

測定要件または 2D 光路図を、説明可能で独立監査可能な Blender 光学テーブルへ変換します。

英語版を技術的な正本とします。形状作業の前に `../../skills/thorlabs-blender-optical-path/references/physical-gates.md`、合否判定の前に `evidence-contract.md`、既存シーンの改訂では `history-derived-rules.md`、実例では `project-case-study.md`、全系 run の前に `end-to-end-workflow.md`、複数 run の scale/release qualification 前に `multi-run-qualification.md` を読みます。

## 権限と改訂

1. システム制約、最新のユーザー指示・注釈画像、active なプロジェクト規則、本 Skill、旧成果物・旧 PASS の順に優先します。
2. 提出済み・合格済み成果物を凍結します。関連する修正は活動中の revision にまとめ、凍結した証拠を上書きせず、プレビューごとの版公開を避けます。
3. 全系は一つの run ID、writer、revision、generator/Blend lineage、workflow ledger を使います。補助 agent は既定で read-only とし、別々に書かれた module を全系として結合しません。
4. 画像指摘を object family、world-space geometry、数値ゲート、必要証拠へ変換します。
5. 実形状で証明できない場合は `UNVERIFIED` または `BLOCKED` とします。CAD の存在、process success、AABB 接触、自己申告は証拠ではありません。

## コア手順

最初に、新しい測定設計、図の再構築、既存シーンの修正、描画のみの変更を区別します。「以前の例と同等の品質で別の光路」という依頼では、旧例は画質比較に限り、空のシーンから新しい topology・generator・asset map を作ります。optics-only は光検出器と機械支持を含み、回路・電気・データ配線の可視化を除きます。詳細は[新設計と描画](../../skills/thorlabs-blender-optical-path/references/fresh-design-and-rendering.md)を参照してください。

1. `scripts/workflow_ledger.py` で一つの whole-system run spec、state ledger、append-only event hash chain を初期化します。
2. `schematic node -> experimental role -> real asset -> optical/fiber/electrical ports -> support path` を作成します。
3. 全 branch、部品、光線高さ、開口、検出端点を列挙します。
4. manifest で固定したメーカー URL だけから公式 CAD を private cache に取得し、atomic placement 前に bytes と SHA-256 を検証します。型番、URL、scale、bbox、local axis/normal、aperture、provenance、redistribution boundary を記録し、明示許諾なしに vendor geometry を公開しません。
5. source lock と全 hashed files を一つの atomic input bundle として扱います。形状作業前に producer-to-consumer artifact preflight を実行し、source bytes、canonical/part-qualified CAD cache keys、公式 drawing、runtime が次の script の実消費 path に存在することを確認します。lookup 前に structured authority input を typed exact-set contract として検証し、missing、duplicate、extra、legacy、malformed、identity mismatch は例外終了や重複の黙示的な折り畳みではなく、永続化された structured `BLOCKED` を生成しなければなりません。
6. 公開 script から semantic lock を差分ゼロで再計算します。multi-state system では全 edge に正確な `active_states` または hashed deterministic expansion を持たせ、全 state に明示的 ray template を要求します。
7. 光学中心、鏡面、分割面、反射、branch continuity を先に解きます。設計座標と再オープンした mesh/port の実測値を区別します。固定値のゼロ誤差や同じ部品 family への hit だけでは開口・first-hit の証明になりません。
8. 実テーブル穴から fastener、clamp、holder、post、mount、device を post-first で組みます。
9. 共通の配置原因を修正し、同じ run の代表 1 台を証明してから展開し、保存後に全コピーを再監査します。
10. beauty render より先に明るい mechanical/axial/cutaway 監査画像を作ります。
11. README/GATE 数値を machine evidence から導出し、同じ ledger で reopen、whole-system ray/BVH、OpenCV、GLB reimport、binary/PNG metadata sanitization、manifest、hash、active-rule matrix を完了します。

自由空間光、ガイドファイバー、電気ケーブルは別 family とし、依頼範囲内だけを生成します。開口は実際に開いている必要があります。低コストの診断プレビューで部品の精細さ、光路の可読性、構図を確認できますが、未完了の物理検証を明示します。最終出版用レンダーは物理ゲートの後に行います。材質スロットと polygon index の意味を保ち、部品 close-up と全 branch を確認します。全画像の sharpness・edge density・色画素総数だけでは精度や連続性を証明できず、2K 出力は 4K 納品を満たしません。

要求と必須ゲートを満たした最初の候補を凍結し、一度の納品・公開に進みます。入力・依存・runtime の変化や検査失敗がある場合に影響範囲を再検証します。Skill 文書の公開で未合格モデルの教訓を記録しても、モデルの release credit は与えません。事例固有の数値閾値を一般基準にしません。

`PASS` は全適用ゲートの新しい証拠、`PARTIAL/SCOPED` は blocker を列挙した限定範囲かつ final/release=false、`UNVERIFIED` は証拠不足、`BLOCKED` は既知の失敗を表します。Sanitization PASS は CAD conversion PASS を意味しません。
