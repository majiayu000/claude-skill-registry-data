---
name: think
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 問題解決と分析：複雑な問題のための構造化思考プロセス。Divide & Conquer（分割統治）、Root Cause Analysis（根本原因分析）、SWOT、Pareto（パレート法則）、および意思決定ヒューリスティクス。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="think banner">

> **日本語** — `think` の公式日本語版。


# Think — 問題解決と分析

> 複雑な問題のための構造化思考プロセス

---

## 問題解決のアプローチ

### 1. Divide & Conquer（分割統治）

```
Problem -> Sub-problems -> Solve individually -> Combine
```

### 2. Root Cause Analysis（根本原因分析）

```
Symptom -> Why? -> Why? -> Why? -> Root cause -> Solution
```

### 3. Constraint Relaxation（制約緩和）

```
Unsolvable problem -> Relax constraints -> Solve -> Re-apply constraints
```

### 4. Analogy Search（類似検索）

```
New problem -> Similar known problem -> Adapt solution
```

---

## 分析手法

| 手法 | 適用 |
|------|------|
| **SWOT** | 強み / 弱み / 機会 / 脅威 |
| **Pro/Con (メリット/デメリット)** | 意思決定 |
| **Pareto** | 80/20 優先順位付け |
| **Fishbone** | 根本原因分析（石川図） |

---

## 意思決定ヒューリスティクス

### 不確実性下

```
1. 最悪のシナリオは何か？
2. それは不可逆か？
3. 行動しないことのコストは何か？
```

### 複雑性下

```
1. 最もシンプルな第一歩は何か？
2. 専門家ならどうするか？
3. 80%の解決策とは何か？
```

---

## 変更履歴

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*
