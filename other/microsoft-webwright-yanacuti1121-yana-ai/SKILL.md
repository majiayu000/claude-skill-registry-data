---
name: microsoft--webwright
description: "Browser agent mã nguồn mở của Microsoft Research — agent viết Python/Playwright script thay vì click từng bước, script có thể reuse. SOTA 86.7% trên Online-Mind2Web."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Webwright là browser agent framework: thay vì predict discrete actions, agent viết Python/Playwright script tự do — script reusable, testable, maintainable như code thật.

## Install

```bash
pip install -e .
playwright install chromium
```

## Usage

```bash
python -m webwright.run.cli \
    -c base.yaml -c model_openai.yaml \
    -t "Book a flight from Hanoi to HCM City, cheapest option" \
    --start-url https://www.google.com/travel/flights \
    -o outputs/flight-booking
```

## Config

```yaml
# base.yaml
workspace_dir: ./workspace
max_steps: 50
screenshot_on_failure: true

# model_anthropic.yaml
model:
  provider: anthropic
  name: claude-sonnet-4-6
  api_key: ${ANTHROPIC_API_KEY}
```

## Core Pattern — Agent Loop

```
Task → Launch browser → Observe (screenshot + DOM)
     → Write Playwright script → Execute → Inspect failure?
     → Screenshot + re-observe → Refine script → Loop
     → Final artifact = reusable Python script + logs
```

## Slash Commands (Claude Code plugin)

```
/plugin install webwright@webwright

/webwright:run    -- single-shot task
/webwright:craft  -- tạo reusable CLI tool từ task description
```

## Điểm mạnh

- Script output là code thật — không phải click trace
- 86.7% Online-Mind2Web SOTA (2026)
- ~1.5k lines core — đọc hiểu dễ
- Support OpenAI, Anthropic, OpenRouter
- Trajectory + screenshots lưu disk để debug

## Khi nào dùng

- Automation web phức tạp (multi-step, conditional logic)
- Cần script có thể chạy lại, không phải one-off recording
- RPA-style workflow với LLM decision layer
- Web scraping có login, dynamic content

## Source

https://github.com/microsoft/Webwright · MIT
