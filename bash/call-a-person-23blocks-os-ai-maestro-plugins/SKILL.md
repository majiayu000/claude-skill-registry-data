---
name: call-a-person
description: "Ring a person's phone (the AI Maestro app) from an agent and see whether they answered. Use when a person must act now and a message would wait: a decision blocks you, something is breaking, or the operator asked to be called. Not for news, progress or anything a message can carry; and there is no audio yet, so a call says who is calling and the person answers or declines."
allowed-tools: Bash
compatibility: Requires AI Maestro (aimaestro.dev) 0.106.20 or later with Bash shell access, curl and jq
metadata:
  author: 23blocks
  version: 1.0.0
---

# Call a person

A call rings the person's paired phones through push and shows "<you> is calling". They answer or decline in the app. There is no voice yet: say what you need in a message as well, because the call only gets their attention.

```bash
aimaestro-call.sh people                       # who you can call (every host you can reach)
aimaestro-call.sh person "Juan Pelaez"         # or an email, or a person id; prints the call id
aimaestro-call.sh wait <callId> --timeout 60   # exit 0 answered, 2 not answered, 3 still ringing
aimaestro-call.sh cancel <callId>              # stop ringing before an answer
aimaestro-call.sh end <callId>                 # hang up
```

- Ring once. If the call is not answered (exit 2 or 3), send a message and go on with other work; do not ring again and again.
- When `person` prints "has no push for calls yet", the phone will not ring: only the open app sees the call. Send a message.
- A name that matches more than one person is refused with the list of ids: use the id.
- Calls are recorded on your host (`GET /api/calls`). Nobody can stop you from calling, so the judgement is yours: urgent and needing that person, or not at all.
