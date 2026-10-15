---
name: evidence-coverage-audit
version: 1.0.0
api_version: data-agent/v2
description: 审核结构化主张与证据引用的映射、内容指纹、来源定位和独立来源数量，并按关键主张权重计算覆盖率，适用于报告交付前的证据完整性门禁。
author: data-team
tags: [governance, evidence, deterministic]
triggers:
  keywords: [证据覆盖审计, 主张引用核对, 关键结论证据]
  intents: []
  tables: []
depends_on:
  mcp_servers: []
  skills: []
  python_packages: []
tools:
  - name: audit_evidence_coverage
    description: 检查主张引用有效性、独立来源数量和加权覆盖率
    input_schema: schemas/coverage_input.json
    output_schema: schemas/coverage_output.json
capabilities: [evidence.coverage.audit]
accepts: [document]
permissions:
  network: []
  files: none
  datasources: none
resources:
  timeout_seconds: 30
  cpu_seconds: 10
  memory_mb: 256
  max_tool_calls: 1
  max_input_bytes: 2097152
  max_output_bytes: 1048576
entrypoints:
  execute: tools:audit_evidence_coverage
input_schema: schemas/coverage_input.json
output_schema: schemas/coverage_output.json
evaluation:
  dataset: eval/cases.yaml
  minimum_score: 0.95
---

# 证据覆盖审计

1. 主张和证据都必须使用稳定标识与完整内容指纹，禁止用自由文本模糊关联。
2. 引用必须指向存在、指纹合法且具有非空来源定位的证据，否则按无效引用处理。
3. 关键主张按双倍权重计算，并默认要求至少两个独立来源；同一来源的多条证据不能重复计数。
4. 达到覆盖比例但仍有未覆盖主张、无效引用或证据结构问题时，整体门禁仍不得通过。
5. 只审核引用结构，不返回主张原文，也不判断证据是否真实或是否语义支持主张。
