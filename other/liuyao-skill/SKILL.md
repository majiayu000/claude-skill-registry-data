---
name: liuyao-casting
description: Normalize, calculate, and interpret one traditional Liu Yao event reading from six coin throws or a verified chart. Use for 六爻起卦, 摇卦, 三枚铜钱, 动爻, 世应, 用神, or a concrete event question; not for broad lifelong natal analysis.
---

# 六爻起卦

这是 6yao 的六爻完整入口：先把六次三枚铜钱结果稳定地转换成六条爻，再由可验证的计算器生成本卦、变卦、纳甲、六亲、六神、世应和旺衰字段，最后围绕一个具体问题形成证据链。模型不得凭记忆补算装卦字段。

## 输入门控

必须确认：

- 一个具体问题；不要把“今年整体运势”当作六爻单一事件；
- 六次投掷，每次恰好三枚钱，顺序从第一次到第六次；
- 每次硬币结果可标准化为 heads / tails 或 H / T；
- 可选提问时间、地点和时区，用于后续日辰、月建和时辰分析。

如果用户没有提供六次结果，询问是否让 6yao 自动投掷；自动投掷必须标注为随机起卦。不要在没有说明的情况下混合手动和随机结果。

## 固定计算规则

爻位从下往上：

1. 第一次投掷 = 初爻 = position 1；
2. 第六次投掷 = 上爻 = position 6；
3. 正面 heads 记 3 分，反面 tails 记 2 分；
4. 三正 = 9 = 老阳 = old_yang = 变爻；
5. 两正 = 8 = 少阴 = young_yin；
6. 一正 = 7 = 少阳 = young_yang；
7. 三反 = 6 = 老阴 = old_yin = 变爻。

阴阳二进制按 6yao 约定从上爻到初爻组成，用于识别本卦。变卦只翻转 old_yang / old_yin，少阳和少阴保持不变。没有变爻时，changedHexagram 为空，不要伪造“变卦”。

## 输出数据契约

每条爻必须包含：

- position：1–6；
- type：old_yang、young_yang、old_yin 或 young_yin；
- symbol：━━━ 或 ━ ━；
- isChanging：是否为老阳/老阴；
- coins：保留三个原始硬币结果及顺序。

提交 6yao 时使用 POST /api/divination/calculate-hexagram，并传入：

- yaos：六条标准化爻，position 必须严格等于数组序号 + 1；
- divinationTimestamp：ISO 时间，可选；
- timeInfo：year、month、day、hour、minute，可选；
- question：原始问题。

服务端会继续计算本卦、变卦、变爻位置、日主、卦宫、世应、六神、六亲和详细排盘。前端不要重复实现装卦逻辑。

## 解读流程

1. 固定原问题和时间范围，按题型选择用神；
2. 先看用神、世爻、应爻与日月旺衰，再看动爻、变爻、空破墓绝和合冲；
3. 至少形成两条“盘面字段 → 传统含义 → 对问题的影响”证据链；
4. 冲突信号必须并列，不得只摘取吉或凶的一边；
5. 先回答趋势和条件，再给一项现实核查、一个可逆行动和复盘时间；
6. 同一问题的追问沿用原卦，不因答案不合预期而重新起卦。

输出顺序为：一句结论、输入与起卦收据、关键盘面、证据链、利好/风险、行动建议、不确定性。结论不得脱离实际计算字段。

## 校验与边界

- 拒绝少于或多于六条爻；
- 拒绝非三枚硬币的投掷；
- 拒绝 position 不连续或不从 1 开始；
- 拒绝无法识别的 H/T 或 heads/tails；
- 保留原始投掷用于回查，但不得用硬币随机性替代现实建议；
- 不输出“必然发生”“百分百”等决策保证。

需要读取字段和示例时，使用 `references/casting-contract.md`。需要离线规范化时，运行 `scripts/normalize_cast.py`。生成解读时同时遵守 `references/evidence-contract.md`；高风险问题遵守 `references/safety-and-privacy.md`。
