---
name: paddlepaddle-dev
description: PaddlePaddle 飞桨开发 — 环境搭建、模型训练、API 使用。涵盖高层 API (paddle.Model)、低层 API 踩坑、WSL GPU 配置、Context7 文档查询。触发词：飞桨、PaddlePaddle、paddle、MNIST、LeNet、paddle.Model。
tags: [paddlepaddle, deep-learning, cv, nlp, wsl, gpu]
category: mlops
---

# PaddlePaddle 飞桨开发

## 核心理念

> **起步用高层 API (`paddle.Model`)，不要手写训练循环。** 高层 API 自动处理 labels 格式、accuracy 计算等细节，避免踩坑。

## 环境搭建

### WSL2 + GPU（笔记本/单机）

```bash
# 1. 创建 venv（Paddle 3.3 需要 Python 3.9-3.13）
uv venv --python 3.12 .venv
source .venv/bin/activate

# 2. 安装 CPU 版
uv pip install paddlepaddle==3.3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# 3. 安装 GPU 版（WSL2 有 NVIDIA 驱动即可，不需要手动装 CUDA）
uv pip install paddlepaddle-gpu==3.3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# 4. WSL 必须追加 LD_LIBRARY_PATH（libcuda.so 在 /usr/lib/wsl/lib/）
export LD_LIBRARY_PATH="/usr/lib/wsl/lib:$LD_LIBRARY_PATH"
```

### 验证

```python
import paddle
print(paddle.__version__)           # 3.3.0
print(paddle.is_compiled_with_cuda()) # True
print(paddle.device.cuda.device_count())
paddle.utils.run_check()
```

### 依赖安装（PyPI 超时备用）

```bash
# 直连 PyPI 超时时，切清华镜像
uv pip install matplotlib pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### matplotlib 中文字体（图表中文显示为方块）

默认 DejaVu Sans 字体不含 CJK 字符，训练脚本生成的图表中文会变成方块（`Glyph missing from font(s)` 警告）。

**一次性修复**：

```bash
# 1. 检查是否有中文字体可用
fc-list :lang=zh | head -3

# 2. 如果没有，安装一个（推荐 SimHei/黑体 或 Noto Sans CJK）
# Arch: sudo pacman -S adobe-source-han-sans-cn-fonts
# 或从 Windows 挂载拷贝: cp /mnt/c/Windows/Fonts/simhei.ttf ~/.local/share/fonts/

# 3. 在脚本 import matplotlib.pyplot 之前插入：
import matplotlib.font_manager as fm
fm.fontManager.addfont('/path/to/simhei.ttf')  # 或 NotoSansCJK 等
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']   # 替换为实际字体名
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题
```

**批量为现有脚本打补丁**：在每个脚本的 `import matplotlib.pyplot` 前插入上述 5 行。字体路径通过 `fc-list :lang=zh` 确认。

## 开始前：先查文档，再写代码

> **读本 skill ≠ 不用查文档。** 本 skill 提供踩坑经验和常用片段，
> 具体 API 细节务必先查 Context7（`/websites/paddlepaddle_cn_zh`），
> 尤其是 3.x 版本间的行为差异。避免凭记忆写代码导致反复调试。

## 正确的 Hello Paddle（高层 API）

```python
import paddle
from paddle.vision.transforms import ToTensor

# 数据
train_dataset = paddle.vision.datasets.MNIST(mode='train', transform=ToTensor())
test_dataset = paddle.vision.datasets.MNIST(mode='test', transform=ToTensor())

# 模型（官方预定义 LeNet）
lenet = paddle.vision.models.LeNet()
model = paddle.Model(lenet)

# 配置 + 训练
model.prepare(
    paddle.optimizer.Adam(learning_rate=0.001, parameters=model.parameters()),
    paddle.nn.CrossEntropyLoss(),
    paddle.metric.Accuracy(),
)
model.fit(train_dataset, epochs=5, batch_size=64, verbose=1)
model.evaluate(test_dataset, verbose=1)

# 保存
paddle.save(model.state_dict(), 'output/mnist.pdparams')
```

高层 API 自动处理：
- label shape（不需要手动 squeeze）
- accuracy 计算（不需要手动 argmax）
- train/eval 模式切换
- 进度条 + 日志

## 低层 API 踩坑（仅当必须手写训练循环时参考）

### 坑 1：MNIST labels 是 (batch, 1) 不是 (batch,)

**现象**：`argmax(1) == labels` 比较结果异常，准确率 >100%

**原因**：Paddle 3.3 的 MNIST 返回 `labels.shape = (64, 1)` 而非 `(64,)`

**修复**：
```python
labels = labels.squeeze()  # 必须在 forward 前 squeeze
```

### 坑 2：.numpy() 返回标量（仅 loss 类）

**现象**：`loss.numpy()[0]` → `IndexError: too many indices`

**原因**：3.x 中 `loss.numpy()` 返回 0 维标量，不是 1 维数组

**修复**：
```python
loss.numpy().item()   # ✅
float(loss.numpy())   # ✅
loss.numpy()[0]       # ❌
```

**注意**：`model.weight.numpy()[0][0]` 仍然正常——weight 是 Parameter，shape 为 (1,1) 的 2D 数组，`[0][0]` 访问元素没问题。只有 **loss 等标量结果** 受影响。

### 坑 3：.astype('int') 行为变更
# model.weight 照常：
w = model.weight.numpy()[0][0]  # ✅ (2D array → 正常索引)
```

### 坑 3：.astype('int') 行为变更

**现象**：`astype('int')` 后 sum 的值不对

**修复**：用 `'int64'` 明确类型
```python
(logits.argmax(1) == labels).astype('int64').sum().numpy()
```

或用 `paddle.metric.accuracy()` 代替手动计算。

## Context7 文档查询

两个最佳 Library ID：

| ID | 内容 | Snippets | 用途 |
|----|------|----------|------|
| `/websites/paddlepaddle_cn_zh` | 中文官方文档 | 8060 | 快速开始、数据加载、模型训练 |
| `/paddlepaddle/paddle` | GitHub 源码 | 2649 | API 细节、Release Notes |

查询示例：
```
Context7 query /websites/paddlepaddle_cn_zh "高层API paddle.Model fit MNIST"
Context7 query /paddlepaddle/paddle "paddle.metric.accuracy API"
```

## 常用代码片段

### Normalize 正确写法

```python
# 高层 API 风格（ToTensor 就够了）
transform = ToTensor()

# 底层 API 风格
transform = Normalize(mean=[127.5], std=[127.5], data_format="CHW")
#                        ^^^^^^     ^^^^^^                  ^^^^^^^^
#                        不是 [0.5]！ data_format="CHW" 必须指定
```

### DataLoader 迭代

```python
loader = paddle.io.DataLoader(dataset, batch_size=64, shuffle=True)
for batch_id, data in enumerate(loader()):
    images, labels = data
    labels = labels.squeeze()  # 3.3 必须！
```

### 模型保存/加载

```python
# 保存
paddle.save(model.state_dict(), 'model.pdparams')
# 加载
model.set_state_dict(paddle.load('model.pdparams'))
```

## GPU 选型

| CUDA 版本 | 飞桨源 | 适用 GPU |
|-----------|--------|----------|
| CUDA 12.6 | `.../cu126/` | RTX 30/40 系列，A10 |
| CUDA 11.8 | `.../cu118/` | 旧卡保守选择 |
| CUDA 12.9 | `.../cu129/` | H100, Blackwell |

驱动要求：`nvidia-smi` 显示的 Driver Version ≥ 545.23.06（CUDA 12.6）。

## Paddle 与 PyTorch API 差异（迁移代码必读）

从 PyTorch 代码迁移到 Paddle 时，以下差异最容易踩坑：

### 差异 1：`nn.Linear.weight.shape` 顺序相反

| 框架 | weight shape | in_features | out_features |
|------|-------------|-------------|--------------|
| PyTorch | `[out_features, in_features]` | `shape[1]` | `shape[0]` |
| Paddle | `[in_features, out_features]` | `shape[0]` | `shape[1]` |

**踩坑场景**：替换预训练模型的分类头时：
```python
# ❌ PyTorch 写法 — Paddle 下会拿到 out_features
feature_dim = backbone.fc.weight.shape[1]  # 拿到 1000（输出），不是 2048（输入）

# ✅ Paddle 正确写法
feature_dim = backbone.fc.weight.shape[0]  # 2048（输入特征维度）
backbone.fc = nn.Linear(feature_dim, NUM_CLASSES)
```

### 差异 2：`parameters(filter=...)` 不支持

PyTorch 的 `model.parameters(filter=lambda p: p.requires_grad)` 在 Paddle 中**不存在**。

```python
# ❌ Paddle 不支持
optimizer = paddle.optimizer.Adam(
    parameters=model.parameters(filter=lambda p: not p.stop_gradient)
)

# ✅ 用列表推导替代
optimizer = paddle.optimizer.Adam(
    parameters=[p for p in model.parameters() if not p.stop_gradient]
)
```

### 差异 3：`import paddle` 作用域问题

`paddle` 在函数内部 import 后，外部类/函数无法访问。确保模块级 import：

```python
# ❌ 只在函数内 import — 外部类调用时 NameError
def get_system_info():
    import paddle  # 局部作用域

# ✅ 模块顶部 import
import paddle
import paddle.nn as nn
```

### 差异 4：MobileNetV3 的 classifier 结构

Paddle 的 `mobilenet_v3_small` 的 `classifier` 是 `nn.Sequential`：
```
Sequential(
  Linear(576, 1024),    # ← 取第一层 Linear 的输入维度
  Hardsigmoid(),
  Dropout(),
  Linear(1024, 1000),   # ← 不是最后一层！
)
```

替换时取**第一个** Linear 层（不是最后一个）的输入维度：
```python
if isinstance(old_cls, nn.Sequential):
    for layer in old_cls:
        if isinstance(layer, nn.Linear):
            in_features = layer.weight.shape[0]  # 576
            break
mobilenet.classifier = nn.Linear(in_features, 4)
```

### 差异 5：自定义模型必须实现 `__call__`

非 `nn.Layer` 子类的自定义模型不会自动获得 `__call__` 方法。如果类只有 `forward()` 方法，`model(tensor)` 会报 `not callable`：

```python
# ❌ 缺少 __call__ — model(tensor) 报错
class DummyTerrainModel:
    def __init__(self): pass
    def forward(self, x):
        return paddle.randn([x.shape[0], 4])

model = DummyTerrainModel()
output = model(input)  # TypeError: 'DummyTerrainModel' object is not callable

# ✅ 添加 __call__ 代理
class DummyTerrainModel:
    def __init__(self): pass
    def __call__(self, x):
        return self.forward(x)
    def forward(self, x):
        return paddle.randn([x.shape[0], 4])
```

## 参考

- 安装指南: https://www.paddlepaddle.org.cn/documentation/docs/zh/install/index_cn.html
- 快速开始: https://www.paddlepaddle.org.cn/documentation/docs/zh/guides/beginner/quick_start_cn.html
- GPU 架构表: https://www.paddlepaddle.org.cn/documentation/docs/zh/develop/install/Tables.html
- Context7: `/websites/paddlepaddle_cn_zh`, `/paddlepaddle/paddle`
- 模板: `templates/HelloPaddle1.py` — 老师参考代码（高层 API MNIST+LeNet）
- 实训作业流程: `references/training-workflow.md`
- 图表验证: `references/chart-verification.md` — 用 mmx vision 检查图表
