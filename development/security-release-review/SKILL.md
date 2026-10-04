---
name: security-release-review
description: V10 安全闸门。用于项目完成后的上线安全检查、框架/语义分析、权限矩阵测试、攻击路径、security-gate 基线、证据制 GO/NO GO、动态角色/API 测试、Git 历史密钥扫描、可执行滥用测试、补丁草案、上线后守护、日志异常分析、安全数字孪生、PR 语义审查、审批/SLA、组织控制面、AI/Agent 红队、餐饮业务合规、复测和 CI 输出。
---

# Security Release Review V10

## 目标

V10 是“可验证、可复测、可运营的商业级上线安全控制平面”。它保留 V1-V5 的安全扫描、修复计划、复测和 GO/NO GO 能力，并按阶段新增：

- V6：语义安全审查、权限矩阵自动测试、补丁草案、攻击路径图、餐饮专项测试包、污点/数据流审查。
- V7：上线后 24/72 小时守护、运行时日志分析、异常检测规则、事故演练、安全债务看板、多租户深测。
- V8：安全数字孪生、业务规则验证、授权攻击模拟、回归测试库、跨项目基线、依赖信誉评分。
- V9：PR 语义审查、安全测试生成、风险知识库、上线审批流、安全 SLA、误报反馈。
- V10：组织安全控制面、策略继承、安全记忆、自动修复 PR 计划、真实流量回放计划、AI Agent 行为审计、发布契约、运行时防护建议、安全成熟度评分。
- 框架识别与专项规则：Next.js、Express、NestJS、FastAPI、Django、Laravel、ASP.NET Core、Spring 等。
- `security-gate.yaml` 基线配置：角色矩阵、预算、上传限制、kill switch、公开 API。
- Git 历史密钥扫描。
- 可执行 `security-abuse-tests.mjs` 烟测脚本。
- `PATCH_STRATEGY.md` 补丁策略。
- `PR_SECURITY_DELTA.md` PR 新风险摘要。
- 证据制报告：没有测试证据不能直接 `GO`。
- API 地图和 API 滥用测试。
- 动态测试模式，支持本地/staging `--base-url`。
- SARIF/JUnit CI 输出。
- 云/运行时配置、供应链、AI 红队、餐饮业务合规检查。
- `RISK_ACCEPTANCE.md` 风险接受机制。

最终必须明确给出：

- `GO`: 可以正式商业上线。
- `CONDITIONAL GO`: 可内部测试或小范围测试，但有条件。
- `NO GO`: 禁止上线。

## 什么时候触发

用户要求上线前安全检查、release gate、launch readiness、威胁建模、API 越权测试、AI/Agent 安全、成本攻击、动态测试、供应链检查、餐饮自动回复合规或修复后复测时使用。

只用于用户拥有或明确授权的项目。不要攻击第三方，不要绕过风控，不要触发生产短信/支付/AI 成本或破坏性动作，除非用户明确授权。

## 输入

- `--project`: 项目根目录。
- `--out`: 输出目录，默认 `security-review`。
- `--config`: `security-gate.yaml/json` 或兼容旧 `security-policy.yaml/json`。
- `--previous`: 上一次 `security-review.json`，用于 retest。
- `--base-url`: 已运行的本地或 staging 地址，用于 dynamic。

## 输出

`scripts/security_audit.py --mode all` 生成：

- `security-review.json`
- `SECURITY_RELEASE_REVIEW.md`
- `THREAT_MODEL.md`
- `API_SECURITY_MAP.md`
- `API_ABUSE_TESTS.md`
- `FRAMEWORK_SECURITY_REVIEW.md`
- `SECURITY_GATE_BASELINE.md`
- `EXECUTABLE_SECURITY_TESTS.md`
- `AI_RED_TEAM_TESTS.md`
- `AGENT_TOOL_RISK_REVIEW.md`
- `COST_ABUSE_REVIEW.md`
- `CLOUD_RUNTIME_CONFIG_REVIEW.md`
- `SUPPLY_CHAIN_REVIEW.md`
- `GIT_HISTORY_SECRETS.md`
- `RESTAURANT_COMPLIANCE_REVIEW.md`
- `DYNAMIC_SECURITY_TEST.md`
- `EVIDENCE_MATRIX.md`
- `SECURITY_FIX_PLAN.md`
- `PATCH_STRATEGY.md`
- `SEMANTIC_SECURITY_REVIEW.md`
- `PERMISSION_MATRIX_TESTS.md`
- `AUTO_PATCH_DRAFTS.md`
- `ATTACK_PATH_GRAPH.md`
- `POST_LAUNCH_GUARD.md`
- `RUNTIME_LOG_ANALYSIS.md`
- `SECURITY_DIGITAL_TWIN.md`
- `PR_SEMANTIC_REVIEW.md`
- `RELEASE_APPROVAL_WORKFLOW.md`
- `ORG_SECURITY_CONTROL_PLANE.md`
- `RELEASE_CONTRACT.md`
- `SECURITY_MATURITY_SCORE.md`
- `SECURITY_RETEST_REPORT.md`
- `PR_SECURITY_DELTA.md`
- `RISK_ACCEPTANCE.md`
- `RELEASE_GO_NO_GO.md`
- `security-abuse-tests.mjs`
- `security-review.sarif`
- `junit-security.xml`

## 执行

全量检查：

```bash
python scripts/security_audit.py --project . --mode all --out security-review
```

带策略配置：

```bash
python scripts/security_audit.py --project . --config security-gate.yaml --mode all --out security-review
```

动态测试：

```bash
python scripts/security_audit.py --project . --mode dynamic --base-url http://localhost:3000 --out security-review
```

复测：

```bash
python scripts/security_audit.py --project . --mode retest --previous security-review/security-review.json --out security-review-retest
```

CI 门禁：

```bash
python scripts/security_audit.py --project . --mode release-gate --config security-gate.yaml --out security-review
```

自测：

```bash
python scripts/validate_skill.py .
python scripts/security_audit.py --self-test
```

## V10 GO 规则

- `GO` 需要无 `critical/high` 阻断项，并且 policy 要求的动态证据已存在。
- 没有动态/API 证据时，即使没有扫描 findings，最多 `CONDITIONAL GO`。
- `NO GO`：密钥泄露、Git 历史有效密钥、admin 无鉴权、IDOR/BOLA、短信/AI/上传无限制、AI key 在前端、公开上传、Webhook 无签名、生产 debug、敏感日志等。
- PR 模式必须重点看 `PR_SECURITY_DELTA.md`；新增 `critical/high/blocks_release=true` 不应合并。

## 风险接受

默认只有 `medium/low` 可通过 `RISK_ACCEPTANCE.md` 接受，必须包含负责人、过期时间、补偿控制、复查日期。`critical/high` 和 `blocks_release=true` 不应接受，必须修复。

## 参考

阅读 `references/` 下的指南：证据门禁、云配置、供应链、餐饮合规、风险接受、API 滥用、AI Agent、安全清单和发布规则。
