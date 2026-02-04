---
name: procedure-checker
description: Validate generated experimental procedures against LA-Bench evaluation criteria. This skill orchestrates formal validation (via script) and semantic evaluation (via subagent) to ensure compliance with LA-Bench standards. Use this skill after generating procedures to assess quality before submission.
---

# Procedure Checker

## Overview

Validate generated experimental procedures against LA-Bench format requirements and semantic quality standards. This skill:

1. **Formal Validation** (Script-based): Checks step count and sentence limits using validate_procedure.py
2. **Semantic Evaluation** (Subagent-based): Analyzes alignment with expected outcomes, completeness, and quality
3. **Report Generation**: Creates comprehensive review markdown

The formal validation is handled by a Python script, while semantic evaluation is delegated to a specialized subagent.

## When to Use This Skill

Use this skill when:
- Evaluating outputs from the procedure-generator agent
- Checking generated procedures against LA-Bench standards before submission
- Debugging why generated procedures might fail evaluation
- Comparing multiple generated procedures to select the best candidate

## Validation Workflow

### Step 1: Read Input Files from Standardized Location

Read the necessary files from the experiment directory:

```bash
# Input data (original LA-Bench entry):
workdir/<filename>_<entry_id>/input.json

# Generated procedure:
workdir/<filename>_<entry_id>/procedure.json
```

The input.json contains:
- `expected_final_states`: Expected outcomes to validate against
- `source_protocol_steps`: Reference protocol steps
- `mandatory_objects`: Required materials and reagents
- `references`: Source documentation
- `measurement.specific_criteria`: Evaluation criteria (if available)

### Step 2: Validate Formal Constraints (Script-based)

Run the validation script to check formal requirements. First, wrap the procedure array in the expected format:

```bash
# Create wrapped version for validation
python3 -c "
import json
with open('workdir/<filename>_<entry_id>/procedure.json', 'r') as f:
    steps = json.load(f)
wrapped = {'procedure_steps': steps}
with open('workdir/<filename>_<entry_id>/procedure_wrapped.json', 'w') as f:
    json.dump(wrapped, f, ensure_ascii=False, indent=2)
"

# Run validation
python .claude/skills/procedure-checker/scripts/validate_procedure.py workdir/<filename>_<entry_id>/procedure_wrapped.json
```

The script validates:
1. **Step count**: Maximum 50 steps allowed
2. **Sentence count**: Each step text must contain ≤10 sentences

**Exit codes:**
- `0`: Validation passed
- `1`: Validation failed (errors printed to stdout)

### Step 3: Semantic Evaluation (Subagent-based)

Invoke a subagent to perform detailed semantic evaluation:

**Subagent invocation:**

Use the Task tool to launch a general-purpose subagent with the following prompt:

````
以下の実験手順を詳細にレビューし、LA-Bench評価基準に基づいて**10点満点で評価**してください。

## 入力データ

### 元の実験データ (input.json)
```json
{input_data}
```

### 生成された実験手順 (procedure.json)
```json
{procedure_steps}
```

## スコアリング基準

### 共通採点基準（5点満点）

以下の5項目について、各+1点で最大5点を付与:

**加点項目（各+1点、最大5点）**:

1. **実験指示のパラメータ反映 (+1点)**
   - `instruction`の全パラメータ（温度、濃度、時間等）が正しく反映されているか
   - 数値の誤り・欠落がないか

2. **使用物品の完全性 (+1点)**
   - `mandatory_objects`の全物品が誤りなく使用されているか
   - 余分/不足がないか

3. **元プロトコルの論理構造反映 (+1点)**
   - `source_protocol_steps`の順序・分岐・論理構造が矛盾なく反映されているか
   - 重要なステップの省略がないか

4. **期待される最終状態の達成 (+1点)**
   - `expected_final_states`が論理的に達成可能か
   - 論理破綻・計算ミスがないか

5. **適切な補完 (+1点)**
   - 明示されていない部分（条件、詳細手順）を適切に補完しているか
   - 補完が科学的に妥当で実行可能か

**減点項目（各-1点、積算しない）**:

- **過度に不自然な日本語/ハルシネーション (-1点)**: 意味不明な文章、入力に存在しない情報の捏造
- **計算ミス (-1点)**: 濃度・容量・希釈計算の数値エラー、単位換算の誤り
- **手順の矛盾 (-1点)**: ステップ間の論理的矛盾、時系列の不整合

**特別制限（過度の安全性）**:

以下の場合、共通基準を**最大2点に制限**:
- 入力や出典の情報を選別なく羅列
- 指示に反して過剰に安全側（例: 中間物100倍量、不要な予備実験大量追加、極端なインキュベーション時間）

### 個別採点基準（5点満点）

`measurement.specific_criteria`が存在する場合、その基準に従って5点満点で評価:
- 出題意図への適合性
- 安全性（適切なレベル）
- コスト効率
- 作業効率
- 実験精度向上

存在しない場合は、上記の一般的な観点から総合評価。

**Individual Criteria (if provided):**
{measurement_criteria}

## 評価項目

### 1. Expected Final Statesとの整合性

元データの`expected_final_states`に記載された期待される最終状態と、生成された手順の結果を比較:
- 手順を実行すると期待される最終状態が達成されるか?
- 全ての重要な処理ステップが含まれているか?
- 手順が目的を達成しているか?

**Expected Final States:**
{expected_final_states}

### 2. 完全性 (Completeness)

以下が手順に含まれているか確認:
- Mandatory Objectsの全ての項目が使用されているか
- Source Protocol Stepsの全てのステップがカバーされているか
- 適切な安全配慮（PPE、危険物取扱い等）
- 論理的な時系列構成

**Mandatory Objects:**
{mandatory_objects}

**Source Protocol Steps:**
{source_protocol_steps}

### 3. 数値仕様の正確性 (Quantitative Accuracy)

以下を検証:
- 濃度・容量が正確に計算されているか
- 希釈ステップが正確か
- 最終濃度が要求を満たすか
- 曖昧な表現（"適量"、"室温"等）がないか

### 4. 手順の一貫性 (Procedural Coherence)

以下を評価:
- ステップが論理的な順序で並んでいるか
- ステップ間の遷移が明確か
- 矛盾する指示がないか
- 再現性のための適切な詳細レベルか

### 5. Completed Protocolの基準（論文"Towards Completed Automated Laboratory"に基づく）

以下の項目について、プロトコルが「構文レベルで構造化」され「意味論レベルで欠落情報を補完」されているかを評価:

#### 5.1 パラメータの完全明示化
- 温度・時間・速度・pH・濃度・容器・デバイスの具体値が明示されているか
- 「室温」は具体的な範囲（例: 22-25°C）で記述されているか
- 暗黙の前提条件が明示的に記述されているか

**例:**
- ❌ 不十分: "室温でインキュベートする"
- ✅ 完成: "22–25°Cで30分間、湿度50%の条件下でインキュベートする（開始・終了時刻を記録）"

#### 5.2 操作パラメータの欠落ゼロ
- 遠心分離: 速度（×g）、時間、温度、ブレーキ設定の全てが記載されているか
- 攪拌: 回転数（rpm）、時間、温度、攪拌子サイズが記載されているか
- インキュベーション: 温度範囲、時間、雰囲気条件（CO2濃度、湿度等）が記載されているか
- 全ての操作で制御パラメータが明示されているか

**例:**
- ❌ 不十分: "サンプルを遠心する"
- ✅ 完成: "サンプルを12,000 × gで5分間、4°Cで遠心（ブレーキ: オン）；上清を除去し、ペレットを100 µL PBS（pH 7.4）で再懸濁する"

#### 5.3 試薬フロー管理（Reagent Flow and Lifecycle）
- 各操作での試薬の定義（defines: どこで作成・調製されるか）が明確か
- 各操作での試薬の消費（kills: どこで使用・消費されるか）が明確か
- 中間生成物のライフサイクルが追跡可能か
- 最終状態で未消費の試薬が残らないか（受容状態の達成）

**例:**
- ❌ 不十分: "等分に分ける"
- ✅ 完成: "混合液（合計80 mL）を2本の50 mL丸底フラスコに40 mLずつ分注；各フラスコに Flask-A/B とラベル付け；以降は並行して300 rpm、25°Cで10分間攪拌する"

#### 5.4 容器・機器の物理的制約
- 容器容量と作業容量の検証（通常、作業容量≤容器容量の80%）
- 連続添加時の総容量が容器容量を超えないことの確認
- 機器仕様（最大速度、温度範囲等）との整合性
- 危険な容量超過の防止（沸騰、飛散等）

**例:**
- ❌ 不十分: "35 mLを加え、続いて25 mLを加える"
- ✅ 完成: "35 mLを加え、続いて25 mLを加える（総容量60 mL；使用容器は最低100 mLビーカー、作業容量≤80 mL = 80%以下であることを確認）"

#### 5.5 時空間制約の検証
- 危険な組合せの回避（例: 熱不安定成分の加熱、不適合試薬の混合）
- 操作順序の依存関係が明確か
- タイムスタンプとトレーサビリティの記録方法が指定されているか
- 動的文脈での安全性確認（例: pH変化による腐食性の変化）

**例:**
- ❌ 不十分: "溶解するまで攪拌する"
- ✅ 完成: "80°Cの蒸留水100 mLに NaCl 10 gを加え、磁気攪拌子（Ø 25 mm）で600 rpmにて5分間攪拌；粒子が残る場合は2分間延長；質量バランスと最終導電率を記録する"

#### 5.6 ループ・条件分岐の明確化
- 終了条件が定量的に記述されているか
- 判断基準の測定方法が明示されているか
- ループ前後の状態管理（試薬の補充、機器の洗浄等）が記述されているか

**例:**
- ❌ 不十分: "終点まで滴定を繰り返す"
- ✅ 完成: "0.1 M HCl を 50 mL NaOH（0.1 M）に滴下（連続攪拌 300 rpm、25°C）；pHを2秒ごとに測定；ループ条件: pH変化が当量点付近（pH ~7.0）で10秒間に0.01未満になったら停止；滴定量と曲線を記録；次回のループ前にビュレットを蒸留水で3回洗浄"

#### 5.7 操作依存と試薬依存のグラフ整合性
- 制御フロー（操作の依存関係）と試薬フロー（試薬の流れ）が矛盾なくリンクしているか
- 各ステップで必要な試薬が事前に準備されているか
- 同時並行操作における試薬の競合がないか

## 出力形式

以下の形式でMarkdownレポートを出力してください:

```markdown
# Procedure Semantic Review Report

**Experiment ID**: {experiment_id}
**Review Date**: {date}

---

## Scoring Results

### Total Score: **X / 10 points**

#### Common Criteria: **Y / 5 points**

| Evaluation Item | Points | Score | Status |
|----------------|--------|-------|--------|
| 1. Parameter Reflection | 1pt | [0/1] | [✅/❌] |
| 2. Object Completeness | 1pt | [0/1] | [✅/❌] |
| 3. Logical Structure Reflection | 1pt | [0/1] | [✅/❌] |
| 4. Expected Outcome Achievement | 1pt | [0/1] | [✅/❌] |
| 5. Appropriate Supplementation | 1pt | [0/1] | [✅/❌] |

**Deductions**:
- [ ] Unnatural Japanese/Hallucination (-1pt)
- [ ] Calculation Errors (-1pt)
- [ ] Procedural Contradictions (-1pt)

**Special Restriction**:
- [ ] Excessive Safety Penalty (common criteria capped at 2pts)

#### Individual Criteria: **Z / 5 points**

[If `measurement.specific_criteria` exists]
- 出題意図への適合性: [詳細]
- 安全性: [詳細]
- コスト効率: [詳細]
- 作業効率: [詳細]
- 実験精度向上: [詳細]

[If not exists]
- 一般的な品質基準に基づく総合評価: [詳細]

---

## 1. Formal Validation Results

(この部分はスクリプトの結果を後で統合)

---

## 2. Semantic Quality Assessment

### 2.1 Alignment with Expected Final States

**Expected Final State 1:**
> {state_1}

**Assessment**: ✅ ACHIEVED / ❌ NOT ACHIEVED
- {詳細な評価と根拠}

(全てのexpected final statesについて繰り返し)

### 2.2 Completeness Check

#### Mandatory Objects Coverage
**Status**: ✅/❌
- 使用確認リスト: [詳細]
- 欠落/誤り: [詳細]

#### Source Protocol Steps Coverage
**Status**: ✅/❌
- 反映状況: [詳細]
- 省略/簡略化: [詳細]

#### Safety Considerations
**Status**: ✅/❌
- PPE、危険物取扱い: [詳細]

#### Logical Temporal Ordering
**Status**: ✅/❌
- 順序の妥当性: [詳細]

### 2.3 Quantitative Specifications

**Status**: ✅/❌

| Item | Expected | Actual | Verification |
|------|----------|--------|--------------|
| [Concentration] | [Expected] | [Actual] | [✅/❌] |
| [Volume] | [Expected] | [Actual] | [✅/❌] |
| [Calculation] | [Expected] | [Actual] | [✅/❌] |

**Calculation Verification**: [詳細な検証過程]

### 2.4 Procedural Coherence

**Status**: ✅/❌

- 論理的順序: [評価]
- ステップ間遷移: [評価]
- 矛盾の有無: [評価]
- 再現性: [評価]

### 2.5 Completed Protocol Criteria Assessment

**Status**: ✅/❌

#### 2.5.1 Parameter Explicitness
- 温度・時間・速度等の具体値: [評価]
- 「室温」等の曖昧表現の有無: [評価]
- 暗黙の前提条件の明示: [評価]

#### 2.5.2 Operation Parameter Completeness
- 遠心分離（速度・時間・温度・ブレーキ）: [評価]
- 攪拌（回転数・時間・温度・攪拌子）: [評価]
- インキュベーション（温度・時間・雰囲気）: [評価]

#### 2.5.3 Reagent Flow Management
- 試薬の定義（defines）の明確性: [評価]
- 試薬の消費（kills）の明確性: [評価]
- 中間生成物のライフサイクル追跡: [評価]
- 受容状態の達成（未消費試薬なし）: [評価]

#### 2.5.4 Physical Constraints
- 容器容量と作業容量の妥当性: [評価]
- 連続添加時の総容量確認: [評価]
- 機器仕様との整合性: [評価]

#### 2.5.5 Spatiotemporal Constraints
- 危険な組合せの回避: [評価]
- 操作順序の依存関係: [評価]
- トレーサビリティ記録方法: [評価]

#### 2.5.6 Loop/Conditional Clarity
- 終了条件の定量的記述: [評価]
- 判断基準の測定方法: [評価]
- ループ前後の状態管理: [評価]

#### 2.5.7 Control/Reagent Flow Consistency
- 操作依存と試薬依存の整合性: [評価]
- 必要試薬の事前準備: [評価]
- 並行操作での試薬競合: [評価]

### 2.6 Individual Criteria Compliance (if applicable)

[各criterionについて詳細評価]

---

## 3. Identified Strengths

1. {強み1 - 具体的な記述}
2. {強み2 - 具体的な記述}
3. {強み3 - 具体的な記述}

---

## 4. Issues and Recommendations

### Critical Issues (High Impact on Score)
1. {問題1 - 詳細な説明と影響}
2. {問題2 - 詳細な説明と影響}

### Minor Issues (Low Impact)
1. {問題3 - 詳細な説明}
2. {問題4 - 詳細な説明}

### Recommendations
#### Must-Fix (Required for Score Improvement)
1. {具体的な改善提案1}
2. {具体的な改善提案2}

#### Nice-to-Have (Quality Enhancement)
1. {具体的な改善提案3}
2. {具体的な改善提案4}

---

## 5. Overall Assessment

### Quality Rating: [⭐⭐⭐⭐⭐ / 5] (X/10 points)

**Rating Scale**:
- 9-10 pts: Excellent (⭐⭐⭐⭐⭐)
- 7-8 pts: Good (⭐⭐⭐⭐)
- 5-6 pts: Needs Improvement (⭐⭐⭐)
- 3-4 pts: Insufficient (⭐⭐)
- 0-2 pts: Unacceptable (⭐)

**Summary**: {総評 - スコアの根拠を明確に}

**Recommendation**: ✅ ACCEPT / ⚠️ REVISE / ❌ REJECT

---

## 6. Conclusion

{結論 - 総合的な判断}

**Final Verdict**: ✅ VALIDATION PASSED / ❌ VALIDATION FAILED

**Next Steps**: {推奨される次のアクション}

---

## Evaluation Metadata

- Evaluator: procedure-semantic-checker agent
- Evaluation Criteria Version: LA-Bench v1.0
- Scoring System: 10-point scale (Common 5pts + Individual 5pts)
```

評価は客観的かつ建設的に行い、具体的な根拠を示してください。スコアリングは厳密に基準に従い、各加点・減点の理由を明確に記載してください。
````

### Step 4: Combine Results and Save Report

1. Combine formal validation results (from script) with semantic evaluation (from subagent)
2. Save the complete review to `workdir/<filename>_<entry_id>/review.md`
3. Report completion to the parent

## Example Usage

```
User: "Check the generated procedure for public_test_1"

Assistant workflow:
1. Read input: workdir/public_test_public_test_1/input.json
2. Read procedure: workdir/public_test_public_test_1/procedure.json
3. Run formal validation: validate_procedure.py on wrapped procedure
4. Invoke semantic evaluation subagent with detailed prompt
5. Combine formal + semantic results
6. Save to: workdir/public_test_public_test_1/review.md
```

## Evaluation Criteria Reference

Based on LA-Bench evaluation standards:

### Formal Constraints (Binary - Script)
- [ ] Step count ≤ 50
- [ ] Each step ≤ 10 sentences

### Semantic Quality (Graded - Subagent)
- **Correctness**: Procedures achieve expected final states without errors
- **Completeness**: All necessary steps, materials, and considerations included
- **Clarity**: Unambiguous instructions with appropriate detail
- **Reproducibility**: Sufficient quantitative specifications for replication
- **Measurement Criteria**: Compliance with specific evaluation criteria (if provided)

## Resources

### scripts/validate_procedure.py

Python script for automated formal constraint validation. Checks step count and sentence limits with detailed error reporting.

**Usage:**
```bash
python .claude/skills/procedure-checker/scripts/validate_procedure.py <json_file>
```

**Output format:**
- Success: Prints "✅ Validation passed!" with step count
- Failure: Prints "❌ Validation failed" with detailed error list

## Integration with Other Skills and Agents

This skill works in conjunction with:
- **la-bench-parser**: Retrieves original entries for comparison
- **procedure-generator (agent)**: Generates procedures that this skill validates
- **Subagent (procedure-semantic-checker)**: Performs detailed semantic evaluation

## Architecture

```
procedure-checker (Skill)
├── Step 1: Read files (input.json, procedure.json)
├── Step 2: Formal validation (Script)
│   └── validate_procedure.py
├── Step 3: Semantic evaluation (Subagent)
│   └── General-purpose subagent with evaluation prompt
├── Step 4: Combine results
└── Step 5: Save review.md
```

## Common Issues and Fixes

**Issue**: Step count exceeds 50
- **Fix**: Consolidate related micro-steps, remove redundant instructions

**Issue**: Steps contain too many sentences
- **Fix**: Split complex steps into sub-steps, use more concise language

**Issue**: Procedure doesn't achieve expected final state
- **Fix**: Review source protocol steps, ensure critical processing steps aren't omitted

**Issue**: Quantitative specifications missing or incorrect
- **Fix**: Add explicit concentrations, volumes, times, and temperatures

**Issue**: Missing measurement criteria compliance
- **Fix**: Review the specific_criteria in input.json and ensure all items are addressed
