---
name: todays-date
description: You can check today's date using this tool.
---

# Your Skill Name

## Instructions
When you need to perform a web search to find the latest information, you must use this tool first to check the current year. This is crucial to prevent you from accidentally searching for information from a previous year (e.g., searching for "library name 2024" when the current year is 2025).

## Examples
Instructions
When you need to perform a web search to find the latest information, you must use this tool first to check the current year. This is crucial to prevent you from accidentally searching for information from a previous year (e.g., searching for "library name 2024" when the current year is 2025).


Examples
Example 1: Researching a library
User's Request: "Pythonのライブラリ requests の最新情報を教えて" (Tell me the latest information about the Python library requests.)

Your Internal Thought Process (Correct):

"I need to search the web for the latest information on requests. To ensure my search is for the current year, I must check today's date first."

(Use this tool: todays-date) -> Tool returns 2025-10-20.

"Okay, the current year is 2025. I will now search for 'requests library latest version 2025'."

Incorrect Action (to avoid): Searching for "requests library latest version 2024" without checking the current date.

Example 2: Researching a general topic
User's Request: "最新のマーケティングトレンドを調べて" (Research the latest marketing trends.)

Your Internal Thought Process (Correct):

"The user wants the latest trends. I need to use the current year in my search."

(Use this tool: todays-date) -> Tool returns 2025-10-20.

"I will search for 'latest marketing trends 2025'."

ヘルパースクリプトを実行：
```bash
python scripts/helper.py
```