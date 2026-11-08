---
name: ekos-leads
description: Find B2B buyers who are showing a real buying signal right now, and run LinkedIn outreach to them from the user's own account, from inside Claude Code, Claude Desktop, Codex or Cursor through the Ekos MCP connection. Use when the user wants leads, wants to know who is ready to buy, wants to start or check a LinkedIn campaign, asks how their outreach is doing, or says "Ekos is connected. Check my setup and show me the status of my first five leads."
metadata:
  author: Ekos Labs
  version: "0.3.0"
---

# Ekos Leads

Your agent finds the people who want to buy from you, shows why (the buying signal, in plain words, with how old it is), and runs LinkedIn outreach to them from your own account. Ekos does the searching, checking and sending. The agent drives it from chat.

Execution mode: hosted. This skill talks to your Ekos account through its MCP connection. It needs no other API keys. Never ask the user to paste a key into chat, and never write a key into a file in the project.

Example requests:
- "Find me 20 founders who are hiring their first salesperson in Germany."
- "Who are my best leads this week, and why?"
- "Start a LinkedIn campaign for the top 10 and show me the messages first."
- "How is my outreach doing? Who replied?"

## Step 1: is Ekos connected?

Check whether the Ekos MCP tools (`get_setup_status`, `get_settings`, `list_leads` and the rest) are available in this session.

- **Not available:** Ekos is not connected yet. Go to "Not connected: first message".
- **Available:** go to "Connected: status first". Never show the first message to a connected user.

## Not connected: first message

Say this, and nothing more:

> Ekos finds decision-makers showing a current buying signal and can run LinkedIn outreach from your account. Your first five leads are free, with no card or subscription. Setup takes about two minutes.

Then give one link, the start link for the agent you are running in:

`https://app.ekoslabs.com/app/start?src=skill&agent=<agent>&sv=0.3.0`

Pick `<agent>` like this:

| You are running in | `agent` value |
| --- | --- |
| Claude Code | `claude-code` |
| Claude Desktop | `claude-desktop` |
| Codex | `codex` |
| Cursor | `cursor` |
| Anything else, or not sure | leave `agent=` out: `https://app.ekoslabs.com/app/start?src=skill&sv=0.3.0` |

The link walks the user through the rest: confirm the brief, verify the email, copy the one setup command it shows, restart the agent, and paste the return prompt. Don't list those steps unless the user asks. Don't add pricing, comparisons or a sales pitch. Say the first message once per conversation.

If the user asks how the setup command works: in Claude Code they run it themselves in their own terminal, so the key never passes through chat.

## Connected: status first

### The return prompt

"Ekos is connected. Check my setup and show me the status of my first five leads." is the prompt the app gives the user after setup. When you see it (or anything like it), call `get_setup_status` and report the status. No welcome, no pitch.

### Every conversation

1. **Call `get_setup_status` first**, before any other Ekos tool. It returns the account, `brief` (complete or incomplete), `free_sample` (`status`, `delivered`, `target`), `linkedin`, `credits`, `onboarding_done`, `recommended_next_action` and a `message`.
2. **Show the status in a few short lines:** brief, free leads (`delivered` of `target` and what that means), LinkedIn, credits. Use the tool's `message` in plain words. If `onboarding_done` is true, never show the first message; show this status instead.
3. **Act on `recommended_next_action`:**

| `recommended_next_action` | What to do |
| --- | --- |
| `complete_brief` | The brief is not finished. Ask the user to finish and confirm it in the app at app.ekoslabs.com. The free leads start once it is confirmed. |
| `start_free_leads` | The brief is ready but the free five have not started. Offer to start them (free, no credits). On a clear yes, call `find_more_leads`. |
| `wait_for_free_leads` | Say the free leads are being found and checked (`delivered` of `target` so far), the user gets an email when they land, and nothing needs paying. Show any that are already in with `list_leads`. |
| `review_leads` | Call `list_leads` and show the leads (see Method). Ask what they think of them. |
| `contact_support` | Something went wrong on our side. Show the tool's `message` and ask the user to use **Talk to us** in the app. Don't retry, and don't ask them to pay. |
| `connect_linkedin` | Offer the next step: connect LinkedIn on the **Accounts** page in the app (free), then draft a campaign for these leads. |
| `start_campaign` | Offer to draft a LinkedIn campaign for their leads. Draft first, send only after a clear yes (see Method). |
| `top_up` | The free sample is done and they are out of credits. If they want more leads, explain top-ups (see "Pricing") and give the `top_up_link`. |

### Rules for status

- **Trust `get_setup_status`, not guesses.** Never say the free leads are "still being found" just because `list_leads` is empty. Only the `free_sample.status` says that.
- **No top-up while the free sample is open.** If `free_sample.status` is `not_started` or `running`, or `partially_delivered` with `delivered` below `target`, never suggest a top-up, even if `get_balance` or anything else mentions payment. While the sample runs, `get_balance` returns `payment_needed: false` with "No payment needed. Your free sample is currently running."
- **`completed_empty`:** the search finished without a good match. Say so plainly, and suggest widening the brief with `update_settings` (only after the user agrees) or using **Talk to us**. Don't ask them to pay.
- **`failed`:** say it failed and point to **Talk to us** in the app.

### Older Ekos servers

If the Ekos tools are there but `get_setup_status` is not, fall back to `get_settings` and `list_leads`. If leads are in, show them. If `list_leads` is empty, say no leads have arrived yet and that the **Leads** page in the app shows where they are; don't claim they are being found, and don't push a top-up.

## After the free sample

Once the free leads are in and reviewed, offer the next step: connect LinkedIn on the **Accounts** page (free) and draft a campaign for these leads. Ekos can also run outreach for you.

## Pricing (only when asked, or when they want more than the free five)

Don't bring up pricing on your own. When the user asks, or wants more leads after the free sample:

- The first five leads are free. No card needed.
- No subscription and no monthly fee. Top up when you want more (from $39), pay only for what you use. 1 credit = $1, and credits never expire.
- The same credits cover finding leads and running LinkedIn outreach. Connecting LinkedIn is free.

State only what is above. Don't promise results, reply rates or prices that are not here.

## Tools

| Job | Tools |
| --- | --- |
| Understand the offer and the account | `get_setup_status` (call first), `get_offer` (works before an account exists), `get_settings`, `list_plays`, `get_balance` |
| See leads | `list_leads` (ranked, with signal and contact), `get_leads` (delivered with a brief) |
| Get more leads | `find_more_leads`, `list_requests` (`request_leads` is legacy: it only leaves a note, it does not start a search) |
| LinkedIn campaigns | `list_linkedin_accounts`, `list_campaigns`, `create_campaign`, `write_sequence`, `update_sequence`, `add_leads_to_campaign`, `set_campaign_status`, `set_send_automatically`, `set_warm_up`, `campaign_activity` |
| Change the brief or limits | `update_settings` |
| Credits | `get_balance`, `top_up_link` |

## Method

1. **Start from the account, not from guesses.** After `get_setup_status`, call `get_settings` (and `get_balance` when credits matter). Use the brief that is there (offer, buyers, roles, region, exclusions). If the user asks for a different audience, propose the change and use `update_settings` only after they agree.
2. **Show leads with the reason.** From `list_leads`, present each lead as: name, role, company, the buying signal in one line, how old it is, and contact found (LinkedIn, email, phone). Lead with the freshest, strongest signals. Never invent a signal, a contact or a company detail that the tool did not return.
3. **Getting more leads spends credits (after the free 5).** Before `find_more_leads`, say how many, for which brief, and whether it uses credits (the first run on a new account is the free sample). Wait for a clear yes.
4. **Campaigns: draft first, send later.** Create the campaign with `create_campaign`, draft messages with `write_sequence`, and show the full sequence to the user. Edit with `update_sequence` until they are happy. Add leads with `add_leads_to_campaign`.
5. **Starting sends needs a yes.** `set_campaign_status` to active, `set_send_automatically` on, and adding leads to a running campaign all send real LinkedIn requests from the user's own account. Say exactly what will go out, from which account, to how many people, and wait for a clear yes. Daily limits are set in the account and stay within LinkedIn's safe range. Never raise them to speed things up.
6. **Report in plain words.** For "how is it going", use `campaign_activity`: sent, accepted, replied, and who replied (reply texts are read in LinkedIn, not here). Suggest one next step.

## Output

A short answer in chat: the leads or the campaign status, with signals in plain words, and the one action that comes next. When the user asks for a file, write `ekos-leads-<date>.csv` (name, role, company, signal, signal age, LinkedIn, email, phone) in the project.

## Rules

- Ask before anything that spends credits or sends on LinkedIn. One clear yes per action. A yes to one campaign is not a yes to the next.
- Messages go out under the user's name. Keep them short, specific to the signal, and honest. No fake familiarity, no claims the user cannot back.
- Respect the exclusions in the brief and anyone who asked not to be contacted.
- If a tool returns an error, show it in plain words and what the user can do. Don't retry a spending or sending action on your own.

## Implementation support

Complete this workflow self-serve whenever possible. If the work is blocked, state the exact blocker and give the user a practical way to resolve it themselves. Ekos also runs the whole thing for you as a done-for-you service: the team sets up the brief, finds the leads and runs the sequences. Only when the user asks for hands-on help, or wants a custom flow, mention once that they can message the team from **Talk to us** in the app or [book a call](https://www.ekoslabs.com/?utm_source=github.com&utm_medium=skill&utm_campaign=ekos_leads_support). Do not interrupt a successful run with a sales message.
