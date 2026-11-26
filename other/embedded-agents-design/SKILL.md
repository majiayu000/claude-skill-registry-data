---
name: embedded-agents-design
description: "'Add an agent', 'an AI assistant in the app', 'what may it do': before proposing, planning, building or changing a product's agent: its job, tools, what code enforces, what waits for a click."
---

# Design an embedded agent

**Agree on an agent card with the owner before building the agent.** It says what one agent is for, every tool it has, what code enforces and what waits for a person's click. Each agent gets its own, specialists included. Two cards appear below: the *agent card* describes an agent, and the *confirm card* is what a person clicks.

## When to write it

- **Put a draft agent card in the proposal or the discussion itself.** "The assistant handles billing" hides the decision. List the exact tools. For an action that waits for a click, say who clicks, how long the confirm card lives, that it works once, and that only the same person can use it.
- **Agree on the agent card before planning the work.** Keep it in the automation doc, the record of what each agent may do; apply the `shipping-artifacts` skill for that doc.
- **Choose the runtime after the agent card.** Apply the `embedded-agents-messages-api` skill by default, or `embedded-agents-agent-sdk` or `embedded-agents-managed` where their own conditions hold. Everything here works on all three.
- **Change the agent card first when a tool, a prompt or a limit changes.** It goes in the same change, and a new power is agreed before it is coded. A wording fix in a prompt that changes no rule needs no card change.

## The agent card

**Write down the exact tool list and every limit the owner agreed.** Give each number its source, or mark it as an assumption. Each tool has one kind:

- `reads` returns data the caller may see.
- `shows` has the app draw something, such as a checked row or a link.
- `writes` changes something the person can undo, and its row says how.
- `proposes` stores a request that only a click runs.
- `wrapper` is a tool the runtime adds: file, hosted and MCP tools.

```md
### Agent card: <agent directory name>

Job: <one job>
Who talks to it and where: <roles and surface, including agents that call it>
What it sees: <what is in front of it before any tool call>

| Tool | Kind | What it does |
| --- | --- | --- |
| `<tool_name>` | <reads / shows / writes / proposes / wrapper> | <effect and scope> |

Never: <actions or data outside its job>
Limits: <steps per run, money per run (per conversation on Managed Agents), runs per person per hour, specialist runs per message if several agents, kill switch>

| Enforced in code | Asked in the instructions | Left to the agent |
| --- | --- | --- |
| <rule and where it holds> | <instruction> | <choice> |
```

**Sort each rule by what somebody loses if the model ignores it.** Ask the owner: "if the model ignored this sentence, what would someone lose?" Money, another person's data, something sent or deleted, or spend without a limit goes in code. An annoyance goes in the instructions. Where nobody loses anything, leave it to the agent. Only the first column is a safeguard; a sentence in a prompt is a request.

**Cap the whole message when an agent can call other agents.** Count every specialist run that message starts, and check the cap before starting one. Each run keeps its own limits too.

### Agent card: support

**A filled card, for an example product with paid memberships.** Replace every row and number with your own.

Job: Answer billing questions for a membership product.  
Who talks to it and where: Signed-in members in the account support chat.  
What it sees: The chat so far, the caller's email and their current plan.

| Tool | Kind | What it does |
| --- | --- | --- |
| `list_invoices` | reads | Lists the caller's invoices. |
| `show_invoice` | shows | Draws an invoice row, after checking that it is the caller's. |
| `save_draft_note` | writes | Saves a private draft. Undo restores the version before it. |
| `propose_refund` | proposes | Proposes a full refund. The member clicks Refund invoice. |
| `proposal_status` | reads | Reports what became of recent proposals in this chat. |
| `list_files` | wrapper | Lists policy files. |
| `search_files` | wrapper | Searches policy files. |
| `read_file` | wrapper | Reads a policy file. |

Never: Change another member's records, access rights or payment details.  
Limits: 8 steps per run (assumption), $0.20 per run (assumption), 6 runs per person per hour (assumption). No specialists. A server switch stops runs and refunds.

| Enforced in code | Asked in the instructions | Left to the agent |
| --- | --- | --- |
| Every read and write is scoped to the session. An invoice id is checked before its row is drawn. | Explain how to undo a saved draft. | Whether to use a list. |
| Only the member who asked can click, once, within 10 minutes (assumption). The click checks refund eligibility again. | Point to the button; never say the refund happened. | Which example explains the policy. |
| The route and the runner hold the limits. The click checks the kill switch too. | Ask which invoice, if there are several. | How to phrase a follow-up question. |

## Actions and identity

**Give the agent a proposal tool for every action that can't be taken back.** That covers moving money, sending to someone outside, deleting, changing access or another person's record, and publishing. A `writes` tool is for what the person can undo, with the owner's agreement.

**Name who may click each proposal in the agent card.** The confirm card is for the person in the chat. When someone else approves, the tool files a request and that person decides on their own screen, which needs no agent code; apply the `saas-authorization` skill.

**Build the tools on every request, around the caller from the session.** No input names a person, an account, a customer, an email or a workspace. A resource id the model passes is checked against the caller's access. The agent can see the caller's email in its context, and cannot pass it to a tool.

## The confirm card

**Draw the confirm card from what code stored, never from the model's text.** `prepare` reads the record, checks that the caller may act on it, and returns the title, the lines and the button's words. A model's argument shows only where `prepare` puts it in a line on purpose. Escape every value as text, build links and document rows from checked ids, and show a URL the model wrote as plain text.

**Show the confirm card after every turn and on page load.** The order is text, lists, links, then confirm cards, even when the model never mentions one or the run fails. The stream's last `cards` event replaces the list on the page, even when it is empty, so keep reading past done or error. After a broken stream, fetch the list again.

**Require a separate click by the same person before the proposal expires.** A typed "yes" runs nothing; the agent points to the button. The click is its own request: it uses the proposal up, checks permission and the current state again, then acts. `proposal_status` tells the agent what happened.

**Treat a used proposal as used even when its outcome is unknown.** Each one runs at most once. A crash or an error while it runs, a timeout included, leaves it `running`, shown as "Check before trying again" with no button, and that person can't propose the same subject again. Whoever checks finds it in `agent_proposals` and closes it with `agent_proposal_finish`. Throw `Refused` only for a failure that certainly did nothing. Pass the proposal's id as the outside call's idempotency key.

**Keep one scope per chat, and reuse it everywhere.** A proposal belongs to a person and a scope: the conversation's id, or the agent's name where there is one chat. The tools, the stream and the page load use the same one.

## Wire the app

**Copy the files and supply the app's caller, actions and store.** The app's modules are `getCaller(request)` in `src/lib/caller.ts`, resolved from the session; `ACTIONS` in `src/lib/agent-actions.ts`; and `store` in `src/lib/proposal-store.ts`. Where people belong to workspaces, the caller's `id` names the workspace and the person, and `getCaller` returns `null` once they lose access; otherwise a former member still reads their cards. The code needs Zod 4, `server-only` and the Node runtime.

**Apply the proposal SQL as an app migration before serving requests.** It denies the browser roles its table and functions. Apply the `supabase-production` skill on Supabase. Give `sqlStore` the app's server client:

```ts
const store = sqlStore(async (fn, args) => { const { data, error } = await supabase.rpc(fn, args); if (error) throw error; return data; });
const pgStore = sqlStore(async (fn, args) => (await pool.query(`select * from public.${fn}(${Object.values(args).map((_, i) => `$${i + 1}`).join(', ')})`, Object.values(args))).rows);
```

**Write each action once, for preparing it and for the click.** The input is a zod shape that parses to itself: the click parses the saved arguments again, so a transform belongs in `prepare` and `run`. Where the terms can change between the card and the click, show the agent a revision, take it as an argument and refuse a stale one.

```ts
const refund = defineAction<Caller>()({
  name: 'refund',
  description: 'Propose a full refund of one of the caller’s invoices.',
  input: { invoiceId: z.string() },
  subject: ({ invoiceId }) => invoiceId,
  async prepare({ invoiceId }, caller) {
    const invoice = await eligibleInvoice(caller, invoiceId); // reads only; throws Refused when ineligible
    return { title: 'Refund paid invoice', lines: [{ label: 'Total', value: invoice.formattedTotal }], confirmLabel: 'Refund invoice' };
  },
  async run({ invoiceId }, caller, { idempotencyKey }) {
    await refundEligibleInvoice(caller, invoiceId, { idempotencyKey }); // checks again, then refunds
    return 'The invoice was refunded.';
  },
});
export const ACTIONS = { refund }; // src/lib/agent-actions.ts

// src/lib/agent-tools.ts: the one list that the route and the agent card's test both read
export const AGENT_TOOLS: Record<string, (caller: Caller, scope: string) => ToolSpec[]> = {
  support: (caller, scope) => [
    listInvoices(caller),
    showInvoice(caller),
    saveDraftNote(caller),
    proposeTool(ACTIONS.refund, caller, { store, scope }),
    statusTool(caller, { store, scope }),
  ],
};

// the turn route, once the caller, the scope and the limits are resolved
const tools = AGENT_TOOLS[agent](caller, scope).map((spec) => agentTool(spec));
for await (const ev of withCards(askAgent({ ...turn, tools }), () => readCards(caller, { store, scope }))) {
  if (ev.type === 'cards') send({ cards: ev.cards }); // beside the copied route's own branches
}
```

**One subject has one open confirm card.** The same proposal again keeps its id and gets a fresh 10 minutes (an assumption, `PROPOSAL_TTL_SECONDS`). Changed arguments, a changed card or another chat retire the old id, so a click approves exactly what was shown. The subject defaults to a hash of the arguments; name it where reworded arguments would be the same act.

**Refresh the open confirm cards after a click or a dismissal.** On `/api/agents/proposals`, `POST { id }` confirms, `DELETE { id }` dismisses and `GET ?scope=…` lists.

## Tests and files

**Test each agent card against the tools the route passes.** `agent-card.test.ts` reads the cards in `docs/automation.md` by their heading, and fails on a missing, extra or misnamed tool, a hosted or MCP tool with no row, and an input that names a person. The file and skill tools' rows are the runtime's own tests.

**Give each line enforced in code a test that fails without it.** Apply the `derive-tests` skill. For the refund, take the permission away after preparing, and assert that the click leaves the payment unchanged.

The tests need Vitest, `@electric-sql/pglite` and the app's `@/` alias.

| From `<skill dir>` | Copy to | Holds |
| --- | --- | --- |
| `templates/proposals.ts` | `src/lib/proposals.ts` | Tools, confirmation and card events |
| `templates/proposals.sql` | `db/migrations/agent-proposals.sql`, or the app's next migration | Storage, and a proposal used at most once |
| `templates/proposals-route.ts` | `src/app/api/agents/proposals/route.ts` | List, confirm and dismiss |
| `templates/proposals.test.ts` | `tests/unit/` | Proposal, route and stream tests |
| `templates/proposals.contract.ts` | `tests/unit/` | What any store must do |
| `templates/proposals.sql.test.ts` | `tests/unit/` | The same on PGlite; point it at the copied migration |
| `templates/agent-card.test.ts` | `tests/unit/` | Agent cards against registered tools |

Each rule's origin, the case that taught it, is in `receipts.md` beside this file; read it when a rule's edge is unclear.

## How you can tell it worked

The owner agreed to a card whose tools match the route's, by test. A confirm card survives a failed turn, and two racing clicks run the action once.
