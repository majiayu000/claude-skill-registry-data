---
name: distributed-claude-sender
description: Send prompts to a remote Claude instance on a VPS for distributed AI collaboration, different model backends, or independent context.
version: 1.0
---

# Distributed Claude - Sender

Send prompts to a remote Claude Code instance (Z.ai GLM backend) running on a VPS.

## When to Use

- **Different backend**: Get responses from Z.ai GLM models while you use Anthropic
- **Independent context**: Remote Claude maintains separate conversation history
- **Collaboration**: Two Claude instances working on different aspects of a problem
- **Testing**: Compare responses across different models

## Usage

```bash
# Replace YOUR_SERVER with your SSH alias or user@host
ssh YOUR_SERVER "cd ~/seed && ./chat.sh 'your prompt here'"

# With custom Doppler project/config
ssh YOUR_SERVER "cd ~/seed && ./chat.sh 'prompt' --project myproj --config dev"
```

## Architecture

```
You (Local Claude)
        |
        v
ssh YOUR_SERVER "./chat.sh 'prompt'"
        |
        v
Remote Claude (Z.ai GLM)
        |
        v
Response (with full remote context)
```

## Reset Remote Conversation

```bash
ssh YOUR_SERVER "rm /tmp/c.txt"
```

## Setup Remote Server

1. Clone seed repo on server: `git clone https://github.com/ebowwa/seed.git && cd seed`
2. Run setup: `./setup.sh`
3. Configure Doppler: `doppler login`
4. Start chatting: `./chat.sh "hello"`

## Example

```bash
# Ask remote Claude to analyze a file on the server
ssh YOUR_SERVER "cd ~/seed && ./chat.sh 'Read README.md and summarize the key points'"
```

## Tips

- The remote Claude has full context of its conversation history
- Each message via `chat.sh` includes the entire conversation log
- Use `rm /tmp/c.txt` on the server to reset remote memory
- The `chat.sh` script accepts `--project` and `--config` flags for Doppler flexibility
