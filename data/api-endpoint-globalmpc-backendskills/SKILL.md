---
name: api-endpoint
description: Rules for HTTP API endpoints. Use when adding or changing any endpoint (route, request or response shape, status codes), especially login and ones that read or change other users' data.
---

# API endpoint

Examples are TypeScript with `pg`. The rules apply to any stack.

The SQL is Postgres. On MySQL, `on conflict ... do update` is `on duplicate key update`, and `on conflict
do nothing` is `on duplicate key update id = id` (0 affected rows: the row was there; not `insert ignore`,
which hides other errors too). There's no `returning`: read the row back in the same transaction.

Anything that changes money, stock or balances, or calls a payment provider or email: also follow the
`data-integrity` skill (transactions, locks, idempotency).

## 1. Check who may call it, not just that they're logged in

Why: a logged-in user who changes the id in the URL reads or edits someone else's data (IDOR).

```ts
// Bad: any logged-in user can read any invoice
const { rows } = await pool.query("select * from invoices where id = $1", [id]);

// Good: scope the query to the caller; someone else's invoice looks the same as a missing one
const { rows } = await pool.query(
  "select id, number, total_cents, status from invoices where id = $1 and account_id = $2", [id, user.accountId]);
if (rows.length === 0) return sendError(res, 404, "not_found", "Invoice not found");
```

Admins or other roles get access through an explicit role check, never by skipping the filter.

Webhooks have no logged-in user, so the signature is the check: verify it on the raw request body with a
constant-time compare (`crypto.timingSafeEqual`, after checking both are the same length, or it throws)
before you parse or trust anything in it. Unsigned or wrongly signed: 401, and nothing changes.

## 2. Bad input is a 4xx, never a 500

Why: a 500 on bad input hides real errors in the noise. Bad values that slip through (negative amounts,
fractions) corrupt data.

- Validate the body and path params at the edge: types, integers where money and quantities are counted,
  ranges (`quantity >= 1`, `amountCents > 0`), required fields, ids that aren't numbers.
- Handle what a request can legally contain but your code doesn't expect, like the same item listed
  twice. Merge the duplicates or reject them with a 400, but don't let the request crash into a 500.
- Map expected database errors: unique violation (`23505`) → 409, foreign key violation (`23503`) → 404 or 400.

## 3. Limit how often anyone can try: login, codes, anything that sends or costs

Why: without a limit, a script guesses passwords or one-time codes until one works, or sends thousands of
emails and SMS on your bill.

```ts
// Bad: counts a failure only after checking it; 50 parallel guesses all see "0 failures so far"
if (failures.get(email) >= 10) return sendError(res, 429, ...);
if (!(await verifyPassword(password, hash))) failures.set(email, failures.get(email) + 1);

// Good: count the try first, in one atomic statement, in storage every server shares.
// The count starts over 15 minutes after the first try, and a successful login clears it.
const key = `login:${email.toLowerCase()}`;
const { rows: [c] } = await pool.query(
  `insert into attempts (key, n, since) values ($1, 1, now())
   on conflict (key) do update set
     n     = case when attempts.since < now() - interval '15 minutes' then 1 else attempts.n + 1 end,
     since = case when attempts.since < now() - interval '15 minutes' then now() else attempts.since end
   returning n`, [key]);
if (c.n > 10) return sendError(res, 429, "too_many_attempts", "Try again later");
if (!(await verifyPassword(password, hash))) return sendError(res, 401, "invalid_credentials", "Wrong email or password");
await pool.query("delete from attempts where key = $1", [key]);
```

- Key the limit on the account (and on the IP, with a looser limit).
- Once the limit is hit, refuse even the right password until the window ends. This is a trade-off:
  anyone who knows an email can lock that account for 15 minutes. Keep a way back in that skips the
  password (a reset link by email still works while locked), and alert on many lockouts from one IP.
- Keep the window short and clear it on success. A counter that never resets locks real users out for
  good, and lets anyone who knows an email lock that account.
- An unknown account and a wrong password get the same response, so nobody can find out which accounts exist.
- In-memory counters only work with one server. Use the database or Redis.

## 4. Take only the fields you allow, send back only the fields you mean to

Why: a request body copied straight into an update lets a user set `role`, `account_id` or their own
token. A `select *` sent back leaks password hashes and tokens.

```ts
// Bad: every key in the body becomes a column; the response is the whole row
await updateUser(user.id, req.body);
res.json((await pool.query("select * from users where id = $1", [user.id])).rows[0]);

// Good: pick the fields the caller may change by name, and name the columns you return
const { name, email } = req.body; // validated as in rule 2
const { rows: [u] } = await pool.query(
  `update users set name = coalesce($2, name), email = coalesce($3, email)
   where id = $1 returning id, name, email`, [user.id, name, email]);
res.json(u);
```

Lists get a maximum page size (say 100), whatever `limit` the client sends.

## 5. Use what the repo already has, and test it

Why: a second auth check, error format or DB helper drifts from the first, and reviewers have to catch it.

- Use the repo's auth, error format and database access. Errors never return a bare string or a stack trace.
- Add tests with the repo's test setup: the happy path, someone else's resource, and bad input.

## Make it yours

Your team's choices. A line that says "not set" means: follow what the repo already does.

- **API docs or collection:** not set.
- **Error format:** not set.
- **Someone else's resource:** 404, so nobody learns it exists.
