---
name: factory-status
description: Live Auto-Factory status audit — inspects real coding CLI conversations on jeff-ubuntu (/linux), captures tmux panes, audits evaluator/coder transcripts, verifies authentic test and commit progress, and reports 7-gate assessments.
---

# /factory-status — Live Auto-Factory Progress & CLI Conversation Audit

The Auto-Factory runs headless coding agents, independent stage-1 skeptics, and sealed evaluators on `jeff-ubuntu` (`/linux`). 

> [!IMPORTANT]
> **IRON LAW OF FACTORY STATUS: LIVE CONVERSATION INSPECTION MANDATE**
> Never report a PR as "making progress", "evaluating", or "remediating" based merely on high-level database state flags (`ATTESTED`, `RE_ROLL`, `QUEUED`). You **MUST** read the actual coding CLI conversations, transcripts (`~/.claude/projects/`), and live tmux capture panes on `jeff-ubuntu` to prove to yourself and the user that genuine work (reasoning, tool calls, tests run, git commits) is taking place.

---

## 1. Verify Host & Daemon Health (`/linux` @ `jeff-ubuntu`)

Check that the host is up and the daemon service is actively processing:

```bash
ssh jeff-ubuntu 'export PATH="/home/jleechan/.cargo/bin:$PATH";
uptime;
free -h;
systemctl --user status ai.dark-factory.daemon.service --no-pager | head -n 20;
'
```

---

## 2. Query Active AO Sessions & Tmux Terminal Panes

List active coding workers dispatched under Agent Orchestrator:

```bash
ssh jeff-ubuntu 'export PATH="/home/jleechan/.nvm/versions/node/v22.23.1/bin:$HOME/.local/bin:$HOME/bin:$PATH";
ao session ls -p worldarchitect;
tmux ls 2>/dev/null || true;
'
```

For any active tmux sessions (e.g. `ed3dd2670551-<id>:0`), capture the recent terminal buffer:

```bash
ssh jeff-ubuntu 'tmux capture-pane -pt <session_name>:0 -S -40 2>/dev/null || true'
```

---

## 3. Read Actual Coding CLI & Evaluator Conversation Transcripts

Inspect the latest JSONL transcripts in `/home/jleechan/.claude/projects/` to view exact agent prompts, reasoning, tool executions, and findings:

```bash
ssh jeff-ubuntu 'export PATH="/home/jleechan/.nvm/versions/node/v22.23.1/bin:$PATH";
python3 - << "EOF"
import glob, json, os

files = sorted(glob.glob("/home/jleechan/.claude/projects/*/*.jsonl"), key=os.path.getmtime, reverse=True)[:10]

for f in files:
    print("=" * 60)
    print(f"FILE: {os.path.basename(f)} (mtime: {os.path.getmtime(f)})")
    with open(f, "r") as fp:
        lines = fp.readlines()
    if not lines: continue
    user_prompt = ""
    last_assistant = ""
    for line in lines:
        try:
            data = json.loads(line)
            if "prompt" in data and not user_prompt:
                user_prompt = str(data["prompt"])
            if "message" in data and isinstance(data["message"], dict):
                role = data["message"].get("role")
                content = data["message"].get("content")
                if role == "user" and not user_prompt:
                    if isinstance(content, str): user_prompt = content
                    elif isinstance(content, list) and content and "text" in content[0]: user_prompt = content[0]["text"]
                elif role == "assistant":
                    if isinstance(content, str): last_assistant = content
                    elif isinstance(content, list) and content:
                        texts = [c.get("text", "") for c in content if isinstance(c, dict) and "text" in c]
                        if texts: last_assistant = " ".join(texts)
        except Exception: pass
    print("PROMPT HEAD:", user_prompt.replace("\n", " ")[:200])
    print("LAST ASSISTANT:", last_assistant.replace("\n", " ")[:300])
EOF
'
```

---

## 4. Audit Live Commits & Test Diffs

Verify that coding workers are actually writing tests and making forward-merge or remediation commits:

```bash
# Check worker branch commits and diffs
ssh jeff-ubuntu 'export PATH="/home/jleechan/.nvm/versions/node/v22.23.1/bin:$PATH";
cd /home/jleechan/projects/worldarchitect.ai && git fetch origin;
git log origin/main..<target_branch> --oneline -n 5;
'
```

---

## 5. Report Structured Status with Concrete Transcript Proof

Every factory status update MUST include:
1. **Host & Daemon State**: Uptime, load, and daemon task count.
2. **PR / Bead Matrix**: Full Markdown links (`🟢 [PR #<N>](url) [OPEN]`), branch names, and lifecycle states (`ATTESTED`, `RE_ROLL`, `DISPATCHED`).
3. **Verified Conversation Snippets**: Direct quotes from the Skeptic, Evidence Reviewer, or MiniMax coder transcripts proving whether tests passed, bugs were detected, or evidence was uploaded.
4. **Actionable Next Steps**: What the auto-factory is executing next autonomously.
