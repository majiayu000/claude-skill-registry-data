---
name: accounts
description: Let the tool apply on job boards that want an account (Workday today). Use when the user says /accounts or /account, with or without a subcommand (signin, password, add, setup, clear, off, on, forget, gmail), "Workday", "sign in for me", "why are Workday jobs skipped", or asks about verification emails.
argument-hint: "[signin <employer> | password <employer> | add workday | setup <employer> | clear | off | on | forget <employer or all> | gmail]"
model: claude-sonnet-5-5
effort: medium
---

# /accounts

The user types a short command; you run the tool for them. They should
never have to type `npx` or edit a file. `docs/ACCOUNTS.md` is the
reference. Everything here is off until the user turns it on.

There are three ways to use it. **Lead with the first.** Offer the second
when a session has ended, and the third only when they ask for less work
per employer, and say that it is experimental.

1. They sign in once at an employer, themselves; the tool keeps the session.
2. They store that employer's password; the tool signs in when the session ends.
3. Experimental: the tool makes accounts where they have none.

## `/accounts` with nothing after it

Run `npx jev accounts`. If nothing is set up, this is the guided setup:

1. Say in two sentences what this is: Workday employers each want an
   account, and the simplest way is to sign in once yourself.
2. Run `npx jev status` and name the two or three Workday employers with
   the best jobs they are missing (`npx jev queue` lists skipped jobs with
   `workday` as the reason; use the companies, not ids).
3. Ask which one to start with, then do `/accounts signin <employer>`.
4. After it works, run `npx jev discover` and say how many jobs at that
   employer are now in the queue. Offer `/apply`.

If something is set up, say what, what waits for them, and the next step.

## What the user can type

| They type | You do |
|---|---|
| `/accounts signin <employer>` | Show `npx jev accounts signin <employer>` in a `bash` block. It opens the employer's page in the tool's Chrome window; they sign in there themselves. Tell them to click Run and then look at that window. |
| `/accounts password <employer>` | Run `npx jev accounts password <employer>`. A window opens on their Mac; they type that employer's password there, twice. You never see it. With no employer it stores the one password they use on accounts they already had. |
| `/accounts browser <employer>` | Only when they say they saved that employer's password in the tool's Chrome and want the tool to use it. Run `npx jev accounts browser <employer>`. The tool then presses Sign In once that browser has filled the page in; it types nothing and never reads the password. `--off` takes it back. |
| `/accounts add workday` | The questions below. Run it with `--preview` first and read what it allows back to them. Save only after a yes, with exactly the flags they agreed to. |
| `/accounts setup <employer>` | Show `npx jev accounts setup <employer>` in a `bash` block. It signs in, or makes the account. They click Run. |
| `/accounts clear` | `npx jev accounts clear`, after they fixed what paused an account. |
| `/accounts off` / `/accounts on` | `npx jev accounts off` / `on`. Say that everything set up is kept. |
| `/accounts forget <employer or all>` | Run it without `--yes` first and read back what it removes. After a yes, run it with `--yes`. Say that the account at the employer still exists. |
| `/accounts gmail` | Only if they want verification emails read for them. Say first that the default needs no setup: they click the link and type `/resume`. If they still want it, walk through "Verification emails" in `docs/ACCOUNTS.md` one step at a time. Do not promise how long it takes. Then `/accounts gmail <file>` runs `npx jev gmail connect --client <file>`. |

After any of these, run `npx jev accounts` and read the result back.

## The questions for `add workday`

Say that this is experimental before asking. Each is a separate yes:

1. May the tool **make** an account where an employer has none for you?
   Each is a real account at that employer, in your name. (`--create`)
2. May it tick the box that accepts each employer's **candidate-account
   terms** for you, without your reading them one by one? A marketing box
   is never ticked. (`--terms`)
3. May it read the **verification email** an employer sends? That needs
   Gmail connected. Without it you click each link. (`--verify-email`)

They choose no password: each new account gets its own random one, kept in
their Keychain. `--max-new 3` is the default.

## What you never do

- **Never ask for, read, type or repeat a password, a code or a token**,
  in chat, in a file or in a command. Never read the Keychain, `.env` or
  the tool's Chrome profile.
- **Never start anything that signs in or signs up at an employer.** That
  is `accounts signin`, `accounts setup`, `apply` on a Workday job in a
  real run, `daily` and `resume --submit` when Workday is set up. Show the
  command in a `bash` block; the app puts a Run button on it. A rehearsal
  (`--dry`) of a Workday job signs in to an account they have and makes
  nothing; treat it the same way.
- **Never pass a human check**: a CAPTCHA, a phone code, a passkey, or the
  code a board emails because it suspects a robot.
- **Never allow more than they said.** No flag they did not agree to, and
  no edit to `data/accounts.json` by hand.
- If the permission system declines a command, do not try another way.
  Show the command in a `bash` block for them to run with one click.

## When a sign-in stops

The reason is on the job's row (`/status`). In their words:

- **The employer refused the password.** Either they sign in themselves in
  the tool's Chrome window, or they type `/accounts password <employer>`
  with the right one. Then `/resume`.
- **A robot check, a phone code, a passkey, single sign-on.** They do it
  in the tool's window. Then `/resume`.
- **A verification email.** They click its link in their own mail. Then
  `/resume`.
- **No account there, in a rehearsal.** `/accounts setup <employer>`, or
  `/accounts signin <employer>` to make it themselves.
