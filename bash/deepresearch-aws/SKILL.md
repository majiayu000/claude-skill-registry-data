---
name: deepresearch-aws
description: "Deep research assistant that transforms user questions into high-quality queries, calls Google Deep Research, and delivers structured results."
license: MIT
metadata:
  id: deepresearch-aws
  display_name: DeepResearch
  trigger: "deep research, research report, in-depth analysis, research, investigate"
  key_type: skill
  scope_platform: claude-code
  version: "2.0.0"
---

# Deep Research Skill (Google Gemini)

> **⚠ Important: Do NOT terminate the process mid-run**
>
> Deep research tasks are long-running end-to-end. **Do not kill or interrupt the script process until the task is complete.**
> - Research plan generation: approx. **1–2 minutes**
> - Deep research execution: approx. **10–30 minutes**
>
> `deepresearch.py` runs in the background; progress is relayed via a log file. `monitor.py` periodically reads the log and prints current progress. The task is only complete when the monitor detects a `[DONE]` marker.

---

## Step 1: Evaluate User Input  

After receiving user input, check whether the following information is missing:

- **Research purpose**: Decision-making, report writing, or general learning?
- **Time scope**: Latest developments or historical breadth?
- **Output format**: Comparative analysis, trend overview, or in-depth report?

If two or more of the above are missing, ask one question (never ask multiple at once). The question MUST be in the same language the user used — never mix languages.

If only one is missing, infer reasonably from the query without bothering the user.
If the information is sufficient, skip this step and proceed to enhancement.

---

## Step 2: Query Enhancement

Rewrite the user's raw input into a single fluent sentence or short paragraph. The query must read like a natural research brief — NOT a structured list, NOT bullet points, NOT section headers.

The sentence should naturally incorporate:
- the specific research subject
- a time scope (default: past two years)
- key perspectives (market / technology / competitive landscape, based on purpose)
- desired output format (comparative analysis / trend overview / in-depth report)

Example of a good query:
> "2024-2025年国内主流AI编程助手（通义灵码、Comate、CodeGeeX、豆包MarsCode）与国外领先产品（GitHub Copilot、Cursor、Devin）在代码生成质量、上下文理解、Agent自主能力和IDE集成体验上的深度对比分析报告。"

If the original question is broad, split into 2–3 independent natural-language sub-queries and call Deep Research separately for each.

After enhancement, show the rewritten query to the user and explicitly ask for confirmation. The entire message MUST be in the same language the user used.

Example (if user wrote in Chinese):
> 我将基于以下课题展开研究，请确认或告诉我需要调整的地方：
> [增强后的 query，一句话或简短段落]
> 是否确认？

Example (if user wrote in English):
> I will research based on the following query. Please confirm or let me know what you'd like to adjust:
> [enhanced query — one sentence or short paragraph]
> Shall I proceed?

**MUST**: Always include the enhanced query text before asking. Never ask for confirmation without showing the query first. Never mix languages — respond entirely in the user's language.

**MUST**: Once the user confirms, pass the enhanced query into `--query` in Step 3 with a directive prefix prepended. The prefix must be in the same language as the query and instructs the API to directly start deep research. Do NOT add any other modifications.

Prefix examples by language:
- Chinese: `深度研究以下内容：`
- English: `Deep research the following: `
- Japanese: `以下の内容を深く調査してください：`

So the final `--query` value = prefix + enhanced query. For example:
> `深度研究以下内容：2024-2025年全球AI编程助手与国内产品的深度对比分析报告。`

---

## Step 3: Launch Research Script in Background and Monitor Progress

### Step 3a: Generate paths and launch in background

Run exactly this single command block — no `ls`, no intermediate scripts, no wrapper files:

```bash
cd /workspace/app-*/skills/deepresearch-aws && LOG_FILE="/tmp/dr_google_$(python3 -c 'import time; print(int(time.time()))').log" && RESULT_FILE=$(mktemp /tmp/dr_aws_XXXXXX.md) && python3 scripts/deepresearch.py "<query>" --log-file "$LOG_FILE" --output-file "$RESULT_FILE" 2>&1 & WORKER_PID=$! && echo "[Launch] PID=$WORKER_PID | log=$LOG_FILE | result=$RESULT_FILE"
```

`INTEGRATIONS_API_KEY` is automatically injected by the platform — no manual setup required.

**MUST**: Pass the query from Step 2 with the language-appropriate directive prefix (as defined in Step 2) into `<query>`. Do NOT compress or rewrite the enhanced query itself.

- Single query: call directly
- Multiple sub-queries: call sequentially, max 3, then consolidate results

### Step 3b: Monitor loop (execute one command at a time — do NOT use a shell loop)

`monitor.py` checks the log once per invocation and exits immediately. Exit code meanings:

| Exit code | Meaning |
|-----------|---------|
| `0` | Task complete (`[DONE]`), **stop monitoring** |
| `1` | Task failed (`[ERROR]`), **stop monitoring** |
| `2` | Still running, continue monitoring |
| `3` | Process exited unexpectedly, **stop monitoring** |

Execute commands one by one as shown below. Sleep duration starts at 120s and increases by 30s each round (max 600s).
**After each monitor.py call, you MUST do both of the following (neither is optional):**
1. **Check exit code**: Stop if 0/1/3; sleep and continue if 2.
2. **Report progress (required)**: If monitor.py printed new content (not "No new progress..."), relay it to the user. If the output was "No new progress...", stay silent — do not output anything to the user.

```bash
# Check 1 (immediately after launch to see if initial log is available)
python3 scripts/monitor.py --log-file "$LOG_FILE" --pid "$WORKER_PID"
# exit 2 → continue; 0/1/3 → stop

sleep 120

# Check 2
python3 scripts/monitor.py --log-file "$LOG_FILE" --pid "$WORKER_PID"
sleep 150

# Check 3
python3 scripts/monitor.py --log-file "$LOG_FILE" --pid "$WORKER_PID"
sleep 180

# Check 4
python3 scripts/monitor.py --log-file "$LOG_FILE" --pid "$WORKER_PID"
sleep 210

# ... and so on, incrementing sleep by 30s each round up to 600s, until exit code is 0/1/3
```

---

## Step 4: Read Final Result

Once exit code `0` is received, read the result file:

```bash
cat "$RESULT_FILE"
```

Then save the content to the task directory as required by the system prompt.

**MUST NOT**: After reading the result, do NOT summarize, analyze, reformat, or add any commentary. Present the raw content of the file to the user as-is. The report is already complete — no second-pass processing of any kind.

---

## Reference Files

- **Research script**: `scripts/deepresearch.py` — Two-step API call (get session → send "Start Research" to stream research), authenticated via gateway, key progress nodes written to log
- **Monitor script**: `scripts/monitor.py` — Single-check mode, reads new log content and exits (exit code: 0=done / 1=error / 2=running / 3=unexpected exit)

## Notes
- When enhancing the query, do not change the user's research direction — only add structure and context
- If the Deep Research result is clearly off-topic, explain why and suggest the user rephrase the question

## Output Constraints
**MUST NOT** include any of the following in any response:
- Preamble explaining what you are about to do ("I'll perform...", "First, I've enhanced...", "I will now...")
- Announcements about file saving paths or task directories
- Sign-offs, greetings, or signatures ("祝好", "Miaoda", "秒哒" etc.)
- Language mixing — every response must be entirely in the user's language

**Correct example** (user wrote in Chinese):
> 我将基于以下课题展开研究，请确认或告诉我需要调整的地方：
> "2024-2025年全球AI编程助手与国内产品的深度对比分析报告。"
> 是否确认？

**Wrong example** (do NOT do this):
> I'll perform a deep research on this topic. First, I've enhanced your request...
> 我将基于以下课题展开研究...
> 生成报告后，我将其保存至 /workspace/...
> 祝好，秒哒 (Miaoda)
