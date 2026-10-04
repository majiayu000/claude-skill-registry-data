---
name: apifox-test-case
description: Apifox 接口测试用例：test-case 与 test-data 的查询、创建、更新、删除、分类和运行；处理测试步骤、断言、提取变量、前后置处理器、数据集，以及“CLI 创建后前端测试步骤无法展示”等问题。
---

# 接口测试用例

> 前置条件：先阅读 `../apifox-cli/SKILL.md`。若旧总入口与本 skill 的领域规则冲突，以当前 CLI help 和本 skill 为准。涉及接口定义时按当前 CLI help 使用 endpoint、schema、folder 等命令；涉及多步骤流程时读取 `../apifox-test-scenario/SKILL.md`。

具体命令参数以当前 CLI help 为准。创建和更新接口测试用例时重点处理 categoryId 展示风险、test-case 与 test-scenario 边界、requestBody/processor/assertion/extractor 结构和运行验证边界。Agent 写入前必须用 `cli-schema validate` 校验 payload，写入后用 `get` 回读确认保存结构。

## 何时使用

- 创建接口下的自动化测试用例。
- 更新测试步骤、断言、提取变量、前后置处理器。
- 查看某个 endpoint 下有哪些测试用例。
- 按 caseId、endpointId、categoryId 运行接口测试用例。
- 创建或维护测试数据集。
- 排查“测试步骤无法展示”“断言不生效”“提取变量为空”。

## 不应使用

- 多接口流程编排或测试场景建模：转 `apifox-test-scenario`。
- 只运行已有场景、套件或 CI 命令：转 `apifox-test-automation`。
- 只改接口定义、请求参数或响应模型：按当前 CLI help 使用 endpoint/schema 等 API 设计命令。
- 只查看测试报告：按当前 CLI help 使用 `test-report`；执行和报告边界参考 `apifox-test-automation`。

## 核心概念

| 概念 | CLI 资源 | 说明 |
|------|----------|------|
| 接口测试用例 | `test-case` | 绑定接口 endpoint 的测试数据与步骤 |
| 测试分类 | `test-case category` | 测试用例分类；创建 case 前用于获取有效 `categoryId` |
| 测试数据集 | `test-data` | 可供迭代运行的数据 |
| 接口定义 | `endpoint` | case 的依赖对象，不等同 case 本身 |
| 测试场景 | `test-scenario` | 多步骤流程编排，边界不同 |

## 命令入口

使用当前 CLI help 查询 `test-case`、`test-data` 和 `apifox run --test-case` 的参数。`test-case category` 用于获取 `categoryId`；当前 `test-case category` 不支持 `--endpoint`。按接口查看已有用例时使用 `test-case list --endpoint <endpointId>`；`apifox run --test-case` 只接收 caseId。

把单接口用例导入测试场景时，不在本 skill 手写场景步骤；转 `apifox-test-scenario` 并使用：

```bash
apifox test-scenario import-steps <scenarioId> --project <projectId> --source test-case --endpoint <endpointId> --ids <testCaseIds> --sync manual
```

## 创建测试用例标准流程

1. 确认项目和分支。
2. 定位 endpoint：`apifox endpoint list/get`。
3. 必须执行 `apifox test-case category --project <projectId>` 获取有效 `categoryId`；如需查看某接口下已有用例，执行 `apifox test-case list --project <projectId> --endpoint <endpointId>`。
4. 如果已有类似 case，先 `apifox test-case list --project <projectId> --endpoint <endpointId>`，再 `get` 一个作为模板。
5. 获取并校验 `test-case-create` schema。
6. 构造完整 JSON，不要只写空壳 name/endpointId。
7. 创建后立即 `test-case get <caseId>`，确认后端实际保存结构。
8. 运行一次并生成本地 JSON 报告，确认 requestBody、处理器、断言和脚本在 runner 中实际生效。
9. 如上传报告，按当前 CLI help 使用 `test-report` 检查步骤详情；若报告缺详情，参考 `apifox-test-automation` 的本地/云端报告边界。

`categoryId` 是前端展示测试用例的关键必填字段，不是普通可选分类。无效 `categoryId` 可能导致 CLI `get/list` 能看到用例，但客户端分类列表里不可见、不可操作。创建前必须使用 `test-case category` 获取有效 ID。

## 更新测试用例标准流程

更新时必须先 `get` 原结构并基于完整结构修改，再校验 `test-case-update` schema，避免丢失已有步骤、断言、变量提取或处理器。`update` 不是 JSON Patch，也不会按 id 合并数组元素。

`test-case-create` 和 `test-case-update` schema 已包含前后置处理器、断言、提取变量和枚举值说明。首次编写 processor 时先看 schema，不要凭经验猜字段名、枚举值或旧格式。当前 `test-case-update` 会按 processor `type` 校验 `data` 结构；例如 `extractor` 会校验 `variableType/subject/shareScope`，`assertion` 会校验 `subject/comparison`，`delay` 的 `data` 必须是数字。

`test-case get` 回读结构里 `method` 可能是空字符串；这不代表前端方法展示异常，客户端通常从绑定 endpoint 展示 HTTP method。当前 `test-case-update` schema 已兼容该回读结构，更新时不要为了补 method 反向猜值，除非用户明确要改绑定接口或请求方法。

## 测试步骤展示规则

如果用户关心前端展示，必须额外验证：

1. 创建或更新后执行 `test-case get`。
2. 确认步骤、断言、提取变量、处理器字段被后端保存。
3. 确认字段不是空数组、空对象或写到错误层级。
4. 如果 CLI 返回成功但前端不展示，转 `apifox-cli-checkup`，先确认 project、branch、endpoint、categoryId 和回读结构是否一致。

## 内容和处理器结构

- `requestBody.data` 必须是字符串，不要把 JSON Body 写成对象。
- 多行 JSON Body、前置脚本和后置脚本用 `\n` 预格式化；这只影响客户端展示可读性，不改变执行语义。
- `preProcessors`、`postProcessors` 使用扁平结构 `{ id, type, data, defaultEnable, enable }`，不要写旧式嵌套 `{ type, config }`。
- 处理器建议带稳定 `id`，尤其是 `assertion`、`extractor`、`customScript`；缺少 `id` 可能 validate 通过但运行器或客户端解析异常。
- 提取全局变量时，`data.variableType` 使用 `globals`；如需指定生效范围，`data.shareScope` 优先使用 `PROJECT`。`TEAM` 是团队范围，可能依赖增值能力，除非用户明确要求团队范围，否则不要默认使用。
- 写入前照常跑 `cli-schema validate`，写入后 `test-case get` 回读确认保存结构。

示例：

```json
{
  "requestBody": {
    "type": "application/json",
    "data": "{\n  \"name\": \"Demo\",\n  \"description\": \"Readable in client\"\n}"
  },
  "postProcessors": [
    {
      "id": "postProcessors.0.customScript",
      "type": "customScript",
      "data": "pm.test('返回 ID', function () {\n  var body = pm.response.json();\n  pm.expect(body.data.id).to.exist;\n});",
      "defaultEnable": true,
      "enable": true
    },
    {
      "id": "postProcessors.1.extractor",
      "type": "extractor",
      "data": {
        "variableName": "project_pet_name",
        "variableType": "globals",
        "shareScope": "PROJECT",
        "subject": "responseJson",
        "expression": "$.name"
      },
      "defaultEnable": true,
      "enable": true
    }
  ]
}
```

## 断言和脚本规则

常规校验优先用可视化 `assertion`，自定义脚本只作为兜底能力。

断言规则：

- HTTP 状态码、JSON 字段存在/相等、文本包含等常规校验优先用可视化 `assertion`，不要默认写 `customScript`。
- 可视化断言字段使用当前 schema 枚举：HTTP 状态码用 `httpCode`，不要用 `responseCode`；JSON 字段用 `responseJson`，不要用 `responseBody`；全文包含用 `responseText` + `include`；比较符用 `equal`，不要用 `equals`。

```json
{
  "type": "assertion",
  "data": {
    "name": "HTTP 状态码为 200",
    "subject": "httpCode",
    "comparison": "equal",
    "value": "200",
    "path": ""
  },
  "defaultEnable": true,
  "enable": true
}
```

脚本规则：

- 自定义脚本只用于可视化断言覆盖不了的逻辑，例如复杂数组筛选、条件判断、二次请求、XML 转换或 schema 校验。
- Apifox 脚本运行时通过 `pm` 对象读写变量、访问响应和定义断言；脚本断言使用 `pm.test(...)` 包裹。
- 不要在 `pm.test` 外裸调用 `pm.response.json()`，避免空响应或非 JSON 响应导致错误难定位。
- 不要凭经验扩展运行上下文字段。

```js
pm.environment.set("variable_key", "variable_value");
pm.variables.set("variable_key", "variable_value");

pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("JSON value equals expected", function () {
  var jsonData = pm.response.json();
  pm.expect(jsonData.value).to.eql(100);
});
```

## 字段风险提醒

- 不要把 `test-scenario` 的步骤结构写进 `test-case`。
- 不要只写 case 名称和 endpointId，这会形成前端看起来没有步骤的空壳。
- 不要使用未验证的 `categoryId`。
- 不要仅凭 `test-case get` 返回的 `method` 为空判断前端展示异常；客户端可能从绑定 endpoint 展示 HTTP method，`test-case-update` schema 也兼容该回读值。
- 不要凭经验猜 processor/assertion/extractor 的字段名。
- 不要用 endpoint response 代替 test-case assertion。
- 不要把单接口 test-case 写成多步骤场景；test-case 不支持场景步骤间数据传递。
- 不要把场景里的 `{{$.1.response...}}`、`forEach` 等步骤间传递规则写进 test-case；如果需要跨步骤流程，创建或维护 `test-scenario`。
- 如果用户要把已有 test-case 作为场景步骤复用，使用 `test-scenario import-steps --source test-case`，导入后再 `get --with-case-detail` 回读并补业务参数值。

## 运行规则

- `test-case run <caseId>` 是按单个 case 运行。
- `test-case run --endpoint <endpointId>` 是按接口运行该接口下可运行 case。
- `--category <categoryId>` 必须和 `--endpoint <endpointId>` 一起使用。
- `apifox run --test-case <caseId>` 只支持 caseId，不支持 endpoint/category selector。
- `--environment` 可省略，但为了复现建议显式指定。
- 创建或更新后至少运行一次，确认 requestBody、处理器、断言和脚本在 runner 中实际生效；`cli-schema validate` 和 `test-case get` 成功不等于运行期一定正确。

## 常见恢复

| 现象 | 处理 |
|------|------|
| 测试步骤不展示 | `test-case get` 看真实结构，必要时转 `apifox-cli-checkup` |
| 断言不生效 | 读取现有成功 case 模板，对比 assertion 字段 |
| 提取变量为空 | 检查 extractor 层级、变量名、响应路径和执行报告 |
| run-config 404 | 确认 case/endpoint/environment/branch 均存在，再转 `apifox-cli-checkup` |
| endpoint 下找不到 case | 检查是否带了正确 `--branch` 和 `--endpoint` |
