---
name: setup
description: Connect looot step by step - sign in through the browser, confirm the connection with a free balance check, then run one free catalog search. Use when looot tools are missing, answer unauthorized, or the person asks how to set looot up.
disable-model-invocation: true
---

# Set up looot

Walk the person through these steps one at a time. Wait for them where a step needs them.

1. **Account.** Ask if they have a looot account. If not, send them to
   https://looot.ai/auth/sign-up (email or Google). A new account gets $2 of free credit once, after
   they confirm the email and sign in.
2. **Sign in.** The plugin already adds the looot MCP server (`https://api.looot.ai/mcp`). Sign-in is
   OAuth in the browser, so no key goes into any file or into this chat. Tell them:
   - Claude Code: type `/mcp`, pick the looot server, choose **Authenticate**, pick the workspace on
     looot.ai and click **Connect**.
   - Codex: run `codex mcp login looot` in their own terminal and keep it open until they approve in
     the browser.
   - If they added looot by hand before (`claude mcp add looot ...`), the tools can show twice. They
     can keep one: `claude mcp remove looot` removes the manual entry.
3. **Check.** When they say they approved, call `balance` with `{}`. Report `available` in dollars. If
   it is $0 on a new account, ask them to click the confirmation link in their sign-up email and sign
   in again. If the call still answers unauthorized, repeat step 2.
4. **First free call.** Call `search` with `{"query": "technology stack a website uses", "limit": 3}`
   and show the rows as a short table: provider, price, endpoint id. Searching is free.
5. **Next.** Say what they can ask for now, for example "find the work email of the head of sales at
   acme.com" or "what does Google show for best crm in the US". Point to `/looot:find` to compare
   providers and prices, and `/looot:balance` to check credit or top up.

Never ask for a password, an API key or a token in the chat.
