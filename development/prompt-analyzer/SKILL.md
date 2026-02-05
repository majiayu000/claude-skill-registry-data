---
name: prompt-analyzer
description: ユーザープロンプトを分析し、topic_type（instruction/question/context）を判定する。
---

# Prompt Analyzer Skill

ユーザープロンプトを分析し、構造化データを返す Skill。

## Purpose

- **topic_type 判定**: プロンプトを instruction / question / context に分類
- **5W1H + リスク + 曖昧さ検出**: タスク依頼の詳細分析
- **論点分解**: 複数指示の分離
- **pm 支援**: playbook 作成前の情報収集

## When to Use

```yaml
triggers:
  - 全てのユーザープロンプト（Hook から強制呼び出し）

invocation:
  Task(subagent_type='prompt-analyzer', prompt='ユーザープロンプト')
```

## Output

```yaml
analysis:
  summary:
    primary_topic_type: instruction|question|context
    confidence: high|medium|low
    ready_for_playbook: true|false
    blocking_issues: ["{問題}"]
  必須アクション:
    - id: 1
      action: "この分析結果をチャットに出力"
    - id: 2
      action: "{topic_type に基づくアクション}"
```

## Next Action

```yaml
instruction:
  action: Skill(skill='playbook-init')
question:
  action: 直接回答
context:
  action: 現在タスクに統合
```

## Related Files

| ファイル | 役割 |
|----------|------|
| agents/prompt-analyzer.md | SubAgent 詳細定義 |
| .claude/hooks/prompt.sh | Hook（呼び出し元） |
