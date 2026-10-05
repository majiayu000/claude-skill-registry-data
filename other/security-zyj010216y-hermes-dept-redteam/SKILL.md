---
name: devsec:security
description: |
  安全·审计 — 漏洞、密钥、注入、加固。调用前必须先经 router 选择。
---
# devsec:security

## 路由信号（L3 匹配详情）
触发词：安全、漏洞、CORS、依赖漏洞、requirements.txt、package.json、Dockerfile 扫描、HTTP 安全头、CSP、HSTS、JWT、token 安全、提示词注入、prompt injection、jailbreak、SAST、代码审计找漏洞、密钥、secret、API key、加固、渗透、安全评估。
不用于：性能审计（frontend:perf-seo）；纯代码质量评审（engineer:craft）。security-research 子项仅显式调用。


## 角色

安全审计与加固专家：CORS、依赖、Dockerfile、HTTP 头、JWT、注入、SAST、密钥扫描与加固。

## 使用步骤

1. 先看下方路由表，定位本次任务命中的子参考。
2. 只读取 `references/<子技能>/<子技能>.md`（及其引用的文件），不要整目录加载。
3. 多个主题命中时按「调用顺序」逐个读取；完成后如需交接，按 router 的交接规则走。

## 路由表

| 任务 | 子参考 |
|---|---|
| CORS 配置审计（通配符/反射 Origin/null origin） | references/cors-auditor/cors-auditor.md |
| 依赖漏洞与版本固定审计（离线库+OSV） | references/dependency-check/dependency-check.md |
| Dockerfile 不安全构建模式扫描 | references/dockerfile-scan/dockerfile-scan.md |
| HTTP 安全头与 Cookie 标志审计 | references/http-sec-audit/http-sec-audit.md |
| JWT 解码与安全审计（alg=none/过期/弱密钥） | references/jwt-inspector/jwt-inspector.md |
| LLM 提示词注入红队测试与韧性评分 | references/prompt-injection-tester/prompt-injection-tester.md |
| Python AST 静态安全分析（CWE 标注） | references/sast-lite/sast-lite.md |
| 硬编码密钥/凭据扫描 | references/secret-scanner/secret-scanner.md |
| 处理不可信输入/会话/第三方集成的加固 | references/security-and-hardening/security-and-hardening.md |
| Web/API/网络全谱安全评估（显式调用） | references/security-research/security-research.md |

## 调用顺序

单项扫描（secret-scanner / sast-lite / dependency-check / dockerfile-scan / cors-auditor / http-sec-audit / jwt-inspector）→ 综合评估（security-research，显式）→ 加固（security-and-hardening / prompt-injection-tester 红队）。

## 互斥与负向

不用于：性能审计（frontend:perf-seo）；纯代码质量评审（engineer:craft）。security-research 子项仅显式调用。

## 维护说明

本伞技能收纳了原 10 个平铺技能。新增子主题时：把原技能目录整体放入 `references/`，将其中的 `SKILL.md` 改名为 `<子技能名>.md`，再在本文件路由表加一行，最后运行 `~/.hermes/skills-archive/route-tests/route-test.py` 做回归。
