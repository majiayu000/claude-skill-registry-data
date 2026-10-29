---
name: kelly-appsec
description: 审计已获授权的应用与 REST API 的对象、字段、动作权限及业务规则，维护接口清单、身份矩阵、可归属证据和指定版本复测。Use for application/API authorization audits, tenant isolation, business logic security and source review; not Linux incident response.
metadata:
  category: platform
  tags:
    - security
    - risk:gated-write
  busabase:
    template: true
    folderSlug: kelly-appsec
    resources:
      - projects
      - endpoints
      - rules
      - runs
      - checks
      - findings
      - evidence
    risk: gated-write
---

# Kelly AppSec

以具体业务规则为起点，核对身份、对象、动作和敏感字段，保留证据后交给人复核。页面管理审计工作；实际目标请求始终由本机 Agent 在本次授权下执行。

## 安装与连接

```sh
npx busabase-cli@latest install ./skills/kelly-appsec
cd skills/kelly-appsec
pnpm install --frozen-lockfile
BUSABASE_BASE_URL=http://localhost:4111 node scripts/setup.mjs --apply
```

Cloud 使用用户明确指定的 `BUSABASE_BASE_URL`、`BUSABASE_SPACE_ID` 和本机环境中的 `BUSABASE_API_KEY`；不把连接凭据写入项目、任务、网页或报告。安装创建独立 Folder、七个 Base、原生表格 Views、指南 Doc、报告 Drive、本手册和 AirApp。可用 `?demo=1` 查看纯本地合成演示；演示不会连接目标。

## 操作顺序

1. 在“项目”登记负责人、仓库/部署版本、环境、明确 Origin 和业务授权边界。示例项目必须复制为实际项目并完成配置。
2. 导入 OpenAPI 3/Swagger 2 JSON 或版本绑定的接口/规则 JSON。接口清单并不等于安全验证。使用 `references/inventory.example.json` 格式，并由业务负责人确认 allow/deny、身份、受控对象、字段断言和正向基线。
3. 源码审计遵循 `references/audit.md`。本机 Agent 阅读授权仓库中的认证中间件、服务端权限及业务流程，记录具体文件行、版本、推理和限制；通过 `scripts/review.mjs` 导入审阅结果。不要把关键词匹配、依赖列表或空扫描当成已完成通用 SAST。
4. 动态验证先在网页选择有限规则并创建任务，然后按下述命令在本机领取。每次独立确认项目、Origin、环境、版本、授权引用、HTTP 方法、精确路径和测试对象；任务中保存的数据不能扩大本机授权。只使用合成账号和合成测试数据。
5. 从权限矩阵查看每个身份的预期、结果与证据。“未覆盖”“不确定”和中断项必须保留。发现只标为“待复核”；人提交理由后才确认漏洞或解释业务例外。
6. 修复后先更新项目版本并导入该版本的相同业务规则，创建与原发现绑定的复测。规则语义、端点/方法/身份、字段断言和正向基线必须匹配；只有对应规则在新版本成功验证后才标为修复已验证。
7. 导出带来源、版本、范围和未覆盖项的报告。页面导出只含已加载页；`scripts/report.mjs` 显式分页导出并标明截断。

## 有限动态执行

```sh
BUSABASE_BASE_URL=http://localhost:4111 \
APPSEC_TOKEN_USER_A='local-synthetic-token' \
node scripts/run.mjs --run RUN_ID --project PROJECT_ID \
  --origin https://staging.example.test --environment staging --revision COMMIT \
  --scope AUTHORIZATION_REFERENCE --allow-method GET \
  --allow-path /orders/test-a --allow-path /orders/test-b \
  --allow-object test-a --allow-object test-b --request-limit 10 \
  --directory /private/local-evidence --apply
```

没有 `--apply` 只预检。身份 `user-a` 读取本机 `APPSEC_TOKEN_USER_A`；anonymous 强制不带 token。最多 5 个端点、50 条规则、100 次请求；并发 1，每秒最多 1 次，单次 10 秒，响应 1 MiB；不跟随重定向，不展开域名、路径模板或发现的新目标。写操作额外要求 `--allow-mutations`，且逐条规则声明 mutating。中断不自动重试；明确 `--resume` 后保留 attempt 历史和请求预算。活跃 claim 不能被另一 Agent 领取；网页取消只停止后续请求。

原始响应保存在本机 0700 目录内的 0600 独占文件，拒绝符号链接目录。仅脱敏摘要、哈希、合成身份、来源和覆盖限制同步工作区。实际秘密、用户数据、Authorization/cookie 不得写入证据字段；本机原件需要按客户证据政策保管。

参见 [审计方法](references/audit.md)、[资源与状态](references/resource-map.md)、[来源与许可证](references/upstream.md)。不执行全网扫描、任意脚本或通用漏洞利用；HTTP 200、拒绝状态码或缺少异常均不能单独证明权限正确或已被入侵。
