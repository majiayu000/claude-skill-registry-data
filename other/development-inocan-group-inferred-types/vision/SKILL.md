---
name: vision
description: 这个技能接收用户给出的图片文件，按照用户的要求进行文字提取、图片描述、图片内容综述、图片内容解释、界面截图复刻等功能。
---

# **vision**的主要功能

## 图片内容描述
## 跟据给出的图片，使用css+html+js 精准的复刻图片的内容
## 跟据图片内容进行分析、推断、预测、总结

# 输入
用户给出的文件和需求描述文本


# 功能要求
首先检查运行环境是否就绪
```bash
uv sync
```
使用下面示例调用处理程序，并获取结果
```python
uv run vision_analyzer.py {image_file_path} {user prompt}
```
将输出的结果按照markdown格式直接输出给用户