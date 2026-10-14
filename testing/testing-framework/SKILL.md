---
name: testing-framework
version: 2.0.0
description: |
  OpenClaw Skills 自动化测试框架 (Level 5)
  完整的测试生命周期管理：需求→执行→报告→CI/CD→质量自检→对抗测试
  支持单元/集成/端到端三级测试，覆盖3个关键Skill
author: Satisficing Institute
tags:
  - testing
  - pytest
  - ci-cd
  - quality-assurance
  - coverage
  - adversarial-testing
requires:
  - python: ">=3.10"
  - tools: ["pytest", "pytest-cov", "pytest-html", "pytest-xdist"]
  - level: 5
---

# Testing Framework Skill V2.0.0 (Level 5)

## 概述

本测试框架为OpenClaw的关键Skill提供**完整的测试生命周期管理**，从测试需求输入到最终质量验证，确保代码质量、功能稳定性和测试本身的有效性。

### 核心能力矩阵

| 标准 | 能力 | 状态 |
|------|------|------|
| **S1** | 输入测试需求/测试计划/被测Skill | ✅ 完整 |
| **S2** | 测试执行（单元→集成→端到端） | ✅ 完整 |
| **S3** | 输出测试报告（覆盖率→通过率→缺陷清单） | ✅ 完整 |
| **S4** | CI/CD集成自动触发 | ✅ 完整 |
| **S5** | 测试质量自检（测试有效性验证） | ✅ 完整 |
| **S6** | 局限标注（无法测试非确定性行为） | ✅ 完整 |
| **S7** | 对抗测试（故意破坏测试验证鲁棒性） | ✅ 完整 |

### 设计目标

1. **早期发现bug** - 在部署前捕获问题
2. **防止回归** - 确保修复不会引入新问题
3. **文档化行为** - 测试即文档
4. **支持重构** - 安全地进行代码改进
5. **CI/CD集成** - 自动化测试流水线
6. **测试有效性** - 确保测试本身是正确的
7. **鲁棒性验证** - 通过对抗测试验证测试质量

---

## 目录结构

```
testing-framework/
├── SKILL.md                        # 本文件
├── SKILL_REQUIREMENTS.md           # S1: 测试需求与计划模板
├── SKILL_LIMITATIONS.md            # S6: 测试局限性说明
├── pyproject.toml                  # pytest和工具配置
├── pytest.ini                      # pytest配置（兼容旧版本）
├── requirements.txt                # 测试依赖
├── run_tests.py                    # S2: 测试执行主脚本
├── run_coverage.py                 # S3: 覆盖率报告生成
├── defect_tracker.py               # S3: 缺陷追踪管理
├── test_quality_checker.py         # S5: 测试质量自检
├── adversarial_test.py             # S7: 对抗测试执行器
├── scripts/
│   ├── ci_trigger.sh               # S4: CI触发脚本
│   ├── pre_commit_hook.sh          # S4: 预提交检查
│   └── nightly_test.sh             # S4: 夜间测试
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # 共享fixtures和配置
│   ├── base.py                     # 测试基类和工具
│   ├── unit/                       # 单元测试
│   │   ├── zero-idle-enforcer/
│   │   ├── token-budget-enforcer/
│   │   └── blue-sentinel/
│   ├── integration/                # 集成测试
│   │   ├── test_skill_interaction.py
│   │   └── test_data_consistency.py
│   └── e2e/                        # 端到端测试
│       ├── test_full_workflow.py
│       └── test_error_recovery.py
├── reports/                        # 测试报告输出
│   ├── coverage/
│   ├── test_report.html
│   ├── test_results.json
│   ├── defects.json                # 缺陷追踪
│   └── quality_report.json         # 质量报告
└── .github/
    └── workflows/
        └── skills-test.yml         # S4: GitHub Actions CI/CD
```

---

## S1: 输入规范 - 测试需求与计划

### 1.1 测试需求输入格式

所有测试必须基于明确的测试需求文档，使用 `SKILL_REQUIREMENTS.md` 模板：

```markdown
### Skill: [skill-name]
#### 测试需求
- **风险等级**: P0/P1/P2
- **测试范围**: 单元/集成/端到端
- **覆盖率要求**: ≥90% (P0) / ≥80% (P1) / ≥70% (P2)

#### 功能点清单
| ID | 功能点 | 优先级 | 测试类型 | 依赖 |
|----|--------|--------|----------|------|
| F1 | [功能描述] | P0 | 单元 | 无 |

#### 边界条件
- [边界1]: [预期行为]
- [边界2]: [预期行为]

#### 异常场景
- [异常1]: [预期处理]
```

### 1.2 测试计划模板

```python
# tests/unit/[skill]/test_plan.py
"""
Test Plan for [Skill Name]
- Created: YYYY-MM-DD
- Reviewer: [Name]
- Last Updated: YYYY-MM-DD
"""

TEST_PLAN = {
    "skill": "skill-name",
    "version": "1.0.0",
    "risk_level": "P0",
    "test_levels": ["unit", "integration", "e2e"],
    "coverage_target": 90,
    "test_cases": [
        {
            "id": "TC001",
            "name": "正常流程测试",
            "type": "unit",
            "priority": "P0",
            "automation": True
        },
        # ...
    ]
}
```

### 1.3 被测Skill注册

在 `conftest.py` 中注册被测Skill：

```python
REGISTERED_SKILLS = {
    "zero-idle-enforcer": {
        "path": "skills/zero-idle-enforcer",
        "risk_level": "P0",
        "test_markers": ["zero_idle", "critical"],
        "coverage_target": 90
    },
    "token-budget-enforcer": {
        "path": "skills/token-budget-enforcer",
        "risk_level": "P0",
        "test_markers": ["token_budget", "critical"],
        "coverage_target": 90
    },
    "blue-sentinel": {
        "path": "skills/blue-sentinel",
        "risk_level": "P1",
        "test_markers": ["blue_sentinel"],
        "coverage_target": 80
    }
}
```

---

## S2: 测试执行 - 三级测试体系

### 2.1 测试层级定义

| 层级 | 标记 | 执行时间 | 目的 | 失败策略 |
|------|------|----------|------|----------|
| **单元测试** | `unit` | <30s | 验证单个函数/类 | 阻塞部署 |
| **集成测试** | `integration` | <2min | 验证组件交互 | 阻塞部署 |
| **端到端** | `e2e` | <5min | 验证完整流程 | 阻塞部署(P0) |

### 2.2 执行命令

```bash
# 运行全部三级测试
python run_tests.py --all-levels

# 仅运行特定层级
python run_tests.py --level unit
python run_tests.py --level integration
python run_tests.py --level e2e

# 运行关键路径（所有层级P0测试）
python run_tests.py --critical

# 运行指定Skill的全部层级测试
python run_tests.py --skill zero_idle --all-levels
```

### 2.3 测试执行流程

```
┌─────────────────────────────────────────────────────────────┐
│                    测试执行流程                              │
├─────────────────────────────────────────────────────────────┤
│  1. 预检查 → 验证测试环境、依赖完整性                        │
│  2. 静态分析 → flake8, black, isort                         │
│  3. 单元测试 → 并行执行（pytest-xdist）                      │
│  4. 集成测试 → 顺序执行（组件依赖）                          │
│  5. 端到端测试 → 顺序执行（完整流程）                        │
│  6. 覆盖率收集 → 合并多层级覆盖率                            │
│  7. 质量检查 → 测试有效性验证                                │
│  8. 报告生成 → HTML/JSON/缺陷清单                            │
└─────────────────────────────────────────────────────────────┘
```

---

## S3: 测试报告 - 三层输出体系

### 3.1 覆盖率报告

```bash
# 生成详细覆盖率报告
python run_coverage.py --threshold 80 --output reports/coverage/

# 输出格式
reports/coverage/
├── index.html              # 总览页面
├── [module]/
│   ├── index.html          # 模块覆盖率
│   └── [file].html         # 文件详细覆盖
├── coverage.xml            # Cobertura格式（CI使用）
└── coverage.json           # JSON格式（程序解析）
```

**覆盖率指标定义：**

| 指标 | 说明 | 目标值 |
|------|------|--------|
| Line Coverage | 代码行覆盖率 | ≥80% |
| Branch Coverage | 分支覆盖率 | ≥75% |
| Function Coverage | 函数覆盖率 | ≥90% |
| Condition Coverage | 条件覆盖率 | ≥70% |

### 3.2 通过率报告

```bash
# 生成测试执行报告
python run_tests.py --report

# 输出文件
reports/
├── test_report.html        # 人类可读报告
├── test_results.json       # 机器可读结果
├── junit.xml               # JUnit格式（CI使用）
└── summary.json            # 执行摘要
```

**test_results.json 结构：**

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "duration": 45.2,
  "summary": {
    "total": 150,
    "passed": 148,
    "failed": 1,
    "skipped": 1,
    "error": 0
  },
  "by_level": {
    "unit": {"total": 100, "passed": 99, "failed": 1},
    "integration": {"total": 30, "passed": 30, "failed": 0},
    "e2e": {"total": 20, "passed": 19, "skipped": 1}
  },
  "by_skill": {
    "zero_idle": {"total": 50, "passed": 50},
    "token_budget": {"total": 50, "passed": 49, "failed": 1},
    "blue_sentinel": {"total": 50, "passed": 49, "skipped": 1}
  }
}
```

### 3.3 缺陷追踪清单

```bash
# 生成缺陷报告
python defect_tracker.py --report

# 输出文件
reports/defects.json
```

**缺陷记录格式：**

```json
{
  "defects": [
    {
      "id": "DEF-001",
      "timestamp": "2024-01-01T12:00:00Z",
      "skill": "token-budget-enforcer",
      "test_case": "test_boundary_overflow",
      "severity": "high",
      "type": "logic_error",
      "description": "边界值处理错误",
      "stack_trace": "...",
      "status": "open",
      "assigned_to": null,
      "fixed_in": null
    }
  ],
  "metrics": {
    "total_open": 1,
    "total_closed": 5,
    "by_severity": {"high": 1, "medium": 0, "low": 0},
    "by_skill": {"token_budget": 1, "zero_idle": 0, "blue_sentinel": 0}
  }
}
```

---

## S4: CI/CD集成 - 自动触发机制

### 4.1 触发条件

| 触发类型 | 条件 | 执行测试 |
|----------|------|----------|
| **Push触发** | 推送到main/develop/feature/* | 单元+集成 |
| **PR触发** | 修改skills/目录的PR | 全部层级 |
| **定时触发** | 每日凌晨2点 | 全部层级+E2E |
| **手动触发** | workflow_dispatch | 可选 |
| **预提交** | git commit前 | 单元测试 |

### 4.2 GitHub Actions 工作流

```yaml
# 详见 .github/workflows/skills-test.yml
jobs:
  precheck:       # 环境检查
  unit-tests:     # 单元测试（并行）
  integration:    # 集成测试
  e2e-tests:      # 端到端测试
  coverage:       # 覆盖率检查
  quality-check:  # S5: 测试质量自检
  adversarial:    # S7: 对抗测试
  report:         # 报告汇总
```

### 4.3 本地预提交钩子

```bash
# 安装预提交钩子
./scripts/pre_commit_hook.sh install

# 钩子执行内容
1. flake8 代码检查
2. black 格式检查
3. 单元测试快速运行
4. 覆盖率阈值检查（≥70%）
```

### 4.4 质量门禁

```yaml
quality_gates:
  unit_tests:
    min_pass_rate: 100%       # 单元测试必须100%通过
    max_duration: 60s         # 最长执行时间
  
  integration_tests:
    min_pass_rate: 100%       # 集成测试必须100%通过
    max_duration: 120s
  
  coverage:
    line_coverage: 80%        # 行覆盖率≥80%
    branch_coverage: 75%      # 分支覆盖率≥75%
  
  code_quality:
    flake8_errors: 0          # 无flake8错误
    black_format: true        # 符合black格式
```

---

## S5: 测试质量自检 - 有效性验证

### 5.1 自检项目

```bash
# 运行测试质量自检
python test_quality_checker.py
```

| 检查项 | 说明 | 通过标准 |
|--------|------|----------|
| **断言完整性** | 每个测试至少一个断言 | 100% |
| **独立性检查** | 测试间无共享状态 | 100% |
| **命名规范** | 测试名清晰描述意图 | ≥95% |
| **重复检测** | 无冗余测试代码 | 0重复 |
| **覆盖深度** | 关键路径被覆盖 | ≥90% |
| **Mock验证** | Mock对象正确验证 | 100% |

### 5.2 变异测试（Mutation Testing）

```bash
# 运行变异测试验证测试有效性
python test_quality_checker.py --mutation

# 原理：故意修改源代码，测试应该失败
# 如果修改后测试仍通过，说明测试不够严格
```

**变异算子：**
- 算术运算符替换 (+ → -, * → /)
- 比较运算符替换 (== → !=, > → >=)
- 条件边界调整 (if x > 5 → if x >= 5)
- 返回值修改 (return True → return False)

### 5.3 测试有效性报告

```json
{
  "quality_score": 92,
  "checks": {
    "assertion_integrity": {"passed": 150, "failed": 0, "score": 100},
    "test_independence": {"passed": 150, "failed": 0, "score": 100},
    "naming_convention": {"passed": 145, "failed": 5, "score": 97},
    "code_duplication": {"duplicates": 0, "score": 100},
    "coverage_depth": {"covered": 85, "missed": 5, "score": 94},
    "mutation_score": {"killed": 45, "survived": 5, "score": 90}
  },
  "recommendations": [
    "test_boundary_case.py:15 添加更多断言",
    "test_edge_case.py:30 测试名不够清晰"
  ]
}
```

---

## S6: 局限性标注 - 无法测试场景

### 6.1 已知的测试局限

以下场景**无法通过自动化测试覆盖**，需人工验证：

| 局限类型 | 场景 | 缓解措施 |
|----------|------|----------|
| **非确定性行为** | AI模型输出、随机数生成 | 边界检查、统计验证 |
| **时间依赖** | 特定时间触发的功能 | Mock时间、时间旅行测试 |
| **外部依赖** | 第三方API、网络状态 | Mock/Stub、契约测试 |
| **并发竞争** | 多线程/多进程竞争条件 | 压力测试、代码审查 |
| **UI交互** | 图形界面操作 | 简化界面、日志验证 |
| **大文件处理** | 超出内存的数据处理 | 小数据代理、性能测试 |

### 6.2 局限性清单（Limitation Registry）

```json
// reports/limitations.json
{
  "limitations": [
    {
      "id": "LIM-001",
      "skill": "blue-sentinel",
      "category": "非确定性",
      "description": "AI模型的认知审计结果具有随机性",
      "impact": "中",
      "mitigation": "多次运行取平均、设置随机种子",
      "manual_test_required": true
    },
    {
      "id": "LIM-002",
      "skill": "token-budget-enforcer",
      "category": "外部依赖",
      "description": "依赖外部Token计数API",
      "impact": "高",
      "mitigation": "Mock API响应、契约测试",
      "manual_test_required": false
    }
  ]
}
```

### 6.3 手动测试清单

对于自动化无法覆盖的场景，维护手动测试清单：

```markdown
### 手动测试清单

#### blue-sentinel 认知审计
- [ ] 运行10次，验证结果一致性>80%
- [ ] 检查极端输入（空字符串、超长文本）
- [ ] 验证审计报告的格式正确性

#### token-budget-enforcer
- [ ] 实际运行24小时，验证预算控制
- [ ] 手动触发临界状态，验证降级行为
```

---

## S7: 对抗测试 - 鲁棒性验证

### 7.1 对抗测试原理

通过**故意破坏**来验证测试的鲁棒性：

```
正常流程:  代码正确 → 测试通过 ✅
对抗测试:  代码破坏 → 测试失败 ✅ (测试有效)
          代码破坏 → 测试通过 ❌ (测试无效!)
```

### 7.2 对抗测试类型

```bash
# 运行对抗测试
python adversarial_test.py --mode all
```

| 对抗类型 | 操作 | 验证目标 |
|----------|------|----------|
| **代码注入** | 在源码中插入bug | 测试能检测bug |
| **边界破坏** | 修改边界条件 | 边界测试有效 |
| **异常遗漏** | 移除异常处理 | 异常测试有效 |
| **返回值篡改** | 修改return值 | 断言能捕获 |
| **时序破坏** | 修改时间逻辑 | 时间相关测试有效 |

### 7.3 对抗测试报告

```json
{
  "adversarial_test": {
    "timestamp": "2024-01-01T12:00:00Z",
    "total_injections": 50,
    "detected": 48,
    "missed": 2,
    "detection_rate": 96,
    "injections": [
      {
        "id": "ADV-001",
        "skill": "zero-idle-enforcer",
        "type": "boundary_break",
        "injection": "将7200秒改为7201秒",
        "detected": true,
        "failed_tests": ["test_idle_exactly_2_hours_boundary"]
      },
      {
        "id": "ADV-002",
        "skill": "token-budget-enforcer",
        "type": "return_value_tamper",
        "injection": "将return NORMAL改为return LOW",
        "detected": true,
        "failed_tests": ["test_token_level_with_normal_percentage"]
      }
    ]
  }
}
```

### 7.4 对抗测试集成到CI

```yaml
# GitHub Actions 中集成
adversarial-tests:
  name: 对抗测试
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: 运行对抗测试
      run: python adversarial_test.py --mode all
    - name: 检查检测率
      run: |
        DETECTION_RATE=$(jq '.adversarial_test.detection_rate' reports/adversarial.json)
        if [ "$DETECTION_RATE" -lt 90 ]; then
          echo "对抗测试检测率低于90%，测试质量不足"
          exit 1
        fi
```

---

## 安装与使用

### 快速开始

```bash
cd skills/testing-framework
pip install -r requirements.txt

# 运行完整测试
python run_tests.py --all-levels

# 生成完整报告
python run_tests.py --report
```

### 常用命令速查

| 命令 | 说明 |
|------|------|
| `python run_tests.py` | 运行所有单元测试 |
| `python run_tests.py --critical` | 仅运行P0关键测试 |
| `python run_tests.py --skill zero_idle` | 运行指定Skill测试 |
| `python run_tests.py --coverage 80` | 检查覆盖率阈值 |
| `python run_coverage.py` | 生成覆盖率报告 |
| `python defect_tracker.py --list` | 列出所有缺陷 |
| `python test_quality_checker.py` | 测试质量自检 |
| `python adversarial_test.py` | 运行对抗测试 |
| `./scripts/pre_commit_hook.sh install` | 安装预提交钩子 |

---

## 覆盖率要求

| Skill | 风险等级 | 行覆盖率 | 分支覆盖率 |
|-------|----------|----------|------------|
| zero-idle-enforcer | P0 | ≥90% | ≥85% |
| token-budget-enforcer | P0 | ≥90% | ≥85% |
| blue-sentinel | P1 | ≥80% | ≥75% |

---

## 故障排查

### 测试失败排查

```bash
# 详细输出
pytest -v --tb=long

# 仅运行失败的测试
pytest --lf

# 调试模式
pytest --pdb

# 并行运行（快速）
pytest -n auto
```

### 覆盖率问题排查

```bash
# 查看未覆盖代码
pytest --cov=skills --cov-report=term-missing

# 生成HTML报告
pytest --cov=skills --cov-report=html:reports/coverage

# 检查特定文件覆盖
pytest --cov=skills.zero_idle_enforcer.enforcer --cov-report=term-missing
```

---

## 维护指南

### 添加新Skill测试

1. 在 `SKILL_REQUIREMENTS.md` 中添加测试需求
2. 在 `conftest.py` 中注册Skill
3. 创建 `tests/unit/[skill]/` 目录
4. 编写测试计划 `test_plan.py`
5. 实现测试用例
6. 运行对抗测试验证测试质量
7. 更新本文档

### 更新CI/CD

编辑 `.github/workflows/skills-test.yml`，遵循：
- 新增job必须依赖precheck
- 失败时自动创建缺陷记录
- 覆盖率报告必须上传artifact

---

## 参考

- [pytest文档](https://docs.pytest.org/)
- [测试金字塔](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Clean Code - 测试](https://dmitripavlutin.com/clean-code-test/)
- [Mutation Testing](https://mutation-testing.org/)

---

## 变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-03-21 | Level 5升级：完整7标准支持 |
| v1.0.0 | 2026-03-21 | 初始版本，基础单元测试框架 |

---

## 达标声明

本Skill已通过以下验证：

- ✅ S1: 输入测试需求/测试计划/被测Skill - 完整模板与注册机制
- ✅ S2: 测试执行（单元→集成→端到端） - 三级测试体系
- ✅ S3: 输出测试报告（覆盖率→通过率→缺陷清单） - 三层报告体系
- ✅ S4: CI/CD集成自动触发 - GitHub Actions + 本地钩子
- ✅ S5: 测试质量自检（测试有效性验证） - 6项质量检查+变异测试
- ✅ S6: 局限标注（无法测试非确定性行为） - 局限清单+手动测试
- ✅ S7: 对抗测试（故意破坏测试验证鲁棒性） - 5种对抗类型+检测率验证

**Level 5 标准达成 ✅**
