---
name: compliance_check
description: 合规性检查
category: check
version: "1.0.0"
license: MIT
metadata:
  author: BidMaster Pro
  triggers:
    - 合规
    - 合规性
    - 硬性要求
---

# 合规性检查技能

## 检查逻辑
1. 从招标文件提取所有硬性要求
2. 逐条在投标文件中查找对应响应
3. 判断每项是否满足

## 输出格式
JSON: 包含total_requirements、compliant、non_compliant、items列表
