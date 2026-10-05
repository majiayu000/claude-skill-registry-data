---
slug: ai-codegenerator
version: 1.0.1
displayName: AI代码生成（AI Codegenerator）
summary: 使用AI技术自动生成代码，提高开发效率。
tags: clawhub
---

# AI_CodeGenerator

## Purpose
自動程式生成

## Primary Agents
Coder

## Notes
可單獨使用

## Inputs
- task: 要執行的任務描述
- context: 額外上下文（可選）
- constraints: 限制條件（可選）

## Outputs
- plan/result/report（依任務類型）
- logs/summary

## Workflow (default)
1. Analyze task
2. Plan subtasks
3. Execute by role
4. Validate result
5. Return final summary

## Safety
- 不執行破壞性操作，除非明確授權
- 外部動作（發送、部署到正式環境）需二次確認
- 記錄關鍵決策與錯誤
