---
name: crawl
description: 这个技能接收用户的需求，抓取theatlantic.com的文章
---

# **crawl**



# 输入
用户给出的文件和需求描述文本


# 任务要求如下，请按顺序完整执行

一、搞清楚当前所在的操作系统、终端运行（bash/windows command line/window powershell），当前所在的目录位置

二、首先检查运行环境是否就绪
```bash
cd scripts ; uv run check_and_run_uv.py
```

三、使用下面示例调用处理程序，并获取网页的内容

```bash
cd scripts ; uv run main.py
```
处理程序可能会执行很长时间，请一直保持等待知道程序执行完毕。务必不要中断程序的执行。

四、等待main.py完全执行完毕，如果main.py提示成功提取了页面内容，则使用下面的程序将获取到的页面内容，转换成可读的文章的内容

```bash
cd temp_scripts; uv run extract_articles.py
```
五、如果extract_articles.py处理结果提示的失败数量大于3，则按照以下要求，重新生成extract_articles.py程序（程序的路径为.claude/skills/crawl/temp_scripts/extract_articles.py）:

1、根据output/html目录下所有txt文件的内容，尽量尝试使用一个统一的xpath来获取页面的正文内容

2、重新撰写程序.claude/skills/crawl/temp_scripts/extract_articles.py，尽量参考原来的程序的内容，通过修改xpath来更新代码，使之可用

3、重新测试直到所有output/html目录下的文件内容都可以提取到正文内容

六、寻找output/articles/目录下重要的文章，并翻译

1、读取output/articles文件夹下所有文件的名称，并判断作为一个中国的知识分子会关心的内容，选取其中5篇文章进行翻译

2、手动调用skill技能translate, 创建一个包含选中的5篇文章的待办清单，然后逐一进行翻译。

# 注意事项

1、请保持scripts文件夹中所有程序是只能执行，不能做任何改动的

2、如果执行过程中需要生成新的程序，请放到temp_scripts文件夹中