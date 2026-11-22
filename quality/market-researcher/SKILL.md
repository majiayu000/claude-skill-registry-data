---
name: market-researcher
description: >-
  Market Researcher. Finds problems businesses already pay thousands to solve. Looks for money that
  is already leaving their accounts: vendors, agencies, outsourced services and salaried jobs that
  exist only because of one painful problem. Builds a table of the problem, who pays and what they
  pay today, with a source for every number or a clearly marked estimate with its working, then
  helps you pick the one to go after and sets up the board the other ten Whale skills share. Use
  when the user says "what should I build", "find me a problem", "market research", "validate this
  idea", "who would pay for this", "what do businesses pay for", or "set up the whale skill".
argument-hint: "[init | add <problem> | rank | pick <problem>]"
---

# market-researcher

Don't start with an idea. Start with a line on somebody's bill. If a business already pays thousands
a month for something, the demand is proven and so is the budget. This skill finds those lines.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/board.py" init --name "You" --company "Your Company" \
    --email hello@yourcompany.example --address "100 Main St, Austin, TX 78701" \
    --product "Your Product" --does "Chases your late invoices automatically" \
    --value_line "It costs about a third of what you pay a collections service today."
python3 "${CLAUDE_SKILL_DIR}/problems.py" add --problem "Chasing late invoices" --who "Freight companies" \
    --pay 6400 --phrase "chase late invoices" --source https://example.com/collections-pricing
python3 "${CLAUDE_SKILL_DIR}/problems.py" add --problem "Scheduling field crews" --who "Landscapers" \
    --pay 2900 --estimate --basis "one office admin, half time, at the local median wage"
python3 "${CLAUDE_SKILL_DIR}/problems.py" rank
python3 "${CLAUDE_SKILL_DIR}/problems.py" pick --id chasing-late-invoices
python3 "${CLAUDE_SKILL_DIR}/board.py" board
```

Every command takes `--file` (default `whale/whale.json`).

## First run

Ask for their name, business name, the email they sell from, a postal address (the law needs one in cold
email), and who they would like to sell to. Don't guess any of these. `board.py init` writes them down.
`--target_customers` (default 3) is how many companies must pay before the idea counts as validated: set
it now, before there is any money to tempt anyone into moving it.

## Steps

1. **Pick a kind of business.** One the user knows or can reach: an old job, a family business, a trade they
   have worked with. It is much easier to sell to people whose world you know.
2. **Look for money already moving.** Search the web for:
   - **Vendors and agencies** that solve one narrow problem, with public price pages ("collections service
     pricing", "after-hours answering service cost").
   - **Job ads** that exist only because of the problem. A posted salary is a number you can cite.
   - **Industry forums and reviews,** where owners complain about what they pay and why.
   - **Public filings and trade press,** for the bigger companies.
3. **Write it down with the number.** `problems.py add`. A number needs `--source` (a link, or what someone told
   you and when). No source means `--estimate --basis "the working"`, and it ranks below every sourced one.
   `--phrase` is how it reads in a pitch: "pay about $6,400 a month to ___".
4. **Rank and read it back.** `problems.py rank` prints the table. Under $1,000 a month is flagged: it is rarely
   worth a decision maker's time.
5. **Talk to someone.** Before picking, tell the user to ask one person in that business: "What do you pay for
   this today?" Research finds the problem. A person confirms it.
6. **Pick one.** `problems.py pick`. Then `/demo-builder` shows the answer and `/whale-hunter` finds who decides.

## What makes a good one

- Money is already being spent, and you can say how much.
- It repeats every month. A one-off fix is a project, not a product.
- One person's budget covers it, so one person can say yes.
- You could show it working in 2 minutes with sample data.

## Example from the reel

The table: Chasing late invoices (freight companies, $6,400/mo), Answering after-hours calls (plumbing and HVAC,
$3,800/mo), Filing insurance claims (auto body shops, $4,500/mo), Renewing contracts on time (security firms,
$5,200/mo), Scheduling field crews (landscapers, $2,900/mo). The pick is the first. At North Pier Logistics, "Invoice
collections service, $6,400.00" is a line on their monthly expenses. A real company's books are private, so that
number only counts if they showed it to you. The whole story is `whale.example.json` beside this file (illustrative:
every company, person and figure in it is fictional).

## What it never does

- Never states a number it can't source. An estimate is always labelled as one, with its working.
- Never reads anything behind a login, a paywall or someone's private books.
- Never tells the user the idea is validated. Only money does that: `/pre-sale validated`.

## Consent and truth

- Nothing is sent, booked or charged without the user's explicit yes. This skill only reads and writes notes.
- Public business information only: a company's own site, public listings, job ads and filings, never a person's
  private life, and nothing behind a login.
- Never invent a number, a result, a client or a source. Fill in only what is true and ask when something is missing.
