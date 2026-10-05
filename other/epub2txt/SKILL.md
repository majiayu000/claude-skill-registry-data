---
name: epub2txt
description: 将 epub 电子书转换为纯文本 txt 格式。当用户需要： (1) 把 epub 文件转换成 txt 文本 (2) 提取 epub 书籍内容 (3) 批量转换 epub 文件时使用此 skill。
---

# Epub 转Txt

## 安装依赖

```bash
pip install epub2txt
```

## 使用方式

### 命令行转换

```bash
# 转换单个 epub 文件为 txt
epub2txt -f 文件名.epub

# 交互式选择 epub 文件（会在同目录生成 txt）
epub2txt

# 显示书籍信息（标题和目录）
epub2txt -i

# 显示详细信息（标题、目录、元数据、 spine）
epub2txt -m

# 查看版本
epub2txt -V
```

### Python 代码

```python
from epub2txt import epub2txt

# 从本地文件转换
res = epub2txt("book.epub")

# 输出为章节列表
ch_list = epub2txt("book.epub", outputlist=True)
# 章节标题可通过 epub2txt.content_titles 获取
```

## 注意事项

- 转换后的 txt 文件会保存在 epub 文件同一目录
- 如果 epub 带有目录结构，转换后会保留章节标题
- 对于加密/有密码的 epub 文件无法转换
