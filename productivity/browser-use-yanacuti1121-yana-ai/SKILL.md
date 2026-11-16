---
name: browser-use
description: "Use when an AI agent needs to control a browser, automate web tasks, scrape pages, fill forms, or click buttons autonomously. Triggers on: 'browser automation', 'web agent', 'browser-use', 'AI browse', 'tự động duyệt web', 'điều khiển trình duyệt', 'scrape with AI', 'click button automatically', 'fill form automatically', 'web task automation'."
---

# Browser-Use Skill

Cho AI agent điều khiển trình duyệt thực sự — click, type, scroll, scrape, fill form.
Source: [browser-use/browser-use](https://github.com/browser-use/browser-use) (95K⭐, MIT)

## Install

```bash
pip install browser-use
uvx browser-use install   # cài Chromium nếu chưa có
```

## Workflow

### Step 1 — Setup env

```bash
# .env
ANTHROPIC_API_KEY=your-key
# hoặc OPENAI_API_KEY, GOOGLE_API_KEY
```

### Step 2 — Basic agent

```python
import asyncio
from browser_use import Agent, Browser
from langchain_anthropic import ChatAnthropic

async def main():
    browser = Browser()
    agent = Agent(
        task="Tìm giá iPhone 15 Pro trên tgdd.vn và trả về kết quả",
        llm=ChatAnthropic(model="claude-sonnet-4-6"),
        browser=browser,
    )
    result = await agent.run()
    print(result.final_result())
    await browser.close()

asyncio.run(main())
```

### Step 3 — Với context tùy chỉnh (login session, cookies)

```python
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig

browser = Browser(
    config=BrowserConfig(
        headless=True,           # chạy ẩn
        disable_security=False,
    )
)

async with await browser.new_context(
    config=BrowserContextConfig(
        cookies=[{"name": "session", "value": "abc", "domain": ".example.com"}]
    )
) as ctx:
    agent = Agent(task="...", llm=llm, browser_context=ctx)
    await agent.run()
```

### Step 4 — Multi-step task với custom actions

```python
from browser_use import Agent, Controller
from browser_use.browser.context import BrowserContext

controller = Controller()

@controller.action("Lưu dữ liệu vào file", param_model=SaveParams)
async def save_data(params: SaveParams, browser: BrowserContext):
    page = await browser.get_current_page()
    content = await page.content()
    with open(params.filename, "w") as f:
        f.write(content)
    return ActionResult(extracted_content="Saved", include_in_memory=True)

agent = Agent(task="...", llm=llm, controller=controller)
await agent.run(max_steps=20)
```

### Step 5 — Khai thác kết quả

```python
history = await agent.run()

# Kết quả cuối
print(history.final_result())

# Toàn bộ actions đã thực hiện
for action in history.model_actions():
    print(action)

# Screenshots từng bước
for screenshot in history.screenshots():
    # screenshot là base64 PNG
    pass

# URLs đã visit
print(history.urls())
```

## Use cases thường gặp

```python
# Scrape + extract structured data
agent = Agent(
    task="""
    Vào trang https://example.com/products
    Lấy tên, giá, và rating của 10 sản phẩm đầu tiên
    Trả về dạng JSON list
    """,
    llm=llm,
)

# Form automation
agent = Agent(
    task="""
    Vào trang https://form.example.com
    Điền: Name='Test', Email='test@mail.com', Message='Hello'
    Submit form
    Xác nhận đã gửi thành công
    """,
    llm=llm,
)
```

## Options

| Option | Default | Mô tả |
|--------|---------|--------|
| `headless` | `True` | Chạy không có cửa sổ |
| `max_steps` | `100` | Số bước tối đa |
| `use_vision` | `True` | Dùng screenshot để hiểu trang |
| `save_conversation_path` | `None` | Lưu toàn bộ conversation log |

## Lỗi thường gặp

| Lỗi | Fix |
|-----|-----|
| `Chromium not found` | Chạy `uvx browser-use install` |
| Agent loop không dừng | Giảm `max_steps`, thêm điều kiện dừng rõ ràng vào task |
| Page không load xong | Thêm "đợi trang load xong trước khi thao tác" vào task description |
