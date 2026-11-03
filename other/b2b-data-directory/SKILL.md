---
name: b2b-data-directory
description: 数据目录管理 — 结构化知识库初始化、档案维护
when_to_use:
  - "结构化管理产品 / 客户 / 报价 / 合同 / 认证 / 物流知识库"
  - "用户提到「数据目录」「知识库管理」"
  - "不要用于：实时数据分析（用 b2b-market-analysis）"
triggers:
  - 数据目录
  - 公司档案
  - 产品目录
  - 客户目录
  - 初始化
  - 数据结构
  - trade目录
  - 数据初始化
  - data directory
  - company profile
  - product catalog
  - customer directory
  - initialization
  - data structure
  - 我的公司
  - 公司信息
  - 产品列表
  - 客户数据存在哪
category: 系统工具
version: 1.0.0
author: Foreign Trade Assistant
injection_prompt: |
  你是 b2b-data-directory 技能。当用户需要了解或初始化 ~/.trade/ 数据目录结构时，请执行以下步骤：
  
  1. 加载 skill: b2b-data-directory
  2. 根据请求类型执行：
     - 查看结构：描述 ~/.trade/companies/{slug}/ 下的完整文件树
       及其用途（company-profile.md / products.md / ...）
     - 初始化数据：使用 .trade-template/ 模板创建公司数据目录
     - 更新文件：读取现有文件 → 修改 → 写回（保留原有数据）
  3. 目录结构说明：
     ~/.trade/
     └── companies/{company-slug}/
         ├── company-profile.md    # 公司介绍
         ├── products.md           # 产品目录（含优势）
         ├── business-scope.md     # 业务范围 + 目标市场
         ├── agent-identity.md     # AI Agent 身份定义
         ├── competitors.md        # 竞争对手分析
         ├── certifications.md     # 证书与合规
         ├── marketing-strategy.md # 营销策略
         ├── sales-playbook.md     # 销售话术 + 异议处理
         ├── libraries/{lib-slug}/ # 文档库（按产品线）
         │   ├── index.md
         │   ├── changelog.md
         │   └── metadata.md
         └── clients/{client-slug}/ # 客户档案
  4. 返回：目录树 + 最近更新的文件 + 存储路径
---
