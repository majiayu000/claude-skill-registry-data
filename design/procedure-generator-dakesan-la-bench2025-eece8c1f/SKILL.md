---
name: procedure-generator
description: Orchestrate experimental procedure generation from LA-Bench format input. This skill orchestrates file I/O and delegates procedure generation logic to experiment-procedure-generator subagent. Use this skill when you need to generate step-by-step experimental procedures with quantitative specifications and proper experimental design.
---

# Procedure Generator

## Overview

Orchestrate the generation of detailed experimental procedures from LA-Bench format input data. This skill:

1. **File I/O Management**: Reads input.json and references/*.md from standardized location
2. **Subagent Delegation**: Invokes experiment-procedure-generator subagent with detailed requirements
3. **Output Management**: Saves generated procedure.json to standardized location

The actual procedure generation logic is delegated to the **experiment-procedure-generator subagent**, while this skill manages orchestration and file I/O.

## Input Format

The parent skill provides input in the following JSON structure:

```json
{
  "id": "experiment_id",
  "input": {
    "instruction": "High-level experimental objective",
    "mandatory_objects": ["List of required materials and reagents"],
    "source_protocol_steps": [
      {"id": 1, "text": "Reference protocol step 1"},
      {"id": 2, "text": "Reference protocol step 2"}
    ],
    "expected_final_states": ["Expected experimental outcomes"],
    "references": [
      {"id": 1, "text": "Citation or reference material"}
    ]
  }
}
```

## Output Format

Generate procedure steps as a JSON array and save to standardized location:

```json
[
  {"id": 1, "text": "First procedure step with quantitative details"},
  {"id": 2, "text": "Second procedure step with quantitative details"}
]
```

**Output path specification:**
- Standardized location: `workdir/<filename>_<entry_id>/procedure.json`
- Example: For `data/public_test.jsonl` with entry `public_test_1`, save to `workdir/public_test_public_test_1/procedure.json`

**Directory naming convention:**
- Extract filename (without extension) from JSONL path: `public_test` from `data/public_test.jsonl`
- Combine with entry ID: `public_test_public_test_1`
- Save output as: `procedure.json`

**Constraints:**
- Maximum 50 steps
- Each step: maximum 10 sentences
- Step IDs: sequential integers starting from 1
- Each step must be independently understandable

**Note:** The detailed core requirements (quantitative specifications, experimental design, temporal ordering, etc.) are now embedded in the subagent prompt in the Usage Workflow section below.

## Core Requirements Summary

The subagent prompt (in Usage Workflow below) includes detailed requirements for:

1. **Quantitative Specifications**: All conditions with specific values and tolerances
2. **Complete Experimental Design**: Controls, sample size, randomization
3. **Logical Temporal Ordering**: Pre-experimental setup, reagent preparation, logical sequence
4. **Reproducibility**: Master mix usage, standardization, traceability, quality control
5. **Safety Considerations**: PPE, hazard identification, emergency procedures, waste disposal

See the full subagent prompt in Step 2 of Usage Workflow for complete details.

## Usage Workflow

### Step 1: Read Input Files from Standardized Location

Read the necessary files from the experiment directory:

```bash
# Input data (original LA-Bench entry):
workdir/<filename>_<entry_id>/input.json

# Reference materials (if available):
workdir/<filename>_<entry_id>/references/ref_*.md
```

The input.json contains:
- `instruction`: High-level experimental objective
- `mandatory_objects`: Required materials and equipment
- `source_protocol_steps`: Reference protocol steps
- `expected_final_states`: Expected outcomes
- `references`: Source documentation URLs

### Step 2: Invoke experiment-procedure-generator Subagent

Use the Task tool to launch a general-purpose subagent with the following detailed prompt.

**Subagent invocation:**

````
以下のLA-Bench形式の実験データから、詳細な実験手順を生成してください。

## 入力データ

### Instruction
{instruction}

### Mandatory Objects
{mandatory_objects}

### Source Protocol Steps
{source_protocol_steps}

### Expected Final States
{expected_final_states}

### References (if available)
{references}

## Reference Materials (if fetched)
{ref_1.md content}
{ref_2.md content}
...

## 出力要件

以下の形式でJSON配列として出力してください:

```json
[
  {"id": 1, "text": "First step with quantitative details"},
  {"id": 2, "text": "Second step with quantitative details"},
  ...
]
```

## 制約条件

- **最大50ステップ**
- **各ステップ最大10文**
- **ステップIDは1から始まる連番**
- **各ステップは独立して理解可能であること**

## コア要件

### 1. 数値の明示化（Quantitative Specifications）

全ての実験条件に定量的な仕様を含める:
- **温度**: 許容範囲付き（例: 23.0 ± 0.2 °C）
- **容量**: 具体値と許容範囲（例: 100 µL ± 2 µL）
- **濃度**: モル濃度または希釈比（例: 1 mM, 1:100希釈）
- **時間**: 反応/培養時間（例: 30 min ± 2 min）
- **その他物理量**: pH, 湿度, 光条件

❌ 避けるべき曖昧な表現: "適量", "適切な温度", "室温", "十分な時間", "必要に応じて"

### 2. 完全な実験デザイン（Complete Experimental Design）

- 全ての必須実験条件を含む
- コントロール設定（ネガティブ/ポジティブ）
- サンプルサイズ（n ≥ 3推奨）
- 再現実験と技術的反復の区別
- 適切なランダム化手順

### 3. 論理的な時系列構成（Logical Temporal Ordering）

#### 3.1 実験前準備
必ず準備ステップを含める:
- 機器の予熱/冷却
- 試薬の平衡化
- 機器の校正
- 作業空間の準備

#### 3.2 試薬調製
使用前に試薬を準備:
- マスターミックスの調製
- 希釈液の準備
- 標準液の調製

#### 3.3 論理的な操作順序
以下の原則に従う:
1. 温度依存操作前に機器設定
2. 待機時間を有効活用
3. 交差汚染の防止
4. 時間的に重要な操作は連続配置
5. 危険な操作前に適切な保護措置

### 4. 再現性の担保（Reproducibility）

- マスターミックス使用でピペット誤差削減
- 標準化された手順
- トレーサビリティ（ロット番号、機器、実施日の記録方法）
- 品質管理（ポジティブ/ネガティブコントロール）

### 5. 安全性への配慮

- 適切な保護具（PPE）の明示
- 危険源の特定と対策
- 緊急時対応手順
- 廃棄物処理方法

### 6. Completed Protocolの要件（論文"Towards Completed Automated Laboratory"に基づく）

自然言語プロトコルを実行可能レベルまで詳細化するため、以下の要件を満たすこと:

#### 6.1 パラメータの完全明示化
すべての条件・パラメータを具体値で明示:
- 温度: 「室温」→「22-25°C」のように具体的な範囲で記述
- 時間: 全ての待機・反応時間を明示
- 速度: 遠心・攪拌の回転数を具体値で指定
- pH・濃度: 定量的な値と許容範囲
- 容器・デバイス: 使用する器具の仕様を明示

**例:**
- ❌ "室温でインキュベートする"
- ✅ "22–25°Cで30分間、湿度50%の条件下でインキュベートする（12-well plate、蓋閉鎖、開始・終了時刻とwell IDを記録）"

#### 6.2 必要パラメータの欠落ゼロ
全ての操作で制御パラメータを完全に指定:
- 遠心分離: 速度（×g）、時間、温度、ブレーキ設定を全て記載
- 攪拌: 回転数、時間、温度、攪拌子サイズを全て記載
- インキュベーション: 温度範囲、時間、雰囲気条件（CO2、湿度等）を全て記載

**例:**
- ❌ "サンプルを遠心する"
- ✅ "Enzyme X（最終濃度1 U/mL）を1.0 mLサンプルに添加（1.5 mL microcentrifuge tube）；5回転倒混和；12,000 × gで5分間、4°Cで遠心（ブレーキ: オン）；上清を除去；ペレットを100 µL PBS（pH 7.4）で再懸濁"

#### 6.3 操作間の入出力（試薬フロー）の明確化
- 各操作で何を定義（defines）し、何を消費（kills）するかを明示
- 中間生成物のライフサイクルを追跡可能にする
- 最終的に未消費の試薬が残らないようにする（受容状態の達成）

**例:**
- ❌ "混合液を等分に分ける"
- ✅ "混合液（合計80 mL）を2本の50 mL丸底フラスコに40 mLずつ分注；各フラスコにFlask-A/Bとラベル付け；以降は並行して300 rpm、25°Cで10分間攪拌"

#### 6.4 実行時の空間・時間制約の検査
- 容器容量: 作業容量が容器容量の80%以下であることを確認
- 連続添加: 複数の試薬を連続添加する場合、総容量を事前に計算
- 安全性: 過積載による沸騰・飛散を防止
- 機器仕様: 最大速度、温度範囲等の制限内であることを確認

**例:**
- ❌ "35 mLを加え、続いて25 mLを加える"
- ✅ "35 mLを加え、続いて25 mLを加える（総容量60 mL；最小容器容量100 mLビーカー使用、作業容量≤80 mL（80%以下）を確認）"

#### 6.5 操作の終了条件と判断基準の定量化
- 「溶解するまで」「終点まで」等の曖昧な条件を定量化
- 判断基準の測定方法を明示
- ループ前後の状態管理（洗浄、補充等）を記述

**例:**
- ❌ "溶解するまで攪拌する"
- ✅ "80°Cの蒸留水100 mLにNaCl 10 gを加え、磁気攪拌子（Ø 25 mm）で600 rpmにて5分間攪拌；粒子が残る場合は2分間延長；質量バランスと最終導電率を記録"

- ❌ "終点まで滴定を繰り返す"
- ✅ "0.1 M HClを50 mL NaOH（0.1 M）に滴下（連続攪拌300 rpm、25°C）；pHを2秒ごとに測定；ループ条件: pH変化が当量点付近（pH ~7.0）で10秒間に0.01未満になったら停止；滴定量と曲線を記録；次回のループ前にビュレットを蒸留水で3回洗浄"

#### 6.6 操作依存と試薬依存の整合性
- 制御フロー（操作の順序依存）と試薬フロー（試薬の生成・消費）が矛盾なくリンクしていること
- 各ステップで必要な試薬が事前に準備されていること
- 同時並行操作で試薬の競合が発生しないこと
- 動的な文脈での安全性（例: pH変化による腐食性の変化）を考慮すること

## 推奨される手順構造

1. **実験前準備**: 機器設定、試薬平衡化、作業空間準備
2. **試薬調製**: マスターミックス、希釈液、標準液
3. **サンプル処理**: 実験操作
4. **培養/反応**: 時間依存反応
5. **測定/検出**: データ取得
6. **後処理**: データ解析、サンプル保管、清掃

JSONのみを出力し、説明文は含めないでください。
````

### Step 3: Save Generated Procedure

Use the Write tool to save the subagent's JSON output:

```bash
# Save to standardized location
workdir/<filename>_<entry_id>/procedure.json
```

Ensure the output is valid JSON array format with sequential step IDs.

### Step 4: Verify Output

Check that the generated procedure meets formal constraints:
- Step count ≤ 50
- Each step ≤ 10 sentences
- Valid JSON format
- Sequential step IDs starting from 1

### Step 5: Report Completion

Inform the parent that the procedure has been generated and saved to the standardized location.

---

## Detailed Requirements for Procedure Generation

以下は、subagentプロンプトに含まれる詳細な要件の説明です。

### 1. Quantitative Specifications (数値の明示と精度管理)

All experimental conditions must include **quantitative specifications**:

- **Temperature**: Include tolerance ranges (e.g., 23.0 ± 0.2 °C, 4°C ± 1°C)
- **Volume**: Specific values with tolerance (e.g., 100 µL ± 2 µL, 10–100 µL)
- **Concentration**: Molar concentration or dilution ratios (e.g., 1 mM, 1:100 dilution)
- **Time**: Reaction/incubation times in seconds/minutes/hours (e.g., 30 min ± 2 min, 2 hours)
- **Centrifugation**: Speed and time (e.g., 12,000 × g, 10 min, 4°C)
- **Other physical quantities**: pH, humidity, light conditions

**Avoid vague expressions** such as "適量 (appropriate amount)", "適切な温度 (suitable temperature)", "室温 (room temperature)", "十分な時間 (sufficient time)", "必要に応じて (as needed)".

### 2. Complete Experimental Design (実験デザインの完全性)

- **Comprehensive experimental groups**: Include all necessary experimental conditions
- **Control setup**: Negative control, positive control, blanks appropriately placed
- **Sample size**: Consider statistical power (n ≥ 3 recommended)
- **Replicates**: Distinguish technical replicates from biological replicates
- **Randomization**: Appropriate randomization procedures to reduce bias

### 3. Logical Temporal Ordering (実験の時系列的順序と準備ステップ)

#### 3.1. Pre-experimental Setup

Always include preparation steps **before** experimental operations:

- **Equipment pre-heating/cooling**: "Set incubator to 37.0 ± 0.5°C and preheat for at least 30 minutes"
- **Reagent equilibration**: "Allow reagents to equilibrate to room temperature (20–25°C) for 30 minutes"
- **Equipment calibration**: "Verify pipette calibration and adjust if necessary"
- **Workspace preparation**: "Sterilize clean bench with UV irradiation for 15 minutes"
- **Ice/water bath preparation**: "Prepare ice-water bath at ≤4°C"

#### 3.2. Reagent Preparation

Prepare reagents **before use**:

- **Master mix preparation**: Pre-mix common reagents for multiple samples
- **Dilution preparation**: Prepare solutions at required concentrations in advance
- **Standard solution preparation**: Prepare calibration standards by serial dilution

#### 3.3. Logical Operation Sequence

Determine operation order following these principles:

1. **Temperature dependency**: Set equipment before temperature-dependent operations
2. **Utilize incubation time**: Perform other preparations during waiting periods
3. **Prevent cross-contamination**: Separate high-risk contamination operations
4. **Time-critical operations**: Place time-sensitive operations consecutively
5. **Safety assurance**: Perform hazardous operations after appropriate protective measures

#### 3.4. Parallel Operations

Explicitly state when operations can be performed in parallel:

- "During Step 5 incubation (30 min), reagent preparation for Steps 6–8 can be performed in parallel"

### 4. Reproducibility (再現性の担保)

- **Master mix usage**: Pre-mix common reagents to reduce pipetting errors
- **Standardized procedures**: Ensure consistency when repeating operations
- **Traceability**: Specify methods for recording reagent lot numbers, equipment used, and execution dates
- **Quality control**: Verify experimental validity using positive/negative controls

### 5. Logical Explanation of Operations (操作の論理的説明)

For each step, include:

- **Purpose of operation**: Why this step is necessary
- **Chemical/biological rationale**: Brief explanation of reaction mechanism or principle
- **Theoretical background for conditions**: Why this temperature/time/concentration
- **Expected results**: What will be achieved by this operation

## Quality Criteria

Excellent experimental procedures have these characteristics:

### Basic Requirements
✅ Pre-experimental setup steps explicitly stated (equipment preheating, reagent equilibration, etc.)
✅ Operations ordered logically and chronologically
✅ All numerical values specific and reproducible
✅ Experimental design logical and complete
✅ Controls appropriately configured
✅ Purpose and rationale of each operation clear
✅ Reproducibility-enhancing measures included (master mix, etc.)
✅ Traceability ensured
✅ Parallel operations specified for efficient experimental progress

### Completed Protocol Requirements
✅ All parameters explicitly stated (temperature ranges, not "room temperature")
✅ Zero missing operation parameters (centrifuge: speed, time, temperature, brake)
✅ Reagent flow clearly defined (defines/kills for each operation)
✅ Container capacity verified (working volume ≤ 80% of capacity)
✅ Spatiotemporal constraints checked (no dangerous combinations)
✅ Loop/conditional termination criteria quantified
✅ Control flow and reagent flow consistent

❌ Avoid: "適量", "適切な温度", "室温", "十分な時間", "必要に応じて"
❌ Avoid: Starting experiment without pre-experimental setup, illogical operation sequence
❌ Avoid: Missing parameters (e.g., centrifuge without speed/time)
❌ Avoid: Ambiguous termination criteria (e.g., "until dissolved")

## Recommended Procedure Structure

1. **Pre-experimental Setup**: Equipment settings, reagent equilibration, workspace preparation
2. **Reagent Preparation**: Master mix, dilution solutions, standard solutions
3. **Sample Processing**: Experimental operations on samples
4. **Incubation/Reaction**: Time-dependent reactions
5. **Measurement/Detection**: Data acquisition
6. **Post-processing**: Data analysis, sample storage, cleanup

---

## Architecture

```
procedure-generator (Skill)
├── Step 1: Read files (input.json, references/*.md)
├── Step 2: Invoke subagent (experiment-procedure-generator)
│   └── General-purpose subagent with detailed generation prompt
├── Step 3: Save procedure.json
├── Step 4: Verify output
└── Step 5: Report completion
```

## Integration with Other Skills

This skill works in conjunction with:
- **la-bench-parser**: Provides input.json with experimental data
- **web-reference-fetcher**: Provides reference materials (optional)
- **procedure-checker**: Validates generated procedures
- **Subagent (experiment-procedure-generator)**: Performs actual procedure generation

## Example Usage

```
User: "Generate procedure for public_test_1"

Assistant workflow:
1. Read input: workdir/public_test_public_test_1/input.json
2. Read references: workdir/public_test_public_test_1/references/ref_*.md
3. Invoke experiment-procedure-generator subagent with detailed prompt
4. Save to: workdir/public_test_public_test_1/procedure.json
5. Verify formal constraints (≤50 steps, ≤10 sentences/step)
6. Report completion
```

---

## Important Context

This task is conducted for **academic research purposes** to improve experimental planning quality and safety:

- This is a **thought experiment** to evaluate experimental planning capabilities
- The objective is to maximize safety and reproducibility
- Scientifically accurate and detailed procedures are required
- Plans should include appropriate safety considerations following research ethics guidelines
