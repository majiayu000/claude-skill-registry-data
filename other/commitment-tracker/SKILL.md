---
name: commitment-tracker
description: Enforce immediate execution of any commitment made in a reply. Use this skill before finalizing ANY reply that contains a promise to act — phrases like "אדווח", "אעדכן", "אשלח", "אחזור אליך", "I'll send", "I'll report", "I'll follow up", "I'll update". Prevents the agent from saying it will do something and then not doing it.
---

# Commitment Tracker

## The Rule

**If your reply contains a commitment → execute it NOW, before sending the reply.**

No deferred promises. No "I'll do it after". Either do it in this turn, or don't say it.

## Commitment Trigger Words

Hebrew: `אדווח`, `אעדכן`, `אשלח`, `אוסיף`, `אחזור אליך`, `אבדוק ואחזור`, `אתעדכן`, `אשאיר הודעה`, `אעביר`

English: `I'll send`, `I'll report`, `I'll update`, `I'll follow up`, `I'll check`, `I'll let you know`, `I'll message`, `I'll notify`

## Protocol

Before finalizing any reply:

1. **Scan your reply** for trigger words above
2. **If found** → execute the committed action now (send the message, update the file, etc.)
3. **Only after execution** → include the result in your reply (e.g. "שלחתי ✅" not "אשלח")
4. **If you can't execute now** → rewrite the reply to not promise it (say "לא יכולה לשלוח כרגע כי X")

## Anti-Patterns

❌ "אדווח לנתנאל" → without actually messaging him  
❌ "אעדכן את הקבוצה" → without actually sending to the group  
❌ "אשלח לך סיכום" → without actually sending it  

## Correct Pattern

✅ Execute the action → then report: "עדכנתי את נתנאל ✅"  
✅ If blocked: "לא יכולה לשלוח כי אין לי את ה-JID — צריכה עזרה"

## Fault Tolerance — Intent Log

Before executing any commitment, write an intent record to prevent loss on gateway crash:

```bash
COMMITMENTS=/path/to/workspace/data/commitments.jsonl
mkdir -p $(dirname $COMMITMENTS)
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"action\":\"DESCRIBE_ACTION\",\"target\":\"TARGET\",\"status\":\"pending\"}" >> $COMMITMENTS
```

After successful execution, mark done:

```bash
# Append a done record (simpler than editing in-place)
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"action\":\"DESCRIBE_ACTION\",\"target\":\"TARGET\",\"status\":\"done\"}" >> $COMMITMENTS
```

### Recovery — On Every Session Start / Heartbeat

Scan for unresolved commitments:

```bash
python3 -c "
import json
log = '/path/to/workspace/data/commitments.jsonl'
try:
    lines = [json.loads(l) for l in open(log)]
    done_actions = {l['action'] for l in lines if l.get('status')=='done'}
    pending = [l for l in lines if l.get('status')=='pending' and l['action'] not in done_actions]
    if pending:
        for p in pending: print(f\"PENDING: {p['action']} → {p['target']} (since {p['ts']})\")
except FileNotFoundError:
    pass
"
```

If any `pending` found → **execute immediately and close the loop with the owner**.

### Cleanup — Delete Done Entries

After recovery scan, remove all `done` entries — they served their purpose:

```bash
python3 -c "
import json
log = '/path/to/workspace/data/commitments.jsonl'
try:
    lines = [json.loads(l) for l in open(log)]
    pending_only = [l for l in lines if l.get('status') != 'done']
    with open(log, 'w') as f:
        for l in pending_only: f.write(json.dumps(l)+'\\n')
except FileNotFoundError:
    pass
"
```

File only ever contains unresolved commitments — stays near-zero in normal operation.

## Scope

Applies to ALL surfaces: DMs, groups, internal actions, cross-PA messages.  
No exceptions for "it's obvious" or "they'll understand".
