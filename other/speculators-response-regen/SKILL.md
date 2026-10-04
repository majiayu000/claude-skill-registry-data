---
name: speculators-response-regen
description: 重采样：把已有多轮对话数据的每条 assistant 回答丢弃，用 verifier 模型/vLLM 服务逐轮重生成，产出可直接进训练的预分词样本（每行含 input_ids/loss_mask）。依赖支持 return_token_ids 的 OpenAI 兼容 chat 服务（服务需由用户提前就绪，本技能不负责拉起服务）。触发：用某模型对某个数据集做重采样/重生成（如“对这个数据集用这个模型做重采样”）、把对话回答用模型重写、生成预分词样本/on-policy/MTP 训练数据。
license: Apache-2.0
---

# 重采样（响应重生成）

## 何时使用
用户要求把已有多轮对话数据的 assistant 回答用 verifier 模型重生成成预分词样本（每行 input_ids/loss_mask），可直通训练。

## 必填输入（用户未给 → 先问，不猜）
- verifier 模型路径（运行机本地可加载 tokenizer/checkpoint，作 --model）
- endpoint（OpenAI 兼容 /v1/chat/completions，须返回 prompt_token_ids 与 choices[0].token_ids）
- 输入对话数据（含 user/assistant 多轮；或用户指定原始数据来源）
- 输出目录、条数（--limit）；可选 --concurrency、--sampling-params
- verifier 服务须已就绪（本技能不拉起服务）；若要自建，先按 speculators 仓（v0.6.0）的方式起好服务，再把 endpoint 给本技能

## 执行步骤

### 0. DFX 预检（输入是原始多轮对话 jsonl 时先做；先质检数据，再决定是否动服务/资源）
- 命令：
  `python3 <本技能目录>/scripts/precheck_data.py --input <原始 jsonl> [--precheck-sample N(0=全量)] [--report-out <输出目录>/precheck.md]`
- 读报告分级处理（DFX 提前上报，不硬跑）：
  - high（JSON 解析失败/无会话容器/回合异常占比大）→ 停下，把报告给用户确认是否继续。
  - medium（无 assistant 轮、首轮非 user、assistant 回答过短、空值回合、超长上下文）→ 记录并默认继续，交付时列明。
  - low/info → 记录即可。
- 预检与 to_regen_input 用同一套解析：能通过即能被转换/重生成；被丢弃的行不会进入后续。

### 1. 服务就绪（先验证，不硬跑）
- 调用方已声明 endpoint：curl <endpoint 前缀>/v1/models 应 200；再发一次最小 chat（带 return_token_ids=true）确认响应含 prompt_token_ids 与 choices[0].token_ids。
- 未声明/探测不通：不自行乱起、不乱扫端口，也不代替用户拉起服务。询问用户现有 endpoint；或请其按 speculators 仓（v0.6.0）的方式自行起服务（模型需支持 return_token_ids）。
- 用户给出 endpoint 后，回到上一步做 return_token_ids 验证；验证通过前不进入重生成。
- 验证通过前绝不执行重生成；探测失败就上报，不硬跑、不伪造产物。

### 2. 准备输入
- 第 0 步预检通过（或用户明确跳过）后：
  - 用户给的就是重生成输入 → 直接用于第 3 步，保持行序与内容不变。
  - 需从原始多轮对话转换 → 用本技能 scripts/to_regen_input.py 转成 {id, conversations:[{from:"human"|"gpt",value}]}。

### 3. 执行重生成（官方脚本 + 本地数据，不改仓）
用本技能 scripts/run_rr_local.py 转发给 speculators 仓 response_regeneration 脚本：
```
cd <本技能目录>/scripts
python3 run_rr_local.py -- \
  --dataset <对应预设，如 sharegpt> \
  --data <第2步输入 jsonl> \
  --endpoint <endpoint>/v1/chat/completions \
  --model <verifier 模型路径> \
  --outfile <输出目录>/rr_out.jsonl \
  --limit <N> --concurrency <n> [--sampling-params '<json>']
```
长任务后台化并轮询；错误行写 <outfile>.errors.jsonl。

### 4. 校验与交付
- 校验产物每行含 id/primary_id/input_ids/loss_mask/text；抽查 input_ids 与 loss_mask 长度一致。
- 汇报：endpoint、参数、ok/errors/truncated、产物与日志路径、错误样例。
- （已做 DFX）附预检报告路径与 high/medium 风险结论。
- 日志与产物统一放用户指定输出目录（未指定先问）。

## 铁律
1. 服务未通过 return_token_ids 验证 → 不执行重生成。
2. 不擅自占用资源或拉起服务；verifier 服务由用户自行就绪后提供 endpoint。
3. 只重生成，不训练、不改变输入数据内容与顺序。
4. 不确定项（模型路径/条数/输出目录/是否停服务）先问用户。
